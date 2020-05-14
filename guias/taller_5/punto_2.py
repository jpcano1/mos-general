from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

numLosas = 20

"""
Variable que representa los arcos entre las losas
"""
losas_arcos = [
    (1, 5),

    (2, 3, 6, 7),

    (5, 9),

    (9, 10, 13, 14),

    (13, 17),

    (10, 11, 14, 15),

    (8, 12, 16, 20, 19)
]

# Rango de variables
p = RangeSet(1, numLosas)

m = ConcreteModel()

m.losas = Var(p, domain=Binary)

# Función objetivo
m.obj = Objective(expr=sum(m.losas[i] for i in p), sense=minimize)

def least_connection(model, i):
    """
    Restricción que busca que se
    levante al menos una baldosa con conexión
    @param model: Modelo al cual se le va a aplicar
    la restricción
    @param i: conjunto sobre el cual se va a iterar
    @return: La restricción del modelo
    """
    tupla = tuple()
    for index in range(len(losas_arcos)):
        if i in losas_arcos[index]:
            tupla = losas_arcos[index]
            break
    return sum(model.losas[k] for k in tupla) >= 1 if tupla else Constraint.Skip

m.res1 = Constraint(p, rule=least_connection)

# Solver
SolverFactory('glpk').solve(m)
m.display()