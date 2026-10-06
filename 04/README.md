# Semaine 04/16

- [x] Création d'un projet Python
- [x] Utilisation de `uv`
- [x] Rôle de `__name__` et `__main__`
- [x] Rôle de `__init__.py`
- [x] Exercice sur les paramètres de fonctions

- [ ] Notion de Classe et d'Objet

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

Un **environnement virtuel** est un dossier (`.venv`) qui contient une copie isolée de Python et des bibliothèques installées pour *ce* projet uniquement. Ainsi, deux projets peuvent utiliser des versions différentes d'une même bibliothèque sans se perturber. UV le crée et l'active automatiquement : vous n'avez pas à vous en occuper.

Le fichier `pyproject.toml` décrit le projet (nom, version, version de Python requise, dépendances). Le fichier `uv.lock` fige les versions exactes installées, pour que tout le monde obtienne le même résultat.

Pour créer un projet avec UV, il suffit de lancer la commande suivante:

```bash
uv init mon_projet # Crée le dossier mon_projet avec la structure standardisée
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
uv run python nom_du_fichier.py # Lance la commande dans l'environnement du projet
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

### Pourquoi `__name__ == "__main__"` ?

Imaginez un fichier `maths.py` contenant des fonctions utiles ainsi que quelques lignes de test. Quand un autre fichier fait `import maths`, Python **exécute tout le fichier** : les lignes de test s'exécuteraient aussi, ce qui n'est pas souhaité. Le test `if __name__ == "__main__":` permet de dire : « exécute ce bloc seulement si on lance ce fichier directement, pas si on l'importe ».

```python
# maths.py
def carre(x):
    return x * x

if __name__ == "__main__":
    print(carre(4))  # affiché avec `python -m maths`, mais pas avec `import maths`
```

> **À retenir :** un fichier Python peut être à la fois une *bibliothèque* (on l'importe) et un *programme* (on l'exécute). Le `if __name__ == "__main__":` sépare les deux rôles.

### Package vs module

- **Module** : un seul fichier `.py`.
- **Package** : un répertoire de modules, reconnu grâce à `__init__.py`.

On importe ensuite avec la notation pointée : `from module.sous_module1 import ma_fonction`. Le fichier `__init__.py` est exécuté **une seule fois**, à la première importation du package. On l'utilise parfois pour exposer directement les éléments importants : avec `from .sous_module1 import ma_fonction` dans `__init__.py`, l'utilisateur peut écrire `from module import ma_fonction`.

## Paramètres de fonctions

Une fonction peut recevoir ses arguments de plusieurs manières. Il faut distinguer :

- **paramètre** : le nom dans la définition (`def f(a, b)`) ;
- **argument** : la valeur fournie lors de l'appel (`f(1, 2)`).

```python
def presenter(nom, age=18, *hobbies, ville="Yverdon", **extras):
    print(nom, age, hobbies, ville, extras)

presenter("Alice")                          # Alice 18 () Yverdon {}
presenter("Bob", 20, "ski", "lecture")      # Bob 20 ('ski', 'lecture') Yverdon {}
presenter("Eve", ville="Lausanne", job="dev")  # Eve 18 () Lausanne {'job': 'dev'}
```

| Syntaxe | Nom | Rôle |
| --- | --- | --- |
| `def f(a, b)` | paramètres positionnels | obligatoires, l'ordre compte |
| `def f(a, b=10)` | valeur par défaut | optionnel, `b` vaut 10 si omis |
| `def f(*args)` | arguments variables | `args` est un **tuple** de tous les arguments positionnels restants |
| `def f(**kwargs)` | arguments nommés variables | `kwargs` est un **dictionnaire** des arguments nommés restants |
| `def f(a, /, b, *, c)` | restrictions | `a` uniquement positionnel, `c` uniquement nommé |

Deux pièges classiques :

1. Les paramètres avec valeur par défaut viennent **après** ceux sans valeur par défaut.
2. Ne jamais utiliser une valeur par défaut *modifiable* (liste, dictionnaire) : elle est créée **une seule fois** et partagée entre tous les appels.

```python
def ajouter(x, liste=[]):      # ❌ la même liste est réutilisée à chaque appel
    liste.append(x)
    return liste

