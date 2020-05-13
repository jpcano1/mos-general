from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

dias = [("L", 17), ("M", 13), ("I", 15), ("J", 19), ("V", 14), ("S", 16), ("D", 11)]

Model = ConcreteModel()

Model.x = Var(domain=PositiveIntegers)

Model.obj = Objective(expr=Model.x, sense=minimize)

SolverFactory("glpk").solve(Model)

Model.display()
