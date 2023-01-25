import random
from biosim import Animal


class Tile:
    """
    The Tile class is the parent class of the landscapes used in the simulation. Each tile has the
    innate ability to hold Herbivores and Carnivores in lists.
    In addition, the tiles has a start value of None for adjacent neighbors, wich get updated once
    the world is generated from a map dictionary.
    Once updated, the adjacent neighbor values allows for interaction between tiles for sending and
    receiving migrating animals.
    """
    _param = {}

    def add_pop_tile_herb(self, herb_list):
        """
        the add pop tile herb function takes a list of dictionaries, converts the entries into
        class objects, and adds these to the specific tile.
        The class object gets its age and weight from the dictionary.

        An improvement to be made later might be to allow the addition of new herbivores without
        setting the tiles herbivore list to empty first.

        Parameters
        ----------
        herb_list

        Updates
        -------
        The herbivore list belonging to a specific tile
        """
        self.herb = []
        if herb_list is not None:
            x = 0
            for _ in herb_list:
                herb_i = Animal.Herbivores(herb_list[x]['age'], herb_list[x]['weight'])
                self.herb.append(herb_i)
                x += 1

    def add_pop_tile_carn(self, carn_list):
        """
        Exactly like the add pop tile herb, the add pop tile carn takes a specific tile, and adds
        class objects Carnivores based on a list of dictionaries.

        Parameters
        ----------
        carn_list

        Returns
        -------
        Carnivore class objects belonging to the carnicore list of a specific tile.
        """
        self.carn = []
        if carn_list is not None:
            x = 0
            for _ in carn_list:
                carn_i = Animal.Carnivores(carn_list[x]['age'], carn_list[x]['weight'])
                self.carn.append(carn_i)
                x += 1

    def tile_have_offspring(self):
        """
        tile have offspring is the first function to be run in a new year in the anual cycle on
        the island.
        This function iterates through every herbivore in the herb list belonging to the tile, and
        likewise for the carnivores.

        The have offspring function is then sent to the Animal.py which goes further into detail,
        working with each animal.

        Returns
        -------
        extends tiles animal lists with newborns of both species
        """
        # Herbivores have offspring
        newborn_list_herb = []
        for i in self.herb:
            newborn = i.have_offspring(self.herb)
            if newborn is not None:
                newborn_list_herb.append(newborn)
        self.herb.extend(newborn_list_herb)

        # Carnivores have offspring
        newborn_list_carn = []
        for i in self.carn:
            newborn = i.have_offspring(self.carn)
            if newborn is not None:
                newborn_list_carn.append(newborn)
        self.carn.extend(newborn_list_carn)

    def tile_eat(self):
        """
        The second yearly task of animals is to eat.
        the tile eat function iterates over every animal belonging to that tile, and tells it to
        conduct its eat function.
        Further description in the Animal.py file.

        It is important to note that the sorting and shuffling of animal lists happen here.
        the Herbivores eat in random order, while the Carnivore are sorted from most fit to least
        and eat the Herbivores of least fitness first, and will attempt to eat Herbivores of
        increasing fitness as their appetite dictates them to try.

        Returns
        -------

        """
        ini_Fodder = self._param['Fodder']
        self.Fodder = ini_Fodder

        # Harbivores eat in random order
        random.shuffle(self.herb)
        for i in self.herb:
            self.Fodder = i.eat(self.Fodder)

        # Carnivores eat in order of the highest fitness,
        # and hunting prey in order of the lowest fitness
        self.herb.sort(key=lambda x: x.fitness)
        self.carn.sort(key=lambda x: x.fitness, reverse=True)
        for i in self.carn:
            i.eat(self.herb)

    def tile_will_migrate(self):
        """
        The tile will migrate is the third function in the anual cycle.
        This function iterates over every animal in a specific tile, and tells it to check
        if it wants to migrate, through its will migrate function.
        the will migrate function is described in Animal.py

        Returns
        -------
        updated will migrate values for class objects belonging to the tile
        """
        for herb in self.herb:
            herb.will_migrate()
        for carn in self.carn:
            carn.will_migrate()

    def tile_aging(self):
        """
        After migration is the time for aging.
        the tile aging function tells every animal in the tile to increase its age by 1.

        Updates
        -------
        Animals age attribute
        """
        for herb in self.herb:
            herb.aging()
        for carn in self.carn:
            carn.aging()

    def tile_weight_loss(self):
        """
        the tile weight loss is the second to last function in the anual cycle.
        It tells every animal in a tile to lose weight dependant on its own weight loss function.
        Further description in the Animal.py file.

        Updates
        -------
        Animals weight attribute
        """
        for herb in self.herb:
            herb.weight_loss()
        for carn in self.carn:
            carn.weight_loss()

    def tile_dying(self):
        """
        The final function in the anual cycle.
        tile dying iterates over a specific tiles animals, and tells them to execute their dying
        function, which given a species specific probability might tell the animal to die.
        Further description in the Animal.py

        This function also updates the lists of Herbivores and Carnivores belonging to a tile.
        The updated lists only include those animals that survived the year.

        The dead animals are not saved anywhere in this version of the simulation, but could easily
        be added to a graveyard list in future updates.

        Returns
        -------
        new animal lists for herbivores and carnivores belonging to the specific tile
        """
        for herb in self.herb:
            herb.dying()
        self.herb = [i for i in self.herb if i.alive is True]
        for carn in self.carn:
            carn.dying()
        self.carn = [i for i in self.carn if i.alive is True]

    def tile_reset_parent(self):
        """
        In addition the the anual cycle, we decided on a safety net for our animals, to ensure that
        no animal might give birth to offspring twice in one year.
        The animal.parent attribute gets set to False if the age of the animal is 0, as in newborns,
        or the animal gives birth to offspring.

        Therefore, after the year has concluded, every live animal can have their parent value set
        to True. Since all newborns will at this point have turned a year old, and the animals
        that already have produced offspring should be capable of creating new offspring, next year.

        Updates
        -------
        animals parent attribute
        """
        # Reset parent to True so they can have offspring next year
        for herb in self.herb:
            herb.parent = True
        for carn in self.carn:
            carn.parent = True

    @classmethod
    def set_param(cls,param_input):
        """
        the classmethod for updating the tile parameters, set param, is primarily used to update
        the landscape parameters.
        A user might want to change to Fodder values of a landscape, or whether or not a landscape
        accepts animals. These two paramters will have huge implications on how the simulation
        of the island evolves over the years.

        Parameters
        ----------
        param_input

        Returns
        -------
        the new class parameters
        """
        cls._param.update(param_input)
        return cls._param

    def count_animals(self):
        """
        count animals is a Tile function that allows a tile to count the number of Herbivores and
        the number of Carnivores that belongs to the tile.

        Returns
        -------
        integers with number of herbivores and number of carnivores in a tile
        """
        self.num_herb = len(self.herb)
        self.num_carn = len(self.carn)
        return self.num_herb, self.num_carn

    def set_fodder(self):
        """
        the set fodder tile function is an initialization function that sets the fodder in a tile
        before the Herbivores start eating. The fodder is set from the landscapes parameter
        dictionary, and is changeable through the set parameter classmethod.

        Returns
        -------

        """
        ini_Fodder = self._param['Fodder']
        self.Fodder = ini_Fodder
        return ini_Fodder

    def __init__(self):
        """
        the tile init sets initial herbivore and carnivore lists to empty lists, and adjacent
        neighbors to None.
        """
        self.N_neighbor_position = None
        self.N_neighbor = None
        self.S_neighbor_position = None
        self.S_neighbor = None
        self.W_neighbor_position = None
        self.W_neighbor = None
        self.E_neighbor_position = None
        self.E_neighbor = None
        self.carn = []
        self.herb = []


