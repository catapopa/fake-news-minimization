import networkx as nx
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
import matplotlib.pyplot as plt
import random
import pickle
from helper import simulate_icm_spread

# This script compares different strategies for blocking nodes in a Barabási–Albert scale-free network
# Random Blocking — baseline noise
# High-Degree Blocking — from Step 3
# High Betweenness Blocking — more strategic, finds nodes that act as bridges

# Load the graph
G = pickle.load(open("graph.pkl", "rb"))

k = 5  # number of nodes to block
iterations = 30

# Strategy 1: Random Blocking
G1 = G.copy()
random_nodes = random.sample(list(G1.nodes()), k)
G1.remove_nodes_from(random_nodes)
result_random = simulate_icm_spread(G1)

# Strategy 2: High-Degree Blocking
G2 = G.copy()
degrees = sorted(G2.degree, key=lambda x: x[1], reverse=True)
degree_nodes = [n for n, _ in degrees[:k]]
G2.remove_nodes_from(degree_nodes)
result_degree = simulate_icm_spread(G2)

# Strategy 3: High-Betweenness Blocking
G3 = G.copy()
betweenness = nx.betweenness_centrality(G3)
betweenness_nodes = sorted(betweenness, key=betweenness.get, reverse=True)[:k]
G3.remove_nodes_from(betweenness_nodes)
result_betweenness = simulate_icm_spread(G3)

# Plot comparison
plt.plot(result_random, label="Random", linestyle='--', marker='o')
plt.plot(result_degree, label="High Degree", linestyle='-', marker='s')
plt.plot(result_betweenness, label="High Betweenness", linestyle='-.', marker='^')
plt.xlabel("Iteration")
plt.ylabel("Infected Nodes")
plt.title(f"Spread Reduction with {k} Blocked Nodes")
plt.legend()
plt.grid(True)
plt.savefig("compare_blocking_strategies.png")
plt.show()