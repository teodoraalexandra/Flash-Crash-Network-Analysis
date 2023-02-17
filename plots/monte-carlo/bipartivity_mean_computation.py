import csv
import numpy as np

with open("bipartivity_mean.csv", "r") as f:
    reader = csv.reader(f)
    data = list(reader)

# Convert the data to a numpy array
data = np.array(data, dtype=float)

# Compute the average of each column
averages = np.mean(data, axis=0)

# Convert the averages to a simple array
averages_array = averages.tolist()

# Print the result
print("Real bipartivity_results after Monte Carlo: ", averages_array)
