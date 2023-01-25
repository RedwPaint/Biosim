.. _Simulation:


BioSim
========
The ``biosim`` class is generating a simulation, and contains properties to count all animal per species,
 number of animals in total and what year it is. With ``biosim`` you can also add population using
``add_population()`` after already running the simulation. The parameters for the tiles and animal
can be updated here using ``set_animal_parameters`` and ``set_landscape_parameters``.

The ``make_movie`` function calls on the make movie function in visualization.

.. autoclass:: biosim.simulation.BioSim
    :members:
