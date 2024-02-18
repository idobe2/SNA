import pandas as pd
import igraph as ig

# Load edge data from CSV
# Replace 'your_edge_data.csv' with the path to your CSV file
edge_data = pd.read_csv('../../csv/musae_git_edges.csv')

# Create a directed graph from edge data
graph = ig.Graph.TupleList(edge_data.itertuples(index=False), directed=True)

# Calculate basic centrality measures
degree_centrality = graph.degree()
betweenness_centrality = graph.betweenness()
closeness_centrality = graph.closeness()

# Calculate average centrality measures
avg_degree_centrality = sum(degree_centrality) / len(degree_centrality)
avg_betweenness_centrality = sum(betweenness_centrality) / len(betweenness_centrality)
avg_closeness_centrality = sum(closeness_centrality) / len(closeness_centrality)

# Calculate the clustering coefficient and average shortest path length
clustering_coefficient = graph.transitivity_undirected()
average_shortest_path_length = graph.average_path_length()

# Print calculated information for the whole graph
print("Basic Centrality Measures for the Whole Graph:")
print(f"Average Degree Centrality: {avg_degree_centrality}")
print(f"Average Betweenness Centrality: {avg_betweenness_centrality}")
print(f"Average Closeness Centrality: {avg_closeness_centrality}")

# Check if the graph exhibits small-world property
if clustering_coefficient > 2 * average_shortest_path_length:
    print("The graph exhibits the small-world property.")
else:
    print("The graph does not exhibit the small-world property.")

# Calculate rank distribution
# You can use the basic centrality measures to calculate the rank distribution

# For example, let's calculate the rank distribution for degree centrality
# degree_rank_distribution = sorted(degree_centrality, reverse=True)

# Print rank distribution for degree centrality
# print("\nRank Distribution for Degree Centrality:")
# for rank, centrality in enumerate(degree_rank_distribution):
#     print(f"Rank {rank + 1}: {centrality}")
