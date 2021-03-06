from Polygon import *
from genetic_utils import *
from fold_utils import *

# testing begins ---------------------------------------------------------

source = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
# source = Polygon([(0, 0.5), (0.5, 0), (1, 0.5)])

# fold descriptions of levels
# lvl1 = (((0, 0), (1, 1), 1), )
# lvl2 = (((0, 0.5), (1, 0.5), 0), ((0.5, 0), (0.5, 1), 0))
# lvl3 = (((0, 0.5), (1, 0.5), 1), ((0.5, 0), (0.5, 1), 0), ((0.5, 0),
#         (1, 0.5), 1))
# lvl4 = (((0, 0.333), (0.333, 0), 0), ((0.666, 0), (1, 0.333), 0),
#         ((0, 0.666), (0.333, 1), 1), ((0.666, 1), (1, 0.666), 1))
# lvl5 = (((0, 1), (1, 0), 1), ((0, 0.5), (0.5, 0), 0), ((0.5, 0),
#         (1, 0.5), 0), ((0, 0.5), (0.5, 1), 1))
# lvl6 = (((0, 0.4), (1, 0.4), 0), ((0.5, 0), (0.5, 1), 1), ((0, 0.8),
#         (0.25, 1), 0), ((0.25, 1), (0.5, 0.8), 1))
# lvl7 = (((0, 0.5), (1, 0.5), 1), ((0.5, 0), (0.5, 1), 1), ((0.25, 0),
#         (0.25, 1), 2), ((0, 0.25), (1, 0.25), 0))

# final shape description of levels
# t8 = Polygon([(1, 0), (1, 0.57), (0.8, 0.7), (0.5, 0.55), (0.51, 0.3)])
# t13 = Polygon([(-0.003, 0.497), (0.141, 0.5), (0.673, 1.032),
#                (0.776, 1.029), (0.676, 0.929), (0.679, 0.676),
#                (0.077, 0.423)])
# t15 = Polygon([(0.5-1./8, 1), (0.5+1./8, 1), (0.5+1./8, 0.5+1./8),
#                (1, 0.5+1./8), (1, 0.5-1./8), (0.5+1./8, 0.5-1./8),
#                (0.5-1./8, 0.5+1./8)])

# target = multiFold(source, lvl7)[0][-1]
target = t15

# create seed population
basicfolds = getBasicfolds(source, target)
population = firstGen(source, target, basicfolds, 200, 4)
for i in xrange(len(population)):
    population.append(mutate(population[i], source, target))

# iterating over generations
i = 30
bestfitness = 0
while i and bestfitness < 0.97:
    i -= 1
    args = [source, target, population, True]
    population, bestfitness, bestchromosome = newGeneration(*args)
