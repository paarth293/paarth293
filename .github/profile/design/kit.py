"""Palette, shared components and 3D projection helpers.

Editorial, not neon: warm graphite and bone, one signal-orange accent used
sparingly, sage for "live". Hairlines instead of glows, small radii instead
of pills, no gradients, no dot grids. Anything that looked like a default
AI landing page was removed on purpose.
"""
from __future__ import annotations

import math

from .doc import Doc, num

# ---------------------------------------------------------------- palette --
BG = "#141312"        # warm graphite (page cards)
PANEL = "#1A1917"     # inset panels
PANEL_2 = "#211F1D"
LINE = "#2E2B28"      # hairlines
GRID = "#1F1D1B"
INK = "#EDE8DD"       # bone
INK_2 = "#BDB6A9"
MUTED = "#8C857A"
DIM = "#625C54"
ACCENT = "#FF5A1F"    # signal orange: the only saturated colour on the page
GREEN = "#9FB585"     # sage, for "live" / "ok"

# The old per-role rainbow collapses into one warm ramp: bone -> tan -> orange.
ROLE = {
    "web": "#D8D1C3",     # full-stack: bone
    "3d": "#8C857A",      # foundations / misc: stone
    "agent": "#C99A6B",   # agents / orchestration: tan
    "ai": ACCENT,         # AI: the accent
}
ROLE_NAME = {"web": "NEXT.JS", "3d": "3D", "ai": "AI"}


def mix(c1: str, c2: str, t: float) -> str:
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


# ------------------------------------------------------------- components --
def card(doc: Doc, x=0, y=0, w=None, h=None, r=8, fill=BG, stroke=LINE) -> str:
    w = doc.w if w is None else w
    h = doc.h if h is None else h
    r = min(r, 8)
    return (f'<rect x="{num(x + .5)}" y="{num(y + .5)}" width="{num(w - 1)}" height="{num(h - 1)}" '
            f'rx="{r}" fill="{fill}" stroke="{stroke}"/>')


def dot_grid(doc: Doc, x, y, w, h, **_ignored) -> str:
    """Retired: dot grids read as template decoration. Kept as a no-op."""
    return ""


def chip(doc: Doc, x, y, text, color, *, fkey="mono-bold", size=12, pad=10, h=24, filled=False) -> tuple[str, float]:
    """A square-cornered tag: hairline outline, no tinted fill."""
    from .type import measure
    tw = measure(fkey, text, size, 0.6)
    w = tw + pad * 2
    if filled:
        s = f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{h}" rx="3" fill="{color}"/>'
        tcol = BG
    else:
        s = (f'<rect x="{num(x + .5)}" y="{num(y + .5)}" width="{num(w - 1)}" height="{h - 1}" rx="3" fill="none" '
             f'stroke="{color}" stroke-opacity=".55"/>')
        tcol = color
    s += doc.text(fkey, text, x + pad, y + h / 2 + size * 0.36, size, tcol, tracking=0.6)
    return s, w


def role_dot(x, y, key, r=4.5) -> str:
    return f'<circle cx="{num(x)}" cy="{num(y)}" r="{r}" fill="{ROLE[key]}"/>'


# ------------------------------------------------------------- isometric --
COS30 = math.cos(math.radians(30))
SIN30 = 0.5


def iso(x: float, y: float, z: float, s: float, ox: float, oy: float) -> tuple[float, float]:
    """World (x right-back, y left-back, z up) → screen."""
    return ox + (x - y) * COS30 * s, oy + (x + y) * SIN30 * s - z * s


def pts(points) -> str:
    return " ".join(f"{num(px)},{num(py)}" for px, py in points)


def prism(x, y, w, d, h, s, ox, oy):
    """Return the three visible faces (top, left(+y), right(+x)) of a box."""
    P = lambda a, b, c: iso(a, b, c, s, ox, oy)
    top = [P(x, y, h), P(x + w, y, h), P(x + w, y + d, h), P(x, y + d, h)]
    left = [P(x, y + d, 0), P(x + w, y + d, 0), P(x + w, y + d, h), P(x, y + d, h)]
    right = [P(x + w, y, 0), P(x + w, y + d, 0), P(x + w, y + d, h), P(x + w, y, h)]
    return top, left, right


# ---------------------------------------------------------- perspective --
def rot(v, ax, ay, az=0.0):
    x, y, z = v
    cy, sy = math.cos(ay), math.sin(ay)
    x, z = x * cy + z * sy, -x * sy + z * cy
    cx, sx = math.cos(ax), math.sin(ax)
    y, z = y * cx - z * sx, y * sx + z * cx
    cz, sz = math.cos(az), math.sin(az)
    x, y = x * cz - y * sz, x * sz + y * cz
    return x, y, z


def project(v, f, cx, cy, scale):
    x, y, z = v
    k = f / (f + z)
    return cx + x * scale * k, cy - y * scale * k, z


def icosahedron():
    t = (1 + 5 ** 0.5) / 2
    v = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
         (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    n = math.sqrt(1 + t * t)
    v = [(a / n, b / n, c / n) for a, b, c in v]
    edges = set()
    for i in range(12):
        for j in range(i + 1, 12):
            d = sum((v[i][k] - v[j][k]) ** 2 for k in range(3)) ** 0.5
            if abs(d - 2 / n) < 1e-6:
                edges.add((i, j))
    return v, sorted(edges)
