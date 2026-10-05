"""Lecture non bloquante du clavier (POSIX et Windows)."""

from __future__ import annotations

import os
import sys
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager

type KeyReader = Callable[[float], str | None]

if os.name == "nt":
    import msvcrt

    @contextmanager
    def keyboard() -> Iterator[KeyReader]:
        def read(timeout: float) -> str | None:
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                if msvcrt.kbhit():
                    return msvcrt.getwch()
                time.sleep(0.005)
            return None

        yield read

else:
    import select
    import termios
    import tty

    @contextmanager
    def keyboard() -> Iterator[KeyReader]:
        fd = sys.stdin.fileno()
        saved = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)

            def read(timeout: float) -> str | None:
                ready, _, _ = select.select([fd], [], [], timeout)
                return os.read(fd, 32).decode(errors="ignore") if ready else None

            yield read
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, saved)
