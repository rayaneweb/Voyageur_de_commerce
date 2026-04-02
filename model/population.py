from model.ville import *
from model.individu import Individu


class Population:
    def __init__(self, villes, taille_population):
        self.liste = []
        for i in range(taille_population):
            individu = Individu(villes)
            self.liste.append(individu)

    def get_best(self):
        best = self.liste[0]
        for individu in self.liste:
            if individu.fitness > best.fitness:
                best = individu
        return best

    def order_by_fitness(self):
        self.liste.sort(key=lambda individu: individu.fitness)

    def afficher_population(self):
        for individu in self.liste:
            print(individu)
