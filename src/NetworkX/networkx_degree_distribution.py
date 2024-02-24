# Importing Libraries
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Importing dataset
users = pd.read_csv('../../csv/musae_git_target.csv')

# Reading Graphs
Data = open('../../csv/musae_git_edges.csv', "r")
next(Data, None)  # skip the first line in the input file
followers = nx.parse_edgelist(Data, delimiter=',', create_using=nx.Graph(), nodetype=int)

degree_distribution = nx.degree_histogram(followers)
fig = plt.figure(figsize=(15, 10))
x = [i for i in range(0, 50)]
plt.bar(x, degree_distribution[0:50])
plt.show()
