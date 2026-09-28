"""A tiny SVG document builder: glyph defs, keyframes, reduced-motion safety."""
from __future__ import annotations

import hashlib
import re
from html import escape

from .type import shape, fit


def _sid(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", s)


def num(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def scl(v: float) -> str:
    """Scale factors need more precision than coordinates: 0.0155 must not become 0.02."""
    return f"{v:.6f}".rstrip("0").rstrip(".")


class Doc:
    def __init__(self, width: int, height: int, label: str):
        self.w = width
        self.h = height
        self.label = label
        self.defs: dict[str, str] = {}
        self.css: list[str] = []
        self._kf: dict[str, str] = {}
        self.body: list[str] = []
        self._n = 0

    # -- ids / defs -------------------------------------------------------
    def uid(self, prefix: str = "u") -> str:
        self._n += 1
        return f"{prefix}{self._n}"

    def add_def(self, key: str, markup: str) -> str:
        self.defs.setdefault(key, markup)
        return key

    def add(self, *markup: str) -> None:
        self.body.extend(markup)

    # -- css / animation ----------------------------------------------------
    def style(self, rule: str) -> None:
        self.css.append(rule)

    def keyframes(self, stops: list[tuple[float, str]]) -> str:
        """Register @keyframes from [(percent, 'prop:val;...')] and return its name.

        Identical keyframe bodies are shared, which keeps files small when
        many elements run the same motion with different delays.
        """
        body = "".join(f"{num(p)}%{{{decl}}}" for p, decl in stops)
        name = "k" + hashlib.md5(body.encode()).hexdigest()[:7]
        if name not in self._kf:
            self._kf[name] = f"@keyframes {name}{{{body}}}"
        return name

    # -- text ---------------------------------------------------------------
    def _glyph(self, f, g) -> str:
        gid = _sid(f"{f.key}-{g}")
        if gid not in self.defs:
            self.defs[gid] = f'<path id="{gid}" d="{f.path(g)}"/>'
        return gid

    def text(self, fkey: str, s: str, x: float, y: float, size: float, fill: str, *,
             anchor: str = "start", tracking: float = 0.0, max_width: float | None = None,
             where: str = "", attrs: str = "") -> str:
        glyphs, width = shape(fkey, s, size, tracking)
        if max_width is not None:
            fit(fkey, s, size, max_width, tracking, where=where or s[:24])
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        if not glyphs:
            return ""
        scale = size / glyphs[0][0].upm
        uses = "".join(
            f'<use href="#{self._glyph(f, g)}" x="{round(gx / scale)}"/>' for f, g, gx in glyphs if g not in ("space",)
        )
        return (f'<g transform="translate({num(x)} {num(y)}) scale({scl(scale)})" fill="{fill}"{attrs}>'
                f"{uses}</g>")

    def glyph_runs(self, fkey: str, s: str, x: float, y: float, size: float, tracking: float = 0.0):
        """Per-character placement for letter-by-letter animation.

        Returns [(char, markup, x_left_px, advance_px)], each markup a
        self-contained <g> positioned in user space.
        """
        glyphs, width = shape(fkey, s, size, tracking)
        out = []
        for i, (f, g, gx) in enumerate(glyphs):
            scale = size / f.upm
            nxt = glyphs[i + 1][2] if i + 1 < len(glyphs) else width
            mk = "" if g == "space" else (
                f'<use href="#{self._glyph(f, g)}" transform="translate({num(x + gx)} {num(y)}) scale({scl(scale)})"/>')
            out.append((s[i], mk, x + gx, nxt - gx))
        return out, width

    # -- output -------------------------------------------------------------
    def render(self) -> str:
        css = "".join(self._kf.values()) + "".join(self.css)
        # Every animated element is authored so its *static* attributes are a
        # correct, complete frame. Turning animation off therefore degrades to
        # a still image instead of hidden or overlapping content.
        css += "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        title = escape(self.label)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-labelledby="title">'
            f'<title id="title">{title}</title>'
            f"<defs><style>{css}</style>{''.join(self.defs.values())}</defs>"
            f"{''.join(self.body)}</svg>"
        )
