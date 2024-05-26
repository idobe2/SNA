import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Load eccentricity data
# with open('../../pickle/eccentricity.pkl', 'rb') as f:
#     eccentricity = pickle.load(f)

# Load user data
users = pd.read_csv('../../csv/musae_git_target.csv')

# Load edges data and create a graph
Data = open('../../csv/musae_git_edges.csv', "r")
next(Data, None)  # skip the first line in the input file
G = nx.parse_edgelist(Data, delimiter=',', create_using=nx.Graph(), nodetype=int)
Data.close()

# Ensure the user IDs match between 'users' DataFrame and the graph G
# Assuming 'id' is the column in users DataFrame that corresponds to node in graph G
users = users.set_index('id')

# Calculate the average degree for ml_target = 0 and ml_target = 1
for target_value in [0, 1]:
    # Filter nodes by ml_target value
    target_nodes = users[users['ml_target'] == target_value].index
    # Create a subgraph for the current target value
    subgraph = G.subgraph(target_nodes)
    # Calculate the sum of degrees of the subgraph
    sum_of_degrees = sum(dict(subgraph.degree()).values())
    # Calculate the average degree
    average_degree = sum_of_degrees / subgraph.number_of_nodes()
    print(f"Average degree for ml_target={target_value}: {average_degree}")
