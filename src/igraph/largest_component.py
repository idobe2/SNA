import igraph

# Read the graph data from the text file
with open('../../txt/Wiki-Vote.txt', 'r') as file:
    lines = file.readlines()

# Extracting edges from the text file
edges = [(int(src), int(dest)) for line in lines for src, dest in [line.strip().split()]]

# Creating a graph object
g = igraph.Graph.TupleList(edges, directed=True)

# Finding the largest connected component
components = g.connected_components()
largest_component = components.giant()

# Using a layout suitable for large txt
layout = largest_component.layout_fruchterman_reingold()

# Visualize the largest connected component
igraph.plot(largest_component, target='Wiki-Vote.png', bbox=(1920, 1080), layout=layout)

# Print the number of vertices and edges
print("Number of vertices:", len(g.vs))
print("Number of edges:", len(g.es))
