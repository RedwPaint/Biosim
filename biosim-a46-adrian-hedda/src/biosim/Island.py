import random
import textwrap
from biosim import Tile

class Whole_map():
    """
    Whole map is a class for creating both a map over the Island and to tie the coordinates
    to actual Tiles in dictionaries.
    The class object has a few attributes that are put in place to make sure the world generated
    follows the rules of the simualtion.

    For example, if one tries to create a world that contains a new landscape type, that is not
    already among the accepted landscapes, the Whole_map functions will not accept it.
    We had plans to give users the ability to easily add more landscapes, but didnt get that far.

    """
    _landscapes = ['W', 'L', 'H', 'D']

    def __init__(self):
        self.map_dict = {}
        self.default_tiles = True
        self.year = 0

    def create_map(self, map_layout_string):
        """
        create map is a function that updates a dictionary with coordinates as keys, and landscapes
        as values.
        This is done in order for the Whole_map class to be easily capable of going to a specific
        type of tile in its functions, skipping ones of the wrong landscape.

        It also allows users to check the dict_map, with keys equal to the coordinates for tiles
        the user is interested in.
        An example would be dict_map[(2,2)], which would return the letter associated with a
        type of landscape.

        Parameters:

        map_layout_string

        Updates:

        dict_map
        """
        #map_layout_string = textwrap.dedent(map_layout_string)
        map_string_lines = map_layout_string.splitlines()
        # map_string_lines = enumerate(map_string_lines)
        self.map_dict = {}
        i = 0
        self.length_y = len(map_string_lines)
        for line in map_string_lines:
            map_string_lines[i] = [landscape for landscape in line]

            for landscape in map_string_lines[i]:
                if landscape not in self._landscapes: #Flytt til test
                    self.default_tiles = False
                    raise ValueError(f'Landscape:', landscape,', is not in the list of default landscapes')

            i += 1
        self.length_x = len(map_string_lines[0])  # assumes that all the lists of landscapes have the same length
        if self.default_tiles is True:
            for i in range(self.length_y):
                y = i + 1
                if i == 0:
                    for landscape in map_string_lines[i]:
                        if landscape != 'W':
                            raise ValueError(f'First and last lines are borders, and must only contain water, W')

                if i == self.length_y - 1:
                    for landscape in map_string_lines[i]:
                        if landscape != 'W':
                            raise ValueError(f'First and last lines are borders, and must only contain water, W')

                if len(map_string_lines[i]) != self.length_x:
                    self.map_dict = {}
                    raise ValueError(f'Map must contain uniform string lenghts. Row: ', i+1, 'does not contain the same number of symbols as the first line')

                for j in range(self.length_x):
                    x = j + 1
                    #loc = str(x) + ',' + str(y)
                    self.map_dict.update({(y, x): map_string_lines[i][j]})
        else:
            print('Map string contains landscapes not included in the simulation')

    def generate_world(self):
        """
        Having run the create map to update the map dictionary gives a user the ability to
        generate a world.
        By using the same layout as the map dictionary, coordinates becomes keys in a new
        dictionary, but the values become tile class objects.
        These tiles allow for animals to be interacted with.
        Examples of this is Herbivores eating the fodder avilable in a specific tile, or
        Animals migrating to adjacent tiles.

        The coordinate keys allow for easy access in functions, testing and debugging.
        A key input in the world dictionary will return the class object itself, allowing further
        inspection.
        Returns


        """

        if self.map_dict == {}:
            print('Map dictionary did not get created, please generate map from a valid string')
            return
        self.world = {}
        keys = self.map_dict.keys()
        for key in keys:
            if self.map_dict[key] == 'W':
                self.world.update({key:Tile.Water()})
            if self.map_dict[key] == 'L':
                self.world.update({key: Tile.Lowland()})
            if self.map_dict[key] == 'H':
                self.world.update({key: Tile.Highland()})
            if self.map_dict[key] == 'D':
                self.world.update({key:Tile.Desert()})
        self.find_neighbors()
        return self.world

    def sim_world(self, map_string):
        """
        The sim world function combines the create map and generate world functions.
        When Island.py is imported to run simulations, the sim world combination allows for
        fewer lines of code.

        Parameters

        map_string

        Returns

        map dictionary
        world dictionary
        """
        self.create_map(map_string)
        self.generate_world()

    def find_neighbors(self):
        """
        When the world gets generated, the find neighbors function is called.
        This function allows for each tile that is not Water to know their adjacent neighbors.
        Each tile is then capable of giving migrating animals their destination options.
        This saves some time compared to the neighbors of a tile being found each time an animal
        wants to migrate.

        Updates

        Tile adjacent neighbors
        """
        # goes through each tile that is not water, and adds neighbor info to tiles
        keys = self.map_dict.keys()
        for key in keys:
            if self.map_dict[key] == 'W':
                continue
            key0 = key[0]
            key1 = key[1]
            self.world[key].N_neighbor_position = str((key0, key1 - 1))
            self.world[key].N_neighbor = self.world[(key0, key1 - 1)]
            self.world[key].S_neighbor_position = str((key0, key1 + 1))
            self.world[key].S_neighbor = self.world[(key0, key1 + 1)]
            self.world[key].E_neighbor_position = str((key0 + 1, key1))
            self.world[key].E_neighbor = self.world[(key0 + 1, key1)]
            self.world[key].W_neighbor_position = str((key0 -1, key1))
            self.world[key].W_neighbor = self.world[(key0 - 1, key1)]

    def migrate(self):
        """
        If an animal wants to migrate, it must go through the Whole map class migrate function.
        This function iterates over keys in the map dict, which goes through all tiles that do
        not belong to the subclass Water.

        Any tile belonging to any other landscape can send their migrating Animals to neighboring
        tiles.

        Updates

        removes migrating animals from tiles
        adds migrating animals to destination tiles
        """
        # goes through each tile and migrates animals that already want to migrate
        keys = self.map_dict.keys()
        for key in keys:
            N = self.world[key].N_neighbor
            S = self.world[key].S_neighbor
            E = self.world[key].E_neighbor
            W = self.world[key].W_neighbor

            if self.map_dict[key] == 'W':
                continue
            if len(self.world[key].carn) != 0:

                migrating_carn_list = [i for i in self.world[key].carn if
                                       i.migrating is True and i.alive is True]

                for i in migrating_carn_list:
                    destination = random.choice([N, S, E, W])
                    if destination.accepts_animals is True:
                        i.migrating = False
                        destination.carn.append(i)
                        self.world[key].carn.remove(i)

            if len(self.world[key].herb) != 0:
                migrating_herb_list = [i for i in self.world[key].herb if
                                       i.migrating is True and i.alive is True]

                for i in migrating_herb_list:
                    destination = random.choice([N, S, E, W])
                    if destination.accepts_animals is True:
                        i.migrating = False
                        destination.herb.append(i)
                        self.world[key].herb.remove(i)

    def new_year_whole_map(self):
        """
        The many functions that animals can run are meant to run happen once a year.
        Every animal belongs to a specific tile, and every tile has a place in our map.

        The new year whole map function, allows for every tile to run all its animals through one
        years worth of actions.

        Because of the order described in the anual cycle of our island, the tiles has to be
        iterated over two times.
        This is because of the animals migration period, where each animal that has decided to
        migrate, leaves its original tile behind, and moves to one of the adjacent neighbor tiles.

        After the migration, the tiles finish their individual processes, and ends with giving the
        map class object its increase in self.year.

        Updates

        All tiles run their animals through one years worth of functions.
        """
        # goes through each tile, and runs new year function on each
        for key in self.map_dict:
            self.world[key].tile_have_offspring()
            self.world[key].tile_eat()
            self.world[key].tile_will_migrate()
        self.migrate()
        for key in self.map_dict:
            self.world[key].tile_aging()
            self.world[key].tile_weight_loss()
            self.world[key].tile_dying()
            self.world[key].tile_reset_parent()

        self.year += 1

    def add_pop(self,key_herb,key_carn,herb_list, carn_list):
        """
        Adding a population of animals is required in order for the anual cycle to do anything of
        interest.
        The add pop function allows for adding Herbivores and/or Carnivores to any coordinate.
        At present, the function allows for adding animals to Water tiles, which is regrettable.

        Parameters

        key herb
        key carn
        herb list
        carn list

        Returns
        -------

        """
        #adds a population of herbs and carns to a tile "key"
        if key_herb is not None:
            self.world[key_herb].add_pop_tile_herb(herb_list)
        if key_carn is not None:
            self.world[key_carn].add_pop_tile_carn(carn_list)

    def all_animals(self):
        """
        At different points, it will be useful to be able to interact with every animal present on
        the island.
        The all animals function goes over every tile on the island, and adds each tile's animals
        to two lists. One for each species.
        These lists contain class objects, that allow for further interaction.

        Returns
        -------
        class object lists
        """
        #returns class objects
        all_herb = []
        all_carn = []
        for key in self.world.keys():
            all_herb.extend(self.world[key].herb)
            all_carn.extend(self.world[key].carn)

        return all_herb, all_carn

    def animal_count_total(self):
        """
        The animal count total function iterates through every tile on the island, and returns
        the total amount of herbivores and the total amount of carnivores present on the island.
        The two returns are integers.

        Returns
        -------
        integer of total amount of Herbivores on the island
        integer of total amount of Carnivores on the island
        """
        # returns number of herbs and carns on island
        temp_count_herb = 0
        temp_count_carn = 0
        for key in self.map_dict.keys():
            temp_herb, temp_carn = self.world[key].count_animals()
            temp_count_herb += temp_herb
            temp_count_carn += temp_carn

        return temp_count_herb, temp_count_carn

    def animal_count_dict(self):
        """
        In certain instances it might be useful to know which tile has which number of which kind
        of animal.
        Such a detailed overview is made through the animal count dict function.

        This function iterates over every tile in the map, and counts each animal belonging to that
        tile.
        The resulting dictionary allows for interesting plotting capabilities, such as heatmaps.

        Returns
        -------
        Dictionary overview of animals belonging to tiles by coordinates
        """
        # returns dictionary that explains the number of herbs and carns in each tile
        count_dict = {}
        for key in self.map_dict.keys():
            temp_herb, temp_carn = self.world[key].count_animals()
            count_dict.update({key:[temp_herb, temp_carn]})

        return count_dict


