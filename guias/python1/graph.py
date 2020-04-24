import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
@requires pandas, numpy
"""
# Functions

def draw_styles():
    """
    Se encarga de poner el estilo en el plot principal
    """
    plt.style.use("dark_background")
    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.9'  # very light grey
    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#212946'  # bluish dark grey

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
            print('No hay ruta')
            break

    path.insert(0, start)
    if shortest_distance[goal] != infinity:
        return path
    else:
        return None

def to_graph(nodes, edges):
    """
    Crea el grafo a partir de puntos y arcos
    @param nodes: los puntos del grafo
    @param edges: los arcos del grafo
    @return: El grafo en forma de diccionario
    """
    frame = pd.DataFrame(edges.loc[:, ["i", "j", "Weight"]])
    frame = frame.set_index("i")
    g = {}
    for point in nodes.index:
        neighbors = {}
        try:
            if len(frame.loc[point].shape) > 1:
                for neighbor, weight in frame.loc[point].values:
                    neighbors[int(neighbor)] = weight
            else:
                neighbor, weight = frame.loc[point]
                neighbors[int(neighbor)] = weight
            g[point] = neighbors
        except:
            g[point] = neighbors
            continue
    return g

def draw_path(path, axes, nodes):
    """
    Dibuja la ruta entre dos puntos del grafo
    @param path: la ruta entre dos puntos del grafo
    @param axes: el plot donde se dibujara el camino
    @param nodes: los nodos de la ruta
    """
    for i in range(1, len(path)):
        current = path[i]
        previous = path[i - 1]
        (x1, y1), (x2, y2) = nodes.loc[current, ["x", "y"]], nodes.loc[previous, ["x", "y"]]
        axes.plot([x1, x2], [y1, y2], color="#08ff08", marker="s", linestyle="-")

def draw_edges(edges, axes):
    """
    Dibuja los arcos entre los nodos
    @param edges: los arcos a dibujar
    @param axes: el plot donde se van a dibujar
    """
    for i in range(len(edges)):
        axes.plot(edges["Inicial"][i], edges["Final"][i],
                "--", color="#00fdff", alpha=0.7)
        axes.plot(edges["Inicial"][i], edges["Final"][i], "-",
                  color="#00fdff", alpha=0.1, linewidth=3.5)

def create_edges(nodes):
    """
    Crea los arcos a partir de la distancia
    euclidiana
    @param nodes: los nodos a ser calculados
    @return: un DataFrame con los arcos calculados
    """
    edges = []
    for i in range(len(nodes)):
        ax.text(x=nodes["x"].iloc[i] + 1, y=nodes["y"].iloc[i],
                s=(i + 1), fontsize=8, weight='bold', color="#00fdff")
        for j in range(len(nodes)):
            first = nodes.iloc[i]
            second = nodes.iloc[j]
            x1, y1, x2, y2 = first["x"], first["y"], second["x"], second["y"]
            dist = distance(x1, y1, x2, y2)
            if 0 < dist <= 14:
                edges.append([(x1, x2), (y1, y2), i + 1, j + 1, dist])
    return pd.DataFrame(edges, columns=["Inicial", "Final", "i", "j", "Weight"])

# Styles
draw_styles()

# Plots
figure = plt.figure(figsize=(5, 5))
ax = figure.add_subplot(1, 1, 1)
ax.set(xlim=(-5, 105), ylim=(-5, 105))
ax.grid(color='#2A3459')

# Points
points = pd.DataFrame(data=np.random.uniform(0, 100, size=(100, 2)),
                      columns=["x", "y"], index=np.arange(1, 101))
# points = pd.read_excel("points.xlsx", index_col=0)
ax.plot(points["x"], points["y"], ".", color="#00fdff")

# Edges
e = create_edges(points)

draw_edges(e, ax)

# Graph and Path
g = to_graph(points, e)
s = int(input("Ingrese el nodo origen: "))
d = int(input("Ingrese el nodo destino: "))

p = dijkstra(g, s, d)

draw_path(p, ax, points)

plt.show()
