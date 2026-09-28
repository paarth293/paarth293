"""Text → vector outlines.

Every word in every image is converted to <path> outlines from the real
font files in ../fonts (Bricolage Grotesque, Instrument Sans, Geist Mono --
the same faces the portfolio uses). That means:

* the type looks identical on Windows, macOS, Linux, iOS and Android;
* GitHub's image proxy can't strip or swap the font (it never loads one);
* text can be measured exactly, so layout overflow is caught at build time
  (see `fit()`), not discovered later on someone's screen.

Glyph outlines are emitted once per SVG in <defs> and reused with <use>, so a
headline costs a few hundred bytes per unique letter, not per occurrence.
"""
from __future__ import annotations

import os
import re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")


class LayoutError(Exception):
    """Raised when a piece of text does not fit the box it was given."""


class Font:
    def __init__(self, key: str, filename: str):
        self.key = key
        self.tt = TTFont(os.path.join(FONT_DIR, filename))
        self.glyphs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.upm = self.tt["head"].unitsPerEm
        self.hmtx = self.tt["hmtx"]
        self.kern = self._read_kerning()
        self._paths: dict[str, str] = {}

    # -- kerning ---------------------------------------------------------
    def _read_kerning(self) -> dict[tuple[str, str], int]:
        """Flatten GPOS PairPos (formats 1 and 2) into {(left, right): dx}."""
        pairs: dict[tuple[str, str], int] = {}
        if "GPOS" not in self.tt:
            return pairs
        gpos = self.tt["GPOS"].table
        if not gpos.LookupList:
            return pairs
        for lookup in gpos.LookupList.Lookup:
            subtables = []
            for st in lookup.SubTable:
                if lookup.LookupType == 9:  # extension
                    st = st.ExtSubTable
                    if getattr(st, "LookupType", None) != 2 and not hasattr(st, "PairSet") and not hasattr(st, "Class1Record"):
                        continue
                elif lookup.LookupType != 2:
                    continue
                subtables.append(st)
            for st in subtables:
                if st.Format == 1:
                    for left, ps in zip(st.Coverage.glyphs, st.PairSet):
                        for rec in ps.PairValueRecord:
                            v = getattr(rec.Value1, "XAdvance", 0) if rec.Value1 else 0
                            if v and (left, rec.SecondGlyph) not in pairs:
                                pairs[(left, rec.SecondGlyph)] = v
                elif st.Format == 2:
                    c1 = st.ClassDef1.classDefs if st.ClassDef1 else {}
                    c2 = st.ClassDef2.classDefs if st.ClassDef2 else {}
                    by1: dict[int, list[str]] = {}
                    for g in st.Coverage.glyphs:
                        by1.setdefault(c1.get(g, 0), []).append(g)
                    by2: dict[int, list[str]] = {}
                    for g, c in c2.items():
                        by2.setdefault(c, []).append(g)
                    for i1, rec1 in enumerate(st.Class1Record):
                        lefts = by1.get(i1)
                        if not lefts:
                            continue
                        for i2, rec2 in enumerate(rec1.Class2Record):
                            v = getattr(rec2.Value1, "XAdvance", 0) if rec2.Value1 else 0
                            if not v or i2 == 0:
                                continue
                            for l in lefts:
                                for r in by2.get(i2, ()):
                                    pairs.setdefault((l, r), v)
        return pairs

    # -- glyphs ----------------------------------------------------------
    def gname(self, ch: str) -> str | None:
        return self.cmap.get(ord(ch))

    def advance(self, gname: str) -> int:
        return self.hmtx[gname][0]

    def path(self, gname: str) -> str:
        if gname not in self._paths:
            pen = SVGPathPen(self.glyphs)
            # flip Y: font units are y-up, SVG is y-down
            self.glyphs[gname].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
            d = pen.getCommands()
            # integer coordinates are plenty at 1000 upm
            d = re.sub(r"-?\d+\.\d+", lambda m: str(round(float(m.group()))), d)
            self._paths[gname] = d
        return self._paths[gname]


_FONTS: dict[str, Font] = {}


def font(key: str) -> Font:
    files = {
        "display": "BricolageGrotesque-Bold.ttf",
        "display-regular": "BricolageGrotesque-Regular.ttf",
        "body": "InstrumentSans-Regular.ttf",
        "body-bold": "InstrumentSans-Bold.ttf",
        "mono": "GeistMono-Regular.ttf",
        "mono-bold": "GeistMono-Bold.ttf",
    }
    if key not in _FONTS:
        _FONTS[key] = Font(key, files[key])
    return _FONTS[key]


FALLBACK = ["mono", "body"]


def _resolve(fkey: str, ch: str) -> tuple[Font, str]:
    f = font(fkey)
    g = f.gname(ch)
    if g:
        return f, g
    for alt in FALLBACK:
        f2 = font(alt)
        g2 = f2.gname(ch)
        if g2:
            return f2, g2
    raise LayoutError(f"no glyph for {ch!r} (U+{ord(ch):04X}) in {fkey} or fallbacks")


def shape(fkey: str, text: str, size: float, tracking: float = 0.0):
    """Return [(Font, gname, x_px)] and total advance width in px."""
    if not fkey.startswith("mono"):
        # proportional faces have a narrow space; give separators room to breathe
        text = text.replace(" · ", "  ·  ")
    out = []
    x = 0.0
    prev: tuple[Font, str] | None = None
    for ch in text:
        f, g = _resolve(fkey, ch)
        scale = size / f.upm
        if prev and prev[0] is f:
            x += f.kern.get((prev[1], g), 0) * scale
        out.append((f, g, x))
        x += f.advance(g) * scale + tracking
        prev = (f, g)
    width = x - tracking if text else 0.0
    return out, width


def measure(fkey: str, text: str, size: float, tracking: float = 0.0) -> float:
    return shape(fkey, text, size, tracking)[1]


def fit(fkey: str, text: str, size: float, max_width: float, tracking: float = 0.0, where: str = "") -> float:
    w = measure(fkey, text, size, tracking)
    if w > max_width + 0.5:
        raise LayoutError(f"{where}: {text!r} is {w:.0f}px wide, box is {max_width:.0f}px")
    return w


def wrap(fkey: str, text: str, size: float, max_width: float, tracking: float = 0.0) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if measure(fkey, trial, size, tracking) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        fit(fkey, ln, size, max_width, tracking, where="wrap")
    return lines
