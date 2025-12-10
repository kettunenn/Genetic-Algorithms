import numpy as np

def general_constraints(Dmax=30,                #Battery discharge limit
                        Glmax=30,               #Grid battery charging
                        Gbmax=20,               #Grid supply
                        Bmax=100,               #Battery size
                        N_HOURS=24):

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

    constraints = [Dmax, Glmax, Gbmax, Bmax, N_HOURS]

    return LOWER_BOUNDS, UPPER_BOUNDS, constraints


def battery_constraints(t, D, B, Bmax):
    # D(t) ≤ B(t) ≤ Bmax
    return B[t] < D[t] or B[t] > Bmax
    

def load_constraints(t, D, Gl, state):
    # Load (t) = Gl(t) + D(t)
    return abs(Gl[t] + D[t] - state["load"].iloc[t]) > 1e3
    

def bounded_constraint(individual, LOWER_BOUNDS, UPPER_BOUNDS):
    return np.all(individual >= LOWER_BOUNDS) and np.all(individual <= UPPER_BOUNDS)
    