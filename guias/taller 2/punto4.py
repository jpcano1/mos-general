# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 07:01:59 2020

@author: Daniel Serrano Juan Pablo Cano
"""

from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

numLosas = 20

tubes = {
        (1, 5): 1,
        (2, 3): 1,
        (5, 1): 1,
        (6, 7): 1
        }

p = RangeSet(1, numLosas)
