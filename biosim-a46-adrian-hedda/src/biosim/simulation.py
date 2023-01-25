"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Hans Ekkehard Plesser / NMBU
from biosim import Island
from biosim import visualization
import textwrap


class BioSim:
    """
    Top-level interface to BioSim package.
    """
    _hist_specs = {}
    _cmax_animals = {}
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_years=None, img_dir=None, img_base=None, img_fmt='png',
                 log_file=None):

        """
        Parameters
        ----------
        island_map : str
            Multi-line string specifying island geography
        ini_pop : list
            List of dictionaries specifying initial population
        seed : int
            Integer used as random number seed
        vis_years : int
            Years between visualization updates (if 0, disable graphics)
        ymax_animals : int
            Number specifying y-axis limit for graph showing animal numbers
        cmax_animals : dict
            Color-scale limits for animal densities, see below
        hist_specs : dict
            Specifications for histograms, see below
        img_years : int
            Years between visualizations saved to files (default: `vis_years`)
        img_dir : str
            Path to directory for figures
        img_base : str
            Beginning of file name for figures
        img_fmt : str
            File type for figures, e.g. 'png' or 'pdf'
        log_file : str
            If given, write animal counts to this file

        Notes
        -----
        - If `ymax_animals` is None, the y-axis limit should be adjusted automatically.
        - If `cmax_animals` is None, sensible, fixed default values should be used.
        - `cmax_animals` is a dict mapping species names to numbers, e.g.,

          .. code:: python

             {'Herbivore': 50, 'Carnivore': 20}

        - `hist_specs` is a dictionary with one entry per property for which a histogram
          shall be shown. For each property, a dictionary providing the maximum value
          and the bin width must be given, e.g.,

          .. code:: python

             {'weight': {'max': 80, 'delta': 2},
              'fitness': {'max': 1.0, 'delta': 0.05}}

          Permitted properties are 'weight', 'age', 'fitness'.
        - If `img_dir` is None, no figures are written to file.
        - Filenames are formed as

          .. code:: python

             Path(img_dir) / f'{img_base}_{img_number:05d}.{img_fmt}'

          where `img_number` are consecutive image numbers starting from 0.

        - `img_dir` and `img_base` must either be both None or both strings.
        """
        self.island = Island.Whole_map()
        self.geogr = island_map

        self.pop = ini_pop
        self.seed = seed
        self.vis_years = vis_years
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.img_years = img_years
        self.img_dir = img_dir
        self._img_base = img_base
        self.img_fmt = img_fmt
        self.log_file = log_file

        Island.Whole_map.sim_world(self.island, self.geogr)


    def set_animal_parameters(self, species, params = None):
        """
        Set parameters for animal species.

        Parameters
        ----------
        species : str
            Name of species for which parameters shall be set.
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """
        Island.animal_parameters(species, params)




    def set_landscape_parameters(self, landscape, params=None):
        """
        Set parameters for landscape type.

        Parameters
        ----------
        landscape : str
            Code letter for landscape
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """
        Island.set_landscape_param(landscape, params)



    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        Parameters
        ----------
        num_years : int
            Number of years to simulate
        """

        self.add_population(self.pop)
        self.vis = visualization.Visualize(num_years, img_dir=self.img_dir, img_base=self._img_base)

        visualization.Visualize.update_hist_specs(self.vis, self.hist_specs)
        visualization.Visualize.update_cmax_animals(self.vis, self.cmax_animals)

        visualization.Visualize.setup_figure(self.vis, self.geogr)

        for i in range(num_years):
            self.island.new_year_whole_map()    # kjører nytt år på island
            self.num_animals_dict()             # oppdaterer dict_count
            self.all_herb, self.all_carn = self.island.all_animals()
            # num_herb_tot, num_carn_tot, tot_animals = self.num_animals
            self.vis.update_figure(self.dict_count, self.all_herb, self.all_carn)





    def add_population(self, population): # Orginalt def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population : List of dictionaries
            See BioSim Task Description, Sec 3.3.3 for details.
        """
        ini_herb_list = []
        ini_carn_list = []
        loc_herb = None
        loc_carn = None
        for pop in population:
            if pop['pop'][0]['species'] == 'Herbivore':
                ini_herb_list = pop['pop']
                loc_herb = pop['loc']

            elif pop['pop'][0]['species'] == 'Carnivore':
                ini_carn_list = pop['pop']
                loc_carn = pop['loc']

        self.island.add_pop(loc_herb, loc_carn, ini_herb_list, ini_carn_list)


    @property
    def year(self):
        """Last year simulated."""
        year = self.island.year
        return year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        num_herb_tot, num_carn_tot = Island.Whole_map.animal_count_total(self.island)
        tot_animals = num_herb_tot + num_carn_tot
        return tot_animals

    def num_animals_dict(self):
        self.dict_count = self.island.animal_count_dict()


    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        num_dict = {}
        num_herb_tot, num_carn_tot = Island.Whole_map.animal_count_total(self.island)
        num_dict.update({'Herbivore':num_herb_tot})
        num_dict.update({'Carnivore': num_carn_tot})
        return num_dict

    def make_movie(self):
        self.vis.make_movie()





