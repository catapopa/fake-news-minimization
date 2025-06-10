import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import matplotlib.animation as animation

# GRAPHICS SETTINGS
df = pd.read_csv("strategy_results.csv")

# Sum infected nodes across all iterations per run
summary = df.groupby(["strategy", "run"])["infected"].sum().reset_index()

# Compute average and std deviation for each strategy
avg_summary = summary.groupby("strategy")["infected"].agg(["mean", "std"]).reset_index()

print("Average infections per strategy:")
print(avg_summary)

# Boxplot: Total infected nodes per strategy across runs
plt.figure(figsize=(10, 6))
sns.boxplot(data=summary, x="strategy", y="infected", hue="strategy", palette="Set2", legend=False)
plt.title("Total Infected Nodes per Strategy (All Iterations)")
plt.xlabel("Strategy")
plt.ylabel("Total Infected Nodes per Run")
plt.tight_layout()
plt.savefig("strategy_comparison_boxplot.png")
plt.show()

# Optional: Lineplot of average infection progression per strategy
iteration_avg = df.groupby(["strategy", "iteration"])["infected"].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(data=iteration_avg, x="iteration", y="infected", hue="strategy", marker="o")
plt.title("Average Infection Spread Over Iterations")
plt.xlabel("Iteration")
plt.ylabel("Average Number of Infected Nodes")
plt.tight_layout()
plt.savefig("infection_progression_lineplot.png")
plt.show()

# Violin Plots or Swarm Plots
plt.figure(figsize=(10, 6))
sns.violinplot(data=summary, x="strategy", y="infected", palette="Set2", inner="box")
plt.title("Distribution of Total Infections per Strategy")
plt.tight_layout()
plt.savefig("strategy_violinplot.png")
plt.show()

from scipy.stats import kruskal

# Kruskal-Wallis H-test to compare strategies
strategies = summary["strategy"].unique()
samples = [summary[summary["strategy"] == s]["infected"] for s in strategies]
stat, p = kruskal(*samples)
print(f"Kruskal-Wallis H-test: H={stat:.3f}, p-value={p:.3e}")

# If p-value < 0.05, we can conclude that at least one strategy is significantly different
plt.figure(figsize=(10, 6))
for strategy, group in df.groupby("strategy"):
    avg = group.groupby("iteration")["infected"].mean()
    std = group.groupby("iteration")["infected"].std()
    plt.plot(avg.index, avg.values, label=strategy)
    plt.fill_between(avg.index, avg - std, avg + std, alpha=0.2)
plt.title("Infection Spread with Standard Deviation")
plt.xlabel("Iteration")
plt.ylabel("Infected Nodes")
plt.legend()
plt.tight_layout()
plt.savefig("infection_spread_std.png")
plt.show()
