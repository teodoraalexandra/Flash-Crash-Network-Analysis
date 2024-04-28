from plots.independent.network import create_graph
from networkx.algorithms import bipartite
import networkx as nx


def compute_metrics(prices, granularity):
    # Length of prices = length of edges from the graph
    informed_transactions = 0
    total_transactions = 0
    average = 0
    items = 0
    g = create_graph(prices)

    for price in prices:
        if price.first_agent.startswith("Overvalued") or price.second_agent.startswith("Overvalued"):
            informed_transactions += 1
        total_transactions += 1

        # Add the prices to y-axis -> Average of all prices from chunk
        average += price.price
        items += 1

    if granularity == 0:
        try:
            if nx.is_connected(g):
                diameter = nx.diameter(g)
            else:
                diameters = []
                for component in nx.connected_components(g):
                    subgraph = g.subgraph(component)
                    diameter = nx.diameter(subgraph)
                    diameters.append(diameter)
                diameter = max(diameters)
        except nx.NetworkXError:
            diameter = 0

        num_stars = sum(1 for node in g if g.degree(node) == 1)

        return informed_transactions / total_transactions, average / items, diameter, num_stars

    if granularity == 1:
        try:
            independent_set = nx.maximal_independent_set(g)
            maximal_independent_set_length = len(independent_set)
        except nx.NetworkXUnfeasible:
            maximal_independent_set_length = 0

        return informed_transactions / total_transactions, average / items, maximal_independent_set_length, \
            nx.degree_assortativity_coefficient(g), nx.number_connected_components(g), nx.density(g)

    if granularity == 2:
        closeness_dict = nx.closeness_centrality(g)
        betweenness_dict = nx.betweenness_centrality(g)

        if bipartite.is_bipartite(g):
            isGraphBipartite = bipartite.average_clustering(g)
        else:
            isGraphBipartite = 2

        return informed_transactions / total_transactions, average / items, \
            max(closeness_dict.values()), max(betweenness_dict.values()), isGraphBipartite

    if granularity == 3:
        return average / items
