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