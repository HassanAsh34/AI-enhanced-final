import math
import random

import numpy as np
from fontTools.merge.util import first
from networkx.algorithms.polynomials import chromatic_polynomial
from numpy.ma.extras import average

import Node as n


def generatePopulation(nodes,colors,size):
    # colors = len(colors)
    population = np.random.randint(0,colors,size=(size,nodes))
    return population


def calculatefitness(population,graph):

    conflicts = calculateConflict(population, edges=graph.edges)
    chromatic = np.array(n.evaluateSolutions(population, True))
    # for t in Population:
    #     conflict.append(t[1])
    #     chromatic.append(t[2])
    # conflict = np.array(conflict)
    # chromatic = np.array(chromatic)
    # EdgeCount = len(graph.edges)
    # fitness = 1.0 / (1 + (conflicts * EdgeCount + chromatic))
    fitness = 1.0 / (1 + (conflicts * 100 + chromatic))
    # pop = [(list(int(x) for x in population[i]), int(conflicts[i]), int(chromatic[i])) for i in
    #        range(population.shape[0])]
    population = population.tolist()
    Population_fitness = [(population[i],float(fitness[i]),int(conflicts[i]),int(chromatic[i])) for i in range(len(population))]

    # Population_fitness.pop()
    # print(pop)
    Population_fitness.sort(key= lambda x:x[1] , reverse= True)
    avg_chromatic = int(np.average(chromatic))
    avg_fitness = float(np.average(fitness))
    return Population_fitness , avg_fitness , avg_chromatic



# def CulturalAlgorithm(nodes,colors,g,pop_size,mutaion_rate,belief_size):
#     population = generatePopulation(len(nodes),len(colors),pop_size)
#     population , avg_fitness , avg_chromatic = calculatefitness(population, g)
#     # conflicts = calculateConflict(population,edges=g.edges)
#     # chromatic = n.evaluateSolutions(population,True)
#     # elite_count = max(1, int(.1 * len(population)))
#     belief_space = []
#     average_fitnessList = list()
#     average_fitnessList.append(avg_fitness)
#     average_chromaticNumberList = list()
#     average_chromaticNumberList.append(avg_chromatic)
#     threshold = 1e-3
#     for i in range(50000):
#         print(i)
#         elites = population[:max(1, int(.1 * len(population)))]
#         belief_space = update_belief_space(belief_space,elites, belief_size)
#         population = generate_new_population(mutaion_rate,elites,belief_size,belief_space,len(nodes),len(colors),pop_size)
#         population , avg_fitness , avg_chromatic  = calculatefitness(population, g)
#
#         average_fitnessList.append(avg_fitness)
#         average_chromaticNumberList.append(avg_chromatic)
#         if len(belief_space) == belief_size:
#             if i% math.ceil(50000 / 1000) == 0:
#                 recent_changes = np.abs(np.diff(average_fitnessList[-5:]))
#                 if np.all(recent_changes < threshold):
#                     print("Algorithm has converged")
#                 else:
#                     print("Still improving")
#         # belief_space = np.array(belief_space)
#         # population = np.array(population)
#     return belief_space , population , average_fitnessList , average_chromaticNumberList

        # return np.array(belief_space), np.array(population)


# def CulturalAlgorithm(nodes, colors, g, pop_size, mutaion_rate, belief_size,influence_rate = .6,threshold = 1e-3):
#     population = generatePopulation(len(nodes), len(colors), pop_size)
#     population, avg_fitness, avg_chromatic = calculatefitness(population, g)
#
#     belief_space = []
#     average_fitnessListforPopulation = list()
#     average_chromaticNumberListforPopulation = list()
#     average_fitnessListforPopulation.append(avg_fitness)
#     average_chromaticNumberListforPopulation.append(avg_chromatic)
#     avg_fitnessforBelief = list()
#     average_chromaticNumberListforBelief = list()
#     # threshold = 1e-3  # convergence threshold
#     convergence_window = 5  # check last 5 iterations
#     converged_at = 0
#     for i in range(50000):
#         # print(i)
#         elites = population[:max(1, int(.1 * len(population)))]
#         belief_space = update_belief_space(belief_space, elites, belief_size)
#         population = generate_new_population(mutaion_rate, elites, belief_size, belief_space,
#                                              len(nodes), len(colors), pop_size,influence_rate)
#         population, avg_fitness, avg_chromatic = calculatefitness(population, g)
#
#         # print(belief_space)
#         # Convergence check
#         if i % 1000 == 0:
#             converged_at = i #i will keep it like this in case we havent converged
#             print("Still improving...")
#             avgf = list()
#             avgc = list()
#             for fitness in belief_space:
#                 avgf.append(fitness[1])
#                 avgc.append(fitness[3])
#             avgf = float(np.average(avgf))
#             avgc = int(np.average(avgc))
#             if len(avg_fitnessforBelief) > convergence_window:
#                 recent_changes = np.abs(np.diff(avg_fitnessforBelief[-convergence_window:]))
#                 if np.all(recent_changes < threshold):
#                     print(f"Algorithm has converged at iteration {i}")
#                     # converged_at = i
#                     break
#                 else:
#                     avg_fitnessforBelief.append(avgf)
#                     average_chromaticNumberListforBelief.append(avgc)
#                     average_fitnessListforPopulation.append(avg_fitness)
#                     average_chromaticNumberListforPopulation.append(avg_chromatic)
#             else:
#                 avg_fitnessforBelief.append(avgf)
#                 average_chromaticNumberListforBelief.append(avgc)
#                 average_fitnessListforPopulation.append(avg_fitness)
#                 average_chromaticNumberListforPopulation.append(avg_chromatic)

