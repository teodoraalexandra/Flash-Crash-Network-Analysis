from plots.independent.processFile import Price
from plots.independent.computeMetrics import compute_metrics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import multiprocessing
import sys


def rolling_correlation(Y1, Y2, window_size):
    if len(Y1) != len(Y2):
        raise ValueError("Y1 and Y2 must be the same length")

    df = pd.DataFrame({'Y1': Y1, 'Y2': Y2})
    rolling_corr = df['Y1'].rolling(window=window_size).corr(df['Y2'])
    rolling_corr = rolling_corr.dropna()
    rolling_corr = rolling_corr[rolling_corr != 0]
    return rolling_corr

def plot_metrics(X, Y1, Y2, Y3, Y4, metric1, metric2, metric3, metric4, window_size):
    # Y1 = VPIN
    # Y2 = Metric values
    # Y3 = PRICE
    # Y4 = Easley VPIN

    # metric1 = VPIN
    # metric2 = Metric
    # metric3 = PRICE
    # metric4 = Easley VPIN

    COLOR_VPIN = "#3399ff"
    COLOR_METRIC = "#D2042D"
    COLOR_PRICE = "#696969"
    COLOR_EASLEY_VPIN = "#00FF00"

    # Price (Y3) Should be normalized first
    x = np.array(Y3)
    # Normalize all values to be between 0 and 1
    Y3_norm = (x - np.min(x)) / (np.max(x) - np.min(x))

    plt.close()
    fig, ax1 = plt.subplots(figsize=(12, 8))
    ax2 = ax1.twinx()

    l1, = ax2.plot(X, Y1, color=COLOR_VPIN)
    l2, = ax1.plot(X, Y2, color=COLOR_METRIC)
    l3, = ax2.plot(X, Y3_norm, color=COLOR_PRICE)
    l4, = ax2.plot(X, Y4, color=COLOR_EASLEY_VPIN)

    def detect_spikes(data, threshold=3):
        mean = np.mean(data)
        std = np.std(data)
        z_scores = (data - mean) / std
        return np.where(np.abs(z_scores) > threshold)[0]

    def split_data(data, spike_indices, window=3):
        spike_region = []
        non_spike_region = []
        for i in range(len(data)):
            if any(abs(i - idx) <= window for idx in spike_indices):
                spike_region.append(data[i])
            else:
                non_spike_region.append(data[i])
        return np.array(non_spike_region), np.array(spike_region)

    def compute_stats(data):
        mean = np.mean(data)
        std = np.std(data)
        lower = mean - 2 * std
        upper = mean + 2 * std
        return mean, std, lower, upper

    # Standard deviation and confidence interval
    spike_indices_Y1 = detect_spikes(Y1)
    non_spike_Y1, spike_Y1 = split_data(Y1, spike_indices_Y1)
    non_spike_Y2, spike_Y2 = split_data(Y2, spike_indices_Y1)
    non_spike_Y4, spike_Y4 = split_data(Y4, spike_indices_Y1)

    # VPIN (Y1)
    mean_ns_1, std_ns_1, lb_ns_1, ub_ns_1 = compute_stats(non_spike_Y1)
    mean_sp_1, std_sp_1, lb_sp_1, ub_sp_1 = compute_stats(spike_Y1)

    # Metric (Y2)
    mean_ns_2, std_ns_2, lb_ns_2, ub_ns_2 = compute_stats(non_spike_Y2)
    mean_sp_2, std_sp_2, lb_sp_2, ub_sp_2 = compute_stats(spike_Y2)

    # Easley VPIN (Y4)
    mean_ns_4, std_ns_4, lb_ns_4, ub_ns_4 = compute_stats(non_spike_Y4)
    mean_sp_4, std_sp_4, lb_sp_4, ub_sp_4 = compute_stats(spike_Y4)

    # Correlation
    correlation_vpin_metric = rolling_correlation(Y1, Y2, window_size=window_size)
    correlation_vpin_metric = correlation_vpin_metric.mean()
    correlation_vpin_easley_vpin = rolling_correlation(Y1, Y4, window_size=window_size)
    correlation_vpin_easley_vpin = correlation_vpin_easley_vpin.mean()

    # Print stats
    with open("results/stats.txt", "a") as file:
        file.write("\n=== VPIN Analysis ===\n")
        file.write(f"{'Metric':<40}{'Mean (NS)':>12}{'Std (NS)':>12}{'LB (NS)':>12}{'UB (NS)':>12} | {'Mean (SP)':>12}{'Std (SP)':>12}{'LB (SP)':>12}{'UB (SP)':>12}\n")
        file.write("-" * 148 + "\n")  # Adjusted line length to match new width

        # VPIN (Y1)
        file.write(f"{metric1:<40}{mean_ns_1:>12.4f}{std_ns_1:>12.4f}{lb_ns_1:>12.4f}{ub_ns_1:>12.4f} | {mean_sp_1:>12.4f}{std_sp_1:>12.4f}{lb_sp_1:>12.4f}{ub_sp_1:>12.4f}\n")

        # Metric (Y2)
        file.write(f"{metric2:<40}{mean_ns_2:>12.4f}{std_ns_2:>12.4f}{lb_ns_2:>12.4f}{ub_ns_2:>12.4f} | {mean_sp_2:>12.4f}{std_sp_2:>12.4f}{lb_sp_2:>12.4f}{ub_sp_2:>12.4f}\n")

        # Easley VPIN (Y4)
        file.write(f"{metric4:<40}{mean_ns_4:>12.4f}{std_ns_4:>12.4f}{lb_ns_4:>12.4f}{ub_ns_4:>12.4f} | {mean_sp_4:>12.4f}{std_sp_4:>12.4f}{lb_sp_4:>12.4f}{ub_sp_4:>12.4f}\n")

        file.write("\n=== Correlation Analysis ===\n")
        file.write(f"Correlation between {metric1} and {metric2}: {correlation_vpin_metric:.4f}\n")
        file.write(f"Correlation between {metric1} and {metric4}: {correlation_vpin_easley_vpin:.4f}\n")

    ax1.set_xticks([])

    ax2.set_ylabel(metric1, color=COLOR_VPIN, fontsize=14)
    ax2.tick_params(axis="y", labelcolor=COLOR_VPIN)

    ax1.set_ylabel(metric2, color=COLOR_METRIC, fontsize=14)
    ax1.tick_params(axis="y", labelcolor=COLOR_METRIC)

    simulations = sys.argv[1]
    agents = sys.argv[2]
    percentage = sys.argv[3]

    first_crash_index = next((i for i, value in enumerate(Y1) if value > 0), None)
    crash_day_x = X[first_crash_index] - 1
    crash_day_line = plt.axvline(x=crash_day_x, color='m', linestyle='--')

    fig.legend((l1, l2, l3, l4, crash_day_line),
               (metric1, metric2, metric3, metric4, 'HFT Market Entry'),
               fontsize="x-large", loc='center left', bbox_to_anchor=(1.00, 0.5))

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


