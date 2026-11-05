# Semaine 07/16

- [ ] Paquet Pint
- [ ] Interface en ligne de commande
  - [ ] Argparse
  - [ ] Click
  - [ ] Typer
- [ ] Expressions régulières
  - [ ] Introduction
  - [ ] Syntaxe
  - [ ] Fonctions
  - [ ] Exemples

## Pint

Pour illustrer au mieux l'intérêt des modules Python, on peut présenter le module [Pint](https://pint.readthedocs.io/en/stable/). Ce module permet de gérer les unités de mesure et les conversions entre elles. Il est particulièrement utile pour les applications scientifiques et d'ingénierie.

Admettons que l'on souhaite tester et/ou utiliser ce module. La procédure est la suivante:

1. On crée un dossier de test
2. On crée un environnement virtuel dans ce dossier
3. On installe le module Pint dans cet environnement virtuel
4. On teste le module en créant un fichier Python ou depuis un terminal REPL

```bash
$ mkdir test-pint
$ cd test-pint
$ uv init
$ uv add pint ipython
$ uv run ipython
```

Depuis Python, on peut alors tester le module Pint:

```python
>>> import pint
>>> ureg = pint.UnitRegistry()
>>> distance = 10 * ureg.meter
>>> time = 5 * ureg.second
>>> speed = distance / time
>>> print(speed)
2.0 meter / second
```

Pint est pratique pour la conversion d'unités hybrides, ajouter des inches à des centimètres, ou encore pour gérer des unités de mesure complexes. Il est également possible de définir ses propres unités et de les utiliser dans les calculs.

## Interface en ligne de commande (CLI)

Dès qu'un script Python est écrit on souhaite avoir une interraction propre avec le terminal. Cela implique de:

- Renseigner l'utilisateur de comment utiliser le script
- Donner accès à une aide
- Gérer les arguments et options passés au script

En C, il faut manuellement gérer `argc` et `argv`. En Python, il existe des modules pour gérer cela de manière plus simple. Les quatre principaux sont:

1. `sys`: module standard de Python pour accéder aux arguments de la ligne de commande
2. `argparse`: module standard de Python pour gérer les arguments de la ligne de commande (hérité de `optparse`)
3. `click`: module externe pour créer des interfaces en ligne de commande
4. `typer`: module externe plus récent pour créer des interfaces en ligne de commande

Voyons donc ensemble ces différents modules et comment les utiliser pour créer des interfaces en ligne de commande. On imagine un programme de résolution de l'équation quadratique:

```bash
$ solve-quadratic -- 1 2 -3
1.0 -3.0

$ solve-quadratic -i -v -- 1 2 -3
x1 = 1.0
x2 = -3.0

$ solve-quadratic -i -vv -- 1 2 -3
Les solutions de l'équation quadratique 1x^2 + 2x - 3 = 0 sont:
x1 = 1.0
x2 = -3.0
```

L'option `-i` indique que l'on veut indiquer les solutions imaginaires. L'option `-v` pour *verbose* est cumulative et peut être répétée pour augmenter le niveau de verbosité. Par exemple `-vvv` très verbeux.

Le `--` est une bizarre convention des terminaux pour indiquer que les arguments suivants ne sont pas des options mais des arguments positionnels. Dans notre exemple, les trois derniers arguments sont les coefficients de l'équation quadratique. Il est nécessaire ici sinon le terminal pourrait interpréter `-3` comme une option et non comme un argument. Cet argument `--` est donc lu par le script et non par le terminal, c'est à lui de l'interpréter.

Enfin les arguments positionnels sont les coefficients de l'équation quadratique.

Pour ne pas répéter la résolution et l'affichage dans chaque variante, on place ce code dans un module `quad.py` que tous les scripts importent. Seule la lecture de la ligne de commande change d'un exemple à l'autre.

