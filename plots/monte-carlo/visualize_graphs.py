from laplacian_metrics import read_prices_in_chunk
from plots.independent.network import create_graph
import pandas as pd
import random
import networkx as nx
import community
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import sys
import numpy as np
import os
import dwave_networkx as dnx
import dimod
from networkx.algorithms import bipartite
from scipy.spatial import ConvexHull

def draw_bipartite_graph(g, agent_type, frequency):
    if nx.is_bipartite(g):
        largest_cc = max(nx.connected_components(g))

        subgraph = g.subgraph(largest_cc)
        U, V = nx.bipartite.sets(subgraph)

        # Visualize the graph
        pos = nx.bipartite_layout(g, nodes=U)

        nodelist = list(subgraph.nodes())
        color_map = []
        for node in nodelist:
            if node.startswith("Overvalued"):
                color_map.append('red')
            elif node.startswith("Noise"):
                color_map.append('green')
            elif node.startswith("MM"):
                color_map.append('blue')
            else:
                color_map.append('orange')

        plt.figure(figsize=(28, 35))
        plt.title(f"Random Network with {agent_type} Agents using Bipartite Layout ({frequency} Frequency)", fontsize=40)

        nx.draw(subgraph, pos=pos, node_color=color_map)
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=30, label='Informed agent'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=30, label='Market Maker'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=30, label='Uninformed agent'),
        ]
        plt.legend(handles=legend_elements, fontsize=40, loc='lower center')

        plt.axis("off")
        plt.savefig(f"results/bipartivity_{agent_type}_{frequency}.png")
        plt.close()
    else:
        print("Graph " + agent_type + " " + frequency + " is not bipartite")

def draw_random_chosen_graph_communities(g, agent_type, frequency):
    partition = community.best_partition(g)
    number_of_communities = nx.community.louvain_communities(g)

    for node, community_id in partition.items():
        g.nodes[node]['community'] = community_id

    pos = nx.kamada_kawai_layout(g)

    color_map = []
    for node in g:
        if node.startswith("Overvalued"):
            color_map.append('red')
        elif node.startswith("Noise"):
            color_map.append('green')
        elif node.startswith("MM"):
            color_map.append('blue')
        else:
            color_map.append('orange')

    plt.figure(figsize=(35, 26))
    plt.title(f"Random Network with {agent_type} Agents using Community Detection (Louvain Algorithm) ({frequency} Frequency)", fontsize=40)
    plt.suptitle(f"Number of communities: {len(number_of_communities)}", fontsize=30)
    nx.draw(g, pos, node_color=color_map, node_size=[200 * g.degree(node) for node in g.nodes])
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=30, label='Informed agent'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=30, label='Market Maker'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=30, label='Uninformed agent'),
    ]
    plt.legend(handles=legend_elements, fontsize=40, loc='lower center')
    plt.axis("off")
    plt.savefig(f"results/community_{agent_type}_{frequency}.png")
    plt.close()

# --- MAIN SCRIPT ---
if __name__ == '__main__':
    plt.close()

    agents = sys.argv[2]
    percentage = sys.argv[3]

    big_granularity = int(sys.argv[4])
    small_granularity = int(sys.argv[5])

    random_noise_graphs = []
    random_informed_graphs = []

    file_path = f"plots/csvs/prices1{agents}{percentage}.csv"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with pd.read_csv(file_path, chunksize=small_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array, noise_only, informed_length = read_prices_in_chunk(chunk)
            g = create_graph(price_array)
            if noise_only:
                random_noise_graphs.append(g)
            else:
                random_informed_graphs.append(g)

    random_chosen_noise = random.choice(random_noise_graphs)
    random_chosen_informed = random.choice(random_informed_graphs)

    draw_random_chosen_graph_communities(random_chosen_noise, "Uninformed and MM", "High")
    draw_random_chosen_graph_communities(random_chosen_informed, "Informed", "High")
    draw_bipartite_graph(random_chosen_noise, "Uninformed and MM", "High")
    draw_bipartite_graph(random_chosen_informed, "Informed", "High")

    random_noise_graphs = []
    random_informed_graphs = []

    with pd.read_csv(file_path, chunksize=big_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array, noise_only, informed_length = read_prices_in_chunk(chunk)
            g = create_graph(price_array)
            if noise_only:
                random_noise_graphs.append(g)
            else:
                random_informed_graphs.append(g)

    random_chosen_noise = random.choice(random_noise_graphs)
    random_chosen_informed = random.choice(random_informed_graphs)

    draw_random_chosen_graph_communities(random_chosen_noise, "Uninformed and MM", "Low")
    draw_random_chosen_graph_communities(random_chosen_informed, "Informed", "Low")
    draw_bipartite_graph(random_chosen_noise, "Uninformed and MM", "Low")
    draw_bipartite_graph(random_chosen_informed, "Informed", "Low")
