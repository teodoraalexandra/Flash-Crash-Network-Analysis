import networkx as nx
import matplotlib.pyplot as plt


def create_graph(prices):
    # Create an empty graph
    g = nx.Graph()

    for price in prices:
        g.add_node(price.first_agent)
        g.add_node(price.second_agent)
        g.add_edge(price.first_agent, price.second_agent)

    return g


def print_graph(g, fileName):
    color_map = []
    for node in g:
        if node.startswith("Overvalued"):
            color_map.append('red')
        elif node.startswith("Noise"):
            color_map.append('green')
        else:
            color_map.append('blue')

    nx.draw(g, node_color=color_map, with_labels=True)

    # Show the plot
    plt.savefig(fileName + ".png")


def gml_graph(g, fileName):
    color_map = []
    for node in g:
        if node.startswith("Overvalued"):
            color_map.append('red')
        elif node.startswith("Noise"):
            color_map.append('green')
        else:
            color_map.append('blue')

    nx.write_gml(g, fileName + ".gml")
