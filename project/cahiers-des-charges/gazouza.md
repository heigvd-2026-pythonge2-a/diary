# Cahier des charges — Psice

*Simulateur de circuits électroniques — HEIG-VD, 10 novembre 2026*

## 1. Contexte et besoin

Psice est un simulateur de circuits électroniques destiné aux étudiants de 1re et 2e année HEIG-VD, conçu comme une alternative plus simple à LTspice. Projet de groupe de 2e année (4 personnes, environ 90 h chacune), développé avec l'assistance de l'IA.

**Problème :** LTspice demande beaucoup de temps de prise en main (interface datée, syntaxe SPICE, résultats peu lisibles). Ce temps est perdu pour l'essentiel. Comprendre le comportement des composants vus en cours est, selon l'équipe de projet, plus important.

**Besoin :** dessiner un circuit, le simuler et lire tensions et courants en quelques clics, sans connaître SPICE.

**Valeur ajoutée:** Psice est open source (licence MIT) et écrit en Python (langage enseigné à la HEIG-VD), ce qui transforme le simulateur d'une « boîte noire » en un outil transparent que les étudiants et enseignants peuvent décoder tout en restant dans un cadre pertinent à la formation.

## 2. Objectifs
- Simuler un premier circuit (diviseur, RC) en moins de 15 minutes, sans formation préalable.
- Mesurer la tension d'un fil ou le courant d'un composant d'un simple clic (sonde interactive).
- Offrir une ergonomie adaptée aux débutants en masquant la complexité de LTspice (aucune directive texte à taper, menus contextuels plus petits et paramètres de simulation guidés).

## 3. Périmètre

| Famille | Composants inclus |
| --- | --- |
| Passifs | R, C, L |
| Sources | Tension et courant : AC, DC, PULSE, SIN ; masse |
| Diodes | Diodes de signal, de redressement, Zener, LED |
| Ampli-op | Modèles idéaux et réels |
| Transistors | Transistors BJT (NPN / PNP) et MOSFET (canal N) |

Les composants et leurs symboles sont stockés dans une bibliothèque (fichiers JSON + modèles SPICE `.model` / `.subckt`), extensible sans toucher au code.

**Hors périmètre :** circuits numériques et logiques, conception de PCB, simulation RF, version macOS/Linux, hébergement en ligne.

## 4. Exigences

| Priorité | Exigence |
| --- | --- |
| Indispensable | Éditeur de schéma 2D : placer, tourner, relier avec des fils, grille, zoom |
| Indispensable | Simulation ngspice : point de fonctionnement (`.op`) et temporelle (`.tran`) |
| Indispensable | Affichage des tensions de nœuds et des courants de branches ; sonde avec le clic |
| Indispensable | Courbes (zoom, curseurs) ; sauvegarde et ouverture des schémas (format JSON) |
| Important | Import des fichiers `.asc` LTspice contenant uniquement des composants du périmètre (section 3) |
| Important | Mesures sur les courbes : crête, moyenne, temps de montée |
| Important | Export : schéma en PNG, courbes en CSV, netlist SPICE |
| Important | Analyse fréquentielle (`.ac`, diagramme de Bode) : l'utilisateur choisit la source d'entrée, l'excitation AC est configurée automatiquement |
| Important | Balayage DC (`.dc`, DC Sweep) |
| Important | Animation du courant sur le schéma ; annuler / rétablir |
| Bonus | FFT d'une courbe temporelle |

## 5. Contraintes

- **Technique** interface web (React + TypeScript) affichée dans une fenêtre pywebview, backend Python. Les binaires de simulation ngspice sont embarqués dans l'application : aucune installation séparée n'est requise et la simulation fonctionne hors ligne.
- **Normes** symboles graphiques selon CEI 60617, symboles et unités selon CEI 60027 et SI.
- **Collaboration** code sur GitHub, une branche par tâche, chaque fusion relue par un autre membre ; liste des tâches suivie dans GitHub Issues.
- **Intégration continue** GitHub Actions exécute les tests pytest et mesure la couverture à chaque pull request ; une fusion n'est possible que si les tests passent. Couverture visée : au moins 80 % du code du moteur Python.
- **Exécution** tout fonctionne en local, sur Windows 10 et 11, sans connexion Internet.

## 6. Livrables et Acceptation

**Livrables :** code source sur GitHub ; tests automatisés du moteur (pytest) ; application Windows zippée (ngspice inclus) ; rapport de projet ; démonstration orale.

**Critères d'acceptation :**
- Toutes les exigences « Indispensable » et « Important » de la section 4 sont fonctionnelles dans l'application livrée.