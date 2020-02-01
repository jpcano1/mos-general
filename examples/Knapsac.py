from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

numUtiles = 5

Model = ConcreteModel()

p = RangeSet(1, numUtiles)

valor = {
    1: {
        'peso': 4,
        'valor': 8
    },
    2: {
        'peso': 6,
        'valor': 5
    },
    3: {
        'peso': 3,
        'valor': 2
    },
    4: {
        'peso': 7,
        'valor': 11
    },
    5: {
        'peso': 2,
        'valor': 4
    }
}

# The model
Model.x = Var(p, domain=Binary)

# We define the objective function
Model.obj = Objective(expr = sum(Model.x[i] * valor[i]['valor'] for i in p), sense=maximize)

# Constraint to the maximum weight in the knapsac
Model.res1 = Constraint(expr = sum(Model.x[i] * valor[i]['peso'] for i in p) <= 20)

# Applying the solver
SolverFactory('glpk').solve(Model)

Model.display()