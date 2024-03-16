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


def spread_with_new_regulation(G, initial_infected, p, q, rho, gamma, steps=10):
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
                # Apply new regulation: if any node is an ML developer, reduce the infection probability
                if G.nodes[node]['ml_target'] == 1 or G.nodes[neighbor]['ml_target'] == 1:
                    infection_probability *= gamma
                # Infect with the determined probability
                if random.random() < infection_probability:
                    new_infected.add(neighbor)
        # Update the infected set with the new infections
        infected.update(new_infected)
        # Record the new size of the infected set
        sizes.append(len(infected))

    return sizes


# New regulation parameter
gamma = 0.7  # Reduction factor for infection probability when at least one ML developer is involved

# Record results for the new regulation
results_new_regulation = {}

# Strong-homophily
sizes_strong_homophily_new_reg = spread_with_new_regulation(G, initial_infected, p=1, q=0, rho=0.25, gamma=gamma)
# p-homophily with p=0.7 and q=0.3
sizes_p_homophily_new_reg = spread_with_new_regulation(G, initial_infected, p=0.7, q=0.3, rho=0.25, gamma=gamma)

# Store the results
results_new_regulation['Strong-homophily'] = sizes_strong_homophily_new_reg
results_new_regulation['p-homophily'] = sizes_p_homophily_new_reg

# Plot the results similar to the example figure
plt.figure(figsize=(10, 6))
plt.plot(range(11), results_new_regulation['Strong-homophily'], label='Strong-homophily new regulation')
plt.plot(range(11), results_new_regulation['p-homophily'], label='p-homophily new regulation')
plt.xlabel('target set size')
plt.ylabel('active set size')
plt.title('Spreading with new regulation')
plt.legend()
plt.show()
