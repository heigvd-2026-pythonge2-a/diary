# Analyse des cahiers des charges — mini-projet PythonGE2-A

État des dépôts au 17 novembre 2026.

## Consigne de référence

Cahier des charges de 1 à 2 pages pour un projet imaginé par le groupe, contenant : un titre, la description du projet, la liste des membres, le chef de projet, une planification rapide (liste des tâches et temps à investir). Rédaction sans LLM.

## Synthèse

Notes sur l'échelle 1 à 6 (4 = suffisant), calibrées sur ce qu'on peut attendre d'un groupe de 2e année dans un cours de projet. La note est la moyenne de quatre critères, arrondie au demi-point.

| Groupe         | Projet             | Consigne | Description | Plan. | Réalisme | Moyenne | Note  | Indices d'usage d'un LLM |
| -------------- | ------------------ | :------: | :---------: | :---: | :------: | :-----: | :---: | ------------------------ |
| git-push-force | Sesame Bot Vision  |   5.5    |      5      |  5.5  |   4.5    |   5.1   |  5.0  | Faibles                  |
| coucou         | Repère             |   4.5    |     5.5     |   4   |   4.5    |   4.6   |  4.5  | Modérés                  |
| lesgaffes      | Physics Sandbox 2D |   4.5    |      5      |   4   |   4.5    |   4.5   |  4.5  | Forts (mise en forme)    |
| to-the-moon    | TTM Backtest       |    5     |     4.5     |  3.5  |   5.5    |   4.6   |  4.5  | Forts (mise en forme)    |
| gazouza        | Psice              |    3     |      6      |   3   |   3.5    |   3.9   |  4.0  | Modérés                  |
| les-fatigues   | Lightworks         |   4.5    |      4      |  3.5  |   3.5    |   3.9   |  4.0  | Très faibles             |

Les quatre critères :

- Consigne : présence des éléments demandés et respect de la longueur.
- Description : clarté du besoin, du périmètre et des critères de réussite.
- Planification : tâches, calendrier, heures, répartition entre membres.
- Réalisme : faisabilité dans le temps imparti et part réelle de Python.

La note porte sur le document rendu, pas sur le respect de l'interdiction des LLM, qui est traité à part (dernière colonne). Les deux sont liés : les documents les plus « propres » sont aussi ceux où les indices sont les plus marqués. À qualité de fond égale, un texte rédigé à la main paraît donc moins bon.

### Éléments demandés

| Groupe         | Titre | Membres |    CdP    | Desc. | Liste des tâches | Temps à investir | Longueur  |
| -------------- | :---: | :-----: | :-------: | :---: | :--------------: | :--------------: | --------- |
| git-push-force |  oui  | oui (4) |    oui    |  oui  |    oui, datée    |       non        | 2,5 pages |
| coucou         |  oui  | oui (5) |    oui    |  oui  | phases seulement |       non        | 2,5 pages |
| lesgaffes      |  oui  | oui (4) |    non    |  oui  |     5 lignes     |  oui, par tâche  | 2,5 pages |
| to-the-moon    |  oui  | oui (3) |    oui    |  oui  |       oui        |       non        | 1,5 page  |
| gazouza        |  oui  |   non   |    non    |  oui  |       non        | total seulement  | 2 pages   |
| les-fatigues   |  oui  | oui (4) | implicite |  oui  |       oui        |       non        | 1 page    |

### Constats communs

- Le temps à investir est l'élément le plus négligé. Un seul groupe chiffre ses tâches (lesgaffes), un autre donne un total (gazouza). Aucun ne répartit les heures par personne.
- Les charges annoncées ne concordent pas : environ 112 h par personne chez lesgaffes (450 h à quatre), environ 90 h chez gazouza. Les autres ne disent rien.
- Aucun groupe ne traite les risques explicitement. Coucou s'en approche (perturbations du signal, précision « à évaluer »).
- Deux projets dépendent de matériel (coucou, git-push-force) sans budget ni délai de livraison ; c'est leur chemin critique.

