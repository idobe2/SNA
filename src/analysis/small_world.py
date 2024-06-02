import pandas as pd
import networkx as nx

# Load data from CSV
edges = pd.read_csv('../../csv/musae_git_edges.csv')
# Construct the graph
G = nx.Graph()
G.add_edges_from(edges.values)

# Calculate the average clustering coefficient
clustering_coefficient = nx.average_clustering(G)
print(f"Average Clustering Coefficient: {clustering_coefficient}")

# Since the graph is large, calculating the exact average shortest path length is computationally expensive.
# We'll use an approximation by sampling a subset of nodes.
def approximate_average_shortest_path_length(G, trials=1000):
    import random
    nodes = list(G.nodes())
    total_path_length = 0
    count = 0
    for _ in range(trials):
        u, v = random.sample(nodes, 2)
        try:
            path_length = nx.shortest_path_length(G, source=u, target=v)
            total_path_length += path_length
            count += 1
        except nx.NetworkXNoPath:
            continue
    return total_path_length / count

avg_path_length = approximate_average_shortest_path_length(G)
print(f"Approximate Average Path Length: {avg_path_length}")

# Generate a random graph with the same number of nodes and edges
random_graph = nx.gnm_random_graph(G.number_of_nodes(), G.number_of_edges())
random_clustering = nx.average_clustering(random_graph)
random_path_length = approximate_average_shortest_path_length(random_graph)

print(f"Random Graph - Average Clustering Coefficient: {random_clustering}")
print(f"Random Graph - Approximate Average Path Length: {random_path_length}")

# Compare and determine if it's a small-world
is_small_world = (clustering_coefficient > random_clustering and
                  avg_path_length <= random_path_length)
print(f"The network is {'a small-world network' if is_small_world else 'not a small-world network'}.")
