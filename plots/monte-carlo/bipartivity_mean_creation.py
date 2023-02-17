from plots.independent.processFile import process
from plots.independent.bipartivityComputing import compute_bipartivity
import csv

index = 1
result = process()
bipartivity_results = []

for day, price_array in result.items():
    bipartivity = compute_bipartivity(price_array)
    bipartivity_results.append(bipartivity)
    index += 1

with open('bipartivity_mean.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(bipartivity_results)
