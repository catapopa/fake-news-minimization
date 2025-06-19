import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time

import pandas as pd
from config import CONFIG
from helper import simulate_icm_spread
from base import genetic_blocking, random_blocking, degree_blocking, betweenness_blocking, greedy_blocking

# Load the real Facebook network
G = nx.read_edgelist("facebook_combined.txt", nodetype=int)
Gcc = G.subgraph(max(nx.connected_components(G), key=len)).copy()

budgets = [5, 40, 80]
probabilities = [0.1, 0.2, 0.3]

results = {}  # {(k, p): {strategy: (mean, std, runtime)}}

strategies = {
    "random": random_blocking,
    "degree": degree_blocking,
    "betweenness": betweenness_blocking,
    "greedy": greedy_blocking,
    "genetic": lambda G, k: genetic_blocking(G, k, CONFIG["genetic_config"])
}

runs = 100
fraction_infected = 0.1
steps = 30

for k in budgets:
    for p in probabilities:
        scenario_key = (k, p)
        results[scenario_key] = {}
        print(f"\n--- Running scenario: k={k}, p={p} ---")
        for name, func in strategies.items():
            print(f"  Running strategy: {name}")
            Gtemp = Gcc.copy()
            t0 = time.time()
            nodes_to_remove = func(Gtemp, k)
            Gtemp.remove_nodes_from(nodes_to_remove)
            total_infected = []
            for _ in range(runs):
                infected_counts, _ = simulate_icm_spread(
                    Gtemp,
                    fraction_infected=fraction_infected,
                    probability=p,
                    steps=steps
                )
                total_infected.append(sum(infected_counts))
            t1 = time.time()
            mean = np.mean(total_infected)
            std = np.std(total_infected)
            runtime = t1 - t0
            results[scenario_key][name] = (mean, std, runtime)
            print(f"    {name}: Mean infected = {mean:.2f} ± {std:.2f}, Time = {runtime:.2f} seconds")

# Plotting: For each p, show a grouped bar chart for all k, all strategies
for p in probabilities:
    plt.figure(figsize=(10,6))
    bar_width = 0.18
    x = np.arange(len(budgets))
    for i, strat in enumerate(strategies.keys()):
        means = [results[(k, p)][strat][0] for k in budgets]
        stds = [results[(k, p)][strat][1] for k in budgets]
        plt.bar(x + i*bar_width, means, bar_width, yerr=stds, capsize=5, label=strat.capitalize())
    plt.xticks(x + bar_width*2, [f'k={k}' for k in budgets])
    plt.xlabel("Blocking Budget (k)")
    plt.ylabel("Average Total Infected Nodes")
    plt.title(f"Blocking Strategies on Facebook Network (p={p})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"real_network_blocking_comparison_p{p}.png")
    plt.show()

summary_rows = []
for (k, p), strat_results in results.items():
    for name, vals in strat_results.items():
        summary_rows.append({
            "k": k,
            "p": p,
            "strategy": name,
            "mean_infected": vals[0],
            "std_infected": vals[1],
            "runtime_seconds": vals[2]
        })
df_summary = pd.DataFrame(summary_rows)
df_summary.to_csv("real_network_blocking_results_summary.csv", index=False)