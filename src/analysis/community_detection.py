import pandas as pd
import networkx as nx
from community import community_louvain

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

# Perform community detection using the Louvain method
partition = community_louvain.best_partition(G)

# Add the community information to the nodes
for node, community_id in partition.items():
    G.nodes[node]['community'] = community_id

# Analyze the composition of communities
community_counts = {}
for node, data in G.nodes(data=True):
    community_id = data['community']

    ml_target = data.get('ml_target')
    most_common_language = data.get('most_common_language')

    if community_id not in community_counts:
        community_counts[community_id] = {'ml_target': {0: 0, 1: 0}, 'language': {}}

    if ml_target is not None:
        community_counts[community_id]['ml_target'][int(ml_target)] += 1
    if most_common_language is not None:
        if most_common_language not in community_counts[community_id]['language']:
            community_counts[community_id]['language'][most_common_language] = 0
        community_counts[community_id]['language'][most_common_language] += 1

# Display the community composition
for community_id, counts in community_counts.items():
    print(f"Community {community_id}:")
    print("  Developer Group (ml_target):", counts['ml_target'])
    print("  Most Common Languages:", counts['language'])
