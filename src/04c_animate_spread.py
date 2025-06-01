import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import pickle

# Load the graph and infection data
G = pickle.load(open("graph.pkl", "rb"))  # Same graph used in simulation
df = pd.read_csv("strategy_results.csv")

# Choose strategy and run
strategy = "random"  # or 'random', 'degree'
run = 1
df_sub = df[(df["strategy"] == strategy) & (df["run"] == run)]

# Extract infection states per iteration
iterations = df_sub["iteration"].max() + 1
infected_by_iter = {i: set() for i in range(iterations)}

for i in range(iterations):
    infected_by_iter[i] = set(df_sub[df_sub["iteration"] == i]["infected_nodes"].dropna().sum().split(',')) if "infected_nodes" in df.columns else set()

# Position nodes
pos = nx.spring_layout(G, seed=42)

# Initialize plot
fig, ax = plt.subplots(figsize=(8, 6))

def update(i):
    ax.clear()
    infected = infected_by_iter.get(i, set())
    node_colors = ["red" if str(n) in infected else "lightgray" for n in G.nodes()]
    nx.draw(G, pos, node_color=node_colors, with_labels=False, node_size=80, ax=ax)
    ax.set_title(f"Infection Spread - {strategy.capitalize()} Strategy\nIteration {i}")
    ax.axis("off")

# Create animation
ani = animation.FuncAnimation(fig, update, frames=iterations, interval=800, repeat=False)

# Save animation
ani.save(f"infection_spread_{strategy}_run{run}.gif", writer="pillow")
plt.show()
