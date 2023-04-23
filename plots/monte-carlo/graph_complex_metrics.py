from plots.independent.processFile import Price
from plots.independent.computeComplexMetrics import compute_complex_metrics
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


def task(counter, mean_PIN_list_small, mean_PIN_list_big, mean_diameter_list, mean_radius_list,
         mean_eccentricity_list, mean_core_list, mean_independence_list, list_lock):
    PIN_results_small = []
    PIN_results_big = []
    diameter_results = []
    radius_results = []
    eccentricity_results = []
    core_results = []
    independence_results = []

    big_granularity = 3000
    small_granularity = 300

    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=big_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            PIN, diameter, radius, eccentricity, core, independence = compute_complex_metrics(price_array)

            PIN_results_big.append(PIN)
            independence_results.append(independence)
            core_results.append(core)

    # Stars on small granularity
    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=small_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            PIN, diameter, radius, eccentricity, core, independence = compute_complex_metrics(price_array)

            PIN_results_small.append(PIN)
            diameter_results.append(diameter)
            radius_results.append(radius)
            eccentricity_results.append(eccentricity)

    with list_lock:
        mean_PIN_list_small.append(PIN_results_small)
        mean_PIN_list_big.append(PIN_results_big)
        mean_diameter_list.append(diameter_results)
        mean_radius_list.append(radius_results)
        mean_eccentricity_list.append(eccentricity_results)
        mean_core_list.append(core_results)
        mean_independence_list.append(independence_results)


def mean_with_padding(a):
    max_len = max([len(row) for row in a])
    mask = np.array([row + [np.nan] * (max_len - len(row)) for row in a])
    return np.nanmean(mask, axis=0)


