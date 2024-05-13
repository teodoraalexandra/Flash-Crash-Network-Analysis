from plots.independent.processFile import Price
from plots.independent.computeMetrics import compute_metrics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import multiprocessing
import sys


def plot_metrics(X, Y1, Y2, Y3, metric1, metric2, metric3):
    # Y1 = VPIN
    # Y2 = Metric values
    # Y3 = PRICE

    # metric1 = VPIN
    # metric2 = Metric
    # metric3 = PRICE

    COLOR_VPIN = "#3399ff"
    COLOR_METRIC = "#D2042D"
    COLOR_PRICE = "#696969"

    # Y3 Should be normalized first
    x = np.array(Y3)
    # Normalize all values to be between 0 and 1
    x_norm = (x - np.min(x)) / (np.max(x) - np.min(x))

    plt.close()
    fig, ax1 = plt.subplots(figsize=(12, 8))
    ax2 = ax1.twinx()

    l1, = ax2.plot(X, Y1, color=COLOR_VPIN)
    l2, = ax1.plot(X, Y2, color=COLOR_METRIC)
    l3, = ax2.plot(X, x_norm, color=COLOR_PRICE)

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
    subtitle3 = round(correlation[1][0], 4)

    fig.text(0.2, 0.93, "Correlation: " + str(subtitle3), ha='center', fontsize=18)

    ax1.set_xlabel(subtitle1 + " - " + subtitle2)
    ax1.set_xticks([])

    ax2.set_ylabel(metric1, color=COLOR_VPIN, fontsize=14)
    ax2.tick_params(axis="y", labelcolor=COLOR_VPIN)

    ax1.set_ylabel(metric2, color=COLOR_METRIC, fontsize=14)
    ax1.tick_params(axis="y", labelcolor=COLOR_METRIC)

    simulations = sys.argv[1]
    agents = sys.argv[2]
    percentage = sys.argv[3]

    fig.legend((l1, l2, l3), (metric1, metric2, metric3), fontsize="medium", loc='upper left')

    # Adjust layout to make room for the legend
    plt.subplots_adjust(left=-0.5)

    plt.savefig("results/plot_" + metric1 + "_" + metric2 + "_" + simulations + "_" + agents + "_" + percentage + ".png",
                bbox_inches='tight')


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


