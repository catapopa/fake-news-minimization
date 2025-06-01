import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import pickle
import ast

# Load the graph and infection data
G = pickle.load(open("graph.pkl", "rb"))  # Same graph used in simulation
df = pd.read_csv("strategy_results.csv", quotechar='"')

# Choose strategy and run
strategy = "degree"  # or 'random', 'degree', 'betweenness'
run = 1
df_sub = df[(df["strategy"] == strategy) & (df["run"] == run)]

# Extract infection states per iteration
infected_by_iter = {}

subset = df_sub[df_sub["iteration"] == 0]
if subset.empty:
    print(f"No data found for strategy='{strategy}', run={run}, iteration=0")
    exit()
row = subset.iloc[0]


# Get the infected_nodes list from the correct row (iteration 0 stores the full spread)
row = df_sub[df_sub["iteration"] == 0].iloc[0]
infected_str = row["infected_nodes"]

# Safely parse the string into a list of lists
try:
    infected_lists = ast.literal_eval(f"[{infected_str}]")
    for i, lst in enumerate(infected_lists):
        infected_by_iter[i] = set(lst)
except Exception as e:
    print(f"Parsing error: {e}")

# Total number of iterations
iterations = len(infected_by_iter)

# Node positions
pos = nx.spring_layout(G, seed=42)

# Initialize plot
fig, ax = plt.subplots(figsize=(8, 6))

def update(i):
    ax.clear()
    infected = infected_by_iter.get(i, set())
    node_colors = ["red" if n in infected else "lightgray" for n in G.nodes()]
    nx.draw(G, pos, node_color=node_colors, with_labels=False, node_size=80, ax=ax)
    ax.set_title(f"Infection Spread - {strategy.capitalize()} Strategy\nIteration {i}")
    ax.axis("off")

# Animate
ani = animation.FuncAnimation(fig, update, frames=iterations, interval=800, repeat=False)

# Save and show
ani.save(f"infection_spread_{strategy}_run{run}.gif", writer="pillow")
plt.show()
