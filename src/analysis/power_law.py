import pandas as pd
import networkx as nx
import powerlaw  # Library for the statistical analysis of power laws
import matplotlib.pyplot as plt

# Load data from CSV
edges = pd.read_csv('../../csv/musae_git_edges.csv')
# Construct the graph
G = nx.Graph()
G.add_edges_from(edges.values)

# Get the degree distribution of the nodes
degrees = [degree for node, degree in G.degree()]

# Fit the degree distribution to a power-law
fit = powerlaw.Fit(degrees)
print("Alpha:", fit.power_law.alpha)
print("Sigma:", fit.power_law.sigma)

# Compare the power-law fit with other distributions
R, p = fit.distribution_compare('power_law', 'exponential')
print("Loglikelihood ratio between power law and exponential:", R)
print("p-value of the fit:", p)

# Plot the degree distribution and the power-law fit
fig = fit.plot_pdf(color='b', linewidth=2)
fit.power_law.plot_pdf(color='b', linestyle='--', ax=fig)
plt.show()
