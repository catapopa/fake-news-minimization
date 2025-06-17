import os
import pandas as pd
import matplotlib.pyplot as plt

strategies = ['random', 'degree', 'betweenness', 'greedy', 'genetic']
ps = [0.05, 0.1, 0.2]
final_results = {s: [] for s in strategies}
print("Current working directory:", os.getcwd())
for p in ps:
    fname = f'./results/results-vary/results_BA_prob{p}_frac0.05_k5/strategy_results_multiple.csv'
    df = pd.read_csv(fname)
    for s in strategies:
        mean = df[df['strategy'] == s]['infected'].mean()
        final_results[s].append(mean)

plt.figure(figsize=(8,6))
for s in strategies:
    plt.plot(ps, final_results[s], marker='o', label=s.capitalize())
plt.title('Effect of Propagation Probability (p) on Final Spread (BA Network)')
plt.xlabel('Propagation Probability (p)')
plt.ylabel('Average Final Infected Nodes')
plt.legend()
plt.tight_layout()
plt.savefig('figure_4_6_1.png')
plt.show()
