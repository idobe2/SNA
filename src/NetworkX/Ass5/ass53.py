import pandas as pd
import networkx as nx
from networkx.algorithms import community

# Read data
edges_df = pd.read_csv('../../../csv/musae_git_edges.csv')
targets_df = pd.read_csv('../../../csv/musae_git_target.csv')

# Create graph
G = nx.from_pandas_edgelist(edges_df, 'Source', 'Target')

# Assign community labels
community_labels = dict(zip(targets_df['id'], targets_df['ml_target']))
nx.set_node_attributes(G, community_labels, 'community')

# Define function to calculate negative modularity
def negative_modularity(G, communities, weight='weight'):
    """
    Calculate negative modularity of the graph G for given communities.
    """
    L = G.size(weight=weight)
    Q = 0
    for community in communities:
        subgraph = G.subgraph(community)
        l_c = subgraph.size(weight=weight)
        d_c = sum(dict(G.degree(community)).values())
        Q += (l_c / L) - (d_c / (2 * L)) ** 2
    return Q

# Calculate negative modularity
communities = [{node} for node in G.nodes()]
negative_modularity_value = negative_modularity(G, communities)
print("Negative Modularity:", negative_modularity_value)
