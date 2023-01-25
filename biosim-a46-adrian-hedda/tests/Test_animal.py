from biosim import Animal
import math
import numpy as np
from scipy.stats import ttest_ind

# Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests
ALPHA = 0.01  # significance level for statistical tests

def test_age_increase():
    """
    Every year the animals get older.
    This tests that over the number of years specified. the animal gets that amount of years
    older.
    """
    num_years = 20
    carn = Animal.Carnivores()
    for _ in range(num_years):
        carn.aging()
    assert carn.age == num_years

def test_weight_loss():
    """
    Like the age increase test, this tests that an animal loses the exact weight specified in its
    lose weight function over many years.
    """
    num_years = 5
    start_weight = 50
    carn = Animal.Carnivores(1, start_weight)
    for _ in range(num_years):
        carn.weight_loss()

    assert round(carn.weight) == round(start_weight*(1 - Animal.Carnivores._param['eta'])**num_years)

def test_update_fitness_nonzero():
    """
    The update fitness nonzero test asserts that when a new animal is made with specified age and
    weight. That animals update fitness function gives that animal the correct fitness attribute
    value.
    """
    weight = 10
    age = 20
    carn = Animal.Carnivores(age,weight)
    q_positive = 1 / (1 + math.exp(Animal.Carnivores._param['phi_age'] * (age - Animal.Carnivores._param['a_half'])))
    q_negative = 1 / (1 + math.exp(-(Animal.Carnivores._param['phi_weight'] * (weight - Animal.Carnivores._param['w_half']))))

    assert carn.fitness == q_positive*q_negative

def test_fitness_weight_zero_kills_carn():
    """
    To make sure that an animal dies should its weight reach zero, this test checks that the animal
    has an alive attribute set to false.
    """
    weight = 0
    age = 10
    carn = Animal.Carnivores(age, weight)
    assert carn.alive is False

def test_carn_eats_herb():
    """
    The carnivores eat function allows it to eat herbivores dependent on its own and the herbivores
    fitness values.
    This tests checks that the carnivore can only eat the animals it has a chance to eat, after
    having altered the chance of eating an animal it can it to certain.
    """
    param_new = {'DeltaPhiMax':0.1}
    herb = [Animal.Herbivores(100,5), Animal.Herbivores(1,500), Animal.Herbivores(1,500)]
    herb_weight = herb[0].weight
    carn = Animal.Carnivores(1,50)
    carn.set_param(param_new)
    carn.eat(herb)
    herb = [i for i in herb if i.alive is True]

    assert len(herb) ==2 and carn._param['DeltaPhiMax'] == 0.1 and carn.weight == (50 + 0.75*herb_weight)

def test_eat_weightgain():
    """
    Animals that eat change their weight.
    This test makes sure that an animals weight increase is equal to the amount specified in that
    animals parameter dictionary.
    """
    herb = [Animal.Herbivores(100,50),Animal.Herbivores(100,30), Animal.Herbivores(1,150), Animal.Herbivores(50,50)]
    herb1_weight = 50
    carn = Animal.Carnivores(3,200)
    carn_weight = 200
    param = {'DeltaPhiMax': 0.1}
    carn.set_param(param)
    carn.eat(herb)
    assert carn.weight == (carn_weight + carn._param['beta']*herb1_weight)

def test_herb_zero_food():
    """
    Should a herbivore be in a tile where there is no food, it should starve.
    this test makes sure that a specific herbivore that eats zero food does not gain weight.
    """
    herb = Animal.Herbivores()
    before = herb.weight
    herb.eat(0)
    after = herb.weight
    assert before == after

def test_herb_eat_food():
    """
    This test checks both that the herbivore gains weight according to its parameter dictionary,
    over the course of the specified amount of years.
    In addition, it makes sure that the remaining food changes with the amount eaten by the
    herbivore.
    """
    herb = Animal.Herbivores(5,20)
    years = 10
    for i in range(years):
        food = 15
        food = herb.eat(food)

    end_weight = 20 + (0.9*10*years)
    assert food == 5 and herb.weight == end_weight

