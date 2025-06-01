import networkx as nx
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
import matplotlib.pyplot as plt
import pickle
from helper import simulate_icm_spread

# This script simulates the Independent Cascade Model (ICM) on a Barabási–Albert scale-free network
# and blocks the top-k high-degree nodes to minimize influence spread.
# High-Degree Node Blocking Strategy

# Load the graph
G = pickle.load(open("graph.pkl", "rb"))

# Block top-k high-degree nodes
k = 5
degrees = sorted(G.degree, key=lambda x: x[1], reverse=True)
nodes_to_block = [node for node, _ in degrees[:k]]
G.remove_nodes_from(nodes_to_block)

infected_counts = simulate_icm_spread(G)

# Plot results
plt.plot(infected_counts, marker='o', label=f'Blocked {k} nodes')
plt.xlabel("Iteration")
plt.ylabel("Number of Infected Nodes")
plt.title("Influence Minimization (High-Degree Node Blocking)")
plt.grid(True)
plt.legend()
plt.savefig("influence_min_baseline.png")
plt.show()