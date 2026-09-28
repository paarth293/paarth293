"""Animated project illustrations, shared by the profile cards and repo banners.

Each function draws into the box (x, y, w, h) and returns markup. The static
attributes of every animated element describe a meaningful still frame.
"""
from __future__ import annotations

import math
import random

from design.doc import Doc, num
from design.kit import (BG, PANEL, PANEL_2, LINE, INK, INK_2, MUTED, DIM, GREEN, ROLE, mix, prism, pts, iso,
                        icosahedron, rot, project)
from design.motion import track, anim


def frame(doc: Doc, x, y, w, h, label: str | None = None) -> str:
    s = f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
    if label:
        s += doc.text("mono", label, x + 16, y + 26, 11, DIM, tracking=1.2)
    return s


# --------------------------------------------------------------- pipeline --
def pipeline(doc: Doc, x, y, w, h, color=None) -> str:
    color = color or ROLE["ai"]
    P = 7.5
    out = frame(doc, x, y, w, h, "PIPELINE · 14 STAGES")
    cols, gap = 7, (w - 48) / 7
    sq = min(34, gap - 10)
    rows_y = [y + h * 0.36, y + h * 0.60]
    centers = []
    for i in range(14):
        r = i // 7
        c = i % 7 if r == 0 else 6 - i % 7
        cx = x + 24 + gap * c + gap / 2
        centers.append((cx, rows_y[r]))
    path = "M" + " L".join(f"{num(a)} {num(b)}" for a, b in centers)
    out += f'<path d="{path}" fill="none" stroke="{LINE}" stroke-width="2"/>'
    for i, (cx, cy) in enumerate(centers):
        t_on = 0.3 + i * 0.36
        kf = track(doc, P, [(0, f"fill:{PANEL_2};stroke:{LINE}"), (t_on, f"fill:{PANEL_2};stroke:{LINE}"),
                            (t_on + .12, f"fill:{mix(BG, color, .35)};stroke:{color}"), (6.6, f"fill:{mix(BG, color, .35)};stroke:{color}"),
                            (7.1, f"fill:{PANEL_2};stroke:{LINE}")])
        out += (f'<rect x="{num(cx - sq/2)}" y="{num(cy - sq/2)}" width="{num(sq)}" height="{num(sq)}" rx="7" '
                f'fill="{mix(BG, color, .35)}" stroke="{color}" stroke-width="1.5" style="{anim(kf, P)}"/>')
        out += doc.text("mono-bold", f"{i+1:02d}", cx, cy + 4, 11, INK, anchor="middle")
    # travelling pulse
    tp = [(0, f"transform:translate({num(centers[0][0])}px,{num(centers[0][1])}px);opacity:0"),
          (0.2, f"transform:translate({num(centers[0][0])}px,{num(centers[0][1])}px);opacity:1")]
    for i, (cx, cy) in enumerate(centers):
        tp.append((0.3 + i * 0.36, f"transform:translate({num(cx)}px,{num(cy)}px);opacity:1"))
    tp += [(5.4, f"transform:translate({num(centers[-1][0])}px,{num(centers[-1][1])}px);opacity:0")]
    out += (f'<circle r="6" fill="{INK}" opacity="0" style="{anim(track(doc, P, tp), P)}"/>')
    # hash chain
    hy = y + h - 46
    out += doc.text("mono", "SHA-256 AUDIT CHAIN", x + 16, hy - 12, 10.5, DIM, tracking=1)
    rng = random.Random(3)
    bw = (w - 32 - 3 * 14) / 4
    for k in range(4):
        bx = x + 16 + k * (bw + 14)
        hx = "".join(rng.choice("0123456789abcdef") for _ in range(6))
        op_kf = None
        if k == 3:
            op_kf = track(doc, P, [(0, "opacity:.25"), (5.3, "opacity:.25"), (5.6, "opacity:1"), (7.0, "opacity:1"), (7.4, "opacity:.25")])
        style = f' style="{anim(op_kf, P)}"' if op_kf else ""
        out += (f'<g{style}><rect x="{num(bx)}" y="{num(hy)}" width="{num(bw)}" height="28" rx="6" fill="{PANEL_2}" stroke="{color if k == 3 else LINE}"/>'
                + doc.text("mono", f"#{hx}…", bx + bw / 2, hy + 18.5, 11, INK_2 if k < 3 else color, anchor="middle") + "</g>")
        if k:
            out += f'<line x1="{num(bx - 14)}" y1="{num(hy + 14)}" x2="{num(bx)}" y2="{num(hy + 14)}" stroke="{MUTED}" stroke-width="1.5"/>'
    return out


