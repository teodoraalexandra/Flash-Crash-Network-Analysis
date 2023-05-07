from plots.independent.network import create_graph
import networkx as nx


def compute_complex_metrics(prices, granularity):
    # Length of prices = length of edges from the graph
    informed_transactions = 0
    total_transactions = 0

    g = create_graph(prices)

    for price in prices:
        if price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Undervalued") \
                or price.second_agent.startswith("Overvalued") or price.second_agent.startswith("Undervalued"):
            informed_transactions += 1
        total_transactions += 1

    if granularity == 0:
        try:
            independent_set = nx.maximal_independent_set(g)
            maximal_independent_set_length = len(independent_set)
        except nx.NetworkXUnfeasible:
            maximal_independent_set_length = 0

        try:
            if nx.is_connected(g):
                # For core, we will compute only the average of the 3 highest values
                values = sorted(nx.core_number(g).values(), reverse=True)
                core = sum(values[:3]) / 3
            else:
                cores = []
                for component in nx.connected_components(g):
                    subgraph = g.subgraph(component)
                    values = sorted(nx.core_number(subgraph).values(), reverse=True)
                    core = sum(values[:3]) / 3
                    cores.append(core)
                core = max(cores)
        except nx.NetworkXError:
            core = 0

        return informed_transactions / total_transactions, maximal_independent_set_length, core

    if granularity == 1:
        try:
            if nx.is_connected(g):
                # For eccentricity, we will compute only the average of the 3 highest values
                values = sorted(nx.eccentricity(g).values(), reverse=True)
                eccentricity = sum(values[:3]) / 3
            else:
                eccentricities = []
                for component in nx.connected_components(g):
                    subgraph = g.subgraph(component)
                    values = sorted(nx.eccentricity(subgraph).values(), reverse=True)
                    eccentricity = sum(values[:3]) / 3
                    eccentricities.append(eccentricity)
                eccentricity = max(eccentricities)
        except nx.NetworkXError:
            eccentricity = 0

        try:
            if nx.is_connected(g):
                radius = nx.radius(g)
            else:
                radius_list = []
                for component in nx.connected_components(g):
                    subgraph = g.subgraph(component)
                    radius = nx.radius(subgraph)
                    radius_list.append(radius)
                radius = max(radius_list)
        except nx.NetworkXError:
            radius = 0

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

        return informed_transactions / total_transactions, diameter, radius, eccentricity
