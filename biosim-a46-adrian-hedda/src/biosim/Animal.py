import math
import random

class Animal:

    """
    Superclass which contains subclasses Herbivores and Carnivores.
    Animal contains functions that are relevant for each subclass
    """
    _param = {}
    @classmethod
    def set_param(cls,param_input):
        """
        the classmethod set_param takes a dictionary input, and updates the _param dictionary of
        the targeted cls

        Parameters
        ----------
        param_input = {}

        Returns the new parameter dictionary for the class.
        -------

        """
        if param_input is not None:
            cls._param.update(param_input)
            return cls._param



    def __init__(self, age=0, weight=None):
        """
        initializing animal, in this case mostly used through super().__init__ in the subclasses
        input Parameters. Age and weight are given as attributes to the class object
        ----------
        age
        weight


        """

        self.migrating = False
        self.alive = True
        self.age = age
        if age == 0:
            self.parent = False
        else:
            self.parent = True
        if weight is None:
            my, sigma = Animal.my_sigma(self)
            self.weight = random.lognormvariate(my,sigma)
        else:
            self.weight = weight
        self.fitness = 0
        self.update_fitness()


    def my_sigma(self):
        """
        my sigma calculates the parameters used in the log normal distribution that the new class
        object gets initialized from. If age and/or weight is not given, the class objects weight
        will be chosen based on this distribution.

        Returns
        -------
        my,sigma

        """
        my = math.log(self._param['w_birth'] ** 2 / (math.sqrt(self._param['w_birth'] ** 2 + self._param['sigma_birth'] ** 2)))
        sigma = math.sqrt(math.log(1 + (self._param['sigma_birth'] ** 2 / self._param['w_birth'] ** 2)))
        return my, sigma


    def update_fitness(self):
        """
        The update fitness function takes a class object and calculates its fitness value.
        This is done based on the class objects own weight and age, and parameters decided in the
        subclass parameter dictionary.

        This function also checks if the animals weight is 0 or has a negative number.
        Should this happen, the animal dies, but is not removed from the list of its kind yet.

        Updates
        -------
        class object.fitness
        class object.alive
        """
        param = self._param
        if self.weight <= 0:
            self.alive = False
            return
        else:
            q_positive = 1 / (1 + math.exp(param['phi_age'] * (self.age - param['a_half'])))
            q_negative = 1 / (1 + math.exp(-(self._param['phi_weight'] * (self.weight - self._param['w_half']))))
            self.fitness = q_positive * q_negative
        if self.fitness > 1:
            raise ValueError (f'The fitness of an animal should not exceed 1')


    def have_offspring(self, animal_list):
        """
        The have offspring function takes a class object and sees if that object is eligible to
        reproduce.
        Its eligibility is decided based on a number of factors like; its weight, its age, whether
        it has had offspring before in the same year. If all of these parameters allow for the
        object to produce offspring, then the function rolls a probability for it to do so.

        The probability parameters are decided in the class objects parameter dictionary, in
        addition to being affected by its own attributes, age and weight.

        Parameters
        ----------
        carn

        Returns
        -------
        A new animal of the same class, in the same Tile
        """
        self.update_fitness()
        if self.parent is False:
            return
        if self.weight < self._param['zeta']*(self._param['w_birth'] + self._param['sigma_birth']):
            return
        if random.random() < min(1.0, self._param['gamma']*self.fitness*len(animal_list)):
            newborn = self.__class__()
            if self.weight - (newborn.weight * self._param['xi']) > 0:
                self.weight -= (newborn.weight * self._param['xi'])
                self.parent = False
                self.update_fitness()
            return newborn
        return

    def will_migrate(self):
        """
        will migrate is a function that tests if the animal class object wants to migrate.
        Its willingness to migrate is decided by its fitness and a class parameter.

        Updates
        -------
        class object.migrating
        """
        if random.random() <= self._param['mu']*self.fitness:
            self.migrating = True

    def aging(self):
        """
        Each animal class object has an age attribute. Each year they are alive, the aging function
        increases this age by one.

        Returns
        -------
        class object.age += 1
        """
        self.age += 1
        self.update_fitness()
    def weight_loss(self):
        """
        Every year on the island, every animal loses weight.
        The amount of weight lost is decided both by the animals own weight, and its class
        parameter.

        An animal that weighs more, loses more.

        Updates
        -------
        class object.weight
        """
        self.weight -= self._param['eta'] * self.weight
        self.update_fitness()
    def dying(self):
        """
        The dying function introduces the probability for random death, and is run towards the
        end of every year.
        This function allows for the class objects alive value to be set to False.

        at the end of the year, each list of each animal gets filtrated with respect to which
        animal is still alive.
        animals with alive = False simply gets removed from their class list.

        Updates
        -------
        class object.alive
        """
        if self.weight <= 0 or random.random() <= self._param['omega'] * (1 - self.fitness):
            self.alive = False


