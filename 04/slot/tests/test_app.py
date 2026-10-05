"""Tests de l'interface (sans terminal)."""

import pytest
from rich.console import Console

from slot.app import (
    CELEBRATION,
    MAX_BET,
    START_CREDITS,
    App,
    Phase,
    ease_out_cubic,
)
from slot.machine import REELS, SYMBOLS, LineWin, SlotMachine, SpinResult


@pytest.fixture
def app():
    return App(machine=SlotMachine(START_CREDITS, seed=123))


def spin_until(app, predicate, max_spins=500):
    """Fait tourner jusqu'à obtenir un résultat qui satisfait `predicate`."""
    for _ in range(max_spins):
        app.machine.credits = 10_000
        app.start_spin()
        if predicate(app.result):
            return
        app.update(app.now + 10)  # termine l'animation
        app.finish_celebration()
    pytest.fail("aucun tirage ne correspond")


def force_win(app, amount):
    """Termine un tirage fictif rapportant `amount` crédits pour une mise de 1."""
    wins = [LineWin(0, SYMBOLS[-1], 3, amount)] if amount else []
    app.result = SpinResult([0] * REELS, [], wins, SlotMachine.cost(1))
    app.phase = Phase.SPINNING
    app.on_spin_end()


def finish_spin(app):
    """Avance l'horloge juste après l'arrêt du dernier rouleau."""
    app.update(app.phase_start + app.reel_duration(REELS - 1) + 1e-6)


@pytest.mark.parametrize(
    ("x", "expected"),
    [(-1, 0), (0, 0), (0.5, 0.875), (1, 1), (2, 1)],
)
def test_ease_out_cubic(x, expected):
    assert ease_out_cubic(x) == pytest.approx(expected)


def test_initial_state(app):
    assert app.phase is Phase.IDLE
    assert app.shown_credits == START_CREDITS
    assert len(app.positions) == REELS
    assert all(0 <= p < app.machine.strip_length for p in app.positions)


@pytest.mark.parametrize("key", ["q", "Q", "\x1b"])
def test_quit(app, key):
    app.handle(key)
    assert not app.running


def test_bet_is_clamped(app):
    app.handle("-")
    assert app.bet == 1
    app.handle("+")
    app.handle("\x1b[A")
    assert app.bet == 3
    app.handle("m")
    assert app.bet == MAX_BET
    app.handle("+")
    assert app.bet == MAX_BET


def test_bet_locked_while_spinning(app):
    app.start_spin()
    app.handle("+")
    assert app.bet == 1


def test_start_spin_ignored_while_spinning(app):
    app.start_spin()
    result, credits = app.result, app.machine.credits
    app.start_spin()
    assert app.result is result
    assert app.machine.credits == credits


def test_toggle_auto_spin(app):
    app.handle("a")
    assert app.auto_spin
    app.handle("a")
    assert not app.auto_spin


def test_space_starts_spin_and_debits(app):
    app.handle(" ")
    assert app.phase is Phase.SPINNING
    assert app.shown_credits == START_CREDITS - SlotMachine.cost(1)


def test_spin_refused_when_bet_too_high(app):
    app.machine.credits = 20
    app.bet = 5
    app.auto_spin = True
    app.start_spin()
    assert app.phase is Phase.IDLE
    assert app.result is None
    assert not app.auto_spin
    assert "trop élevée" in app.message.plain


def test_spin_refused_without_credits(app):
    app.machine.credits = 0
    app.start_spin()
    assert app.phase is Phase.IDLE
    assert "recharger" in app.message.plain


def test_reload_only_when_broke(app):
    app.handle("r")
    assert app.machine.credits == START_CREDITS
    app.machine.credits = 2
    app.handle("r")
    assert app.machine.credits == START_CREDITS
    assert app.shown_credits == START_CREDITS


def test_reels_stop_one_after_another(app):
    app.start_spin()
    start = app.now
    app.update(start + app.reel_duration(0))
    assert app.reel_stopped(0)
    assert not app.reel_stopped(REELS - 1)


def test_spin_ends_on_result_stops(app):
    app.start_spin()
    finish_spin(app)
    assert app.positions == app.result.stops
    assert app.phase is not Phase.SPINNING


def test_losing_spin_returns_to_idle(app):
    spin_until(app, lambda r: r.total == 0)
    finish_spin(app)
    assert app.phase is Phase.IDLE
    assert "Pas de chance" in app.message.plain
    assert app.winning_cells() == set()


def test_winning_spin_celebrates_then_settles(app):
    spin_until(app, lambda r: r.total > 0)
    win = app.result.total
    finish_spin(app)
    assert app.phase is Phase.CELEBRATING
    assert app.best_win >= win
    assert f"+{win}" in app.message.plain
    assert app.winning_cells() == {c for w in app.result.wins for c in w.cells}

    app.update(app.now + CELEBRATION)
    assert app.phase is Phase.IDLE
    assert app.shown_credits == app.machine.credits


@pytest.mark.parametrize(
    ("amount", "text"),
    [(5, "Gagné"), (19, "Gagné"), (20, "GROS GAIN"), (99, "GROS GAIN"), (100, "MEGA JACKPOT")],
)
def test_win_message_depends_on_ratio(app, amount, text):
    force_win(app, amount)
    assert app.phase is Phase.CELEBRATING
    assert text in app.message.plain
    assert f"+{amount}" in app.message.plain


def test_big_win_message_is_rainbow(app):
    force_win(app, 20)
    rendered = app.render_message()
    assert rendered.plain == app.message.plain
    assert len({span.style for span in rendered.spans}) > 1


def test_small_win_message_is_plain(app):
    force_win(app, 5)
    assert app.render_message() is app.message


def test_new_spin_skips_celebration(app):
    spin_until(app, lambda r: r.total > 0)
    finish_spin(app)
    assert app.phase is Phase.CELEBRATING
    app.start_spin()
    assert app.phase is Phase.SPINNING


def test_auto_spin_restarts_after_delay(app):
    app.auto_spin = True
    app.update(0.1)
    assert app.phase is Phase.IDLE
    app.update(0.5)
    assert app.phase is Phase.SPINNING


@pytest.mark.parametrize("phase", list(Phase))
def test_render_does_not_crash(app, phase):
    if phase is not Phase.IDLE:
        spin_until(app, lambda r: r.total > 0)
        if phase is Phase.CELEBRATING:
            finish_spin(app)
        else:
            app.update(app.now + 0.3)
    assert app.phase is phase
    console = Console(width=120, file=None, record=True)
    console.print(app.render())
    assert "L U C K Y" in console.export_text()
