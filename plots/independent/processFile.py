import csv


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
        return f"Day {self.day_number}: {self.first_price} {self.last_price} {self.lowest_price} {self.highest_price} {self.fixed_prices}"


# def read_csv_prices(i):
    # with open("plots/csvs/prices" + str(i) + ".csv", "r") as csvfile:
    #     reader_variable = csv.reader(csvfile, delimiter=";")
    #
    #     # Skip the first two headers
    #     next(reader_variable, None)
    #     next(reader_variable, None)
    #
    #     # Intermediate array for adding all prices from one day
    #     array = []
    #
    #     # Resulting array
    #     result = {}
    #
    #     for row in reader_variable:
    #         if row[0] == 'Price' and row[5] != 'noname':
    #             # Create price object
    #             price_object = Price()
    #
    #             # Append the properties
    #             price_object.price = row[2]
    #             price_object.quantity = row[3]
    #             price_object.direction = row[4]
    #             price_object.first_agent = row[5]
    #             price_object.second_agent = row[7]
    #             price_object.best_ask = row[9]
    #             price_object.best_bid = row[10]
    #
    #             # Add the price to the intermediate array
    #             array.append(price_object)
    #         elif row[0] == 'Day':
    #             # Create day object
    #             day_object = Day()
    #
    #             # Append the properties
    #             day_object.day_number = row[1]
    #             day_object.first_price = row[3]
    #             day_object.last_price = row[4]
    #             day_object.lowest_price = row[5]
    #             day_object.highest_price = row[6]
    #             day_object.fixed_prices = row[7]
    #
    #             # Append the final aggregation to result
    #             result[day_object] = array
    #
    #             # Clear the array
    #             array = []
    #
    #     return result
