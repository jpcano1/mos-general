from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Sets and Parameters
numProyectos=8

#p=[1, 2, 3, 4, 5, 6, 7, 8]
p=RangeSet(1, numProyectos)

valor={1:2, 2:5, 3:4, 4:2, 5:6, 6:3, 7:1, 8:4}

# Variables
Model.x = Var(p, domain=Binary)

# Objective Function
Model.obj = Objective(expr = sum(Model.x[i]*valor[i] for i in p), sense=maximize)

# Constraints
Model.res1 = Constraint(expr = sum(Model.x[i] for i in p) == 2)

# Applying the solver
SolverFactory('glpk').solve(Model)

Model.display()