import pandas as pd
import networkx as nx
import numpy as np


# Load the provided CSV files
edges_file_path = '../../csv/musae_git_edges.csv'
target_file_path = '../../csv/git_target_languages.csv'

edges_df = pd.read_csv(edges_file_path)
target_df = pd.read_csv(target_file_path)

# Create a graph from the edges dataframe
G = nx.from_pandas_edgelist(edges_df, source='Source', target='Target')

target_df = target_df[target_df['id'] != 'id']
target_df['id'] = target_df['id'].astype(int)

# Add node attributes from the target dataframe
attributes = target_df.set_index('id').to_dict('index')
for node, data in attributes.items():
    if node in G:
        G.nodes[node].update(data)

# Initialize all nodes with the 'developer_type' and 'language' attributes
for node in G.nodes:
    if 'ml_target' in G.nodes[node]:
        G.nodes[node]['developer_type'] = 'web' if G.nodes[node]['ml_target'] == '0' else 'ml'
    else:
        G.nodes[node]['developer_type'] = 'unknown'
    if 'most_common_language' in G.nodes[node]:
        G.nodes[node]['language'] = G.nodes[node]['most_common_language']
    else:
        G.nodes[node]['language'] = 'unknown'

# Define the spread_message function
def spread_message(G, p, q, initial_active_nodes, attribute, steps):
    # Set all nodes as inactive initially
    nx.set_node_attributes(G, False, 'active')
    nx.set_node_attributes(G, False, 'spread')

    # Activate the initial nodes
    for node in initial_active_nodes:
        G.nodes[node]['active'] = True

    # Iterate over active nodes and spread messages
    for _ in range(steps):
        spreading = False
        new_activations = []
        for node in G.nodes:
            if G.nodes[node]['active'] and not G.nodes[node]['spread']:
                for neighbor in G.neighbors(node):
                    if not G.nodes[neighbor]['active']:
                        if G.nodes[node][attribute] == G.nodes[neighbor][attribute]:
                            if np.random.rand() < p:
                                new_activations.append(neighbor)
                                spreading = True
                        else:
                            if np.random.rand() < q:
                                new_activations.append(neighbor)
                                spreading = True
                G.nodes[node]['spread'] = True
        for node in new_activations:
            G.nodes[node]['active'] = True
        if not spreading:
            break

    # Return the number of active nodes after spreading
    return len([node for node in G.nodes if G.nodes[node]['active']])

# Select initial active nodes for web developers (ml_target = 0)
initial_active_nodes_web = [node for node in G.nodes if G.nodes[node]['developer_type'] == 'web']
initial_active_nodes_web = np.random.choice(initial_active_nodes_web, size=4, replace=False)

# Select initial active nodes for ML developers (ml_target = 1)
initial_active_nodes_ml = [node for node in G.nodes if G.nodes[node]['developer_type'] == 'ml']
print('here', len(initial_active_nodes_ml))
initial_active_nodes_ml = np.random.choice(initial_active_nodes_ml, size=4, replace=False)

# Select initial active nodes for JavaScript developers
initial_active_nodes_js = [node for node in G.nodes if G.nodes[node]['language'] == 'JavaScript']
initial_active_nodes_js = np.random.choice(initial_active_nodes_js, size=4, replace=False)

# Select initial active nodes for Python developers
initial_active_nodes_py = [node for node in G.nodes if G.nodes[node]['language'] == 'Python']
initial_active_nodes_py = np.random.choice(initial_active_nodes_py, size=4, replace=False)



# Scenario 1: p = 1, q = 0 (web developer)
spread_count_scenario_1_web = spread_message(G, p=1, q=0, initial_active_nodes=initial_active_nodes_web, attribute='developer_type', steps=5)

# Scenario 2: p = 0.7, q = 0.3 (web developer)
spread_count_scenario_2_web = spread_message(G, p=0.7, q=0.3, initial_active_nodes=initial_active_nodes_web, attribute='developer_type', steps=5)

# Scenario 3: p = 1, q = 0 (ML developer)
spread_count_scenario_3_ml = spread_message(G, p=1, q=0, initial_active_nodes=initial_active_nodes_ml, attribute='developer_type', steps=5)

# Scenario 4: p = 0.7, q = 0.3 (ML developer)
spread_count_scenario_4_ml = spread_message(G, p=0.7, q=0.3, initial_active_nodes=initial_active_nodes_ml, attribute='developer_type', steps=5)

# Scenario 5: p = 1, q = 0 (JavaScript)
spread_count_scenario_5_js = spread_message(G, p=1, q=0, initial_active_nodes=initial_active_nodes_js, attribute='language', steps=5)

# Scenario 6: p = 0.7, q = 0.3 (JavaScript)
spread_count_scenario_6_js = spread_message(G, p=0.7, q=0.3, initial_active_nodes=initial_active_nodes_js, attribute='language', steps=5)

# Scenario 7: p = 1, q = 0 (Python)
spread_count_scenario_7_py = spread_message(G, p=1, q=0, initial_active_nodes=initial_active_nodes_py, attribute='language', steps=5)

# Scenario 8: p = 0.7, q = 0.3 (Python)
spread_count_scenario_8_py = spread_message(G, p=0.7, q=0.3, initial_active_nodes=initial_active_nodes_py, attribute='language', steps=5)


print('len', len(initial_active_nodes_web))


print(spread_count_scenario_1_web, spread_count_scenario_2_web, spread_count_scenario_3_ml, spread_count_scenario_4_ml, spread_count_scenario_5_js, spread_count_scenario_6_js, spread_count_scenario_7_py, spread_count_scenario_8_py)

# Visualize the results
import matplotlib.pyplot as plt

# Data for visualization
scenarios = ['p=1, q=0 (web dev)', 'p=0.7, q=0.3 (web dev)', 'p=1, q=0 (ML dev)', 'p=0.7, q=0.3 (ML dev)', 'p=1, q=0 (JavaScript)', 'p=0.7, q=0.3 (JavaScript)', 'p=1, q=0 (Python)', 'p=0.7, q=0.3 (Python)']
spread_counts = [spread_count_scenario_1_web, spread_count_scenario_2_web, spread_count_scenario_3_ml, spread_count_scenario_4_ml, spread_count_scenario_5_js, spread_count_scenario_6_js, spread_count_scenario_7_py, spread_count_scenario_8_py]

# Plot the results
plt.figure(figsize=(12, 6))
plt.bar(scenarios, spread_counts, color=['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'yellow', 'black'])
plt.xlabel('Scenarios')
plt.ylabel('Number of Active Nodes')
plt.title('Spreading Simulation Results for Different Developer Types')
plt.ylim(0, max(spread_counts) + 1000)  # Adding some space above the highest bar for better visualization
plt.xticks(rotation=45)
plt.grid(axis='y')

# Show the plot
plt.show()
