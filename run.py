import numpy
from fa_1 import *
import math
import numpy as np

def Fun(d, sol):
    val = 0.0
    for i in range(d):
        val = val + sol[i] * sol[i]
    return val


def Function1(d,sol):
    fc = 0.0  
    for i in range(d):
        sol = numpy.array(sol)
        #fc = sum(100.0*math.pow((sol[1:]-math.pow(sol[:-1],2.0)),2.0) + math.pow((1-sol[:-1]),2.0))
        fc = sum(100.0*((sol[1:]-(sol[:-1]**2.0))**2.0) + ((1-sol[:-1])**2.0))
    return fc



Algorithm = FireflyAlgorithm(10, 20, 2, 0.5, 0.2, 1.0, -40.0, 40.0, Function1)


Best = Algorithm.Run()
Move = Algorithm
print(Best)
print(Move)