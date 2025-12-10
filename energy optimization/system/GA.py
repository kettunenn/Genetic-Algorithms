import numpy as np
import system_ as sys
import constraints as constraints

# -----------------------------
# Design parameters 
# -----------------------------

# D(t) battery discharge to meet demand at t 
# Gl(t) power supplied from the grid to meet demand at t
# Gb(t) power supplied from the grid to charge battery at t
# gamma amount of energy stored from solar in battery 


def unpack(individual, N_HOURS=24):
    D   = individual[0:N_HOURS]
    Gb  = individual[N_HOURS:2*N_HOURS]
    Gl  = individual[2*N_HOURS:3*N_HOURS]
    g   = individual[3*N_HOURS:4*N_HOURS]
    return D, Gb, Gl, g


def create_individual(LOWER_BOUNDS, UPPER_BOUNDS):
    
    return np.random.uniform(LOWER_BOUNDS, UPPER_BOUNDS)


def create_population(individuals, genome, LOWER_BOUNDS, UPPER_BOUNDS):
    # population = np.random.random([individuals,genome])
    # population = np.where(population > 0.5, population*0, population*0 + 1)
    population = np.zeros([individuals,genome])
    for i in range(individuals):
        population[i] = create_individual(LOWER_BOUNDS, UPPER_BOUNDS)
        
    return population


def fitness(individual, state, LOWER_BOUNDS, UPPER_BOUNDS, constraint):
    D, Gb, Gl, g = unpack(individual)
    penalty = 0

    Dmax, Glmax, Gbmax, Bmax, N_HOURS = constraint
   
    if not sys.battery_sim(D,Gb,g, state, Bmax):
        # print("battery constraint error")
        penalty = 1e6

    for t in range(N_HOURS):
        
        if not constraints.load_constraints(t, D, Gl, state):
            # print("load constraint error")
            penalty = 1e6
    
    
    if not constraints.bounded_constraint(individual, LOWER_BOUNDS, UPPER_BOUNDS):
        # print("Bounded error")
        penalty = 1e6
    

    cost = sys.cost(Gb,Gl, state)
    print(cost + penalty)
    return (cost + penalty, )




