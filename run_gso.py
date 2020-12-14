import time
import numpy as np
import math

from gso_1_seq import GlowwormSwarmOptimization

dims = 10
num_worms = 7
nturns = 100
lower_bound = 70
influence_factor = 30
max_jitter = .2

def Function1(d, sol):
    fc_a = 0.0
    fc_b = 0.0
    sol = np.array(sol)
    for i in range(1,d,1):
        fc_a = fc_a +(sol[i]**2.0)
        fc_b = fc_b * math.cos(sol[i]/i)

    fc_final = 1/40 * fc_a + 1 - fc_b
    return fc_final

# TODO - Validate it
def Function2(d,sol):
    fc = 0.0
    sol = np.array(sol)
    for i in range(1,d-1,1):
        fc = fc + (100.0*((sol[i+1]-(sol[i]**2.0))**2.0) + ((1-sol[i])**2.0))
    return fc

Algorithm1 = GlowwormSwarmOptimization(dims, num_worms, nturns, lower_bound, influence_factor, max_jitter)
start_time = time.time()
Algorithm1.Run()
print('End time is: ', time.time() - start_time)