#Daniel Serrano y Juan Pablo Cano
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

num_canciones = 8

# Canciones
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

# Rango de variables
p = RangeSet(1, num_canciones)

# Modelo
m = ConcreteModel()

m.ladoA = Var(p, domain=Binary)
m.ladoB = Var(p, domain=Binary)

# Funcioń objetivo
m.obj = Objective(expr=sum(m.ladoA[i]*canciones[i]['duracion'] for i in p) + sum(m.ladoB[i]*canciones[i]['duracion'] for i in p), sense=maximize)

def max_songsA(model):
    """
    Restricción que modela el número
    máximo de canciones por el lado A
    @param model: Modelo sobre el cual se
    va a aplicar la restricción
    @return: La resticción
    """
    a = sum(model.ladoA[i] * canciones[i]['duracion'] for i in p)
    return inequality(14, a, 16, False)

def max_songsB(model):
    """
    Restricción que modela el número
    máximo de canciones por el lado B
    @param model: Modelo sobre el cual se
    va a aplicar la restricción
    @return: la restricción
    """
    a = sum(model.ladoB[i] * canciones[i]['duracion'] for i in p)
    return inequality(14, a, 16, False)

def least_bluesA(model):
    """
    Restricción que modela el número
    exacto de canciones de blues en
    lado A
    @param model:
    @type model: Modelo sobre el cual se
    va a aplicar la restricción
    @return: La restricción
    """
    index = []
    for i in range(1, num_canciones+1):
        if 'blues' in  canciones[i]['genero']:
            index.append(i)

    return sum(model.ladoA[j] for j in index) == 2

def least_bluesB(model):
    """
    Restricción que modela el número
    exacto de canciones de blues en
    lado B
    @param model:
    @type model: Modelo sobre el cual se
    va a aplicar la restricción
    @return: La restricción
    """
    index = []
    for i in range(1, num_canciones+1):
        if 'blues' in  canciones[i]['genero']:
            index.append(i)

    return sum(model.ladoB[j] for j in index) == 2

def least_rockA(model):
    """
    Restricción que modela el número
    mínimo de canciones de rock en
    lado A
    @param model:
    @type model: Modelo sobre el cual se
    va a aplicar la restricción
    @return: La restricción
    """
    index = []
    for i in range(1, num_canciones + 1):
        if 'rock_n_roll' in canciones[i]['genero']:
            index.append(i)

    return sum(model.ladoA[j] for j in index) >= 3

m.res1 = Constraint(rule=max_songsA)
m.res2 = Constraint(rule=max_songsB)
m.res3 = Constraint(rule=least_bluesA)
m.res4 = Constraint(rule=least_bluesB)
m.res5 = Constraint(rule=least_rockA)

# Restricción condicional, en el lado A
# está la canción 1 o la 5
m.res6 = Constraint(expr=m.ladoA[1] + m.ladoA[5] <= 1)

# Restricción condicional, Si en el lado B
# está la canción 1, en el lado A sólo puede estar
# la canción 2 o 4.
m.res7 = Constraint(expr=m.ladoA[2] + m.ladoA[4] + m.ladoB[1] <= 2)

# Solver
SolverFactory('glpk').solve(m)

m.display()
