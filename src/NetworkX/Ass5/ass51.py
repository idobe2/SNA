import pandas as pd
import networkx as nx
import community

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
