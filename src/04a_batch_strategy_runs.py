import pickle
import networkx as nx
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
import random
import csv
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
    writer.writerow(["strategy", "run", "iteration", "infected"])

    for run in range(1, runs + 1):
        # Random Blocking
        G = nx.barabasi_albert_graph(num_nodes, edges_per_node)
        rand_nodes = random.sample(list(G.nodes()), k)
        G.remove_nodes_from(rand_nodes)
        results = simulate_icm_spread(G, fraction_infected=0.05, probability=0.1, steps=iterations)
        for i, val in enumerate(results):
            writer.writerow(["random", run, i, val])

        # High-Degree Blocking
        G = nx.barabasi_albert_graph(num_nodes, edges_per_node)
        deg_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:k]
        G.remove_nodes_from([n for n, _ in deg_nodes])
        results = simulate_icm_spread(G, fraction_infected=0.05, probability=0.1, steps=iterations)

        for i, val in enumerate(results):
            writer.writerow(["degree", run, i, val])

        # High-Betweenness Blocking
        G = nx.barabasi_albert_graph(num_nodes, edges_per_node)
        btw_nodes = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:k]
        G.remove_nodes_from([n for n, _ in btw_nodes])
        results = simulate_icm_spread(G, fraction_infected=0.05, probability=0.1, steps=iterations)

        for i, val in enumerate(results):
            writer.writerow(["betweenness", run, i, val])