```python
# quad.py
import cmath
import math


def solve_quadratic(a, b, c, imaginary=False):
    """Retourne les racines de ax^2 + bx + c = 0 (tuple vide si aucune)."""
    if a == 0:
        raise ValueError("a doit être non nul")
    delta = b * b - 4 * a * c
    if delta < 0 and not imaginary:
        return ()
    root = cmath.sqrt(delta) if delta < 0 else math.sqrt(delta)
    return ((-b + root) / (2 * a), (-b - root) / (2 * a))


def equation(a, b, c):
    """Formate l'équation, p. ex. '1x^2 + 2x - 3 = 0'."""
    text = f"{a:g}x^2"
    for coef, var in ((b, "x"), (c, "")):
        sign = "-" if coef < 0 else "+"
        text += f" {sign} {abs(coef):g}{var}"
    return text + " = 0"


def show(solutions, a, b, c, verbose=0):
    """Affiche les solutions selon le niveau de verbosité."""
    if verbose >= 2:
        print(f"Les solutions de l'équation quadratique {equation(a, b, c)} sont:")
    if not solutions:
        print("aucune solution réelle")
    elif verbose == 0:
        print(*solutions)
    else:
        for i, x in enumerate(solutions, 1):
            print(f"x{i} = {x}")
```

### sys et argv

Le module système de Python donne accès à la liste `argv` qui contient les arguments passés au script. C'est exactement le même contenu que ce que l'on aurait en C avec `argc` et `argv`. Le premier élément de la liste est le nom du script, et les éléments suivants sont les arguments passés au script. Il n'y a plus de `argc` pour compter le nombre d'arguments car une liste Python est dynamique et peut être parcourue avec une boucle `for` et donc contient déjà une longueur.

```python
# quad-sys.py
import sys
from quad import solve_quadratic, show

USAGE = "usage: quad-sys.py [-h] [-i] [-v] [--] a b c"


def main(argv):
    imaginary, verbose, positional = False, 0, []
    args = iter(argv[1:])
    for arg in args:
        if arg == "--":
            positional += list(args)  # tout ce qui suit est positionnel
        elif arg in ("-h", "--help"):
            print(USAGE)
            return 0
        elif arg.startswith("-"):
            for flag in arg[1:]:  # permet -vv ou -iv
                if flag == "i":
                    imaginary = True
                elif flag == "v":
                    verbose += 1
                else:
                    print(f"option inconnue: -{flag}", file=sys.stderr)
                    return 2
        else:
            positional.append(arg)

    if len(positional) != 3:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        a, b, c = map(float, positional)
    except ValueError:
        print("les coefficients doivent être des nombres", file=sys.stderr)
        return 2
    if a == 0:
        print("a doit être non nul", file=sys.stderr)
        return 2

    show(solve_quadratic(a, b, c, imaginary), a, b, c, verbose)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

```bash
$ python quad-sys.py -i -vv -- 1 2 -3
Les solutions de l'équation quadratique 1x^2 + 2x - 3 = 0 sont:
x1 = 1.0
x2 = -3.0
```

Tout est à la charge du programmeur: reconnaître le `--`, accepter les options groupées (`-iv`), compter les `-v`, vérifier le nombre d'arguments, convertir les chaînes en nombres, afficher l'usage et choisir un code de retour. Le code fonctionne, mais plus de la moitié ne concerne pas le problème à résoudre. C'est le même constat qu'en C.

### argparse

Plutôt que de gérer manuellement tous les cas de figure, la position des arguments et des options, on utilise argparse. On *déclare* les arguments et les options attendus, et le module se charge de lire `sys.argv`, de convertir les valeurs, de générer l'aide (`-h`/`--help`) et d'afficher les erreurs avec le bon code de retour.

```python
# quad-argparse.py
import argparse
from quad import solve_quadratic, show


