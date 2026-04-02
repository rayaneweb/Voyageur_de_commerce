import tkinter as tk
from tkinter import ttk
import sys, os, random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from controlleur.controller import Controller, NB_GENERATIONS
from model.ville import Ville
from model.genetic_algorithm import GeneticAlgorithm

# ── Palette ───────────────────────────────────────────────────────────────────
BG = "#FAF7F5"
TOPBAR_BG = "#F2E8E8"
PANEL_BG = "#FDF9F8"
CARD_BG = "#FFFFFF"
BORDER = "#EDD8D8"
ACCENT = "#D4788A"
ACCENT_SOFT = "#EBA8B5"
ACCENT_PALE = "#F7E0E5"
ROUTE_RUN = "#D4788A"
ROUTE_DONE = "#9B6B8A"
FG = "#3D2B2B"
FG_MID = "#8A6A6A"
FG_DIM = "#BFA0A0"
CITY_FILL = "#D4788A"
GRID = "#F0EAEA"
BTN_GEN_BG = "#D4788A"
BTN_RUN_BG = "#7ABFA8"
BTN_STOP_BG = "#C49080"
BTN_RST_BG = "#A0A0C0"

FONT_UI = ("Segoe UI", 9)
FONT_BOLD = ("Segoe UI", 9, "bold")
FONT_SMALL = ("Segoe UI", 8)
FONT_TINY = ("Segoe UI", 7)


# ── Dessin carte ──────────────────────────────────────────────────────────────
def dessiner_carte(canvas, villes, chemin=None, couleur=ROUTE_RUN):
    canvas.delete("all")
    w = canvas.winfo_width() or 640
    h = canvas.winfo_height() or 400
    canvas.create_rectangle(0, 0, w, h, fill=BG, outline="")
    for x in range(0, w, 40):
        canvas.create_line(x, 0, x, h, fill=GRID, width=1)
    for y in range(0, h, 40):
        canvas.create_line(0, y, w, y, fill=GRID, width=1)
    if chemin:
        for i in range(len(chemin)):
            v1 = chemin[i]
            v2 = chemin[(i + 1) % len(chemin)]
            canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill=ACCENT_PALE, width=6)
        for i in range(len(chemin)):
            v1 = chemin[i]
            v2 = chemin[(i + 1) % len(chemin)]
            canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill=couleur, width=1.5)
    for v in villes:
        r = 5
        canvas.create_oval(
            v.x - r - 3,
            v.y - r - 3,
            v.x + r + 3,
            v.y + r + 3,
            fill=ACCENT_PALE,
            outline="",
        )
        canvas.create_oval(
            v.x - r,
            v.y - r,
            v.x + r,
            v.y + r,
            fill=CITY_FILL,
            outline=CARD_BG,
            width=1.5,
        )
        canvas.create_text(
            v.x + 10, v.y - 10, text=str(v.num), fill=FG_DIM, font=FONT_TINY
        )


# ── Dessin courbe ─────────────────────────────────────────────────────────────
def dessiner_courbe(canvas, hist):
    canvas.delete("all")
    w = canvas.winfo_width() or 220
    h = canvas.winfo_height() or 120
    pL, pR, pT, pB = 42, 8, 10, 20
    cw, ch = w - pL - pR, h - pT - pB
    canvas.create_rectangle(0, 0, w, h, fill=CARD_BG, outline="")
    canvas.create_line(pL, pT, pL, h - pB, fill=BORDER, width=1)
    canvas.create_line(pL, h - pB, w - pR, h - pB, fill=BORDER, width=1)
    if len(hist) < 2:
        canvas.create_text(
            w // 2, h // 2, text="en attente", fill=FG_DIM, font=FONT_TINY
        )
        return
    mn, mx = min(hist), max(hist)
    sp = mx - mn or 1
    n = len(hist)
    pts = [
        (pL + (i / (n - 1)) * cw, h - pB - ((d - mn) / sp) * ch)
        for i, d in enumerate(hist)
    ]
    poly = [pL, h - pB] + [c for p in pts for c in p] + [pts[-1][0], h - pB]
    canvas.create_polygon(poly, fill=ACCENT_PALE, outline="")
    for i in range(len(pts) - 1):
        canvas.create_line(
            pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], fill=ACCENT, width=2
        )
    canvas.create_text(
        pL - 4, pT + 4, text=f"{mx:.0f}", fill=FG_DIM, font=FONT_TINY, anchor="e"
    )
    canvas.create_text(
        pL - 4, h - pB, text=f"{mn:.0f}", fill=ACCENT, font=FONT_TINY, anchor="e"
    )
    xf, yf = pts[-1]
    canvas.create_oval(
        xf - 4, yf - 4, xf + 4, yf + 4, fill=ACCENT, outline=CARD_BG, width=1.5
    )


