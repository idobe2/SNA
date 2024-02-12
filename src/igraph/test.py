import pandas as pd
import igraph

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('../../csv/Middle_East_Israel_Palestine.csv')

# Initialize an empty graph object
g = igraph.Graph()

# Add vertices (nodes) to the graph
unique_nodes = set(df['event_type']).union(set(df['location']))
g.add_vertices(list(unique_nodes))

# Add edges to the graph
for _, row in df.iterrows():
    source = row['event_type']
    target = row['location']
    g.add_edge(source, target)

# Visualize the graph (optional)
g.vs["label"] = g.vs["name"]  # Set node labels
g.vs["color"] = "blue"  # Set node color
igraph.plot(g, target='test.png', bbox=(1920, 1080))
print("Number of vertices:", len(g.vs))
print("Number of edges:", len(g.es))

# Now you have a graph object 'g' representing your dataset