def main():
    parser = argparse.ArgumentParser(description="Résout l'équation ax^2 + bx + c = 0")
    parser.add_argument("a", type=float, help="coefficient de x^2")
    parser.add_argument("b", type=float, help="coefficient de x")
    parser.add_argument("c", type=float, help="terme constant")
    parser.add_argument("-i", "--imaginary", action="store_true",
                        help="afficher les solutions complexes")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="augmente la verbosité (cumulable)")
    args = parser.parse_args()

    if args.a == 0:
        parser.error("a doit être non nul")

    solutions = solve_quadratic(args.a, args.b, args.c, args.imaginary)
    show(solutions, args.a, args.b, args.c, args.verbose)


if __name__ == "__main__":
    main()
```

Quelques points à noter:

- `type=float` convertit l'argument et produit une erreur propre si ce n'est pas un nombre.
- `action="store_true"` définit un drapeau booléen, `action="count"` compte les répétitions (`-vv` donne 2).
- Le `--` est compris nativement. Argparse accepte même `1 2 -3` sans `--` tant qu'aucune option ne ressemble à un nombre négatif.
- `parser.error()` affiche l'usage et le message, puis quitte avec le code 2.

```bash
$ python quad-argparse.py --help
usage: quad-argparse.py [-h] [-i] [-v] a b c

Résout l'équation ax^2 + bx + c = 0

positional arguments:
  a                coefficient de x^2
  b                coefficient de x
  c                terme constant

options:
  -h, --help       show this help message and exit
  -i, --imaginary  afficher les solutions complexes
  -v, --verbose    augmente la verbosité (cumulable)

$ python quad-argparse.py -i -v -- 1 2 -3
x1 = 1.0
x2 = -3.0
```

### click

Click utilise un mécanisme puissant de Python appelé *decorators*. Un décorateur est une fonction qui prend une autre fonction en argument et qui retourne une nouvelle fonction. Cela permet de modifier le comportement d'une fonction sans la modifier directement. Dans le cas de Click, les décorateurs sont utilisés pour définir les options et les arguments d'une commande. Click n'est pas dans la bibliothèque standard, il faut l'ajouter au projet avec `uv add click`.

```python
# quad-click.py
import click
from quad import solve_quadratic, show


@click.command(help="Résout l'équation ax^2 + bx + c = 0")
@click.argument("a", type=float)
@click.argument("b", type=float)
@click.argument("c", type=float)
@click.option("-i", "--imaginary", is_flag=True,
              help="afficher les solutions complexes")
@click.option("-v", "--verbose", count=True,
              help="augmente la verbosité (cumulable)")
def main(a, b, c, imaginary, verbose):
    if a == 0:
        raise click.BadParameter("a doit être non nul", param_hint="a")
    show(solve_quadratic(a, b, c, imaginary), a, b, c, verbose)


if __name__ == "__main__":
    main()
```

Les décorateurs se lisent de bas en haut: chaque `@click.argument` ou `@click.option` ajoute un paramètre, et `@click.command` transforme la fonction en commande. Les noms des paramètres de `main` doivent correspondre aux noms déclarés (`imaginary`, `verbose`). `is_flag=True` correspond au `store_true` d'argparse et `count=True` à `action="count"`. Un seul bémol: contrairement à argparse, click ne devine pas qu'un `-3` est un nombre, le `--` est donc obligatoire.

```bash
$ python quad-click.py --help
Usage: quad-click.py [OPTIONS] A B C

  Résout l'équation ax^2 + bx + c = 0

Options:
  -i, --imaginary  afficher les solutions complexes
  -v, --verbose    augmente la verbosité (cumulable)
  --help           Show this message and exit.

$ python quad-click.py -i -vv -- 1 2 -3
Les solutions de l'équation quadratique 1x^2 + 2x - 3 = 0 sont:
x1 = 1.0
x2 = -3.0
```

### typer

Typer est un module plus récent qui utilise les annotations de type de Python pour définir les arguments et les options d'une commande. Il est basé sur Click et offre une syntaxe plus simple et plus lisible. Il offre des couleurs et des messages d'erreur plus clairs, ainsi qu'une meilleure intégration avec les IDE. Il s'installe avec `uv add typer`.

```python
# quad-typer.py
from typing import Annotated
import typer
from quad import solve_quadratic, show


