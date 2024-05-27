import pandas as pd
import networkx as nx

edges_path = "../../csv/musae_git_edges.csv"
attributes_path = "../../csv/git_target_languages.csv"

edges_df = pd.read_csv(edges_path)
attributes_df = pd.read_csv(attributes_path)

# Create the graph
G = nx.from_pandas_edgelist(edges_df, source='Source', target='Target')


# Add attributes to nodes
developer_type_dict = attributes_df.set_index('id')['ml_target'].to_dict()
programming_language_dict = attributes_df.set_index('id')['most_common_language'].to_dict()

nx.set_node_attributes(G, developer_type_dict, 'developer_type')
nx.set_node_attributes(G, programming_language_dict, 'programming_language')

# Check if all nodes have the necessary attributes
nodes_with_missing_data = [node for node, attr in G.nodes(data=True) if 'developer_type' not in attr or 'programming_language' not in attr]
if nodes_with_missing_data:
    print("Nodes with missing data:", nodes_with_missing_data)
else:
    print("All nodes have attributes assigned.")

# Check and print unique values of attributes
print("Unique Developer Types:", attributes_df['ml_target'].unique())
print("Unique Programming Languages:", attributes_df['most_common_language'].unique())

# Check for NaN values
print("Missing 'developer_type' values:", attributes_df['ml_target'].isnull().sum())
print("Missing 'programming_language' values:", attributes_df['most_common_language'].isnull().sum())

# Recalculate assortativity coefficients
type_assortativity = nx.attribute_assortativity_coefficient(G, 'developer_type')
language_assortativity = nx.attribute_assortativity_coefficient(G, 'programming_language')

print(f"Assortativity Coefficient for Developer Type: {type_assortativity}")
print(f"Assortativity Coefficient for Programming Language: {language_assortativity}")
