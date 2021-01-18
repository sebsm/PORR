from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
status = MPI.Status()

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
            comm.isend(i, dest = i, tag = 12) ##### MPI COMM SEND
            for j in range(self.d):
                comm.isend(j,dest = j, tag = 12) ##### MPI COMM SEND
                if True:
                    comm.irecv(source = i, tag = 12) ##### MPI COMM RECEIVE
                    comm.irecv(source = j, tag = 12) ##### MPI COMM RECEIVE
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
            comm.send(i,dest=i, tag = 11) ##### MPI COMM SEND
            j = i + 1
            for j in range(j, self.n):
                comm.send(j,dest=j, tag = 11) ##### MPI COMM SEND
                if (self.I[i] > self.I[j]):
                    
                    src_rank = status.Get_source() ##### MPI STATUS SOURCE
                    # wymiana atrakcyjności
                    if True:
                        comm.recv(source = i,  tag = 11) ##### MPI COMM RECEIVE   
                        comm.recv(source = j,  tag = 11) ##### MPI COMM RECEIVE
                        self.I[i], self.I[j] = self.I[j], self.I[i]
                        
                        # wymiana dopasowania
                        self.Fitness[i], self.Fitness[j] = self.Fitness[j], self.Fitness[i]
                        
                        # wymiana indexów
                        self.Index[i], self.Index[j] = self.Index[j], self.Index[i]
                    

    def replace_ffa(self):  # wymiana starej populacji w powiązaniu z nowymi wartosciami Indexów
        # skopiowanie oryginalnej populacji do tymczasowej
        for i in range(self.n):
            comm.send(i,dest=i, tag = 13) ##### MPI COMM SEND
            for j in range(self.d):
                comm.send(j,dest=j, tag = 13) ##### MPI COMM SEND
                if True:
                    comm.recv(source = i,  tag = 13) ##### MPI COMM RECEIVE   
                    comm.recv(source = j,  tag = 13) ##### MPI COMM RECEIVE
                    self.Fireflies_tmp[i][j] = self.Fireflies[i][j]

        # wymiana populacji w nawiązaniu do algorytmu ewolucyjnego
        for i in range(self.n):
            comm.send(i,dest=i, tag = 14) ##### MPI COMM SEND
            for j in range(self.d):
                comm.send(j,dest=j, tag = 14) ##### MPI COMM SEND
                if True:
                    comm.recv(source = i,  tag = 14) ##### MPI COMM RECEIVE   
                    comm.recv(source = j,  tag = 14) ##### MPI COMM RECEIVE
                    self.Fireflies[i][j] = self.Fireflies_tmp[self.Index[i]][j]

    def FindLimits(self, k):
        for i in range(self.d):
            temp = (i, k)
            comm.send(temp, dest = 5, tag = 15) ##### MPI COMM SEND
            if True:
                comm.recv(source = 5, tag = 15) ##### MPI COMM RECEIVE
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
                    comm.send(k, dest=k, tag = 16) ##### MPI COMM SEND
                    if True:
                        comm.recv(source = k, tag = 16) ##### MPI COMM RECEIVE
                        r += (self.Fireflies[i][k] - self.Fireflies[j][k]) * \
                            (self.Fireflies[i][k] - self.Fireflies[j][k])
                r = math.sqrt(r)
                if self.I[i] > self.I[j]:  # jaśniejsze i bardziej atrakcyjne
                    beta0 = 1.0
                    beta = (beta0 - self.betamin) * \
                        math.exp(-self.gamma * math.pow(r, 2.0)) + self.betamin
                    for k in range(self.d):
                        comm.send(k, dest = k , tag = 17)##### MPI COMM SEND
                        r = random.uniform(0, 1)
                        if True:
                            comm.recv(source = k, tag = 17)
                            tmpf = self.alpha * (r - 0.5) * scale
                            self.Fireflies[i][k] = self.Fireflies[i][
                                k] * (1.0 - beta) + self.Fireflies_tmp[j][k] * beta + tmpf
            comm.send(i, dist = i, tag = 18)
            self.FindLimits(i)
            comm.recv(source = i, tag = 18)

    def Run(self):
        self.init_ffa()
        
        self.iteration_dict = {}
        
        while self.evaluations < self.nfe:

            # opcjonalna redukcja alphy
            self.alpha = self.alpha_new(self.nfe/self.n)

            # wyliczenie nowych rozwiązań
            for i in range(self.n):
                comm.bcast(i, root = 0)
                self.Fitness[i] = self.Fun(self.d, self.Fireflies[i])
                self.I[i] = self.Fitness[i]
                comm.gather(i, root = 0)
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