def task(counter, mean_VPIN_list_very_small, mean_VPIN_list_small, mean_VPIN_list_big,
         mean_PRICE_list_very_small, mean_PRICE_list_small, mean_PRICE_list_big,
         mean_assortativity_list, mean_bipartivity_list, mean_average_clustering_list,
         mean_connected_list, mean_stars_list, mean_diameter_list,
         mean_independence_list, mean_closeness_list, mean_betweenness_list,
         y_axis, informed, uninformed, marketMaker, list_lock, PRICE_ONLY):
    VPIN_results_very_small = []
    VPIN_results_small = []
    VPIN_results_big = []

    PRICE_results_very_small = []
    PRICE_results_small = []
    PRICE_results_big = []

    assortativity_results = []
    bipartivity_results = []
    average_clustering_results = []
    connected_results = []
    stars_results = []
    diameter_results = []
    independence_results = []
    closeness_results = []
    betweenness_results = []

    intermediate_y = []
    intermediate_informed = 0
    intermediate_uninformed = 0
    intermediate_market_maker = 0

    agents = sys.argv[2]
    percentage = sys.argv[3]

    big_granularity = int(sys.argv[4])
    small_granularity = int(sys.argv[5])
    very_small_granularity = int(sys.argv[6])

    if not PRICE_ONLY:
        with pd.read_csv("plots/csvs/prices" + str(counter + 1) + agents + percentage + ".csv",
                         chunksize=big_granularity, delimiter=";") as reader:
            for chunk in reader:
                price_array = read_prices_in_chunk(chunk)
                if len(price_array) == big_granularity:
                    VPIN, PRICE, diameter, stars = compute_metrics(price_array, 0)

                    VPIN_results_big.append(VPIN)
                    PRICE_results_big.append(PRICE)
                    diameter_results.append(diameter)
                    stars_results.append(stars)

        with pd.read_csv("plots/csvs/prices" + str(counter + 1) + agents + percentage + ".csv",
                         chunksize=small_granularity, delimiter=";") as reader:
            for chunk in reader:
                price_array = read_prices_in_chunk(chunk)
                if len(price_array) == small_granularity:
                    VPIN, PRICE, independence, assortativity, conn, bipartivity = \
                        compute_metrics(price_array, 1)

                    VPIN_results_small.append(VPIN)
                    PRICE_results_small.append(PRICE)
                    independence_results.append(independence)
                    assortativity_results.append(assortativity)
                    connected_results.append(conn)
                    bipartivity_results.append(bipartivity)

        with pd.read_csv("plots/csvs/prices" + str(counter + 1) + agents + percentage + ".csv",
                         chunksize=very_small_granularity, delimiter=";") as reader:
            for chunk in reader:
                price_array = read_prices_in_chunk(chunk)
                if len(price_array) == very_small_granularity:
                    VPIN, PRICE, closeness, betweenness, averageClustering = compute_metrics(price_array, 2)

                    VPIN_results_very_small.append(VPIN)
                    PRICE_results_very_small.append(PRICE)
                    closeness_results.append(closeness)
                    betweenness_results.append(betweenness)
                    average_clustering_results.append(averageClustering)

    if PRICE_ONLY:
        with pd.read_csv("plots/csvs/prices" + str(counter + 1) + agents + percentage + ".csv",
                         chunksize=small_granularity * 2, delimiter=";") as reader:
            for chunk in reader:
                price_array = read_prices_in_chunk(chunk)
                if len(price_array) == small_granularity * 2:
                    averagePrice, informed_agents, uninformed_agents, mm_agents = compute_metrics(price_array, 3)

                    intermediate_y.append(averagePrice)
                    intermediate_informed += informed_agents
                    intermediate_uninformed += uninformed_agents
                    intermediate_market_maker += mm_agents

    with list_lock:
        informed.append(intermediate_informed)
        uninformed.append(intermediate_uninformed)
        marketMaker.append(intermediate_market_maker)
        y_axis.append(intermediate_y)
        mean_VPIN_list_very_small.append(VPIN_results_very_small)
        mean_VPIN_list_small.append(VPIN_results_small)
        mean_VPIN_list_big.append(VPIN_results_big)
        mean_PRICE_list_very_small.append(PRICE_results_very_small)
        mean_PRICE_list_small.append(PRICE_results_small)
        mean_PRICE_list_big.append(PRICE_results_big)
        mean_assortativity_list.append(assortativity_results)
        mean_bipartivity_list.append(bipartivity_results)
        mean_average_clustering_list.append(average_clustering_results)
        mean_connected_list.append(connected_results)
        mean_stars_list.append(stars_results)
        mean_diameter_list.append(diameter_results)
        mean_independence_list.append(independence_results)
        mean_closeness_list.append(closeness_results)
        mean_betweenness_list.append(betweenness_results)


def mean_with_padding(a):
    max_len = max([len(row) for row in a])
    mask = np.array([row + [np.nan] * (max_len - len(row)) for row in a])
    return np.nanmean(mask, axis=0)


