import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
@requires pandas, numpy
"""
# Functions
def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + ( y2 - y1) ** 2)

def dijkstra(graph, start, goal):
    """
    Crea el camino de menor costo entre un
    punto de inicio y otro de llegada
    @param graph: el espacio de busqueda
    @param start: nodo de inicio
    @param goal: nodo de llegada
    @return: el camino de menor costo
    """
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph.copy()
    infinity = 9999999
    path = []
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0

    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node

        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)

    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break

    path.insert(0, start)
    if shortest_distance[goal] != infinity:
        return path
    else:
        return None

def to_graph(p, e):
    """
    Crea el grafo a partir de puntos y arcos
    @param p: los puntos del grafo
    @param e: los arcos del grafo
    @return: El grafo en forma de diccionario
    """
    frame = pd.DataFrame(e.loc[:, ["i", "j", "Weight"]])
    frame = frame.set_index("i")
    g = {}
    for point in p.index:
        neighbors = {}
        try:
            for neighbor, weight in frame.loc[point].values:
                neighbors[int(neighbor)] = weight
            g[point] = neighbors
        except:
            g[point] = neighbors
            continue
    return g

# Styles
plt.style.use("dark_background")
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey

# Plots
figure = plt.figure(figsize=(5, 5))
ax = figure.add_subplot(1, 1, 1)
ax.set(xlim=(-5, 105), ylim=(-5, 105))
ax.grid(color='#2A3459')

n_shades = 10
diff_linewidth = 1.05
alpha_value = 0.3 / n_shades

# points = pd.DataFrame(data=np.random.uniform(0, 100, size=(100, 2)),
#                       columns=["x", "y"], index=np.arange(1, 101))
points = pd.read_excel("points.xlsx", index_col=0)
ax.plot(points["x"], points["y"], ".", color="#00fdff")

edges = []

for i in range(len(points)):
    ax.text(x=points["x"].iloc[i] + 1, y=points["y"].iloc[i],
            s=(i+1), fontsize=8, weight='bold', color="#00fdff")

    for j in range(len(points)):
        first = points.iloc[i]
        second = points.iloc[j]
        x1, y1, x2, y2 = first["x"], first["y"], second["x"], second["y"]
        dist = distance(x1, y1, x2, y2)
        if 0 < dist <= 14:
            edges.append([(x1, x2), (y1, y2), i+1, j+1, dist])

edges = pd.DataFrame(edges, columns=["Inicial", "Final", "i", "j", "Weight"])

for i in range(len(edges)):
    ax.plot(edges["Inicial"][i], edges["Final"][i],
            "--", color="#00fdff")
    ax.plot(edges["Inicial"][i], edges["Final"][i], "-",
            color="#00fdff", alpha=0.1, linewidth=3.5)
graph = to_graph(points, edges)
path = dijkstra(graph, 22, 44)

print(str(path))
# plt.show()
