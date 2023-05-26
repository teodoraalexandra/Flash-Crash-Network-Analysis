import random

from graph_metrics import create_price_object
from plots.independent.network import create_graph
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import itertools
import pandas as pd
import multiprocessing
import sys


def read_prices_in_chunk(chunk):
    price_array = []
    noise_only = True
    informed_length = 0
    for row in chunk.itertuples():
        price_object = create_price_object(row)

        if price_object.first_agent.startswith('Overvalued') or price_object.second_agent.startswith('Overvalued'):
            noise_only = False
            informed_length += 1

        # Add the price to the intermediate array
        price_array.append(price_object)
    return price_array, noise_only, informed_length


def concatenate_lists(a):
    return list(itertools.chain.from_iterable(a))


def task(counter, mean_laplacian_noise_list, mean_laplacian_informed_list, list_lock):
    laplacian_noise = []
    laplacian_informed = []
    laplacian_granularity = 300000

    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=laplacian_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array, noise_only, informed_length = read_prices_in_chunk(chunk)
            if noise_only:
                g_noise = create_graph(price_array)
                laplacian_noise.append(list(nx.laplacian_spectrum(g_noise)))
            elif informed_length > 100:
                g_informed = create_graph(price_array)
                laplacian_informed.append(list(nx.laplacian_spectrum(g_informed)))

    # Noise will always be bigger because informed agents are here only 2 days
    # Equilibrate the lists: choose N random values from noise
    random_values_from_noise = random.sample(laplacian_noise, len(laplacian_informed))
    print("Number of graphs per population: ", len(laplacian_informed))
    with list_lock:
        mean_laplacian_noise_list.append(concatenate_lists(random_values_from_noise))
        mean_laplacian_informed_list.append(concatenate_lists(laplacian_informed))


if __name__ == '__main__':
    # Create a PIN list
    mean_laplacian_noise = multiprocessing.Manager().list()
    mean_laplacian_informed = multiprocessing.Manager().list()
    lock = multiprocessing.Lock()

    simulations = sys.argv[1]
    agents = sys.argv[2]
    percentage = sys.argv[3]

    # Create three processes for each task using a for loop
    processes = []
    for simulationIndex in range(int(simulations)):
        process = multiprocessing.Process(target=task, args=(simulationIndex, mean_laplacian_noise,
                                                             mean_laplacian_informed, lock))
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print('Monte Carlo done. Start generating plots!\n')
    fig, ax1 = plt.subplots(figsize=(8, 8))

    # Concatenate eigenvalues from N simulations
    mean_laplacian_noise = sorted(concatenate_lists(mean_laplacian_noise))
    mean_laplacian_informed = sorted(concatenate_lists(mean_laplacian_informed))

    # Covert to float
    values_float_noise = [float(x) for x in mean_laplacian_noise]
    values_float_informed = [float(x) for x in mean_laplacian_informed]

    # Plot the Laplacian spectrum of Noise
    sns.kdeplot(ax=ax1, data=values_float_noise, color='blue', fill=True, alpha=0.5, label='Noise')

    # Plot the Laplacian spectrum of Informed
    sns.kdeplot(ax=ax1, data=values_float_informed, color='red', fill=True, alpha=0.5, label='Informed')

    # Add title, labels, and legend to the plot
    fig.suptitle('Laplacian Spectrum')
    ax1.set_xlabel('Eigenvalue')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    fig.savefig("laplacian" + "_" + simulations + "_" + agents + "_" + percentage + ".png")
