import time
import numpy as np
import pymp
import math

from gso_1_seq import GlowwormSwarmOptimization
from termcolor import colored

dims = 40
num_worms = [2, 10, 20, 50, 100]
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

def Function2(d,sol):
    fc = 0.0
    sol = np.array(sol)
    for i in range(1,d,1):
        fc = fc + (100.0*((sol[i+1]-(sol[i]**2.0))**2.0) + ((1-sol[i])**2.0))
    return fc


n_list = [2, 10, 20, 50, 100]

glob_time = time.time()
with pymp.Parallel(8) as p:
    for num_worms in p.iterate(n_list):
        
        Algorithm1 = GlowwormSwarmOptimization(dims, num_worms, nturns, lower_bound, influence_factor, max_jitter, Function1)
        Algorithm2 = GlowwormSwarmOptimization(dims, num_worms, nturns, lower_bound, influence_factor, max_jitter, Function2)

        p.print('#################')
        p.print(colored('Rozmiar populacji: ' + str(num_worms), 'green'))
        p.print(colored('Zadanie #1', attrs=['bold']))
        
        start_time = time.time()
        best = Algorithm1.Run()
        
        p.print('Czas wykonania: %s sek. ' % colored((time.time() - start_time), attrs=['bold']))    
        p.print('------------------')
        p.print(colored('Zadanie #2', attrs=['bold']))
        best = Algorithm2.Run()
        
        p.print('Czas wykonania: %s sek. ' % colored((time.time() - start_time), attrs=['bold']))
        p.print('#################')
        p.print('')
        
print(f'Glob time: {time.time() - glob_time}')