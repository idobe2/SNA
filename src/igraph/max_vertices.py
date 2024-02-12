import igraph

# Read the graph data from the text file
with open('../../txt/Wiki-Vote.txt', 'r') as file:
    lines = file.readlines()

# Extracting edges from the text file
edges = [(int(src), int(dest)) for line in lines for src, dest in [line.strip().split()]]

# Creating a graph object
g = igraph.Graph.TupleList(edges, directed=True)

# Limiting the number of vertices to visualize
max_vertices = 7200
if len(g.vs) > max_vertices:
    g = g.subgraph(range(max_vertices))

# Using a layout suitable for large txt
layout = g.layout_fruchterman_reingold()

# Visualize the graph
igraph.plot(g, target='test.png', bbox=(1920, 1080), layout=layout)

# Print the number of vertices and edges
print("Number of vertices:", len(g.vs))
print("Number of edges:", len(g.es))
