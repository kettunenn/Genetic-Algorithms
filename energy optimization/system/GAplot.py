import matplotlib.pyplot as plt
from system import system_ as sys
import numpy as np

def plot_individual(D, Gl, Gb, g, state):
    plt.figure(figsize=(20, 5))
    plt.plot(D, label='Discharge')
    

    sol = np.zeros(len(D))
    for i in range(len(D)):
        sol[i] = g[i] *sys.solar_gen(i, state)
    plt.plot(sol, label="Generated")

    
    plt.plot(state["load"], label='Total Load')

    plt.plot(Gb, label='Battery Charging')
    
    
    plt.plot(Gl, label='Grid')
    
    
    
    plt.legend()
    plt.show()



def plot_battery(D,Gb,g, state):
    check, gen, B = sys.battery_sim2(D,Gb,g, state)

    plt.figure(figsize=(20, 5))
    plt.plot(B, label='SoC')

    plt.plot(D, label='Discharge')

    plt.plot(Gb, label='G_Charge')

    plt.plot(gen, label='S_Charge')

    plt.legend()
    plt.show()


def plot_fitness(fitness_history):
    
    plt.figure()
    plt.plot(fitness_history)
    plt.xlabel("Generation")
    plt.ylabel("Best fitness")
    plt.title("GA Convergence")
    plt.grid(True)
    plt.show()