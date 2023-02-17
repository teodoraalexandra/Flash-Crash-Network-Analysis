from laplacian_metrics import read_prices_in_chunk
from plots.independent.network import create_graph, gml_graph
import pandas as pd
import random


if __name__ == '__main__':
    big_granularity = 3000
    medium_granularity = 1000
    small_granularity = 300
    super_small_granularity = 50

    random_noise_graphs = []
    random_informed_graphs = []

    with pd.read_csv("plots/csvs/prices1.csv", chunksize=big_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array, noise_only, informed_length = read_prices_in_chunk(chunk)
            if noise_only:
                g_noise = create_graph(price_array)
                random_noise_graphs.append(g_noise)
            else:
                g_informed = create_graph(price_array)
                random_informed_graphs.append(g_informed)

    random_chosen_noise = random.choice(random_noise_graphs)
    gml_graph(random_chosen_noise, "noise_medium_granularity")
    random_chosen_informed = random.choice(random_informed_graphs)
    gml_graph(random_chosen_informed, "informed_medium_granularity")
