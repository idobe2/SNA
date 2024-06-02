import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Set the display option to show all rows
pd.set_option('display.max_rows', None)

users = pd.read_csv('../../csv/musae_git_target.csv')

Data = open('../../csv/musae_git_edges.csv', "r")

next(Data, None)  # skip the first line in the input file

followers = nx.parse_edgelist(Data, delimiter=',', create_using=nx.Graph(), nodetype=int)

local_cluster = nx.clustering(followers)
sorted_local_cluster = {k: v for k, v in sorted(local_cluster.items(), key=lambda item: item[1])}

# global_cluster = nx.average_clustering(followers, count_zeros=True)
# print(global_cluster)

with open('../../pickle/eccentricity.pkl', 'rb') as f:
    eccentricity = pickle.load(f)

# eccentricity = nx.eccentricity(followers)
# sorted_eccentricity = {k: v for k, v in sorted(eccentricity.items(), key=lambda item: item[1])}

sorted_eccentricity = list(dict(sorted(eccentricity.items(), key=lambda item: item[1], reverse=True)).items())

num_nodes_to_display = 50

dev_type = 1

# get index (node number) and value (node eccentricity value) top x after sorting
sorted_eccentricity_indexes = [x[0] for x in sorted_eccentricity[:num_nodes_to_display]]
sorted_eccentricity_values = [x[1] for x in sorted_eccentricity[:num_nodes_to_display]]

# Creating dataframe
top_sorted_eccentricity = pd.DataFrame({'Name':users.iloc[sorted_eccentricity_indexes].name.tolist(),
                                      'Eccentricity': sorted_eccentricity_values,
                                      'ml_target':users.iloc[sorted_eccentricity_indexes].ml_target.tolist()})

print(top_sorted_eccentricity.groupby('Eccentricity').count()['ml_target'].sort_values(ascending=False))

local_clustering_sort = list((k,v) for k, v in sorted(local_cluster.items(), key=lambda item: item[0], reverse=True))
eccentricity_sort = list((k,v)for k, v in sorted(eccentricity.items(), key=lambda item: item[0], reverse=True))

# get index (node number) and value (node centrality value) top x after sorting
sorted_indexes = [x[0] for x in local_clustering_sort[:num_nodes_to_display]]
local_values_sort = [x[1] for x in local_clustering_sort[:num_nodes_to_display]]
eccentricity_values_sort = [x[1] for x in eccentricity_sort[:num_nodes_to_display]]

# Creating dataframe
eccentricity_and_local_cluster = pd.DataFrame({'Name':users.iloc[sorted_indexes].name.tolist(),
                                      'Eccentricity': eccentricity_values_sort,
                                      'Local Clustering': local_values_sort,
                                      'ml_target': users.iloc[sorted_eccentricity_indexes].ml_target.tolist()})

# print(eccentricity_and_local_cluster[eccentricity_and_local_cluster['ml_target'] == dev_type])
print(eccentricity_and_local_cluster)

# Applying degree centrality in NetworX
deg_centrality = nx.degree_centrality(followers)

# Sorting degree centrality and getting top x
sorted_deg_centrality = list(dict(sorted(deg_centrality.items(), key=lambda item: item[1], reverse=True)).items())

# get index (node number) and value (node centrality value) top x after sorting
sorted_deg_centrality_indexes = [x[0] for x in sorted_deg_centrality[:num_nodes_to_display]]
sorted_deg_centrality_values = [x[1] for x in sorted_deg_centrality[:num_nodes_to_display]]

# Creating dataframe
top_degree_centrality = pd.DataFrame({'Name':users.iloc[sorted_deg_centrality_indexes].name.tolist(),
                                      'Degree Centrality': sorted_deg_centrality_values,
                                      'ml_target':users.iloc[sorted_deg_centrality_indexes].ml_target.tolist()})

# print(top_degree_centrality[top_degree_centrality['ml_target'] == dev_type])
print(top_degree_centrality)

with open('../../pickle/closness_centrality.pkl', 'rb') as f:
    closeness_centrality = pickle.load(f)

# Applying closeness centrality in NetworX
# closeness_centrality = nx.closeness_centrality(followers)

# Sorting degree centrality and getting top x
sorted_closness_centrality = list(dict(sorted(closeness_centrality.items(), key=lambda item: item[1], reverse=True)).items())

# get index (node number) and value (node centrality value) top x after sorting
sorted_closeness_centrality_indexes = [x[0] for x in sorted_closness_centrality[:num_nodes_to_display]]
sorted_closeness_centrality_values = [x[1] for x in sorted_closness_centrality[:num_nodes_to_display]]

# Creating dataframe
top_closeness_centrality = pd.DataFrame({'Name':users.iloc[sorted_closeness_centrality_indexes].name.tolist(),
                                      'Closeness Centrality': sorted_closeness_centrality_values,
                                      'ml_target':users.iloc[sorted_closeness_centrality_indexes].ml_target.tolist()})

# print(top_closeness_centrality[top_closeness_centrality['ml_target'] == dev_type])
print(top_closeness_centrality)

with open('../../pickle/betweeness_centrality.pkl', 'rb') as f:
    betweeness_centrality = pickle.load(f)

# Applying betweeness centrality in NetworX
# betweeness_centrality = nx.betweenness_centrality(followers)

# Sorting degree centrality and getting top x
sorted_between_centrality = list(dict(sorted(betweeness_centrality.items(), key=lambda item: item[1], reverse=True)).items())

# get index (node number) and value (node centrality value) top x after sorting
sorted_between_centrality_indexes = [x[0] for x in sorted_between_centrality[:num_nodes_to_display]]
sorted_between_centrality_values = [x[1] for x in sorted_between_centrality[:num_nodes_to_display]]

# Creating dataframe
top_between_centrality = pd.DataFrame({'Name':users.iloc[sorted_between_centrality_indexes].name.tolist(),
                                      'Betweeness Centrality': sorted_between_centrality_values,
                                      'ml_target':users.iloc[sorted_between_centrality_indexes].ml_target.tolist()})

# print(top_between_centrality[top_between_centrality['ml_target'] == dev_type])
print(top_between_centrality)
