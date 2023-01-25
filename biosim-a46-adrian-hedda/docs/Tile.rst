.. _Tile:


Tile
=====
The Tile class is a superclass which contains all actions for one single tile on a map.
A tile contains a population of herbivores and carnivores, where the class fuctions call
on the functions from ``Animal`` and run them on every animal in that tile.

``Tile`` is a superclass with 4 subclasses ``Water``, ``Desert``, ``Lowland`` and ``Highland``
which describes the type of terrain on the tile. The subclasses contains parameters for available
fodder and if the animals can be on that tile. Animals can not be on water tiles.

The file also contains a set_animal_param function to change the params for all the animals in the tile.


.. autoclass:: biosim.Tile.Tile
    :members: