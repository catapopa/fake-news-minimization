import matplotlib.pyplot as plt
import pickle
from helper import simulate_icm_spread
import copy

# Load graph and GA-selected nodes
G = pickle.load(open("graph.pkl", "rb"))
blocked_nodes = [0, 90, 27, 96, 10]  # Replace with actual best nodes from GA

# Simulate spread on original graph
infected_counts_original, _ = simulate_icm_spread(G, probability=0.3)

# Simulate spread on graph with blocked nodes
G_blocked = copy.deepcopy(G)
G_blocked.remove_nodes_from(blocked_nodes)
infected_counts_blocked, _ = simulate_icm_spread(G_blocked, probability=0.3)

print("Infected counts (original):", infected_counts_original)
print("Infected counts (after blocking):", infected_counts_blocked)
print("Blocked nodes:", blocked_nodes)
# Plotting
plt.figure(figsize=(10, 5))
plt.plot(infected_counts_original, label="Original", marker='o')
plt.plot(infected_counts_blocked, label="After Blocking", marker='s')
plt.title("ICM Spread Over Time")
plt.xlabel("Steps")
plt.ylabel("Infected Nodes")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("spread_comparison_plot.png")
plt.show()

total_original = sum(infected_counts_original)
total_blocked = sum(infected_counts_blocked)

plt.bar(["Original", "After Blocking"], [total_original, total_blocked], color=["skyblue", "salmon"])
plt.title("Total Infections Comparison")
plt.ylabel("Total Infected Nodes")
plt.tight_layout()
plt.savefig("total_infections_comparison.png")
plt.show()