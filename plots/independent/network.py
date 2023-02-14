from processFile import *
import networkx as nx
import matplotlib.pyplot as plt


def create_graph(prices):
    # Create an empty graph
    G = nx.DiGraph()

    # Specify a color map which maps a color to each node

    for price in prices:
        if price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Undervalued"):
            G.add_node(price.first_agent, color='red')
        elif price.first_agent.startswith("ZIT") or price.first_agent.startswith("Noise"):
            G.add_node(price.first_agent, color='green')

        if price.second_agent.startswith("Overvalued") or price.second_agent.startswith("Undervalued"):
            G.add_node(price.second_agent, color='red')
        elif price.second_agent.startswith("ZIT") or price.second_agent.startswith("Noise"):
            G.add_node(price.second_agent, color='green')

        G.add_edge(price.first_agent, price.second_agent)

    return G


index = 1
result = process()

# Informed = BLUE
# Uninformed = GREEN
for day, price_array in result.items():
    graph = create_graph(price_array)
    colors = [node[1]['color'] for node in graph.nodes(data=True)]

    nx.draw(graph, node_color=colors, with_labels=True)
    plt.title("Day " + str(index))
    plt.show()

    index += 1
