from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

num_nadadores = 6

# Variable que modela los nadadores
nadadores = {
    1: {
        "E": 85,
        "P": 78,
        "M": 82,
        "L": 84
    },
    2: {
        "E": 88,
        "P": 77,
        "M": 81,
        "L": 84
    },
    3: {
        "E": 87,
        "P": 77,
        "M": 82,
        "L": 86
    },
    4: {
        "E": 82,
        "P": 76,
        "M": 80,
        "L": 83
    },
    5: {
        "E": 89,
        "P": 79,
        "M": 83,
        "L": 84
    },
    6: {
        "E": 86,
        "P": 78,
        "M": 81,
        "L": 85
    }
}

# Variables que modelan los indices
p = RangeSet(1, num_nadadores)
estilos = Set(initialize=["E", "P", "M", "L"])

Model = ConcreteModel()

Model.nadadores = Var(p, estilos, within=Binary)

# Funcion objetivo del modelo matematico
Model.obj = Objective(expr=sum(Model.nadadores[i, j] * nadadores[i][j] for i in p for j in estilos), sense=minimize)

def totalSwimmers(model):
    """
    Expresion que garantiza que van a haber 4
    nadadores exactamente en la competencia
    @param model: el modelo matematico
    @return: una expresion que evalua la restricción
    """
    return sum(model.nadadores[i, j] for i in p for j in estilos) == 4

Model.res1 = Constraint(rule=totalSwimmers)

def onePerStyle(model, j):
    """
    Restriccion que garantiza que va a haber un nadador
    que se desempeñe en unico estilo
    @param model: el modelo matematico
    @param j: los indices de los estilos
    @return: Una expresión que evalua la restricción
    """
    return sum(model.nadadores[i, j] for i in p) == 1

Model.res2 = Constraint(estilos, rule=onePerStyle)

def onePerSwimmer(model, i):
    """
    Restriccion que asegura que cada nadador seleccionado
    se desempeñe en un unico estilo de nado
    @param model: el modelo matematico
    @param i: los indices de los nadadores
    @return: Una expresión que evalua la restricción
    """
    return sum(model.nadadores[i, j] for j in estilos) <= 1

Model.res3 = Constraint(p, rule=onePerSwimmer)

SolverFactory('glpk').solve(Model)

# var = 0
# for i in p:
#     for j in estilos:
#         if Model.nadadores[i, j].value == 1:
#             var += nadadores[i][j]
# print(var)
Model.display()