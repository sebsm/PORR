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