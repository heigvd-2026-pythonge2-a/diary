"""Logique de la machine à sous, indépendante de l'affichage."""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Symbol:
    glyph: str
    name: str
    weight: int  # nombre d'occurrences sur chaque rouleau
    payout: int  # multiplicateur de la mise pour 3 symboles alignés
    color: str


SYMBOLS: tuple[Symbol, ...] = (
    Symbol("🍒", "Cerise", 9, 15, "red"),
    Symbol("🍋", "Citron", 8, 20, "yellow"),
    Symbol("🍊", "Orange", 7, 25, "dark_orange"),
    Symbol("🍇", "Raisin", 6, 40, "magenta"),
    Symbol("🔔", "Cloche", 4, 80, "gold1"),
    Symbol("⭐", "Étoile", 3, 150, "bright_yellow"),
    Symbol("🍀", "Trèfle", 2, 300, "green"),
    Symbol("💎", "Diamant", 1, 1000, "cyan"),
)
CHERRY = SYMBOLS[0]
TWO_CHERRIES_PAYOUT = 4

REELS = 3
ROWS = 3

# Lignes de paiement : pour chaque rouleau, la rangée concernée.
PAYLINES: tuple[tuple[int, ...], ...] = (
    (1, 1, 1),  # milieu
    (0, 0, 0),  # haut
    (2, 2, 2),  # bas
    (0, 1, 2),  # diagonale ╲
    (2, 1, 0),  # diagonale ╱
)

type Grid = list[list[Symbol]]  # grid[rouleau][rangée]


@dataclass(frozen=True, slots=True)
class LineWin:
    line: int
    symbol: Symbol
    count: int
    amount: int

    @property
    def cells(self) -> list[tuple[int, int]]:
        return [(reel, PAYLINES[self.line][reel]) for reel in range(self.count)]


@dataclass(frozen=True, slots=True)
class SpinResult:
    stops: list[int]
    grid: Grid
    wins: list[LineWin]
    cost: int

    @property
    def total(self) -> int:
        return sum(w.amount for w in self.wins)


@dataclass
class SlotMachine:
    credits: int = 100
    seed: int | None = None
    rng: random.Random = field(init=False)
    strips: list[list[Symbol]] = field(init=False)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        base = [s for s in SYMBOLS for _ in range(s.weight)]
        self.strips = [self.rng.sample(base, len(base)) for _ in range(REELS)]

    @property
    def strip_length(self) -> int:
        return len(self.strips[0])

    @staticmethod
    def cost(bet: int) -> int:
        return bet * len(PAYLINES)

    def window(self, reel: int, stop: int) -> list[Symbol]:
        """Les symboles visibles sur un rouleau, centrés sur `stop`."""
        strip = self.strips[reel]
        n = len(strip)
        return [strip[(stop + offset) % n] for offset in range(-1, ROWS - 1)]

    def spin(self, bet: int) -> SpinResult:
        cost = self.cost(bet)
        if cost > self.credits:
            raise ValueError("Crédits insuffisants")
        self.credits -= cost
        stops = [self.rng.randrange(self.strip_length) for _ in range(REELS)]
        grid = [self.window(reel, stop) for reel, stop in enumerate(stops)]
        result = SpinResult(stops, grid, evaluate(grid, bet), cost)
        self.credits += result.total
        return result


def evaluate(grid: Grid, bet: int) -> list[LineWin]:
    wins: list[LineWin] = []
    for index, line in enumerate(PAYLINES):
        symbols = [grid[reel][row] for reel, row in enumerate(line)]
        match symbols:
            case [a, b, c] if a == b == c:
                wins.append(LineWin(index, a, 3, a.payout * bet))
            case [a, b, _] if a == b == CHERRY:
                wins.append(LineWin(index, CHERRY, 2, TWO_CHERRIES_PAYOUT * bet))
    return wins
