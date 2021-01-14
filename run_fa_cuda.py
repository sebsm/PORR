import math
import numpy as np
import time

#from fa_1_seq import *
from termcolor import colored
from numba import jit, njit, prange

import random
import math


class FireflyAlgorithm():

    def __init__(self, d, n, nfe, alpha, betamin, gamma, LB, UB, function):
        self.d = d  # rozmiar wymiarów
        self.n = n  # rozmiar populacji
        self.nfe = nfe  # liczba iteracji
        self.alpha = alpha  # parametr alpha
        self.betamin = betamin  # parametr beta
        self.gamma = gamma  # parametr gamma

        # sortowanie świetlików w zależności od funkcji dopasowania
        self.Index = [0] * self.n
        self.Fireflies = [[0 for i in range(self.d)]
                          for j in range(self.n)]  # init świetlików
        self.Fireflies_tmp = [[0 for i in range(self.d)] for j in range(
            self.n)]  # tymczasowa populacja
        self.Fitness = [0.0] * self.n  # wartosci dopasowania
        self.I = [0.0] * self.n  # intensywność światła
        self.nbest = [0.0] * self.n  # najlepsze znalezione rozwiązanie
        self.LB = LB  # dolne ograniczenie
        self.UB = UB  # górne ograniczenie
        self.fbest = None  # najlepszy
        self.evaluations = 0
        self.Fun = function
        
    def init_ffa(self):
        for i in range(self.n):
            for j in range(self.d):
                self.Fireflies[i][j] = random.uniform(
                    0, 1) * (self.UB - self.LB) + self.LB
            self.Fitness[i] = 1.0  # dopasowanie
            self.I[i] = self.Fitness[i]

    def alpha_new(self, a):
        delta = 1.0 - math.pow((math.pow(10.0, -4.0) / 0.9), 1.0 / float(a))
        return (1 - delta) * self.alpha

    def sort_ffa(self):  # sortowanie bąbelkowe
        for i in range(self.n):
            self.Index[i] = i

        for i in range(0, (self.n - 1)):
            j = i + 1
            for j in range(j, self.n):
                if (self.I[i] > self.I[j]):
                    # wymiana atrakcyjności
                    self.I[i], self.I[j] = self.I[j], self.I[i]
                    
                    # wymiana dopasowania
                    self.Fitness[i], self.Fitness[j] = self.Fitness[j], self.Fitness[i]
                    
                    # wymiana indexów
                    self.Index[i], self.Index[j] = self.Index[j], self.Index[i]

    def replace_ffa(self):  # wymiana starej populacji w powiązaniu z nowymi wartosciami Indexów
        # skopiowanie oryginalnej populacji do tymczasowej
        for i in range(self.n):
            for j in range(self.d):
                self.Fireflies_tmp[i][j] = self.Fireflies[i][j]

        # wymiana populacji w nawiązaniu do algorytmu ewolucyjnego
        for i in range(self.n):
            for j in range(self.d):
                self.Fireflies[i][j] = self.Fireflies_tmp[self.Index[i]][j]

    
    def FindLimits(self, k):
        for i in range(self.d):
            if self.Fireflies[k][i] < self.LB:
                self.Fireflies[k][i] = self.LB
            if self.Fireflies[k][i] > self.UB:
                self.Fireflies[k][i] = self.UB

    def move_ffa(self):
        for i in range(self.n):
            scale = abs(self.UB - self.LB)
            for j in range(self.n):
                r = 0.0
                for k in range(self.d):
                    r += (self.Fireflies[i][k] - self.Fireflies[j][k]) * \
                        (self.Fireflies[i][k] - self.Fireflies[j][k])
                r = math.sqrt(r)
                if self.I[i] > self.I[j]:  # jaśniejsze i bardziej atrakcyjne
                    beta0 = 1.0
                    beta = (beta0 - self.betamin) * \
                        math.exp(-self.gamma * math.pow(r, 2.0)) + self.betamin
                    for k in range(self.d):
                        r = random.uniform(0, 1)
                        tmpf = self.alpha * (r - 0.5) * scale
                        self.Fireflies[i][k] = self.Fireflies[i][
                            k] * (1.0 - beta) + self.Fireflies_tmp[j][k] * beta + tmpf
            self.FindLimits(i)

    #@jit(parallel=True)
    def Run(self):
        self.init_ffa()
        
        self.iteration_dict = {}
        
        while self.evaluations < self.nfe:

            # opcjonalna redukcja alphy
            self.alpha = self.alpha_new(self.nfe/self.n)

            # wyliczenie nowych rozwiązań
            #for i in prange(self.n):
            for i in range(self.n):
                self.Fitness[i] = self.Fun(self.d, self.Fireflies[i])
                self.I[i] = self.Fitness[i]
                
            self.evaluations = self.evaluations + 1
            
            # ocena świetlików pod kątem jasności
            self.sort_ffa()
            # wymiana starej populacji
            self.replace_ffa()
            # znajdź najlepszego
            self.fbest = self.I[0]
            # przeniesienie świetlików do lepszych pozycji
            self.move_ffa()
            #print(self.Fireflies)
            
            self.iteration_dict[self.evaluations] = self.fbest
            
        return self.fbest, self.iteration_dict






