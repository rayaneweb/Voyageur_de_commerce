import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from controlleur.controller import Controller
from model.ville import Ville
from model.genetic_algorithm import GeneticAlgorithm


def dessiner(canvas, villes, chemin=None, couleur_route="blue"):
    canvas.delete("all")
    if chemin:
        for i in range(len(chemin)):
            v1 = chemin[i]
            v2 = chemin[(i + 1) % len(chemin)]
            canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill=couleur_route, width=2)
    for v in villes:
        r = 5
        canvas.create_oval(
            v.x - r, v.y - r, v.x + r, v.y + r, fill="red", outline="white"
        )
        canvas.create_text(
            v.x + 9, v.y - 9, text=str(v.num), fill="black", font=("Arial", 7)
        )


# Fenêtre principale 
root = tk.Tk()
root.title("Voyageur de Commerce — Algorithme Génétique")
root.geometry("700x580")
root.resizable(True, True)

#  Panneau de contrôle ───────────────────────────────────────────────────────
panel = tk.Frame(root, bg="#FFB5C0", pady=8)
panel.pack(fill="x", padx=10, pady=(10, 0))

tk.Label(panel, text="Nombre de villes:").pack(side="left", padx=(0, 4))
var_n = tk.StringVar(value="10")
tk.Spinbox(panel,  from_=0 ,to=1000000, textvariable=var_n, width=5).pack(
    side="left", padx=(0, 15)
)

tk.Label(panel, text="Population :").pack(side="left", padx=(0, 4))
var_pop = tk.StringVar(value="50")
tk.Spinbox(panel, from_=0, to=1000000, textvariable=var_pop, width=6).pack(
    side="left", padx=(0, 15)
)

btn_generer = tk.Button(
    panel,
    text="Générer",
    bg="#002FFF",
    fg="white",
    padx=10,
    command=lambda: controller.generer_villes(
        int(var_n.get()), canvas.winfo_width() or 600, canvas.winfo_height() or 450
    ),
)
btn_generer.pack(side="left", padx=(0, 8))

btn_lancer = tk.Button(
    panel,
    text="Lancer",
    bg="#18D127",
    fg="white",
    padx=10,
    command=lambda: controller.lancer(int(var_pop.get())),
)
btn_lancer.pack(side="left", padx=(0, 8))

btn_reset = tk.Button(
    panel,
    text="Reset",
    bg="#f44336",
    fg="white",
    padx=10,
    command=lambda: controller.reset(),
)
btn_reset.pack(side="left")

# ── Canvas ────────────────────────────────────────────────────────────────────
canvas = tk.Canvas(root, bg="WHITE")
canvas.pack(fill="both", expand=True, padx=10, pady=8)

# ── Barre d'état ──────────────────────────────────────────────────────────────
status_bar = tk.Frame(root, bg="#f0f0f0")
status_bar.pack(fill="x", padx=10, pady=(0, 8))

lbl_gen = tk.Label(
    status_bar, text="Génération : —", bg="#f0f0f0", width=20, anchor="w"
)
lbl_gen.pack(side="left")

lbl_dist = tk.Label(status_bar, text="Distance : —", bg="#f0f0f0")
lbl_dist.pack(side="left")

progress = ttk.Progressbar(status_bar, orient="horizontal", length=100)
progress.pack(side="left", padx=10)

lbl_status = tk.Label(status_bar, text="Prêt", bg="#f0f0f0", fg="gray", anchor="e")
lbl_status.pack(side="right")


# ── Objet vue exposé au contrôleur ────────────────────────────────────────────
class View:
    def __init__(self):
        self.root = root
        self.canvas = canvas
        self.lbl_gen = lbl_gen
        self.lbl_dist = lbl_dist
        self.lbl_status = lbl_status
        self.progress = progress

    def dessiner(self, villes, chemin=None, couleur_route="blue"):
        dessiner(canvas, villes, chemin, couleur_route)

    def reset_stats(self):
        lbl_gen.config(text="Génération : —")
        lbl_dist.config(text="Distance : —")
        lbl_status.config(text="Prêt")
        progress["value"] = 0

    def set_boutons(self, actif):
        state = "normal" if actif else "disabled"
        btn_generer.config(state=state)
        btn_lancer.config(state=state)
        btn_reset.config(state=state)


view = View()
controller = Controller(view)
