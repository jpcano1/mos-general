from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

# Variable que modela las corrientes I
corrientes = {
    1: 4,
    2: 6,
    3: 8,
    4: 18
}

p = RangeSet(1, 4)

# Creación del modelo
Model = ConcreteModel()

# Modela las resistencias del circuito
Model.resistencias = Var(p, domain=PositiveReals)

# Funcion objetivo. Optimizar la potencia total disipada
Model.obj = Objective(expr=sum(corrientes[i]**2 * Model.resistencias[i] for i in p), sense=minimize)

# Resticciones
def equal_voltage(model):
    """
    Modela la primera restricción, que el voltage
    de la resistencia 1 y 2 sea igual
    @param model: el modelo al cual se le aplicará la restricción
    @return: la restricción que se aplicará
    """
    v1 = model.resistencias[1] * corrientes[1]
    v2 = model.resistencias[2] * corrientes[2]
    return v1 == v2

Model.res1 = Constraint(rule=equal_voltage)

def equal_voltage_2(model):
    """
    Modela la primera restricción, que el voltage
    de la resistencia 2 y 3 sea igual
    @param model: el modelo al cual se le aplicará la restricción
    @return: la restricción que se aplicará
    """
    v1 = model.resistencias[1] * corrientes[1]
    v3 = model.resistencias[3] * corrientes[3]
    return v1 == v3

Model.res2 = Constraint(rule=equal_voltage_2)

def resistance_limits(model, i):
    """
    Resticción que limita el valor de las resistencias
    @param model: el modelo al cual se le aplicará la restricción
    @param i: El iterador de las resistencias
    @return: la restricción que se aplicará
    """
    return inequality(2, model.resistencias[i] * corrientes[i], 10)

Model.res3 = Constraint(p, rule=resistance_limits)

# Se resuelve el modelo
SolverFactory('glpk').solve(Model)
Model.display()