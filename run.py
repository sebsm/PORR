from fa_1 import *

def Fun(d, sol):
    val = 0.0
    for i in range(d):
        val = val + sol[i] * sol[i]
    return val


def Function1(d):
    fc = 0.0    
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

def Function2():
    return val


Algorithm = FireflyAlgorithm(10, 20, 2, 0.5, 0.2, 1.0, -40.0, 40.0, Fun)


Best = Algorithm.Run()
Move = Algorithm
print(Best)
print(Move)