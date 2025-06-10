import random
import networkx as nx
from helper import simulate_icm_spread
import copy
import pickle

def evaluate_fitness(G, candidate, steps=30):
    G_copy = copy.deepcopy(G)
    G_copy.remove_nodes_from(candidate)
    infected, _ = simulate_icm_spread(G_copy, steps=steps)
    return -sum(infected)  # Lower spread = better

def initialize_population(G, k, pop_size):
    nodes = list(G.nodes())
    return [random.sample(nodes, k) for _ in range(pop_size)]

def crossover(parent1, parent2):
    child = list(set(parent1[:len(parent1)//2] + parent2[len(parent2)//2:]))
    while len(child) < len(parent1):
        new_node = random.choice(list(set(parent1 + parent2) - set(child)))
        child.append(new_node)
    return child

def mutate(chromosome, G, mutation_rate=0.2):
    if random.random() < mutation_rate:
        idx = random.randint(0, len(chromosome) - 1)
        remaining = list(set(G.nodes()) - set(chromosome))
        if remaining:
            chromosome[idx] = random.choice(remaining)
    return chromosome

def select_parents(population, fitnesses, tournament_size=3):
    selected = random.sample(list(zip(population, fitnesses)), tournament_size)
    return max(selected, key=lambda x: x[1])[0]

def genetic_blocking_strategy(G, k, generations=30, pop_size=20):
    population = initialize_population(G, k, pop_size)
    for _ in range(generations):
        fitnesses = [evaluate_fitness(G, indiv) for indiv in population]
        new_pop = []
        for _ in range(pop_size):
            p1 = select_parents(population, fitnesses)
            p2 = select_parents(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, G)
            new_pop.append(child)
        population = new_pop
    best = max(population, key=lambda indiv: evaluate_fitness(G, indiv))
    return best

if __name__ == "__main__":
    G = pickle.load(open("graph.pkl", "rb"))
    k = 5
    selected_nodes = genetic_blocking_strategy(G, k)
    print("Blocked nodes:", selected_nodes)