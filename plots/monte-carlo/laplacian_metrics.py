import random

from plots.independent.processFile import Price
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
        # Create price object
        price_object = Price()

        # Append the properties
        price_object.price = row[row._fields.index("price")]
        price_object.quantity = row[row._fields.index("quty")]
        price_object.direction = row[row._fields.index("dirTrigger")]
        price_object.first_agent = row[row._fields.index("AgTrigger")]
        price_object.second_agent = row[row._fields.index("ag2")]
        price_object.best_ask = row[row._fields.index("bestask")]
        price_object.best_bid = row[row._fields.index("bestbid")]

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

    # Create three processes for each task using a for loop
    processes = []
    for simulationIndex in range(int(sys.argv[1])):
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
    with open(r'noise.txt', 'w') as fp:
        for item in values_float_noise:
            # write each item on a new line
            fp.write("%s\n" % item)
    # ax1.hist(values_float_noise, alpha=0.5, color='blue', label='Noise', bins=10)
    sns.kdeplot(ax=ax1, data=values_float_noise, color='blue', fill=True, alpha=0.5, label='Noise')

    # Plot the Laplacian spectrum of Informed
    with open(r'informed.txt', 'w') as fp:
        for item in values_float_informed:
            # write each item on a new line
            fp.write("%s\n" % item)
    # ax1.hist(values_float_informed, alpha=0.5, color='red', label='Informed', bins=10)
    sns.kdeplot(ax=ax1, data=values_float_informed, color='red', fill=True, alpha=0.5, label='Informed')

    # Add title, labels, and legend to the plot
    fig.suptitle('Laplacian Spectrum')
    ax1.set_xlabel('Eigenvalue')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    fig.savefig("laplacian.png")
