import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def giant_component_size(G):
    # Compute the sizes of all connected components
    component_sizes = [len(c) for c in nx.connected_components(G)]
    # Return the size of the largest connected component
    return max(component_sizes)


# Load edge list
edges_df = pd.read_csv("../../../csv/stormofswords.csv")

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
colors = ['red', 'green', 'blue']  # Define colors for each method

# Compute the size of the giant component after removing each percentage of edges
total_edges = len(G.edges())

# Method 1: Strong to weak
for percentage in range(0, 101, 5):
    num_edges_to_remove = int(total_edges * percentage / 100)
    G_copy = G.copy()
    edges_to_remove = sorted(G_copy.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:num_edges_to_remove]
    G_copy.remove_edges_from(edges_to_remove)
    giant_component_sizes.append(giant_component_size(G_copy))
    percentage_removed_edges.append(percentage)

# Plot Method 1 with a red color
plt.plot(percentage_removed_edges, giant_component_sizes, marker='o', color=colors[0], label='Strong to Weak')

# Method 2: Weak to strong
percentage_removed_edges.clear()
giant_component_sizes.clear()

for percentage in range(0, 101, 5):
    num_edges_to_remove = int(total_edges * percentage / 100)
    G_copy = G.copy()
    edges_to_remove = sorted(G_copy.edges(data=True), key=lambda x: x[2]['weight'])[:num_edges_to_remove]
    G_copy.remove_edges_from(edges_to_remove)
    giant_component_sizes.append(giant_component_size(G_copy))
    percentage_removed_edges.append(percentage)

# Plot Method 2 with a green color
plt.plot(percentage_removed_edges, giant_component_sizes, marker='o', color=colors[1], label='Weak to Strong')

# Method 3: Betweenness centrality order
percentage_removed_edges.clear()
giant_component_sizes.clear()

betweenness = nx.edge_betweenness_centrality(G)
for percentage in range(0, 101, 5):
    num_edges_to_remove = int(total_edges * percentage / 100)
    G_copy = G.copy()
    edges_to_remove = sorted(G_copy.edges(data=True), key=lambda x: betweenness[x[:2]], reverse=True)[
                      :num_edges_to_remove]
    G_copy.remove_edges_from(edges_to_remove)
    giant_component_sizes.append(giant_component_size(G_copy))
    percentage_removed_edges.append(percentage)

# Plot Method 3 with a blue color
plt.plot(percentage_removed_edges, giant_component_sizes, marker='o', color=colors[2], label='Betweenness Centrality')

# Plot the figure
plt.title('Edge removal and giant component size')
plt.xlabel('Percentage of removed edges')
plt.ylabel('Size of giant component')
plt.grid(True)
plt.legend()
plt.show()
