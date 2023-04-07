from plots.independent.processFile import Price
from plots.independent.computeMetrics import compute_metrics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import multiprocessing
import sys


def read_prices_in_chunk(chunk):
    price_array = []
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

        # Add the price to the intermediate array
        price_array.append(price_object)
    return price_array


def task(counter, mean_PIN_list_super_small, mean_PIN_list_small, mean_PIN_list_big, mean_assortativity_list,
         mean_bipartivity_list, mean_spectral_list, mean_connected_list, mean_stars_list, y_axis, list_lock):
    PIN_results_super_small = []
    PIN_results_small = []
    PIN_results_big = []
    assortativity_results = []
    bipartivity_results = []
    spectral_results = []
    connected_results = []
    stars_results = []
    intermediate_y = []

    big_granularity = 3000
    small_granularity = 300
    super_small_granularity = 50

    # Bipartivity, Spectral on big granularity
    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=big_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            PIN, assortativity, bipartivity, spectralBipartivity, conn, averagePrice, stars \
                = compute_metrics(price_array)

            PIN_results_big.append(PIN)
            bipartivity_results.append(bipartivity)
            spectral_results.append(spectralBipartivity)
            intermediate_y.append(averagePrice)

    # Assortativity, Connected components on small granularity
    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=small_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            PIN, assortativity, bipartivity, spectralBipartivity, conn, averagePrice, stars \
                = compute_metrics(price_array)

            PIN_results_small.append(PIN)
            assortativity_results.append(assortativity)
            connected_results.append(conn)

    # Stars on super-small granularity
    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=super_small_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            PIN, assortativity, bipartivity, spectralBipartivity, conn, averagePrice, stars \
                = compute_metrics(price_array)

            PIN_results_super_small.append(PIN)
            stars_results.append(stars)

    with list_lock:
        y_axis.append(intermediate_y)
        mean_PIN_list_super_small.append(PIN_results_super_small)
        mean_PIN_list_small.append(PIN_results_small)
        mean_PIN_list_big.append(PIN_results_big)
        mean_assortativity_list.append(assortativity_results)
        mean_bipartivity_list.append(bipartivity_results)
        mean_spectral_list.append(spectral_results)
        mean_connected_list.append(connected_results)
        mean_stars_list.append(stars_results)


def mean_with_padding(a):
    max_len = max([len(row) for row in a])
    mask = np.array([row + [np.nan] * (max_len - len(row)) for row in a])
    return np.nanmean(mask, axis=0)


