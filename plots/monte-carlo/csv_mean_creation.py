from plots.independent.processFile import read_csv_prices
from plots.independent.pinComputing import compute_pin
from plots.independent.assortativityComputing import compute_assortativity
from plots.independent.bipartivityComputing import compute_bipartivity
from plots.independent.spectralBipartivityComputing import compute_spectral_bipartivity
from plots.independent.plotNetwork import plot_network
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
import sys


def task(index, mean_PIN_results, mean_assortativity_results, mean_bipartivity_results, mean_spectral_results, y_price_axis, lock):
    result = read_csv_prices(index + 1)
    PIN_results = []
    assortativity_results = []
    bipartivity_results = []
    spectral_results = []
    intermediate_y = []

    for day, price_array in result.items():
        PIN = compute_pin(price_array)
        PIN_results.append(PIN)

        assortativity = compute_assortativity(price_array)
        assortativity_results.append(assortativity)

        bipartivity = compute_bipartivity(price_array)
        bipartivity_results.append(bipartivity)

        spectralBipartivity = compute_spectral_bipartivity(price_array)
        spectral_results.append(spectralBipartivity)

        intermediate_y.append(int(day.last_price))

    y_price_axis.append(intermediate_y)

    with lock:
        mean_PIN_results.append(PIN_results)
        mean_assortativity_results.append(assortativity_results)
        mean_bipartivity_results.append(bipartivity_results)
        mean_spectral_results.append(spectral_results)


if __name__ == '__main__':
    # Create a PIN list
    mean_PIN_results = multiprocessing.Manager().list()
    mean_assortativity_results = multiprocessing.Manager().list()
    mean_bipartivity_results = multiprocessing.Manager().list()
    mean_spectral_results = multiprocessing.Manager().list()
    y_price_axis = multiprocessing.Manager().list()
    lock = multiprocessing.Lock()

    # Create three processes for each task using a for loop
    processes = []
    for simulationIndex in range(int(sys.argv[1])):
        process = multiprocessing.Process(target=task, args=(simulationIndex, mean_PIN_results, mean_assortativity_results, mean_bipartivity_results, mean_spectral_results, y_price_axis, lock))
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

    mean_spectral_results = np.array(mean_spectral_results, dtype=float)
    mean_spectral_results = np.mean(mean_spectral_results, axis=0)

    # CORRELATION PLOTS
    x_axis_PIN = np.array(mean_PIN_results)
    y_axis_assortativity = np.array(mean_assortativity_results)
    y_axis_bipartivity = np.array(mean_bipartivity_results)
    y_axis_spectral = np.array(mean_spectral_results)

    # correlation_matrix_assortativity = np.corrcoef(x_axis_PIN, y_axis_assortativity)
    # print("Correlation matrix PIN-assortativity: \n", correlation_matrix_assortativity)
    # correlation_matrix_bipartivity = np.corrcoef(x_axis_PIN, y_axis_bipartivity)
    # print("Correlation matrix PIN-bipartivity: \n", correlation_matrix_bipartivity)

    # The red squares represent the observations
    # The blue line is the regression line

    # Plot first
    plt.close()
    plt.title('Correlation between PIN and assortativity')
    plt.scatter(x_axis_PIN, y_axis_assortativity)
    plt.xlabel('PIN')
    plt.ylabel('Assortativity')
    plt.savefig("plot_PIN_assortativity.png")

    # Plot second
    plt.close()
    plt.title('Correlation between PIN and density')
    plt.scatter(x_axis_PIN, y_axis_bipartivity)
    plt.xlabel('PIN')
    plt.ylabel('Density')
    plt.savefig("plot_PIN_density.png")

    # Plot third
    plt.close()
    plt.title('Correlation between PIN and spectral bipartivity')
    plt.scatter(x_axis_PIN, y_axis_spectral)
    plt.xlabel('PIN')
    plt.ylabel('Bipartivity')
    plt.savefig("plot_PIN_spectral_bipartivity.png")

    plt.close()
    plot_network()
