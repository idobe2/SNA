import pandas as pd
import networkx as nx

# Load the data with proper handling to skip any problematic rows
try:
    edges = pd.read_csv('../../csv/musae_git_edges.csv')
    target = pd.read_csv('../../csv/git_target_languages.csv')
except Exception as e:
    print("Error loading CSV files:", e)
    raise

# Check for any rows where 'id' columns might have non-numeric data
print("Checking for non-numeric data in 'id' columns...")
print(target[target['id'].apply(lambda x: not str(x).isdigit())])
print(edges[edges['id_1'].apply(lambda x: not str(x).isdigit())])
print(edges[edges['id_2'].apply(lambda x: not str(x).isdigit())])

# Convert 'id' to int explicitly after cleaning
target['id'] = pd.to_numeric(target['id'], errors='coerce')
edges['id_1'] = pd.to_numeric(edges['id_1'], errors='coerce')
edges['id_2'] = pd.to_numeric(edges['id_2'], errors='coerce')

# Drop any rows with NaN values that resulted from conversion errors
target.dropna(subset=['id'], inplace=True)
edges.dropna(subset=['id_1', 'id_2'], inplace=True)

# Prepare the network
G = nx.from_pandas_edgelist(edges, 'id_1', 'id_2')

# Set attributes
attributes = target.set_index('id').to_dict('index')
nx.set_node_attributes(G, attributes)


# Define a function to calculate expected and observed homophily
def homophily_test(graph, attribute):
    degrees = dict(graph.degree())
    m = len(graph.edges())
    total_possible_edges = sum(degrees.values())

    same_attr_expected = 0
    different_attr_expected = 0
    observed_same_attr = 0
    observed_different_attr = 0

    for node, data in graph.nodes(data=True):
        node_attr = data.get(attribute)
        if node_attr is None:
            continue
        for neighbor in graph.neighbors(node):
            neighbor_attr = graph.nodes[neighbor].get(attribute)
            if neighbor_attr is None:
                continue
            if node_attr == neighbor_attr:
                observed_same_attr += 1
            else:
                observed_different_attr += 1

            same_attr_expected += (degrees[node] * degrees[neighbor]) / total_possible_edges
            different_attr_expected += (degrees[node] * degrees[neighbor]) / total_possible_edges

    observed_same_attr /= 2
    observed_different_attr /= 2
    same_attr_expected /= 2
    different_attr_expected /= 2

    return {
        'observed_same': observed_same_attr,
        'observed_different': observed_different_attr,
        'expected_same': same_attr_expected,
        'expected_different': different_attr_expected
    }


# Calculate homophily for developer group and programming language
homophily_ml_target = homophily_test(G, 'ml_target')
homophily_language = homophily_test(G, 'most_common_language')

print("Homophily based on developer group (web vs. ML):")
print(homophily_ml_target)
print("\nHomophily based on programming language:")
print(homophily_language)
