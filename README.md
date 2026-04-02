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
3. Sélection par tournoi (k=3)
4. Croisement — Order Crossover (OX)
5. Mutation par inversion de segment
6. Élitisme — conservation du meilleur individu
7. Répétition sur **300 générations**

La **fitness** est définie par :

```
fitness = 1 / distance_totale
```

> Plus la distance est petite, plus la fitness est grande.

---

## 🔬 Opérateurs génétiques

### Sélection — Tournoi (k=3)
À chaque étape, 3 individus sont tirés aléatoirement dans la population et le meilleur est sélectionné comme parent. Cette méthode évite la convergence prématurée causée par une sélection trop stricte des meilleurs individus.

### Croisement — Order Crossover (OX)
Un segment du chemin du premier parent est copié dans l'enfant, puis les villes manquantes sont ajoutées dans l'ordre du second parent. Cette méthode **garantit un chemin valide** (sans doublons ni villes manquantes), ce qui est essentiel pour le TSP.

### Mutation — Inversion de segment
Un segment aléatoire du chemin est inversé (probabilité 20%). Cette opération est plus efficace qu'un simple échange de deux villes car elle explore l'espace des solutions plus efficacement tout en préservant des sous-séquences valides.

### Élitisme
Le meilleur individu de chaque génération est automatiquement conservé dans la génération suivante. Cela garantit que la meilleure solution trouvée ne peut jamais se dégrader.

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
| `model` | Structures de données (villes, individus, population) |
| `vue` | Interface graphique Tkinter |
| `controlleur` | Boucle évolutive et lien avec l'interface |
| `main.py` | Point d'entrée — lance l'application |

> Les opérateurs génétiques (sélection, croisement, mutation) sont implémentés dans le contrôleur afin de permettre une mise à jour de l'interface en temps réel à chaque génération.

---

## 🖥 Interface graphique

L'interface propose :

- **Saisie libre** du nombre de villes et de la taille de la population directement dans la barre du haut
- **Génération** de villes aléatoires sur la carte
- **Lancement** de l'algorithme génétique avec visualisation en direct
- **Arrêt anticipé** via le bouton *Stop* — affiche le meilleur résultat atteint
- **Courbe d'évolution** de la meilleure distance génération par génération
- **Indicateur de progression** et affichage de la meilleure distance trouvée
- **Panneau "Méthodes"** récapitulant les opérateurs utilisés

Les villes sont représentées par des points colorés, le chemin courant par des lignes roses, et le chemin final s'affiche en mauve à la fin.

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
6. Cliquer sur **Stop** pour interrompre à tout moment, ou attendre la fin des 300 générations
7. Le chemin optimal final s'affiche en mauve à la fin

---

## ⚙️ Paramètres de l'algorithme

| Paramètre | Valeur |
|---|---|
| Taille population | Saisie libre (défaut : 50) |
| Nombre de générations | **300** |
| Sélection | **Tournoi (k=3)** |
| Croisement | **Order Crossover (OX)** |
| Mutation | **Inversion de segment** (probabilité : 20%) |
| Élitisme | **Oui** — meilleur individu conservé |

---

## 📚 Contexte académique

> Projet réalisé dans le cadre du cours **Intelligence Artificielle — Algorithmes Génétiques**  
> Problème du Voyageur de Commerce (TSP)

---

## 👤 Auteurs

- **Rayane Ait Braham**
- **Salah Benrabah**
- **Lina Ouallam**