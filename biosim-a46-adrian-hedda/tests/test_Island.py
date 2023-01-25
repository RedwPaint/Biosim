import biosim.Island
#from biosim import Island
from biosim import Animal
from src.biosim import Tile
#from biosim import Plotting
import textwrap
import random


def test_create_map_dict():
    """
    The test create map dict goes through a string, and creates a dictionary with coordinates as
    keys. The value corresponding to a key is the landscape symbol from the string, in that
    position.
    """
    geogr = """\
               WW
               WW"""
    geogr = textwrap.dedent(geogr)
    test_map = biosim.Island.Whole_map()
    test_map.create_map(geogr)

    answer_map_dict = {(1,1):'W', (1,2):'W', (2,1):'W', (2,2):'W'}
    assert answer_map_dict == test_map.map_dict

def test_wrong_map_border():
    """
    Should a map string contain different landscape symbols than what is allowed, a valueerror is
    raised.
    this test will fail when testing.
    """
    geogr = """\
                   WL
                   DH"""
    geogr = textwrap.dedent(geogr)
    test_map = biosim.Island.Whole_map()
    test_map.create_map(geogr)

    assert test_map.map_dict == {}

def test_wrong_string_dimensions():
    """
    Like the previous test, this test is designed to fail, should the map string contain the
    wrong amount of lengths.
    the value error raised, tells a user which row of string contains a different amount of
    landscapes compared to the first row of symbols.
    """
    geogr = """\
                WWW
                WLWW
                WWW"""
    geogr = textwrap.dedent(geogr)
    test_map = biosim.Island.Whole_map()
    test_map.create_map(geogr)

    assert test_map.map_dict == {}


def test_generate_world():
    """
    The test for generating a world looks at the world dictionary created by the
    generate world function, and makes sure that the class objects in each coordinate is of the
    correct type.
    """
    geogr = """\
                WWW
                WLW
                WWW"""
    geogr = textwrap.dedent(geogr)
    test_map = biosim.Island.Whole_map()
    test_map.create_map(geogr)
    test_map.generate_world()
    world_map_list = [biosim.Tile.Water, biosim.Tile.Water, biosim.Tile.Water, biosim.Tile.Water, biosim.Tile.Lowland, biosim.Tile.Water,
                      biosim.Tile.Water, biosim.Tile.Water, biosim.Tile.Water]
    test_world_list = []
    for key in test_map.world.keys():
        tile = type(test_map.world[key])
        test_world_list.append(tile)

    assert world_map_list == test_world_list

def test_find_neighbors():
    """
    the find neighbors test makes sure that the tile in the middle has the correct adjacent
    neighbors.
    """
    geogr = """\
                    WWW
                    WLW
                    WWW"""
    test_map = biosim.Island.Whole_map()
    test_map.create_map(geogr)
    test_map.generate_world()
    test_map.find_neighbors()

    N_neighbor = type(test_map.world[(2,2)].N_neighbor)
    N_neighbor_postition = test_map.world[(2, 2)].N_neighbor_position
    S_neighbor = type(test_map.world[(2,2)].S_neighbor)
    S_neighbor_position = test_map.world[(2, 2)].S_neighbor_position
    E_neighbor = type(test_map.world[(2,2)].E_neighbor)
    E_neighbor_position = test_map.world[(2, 2)].E_neighbor_position
    W_neighbor = type(test_map.world[(2,2)].W_neighbor)
    W_neighbor_position = test_map.world[(2, 2)].W_neighbor_position

    test_type_list = [N_neighbor, S_neighbor, E_neighbor, W_neighbor]
    answer_type_list = [biosim.Tile.Water, biosim.Tile.Water, biosim.Tile.Water, biosim.Tile.Water]
    test_position_list = [N_neighbor_postition, S_neighbor_position, E_neighbor_position, W_neighbor_position]
    answer_position_list =['(2, 1)', '(2, 3)', '(3, 2)', '(1, 2)']

    assert test_type_list == answer_type_list and test_position_list == answer_position_list

def test_migrate_all_animals(): #må gjøres statistisk
    """
    This is an incomplete test, intended to look at the statistical result of animals, who all
    want to migrate. The intent was to see if the amount of animals who migrated from one tile
    to another was within the acceptable realm of probability.
    """
    geogr = """\
                    WWWW
                    WLLW
                    WWWW"""
    test_map = biosim.Island.Whole_map()
    test_map.create_map(geogr)
    test_map.generate_world()

def test_new_year_island():
    """
    Each year simulated increases the island year count as well.
    this test checks that the island's year count increases at the correct pace.
    """
    geogr = """\
                   WWW
                   WDW
                   WWW"""
    test_map = biosim.Island.Whole_map()
    test_map.create_map(geogr)
    test_map.generate_world()
    for i in range(10):
        test_map.new_year_whole_map()

    assert test_map.year == 10

def test_count_animals():
    """
    It is valuable to know how many animals are on the island.
    this test goes tile by tile and counts the herbivores and carnivores in all the tiles.
    """
    geogr = """\
                       WWW
                       WDW
                       WWW"""

    herb = []
    carn = []
    for i in range(10):
        herb_i = Animal.Herbivores()
        carn_i = Animal.Carnivores()
        herb.append(herb_i)
        carn.append(carn_i)

    test_map = biosim.Island.Whole_map()
    test_map.create_map(geogr)
    test_map.generate_world()
    for key in test_map.world.keys():
        test_map.world[key].add_pop(herb, carn)

    tot_herb, tot_carn = test_map.animal_count_total()
    #tot_herb = len(tot_herb_list)
    #tot_carn = len(tot_carn_list)

    assert tot_carn and tot_herb == 90

