import numpy as np
# import system_ as sys
from system import system_ as sys
from system import constraints as constraints


# -----------------------------
# Design parameters 
# -----------------------------

# D(t) battery discharge to meet demand at t 
# Gl(t) power supplied from the grid to meet demand at t
# Gb(t) power supplied from the grid to charge battery at t
# gamma amount of energy stored from solar in battery 


def unpack(individual, N_HOURS=24):
    
    D   = individual[0:N_HOURS]
    Gl  = individual[N_HOURS:2*N_HOURS]
    Gb  = individual[2*N_HOURS:3*N_HOURS]
    g   = individual[3*N_HOURS:4*N_HOURS]
    return D, Gl, Gb, g



def create_individual(LOWER_BOUNDS, UPPER_BOUNDS, N_HOURS=24):
    Dmax, Glmax, Gbmax, gmax = unpack(UPPER_BOUNDS)

    alpha = np.random.uniform(0.55, 1, N_HOURS)

    Gl = Glmax
    D = np.zeros(N_HOURS)
    #Gl = np.clip(alpha * Glmax, 0, Glmax)
    #Gl[0] = Glmax[0]
    #D  = np.clip((1 - alpha) * Glmax, 0, Dmax)
    #D[0] = 0
    
    Gb = np.random.uniform(0, Gbmax, size=N_HOURS)

    g = np.random.uniform(0, gmax, size=N_HOURS)

    return np.concatenate([D, Gl, Gb, g])

    # return np.random.uniform(LOWER_BOUNDS, UPPER_BOUNDS)

def create_population(individuals, genome, LOWER_BOUNDS, UPPER_BOUNDS):
    # population = np.random.random([individuals,genome])
    # population = np.where(population > 0.5, population*0, population*0 + 1)
    population = np.zeros([individuals,genome])
    for i in range(individuals):
        population[i] = create_individual(LOWER_BOUNDS, UPPER_BOUNDS)
        
    return population


def fitness(individual, state, LOWER_BOUNDS, UPPER_BOUNDS, constraint):
    D, Gl, Gb, g = unpack(individual)
    penalty = 0

    Dmax, Glmax, Gbmax, Bmax, N_HOURS = constraint
   
    check, gen, B = sys.battery_sim2(D,Gb,g, state, Bmax)

    if not sys.battery_sim(D,Gb,g, state, Bmax):
        print("battery constraint error")
        penalty += 1e6

    for t in range(N_HOURS):
        
        if not constraints.load_constraints(t, D, Gl, gen, state):
            print("load constraint error")
            # penalty += 10 * sum(max(0, abs(Gl+D-state["load"])-1))
            penalty = 1e6
    
    
    if not constraints.bounded_constraint(individual, LOWER_BOUNDS, UPPER_BOUNDS):
        print("Bounded error")
        penalty += 1e6
    

    cost = sys.cost(Gb,Gl, state)

    return (cost + penalty, )