# ── Fenêtre ───────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Voyageur de Commerce")
root.geometry("960x640")
root.configure(bg=BG)
root.resizable(True, True)

style = ttk.Style(root)
style.theme_use("clam")
style.configure(
    "P.Horizontal.TProgressbar",
    troughcolor=ACCENT_PALE,
    background=ACCENT,
    bordercolor=ACCENT_PALE,
    lightcolor=ACCENT_SOFT,
    darkcolor=ACCENT,
    thickness=4,
)

# ── Topbar ────────────────────────────────────────────────────────────────────
topbar = tk.Frame(root, bg=TOPBAR_BG, height=64)
topbar.pack(fill="x")
topbar.pack_propagate(False)

tk.Label(
    topbar,
    text="Voyageur de Commerce",
    bg=TOPBAR_BG,
    fg=FG,
    font=("Georgia", 12, "italic"),
).pack(side="left", padx=(18, 6), pady=14)
tk.Label(topbar, text="·", bg=TOPBAR_BG, fg=FG_DIM, font=FONT_UI).pack(
    side="left", padx=(0, 6)
)
tk.Label(
    topbar, text="algorithme génétique", bg=TOPBAR_BG, fg=FG_DIM, font=FONT_SMALL
).pack(side="left")
tk.Frame(topbar, bg=BORDER, width=1).pack(side="left", fill="y", padx=18, pady=14)


def make_entry(parent, label, default, width=5):
    f = tk.Frame(parent, bg=TOPBAR_BG)
    tk.Label(f, text=label, bg=TOPBAR_BG, fg=FG_MID, font=FONT_SMALL).pack(
        anchor="w", pady=(0, 3)
    )
    e = tk.Entry(
        f,
        width=width,
        bg=CARD_BG,
        fg=ACCENT,
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        bd=0,
        insertbackground=ACCENT,
        justify="center",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
    )
    e.insert(0, str(default))
    e.pack()
    return f, e


frm_n, entry_n = make_entry(topbar, "Villes", 10, width=5)
frm_pop, entry_pop = make_entry(topbar, "Population", 50, width=5)
frm_n.pack(side="left", padx=(0, 16), pady=12)
frm_pop.pack(side="left", padx=(0, 20), pady=12)


def get_n():
    try:
        return max(2, int(entry_n.get()))
    except:
        return 10


def get_pop():
    try:
        return max(2, int(entry_pop.get()))
    except:
        return 50


tk.Frame(topbar, bg=BORDER, width=1).pack(side="left", fill="y", padx=(0, 16), pady=14)


def make_btn(parent, text, bg, cmd):
    return tk.Button(
        parent,
        text=text,
        bg=bg,
        fg="white",
        font=FONT_BOLD,
        padx=14,
        pady=5,
        relief="flat",
        bd=0,
        cursor="hand2",
        activebackground=bg,
        activeforeground="white",
        command=cmd,
    )


btn_generer = make_btn(
    topbar,
    "Générer",
    BTN_GEN_BG,
    lambda: controller.generer_villes(
        get_n(), canvas_map.winfo_width() or 640, canvas_map.winfo_height() or 400
    ),
)
btn_generer.pack(side="left", padx=(0, 8), pady=16)

btn_lancer = make_btn(
    topbar, "Lancer", BTN_RUN_BG, lambda: controller.lancer(get_pop())
)
btn_lancer.pack(side="left", padx=(0, 8), pady=16)

btn_stop = make_btn(topbar, "Stop", BTN_STOP_BG, lambda: controller.stop())
btn_stop.pack(side="left", padx=(0, 8), pady=16)

btn_reset = make_btn(topbar, "Reset", BTN_RST_BG, lambda: controller.reset())
btn_reset.pack(side="left", pady=16)

lbl_status = tk.Label(topbar, text="prêt", bg=TOPBAR_BG, fg=FG_DIM, font=FONT_SMALL)
lbl_status.pack(side="right", padx=18)

tk.Frame(root, bg=BORDER, height=1).pack(fill="x")

# ── Contenu ───────────────────────────────────────────────────────────────────
content = tk.Frame(root, bg=BG)
content.pack(fill="both", expand=True, padx=12, pady=10)

