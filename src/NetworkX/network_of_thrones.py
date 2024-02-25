import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def neighborhood_overlap(G, node_a, node_b):
    neighbors_a = set(G.neighbors(node_a))
    neighbors_b = set(G.neighbors(node_b))

    # Nodes that are neighbors of both A and B
    common_neighbors = neighbors_a.intersection(neighbors_b)

    # Nodes that are neighbors of at least one of A or B
    all_neighbors = neighbors_a.union(neighbors_b)

    if len(all_neighbors) == 0:
        return 0
    else:
        return len(common_neighbors) / len(all_neighbors)


def giant_component_size(G):
    # Compute the sizes of all connected components
    component_sizes = [len(c) for c in nx.connected_components(G)]
    # Return the size of the largest connected component
    return max(component_sizes)


# Load edge list
edges_df = pd.read_csv("../../csv/stormofswords.csv")

# Load the dataset into a NetworkX graph
G = nx.Graph()
for index, row in edges_df.iterrows():
    G.add_edge(row['Source'], row['Target'], weight=row['Weight'])

# Calculate the degree of each node
degrees = dict(G.degree())

# Plot the degree distribution
degree_values = list(degrees.values())
plt.hist(degree_values, bins=50, color='skyblue', edgecolor='black')
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Number of Nodes')
plt.show()

# Create empty lists to store the data for the figure
percentage_removed_edges = []
giant_component_sizes = []

# Compute the size of the giant component after removing each percentage of edges
total_edges = len(G.edges())
for percentage in range(0, 101, 5):
    num_edges_to_remove = int(total_edges * percentage / 100)
    G_copy = G.copy()
    G_copy.remove_edges_from(list(G_copy.edges())[:num_edges_to_remove])
    giant_component_sizes.append(giant_component_size(G_copy))
    percentage_removed_edges.append(percentage)

# Plot the figure
plt.plot(percentage_removed_edges, giant_component_sizes, marker='o')
plt.title('Edge removal and giant component size')
plt.xlabel('Percentage of removed edges')
plt.ylabel('Size of giant component')
plt.grid(True)
plt.show()

overlap = neighborhood_overlap(G, 'Sandor', 'Ilyn')
print("Neighborhood overlap between node_a and node_b:", overlap)

# Create a list of neighborhoods for each edge
neighborhoods = [set(nx.neighbors(G, edge[0])) & set(nx.neighbors(G, edge[1])) for edge in G.edges()]

# Create a weighted graph where edge weights correspond to neighborhood overlap
WG = nx.Graph()
for edge, neighborhood in zip(G.edges(), neighborhoods):
    WG.add_edge(edge[0], edge[1], weight=len(neighborhood))

# Extract edge weights and neighborhood overlap
weights = [WG[edge[0]][edge[1]]['weight'] for edge in WG.edges()]
overlap = [len(set(nx.neighbors(G, edge[0])) & set(nx.neighbors(G, edge[1]))) for edge in WG.edges()]

# Plot the data
plt.scatter(weights, overlap)
plt.xlabel('Edge Weight')
plt.ylabel('Neighborhood Overlap')
plt.title('Edge Weight vs. Neighborhood Overlap')
plt.grid(True)
plt.show()