## Analyse par groupe

### git-push-force — Sesame Bot Vision — 5.0

Robot quadrupède open source (ESP32) auquel le groupe ajoute un Raspberry Pi Zero 2 W et une caméra pour suivre une personne.

- Points forts. C'est le document le plus proche de la consigne. L'apport du groupe est clairement séparé de l'existant. Le planning est daté semaine par semaine, les responsabilités sont réparties par membre et sept jalons ont un critère de validation vérifiable. Le ton est simple et direct.
- Points faibles. Aucune estimation en heures. La section « Matériel et coûts » ne contient aucun coût. La « console Internet » apparaît dans le planning et les jalons sans être décrite dans les objectifs. La tâche centrale (suivi de la personne) tombe sur les vacances de Noël. La capacité du Pi Zero 2 W à détecter une personne en temps réel n'est pas discutée.
- Part de Python. Limitée au Pi (détection, commande) ; le micrologiciel de l'ESP32 vient du projet d'origine.
- Indices LLM : faibles. Fautes et maladresses humaines (lignes de tableau non fermées, « 23 – 6 déc »), commits successifs de trois membres.

### coucou — Repère — 4.5

Localisation de matériel dans un bâtiment par balises Bluetooth, antennes, serveur et application avec plan.

- Points forts. Meilleure description du lot après Psice : fonctionnement expliqué, périmètre en trois niveaux (MVP, après MVP, extensions) et critères de réussite chiffrés (5 balises, 3 salles, 80 % de localisations correctes, actualisation en moins de 10 s). Le groupe reconnaît que la précision au mètre est incertaine et se replie sur une localisation par salle, ce qui est mûr.
- Points faibles. Le planning se limite à cinq phases de deux semaines : pas de liste de tâches, pas d'heures, pas de répartition entre les cinq membres. Le matériel n'est ni listé ni chiffré (« selon le budget et les autorisations »). « Principalement en Python » laisse ouverte la question du code des antennes.
- Indices LLM : modérés. Le document arrive complet en un seul commit le 15 novembre, sans brouillon dans l'historique. Formulations génériques (« en privilégiant la simplicité et la fiabilité »), apostrophes typographiques et droites mélangées. Rien de probant.

### lesgaffes — Physics Sandbox 2D — 4.5

Application pédagogique regroupant des simulations 2D (électrostatique, dynamique, optique, ondes) avec explication théorique intégrée.

- Points forts. Seul groupe à chiffrer ses tâches (450 h au total). Exigences fonctionnelles et non fonctionnelles distinguées, hors périmètre explicite, livrable précis (exécutable Windows sans Python installé). L'idée d'une théorie consultable pendant la simulation est bonne.
- Points faibles. Aucun chef de projet désigné. Le planning tient en cinq lignes : « Développement des simulations, 200 h » n'est découpé ni par simulation ni par personne, et 140 h de test contre 30 h de conception est peu crédible. Pas de calendrier ; l'échéance (« fin du 2ᵉ semestre 2026 ») est floue. « Sans bug bloquant » n'est pas vérifiable. Aucune bibliothèque graphique n'est nommée. Les notes finales répètent le corps du texte.
- Indices LLM : forts pour la mise en forme. L'historique contient une première version du 10 novembre, rédigée à la main en environ 150 mots. Le commit « CdC formalized » du 15 novembre la remplace par le texte actuel, cinq fois plus long, au vocabulaire normalisé (fiabilité, ergonomie, extensibilité, maintenabilité, parties prenantes). Les idées de fond (simulations, 450 h, Windows, doyen) sont bien celles de la version manuscrite.

### to-the-moon — TTM Backtest — 4.5

Application de backtest de stratégies de trading sur données historiques.

