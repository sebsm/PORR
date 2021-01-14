import math
#import pymp
import numpy as np
import time
import matplotlib.pyplot as plt
from fa_1_seq import *
from termcolor import colored

from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
install_requires=[
        'pyspark=={site.SPARK_VERSION}'
]

def init_spark():
        logFile = "README.md"  # Plik
        spark = SparkSession.builder.appName("PORR").getOrCreate()
        sc = spark.sparkContext
        logData = spark.read.text(logFile).cache()
        return spark, sc, logData

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
for n in [10]:
    spark, sc, logData = init_spark()

    df = sc.parallelize([1,2,3,4,5])
    df_all = df.collect()

    empty_1 = spark.sparkContext.emptyRDD()
    empty_2 = df = spark.sparkContext.parallelize([])
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
    spark.stop()


plt.plot(iter_dict.keys(), iter_dict.values())
plt.xlabel('Liczba iteracji')
plt.ylabel('Wartość funkcji celu')
plt.show()

plt.plot(iter_dict2.keys(), iter_dict2.values())
plt.xlabel('Liczba iteracji')
plt.ylabel('Wartość funkcji celu')
plt.show()
print(f'Glob time: {time.time() - glob_time}')