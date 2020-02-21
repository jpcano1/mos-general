from __future__ import division
import math
from pyomo.environ import *

from pyomo.opt import SolverFactory

def cartesian_distance(x1, x2, y1, y2):
    x_distance = (x2-x1)**2
    y_distance = (y2-y1)**2
    xy_distance = x_distance + y_distance
    return math.sqrt(xy_distance)

nodos = {
    1: (20, 6),
    2: (22, 1),
    3: (9, 2),
    4: (3, 25),
    5: (21, 10),
    6: (29, 2),
    7: (14, 12),
}

arcos = {}

for i in nodos.keys():
    for j in nodos.keys():
        coords_1 = nodos[i]
        coords_2 = nodos[j]
        dist = cartesian_distance(coords_1[0], coords_2[0], coords_1[1], coords_2[1])
        if  0 < dist <= 20:
            arcos[i, j] = dist
        else:
            arcos[i, j] = 999
n = 7

sourceNode = int(input("Ingrese el nodo de salida: "))
destinationNode = int(input("Ingrese el nodo de llegada: "))

p = RangeSet(1, n)

Model = ConcreteModel()

Model.x = Var(p, p, domain=Binary)

Model.obj = Objective(expr=sum(Model.x[i, j] * arcos[i, j] for i in p for j in p), sense=minimize)

def source_rule(model, i):
    if i == sourceNode:
        return sum(model.x[i, j] for j in p) == 1
    else:
        return Constraint.Skip

Model.source = Constraint(p, rule=source_rule)

def destination_rule(model, j):
    if j == destinationNode:
        return sum(model.x[i, j] for i in p) == 1
    else:
        return Constraint.Skip

Model.destination = Constraint(p, rule=destination_rule)

def intermediate_rule(model, i):
    if i != sourceNode and i != destinationNode:
        return sum(model.x[i, j] for j in p) - sum(model.x[j, i] for j in p) == 0
    else:
        return Constraint.Skip

Model.intermediate = Constraint(p, rule=intermediate_rule)

SolverFactory('glpk').solve(Model)

Model.display()