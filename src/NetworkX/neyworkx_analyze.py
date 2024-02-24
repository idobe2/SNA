# Importing Libraries
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Importing dataset
users = pd.read_csv('../../csv/musae_git_target.csv')

# Reading Graphs
Data = open('../../csv/musae_git_edges.csv', "r")
next(Data, None)  # skip the first line in the input file
followers = nx.parse_edgelist(Data, delimiter=',', create_using=nx.Graph(), nodetype=int)

# Finding Local Cluster (each node clustering coefficient)
local_cluster = nx.clustering(followers)
sorted_local_cluster = {k: v for k, v in sorted(local_cluster.items(), key=lambda item: item[1])}
print(sorted_local_cluster)

# Global Clustering with count zeroes (default)
global_cluster = nx.average_clustering(followers, count_zeros=True)
print(f'Global Clustering:\t{global_cluster}')

# Radius of Followers Graph
radius_of_graph = nx.radius(followers)
print(f'Radius of Followers:\t{radius_of_graph}')

# Diameter of Followers Graph
diameter_of_graph = nx.diameter(followers)
print(f'Diameter of Followers:\t{diameter_of_graph}')

# Density of follower
density_of_graph = nx.density(followers)
print(f'Density of follower:\t{density_of_graph}')

# Connected Components
print(nx.is_connected(followers))
print(nx.number_connected_components(followers))

# Average Path Length
average_short_path_length = nx.average_shortest_path_length(followers)
print(f'Average Path Length:\t{average_short_path_length}')


