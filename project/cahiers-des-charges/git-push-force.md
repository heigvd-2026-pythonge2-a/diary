# Sesame Bot Vision by push --force

## 1. Membres de l'équipe

- **Alrick Delley** — chef de projet
- **Missègue Noah**
- **Thiébaud Maïnau**
- **Nicolas Besson**

## 2. Description du projet

### 2.1 Contexte

Nous voulons construire un petit robot à quatre pattes, imprimé en 3D, qui repère une personne et la suit tout seul.

Nous partons d'un projet open source existant, le **[Sesame Robot](https://github.com/dorianborian/sesame-robot)**. C'est un robot araignée piloté par un ESP32, avec huit petits servomoteurs (deux par patte) et un écran OLED qui affiche son visage. De base, il se contrôle seulement à distance depuis un téléphone.

### 2.2 Notre apport

Notre ajout est de lui donner des « yeux ». Nous plaçons sur le robot un **Raspberry Pi Zero 2 W** avec une petite caméra. Le Pi analyse l'image pour détecter une personne, puis envoie des ordres simples à l'ESP32 : avancer, tourner à gauche, tourner à droite ou s'arrêter. Le robot se tourne vers la personne, la suit en restant à environ un mètre, et s'arrête s'il la perd de vue.

Le visage sur l'écran change selon ce que fait le robot : il dort au repos, a l'air surpris quand il voit quelqu'un, et concentré quand il le suit.

### 2.3 Objectifs

- détecter une personne devant le robot ;
- se tourner vers elle et la suivre en marchant ;
- s'arrêter si la personne disparaît ;
- fonctionner sur batterie, sans ordinateur.

## 3. Matériel et coûts

Le coût du matériel dépendra de ce que nous pourrons obtenir auprès du **MakeLab**. Les pièces disponibles sur place seront utilisées en priorité ; seul le reste sera commandé.

| Matériel | Source envisagée |
| --- | --- |
| ESP32 | MakeLab, sinon commande |
| 8 servomoteurs | MakeLab, sinon commande |
| Écran OLED | MakeLab, sinon commande |
| Raspberry Pi Zero 2 W + caméra | MakeLab, sinon commande |
| Batterie et alimentation | MakeLab, sinon commande |
| Filament pour l'impression 3D | MakeLab |

## 4. Tâches et planification

| Semaine | Dates | Tâche
| --- | --- | ---
| 1-2 | 9 – 22 nov. 2026 | Réaliser le cahier des charges, commander le matériel, imprimer les pièces
| 3-4 | 23 – 6 déc 2026 | Monter le robot et le faire marcher avec le programme d'origine
| 5 | 7 – 13 déc. 2026 | Installer le Pi et la caméra, détecter une personne, faire communiquer le Pi et l'ESP32
| 6 | 14 – 20 déc. 2026 | Faire console Internet
| 7–8 | 20 déc. 2026 – 3 janv. 2027 | Programmer le suivi de la personne
| 9 | 4 – 10 janv. 2027 | Tester et corriger
| 10 | 11 – 17 janv. 2027 | Rapport et présentation

Ce planning est donné à titre indicatif : il sert uniquement à donner un aperçu des tâches à réaliser dans le temps imparti.

## 5. Répartition du travail

Cette répartition donne une idée générale des responsabilités ; elle n'est pas figée et chacun pourra aider sur les autres parties selon l'avancement.

| Membre | Responsabilité principale |
| --- | --- |
| **Alrick Delley** | Impression 3D, montage mécanique, servomoteurs et marche du robot , coordination du projet,|
| **Missègue Noah** | Console Internet et animations du visage sur l'écran OLED, caméra et détection de personne sur le Raspberry Pi |
| **Thiébaud Maïnau** | Impression 3D, montage mécanique, servomoteurs et marche du robot |
| **Nicolas Besson** |  Communication Pi ↔ ESP32, caméra et détection de personne sur le Raspberry Pi  |
| **Toute l'équipe** | Logique de suivi, tests, rapport et présentation |

## 6. Jalons de qualité

| Jalon | Fin de semaine | Critère de validation | OK |
| --- | --- | --- | :---: |
| J1 — Préparation | 2 (22 nov.) | Cahier des charges rendu, matériel obtenu ou commandé, pièces imprimées | ☐ |
| J2 — Robot assemblé | 4 (6 déc.) | Le robot marche avec le programme d'origine, les 8 servos et l'écran fonctionnent | ☐ |
| J3 — Détection et communication | 5 (13 déc.) | Le Pi détecte une personne de façon fiable et ses ordres (avancer, gauche, droite, stop) sont exécutés par l'ESP32 | ☐ |
| J4 — Console Internet | 6 (20 déc.) | La console Internet permet de voir l'état du robot et de le contrôler | ☐ |
| J5 — Suivi | 8 (3 janv.) | Le robot se tourne vers la personne, la suit à environ 1 m et s'arrête s'il la perd | ☐ |
| J6 — Autonomie | 9 (10 janv.) | Démonstration complète sur batterie | ☐ |
| J7 — Livraison | 10 (17 janv.) | Rapport rendu et présentation prête | ☐ |

☐ En cours.
✅ Jalon validé.

