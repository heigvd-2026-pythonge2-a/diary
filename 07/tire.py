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
