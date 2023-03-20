from plots.independent.network import create_graph
from networkx.algorithms import bipartite
import networkx as nx


def compute_metrics(prices):
    # Length of prices = length of edges from the graph
    informed_transactions = 0
    total_transactions = 0
    g = create_graph(prices)

    for price in prices:
        if price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Undervalued") \
                or price.second_agent.startswith("Overvalued") or price.second_agent.startswith("Undervalued"):
            informed_transactions += 1
        total_transactions += 1

    return informed_transactions / total_transactions, nx.degree_assortativity_coefficient(g), \
        nx.density(g), bipartite.spectral_bipartivity(g)
