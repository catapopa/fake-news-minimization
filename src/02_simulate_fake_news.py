import matplotlib.pyplot as plt
from helper import simulate_icm_spread

infected_counts = simulate_icm_spread()

# Plot results
plt.plot(infected_counts, marker='o')
plt.xlabel("Iteration")
plt.ylabel("Number of Infected Nodes")
plt.title("Fake News Spread Over Time (ICM)")
plt.grid(True)
plt.savefig("fake_news_over_time.png")
plt.show()
