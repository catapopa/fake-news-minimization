import networkx as nx
import csv
from base import betweenness_blocking, degree_blocking, genetic_blocking, greedy_blocking, random_blocking
from helper import simulate_icm_spread
import sys
import os

def run_batch(config):
    with open("strategy_results.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["strategy", "run", "iteration", "infected", "infected_nodes"])

        for run in range(config["runs"]):
            G_orig = nx.barabasi_albert_graph(config["num_nodes"], config["edges_per_node"])
            for strategy_name in config["strategies"]:
                G = G_orig.copy()
                nodes_to_remove = STRATEGY_FUNCTIONS[strategy_name](G, config["k"])
                G.remove_nodes_from(nodes_to_remove)
                results, infected_set = simulate_icm_spread(
                    G,
                    fraction_infected=config["fraction_infected"],
                    probability=config["probability"],
                    steps=config["iterations"]
                )
                for i, val in enumerate(results):
                    writer.writerow([
                        strategy_name,
                        run,
                        i,
                        val,
                        ",".join(map(str, infected_set[i]))
                    ])

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from config import CONFIG as config

    # Define strategies
    STRATEGY_FUNCTIONS = {
        "random": lambda G, k: random_blocking(G, k),
        "degree": lambda G, k: degree_blocking(G, k),
        "betweenness": lambda G, k: betweenness_blocking(G, k),
        "greedy": lambda G, k: greedy_blocking(G, k),
        "genetic": lambda G, k: genetic_blocking(G, k, config["genetic_config"])
    }

    # Run batch processing
    run_batch(config)