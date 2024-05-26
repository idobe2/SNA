import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Load the datasets
edges_df = pd.read_csv('../../csv/musae_git_edges.csv')
target_df = pd.read_csv('../../csv/git_target_languages.csv')

# Create the graph
G = nx.Graph()

# Add nodes with the 'ml_target' attribute
for _, row in target_df.iterrows():
    G.add_node(row['id'], ml_target=row['ml_target'])

# Add edges
for _, row in edges_df.iterrows():
    G.add_edge(row['Source'], row['Target'])


# Define a function for the Linear Threshold Model
def linear_threshold(G, initial_active, steps=10):
    """
    Simulate the Linear Threshold Model
    :param G: networkx graph
    :param initial_active: set of initially active nodes
    :param steps: number of steps to simulate
    :return: list of active nodes after each step
    """
    active = set(initial_active)
    newly_active = set(initial_active)
    active_over_time = []

    for _ in range(steps):
        active_over_time.append(len(active))
        current_newly_active = set()
        for node in set(G.nodes()) - active:
            neighbors = set(G.neighbors(node))
            active_neighbors = len(neighbors & active)
            if active_neighbors / max(len(neighbors), 1) > np.random.rand():
                current_newly_active.add(node)
        newly_active = current_newly_active - active
        active |= newly_active

    return active_over_time


# We will now simulate the spread of the most_common_language and ml_target
# First we need to identify the most common language in the network and create initial sets of active nodes

# Identifying the most common language
languages = target_df['name'].apply(lambda x: x.split()[-1])  # Assuming the last word in 'name' is the language
most_common_language = languages.value_counts().idxmax()

# Creating sets of active nodes for ml_target and most_common_language
initial_ml_target = set(target_df[target_df['ml_target'] == 1]['id'])
initial_common_language = set(target_df[languages == most_common_language]['id'])

# Simulate the spreading processes
steps = 30  # Number of steps in the simulation
active_ml_target = linear_threshold(G, initial_ml_target, steps=steps)
active_common_language = linear_threshold(G, initial_common_language, steps=steps)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(range(steps), active_ml_target, label='ML Target')
plt.plot(range(steps), active_common_language, label='Most Common Language')
plt.xlabel('Target Set Size')
plt.ylabel('Active Set Size')
plt.title('Results for the Linear Threshold Model')
plt.legend()
plt.show()
