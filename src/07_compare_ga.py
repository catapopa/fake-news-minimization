import matplotlib.pyplot as plt
import pickle
from helper import simulate_icm_spread
import copy
import numpy as np

# Load graph and GA-selected nodes
G = pickle.load(open("graph.pkl", "rb"))

blocked_nodes = [0, 69, 70, 9, 81]

G_blocked = copy.deepcopy(G)
G_blocked.remove_nodes_from(blocked_nodes)

# Run multiple simulations and collect totals
n_runs = 1000
original_totals = []
blocked_totals = []

for _ in range(n_runs):
    infected_counts_original, _ = simulate_icm_spread(G)
    infected_counts_blocked, _ = simulate_icm_spread(G_blocked)
    original_totals.append(sum(infected_counts_original))
    blocked_totals.append(sum(infected_counts_blocked))

# Calculate means and stds
mean_original = np.mean(original_totals)
std_original = np.std(original_totals)
mean_blocked = np.mean(blocked_totals)
std_blocked = np.std(blocked_totals)

# Print results
print("Original mean:", mean_original, "std:", std_original)
print("Blocked mean:", mean_blocked, "std:", std_blocked)

# Plot bar chart with error bars
plt.figure(figsize=(6, 5))
plt.bar(["Original", "After Blocking"], [mean_original, mean_blocked], 
        yerr=[std_original, std_blocked], color=["skyblue", "salmon"], capsize=10)
plt.title("Average Total Infections Over {} Runs".format(n_runs))
plt.ylabel("Total Infected Nodes")
plt.tight_layout()
plt.savefig("total_infections_comparison_avg.png")
plt.show()