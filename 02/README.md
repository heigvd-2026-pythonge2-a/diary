
# Installer Python 

## Sous Windows

- Python.org (https://www.python.org/downloads/)
- Microsoft Store (...)
- Winget (`winget install Python.Python.3`)
- Chocolatey (`choco install python`)

## Sous Linux

- Ubuntu/Debian : `sudo apt install python3`
- Fedora : `sudo dnf install python3`
- Arch Linux : `sudo pacman -S python`
- OpenSUSE : `sudo zypper install python3`
- Gentoo : `sudo emerge dev-lang/python`

## Distributions Python

- Anaconda (https://www.anaconda.com/)
- Miniconda (https://docs.conda.io/en/latest/miniconda.html)
- ActivePython (https://www.activestate.com/products/python/)

## Modules/Packages Python

- uv
- poetry
- pyenv

## Python est un langage interprété

Il faut un interpréteur pour exécuter les programmes Python. L'interpréteur est fourni par l'installation de Python. 

Donc l'exécution d'un programme Python est lent comparé à un programme compilé. Il est environ 50 à 100 fois plus lent qu'un programme compilé.

## Shebang

La ligne shebang est utilisée pour spécifier le chemin vers l'interpréteur à utiliser pour exécuter un script. Elle est généralement placée en première ligne du fichier et commence par `#!`. Par exemple, `#!/usr/bin/env python3` indique que le script doit être exécuté avec l'interpréteur Python 3.