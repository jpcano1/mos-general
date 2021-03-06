################## Punto 1
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

num = 4

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

maquinas = RangeSet(1, num)
trabajos = RangeSet(1, num)

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
