from processFile import *
import networkx as nx


def compute_degree_centrality(prices):
    # Create an empty graph
    G = nx.Graph()

    # Add nodes and edges to the graph
    informed = []
    uninformed = []
    edges = []
    for price in prices:
        if price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Undervalued"):
            informed.append(price.first_agent)
        elif price.first_agent.startswith("ZIT") or price.first_agent.startswith("Noise"):
            uninformed.append(price.first_agent)

        if price.second_agent.startswith("Overvalued") or price.second_agent.startswith("Undervalued"):
            informed.append(price.second_agent)
        elif price.second_agent.startswith("ZIT") or price.second_agent.startswith("Noise"):
            uninformed.append(price.second_agent)

        edges.append((price.first_agent, price.second_agent))

    G.add_nodes_from(informed, bipartite=0)
    G.add_nodes_from(uninformed, bipartite=1)
    G.add_edges_from(edges)

    return nx.degree_centrality(G)


index = 1
result = process()

for day, price_array in result.items():
    degree_centrality = compute_degree_centrality(price_array)
    print("Day: ", index, "Central node: ", degree_centrality)
    index += 1