# ---------------------------------------------------------------- air-gap --
def airgap(doc: Doc, x, y, w, h, color=None) -> str:
    color = color or ROLE["ai"]
    P = 6.0
    out = frame(doc, x, y, w, h)
    bx, by, bw, bh = x + 16, y + 16, w * 0.70, h - 32
    out += (f'<rect x="{num(bx)}" y="{num(by)}" width="{num(bw)}" height="{num(bh)}" rx="12" fill="none" '
            f'stroke="{MUTED}" stroke-dasharray="6 5"/>')
    out += doc.text("mono", "AIR-GAPPED SITE", bx + 14, by + 22, 10.5, DIM, tracking=1.2)
    cx, cy = bx + bw / 2, by + bh / 2 + 8
    r = min(bw, bh) * 0.34
    nodes = [("reason", -150), ("code", -30), ("vision", 30), ("docs", 150)]
    for k, (lab, ang) in enumerate(nodes):
        a = math.radians(ang)
        nx, ny = cx + math.cos(a) * r * 1.25, cy + math.sin(a) * r * 0.9
        out += f'<line x1="{num(cx)}" y1="{num(cy)}" x2="{num(nx)}" y2="{num(ny)}" stroke="{LINE}" stroke-width="1.5"/>'
        t0 = 0.4 + k * 1.2
        kf = track(doc, P, [(0, f"transform:translate({num(cx)}px,{num(cy)}px);opacity:0"),
                            (t0, f"transform:translate({num(cx)}px,{num(cy)}px);opacity:1"),
                            (t0 + .7, f"transform:translate({num(nx)}px,{num(ny)}px);opacity:1"),
                            (t0 + .8, f"transform:translate({num(nx)}px,{num(ny)}px);opacity:0")])
        out += f'<circle r="4" fill="{color}" opacity="0" style="{anim(kf, P)}"/>'
        nk = track(doc, P, [(0, f"stroke:{LINE}"), (t0 + .65, f"stroke:{LINE}"), (t0 + .75, f"stroke:{color}"),
                            (t0 + 1.4, f"stroke:{color}"), (t0 + 1.7, f"stroke:{LINE}")])
        tw = 64
        out += (f'<rect x="{num(nx - tw/2)}" y="{num(ny - 15)}" width="{tw}" height="30" rx="8" fill="{PANEL_2}" '
                f'stroke="{LINE}" stroke-width="1.5" style="{anim(nk, P)}"/>')
        out += doc.text("mono", lab, nx, ny + 4.5, 12, INK_2, anchor="middle")
    out += f'<circle cx="{num(cx)}" cy="{num(cy)}" r="30" fill="{mix(BG, color, .25)}" stroke="{color}" stroke-width="1.5"/>'
    out += doc.text("mono-bold", "LLM", cx, cy - 1, 12, INK, anchor="middle")
    out += doc.text("mono", "ollama", cx, cy + 14, 9.5, INK_2, anchor="middle")
    # outside: the internet, cut off
    gx, gy = x + w - 46, y + h / 2
    out += (f'<circle cx="{num(gx)}" cy="{num(gy)}" r="18" fill="none" stroke="{DIM}"/>'
            f'<ellipse cx="{num(gx)}" cy="{num(gy)}" rx="8" ry="18" fill="none" stroke="{DIM}"/>'
            f'<line x1="{num(gx - 18)}" y1="{num(gy)}" x2="{num(gx + 18)}" y2="{num(gy)}" stroke="{DIM}"/>')
    out += doc.text("mono", "internet", gx, gy + 36, 10, DIM, anchor="middle")
    lx1, lx2 = bx + bw + 2, gx - 22
    out += f'<line x1="{num(lx1)}" y1="{num(gy)}" x2="{num(lx2)}" y2="{num(gy)}" stroke="{DIM}" stroke-dasharray="3 4"/>'
    mx = (lx1 + lx2) / 2
    blink = track(doc, 1.6, [(0, "opacity:1"), (0.8, "opacity:1"), (0.81, "opacity:.25"), (1.6, "opacity:.25")])
    out += (f'<g style="{anim(blink, 1.6)}" stroke="{ROLE["ai"]}" stroke-width="2.5" stroke-linecap="round">'
            f'<line x1="{num(mx - 6)}" y1="{num(gy - 6)}" x2="{num(mx + 6)}" y2="{num(gy + 6)}"/>'
            f'<line x1="{num(mx + 6)}" y1="{num(gy - 6)}" x2="{num(mx - 6)}" y2="{num(gy + 6)}"/></g>')
    return out


