import numpy as np
# import system_ as sys
from modules import system_ as sys
from modules import constraints as constraints
from deap import base, creator, tools
import random

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


def create_individual(LOWER_BOUNDS, UPPER_BOUNDS, state, N_HOURS=24):
    Dmax, Glmax, Gbmax, gmax = unpack(UPPER_BOUNDS)
    Dmin, Glmin, Gbmin, gmin = unpack(LOWER_BOUNDS)

    Gb = np.random.uniform(Gbmin, Gbmax, size=N_HOURS)
    g = np.random.uniform(gmin, gmax, size=N_HOURS)
    D = np.zeros(N_HOURS)

    check, gen, B = sys.battery_sim2(D,Gb,g, state, Bmax=100, N_HOURS=24)

    # alpha = np.random.uniform(0.55, 1, N_HOURS)
    
    Gl = Glmax - gen
        
    #Gl = np.clip(alpha * Glmax, 0, Glmax)
    #Gl[0] = Glmax[0]
    #D  = np.clip((1 - alpha) * Glmax, 0, Dmax)
    #D[0] = 0

    return np.concatenate([D, Gl, Gb, g])

def create_population(individuals, genome, LOWER_BOUNDS, UPPER_BOUNDS,state):
    # population = np.random.random([individuals,genome])
    # population = np.where(population > 0.5, population*0, population*0 + 1)
    population = np.zeros([individuals,genome])
    for i in range(individuals):
        population[i] = create_individual(LOWER_BOUNDS, UPPER_BOUNDS,state)
        
    return population


def fitness(individual, state, LOWER_BOUNDS, UPPER_BOUNDS, constraint):
    D, Gl, Gb, g = unpack(individual)
    penalty = 0

    Dmax, Glmax, Gbmax, Bmax, N_HOURS = constraint
    
    check, gen, B = sys.battery_sim2(D,Gb,g, state, Bmax)

    if not check:
        # print("battery constraint error")
        penalty += 1e6

    for t in range(N_HOURS):
        
        if not constraints.load_constraints(t, D, Gl, gen, state):
            # print("load constraint error")
            # penalty += 10 * sum(max(0, abs(Gl+D-state["load"])-1))
            penalty = 1e6
    
    
    if not constraints.bounded_constraint(individual, LOWER_BOUNDS, UPPER_BOUNDS):
        # print("Bounded error")
        penalty += 1e6
    
    

    cost = sys.cost(Gb,Gl, state)
    # cost -= SOC_T * future_price
    # SOC_T = B[-1]
    # future_price = np.mean(state["spotprice"])/1000  # or max, or percentile
    
    return (cost + penalty, )




def simulation(POP_SIZE, MAX_GEN, state, LOWER_BOUNDS, UPPER_BOUNDS, constraint):

    toolbox = base.Toolbox()

    # Fitness: minimize cost ⇒ weight = -1.0
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

    # Individual = list with attached fitness
    creator.create("Individual", list, fitness=creator.FitnessMin)

    # Register the evaluation function
    toolbox.register("evaluate", fitness, state=state, LOWER_BOUNDS=LOWER_BOUNDS, UPPER_BOUNDS=UPPER_BOUNDS, constraint=constraint)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxBlend, alpha=0.3)

    CXPB = 0.9  # crossover probability
    MUTPB = 0.3 # Mutation probability

    toolbox.register(
        "mutate",
        tools.mutPolynomialBounded,
        low=list(LOWER_BOUNDS),
        up=list(UPPER_BOUNDS),
        eta=20,
        indpb=0.05
    )

    population = create_population(POP_SIZE,96, LOWER_BOUNDS, UPPER_BOUNDS, state)
    population_dp = [creator.Individual(ind.tolist()) for ind in population]
    population = population_dp


    fitness_history = []

    for gen in range(MAX_GEN):
        # --- SELECTION ---
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # --- CROSSOVER ---
        for i in range(1, len(offspring), 2):
            if random.random() < CXPB:
                toolbox.mate(offspring[i-1], offspring[i])
                del offspring[i-1].fitness.values
                del offspring[i].fitness.values

        # --- MUTATION ---
        for ind in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(ind)
                del ind.fitness.values

        # --- EVALUATE IF NEEDED ---
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid:
            ind.fitness.values = toolbox.evaluate(ind)

        # --- ELITIST REPLACEMENT (μ + λ) ---
        population = tools.selBest(population + offspring, POP_SIZE)

        best = tools.selBest(population, 1)[0]
        best_fitness = best.fitness.values[0]
        fitness_history.append(best_fitness)

        # print progress
        print(f"Gen {gen}: Best = {best_fitness}")
    
    D, Gl, Gb, g = unpack(best)
    
    return fitness_history, D, Gl, Gb, g






