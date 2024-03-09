# Importing Libraries
import networkx as nx
import pandas as pd

# Importing dataset
users = pd.read_csv('../../../csv/musae_git_target.csv')

# Reading Graphs
Data = open('../../../csv/musae_git_edges.csv', "r")
next(Data, None)  # skip the first line in the input file
followers = nx.parse_edgelist(Data, delimiter=',', create_using=nx.Graph(), nodetype=int)

# Calculate modularity
def calculate_modularity(G):
    return nx.algorithms.community.modularity(G, nx.algorithms.community.label_propagation_communities(G))

# Positive modularity example: Social Network
# You can assume your dataset represents a social network where nodes are individuals and edges represent friendships or connections between them.

# Calculate modularity
positive_modularity = calculate_modularity(followers)
print("Positive Modularity:", positive_modularity)

# Negative modularity example: Random Network
# For negative modularity example, we can generate a random graph.

# random_graph = nx.erdos_renyi_graph(len(users), 0.1)  # Generate a random graph
# negative_modularity = calculate_modularity(random_graph)
# print("Negative Modularity:", negative_modularity)

