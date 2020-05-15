from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

# Modela los días de la semana
dias = {
    "L": 17,
    "M": 13,
    "I": 15,
    "J": 19,
    "V": 14,
    "S": 16,
    "D": 11
}

p = RangeSet(1, 7)

Model = ConcreteModel()

Model.dias = Var(p, domain=PositiveIntegers)

# Función objetivo
Model.obj = Objective(expr=sum(Model.dias[i] for i in p), sense=minimize)

# Restricciones
Model.res1 = Constraint(expr=Model.dias[1] + Model.dias[4] + Model.dias[5] + Model.dias[6] + Model.dias[7] >= dias["L"])
Model.res2 = Constraint(expr=Model.dias[1] + Model.dias[2] + Model.dias[5] + Model.dias[6] + Model.dias[7] >= dias["M"])
Model.res3 = Constraint(expr=Model.dias[1] + Model.dias[2] + Model.dias[3] + Model.dias[6] + Model.dias[7] >= dias["I"])
Model.res4 = Constraint(expr=Model.dias[1] + Model.dias[2] + Model.dias[3] + Model.dias[4] + Model.dias[7] >= dias["J"])
Model.res5 = Constraint(expr=Model.dias[1] + Model.dias[2] + Model.dias[3] + Model.dias[4] + Model.dias[5] >= dias["V"])
Model.res6 = Constraint(expr=Model.dias[2] + Model.dias[3] + Model.dias[4] + Model.dias[5] + Model.dias[6] >= dias["S"])
Model.res7 = Constraint(expr=Model.dias[3] + Model.dias[4] + Model.dias[5] + Model.dias[6] + Model.dias[7] >= dias["D"])

# Solver
SolverFactory("glpk").solve(Model)

a = 0

for i in p:
    a += Model.dias[i].value

Model.display()

print(f"Valor óptimo: {a}")