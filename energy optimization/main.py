import numpy as np
from deap import base, creator, tools
import random
import system.GA as GA


##################################
# Objectives reduce cost
#            reduce grid usage
#
# New Control variables HVDC -> energy usage 
#                       Load scheduling
#                       
#
##################################



Dmax = 30             #kW
Glmax = 30            #kW
Gbmax = 20          #kW
Bmax = 150            #kW
N_HOURS = 24


LOWER_BOUNDS = np.concatenate([
    np.zeros(N_HOURS),          # D ≥ 0
    np.zeros(N_HOURS),          # Gl ≥ 0
    np.zeros(N_HOURS),          # Gb ≥ 0
    np.zeros(N_HOURS)           # gamma ≥ 0
])

UPPER_BOUNDS = np.concatenate([
    np.ones(N_HOURS) * Dmax,    # D
    np.ones(N_HOURS) * Glmax,   # Gl
    np.ones(N_HOURS) * Gbmax,   # Gb
    np.ones(N_HOURS)            # gamma ∈ [0,1]
])

genome      = 96
individuals = 2

#TODO fix load to be resoanble size

test = GA.create_population(genome, individuals, LOWER_BOUNDS, UPPER_BOUNDS)



print(test)

