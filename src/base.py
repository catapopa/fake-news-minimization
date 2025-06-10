import random
import networkx as nx
from genetic import genetic_blocking_strategy
from greedy import greedy_blocking_strategy

def random_blocking(G, k):
    return random.sample(list(G.nodes()), k)

def degree_blocking(G, k):
    return [n for n, _ in sorted(G.degree, key=lambda x: x[1], reverse=True)[:k]]

def betweenness_blocking(G, k):
    return [n for n, _ in sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:k]]

def greedy_blocking(G, k):
    return greedy_blocking_strategy(G, k)

def genetic_blocking(G, k):
    return genetic_blocking_strategy(G, k)