def main(
    a: Annotated[float, typer.Argument(help="coefficient de x^2")],
    b: Annotated[float, typer.Argument(help="coefficient de x")],
    c: Annotated[float, typer.Argument(help="terme constant")],
    imaginary: Annotated[bool, typer.Option("-i", "--imaginary",
                         help="afficher les solutions complexes")] = False,
    verbose: Annotated[int, typer.Option("-v", "--verbose", count=True,
                       help="augmente la verbosité (cumulable)")] = 0,
):
    """Résout l'équation ax^2 + bx + c = 0"""
    if a == 0:
        raise typer.BadParameter("a doit être non nul")
    show(solve_quadratic(a, b, c, imaginary), a, b, c, verbose)


if __name__ == "__main__":
    typer.run(main)
```

Ici plus de décorateurs: la signature de la fonction *est* l'interface. Un paramètre sans valeur par défaut devient un argument positionnel, un paramètre avec valeur par défaut devient une option. Le type Python (`float`, `bool`, `int`) sert à la conversion et à la validation. `Annotated` permet d'attacher les métadonnées (nom court `-i`, texte d'aide, `count=True`) sans altérer le type, ce qui garde la fonction utilisable et testable comme n'importe quelle fonction Python. La *docstring* devient la description de la commande.

```bash
$ python quad-typer.py --help
 Usage: quad-typer.py [OPTIONS] {a} {b} {c}

 Résout l'équation ax^2 + bx + c = 0

╭─ Arguments ──────────────────────────────────────────────────────────╮
│ *    a      <float>  coefficient de x^2 [required]                   │
│ *    b      <float>  coefficient de x [required]                     │
│ *    c      <float>  terme constant [required]                       │
╰──────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────╮
│ --imaginary  -i             afficher les solutions complexes         │
│ --verbose    -v      <int>  augmente la verbosité (cumulable)        │
│                             [default: 0]                             │
│ --help                      Show this message and exit.              │
╰──────────────────────────────────────────────────────────────────────╯

