import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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
