import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from config import CONFIG
from helper import simulate_icm_spread
from base import genetic_blocking, random_blocking, degree_blocking, betweenness_blocking, greedy_blocking

# --- PARAMETERS TO SWEEP ---
blocking_percents = [0.1, 0.5, 1, 2, 5]  # Percentages of nodes to block
runs = 100
steps = 30
fraction_infected = 0.05
probability = 0.1

# --- LOAD NETWORK ---
G = nx.read_edgelist("facebook_combined.txt", nodetype=int)
Gcc = G.subgraph(max(nx.connected_components(G), key=len)).copy()
n_nodes = Gcc.number_of_nodes()
print(f"Largest component: {n_nodes} nodes, {Gcc.number_of_edges()} edges.")

# --- STRATEGY DEFS ---
strategies = {
    "random": random_blocking,
    "degree": degree_blocking,
    "betweenness": betweenness_blocking,
    "greedy": greedy_blocking,
    "genetic": lambda G, k: genetic_blocking(G, k, CONFIG["genetic_config"])
}

# --- MAIN LOOP OVER k VALUES ---
for percent in blocking_percents:
    k = max(1, int(round(percent * n_nodes / 100)))
    outdir = f"results_facebook_k{percent:.1f}pct"
    os.makedirs(outdir, exist_ok=True)

    CONFIG["k"] = k
    CONFIG["genetic_config"]["steps"] = steps

    means, stds = {}, {}
    all_results = {}

    result_lines = [f"\n==== Blocking {k} nodes ({percent:.1f}% of network, {n_nodes} nodes total) ====\n"]

    for name, func in strategies.items():
        print(f"\nRunning strategy: {name} (k={k})")
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
        mean, std = np.mean(total_infected), np.std(total_infected)
        means[name], stds[name] = mean, std
        all_results[name] = total_infected
        line = f"{name}: Mean infected = {mean:.2f} ± {std:.2f}"
        print(line)
        result_lines.append(line)

    # --- SAVE RESULTS TO TEXT FILE ---
    with open(os.path.join(outdir, "results.txt"), "w") as f:
        f.write("\n".join(result_lines))
        f.write("\n\nMeans:\n")
        f.write(str(means))
        f.write("\nStds:\n")
        f.write(str(stds))

    # --- SAVE PLOT ---
    plt.figure(figsize=(8,5))
    strategy_names = list(strategies.keys())
    bar_means = [means[s] for s in strategy_names]
    bar_stds = [stds[s] for s in strategy_names]
    plt.bar(strategy_names, bar_means, yerr=bar_stds, capsize=10, color='skyblue')
    plt.ylabel("Average Total Infected Nodes")
    plt.title(f"Blocking {k} Nodes ({percent:.1f}% of Facebook Network)")
    plt.tight_layout()
    plot_file = os.path.join(outdir, "blocking_comparison.png")
    plt.savefig(plot_file)
    plt.close()

    # --- SAVE RAW DATA ---
    for name in strategy_names:
        np.savetxt(os.path.join(outdir, f"{name}_infected_runs.csv"), all_results[name], delimiter=",")
