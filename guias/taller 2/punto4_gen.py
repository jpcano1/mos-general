from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

numLosas = 20

losas_arcos = [
    (1, 5),

    (2, 3, 6, 7),

    (5, 9),

    (9, 10, 13, 14),

    (13, 17),

    (10, 11, 14, 15),

    (8, 12, 16, 20, 19)
]

p = RangeSet(1, numLosas)

m = ConcreteModel()

m.losas = Var(p, domain=Binary)

m.obj = Objective(expr=sum(m.losas[i] for i in p), sense=minimize)

def least_connection(model, i):
    index = []
    for tuple_ in losas_arcos:
        if i in tuple_:
            for j in tuple_:
                index.append(j)
            losas_arcos.remove(tuple_)
    print(index)
    return sum(model.losas[k] for k in index) >= 1

m.res1 = Constraint(p, rule=least_connection)

SolverFactory('glpk').solve(m)
m.display()