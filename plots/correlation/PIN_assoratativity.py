from plots.independent.pinComputing import compute_pin
from plots.independent.assortativityComputing import compute_assortativity
from plots.independent.processFile import process
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats


index = 1
result = process()
PIN_results = []
assortativity_results = []

for day, price_array in result.items():
    PIN = compute_pin(price_array)
    assortativity = compute_assortativity(price_array)
    PIN_results.append(PIN)
    assortativity_results.append(assortativity)
    index += 1

x_axis_PIN = np.array(PIN_results)
y_axis_assortativity = np.array(assortativity_results)

# This returns the correlation matrix
# -> a two-dimensional array with the correlation coefficients
r = np.corrcoef(x_axis_PIN, y_axis_assortativity)
print("Correlation matrix: \n", r)

plt.style.use('ggplot')
slope, intercept, r, p, stderr = scipy.stats.linregress(x_axis_PIN, y_axis_assortativity)
line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.2f}'

# The red squares represent the observations
# The blue line is the regression line
fig, ax = plt.subplots()
ax.plot(x_axis_PIN, y_axis_assortativity, linewidth=0, marker='s', label='Data points')
ax.plot(x_axis_PIN, intercept + slope * x_axis_PIN, label=line)
ax.set_xlabel('PIN')
ax.set_ylabel('ASSORTATIVITY')
ax.legend(facecolor='white')
plt.show()
