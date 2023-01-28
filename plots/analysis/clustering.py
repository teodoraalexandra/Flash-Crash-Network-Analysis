# Clustering = the process of identifying groups of nodes in a network
# that are more densely connected to each other than to the rest of the network.
# Clustering can reveal the underlying structure of a social network and
# help identify communities or subgroups within it.

import networkx as nx
from networkx.algorithms import community
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("../prices.csv", sep=';')

# Create an empty graph
G = nx.Graph()

# Add nodes and edges to the graph
nodes = []
edges = []
for _, row in df.iterrows():
    first_agent = row["AgTrigger"]
    second_agent = row["ag2"]
    if first_agent != 'noname' and second_agent != 'noname':
        nodes.append(first_agent)
        nodes.append(second_agent)
    if first_agent != 'noname' and second_agent != 'noname':
        edges.append((first_agent, second_agent))

G.add_nodes_from(nodes)
G.add_edges_from(edges)

communities_generator = community.girvan_newman(G)
top_level_communities = next(communities_generator)
next_level_communities = next(communities_generator)

node_lists_community1 = sorted(map(sorted, next_level_communities))[0]
node_lists_community2 = sorted(map(sorted, next_level_communities))[1]
node_lists_community3 = sorted(map(sorted, next_level_communities))[2]

pos = nx.spring_layout(G)

# Draw the graph, but don't color the nodes
nx.draw(G, pos)

# For each community list, draw the nodes, giving it a specific color.
nx.draw_networkx_nodes(G, pos, nodelist=node_lists_community1, node_color='b')
nx.draw_networkx_nodes(G, pos, nodelist=node_lists_community2, node_color='r')
nx.draw_networkx_nodes(G, pos, nodelist=node_lists_community3, node_color='g')

plt.show()
