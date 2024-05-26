import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Importing dataset
users = pd.read_csv('../../csv/musae_git_target.csv')

# Reading Graphs
Data = open('../../csv/musae_git_edges.csv', "r")
next(Data, None)  # skip the first line in the input file
G = nx.parse_edgelist(Data, delimiter=',', create_using=nx.Graph(), nodetype=int)
Data.close()

# Assign 'ml_target' attribute to the nodes in the graph
ml_target_dict = users.set_index('id')['ml_target'].to_dict()
nx.set_node_attributes(G, ml_target_dict, 'ml_target')

# Function to calculate and plot degree distribution for given ml_target
def plot_degree_distribution(G, ml_target_value, ax, title):
    # Filter nodes by ml_target value and get their degrees
    degrees = [degree for node, degree in G.degree() if G.nodes[node]['ml_target'] == ml_target_value]
    # Calculate the degree distribution
    degree_counts = {}
    for degree in degrees:
        degree_counts[degree] = degree_counts.get(degree, 0) + 1
    # Sort the degrees and get corresponding counts
    items = sorted(degree_counts.items())
    degrees, counts = zip(*items)
    # Plot
    ax.plot(degrees, counts, 'o')
    ax.set_title(title)
    ax.set_xlabel('Degree (log)')
    ax.set_ylabel('Frequency (log)')
    ax.set_xscale('log')
    ax.set_yscale('log')

# Create figure and axes for the subplots
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# Plot degree distribution for ml_target = 0
plot_degree_distribution(G, 0, axes[0], 'Web Developers')

# Plot degree distribution for ml_target = 1
plot_degree_distribution(G, 1, axes[1], 'ML Developers')

plt.tight_layout()
plt.show()
