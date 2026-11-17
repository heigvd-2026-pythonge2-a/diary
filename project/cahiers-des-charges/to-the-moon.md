# Cahier des charges

> **Titre projet :** TTM Backtest

---

## Liste des membres et rôles

- **Nathan Vadillo** (chef de projet) : Résultats / Statistiques & coordination
- **Tiziano Giorgio** : Indicateurs & Stratégies
- **Mathis Cottet** : Données (Data)
- **En commun** : Moteur de backtest
- **Interface utilisateur (UI)** : gérée par chaque partie sur sa propre page (Données, Moteur/Indicateurs, Résultats)

---

## Présentation

Développer une application de backtest de stratégies de trading sur données historiques.

**Objectif :** tester et comparer la rentabilité et le risque d'une stratégie.

### Fonctionnalités

- **Ajout de données** :
  - Import de fichiers locaux (CSV / Parquet) nettoyés automatiquement (dates en UTC, suppression des doublons et erreurs).
- **Ajout de stratégies** :
  - Stratégies prêtes à l'emploi modifiables depuis l'interface (ex. : croisement de moyennes mobiles, RSI).
  - Possibilité d'ajouter ses propres stratégies en Python.
  - Filtre via un calendrier économique (éviter de trader lors des annonces importantes).
- **Ajout de paramètres** :
  - Choix du capital de départ, des frais, du slippage, des Stop-Loss / Take-Profit (SL/TP) et des réglages de la stratégie.
- **Sortie graphique** :
  - Graphique des prix avec les points d'achat et de vente.
  - Courbe d'évolution du capital et des pertes maximales (drawdown).
  - Comparaison de plusieurs tests entre eux et avec un simple achat/conservation (*Buy & Hold*).
- **Sortie statistique** :
  - Chiffres clés : rendement total, CAGR, ratios Sharpe/Sortino, perte maximale (Max Drawdown), taux de réussite (Win Rate), Profit Factor, ...
  - Tableau complet des trades exécutés.

---

## Contraintes

- Exécution rapide du moteur de backtest.
- Interface visuelle logique, simple et compréhensible (une page par partie : Données, Moteur/Indicateurs, Résultats).
- Code séparé par dossiers avec des formats d'échange communs (dates en UTC).

---

## Livrables

- L'application fonctionnelle.
- La documentation (installation, utilisation et cahier des charges).
- Les tests automatiques (`pytest`) avec couverture de code.
- Une vérification automatique sur GitHub (CI).

---

## Liste des tâches

- Choix des formats d'échange entre les parties
- Gestion des données et nettoyage (+ page UI Données)
- Bibliothèque :
  - Indicateurs
  - SL/TP
  - Calendrier économique
- Moteur de backtest et stratégies (+ page UI Moteur/Indicateurs)
- Calcul des statistiques et graphiques (+ page UI Résultats)
- Tests et mise en place de la CI

---

## Planification du projet

- **1. Conception** : définition de l'architecture et des formats d'échange.
- **2. Développement par module** : chacun code sa partie (logique + sa page UI) en parallèle avec ses tests.
- **3. Assemblage** : connexion des modules et des pages de l'application.
- **4. Finalisation** : tests complets, vérifications CI et documentation.
