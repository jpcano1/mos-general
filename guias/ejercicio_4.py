from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

numCities = 6

''' Modelado del problema número 4 '''
distBetweenCities = {
    (1, 1): 0,
    (1, 2): 10,
    (1, 3): 20,
    (1, 4): 30,
    (1, 5): 30,
    (1, 6): 20,

    (2, 1): 10,
    (2, 2): 0,
    (2, 3): 25,
    (2, 4): 35,
    (2, 5): 20,
    (2, 6): 10,

    (3, 1): 20,
    (3, 2): 25,
    (3, 3): 0,
    (3, 4): 15,
    (3, 5): 30,
    (3, 6): 20,

    (4, 1): 30,
    (4, 2): 35,
    (4, 3): 15,
    (4, 4): 0,
    (4, 5): 15,
    (4, 6): 25,

    (5, 1): 30,
    (5, 2): 20,
    (5, 3): 30,
    (5, 4): 15,
    (5, 5): 0,
    (5, 6): 14,

    (6, 1): 20,
    (6, 2): 10,
    (6, 3): 20,
    (6, 4): 25,
    (6, 5): 14,
    (6, 6): 0,
}

cities = RangeSet(1, numCities)

Model.cities = Var(cities, cities, domain=Binary)

def objective(model):
    operation = sum(model.cities[i, j]*distBetweenCities[i, j] for i in cities for j in cities)
    return operation

Model.obj = Objective(rule=objective, sense=minimize)

# def least_time(model, i, j):
#     dist = model.cities[i] * distBetweenCities[i, j]
#     return dist <= 15

def least_stations(model):
    return sum(model.cities[i, j] for i in cities for j in cities) >= 1

# Model.con_1 = Constraint(cities, cities, rule=least_time)

Model.con_2 = Constraint(rule=least_stations)

SolverFactory('glpk').solve(Model)

Model.display()