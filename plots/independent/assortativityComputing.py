from plots.independent.processFile import *
import networkx as nx


def compute_assortativity(prices):
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

    # Compute the assortativity of the graph
    # This function calculates Pearson's correlation coefficient between
    # the degrees of all pairs of connected nodes in the graph.
    return nx.degree_assortativity_coefficient(G)


# index = 1
# result = process()
#
# for day, price_array in result.items():
#     assortativity = compute_assortativity(price_array)
#     print("Day: ", index, "Assortativity: ", assortativity)
#     index += 1

# The degree_assortativity_coefficient function returns a value between -1 and 1,
# where a value of -1 means that nodes tend to connect to nodes with a different degree,
# a value of 0 means that the degree of connected nodes is uncorrelated,
# and a value of 1 means that nodes tend to connect to nodes with the same degree.
