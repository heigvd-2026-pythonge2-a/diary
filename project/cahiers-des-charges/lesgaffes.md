# Cahier des charges — Physics Sandbox 2D

| Champ | Valeur |
|---|---|
| **Version** | 0.1 |
| **Date** | 15/11/2026 |
| **Équipe** | Lesgaffes : Louis Buffin, Leonel Saez, Jonathan Greppin, Michele Baschiera |
| **Encadrant** | Prof. Yves Chevallier |
| **Langage** | Python 3 |

---

## 1. Contexte

L'apprentissage de la physique repose en grande partie sur des notions abstraites, que les étudiants ont souvent du mal à se représenter. Les supports classiques (énoncés, schémas statiques) ne permettent pas toujours de comprendre comment un phénomène évolue quand on modifie ses paramètres.

Le projet *Physics Sandbox 2D* répond à ce besoin : une application pédagogique interactive qui permet de **simuler, visualiser et expérimenter** des phénomènes physiques en deux dimensions.

## 2. Objectifs

L'application doit proposer un ensemble de simulations physiques interactives, accessibles depuis un **menu principal**. L'utilisateur doit pouvoir choisir une simulation, modifier ses paramètres et observer le résultat en temps réel.

### 2.1 Simulations requises (périmètre minimal)

| Domaine | Simulation |
|---|---|
| **Électrostatique** | Interaction entre 2 à 3 charges ponctuelles (forces, lignes de champ) |
| | Interaction entre une charge ponctuelle et des objets chargés (plaque, disque, sphère) |
| **Dynamique** | Simulateur des lois de Newton (forces, masse, accélération, frottements) |
| **Optique** | Réfraction de rayons lumineux à travers diverses lentilles (convergentes, divergentes) |
| **Ondes** | Spectre électromagnétique, générateur d'ondes et étude des ondes (fréquence, amplitude, longueur d'onde) |

### 2.2 Exigences fonctionnelles générales

- Paramètres modifiables par l'utilisateur (curseurs, champs de saisie).
- Mise à jour de la simulation en temps réel.
- Possibilité de réinitialiser une simulation et de revenir au menu.
- Chaque simulation intègre son explication théorique, consultable dans l'application pendant la simulation (voir Notes).

### 2.3 Exigences non fonctionnelles

- **Fiabilité :** toutes les simulations doivent fonctionner sans bug bloquant.
- **Ergonomie :** interface simple, adaptée à des étudiants débutants.
- **Performance :** fluidité constante des animations (>30fps) sur des pc ou laptop de bureau sans gpu dédié.
- **Extensibilité :** architecture modulaire permettant l'ajout de futurs modules physiques sans modifier le noyau (voir Notes).
- **Maintenabilité :** code commenté et versionné (Git).

## 3. Livrable

- Une **application exécutable pour Windows**, téléchargeable et utilisable sans installation de Python.
- Le code source documenté.

## 4. Périmètre

### 4.1 Parties prenantes

- **Équipe de développement :** Louis Buffin, Leonel Saez, Jonathan Greppin, Michele Baschiera
- **Encadrant :** Prof. Yves Chevallier (suivi et validation)
- **Doyen :** présentation finale du projet

### 4.2 Hors périmètre

- Modélisation et simulation en 3D.
- Compatibilité avec d'autres plateformes (Linux, macOS).
- Fonctionnalités en ligne (comptes utilisateurs, partage des configurations de simulation).

## 5. Délais

- **Charge totale estimée :** 450 heures (équipe complète).
- **Échéance :** fin du 2ᵉ semestre 2026.

## Planning général

| Tâche | Activité | Charge |
|---|---|---|
| **1** | Analyse et conception | 30 h |
| **2** | Développement des simulations | 200 h |
| **3** | Homogénisation de l'interface graphique | 60 h |
| **4** | Test/Debug | 140 h |
| **5** | Documentation | 20 h |
| **Total** | | 450 h |

---

## Notes

1. **Architecture modulaire et extensible :** l'application doit être conçue comme un noyau commun (menu, affichage, gestion des paramètres) auquel viennent se brancher des **modules de simulation indépendants**. Chaque module respecte une interface commune (initialisation, mise à jour, affichage, paramètres, contenu pédagogique). Ainsi, de nouveaux modules physiques (ex. magnétisme, thermodynamique, mécanique des fluides) pourront être ajoutés à l'avenir **sans modifier le code existant** : il suffira de déposer le nouveau module dans le dossier prévu pour qu'il apparaisse automatiquement dans le menu.
2. **Dimension pédagogique :** chaque simulation est accompagnée d'une **explication théorique** accessible **directement depuis la simulation en cours** (ex. panneau latéral ou bouton « Théorie »), sans quitter la simulation ni consulter de document externe. L'étudiant peut ainsi lire l'explication tout en manipulant les paramètres. Le contenu comprend : présentation du phénomène, lois et formules utilisées, signification des paramètres, et un ou deux exemples à tester. L'objectif est que l'étudiant puisse relier ce qu'il observe à la théorie vue en cours.
3. **Format du contenu pédagogique :** les explications sont stockées dans des fichiers séparés du code (ex. Markdown), propres à chaque module. Elles peuvent ainsi être rédigées, corrigées ou enrichies sans toucher à la programmation.
