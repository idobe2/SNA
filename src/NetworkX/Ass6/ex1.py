import pandas as pd
import networkx as nx
import random
import matplotlib.pyplot as plt

# Reading the data from the CSV files
edges_df = pd.read_csv('../../../csv/musae_git_edges.csv')
target_df = pd.read_csv('../../../csv/musae_git_target.csv')

# Creating the graph from the edges data
G = nx.from_pandas_edgelist(edges_df, 'Source', 'Target')

# Mapping the 'ml_target' attribute to the nodes
target_dict = target_df.set_index('id')['ml_target'].to_dict()
nx.set_node_attributes(G, target_dict, 'ml_target')

def spread_without_regulation(G, initial_infected, p, q, steps=10):
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
                # Infect with the determined probability
                if random.random() < infection_probability:
                    new_infected.add(neighbor)
        # Update the infected set with the new infections
        infected.update(new_infected)
        # Record the new size of the infected set
        sizes.append(len(infected))

    return sizes


# We need to select a set of initial infected nodes, let's randomly select 10 nodes for simplicity
initial_infected = random.sample(list(G.nodes), 10)

# Run the simulation for spreading without regulation
# For strong-homophily (p=1, q=0)
sizes_strong_homophily = spread_without_regulation(G, initial_infected, p=1, q=0)

# For p-homophily with p=0.7 and q=0.3
sizes_p_homophily = spread_without_regulation(G, initial_infected, p=0.7, q=0.3)

# Plot the results similar to the example figure
plt.figure(figsize=(10, 6))
plt.plot(range(11), sizes_strong_homophily, label='Strong-homophily (p=1, q=0)')
plt.plot(range(11), sizes_p_homophily, label='p-homophily (p=0.7, q=0.3)')
plt.xlabel('tatget set size')
plt.ylabel('active set size')
plt.title('Spreading without regulation')
plt.legend()
plt.show()
