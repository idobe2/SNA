import igraph

# Read the graph data from the text file
with open('../../txt/facebook_combined.txt', 'r') as file:
    lines = file.readlines()

# Extracting vertices and edges from the text file
vertices = set()
edges = []
for line in lines:
    src, dest = map(int, line.strip().split())
    vertices.add(src)
    vertices.add(dest)
    edges.append((src, dest))

# Creating a graph object
g = igraph.Graph()
g.add_vertices(list(vertices))
g.add_edges(edges)

# Visualize the graph
igraph.plot(g, target='facebook_combined.png', bbox=(1920, 1080))  # Adjust the images size as needed


