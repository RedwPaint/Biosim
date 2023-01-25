import random
import scipy.stats as stats
from biosim import Island
import time
import Tile
from biosim import Animal
#import Plotting
#import random
import numpy as np


geogr = """\
            WWWWWWWWWWW
            WDDDDDDDDDW
            WDDDDDDDDDW
            WDDLLLLLDDW
            WDDLLLLLDDW
            WDDLLLLLDDW
            WDDLLLLLDDW
            WDDLLLLLDDW
            WDDLLLLLDDW
            WDDDDDDDDDW
            WWWWWWWWWWW"""


test_map = Island.Whole_map()
test_map.create_map(geogr)
test_map.generate_world()

herb = []
carn = []
for i in range (100):
    herb.append(Animal.Herbivores())

for i in range (10):
    carn.append(Animal.Carnivores())
#for i in range (50):
#    carn.append(Animal.Carnivores())

#print(test_map.world[(2,3)])
test_map.add_pop((6,6),herb,carn)
#print(test_map.world[(2,3)].carn)
#test_map.world[(2,4)].add_pop(herb,carn)
#Plotting.plot_heatmap(test_map)

#print(len(test_map.world[2,4].herb))
#print(test_map.world[(2,3)].N_neighbor)

# st = time.time()
#
# test_map.new_year_whole_map()
# for i in range(1000):
#     #print(len(test_map.world[(6, 6)].herb), len(test_map.world[(6, 6)].carn))
#     test_map.new_year_whole_map()
#     # for key in test_map.map_dict.keys():
#     #     for i in test_map.world[key].herb:
#     #         i.migrating = True
#     #     for i in test_map.world[key].carn:
#     #         i.migrating = True
#
# et = time.time()
# tid = et - st
# print(tid)
# tot_herb = 0
# i = 81
# for key in test_map.map_dict.keys():
#     herb_count = len(test_map.world[key].herb)
#     tot_herb += herb_count
#
#
# herb_ave = tot_herb / i
# print(herb_ave)
#
# all_herb, all_carn = test_map.animal_count_list()

# all_carn = test_map.animal_count_dict()
# matrix = np.zeros((10,10))
# matrix[2,2] = 1
# print(all_carn)
#
# print(all_carn[(2,2)][1])


#print(len(test_map.world[(6,6)].herb),len(test_map.world[(6,6)].carn))
#print(len(test_map.world[(6,7)].herb),len(test_map.world[(6,7)].carn))

#destination = random.choice(['N', 'S', 'E', 'W'])
#print(destination)

# summ = 0
# for i in range(100000):
#     summ += random.choice([1,2,3,4])
#
# print(summ)

#
# for key, values in ini_carns.items():
#     for i in values:
#         print(key, " : ", i)


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


# b_mean = np.mean(lengths)
# b_std = np.std(lengths)
#
# expected = 1.65
# t = (b_mean - b_std)/num_simulations
# res = stats.ttest_ind_from_stats(b_mean, b_std, )
# #ratio = round(ratio,2)
# prob = round((Animal.Herbivores._param['gamma'] * herb_test.fitness * n_animals), 2)
#
# print(res)

param_highland = {'Accepts_animals': True, 'Fodder':500}
Tile.Highland._param = Tile.Highland.set_param(param_highland)
print(Tile.Highland._param)
