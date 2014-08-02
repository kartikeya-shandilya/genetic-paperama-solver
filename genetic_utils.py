from Polygon import *
from Polygon.IO import *
from copy import deepcopy
from random import random, randint, uniform
from fold_utils import *
from math import sqrt

def getBasicfolds(source, target):
    source = deepcopy(source)
    target = deepcopy(target)
    basicfolds = []
    basicfolds.append(((0,0),(1,1),0))
    basicfolds.append(((0,0),(1,1),1))
    basicfolds.append(((1,0),(0,1),0))
    basicfolds.append(((1,0),(0,1),1))
    basicfolds.append(((0,0.5),(1,0.5),0))
    basicfolds.append(((0,0.5),(1,0.5),1))
    basicfolds.append(((0.5,0),(0.5,1),0))
    basicfolds.append(((0.5,0),(0.5,1),1))
    for i in xrange(len(target[0])-1):
        basicfolds.append((target[0][i],target[0][i+1],0))
        basicfolds.append((target[0][i],target[0][i+1],1))
    basicfolds.append((target[0][len(target[0])-1],target[0][0],0))
    basicfolds.append((target[0][len(target[0])-1],target[0][0],1))
    return basicfolds

def fitness(candidate, target):
    union = target + candidate
    commn = candidate & target
    if not union.area():
        return 0
    ar1 = commn.area()/union.area()
    return ar1
 
def firstGen(source, target, onefolds, n=400, folds=1):
    onefolds = deepcopy(onefolds)
    chromosomes = []
    for i in xrange(n):
        tmp = []
        while len(tmp)<folds:
            tmp.append(onefolds[randint(0,len(onefolds)-1)])
        chromosomes.append(tuple(tmp))
    return chromosomes

def crossOver(chromosome1, chromosome2, chance=0.25):
    offspring1 = []
    offspring2 = []
    for i in xrange(len(chromosome1)):
        (p1,q1),(p2,q2),X = chromosome1[i]
        (r1,s1),(r2,s2),Y = chromosome2[i]
        tmp1 = (((p1+r1)/2.0,(q1+s1)/2.0),((p2+r2)/2.0,(q2+s2)/2.0),X)
        tmp2 = (((p1+r1)/2.0,(q1+s1)/2.0),((p2+r2)/2.0,(q2+s2)/2.0),Y)
        if random()<chance: tmp1 = chromosome1[i]
        if random()<chance: tmp2 = chromosome2[i]
        offspring1.append(tmp1)
        offspring2.append(tmp2)
    return [list(offspring1),list(offspring1)]
    
def weighted_random_choice(popfitness):
    ulim = sum(popfitness.values())
    pick = uniform(0, ulim)
    current = 0
    for key, value in popfitness.items():
        current += value
        if current > pick:
            return key

def mutate(chromosome, source, target, rate=0.4):
    basicfolds = getBasicfolds(source, target)
    mutation = []
    for i in xrange(len(chromosome)):
        (p1,q1),(p2,q2),X = chromosome[i]
        if random()<rate**2:
            if random()<rate/4.: p1 += (2*round(random(),2)-1)
            if random()<rate/4.: q1 += (2*round(random(),2)-1)
            if random()<rate/4.: p2 += (2*round(random(),2)-1)
            if random()<rate/4.: q2 += (2*round(random(),2)-1)
        else:
            if random()<rate**2:
                p1 += (2*round(random(),2)-1)
                p2 += (2*round(random(),2)-1)
        if random()<rate**2: X = 1-X
        tmp = ((round(p1,3),round(q1,3)),(round(p2,3),round(q2,3)),X)
        if random()<0.7: tmp = basicfolds[randint(0,len(basicfolds)-1)]
        mutation.append(tmp)
    if random()<(sqrt(sqrt(len(chromosome)-1))*fitness(multiFold(source,chromosome)[0][-1],target)**4)/10.0:
        picker = {i:i for i in range(len(chromosome))}
        fupto = weighted_random_choice(picker)
        if fupto:
            src = multiFold(source,chromosome[:fupto])[0][-1]
            bfolds = getBasicfolds(src, target)
            spopul = firstGen(source, target, bfolds, 100, len(chromosome)-fupto)
            for i in xrange(len(spopul)): spopul.append(mutate(spopul[i], src, target))
            for i in xrange(3):
                spopul, bestfitness, bestchromosome = newGeneration(src, target, spopul)
            mutation = tuple(list(chromosome[:fupto])+list(bestchromosome))
            print 'recursive: genetic-programming:: recursed at ', `len(chromosome)`,' at ', `fupto`,': initial-fitness', `fitness(multiFold(source,chromosome)[0][-1],target)`, ' final-fitness', `fitness(multiFold(source,mutation)[0][-1],target)`
    return tuple(mutation)

def getPopFitness(source, target, population):
    allfitness = {}
    for chromosome in population:
        myfitness = fitness(multiFold(source,chromosome)[0][-1],target)
        allfitness[chromosome] = myfitness
    return allfitness
    
def newGeneration(source, target, population, verbose=False):
    basicfolds = getBasicfolds(source, target)
    popfitness = getPopFitness(source, target, population)
    bestcandidates = sorted(popfitness, key=popfitness.get, reverse=True)
    if verbose:
        print "Best candidate fitness = ", popfitness[bestcandidates[0]]
        printMultiBigChromosome(source, target, bestcandidates[:5])
    newpop = bestcandidates[:min(50,len(population))]
    while len(newpop)<len(population):
        parent1 = weighted_random_choice(popfitness)
        parent2 = weighted_random_choice(popfitness)
        if parent1==None or parent2==None:
            kid1, kid2 = parent1, parent2
        else:
            kid1, kid2 = crossOver(parent1, parent2)
        if verbose:
            reqFitness = getPopFitness(source, target, (parent1, parent2, kid1, kid2))
            print 'cross-over: effect', reqFitness
        tmp1 = mutate(kid1, source, target)
        if tmp1:
            newpop.append(tmp1)
        tmp2 = mutate(kid2, source, target)
        if tmp2:
            newpop.append(tmp2)
    return newpop, popfitness[bestcandidates[0]], bestcandidates[0]
