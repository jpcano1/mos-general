import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Plots
figure = plt.figure(figsize=(5, 5))
ax = figure.add_subplot(1, 1, 1)
ax.set(xlim=(-5, 105), ylim=(-5, 105))
ax.grid(1)

# Functions
def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + ( y2 - y1) ** 2)

points = pd.DataFrame(data=np.random.uniform(0, 100, size=(100, 2)), columns=["x", "y"])
ax.plot(points["x"], points["y"], "ko")

edges = []

for i in range(len(points)):
    ax.text(x=points["x"][i] - 0.1, y=points["y"][i] - 0.1, s=(i+1))

    for j in range(i+1, len(points)):
        first = points.loc[i]
        second = points.loc[j]
        x1, y1, x2, y2 = first["x"], first["y"], second["x"], second["y"]
        dist = distance(x1, y1, x2, y2)
        if 0 < dist <= 15:
            edges.append([(x1, x2), (y1, y2)])

edges = pd.DataFrame(edges, columns=["Inicial", "Final"])

for i in range(len(edges)):
    ax.plot(edges["Inicial"][i], edges["Final"][i], "k--")

plt.show()