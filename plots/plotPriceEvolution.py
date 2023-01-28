import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file
df = pd.read_csv("prices.csv", sep=';')

x_axis = []
y_price_axis = []
index = 0

# Iterate through the rows of the dataframe
for _, row in df.iterrows():
    # Get the values from the row
    price = row["price"]
    first_agent = row["AgTrigger"]

    if first_agent != 'noname':
        x_axis.append(index)
        y_price_axis.append(price)
        index += 1

plt.plot(x_axis, y_price_axis)
plt.title('Price evolution')
plt.xlabel('Time')
plt.ylabel('Price')

# Show the plot
plt.show()
