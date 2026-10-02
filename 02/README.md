# Semaine 02/16

## Installer Python

Python comprend un interpréteur : c'est le programme qui lit et exécute votre code. Après l'installation, vérifiez qu'il est accessible dans le terminal avec `python3 --version` (ou `python --version` sous Windows). Pour exécuter l'exemple de cette semaine, placez-vous dans le dossier `02` puis lancez `python3 hello.py`.

### Sous Windows

- Python.org (https://www.python.org/downloads/)
- Microsoft Store (...)
- Winget (`winget install Python.Python.3`)
- Chocolatey (`choco install python`)

### Sous Linux

- Ubuntu/Debian : `sudo apt install python3`
- Fedora : `sudo dnf install python3`
- Arch Linux : `sudo pacman -S python`
- OpenSUSE : `sudo zypper install python3`
- Gentoo : `sudo emerge dev-lang/python`

## Distributions Python

Une distribution regroupe Python et des outils ou bibliothèques supplémentaires. Anaconda en fournit notamment pour le calcul scientifique ; une installation depuis Python.org suffit pour commencer ce cours.

- Anaconda (https://www.anaconda.com/)
- Miniconda (https://docs.conda.io/en/latest/miniconda.html)
- ActivePython (https://www.activestate.com/products/python/)

## Modules/Packages Python

Un module est un fichier Python que l'on peut importer ; un package regroupe des modules. Certains sont fournis avec Python, d'autres s'installent séparément. Les outils suivants aident à gérer votre environnement de travail :

- uv : gestion des dépendances et des environnements virtuels.
- poetry : gestion des dépendances et de la configuration d'un projet.
- pyenv : installation et sélection de différentes versions de Python.

Un environnement virtuel isole les bibliothèques d'un projet pour éviter les conflits avec celles d'un autre projet.

## Shebang

La ligne shebang est utilisée pour spécifier le chemin vers l'interpréteur à utiliser pour exécuter un script. Elle est généralement placée en première ligne du fichier et commence par `#!`. Par exemple, `#!/usr/bin/env python3` indique que le script doit être exécuté avec l'interpréteur Python 3.

Sous Linux, on peut ainsi lancer `./hello.py` après avoir rendu le fichier exécutable avec `chmod +x hello.py`. Avec `python3 hello.py`, on choisit directement l'interpréteur et le shebang n'est pas nécessaire.

## Python est un langage interprété

Il faut un interpréteur pour exécuter les programmes Python. L'interpréteur est fourni par l'installation de Python.

Pour des calculs écrits directement en Python, l'exécution est souvent plus lente qu'en C compilé. L'écart dépend cependant du programme : des bibliothèques comme NumPy effectuent leurs calculs dans du code compilé.

On peut prendre l'exemple d'un programme simple en Python:

```python
#! /usr/bin/env python3
print("hello, world\n")
```

Ce fichier fait sur le disque 48 octets. Avant de l'exécuter, Python le compile en bytecode, des instructions destinées à sa machine virtuelle. Lors de l'import d'un module, ce bytecode peut être conservé dans un fichier `.pyc` du dossier `__pycache__` pour les prochains lancements ; l'exécution directe d'un script ne crée pas forcément ce fichier.

Le même exemple en C est de 65 octets :

```c
#include <stdio.h>

int main() { printf("hello, world\n"); }
```

Et on peut pousser plus loin et écrire le même programme en assembleur, un langage proche des instructions de la machine :

```asm
section .data
    msg db "Hello, world!", 10
    len equ $ - msg

section .text
    global _start

_start:
    mov eax, 4      ; sys_write
    mov ebx, 1      ; stdout
    mov ecx, msg
    mov edx, len
    int 0x80

    mov eax, 1      ; sys_exit
    xor ebx, ebx    ; code retour 0
    int 0x80
```

Lui il est encore plus gros 296 octets.

Voyons ce que ca fait de les compiler:

Ces commandes sont à lancer sous Linux, depuis le dossier `02`, avec GCC, NASM et PyInstaller installés. GCC transforme le C en exécutable ; NASM produit un fichier objet, puis `ld` le relie pour obtenir l'exécutable. PyInstaller regroupe le script Python, son interpréteur et ses dépendances dans un seul fichier.

```bash
gcc -o hello.c.out hello.c
pyinstaller --onefile hello.py && mv dist/hello hello.py.out  # Après avoir fait pipx install pyinstaller
nasm -f elf64 hello.asm -o hello.asm.o && ld -o hello.asm.out hello.asm.o
ls -alh hello.*.out
```

On obtient :

```
.rwxr-xr-x  8.9k ycr   2 Oct 16:14  hello.asm.out
.rwxr-xr-x   16k ycr   2 Oct 16:13  hello.c.out
.rwxr-xr-x  9.3M ycr   2 Oct 16:12  hello.py.out
```

L'exécutable produit par PyInstaller est beaucoup plus gros car il embarque l'environnement nécessaire à Python. Ici, le plus petit est celui en assembleur. Les tailles varient selon les outils et le système ; elles ne permettent pas, à elles seules, de comparer la vitesse d'exécution.
