"""Experience (Language Metrics), the journey timeline, and proof tiles."""
from __future__ import annotations

from design.doc import Doc, num
from design.kit import BG, PANEL, PANEL_2, LINE, INK, INK_2, MUTED, DIM, GREEN, ROLE, card, chip, mix
from design.motion import track, anim
from design.type import wrap, measure
from sections.illus import frame

# ---------------------------------------------------------------- experience --
def portal(doc: Doc, x, y, w, h, color=None) -> str:
    from design.kit import ACCENT
    color = color or ACCENT
    P = 8.0
    out = frame(doc, x, y, w, h)
    # sidebar
    sw = 64
    out += f'<rect x="{x + 1}" y="{y + 1}" width="{sw}" height="{h - 2}" rx="5" fill="{PANEL_2}"/>'
    out += f'<line x1="{x + sw}" y1="{y + 1}" x2="{x + sw}" y2="{y + h - 1}" stroke="{LINE}"/>'
    for k in range(5):
        yy = y + 28 + k * 30
        fill = color if k == 1 else LINE
        out += f'<rect x="{x + 16}" y="{yy}" width="{sw - 32}" height="8" rx="4" fill="{fill}"/>'
    mx = x + sw + 18
    out += doc.text("mono", "admin / bookings", mx, y + 30, 11.5, DIM)
    # calendar
    cols, rows = 7, 4
    cw, ch, g = 30, 24, 6
    gy = y + 46
    booked = [(0, 1), (0, 3), (1, 0), (1, 4), (2, 2), (2, 5), (3, 1), (3, 6), (1, 6), (2, 0)]
    for r in range(rows):
        for c in range(cols):
            cx, cy = mx + c * (cw + g), gy + r * (ch + g)
            if (r, c) in booked:
                k = booked.index((r, c))
                t0 = 0.3 + k * 0.45
                kf = track(doc, P, [(0, f"fill:{PANEL_2}"), (t0, f"fill:{PANEL_2}"), (t0 + .15, f"fill:{color}"),
                                    (7.4, f"fill:{color}"), (7.8, f"fill:{PANEL_2}")])
                out += f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="2" fill="{color}" stroke="{LINE}" style="{anim(kf, P)}"/>'
            else:
                out += f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="2" fill="{PANEL_2}" stroke="{LINE}"/>'
    # wallet card
    wy = gy + rows * (ch + g) + 10
    ww = cols * (cw + g) - g
    out += f'<rect x="{mx}" y="{wy}" width="{ww}" height="52" rx="4" fill="{PANEL_2}" stroke="{LINE}"/>'
    out += doc.text("mono", "COIN WALLET", mx + 14, wy + 20, 10, DIM, tracking=1)
    out += f'<circle cx="{mx + 22}" cy="{wy + 36}" r="7" fill="#F5C542"/><circle cx="{mx + 22}" cy="{wy + 36}" r="3.5" fill="none" stroke="#8a6a12" stroke-width="1.2"/>'
    vals = ["240", "260", "280", "300", "320"]
    for k, v in enumerate(vals):
        a = 0.3 + k * 1.4
        b = a + 1.4 if k < len(vals) - 1 else 7.6
        kf = track(doc, P, [(0, "opacity:0"), (a, "opacity:0"), (a + .01, "opacity:1"), (b, "opacity:1"), (b + .01, "opacity:0")])
        out += f'<g opacity="{1 if k == 0 else 0}" style="{anim(kf, P)}">{doc.text("mono-bold", v, mx + 36, wy + 41, 14, INK)}</g>'
    # request log
    ly = wy + 70
    out += doc.text("mono", "REQUESTS", mx, ly, 10, DIM, tracking=1)
    reqs = [("GET", "/classes", "200"), ("POST", "/bookings", "201"), ("POST", "/payments", "201")]
    for k, (m, path, code) in enumerate(reqs):
        ry = ly + 12 + k * 26
        t0 = 0.6 + k * 1.6
        kf = track(doc, P, [(0, f"fill:{PANEL_2}"), (t0, f"fill:{PANEL_2}"), (t0 + .1, f"fill:{mix(BG, color, .3)}"),
                            (t0 + .9, f"fill:{PANEL_2}")])
        out += (f'<rect x="{mx}" y="{ry}" width="{ww}" height="20" rx="5" fill="{PANEL_2}" style="{anim(kf, P)}"/>'
                + doc.text("mono-bold", m, mx + 10, ry + 14, 11, color)
                + doc.text("mono", path, mx + 56, ry + 14, 11, INK_2)
                + doc.text("mono", code, mx + ww - 10, ry + 14, 11, GREEN, anchor="end"))
    # payment toast
    tw, th = 196, 40
    tx, ty = x + w - tw - 14, y + 14
    kf = track(doc, P, [(0, "opacity:0;transform:translateY(-10px)"), (2.6, "opacity:0;transform:translateY(-10px)"),
                        (3.0, "opacity:1;transform:translateY(0px)"), (6.2, "opacity:1;transform:translateY(0px)"),
                        (6.6, "opacity:0;transform:translateY(-10px)")])
    toast = (f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="4" fill="{PANEL_2}" stroke="{GREEN}" stroke-opacity=".6"/>'
             f'<circle cx="{tx + 20}" cy="{ty + 20}" r="8" fill="{GREEN}"/>'
             f'<path d="M{tx + 16} {ty + 20} l3 3 l6 -6" fill="none" stroke="{BG}" stroke-width="2" stroke-linecap="round"/>'
             + doc.text("mono-bold", "razorpay · paid", tx + 36, ty + 25, 12, INK))
    out += f'<g opacity="0" style="{anim(kf, P)}">{toast}</g>'
    return out


