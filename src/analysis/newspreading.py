import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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

# Check a sample of node attributes
for i, (node, data) in enumerate(G.nodes(data=True)):
    if i < 5:  # Print only the first 5 nodes
        print(f"Node {node}: {data}")

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
    active_nodes = [node for node in G.nodes if G.nodes[node]['active']]
    count_web = sum(1 for node in active_nodes if G.nodes[node]['developer_type'] == 'web')
    count_ml = sum(1 for node in active_nodes if G.nodes[node]['developer_type'] == 'ml')
    count_js = sum(1 for node in active_nodes if G.nodes[node]['language'] == 'Java')
    count_py = sum(1 for node in active_nodes if G.nodes[node]['language'] == 'Python')
    count_other = sum(1 for node in active_nodes if G.nodes[node]['language'] not in ['Java', 'Python'])

    return count_web, count_ml, count_js, count_py, count_other

# Set the random seed for reproducibility
np.random.seed(42)

# Select initial active nodes
initial_active_nodes_web = [node for node in G.nodes if G.nodes[node]['developer_type'] == 'web']
initial_active_node_web = [np.random.choice(initial_active_nodes_web)]

initial_active_nodes_ml = [node for node in G.nodes if G.nodes[node]['developer_type'] == 'ml']
initial_active_node_ml = [np.random.choice(initial_active_nodes_ml)]

initial_active_nodes_js = [node for node in G.nodes if G.nodes[node]['language'] == 'Java']
initial_active_node_js = [np.random.choice(initial_active_nodes_js)]

initial_active_nodes_py = [node for node in G.nodes if G.nodes[node]['language'] == 'Python']
initial_active_node_py = [np.random.choice(initial_active_nodes_py)]

# Print the initial active nodes for debugging
print(f'Initial active node (Web Dev): {initial_active_node_web}')
print(f'Initial active node (ML Dev): {initial_active_node_ml}')
print(f'Initial active node (Java): {initial_active_node_js}')
print(f'Initial active node (Python): {initial_active_node_py}')

# Scenario 1: p = 1, q = 0 (web developer)
spread_count_scenario_1_web = spread_message(G, p=1, q=0, initial_active_nodes=initial_active_node_web, attribute='developer_type', steps=3)

# Scenario 2: p = 0.7, q=0.3 (web developer)
spread_count_scenario_2_web = spread_message(G, p=0.7, q=0.3, initial_active_nodes=initial_active_node_web, attribute='developer_type', steps=3)

# Scenario 3: p = 1, q = 0 (ML developer)
spread_count_scenario_3_ml = spread_message(G, p=1, q=0, initial_active_nodes=initial_active_node_ml, attribute='developer_type', steps=5)

# Scenario 4: p = 0.7, q=0.3 (ML developer)
spread_count_scenario_4_ml = spread_message(G, p=0.7, q=0.3, initial_active_nodes=initial_active_node_ml, attribute='developer_type', steps=5)

# Scenario 5: p = 1, q = 0 (Java)
spread_count_scenario_5_js = spread_message(G, p=1, q=0, initial_active_nodes=initial_active_node_js, attribute='language', steps=3)

# Scenario 6: p = 0.7, q=0.3 (Java)
spread_count_scenario_6_js = spread_message(G, p=0.7, q=0.3, initial_active_nodes=initial_active_node_js, attribute='language', steps=3)

# Scenario 7: p = 1, q = 0 (Python)
spread_count_scenario_7_py = spread_message(G, p=1, q=0, initial_active_nodes=initial_active_node_py, attribute='language', steps=3)

# Scenario 8: p = 0.7, q=0.3 (Python)
spread_count_scenario_8_py = spread_message(G, p=0.7, q=0.3, initial_active_nodes=initial_active_node_py, attribute='language', steps=2)

