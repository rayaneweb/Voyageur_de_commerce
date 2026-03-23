# 🧬 Voyageur de Commerce — Algorithme Génétique (TSP)

## 📌 Description

Ce projet résout le **problème du voyageur de commerce (TSP)** à l'aide d'un algorithme génétique.  
L'objectif est de trouver le chemin le plus court passant par toutes les villes exactement une fois, avant de revenir au point de départ.

Une interface graphique en **Tkinter** permet de saisir les paramètres, de générer des villes aléatoires et de visualiser en temps réel l'évolution du chemin trouvé par l'algorithme.

---

## 🧠 Algorithme génétique

L'algorithme génétique simule l'évolution naturelle pour améliorer progressivement les solutions.

**Étapes :**
1. Génération d'une population initiale aléatoire
2. Évaluation de la fitness de chaque individu
3. Sélection des meilleurs individus
4. Croisement *(crossover)*
5. Mutation
6. Création d'une nouvelle population
7. Répétition sur 100 générations

La **fitness** est définie par :

```
fitness = 1 / distance_totale
```

> Plus la distance est petite, plus la fitness est grande.

---

## 🏗 Architecture MVC

Le projet suit l'architecture **Model – View – Controller** :

```
project/
│
├── model/
│   ├── ville.py
│   ├── individu.py
│   ├── population.py
│   └── genetic_algorithm.py
│
├── vue/
│   └── interface.py
│
├── controlleur/
│   └── controller.py
│
└── main.py
```

| Partie | Rôle |
|---|---|
| `model` | Algorithme génétique et structures de données |
| `vue` | Interface graphique Tkinter |
| `controlleur` | Lien entre l'interface et l'algorithme |
| `main.py` | Point d'entrée — lance l'application |

---

## 🖥 Interface graphique

L'interface propose :

- **Saisie libre** du nombre de villes et de la taille de la population directement dans la barre du haut
- **Génération** de villes aléatoires sur la carte
- **Lancement** de l'algorithme génétique avec visualisation en direct
- **Courbe d'évolution** de la meilleure distance génération par génération
- **Indicateur de progression** et affichage de la meilleure distance trouvée

Les villes sont représentées par des points colorés, le chemin courant par des lignes, et le chemin final s'affiche dans une couleur distincte à la fin.

---

## ▶️ Lancer le projet

```bash
python main.py
```

**Utilisation :**
1. Saisir le nombre de villes souhaité dans le champ *Villes*
2. Saisir la taille de la population dans le champ *Population*
3. Cliquer sur **Générer** pour placer les villes aléatoirement
4. Cliquer sur **Lancer** pour démarrer l'algorithme
5. Observer l'évolution du chemin et de la courbe en temps réel
6. Le chemin optimal final s'affiche à la fin des 100 générations

---

## ⚙️ Paramètres de l'algorithme

| Paramètre | Valeur |
|---|---|
| Taille population | Saisie libre (défaut : 50) |
| Nombre de générations | 100 *(fixe)* |
| Mutation | Échange de deux villes aléatoires |
| Sélection | Meilleurs individus |
| Crossover | Order crossover (OX) |

---

## 📚 Contexte académique

> Projet réalisé dans le cadre du cours **Intelligence Artificielle — Algorithmes Génétiques**  
> Problème du Voyageur de Commerce (TSP)

---

## 👤 Auteurs

- **Rayane Ait Braham**
- **Salah Benrabah**
- **Lina Ouallam**