class Herbivores(Animal):
    """
    The class Herbivores is an Animal subclass.
    This class of animals eat fodder which grows on certain landscapes(Tile subclasses).
    Every year they have access to a fresh supply of fodder, and in a randomized order eat this
    fodder.
    Each Herbivore that eats from the tiles fodder, reduces it until it reaches zero.

    Every year there is a chance the herbivore wants to migrate. Should this happen, it will
    migrate to one of its adjacent tiles in a random direction.
    """
    _param =   {'w_birth': 8.,
              'sigma_birth': 1.5,
              'beta': 0.9,
              'eta': 0.05,
              'a_half': 40.0,
              'phi_age': 0.6,
              'w_half': 10.,
              'phi_weight': 0.1,
              'mu': 0.25,
              'gamma': 0.2,
              'zeta': 3.5,
              'xi': 1.2,
              'omega': 0.4,
              'F': 10.}


    def __init__(self, age=0, weight=None):
        """
        Herbivores init function sends both of its input parameters to its parent class, Animal.

        Parameters
        ----------
        age
        weight
        """
        super().__init__(age, weight)



    def eat(self, temp_fodder):
        """
        Eat is a function that allows a Herbivore to eat fodder from the tile its in.
        The function returns an updated value for the fodder, which is dependent on the
        Herbivores parameter dictionary.

        The Herbivore parameter dictionary also informs the Herbivore on how much weight it should
        gain. If the Herbivore manages to eat its fill, it increases in weight solely dependent
        on its parameter value.

        However, should the Herbivore not have access to all the food it wants to eat, its weight
        increase will also depend on how much remaining fodder there is.

        Updates
        ----------
        temp_fodder
        Herbivore.weight
        -------

        """
        if temp_fodder == 0:
            return temp_fodder
        if temp_fodder >= self._param['F']:
            eaten = self._param['F']
            self.weight += self._param['beta']*eaten
            temp_fodder -= eaten
            self.update_fitness()
            return temp_fodder
        else:
            self.weight += self._param['beta']*temp_fodder
            temp_fodder = 0
            self.update_fitness()
            return temp_fodder

class Carnivores(Animal):
    """
    The Carnivores class is a sublcass of Animal.
    Each Carnivore is an animal that eats Herbivores, animals of another subclass, in order to
    survive.

    This sublcass shares all its attributes with the Herbivores subclass, except for its Eat
    function.
    A Carnivore class object will only eat Herbivore class objects, but based on a number of
    parameters and attributes, it might or might not be successful.
    """
    _param = {"w_birth": 6.0,
             "sigma_birth": 1.0,
             "beta": 0.75,
             "eta": 0.125,
             "a_half": 40.0,
             "phi_age": 0.3,
             "w_half": 4.0,
             "phi_weight": 0.4,
             "mu": 0.4,
             "gamma": 0.8,
             "zeta": 3.5,
             "xi": 1.1,
             "omega": 0.8,
             "F": 50.0,
             "DeltaPhiMax": 10}
    def __init__(self, age=0, weight=None):
        """
        Like the Herbivores subclass, the Carnivores also send their input parameters to its parent
        class for init

        Updates
        ----------
        Carnivore.age
        Carnivore.weight
        """
        super().__init__(age, weight)

    def eat(self, herb_list):
        """
        For a Carnivore to eat, it requires herbivores in its vicinity.
        The Carnivore class object iterates over the Herbivore list in a sorted order.
        Each instance in the list of herbivores is ranked based on the herbivores fitness.
        In order for the Carnivore to be able to eat the Herbivore; the Herbivore needs to have
        an alive = True, its fitness needs to be less than that of the carnivore.

        Should the Carnivore be able to eat a specific Herbivore, there is a probability for its
        success in eating it.

        The eating probability is determined by both the Carnivore's and the Herbivore's fitness
        values.

        Eaten Herbivores get their alive statues updated to False, so they cant be eaten by
        multiple Carnivores.

        Parameters
        ----------
        herb_list

        Returns
        -------

        """
        self.update_fitness()
        appetite = self._param['F']
        for i in herb_list:
            if i.alive is False:
                continue
            if appetite <= 0 or self.fitness <= i.fitness:
                return
            p = ((self.fitness - i.fitness) / self._param['DeltaPhiMax'])
            if appetite > 0:
                if self.fitness - i.fitness > self._param['DeltaPhiMax'] or random.random() <= p:
                    i.alive = False
                    Feed = min(appetite, i.weight)
                    appetite -= Feed
                    self.weight += self._param['beta'] * Feed
                    self.update_fitness()

                else:
                    continue