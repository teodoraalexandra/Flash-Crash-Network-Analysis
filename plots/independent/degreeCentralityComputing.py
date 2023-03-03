from plots.independent.network import create_graph
import networkx as nx


def compute_degree_centrality(prices):
    g = create_graph(prices)

    return nx.degree_centrality(g)