# ----------------------------------------------------------------- memory --
MEMS = ["project uses Prisma ORM", "tests run with pytest -q", "API base path: /v1", "deploy via docker compose",
        "prefers small, typed PRs"]


def memory(doc: Doc, x, y, w, h, color=None) -> str:
    color = color or ROLE["ai"]
    P = 8.0
    out = frame(doc, x, y, w, h, "MEMORY · HYBRID RECALL")
    rh, gap = 30, 9
    top = y + 44
    rw = w - 32
    for i, m in enumerate(MEMS):
        ry = top + i * (rh + gap)
        out += f'<rect x="{num(x + 16)}" y="{num(ry)}" width="{num(rw)}" height="{rh}" rx="8" fill="{PANEL_2}" stroke="{LINE}"/>'
        if i == 2:
            # stale record: struck out, then replaced by the resolved one
            old = doc.text("mono", m, x + 30, ry + 19.5, 12, INK_2)
            ow = len(m) * 7.2
            kf_old = track(doc, P, [(0, "opacity:1"), (3.6, "opacity:1"), (4.0, "opacity:0"), (7.4, "opacity:0"), (7.8, "opacity:1")])
            kf_strike = track(doc, P, [(0, "transform:scaleX(0)"), (2.6, "transform:scaleX(0)"), (3.2, "transform:scaleX(1)"),
                                       (7.4, "transform:scaleX(1)"), (7.8, "transform:scaleX(0)")])
            kf_new = track(doc, P, [(0, "opacity:0"), (3.8, "opacity:0"), (4.2, "opacity:1"), (7.4, "opacity:1"), (7.8, "opacity:0")])
            out += f'<g opacity="0" style="{anim(kf_old, P)}">{old}<line x1="{num(x + 28)}" y1="{num(ry + 15)}" x2="{num(x + 32 + ow)}" y2="{num(ry + 15)}" stroke="{ROLE["ai"]}" stroke-width="2" class="sx" style="{anim(kf_strike, P)}"/></g>'
            new = doc.text("mono", "API base path: /v2", x + 30, ry + 19.5, 12, INK)
            tag_w = 74
            new += (f'<rect x="{num(x + 16 + rw - tag_w - 8)}" y="{num(ry + 6)}" width="{tag_w}" height="18" rx="9" fill="{mix(BG, GREEN, .2)}"/>'
                    + doc.text("mono-bold", "resolved", x + 16 + rw - tag_w / 2 - 8, ry + 18.5, 10, GREEN, anchor="middle"))
            out += f'<g style="{anim(kf_new, P)}">{new}</g>'
        else:
            out += doc.text("mono", m, x + 30, ry + 19.5, 12, INK_2)
    doc.style(".sx{transform-box:fill-box;transform-origin:0 50%}")
    # recall beam sweeping the rows
    beam = [(0, f"transform:translateY(0px);opacity:0"), (0.3, "transform:translateY(0px);opacity:1")]
    for i in range(len(MEMS)):
        beam.append((0.3 + i * 0.5, f"transform:translateY({i * (rh + gap)}px);opacity:1"))
    beam += [(2.6, f"transform:translateY({2 * (rh + gap)}px);opacity:1"), (3.3, f"transform:translateY({2 * (rh + gap)}px);opacity:0")]
    out += (f'<rect x="{num(x + 12)}" y="{num(top - 3)}" width="{num(rw + 8)}" height="{rh + 6}" rx="10" fill="none" '
            f'stroke="{color}" stroke-width="2" opacity="0" style="{anim(track(doc, P, beam), P)}"/>')
    return out


