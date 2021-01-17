import math
#import pymp
import numpy as np
import time
import matplotlib.pyplot as plt
from gso import glowworm_swarm_optimization
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

### ZMIENNE KONFIGURACYJNE ###
DIMS_LIST = [2, 10, 20, 50, 100]
WORMS = 30
NTURNS = 100
DIMS_LIM = [-30,30]
STEP_SIZE = 1
### ---------------------  ###

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
for dims in [2]:
    spark, sc, logData = init_spark()

    df = sc.parallelize([1,2,3,4,5])
    df_all = df.collect()

    empty_1 = spark.sparkContext.emptyRDD()
    empty_2 = df = spark.sparkContext.parallelize([])
    
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