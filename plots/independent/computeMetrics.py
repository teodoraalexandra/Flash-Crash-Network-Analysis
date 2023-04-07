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
        nx.density(g), isGraphBipartite, nx.number_connected_components(g), average / items, num_stars
