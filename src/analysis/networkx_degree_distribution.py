# Importing Libraries
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Importing dataset
users = pd.read_csv('../../csv/musae_git_target.csv')

# Reading Graphs
Data = open('../../csv/musae_git_edges.csv', "r")
next(Data, None)  # skip the first line in the input file
followers = nx.parse_edgelist(Data, delimiter=',', create_using=nx.Graph(), nodetype=int)

# Assign 'ml_target' attribute to the nodes in the graph
ml_target_dict = users.set_index('id')['ml_target'].to_dict()
nx.set_node_attributes(followers, ml_target_dict, 'ml_target')

# Calculate the degree distribution for each group
degrees_ml_0 = [degree for node, degree in followers.degree() if followers.nodes[node]['ml_target'] == 0]
degrees_ml_1 = [degree for node, degree in followers.degree() if followers.nodes[node]['ml_target'] == 1]

# Create a histogram of the degree distribution
degree_distribution_ml_0 = nx.degree_histogram(followers.subgraph([node for node in followers if followers.nodes[node]['ml_target'] == 0]))
degree_distribution_ml_1 = nx.degree_histogram(followers.subgraph([node for node in followers if followers.nodes[node]['ml_target'] == 1]))

# Plot the degree distribution for ml_target = 0 in log-log scale
fig, ax = plt.subplots(figsize=(15, 10))
# x = [i for i in range(len(degree_distribution_ml_0)) if degree_distribution_ml_0[i] > 0]
x = [i for i in range(150) if degree_distribution_ml_0[i] > 0]
y = [degree_distribution_ml_0[i] for i in x]
ax.bar(x, y)
ax.set_title('Web Developers')
ax.set_xlabel('Degree')
ax.set_ylabel('Frequency')
ax.set_yscale('log')
plt.show()

# Plot the degree distribution for ml_target = 1 in log-log scale
fig, ax = plt.subplots(figsize=(15, 10))
# x = [i for i in range(len(degree_distribution_ml_1)) if degree_distribution_ml_1[i] > 0]
x = [i for i in range(150) if degree_distribution_ml_0[i] > 0]
y = [degree_distribution_ml_1[i] for i in x]
ax.bar(x, y)
ax.set_title('Machine Learning Developers')
ax.set_xlabel('Degree')
ax.set_ylabel('Frequency')
ax.set_yscale('log')
plt.show()

