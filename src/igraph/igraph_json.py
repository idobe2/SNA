# Works with file: wikivital_mathematics.json

# Import libraries
import json

import igraph as ig

# Load the JSON data
with open("../../csv/reddit_edges.json", "r") as f:
    data = json.load(f)

# Extract edges and create graph
g = ig.Graph()
edges = data["edges"]
graph = ig.Graph(edges=edges, directed=False)

# Print summary information
print("Number of nodes:", graph.vcount())
print("Number of edges:", graph.ecount())

# Print edges
# print("Edges:")
# for src, dst in edges:
#     print(f"{src} -> {dst}")

# Visualize the graph
# graph.vs["label"] = graph.vs["name"]  # Set node labels
graph.vs["color"] = "blue"  # Set node color
ig.plot(graph, target='wikivital_mathematics.png', bbox=(1920, 1080))

