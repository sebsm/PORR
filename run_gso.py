import time
import numpy as np
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
    # sol = np.array(sol)
    # for i in range(1,d,1):
    fc_a = fc_a +(sol**2.0)
    fc_b = fc_b * math.cos(sol/1)
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
for num_worms in n_list:
    
    Algorithm1 = GlowwormSwarmOptimization(dims, num_worms, nturns, lower_bound, influence_factor, max_jitter, Function1)
    Algorithm2 = GlowwormSwarmOptimization(dims, num_worms, nturns, lower_bound, influence_factor, max_jitter, Function2)

    print ('#################')
    print (colored('Rozmiar populacji: ' + str(num_worms), 'green'))
    print(colored('Zadanie #1', attrs=['bold']))
    
    start_time = time.time()
    best, iter_dict = Algorithm1.Run()
    
    # print('Wynnik dla zadania #1: ', best)
    
    print('Czas wykonania: %s sek. ' % colored((time.time() - start_time), attrs=['bold']))    
    print('------------------')
    print(colored('Zadanie #2', attrs=['bold']))
    best, iter_dict2 = Algorithm2.Run()
    
    # print('Wynnik dla zadania #2: ', best)
    
    print('Czas wykonania: %s sek. ' % colored((time.time() - start_time), attrs=['bold']))
    print ('#################')
    print('')

import matplotlib.pyplot as plt
plt.plot(iter_dict.keys(), iter_dict.values())
plt.xlabel('Iteracja')
plt.ylabel('Zbieznosc')
plt.show()

plt.plot(iter_dict2.keys(), iter_dict2.values())
plt.xlabel('Iteracja')
plt.ylabel('Zbieznosc')
plt.show()
print(f'Glob time: {time.time() - glob_time}')