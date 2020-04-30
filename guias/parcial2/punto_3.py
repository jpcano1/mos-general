from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Funciones
"""

# Generación de una semilla aleatoria
np.random.seed(4321)

def distance(x1, x2, y1, y2):
    """
    Calcula la distancia euclidiana entre dos puntos x, y
    @param x1: coordenada x del primer punto
    @param y1: coordenada y del primer punto
    @param x2: coordenada x del segundo punto
    @param y2: coordenada y del segundo punto
    @return: la distancia euclidiana
    """
    x_distance = (x2-x1)**2
    y_distance = (y2-y1)**2
    xy_distance = x_distance + y_distance
    return np.sqrt(xy_distance)

# 1. Generación del grafo
def generate_graph():
    """
    Funcion que genera el grafo y lo retorna
    como un diccionario y como un DataFrame
    @return: un grafo como diccionario y como DataFrame
    """
    graph = {}
    for i in range(1, 7):
        x = np.random.randint(low=0, high=60)
        y = np.random.randint(low=0, high=60)
        graph[i] = (x, y)

    frame = pd.DataFrame(data=graph, index=["x", "y"]).transpose()
    return graph, frame

# Generación de los arcos
def generate_edges(graph):
    """
    Genera los arcos del grafo
    @param graph: El grafo a l cual se le van a generar los arcos
    @return: Los arcos del grafo
    """
    edges = {}
    edges_df = []
    for i in graph.keys():
        for j in graph.keys():
            coords_1 = graph[i]
            coords_2 = graph[j]
            # Se calcula la distancia euclidiana
            dist = distance(coords_1[0], coords_2[0], coords_1[1], coords_2[1])
            if 0 < dist <= 25:
                # Se añaden los arcos al diccionario y al arreglo
                edges[i, j] = dist
                edges_df.append([(coords_1[0], coords_2[0]), (coords_1[1], coords_2[1])])
            else:
                edges[i, j] = 9999
    edges_df = pd.DataFrame(edges_df, columns=["x", "y"])
    return edges, edges_df

# Creacion del plot
def create_figure():
    """
    Se crea la figura donde se hará el plot del gr
    @return: el subplot donde se pintara el grafo
    """
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    ax.grid(linestyle="--")
    ax.set_title("Graph")
    return ax

# 2. Dibujo del grafo
def draw_graph(df, edges_df, ax):
    """
    Dibuja el grafo a partir de los puntos y los arcos entre ellos
    @param df: Los puntos del grafo
    @param edges_df: los arcos entre los puntos
    @param ax: la figura donde se va a dibujar el grafo
    """
    ax.plot(df.loc[:, "x"], df.loc[:, "y"], "bo", label="Nodes")
    # for i in graph.keys():
    #     ax.text(x=graph[i][0] - 3, y=graph[i][1], s=i, fontsize=12, color="b")
    for i in range(1, len(df) + 1):
        ax.text(x=df.loc[i, "x"] - 3, y=df.loc[i, "y"], s=i, fontsize=12, color="b")
    for i in range(len(edges_df)-1):
        ax.plot(edges_df.loc[i, "x"], edges_df.loc[i, "y"], "b-")
    ax.plot(edges_df.iloc[-1, 0], edges_df.iloc[-1, 1], "b-", label="Edges")

# 3. Creación del modelo
# Funcion objetivo
def objective(model):
    """
    Funcion objetivo del modelo
    @param model: el modelo al que se le
     creará la funcion objetivo
    @return: la funcion onjetivo
    """
    # Se busca optimizar el tiempo entre rutas de domiciliarios
    # Se toma el tiempo como la distancia entre puntos
    operation = sum(model.x[i, j] * e[i, j] for i in p for j in p)
    return operation

# Restricciones
def source_rule(model, i):
    """
    La restriccion de los nodos fuente, o de los domiciliarios
    @param model: el modelo al cual se le aplicara  la restricción
    @param i: los nodos
    @return: la restriccion
    """
    # Si los nodos que entran por
    # parametro representan al domiciliario 1 o 2
    if i == source1 or i == source2:
        # Se debe garantizar que de estos nodos solamente salga un arco
        # No le debe entrar ningun arco
        return sum(model.x[i, j] for j in p) - sum(model.x[j, i] for j in p) == 1
    else:
        return Constraint.Skip

def not_source_rule(model, i):
    """
    Restricción que se aplica a los nodos
    que no son domiciliarios
    @param model: el modelo al cual se le aplicará la restricción
    @param i: los nodos
    @return: la resticción
    """
    # Busca que todos los nodos que no son
    # domiciliarios les llegue exactamente un arco
    if i != source1 and i != source2:
        return sum(model.x[j, i] for j in p) == 1
    else:
        return Constraint.Skip

def intermediate_rule(model, i):
    """
    Restricción que se aplica a los nodos
    que no son domiciliarios
    @param model: el modelo al cual se le aplicará la restricción
    @param i: los nodos
    @return: la restricción
    """
    # De todos los nodos que no son
    # domiciliarios, solo puede salir maximo un arco
    if i != source1 and i != source2:
        return sum(model.x[i, j] for j in p) <= 1
    else:
        return Constraint.Skip

def not_repeated(model, i, j):
    """
    Restricción que se aplica a todos
    los nodos del grafo
    @param model: el modelo al cual se le aplicará la restricción
    @param i: los nodos de salida-llegada
    @param j: los nodos de llegada-salida
    @return: la resticción
    """
    # Garantiza que cualquier arco que sale de un nodo
    # No se devuelve
    return model.x[i, j] + model.x[j, i] <= 1

def create_model():
    """
    Funcion que se encarga de crear el modelo,
    asignarle la función objetivo y las restricciones.
    @return: el modelo creado
    """
    # Crea el modelo
    model = ConcreteModel()
    # Le asigna la variable del grafo
    model.x = Var(p, p, domain=Binary)
    # Le asigna la funcion objetivo
    model.obj =Objective(rule=objective, sense=minimize)
    # Le asigna las restricciones
    model.res1 = Constraint(p, rule=source_rule)
    model.res2 = Constraint(p, rule=not_source_rule)
    model.res3 = Constraint(p, rule=intermediate_rule)
    model.res4 = Constraint(p, p, rule=not_repeated)
    return model

# 4. Mostrar el camino
def draw_path(model, ax, graph):
    """
    Dibuja el camino generado por la solucion del modelo
    @param model: El modelo que da la solucion
    @param ax: la figura donde se dibujará el grafo con los caminos
    @param graph: el grafo donde se localizará el camino
    """
    for i in p:
        for j in p:
            if model.x[i, j].value == 1.0:
                ax.plot((graph[i][0], graph[j][0]), (graph[i][1], graph[j][1]), "r*-")

nodos = {
    1: (10, 50),
    2: (30, 60),
    3: (50, 60),
    4: (30, 40),
    5: (50, 40),
    6: (70, 50)
}

def print_menu():
    print("------------Parcial 2------------")
    print("   ---------Punto 3---------")
    print("Escoja una opción")
    print("1. Generar un grafo")
    if len(points) > 0:
        print("2. Ingresar los nodos de los domiciliarios")
    if Model is not None:
        print("3. Mostrar resultado del modelo")
        print("4. Mostrar ruta en el grafo")
        print("5. Salir")

if __name__ == "__main__":
    finished = False

    points, points_df = {}, {}; Model = None
    e, e_df = None, None; source1, source2 = None, None

    while not finished:
        print_menu()
        option = int(input())

        if option == 1:
            axes = create_figure()
            print("1. Aleatorio\n2. Fijo")
            rand = int(input())
            points, points_df = generate_graph() if rand == 1 else (nodos, pd.DataFrame(data=nodos, index=["x", "y"]).transpose())
            e, e_df = generate_edges(points)
            draw_graph(points_df, e_df, axes)
            plt.show()

        elif option == 2:
            source1 = int(input("Ingresar domiciliario 1: "))
            source2 = int(input("Ingresar domiciliario 2: "))
            p = RangeSet(1, len(points))

            Model = create_model()
            SolverFactory('glpk').solve(Model)

        elif option == 3:
            Model.display()

        elif option == 4:
            axes = create_figure()
            draw_graph(points_df, e_df, axes)
            draw_path(Model, axes, points)
            plt.show()

        elif option == 5:
            finished = True
        else:
            print("Opcion no valida")