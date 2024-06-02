# Importing Libraries
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Importing dataset
users = pd.read_csv('../../csv/musae_git_target.csv')

# Reading Graphs
Data = open('../../csv/musae_git_edges.csv', "r")
next(Data, None)  # skip the first line in the input file
followers = nx.parse_edgelist(Data, delimiter=',', create_using=nx.Graph(), nodetype=int)

# Assign 'ml_target' attribute to the nodes in the graph
ml_target_dict = users.set_index('id')['ml_target'].to_dict()
nx.set_node_attributes(followers, ml_target_dict, 'ml_target')


# Function to calculate degree distribution
def degree_distribution(graph, beta):
    degrees = [degree for node, degree in graph.degree()]
    hist, bin_edges = np.histogram(degrees, bins=np.arange(0, max(degrees) + 2))
    return hist ** beta


# Control the beta value
beta = 1.0  # You can change this value to see the effect

# Calculate the degree distribution for each group
degrees_ml_0 = [degree for node, degree in followers.degree() if followers.nodes[node]['ml_target'] == 0]
degrees_ml_1 = [degree for node, degree in followers.degree() if followers.nodes[node]['ml_target'] == 1]

# Create a histogram of the degree distribution with beta adjustment
degree_distribution_ml_0 = degree_distribution(
    followers.subgraph([node for node in followers if followers.nodes[node]['ml_target'] == 0]), beta)
degree_distribution_ml_1 = degree_distribution(
    followers.subgraph([node for node in followers if followers.nodes[node]['ml_target'] == 1]), beta)

# Plot the degree distribution for ml_target = 0
fig, ax = plt.subplots(figsize=(15, 10))
ax.bar(range(len(degree_distribution_ml_0)), degree_distribution_ml_0, color='b', alpha=0.7)
ax.set_title(f'Degree Distribution (Web Developers) with Beta={beta}')
ax.set_xlabel('Degree')
ax.set_ylabel('Frequency')
plt.show()

# Plot the degree distribution for ml_target = 1
fig, ax = plt.subplots(figsize=(15, 10))
ax.bar(range(len(degree_distribution_ml_1)), degree_distribution_ml_1, color='r', alpha=0.7)
ax.set_title(f'Degree Distribution (Machine Learning Developers) with Beta={beta}')
ax.set_xlabel('Degree')
ax.set_ylabel('Frequency')
plt.show()

# Plot the degree distribution for ml_target = 0 in log-log scale
fig, ax = plt.subplots(figsize=(15, 10))
x = [i for i in range(len(degree_distribution_ml_0)) if degree_distribution_ml_0[i] > 0]
y = [degree_distribution_ml_0[i] for i in x]
ax.plot(x, y, 'bo', markersize=5)
ax.set_title(f'Degree Distribution (Web Developers) - Log-Log Scale with Beta={beta}')
ax.set_xlabel('Degree')
ax.set_ylabel('Frequency')
ax.set_xscale('log')
ax.set_yscale('log')
plt.show()

# Plot the degree distribution for ml_target = 1 in log-log scale
fig, ax = plt.subplots(figsize=(15, 10))
x = [i for i in range(len(degree_distribution_ml_1)) if degree_distribution_ml_1[i] > 0]
y = [degree_distribution_ml_1[i] for i in x]
ax.plot(x, y, 'ro', markersize=5)
ax.set_title(f'Degree Distribution (Machine Learning Developers) - Log-Log Scale with Beta={beta}')
ax.set_xlabel('Degree')
ax.set_ylabel('Frequency')
ax.set_xscale('log')
ax.set_yscale('log')
plt.show()
