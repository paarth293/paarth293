"""Timeline helpers: describe motion in seconds, emit CSS keyframes in %."""
from __future__ import annotations

from .doc import Doc


def track(doc: Doc, period: float, points: list[tuple[float, str]]) -> str:
    """points: [(seconds_into_loop, 'css decls')] → keyframes name.

    Adds 0% / 100% stops from the first/last point so every loop starts and
    ends in a defined state. Points at equal times are nudged apart so a
    pair of stops behaves as an instant switch.
    """
    pts = sorted(points, key=lambda p: p[0])
    fixed: list[tuple[float, str]] = []
    last = -1.0
    for t, d in pts:
        t = max(t, last + 0.001)
        fixed.append((t, d))
        last = t
    if fixed[0][0] > 0:
        fixed.insert(0, (0.0, fixed[0][1]))
    if fixed[-1][0] < period:
        fixed.append((period, fixed[-1][1]))
    stops = [(min(100.0, t / period * 100), d) for t, d in fixed]
    return doc.keyframes(stops)


def anim(name: str, period: float, delay: float = 0.0, *, loop: bool = True, ease: str = "linear") -> str:
    it = "infinite" if loop else "1"
    return f"animation:{name} {period}s {ease} {delay}s {it} both"


def show_between(doc: Doc, period: float, spans: list[tuple[float, float]], fade: float = 0.25,
                 on: str = "opacity:1", off: str = "opacity:0") -> str:
    """Visible during each (start, end) span of the loop, hidden otherwise."""
    pts: list[tuple[float, str]] = [(0.0, off)]
    for a, b in spans:
        pts += [(a, off), (a + fade, on), (b, on), (b + fade, off)]
    return track(doc, period, pts)
