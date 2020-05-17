from __future__ import division
from pyomo.environ import *
import numpy as np
import pandas as pd

from pyomo.opt import SolverFactory

np.random.seed(1234)
precio_gasolina = 8

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
            if 0 < dist <= 25:
                # Se añaden los arcos al diccionario y al arreglo
                edges[i, j] = {"D": dist, "M": 30}
                edges_df.append([(coords_1[0], coords_2[0]), (coords_1[1], coords_2[1])])
            else:
                edges[i, j] = {"D": 9999, "M": 0}
    edges_df = pd.DataFrame(edges_df, columns=["x", "y"])
    return edges, edges_df

nodos = {
    1: (10, 50),
    2: (30, 60),
    3: (50, 60),
    4: (30, 40),
    5: (50, 40),
    6: (70, 50)
}

arcos, _ = generate_edges(nodos)

paquetes = {
    1: {
        "G": 40,
        "P": 15
    },
    2: {
        "G": 35,
        "P": 10
    },
    3: {
        "G": 30,
        "P": 12
    },
    4: {
        "G": 25,
        "P": 8
    },
    5: {
        "G": 32,
        "P": 11
    }
}

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
    """
    Restricción que modela el peso máximo para el número
    de paquetes que un envío puede llevar por las vías del país
    @param model: el modelo al cual se le aplicara  la restricción
    @param i: los nodos de salida
    @param j: los nodos de llegada
    @return: la restricción
    """
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

# Solver
SolverFactory('glpk').solve(Model)
Model.display()