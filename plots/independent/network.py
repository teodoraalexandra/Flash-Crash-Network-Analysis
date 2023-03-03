import networkx as nx


def create_graph(prices):
    # Create an empty graph
    g = nx.DiGraph()

    # Specify a color map which maps a color to each node

    for price in prices:
        if price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Undervalued"):
            g.add_node(price.first_agent, color='red')
        elif price.first_agent.startswith("ZIT") or price.first_agent.startswith("Noise"):
            g.add_node(price.first_agent, color='green')

        if price.second_agent.startswith("Overvalued") or price.second_agent.startswith("Undervalued"):
            g.add_node(price.second_agent, color='red')
        elif price.second_agent.startswith("ZIT") or price.second_agent.startswith("Noise"):
            g.add_node(price.second_agent, color='green')

        g.add_edge(price.first_agent, price.second_agent)

    return g
