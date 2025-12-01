# GA Function Optimization — single-file demo
# Run: python ga_function_opt.py
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos

def f(x: float) -> float:
    return sin(10*x)*x + cos(2*x)*x

X_MIN, X_MAX = 0.0, 10.0

POP_SIZE = 60
GENERATIONS = 60
TOURNAMENT_K = 3
CROSSOVER_RATE = 0.9
MUTATION_STD = 0.15
ELITE_COUNT = 2
RNG = np.random.default_rng(42)

def random_individual():
    return RNG.uniform(X_MIN, X_MAX)

def fitness(x):
    return f(x)

def tournament_select(pop, fits, k=TOURNAMENT_K):
    idxs = RNG.integers(0, len(pop), size=k)
    best = idxs[0]
    best_fit = fits[best]
    for i in idxs[1:]:
        if fits[i] > best_fit:
            best = i
            best_fit = fits[i]
    return pop[best]

def blend_crossover(a, b, alpha=0.5):
    lo = min(a, b)
    hi = max(a, b)
    range_ = hi - lo
    lo_ = lo - alpha * range_
    hi_ = hi + alpha * range_
    child = RNG.uniform(lo_, hi_)
    return float(np.clip(child, X_MIN, X_MAX))

def mutate(x, std=MUTATION_STD):
    child = x + RNG.normal(0.0, std)
    return float(np.clip(child, X_MIN, X_MAX))

def main():
    pop = np.array([random_individual() for _ in range(POP_SIZE)], dtype=float)
    history_best = []
    history_mean = []
    for _ in range(GENERATIONS):
        fits = np.array([fitness(x) for x in pop])
        history_best.append(float(np.max(fits)))
        history_mean.append(float(np.mean(fits)))
        elite_idxs = np.argsort(fits)[-ELITE_COUNT:]
        elites = pop[elite_idxs].copy()
        next_pop = []
        while len(next_pop) < POP_SIZE - ELITE_COUNT:
            p1 = tournament_select(pop, fits)
            p2 = tournament_select(pop, fits)
            if RNG.random() < CROSSOVER_RATE:
                child = blend_crossover(p1, p2, alpha=0.5)
            else:
                child = p1
            child = mutate(child)
            next_pop.append(child)
        pop = np.array(next_pop + elites.tolist(), dtype=float)

    final_fits = np.array([fitness(x) for x in pop])
    best_idx = int(np.argmax(final_fits))
    best_x = float(pop[best_idx])
    best_f = float(final_fits[best_idx])
    print(f"Best solution: x = {best_x:.5f}, f(x) = {best_f:.5f}")

    xs = np.linspace(X_MIN, X_MAX, 800)
    ys = np.array([f(x) for x in xs])

    plt.figure()
    plt.plot(history_best, label="Best fitness")
    plt.plot(history_mean, label="Mean fitness")
    plt.title("GA on f(x) = sin(10x)*x + cos(2x)*x")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    plt.show()

    plt.figure()
    plt.plot(xs, ys, label="f(x)")
    plt.scatter(pop, [f(x) for x in pop], s=16, label="Final population")
    plt.scatter([best_x], [best_f], s=64, marker="x", label="Best")
    plt.title("Function and final population")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()