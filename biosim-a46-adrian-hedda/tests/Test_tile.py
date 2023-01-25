from biosim import Tile


ini_herbs = [{'loc': (2, 7),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(200)]}]

ini_herbs = ini_herbs[0]['pop']

ini_carns = [{'loc': (2, 7),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]

ini_carns = ini_carns[0]['pop']

test_tile = Tile.Lowland()

def test_add_pop_tile_herb_and_count():
    """
    Tests the adding of a herbivore population to a tile, and counts them.
    """
    Tile.Lowland.add_pop_tile_herb(test_tile, ini_herbs)
    test_tile_herbs, test_tile_carns = Tile.Lowland.count_animals(test_tile)
    assert test_tile_herbs == 200 and test_tile_carns == 0

def test_add_pop_tile_carn_and_count():
    """
    Tests the adding of a carnivore population to a tile, and counts them.
    """
    Tile.Lowland.add_pop_tile_carn(test_tile, ini_carns)
    test_tile_herbs, test_tile_carns = Tile.Lowland.count_animals(test_tile)
    assert test_tile_herbs == 0 and test_tile_carns == 50


def test_set_param():
    """
    Should a user want to change the parameter of a landscape, this test make sure that the
    set param function works as intended.
    """
    test_tile.set_param({'Fodder':100})
    test_tile.set_fodder()
    assert test_tile.Fodder == 100

