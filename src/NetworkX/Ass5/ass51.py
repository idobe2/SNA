import pandas as pd
import networkx as nx
import community
import matplotlib.pyplot as plt

# Read data
edges_df = pd.read_csv('../../../csv/musae_git_edges.csv')
targets_df = pd.read_csv('../../../csv/musae_git_target.csv')

# Create graph
G = nx.from_pandas_edgelist(edges_df, 'Source', 'Target')

# Assign community labels
community_labels = dict(zip(targets_df['id'], targets_df['ml_target']))
nx.set_node_attributes(G, community_labels, 'community')

# Calculate modularity
partition = community.best_partition(G)
modularity = community.modularity(partition, G)
print("Modularity:", modularity)

# Count the number of nodes in each modularity class
class_sizes = {}
for node, community_label in partition.items():
    class_sizes[community_label] = class_sizes.get(community_label, 0) + 1

# Plot number of nodes in each modularity class
plt.bar(range(len(class_sizes)), list(class_sizes.values()), align='center', color='skyblue')
plt.xlabel('Modularity Class')
plt.ylabel('Number of Nodes')
plt.title('Number of Nodes in Each Modularity Class')
plt.xticks(range(len(class_sizes)), list(class_sizes.keys()))
plt.grid(True, axis='y')
plt.show()
