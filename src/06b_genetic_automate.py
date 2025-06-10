import itertools
import random
import pickle
import copy
from helper import simulate_icm_spread
import pandas as pd
import networkx as nx

# --- GA components from previous code ---
def evaluate_fitness(G, candidate, steps=30):
    G_copy = copy.deepcopy(G)
    G_copy.remove_nodes_from(candidate)
    infected, _ = simulate_icm_spread(G_copy, steps=steps)
    return -sum(infected)

def initialize_population(G, k, pop_size):
    nodes = list(G.nodes())
    return [random.sample(nodes, k) for _ in range(pop_size)]

def crossover(parent1, parent2):
    child = list(set(parent1[:len(parent1)//2] + parent2[len(parent2)//2:]))
    while len(child) < len(parent1):
        new_node = random.choice(list(set(parent1 + parent2) - set(child)))
        child.append(new_node)
    return child

def mutate(chromosome, G, mutation_rate):
    if random.random() < mutation_rate:
        idx = random.randint(0, len(chromosome) - 1)
        remaining = list(set(G.nodes()) - set(chromosome))
        if remaining:
            chromosome[idx] = random.choice(remaining)
    return chromosome

def select_parents(population, fitnesses, tournament_size):
    selected = random.sample(list(zip(population, fitnesses)), tournament_size)
    return max(selected, key=lambda x: x[1])[0]

def genetic_blocking_strategy(G, k, generations, pop_size, mutation_rate, elitism_count, tournament_size):
    population = initialize_population(G, k, pop_size)
    for _ in range(generations):
        fitnesses = [evaluate_fitness(G, indiv) for indiv in population]
        new_pop = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)[:elitism_count]
        elites = [ind for ind, fit in new_pop]

        while len(new_pop) < pop_size:
            p1 = select_parents(population, fitnesses, tournament_size)
            p2 = select_parents(population, fitnesses, tournament_size)
            child = crossover(p1, p2)
            child = mutate(child, G, mutation_rate)
            new_pop.append((child, evaluate_fitness(G, child)))

        population = [ind for ind, fit in new_pop]
    best = max(population, key=lambda indiv: evaluate_fitness(G, indiv))
    return best, evaluate_fitness(G, best)

# --- Grid Search ---
if __name__ == "__main__":
    G = pickle.load(open("graph.pkl", "rb"))
    k = 5
    trials_per_combo = 3

    param_grid = {
        'generations': [20, 30],
        'pop_size': [20, 30],
        'mutation_rate': [0.1, 0.3],
        'elitism_count': [1, 2],
        'tournament_size': [3, 5]
    }

    keys = param_grid.keys()
    all_combos = list(itertools.product(*param_grid.values()))
    results = []

    for combo in all_combos:
        combo_dict = dict(zip(keys, combo))
        fitness_scores = []
        for _ in range(trials_per_combo):
            _, fitness = genetic_blocking_strategy(G, k, **combo_dict)
            fitness_scores.append(fitness)
        avg_fitness = sum(fitness_scores) / len(fitness_scores)
        combo_dict["avg_fitness"] = avg_fitness
        results.append(combo_dict)
        print(f"Tested {combo_dict}")

    # Save and sort results
    df = pd.DataFrame(results)
    df = df.sort_values(by="avg_fitness", ascending=False)
    df.to_csv("ga_hyperparameter_tuning_results.csv", index=False)
    print("Top configurations:")
    print(df.head(5))