class Lowland(Tile):
    """
    the subclass Lowland is thought of as the landscape with lush vegitation in this simulation.
    it has the largest amount of fodder in its default value. Herbivores, and by extention
    Carnivores, should thrive here.
    """
    _param = {'Accepts_animals': True, 'Fodder': 800}
    def __init__(self):
        super().__init__()
        self.accepts_animals = True


class Highland(Tile):
    """
    the tile subclass Highland is less accommodating than the Lowland subclass in its default
    fodder setting. The lower fodder amount allows for far fewer Herbivores to eat their fill,
    leading to lower average weightgain for its inhabiting Herbivores.
    This lower weight gain has many implications for how the simulation evolves.
    """
    _param = {'Accepts_animals': True, 'Fodder': 400}
    def __init__(self):
        super().__init__()
        self.accepts_animals = True


class Desert(Tile):
    """
    tile subclass Desert is a hazardous place for Herbivores to live. The default fodder is set to
    zero, meaning the fintess of a Herbivore living in the desert can only decrease.
    Carnivores might still find food to eat, supposing the herbivores in the desert arent all dead
    already.
    """
    _param = {'Accepts_animals': True, 'Fodder': 0}
    def __init__(self):
        super().__init__()
        self.accepts_animals = True


class Water(Tile):
    """
    the water sublcass is the barrier that contains the animals on the island.
    should the animals learn to swim, the programmers will have to learn to fish out of bounds.
    """
    _param = {'Accepts_animals': False, 'Fodder': 0}
    def __init__(self):
        super().__init__()
        self.accepts_animals = False


def set_animal_param(species, param = None):
    """
    set animal param is a function to update the parameters of the target species.
    If a user wants to update 'Herbivores' beta value to 9.5, the param dictionary input will be:
    param = {'beta':9.5}

    Parameters
    ----------
    species
    param

    Returns
    -------
    string explaining the action taken by the function
    """
    if param is None:
        return
    if species =='Herbivore':
        Animal.Herbivores.set_param(param)

    if species == 'Carnivore':
        Animal.Carnivores.set_param(param)