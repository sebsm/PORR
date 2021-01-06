import copy
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from scipy.spatial import distance as dist

class GlowwormSwarmOptimization:
    
    # Values example
    # dims = 10
    # num_worms = 20
    # nturns = 100
    # lower_bound = 70
    # influence_factor = 30
    # max_jitter = .2
    
    def __init__(self, dims, num_worms, nturns, lower_bound, influence_factor, max_jitter, function):
        self.dims = dims # const value
        self.num_worms = num_worms # const value
        self.nturns = nturns # const value
        self.lower_bound = lower_bound # const value
        self.influence_factor = influence_factor # const value
        self.max_jitter = max_jitter # const value   
        self.Fun = function
        
    def init_gso(self):
        return np.random.rand(self.num_worms,2) * 10
    
    def fitness_function(self, xy_tuple):
        x = xy_tuple[0]/2
        y = xy_tuple[1]/2
        value = dist.euclidean(x, y)
        
        ret = self.Fun(1, value)
        return ret

    
    def get_score(self, pop):
        temp = [(self.fitness_function(tup)) for tup in pop]
        normal = [x + self.lower_bound for x in temp]
        return [x / self.influence_factor for x in normal]
    
    def influence_matrix(self, pop, score):
        graph = np.array([np.zeros(self.num_worms)] * self.num_worms)

        for i in range(self.num_worms):
            for j in range(self.num_worms):
                if i == j:
                    graph[i][j] = 0
                elif dist.euclidean(pop[i], pop[j]) <= score[j]:
                    graph[i][j] = dist.euclidean(pop[i], pop[j])
                else:
                    continue
        return graph
    
    def next_turn(self, pop, score, im):
        n_turn = copy.deepcopy(pop)
        
        for i in range(self.num_worms):
            x_move = 0
            y_move = 0
            for j in range(self.num_worms):
                percent_move = 1 - (im[i][j] / score[j]) if im[i][j] != 0 else 0
                x_move += (pop[j][0] - pop[i][0]) * percent_move / 10 if score[i] < score[j] else 0
                y_move += (pop[j][1] - pop[i][1]) * percent_move / 10 if score[i] < score[j] else 0
            jitter_x = self.max_jitter * np.random.rand() * np.random.randint(-1,2)
            jitter_y = self.max_jitter * np.random.rand() * np.random.randint(-1,2)
            n_turn[i][0] += x_move + jitter_x
            n_turn[i][1] += y_move + jitter_y
            
            n_turn[i][0] = self.keep_in_bounds(n_turn[i][0], self.dims)
            n_turn[i][1] = self.keep_in_bounds(n_turn[i][1], self.dims)
            
        return n_turn
    
    def keep_in_bounds(self, x, dims):
        if x < 0:
            return 0
        elif x > dims:
            return dims
        else:
            return x
    
    def Run(self):
        pop = self.init_gso()
        value_dict = {}
        
        for each in range(self.nturns):
            score = self.get_score(pop)
            
            im = self.influence_matrix(pop,score)
            pop = copy.deepcopy(self.next_turn(pop,score,im))
            value_dict[each] = sorted(score)[0]
            
        return pop, value_dict