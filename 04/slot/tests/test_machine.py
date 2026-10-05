"""Tests de la logique de la machine à sous."""

import pytest

from slot.machine import (
    CHERRY,
    PAYLINES,
    REELS,
    ROWS,
    SYMBOLS,
    TWO_CHERRIES_PAYOUT,
    LineWin,
    SlotMachine,
    evaluate,
)

DIAMOND = SYMBOLS[-1]
LEMON = SYMBOLS[1]
ORANGE = SYMBOLS[2]
GRAPE = SYMBOLS[3]


def grid_from_rows(*rows):
    """Construit une grille grid[rouleau][rangée] à partir de rangées lisibles."""
    return [[rows[row][reel] for row in range(ROWS)] for reel in range(REELS)]


# Grille sans aucune combinaison gagnante.
LOSING = grid_from_rows(
    (LEMON, ORANGE, GRAPE),
    (ORANGE, LEMON, DIAMOND),
    (DIAMOND, GRAPE, ORANGE),
)


def test_strips_contain_every_symbol_by_weight():
    machine = SlotMachine(seed=1)
    total = sum(s.weight for s in SYMBOLS)
    assert machine.strip_length == total
    for strip in machine.strips:
        for symbol in SYMBOLS:
            assert strip.count(symbol) == symbol.weight


def test_same_seed_gives_same_machine():
    a, b = SlotMachine(seed=42), SlotMachine(seed=42)
    assert a.strips == b.strips
    assert a.spin(1) == b.spin(1)


@pytest.mark.parametrize("bet", [1, 3, 10])
def test_cost_is_bet_times_paylines(bet):
    assert SlotMachine.cost(bet) == bet * len(PAYLINES)


def test_window_is_centered_and_wraps():
    machine = SlotMachine(seed=0)
    strip = machine.strips[0]
    n = machine.strip_length
    assert machine.window(0, 5) == [strip[4], strip[5], strip[6]]
    assert machine.window(0, 0) == [strip[n - 1], strip[0], strip[1]]
    assert machine.window(0, n - 1) == [strip[n - 2], strip[n - 1], strip[0]]


def test_evaluate_no_win():
    assert evaluate(LOSING, 1) == []


def test_evaluate_three_on_middle_line():
    grid = grid_from_rows(
        (LEMON, ORANGE, GRAPE),
        (DIAMOND, DIAMOND, DIAMOND),
        (GRAPE, LEMON, ORANGE),
    )
    assert evaluate(grid, 2) == [LineWin(0, DIAMOND, 3, DIAMOND.payout * 2)]


def test_evaluate_diagonals():
    grid = grid_from_rows(
        (GRAPE, ORANGE, GRAPE),
        (ORANGE, GRAPE, LEMON),
        (GRAPE, LEMON, GRAPE),
    )
    wins = evaluate(grid, 1)
    assert {w.line for w in wins} == {3, 4}
    assert all(w.symbol == GRAPE and w.count == 3 for w in wins)


def test_evaluate_two_cherries_on_left():
    grid = grid_from_rows(
        (LEMON, ORANGE, GRAPE),
        (CHERRY, CHERRY, LEMON),
        (GRAPE, LEMON, ORANGE),
    )
    assert evaluate(grid, 3) == [LineWin(0, CHERRY, 2, TWO_CHERRIES_PAYOUT * 3)]


def test_two_cherries_must_start_on_first_reel():
    grid = grid_from_rows(
        (LEMON, ORANGE, GRAPE),
        (LEMON, CHERRY, CHERRY),
        (GRAPE, LEMON, ORANGE),
    )
    assert evaluate(grid, 1) == []


def test_three_cherries_pay_full_payout():
    grid = grid_from_rows(
        (LEMON, ORANGE, GRAPE),
        (CHERRY, CHERRY, CHERRY),
        (GRAPE, LEMON, ORANGE),
    )
    assert evaluate(grid, 1) == [LineWin(0, CHERRY, 3, CHERRY.payout)]


def test_linewin_cells():
    assert LineWin(3, GRAPE, 3, 0).cells == [(0, 0), (1, 1), (2, 2)]
    assert LineWin(4, CHERRY, 2, 0).cells == [(0, 2), (1, 1)]


def test_spin_updates_credits():
    machine = SlotMachine(credits=100, seed=7)
    for _ in range(20):
        before = machine.credits
        result = machine.spin(1)
        assert result.cost == SlotMachine.cost(1)
        assert machine.credits == before - result.cost + result.total
        assert result.wins == evaluate(result.grid, 1)
        assert len(result.stops) == REELS


def test_spin_grid_matches_stops():
    machine = SlotMachine(seed=3)
    result = machine.spin(1)
    for reel, stop in enumerate(result.stops):
        assert result.grid[reel] == machine.window(reel, stop)


def test_spin_with_insufficient_credits_raises():
    machine = SlotMachine(credits=4)
    with pytest.raises(ValueError):
        machine.spin(1)
    assert machine.credits == 4
