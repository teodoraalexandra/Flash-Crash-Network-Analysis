from plots.independent.processFile import process
from plots.independent.assortativityComputing import compute_assortativity
import csv

index = 1
result = process()
assortativity_results = []

for day, price_array in result.items():
    assortativity = compute_assortativity(price_array)
    assortativity_results.append(assortativity)
    index += 1

with open('assortativity_mean.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(assortativity_results)