if __name__ == '__main__':
    # Create a PIN list
    mean_PIN_results_super_small = multiprocessing.Manager().list()
    mean_PIN_results_small = multiprocessing.Manager().list()
    mean_PIN_results_big = multiprocessing.Manager().list()
    mean_assortativity_results = multiprocessing.Manager().list()
    mean_bipartivity_results = multiprocessing.Manager().list()
    mean_spectral_results = multiprocessing.Manager().list()
    mean_connected_results = multiprocessing.Manager().list()
    mean_stars_results = multiprocessing.Manager().list()
    y_price_axis = multiprocessing.Manager().list()
    lock = multiprocessing.Lock()

    # Create three processes for each task using a for loop
    processes = []
    for simulationIndex in range(int(sys.argv[1])):
        process = multiprocessing.Process(target=task, args=(simulationIndex, mean_PIN_results_super_small,
                                                             mean_PIN_results_small, mean_PIN_results_big,
                                                             mean_assortativity_results, mean_bipartivity_results,
                                                             mean_spectral_results, mean_connected_results,
                                                             mean_stars_results, y_price_axis, lock))
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print('Monte Carlo done. Start generating plots!\n')
    x_axis = []
    plt.figure().set_figheight(5)
    plt.figure().set_figwidth(20)
    for simulationIndex in range(int(sys.argv[1])):
        for priceIndex in range(len(y_price_axis[simulationIndex])):
            x_axis.append(priceIndex)
        plt.plot(x_axis, y_price_axis[simulationIndex], label="Simulation" + str(simulationIndex + 1))
        x_axis = []
    plt.title('Price evolution')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.savefig("price_evolution.png")

    # Mean PIN (super-small)
    mean_PIN_results_super_small = mean_with_padding(mean_PIN_results_super_small)

    # Mean PIN (small)
    mean_PIN_results_small = mean_with_padding(mean_PIN_results_small)

    # Mean PIN (big)
    mean_PIN_results_big = mean_with_padding(mean_PIN_results_big)

    # Mean Assortativity
    mean_assortativity_results = mean_with_padding(mean_assortativity_results)

    # Mean Bipartivity
    mean_bipartivity_results = mean_with_padding(mean_bipartivity_results)

    # Mean Density
    mean_spectral_results = mean_with_padding(mean_spectral_results)

    # Mean Connected Components
    mean_connected_results = mean_with_padding(mean_connected_results)

    # Mean Stars
    mean_stars_results = mean_with_padding(mean_stars_results)

    # CORRELATION PLOTS
    x_axis_PIN_super_small = np.array(mean_PIN_results_super_small)
    x_axis_PIN_small = np.array(mean_PIN_results_small)
    x_axis_PIN_big = np.array(mean_PIN_results_big)
    y_axis_assortativity = np.array(mean_assortativity_results)
    y_axis_bipartivity = np.array(mean_bipartivity_results)
    y_axis_spectral = np.array(mean_spectral_results)
    y_axis_connected = np.array(mean_connected_results)
    y_axis_stars = np.array(mean_stars_results)

    x_axis_super_small = []
    for index in range(len(x_axis_PIN_super_small)):
        x_axis_super_small.append(index)

    x_axis_small = []
    for index in range(len(x_axis_PIN_small)):
        x_axis_small.append(index)

    x_axis_big = []
    for index in range(len(x_axis_PIN_big)):
        x_axis_big.append(index)

    # Plot first
    plt.close()
    plt.title('Correlation between PIN and assortativity')
    plt.plot(x_axis_small, x_axis_PIN_small, label="PIN")
    plt.plot(x_axis_small, y_axis_assortativity, label="ASSORTATIVITY")
    plt.legend()
    plt.xlabel('PIN')
    plt.ylabel('Assortativity')
    plt.savefig("plot_PIN_assortativity.png")

    # Plot second
    plt.close()
    plt.title('Correlation between PIN and density')
    plt.plot(x_axis_big, x_axis_PIN_big, label="PIN")
    plt.plot(x_axis_big, y_axis_bipartivity, label="DENSITY")
    plt.legend()
    plt.xlabel('PIN')
    plt.ylabel('Density')
    plt.savefig("plot_PIN_density.png")

    # Plot third
    plt.close()
    plt.title('Correlation between PIN and spectral bipartivity')
    plt.plot(x_axis_big, x_axis_PIN_big, label="PIN")
    plt.plot(x_axis_big, y_axis_spectral, label="BIPARTIVITY")
    plt.legend()
    plt.xlabel('PIN')
    plt.ylabel('Bipartivity')
    plt.savefig("plot_PIN_spectral_bipartivity.png")

    # Plot fourth
    plt.close()
    plt.title('Correlation between PIN and connected')
    plt.plot(x_axis_small, x_axis_PIN_small, label="PIN")
    plt.plot(x_axis_small, y_axis_connected, label="CONNECTED")
    plt.legend()
    plt.xlabel('PIN')
    plt.ylabel('Connected')
    plt.savefig("plot_PIN_connected.png")

    # Plot fifth
    plt.close()
    plt.title('Correlation between PIN and stars')
    plt.plot(x_axis_super_small, x_axis_PIN_super_small, label="PIN")
    plt.plot(x_axis_super_small, y_axis_stars, label="STARS")
    plt.legend()
    plt.xlabel('PIN')
    plt.ylabel('Stars')
    plt.savefig("plot_PIN_stars.png")

    plt.close()
