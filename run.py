from fa_1 import *

def Fun(d, sol):
    val = 0.0
    for i in range(d):
        val = val + sol[i] * sol[i]
    return val


def Function1():
    
    return val

def Function2():
    return val


Algorithm = FireflyAlgorithm(10, 20, 2, 0.5, 0.2, 1.0, -40.0, 40.0, Fun)


Best = Algorithm.Run()
Move = Algorithm
print(Best)
print(Move)