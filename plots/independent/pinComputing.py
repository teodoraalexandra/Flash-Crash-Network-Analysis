def compute_pin(prices):
    informed_transactions = 0
    total_transactions = 0

    for price in prices:
        if price.first_agent.startswith("Overvalued") or price.first_agent.startswith("Undervalued")\
                or price.second_agent.startswith("Overvalued") or price.second_agent.startswith("Undervalued"):
            informed_transactions += 1
        total_transactions += 1

    return informed_transactions / total_transactions
