import networkx as nx


def create_graph(prices):
    # Create an empty graph
    g = nx.Graph()

    # Specify a color map which maps a color to each node

    for price in prices:
        # if (price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Noise")) \
        #         and (price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Noise")):
        #     g.add_node(price.first_agent)
        #     g.add_node(price.second_agent)
        #     g.add_edge(price.first_agent, price.second_agent)
        if price.first_agent.startswith("Overvalued"):
            g.add_node(price.first_agent, bipartite=0)
        if price.second_agent.startswith("Overvalued"):
            g.add_node(price.second_agent, bipartite=0)
        if price.first_agent.startswith("Noise"):
            g.add_node(price.first_agent, bipartite=1)
        if price.second_agent.startswith("Noise"):
            g.add_node(price.second_agent, bipartite=1)
        g.add_edge(price.first_agent, price.second_agent)

    return g
