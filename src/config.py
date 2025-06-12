CONFIG = {
    "num_nodes": 100,
    "edges_per_node": 2,
    "k": 5,
    "iterations": 10,
    "runs": 100,
    "fraction_infected": 0.05,
    "probability": 0.1,
    "strategies": ["random", "degree", "betweenness", "greedy", "genetic"],
    "output_file": "strategy_results.csv",
    "genetic_config": {
        'pop_size': 40,
        'generations': 100,
        'mutation_rate': 0.3,
        'tournament_size': 5,
        'elitism_count': 1,
        'steps': 30
    }
}