$ python quad-typer.py -i -vv -- 1 2 -3
Les solutions de l'équation quadratique 1x^2 + 2x - 3 = 0 sont:
x1 = 1.0
x2 = -3.0
```

Pour résumer, `sys.argv` convient à un script jetable, `argparse` est le choix par défaut puisqu'il ne nécessite aucune dépendance, et `click` ou `typer` s'imposent dès que l'interface grossit (sous-commandes, couleurs, complétion du shell).

## Expressions régulières

Les expressions régulières (ou regex) sont un outil extrèmement puissant pour rechercher, extraire et manipuler des chaînes de caractères. Elles permettent de définir des motifs (patterns) que l'on souhaite trouver dans une chaîne. Python fournit le module `re` pour travailler avec les expressions régulières.

Elles existent depuis au moins 1968 et sont utilisées dans de nombreux langages de programmation et outils. Elles sont de plus en plus méconnues car elles sont souvent perçues comme complexes et difficiles à lire, et depuis l'avènement des IDE modernes, quelques clics supplémentaires et du temps permettent avec moins de compétences de faire les choses à la main. Néanmoins elles restent un outil incontournable pour le traitement de texte, la validation de données, l'extraction d'informations et bien d'autres tâches.

Les enseigner en profondeur ce serait un cours à part entière. Le livre [Mastering Regular Expressions, 3rd Edition](https://www.oreilly.com/library/view/mastering-regular-expressions/0596528124/) de 542 pages est une référence incontournable. Il est très complet et couvre de nombreux aspects des expressions régulières, y compris les subtilités et les pièges à éviter.

Pour cette introduction restons simple et utilisons l'outil en ligne [regex101](https://regex101.com/) pour tester nos expressions régulières. Il permet de visualiser les correspondances, de comprendre les motifs et de déboguer les regex.

### Les motifs de base

Prenons une chaîne de caractère simple:

```text
Bonjour, je m'appelle Alice. J'ai 30 ans et j'habite à Paris.
```

Si on souhaite chercher toutes les occurences de la lettre `a` on utilise le motif `a`. Si je cherche le mot `Alice`, le motif est `Alice`. Par contre de nombreux caractères sont réservés et ont une signification particulière, cela ne marche pas avec tous les caractères et nous le verrons.

Si je souhaite chercher tous les mots qui commencent par une majuscule, je peux utiliser le motif `[A-Z][a-z]+`. Cela signifie:

- `[]`: définit une classe de caractères (n'importe quel caractère à l'intérieur des crochets)
- `+`: indique que le caractère précédent (ou la classe) doit apparaître une ou plusieurs fois

Donc `[A-Z]` correspond à une majuscule, et `[a-z]+` correspond à une ou plusieurs lettres minuscules. Ainsi, le motif `[A-Z][a-z]+` correspond à tous les mots qui commencent par une majuscule suivie de lettres minuscules (voir l'exemple sur [regex101](https://regex101.com/?regex=%5BA-Z%5D%5Ba-z%5D%2B&testString=Bonjour%2C+je+m%27appelle+Alice.+J%27ai+30+ans+et+j%27habite+%C3%A0+Paris.%0A&flags=gm&flavor=pcre2&delimiter=%2F)).

Si je souhaite chercher tous les nombres dans la chaîne, je peux utiliser le motif `[0-9]+`, ou de manière simplifiée `\d+`. Le `\d` correspond à un chiffre (0-9). Le problème c'est que dans le texte `R2-D2` le motif `\d+` va trouver `2` et `2` séparément alors qu'il s'agit d'un nom de robot dans StarWars et non de deux nombres. Il faut affiner la recherche. On peut utiliser le motif `\b\d+\b` pour chercher des nombres entiers isolés. Le `\b` correspond à une frontière de mot, ce qui signifie que le nombre doit être entouré d'espaces ou de ponctuation pour être considéré comme un mot entier. Ainsi, le motif `\b\d+\b` ne correspondra pas à `2` dans `R2-D2`, mais correspondra à `30` dans notre exemple.

Si je cherche soit le mot `foo`, soit le mot `bar`, je peux utiliser le motif `(foo|bar)`. Le `|` correspond à un "ou" logique. Ainsi, le motif `foo|bar` correspondra à toutes les occurences de `foo` ou de `bar`. Les parenthèses sont utilisées pour grouper les motifs et appliquer des quantificateurs ou des opérateurs logiques à l'ensemble du groupe. Par exemple je cherche une répétition de trois fois le mot `foo` ou le mot `bar`, par exemple `foofoobar` ou `barfoofoo`, je peux utiliser le motif `(foo|bar){3}`. Le `{3}` indique que le motif précédent (le groupe `(foo|bar)`) doit apparaître exactement trois fois.

Enfin si je cherche tous les mots d'au moins trois lettres, jusqu'à 7 lettres, je peux utiliser le motif `\b[a-zA-Z]{3,7}\b`. Le `{3,7}` indique que le mot doit avoir entre 3 et 7 lettres. Si les mots peuvent comporter `[a-zA-Z0-9_]` (lettres, chiffres et underscore), on peut utiliser le motif `\b\w{3,7}\b`. Le `\w` correspond à un caractère alphanumérique ou un underscore.

Résumons:

| Motif | Alternative | Signification |
|-------|----------|----------------|
| `[a-zA-Z0-9_]` | `\w` | Caractère alphanumérique ou underscore |
| `[0-9]` | `\d` | Chiffre |
| `{3,7}` |  | Entre 3 et 7 occurrences |
| `{0,}` | `*` | 0 ou plusieurs occurrences |
| `{1,}` | `+` | 1 ou plusieurs occurrences |
| `{0,1}` | `?` | 0 ou 1 occurrence |
| `()` |  | Groupe |
| `(?:(?<=\w)(?!\w)|(?<!\w)(?=\w))` | `\b` | Frontière de mot |

Oui pour le dernier, le motif semble compliqué, Pourtant on connait déjà presque tout, le `|`, le `\w` et les parenthèses. Il ne manque que les assertions `(?=...)` et `(?!...)`.

### Les assertions

Les assertions sont des motifs qui ne consomment pas de caractères dans la chaîne de caractères, mais qui vérifient si une condition est remplie à un endroit donné. Il y a deux types d'assertions : les assertions positivas `(?=...)` et les assertions négatives `(?!...)`. Dans notre `\b`, on a utilisé les assertions pour vérifier si un caractère est précédé ou suivi d'une frontière de mot. Le `(?<=\w)` vérifie si le caractère précédent est un caractère alphanumérique, et le `(?!\w)` vérifie si le caractère suivant n'est pas un caractère alphanumérique. De même, le `(?<!\w)` vérifie si le caractère précédent n'est pas un caractère alphanumérique, et le `(?=\w)` vérifie si le caractère suivant est un caractère alphanumérique.

### Les groupes nommés

Parfois il est utile de créer des groupes pour capturer une partie spécifique d'une chaîne de caractères par exemple j'ai une expression XML:

```xml
<person>Bob</person>
<age>30</age>
```

J'aimerais récupérer tous les éléments. Je vais avoir deux groupes: les tags et le contenu. Ici le `\1` est une référence au premier groupe capturé car le tag se termine par le même nom que celui qui l'ouvre. Le motif est donc:

```text
<(\w+)>(.*?)</\1>
```

Voyons en Python:

```python
import re

