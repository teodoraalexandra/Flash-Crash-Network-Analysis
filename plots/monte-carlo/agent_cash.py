import csv
import sys
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
from plots.independent.processFile import Day
from plots.independent.processFile import Agent


def legend_without_duplicate_labels(figure):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    figure.legend(by_label.values(), by_label.keys(), loc='upper right')


def task(counter, y_noise_all, y_informed_all, y_mm_all,
         y_noise_all_average, y_informed_all_average, y_mm_all_average, list_lock):
    list_of_agents = []

    with open("plots/csvs/agents" + str(counter + 1) + ".csv", "r") as csvfile:
        reader_variable = csv.reader(csvfile, delimiter=";")

        # Skip the first two headers
        next(reader_variable, None)
        next(reader_variable, None)

        # Intermediate array for adding all agents and cash from one day
        array = {}

        # Resulting array
        result = {}

        for row in reader_variable:
            if row[0] == 'Agent':
                agent_object = Agent()
                agent_object.name = row[1]
                agent_object.cash = row[2]
                agent_object.invests = row[4]
                agent_object.LastFixedPrice = row[5]

                if agent_object.name not in list_of_agents:
                    list_of_agents.append(agent_object.name)

                # Add the price to the intermediate array
                if agent_object.name in array:
                    wealth = int(agent_object.cash) + int(agent_object.invests) * int(agent_object.LastFixedPrice)
                    array[agent_object.name].append(wealth)
                else:
                    wealth = int(agent_object.cash) + int(agent_object.invests) * int(agent_object.LastFixedPrice)
                    array[agent_object.name] = [wealth]
            elif row[0] == 'Day':
                day_object = Day()
                day_object.day_number = row[1]

                result[day_object.day_number] = array
                array = {}

    sorted_list_of_agents = sorted(list_of_agents)

    # Y axis values
    y_noise = []
    y_noise_average = []
    y_informed = []
    y_informed_average = []
    y_mm = []
    y_mm_average = []

    for agent in sorted_list_of_agents:
        for day in result.keys():
            value = result.get(day).get(agent)
            if agent.startswith('Noise'):
                if value is None:
                    y_noise.append(0)
                else:
                    y_noise.append(round(mean(value)))
            if agent.startswith('Overvalued'):
                if value is None:
                    y_informed.append(0)
                else:
                    y_informed.append(round(mean(value)))
            if agent.startswith('MM'):
                if value is None:
                    y_mm.append(0)
                else:
                    y_mm.append(round(mean(value)))

        # Plotting the points
        if agent.startswith('Noise'):
            with list_lock:
                y_noise_all.append(y_noise)
        if agent.startswith('Overvalued'):
            with list_lock:
                y_informed_all.append(y_informed)
        if agent.startswith('MM'):
            with list_lock:
                y_mm_all.append(y_mm)

        if agent.startswith('Noise'):
            y_noise_average.append(y_noise)
            y_noise = []
        if agent.startswith('Overvalued'):
            y_informed_average.append(y_informed)
            y_informed = []
        if agent.startswith('MM'):
            y_mm_average.append(y_mm)
            y_mm = []

    column_average_noise = [sum(sub_list) / len(sub_list) for sub_list in zip(*y_noise_average)]
    column_average_informed = [sum(sub_list) / len(sub_list) for sub_list in zip(*y_informed_average)]
    column_average_mm = [sum(sub_list) / len(sub_list) for sub_list in zip(*y_mm_average)]

    # Plotting the points
    with list_lock:
        y_noise_all_average.append(column_average_noise)
        y_informed_all_average.append(column_average_informed)
        y_mm_all_average.append(column_average_mm)


def mean_with_padding(a):
    max_len = max([len(row) for row in a])
    mask = np.array([row + [np.nan] * (max_len - len(row)) for row in a])
    return np.nanmean(mask, axis=0)


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    # Create three processes for each task using a for loop
    processes = []

    simulations = sys.argv[1]
    agents = sys.argv[2]
    percentage = sys.argv[3]
    days = sys.argv[4]

    # X axis values
    x = list(range(1, int(days) + 1))

    axis_noise = multiprocessing.Manager().list()
    axis_informed = multiprocessing.Manager().list()
    axis_mm = multiprocessing.Manager().list()
    axis_noise_average = multiprocessing.Manager().list()
    axis_informed_average = multiprocessing.Manager().list()
    axis_mm_average = multiprocessing.Manager().list()

    for simulationIndex in range(int(simulations)):
        process = multiprocessing.Process(target=task, args=(simulationIndex, axis_noise, axis_informed, axis_mm,
                                                             axis_noise_average, axis_informed_average, axis_mm_average,
                                                             lock))
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    plt.figure(figsize=(9, 5))

    # Naming the X axis
    plt.xlabel('Day number')
    # Naming the Y axis
    plt.ylabel('Cash')

    plt.axvline(x=15, color='m', label='HFT Market Entry')

    # For a more detailed graph
    # for noise in axis_noise:
    #     plt.plot(x, noise, color='k', label='Uninformed agents')
    # for informed in axis_informed:
    #     plt.plot(x, informed, color='r', label='Informed agents')
    # for market in axis_mm:
    #     plt.plot(x, market, color='g', label='Market makers')

    plt.plot(x, mean_with_padding(axis_noise_average), color='k', label='Uninformed average performance')
    plt.plot(x, mean_with_padding(axis_informed_average), color='r', label='Informed average performance')
    plt.plot(x, mean_with_padding(axis_mm), color='g', label='Market makers average performance')

    # Giving a title
    plt.title("Evolution of Agents' cash")

    # Prevent scientific notation
    plt.ticklabel_format(style='plain')

    # Adding a label with no duplicates
    legend_without_duplicate_labels(plt)

    axis_noise_average = mean_with_padding(axis_noise_average)
    axis_informed_average = mean_with_padding(axis_informed_average)

    initial_price_noise = int(axis_noise_average[0])  # First day
    final_price_noise = int(axis_noise_average[-1])  # Last day
    initial_price_informed = int(axis_informed_average[14])  # Day 15
    final_price_informed = int(axis_informed_average[-1])  # Last day

    # Function to show the plot
    plt.savefig("results/agents_cash_evolution" + "_" + simulations + "_" + agents + "_" + percentage + ".png")
    plt.close()
