# Semaine 09/16

- [x] CI/CD
- [x] Documentation
- [x] Tests de non-régression
- [x] Configuration de votre LLM (Claude)

## CI/CD

L'**intégration continue** (*Continuous Integration*, CI) consiste à intégrer fréquemment les modifications de chaque développeur dans la branche principale. À chaque `push` ou *pull request*, un serveur récupère le code, installe les dépendances, puis lance automatiquement les vérifications : tests, analyse statique (*linter*), formatage, compilation, etc. Un problème est donc détecté quelques minutes après avoir été introduit, et non trois semaines plus tard, juste avant le rendu.

Le sigle **CD** recouvre deux notions voisines :

- la **livraison continue** (*Continuous Delivery*) : chaque version qui passe la CI est prête à être déployée, mais la mise en production reste déclenchée par un humain ;
- le **déploiement continu** (*Continuous Deployment*) : chaque version qui passe la CI est déployée automatiquement, sans intervention humaine (publication d'un paquet sur PyPI, mise en ligne d'un site, d'une documentation, etc.).

La CI/CD permet donc d'automatiser les tâches répétitives et d'avoir une garantie objective : « la branche `main` compile et ses tests passent ».

Historiquement, on utilisait des outils dédiés : **Jenkins** (auto-hébergé, configuré par un `Jenkinsfile`), **Travis CI**, **CircleCI** (`.circleci/config.yml`). La configuration est un fichier versionné dans le dépôt Git du projet. Ces outils restent très utilisés en entreprise, tout comme **GitLab CI** (`.gitlab-ci.yml`). Sur GitHub, on dispose aujourd'hui de **GitHub Actions**, une solution de CI/CD complète intégrée à la plateforme et gratuite pour les dépôts publics.

### GitHub Actions

Tout se passe dans le dossier `.github/workflows/` de votre projet. Il contient un ou plusieurs fichiers YAML (*workflows*), qui décrivent :

- **quand** le workflow se déclenche (`on:` : `push`, `pull_request`, une planification `schedule`, un déclenchement manuel `workflow_dispatch`, etc.) ;
- **où** il s'exécute (`runs-on:` : une machine virtuelle Ubuntu, Windows ou macOS fournie par GitHub) ;
- **quoi** exécuter (`jobs:`, eux-mêmes composés de `steps:`). Une étape est soit une commande shell (`run:`), soit une *action* réutilisable (`uses:`).

```text
mon-projet/
├── .github/
│   └── workflows/
│       ├── ci.yml        # tests à chaque push / PR
│       └── docs.yml      # déploiement de la documentation
├── src/
├── tests/
├── pyproject.toml
└── uv.lock
```

Exemple de fichier `.github/workflows/ci.yml` pour un projet géré avec `uv`. À chaque `push` sur `main` et à chaque *pull request*, le workflow installe Python, vérifie le code avec `ruff`, puis lance les tests sur trois versions de Python :

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13", "3.14"]

    steps:
      - name: Récupération du code
        uses: actions/checkout@v5

      - name: Installation de uv
        uses: astral-sh/setup-uv@v6
        with:
          python-version: ${{ matrix.python-version }}

      - name: Installation des dépendances
        run: uv sync --locked

      - name: Analyse statique
        run: uv run ruff check .

      - name: Tests et couverture
        run: uv run pytest --cov --cov-report=term-missing
```

Quelques remarques :

- `uv sync --locked` échoue si `uv.lock` n'est pas à jour par rapport à `pyproject.toml`. Cela garantit que la CI teste exactement les versions de dépendances que vous utilisez localement. Pensez donc à commiter `uv.lock`.
- La `matrix` lance un job par version de Python, en parallèle.
- Le numéro après `@` est la version de l'action. Vérifiez la dernière version sur la page GitHub de l'action (`actions/checkout`, `astral-sh/setup-uv`).
- Le résultat apparaît dans l'onglet **Actions** du dépôt, sous forme de coche verte ou de croix rouge à côté de chaque commit et de chaque PR. On peut même interdire le *merge* d'une PR tant que la CI ne passe pas (*Settings → Branches → Branch protection rules*).
- Avant de pousser, vous pouvez vérifier la syntaxe YAML localement. Une erreur d'indentation suffit à empêcher le workflow de démarrer.

## Documentation

Un bon projet est un projet correctement documenté. On distingue :

- le `README.md` : présentation, installation, démarrage rapide ;
- la documentation utilisateur et développeur : un site web généré à partir de fichiers Markdown placés dans `docs/` ;
- la documentation de l'API : générée automatiquement à partir des *docstrings* de votre code (par exemple avec `mkdocstrings`).

On utilise un **générateur de site statique**. **MkDocs** associé au thème **Material for MkDocs** a longtemps été la référence dans l'écosystème Python. Son équipe développe désormais **Zensical**, son successeur, qui reste capable de lire un `mkdocs.yml` existant. **Sphinx** reste très utilisé, notamment pour la documentation officielle de Python et de NumPy.

Avec Zensical :

```bash
uv add --dev zensical   # installation comme dépendance de développement
uv run zensical new .   # crée zensical.toml et docs/index.md
uv run zensical serve   # serveur local avec rechargement automatique (http://localhost:8000)
uv run zensical build   # génère le site statique dans site/
```

Un LLM fait très bien ce travail de mise en place. Un prompt comme :

```text
Crée une documentation Zensical pour mon projet (installation, utilisation,
architecture, référence de l'API à partir des docstrings). Ajoute un Makefile
avec `make doc` pour servir la documentation localement et un workflow GitHub
Actions qui la publie sur GitHub Pages à chaque push sur main.
```

Relisez ensuite ce qui a été généré : un LLM peut décrire des fonctionnalités qui n'existent pas, ou des options en ligne de commande que votre programme ne possède pas.

### Déploiement continu de la documentation

C'est un bon premier exemple de **CD**. Le fichier `.github/workflows/docs.yml` ci-dessous publie la documentation sur GitHub Pages à chaque `push` sur `main`. Il faut au préalable activer *Settings → Pages → Source : GitHub Actions*.

```yaml
name: Documentation

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v5
      - uses: astral-sh/setup-uv@v6
      - run: uv sync --locked
      - run: uv run zensical build --clean
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v4
        with:
          path: site
      - id: deployment
        uses: actions/deploy-pages@v4
```

La documentation est alors accessible à l'adresse `https://<utilisateur>.github.io/<projet>/`.

### Makefile

Un `Makefile` sert de point d'entrée unique pour les commandes courantes du projet. Un nouveau venu n'a pas besoin de connaître les options de chaque outil :

```makefile
.PHONY: install test lint doc build-doc

install:
	uv sync

test:
	uv run pytest --cov --cov-report=term-missing

lint:
	uv run ruff check .
	uv run ruff format --check .

doc:
	uv run zensical serve

build-doc:
	uv run zensical build --clean
```

> ⚠️ Dans un `Makefile`, les lignes de commande doivent être indentées avec une **tabulation**, et non avec des espaces. Sinon, `make` affiche l'erreur `missing separator`.

## Tests de non-régression

Depuis le début du semestre, on utilise `pytest` pour écrire des tests unitaires. Avec `uv` :

```bash
uv run pytest
```

Pour mesurer la **couverture de code** (la proportion des lignes exécutées par les tests), il faut le plugin `pytest-cov` :

```bash
uv add --dev pytest-cov
uv run pytest --cov=mon_paquet --cov-report=term-missing
```

L'option `--cov-report=term-missing` indique les numéros des lignes non couvertes. L'option `--cov-fail-under=80` fait échouer la commande (et donc la CI) si la couverture descend sous 80 %. On ajoute ces commandes au `Makefile` (`make test`) et au workflow de CI, comme ci-dessus.

Une couverture de 100 % ne prouve pas que le code est correct. Elle indique seulement que chaque ligne a été exécutée au moins une fois, et non que le résultat a été vérifié.

### Pourquoi « non-régression » ?

Une **régression**, c'est une fonctionnalité qui fonctionnait et qui ne fonctionne plus après une modification. Les tests de non-régression sont rejoués à chaque modification (d'où l'intérêt de la CI) pour détecter ces régressions immédiatement.

Attention aux tests générés par un LLM **à partir du code existant** : ils décrivent ce que le code *fait*, pas ce qu'il *devrait faire*. Si le code contient un bug, le test généré « figera » ce bug et passera au vert. Exemple :

```python
def moyenne(notes: list[float]) -> float:
    return sum(notes) / (len(notes) + 1)   # bug : + 1 en trop


# Test généré en lisant le code : il passe... et valide le bug !
def test_moyenne():
    assert moyenne([4.0, 5.0, 6.0]) == 3.75
```

Le bon test, écrit à partir de la **spécification** (« la moyenne de 4, 5 et 6 vaut 5 »), aurait échoué :

```python
import pytest

def test_moyenne():
    assert moyenne([4.0, 5.0, 6.0]) == pytest.approx(5.0)
```

En résumé :

- des tests générés à partir du code protègent contre les régressions futures, mais ne prouvent pas que le code actuel est correct ;
- pour tester le bon fonctionnement, écrivez (ou faites écrire) les tests à partir de la **spécification**, idéalement **avant** le code (*Test-Driven Development*) ;
- relisez les assertions des tests générés : ce sont elles qui définissent le comportement attendu ;
- faites toujours des **essais manuels** pour vous assurer que l'application fonctionne comme vous le voulez ;
- quand vous trouvez un bug, commencez par écrire un test qui le reproduit (il échoue), puis corrigez le code (le test passe). Ce bug ne pourra plus revenir sans être détecté.

## Configuration avec un LLM

Claude ne garde aucune mémoire d'une session à l'autre. Tout ce qu'il doit savoir de votre projet doit donc se trouver **dans des fichiers du dépôt**. Les sections suivantes décrivent les fichiers utiles et le rôle de chacun.

### CLAUDE.md

Le fichier `CLAUDE.md`, à la racine du projet, est lu automatiquement au début de chaque session. La commande `/init` en génère un premier jet à partir de votre code. On y met :

- une description courte du projet et de son architecture ;
- les commandes utiles (`make test`, `make doc`, etc.) ;
- les conventions (style, langue des commentaires, structure des dossiers) ;
- des renvois vers les autres documents : « Lis `specs/` avant toute nouvelle fonctionnalité », « Consigne toute décision d'architecture dans `docs/adr/` ».

Gardez-le court et à jour : il est chargé à chaque session et consomme du contexte.

### Spécification

Une bonne approche consiste à commencer un projet par une spécification. Créez un projet vide avec un dossier `specs/` contenant un fichier Markdown. Pas besoin d'écrire dans un français parfait : l'idée est de décrire votre projet, ce que vous voulez et comment vous le voulez. Ajoutez un maximum de détails : utilisateurs visés, fonctionnalités, contraintes, formats d'entrée et de sortie, cas limites, ce qui est **hors périmètre**.

Demandez ensuite à Claude de réécrire la spécification de manière professionnelle, puis **relisez-la** : c'est votre document, pas le sien. Si `CLAUDE.md` y fait référence, Claude s'appuiera sur cette spécification pour vous challenger quand vous lui demanderez une nouvelle fonctionnalité qui la contredit.

### ADR

Un second élément consiste à tenir des **ADR** (*Architecture Decision Records*), par exemple dans `docs/adr/`. Un ADR est un court fichier Markdown qui consigne **une** décision d'architecture importante : le contexte, la décision prise, les alternatives envisagées et les conséquences. Ce format a été popularisé par Michael Nygard en 2011.

```markdown
# 0003 — Utiliser SQLite pour le stockage

- Statut : accepté
- Date : 2026-11-23

## Contexte
L'application est mono-utilisateur et doit fonctionner sans serveur.

## Décision
Les données sont stockées dans une base SQLite locale, via le module standard `sqlite3`.

## Alternatives envisagées
- Fichiers JSON : simple, mais pas de requêtes ni d'accès concurrent sûr.
- PostgreSQL : surdimensionné, nécessite un serveur.

## Conséquences
Pas de dépendance externe ; migration nécessaire si l'application devient multi-utilisateur.
```

Les ADR sont numérotés et ne sont pas réécrits. Si une décision change, on crée un nouvel ADR et on marque l'ancien comme « remplacé par 0007 ». On garde ainsi l'historique du *pourquoi*.

Claude ne le fait pas spontanément. Ajoutez dans `CLAUDE.md` une consigne du type : « Quand nous prenons une décision d'architecture, crée un ADR dans `docs/adr/` ». Lors des sessions suivantes, il relira ces ADR et ne remettra pas en cause des choix déjà tranchés.

### Rôles (sous-agents)

Quand le projet devient conséquent, il devient utile de définir des **rôles** pour vos agents (*subagents*). Chaque sous-agent est un fichier Markdown placé dans `.claude/agents/`. Il possède ses propres instructions, son propre modèle et, surtout, **son propre contexte** : il travaille « à neuf », sans être influencé par la conversation en cours, et ne renvoie que sa conclusion.

Par exemple :

- un **relecteur** qui relit le code modifié et vérifie sa qualité (lisibilité, tests, gestion des erreurs) ;
- un **spec-challenger** qui confronte chaque nouvelle fonctionnalité à la spécification, pour vérifier que vous n'allez pas à l'encontre de vos propres specs.

```markdown
---
name: relecteur
description: Relit le code modifié et signale bugs, manques de tests et problèmes de lisibilité. À utiliser après chaque modification significative.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Tu es un relecteur de code Python exigeant. Pour les fichiers modifiés :
1. Vérifie la correction et les cas limites.
2. Vérifie que chaque fonctionnalité est couverte par un test.
3. Signale le code dupliqué ou inutilement complexe.
Réponds par une liste de problèmes classés par gravité.
```

Le choix du modèle est un compromis entre coût, vitesse et capacité. Dans la famille Claude 5 :

| Modèle         | Profil                          | Usage typique                                   |
| -------------- | ------------------------------- | ----------------------------------------------- |
| **Haiku 5.5**  | petit, rapide, économique       | tâches simples et répétitives, recherche        |
| **Sonnet 5.5** | intermédiaire, bon compromis    | relecture, la plupart des tâches de code        |
| **Opus 5.5**   | le plus capable, le plus cher   | conception, problèmes difficiles, raisonnement  |

Vous pouvez demander à Claude de créer ces rôles pour vous, ou utiliser la commande `/agents`.

### Skills

Chaque fois que vous demandez à Claude une tâche spécifique, comme écrire une documentation avec Zensical, il doit consommer une partie de son contexte pour lire la documentation (voire le code source) de l'outil et réapprendre à s'en servir. C'est lent et gourmand en *tokens*.

La solution consiste à lui demander de créer un **skill**. Un skill est un dossier dans `.claude/skills/` contenant un fichier `SKILL.md`, qui résume comment accomplir une tâche donnée : commandes, conventions, pièges à éviter. Il peut être accompagné de scripts ou de modèles de fichiers.

```markdown
---
name: zensical-docs
description: Créer ou modifier la documentation du projet avec Zensical (zensical.toml, docs/, déploiement GitHub Pages).
---

# Documentation Zensical

- Configuration : `zensical.toml` à la racine.
- Pages : `docs/*.md`, navigation déclarée dans `nav` de `zensical.toml`.
- Prévisualiser : `make doc` ; construire : `make build-doc` (sortie dans `site/`).
- Ne jamais commiter `site/` (déjà dans `.gitignore`).
```

Au démarrage, seuls le nom et la `description` de chaque skill sont chargés. Quand une demande correspond à la description, Claude charge automatiquement le contenu complet du skill. Une description précise est donc essentielle pour que le bon skill soit utilisé au bon moment.

### En résumé

```text
mon-projet/
├── CLAUDE.md                  # lu à chaque session : contexte et consignes
├── specs/                     # ce que le projet doit faire
├── docs/adr/                  # pourquoi il est construit ainsi
├── .claude/
│   ├── agents/                # rôles : relecteur, spec-challenger...
│   └── skills/                # savoir-faire réutilisable
└── .github/workflows/         # CI/CD : tests et déploiement automatiques
```
