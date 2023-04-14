import csv
import matplotlib.pyplot as plt
from statistics import mean
from plots.independent.processFile import Day
from plots.independent.processFile import Agent


def legend_without_duplicate_labels(figure):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    figure.legend(by_label.values(), by_label.keys(), loc='upper right')


index = 0
list_of_agents = []

with open("plots/csvs/agents1.csv", "r") as csvfile:
    reader_variable = csv.reader(csvfile, delimiter=";")

    # Skip the first two headers
    next(reader_variable, None)
    next(reader_variable, None)

    # Intermediate array for adding all agents and cash from one day
    array = {}

    # Resulting array
    result = {}

    for row in reader_variable:
        if row[0] == 'Agent':
            # Create agent object
            agent_object = Agent()

            # Append the properties
            agent_object.name = row[1]
            agent_object.cash = row[2]
            agent_object.obName = row[3]
            agent_object.invests = row[4]
            agent_object.LastFixedPrice = row[5]
            if agent_object.name not in list_of_agents:
                list_of_agents.append(agent_object.name)

            # Add the price to the intermediate array
            if agent_object.name in array:
                array[agent_object.name].append(int(agent_object.cash))
            else:
                array[agent_object.name] = [int(agent_object.cash)]
        elif row[0] == 'Day':
            # Create day object
            day_object = Day()

            # Append the properties
            day_object.day_number = row[1]
            day_object.first_price = row[3]
            day_object.last_price = row[4]
            day_object.lowest_price = row[5]
            day_object.highest_price = row[6]
            day_object.fixed_prices = row[7]

            # Append the final aggregation to result
            result[day_object.day_number] = array

            # Clear the array
            array = {}

days = 100  # TODO: get from args
sorted_list_of_agents = sorted(list_of_agents)

# Plot
# X axis values
x = list(range(1, days + 1))
# Y axis values
y_noise = []
y_noise_average = []
y_informed = []
y_informed_average = []

for agent in sorted_list_of_agents:
    for day in result.keys():
        value = result.get(day).get(agent)
        if agent.startswith('Noise'):
            y_noise.append(round(mean(value)))
        else:
            if value is None:
                y_informed.append(0)
            else:
                y_informed.append(round(mean(value)))

    # Plotting the points -> Green Uninformed
    if len(y_noise) > 0 and agent.startswith('Noise'):
        plt.plot(x, y_noise, color='g', label='Uninformed agents')
    if len(y_informed) > 0 and agent.startswith('Overvalued'):
        plt.plot(x, y_informed, color='m', label='Informed agents')
    if agent.startswith('Noise'):
        y_noise_average.append(y_noise)
        y_noise = []
    else:
        y_informed_average.append(y_informed)
        y_informed = []

plt.axvline(x=30, color='r', label='Crash Day')

column_average_noise = [sum(sub_list) / len(sub_list) for sub_list in zip(*y_noise_average)]
column_average_informed = [sum(sub_list) / len(sub_list) for sub_list in zip(*y_informed_average)]

# Naming the X axis
plt.xlabel('Day number')
# Naming the Y axis
plt.ylabel('Cash')

# Giving a title
plt.title('Evolution of Agents cash')

# Plotting the points -> Blue Average
plt.plot(x, column_average_noise, color='b', label='Uninformed average performance')
plt.plot(x, column_average_informed, color='c', label='Informed average performance')

# Adding a label with no duplicates
legend_without_duplicate_labels(plt)

# Function to show the plot
plt.savefig("agents_cash_evolution.png")
plt.close()
