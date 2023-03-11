from plots.independent.network import create_graph
from networkx.algorithms import bipartite


def compute_spectral_bipartivity(prices):
    g = create_graph(prices)

    return bipartite.spectral_bipartivity(g)