# ------------------------------------------------------------- mini city --
def mini_city(doc: Doc, x, y, w, h, color=None, pin_label="The Index") -> str:
    P = 9.0
    out = frame(doc, x, y, w, h)
    n = 5
    heights = {(0, 0): 1.3, (1, 0): 0.9, (2, 0): 1.7, (3, 0): 1.1, (4, 0): 0.8, (0, 1): 1.0, (1, 1): 2.2, (2, 1): 1.2,
               (3, 1): 1.9, (4, 1): 0.9, (0, 2): 1.5, (1, 2): 0.8, (2, 2): 2.6, (3, 2): 1.0, (4, 2): 1.3,
               (0, 3): 0.7, (1, 3): 1.4, (2, 3): 0.9, (3, 3): 1.6, (4, 3): 0.6, (0, 4): 0.9, (1, 4): 0.6,
               (2, 4): 1.1, (3, 4): 0.7, (4, 4): 0.5}
    probe = [iso(a, b, 0, 1, 0, 0) for a in (0, n) for b in (0, n)]
    probe += [iso(i + a, j + b, hh, 1, 0, 0) for (i, j), hh in heights.items() for a in (0, 1) for b in (0, 1)]
    xs, ys = [p[0] for p in probe], [p[1] for p in probe]
    region = (x + 24, y + 60, w - 48, h - 76)
    s = min(region[2] / (max(xs) - min(xs)), region[3] / (max(ys) - min(ys)))
    ox = region[0] + region[2] / 2 - s * (min(xs) + max(xs)) / 2
    oy = region[1] + region[3] / 2 - s * (min(ys) + max(ys)) / 2
    top, left, right = prism(-.1, -.1, n + .2, n + .2, .1, s, ox, oy - .1 * s)
    out += f'<polygon points="{pts(left)}" fill="#12141B"/><polygon points="{pts(right)}" fill="#171A23"/><polygon points="{pts(top)}" fill="#101218" stroke="{LINE}"/>'
    seq = [((2, 2), "web"), ((3, 3), "3d"), ((1, 3), "ai")]
    base = {"top": "#272B38", "left": "#161921", "right": "#1D212C"}
    for (i, j), hh in sorted(heights.items(), key=lambda kv: (kv[0][0] + kv[0][1], kv[0][0])):
        t_, l_, r_ = prism(i + .15, j + .15, .7, .7, hh, s, ox, oy)
        hits = [k for k, (cell, _) in enumerate(seq) if cell == (i, j)]
        faces = ""
        for name, poly in (("left", l_), ("right", r_), ("top", t_)):
            if hits:
                k = hits[0]
                c = ROLE[seq[k][1]]
                col = {"top": c, "left": mix(BG, c, .42), "right": mix(BG, c, .62)}[name]
                a = k * 3.0
                kf = track(doc, P, [(0, f"fill:{base[name]}"), (a + .3, f"fill:{base[name]}"), (a + .6, f"fill:{col}"),
                                    (a + 2.6, f"fill:{col}"), (a + 2.9, f"fill:{base[name]}")])
                static = col if k == 0 else base[name]
                faces += f'<polygon points="{pts(poly)}" fill="{static}" stroke="{BG}" stroke-width=".8" style="{anim(kf, P)}"/>'
            else:
                faces += f'<polygon points="{pts(poly)}" fill="{base[name]}" stroke="{BG}" stroke-width=".8"/>'
        out += faces
    # pin over the tallest block
    px, py = iso(2.5, 2.5, heights[(2, 2)], s, ox, oy)
    bounce = track(doc, 1.8, [(0, "transform:translateY(0px)"), (0.9, "transform:translateY(-8px)"), (1.8, "transform:translateY(0px)")])
    out += (f'<g style="{anim(bounce, 1.8, ease="ease-in-out")}"><line x1="{num(px)}" y1="{num(py - 4)}" x2="{num(px)}" y2="{num(py - 34)}" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{num(px)}" cy="{num(py - 40)}" r="7" fill="{INK}"/><circle cx="{num(px)}" cy="{num(py - 40)}" r="2.6" fill="{BG}"/></g>')
    out += doc.text("mono", "?q=", x + 16, y + 28, 12, DIM)
    out += doc.text("mono", "next.js + three.js + agents", x + 44, y + 28, 12, INK_2)
    return out


