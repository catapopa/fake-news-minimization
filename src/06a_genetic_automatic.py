import itertools
import pickle
import pandas as pd
import time
import matplotlib.pyplot as plt
from genetic import crossover, initialize_population, mutate, select_parents
from helper import simulate_icm_spread_total_custom


def evaluate_fitness(G, node_set, n_runs=5):
    results = [simulate_icm_spread_total_custom(G, node_set) for _ in range(n_runs)]
    return -sum(results) / len(results)


def genetic_blocking_strategy(G, k, generations, pop_size, mutation_rate, elitism_count, tournament_size):
    population = initialize_population(G, k, pop_size)
    best_fitnesses = []
    mean_fitnesses = []

    for gen in range(generations):
        fitnesses = [evaluate_fitness(G, indiv) for indiv in population]
        best_fitness = max(fitnesses)
        mean_fitness = sum(fitnesses) / len(fitnesses)

        best_fitnesses.append(best_fitness)
        mean_fitnesses.append(mean_fitness)

        new_pop = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)[:elitism_count]

        while len(new_pop) < pop_size:
            p1 = select_parents(population, fitnesses, tournament_size)
            p2 = select_parents(population, fitnesses, tournament_size)
            child = crossover(p1, p2)
            child = mutate(child, G, mutation_rate)
            new_pop.append((child, evaluate_fitness(G, child)))

        population = [ind for ind, fit in new_pop]

        if len(best_fitnesses) > 10 and all(f == best_fitnesses[-1] for f in best_fitnesses[-10:]):
            print(f"Early stopping at generation {gen} (fitness plateau)")
            break

    best = max(population, key=lambda indiv: evaluate_fitness(G, indiv))
    best_fitness = evaluate_fitness(G, best)

    return best, best_fitness, best_fitnesses, mean_fitnesses


if __name__ == "__main__":
    G = pickle.load(open("graph.pkl", "rb"))
    k = 5
    trials_per_combo = 3

    param_grid = {
        'generations': [100, 150],
        'pop_size': [40, 60],
        'mutation_rate': [0.2, 0.3],
        'elitism_count': [1, 2],
        'tournament_size': [3, 5]
    }

    keys = param_grid.keys()
    all_combos = list(itertools.product(*param_grid.values()))
    results = []

    for idx, combo in enumerate(all_combos):
        combo_dict = dict(zip(keys, combo))
        fitness_scores = []
        top_individuals = []
        convergence_data = []
        convergence_means = []
        start_time = time.time()

        for _ in range(trials_per_combo):
            best_nodes, fitness, best_fit_list, mean_fit_list = genetic_blocking_strategy(G, k, **combo_dict)
            fitness_scores.append(fitness)
            top_individuals.append(best_nodes)
            convergence_data.append(best_fit_list)
            convergence_means.append(mean_fit_list)

        avg_fitness = sum(fitness_scores) / len(fitness_scores)
        std_fitness = pd.Series(fitness_scores).std()
        elapsed = time.time() - start_time

        combo_dict.update({
            "avg_fitness": avg_fitness,
            "std_fitness": std_fitness,
            "top_nodes": top_individuals,
            "convergence": convergence_data,
            "mean_convergence": convergence_means,
            "time_sec": elapsed
        })

        results.append(combo_dict)
        print(f"[{idx+1}/{len(all_combos)}] Config: {combo_dict}, Time: {elapsed:.2f}s")

    df = pd.DataFrame(results)
    df = df.sort_values(by="avg_fitness", ascending=False)
    df.to_csv("ga_improved_avg_fitness_results_a.csv", index=False)

    print("Top configurations:")
    print(df.head(5))

    best_convergence = df.iloc[0]['convergence'][0]
    worst_convergence = df.iloc[-1]['convergence'][0]
    best_mean = df.iloc[0]['mean_convergence'][0]
    worst_mean = df.iloc[-1]['mean_convergence'][0]

    plt.figure(figsize=(12, 6))
    plt.plot(best_convergence, marker='o', label='Best Fitness (Best Config)')
    plt.plot(best_mean, linestyle='--', label='Mean Fitness (Best Config)')
    plt.plot(worst_convergence, marker='x', label='Best Fitness (Worst Config)', alpha=0.6)
    plt.plot(worst_mean, linestyle='--', label='Mean Fitness (Worst Config)', alpha=0.6)
    plt.title("Improved GA Convergence: Best vs Worst Config")
    plt.xlabel("Generation")
    plt.ylabel("Fitness (lower = better)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("ga_improved_convergence_plot_a.png")
    plt.show()
