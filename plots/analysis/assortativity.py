import networkx as nx
import pandas as pd

# Read the CSV file
df = pd.read_csv("../prices.csv", sep=';')

# Create an empty graph
G = nx.Graph()

# Add nodes and edges to the graph
buyers = []
sellers = []
edges = []
for _, row in df.iterrows():
    first_agent = row["AgTrigger"]
    second_agent = row["ag2"]
    direction = row["dirTrigger"]
    if direction == 'A' and first_agent != 'noname':
        sellers.append(first_agent)
    if direction == 'B' and first_agent != 'noname':
        buyers.append(first_agent)
    if first_agent != 'noname' and second_agent != 'noname':
        edges.append((first_agent, second_agent))

G.add_nodes_from(buyers, bipartite=0)
G.add_nodes_from(sellers, bipartite=1)
G.add_edges_from(edges)

# Compute the assortativity of the graph
# This function calculates Pearson's correlation coefficient between
# the degrees of all pairs of connected nodes in the graph.
r = nx.degree_assortativity_coefficient(G)
print(r)

# The degree_assortativity_coefficient function returns a value between -1 and 1,
# where a value of -1 means that nodes tend to connect to nodes with a different degree,
# a value of 0 means that the degree of connected nodes is uncorrelated,
# and a value of 1 means that nodes tend to connect to nodes with the same degree.
