import pandas as pd
import igraph

# Read the CSV file
df = pd.read_csv('../../txt/games.csv')

# Create a graph object
g = igraph.Graph()

# Add vertices for each game
for index, row in df.iterrows():
    g.add_vertex(name=row['Title'])

# Visualize the graph
layout = g.layout_fruchterman_reingold()
igraph.plot(g, target='game_graph.png', bbox=(1920, 1080), layout=layout)
