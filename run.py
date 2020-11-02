import numpy
from fa_1 import *
import math
import numpy as np

def Fun(d, sol):
    val = 0.0
    for i in range(d):
        val = val + sol[i] * sol[i]
    return val


def Function2(d,sol):
    fc = 0.0  
    sol = numpy.array(sol)
    #for i in range(d):   
        #fc = sum(100.0*math.pow((sol[1:]-math.pow(sol[:-1],2.0)),2.0) + math.pow((1-sol[:-1]),2.0))
    fc = sum(100.0*((sol[1:]-(sol[:-1]**2.0))**2.0) + ((1-sol[:-1])**2.0))
    return fc

def Function1(d, sol):
    fc = 0.0
    fc_a = 0.0
    fc_b = 0.0
    sol = numpy.array(sol)
    for i in range(d):
        fc_a = (sol[i]**2.0)
        fc_b = math.prod(math.cos(sol[i]/i))
        return fc_a, fc_b
    #fc = 1/40*sum(sol[:-1]**2.0) + 1 - math.prod(math.cos(sol[:-1]/sol.index(sol[:-1])))
    fc_final = 1/40 * fc_a + 1 - fc_b
    return fc_final




Algorithm = FireflyAlgorithm(10, 20, 2, 0.5, 0.2, 1.0, -40.0, 40.0, Function1)


Best = Algorithm.Run()
Move = Algorithm
print(Best)
print(Move)