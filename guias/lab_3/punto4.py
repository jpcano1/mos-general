from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

num_canciones = 8

canciones = {
    1: {
        "genero": ["blues"],
        "duracion": 4
    },
    2: {
        "genero": ["rock_n_roll"],
        "duracion": 5
    },
    3: {
        "genero": ["blues"],
        "duracion": 3
    },
    4: {
        "genero": ["rock_n_roll"],
        "duracion": 2
    },
    5: {
        "genero": ["blues"],
        "duracion": 4
    },
    6: {
        "genero": ["rock_n_roll"],
        "duracion": 3
    },
    7: {
        "genero": [],
        "duracion": 5
    },
    8: {
        "genero": ["blues", 'rock_n_roll'],
        "duracion": 4
    },
}

p = RangeSet(1, num_canciones)

m = ConcreteModel()

m.ladoA = Var(p, domain=Binary)
m.ladoB = Var(p, domain=Binary)

m.obj = Objective(expr=sum(m.ladoA[i]*canciones[i]['duracion'] for i in p) + sum(m.ladoB[i]*canciones[i]['duracion'] for i in p), sense=maximize)

def max_songsA(model):
    a = sum(model.ladoA[i] * canciones[i]['duracion'] for i in p)
    return inequality(14, a, 16, False)

def max_songsB(model):
    a = sum(model.ladoB[i] * canciones[i]['duracion'] for i in p)
    return inequality(14, a, 16, False)

def least_bluesA(model):
    index = []
    for i in range(1, num_canciones+1):
        if 'blues' in  canciones[i]['genero']:
            index.append(i)

    return sum(model.ladoA[j] for j in index) == 2

def least_bluesB(model):
    index = []
    for i in range(1, num_canciones+1):
        if 'blues' in  canciones[i]['genero']:
            index.append(i)

    return sum(model.ladoB[j] for j in index) == 2

def least_rockA(model):
    index = []
    for i in range(1, num_canciones + 1):
        if 'rock_n_roll' in canciones[i]['genero']:
            index.append(i)

    return sum(model.ladoA[j] for j in index) >= 3

m.res_1 = Constraint(rule=max_songsA)
m.res_2 = Constraint(rule=max_songsB)
m.res_3 = Constraint(rule=least_bluesA)
m.res_4 = Constraint(rule=least_bluesB)
m.res_5 = Constraint(rule=least_rockA)
m.res6 = Constraint(expr=m.ladoA[1] + m.ladoA[5] <= 1)
m.res7 = Constraint(expr=m.ladoA[2] + m.ladoA[4] + m.ladoB[1] <= 2)

SolverFactory('glpk').solve(m)

m.display()