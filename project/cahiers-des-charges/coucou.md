# Cahier des charges - Repère

**Projet Python - 2026-2027 - HEIG-VD**

## 1. Présentation du projet

Repère est un système permettant de localiser et de retrouver du matériel à l'intérieur d'un bâtiment.

L’équipe du projet est composée de cinq membres. Samuel Nyitrai assurera la coordination de l’équipe et le suivi de l’avancement en tant que chef de projet.

- Samuel Nyitrai - chef de projet
- Luca Gingras
- Luca Schweitzer
- Logan Maire
- Mateo Cervellin

Le projet repose sur des balises Bluetooth fixées aux objets, des antennes qui détectent leurs signaux, un serveur qui estime la position de chaque objet à partir de ces mesures, et une application qui l’affiche sur un plan.

L'objectif est de réaliser une preuve de concept fonctionnelle, avec la possibilité d'étendre le système à différents bâtiments par la suite.

## 2. Fonctionnement général

Chaque objet est associé à une balise Bluetooth qui émet un identifiant.

Des antennes réparties dans le bâtiment détectent ces signaux, mesurent leur puissance (RSSI) et transmettent les données à un serveur. Celui-ci estime la position des objets et met les informations à disposition de l'application.

Le système doit d'abord permettre d'identifier la salle dans laquelle se trouve un objet. Une localisation plus précise, de l'ordre du mètre, est un objectif de développement qui devra être évalué lors des tests.

## 3. Fonctionnalités

### Fonctionnalités minimales (MVP)

- Ajouter, modifier et supprimer des objets dans l'inventaire.
- Associer chaque objet à une balise Bluetooth.
- Rechercher un objet par son nom.
- Localiser automatiquement les objets par salle.
- Afficher les objets sur un plan prédéfini du bâtiment.
- Conserver la dernière position connue et signaler une perte de détection.
- Indiquer la date de dernière détection et signaler une localisation incertaine lorsque nécessaire.


### Fonctionnalités visées après le MVP

- Améliorer la précision de localisation, avec un objectif d'environ un mètre.
- Afficher un itinéraire sur le plan jusqu'à l'objet recherché, en localisant automatiquement la salle dans laquelle se trouve l'utilisateur.
- Ajouter un mode administrateur pour gérer le matériel et les équipements.

### Extensions possibles

- Importer et configurer les plans de différents bâtiments.
- Optimiser l'autonomie des balises grâce à la détection de mouvement.
- Ajouter des fonctions de gestion de parc (disponibilité, prêts, historique).

## 4. Contraintes techniques

- Utilisation de balises Bluetooth Low Energy (BLE) et d'antennes.
- Développement principalement en Python.
- Application accessible sur ordinateur et sur smartphone.
- Communication entre les antennes et le serveur par Wi-Fi ou une autre solution adaptée.
- Déploiement initial sur une zone de test limitée, avec un plan fixe.
- Choix des solutions techniques en privilégiant la simplicité et la fiabilité.
- Prise en compte des perturbations des signaux Bluetooth liées aux murs, aux obstacles et à l'environnement.


## 5. Critères de réussite

La preuve de concept sera considérée comme fonctionnelle si :

- Plusieurs balises peuvent être détectées et identifiées.
- Le système permet de déterminer la salle d'un objet.
- Les positions sont consultables sur un plan.
- Un objet peut être ajouté à l'inventaire et associé à une balise.
- La dernière position reste disponible lorsqu'une balise n'est plus détectée.
- L'application distingue les objets détectés des objets dont seule la dernière position est connue.

Les essais viseront notamment les objectifs suivants :

| Critère | Objectif |
|---|---|
| Balises simultanées | Au moins 5 |
| Salles couvertes | Au moins 3 |
| Fiabilité de localisation par salle | Au moins 80 % de résultats corrects |
| Actualisation des positions | Moins de 10 secondes |
| Perte de détection | Signalement après environ 30 secondes |

Ces valeurs constituent des objectifs de test et pourront être adaptées selon les résultats expérimentaux et les contraintes matérielles.

La précision de localisation sera mesurée et établi lors des essais.


## 6. Organisation et moyens

Le projet est réalisé par un groupe de cinq étudiants, avec une organisation permettant de travailler en parallèle sur plusieurs aspects du projet.

### Planning prévisionnel

| Période | Phase | Objectif |
|---|---|---|
| Semaines 1–2 | Préparation et tests | Choix du matériel, tests BLE et communication avec les antennes |
| Semaines 3–4 | Localisation | Réception des signaux et première estimation de la position des objets |
| Semaines 5–6 | MVP | Inventaire, recherche et affichage des objets sur un plan |
| Semaines 7–8 | Améliorations | Précision de localisation, guidage et fonctionnalités supplémentaires |
| Semaines 9–10 | Finalisation | Intégration, tests, corrections et documentation |

Les phases pourront se chevaucher afin de permettre aux membres du groupe de travailler en parallèle.

La surface de déploiement et le nombre d'antennes seront définis selon les résultats des premiers essais, le budget et les autorisations disponibles.

## 7. Livrables

- Une preuve de concept fonctionnelle.
- Le code source du projet et les instructions nécessaires à son installation.
- Une démonstration et un bilan des résultats obtenus, comprenant les mesures de fiabilité et de précision de localisation.