import time
import numpy as np
import pymp
import math

from gso import glowworm_swarm_optimization
from termcolor import colored

### ZMIENNE KONFIGURACYJNE ###
DIMS_LIST = [2, 10, 20, 50, 100]
WORMS = 30
NTURNS = 100
DIMS_LIM = [-30,30]
STEP_SIZE = 1
### ---------------------  s###

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
    for i in range(0,d-1):
        fc = fc + (100.0*((sol[i+1]-(sol[i]**2.0))**2.0) + ((1-sol[i])**2.0))
    return fc

glob_time = time.time()
with pymp.Parallel(8) as p:
    for dims in p.iterate(DIMS_LIST):
        print ('#################')
        print (colored('Rozmiar populacji: ' + str(WORMS), 'green'))
        print(colored('Zadanie #1', attrs=['bold']))
        
        start_time = time.time()
        result = glowworm_swarm_optimization(agents_number=WORMS, dim=dims, func_obj=Function1, epochs=NTURNS, step_size=STEP_SIZE, random_step=True, dims_lim=DIMS_LIM)
        min_key = min(result, key=result.get)

        print('Wynnik dla zadania #1: ', result[min_key])
        
        print('Czas wykonania: %s sek. ' % colored((time.time() - start_time), attrs=['bold']))
        print('------------------')
        print(colored('Zadanie #2', attrs=['bold']))
        
        start_time = time.time()
        result = glowworm_swarm_optimization(agents_number=WORMS, dim=dims, func_obj=Function2, epochs=NTURNS, step_size=STEP_SIZE, random_step=True, dims_lim=DIMS_LIM)
        
        min_key = min(result, key=result.get)
        print('Wynnik dla zadania #2: ', result[min_key])    
        
        print('Czas wykonania: %s sek. ' % colored((time.time() - start_time), attrs=['bold']))
        print ('#################')
        print('')
        
print(f'Glob time: {time.time() - glob_time}')