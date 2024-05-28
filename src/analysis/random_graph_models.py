import pandas as pd
import networkx as nx
from networkx.generators.random_graphs import erdos_renyi_graph
import numpy as np

# Load the provided CSV files
edges_file_path = '../../csv/musae_git_edges.csv'
target_file_path = '../../csv/git_target_languages.csv'

edges_df = pd.read_csv(edges_file_path)
target_df = pd.read_csv(target_file_path)

# Create a graph from the edges dataframe
G = nx.from_pandas_edgelist(edges_df, source='Source', target='Target')

# Convert the IDs in the attribute DataFrame to integers and remove any invalid rows
target_df = target_df[target_df['id'] != 'id']
target_df['id'] = target_df['id'].astype(int)

# Add node attributes from the target dataframe
attributes = target_df.set_index('id').to_dict('index')
for node, data in attributes.items():
    if node in G:
        G.nodes[node].update(data)

# Generate a random graph with the same number of nodes and edges
n = G.number_of_nodes()
p = nx.density(G)

random_graph = erdos_renyi_graph(n, p)

# Add attributes to the random graph nodes based on the original distribution
random_attrs = {node: data for node, data in zip(random_graph.nodes, target_df.to_dict('records'))}
nx.set_node_attributes(random_graph, random_attrs)

# Function to calculate homophily for a given attribute
def calculate_homophily_safe(G, attribute):
    same_attribute_edges = 0
    total_edges = 0

    for u, v in G.edges():
        if attribute in G.nodes[u] and attribute in G.nodes[v]:
            total_edges += 1
            if G.nodes[u][attribute] == G.nodes[v][attribute]:
                same_attribute_edges += 1

    homophily_ratio = same_attribute_edges / total_edges if total_edges > 0 else 0
    return homophily_ratio

# Calculate homophily in the random graph for comparison
random_homophily_ml_target = calculate_homophily_safe(random_graph, 'ml_target')
random_homophily_language = calculate_homophily_safe(random_graph, 'most_common_language')

print("Homophily in random graph for Developer Group (ml_target):", random_homophily_ml_target)
print("Homophily in random graph for Programming Language (most_common_language):", random_homophily_language)
