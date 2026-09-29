# Semaine 03/16

- [ ] Import de paquets
- [ ] Fonctions
- [ ] Crée un script

## Import de paquets

```python
# Import le namespace numpy dans l'espace courant
import numpy
import numpy as np

# Import sélectif de fonctions du namespace numpy ou math
from numpy import array
from numpy import array as arr
from numpy import *

from math import sqrt, log, exp

# Avantage : chargement global du programme plus rapide
# Inconvénient : chargement de la fonction plus longue 
def function():
    import numpy as np
    return np.array([1, 2, 3])
```

## Fonctions

```python
# Deux choix pour une fonction vide, l'ellipse ou le pass
def f():
    ...

def f():
    pass

# Une fonction par défaut retourne None
def f():
    if rand() % 2:
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

### Proxy d'une fonction

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