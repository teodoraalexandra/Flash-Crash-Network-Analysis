from plots.independent.processFile import process
from plots.independent.pinComputing import compute_pin
from plots.independent.assortativityComputing import compute_assortativity
from plots.independent.bipartivityComputing import compute_bipartivity
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
import sys


def task(index, mean_PIN_results, mean_assortativity_results, mean_bipartivity_results, y_price_axis, lock):
    result = process(index + 1)
    PIN_results = []
    assortativity_results = []
    bipartivity_results = []
    intermediate_y = []

    for day, price_array in result.items():
        PIN = compute_pin(price_array)
        PIN_results.append(PIN)

        assortativity = compute_assortativity(price_array)
        assortativity_results.append(assortativity)

        bipartivity = compute_bipartivity(price_array)
        bipartivity_results.append(bipartivity)

        intermediate_y.append(int(day.last_price))

        # For network graph displaying
        # Informed = RED
        # Uninformed = GREEN

        # graph = create_graph(price_array)
        # colors = [node[1]['color'] for node in graph.nodes(data=True)]
        #
        # nx.draw(graph, node_color=colors, with_labels=True)
        # plt.title("Day " + str(index))
        # plt.show()

    y_price_axis.append(intermediate_y)

    with lock:
        mean_PIN_results.append(PIN_results)
        mean_assortativity_results.append(assortativity_results)
        mean_bipartivity_results.append(bipartivity_results)


if __name__ == '__main__':
    # Create a PIN list
    mean_PIN_results = multiprocessing.Manager().list()
    mean_assortativity_results = multiprocessing.Manager().list()
    mean_bipartivity_results = multiprocessing.Manager().list()
    y_price_axis = multiprocessing.Manager().list()
    lock = multiprocessing.Lock()

    # Create three processes for each task using a for loop
    processes = []
    for simulationIndex in range(int(sys.argv[1])):
        process = multiprocessing.Process(target=task, args=(simulationIndex, mean_PIN_results, mean_assortativity_results, mean_bipartivity_results, y_price_axis, lock))
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print('Monte Carlo done. Start correlations!\n')
    x_axis = []
    plt.figure().set_figheight(5)
    for dayIndex in range(int(sys.argv[2])):
        x_axis.append(dayIndex + 1)
    for simulationIndex in range(int(sys.argv[1])):
        plt.plot(x_axis, y_price_axis[simulationIndex], label="Simulation" + str(simulationIndex + 1))
    plt.title('Price evolution')
    plt.xlabel('Time')
    plt.ylabel('Price')
    # plt.legend(bbox_to_anchor=(1, 1))
    plt.savefig("price_evolution.png")

    # Convert the data to a numpy array & compute the average of each column
    mean_PIN_results = np.array(mean_PIN_results, dtype=float)
    mean_PIN_results = np.mean(mean_PIN_results, axis=0)

    mean_assortativity_results = np.array(mean_assortativity_results, dtype=float)
    mean_assortativity_results = np.mean(mean_assortativity_results, axis=0)

    mean_bipartivity_results = np.array(mean_bipartivity_results, dtype=float)
    mean_bipartivity_results = np.mean(mean_bipartivity_results, axis=0)

    # CORRELATION PLOTS
    x_axis_PIN = np.array(mean_PIN_results)
    y_axis_assortativity = np.array(mean_assortativity_results)
    y_axis_bipartivity = np.array(mean_bipartivity_results)

    # correlation_matrix_assortativity = np.corrcoef(x_axis_PIN, y_axis_assortativity)
    # print("Correlation matrix PIN-assortativity: \n", correlation_matrix_assortativity)
    # correlation_matrix_bipartivity = np.corrcoef(x_axis_PIN, y_axis_bipartivity)
    # print("Correlation matrix PIN-bipartivity: \n", correlation_matrix_bipartivity)

    # The red squares represent the observations
    # The blue line is the regression line

    plt.style.use('ggplot')

    # Plot first
    fig1, ax1 = plt.subplots()
    ax1.plot(x_axis_PIN, y_axis_assortativity, linewidth=0, marker='s', label='Data points')
    ax1.set_xlabel('PIN')
    ax1.set_ylabel('ASSORTATIVITY')
    ax1.legend(facecolor='white')
    plt.savefig("plot_correlation_1.png")

    # Plot second
    fig2, ax2 = plt.subplots()
    ax2.plot(x_axis_PIN, y_axis_bipartivity, linewidth=0, marker='s', label='Data points')
    ax2.set_xlabel('PIN')
    ax2.set_ylabel('BIPARTIVITY')
    ax2.legend(facecolor='white')
    plt.savefig("plot_correlation_2.png")
