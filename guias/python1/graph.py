from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyomo.environ import *
from pyomo.opt import SolverFactory
"""
@requires pandas, numpy, xlrd, openpyxl
"""

# Functions
def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + ( y2 - y1) ** 2)

# Plots
figure = plt.figure(figsize=(5, 5))
ax = figure.add_subplot(1, 1, 1)
ax.set(xlim=(-5, 105), ylim=(-5, 105))
ax.grid(1)

points = pd.DataFrame(data=np.random.uniform(0, 100, size=(100, 2)), columns=["x", "y"], index=np.arange(1, 101))
# points = pd.read_excel("points.xlsx", index_col=0)
ax.plot(points["x"], points["y"], "k.")

edges = []

for i in range(len(points)):
    ax.text(x=points["x"].iloc[i] - 2, y=points["y"].iloc[i], s=(i+1), fontsize=12, weight='bold')

    for j in range(i+1, len(points)):
        first = points.iloc[i]
        second = points.iloc[j]
        x1, y1, x2, y2 = first["x"], first["y"], second["x"], second["y"]
        dist = distance(x1, y1, x2, y2)
        if 0 < dist <= 14:
            edges.append([(x1, x2), (y1, y2)])

edges = pd.DataFrame(edges, columns=["Inicial", "Final"])

for i in range(len(edges)):
    ax.plot(edges["Inicial"][i], edges["Final"][i], "k--")

# Hasta aquí va  la grafica de nodos y arcos
edges = {}
for i in range(1, len(points) + 1):
    for j in range(1, len(points) + 1):
        first = points.loc[i]
        second = points.loc[j]
        x1, y1, x2, y2 = first["x"], first["y"], second["x"], second["y"]
        dist = distance(x1, y1, x2, y2)
        if 0 < dist <= 14:
            edges[i, j] = dist
        else:
            edges[i, j] = 9999

p = RangeSet(1, 100)

sourceNode = int(input("Ingrese el nodo de salida: "))
destinationNode = int(input("Ingrese el nodo de llegada: "))

Model =ConcreteModel()

Model.x = Var(p, p, domain=Binary)
Model.obj = Objective(expr=sum(Model.x[i, j] * edges[i, j] for i in p for j in p), sense=minimize)

def source_rule(model, i):
    if i == sourceNode:
        return sum(model.x[i, j] for j in p) + sum(model.x[j, i] for j in p) == 1
    else:
        return Constraint.Skip

Model.source = Constraint(p, rule=source_rule)

def destination_rule(model, j):
    if j == destinationNode:
        return sum(model.x[i, j] for i in p) + sum(model.x[j, i] for i in p) == 1
    else:
        return Constraint.Skip

Model.destination = Constraint(p, rule=destination_rule)

def intermediate_rule(model, i):
    if i != sourceNode and i != destinationNode:
        return sum(model.x[i, j] for j in p) - sum(model.x[j, i] for j in p) == 0
    else:
        return Constraint.Skip

Model.intermediate = Constraint(p, rule=intermediate_rule)

def not_repeat_edge_rule(model, i, j):
    return model.x[i, j] + model.x[j, i] <= 1

Model.notRepeatEdge = Constraint(p, p, rule=not_repeat_edge_rule)

SolverFactory('glpk').solve(Model)

for i in range(1, len(points) + 1):
    for j in range(1, len(points) + 1):
        if Model.x[i, j] == 1 and edges[i, j] != 9999:
            ax.plot([points.loc[i, "x"], points.loc[j, "x"]], [points.loc[i, "y"], points.loc[j, "y"]], "rs-")

plt.show()
