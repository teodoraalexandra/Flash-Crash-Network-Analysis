from plots.independent.network import create_graph
import networkx as nx


def compute_bipartivity(prices):
    g = create_graph(prices)

    return nx.density(g)
