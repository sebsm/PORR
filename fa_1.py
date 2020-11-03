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
                    z = self.I[i]  # wymiana atrakcyjności
                    self.I[i] = self.I[j]
                    self.I[j] = z
                    z = self.Fitness[i]  # wymiana dopasowania
                    self.Fitness[i] = self.Fitness[j]
                    self.Fitness[j] = z
                    z = self.Index[i]  # wymiana indexów
                    self.Index[i] = self.Index[j]
                    self.Index[j] = z

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

    def Run(self):
        self.init_ffa()
        
        while self.evaluations < self.nfe:

            # opcjonalna redukcja alphy
            self.alpha = self.alpha_new(self.nfe/self.n)

            # wyliczenie nowych rozwiązań
            for i in range(self.n):
                self.Fitness[i] = self.Fun(self.d, self.Fireflies[i])
                self.evaluations = self.evaluations + 1
                self.I[i] = self.Fitness[i]
                
            # ocena świetlików pod kątem jasności
            self.sort_ffa()
            # wymiana starej populacji
            self.replace_ffa()
            # znajdź najlepszego
            self.fbest = self.I[0]
            # przeniesienie świetlików do lepszych pozycji
            self.move_ffa()
            #print(self.Fireflies)
        return self.fbest