def Fun(d, sol):
    val = 0.0
    for i in range(d):
        val = val + sol[i] * sol[i]
    return val

@jit(parallel=True)
def Function1(d, sol):
    fc_a = 0.0
    fc_b = 0.0
    sol = np.array(sol)
    for i in prange(1,d,1):
        fc_a = fc_a +(sol[i]**2.0)
        fc_b = fc_b * math.cos(sol[i]/i)

    fc_final = 1/40 * fc_a + 1 - fc_b
    return fc_final

@jit(parallel=True)
def Function2(d,sol):
    fc = 0.0  
    sol = np.array(sol)
    for i in prange(1,d-1,1):
        fc = fc + (100.0*((sol[i+1]-(sol[i]**2.0))**2.0) + ((1-sol[i])**2.0))
    return fc

### Opis parametrów ###

# self.d = d  # rozmiar wymiarów
# self.n = n  # rozmiar populacji
# self.nfe = nfe  # liczba iteracji
# self.alpha = alpha  # parametr alpha
# self.betamin = betamin  # parametr beta
# self.gamma = gamma  # parametr gamma

# # sortowanie świetlików w zależności od funkcji dopasowania
# self.Index = [0] * self.n
# self.Fireflies = [[0 for i in range(self.d)]
#                     for j in range(self.n)]  # init świetlików
# self.Fireflies_tmp = [[0 for i in range(self.d)] for j in range(
#     self.n)]  # tymczasowa populacja
# self.Fitness = [0.0] * self.n  # wartosci dopasowania
# self.I = [0.0] * self.n  # intensywność światła
# self.nbest = [0.0] * self.n  # najlepsze znalezione rozwiązanie
# self.LB = LB  # dolne ograniczenie
# self.UB = UB  # górne ograniczenie
# self.fbest = None  # najlepszy świetlik
# self.evaluations = 0 # liczba wykonania obliczenia wartości
# self.Fun = function # funkcja podlegająca rozwiązaniu


n_list = [2, 10, 20, 50, 100]
glob_time = time.time()
for n in [10]:
    
    Algorithm1 = FireflyAlgorithm(n, 100, 100, 1.0, 1.0, 0.01, -40.0, 40.0, Function1)
    Algorithm2 = FireflyAlgorithm(n, 100, 100, 1.0, 1.0, 0.01, -40.0, 40.0, Function2)
    
    print ('#################')
    print (colored('Rozmiar populacji: ' + str(n), 'green'))
    print(colored('Zadanie #1', attrs=['bold']))
    
    start_time = time.time()
    Best, iter_dict = Algorithm1.Run()
    
    print('Wynnik dla zadania #1: ', Best)
    
    print('Czas wykonania: %s sek. ' % colored((time.time() - start_time), attrs=['bold']))    
    print('------------------')
    print(colored('Zadanie #2', attrs=['bold']))
    Best2, iter_dict2 = Algorithm2.Run()
    
    print('Wynnik dla zadania #2: ', Best2)
    
    print('Czas wykonania: %s sek. ' % colored((time.time() - start_time), attrs=['bold']))
    print ('#################')
    print('')

# import matplotlib.pyplot as plt
# plt.plot(iter_dict.keys(), iter_dict.values())
# plt.xlabel('Liczba iteracji')
# plt.ylabel('Wartość funkcji celu')
# plt.show()

# plt.plot(iter_dict2.keys(), iter_dict2.values())
# plt.xlabel('Liczba iteracji')
# plt.ylabel('Wartość funkcji celu')
# plt.show()
# print(f'Glob time: {time.time() - glob_time}')