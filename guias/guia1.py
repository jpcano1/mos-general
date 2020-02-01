################## Punto 1
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

maquinasTrabajos = {
    (1, 1): 14,
    (1, 2): 5,
    (1, 3): 8,
    (1, 4): 7,

    (2, 1): 2,
    (2, 2): 12,
    (2, 3): 6,
    (2, 4): 5,

    (3, 1): 7,
    (3, 2): 8,
    (3, 3): 3,
    (3, 4): 9,

    (4, 1): 2,
    (4, 2): 4,
    (4, 3): 6,
    (4, 4): 10,
}

maquinas = [1, 2, 3, 4]
trabajos = [1, 2, 3, 4]

Model.x = Var(maquinas, trabajos, domain=Binary)

def objective(model):
    """
        Defines the objective of the model
        :param model: the model
        :return: the operation associated to the model
    """
    operation = sum(maquinasTrabajos[i, j] * model.x[i, j] for i in maquinas for j in trabajos)
    return operation

Model.obj = Objective(rule=objective, sense=minimize)

def onePerWork(model, j):
    """
        Defines a constraint for a model iterating on the work
        :param model: the model
        :param j: the work
        :return: the rule
    """
    operation = sum(model.x[i, j] for i in maquinas) == 1
    return operation

Model.onePerWork = Constraint(trabajos, rule=onePerWork)

def onePerMachine(model, i):
    """
        Defines a constraint for a model iterating on the machines
        :param model: the model
        :param i: the machine
        :return: the rule
    """
    operation = sum(model.x[i, j] for j in maquinas) == 1
    return operation

Model.onePerMachine = Constraint(maquinas, rule=onePerMachine)

# Applying the solver
SolverFactory('glpk').solve(Model)

Model.display()

#####################Punto 4


''' Modelado del problema número 4 '''
ciudades = {
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