def animal_parameters(species, param = None):
    """
    A user might be interested in changing specific parameters that influence a species of animal.
    The animal parameters function delivers the parameter and species to the Tile file, which in
    turn updates the parameter dictionary of the species in question.
    Parameters
    ----------
    species
    param

    Returns
    -------
    string that describes which species got its parameters updated, or if anything went wrong
    """
    Tile.set_animal_param(species, param)


def set_landscape_param(landscape, param = None):
    """
    A user might be interested in changing specific parameters of a kind of landscape.
    The set landscape parameters function uses the tile classmethod set param to update the
    parameters of the landscape in question, with the parameter dictionary used in the input.

    Parameters
    ----------
    landscape
    param

    Returns
    -------
    string that describes which landscape got its parameters updated, or if anything went wrong
    """
    if param is None:
        answer_string = "Parameter input is empty. No parameter was updated"
        return answer_string

    if landscape =='W':
        Tile.Water.set_param(param)
        answer_string = "Water parameters have been updated"

    if landscape == 'L':
        Tile.Lowland.set_param(param)
        answer_string = "Lowland parameters have been updated"

    if landscape =='H':
        Tile.Highland.set_param(param)
        answer_string = "Highland parameters have been updated"

    if landscape =='D':
        Tile.Desert.set_param(param)
        answer_string = "Desert parameters have been updated"

    return answer_string


if __name__ == "__main__":

    print('Nothing to see here')
