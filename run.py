import numpy
from fa_1 import *
import math
import numpy as np

def Fun(d, sol):
    val = 0.0
    for i in range(d):
        val = val + sol[i] * sol[i]
    return val

def Function1(d, sol):
    fc = 0.0
    fc_a = 0.0
    fc_b = 1.0
    sol = numpy.array(sol)
    for i in range(1,d,1):
        fc_a = fc_a +(sol[i-1]**2.0)
        fc_b = fc_b * math.cos(sol[i-1]/i)

    fc_final = 1/40 * fc_a + 1 - fc_b
    return fc_final


def Function2(d,sol):
    fc = 0.0  
    sol = numpy.array(sol)
    for i in range(1,d-1,1):
        fc = fc + (100.0*((sol[i+1]-(sol[i]**2.0))**2.0) + ((1-sol[i])**2.0))
        
    return fc


Algorithm = FireflyAlgorithm(10, 2, 10, 1.0, 1.0, 0.01, -40.0, 40.0, Function2)


Best = Algorithm.Run()
Move = Algorithm
print(Best)
print(Move)