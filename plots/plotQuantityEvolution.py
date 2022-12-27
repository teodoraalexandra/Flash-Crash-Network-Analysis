import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file
df = pd.read_csv("prices.csv", sep=';')

x_axis = []
y_quantity_axis = []
index = 0

# Iterate through the rows of the dataframe
for _, row in df.iterrows():
    # Get the values from the row
    quantity = row["quty"]

    x_axis.append(index)
    y_quantity_axis.append(quantity)

    index += 1

plt.plot(x_axis, y_quantity_axis)
plt.title('Quantity evolution')
plt.xlabel('Time')
plt.ylabel('Quantity')

# Show the plot
plt.show()
