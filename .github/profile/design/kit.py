"""Palette, shared components and 3D projection helpers.

The palette is the portfolio's, moved to night: the portfolio's paper
(#F3F1EA) becomes the ink, and its three accent colours become the three
roles this profile is built around.
"""
from __future__ import annotations

import math

from .doc import Doc, num

# ---------------------------------------------------------------- palette --
BG = "#0B0C10"        # page-card background
PANEL = "#12141A"     # inner panels
PANEL_2 = "#171A22"
LINE = "#252936"      # hairlines, borders
GRID = "#1B1E27"
INK = "#EDEBE4"       # = portfolio paper colour
INK_2 = "#BDBBB3"
MUTED = "#8B8E99"
DIM = "#5C606C"
GREEN = "#3DDC84"

ROLE = {
    "web": "#5B6CFF",   # Next.js & full-stack   (portfolio cobalt, lifted for dark)
    "3d": "#F5A300",    # 3D / Three.js          (portfolio amber)
    "ai": "#FF3B55",    # AI / agents            (portfolio red, lifted for dark)
}
ROLE["agent"] = "#A77BFF"   # agents / orchestration: between AI red and web blue
ROLE_NAME = {"web": "NEXT.JS", "3d": "3D", "ai": "AI"}


def mix(c1: str, c2: str, t: float) -> str:
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


# ------------------------------------------------------------- components --
def card(doc: Doc, x=0, y=0, w=None, h=None, r=18, fill=BG, stroke=LINE) -> str:
    w = doc.w if w is None else w
    h = doc.h if h is None else h
    return (f'<rect x="{num(x + .5)}" y="{num(y + .5)}" width="{num(w - 1)}" height="{num(h - 1)}" '
            f'rx="{r}" fill="{fill}" stroke="{stroke}"/>')


def dot_grid(doc: Doc, x, y, w, h, step=22, color=GRID, r=1.1) -> str:
    pid = doc.add_def("dotgrid", f'<pattern id="dotgrid" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
                                 f'<circle cx="{step/2}" cy="{step/2}" r="{r}" fill="{color}"/></pattern>')
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{pid})"/>'


def chip(doc: Doc, x, y, text, color, *, fkey="mono-bold", size=12, pad=10, h=24, filled=False) -> tuple[str, float]:
    from .type import measure
    tw = measure(fkey, text, size, 0.6)
    w = tw + pad * 2
    fill = color if filled else mix(BG, color, 0.14)
    tcol = BG if filled else color
    stroke = color if not filled else color
    s = (f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{h}" rx="{h/2}" fill="{fill}" '
         f'stroke="{stroke}" stroke-opacity="{0 if filled else .45}"/>')
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
