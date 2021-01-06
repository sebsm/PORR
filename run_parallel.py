import math
import pymp
import numpy as np
import time

from fa_1_seq import *
from termcolor import colored

def Fun(d, sol):
    val = 0.0
    for i in range(d):
        val = val + sol[i] * sol[i]
    return val

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
    for i in range(1,d-1,1):
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
with pymp.Parallel(8) as p:
    for n in p.iterate(n_list):
        
        Algorithm1 = FireflyAlgorithm(4, n, 100, 1.0, 1.0, 0.01, -40.0, 40.0, Function1)
        Algorithm2 = FireflyAlgorithm(4, n, 100, 1.0, 1.0, 0.01, -40.0, 40.0, Function2)
        
        hashtags = ('#################\n')
        population_size = colored(f'Rozmiar populacji: {str(n)}', 'green')
        task_number = colored('Zadanie #1', attrs=['bold'])
        
        start_time = time.time()
        Best, iter_dict = Algorithm1.Run()
        
        p.print(hashtags)
        p.print(population_size)
        p.print(task_number)
        
        p.print('Czas wykonania: %s sek.\n' % colored((time.time() - start_time), attrs=['bold']))
        
        p.print('------------------\n')
        
        p.print(colored('Zadanie #2', attrs=['bold']))
        Best2, iter_dict = Algorithm2.Run()
        
        p.print('Czas wykonania: %s sek. \n' % colored((time.time() - start_time), attrs=['bold']))
        p.print ('#################')
    
print(f'Glob time: {time.time() - glob_time}')