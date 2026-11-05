#!/usr/bin/env python3
"""Variante click (pip install click).
Usage : quad_click.py [-i] a b c"""
import math, cmath
import click


def resoudre(a, b, c, imaginaire=False):
    if a == 0:
        raise click.BadParameter("a doit être non nul", param_hint="a")
    delta = b * b - 4 * a * c
    if delta < 0 and not imaginaire:
        return ()
    racine = cmath.sqrt(delta) if delta < 0 else math.sqrt(delta)
    return ((-b + racine) / (2 * a), (-b - racine) / (2 * a))


@click.command(help="Résout ax² + bx + c = 0")
@click.argument("a", type=float)
@click.argument("b", type=float)
@click.argument("c", type=float)
@click.option("-i", "--imaginaire", is_flag=True, help="accepter les solutions complexes")
def main(a, b, c, imaginaire):
    solutions = resoudre(a, b, c, imaginaire)
    click.echo(" ".join(map(str, solutions)) if solutions else "aucune solution réelle")


if __name__ == "__main__":
    main()