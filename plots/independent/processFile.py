class Price:
    def __int__(self, price, quantity, direction, first_agent, second_agent, best_ask, best_bid):
        self.price = price
        self.quantity = quantity
        self.direction = direction
        self.first_agent = first_agent
        self.second_agent = second_agent
        self.best_ask = best_ask
        self.best_bid = best_bid

    def __str__(self):
        return f"Price: {self.price} {self.quantity} {self.direction} " \
               f"{self.first_agent} {self.second_agent} {self.best_ask} {self.best_bid}"


class Day:
    def __int__(self, day_number, first_price, last_price, lowest_price, highest_price, fixed_prices):
        self.day_number = day_number
        self.first_price = first_price
        self.last_price = last_price
        self.lowest_price = lowest_price
        self.highest_price = highest_price
        self.fixed_prices = fixed_prices

    def __str__(self):
        return f"Day {self.day_number}: {self.first_price} {self.last_price} {self.lowest_price} " \
               f"{self.highest_price} {self.fixed_prices}"


class Agent:
    def __int__(self, name, cash, obName, invests, LastFixedPrice):
        self.name = name
        self.cash = cash
        self.obName = obName
        self.invests = invests
        self.LastFixedPrice = LastFixedPrice

    def __str__(self):
        return f"Agent {self.name} {self.cash}"
