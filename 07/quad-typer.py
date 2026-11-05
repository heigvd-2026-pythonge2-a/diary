#!/usr/bin/env python3
"""Variante typer (pip install typer).
Usage : quad_typer.py [-i] a b c"""
import math, cmath
from typing import Annotated
import typer

def resoudre(a, b, c, imaginaire=False):
    if a == 0:
        raise typer.BadParameter("a doit être non nul")
    delta = b * b - 4 * a * c
    if delta < 0 and not imaginaire:
        return ()
    racine = cmath.sqrt(delta) if delta < 0 else math.sqrt(delta)
    return ((-b + racine) / (2 * a), (-b - racine) / (2 * a))


def main(
    a: float,
    b: float,
    c: float,
    imaginaire: Annotated[bool, typer.Option("-i", "--imaginaire",
                          help="accepter les solutions complexes")] = False,
):
    """Résout ax² + bx + c = 0"""
    solutions = resoudre(a, b, c, imaginaire)
    print(*solutions) if solutions else print("aucune solution réelle")


if __name__ == "__main__":
    typer.run(main)