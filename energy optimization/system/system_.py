import numpy as np
from deap import base, creator, tools
import random
import constraints



# g (gamma) amount of energy stored from solar in battery 
# D(t) battery discharge to meet demand at t 
# Gl(t) power supplied from the grid to meet demand at t
# Gb(t) power supplied from the grid to charge battery at t
# B(t) Battery SOC at t





def solar_gen(t, state, S=20):
    theta_S = 0.15 # solarpanel efficiency

    return theta_S * S * state["irradiance"].iloc[t]/1000


def electricity_price(Gb, Gl, t, state):
    return (Gb[t] + Gl[t]) * state["spotprice"].iloc[t]



def battery_sim(D,Gb,g, state, Bmax=100, N_HOURS=24):
    B = np.zeros(N_HOURS + 1)

    for t in range(N_HOURS):
        B[t + 1] = B[t] - D[t] + g[t]*solar_gen(t, state) + Gb[t]

        if not constraints.battery_constraints(t, D, B, Bmax):
            return False

    return True

def cost(Gb,Gl, state):
    
    total_sum = 0

    for i in range(len(Gb)):
        total_sum += electricity_price(Gb,Gl,i,state)
    
    return total_sum



