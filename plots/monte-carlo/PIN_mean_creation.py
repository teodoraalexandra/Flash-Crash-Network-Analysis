from plots.independent.processFile import process
from plots.independent.pinComputing import compute_pin
import csv

index = 1
result = process()
PIN_results = []

for day, price_array in result.items():
    PIN = compute_pin(price_array)
    PIN_results.append(PIN)
    index += 1

with open('PIN_mean.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(PIN_results)
