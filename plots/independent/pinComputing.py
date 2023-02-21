from plots.independent.processFile import *


def compute_pin(prices):
    informed_transactions = 0
    total_transactions = 0

    for price in prices:
        if price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Undervalued")\
                or price.second_agent.startswith("Overvalued") or price.second_agent.startswith("Undervalued"):
            informed_transactions += 1
        total_transactions += 1

    return informed_transactions / total_transactions


# index = 1
# result = process()
#
# for day, price_array in result.items():
#     PIN = compute_pin(price_array)
#     print("Day: ", index, " PIN: ", PIN)
#     index += 1