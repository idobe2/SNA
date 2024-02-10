# import snap

import networkx as nx
import matplotlib.pyplot as plt

g = nx.read_edgelist('graphs/Wiki-Vote.txt', create_using=nx.DiGraph(), nodetype=int)

print(nx.info(g))

sp = nx.spring_layout(g)

plt.axis('off')

nx.draw_networkx(g, pos=sp, with_labels=False, node_size=35)

plt.show()






