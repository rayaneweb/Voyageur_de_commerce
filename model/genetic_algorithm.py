from model.population import Population, Individu
import random


class GeneticAlgorithm:
    def __init__(self, villes, taille_population):
        self.taille_population = taille_population
        self.population = Population(villes, taille_population)

    def selection_tournoi(self, k=3):
        """Sélection par tournoi pour plus de diversité"""
        candidats = random.sample(self.population.liste, k)
        return max(candidats, key=lambda ind: ind.fitness)

    def crossover(self, parent1, parent2):
        """Order Crossover (OX) — standard pour le TSP"""
        n = len(parent1.chemin)
        start, end = sorted(random.sample(range(n), 2))

        child_chemin = [None] * n
        child_chemin[start:end] = parent1.chemin[start:end]

        remaining = [v for v in parent2.chemin if v not in child_chemin]
        idx = 0
        for i in range(n):
            if child_chemin[i] is None:
                child_chemin[i] = remaining[idx]
                idx += 1
        return child_chemin

    def mutation(self, child_chemin):
        """Mutation par inversion de segment (plus efficace pour TSP)"""
        if random.random() < 0.2:
            i, j = sorted(random.sample(range(len(child_chemin)), 2))
            child_chemin[i:j] = reversed(child_chemin[i:j])
        return child_chemin

    def run(self):
        for _ in range(300):  # Plus d'itérations
            enfants = []

            # Élitisme : garder le meilleur
            self.population.order_by_fitness()
            enfants.append(self.population.liste[-1])

            while len(enfants) < self.taille_population:
                parent1 = self.selection_tournoi()
                parent2 = self.selection_tournoi()
                child_chemin = self.crossover(parent1, parent2)
                child_chemin = self.mutation(child_chemin)

                enfant = Individu(child_chemin)
                enfant.distance_totale = enfant.calculer_distance_totale()
                enfant.fitness = 1 / enfant.distance_totale
                enfants.append(enfant)

            self.population.liste = enfants  # Nouvelle génération complète

        return self.population.get_best()