def CulturalAlgorithm(nodes, colors, g, pop_size, mutaion_rate, belief_size, influence_rate=.6, threshold=1e-3):
    population = generatePopulation(len(nodes), len(colors), pop_size)
    population, avg_fitness, avg_chromatic = calculatefitness(population, g)

    belief_space = []
    average_fitnessListforPopulation = list()
    average_chromaticNumberListforPopulation = list()
    average_fitnessListforPopulation.append(avg_fitness)
    average_chromaticNumberListforPopulation.append(avg_chromatic)
    avg_fitnessforBelief = list()
    average_chromaticNumberListforBelief = list()
    # threshold = 1e-3  # convergence threshold
    convergence_window = 5  # check last 5 iterations
    converged_at = 0
    for i in range(50000):
        # print(i)
        elites = population[:max(1, int(.1 * len(population)))]
        belief_space = update_belief_space(belief_space, elites, belief_size)
        population = generate_new_population(mutaion_rate, elites, belief_size, belief_space,
                                             len(nodes), len(colors), pop_size, influence_rate)
        population, avg_fitness, avg_chromatic = calculatefitness(population, g)

        # print(belief_space)
        # Convergence check
        if i % 1000 == 0:
            converged_at = i  # i will keep it like this in case we havent converged
            print("Still improving...")
            avgf = list()
            avgc = list()
            for fitness in belief_space:
                avgf.append(fitness[1])
                avgc.append(fitness[3])
            avgf = float(np.average(avgf))
            avgc = int(np.average(avgc))
            if len(avg_fitnessforBelief) > convergence_window:
                recent_changes = np.abs(np.diff(avg_fitnessforBelief[-convergence_window:]))
                if np.all(recent_changes < threshold):
                    print(f"Algorithm has converged at iteration {i}")
                    # converged_at = i
                    break
            avg_fitnessforBelief.append(avgf)
            average_chromaticNumberListforBelief.append(avgc)
            average_fitnessListforPopulation.append(avg_fitness)
            average_chromaticNumberListforPopulation.append(avg_chromatic)


    return belief_space, population, average_fitnessListforPopulation, average_chromaticNumberListforPopulation, avg_fitnessforBelief , average_chromaticNumberListforBelief , converged_at



def update_belief_space(belief_space,elites,belief_size):
    belief_size_curr = len(belief_space)
    if belief_size_curr == 0:
        if belief_size > len(elites):
            belief_space.extend(elites)
        else:
            belief_space.extend(elites[:belief_size])
    else:
        for elite in elites:
            # if belief_size_curr < len(elites):
            if belief_size_curr < belief_size:
                belief_space.append(elite)
                continue
            worst = min(belief_space,key=lambda x:x[1])
            if elite[1] > worst[1]:
                belief_space.remove(worst)
                belief_space.append(elite)
    return belief_space


def generate_new_population(mutaion_rate,elites,belief_size,belief_space,num_nodes,num_colors,pop_size,influence_rate):
    new_pop = []
    # print(elites)
    # for e in elites:
    #     # print(e[0])
    #     new_pop.append(e[0])
    crossover_elites = crossover(elites,num_nodes)
    new_pop.extend(crossover_elites)

    belief_offspring_count = int((pop_size-len(new_pop))*.7)

    belief_influenced = get_belief_influenced_children(belief_offspring_count,belief_space,num_nodes,num_colors,influence_rate)
    new_pop.extend(belief_influenced)

    if len(new_pop) < pop_size:
        pop = generatePopulation(num_nodes,num_colors,(pop_size-len(new_pop)));
        new_pop.extend(pop)

    for child in new_pop:
        if random.random() < mutaion_rate:
            idx = random.randint(0,num_nodes-1)
            child[idx] = random.randint(0,num_colors-1)
    return np.array(new_pop)
    # for _ in range(belief_offspring_count):


# def crossover(elites,num_nodes):
#     size = len(elites)
#     children = list()
#     for i in range(size):
#         i1 = i % size
#         i2 = (i+1)%size
#         point = random.randint(0,num_nodes-1)
#         p1 = elites[i1][0]
#         p2 = elites[i2][0]
#         child = p1[:point] + p2[point:]
#         children.append(child)

def crossover(elites, num_nodes):
    size = len(elites)
    children = []
    for _ in range(size):
        i1, i2 = random.sample(range(size), 2)  # pick 2 distinct parents
        p1, p2 = elites[i1][0], elites[i2][0]
        point = random.randint(1, num_nodes-1)  # meaningful crossover
        child = p1[:point] + p2[point:]
        children.append(child)
    return children




# def get_belief_influnced_children(belief_offspring_count,belief_space,num_nodes,num_colors,influence_rate):
#     children = np.zeros((belief_offspring_count,num_nodes),int)
#     for child in children:
#         if random.random() < influence_rate:
#             for i in range(num_nodes):
#                 belief = random.choice(belief_space)
#                 elite_solution = belief[0]
#                 child[i] = elite_solution[0]
#         else:
#             child[i] = random.randint(0,num_colors-1)
#     return children

def get_belief_influenced_children(belief_offspring_count, belief_space, num_nodes, num_colors, influence_rate):
    children = []
    for _ in range(belief_offspring_count):
        child = []
        for i in range(num_nodes):
            if random.random() < influence_rate:
                belief = random.choice(belief_space)
                elite_solution = belief[0]  # full chromosome list
                child.append(elite_solution[i])  # pick the i-th gene from elite
            else:
                child.append(random.randint(0, num_colors - 1))
        children.append(child)
    return children





def calculateConflict(population,edges):
    conflict = np.zeros(len(population))
    for u,v in edges:
        conflict += (population[:,u-1]==population[:,v-1])
    return conflict