def experience() -> str:
    W, H = 1000, 372
    doc = Doc(W, H, "Experience: Full Stack Developer Intern at Language Metrics, August 2026 to present.")
    doc.add(card(doc))
    x0, maxw = 44, 510
    s, w = chip(doc, x0, 30, "FULL-STACK", ROLE["web"], size=11, h=22, pad=9)
    doc.add(s)
    doc.add(f'<circle cx="{x0 + w + 16}" cy="41" r="4" fill="{GREEN}"/>')
    doc.add(doc.text("mono", "AUG 2026 — NOW · REMOTE", x0 + w + 28, 45, 11.5, MUTED, tracking=1))
    doc.add(doc.text("display", "Language Metrics", x0 - 2, 100, 50, INK, max_width=maxw, where="exp title"))
    doc.add(doc.text("body", "Full Stack Developer Intern · languagemetrics.in", x0, 128, 16.5, INK_2, max_width=maxw))
    points = [
        "Shipped the Teacher and Admin portals: JWT auth, class booking, Razorpay checkout and a coin wallet.",
        "Built React front ends over Node/Express REST APIs on PostgreSQL + Supabase, managed with Prisma.",
        "Defined and versioned the API contracts, and integrated a live video-class provider.",
        "Tuned Prisma schemas and queries on high-traffic endpoints to cut response times.",
    ]
    yy = 168
    for p in points:
        lines = wrap("body", p, 15, maxw - 18)
        doc.add(f'<rect x="{x0}" y="{yy - 9}" width="6" height="6" rx="1" fill="{ROLE["web"]}"/>')
        for i, ln in enumerate(lines):
            doc.add(doc.text("body", ln, x0 + 18, yy + i * 20, 15, INK_2))
        yy += len(lines) * 20 + 8
    assert yy <= H - 10, f"experience text overflows ({yy})"
    doc.add(portal(doc, 590, 20, 390, H - 40))
    return doc.render()


# ------------------------------------------------------------------- journey --
MILESTONES = [
    ("2024", "KIET Ghaziabad", "Started B.Tech CSE · CGPA 8.57", INK_2),
    ("2025", "VeriVolunte", "First project shipped end to end", ROLE["web"]),
    ("2026", "Drishti · SIH", "Offline agent workbench for a refinery", ROLE["ai"]),
    ("JUN 2026", "Quackathon", "Track winner, as team lead", ROLE["3d"]),
    ("AUG 2026", "Language Metrics", "Full-stack intern, production code", ROLE["web"]),
    ("NEXT", "Your team", "SDE · full-stack · AI internship", GREEN),
]