print(f'Scenario 1 (Web Dev, p=1, q=0): Web: {spread_count_scenario_1_web[0]}, ML: {spread_count_scenario_1_web[1]}, JS: {spread_count_scenario_1_web[2]}, PY: {spread_count_scenario_1_web[3]}, Other: {spread_count_scenario_1_web[4]}')
print(f'Scenario 2 (Web Dev, p=0.7, q=0.3): Web: {spread_count_scenario_2_web[0]}, ML: {spread_count_scenario_2_web[1]}, JS: {spread_count_scenario_2_web[2]}, PY: {spread_count_scenario_2_web[3]}, Other: {spread_count_scenario_2_web[4]}')
print(f'Scenario 3 (ML Dev, p=1, q=0): Web: {spread_count_scenario_3_ml[0]}, ML: {spread_count_scenario_3_ml[1]}, JS: {spread_count_scenario_3_ml[2]}, PY: {spread_count_scenario_3_ml[3]}, Other: {spread_count_scenario_3_ml[4]}')
print(f'Scenario 4 (ML Dev, p=0.7, q=0.3): Web: {spread_count_scenario_4_ml[0]}, ML: {spread_count_scenario_4_ml[1]}, JS: {spread_count_scenario_4_ml[2]}, PY: {spread_count_scenario_4_ml[3]}, Other: {spread_count_scenario_4_ml[4]}')
print(f'Scenario 5 (Java, p=1, q=0): Web: {spread_count_scenario_5_js[0]}, ML: {spread_count_scenario_5_js[1]}, JS: {spread_count_scenario_5_js[2]}, PY: {spread_count_scenario_5_js[3]}, Other: {spread_count_scenario_5_js[4]}')
print(f'Scenario 6 (Java, p=0.7, q=0.3): Web: {spread_count_scenario_6_js[0]}, ML: {spread_count_scenario_6_js[1]}, JS: {spread_count_scenario_6_js[2]}, PY: {spread_count_scenario_6_js[3]}, Other: {spread_count_scenario_6_js[4]}')
print(f'Scenario 7 (Python, p=1, q=0): Web: {spread_count_scenario_7_py[0]}, ML: {spread_count_scenario_7_py[1]}, JS: {spread_count_scenario_7_py[2]}, PY: {spread_count_scenario_7_py[3]}, Other: {spread_count_scenario_7_py[4]}')
print(f'Scenario 8 (Python, p=0.7, q=0.3): Web: {spread_count_scenario_8_py[0]}, ML: {spread_count_scenario_8_py[1]}, JS: {spread_count_scenario_8_py[2]}, PY: {spread_count_scenario_8_py[3]}, Other: {spread_count_scenario_8_py[4]}')



# Calculate the total number of nodes in each category
total_web = sum(1 for node in G.nodes if G.nodes[node]['developer_type'] == 'web')
total_ml = sum(1 for node in G.nodes if G.nodes[node]['developer_type'] == 'ml')
total_js = sum(1 for node in G.nodes if G.nodes[node]['language'] == 'Java')
total_py = sum(1 for node in G.nodes if G.nodes[node]['language'] == 'Python')
total_other = sum(1 for node in G.nodes if G.nodes[node]['language'] not in ['Java', 'Python'])



# Data for visualization
scenarios_developer_type = ['p=1, q=0 (Web)', 'p=0.7, q=0.3 (Web)', 'p=1, q=0 (ML)', 'p=0.7, q=0.3 (ML)']
scenarios_language = ['p=1, q=0 (Java)', 'p=0.7, q=0.3 (Java)', 'p=1, q=0 (Python)', 'p=0.7, q=0.3 (Python)']

# Stacked bar data for developer types
web_counts = [spread_count_scenario_1_web[0], spread_count_scenario_2_web[0], spread_count_scenario_3_ml[0], spread_count_scenario_4_ml[0]]
ml_counts = [spread_count_scenario_1_web[1], spread_count_scenario_2_web[1], spread_count_scenario_3_ml[1], spread_count_scenario_4_ml[1]]

# Stacked bar data for languages
js_counts = [spread_count_scenario_5_js[2], spread_count_scenario_6_js[2], spread_count_scenario_7_py[2], spread_count_scenario_8_py[2]]
py_counts = [spread_count_scenario_5_js[3], spread_count_scenario_6_js[3], spread_count_scenario_7_py[3], spread_count_scenario_8_py[3]]
other_counts = [spread_count_scenario_5_js[4], spread_count_scenario_6_js[4], spread_count_scenario_7_py[4], spread_count_scenario_8_py[4]]

# Normalized data
web_counts_norm = [count / total_web for count in web_counts]
ml_counts_norm = [count / total_ml for count in ml_counts]
js_counts_norm = [count / total_js for count in js_counts]
py_counts_norm = [count / total_py for count in py_counts]
other_counts_norm = [count / total_other for count in other_counts]


