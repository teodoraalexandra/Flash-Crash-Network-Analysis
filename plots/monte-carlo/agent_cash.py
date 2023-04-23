import csv
import sys
import multiprocessing
import matplotlib.pyplot as plt
from statistics import mean
from plots.independent.processFile import Day
from plots.independent.processFile import Agent


def legend_without_duplicate_labels(figure):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    figure.legend(by_label.values(), by_label.keys(), loc='upper right')


def task(counter, y_noise_all, y_informed_all, y_noise_all_average, y_informed_all_average, list_lock):
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

                if agent_object.name not in list_of_agents:
                    list_of_agents.append(agent_object.name)

                # Add the price to the intermediate array
                if agent_object.name in array:
                    array[agent_object.name].append(int(agent_object.cash))
                else:
                    array[agent_object.name] = [int(agent_object.cash)]
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

    for agent in sorted_list_of_agents:
        for day in result.keys():
            value = result.get(day).get(agent)
            if agent.startswith('Noise'):
                y_noise.append(round(mean(value)))
            else:
                if value is None:
                    y_informed.append(0)
                else:
                    y_informed.append(round(mean(value)))

        # Plotting the points
        if len(y_noise) > 0 and agent.startswith('Noise'):
            with list_lock:
                y_noise_all.append(y_noise)
        if len(y_informed) > 0 and agent.startswith('Overvalued'):
            with list_lock:
                y_informed_all.append(y_informed)

        if agent.startswith('Noise'):
            y_noise_average.append(y_noise)
            y_noise = []
        else:
            y_informed_average.append(y_informed)
            y_informed = []

    column_average_noise = [sum(sub_list) / len(sub_list) for sub_list in zip(*y_noise_average)]
    column_average_informed = [sum(sub_list) / len(sub_list) for sub_list in zip(*y_informed_average)]

    # Plotting the points
    with list_lock:
        y_noise_all_average.append(column_average_noise)
        y_informed_all_average.append(column_average_informed)


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    # Create three processes for each task using a for loop
    processes = []

    # X axis values
    x = list(range(1, int(sys.argv[2]) + 1))

    axis_noise = multiprocessing.Manager().list()
    axis_informed = multiprocessing.Manager().list()
    axis_noise_average = multiprocessing.Manager().list()
    axis_informed_average = multiprocessing.Manager().list()

    for simulationIndex in range(int(sys.argv[1])):
        process = multiprocessing.Process(target=task, args=(simulationIndex, axis_noise, axis_informed,
                                                             axis_noise_average, axis_informed_average, lock))
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

    plt.axvline(x=30, color='r', label='Crash Day')

    for noise in axis_noise:
        plt.plot(x, noise, color='g', label='Uninformed agents')
    for informed in axis_informed:
        plt.plot(x, informed, color='m', label='Informed agents')
    for noiseAverage in axis_noise_average:
        plt.plot(x, noiseAverage, color='b', label='Uninformed average performance')
    for informedAverage in axis_informed_average:
        plt.plot(x, informedAverage, color='c', label='Informed average performance')

    # Giving a title
    plt.title("Evolution of Agents' cash")

    # Prevent scientific notation
    plt.ticklabel_format(style='plain')

    # Adding a label with no duplicates
    legend_without_duplicate_labels(plt)

    # Function to show the plot
    plt.savefig("agents_cash_evolution.png")
    plt.close()