- Points forts. Projet le plus réaliste : entièrement en Python, périmètre adapté à trois personnes, fonctionnalités concrètes (import CSV/Parquet, stratégies, frais et slippage, statistiques nommées). Chef de projet désigné et rôle attribué à chaque membre. Longueur respectée.
- Points faibles. La planification se réduit à quatre phases génériques sans durée, date ni heure. Les tâches ne sont pas rattachées aux personnes dans la liste. Pas de contexte ni de public visé. Contraintes non mesurables (« exécution rapide », « interface logique »). Aucune technologie d'interface n'est citée.
- Indices LLM : forts pour la mise en forme. La première version du 10 novembre est manuscrite et brève (fautes de frappe, section « planification » vide). Elle est ensuite « mise en forme » puis « simplifiée ». Le dépôt contient depuis le 10 novembre des fichiers `CLAUDE.md`, `GEMINI.md` et des *skills* d'agent. Le fond (titre, membres, fonctionnalités, tâches) figure déjà dans la version manuscrite.

### gazouza — Psice — 4.0

Simulateur de circuits électroniques pour débutants, alternative simplifiée à LTspice, bâti sur ngspice.

- Points forts. Meilleur cahier des charges au sens professionnel : problème, besoin et valeur ajoutée, périmètre par famille de composants, hors périmètre, exigences priorisées en trois niveaux, contraintes, livrables et critère d'acceptation. Le besoin est réel et bien ciblé.
- Points faibles. Trois éléments de la consigne manquent dans le document : la liste des membres, le chef de projet et toute planification. Seul un total figure (« 4 personnes, environ 90 h chacune »). Ces informations existent dans le `README.md` du dépôt (membres, jalons par semaine), où les rôles sont encore « à définir » et où aucun chef n'est nommé. Le périmètre est très ambitieux pour 360 h, et le critère d'acceptation exige toutes les exigences « Indispensable » et « Important », sans repli.
- Part de Python. L'interface est en React et TypeScript ; Python se limite au moteur et au lien avec ngspice. À discuter avec le groupe.
- Indices LLM : modérés. Le texte dit que le projet est « développé avec l'assistance de l'IA », sans préciser si cela concerne le document. Celui-ci arrive complet le 10 novembre (« synced with previous repo »), puis est révisé six fois par trois membres, avec des irrégularités de ponctuation typiques d'une retouche manuelle.

### les-fatigues — Lightworks — 4.0

Cartographie 3D de l'éblouissement causé par la réverbération du soleil sur des surfaces (modules photovoltaïques), à partir des données GIS suisses.

- Points forts. Sujet le plus original, ancré dans un besoin réel (cadre légal, 30 minutes d'éblouissement par jour). Consigne de longueur respectée (une page). Liste de tâches hiérarchisée, avec une bonne idée de cadrage : un MVP limité à une seule coordonnée GPS avant toute généralisation.
- Points faibles. L'objectif et le livrable ne disent pas la même chose (intensité d'une source lumineuse, puis durée d'ensoleillement). Pas d'heures, pas de dates, pas de répartition. Le chef de projet n'est désigné que par « BDFL ». Aucune source de données ni bibliothèque n'est nommée, alors que c'est le risque principal. La suite du plan déborde du cours : toute la Suisse, réécriture dans d'autres langages, analyse de marché. La figure n'a ni légende ni source. Plusieurs fautes d'orthographe.
- Indices LLM : très faibles. Style personnel, fautes, rédaction progressive dans l'historique. C'est le document qui respecte le plus visiblement la consigne. La première tâche prévoit en revanche des outils d'IA pour le développement.

## Limites de cette analyse

- Les indices d'usage d'un LLM reposent sur l'historique git et sur le style. Ils ne constituent pas une preuve ; seuls les cas lesgaffes et to-the-moon s'appuient sur une comparaison de versions.
- Seule la version actuelle de chaque document a été notée. Pour git-push-force, coucou et les-fatigues, les versions antérieures n'ont pas été comparées.
- Les nombres de pages sont estimés d'après le nombre de mots (360 à 840) et la place des tableaux.
