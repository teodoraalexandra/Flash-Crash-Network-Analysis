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
        if price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Undervalued") \
                or price.second_agent.startswith("Overvalued") or price.second_agent.startswith("Undervalued"):
            informed_transactions += 1
        total_transactions += 1

        # Add the prices to y-axis -> Average of all prices from chunk
        average += price.price
        items += 1

    if granularity == 0:
        if bipartite.is_bipartite(g):
            isGraphBipartite = bipartite.average_clustering(g)
        else:
            isGraphBipartite = 2

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

        return informed_transactions / total_transactions, nx.density(g), \
            isGraphBipartite, average / items, maximal_independent_set_length, core

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

        return informed_transactions / total_transactions, \
            nx.degree_assortativity_coefficient(g), nx.number_connected_components(g), \
            diameter, radius, eccentricity

    if granularity == 2:
        num_stars = sum(1 for node in g if g.degree(node) == 1)
        return informed_transactions / total_transactions, bipartite.spectral_bipartivity(g), num_stars

# Defs
# Compute the assortativity of the graph
# This function calculates Pearson's correlation coefficient between
# the degrees of all pairs of connected nodes in the graph.
# The degree_assortativity_coefficient function returns a value between -1 and 1,
# where a value of -1 means that nodes tend to connect to nodes with a different degree,
# a value of 0 means that the degree of connected nodes is uncorrelated,
# and a value of 1 means that nodes tend to connect to nodes with the same degree.