def test_herb_eats_rest_of_food():
    """
    Should a herbivore find itself in a situation where there is food, but not enough to fill its
    appetite. The herbivore should eat the remaining food, and gain the weight of the eaten fodder.
    In our simulation, there does not seem to be a case where herbivores actually get to eat less
    than their appetite when they do get to eat, but this proves that our herbivore eat function
    functions as intended.
    """
    food_ini = 5
    herb = Animal.Herbivores(5,20)
    start_weight = herb.weight
    food_end = herb.eat(food_ini)
    assert food_end == 0 and herb.weight == (start_weight+ Animal.Herbivores._param['beta'] * food_ini)

def test_fitness_greater_than_one():
    """
    Should an animals fitness be greater than one, the update fitness function should raise a
    value error.
    This test creates 1000 herbivores, and through its initialization update each herbivores
    fitness. Should any of these have a fitness of greater than one, the value error will be
    raised.
    """
    herb = []
    for _ in range(1000):
        herb.append(Animal.Herbivores())
    #herb[1].fitness = 1.2 #manuelt overskrider grensen
    for i in herb:
        assert i.fitness <= 1

def test_dying_with_weight_zero_herb():
    """
    Exactly like the test for killing carnivores at weight zero, this test checks that should a
    herbivore reach weight = zero, that herbivore dies.
    """
    herb = Animal.Herbivores(2,0)
    herb.dying()
    assert herb.alive is False


def test_dying_with_probability():
    """
    This test checks in a roundabout way if the probability for dying as specified in the
    animal functions manifests in our code.
    it is not what we call a statistical test, and is therefore not what we wanted to use
    for this kind of testing.
    the test however, runs fine, but slow.
    """
    num_simulations = 3000000
    herb = []
    for _ in range(num_simulations):
        herb.append(Animal.Herbivores(5,20))
    old_n = len(herb)
    for i in herb:
        i.dying()

    herb = [i for i in herb if i.alive is False]
    new_n = len(herb)
    ratio = round(new_n/old_n, 3)
    prob = round(Animal.Herbivores._param['omega'] * (1-herb[1].fitness), 3)
    assert ratio == prob


def test_herb_age_zero_or_underweight_infertile():
    """
    Should an animal be a "newborn" or "underweight", it can not reproduce.
    this test checks if animals that do not fit the criteria for creating offspring, are unable to
    do so, and that none of them actually reproduce.
    """
    herb=[]
    herb1 = Animal.Herbivores(0,40)
    for i in range(10000):
        herb_i = Animal.Herbivores(1, 20)
        herb.append(herb_i)
    herb.append(herb1)

    for i in herb:
        i.have_offspring(herb)
    length = len(herb)
    assert herb1.parent is False and length == 10001

def test_offspring_with_probability():
    """
    Similarly to the dying with probability test, this test is also not a statistical test.
    the test offspring with probability looks at how many newborns get created when the probability
    for them being created is known.
    """
    num_simulations = 6000
    success = 0
    herb_test = Animal.Herbivores(5, 35)
    for _ in range(num_simulations):
        herb = []
        newborn_list = []

        n_animals = 3
        for i in range(n_animals):
            herb.append(Animal.Herbivores(5,35))
        old_n = len(herb)
        for i in herb:
            newborn = i.have_offspring(herb)
            if newborn is not None:
                newborn_list.append(newborn)
        n_success = len(newborn_list)
        herb.extend(newborn_list)
        new_n = len(herb)
        success += n_success

    ratio = success/(n_animals*num_simulations)
    ratio = round(ratio,2)
    prob = round((Animal.Herbivores._param['gamma'] * herb_test.fitness * n_animals), 2)
    assert ratio == prob

def test_offspring_with_probability_2():
    """
    The offspring with probability 2 test is not a completed test. It is intended to become
    a statistical test, that decreases the runtime of the test, and allows for a more accurate
    interpetation of the result.
    """
    num_simulations = 6000
    lengths = []
    herb_test = Animal.Herbivores(5, 35)
    for _ in range(num_simulations):
        herb = []
        newborn_list = []

        n_animals = 3
        for i in range(n_animals):
            herb.append(Animal.Herbivores(5,35))

        for i in herb:
            newborn = i.have_offspring(herb)
            if newborn is not None:
                newborn_list.append(newborn)
        lengths.append(len(newborn_list))
        herb.extend(newborn_list)


    b_mean = np.mean(lengths)
    b_std = np.std(lengths)

    expected = 1.65
    res = ttest_ind(expected, b_mean)
    #ratio = round(ratio,2)
    prob = round((Animal.Herbivores._param['gamma'] * herb_test.fitness * n_animals), 2)
    assert 3*prob == res