
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os



# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
# _DEFAULT_GRAPHICS_DIR = os.path.join(f'{img_dir}/{img_base}', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif

class Visualize:
    """
    the Visualize class is where pyplot gets to save its contributions to our project.
    Here the class object gets the attribute figure, which get further specifications through the
    various functions belonging to the Visualize class.
    """
    _hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}}
    _cmax_animals = {'Herbivore': 200, 'Carnivore': 50}
    def __init__(self, num_years = 400, img_dir=None, img_name=None, img_fmt=None, img_base=None):

        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            self.img_base = os.path.join(img_dir, img_name)
        else:
            self.img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None
        self._mean_line = None

        self.fig = plt.figure(figsize=(10, 10))
        self.year = 0
        self.num_years = num_years
        self.cax = {0: self.fig.add_axes([0.4, 0.4, 0.05, 0.2]),
                    1: self.fig.add_axes([0.52, 0.4, 0.05, 0.2])}

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt
        """

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self.img_base),
                                       '{}.{}'.format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self.img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1

    def update_hist_specs(self, hist_specs):
        """
        Updates the histogram parameters,
        hist_specs must be in the format:
        {'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}}
        """
        if hist_specs:
            self._hist_specs.update(hist_specs)

    def update_cmax_animals(self, cmax_animals):
        """
        This function is not used, but I would have used it to make the bar
        which shows the colors og the heatmap
        """
        if cmax_animals:
            self._cmax_animals.update(cmax_animals)

    def plot_island_map(self, island_map):
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in island_map.splitlines()]

        ax_im = self.island_ax

        ax_im.imshow(map_rgb)

        ax_im.set_xticks(range(len(map_rgb[0])))
        ax_im.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        ax_im.set_yticks(range(len(map_rgb)))
        ax_im.set_yticklabels(range(1, 1 + len(map_rgb)))

        ax_lg = self.island_ax.inset_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        ax_lg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            ax_lg.add_patch(plt.Rectangle((0.8, ix * 0.2), 0.5 , 0.1,
                                          edgecolor='none',
                                          facecolor=rgb_value[name[0]]))
            ax_lg.text(0.35, ix * 0.17, name, transform=ax_lg.transAxes)

    def plot_empty_heatmap(self, ax, map_values):
        """
        Before the figure can start looking at animals in tiles, it needs to initialize the
        heatmap. this creates a matrix with sides equal to the lenghts of the map.
        All values in this matrix is zero, and then the function plots this empty heatmap.
        These zero values are then updated in the update heatmap function.
        """
        self.matrix = np.zeros((len(map_values), len(map_values[0])))
        #self.matrix_img = None
        ax.imshow(self.matrix)
        #self.matrix_img = ax.imshow(self.matrix)



    def update_heatmap(self, ax, year_dict, species):
        """
        The update heatmap function looks at the dictionary of that year, for where animals can be
        found. This dictionary provides the amount of herbivores and carnivores given at a
        specific tile, and is accessed through the tile coordinate as key.

        the ax.clear tells the plotting to disregard the original image, and lets the update
        heatmap function change the matrix used in the original image.
        In this way the code deletes the previous image, preventing slower running code.

        """
        ax.clear()
        for key in year_dict.keys():
            self.matrix[key[0] - 1, key[1] - 1] = year_dict[key][species]


        if species == 0:
            img = ax.imshow(self.matrix, vmin=0, vmax=self._cmax_animals['Herbivore'])
        elif species == 1:
            img = ax.imshow(self.matrix, vmin=0, vmax=self._cmax_animals['Carnivore'])


        self.fig.colorbar(img, self.cax[species])

    def setup_figure(self, geogr):
        """
        The setup figure function creates the actual subplots shown when the simulation is running.
        This function give the different subplots their titles, and their initial data.
        """
        # Sette opp Island map
        self.island_ax = self.fig.add_subplot(3,3,1)
        self.island_ax.set_title('Island')
        self.plot_island_map(geogr)
        #self.fig.tight_layout(pad=1.1, w_pad=0., h_pad=1.9)


        # set up the second plot (year count)
        self.year_count = self.fig.add_subplot(3,3,2)
        self.year_count.set_title("Year: {}".format(self.year))
        self.year_count.axis('off')



        # set up the third plot (animals count)
        animal_graph = self.fig.add_subplot(3, 3, 3)
        animal_graph.set_title('Animals count')
        animal_graph.set_xlim(0, self.num_years)
        animal_graph.set_ylim(0, 12000)
        self.line_herb = animal_graph.plot(np.arange(self.num_years),
                       np.full(self.num_years, np.nan), 'b-')[0]
        self.line_carn = animal_graph.plot(np.arange(self.num_years),
                                      np.full(self.num_years, np.nan), 'r-')[0]
        animal_graph.legend(['Herbivores', 'Carnivores'])


        # HEATMAPS
        map_values = [[column for column in row]
                      for row in geogr.splitlines()]

        # Herbivore heatmap
        self.herb_heat = self.fig.add_subplot(3, 3, 4)
        self.herb_heat.set_title('Herbivores')
        self.plot_empty_heatmap(self.herb_heat, map_values)

        # Sette lengden på aksene
        self.herb_heat.set_xticks(range(len(map_values[0])))
        self.herb_heat.set_yticks(range(len(map_values)))
        # Sette tallene på aksene
        self.herb_heat.set_xticklabels(range(1, 1 + len(map_values[0])))
        self.herb_heat.set_yticklabels(range(1, 1 + len(map_values)))



        # Carnivore heatmap
        self.carn_heat = self.fig.add_subplot(3, 3, 6)
        self.carn_heat.set_title('Carnivores')
        self.plot_empty_heatmap(self.carn_heat, map_values)

        # Sette lengden på aksene
        self.carn_heat.set_xticks(range(len(map_values[0])))
        self.carn_heat.set_yticks(range(len(map_values)))
        # Sette tallene på aksene
        self.carn_heat.set_xticklabels(range(1, 1 + len(map_values[0])))
        self.carn_heat.set_yticklabels(range(1, 1 + len(map_values)))


        # BAR CHARTS
        self.bin_edges_fitness = np.arange(0,
                                           self._hist_specs['fitness']['max'] + self._hist_specs['fitness']['delta'] / 2,
                                           self._hist_specs['fitness']['delta'])
        self.bin_edges_age = np.arange(0,
                                       self._hist_specs['age']['max'] + self._hist_specs['age']['delta'] / 2,
                                       self._hist_specs['age']['delta'])
        self.bin_edges_weight = np.arange(0,
                                          self._hist_specs['weight']['max'] + self._hist_specs['weight']['delta'] / 2,
                                          self._hist_specs['weight']['delta'])

        self.fitness_bars = self.fig.add_subplot(3, 3, 7)
        self.fitness_bars.set_title("Fitness")
        hist_counts = np.zeros_like(self.bin_edges_fitness[:-1], dtype=float)
        self.hist_fit_herb = self.fitness_bars.stairs(hist_counts, self.bin_edges_fitness, color='b', lw=2)
        self.hist_fit_carn = self.fitness_bars.stairs(hist_counts, self.bin_edges_fitness, color='r', lw=2)
        self.fitness_bars.set_ylim([0, 5000])

        self.age_bars = self.fig.add_subplot(3, 3, 8)
        self.age_bars.set_title("Age")
        hist_counts = np.zeros_like(self.bin_edges_age[:-1], dtype=float)
        self.hist_age_carn = self.age_bars.stairs(hist_counts, self.bin_edges_age, color='r', lw=2)
        self.hist_age_herb = self.age_bars.stairs(hist_counts, self.bin_edges_age, color='b', lw=2)
        self.age_bars.set_ylim([0, 2000])

        self.weight_bars = self.fig.add_subplot(3, 3, 9)
        self.weight_bars.set_title("Weight")
        hist_counts = np.zeros_like(self.bin_edges_weight[:-1], dtype=float)
        self.hist_weight_carn = self.weight_bars.stairs(hist_counts, self.bin_edges_weight, color='r', lw=2)
        self.hist_weight_herb = self.weight_bars.stairs(hist_counts, self.bin_edges_weight, color='b', lw=2)
        self.weight_bars.set_ylim([0, 2000])
        plt.draw()

    def update_figure(self, year_dict, tot_herb, tot_carn):
        """
        Update figure allows for the already existing figure to be changed, without having to
        create a new figure for each year. Updating already existing figures is generally
        faster than continually creating new ones.
        """
        # UPDATE YEAR
        self.year += 1 #Flytt til slutten
        self.year_count.set_title("Year: {}".format(self.year))


        # UPDATE ANIMAL COUNT
        ydata = self.line_herb.get_ydata()
        ydata[self.year-1] = len(tot_herb)
        self.line_herb.set_ydata(ydata)

        ydata = self.line_carn.get_ydata()
        ydata[self.year-1] = len(tot_carn)
        self.line_carn.set_ydata(ydata)


        self._save_graphics(self.year)

        # UPDATE HEATMAP
        # HERBIVORES
        self.update_cmax_animals(self._cmax_animals)

        self.update_heatmap(self.herb_heat, year_dict, 0,)

        # CARNIVORES
        self.update_heatmap(self.carn_heat, year_dict,1)


        # UPDATE BAR CHARTS

        #FITNESS

        data_fitness_herb = [herb.fitness for herb in tot_herb]
        hist_counts_fitness_herb, _ = np.histogram(data_fitness_herb, self.bin_edges_fitness)
        self.hist_fit_herb.set_data(hist_counts_fitness_herb)
        data_fitness_carn = [carn.fitness for carn in tot_carn]
        hist_counts_fitness_carn, _ = np.histogram(data_fitness_carn, self.bin_edges_fitness)
        self.hist_fit_carn.set_data(hist_counts_fitness_carn)

        #AGE
        data_age_herb = [herb.age for herb in tot_herb]
        hist_counts_age_herb, _ = np.histogram(data_age_herb, self.bin_edges_age)
        self.hist_age_herb.set_data(hist_counts_age_herb)
        data_age_carn = [carn.age for carn in tot_carn]
        hist_counts_age_carn, _ = np.histogram(data_age_carn, self.bin_edges_age)
        self.hist_age_carn.set_data(hist_counts_age_carn)

        #WEIGHT
        data_weight_herb = [herb.weight for herb in tot_herb]
        hist_counts_weight_herb, _ = np.histogram(data_weight_herb, self.bin_edges_weight)
        self.hist_weight_herb.set_data(hist_counts_weight_herb)
        data_weight_carn = [carn.weight for carn in tot_carn]
        hist_counts_weight_carn, _ = np.histogram(data_weight_carn, self.bin_edges_weight)
        self.hist_weight_carn.set_data(hist_counts_weight_carn)

        plt.pause(1e-6)



