import random
import networkx as nx
from helper import simulate_icm_spread_total
import copy
import pickle
import matplotlib.pyplot as plt

def evaluate_fitness(G, candidate, steps=30, runs=5):
    total = 0
    for _ in range(runs):
        G_copy = copy.deepcopy(G)
        G_copy.remove_nodes_from(candidate)
        infected = simulate_icm_spread_total(G_copy, steps=steps)
        total += len(infected)
    return -total / runs


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

def genetic_blocking_strategy(G, k, config, plot=True):
    pop_size = config.get("pop_size", 30)
    generations = config.get("generations", 50)
    mutation_rate = config.get("mutation_rate", 0.1)
    tournament_size = config.get("tournament_size", 3)
    elitism_count = config.get("elitism_count", 1)
    steps = config.get("steps", 30)

    population = initialize_population(G, k, pop_size)
    best_fitnesses = []

    for gen in range(generations):
        fitnesses = [evaluate_fitness(G, indiv, steps=steps) for indiv in population]

        # Save best fitness for convergence plot
        best_fitnesses.append(max(fitnesses))

        new_pop = []

        # Elitism
        elites = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)[:elitism_count]
        new_pop.extend([indiv for indiv, _ in elites])

        while len(new_pop) < pop_size:
            p1 = select_parents(population, fitnesses, tournament_size)
            p2 = select_parents(population, fitnesses, tournament_size)
            child = crossover(p1, p2)
            child = mutate(child, G, mutation_rate)
            new_pop.append(child)

        population = new_pop

    best_individual = max(population, key=lambda indiv: evaluate_fitness(G, indiv, steps=steps))
    print(f"Best fitness: {best_individual}")
    if plot:
        plt.figure(figsize=(10, 5))
        plt.plot(best_fitnesses, marker="o")
        plt.title("Genetic Algorithm Convergence")
        plt.xlabel("Generation")
        plt.ylabel("Best Fitness (negative spread)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("ga_convergence_plot.png")
        plt.show()

    return best_individual

if __name__ == "__main__":
    G = pickle.load(open("graph.pkl", "rb"))
    k = 5

    # config = {
    #     "pop_size": 50,
    #     "generations": 100,
    #     "mutation_rate": 0.1,
    #     "tournament_size": 3,
    #     "elitism_count": 2,
    #     "steps": 30
    # }

    config = {
        'pop_size': 20,
        'generations': 30,
        'mutation_rate': 0.1,
        'tournament_size': 5,
        'elitism_count': 1,
        'steps': 30
    }

    selected_nodes = genetic_blocking_strategy(G, k, config)
    print("Blocked nodes by GA:", selected_nodes)
