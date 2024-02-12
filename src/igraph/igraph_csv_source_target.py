import pandas as pd
import igraph

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('../../csv/musae_git_edges.csv')

# Initialize an empty graph object
g = igraph.Graph()

# Add vertices (nodes) to the graph
unique_nodes = set(df['id_1']).union(set(df['id_2']))
g.add_vertices(list(unique_nodes))

# Add edges to the graph
for _, row in df.iterrows():
    source = row['id_1']
    target = row['id_2']
    g.add_edge(source, target)

# Visualize the graph (optional)
g.vs["label"] = g.vs["name"]  # Set node labels
g.vs["color"] = "blue"  # Set node color
igraph.plot(g, target='musae_git.png', bbox=(1920, 1080))
print("Number of vertices:", len(g.vs))
print("Number of edges:", len(g.es))

# Now you have a graph object 'g' representing your dataset