def task(counter,
         mean_VPIN_list_small,
         mean_VPIN_list_big,
         mean_EVPIN_list_small,
         mean_EVPIN_list_big,
         mean_PRICE_list_small,
         mean_PRICE_list_big,
         mean_assortativity_list_small,
         mean_assortativity_list_big,
         mean_bipartivity_list_small,
         mean_bipartivity_list_big,
         mean_average_clustering_list_small,
         mean_average_clustering_list_big,
         mean_connected_list_small,
         mean_connected_list_big,
         mean_stars_list_small,
         mean_stars_list_big,
         mean_diameter_list_small,
         mean_diameter_list_big,
         mean_independence_list_small,
         mean_independence_list_big,
         mean_closeness_list_small,
         mean_closeness_list_big,
         mean_betweenness_list_small,
         mean_betweenness_list_big,
         y_axis, informed, uninformed, marketMaker, list_lock, PRICE_ONLY):
    VPIN_results_small = []
    VPIN_results_big = []

    EVPIN_results_small = []
    EVPIN_results_big = []

    PRICE_results_small = []
    PRICE_results_big = []

    assortativity_results_small = []
    assortativity_results_big = []

    bipartivity_results_small = []
    bipartivity_results_big = []

    average_clustering_results_small = []
    average_clustering_results_big = []

    connected_results_small = []
    connected_results_big = []

    stars_results_small = []
    stars_results_big = []

    diameter_results_small = []
    diameter_results_big = []

    independence_results_small = []
    independence_results_big = []

    closeness_results_small = []
    closeness_results_big = []

    betweenness_results_small = []
    betweenness_results_big = []

    intermediate_y = []
    intermediate_informed = 0
    intermediate_uninformed = 0
    intermediate_market_maker = 0

    agents = sys.argv[2]
    percentage = sys.argv[3]

    big_granularity = int(sys.argv[4])
    small_granularity = int(sys.argv[5])

    if not PRICE_ONLY:
        with pd.read_csv("plots/csvs/prices" + str(counter + 1) + agents + percentage + ".csv",
                         chunksize=big_granularity, delimiter=";") as reader:
            for chunk in reader:
                price_array = read_prices_in_chunk(chunk)
                if len(price_array) == big_granularity:
                    VPIN, EVPIN, PRICE, assortativity, bipartivity, \
                        averageClustering, conn, stars, diameter, independence, \
                        closeness, betweenness = \
                        compute_metrics(price_array, 0)

                    VPIN_results_big.append(VPIN)
                    EVPIN_results_big.append(EVPIN)
                    PRICE_results_big.append(PRICE)

                    assortativity_results_big.append(assortativity)
                    bipartivity_results_big.append(bipartivity)
                    average_clustering_results_big.append(averageClustering)
                    connected_results_big.append(conn)
                    stars_results_big.append(stars)
                    diameter_results_big.append(diameter)
                    independence_results_big.append(independence)
                    closeness_results_big.append(closeness)
                    betweenness_results_big.append(betweenness)

        with pd.read_csv("plots/csvs/prices" + str(counter + 1) + agents + percentage + ".csv",
                         chunksize=small_granularity, delimiter=";") as reader:
            for chunk in reader:
                price_array = read_prices_in_chunk(chunk)
                if len(price_array) == small_granularity:
                    VPIN, EVPIN, PRICE, assortativity, bipartivity, \
                        averageClustering, conn, stars, diameter, independence, \
                        closeness, betweenness = \
                        compute_metrics(price_array, 1)

                    VPIN_results_small.append(VPIN)
                    EVPIN_results_small.append(EVPIN)
                    PRICE_results_small.append(PRICE)

                    assortativity_results_small.append(assortativity)
                    bipartivity_results_small.append(bipartivity)
                    average_clustering_results_small.append(averageClustering)
                    connected_results_small.append(conn)
                    stars_results_small.append(stars)
                    diameter_results_small.append(diameter)
                    independence_results_small.append(independence)
                    closeness_results_small.append(closeness)
                    betweenness_results_small.append(betweenness)

    if PRICE_ONLY:
        with pd.read_csv("plots/csvs/prices" + str(counter + 1) + agents + percentage + ".csv",
                         chunksize=small_granularity * 2, delimiter=";") as reader:
            for chunk in reader:
                price_array = read_prices_in_chunk(chunk)
                if len(price_array) == small_granularity * 2:
                    averagePrice, informed_agents, uninformed_agents, mm_agents = compute_metrics(price_array, 2)

                    intermediate_y.append(averagePrice)
                    intermediate_informed += informed_agents
                    intermediate_uninformed += uninformed_agents
                    intermediate_market_maker += mm_agents

    with list_lock:
        informed.append(intermediate_informed)
        uninformed.append(intermediate_uninformed)
        marketMaker.append(intermediate_market_maker)
        y_axis.append(intermediate_y)
        mean_VPIN_list_small.append(VPIN_results_small)
        mean_VPIN_list_big.append(VPIN_results_big)
        mean_EVPIN_list_small.append(EVPIN_results_small)
        mean_EVPIN_list_big.append(EVPIN_results_big)
        mean_PRICE_list_small.append(PRICE_results_small)
        mean_PRICE_list_big.append(PRICE_results_big)
        mean_assortativity_list_big.append(assortativity_results_big)
        mean_assortativity_list_small.append(assortativity_results_small)
        mean_bipartivity_list_big.append(bipartivity_results_big)
        mean_bipartivity_list_small.append(bipartivity_results_small)
        mean_average_clustering_list_big.append(average_clustering_results_big)
        mean_average_clustering_list_small.append(average_clustering_results_small)
        mean_connected_list_big.append(connected_results_big)
        mean_connected_list_small.append(connected_results_small)
        mean_stars_list_big.append(stars_results_big)
        mean_stars_list_small.append(stars_results_small)
        mean_diameter_list_big.append(diameter_results_big)
        mean_diameter_list_small.append(diameter_results_small)
        mean_independence_list_big.append(independence_results_big)
        mean_independence_list_small.append(independence_results_small)
        mean_closeness_list_big.append(closeness_results_big)
        mean_closeness_list_small.append(closeness_results_small)
        mean_betweenness_list_big.append(betweenness_results_big)
        mean_betweenness_list_small.append(betweenness_results_small)


