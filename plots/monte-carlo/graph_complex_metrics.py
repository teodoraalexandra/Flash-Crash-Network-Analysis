from graph_metrics import read_prices_in_chunk, plot_metrics
from plots.independent.computeComplexMetrics import compute_complex_metrics
import numpy as np
import pandas as pd
import multiprocessing
import sys


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
            PIN, independence, core = compute_complex_metrics(price_array, 0)

            PIN_results_big.append(PIN)
            independence_results.append(independence)
            core_results.append(core)

    # Stars on small granularity
    with pd.read_csv("plots/csvs/prices" + str(counter + 1) + ".csv",
                     chunksize=small_granularity, delimiter=";") as reader:
        for chunk in reader:
            price_array = read_prices_in_chunk(chunk)
            PIN, diameter, radius, eccentricity = compute_complex_metrics(price_array, 1)

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

    plot_metrics(x_axis_small, x_axis_PIN_small, y_axis_diameter, "PIN", "DIAMETER")
    plot_metrics(x_axis_small, x_axis_PIN_small, y_axis_radius, "PIN", "RADIUS")
    plot_metrics(x_axis_small, x_axis_PIN_small, y_axis_eccentricity, "PIN", "ECCENTRICITY")
    plot_metrics(x_axis_big, x_axis_PIN_big, y_axis_core, "PIN", "CORE NUMBER")
    plot_metrics(x_axis_big, x_axis_PIN_big, y_axis_independence, "PIN", "MAXIMAL INDEPENDENT SET")
