import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
@requires pandas, numpy, openpyxl, xlrd
"""
# Functions
graph_color = "#00fdff"
path_color = "#00ff41"

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
    """
    Calcula la distancia euclidiana entre dos puntos x, y
    @param x1: coordenada x del primer punto
    @param y1: coordenada y del primer punto
    @param x2: coordenada x del segundo punto
    @param y2: coordenada y del segundo punto
    @return: la distancia euclidiana
    """
    return np.sqrt((x2 - x1) ** 2 + ( y2 - y1) ** 2)

def dijkstra(graph, source, destination):
    """
    Crea el camino de menor costo entre un
    punto de inicio y otro de llegada
    @param graph: el espacio de busqueda
    @param source: nodo de inicio
    @param destination: nodo de llegada
    @return: el camino de menor costo
    """
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph.copy()
    infinity = 9999999
    path = []
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[source] = 0

    # Mientras hayan nodos sin visitar
    while unseenNodes:
        minNode = None
        # Para cada nodo sin visitar busca la menor distancia
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node

        # Almacena el nodo
        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)

    # Empieza a añadir la ruta
    currentNode = destination
    while currentNode != source:
        try:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('No hay ruta')
            break

    # Si hay ruta, la traza
    path.insert(0, source)
    if shortest_distance[destination] != infinity:
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
    graph = {}
    for point in nodes.index:
        neighbors = {}
        try:
            if len(frame.loc[point].shape) > 1:
                for neighbor, weight in frame.loc[point].values:
                    neighbors[int(neighbor)] = weight
            else:
                neighbor, weight = frame.loc[point]
                neighbors[int(neighbor)] = weight
            graph[point] = neighbors
        except:
            graph[point] = neighbors
            continue
    return graph

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
        axes.plot([x1, x2], [y1, y2], color=path_color, marker="s", linestyle="-")

def draw_edges(edges, axes):
    """
    Dibuja los arcos entre los nodos
    @param edges: los arcos a dibujar
    @param axes: el plot donde se van a dibujar
    """
    for i in range(len(edges)):
        axes.plot(edges["Inicial"][i], edges["Final"][i],
                "--", color=graph_color, alpha=0.7)
        axes.plot(edges["Inicial"][i], edges["Final"][i], "-",
                  color=graph_color, alpha=0.1, linewidth=3.5)

def create_edges(nodes):
    """
    Crea los arcos a partir de la distancia
    euclidiana
    @param nodes: los nodos a ser calculados
    @return: un DataFrame con los arcos calculados
    """
    edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            first = nodes.iloc[i]
            second = nodes.iloc[j]
            x1, y1, x2, y2 = first["x"], first["y"], second["x"], second["y"]
            dist = distance(x1, y1, x2, y2)
            if 0 < dist <= 14:
                edges.append([(x1, x2), (y1, y2), i + 1, j + 1, dist])
    return pd.DataFrame(edges, columns=["Inicial", "Final", "i", "j", "Weight"])

def generate_points():
    """
    Funcion que genera los puntos ubicados en el grafo
    @return: un DataFrame con los puntos en el grafo
    """
    return pd.DataFrame(data=np.random.uniform(0, 100, size=(100, 2)),
                          columns=["x", "y"], index=range(1, 101))
    # return pd.read_excel("points.xlsx", index_col=0)

def draw_points(axes, nodes):
    """
    Se encarga de dibujar los puntos en el grafo
    con su respectivo texto
    @param axes: la figura donde se dibujará el grafo
    @param nodes: los nodos que serán dibujados
    """
    axes.plot(nodes["x"], nodes["y"], ".", color=graph_color)
    for i in range(100):
        axes.text(x=nodes["x"].iloc[i] + 1, y=nodes["y"].iloc[i],
                s=(i + 1), fontsize=8, weight='bold', color=graph_color)

def create_figure():
    """
    Crea la figura donde se dibujara el grafo
    @return: la figura de dibujo
    """
    draw_styles()
    fig = plt.figure(figsize=(5, 5))
    axes = fig.add_subplot(111)
    axes.set(xlim=(-5, 105), ylim=(-5, 105))
    axes.grid(color='#2A3459', linestyle="--")
    axes.set_title("Graph")
    return axes

# Graph and Path

def print_menu():
    """
    Imprime el menu del programa
    """
    print("-------------Taller 2--------------")
    print("Escoja una opción:")
    print("1. Generar grafo")
    if len(points) > 0:
        print("2. Ingresar nodos de ruta")
    if len(p) > 0:
        print("3. Mostrar ruta en el grafo")
        print("4. Salir")

if __name__ == "__main__":
    finished = False

    points = []; e = []; p = []

    while not finished:
        print_menu()
        option = int(input())

        if option == 1:
            ax = create_figure()
            points = generate_points()
            draw_points(ax, points)
            e = create_edges(points)
            draw_edges(e, ax)
            plt.show()
        elif option == 2:
            g = to_graph(points, e)
            s = int(input("Ingrese el nodo origen: "))
            d = int(input("Ingrese el nodo destino: "))
            p = dijkstra(g, s, d)
        elif option == 3:
            ax = create_figure()
            draw_points(ax, points)
            draw_edges(e, ax)
            draw_path(p, ax, points)
            plt.show()
        elif option == 4:
            finished = True
        else:
            print("Opcion no valida")