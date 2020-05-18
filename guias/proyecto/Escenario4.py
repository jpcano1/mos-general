from __future__ import division
from pyomo.environ import *
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from pyomo.opt import SolverFactory

G = nx.Graph()
G2 = nx.Graph()
precio_gasolina = 1
nodos = {
    1: (np.random.randint(0, 25), np.random.randint(0, 25)),
    2: (np.random.randint(10, 40), np.random.randint(10, 40)),
    3: (np.random.randint(10, 40), np.random.randint(10, 40)),
    4: (np.random.randint(10, 40), np.random.randint(10, 40)),
    5: (np.random.randint(10, 40), np.random.randint(10, 40)),
    6: (np.random.randint(25, 50), np.random.randint(25, 50)),
}

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
            if 0 < dist <= 20:
                # Se añaden los arcos al diccionario y al arreglo
                peso = np.random.randint(20, 60)
                edges[i, j] = {"D": dist, "M": peso}
                G.add_edge(i,j, weight= round(dist))

                G2.add_edge(i,j, weight = peso)
                edges_df.append([(coords_1[0], coords_2[0]), (coords_1[1], coords_2[1])])
            else:
                edges[i, j] = {"D": 9999, "M": 0}
    edges_df = pd.DataFrame(edges_df, columns=["x", "y"])
    return edges, edges_df



arcos, _ = generate_edges(nodos)
plt.figure(2)
pos = nx.spring_layout(G)  # positions for all nodes
# nodes
nx.draw_networkx_nodes(G,pos, node_size=400)
# edges
nx.draw_networkx_edges(G,pos, width=4)
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

#nx.draw_networkx_edges(G, pos,edgelist=[(1, 2), (2, 3), (3, 8),(8,6)], width=8, alpha=0.5, edge_color='r')
#"""
pos2 = nx.spring_layout(G2)  # positions for all nodes


for k,v in pos2.items():
    # Shift the x values of every node by 10 to the right
    v[0] = v[0] + 2.2
# nodes
nx.draw_networkx_nodes(G2,pos2, node_size=400)
# edges
nx.draw_networkx_edges(G2,pos2, width=5)
labels = nx.get_edge_attributes(G2,'weight')
nx.draw_networkx_edge_labels(G2,pos2,edge_labels=labels)
nx.draw_networkx_labels(G2, pos2, font_size=12, font_family='sans-serif')
#"""
paquetes = {
    1: {
        "G": np.random.randint(20, 60),
        "P": np.random.randint(5, 20)
    },
    2: {
        "G": np.random.randint(20, 60),
        "P": np.random.randint(5, 20)
    },
    3: {
        "G": np.random.randint(20, 60),
        "P": np.random.randint(5, 20)
    },
    4: {
        "G": np.random.randint(20, 60),
        "P": np.random.randint(5, 20)
    },
    5: {
        "G": np.random.randint(20, 60),
        "P": np.random.randint(5, 20)
    }
}
print(paquetes)
r = RangeSet(1, len(nodos))
p = RangeSet(1, len(paquetes))

source = 1
destination = 6

Model = ConcreteModel()
Model.rutas = Var(r, r, domain=Binary)
Model.paquetes = Var(p, domain=Binary)

def objective(model):
    expr1 = sum(paquetes[i]["G"] * model.paquetes[i] for i in p)
    expr2 = precio_gasolina * sum(model.rutas[i, j] * arcos[i, j]["D"] for i in r for j in r)
    return expr1 - expr2

Model.obj = Objective(rule=objective, sense=maximize)

def max_weight(model, i, j):
    if arcos[i, j]["M"] > 0:
        expr1 = sum(paquetes[k]["P"] * model.paquetes[k] for k in p)
        expr2 = arcos[i, j]["M"]
        return expr1 <= expr2
    else:
        return Constraint.Skip

def source_rule(model, i):
    """
    La restriccion del nodo fuente
    @param model: el modelo al cual se le aplicara  la restricción
    @param i: los nodos
    @return: la restriccion
    """
    if i == source:
        return sum(model.rutas[i, j] for j in r) - sum(model.rutas[j, i] for j in r) == 1
    else:
        return Constraint.Skip

def destination_rule(model, j):
    """
    La restriccion del nodo destino
    @param model: el modelo al cual se le aplicara  la restricción
    @param j: los nodos
    @return: la restriccion
    """
    if j == destination:
        return sum(model.rutas[i, j] for i in r) -sum(model.rutas[j, i] for i in r) == 1
    else:
        return Constraint.Skip

def intermediate_rule(model, i):
    """
    Restricción de nodo intermedio
    @param model: el modelo al cual se le aplicara  la restricción
    @param i: los nodos
    @return: la restricción
    """
    if i != source and i != destination:
        return sum(model.rutas[i, j] for j in r) - sum(model.rutas[j, i] for j in r) == 0
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
    return model.rutas[i, j] + model.rutas[j, i] <= 1

Model.res1 = Constraint(r, r, rule=max_weight)
Model.res2 = Constraint(r, rule=source_rule)
Model.res3 = Constraint(r, rule=destination_rule)
Model.res4 = Constraint(r, rule=intermediate_rule)
Model.res5 = Constraint(r, r, rule=not_repeated)

SolverFactory('glpk').solve(Model)
Model.display()