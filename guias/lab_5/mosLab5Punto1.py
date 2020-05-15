#Daniel Serrano y Juan Pablo Cano
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

dias = [17, 13, 15, 19, 14, 16,  11]

Model = ConcreteModel()

numdias = 7
Model.N = RangeSet(1, numdias)
Model.cost = Param(Model.N, Model.N, mutable = True)

for i in Model.N:
    for j in Model.N:
        Model.cost[i,j] = 1

#LUNES
Model.cost[1,2] = 0
Model.cost[1,3] = 0
#MARTES
Model.cost[2,3] = 0
Model.cost[2,4] = 0
#MIERCOLES
Model.cost[3,4] = 0
Model.cost[3,5] = 0
#JUEVES
Model.cost[4,5] = 0
Model.cost[4,6] = 0
#VIERNES
Model.cost[5,6] = 0
Model.cost[5,7] = 0
#SABADO
Model.cost[6,7] = 0
Model.cost[6,1] = 0
#DOMINGO
Model.cost[7,1] = 0
Model.cost[7,2] = 0

Model.x = Var(Model.N, domain=PositiveIntegers)

Model.obj = Objective(expr=sum(Model.x[N] for N in Model.N), sense=minimize)

def restriccionDia(Model, c):
    return sum(Model.x[c]*Model.cost[t,c] for t in Model.N)
def restriccionGeneral(Model):
    i=0
    for c in Model.N:
        if value(restriccionDia(Model, c)) > dias[c-1]:
            i = i+1
    return(i==7)
Model.res1 = Constraint(rule = restriccionGeneral)
SolverFactory("glpk").solve(Model)

Model.display()