if __name__ == '__main__':
    # Create a PIN list
    mean_PIN_results_small = multiprocessing.Manager().list()
    mean_PIN_results_big = multiprocessing.Manager().list()
    mean_diameter_results = multiprocessing.Manager().list()
    mean_radius_results = multiprocessing.Manager().list()
    mean_eccentricity_results = multiprocessing.Manager().list()
    mean_core_results = multiprocessing.Manager().list()
    mean_independence_results = multiprocessing.Manager().list()
    lock = multiprocessing.Lock()

    # Create three processes for each task using a for loop
    processes = []
    for simulationIndex in range(int(sys.argv[1])):
        process = multiprocessing.Process(target=task, args=(simulationIndex, mean_PIN_results_small,
                                                             mean_PIN_results_big, mean_diameter_results,
                                                             mean_radius_results, mean_eccentricity_results,
                                                             mean_core_results, mean_independence_results, lock))
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print('Monte Carlo done. Start generating plots!\n')
    # Mean PIN (small)
    mean_PIN_results_small = mean_with_padding(mean_PIN_results_small)

    # Mean PIN (big)
    mean_PIN_results_big = mean_with_padding(mean_PIN_results_big)

    # Mean Diameter
    mean_diameter_results = mean_with_padding(mean_diameter_results)

    # Mean Radius
    mean_radius_results = mean_with_padding(mean_radius_results)

    # Mean Eccentricity
    mean_eccentricity_results = mean_with_padding(mean_eccentricity_results)

    # Mean Core
    mean_core_results = mean_with_padding(mean_core_results)

    # Mean Independence results
    mean_independence_results = mean_with_padding(mean_independence_results)

    # CORRELATION PLOTS
    x_axis_PIN_small = np.array(mean_PIN_results_small)
    x_axis_PIN_big = np.array(mean_PIN_results_big)
    y_axis_diameter = np.array(mean_diameter_results)
    y_axis_radius = np.array(mean_radius_results)
    y_axis_eccentricity = np.array(mean_eccentricity_results)
    y_axis_core = np.array(mean_core_results)
    y_axis_independence = np.array(mean_independence_results)

    x_axis_small = []
    for index in range(len(x_axis_PIN_small)):
        x_axis_small.append(index)

    x_axis_big = []
    for index in range(len(x_axis_PIN_big)):
        x_axis_big.append(index)

    COLOR_PIN = "#69b3a2"
    COLOR_METRIC = "#3399e6"

    # Plot first
    plt.close()
    fig, ax1 = plt.subplots(figsize=(8, 8))
    ax2 = ax1.twinx()
    ax1.plot(x_axis_small, x_axis_PIN_small, color=COLOR_PIN)
    ax2.plot(x_axis_small, y_axis_diameter, color=COLOR_METRIC)
    ax1.set_xlabel("Small granularity")

    ax1.set_ylabel("PIN", color=COLOR_PIN, fontsize=14)
    ax1.tick_params(axis="y", labelcolor=COLOR_PIN)

    ax2.set_ylabel("DIAMETER", color=COLOR_METRIC, fontsize=14)
    ax2.tick_params(axis="y", labelcolor=COLOR_METRIC)

    fig.suptitle('Correlation between PIN and diameter', fontsize=20)
    fig.savefig("plot_PIN_diameter.png")
    correlation1 = np.corrcoef(x_axis_PIN_small, y_axis_diameter)
    print("\nCorrelation between PIN and diameter\n")
    print(correlation1)

    # Plot second
    plt.close()
    fig, ax1 = plt.subplots(figsize=(8, 8))
    ax2 = ax1.twinx()
    ax1.plot(x_axis_small, x_axis_PIN_small, color=COLOR_PIN)
    ax2.plot(x_axis_small, y_axis_radius, color=COLOR_METRIC)
    ax1.set_xlabel("Small granularity")

    ax1.set_ylabel("PIN", color=COLOR_PIN, fontsize=14)
    ax1.tick_params(axis="y", labelcolor=COLOR_PIN)

    ax2.set_ylabel("RADIUS", color=COLOR_METRIC, fontsize=14)
    ax2.tick_params(axis="y", labelcolor=COLOR_METRIC)

    fig.suptitle('Correlation between PIN and radius', fontsize=20)
    fig.savefig("plot_PIN_radius.png")
    correlation2 = np.corrcoef(x_axis_PIN_small, y_axis_radius)
    print("\nCorrelation between PIN and radius\n")
    print(correlation2)

    # Plot third
    plt.close()
    fig, ax1 = plt.subplots(figsize=(8, 8))
    ax2 = ax1.twinx()
    ax1.plot(x_axis_small, x_axis_PIN_small, color=COLOR_PIN)
    ax2.plot(x_axis_small, y_axis_eccentricity, color=COLOR_METRIC)
    ax1.set_xlabel("Small granularity")

    ax1.set_ylabel("PIN", color=COLOR_PIN, fontsize=14)
    ax1.tick_params(axis="y", labelcolor=COLOR_PIN)

    ax2.set_ylabel("ECCENTRICITY", color=COLOR_METRIC, fontsize=14)
    ax2.tick_params(axis="y", labelcolor=COLOR_METRIC)

    fig.suptitle('Correlation between PIN and eccentricity', fontsize=20)
    fig.savefig("plot_PIN_eccentricity.png")
    correlation3 = np.corrcoef(x_axis_PIN_small, y_axis_eccentricity)
    print("\nCorrelation between PIN and eccentricity\n")
    print(correlation3)

    # Plot fourth
    plt.close()
    fig, ax1 = plt.subplots(figsize=(8, 8))
    ax2 = ax1.twinx()
    ax1.plot(x_axis_big, x_axis_PIN_big, color=COLOR_PIN)
    ax2.plot(x_axis_big, y_axis_core, color=COLOR_METRIC)
    ax1.set_xlabel("Big granularity")

    ax1.set_ylabel("PIN", color=COLOR_PIN, fontsize=14)
    ax1.tick_params(axis="y", labelcolor=COLOR_PIN)

    ax2.set_ylabel("CORE", color=COLOR_METRIC, fontsize=14)
    ax2.tick_params(axis="y", labelcolor=COLOR_METRIC)

    fig.suptitle('Correlation between PIN and core', fontsize=20)
    fig.savefig("plot_PIN_core.png")
    correlation4 = np.corrcoef(x_axis_PIN_big, y_axis_core)
    print("\nCorrelation between PIN and core\n")
    print(correlation4)

    # Plot fifth
    plt.close()
    fig, ax1 = plt.subplots(figsize=(8, 8))
    ax2 = ax1.twinx()
    ax1.plot(x_axis_big, x_axis_PIN_big, color=COLOR_PIN)
    ax2.plot(x_axis_big, y_axis_independence, color=COLOR_METRIC)
    ax1.set_xlabel("Big granularity")

    ax1.set_ylabel("PIN", color=COLOR_PIN, fontsize=14)
    ax1.tick_params(axis="y", labelcolor=COLOR_PIN)

    ax2.set_ylabel("INDEPENDENCE", color=COLOR_METRIC, fontsize=14)
    ax2.tick_params(axis="y", labelcolor=COLOR_METRIC)

    fig.suptitle('Correlation between PIN and independence', fontsize=20)
    fig.savefig("plot_PIN_independence.png")
    correlation5 = np.corrcoef(x_axis_PIN_big, y_axis_independence)
    print("\nCorrelation between PIN and independence\n")
    print(correlation5)
