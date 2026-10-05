"""Interface terminal animée de la machine à sous."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto

from rich import box
from rich.align import Align
from rich.console import Console, Group, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .keyboard import keyboard
from .machine import (
    PAYLINES,
    REELS,
    SYMBOLS,
    CHERRY,
    TWO_CHERRIES_PAYOUT,
    SlotMachine,
    SpinResult,
)

FPS = 30
START_CREDITS = 100
MAX_BET = 10
SPIN_BASE = 1.0  # durée du premier rouleau (s)
SPIN_STAGGER = 0.45  # délai supplémentaire par rouleau (s)
CELEBRATION = 2.5  # durée de l'animation de gain (s)
RAINBOW = ("red", "dark_orange", "yellow", "green", "cyan", "blue", "magenta")


class Phase(Enum):
    IDLE = auto()
    SPINNING = auto()
    CELEBRATING = auto()


def ease_out_cubic(x: float) -> float:
    return 1 - (1 - min(max(x, 0.0), 1.0)) ** 3


@dataclass
class App:
    machine: SlotMachine = field(default_factory=lambda: SlotMachine(START_CREDITS))
    bet: int = 1
    phase: Phase = Phase.IDLE
    auto_spin: bool = False
    running: bool = True
    message: Text = field(default_factory=lambda: Text("Bonne chance ! 🍀", style="bold"))
    shown_credits: float = 0
    positions: list[int] = field(default_factory=lambda: [0] * REELS)
    result: SpinResult | None = None
    spin_from: list[int] = field(default_factory=list)
    distances: list[int] = field(default_factory=list)
    phase_start: float = 0.0
    credits_before_win: int = 0
    best_win: int = 0
    now: float = 0.0

    def __post_init__(self) -> None:
        self.shown_credits = self.machine.credits
        self.positions = [self.machine.rng.randrange(self.machine.strip_length) for _ in range(REELS)]

    # ------------------------------------------------------------------ input
    def handle(self, key: str) -> None:
        match key:
            case "q" | "Q" | "\x1b":
                self.running = False
            case " " | "\n" | "\r":
                self.auto_spin = False
                self.start_spin()
            case "+" | "=" | "\x1b[A" | "\x1b[C":
                self.change_bet(+1)
            case "-" | "_" | "\x1b[B" | "\x1b[D":
                self.change_bet(-1)
            case "m" | "M":
                self.change_bet(MAX_BET)
            case "a" | "A":
                self.auto_spin = not self.auto_spin
                self.say("Auto-spin activé 🔁" if self.auto_spin else "Auto-spin désactivé", "cyan")
            case "r" | "R" if self.machine.credits < SlotMachine.cost(1) and self.phase is Phase.IDLE:
                self.machine.credits = START_CREDITS
                self.shown_credits = START_CREDITS
                self.say("La banque vous offre 100 crédits 💸", "green")

    def change_bet(self, delta: int) -> None:
        if self.phase is Phase.SPINNING:
            return
        self.bet = min(MAX_BET, max(1, self.bet + delta))

    def say(self, text: str, style: str = "bold") -> None:
        self.message = Text(text, style=style)

    # -------------------------------------------------------------- animation
    def start_spin(self) -> None:
        if self.phase is Phase.SPINNING:
            return
        self.finish_celebration()
        if SlotMachine.cost(self.bet) > self.machine.credits:
            self.auto_spin = False
            if self.machine.credits < SlotMachine.cost(1):
                self.say("Plus de crédits… appuyez sur R pour recharger", "bold red")
            else:
                self.say("Mise trop élevée pour vos crédits", "bold red")
            return
        self.result = self.machine.spin(self.bet)
        self.credits_before_win = self.machine.credits - self.result.total
        self.shown_credits = self.credits_before_win
        n = self.machine.strip_length
        self.spin_from = list(self.positions)
        # Les rouleaux tournent vers le bas : la position décroît.
        self.distances = [
            (start - stop) % n + n * (2 + i)
            for i, (start, stop) in enumerate(zip(self.spin_from, self.result.stops))
        ]
        self.phase = Phase.SPINNING
        self.phase_start = self.now
        self.say("Les rouleaux tournent…", "italic bright_white")

    def reel_duration(self, reel: int) -> float:
        return SPIN_BASE + SPIN_STAGGER * reel

    def reel_stopped(self, reel: int) -> bool:
        return self.phase is not Phase.SPINNING or self.now - self.phase_start >= self.reel_duration(reel)

    def update(self, now: float) -> None:
        self.now = now
        elapsed = now - self.phase_start
        match self.phase:
            case Phase.SPINNING:
                assert self.result is not None
                n = self.machine.strip_length
                for reel in range(REELS):
                    progress = ease_out_cubic(elapsed / self.reel_duration(reel))
                    self.positions[reel] = (self.spin_from[reel] - round(self.distances[reel] * progress)) % n
                if elapsed >= self.reel_duration(REELS - 1):
                    self.positions = list(self.result.stops)
                    self.on_spin_end()
            case Phase.CELEBRATING:
                progress = ease_out_cubic(elapsed / (CELEBRATION * 0.8))
                self.shown_credits = self.credits_before_win + (self.machine.credits - self.credits_before_win) * progress
                if elapsed >= CELEBRATION:
                    self.finish_celebration()
            case Phase.IDLE if self.auto_spin and elapsed >= 0.4:
                self.start_spin()

    def on_spin_end(self) -> None:
        assert self.result is not None
        self.phase_start = self.now
        win = self.result.total
        if win == 0:
            self.phase = Phase.IDLE
            self.say("Pas de chance… on retente ? 🎲", "grey70")
            return
        self.best_win = max(self.best_win, win)
        self.phase = Phase.CELEBRATING
        ratio = win / self.result.cost
        if ratio >= 20:
            self.say(f"💥 MEGA JACKPOT 💥  +{win} crédits !", "bold")
        elif ratio >= 4:
            self.say(f"🎉 GROS GAIN ! +{win} crédits 🎉", "bold")
        else:
            self.say(f"Gagné : +{win} crédits ✨", "bold green")

    def finish_celebration(self) -> None:
        if self.phase is Phase.CELEBRATING:
            self.phase = Phase.IDLE
            self.phase_start = self.now
        if self.phase is Phase.IDLE:
            self.shown_credits = self.machine.credits

    # -------------------------------------------------------------- rendering
    def winning_cells(self) -> set[tuple[int, int]]:
        if self.phase is not Phase.CELEBRATING or self.result is None:
            return set()
        return {cell for win in self.result.wins for cell in win.cells}

    def render(self) -> RenderableType:
        body = Table.grid(padding=(0, 2))
        body.add_column(vertical="middle")
        body.add_column(vertical="middle")
        body.add_row(self.render_reels(), self.render_paytable())
        return Align.center(
            Group(
                Align.center(self.render_title()),
                Align.center(self.render_lights()),
                Align.center(body),
                Align.center(self.render_lights(offset=1)),
                Align.center(self.render_status()),
                Align.center(self.render_message()),
                Align.center(self.render_help()),
            ),
            vertical="middle",
        )

    def tick(self, speed: float = 8) -> int:
        return int(self.now * speed)

    def render_title(self) -> Text:
        title = "★  L U C K Y   S L O T S  ★"
        shift = self.tick(6)
        text = Text()
        for i, char in enumerate(title):
            text.append(char, style=f"bold {RAINBOW[(i + shift) % len(RAINBOW)]}")
        return text

    def render_lights(self, offset: int = 0) -> Text:
        fast = self.phase is not Phase.IDLE
        shift = self.tick(12 if fast else 3) + offset
        text = Text()
        for i in range(29):
            on = (i + shift) % 3 == 0
            text.append("● " if on else "○ ", style="bold gold1" if on else "grey35")
        return text

    def render_reels(self) -> Panel:
        cells = self.winning_cells()
        blink = self.tick(4) % 2 == 0
        table = Table(
            box=box.HEAVY,
            show_header=False,
            show_lines=True,
            padding=(1, 3),
            border_style="gold1",
        )
        for _ in range(REELS):
            table.add_column(justify="center", vertical="middle")
        windows = [self.machine.window(reel, pos) for reel, pos in enumerate(self.positions)]
        for row in range(3):
            line: list[Text] = []
            for reel in range(REELS):
                symbol = windows[reel][row]
                style = ""
                if (reel, row) in cells:
                    style = "on dark_red" if blink else "on gold3"
                elif not self.reel_stopped(reel):
                    style = "on grey15"
                line.append(Text(f" {symbol.glyph} ", style=style))
            table.add_row(*line)

        middle = 6  # ligne du rang central dans le tableau (bordures comprises)
        left = Text("\n" * middle + "▶", style="bold red")
        right = Text("\n" * middle + "◀", style="bold red")
        frame = Table.grid()
        frame.add_column()
        frame.add_column()
        frame.add_column()
        frame.add_row(left, table, right)
        border = RAINBOW[self.tick(10) % len(RAINBOW)] if self.phase is Phase.CELEBRATING else "red3"
        return Panel(frame, box=box.DOUBLE, border_style=border, padding=(0, 1))

    def render_paytable(self) -> Panel:
        active = {(w.symbol, w.count) for w in self.result.wins} if self.phase is Phase.CELEBRATING and self.result else set()
        table = Table(box=None, show_header=False, padding=(0, 1))
        table.add_column()
        table.add_column(justify="right")
        for symbol in reversed(SYMBOLS):
            style = "reverse bold" if (symbol, 3) in active else ""
            table.add_row(
                Text(symbol.glyph * 3, style=style),
                Text(f"{symbol.payout * self.bet:>5}", style=f"bold {symbol.color} {style}"),
            )
        style = "reverse bold" if (CHERRY, 2) in active else ""
        table.add_row(Text(CHERRY.glyph * 2 + "❔", style=style), Text(f"{TWO_CHERRIES_PAYOUT * self.bet:>5}", style=f"bold red {style}"))
        footer = Text(f"\n{len(PAYLINES)} lignes : ─ ─ ─ ╲ ╱", style="grey62")
        return Panel(
            Group(table, footer),
            title="[bold gold1]Gains[/]",
            subtitle=f"[grey62]par ligne × {self.bet}[/]",
            box=box.ROUNDED,
            border_style="gold1",
        )

    def render_status(self) -> Table:
        table = Table(box=box.ROUNDED, show_header=False, border_style="grey50", padding=(0, 2))
        for _ in range(4):
            table.add_column(justify="center")
        credits = round(self.shown_credits)
        credit_style = "bold green" if credits >= SlotMachine.cost(self.bet) else "bold red"
        last = self.result.total if self.result and self.phase is not Phase.SPINNING else 0
        table.add_row(
            Text.assemble("💰 Crédits ", (f"{credits:>6}", credit_style)),
            Text.assemble("🎯 Mise ", (f"{self.bet}×{len(PAYLINES)} = {SlotMachine.cost(self.bet):>2}", "bold cyan")),
            Text.assemble("🏆 Gain ", (f"{last:>5}", "bold gold1")),
            Text.assemble("🔁 Auto ", ("ON " if self.auto_spin else "OFF", "bold magenta" if self.auto_spin else "grey50")),
        )
        return table

    def render_message(self) -> Text:
        if self.phase is Phase.CELEBRATING and self.result and self.result.total >= 4 * self.result.cost:
            shift = self.tick(10)
            text = Text()
            for i, char in enumerate(self.message.plain):
                text.append(char, style=f"bold {RAINBOW[(i + shift) % len(RAINBOW)]}")
            return text
        return self.message

    def render_help(self) -> Text:
        keys = [("ESPACE", "tourner"), ("+/-", "mise"), ("M", "mise max"), ("A", "auto"), ("Q", "quitter")]
        text = Text()
        for key, label in keys:
            text.append(f" {key} ", style="bold black on gold1")
            text.append(f" {label}   ", style="grey70")
        return text


def main() -> None:
    console = Console()
    app = App()
    try:
        with keyboard() as read_key, Live(app.render(), console=console, screen=True, auto_refresh=False) as live:
            while app.running:
                if key := read_key(1 / FPS):
                    app.handle(key)
                app.update(time.monotonic())
                live.update(app.render(), refresh=True)
    except KeyboardInterrupt:
        pass
    console.print(
        Panel.fit(
            Text.assemble(
                ("Merci d'avoir joué ! ", "bold"),
                "Crédits finaux : ",
                (str(app.machine.credits), "bold green"),
                "  •  Meilleur gain : ",
                (str(app.best_win), "bold gold1"),
            ),
            border_style="gold1",
        )
    )
