import networkx as nx
import matplotlib.pyplot as plt
import pickle
from config import CONFIG

# Create a scale-free network
num_nodes = CONFIG["num_nodes"] 
edges_per_node = CONFIG["edges_per_node"]
G = nx.barabasi_albert_graph(num_nodes, edges_per_node)

with open("graph.pkl", "wb") as f:
    pickle.dump(G, f)

# Visualize the graph
plt.figure(figsize=(8, 6))
nx.draw(G, node_size=30, with_labels=False)
plt.title("Barabási–Albert Scale-Free Network")
plt.savefig("graph.png")
plt.show()