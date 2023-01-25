.. _Island:


Island map
===========
In the ``Island.py`` file you have an class ``Whole_map`` which generates the map over the island.
The map consists of letters representing different terrains, and creat a dictionary with
coordinates and ``Tile`` objects. When the map is generated the tiles get assigned neighbors so
the animals in the ``Tile`` objects can migrate to their neighbor tiles.

``Whole_map`` also have a function to run the simulation for one year on the whole island. Functions
for num of animals, list of animals and dicts of animals is also in ``Whole_map``

The file ``Island.py`` have a set_landscape_param if you want to update amount of fodder or if a
terrain can have animals or not.

.. autoclass:: biosim.Island.Whole_map
    :members:

