from plots.independent.processFile import Price
from plots.independent.computeMetrics import compute_metrics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import multiprocessing
import sys


def plot_metrics(X, Y1, Y2, metric1, metric2):
    COLOR_PIN = "#3399ff"
    COLOR_METRIC = "#ff6600"

    plt.close()
    fig, ax1 = plt.subplots(figsize=(8, 8))
    ax2 = ax1.twinx()
    ax1.plot(X, Y1, color=COLOR_PIN)
    ax2.plot(X, Y2, color=COLOR_METRIC)

    # Standard deviation and confidence interval
    standard_deviation_metric1 = np.std(Y1)
    standard_deviation_metric2 = np.std(Y2)
    average_metric1 = np.mean(Y1)
    average_metric2 = np.mean(Y2)
    lower_bound_1 = average_metric1 - 2 * standard_deviation_metric1
    upper_bound_1 = average_metric1 + 2 * standard_deviation_metric1
    lower_bound_2 = average_metric2 - 2 * standard_deviation_metric2
    upper_bound_2 = average_metric2 + 2 * standard_deviation_metric2

    # Correlation
    correlation = np.corrcoef(Y1, Y2)

    # Plot statistics
    number_of_rounded_decimals = 6
    subtitle1 = metric1 + " CI: [" + str(round(lower_bound_1, number_of_rounded_decimals)) + ", " + \
        str(round(upper_bound_1, number_of_rounded_decimals)) + "]"
    subtitle2 = metric2 + " CI: [" + str(round(lower_bound_2, number_of_rounded_decimals)) + ", " + \
        str(round(upper_bound_2, number_of_rounded_decimals)) + "]"

    ax1.set_xlabel("Correlation: " + str(correlation))

    ax1.set_ylabel(metric1, color=COLOR_PIN, fontsize=14)
    ax1.tick_params(axis="y", labelcolor=COLOR_PIN)

    ax2.set_ylabel(metric2, color=COLOR_METRIC, fontsize=14)
    ax2.tick_params(axis="y", labelcolor=COLOR_METRIC)

    fig.suptitle(metric1 + ' and ' + metric2, fontsize=20)
    fig.text(0.5, 0.93, subtitle1, ha='center', fontsize=14)
    fig.text(0.5, 0.90, subtitle2, ha='center', fontsize=14)
    fig.savefig("plot_" + metric1 + "_" + metric2 + ".png")


def create_price_object(row):
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

    return price_object


def read_prices_in_chunk(chunk):
    price_array = []
    for row in chunk.itertuples():
        price_object = create_price_object(row)

        # Add the price to the intermediate array
        price_array.append(price_object)
    return price_array


def task(counter, mean_PIN_list_super_small, mean_PIN_list_small, mean_PIN_list_big, mean_assortativity_list,
         mean_density_list, mean_average_clustering_list, mean_bipartivity_list, mean_connected_list,
         mean_stars_list, y_axis, list_lock):
    PIN_results_super_small = []
    PIN_results_small = []
    PIN_results_big = []
    assortativity_results = []
    density_results = []
    average_clustering_results = []
    bipartivity_results = []
    connected_results = []
    stars_results = []
    intermediate_y = []

    big_granularity = 3000
    small_granularity = 300
    super_small_granularity = 50

    # Density, Average clustering and Bipartivity on big granularity
    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=big_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            PIN, density, averageClustering, averagePrice = compute_metrics(price_array, 0)

            PIN_results_big.append(PIN)
            density_results.append(density)
            average_clustering_results.append(averageClustering)
            intermediate_y.append(averagePrice)

    # Assortativity, Connected components on small granularity
    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=small_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            PIN, assortativity, conn = compute_metrics(price_array, 1)

            PIN_results_small.append(PIN)
            assortativity_results.append(assortativity)
            connected_results.append(conn)

    # Stars on super-small granularity
    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=super_small_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            PIN, bipartivity, stars = compute_metrics(price_array, 2)

            PIN_results_super_small.append(PIN)
            bipartivity_results.append(bipartivity)
            stars_results.append(stars)

    with list_lock:
        y_axis.append(intermediate_y)
        mean_PIN_list_super_small.append(PIN_results_super_small)
        mean_PIN_list_small.append(PIN_results_small)
        mean_PIN_list_big.append(PIN_results_big)
        mean_assortativity_list.append(assortativity_results)
        mean_density_list.append(density_results)
        mean_average_clustering_list.append(average_clustering_results)
        mean_bipartivity_list.append(bipartivity_results)
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
    mean_density_results = multiprocessing.Manager().list()
    mean_average_clustering_results = multiprocessing.Manager().list()
    mean_bipartivity_results = multiprocessing.Manager().list()
    mean_connected_results = multiprocessing.Manager().list()
    mean_stars_results = multiprocessing.Manager().list()
    y_price_axis = multiprocessing.Manager().list()
    lock = multiprocessing.Lock()

    # Create processes for each simulation using a for loop
    processes = []
    for simulationIndex in range(int(sys.argv[1])):
        process = multiprocessing.Process(target=task, args=(simulationIndex, mean_PIN_results_super_small,
                                                             mean_PIN_results_small, mean_PIN_results_big,
                                                             mean_assortativity_results, mean_density_results,
                                                             mean_average_clustering_results, mean_bipartivity_results,
                                                             mean_connected_results, mean_stars_results,
                                                             y_price_axis, lock))
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

    # Mean Density
    mean_density_results = mean_with_padding(mean_density_results)

    # Mean Average Clustering
    mean_average_clustering_results = mean_with_padding(mean_average_clustering_results)

    # Mean Bipartivity
    mean_bipartivity_results = mean_with_padding(mean_bipartivity_results)

    # Mean Connected Components
    mean_connected_results = mean_with_padding(mean_connected_results)

    # Mean Stars
    mean_stars_results = mean_with_padding(mean_stars_results)

    # CORRELATION PLOTS
    x_axis_PIN_super_small = np.array(mean_PIN_results_super_small)
    x_axis_PIN_small = np.array(mean_PIN_results_small)
    x_axis_PIN_big = np.array(mean_PIN_results_big)
    y_axis_assortativity = np.array(mean_assortativity_results)
    y_axis_density = np.array(mean_density_results)
    y_axis_average_clustering = np.array(mean_average_clustering_results)
    y_axis_bipartivity = np.array(mean_bipartivity_results)
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

    plot_metrics(x_axis_small, x_axis_PIN_small, y_axis_assortativity, "PIN", "ASSORTATIVITY")
    plot_metrics(x_axis_big, x_axis_PIN_big, y_axis_density, "PIN", "DENSITY")
    plot_metrics(x_axis_big, x_axis_PIN_big, y_axis_average_clustering, "PIN", "AVERAGE CLUSTERING")
    plot_metrics(x_axis_super_small, x_axis_PIN_super_small, y_axis_bipartivity, "PIN", "BIPARTIVITY")
    plot_metrics(x_axis_small, x_axis_PIN_small, y_axis_connected, "PIN", "CONNECTED COMPONENTS")
    plot_metrics(x_axis_super_small, x_axis_PIN_super_small, y_axis_stars, "PIN", "NUMBER OF STARS")
