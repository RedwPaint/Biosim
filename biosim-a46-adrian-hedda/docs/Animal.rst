.. _Animal:


Animal
===================
This animal class is a superclass which contains all the animals on the island.
The ``Animal`` class contains common methods for the ``Herbivores`` and ``Carnivores`` which
are subclasses to ``Animal``.

``Herbivores`` and ``Carnivores`` have their own eat function and parameters for the set
values. Migrating, aging, weight loss, who dies, updating fitness, if they will
have children, sigma and update params are the common methods for both animals.




.. autoclass:: biosim.Animal.Animal
    :members: