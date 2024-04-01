import igraph as ig
import pandas as pd

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
node_colors = ['blue' if node['name'] in ml_target_values and ml_target_values[node['name']] == 1 else 'yellow' for node in largest_component.vs]

# Using a layout suitable for large graphs
layout = largest_component.layout_fruchterman_reingold()

# Visualize the largest connected component and save as PNG image
ig.plot(largest_component, target='musae_git_graph_all.png', bbox=(1920, 1080), layout=layout, vertex_color=node_colors, vertex_size=5)

# Print the number of vertices and edges
print("Number of vertices:", len(g.vs))
print("Number of edges:", len(g.es))
