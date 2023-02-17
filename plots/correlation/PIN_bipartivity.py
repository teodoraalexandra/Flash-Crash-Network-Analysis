from plots.independent.pinComputing import compute_pin
from plots.independent.bipartivityComputing import compute_bipartivity
from plots.independent.processFile import process
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats


index = 1
result = process()
PIN_results = []
bipartivity_results = []

for day, price_array in result.items():
    PIN = compute_pin(price_array)
    bipartivity = compute_bipartivity(price_array)
    PIN_results.append(PIN)
    bipartivity_results.append(bipartivity)
    index += 1

