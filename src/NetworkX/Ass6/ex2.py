import pandas as pd
import networkx as nx
import random
import matplotlib.pyplot as plt

from src.NetworkX.Ass6.ex1 import initial_infected

# Reading the data from the CSV files
edges_df = pd.read_csv('../../../csv/musae_git_edges.csv')
target_df = pd.read_csv('../../../csv/musae_git_target.csv')

# Creating the graph from the edges data
G = nx.from_pandas_edgelist(edges_df, 'Source', 'Target')

# Mapping the 'ml_target' attribute to the nodes
target_dict = target_df.set_index('id')['ml_target'].to_dict()
nx.set_node_attributes(G, target_dict, 'ml_target')
def spread_with_RLR_regulation(G, initial_infected, p, q, rho, steps=10):
    # Initialize the set of infected nodes with the initial infected set
    infected = set(initial_infected)
    # Record the size of the infected set at each step
    sizes = [len(infected)]

    for _ in range(steps):
        new_infected = set()
        for node in infected:
            # Get the neighbors of the node
            neighbors = G.neighbors(node)
            for neighbor in neighbors:
                # If the neighbor is already infected, do nothing
                if neighbor in infected:
                    continue
                # Homophily influence: Check if the node and neighbor have the same ml_target
                same_target = G.nodes[node]['ml_target'] == G.nodes[neighbor]['ml_target']
                # Determine infection probability
                infection_probability = p if same_target else q
                # Apply RLR regulation
                infection_probability *= (1 - rho)
                # Infect with the determined probability
                if random.random() < infection_probability:
                    new_infected.add(neighbor)
        # Update the infected set with the new infections
        infected.update(new_infected)
        # Record the new size of the infected set
        sizes.append(len(infected))

    return sizes


# RLR regulation parameters
rho_values = [0.25, 0.5]

# Record results for each regulation parameter
results_RLR_regulation = {}

for rho in rho_values:
    # Strong-homophily
    sizes_strong_homophily_RLR = spread_with_RLR_regulation(G, initial_infected, p=1, q=0, rho=rho)
    # p-homophily with p=0.7 and q=0.3
    sizes_p_homophily_RLR = spread_with_RLR_regulation(G, initial_infected, p=0.7, q=0.3, rho=rho)

    # Store the results
    results_RLR_regulation[rho] = {
        'Strong-homophily': sizes_strong_homophily_RLR,
        'p-homophily': sizes_p_homophily_RLR
    }

# Plot the results similar to the example figure
plt.figure(figsize=(10, 6))

for rho in rho_values:
    plt.plot(range(11), results_RLR_regulation[rho]['Strong-homophily'], label=f'Strong-homophily RLR (ρ={rho})')
    plt.plot(range(11), results_RLR_regulation[rho]['p-homophily'], label=f'p-homophily RLR (ρ={rho})')

plt.xlabel('target set size')
plt.ylabel('active set size')
plt.title('Spreading with RLR regulation')
plt.legend()
plt.show()
