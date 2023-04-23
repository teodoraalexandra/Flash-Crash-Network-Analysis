from plots.independent.network import create_graph
from networkx.algorithms import bipartite
import networkx as nx


def compute_metrics(prices):
    # Length of prices = length of edges from the graph
    informed_transactions = 0
    total_transactions = 0
    average = 0
    items = 0
    g = create_graph(prices)

    for price in prices:
        if price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Undervalued") \
                or price.second_agent.startswith("Overvalued") or price.second_agent.startswith("Undervalued"):
            informed_transactions += 1
        total_transactions += 1

        # Add the prices to y-axis -> Average of all prices from chunk
        average += price.price
        items += 1

    if bipartite.is_bipartite(g):
        isGraphBipartite = bipartite.average_clustering(g)
    else:
        isGraphBipartite = 2

    num_stars = sum(1 for node in g if g.degree(node) == 1)

    return informed_transactions / total_transactions, nx.degree_assortativity_coefficient(g), \
        nx.density(g), isGraphBipartite, bipartite.spectral_bipartivity(g), nx.number_connected_components(g), \
        average / items, num_stars

# Defs
# Compute the assortativity of the graph
# This function calculates Pearson's correlation coefficient between
# the degrees of all pairs of connected nodes in the graph.
# The degree_assortativity_coefficient function returns a value between -1 and 1,
# where a value of -1 means that nodes tend to connect to nodes with a different degree,
# a value of 0 means that the degree of connected nodes is uncorrelated,
# and a value of 1 means that nodes tend to connect to nodes with the same degree.
