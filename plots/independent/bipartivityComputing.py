from plots.independent.network import *
from networkx.algorithms import bipartite


def compute_bipartivity(prices):
    G = create_graph(prices)

    return bipartite.spectral_bipartivity(G)


# index = 1
# result = process()
#
# for day, price_array in result.items():
#     bipartivity = compute_bipartivity(price_array)
#     print("Day: ", index, "Bipartivity: ", bipartivity)
#     index += 1
