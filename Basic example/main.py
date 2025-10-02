# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:21:46 2024

@author: elias
"""
import numpy as np
import matplotlib.pyplot as plt
import time
import ga_simulation as sim

if __name__ == '__main__':
    
    genome = 50 #genome = 50
    individuals = 20 #individuals = 20
    p_crossover = 0.06 #p_crossover = 0.6
    p_mutation = 0.03 #p_mutation = 0.03
    max_iterations = 10000

    data = []
    
    
    #fitness_growth, t = sim.simulation(genome, individuals, p_crossover, p_mutation, max_iterations)
    
    #plt.figure()
    #plt.plot(fitness_growth)
    #plt.show()

    tot = 0
    
    start_time = time.time()
    data_mutation = []
    p_mutation = 0.005
    for i in range(100):
        iteration_time = time.time()
        fitness_growth, t = sim.simulation(genome, individuals, p_crossover, p_mutation + i/1000, max_iterations)
        data_mutation.append(t)
        print("time elapsed", time.time()-start_time)
        print("Current iteration", i)
        print("Iteration time", time.time()-iteration_time)
        tot =+ i
    
    #plt.plot(fitness_growth)
    plt.figure()
    plt.plot((np.arange(p_mutation, p_mutation + 100/1000, 1/1000)),data_mutation)
    plt.ylabel("Generations")
    plt.xlabel("Probability of mutation")
    p_mutation = 0.03
    
    data_crossover = []
    
    p_crossover = 0
    for i in range(500):
        iteration_time = time.time()
        fitness_growth, t = sim.simulation(genome, individuals, p_crossover + i/500, p_mutation , max_iterations)
        data_crossover.append(t)
        print("time elapsed", time.time()-start_time)
        print("Current iteration", i)
        print("Iteration time", time.time()-iteration_time)
        tot =+ i
    
    #plt.plot(fitness_growth)
    plt.figure()
    plt.plot((np.arange(p_crossover, p_crossover + 500/500, 1/500)),data_crossover)
    plt.ylabel("Generations")
    plt.xlabel("Probability crossover")
    p_crossover = 0.6  
    """
    data_individuals = []
    individuals = 10
    for i in range(90):
        iteration_time = time.time()
        fitness_growth, t = sim.simulation(genome, individuals + i, p_crossover, p_mutation , max_iterations)
        data_individuals.append(t)
        print("time elapsed", time.time()-start_time)
        print("Current iteration", i)
        print("Iteration time", time.time()-iteration_time)
        tot =+ i
        
    #plt.plot(fitness_growth)
    plt.figure()
    plt.plot((np.arange(individuals, individuals + 90)),data_individuals)
    plt.ylabel("Generations")
    plt.xlabel("Number of individuals")
"""