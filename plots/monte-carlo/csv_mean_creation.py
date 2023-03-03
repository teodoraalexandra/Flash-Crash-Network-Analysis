from plots.independent.processFile import process
from plots.independent.pinComputing import compute_pin
from plots.independent.assortativityComputing import compute_assortativity
from plots.independent.bipartivityComputing import compute_bipartivity
import numpy as np
import matplotlib.pyplot as plt
import sys

mean_PIN_results = []
mean_assortativity_results = []
mean_bipartivity_results = []

for simulationIndex in range(int(sys.argv[1])):
    index = 1
    result = process(simulationIndex + 1)
    PIN_results = []
    assortativity_results = []
    bipartivity_results = []

    for day, price_array in result.items():
        PIN = compute_pin(price_array)
        PIN_results.append(PIN)

        assortativity = compute_assortativity(price_array)
        assortativity_results.append(assortativity)

        bipartivity = compute_bipartivity(price_array)
        bipartivity_results.append(bipartivity)

        # For network graph displaying
        # Informed = RED
        # Uninformed = GREEN

        # graph = create_graph(price_array)
        # colors = [node[1]['color'] for node in graph.nodes(data=True)]
        #
        # nx.draw(graph, node_color=colors, with_labels=True)
        # plt.title("Day " + str(index))
        # plt.show()

        index += 1

    mean_PIN_results.append(PIN_results)
    mean_assortativity_results.append(assortativity_results)
    mean_bipartivity_results.append(bipartivity_results)

print('Monte Carlo done. Start correlations!\n')
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