# ---------------------------------------------------------- wireframe 3D --
def wireframe(doc: Doc, x, y, w, h, color=None, frames=48, period=8.0) -> str:
    color = color or ROLE["3d"]
    cid = doc.uid("wf")
    out = f'<clipPath id="{cid}"><rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}"/></clipPath><g clip-path="url(#{cid})">'
    cx, cy = x + w / 2, y + h * 0.46
    R = min(w, h) * 0.34
    # perspective floor
    floor = ""
    fy = y + h * 0.86
    for k in range(-5, 6):
        a = project((k * 0.5, -1.25, -1.2), 3.2, cx, fy - 40, R)
        b = project((k * 0.5, -1.25, 1.8), 3.2, cx, fy - 40, R)
        floor += f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(b[0])}" y2="{num(b[1])}"/>'
    for k in range(0, 7):
        z = -1.2 + k * 0.5
        a = project((-2.5, -1.25, z), 3.2, cx, fy - 40, R)
        b = project((2.5, -1.25, z), 3.2, cx, fy - 40, R)
        floor += f'<line x1="{num(a[0])}" y1="{num(a[1])}" x2="{num(b[0])}" y2="{num(b[1])}"/>'
    out += f'<g stroke="{LINE}" stroke-width="1">{floor}</g>'
    v, edges = icosahedron()
    for f_i in range(frames):
        ang = 2 * math.pi * f_i / frames
        pv = [project(rot(p, 0.42, ang, 0.18), 3.2, cx, cy, R) for p in v]
        buckets = {0: "", 1: "", 2: ""}
        for a, b in edges:
            z = (pv[a][2] + pv[b][2]) / 2
            bk = 0 if z < -0.25 else (1 if z < 0.25 else 2)
            buckets[bk] += f"M{num(pv[a][0])} {num(pv[a][1])}L{num(pv[b][0])} {num(pv[b][1])}"
        g = ""
        for bk, op in ((2, .22), (1, .55), (0, 1)):
            if buckets[bk]:
                g += f'<path d="{buckets[bk]}" stroke-opacity="{op}"/>'
        dots = "".join(f'<circle cx="{num(px)}" cy="{num(py)}" r="{2.8 if pz < 0 else 1.6}"/>' for px, py, pz in pv)
        t0 = f_i * period / frames
        kf = track(doc, period, [(0, "opacity:0"), (t0, "opacity:0"), (t0 + .001, "opacity:1"),
                                 (t0 + period / frames, "opacity:1"), (t0 + period / frames + .001, "opacity:0")])
        out += (f'<g opacity="{1 if f_i == 0 else 0}" style="{anim(kf, period)}">'
                f'<g fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round">{g}</g>'
                f'<g fill="{color}">{dots}</g></g>')
    # shadow
    sy = fy - 40 + 8
    out += f'<ellipse cx="{num(cx)}" cy="{num(y + h * 0.83)}" rx="{num(R * .8)}" ry="{num(R * .14)}" fill="{color}" opacity=".08"/>'
    return out + "</g>"


