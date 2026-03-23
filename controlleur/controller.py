import sys, os, random, threading, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from model.ville import Ville
from model.genetic_algorithm import GeneticAlgorithm
from model.individu import Individu

ROUTE_RUN = "#D4788A"
ROUTE_DONE = "#9B6B8A"


class Controller:
    def __init__(self, view):
        self.view = view
        self.villes = []

    def generer_villes(self, n, width, height):
        margin = 30
        self.villes = [
            Ville(
                i,
                random.randint(margin, width - margin),
                random.randint(margin, height - margin),
            )
            for i in range(n)
        ]
        self.view.dessiner(self.villes)
        self.view.reset_stats()

    def lancer(self, taille_pop):
        if not self.villes:
            return
        self.view.set_boutons(False)
        self.view.lbl_status.config(text="en cours…", fg="#D4788A")

        def run():
            algo = GeneticAlgorithm(self.villes, taille_pop)
            for gen in range(100):
                if len(algo.population.liste) < 2:
                    break
                enfants = []
                while len(enfants) < taille_pop:
                    p1, p2 = algo.selection()
                    ch = algo.mutation(algo.crossover(p1, p2))
                    e = Individu(ch)
                    e.chemin = ch.copy()
                    e.distance_totale = e.calculer_distance_totale()
                    e.fitness = 1 / e.distance_totale
                    enfants.append(e)
                algo.population.liste = enfants
                best = algo.population.get_best()

                def update(g=gen, b=best):
                    self.view.dessiner(self.villes, b.chemin, ROUTE_RUN)
                    self.view.lbl_gen.config(text=f"{g+1} / 100")
                    self.view.lbl_dist.config(text=f"{b.distance_totale:.1f}")
                    self.view.update_courbe(b.distance_totale)
                    self.view.progress["value"] = g + 1

                self.view.root.after(0, update)
                time.sleep(0.02)

            best = algo.population.get_best()

            def finish(b=best):
                self.view.dessiner(self.villes, b.chemin, ROUTE_DONE)
                self.view.lbl_gen.config(text=f"{min(100, gen+1)} / 100")
                self.view.lbl_dist.config(text=f"{b.distance_totale:.1f}")
                self.view.lbl_status.config(text="terminé ✓", fg="#9B6B8A")
                self.view.progress["value"] = min(100, gen + 1)
                self.view.set_boutons(True)

            self.view.root.after(0, finish)

        threading.Thread(target=run, daemon=True).start()

    def reset(self):
        self.villes = []
        self.view.canvas.delete("all")
        self.view.reset_stats()
        self.view.set_boutons(True)
