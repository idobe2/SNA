import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Load the data from CSV
df = pd.read_csv("../../../csv/stormofswords.csv")
edges = [(row["Source"], row["Target"], {"weight": row["Weight"]}) for index, row in df.iterrows()]

# Create the original network
G_original = nx.Graph()
G_original.add_edges_from(edges)

# Plot the original network
plt.figure(figsize=(8, 6))
nx.draw(G_original, with_labels=True, font_weight='bold')
plt.title("Original Network")
plt.show()

# 1a. G(n,p) model
n = len(G_original.nodes)
p = 0.2  # Adjust the probability as needed
G_Gnp = nx.erdos_renyi_graph(n, p)

# Plot the G(n,p) model
plt.figure(figsize=(8, 6))
nx.draw(G_Gnp, with_labels=True, font_weight='bold')
plt.title("G(n,p) Model")
plt.show()

# 1b. G(n,m) model
m = len(G_original.edges)
G_Gnm = nx.gnm_random_graph(n, m)

# Plot the G(n,m) model
plt.figure(figsize=(8, 6))
nx.draw(G_Gnm, with_labels=True, font_weight='bold')
plt.title("G(n,m) Model")
plt.show()

# 1c. Configuration model
degrees = [val for (node, val) in G_original.degree()]
G_configuration = nx.configuration_model(degrees)

# Plot the Configuration model
plt.figure(figsize=(8, 6))
nx.draw(G_configuration, with_labels=True, font_weight='bold')
plt.title("Configuration Model")
plt.show()

# 1d. Bonus: Block model (example, you may need to customize)
G_block = nx.random_partition_graph([4, 5], 0.5, 0.05)

# Plot the Block model
plt.figure(figsize=(8, 6))
nx.draw(G_block, with_labels=True, font_weight='bold')
plt.title("Block Model")
plt.show()
