# Semaine 04/16

- [x] Création d'un projet Python
- [x] Utilisation de `uv`
- [x] Rôle de `__name__` et `__main__`
- [x] Rôle de `__init__.py`
- [x] Exercice sur les paramètres de fonctions

- [ ] Notion d'itérable
- [ ] Variables cachées (`__iter__`, `__next__`, `__getitem__`, `__len__`)

## Création d'un projet Python

En Python, un projet est généralement un répertoire contenant un ensemble de fichiers. On y retrouve notament:

- Un fichier `README.md` qui contient des informations sur le projet: comment l'installer, comment l'utiliser, etc.
- Un fichier `.gitignore` qui contient la liste des fichiers et répertoires à ignorer par Git.
- Un fichier `pyproject.toml` qui contient les informations sur le projet et ses dépendances (créé avec `uv`).
- Un répertoire `src` qui contient le code source du projet.
- Un répertoire `tests` qui contient les tests du projet.

### `.gitignore`

Le fichier `.gitignore` est utilisé pour indiquer à Git quels fichiers ou répertoires doivent être ignorés. Cela permet d'éviter de versionner des fichiers temporaires, des fichiers de configuration locaux, ou des dépendances installées. Traditionnellement en Python on ignore les fichiers suivants:

- `__pycache__/` : répertoire contenant les fichiers compilés Python.
- `*.pyc` : fichiers compilés Python.
- `*.pyo` : fichiers optimisés Python.
- `*.pyd` : fichiers de dépendance Python.

Selon le langage, par exemple en C ou C++, on ignore aussi les fichiers `*.o` (fichiers objets) et `*.out` (fichiers exécutables).

### `README.md`

Le fichier `README.md` est un fichier texte au format Markdown qui contient des informations sur le projet. Il est généralement utilisé pour expliquer comment installer et utiliser le projet, ainsi que pour fournir des informations sur la licence, les contributeurs, etc. Il doit être concis et clair, et doit donner envie aux utilisateurs de découvrir le projet.

1. C'est quoi le projet ?
2. Ca sert à quoi ?
3. Comment l'installer ?
4. Comment l'utiliser ?

### UV

UV est l'outil de gestion de projet Python qui permet de créer un projet avec une structure standardisée. Il permet également de gérer les dépendances et de créer des environnements virtuels.
Pour créer un projet avec UV, il suffit de lancer la commande suivante:

```bash
uv new mon_projet # Crée le dossier mon_projet avec la structure standardisée
```

Ou bien, si vous êtes déjà dans le dossier du projet, vous pouvez lancer la commande suivante:

```bash
uv init # Initialise le projet avec la structure standardisée
```

Pour ajouter une dépendance, il suffit de lancer la commande suivante:

```bash
uv add nom_de_la_dependance # Ajoute la dépendance au projet par exempl uv add numpy
```

Ensuite pour lancer le projet, il suffit de lancer la commande suivante:

```bash
uv run # Lance le projet
```

Vous pouvez également lancer le projet avec un fichier spécifique en utilisant la commande suivante:

```bash
uv run nom_du_fichier.py # Lance le projet avec le fichier spécifié
```

Ou une commande spécifique en utilisant la commande suivante:

```bash
uv run "python nom_du_fichier.py" # Lance le projet avec la commande spécifiée
```

## Rôle de `__name__` et `__main__`

En Python, chaque fichier est un module. Lorsqu'un fichier est exécuté directement, Python lui attribue le nom spécial `__main__`. Cela permet de distinguer si le fichier est exécuté directement ou s'il est importé en tant que module dans un autre fichier.

La variable `__name__` contient le nom du module. Si le fichier est exécuté directement, `__name__` vaut `"__main__"`. Si le fichier est importé en tant que module, `__name__` vaut le nom du module. Essayez d'exécuter le code suivant dans un fichier `mon_module.py`:

```python
# mon_module.py
print(f"Nom du module: {__name__}")
if __name__ == "__main__":
    print("Le fichier est exécuté directement.")
```

Et essayez les deux commandes suivantes:

```bash
python -m mon_module # Exécute le fichier directement
```

```bash
python -c "import mon_module" # Importe le module sans l'exécuter directement
```

## Rôle de `__init__.py`

Lorsque votre projet à plusieurs fichiers, il est souvent utile de les regrouper dans un répertoire. Pour que Python considère ce répertoire comme un package, il faut y ajouter un fichier `__init__.py`. Ce fichier peut être vide, mais il peut également contenir du code d'initialisation pour le package.

```text
mon_projet/
├── module/
│   ├── __init__.py      # Indique que le répertoire est un package
│   ├── sous_module1.py
│   └── sous_module2.py
```

