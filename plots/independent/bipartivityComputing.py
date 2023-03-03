from plots.independent.network import create_graph
from networkx.algorithms import bipartite
import networkx as nx


def compute_bipartivity(prices):
    g = create_graph(prices)

    # return bipartite.spectral_bipartivity(g)
    return nx.density(g)