if __name__ == '__main__':
    ONLY_PRICE = False

    # Create a VPIN list
    mean_VPIN_results_very_small = multiprocessing.Manager().list()
    mean_VPIN_results_small = multiprocessing.Manager().list()
    mean_VPIN_results_big = multiprocessing.Manager().list()

    mean_PRICE_results_very_small = multiprocessing.Manager().list()
    mean_PRICE_results_small = multiprocessing.Manager().list()
    mean_PRICE_results_big = multiprocessing.Manager().list()

    mean_assortativity_results = multiprocessing.Manager().list()
    mean_bipartivity_results = multiprocessing.Manager().list()
    mean_average_clustering_results = multiprocessing.Manager().list()
    mean_connected_results = multiprocessing.Manager().list()
    mean_stars_results = multiprocessing.Manager().list()
    mean_diameter_results = multiprocessing.Manager().list()
    mean_independence_results = multiprocessing.Manager().list()
    mean_closeness_results = multiprocessing.Manager().list()
    mean_betweenness_results = multiprocessing.Manager().list()

    y_price_axis = multiprocessing.Manager().list()
    informed_transactions = multiprocessing.Manager().list()
    uninformed_transactions = multiprocessing.Manager().list()
    market_maker_transactions = multiprocessing.Manager().list()

    lock = multiprocessing.Lock()

    number_of_simulations = int(sys.argv[1])
    small_granularity = int(sys.argv[5])
    days = int(sys.argv[7])

    # Create processes for each simulation using a for loop
    processes = []
    for simulationIndex in range(number_of_simulations):
        process = multiprocessing.Process(target=task, args=(simulationIndex,
                                                             mean_VPIN_results_very_small,
                                                             mean_VPIN_results_small,
                                                             mean_VPIN_results_big,
                                                             mean_PRICE_results_very_small,
                                                             mean_PRICE_results_small,
                                                             mean_PRICE_results_big,
                                                             mean_assortativity_results,
                                                             mean_bipartivity_results,
                                                             mean_average_clustering_results, 
                                                             mean_connected_results,
                                                             mean_stars_results,
                                                             mean_diameter_results,
                                                             mean_independence_results,
                                                             mean_closeness_results,
                                                             mean_betweenness_results,
                                                             y_price_axis,
                                                             informed_transactions,
                                                             uninformed_transactions,
                                                             market_maker_transactions,
                                                             lock, ONLY_PRICE))
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print('Monte Carlo done. Start generating plots!\n')

    x_axis = []
    number_of_days = 1
    plt.figure().set_figheight(5)
    plt.figure().set_figwidth(20)

    if ONLY_PRICE:
        for simulationIndex in range(int(sys.argv[1])):
            for priceIndex in range(len(y_price_axis[simulationIndex])):
                x_axis.append(priceIndex)
            number_of_days = len(x_axis)
            plt.plot(x_axis, y_price_axis[simulationIndex], label="Simulation" + str(simulationIndex + 1))
            x_axis = []
        plt.title('Price evolution')
        plt.xlabel('Time')
        plt.ylabel('Price')
        # number_of_days (250) === days (40)
        # fictive_crash_day (x) === day (15)
        plt.axvline(x=((15 * number_of_days) / days), color='r', label='Crash Day')
        plt.savefig("price_evolution.png")

        average_informed = np.nanmean(informed_transactions, axis=0)
        average_uninformed = np.nanmean(uninformed_transactions, axis=0)
        average_mm = np.nanmean(market_maker_transactions, axis=0)
        total = average_informed + average_uninformed + average_mm

        print("Informed percentage " + str(average_informed * 100 / total))
        print("Uninformed percentage " + str(average_uninformed * 100 / total))
        print("Market makers percentage " + str(average_mm * 100 / total))

    if not ONLY_PRICE:
        # Mean VPIN (very small)
        mean_VPIN_results_very_small = mean_with_padding(mean_VPIN_results_very_small)

        # Mean VPIN (small)
        mean_VPIN_results_small = mean_with_padding(mean_VPIN_results_small)

        # Mean VPIN (big)
        mean_VPIN_results_big = mean_with_padding(mean_VPIN_results_big)

        # Mean PRICE (very small)
        mean_PRICE_results_very_small = mean_with_padding(mean_PRICE_results_very_small)

        # Mean PRICE (small)
        mean_PRICE_results_small = mean_with_padding(mean_PRICE_results_small)

        # Mean PRICE (big)
        mean_PRICE_results_big = mean_with_padding(mean_PRICE_results_big)

        # Mean Assortativity
        mean_assortativity_results = mean_with_padding(mean_assortativity_results)

        # Mean Average Clustering
        mean_average_clustering_results = mean_with_padding(mean_average_clustering_results)

        # Mean Bipartivity
        mean_bipartivity_results = mean_with_padding(mean_bipartivity_results)

        # Mean Connected Components
        mean_connected_results = mean_with_padding(mean_connected_results)

        # Mean Stars
        mean_stars_results = mean_with_padding(mean_stars_results)

        # Mean Diameter
        mean_diameter_results = mean_with_padding(mean_diameter_results)

        # Mean Independence results
        mean_independence_results = mean_with_padding(mean_independence_results)

        # Mean Closeness results
        mean_closeness_results = mean_with_padding(mean_closeness_results)

        # Mean Betweeness results
        mean_betweenness_results = mean_with_padding(mean_betweenness_results)

        # CORRELATION PLOTS
        x_axis_VPIN_very_small = np.array(mean_VPIN_results_very_small)
        x_axis_VPIN_small = np.array(mean_VPIN_results_small)
        x_axis_VPIN_big = np.array(mean_VPIN_results_big)
        y_axis_PRICE_very_small = np.array(mean_PRICE_results_very_small)
        y_axis_PRICE_small = np.array(mean_PRICE_results_small)
        y_axis_PRICE_big = np.array(mean_PRICE_results_big)
        y_axis_assortativity = np.array(mean_assortativity_results)
        y_axis_bipartivity = np.array(mean_bipartivity_results)
        y_axis_average_clustering = np.array(mean_average_clustering_results)
        y_axis_connected = np.array(mean_connected_results)
        y_axis_stars = np.array(mean_stars_results)
        y_axis_diameter = np.array(mean_diameter_results)
        y_axis_independence = np.array(mean_independence_results)
        y_axis_closeness = np.array(mean_closeness_results)
        y_axis_betweeness = np.array(mean_betweenness_results)

        x_axis_very_small = []
        for index in range(len(x_axis_VPIN_very_small)):
            x_axis_very_small.append(index)

        x_axis_small = []
        for index in range(len(x_axis_VPIN_small)):
            x_axis_small.append(index)

        x_axis_big = []
        for index in range(len(x_axis_VPIN_big)):
            x_axis_big.append(index)

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_diameter, y_axis_PRICE_big,
                     "VPIN", "DIAMETER", "PRICE")
        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_stars, y_axis_PRICE_big,
                     "VPIN", "NUMBER OF STARS", "PRICE")
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_independence, y_axis_PRICE_small,
                     "VPIN", "MAXIMAL INDEPENDENT SET SIZE", "PRICE")
        plot_metrics(x_axis_very_small, x_axis_VPIN_very_small, y_axis_average_clustering, y_axis_PRICE_very_small,
                     "VPIN", "AVERAGE CLUSTERING", "PRICE")
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_assortativity, y_axis_PRICE_small,
                     "VPIN", "ASSORTATIVITY", "PRICE")
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_connected, y_axis_PRICE_small,
                     "VPIN", "CONNECTED COMPONENTS", "PRICE")
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_bipartivity, y_axis_PRICE_small,
                     "VPIN", "BIPARTIVITY", "PRICE")
        plot_metrics(x_axis_very_small, x_axis_VPIN_very_small, y_axis_closeness, y_axis_PRICE_very_small,
                     "VPIN", "CLOSENESS CENTRALITY", "PRICE")
        plot_metrics(x_axis_very_small, x_axis_VPIN_very_small, y_axis_betweeness, y_axis_PRICE_very_small,
                     "VPIN", "BETWEENNESS CENTRALITY", "PRICE")