# ----------------------------------------------------------- request flow --
def request_flow(doc: Doc, x, y, w, h, color=None) -> str:
    color = color or ROLE["web"]
    P = 4.8
    out = ""
    # browser window
    bw, bh = w * 0.42, h * 0.72
    bx, by = x + 10, y + (h - bh) / 2
    out += (f'<rect x="{num(bx)}" y="{num(by)}" width="{num(bw)}" height="{num(bh)}" rx="10" fill="{PANEL_2}" stroke="{LINE}"/>'
            f'<line x1="{num(bx)}" y1="{num(by + 22)}" x2="{num(bx + bw)}" y2="{num(by + 22)}" stroke="{LINE}"/>')
    for k, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        out += f'<circle cx="{num(bx + 14 + k * 11)}" cy="{num(by + 11)}" r="3.2" fill="{c}" opacity=".8"/>'
    # skeleton page
    sk = [(0.12, 0.36, 0.55, 10), (0.12, 0.50, 0.76, 6), (0.12, 0.60, 0.66, 6)]
    for fx, fy, fw, fh in sk:
        out += f'<rect x="{num(bx + bw * fx)}" y="{num(by + bh * fy)}" width="{num(bw * fw)}" height="{fh}" rx="3" fill="{LINE}"/>'
    card_kf = track(doc, P, [(0, f"fill:{PANEL}"), (3.9, f"fill:{PANEL}"), (4.1, f"fill:{mix(BG, color, .45)}"), (4.6, f"fill:{mix(BG, color, .45)}"), (4.8, f"fill:{PANEL}")])
    out += (f'<rect x="{num(bx + bw * .12)}" y="{num(by + bh * .72)}" width="{num(bw * .76)}" height="{num(bh * .16)}" rx="5" '
            f'fill="{PANEL}" stroke="{LINE}" style="{anim(card_kf, P)}"/>')
    # server stack
    labels = ["app router", "api · jwt", "postgres"]
    sw, shh, sg = w * 0.44, 34, 12
    sx = x + w - sw - 6
    total = 3 * shh + 2 * sg
    sy0 = y + (h - total) / 2
    boxes = []
    for k, lab in enumerate(labels):
        yy = sy0 + k * (shh + sg)
        boxes.append((sx, yy))
        kf = track(doc, P, [(0, f"stroke:{LINE}"), (0.5 + k * .7, f"stroke:{LINE}"), (0.6 + k * .7, f"stroke:{color}"),
                            (1.2 + k * .7, f"stroke:{color}"), (1.4 + k * .7, f"stroke:{LINE}")])
        out += (f'<rect x="{num(sx)}" y="{num(yy)}" width="{num(sw)}" height="{shh}" rx="8" fill="{PANEL_2}" stroke="{LINE}" '
                f'stroke-width="1.5" style="{anim(kf, P)}"/>')
        out += doc.text("mono", lab, sx + 12, yy + 21.5, 12, INK_2)
        if k:
            out += f'<line x1="{num(sx + sw/2)}" y1="{num(yy - sg)}" x2="{num(sx + sw/2)}" y2="{num(yy)}" stroke="{LINE}" stroke-width="1.5"/>'
    ax1, ay = bx + bw, sy0 + shh / 2
    out += f'<line x1="{num(ax1)}" y1="{num(ay)}" x2="{num(sx)}" y2="{num(ay)}" stroke="{LINE}" stroke-width="1.5"/>'
    # packet: browser → app → api → db → back
    mid = sx + sw / 2
    path = [(0, ax1, ay, 0), (0.5, sx, ay, 1), (0.6, mid, ay, 1), (1.3, mid, boxes[1][1] + shh / 2, 1),
            (2.0, mid, boxes[2][1] + shh / 2, 1), (2.7, mid, boxes[1][1] + shh / 2, 1), (3.3, mid, ay, 1),
            (3.4, sx, ay, 1), (3.9, ax1, ay, 1), (4.0, ax1, ay, 0)]
    kf = track(doc, P, [(t, f"transform:translate({num(px)}px,{num(py)}px);opacity:{o}") for t, px, py, o in path])
    out += f'<circle r="5" fill="{color}" opacity="0" style="{anim(kf, P)}"/>'
    return out