print(f'Normalized Scenario 1 (Web Dev, p=1, q=0): Web: {web_counts_norm[0]}, ML: {ml_counts_norm[0]}, JS: {js_counts_norm[0]}, PY: {py_counts_norm[0]}, Other: {other_counts_norm[0]}')
print(f'Normalized Scenario 2 (Web Dev, p=0.7, q=0.3): Web: {web_counts_norm[1]}, ML: {ml_counts_norm[1]}, JS: {js_counts_norm[1]}, PY: {py_counts_norm[1]}, Other: {other_counts_norm[1]}')
print(f'Normalized Scenario 3 (ML Dev, p=1, q=0): Web: {web_counts_norm[2]}, ML: {ml_counts_norm[2]}, JS: {js_counts_norm[2]}, PY: {py_counts_norm[2]}, Other: {other_counts_norm[2]}')
print(f'Normalized Scenario 4 (ML Dev, p=0.7, q=0.3): Web: {web_counts_norm[3]}, ML: {ml_counts_norm[3]}, JS: {js_counts_norm[3]}, PY: {py_counts_norm[3]}, Other: {other_counts_norm[3]}')

print(f'Normalized Scenario 5 (Java, p=1, q=0): JS: {js_counts_norm[0]}, PY: {py_counts_norm[0]}, Other: {other_counts_norm[0]}')
print(f'Normalized Scenario 6 (Java, p=0.7, q=0.3): JS: {js_counts_norm[1]}, PY: {py_counts_norm[1]}, Other: {other_counts_norm[1]}')
print(f'Normalized Scenario 7 (Python, p=1, q=0): JS: {js_counts_norm[2]}, PY: {py_counts_norm[2]}, Other: {other_counts_norm[2]}')
print(f'Normalized Scenario 8 (Python, p=0.7, q=0.3): JS: {js_counts_norm[3]}, PY: {py_counts_norm[3]}, Other: {other_counts_norm[3]}')


# Create first figure for original data
bar_width = 0.35
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Original Developer type chart
bars_web = ax1.bar(scenarios_developer_type, web_counts, bar_width, label='Web Developers', color='blue')
bars_ml = ax1.bar(scenarios_developer_type, ml_counts, bar_width, bottom=web_counts, label='ML Developers', color='red')

ax1.set_ylim(0, 18000)
ax1.set_xlabel('Scenarios', fontsize=12)
ax1.set_ylabel('Number of Active Nodes', fontsize=12)
ax1.set_title('Spreading Simulation Results by Developer Type', fontsize=14)
ax1.legend()
ax1.grid(axis='y')

# Original Language chart
bars_js = ax2.bar(scenarios_language, js_counts, bar_width, label='Java', color='yellow')
bars_py = ax2.bar(scenarios_language, py_counts, bar_width, bottom=js_counts, label='Python', color='purple')
bars_other = ax2.bar(scenarios_language, other_counts, bar_width, bottom=[i+j for i, j in zip(js_counts, py_counts)], label='Other', color='gray')

ax2.set_xlabel('Scenarios')
ax2.set_ylabel('Number of Active Nodes')
ax2.set_title('Spreading Simulation Results Segmented by Language')
ax2.legend()
ax2.grid(axis='y')

plt.tight_layout()
plt.show()

# Create second figure for normalized data
fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 6))

# Normalized Developer type chart
bars_web_norm = ax3.bar(scenarios_developer_type, web_counts_norm, bar_width, label='Web Developers', color='blue')
bars_ml_norm = ax3.bar(scenarios_developer_type, ml_counts_norm, bar_width, bottom=web_counts_norm, label='ML Developers', color='red')

ax3.set_ylim(0, 1)
ax3.set_xlabel('Scenarios', fontsize=12)
ax3.set_ylabel('Proportion of Active Nodes', fontsize=12)
ax3.set_title('Normalized Spreading Simulation Results by Developer Type', fontsize=14)
ax3.legend()
ax3.grid(axis='y')

# Normalized Language chart
bars_js_norm = ax4.bar(scenarios_language, js_counts_norm, bar_width, label='Java', color='yellow')
bars_py_norm = ax4.bar(scenarios_language, py_counts_norm, bar_width, bottom=js_counts_norm, label='Python', color='purple')
bars_other_norm = ax4.bar(scenarios_language, other_counts_norm, bar_width, bottom=[i+j for i, j in zip(js_counts_norm, py_counts_norm)], label='Other', color='gray')

ax4.set_ylim(0, 1.5)
ax4.set_xlabel('Scenarios')
ax4.set_ylabel('Proportion of Active Nodes')
ax4.set_title('Normalized Spreading Simulation Results Segmented by Language')
ax4.legend()
ax4.grid(axis='y')

plt.tight_layout()
plt.show()
