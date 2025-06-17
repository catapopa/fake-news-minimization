import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from config import CONFIG
from helper import simulate_icm_spread
from base import genetic_blocking, random_blocking, degree_blocking, betweenness_blocking, greedy_blocking

# Load the real Facebook network
G = nx.read_edgelist("facebook_combined.txt", nodetype=int)
print(f"Loaded Facebook network with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

# Optionally, use only the largest connected component
Gcc = G.subgraph(max(nx.connected_components(G), key=len)).copy()
print(f"Largest component: {Gcc.number_of_nodes()} nodes.")

# Set parameters for simulation
k = 5  # blocking budget
fraction_infected = 0.05
probability = 0.1
runs = 100
steps = 30

# Define strategies
strategies = {
    "random": random_blocking,
    "degree": degree_blocking,
    "betweenness": betweenness_blocking,
    "greedy": greedy_blocking,
    "genetic": lambda G, k: genetic_blocking(G, k, CONFIG["genetic_config"])
}

# Collect results
results = {}
for name, func in strategies.items():
    print(f"Running strategy: {name}")
    Gtemp = Gcc.copy()
    nodes_to_remove = func(Gtemp, k)
    Gtemp.remove_nodes_from(nodes_to_remove)
    total_infected = []
    for _ in range(runs):
        infected_counts, _ = simulate_icm_spread(
            Gtemp,
            fraction_infected=fraction_infected,
            probability=probability,
            steps=steps
        )
        total_infected.append(sum(infected_counts))
    results[name] = (np.mean(total_infected), np.std(total_infected))
    print(f"{name}: Mean infected = {results[name][0]:.2f} ± {results[name][1]:.2f}")

# Plot
plt.figure(figsize=(7,5))
means = [results[s][0] for s in strategies]
stds = [results[s][1] for s in strategies]
plt.bar(list(strategies.keys()), means, yerr=stds, capsize=10, color='skyblue')
plt.ylabel("Average Total Infected Nodes")
plt.title("Blocking Strategies on Real Facebook Network")
plt.tight_layout()
plt.savefig("real_network_blocking_comparison.png")
plt.show()
