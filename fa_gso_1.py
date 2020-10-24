#importy

import math
import random
import sys

# dane 

n1=2   # liczba członków populacji
n2=10
n3=20
n4=50
n5=100

# definicja klasy
class FireflyAlgorith():

    def __init__(self, d, n, nfes, alpha, beta_min, gamma, LB, UB): 
        self.alpha = 1.0 # parametr losowości, gdzie 1 - bardzo losowy
        self.n = n
        self.beta_min = 1.0 # współczynnik atrakycjności
        self.gamma = 0.01 # wspólczynnik absorpcji światła/dążenia (?)
        self.theta = 0.95 # 
        self.d = d # liczba przestrzeni/wymiarów
        self.nfes = 100 # ilośc iteracji/ewaluacji

        # macierz świetlików
        self.Index = [0] * self.n
        print(self.Index)
        self.Fireflies = [0 for i in range(self.d)
            for j in range(self.n)]
        print(self.Fireflies)

        self.Fireflies_temporary = [[0 for i in range(self.n)] for j in range(self.n)]
        print(self.Fireflies_temporary)

        # dopasowanie
        self.Fitness = [0.0] * self.n
        self.I = [0.0] * self.n # intensywność światła 
        self.nbest = [0.0] * self.n
        self.LB = LB
        self.UB = UB
        self.fbest = None
        self.evaluations = 0
        self.Fun = function

    def init_ffa(self):
        for i in range(self.n):
            for j in range(self.d):
                self.Fireflies[i][j] = random.uniform(0,1) * (self.UB - self.LB) + self.LB
            self.Fitness[i] = 1.0
            self.I[i] = self.Fitness[i]
    
    def alpha_new(self, a):
        delta = 1.0 - math.pow((math.pow(10.0, -4.0) / 0.9), 1.0 / float(a))
        return (1 - delta) * self.alpha

    def sort_ffa(self): # sortowanie bąbelkowe
        for i in range(self.n):
            self.Index[i] = i
            
        for i in range(0, (self.n - 1)):
            j = i + 1
            for j in range(j, self.n):
                if (self.I[i]) > self.I[j]:
                    z = self.I[i]
                    self.I[i] = self.I[j]
                    self.I[j] = z
                    z = self.Fitness[i]
                    self.Fitness[i] = self.Fitness[j]
                    self.Fitness[j] = z
                    z = self.Index[i]
                    self.Index[i]=self.Index[j]
                    self.Index[j] = z

    def replace_ffa(self):
        for i in range(self.n):
            for j in range(self.d):
                self.Fireflies_temporary[i][j] = self.Fireflies[i][j]
    
        for i in range(self.m):
            for j in range(self.d):
                self.Fireflies[i][j] = self.Fireflies_temporary[self.Index[i]][j]
            
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
                    r += (self.Fireflies[i][k] - self.Fireflies[j][k] * (self.Fireflies[i][k] - self.Fireflies[j][k]))
                r = math.sqrt(r)
                if self.I[i] > self.I[j]:
                    beta0 = 1.0
                    beta = (beta0 - self.beta_min) * math.exp(-self.gamma * math.pow(r, 2.0)) + self.beta_min
                    for k in range(self.d):
                        r = random.uniform(0, 1)
                        tmpf = self.aplpha * (r - 0.5) * scale
                        self.Fireflies[i][k] = self.Fireflies[i][k] * (1.0 - beta) + self.Fireflies_temporary[j][k] * beta + tmpf
                self.FindLimits(i)

    def Run(self):
        self.init_ffa()


        while self.evaluations < self.nfes:

            self.alpha = self.alpha_new(self.nfes/self.n)


            for i in range(self.n):
                self.Fitness[i] = self.Fun(self.d, self.Fireflies[i])
                self.evaluations = self.evaluations + 1
                self.I[i] = self.Fitness[i]

            self.sort_ffa()

            self.replace_ffa()

            self.fbest = self.I[0]

            self.move_ffa()

        return self.fbest


FireflyAlgorith(10,2,100,1.0,1.0,0.01,-10,10)
print(sys.argv)
# Zadanie 1










# Zadanie 2



