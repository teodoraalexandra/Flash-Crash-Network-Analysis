import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file
df = pd.read_csv("prices.csv", sep=';')

# Create an empty directed graph
G = nx.DiGraph()

# Iterate through the rows of the dataframe
for _, row in df.iterrows():
    # Get the values from the row
    first_agent = row["AgTrigger"]
    second_agent = row["ag2"]

    G.add_edge(first_agent, second_agent)

# Draw the graph
nx.draw(G, with_labels=True)

# Show the plot
plt.show()