# ------------------------------------------------------------- agent loop --
def agent_loop(doc: Doc, x, y, w, h, color=None) -> str:
    color = color or ROLE["ai"]
    P = 7.5
    out = ""
    cx, cy = x + w / 2, y + h / 2 + 4
    rx, ry = w * 0.36, h * 0.36
    steps = ["plan", "retrieve", "act", "observe", "remember"]
    out += f'<ellipse cx="{num(cx)}" cy="{num(cy)}" rx="{num(rx)}" ry="{num(ry)}" fill="none" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="3 5"/>'
    pos = []
    for k, s in enumerate(steps):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        px, py = cx + math.cos(a) * rx, cy + math.sin(a) * ry
        pos.append((px, py))
    seg = P / 5
    for k, (s, (px, py)) in enumerate(zip(steps, pos)):
        t0 = k * seg
        kf = track(doc, P, [(0, f"fill:{PANEL_2};stroke:{LINE}"), (t0, f"fill:{PANEL_2};stroke:{LINE}"),
                            (t0 + .15, f"fill:{mix(BG, color, .4)};stroke:{color}"), (t0 + seg, f"fill:{mix(BG, color, .4)};stroke:{color}"),
                            (t0 + seg + .2, f"fill:{PANEL_2};stroke:{LINE}")])
        tw = max(58, len(s) * 7.8 + 18)
        static = (mix(BG, color, .4), color) if k == 0 else (PANEL_2, LINE)
        out += (f'<rect x="{num(px - tw/2)}" y="{num(py - 13)}" width="{num(tw)}" height="26" rx="13" fill="{static[0]}" '
                f'stroke="{static[1]}" stroke-width="1.5" style="{anim(kf, P)}"/>')
        out += doc.text("mono", s, px, py + 4.5, 12, INK, anchor="middle")
    out += f'<circle cx="{num(cx)}" cy="{num(cy)}" r="24" fill="{mix(BG, color, .22)}" stroke="{color}" stroke-width="1.5"/>'
    out += doc.text("mono-bold", "LLM", cx, cy + 4.5, 12, INK, anchor="middle")
    # spokes pulse to the active step
    for k, (px, py) in enumerate(pos):
        t0 = k * seg
        kf = track(doc, P, [(0, "opacity:0"), (t0, "opacity:0"), (t0 + .1, "opacity:.9"), (t0 + seg * .8, "opacity:.9"), (t0 + seg, "opacity:0")])
        out += (f'<line x1="{num(cx)}" y1="{num(cy)}" x2="{num(px)}" y2="{num(py)}" stroke="{color}" stroke-width="1.5" '
                f'stroke-dasharray="2 4" opacity="{1 if k == 0 else 0}" style="{anim(kf, P)}"/>')
    return out


