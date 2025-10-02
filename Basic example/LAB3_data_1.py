# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 21:03:13 2024

@author: elias
"""

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()

#class individual:
#    np.array()

"""
def create_individual():
    individual = np.random.random([1,50])
    individual = np.where(individual > 0.5, individual*0, individual*0 + 1)
    return individual
"""


#init pop(t)


def create_population():
    population = np.random.random([individuals,genome])
    population = np.where(population > 0.5, population*0, population*0 + 1)
    return population

def fitness(individual):
    evaluation = np.sum(individual)
    return evaluation

def evaluate_population(population):
    pop_fitness = np.sum(population, axis = 1)
    return pop_fitness

def roulette_selection(population,pop_fitness):
    
    probabilities = np.empty([individuals])
    i = 0
    
    for individual in population:
        p_i = fitness(individual)/np.sum(pop_fitness)
        probabilities[i] = p_i
        i += 1
        
    #print(np.sum(probabilities))
    return rng.choice(population, size=2, replace=False, p=probabilities)
    
def mutation(gene, p_mutation):    
    

    if np.random.rand() < p_mutation:
        gene = (gene + 1)%2

    return gene

def crossover(population, p_crossover):
    offspring = np.empty([2,genome])
    
    for gene in range(population[0,:].size):
        
        
        new_gene = rng.choice([population[0,gene],population[1,gene]], size=1, replace=False, p = [p_crossover, 1 - p_crossover])
        offspring[0,gene] = mutation(new_gene[0], p_mutation)
        new_gene = rng.choice([population[0,gene],population[1,gene]], size=1, replace=False, p = [p_crossover, 1 - p_crossover])
        offspring[1,gene] = mutation(new_gene[0], p_mutation)
    
    return offspring



genome = 50
individuals = 20
p_crossover = 0.6
p_mutation = 0.03

pop = create_population()

pop_fitness = evaluate_population(pop)

t = 0

fitness_growth = []
while True:
    t += 1
        

    parents_AB = roulette_selection(pop, pop_fitness)
    offspring_AB = crossover(parents_AB,p_crossover)                        
    

    po = np.concatenate((parents_AB,offspring_AB))
    po_fitness = evaluate_population(po)
    
    
    seeding = np.empty([2, genome])
    for i in range(2):
        seeding[i,:] = po[np.argmax(po_fitness),:]
        po_fitness[np.argmax(po_fitness)] = 0
        
         
        
        #pop = np.where(pop == (parents_AB[0,:] or parents_AB[1,:]), pop, pop = seeding)
            
    for i in range(pop.shape[0]):
        if np.array_equal(pop[i], parents_AB[0,:]):
            pop[i] = seeding[0,:]
        if np.array_equal(pop[i], parents_AB[1,:]):
            pop[i] = seeding[1,:]


        
    pop_fitness = evaluate_population(pop)
    fitness_growth.append(np.max(pop_fitness))
    
    if 50 in pop_fitness or t == 1000:
        plt.plot(fitness_growth)
        plt.show()
        
        print(t)
        break
    


