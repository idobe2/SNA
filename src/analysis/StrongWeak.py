import pandas as pd
import networkx as nx
import random_graph_models

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

# Assuming tie strength is based on the number of shared repositories (example)
# We don't have actual shared repository data, so we'll create a mock-up for this purpose
for u, v in G.edges():
    G[u][v]['weight'] = random.randint(1, 10)  # Randomly assign a weight (1-10) to each edge

# Define strong ties as those with a weight above a threshold (e.g., 5)
strong_threshold = 5

strong_ties = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] > strong_threshold]
weak_ties = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] <= strong_threshold]

print("Number of strong ties:", len(strong_ties))
print("Number of weak ties:", len(weak_ties))