s = """
<person>Bob</person>
<age>30</age>
"""

re.findall(r"<(\w+)>(.*?)</\1>", s)
# Retourne [('person', 'Bob'), ('age', '30')]
```

Il est parfois utile de nommer les groupes pour les retrouver plus facilement. On peut utiliser la syntaxe `(?P<name>...)` pour nommer un groupe. Par exemple, on peut nommer le premier groupe `tag` et le second groupe `content`:

```python
[m.groupdict() for m in re.finditer(r"<(?P<tag>\w+)>(?P<content>.*?)</(?P=tag)>", s)]
# Retourne [{'tag': 'person', 'content': 'Bob'}, {'tag': 'age', 'content': '30'}]
```

### Exemple d'un code de pneu

Un code de pneu est généralement composé de plusieurs éléments, tels que la largeur, la hauteur, le diamètre, le type de pneu, etc. Par exemple, un code de pneu peut être `205/55R1691V`, où:

- `205` est la largeur du pneu en millimètres
- `55` est le rapport hauteur/largeur en pourcentage
- `R` indique que le pneu est radial
- `16` est le diamètre de la jante en pouces

Selon le standard on peut écrire une expression régulière pour extraire ces informations:

```text
(\d{3})/(\d{2})([A-Z])(\d{2})(\d{2})([A-Z])
```

En Python:

```python
>>> re.findall(r"(\d{3})/(\d{2})([A-Z])(\d{2})(\d{2})([A-Z])", "205/55R1691V")
[('205', '55', 'R', '16', '91', 'V')]
```

Ou on peut aller plus loin et nommer les groupes pour plus de clarté:

```python
>>> r = r"(?P<width>\d{3})/(?P<height>\d{2})(?P<type>[A-Z])(?P<rim>\d{2})(?P<load>\d{2})(?P<speed>[A-Z])"
>>> [m.groupdict() for m in re.finditer(r, "205/55R1691V")]
[{'width': '205', 'height': '55', 'type': 'R', 'rim': '16', 'load': '91', 'speed': 'V'}]
```

On peut combiner tout ce qu'on a appris avec `typer` et les expression régulière pour faire un programme Python qui lit un code de pneu selon le standard complet. L'expression régulière est beaucoup plus complexe mais vous devriez être capable de la lire.

```python
#!/usr/bin/env python3
"""Décode un code pneumatique (ex. P195/55R16 85H XL) et l'affiche avec rich.

Usage :
    python pneu.py "205/55 R16 91V"
    echo "37x12.5R17LT" | python pneu.py
"""
import re
import sys