def ajouter(x, liste=None):    # ✅ on crée une nouvelle liste à chaque appel
    if liste is None:
        liste = []
    liste.append(x)
    return liste
```

## Classe et objet

Une classe c'est "un plan de fabrication". Un objet c'est la réalisation du 
plan. 

Défini une classe -> Instancie un objet -> on obtient une instance

Pour faire une analogie : le plan d'une maison (la classe) décrit combien il y a de pièces et comment elles sont agencées. Avec ce même plan, on peut construire plusieurs maisons (les objets). Chaque maison a ses propres caractéristiques (couleur des volets, adresse…), mais toutes suivent le même plan.

Une classe regroupe deux choses :

- des **attributs** : les données de l'objet (ce qu'il *a*), par exemple `x` et `y` pour un vecteur ;
- des **méthodes** : les actions de l'objet (ce qu'il *fait*), ce sont des fonctions définies dans la classe.

```python
class Chien:
    def __init__(self, nom):      # constructeur : appelé à la création de l'objet
        self.nom = nom            # attribut

    def aboyer(self):             # méthode
        print(f"{self.nom} dit : Wouf !")

rex = Chien("Rex")     # instanciation : on crée un objet (une instance)
medor = Chien("Médor") # un second objet, indépendant du premier
rex.aboyer()           # Rex dit : Wouf !
```

### Le rôle de `self`

`self` désigne **l'objet sur lequel on appelle la méthode**. Python le passe automatiquement comme premier argument : `rex.aboyer()` est équivalent à `Chien.aboyer(rex)`. C'est grâce à `self` que `rex` et `medor` peuvent avoir chacun leur propre `nom`.

### `__init__`, le constructeur

`__init__` est appelée automatiquement juste après la création de l'objet. Elle sert à **initialiser les attributs**. Attention à ne pas la confondre avec le fichier `__init__.py` vu plus haut : même nom, rôles différents.

## Itérables et itérateurs

Un **itérable** est un objet que l'on peut parcourir avec une boucle `for` : liste, tuple, chaîne de caractères, dictionnaire, fichier, etc.

```python
for lettre in "abc":
    print(lettre)
```

Que fait Python en coulisses ? Il applique un protocole en deux étapes :

1. Il appelle `iter(objet)`, qui appelle la méthode `__iter__` et renvoie un **itérateur**.
2. Il appelle répétitivement `next(iterateur)`, qui appelle la méthode `__next__`, jusqu'à ce que `StopIteration` soit levée : la boucle s'arrête alors.

```python
it = iter([10, 20])
print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # StopIteration
```

- **Itérable** : possède `__iter__` (peut fournir un itérateur).
- **Itérateur** : possède `__next__` (sait donner l'élément suivant et se souvient où il en est).

Un itérateur ne se parcourt qu'**une seule fois** : une fois épuisé, il faut en créer un nouveau.

### Les générateurs et `yield`

Écrire un itérateur à la main est fastidieux. Le mot-clé `yield` permet de le faire simplement : la fonction **se met en pause** à chaque `yield`, renvoie une valeur, puis reprend là où elle s'était arrêtée au prochain appel.

```python
def compte_a_rebours(n):
    while n > 0:
        yield n
        n -= 1

for i in compte_a_rebours(3):
    print(i)  # 3, 2, 1
