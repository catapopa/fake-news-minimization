import networkx as nx
import pickle
from config import CONFIG
from helper import simulate_icm_spread


def greedy_blocking_strategy(G, k, num_simulations=5, max_steps=10):
    """
    Selects k nodes to block using a greedy influence minimization approach.

    Args:
        G: networkx graph
        k: number of nodes to block
        num_simulations: number of ICM runs for estimating influence
        max_steps: maximum steps for each ICM run

    Returns:
        blocked_nodes: list of k selected nodes
    """
    blocked_nodes = set()
    all_nodes = set(G.nodes())

    for _ in range(k):
        best_node = None
        best_reduction = float('-inf')

        candidates = all_nodes - blocked_nodes
        for candidate in candidates:
            temp_blocked = blocked_nodes | {candidate}

            # Create a copy of the graph with blocked nodes removed
            G_blocked = G.copy()
            G_blocked.remove_nodes_from(temp_blocked)

            # Estimate influence
            total_infected = 0
            for _ in range(num_simulations):
                infected, _ = simulate_icm_spread(G_blocked, steps=max_steps)
                total_infected += sum(infected)
            avg_infected = total_infected / num_simulations

            if avg_infected < best_reduction or best_node is None:
                best_reduction = avg_infected
                best_node = candidate

        blocked_nodes.add(best_node)
        print(f"Selected node {best_node} for blocking (expected infections: {best_reduction:.2f})")

    return list(blocked_nodes)


# Example usage
if __name__ == "__main__":
    G = pickle.load(open("graph.pkl", "rb"))
    k = CONFIG["k"] 
    selected_nodes = greedy_blocking_strategy(G, k)
    print("Blocked nodes:", selected_nodes)