from rich.console import Console
from rich.table import Table

TIRE_RE = re.compile(
    r"""
    ^\s*
    (?:
        # Système métrique (ETRTO / P-Metric) : [classe] largeur [/ratio] [R] jante [C]
        (?P<classe>LT|ST|M/C|P|T|C)?\s*
        (?P<largeur>\d{3})
        (?:\s*/\s*(?P<ratio>\d{2,3}))?\s*
        (?P<vitesse_ancienne>[SHVZ](?=R))?
        (?P<construction>[RBD])?\s*
        (?P<jante>\d{3}|\d{1,2}(?:\.5)?)
        (?P<utilitaire>C\b)?
    |
        # Système flottaison (Light Truck High Flotation) : diamètre x largeur R jante LT
        (?P<diametre_pouces>\d{2})\s*[xX]\s*
        (?P<largeur_pouces>\d{1,2}(?:\.\d{1,2})?)\s*
        (?P<construction_f>[RBD])?\s*-?\s*
        (?P<jante_f>\d{2}(?:\.5)?)\s*
        (?P<lt>LT)?
    )
    # Description de service : indice de charge (simple ou jumelé) et indice de vitesse
    (?:\s*
        (?P<parenthese>\()?
        (?P<charge>\d{2,3})(?:/(?P<charge_jumelee>\d{2,3}))?
        (?P<vitesse>A[1-8]|[B-HJ-NP-WYZ])
        (?(parenthese)\))
    )?
    # Marquages complémentaires
    (?:\s*(?P<renfort>XL|SL|LL|RF|EXTRA\s+LOAD))?
    (?:\s*(?P<hiver>M\+SE|M\+S|M&S|3PMSF))?
    \s*$
    """,
    re.VERBOSE | re.IGNORECASE,
)

CLASSES = {
    "P": "Véhicule de tourisme (normes TRA)",
    "LT": "Camionnette (light truck)",
    "C": "Utilitaire",
    "ST": "Remorque spéciale",
    "M/C": "Moto",
    "T": "Roue de secours temporaire",
}
CONSTRUCTIONS = {"R": "Radiale", "B": "Diagonale ceinturée", "D": "Diagonale"}
RENFORTS = {
    "XL": "Charge renforcée (extra load)",
    "RF": "Renforcé, équivalent XL",
    "SL": "Charge standard",
    "LL": "Charge légère",
    "EXTRA LOAD": "Charge renforcée (extra load)",
}
HIVER = {
    "M+S": "Boue et neige",
    "M&S": "Boue et neige",
    "M+SE": "Boue et neige, conditions extrêmes",
    "3PMSF": "Neige sévère (symbole alpin)",
}
VITESSES = {
    "A1": "5", "A2": "10", "A3": "15", "A4": "20", "A5": "25", "A6": "30",
    "A7": "35", "A8": "40", "B": "50", "C": "60", "D": "65", "E": "70",
    "F": "80", "G": "90", "J": "100", "K": "110", "L": "120", "M": "130",
    "N": "140", "P": "150", "Q": "160", "R": "170", "S": "180", "T": "190",
    "U": "200", "H": "210", "V": "240", "Z": "> 240", "W": "270", "Y": "300",
}
# Indices de charge 50 à 129 (kg par pneu), plage usuelle tourisme et utilitaire
CHARGES = dict(zip(range(50, 130), [
    190, 195, 200, 206, 212, 218, 224, 230, 236, 243,
    250, 257, 265, 272, 280, 290, 300, 307, 315, 325,
    335, 345, 355, 365, 375, 387, 400, 412, 425, 437,
    450, 462, 475, 487, 500, 515, 530, 545, 560, 580,
    600, 615, 630, 650, 670, 690, 710, 730, 750, 775,
    800, 825, 850, 875, 900, 925, 950, 975, 1000, 1030,
    1060, 1090, 1120, 1150, 1180, 1215, 1250, 1285, 1320, 1360,
    1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850,
]))


