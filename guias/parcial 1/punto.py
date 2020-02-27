from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

numPlayers = 7

players = {
    1: {
        'rol': ['A'],
        'control': 3,
        'disparo': 3,
        'rebotes': 1,
        'defensa': 3
    },
    2: {
        'rol': ['C'],
        'control': 2,
        'disparo': 1,
        'rebotes': 3,
        'defensa': 2
    },
    3: {
        'rol': ['A', 'D'],
        'control': 2,
        'disparo': 3,
        'rebotes': 2,
        'defensa': 2
    },
    4: {
        'rol': ['C', 'D'],
        'control': 1,
        'disparo': 3,
        'rebotes': 3,
        'defensa': 1
    },
    5: {
        'rol': ['A', 'D'],
        'control': 3,
        'disparo': 3,
        'rebotes': 3,
        'defensa': 3
    },
    6: {
        'rol': ['C', 'D'],
        'control': 3,
        'disparo': 1,
        'rebotes': 2,
        'defensa': 3
    },
    7: {
        'rol': ['A', 'D'],
        'control': 3,
        'disparo': 2,
        'rebotes': 2,
        'defensa': 1
    },
}
p = RangeSet(1, numPlayers)

m = ConcreteModel()

m.players = Var(p, domain=Binary)

m.obj = Objective(expr=sum(m.players[i]*players[i]['defensa'] for i in p), sense=maximize)

m.res1 = Constraint(expr=sum(m.players[i] for i in p) == 5)

def least_defense(model):
    index = []
    for i in range(1, numPlayers+1):
        if 'D' in players[i]['rol']:
            index.append(i)
    return sum(model.players[j] for j in index) >= 4

def least_attack(model):
    index = []
    for i in range(1, numPlayers + 1):
        if 'A' in players[i]['rol']:
            index.append(i)
    return sum(model.players[j] for j in index) >= 2

def least_center(model):
    index = []
    for i in range(1, numPlayers + 1):
        if 'C' in players[i]['rol']:
            index.append(i)
    return sum(model.players[j] for j in index) >= 1

m.res2 = Constraint(rule=least_defense)
m.res3 = Constraint(rule=least_attack)
m.res4 = Constraint(rule=least_center)
m.res5 = Constraint(expr=sum(m.players[i] * players[i]['control'] for i in p) / 5 >= 2)
m.res6 = Constraint(expr=sum(m.players[i] * players[i]['disparo'] for i in p) / 5 >= 2)
m.res7 = Constraint(expr=sum(m.players[i] * players[i]['rebotes'] for i in p) / 5 >= 2)
m.res8 = Constraint(expr=m.players[2] + m.players[3] == 1)

SolverFactory('glpk').solve(m)

m.display()