import pickle
import networkx as nx
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
import random
import csv
from genetic import genetic_blocking_strategy
from greedy import greedy_blocking_strategy
from helper import simulate_icm_spread

# Parameters
num_nodes = 100
edges_per_node = 2
k = 5
iterations = 10
runs = 100  # Number of times to run each strategy

# Initialize CSV
with open("strategy_results.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["strategy", "run", "iteration", "infected", "infected_nodes"])
    G_orig = nx.barabasi_albert_graph(num_nodes, edges_per_node)

    for run in range(1, runs + 1):
        # Random Blocking
        G = G_orig.copy()
        rand_nodes = random.sample(list(G.nodes()), k)
        G.remove_nodes_from(rand_nodes)
        [results,infected_set] = simulate_icm_spread(G, fraction_infected=0.05, probability=0.1, steps=iterations)
        for i, val in enumerate(results):
            writer.writerow(["random", run, i, val, ",".join(map(str, infected_set))])

        # High-Degree Blocking
        G = G_orig.copy()
        deg_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:k]
        G.remove_nodes_from([n for n, _ in deg_nodes])
        [results,infected_set] = simulate_icm_spread(G, fraction_infected=0.05, probability=0.1, steps=iterations)

        for i, val in enumerate(results):
            writer.writerow(["degree", run, i, val, ",".join(map(str, infected_set))])

        # High-Betweenness Blocking
        G = G_orig.copy()
        btw_nodes = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:k]
        G.remove_nodes_from([n for n, _ in btw_nodes])
        [results,infected_set] = simulate_icm_spread(G, fraction_infected=0.05, probability=0.1, steps=iterations)

        for i, val in enumerate(results):
            writer.writerow(["betweenness", run, i, val, ",".join(map(str, infected_set))])

        G = G_orig.copy()
        greedy_nodes = greedy_blocking_strategy(G, k)
        G.remove_nodes_from(greedy_nodes)
        [results,infected_set] = simulate_icm_spread(G, fraction_infected=0.05, probability=0.1, steps=iterations)

        for i, val in enumerate(results):
            writer.writerow(["greedy", run, i, val, ",".join(map(str, infected_set))])

        G = G_orig.copy()
        greedy_nodes = genetic_blocking_strategy(G, k)
        G.remove_nodes_from(greedy_nodes)
        [results,infected_set] = simulate_icm_spread(G, fraction_infected=0.05, probability=0.1, steps=iterations)

        for i, val in enumerate(results):
            writer.writerow(["genetic", run, i, val, ",".join(map(str, infected_set))])