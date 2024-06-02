from plots.independent.network import create_graph
from networkx.algorithms import bipartite
import networkx as nx


def calculate_easley_vpin(bucket):
    buy_volume = sum(trade.quantity for trade in bucket if trade.direction == 'B')
    sell_volume = sum(trade.quantity for trade in bucket if trade.direction == 'A')
    total_volume = buy_volume + sell_volume
    imbalance = abs(buy_volume - sell_volume) / total_volume if total_volume != 0 else 0
    return imbalance

def compute_metrics(prices, granularity):
    # Length of prices = length of edges from the graph
    informed_transactions = 0
    uninformed_transactions = 0
    market_makers_transactions = 0

    total_transactions = 0
    average = 0
    items = 0

    g = create_graph(prices)
    easley_vpin = calculate_easley_vpin(prices)

    for price in prices:
        if price.first_agent.startswith("Overvalued"):
            informed_transactions += 1
        if price.second_agent.startswith("Overvalued"):
            informed_transactions += 1

        if price.first_agent.startswith("Noise"):
            uninformed_transactions += 1
        if price.second_agent.startswith("Noise"):
            uninformed_transactions += 1

        if price.first_agent.startswith("MM"):
            market_makers_transactions += 1
        if price.second_agent.startswith("MM"):
            market_makers_transactions += 1

        total_transactions += 1
        # Add the prices to y-axis -> Average of all prices from chunk
        average += price.price
        items += 1

    vpin = informed_transactions / total_transactions

    if granularity == 0:
        if bipartite.is_bipartite(g):
            isGraphBipartite = bipartite.average_clustering(g)
        else:
            isGraphBipartite = 2

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

        try:
            independent_set = nx.maximal_independent_set(g)
            maximal_independent_set_length = len(independent_set)
        except nx.NetworkXUnfeasible:
            maximal_independent_set_length = 0

        num_stars = sum(1 for node in g if g.degree(node) == 1)

        return vpin, easley_vpin, average / items, nx.degree_assortativity_coefficient(g), isGraphBipartite, \
            diameter, maximal_independent_set_length, num_stars

    if granularity == 1:
        betweenness_dict = nx.betweenness_centrality(g)
        closeness_dict = nx.closeness_centrality(g)

        return vpin, easley_vpin, average / items, max(betweenness_dict.values()), nx.density(g), \
            max(closeness_dict.values()), nx.number_connected_components(g)

    if granularity == 2:
        return average / items, informed_transactions, uninformed_transactions, market_makers_transactions
