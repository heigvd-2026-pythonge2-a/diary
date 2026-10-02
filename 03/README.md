# Semaine 03/16

- [ ] Import de paquets
- [ ] Fonctions
- [ ] Créer un script

## Import de paquets

Un import donne accès au code d'un autre module. `math` est fourni avec Python ; NumPy est une bibliothèque externe à installer dans votre environnement avec `python3 -m pip install numpy`. Avec `import numpy as np`, on utilise ensuite le nom court `np`, par exemple `np.array([1, 2, 3])`.

Les lignes ci-dessous montrent plusieurs façons d'importer : choisissez celle qui convient à votre besoin. Évitez en général `import *`, car les noms ajoutés sont moins faciles à identifier et peuvent remplacer des noms déjà définis.

```python
# Import le namespace numpy dans l'espace courant
import numpy
import numpy as np

# Import sélectif de fonctions du namespace numpy ou math
from numpy import array
from numpy import array as arr
from numpy import *

from math import sqrt, log, exp

# Un import local reporte le chargement au premier appel de la fonction.
# Les appels suivants réutilisent le module déjà chargé.
def function():
    import numpy as np
    return np.array([1, 2, 3])
```

## Fonctions

Une fonction regroupe des instructions réutilisables. `def` la définit, les paramètres reçoivent les valeurs de l'appel et `return` renvoie un résultat. L'indentation délimite son contenu. Chaque exemple ci-dessous est indépendant : redéfinir `f` remplace sa définition précédente.

```python
# Deux choix pour une fonction vide, l'ellipse ou le pass
def f():
    ...

def f():
    pass

# Sans return exécuté, une fonction retourne None
def f():
    from random import randint
    if randint(0, 1):
        return 42

# Un paramètre positionnel
def f(a):
    return a * 2

# Deux paramètres positionnels
def f(a, b):
    return (a, b)

f(1,2)
f(1, b=2)
f(b=2, a=1)
p = {'a': 23, 'b': 42}
f(**p)

# Un paramètre par défaut
def f(a, b=42):
    return (a, b)

>>> f(1)
(1, 42)

>>> f(1, 2)
(1, 2)

# Une fonction générique
def f(*args, **kwargs):
    return (args, kwargs)
```

Les arguments peuvent être passés dans l'ordre (`f(1, 2)`) ou par leur nom (`f(b=2, a=1)`). Une valeur par défaut est utilisée si l'argument est omis. `*args` recueille les arguments positionnels dans un tuple et `**kwargs` les arguments nommés dans un dictionnaire. À l'appel, `f(**p)` répartit les entrées du dictionnaire `p` entre les paramètres.

### Proxy d'une fonction

Une fonction peut aussi être passée comme argument à une autre fonction. Ici, `debug` affiche les arguments, appelle la fonction reçue, puis affiche et renvoie son résultat. Par exemple, `debug(f, 2, 3)` renvoie `5`.

```python
def f(a, b):
    return a + b

def debug(function, *args, **kwargs):
    print(args, kwargs)
    r = function(*args, **kwargs)
    print(r)
    return r
```

## Zip

La fonction `zip` permet de regrouper des éléments de plusieurs itérables. Elle retourne un itérateur de tuples, où le i-ème tuple contient le i-ème élément de chaque itérable passé en argument.

Un itérable est un objet que l'on peut parcourir, comme une liste ou une chaîne de caractères. `zip` produit les couples au fur et à mesure : `list(...)` permet de tous les afficher et `dict(...)` de construire un dictionnaire à partir de couples clé/valeur. Par défaut, `zip` s'arrête au plus court des itérables.

```python
In [11]: a = [1,2,3,4]

In [12]: b = 'abcd'

In [13]: list(zip(b,a))
Out[13]: [('a', 1), ('b', 2), ('c', 3), ('d', 4)]

In [14]: zip(b,a)
Out[14]: <zip at 0x756da6f13180>

In [15]: dict(zip(b,a))
Out[15]: {'a': 1, 'b': 2, 'c': 3, 'd': 4}

In [16]: zip(*list(zip(b,a)))
Out[16]: <zip at 0x756da6a142c0>

In [17]: list(zip(*list(zip(b,a))))
Out[17]: [('a', 'b', 'c', 'd'), (1, 2, 3, 4)]
```

Dans le dernier exemple, `*` déplie la liste de couples en arguments séparés : `zip` regroupe alors les lettres d'un côté et les nombres de l'autre. Les préfixes `In` et `Out` viennent d'IPython ; pour essayer ces exemples dans un script, recopiez uniquement les expressions et utilisez `print(...)` pour afficher les résultats.

## Créer un script

Un script est un fichier `.py` contenant des instructions exécutées dans l'ordre. Pour essayer dans `script.py` :

```python
import numpy as np

def main():
    valeurs = np.array([1, 2, 3])
    print(valeurs * 2)

if __name__ == "__main__":
    main()
```

Depuis le dossier `03`, lancez `python3 script.py` : cet exemple affiche `[2 4 6]`. Le bloc `if __name__ == "__main__":` appelle `main()` lorsque le fichier est lancé directement, mais pas lorsqu'il est importé par un autre fichier.
