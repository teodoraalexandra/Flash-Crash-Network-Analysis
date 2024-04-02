from laplacian_metrics import read_prices_in_chunk
from plots.independent.network import create_graph
import pandas as pd
import random
import networkx as nx
import community
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import sys


def draw_random_chosen_graph(g, agent_type):
    # Run the Louvain algorithm
    partition = community.best_partition(g)
    number_of_communities = nx.community.louvain_communities(g)

    # Draw the network with node colors based on community
    # Assign community information to nodes
    for node, community_id in partition.items():
        g.nodes[node]['community'] = community_id

    # # Draw the graph with communities colored
    pos = nx.kamada_kawai_layout(g)

    colors = [partition[node] for node in g.nodes]

    color_map = []
    for node in g:
        if node.startswith("Overvalued"):
            color_map.append('red')
        elif node.startswith("Noise"):
            color_map.append('green')
        else:
            color_map.append('blue')

    plt.figure(figsize=(28, 26))
    plt.title("Random Network with " + agent_type + " Agents using Community Detection (Louvain Algorithm)", fontsize=40)
    plt.suptitle("Number of communities: " + str(len(number_of_communities)), fontsize=30)
    nx.draw(g, pos, node_color=color_map, node_size=[200 * g.degree(node) for node in g.nodes])

    # Create a legend based on colors
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=30, label='Informed agent'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=30, label='Noise agent'),
    ]

    plt.legend(handles=legend_elements, fontsize=40, loc='lower center')

    plt.axis("off")
    plt.savefig("random_chosen_" + agent_type + "_network.png")
    plt.close()

    plt.figure(figsize=(28, 26))
    plt.title("Random Network with " + agent_type + " Agents using Community Detection (Louvain Algorithm)", fontsize=40)
    plt.suptitle("Number of communities: " + str(len(number_of_communities)), fontsize=30)

    nx.draw(g, pos, node_color=colors, cmap=plt.cm.Set1,
            node_size=[200 * g.degree(node) for node in g.nodes])

    plt.axis("off")
    plt.savefig("random_chosen_" + agent_type + "_communities.png")
    plt.close()


if __name__ == '__main__':
    plt.close()

    agents = sys.argv[2]
    percentage = sys.argv[3]

    big_granularity = int(sys.argv[4])
    small_granularity = int(sys.argv[5])

    random_noise_graphs = []
    random_informed_graphs = []

    with pd.read_csv("plots/csvs/prices1" + agents + percentage + ".csv",
                     chunksize=17, delimiter=";") as reader:
        for chunk in reader:
            price_array, noise_only, informed_length = read_prices_in_chunk(chunk)
            if noise_only:
                g_noise = create_graph(price_array)
                random_noise_graphs.append(g_noise)
            else:
                g_informed = create_graph(price_array)
                random_informed_graphs.append(g_informed)

    random_chosen_noise = random.choice(random_noise_graphs)
    # gml_graph(random_chosen_noise, "noise_medium_granularity")
    random_chosen_informed = random.choice(random_informed_graphs)
    # gml_graph(random_chosen_informed, "informed_medium_granularity")

    draw_random_chosen_graph(random_chosen_noise, "Noise")
    draw_random_chosen_graph(random_chosen_informed, "Informed")
