import networkx as nx
import csv
import os
from base import betweenness_blocking, degree_blocking, genetic_blocking, greedy_blocking, random_blocking
from helper import simulate_icm_spread
import time

# Define strategy functions
STRATEGY_FUNCTIONS = {
    "random": random_blocking,
    "degree": degree_blocking,
    "betweenness": betweenness_blocking,
    "greedy": greedy_blocking,
    "genetic": lambda G, k: genetic_blocking(G, k, config["genetic_config"])
}

# List of experiment configurations
EXPERIMENTS = [
    {"name": "results_BA_prob0.1_frac0.05_k5", "graph": "BA", "n": 100, "probability": 0.1, "fraction_infected": 0.05, "k": 5},
    {"name": "results_BA_prob0.05_frac0.05_k5", "graph": "BA", "n": 100, "probability": 0.05, "fraction_infected": 0.05, "k": 5},
    {"name": "results_BA_prob0.2_frac0.05_k5", "graph": "BA", "n": 100, "probability": 0.2, "fraction_infected": 0.05, "k": 5},
    {"name": "results_BA_prob0.1_frac0.01_k5", "graph": "BA", "n": 100, "probability": 0.1, "fraction_infected": 0.01, "k": 5},
    {"name": "results_BA_prob0.1_frac0.1_k5", "graph": "BA", "n": 100, "probability": 0.1, "fraction_infected": 0.1, "k": 5},
    {"name": "results_BA_prob0.1_frac0.05_k3", "graph": "BA", "n": 100, "probability": 0.1, "fraction_infected": 0.05, "k": 3},
    {"name": "results_BA_prob0.1_frac0.05_k10", "graph": "BA", "n": 100, "probability": 0.1, "fraction_infected": 0.05, "k": 10},
    {"name": "results_WS_prob0.1_frac0.05_k5", "graph": "WS", "n": 100, "probability": 0.1, "fraction_infected": 0.05, "k": 5},
    {"name": "results_ER_prob0.1_frac0.05_k5", "graph": "ER", "n": 100, "probability": 0.1, "fraction_infected": 0.05, "k": 5},
    {"name": "results_BA_prob0.1_frac0.05_k5_large", "graph": "BA", "n": 500, "probability": 0.1, "fraction_infected": 0.05, "k": 5},
    {"name": "results_BA_prob0.1_frac0.05_k10_large", "graph": "BA", "n": 500, "probability": 0.1, "fraction_infected": 0.05, "k": 10},
]

# Default configuration
config = {
    "iterations": 30,
    "runs": 50,
    "strategies": ["random", "degree", "betweenness", "greedy", "genetic"],
    "genetic_config": {
        'generations': 100,
        'pop_size': 40,
        'mutation_rate': 0.1,
        'tournament_size': 3,
        'elitism_count': 1,
        'steps': 30
    }
}

def generate_graph(exp):
    if exp["graph"] == "BA":
        return nx.barabasi_albert_graph(exp["n"], 2)
    elif exp["graph"] == "WS":
        return nx.watts_strogatz_graph(exp["n"], 4, 0.1)
    elif exp["graph"] == "ER":
        return nx.erdos_renyi_graph(exp["n"], 0.05)
    else:
        raise ValueError("Unknown graph type")

def run_experiment(exp):
    output_dir = exp["name"]
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "strategy_results_multiple.csv")

    with open(output_file, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["strategy", "run", "iteration", "infected", "infected_nodes"])

        for run in range(config["runs"]):
            G_orig = generate_graph(exp)
            for strategy in config["strategies"]:
                G = G_orig.copy()
                nodes_to_remove = STRATEGY_FUNCTIONS[strategy](G, exp["k"])
                G.remove_nodes_from(nodes_to_remove)

                infected_counts, infected_nodes = simulate_icm_spread(
                    G,
                    fraction_infected=exp["fraction_infected"],
                    probability=exp["probability"],
                    steps=config["iterations"]
                )

                for i, count in enumerate(infected_counts):
                    writer.writerow([
                        strategy, run, i, count, ",".join(map(str, infected_nodes[i]))
                    ])

if __name__ == "__main__":
    for exp in EXPERIMENTS:
        print(f"Running {exp['name']}...")
        start = time.time()
        run_experiment(exp)
        print(f"Finished in {time.time() - start:.2f} seconds.")
