import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load edge list
edges_df = pd.read_csv("../../csv/musae_git_edges.csv")

# Load the dataset into a NetworkX graph
G = nx.Graph()
for index, row in edges_df.iterrows():
    G.add_edge(row['Source'], row['Target'])

# Calculate the degree of each node
degrees = dict(G.degree())

# Plot the degree distribution
degree_values = list(degrees.values())
plt.hist(degree_values, bins=50, color='skyblue', edgecolor='black')
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Number of Nodes')
plt.show()
