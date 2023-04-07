import networkx as nx


def create_graph(prices):
    # Create an empty graph
    g = nx.Graph()

    for price in prices:
        g.add_node(price.first_agent)
        g.add_node(price.second_agent)
        g.add_edge(price.first_agent, price.second_agent)

    return g