# -------------------------------------------------------------- volunteer --
def geo_map(doc: Doc, x, y, w, h, color=None) -> str:
    color = color or ROLE["web"]
    P = 7.0
    out = frame(doc, x, y, w, h, "VERIFIED NEEDS · LIVE MAP")
    rng = random.Random(11)
    streets = ""
    for k in range(7):
        yy = y + 50 + k * (h - 70) / 6
        streets += f'<line x1="{num(x + 16)}" y1="{num(yy + rng.uniform(-6, 6))}" x2="{num(x + w - 16)}" y2="{num(yy + rng.uniform(-6, 6))}"/>'
    for k in range(9):
        xx = x + 30 + k * (w - 60) / 8
        streets += f'<line x1="{num(xx + rng.uniform(-8, 8))}" y1="{num(y + 44)}" x2="{num(xx + rng.uniform(-8, 8))}" y2="{num(y + h - 16)}"/>'
    out += f'<g stroke="{LINE}" stroke-width="1.2">{streets}</g>'
    pins = [(0.22, 0.40), (0.48, 0.30), (0.74, 0.46), (0.34, 0.72), (0.62, 0.78), (0.86, 0.66)]
    for k, (fx, fy) in enumerate(pins):
        px, py = x + w * fx, y + h * fy
        t0 = 0.4 + k * 0.9
        kf = track(doc, P, [(0, f"fill:{DIM}"), (t0, f"fill:{DIM}"), (t0 + .2, f"fill:{GREEN}"), (6.4, f"fill:{GREEN}"), (6.8, f"fill:{DIM}")])
        out += (f'<path d="M{num(px)} {num(py)} c-7-9-11-13-11-18a11 11 0 0 1 22 0c0 5-4 9-11 18z" fill="{GREEN if k == 0 else DIM}" style="{anim(kf, P)}"/>'
                f'<circle cx="{num(px)}" cy="{num(py - 18)}" r="3.6" fill="{PANEL}"/>')
    # volunteer
    route = [(0, 0.1, 0.9), (2.0, 0.34, 0.72), (4.0, 0.62, 0.78), (6.0, 0.86, 0.66), (7.0, 0.1, 0.9)]
    kf = track(doc, P, [(t, f"transform:translate({num(x + w*fx)}px,{num(y + h*fy - 4)}px)") for t, fx, fy in route])
    out += f'<g style="{anim(kf, P, ease="ease-in-out")}"><circle r="9" fill="{color}" opacity=".25"/><circle r="5" fill="{color}"/></g>'
    return out


# -------------------------------------------------------------------- blur --
DIGIT = ["....####....", "...#....#...", "..#......#..", "..........#.", ".........#..", "........#...",
         ".......#....", "......#.....", ".....#......", "....#.......", "...#........", "...######..."]


def blur_grid(doc: Doc, x, y, w, h, color=None) -> str:
    color = color or ROLE["ai"]
    out = frame(doc, x, y, w, h, "SAME DIGIT · RISING BLUR")
    levels = [0, 1.2, 2.4, 3.6]
    cw = (w - 32 - 3 * 14) / 4
    cell = cw / 12
    gy = y + 48
    for k, sd in enumerate(levels):
        gx = x + 16 + k * (cw + 14)
        fid = f"bl{k}"
        if sd:
            doc.add_def(fid, f'<filter id="{fid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{sd}"/></filter>')
        cells = ""
        for r, row in enumerate(DIGIT):
            for c, ch in enumerate(row):
                if ch == "#":
                    cells += f'<rect x="{num(gx + c*cell)}" y="{num(gy + r*cell)}" width="{num(cell)}" height="{num(cell)}"/>'
        out += f'<rect x="{num(gx)}" y="{num(gy)}" width="{num(cw)}" height="{num(cw)}" rx="6" fill="{BG}" stroke="{LINE}"/>'
        f = f' filter="url(#{fid})"' if sd else ""
        out += f'<g fill="{INK}"{f}>{cells}</g>'
        out += doc.text("mono", f"blur {sd:g}", gx + cw / 2, gy + cw + 22, 12, INK_2 if k == 0 else MUTED, anchor="middle")
    # scanning marker
    P = 6.0
    kf = track(doc, P, [(0, "transform:translateX(0px)")] +
               [(0.2 + k * 1.4, f"transform:translateX({num(k * (cw + 14))}px)") for k in range(4)] +
               [(5.8, f"transform:translateX({num(3 * (cw + 14))}px)"), (6.0, "transform:translateX(0px)")])
    out += (f'<rect x="{num(x + 12)}" y="{num(gy - 4)}" width="{num(cw + 8)}" height="{num(cw + 8)}" rx="8" fill="none" '
            f'stroke="{color}" stroke-width="2" style="{anim(kf, P, ease="ease-in-out")}"/>')
    out += doc.text("mono", "CNN · Xception · DenseNet · SqueezeNet", x + w / 2, y + h - 16, 11, DIM, anchor="middle")
    return out