def journey() -> str:
    W, H = 1000, 220
    doc = Doc(W, H, "Journey: KIET 2024, VeriVolunte 2025, Drishti at Smart India Hackathon 2026, Quackathon track "
                    "win June 2026, Language Metrics August 2026, next: an internship on your team.")
    doc.add(card(doc))
    n = len(MILESTONES)
    colw = (W - 60) / n
    ly = 92
    x_first, x_last = 30 + colw / 2, 30 + colw * (n - 0.5)
    doc.add(f'<line x1="{num(x_first)}" y1="{ly}" x2="{num(x_last)}" y2="{ly}" stroke="{LINE}" stroke-width="2"/>')
    length = x_last - x_first
    draw = track(doc, 1, [(0, f"stroke-dashoffset:{num(length)}"), (1, "stroke-dashoffset:0")])
    doc.add(f'<line x1="{num(x_first)}" y1="{ly}" x2="{num(x_last)}" y2="{ly}" stroke="{INK_2}" stroke-width="2" '
            f'stroke-dasharray="{num(length)}" style="{anim(draw, 2.4, 0.2, loop=False, ease="cubic-bezier(.3,.7,.3,1)")}"/>')
    doc.style(".pop{transform-box:fill-box;transform-origin:50% 50%}")
    for k, (yr, title, sub, col) in enumerate(MILESTONES):
        cx = 30 + colw * (k + 0.5)
        pop = track(doc, 1, [(0, "transform:scale(0)"), (0.7, "transform:scale(1.3)"), (1, "transform:scale(1)")])
        doc.add(doc.text("mono-bold", yr, cx, 62, 12.5, col, anchor="middle", tracking=1))
        doc.add(f'<circle cx="{num(cx)}" cy="{ly}" r="7" fill="{BG}" stroke="{col}" stroke-width="2.5" class="pop" '
                f'style="{anim(pop, 0.45, 0.25 + k * 0.38, loop=False)}"/>')
        if k == n - 1:
            ring = track(doc, 2.2, [(0, "opacity:.8;transform:scale(1)"), (1.8, "opacity:0;transform:scale(2.6)"), (2.2, "opacity:0;transform:scale(2.6)")])
            doc.add(f'<circle cx="{num(cx)}" cy="{ly}" r="7" fill="none" stroke="{col}" class="pop" opacity="0" style="{anim(ring, 2.2, 2.6)}"/>')
        doc.add(doc.text("body-bold", title, cx, 134, 15, INK, anchor="middle", max_width=colw - 12, where="journey title"))
        for i, ln in enumerate(wrap("body", sub, 13, colw - 16)):
            doc.add(doc.text("body", ln, cx, 158 + i * 18, 13, MUTED, anchor="middle"))
    return doc.render()


# --------------------------------------------------------------------- proof --
TILES = [("1400+", "LEETCODE", "contest rating · Java DSA", ROLE["3d"]),
         ("8.57", "CGPA", "B.Tech CSE · KIET", ROLE["web"]),
         ("1st", "QUACKATHON 2026", "track win, as team lead", ROLE["ai"]),
         ("2", "LIVE PRODUCTS", "platform + admin portal", GREEN)]


def proof() -> str:
    W, H = 1000, 150
    doc = Doc(W, H, "LeetCode 1400+ rating, 8.57 CGPA, Quackathon 2026 track winner, 2 live products in production.")
    gap = 20
    tw = (W - gap * 3) / 4
    for k, (big, lab, sub, col) in enumerate(TILES):
        x = k * (tw + gap)
        doc.add(card(doc, x, 0, tw, H))
        doc.add(f'<rect x="{num(x + 24)}" y="28" width="22" height="3" rx="1.5" fill="{col}"/>')
        doc.add(doc.text("display", big, x + 22, 86, 44, INK, max_width=tw - 44, where="proof big"))
        doc.add(doc.text("mono-bold", lab, x + 24, 112, 11, col, tracking=1.2, max_width=tw - 44, where="proof lab"))
        doc.add(doc.text("body", sub, x + 24, 131, 13.5, MUTED, max_width=tw - 44, where="proof sub"))
    return doc.render()


def build_all():
    return [("experience.svg", experience())]
