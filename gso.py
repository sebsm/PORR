import numpy as np


def glowworm_swarm_optimization(
    agents_number, dim, func_obj, epochs, step_size, dims_lim=[-1, 1], random_step=False, print_per_epoche=False
):

    assert len(dims_lim) == 2
    assert type(agents_number) == int
    assert type(dim) == int

    """
	PARAMETRY
	"""
    # RANGE
    range_init = 30.0
    range_min = 5
    range_boundary = 30.0

    # LUCIFERIN
    luciferin_init = 0
    luciferin_decay = 0.4
    luciferin_enhancement = 0.6

    # POSITION
    # step_size = 0.1

    # Neighbors
    k_neigh = 10
    beta = 0.2

    """
    INICJALIZACJA AGENTA
	"""

    # random initiation
    _min = dims_lim[0]
    _max = dims_lim[1]
    glowworms = np.random.uniform(_min, _max, [agents_number, dim])

    # distances
    distances = np.zeros([agents_number, agents_number])

    # luciferin
    luciferins = np.zeros(agents_number)
    luciferins += luciferin_init

    # range of sigth
    ranges = np.zeros(agents_number)
    ranges += range_init

    """
	FAZA MODYFIKACJI LUCEFYRYNY
	"""

    def luciferin_update(last_luciferin, fitness):
        l = (1 - luciferin_decay) * last_luciferin + luciferin_enhancement * fitness
        return l

    """
	FAZA RUCHU
	"""

    def find_neighbors(glowworm_index):

        i = glowworm_index
        neighbors_index = []

        # look for all the neighbors in a triangle distance matrix
        for k in range(agents_number):

            dist = get_distance(i, k)
            # if it is in it's range of sigth and it's brightness is higher
            if dist != 0 and dist <= ranges[i] and luciferins[i] < luciferins[k]:
                neighbors_index.append(k)

        return neighbors_index

    def follow(glowworm_index, neighbors_index):

        # stan luceferyny - li
        li = luciferins[glowworm_index]

        # luceferyna wszystkich sasiadow (lj or lk)
        sum_lk = sum([luciferins[k] for k in neighbors_index])

        # oblicznie prawdopodobieństwa dla kazdego sasiada ktorego agent nasladuje
        probs = np.array([luciferins[j] - li for j in neighbors_index])
        probs /= sum_lk - (len(probs) * li)

        # calc prob range
        acc = 0
        wheel = []
        for prob in probs:
            acc += prob
            wheel.append(acc)

        wheel[-1] = 1

        # losowo wybrana wartosc
        rand_val = np.random.random()
        following = None
        for i, value in enumerate(wheel):
            if rand_val <= value:
                following = i

        return neighbors_index[following]

    def position_update(i, j):
        glowworm = glowworms[i]

        toward = None
        if type(j) == int:
            toward = glowworms[j]
        elif type(j) == type(np.array([])):
            toward = j

        norm = np.linalg.norm(toward - glowworm)

        if norm == 0 or np.isnan(norm):
            norm = step_size

        # if dynamic_step_size:
        # 	step_size =

        if random_step:
            step = step_size * np.random.random()
            if step < 0.1:
                step = 0.1
        else:
            step = step_size

        new_position = glowworm + step_size * (toward - glowworm) / norm

        for k in range(agents_number):

            if max(k, i) == k:
                distances[i][k] = np.linalg.norm(new_position - glowworms[k])
            elif max(k, i) == i:
                distances[k][i] = np.linalg.norm(new_position - glowworms[k])

        return new_position

    def range_update(glowworm_index, neighbors):
        return min(
            range_min,
            max(0, ranges[glowworm_index] + (beta * (k_neigh - len(neighbors)))),
        )

    def virtual_glowworm(glowworm_index):
        glowworm = glowworms[glowworm_index]
        virtual = np.random.uniform(_min, _max, [1, dim])
        virtual = glowworm + ranges[glowworm_index] * (
            virtual - glowworm
        ) / np.linalg.norm(virtual - glowworm)
        return virtual

    def get_distance(i, j):
        if max(j, i) == j:
            return distances[i][j]
        elif max(j, i) == i:
            return distances[j][i]
        else:
            return 0.0

    """
	WYKONANIE ALGORYTMU
	"""

    best_fitness_history = []
    algorithm_history = {}

    # initialize distance matrix (over main diagonal, only)
    for i in range(agents_number):
        for j in range(agents_number):
            if max(i, j) == j:
                distances[i][j] = np.linalg.norm(glowworms[i] - glowworms[j])
            elif max(i, j) == i:
                distances[j][i] = np.linalg.norm(glowworms[i] - glowworms[j])

    for epoch in range(epochs):
        epoch_fitness_history = []
        # update all glowworms luciferin
        for i in range(agents_number):

            li = luciferins[i]
            fitness = func_obj(dim, glowworms[i])
            luciferins[i] = luciferin_update(li, fitness)
            epoch_fitness_history.append(fitness)

        best_fitness_history.append(max(epoch_fitness_history))

        # movement phase
        for i in range(agents_number):

            # find best neighbors
            neighbors = find_neighbors(i)

            if len(neighbors) > 0:

                toward_index = follow(i, neighbors)
                glowworms[i] = position_update(i, toward_index)

            else:

                virtual = virtual_glowworm(i)
                glowworms[i] = position_update(i, virtual)

            ranges[i] = range_update(i, neighbors)
        algorithm_history[epoch] = best_fitness_history[-1]
        if print_per_epoche:
            print(epoch, "> best:", best_fitness_history[-1])
        
    return algorithm_history
        

