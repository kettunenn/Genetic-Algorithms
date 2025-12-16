import numpy as np
import random
from system import constraints as constraints



# g (gamma) amount of energy stored from solar in battery 
# D(t) battery discharge to meet demand at t 
# Gl(t) power supplied from the grid to meet demand at t
# Gb(t) power supplied from the grid to charge battery at t
# B(t) Battery SOC at t





def solar_gen(t, state, S=2000):
    theta_S = 0.15 # solarpanel efficiency

    return theta_S * S * state["irradiance"].iloc[t]/1000


def electricity_price(Gb, Gl, t, state):
    return (Gb[t] + Gl[t]) * state["spotprice"].iloc[t]/1000



def battery_sim(D,Gb,g, state, Bmax=100, N_HOURS=24):
    B = np.zeros(N_HOURS + 1)

    for t in range(N_HOURS):
        B[t + 1] = B[t] - D[t] + g[t]*solar_gen(t, state) + Gb[t]
        
        if (B[t + 1] > Bmax):
            B[t + 1] = Bmax

        if constraints.battery_constraints(t, D, B, Bmax):
            return False

    return True



def battery_sim2(D,Gb,g, state, Bmax=100, N_HOURS=24):
    B = np.zeros(N_HOURS + 1)
    gen = np.zeros(N_HOURS)
    gen2 = np.zeros(N_HOURS)
    check = True

    for i in range(N_HOURS):
        gen[i] = g[i]*solar_gen(i, state)
        gen2[i] = (1 - g[i])*solar_gen(i, state)

    for t in range(N_HOURS):
        B[t + 1] = B[t] - D[t] + gen2[t] + Gb[t]
        
        if (B[t + 1] > Bmax):
            B[t + 1] = Bmax
        
        if constraints.battery_constraints(t, D, B, Bmax):
            check = False

    return check, gen, B

def cost(Gb,Gl, state):
    
    total_sum = 0

    for i in range(len(Gb)):
        total_sum += electricity_price(Gb,Gl,i,state)
    
    return total_sum



