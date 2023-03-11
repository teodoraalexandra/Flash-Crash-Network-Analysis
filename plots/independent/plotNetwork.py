import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


def plot_network():
    # Read the CSV file
    df = pd.read_csv("plots/csvs/prices.csv", sep=';')

    # Create an empty directed graph
    g = nx.DiGraph()

    # Iterate through the rows of the dataframe
    for _, row in df.iterrows():
        # Get the values from the row
        first_agent = row["AgTrigger"]
        second_agent = row["ag2"]

        if (first_agent.startswith("Overvalued") or first_agent.startswith("Noise")) \
                and (first_agent.startswith("Overvalued") or first_agent.startswith("Noise")):
            g.add_node(first_agent)
            g.add_node(second_agent)
            g.add_edge(first_agent, second_agent)

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
    plt.savefig("random_chosen_network.png")
