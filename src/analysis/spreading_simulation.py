import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
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


# SIR Model Simulation
def sir_model(G, beta, gamma, initial_infected, steps):
    S = {node: True for node in G.nodes()}
    I = {node: False for node in G.nodes()}
    R = {node: False for node in G.nodes()}

    # Initialize the first infected nodes
    for node in initial_infected:
        S[node] = False
        I[node] = True

    susceptible_count = [len(G.nodes()) - len(initial_infected)]
    infected_count = [len(initial_infected)]
    recovered_count = [0]

    for step in range(steps):
        new_infected = []
        new_recovered = []

        for node in G.nodes():
            if I[node]:
                # Spread the infection
                for neighbor in G.neighbors(node):
                    if S[neighbor] and np.random.rand() < beta:
                        S[neighbor] = False
                        new_infected.append(neighbor)

                # Recover
                if np.random.rand() < gamma:
                    I[node] = False
                    R[node] = True
                    new_recovered.append(node)

        for node in new_infected:
            I[node] = True

        susceptible_count.append(sum(S.values()))
        infected_count.append(sum(I.values()))
        recovered_count.append(sum(R.values()))

    return susceptible_count, infected_count, recovered_count


# Parameters
beta = 0.3  # Infection rate
gamma = 0.1  # Recovery rate
initial_infected = [0, 1, 2, 3, 4]  # Starting with a few initial infected nodes
steps = 50

# Run the simulation
susceptible_count, infected_count, recovered_count = sir_model(G, beta, gamma, initial_infected, steps)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(susceptible_count, label="Susceptible")
plt.plot(infected_count, label="Infected")
plt.plot(recovered_count, label="Recovered")
plt.xlabel("Time Steps")
plt.ylabel("Number of Nodes")
plt.title("SIR Model Simulation on GitHub Network")
plt.legend()
plt.show()


# Analyze the spread within groups
def analyze_spread_within_groups(G, initial_infected, attribute):
    infected_by_group = {group: 0 for group in set(nx.get_node_attributes(G, attribute).values())}

    for node in initial_infected:
        if attribute in G.nodes[node]:
            group = G.nodes[node][attribute]
            infected_by_group[group] += 1

    return infected_by_group


# Analyze spread within developer groups
spread_within_ml_target = analyze_spread_within_groups(G, initial_infected, 'ml_target')
spread_within_language = analyze_spread_within_groups(G, initial_infected, 'most_common_language')

print("Spread within developer groups (ml_target):", spread_within_ml_target)
print("Spread within programming languages (most_common_language):", spread_within_language)
