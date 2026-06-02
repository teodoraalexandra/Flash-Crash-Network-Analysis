from plots.independent.network import create_graph
from networkx.algorithms import bipartite
import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigsh

def compute_bipartivity(g):
    n = g.number_of_nodes()
    if n < 2 or g.number_of_edges() == 0:
        return 0.0

    visited = set()
    total_nodes = 0
    weighted_imbalance = 0.0

    for start in g.nodes():
        if start in visited:
            continue

        color = {start: 0}
        stack = [start]
        comp_nodes = [start]
        component_is_bipartite = True

        while stack:
            u = stack.pop()
            for v in g.neighbors(u):
                if v not in color:
                    color[v] = 1 - color[u]
                    stack.append(v)
                    comp_nodes.append(v)
                elif color[v] == color[u]:
                    component_is_bipartite = False

        visited.update(comp_nodes)

        if not component_is_bipartite or len(comp_nodes) < 2:
            continue

        side0 = sum(1 for u in comp_nodes if color[u] == 0)
        side1 = len(comp_nodes) - side0
        imbalance = abs(side0 - side1) / (side0 + side1)
        weighted_imbalance += imbalance * len(comp_nodes)
        total_nodes += len(comp_nodes)

    if total_nodes == 0:
        return 0.0
    return weighted_imbalance / total_nodes

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

    if bipartite.is_bipartite(g):
        isGraphBipartite = bipartite.average_clustering(g)
    else:
        isGraphBipartite = 2

    try:
        if nx.is_connected(g):
            diameter = nx.diameter(g)
        else:
            largest_cc = max(nx.connected_components(g), key=len)
            diameter = nx.diameter(g.subgraph(largest_cc))
    except nx.NetworkXError:
        diameter = 0

    try:
        independent_set = nx.maximal_independent_set(g)
        maximal_independent_set_length = len(independent_set)
    except nx.NetworkXUnfeasible:
        maximal_independent_set_length = 0

    num_stars = sum(
        leaf_count
        for node in g
        for leaf_count in [sum(1 for nbr in g.neighbors(node) if g.degree(nbr) == 1)]
        if leaf_count >= 2
    )

    betweenness_dict = nx.betweenness_centrality(g)
    closeness_dict = nx.closeness_centrality(g)

    assortativity = nx.degree_assortativity_coefficient(g)
    average_clustering = isGraphBipartite

    betweenness = max(betweenness_dict.values())
    closeness = max(closeness_dict.values())
    bipartivity = compute_bipartivity(g)
    connected_components = nx.number_connected_components(g)

    if granularity == 0 or granularity == 1:
        return vpin, easley_vpin, average / items, assortativity, bipartivity, average_clustering, connected_components, num_stars, diameter, maximal_independent_set_length, closeness, betweenness

    if granularity == 2:
        return average / items, informed_transactions, uninformed_transactions, market_makers_transactions

    return None
