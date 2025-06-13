import pandas as pd
import matplotlib.pyplot as plt
import ast

# Load your results CSV
df = pd.read_csv("./results-ga/ga_hyperparameter_tuning_results.csv")

# Convert stringified lists back to Python objects
df['convergence'] = df['convergence'].apply(ast.literal_eval)

# Extract convergence of first trial from best config
best_convergence = df.iloc[0]['convergence'][0]

# Plot it
plt.figure(figsize=(10, 6))
plt.plot(best_convergence, marker='o')
plt.title("GA Convergence Over Generations")
plt.xlabel("Generation")
plt.ylabel("Best Fitness (negative spread)")
plt.grid(True)
plt.tight_layout()
plt.savefig("ga_convergence_plot.png")
plt.show()
