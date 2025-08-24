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
from scipy.spatial import ConvexHull

def draw_random_chosen_graph_communities(g, agent_type):
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

    plt.figure(figsize=(28, 26))
    plt.title(f"Random Network with {agent_type} Agents using Community Detection (Louvain Algorithm)", fontsize=40)
    plt.suptitle(f"Number of communities: {len(number_of_communities)}", fontsize=30)
    nx.draw(g, pos, node_color=color_map, node_size=[200 * g.degree(node) for node in g.nodes])
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=30, label='Informed agent'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=30, label='Market Maker'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=30, label='Uninformed agent'),
    ]
    plt.legend(handles=legend_elements, fontsize=40, loc='lower center')
    plt.axis("off")
    plt.savefig(f"results/community_{agent_type}_network.png")
    plt.close()

def compute_concentric_degree_layout(g, max_radius=10, num_rings=5):
    degrees = dict(g.degree())
    min_deg = min(degrees.values())
    max_deg = max(degrees.values())

    def degree_to_ring(degree):
        if max_deg == min_deg:
            return 0
        norm = (degree - min_deg) / (max_deg - min_deg)
        return int(norm * (num_rings - 1))

    ring_nodes = [[] for _ in range(num_rings)]
    for node, degree in degrees.items():
        ring = degree_to_ring(degree)
        ring_nodes[ring].append(node)

    pos = {}
    for ring_index, nodes_in_ring in enumerate(ring_nodes):
        radius = (ring_index + 1) * (max_radius / num_rings)
        for i, node in enumerate(nodes_in_ring):
            angle = 2 * np.pi * i / len(nodes_in_ring)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            pos[node] = (x, y)
    return pos

def draw_sun_layout_graph(g, agent_type):
    degrees = dict(g.degree())
    sorted_nodes = sorted(degrees.items(), key=lambda x: x[1])
    max_radius = 10

    pos = compute_concentric_degree_layout(g)

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

    plt.figure(figsize=(28, 26))
    nx.draw(g, pos, node_color=color_map, node_size=[50 * g.degree(node) for node in g.nodes])

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=30, label='Informed agent'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=30, label='Market Maker'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=30, label='Uninformed agent'),
    ]
    plt.legend(handles=legend_elements, fontsize=40, loc='lower center')

    plt.axis("off")
    plt.savefig(f"results/layout_{agent_type}_network.png")
    plt.close()

def draw_bipartite_graph(g, agent_type):
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

    degrees = [g.degree(n) for n in g.nodes()]
    degree_threshold = np.percentile(degrees, 95)

    pos = {}
    for node in g.nodes():
        if g.degree(node) > degree_threshold:
            x = random.uniform(-10, -2)
        else:
            x = random.uniform(2, 10)
        y = random.uniform(-5, 5)
        pos[node] = (x, y)

    plt.figure(figsize=(28, 26))
    nx.draw(g, pos, node_color=color_map, node_size=[50 * g.degree(node) for node in g.nodes])

    plt.axvline(x=0, color='orange', linestyle='-', linewidth=3)

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=30, label='Informed agent'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=30, label='Market Maker'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=30, label='Uninformed agent'),
    ]
    plt.legend(handles=legend_elements, fontsize=40, loc='lower center')

    plt.axis("off")
    plt.savefig(f"results/degree_{agent_type}_network.png")
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

    with pd.read_csv(file_path, chunksize=500, delimiter=";") as reader:
        for chunk in reader:
            price_array, noise_only, informed_length = read_prices_in_chunk(chunk)
            g = create_graph(price_array)
            if noise_only:
                random_noise_graphs.append(g)
            else:
                random_informed_graphs.append(g)

    random_chosen_noise = random.choice(random_noise_graphs)
    random_chosen_informed = random.choice(random_informed_graphs)

    draw_random_chosen_graph_communities(random_chosen_noise, "Uninformed and MM")
    draw_random_chosen_graph_communities(random_chosen_informed, "Informed")

    with pd.read_csv(file_path, chunksize=3000, delimiter=";") as reader:
        for chunk in reader:
            price_array, noise_only, informed_length = read_prices_in_chunk(chunk)
            g = create_graph(price_array)
            if noise_only:
                random_noise_graphs.append(g)
            else:
                random_informed_graphs.append(g)

    random_chosen_noise = random.choice(random_noise_graphs)
    random_chosen_informed = random.choice(random_informed_graphs)

    draw_sun_layout_graph(random_chosen_informed, "Informed")
    draw_bipartite_graph(random_chosen_informed, "Informed")