```

C'est exactement ce que fait `Vector.__iter__` ci-dessous : il « produit » `x` puis `y`.

## Méthodes spéciales ("dunder")

Les méthodes dont le nom commence et finit par deux underscores (`__init__`, `__len__`…) sont appelées **méthodes spéciales** ou *dunder* (*double underscore*). On ne les appelle généralement pas directement : c'est Python qui les appelle à notre place quand on utilise une syntaxe particulière. Les implémenter permet à nos objets de se comporter comme les types natifs.

| Vous écrivez | Python appelle | Rôle |
| --- | --- | --- |
| `Vector(1, 2)` | `__init__` | initialiser l'objet |
| `len(v)` | `__len__` | nombre d'éléments |
| `v[0]`, `v['x']` | `__getitem__` | lire un élément |
| `v[0] = 5` | `__setitem__` | modifier un élément |
| `for c in v` | `__iter__` | parcourir l'objet |
| `v + w` | `__add__` | addition |
| `v * 2` | `__mul__` | multiplication (objet à gauche) |
| `2 * v` | `__rmul__` | multiplication (objet à droite) |
| `str(v)`, `print(v)` | `__str__` | affichage lisible pour l'utilisateur |
| `repr(v)` | `__repr__` | affichage sans ambiguïté pour le développeur |

> **`__str__` vs `__repr__`** : `__str__` s'adresse à l'utilisateur final, `__repr__` au développeur (idéalement, il montre comment recréer l'objet). Si `__str__` n'est pas défini, Python utilise `__repr__`.

## Exemple d'un vecteur

L'exemple suivant rassemble tous les concepts du chapitre : une classe qui se comporte comme une séquence de deux nombres, que l'on peut indexer, parcourir, additionner et multiplier.

Points à observer dans le code :

- `_KEYS` est un attribut **de classe** (partagé par toutes les instances), alors que `self.x` et `self.y` sont des attributs **d'instance**.
- Le préfixe `_` (comme dans `_index` ou `_KEYS`) est une convention : « usage interne, ne pas utiliser de l'extérieur ».
- `__getitem__` accepte un entier, une chaîne (`'x'`) ou une tranche (`slice`) : `v[0]`, `v['y']` et `v[0:2]` fonctionnent.
- `__mul__` renvoie `NotImplemented` (et non une erreur) quand il ne sait pas gérer le type : Python essaie alors l'opération inverse avant de lever `TypeError`.
- `__rmul__ = __mul__` rend la multiplication commutative : `2 * v` donne le même résultat que `v * 2`.
- Les annotations de type (`float`, `-> None`…) documentent le code mais ne sont **pas vérifiées** à l'exécution.

```python
from __future__ import annotations

from collections.abc import Iterator, Sequence
from numbers import Number


class Vector:
    _KEYS: dict[str, int] = {'x': 0, 'y': 1}

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __len__(self) -> int:
        return 2

    def _index(self, key: int | str | slice) -> int | slice:
        """Normalise une clé textuelle en indice, laisse passer le reste."""
        if isinstance(key, str):
            try:
                return self._KEYS[key]
            except KeyError:
                raise KeyError(key) from None
        return key

    def __getitem__(self, key: int | str | slice) -> float | tuple[float, ...]:
        return (self.x, self.y)[self._index(key)]

    def __setitem__(self, key: int | str, value: float) -> None:
        i = self._index(key)
        if i in (0, -2):
            self.x = value
        elif i in (1, -1):
            self.y = value
        else:
            raise IndexError("Index hors limites")

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    def __add__(self, other: Sequence[float]) -> Vector:
        return Vector(self.x + other[0], self.y + other[1])

    def __mul__(self, scalar: float) -> Vector:
        if not isinstance(scalar, Number):
            return NotImplemented
        return Vector(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def __str__(self) -> str:
        return "prout"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
```

Pour l'essayer dans l'interpréteur :

```python
>>> v = Vector(1, 2)
>>> len(v)
2
>>> v['x'], v[1]
(1, 2)
>>> list(v)          # utilise __iter__
[1, 2]
>>> v + (10, 10)     # utilise __add__
(11, 12)
>>> 3 * v            # utilise __rmul__
(3, 6)
>>> print(v)         # utilise __str__
prout
```

## Exercice

Créer une classe `Duck` et ajouter les méthodes (actions) `quack`, `eat`, `sleep`. Et l'attribut name

```python
>>> donald = Duck('Trump')
>>> donald.sleep()
Trump is sleeping... ZZZzzzzzZZZzzz
```

**Indications :**

1. Définissez la classe avec `class Duck:`.
2. Dans `__init__(self, name)`, stockez le nom : `self.name = name`.
3. Chaque méthode prend `self` en premier paramètre, ce qui permet d'accéder à `self.name`.
4. Utilisez une f-string pour l'affichage : `print(f"{self.name} is sleeping...")`.
5. Pour tester, placez votre code de démonstration sous `if __name__ == "__main__":`.