map_outer = tk.Frame(content, bg=BORDER, padx=1, pady=1)
map_outer.pack(side="left", fill="both", expand=True)
canvas_map = tk.Canvas(map_outer, bg=BG, highlightthickness=0)
canvas_map.pack(fill="both", expand=True)

right = tk.Frame(
    content, bg=PANEL_BG, width=220, highlightthickness=1, highlightbackground=BORDER
)
right.pack(side="right", fill="y", padx=(10, 0))
right.pack_propagate(False)


def section_title(parent, text):
    f = tk.Frame(parent, bg=PANEL_BG)
    f.pack(fill="x", padx=14, pady=(14, 6))
    tk.Label(f, text=text, bg=PANEL_BG, fg=FG_MID, font=("Segoe UI", 8, "bold")).pack(
        side="left"
    )
    tk.Frame(f, bg=BORDER, height=1).pack(
        side="left", fill="x", expand=True, padx=(8, 0), pady=4
    )


def stat_card(parent, label, accent=ACCENT):
    card = tk.Frame(parent, bg=ACCENT_PALE)
    card.pack(fill="x", padx=14, pady=(0, 8))
    tk.Label(
        card, text=label, bg=ACCENT_PALE, fg=FG_DIM, font=FONT_TINY, anchor="w"
    ).pack(fill="x", padx=10, pady=(8, 0))
    val = tk.Label(
        card,
        text="—",
        bg=ACCENT_PALE,
        fg=accent,
        font=("Segoe UI", 16, "bold"),
        anchor="w",
    )
    val.pack(fill="x", padx=10, pady=(2, 8))
    return val


section_title(right, "Résultats")
lbl_gen = stat_card(right, "génération", ACCENT)
lbl_dist = stat_card(right, "meilleure distance", ROUTE_DONE)

section_title(right, "Évolution")
canvas_chart = tk.Canvas(
    right, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER, height=120
)
canvas_chart.pack(fill="x", padx=14, pady=(0, 10))

section_title(right, "Progression")
prog_wrap = tk.Frame(right, bg=PANEL_BG)
prog_wrap.pack(fill="x", padx=14, pady=(0, 10))
progress = ttk.Progressbar(
    prog_wrap, orient="horizontal", style="P.Horizontal.TProgressbar", maximum=100
)
progress.pack(fill="x")

section_title(right, "Méthodes")
legende_frame = tk.Frame(right, bg=PANEL_BG)
legende_frame.pack(fill="x", padx=14, pady=(0, 10))
for label, detail in [
    ("Sélection", "tournoi k=3"),
    ("Croisement", "Order Crossover"),
    ("Mutation", "swap aléatoire"),
    ("Élitisme", "meilleur conservé"),
    ("Générations", str(NB_GENERATIONS)),
]:
    row = tk.Frame(legende_frame, bg=PANEL_BG)
    row.pack(fill="x", pady=1)
    tk.Label(
        row, text=label, bg=PANEL_BG, fg=FG_MID, font=FONT_TINY, width=11, anchor="w"
    ).pack(side="left")
    tk.Label(row, text=detail, bg=PANEL_BG, fg=ACCENT, font=FONT_TINY, anchor="w").pack(
        side="left"
    )

historique = []


# ── Vue ───────────────────────────────────────────────────────────────────────
class View:
    def __init__(self):
        self.root = root
        self.canvas = canvas_map
        self.lbl_gen = lbl_gen
        self.lbl_dist = lbl_dist
        self.lbl_status = lbl_status
        self.progress = progress

    def dessiner(self, villes, chemin=None, couleur=ROUTE_RUN):
        dessiner_carte(canvas_map, villes, chemin, couleur)

    def update_courbe(self, distance):
        historique.append(distance)
        dessiner_courbe(canvas_chart, historique)

    def reset_stats(self):
        lbl_gen.config(text="—")
        lbl_dist.config(text="—")
        lbl_status.config(text="prêt", fg=FG_DIM)
        progress["value"] = 0
        historique.clear()
        dessiner_courbe(canvas_chart, [])

    def set_boutons(self, actif):
        s = "normal" if actif else "disabled"
        btn_generer.config(state=s)
        btn_lancer.config(state=s)
        btn_reset.config(state=s)
        btn_stop.config(state="disabled" if actif else "normal")


view = View()
controller = Controller(view)
btn_stop.config(state="disabled")
root.mainloop()
