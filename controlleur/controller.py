import sys, os, threading, time, random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from model.ville import Ville
from model.genetic_algorithm import GeneticAlgorithm
from model.individu import Individu

ROUTE_RUN = "#D4788A"
ROUTE_DONE = "#9B6B8A"

NB_GENERATIONS = 300


class Controller:
    def __init__(self, view):
        self.view = view
        self.villes = []
        self._stop_flag = False

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
        self._stop_flag = False
        self.view.set_boutons(False)
        self.view.lbl_status.config(text="en cours…", fg=ROUTE_RUN)

        def _make_individu(chemin):
            e = Individu(chemin)
            e.chemin = chemin.copy()
            e.distance_totale = e.calculer_distance_totale()
            e.fitness = 1 / e.distance_totale if e.distance_totale > 0 else 0
            return e

        def run():
            algo = GeneticAlgorithm(self.villes, taille_pop)

            for gen in range(NB_GENERATIONS):
                if self._stop_flag:
                    break

                if len(algo.population.liste) < 2:
                    break

                # Élitisme : conserver le meilleur individu
                algo.population.order_by_fitness()
                elite = algo.population.liste[-1]
                enfants = [_make_individu(elite.chemin)]

                # Génération des enfants — opérateurs délégués à GeneticAlgorithm
                while len(enfants) < taille_pop:
                    p1 = algo.selection_tournoi()
                    p2 = algo.selection_tournoi()
                    ch = algo.crossover(p1, p2)
                    ch = algo.mutation(ch)
                    enfants.append(_make_individu(ch))

                algo.population.liste = enfants
                best = max(enfants, key=lambda ind: ind.fitness)

                def update(g=gen, b=best):
                    self.view.dessiner(self.villes, b.chemin, ROUTE_RUN)
                    self.view.lbl_gen.config(text=f"{g + 1} / {NB_GENERATIONS}")
                    self.view.lbl_dist.config(text=f"{b.distance_totale:.1f}")
                    self.view.update_courbe(b.distance_totale)
                    self.view.progress["value"] = (g + 1) / NB_GENERATIONS * 100

                self.view.root.after(0, update)
                time.sleep(0.01)

            best = max(algo.population.liste, key=lambda ind: ind.fitness)

            def finish(b=best, g=gen):
                self.view.dessiner(self.villes, b.chemin, ROUTE_DONE)
                self.view.lbl_gen.config(
                    text=f"{min(NB_GENERATIONS, g + 1)} / {NB_GENERATIONS}"
                )
                self.view.lbl_dist.config(text=f"{b.distance_totale:.1f}")
                self.view.lbl_status.config(
                    text="interrompu ✗" if self._stop_flag else "terminé ✓",
                    fg="#C49080" if self._stop_flag else "#9B6B8A",
                )
                if not self._stop_flag:
                    self.view.progress["value"] = 100
                self.view.set_boutons(True)

            self.view.root.after(0, finish)

        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        self._stop_flag = True

    def reset(self):
        self._stop_flag = True
        self.villes = []
        self.view.canvas.delete("all")
        self.view.reset_stats()
        self.view.set_boutons(True)
