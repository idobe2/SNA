import snap
import networkx as nx
import matplotlib.pyplot as plt

g = nx.read_edgelist('Wiki-Vote.txt', create_using=nx.DiGraph(), nodetype=int)

print(nx.info(g))

sp = nx.spring_layout(g)

plt.axis('off')

nx.draw_networkx(g, pos=sp, with_labels=False, node_size=35)

plt.show()

# import snap
# import graphviz
#
# def load_graph_from_txt(filename):
#     # Create a new undirected graph
#     graph = snap.TUNGraph.New()
#
#     # Read the graph from the text file
#     with open(filename, 'r') as file:
#         for line in file:
#             src, dst = map(int, line.strip().split())  # assuming each line contains source and destination nodes
#             if not graph.IsNode(src):
#                 graph.AddNode(src)
#             if not graph.IsNode(dst):
#                 graph.AddNode(dst)
#             graph.AddEdge(src, dst)
#
#     return graph
#
# def visualize_graph(graph):
#     # Draw the graph
#     snap.DrawGViz(graph, snap.gvlDot, "facebook_graph.png", "Facebook Graph", True)
#
# if __name__ == "__main__":
#     filename = "facebook_combined.txt"  # Path to the facebook_combined.txt file
#     graph = load_graph_from_txt(filename)
#     visualize_graph(graph)




