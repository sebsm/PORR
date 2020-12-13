import time

from gso_1_seq import GlowwormSwarmOptimization

dims = 10
num_worms = 7
nturns = 100
lower_bound = 70
influence_factor = 30
max_jitter = .2

Algorithm1 = GlowwormSwarmOptimization(dims, num_worms, nturns, lower_bound, influence_factor, max_jitter)
start_time = time.time()
Algorithm1.Run()
print('End time is: ', time.time() - start_time)