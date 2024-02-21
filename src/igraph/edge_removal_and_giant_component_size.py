import igraph as ig
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the edge list from CSV file
edges_df = pd.read_csv('../../csv/musae_git_edges.csv')

# Read the target data from CSV file
target_df = pd.read_csv('../../csv/musae_git_target.csv')

# Extracting edges from the DataFrame
edges = [(int(src), int(dest)) for src, dest in edges_df[['Source', 'Target']].values]

# Create a graph object
g = ig.Graph.TupleList(edges, directed=False)

# Finding the largest connected component
components = g.components()
largest_component = components.giant()

# Read the ml_target values from target_df
ml_target_values = target_df.set_index('id')['ml_target']

# Define colors for nodes based on ml_target values
node_colors = ['blue' if node['name'] in ml_target_values and ml_target_values[node['name']] == 1 else 'gray' for node in largest_component.vs]

# Using a layout suitable for large graphs
layout = largest_component.layout_fruchterman_reingold()

# Visualize the largest connected component and save as PNG image
# ig.plot(largest_component, target='musae_git_graph_all.png', bbox=(1920, 1080), layout=layout, vertex_color=node_colors, vertex_size=5)

# Print the number of vertices and edges for the largest connected component
print("Number of vertices in the largest connected component:", len(largest_component.vs))
print("Number of edges in the largest connected component:", len(largest_component.es))

# 1. Generate the figure "Edge removal and giant component size"
# Initialize lists to store number of edges removed and corresponding giant component sizes
edges_removed = []
giant_component_sizes = []

# Copy the graph to perform edge removal without affecting the original graph
temp_graph = largest_component.copy()

# Remove edges iteratively and track the size of the giant component
for i in range(len(temp_graph.es)):
    temp_graph.delete_edges(i)  # Remove edge at index i
    giant_component = temp_graph.components().giant()
    giant_component_sizes.append(len(giant_component.vs))
    edges_removed.append(i)

# Plotting the figure
plt.figure(figsize=(10, 6))
plt.plot(edges_removed, giant_component_sizes)
plt.title("Edge Removal and Giant Component Size")
plt.xlabel("Number of Edges Removed")
plt.ylabel("Size of Giant Component")
plt.grid(True)
plt.show()

# 2. Generate the figure "neighborhood overlap as function weight"
# Let's assume edge weights based on a random uniform distribution between 0 and 1
weights = np.random.rand(len(edges))

# Calculate neighborhood overlap as a function of weight
neighborhood_overlap = []
for weight in weights:
    overlap = sum(1 for v in g.vs if all(e['weight'] >= weight for e in v.all_edges())) / len(g.vs)
    neighborhood_overlap.append(overlap)

# Plotting the figure
plt.figure(figsize=(10, 6))
plt.scatter(weights, neighborhood_overlap, alpha=0.5)
plt.title("Neighborhood Overlap as a Function of Weight")
plt.xlabel("Edge Weights")
plt.ylabel("Neighborhood Overlap")
plt.grid(True)
plt.show()
