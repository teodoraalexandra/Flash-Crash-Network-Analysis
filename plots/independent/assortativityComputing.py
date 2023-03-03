from plots.independent.network import create_graph
import networkx as nx


def compute_assortativity(prices):
    g = create_graph(prices)

    # Compute the assortativity of the graph
    # This function calculates Pearson's correlation coefficient between
    # the degrees of all pairs of connected nodes in the graph.
    return nx.degree_assortativity_coefficient(g)

# The degree_assortativity_coefficient function returns a value between -1 and 1,
# where a value of -1 means that nodes tend to connect to nodes with a different degree,
# a value of 0 means that the degree of connected nodes is uncorrelated,
# and a value of 1 means that nodes tend to connect to nodes with the same degree.
