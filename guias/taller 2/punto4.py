# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 07:01:59 2020

@author: Daniel Serrano Juan Pablo Cano
"""

from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

numLosas = 20

p = RangeSet(1, numLosas)

Model = ConcreteModel()

Model.losas = Var(p, domain=Binary)

Model.obj = Objective(expr=sum(Model.losas[i] for i in p), sense=minimize)

def least_one_1(model):
    return model.losas[1] + model.losas[5] >= 1

def least_one_2(model):
    return model.losas[2] + model.losas[3] + model.losas[6] + model.losas[7] >= 1

def least_one_3(model):
    return model.losas[5] + model.losas[9] >= 1

def least_one_4(model):
    return model.losas[9] + model.losas[10] + model.losas[13] + model.losas[14] >= 1

def least_one_5(model):
    return model.losas[13] + model.losas[17] >= 1

def least_one_6(model):
    return model.losas[10] + model.losas[11] + model.losas[14] + model.losas[15] >= 1

def least_one_7(model):
    return model.losas[8] + model.losas[16] + model.losas[16] + model.losas[20] + model.losas[19] >= 1

Model.res1 = Constraint(rule=least_one_1)
Model.res2 = Constraint(rule=least_one_2)
Model.res3 = Constraint(rule=least_one_3)
Model.res4 = Constraint(rule=least_one_4)
Model.res5 = Constraint(rule=least_one_5)
Model.res6 = Constraint(rule=least_one_6)
Model.res7 = Constraint(rule=least_one_7)

SolverFactory('glpk').solve(Model)

Model.display()
