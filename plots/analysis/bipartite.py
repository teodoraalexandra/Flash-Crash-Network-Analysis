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

# Check if the graph is bipartite
print(nx.is_bipartite(G))

# ----- Example of bipartite graph -----
# # Create an empty bipartite graph
# G = nx.Graph()
#
# # Add nodes to the graph
# A = [1, 2, 3]
# B = ['a', 'b', 'c']
# G.add_nodes_from(A, bipartite=0)
# G.add_nodes_from(B, bipartite=1)
#
# # Add edges to the graph
# G.add_edges_from([(1, 'a'), (1, 'b'), (2, 'b'), (2, 'c'), (3, 'c')])
#
# # Check if the graph is bipartite
# print(nx.is_bipartite(G))