def charge(indice: str) -> str:
    kg = CHARGES.get(int(indice))
    return f"{kg} kg par pneu" if kg else "Hors table embarquée (50 à 129)"


def decode(code: str) -> Table | None:
    m = TIRE_RE.match(code)
    if not m:
        return None
    g = {k: (v.upper() if v else v) for k, v in m.groupdict().items()}

    t = Table(title=f"Pneu {code.strip()}", header_style="bold cyan")
    t.add_column("Élément")
    t.add_column("Code", style="magenta", justify="center")
    t.add_column("Signification")

    if g["largeur"]:
        largeur, jante = int(g["largeur"]), float(g["jante"])
        t.add_row("Usage", g["classe"] or "", CLASSES.get(g["classe"], "Non précisé (normes ETRTO)"))
        t.add_row("Largeur de section", g["largeur"], f"{largeur} mm")
        ratio = int(g["ratio"]) if g["ratio"] else None
        if ratio is None:
            t.add_row("Série", "", "Omise, 82 % par convention")
            ratio = 82
        elif ratio > 200:
            t.add_row("Diamètre global", g["ratio"], f"{ratio} mm (notation japonaise)")
        else:
            flanc = largeur * ratio / 100
            t.add_row("Série", g["ratio"], f"Flanc à {ratio} % de la largeur, soit {flanc:.0f} mm")
        if g["vitesse_ancienne"]:
            t.add_row("Vitesse (ancien format)", g["vitesse_ancienne"], "Marquage antérieur à 1991")
        t.add_row("Structure", g["construction"] or "",
                  CONSTRUCTIONS.get(g["construction"], "Carcasse croisée"))
        unite = "mm" if jante > 100 else "pouces"
        t.add_row("Diamètre de jante", g["jante"], f"{g['jante']} {unite}")
        if g["utilitaire"]:
            t.add_row("Suffixe", "C", "Pneu utilitaire")
        if unite == "pouces":
            diametre = ratio if ratio > 200 else 2 * largeur * ratio / 100 + jante * 25.4
            t.add_row("Diamètre théorique", "", f"{diametre:.0f} mm, {diametre / 25.4:.2f} pouces")
    else:
        t.add_row("Diamètre du pneu", g["diametre_pouces"], f"{g['diametre_pouces']} pouces")
        t.add_row("Largeur de section", g["largeur_pouces"], f"{g['largeur_pouces']} pouces")
        t.add_row("Structure", g["construction_f"] or "",
                  CONSTRUCTIONS.get(g["construction_f"], "Carcasse croisée"))
        t.add_row("Diamètre de jante", g["jante_f"], f"{g['jante_f']} pouces")
        if g["lt"]:
            t.add_row("Usage", "LT", CLASSES["LT"])

    if g["charge"]:
        t.add_row("Indice de charge", g["charge"], charge(g["charge"]))
        if g["charge_jumelee"]:
            t.add_row("Indice de charge jumelé", g["charge_jumelee"], charge(g["charge_jumelee"]))
        mention = ", plafond fixé par le fabricant" if g["parenthese"] else ""
        t.add_row("Indice de vitesse", g["vitesse"], f"{VITESSES[g['vitesse']]} km/h{mention}")
    if g["renfort"]:
        cle = re.sub(r"\s+", " ", g["renfort"])
        t.add_row("Renfort", g["renfort"], RENFORTS[cle])
    if g["hiver"]:
        t.add_row("Marquage hiver", g["hiver"], HIVER[g["hiver"]])
    return t


def main() -> int:
    console = Console()
    codes = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else [
        line for line in sys.stdin.read().splitlines() if line.strip()
    ]
    status = 0
    for code in codes:
        table = decode(code)
        if table:
            console.print(table)
        else:
            console.print(f"[red]Code non reconnu :[/red] {code!r}")
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
```
