import pandas as pd
import networkx as nx

# Load the provided CSV files
edges_file_path = '../../csv/filtered_edges.csv'
target_file_path = '../../csv/git-exported.csv'

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

# Function to calculate homophily for a given attribute, handling nodes without attributes
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

# Calculate homophily for 'ml_target' and 'most_common_language'
homophily_ml_target_safe = calculate_homophily_safe(G, 'ml_target')
homophily_language_safe = calculate_homophily_safe(G, 'most_common_language')

print("Homophily for Developer Group (ml_target):", homophily_ml_target_safe)
print("Homophily for Programming Language (most_common_language):", homophily_language_safe)