def mean_with_padding(a):
    max_len = max([len(row) for row in a])
    mask = np.array([row + [np.nan] * (max_len - len(row)) for row in a])
    return np.nanmean(mask, axis=0)


if __name__ == '__main__':
    ONLY_PRICE = False

    # Create a VPIN list
    mean_VPIN_results_small = multiprocessing.Manager().list()
    mean_VPIN_results_big = multiprocessing.Manager().list()

    # Create a EVPIN list
    mean_EVPIN_results_small = multiprocessing.Manager().list()
    mean_EVPIN_results_big = multiprocessing.Manager().list()

    # Price
    mean_PRICE_results_small = multiprocessing.Manager().list()
    mean_PRICE_results_big = multiprocessing.Manager().list()

    # Assortativity
    mean_assortativity_results_small = multiprocessing.Manager().list()
    mean_assortativity_results_big = multiprocessing.Manager().list()

    # Bipartivity
    mean_bipartivity_results_small = multiprocessing.Manager().list()
    mean_bipartivity_results_big = multiprocessing.Manager().list()

    # Average clustering
    mean_average_clustering_results_small = multiprocessing.Manager().list()
    mean_average_clustering_results_big = multiprocessing.Manager().list()

    # Connected components
    mean_connected_results_small = multiprocessing.Manager().list()
    mean_connected_results_big = multiprocessing.Manager().list()

    # Stars
    mean_stars_results_small = multiprocessing.Manager().list()
    mean_stars_results_big = multiprocessing.Manager().list()

    # Diameter
    mean_diameter_results_small = multiprocessing.Manager().list()
    mean_diameter_results_big = multiprocessing.Manager().list()

    # Max independent set size
    mean_independence_results_small = multiprocessing.Manager().list()
    mean_independence_results_big = multiprocessing.Manager().list()

    # Closeness centrality
    mean_closeness_results_small = multiprocessing.Manager().list()
    mean_closeness_results_big = multiprocessing.Manager().list()

    # Betweenness centrality
    mean_betweenness_results_small = multiprocessing.Manager().list()
    mean_betweenness_results_big = multiprocessing.Manager().list()

    y_price_axis = multiprocessing.Manager().list()
    informed_transactions = multiprocessing.Manager().list()
    uninformed_transactions = multiprocessing.Manager().list()
    market_maker_transactions = multiprocessing.Manager().list()

    lock = multiprocessing.Lock()

    number_of_simulations = int(sys.argv[1])
    small_granularity = int(sys.argv[5])
    days = int(sys.argv[6])

    # Create processes for each simulation using a for loop
    processes = []
    for simulationIndex in range(number_of_simulations):
        process = multiprocessing.Process(target=task, args=(simulationIndex,
                                                             mean_VPIN_results_small,
                                                             mean_VPIN_results_big,
                                                             mean_EVPIN_results_small,
                                                             mean_EVPIN_results_big,
                                                             mean_PRICE_results_small,
                                                             mean_PRICE_results_big,
                                                             mean_assortativity_results_small,
                                                             mean_assortativity_results_big,
                                                             mean_bipartivity_results_small,
                                                             mean_bipartivity_results_big,
                                                             mean_average_clustering_results_small,
                                                             mean_average_clustering_results_big,
                                                             mean_connected_results_small,
                                                             mean_connected_results_big,
                                                             mean_stars_results_small,
                                                             mean_stars_results_big,
                                                             mean_diameter_results_small,
                                                             mean_diameter_results_big,
                                                             mean_independence_results_small,
                                                             mean_independence_results_big,
                                                             mean_closeness_results_small,
                                                             mean_closeness_results_big,
                                                             mean_betweenness_results_small,
                                                             mean_betweenness_results_big,
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
        # Mean VPIN (small)
        mean_VPIN_results_small = mean_with_padding(mean_VPIN_results_small)

        # Mean VPIN (big)
        mean_VPIN_results_big = mean_with_padding(mean_VPIN_results_big)

        # Mean EVPIN (small)
        mean_EVPIN_results_small = mean_with_padding(mean_EVPIN_results_small)

        # Mean EVPIN (big)
        mean_EVPIN_results_big = mean_with_padding(mean_EVPIN_results_big)

        # Mean PRICE (small)
        mean_PRICE_results_small = mean_with_padding(mean_PRICE_results_small)

        # Mean PRICE (big)
        mean_PRICE_results_big = mean_with_padding(mean_PRICE_results_big)

        # Mean Assortativity (small)
        mean_assortativity_results_small = mean_with_padding(mean_assortativity_results_small)

        # Mean Assortativity (big)
        mean_assortativity_results_big = mean_with_padding(mean_assortativity_results_big)

        # Mean Average Clustering (small)
        mean_average_clustering_results_small = mean_with_padding(mean_average_clustering_results_small)

        # Mean Average Clustering (big)
        mean_average_clustering_results_big = mean_with_padding(mean_average_clustering_results_big)

        # Mean Bipartivity (small)
        mean_bipartivity_results_small = mean_with_padding(mean_bipartivity_results_small)

        # Mean Bipartivity (big)
        mean_bipartivity_results_big = mean_with_padding(mean_bipartivity_results_big)

        # Mean Connected Components (small)
        mean_connected_results_small = mean_with_padding(mean_connected_results_small)

        # Mean Connected Components (big)
        mean_connected_results_big = mean_with_padding(mean_connected_results_big)

        # Mean Stars (small)
        mean_stars_results_small = mean_with_padding(mean_stars_results_small)

        # Mean Stars (big)
        mean_stars_results_big = mean_with_padding(mean_stars_results_big)

        # Mean Diameter (small)
        mean_diameter_results_small = mean_with_padding(mean_diameter_results_small)

        # Mean Diameter (big)
        mean_diameter_results_big = mean_with_padding(mean_diameter_results_big)

        # Mean Independence results (small)
        mean_independence_results_small = mean_with_padding(mean_independence_results_small)

        # Mean Independence results (big)
        mean_independence_results_big = mean_with_padding(mean_independence_results_big)

        # Mean Closeness results (small)
        mean_closeness_results_small = mean_with_padding(mean_closeness_results_small)

        # Mean Closeness results (big)
        mean_closeness_results_big = mean_with_padding(mean_closeness_results_big)

        # Mean Betweenness results (small)
        mean_betweenness_results_small = mean_with_padding(mean_betweenness_results_small)

        # Mean Betweenness results (big)
        mean_betweenness_results_big = mean_with_padding(mean_betweenness_results_big)

        big_granularity = int(0.1 * len(mean_PRICE_results_big))
        small_granularity = int(0.1 * len(mean_PRICE_results_small))

        # CORRELATION PLOTS
        x_axis_VPIN_small = np.array(mean_VPIN_results_small)[small_granularity : -small_granularity]
        x_axis_VPIN_big = np.array(mean_VPIN_results_big)[big_granularity : -big_granularity]

        x_axis_EVPIN_small = np.array(mean_EVPIN_results_small)[small_granularity : -small_granularity]
        x_axis_EVPIN_big = np.array(mean_EVPIN_results_big)[big_granularity : -big_granularity]

        y_axis_PRICE_small = np.array(mean_PRICE_results_small)[small_granularity : -small_granularity]
        y_axis_PRICE_big = np.array(mean_PRICE_results_big)[big_granularity : -big_granularity]

        y_axis_assortativity_small = np.array(mean_assortativity_results_small)[small_granularity : -small_granularity]
        y_axis_assortativity_big = np.array(mean_assortativity_results_big)[big_granularity : -big_granularity]

        y_axis_average_clustering_small = np.array(mean_average_clustering_results_small)[small_granularity : -small_granularity]
        y_axis_average_clustering_big = np.array(mean_average_clustering_results_big)[big_granularity : -big_granularity]

        y_axis_diameter_small = np.array(mean_diameter_results_small)[small_granularity : -small_granularity]
        y_axis_diameter_big = np.array(mean_diameter_results_big)[big_granularity : -big_granularity]

        y_axis_independence_small = np.array(mean_independence_results_small)[small_granularity : -small_granularity]
        y_axis_independence_big = np.array(mean_independence_results_big)[big_granularity : -big_granularity]

        y_axis_stars_small = np.array(mean_stars_results_small)[small_granularity : -small_granularity]
        y_axis_stars_big = np.array(mean_stars_results_big)[big_granularity : -big_granularity]

        y_axis_betweenness_small = np.array(mean_betweenness_results_small)[small_granularity : -small_granularity]
        y_axis_betweenness_big = np.array(mean_betweenness_results_big)[big_granularity : -big_granularity]

        y_axis_bipartivity_small = np.array(mean_bipartivity_results_small)[small_granularity : -small_granularity]
        y_axis_bipartivity_big = np.array(mean_bipartivity_results_big)[big_granularity : -big_granularity]

        y_axis_closeness_small = np.array(mean_closeness_results_small)[small_granularity : -small_granularity]
        y_axis_closeness_big = np.array(mean_closeness_results_big)[big_granularity : -big_granularity]

        y_axis_connected_small = np.array(mean_connected_results_small)[small_granularity : -small_granularity]
        y_axis_connected_big = np.array(mean_connected_results_big)[big_granularity : -big_granularity]

        x_axis_small = []
        for index in range(len(x_axis_VPIN_small)):
            x_axis_small.append(index)

        x_axis_big = []
        for index in range(len(x_axis_VPIN_big)):
            x_axis_big.append(index)

        # EASLEY
        # Should be normalized first
        e_vpin_big = np.array(x_axis_EVPIN_big)
        e_vpin_small = np.array(x_axis_EVPIN_small)
        # Normalize all values to be between 0 and 1
        e_vpin_norm_big= (e_vpin_big - np.min(e_vpin_big)) / (np.max(e_vpin_big) - np.min(e_vpin_big))
        e_vpin_norm_small = (e_vpin_small - np.min(e_vpin_small)) / (np.max(e_vpin_small) - np.min(e_vpin_small))

        WINDOW_SIZE_BIG = 40 # Low frequency
        WINDOW_SIZE_SMALL = 40 # High frequency

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_assortativity_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Assortativity (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_assortativity_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Assortativity (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_average_clustering_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Average clustering (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_average_clustering_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Average clustering (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_diameter_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Diameter (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_diameter_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Diameter (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_independence_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Maximal independent set size (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_independence_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Maximal independent set size (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_stars_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Number of stars (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_stars_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Number of stars (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_betweenness_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Betweenness centrality (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_betweenness_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Betweenness centrality (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_bipartivity_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Bipartivity (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_bipartivity_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Bipartivity (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_closeness_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Closeness centrality (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_closeness_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Closeness centrality (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)

        plot_metrics(x_axis_big, x_axis_VPIN_big, y_axis_connected_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Number of connected components (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, y_axis_connected_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Number of connected components (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)

        plot_metrics(x_axis_big, x_axis_VPIN_big, e_vpin_norm_big, y_axis_PRICE_big, e_vpin_norm_big,
                     "VPIN", "Easley's VPIN (low frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_BIG)
        plot_metrics(x_axis_small, x_axis_VPIN_small, e_vpin_norm_small, y_axis_PRICE_small, e_vpin_norm_small,
                     "VPIN", "Easley's VPIN (high frequency)", "Price", "Easley's VPIN", WINDOW_SIZE_SMALL)
