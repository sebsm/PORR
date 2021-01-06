import pymp
import numpy as np
import time

start_time = time.time()
ex_array = pymp.shared.array((100,), dtype='uint8')
with pymp.Parallel(4) as p:
    for index in p.range(0, 100):
        ex_array[index] = 1
        p.print('Yay! {} done!'.format(index))
        
parallel_execution = time.time() - start_time


ln_start_time = time.time()
ex_array = np.zeros((100,), dtype='uint8')
for index in range(0, 100):
    ex_array[index] = 1
    print('Yay! {} done!'.format(index))
    
linear_execution = time.time() - ln_start_time

print('End time of parallel execution', parallel_execution)
print('End time of linear execution', linear_execution)