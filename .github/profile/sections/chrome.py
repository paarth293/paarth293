"""Section headers, link buttons and the footer."""
from __future__ import annotations

import random

from design.doc import Doc, num
from design.kit import BG, PANEL, LINE, INK, INK_2, MUTED, DIM, GREEN, ROLE, card, mix
from design.motion import track, anim
from design.type import measure

HEADERS = [
    ("layers", "01", "Every layer", "LLM products, top to bottom", ["web", "agent", "ai"]),
    ("card", "02", "Model card", "me, documented like a model", ["agent"]),
    ("skills", "03", "Skill space", "where my skills cluster", ["ai", "web"]),
    ("prod", "04", "In production", "Language Metrics · Aug 2026 → now", ["web"]),
    ("evidence", "05", "Evidence", "six repos · two live", ["agent", "ai"]),
    ("activity", "06", "Activity", "synced daily from GitHub", ["ai"]),
    ("contact", "07", "Prompt me", "replies within a day, IST", ["green"]),
]


# GitHub light theme: headers sit on the page, not on a card, so they need their own ink
LIGHT = {"ink": "#1F2328", "muted": "#59636E", "line": "#D1D9E0",
         "web": "#2438E8", "3d": "#B87700", "ai": "#D1242F", "agent": "#8250DF", "green": "#1A7F37"}


def header(slug, n, title, desc, roles, theme="dark") -> str:
    W, H = 1000, 76
    doc = Doc(W, H, f"{n} — {title}")
    if theme == "dark":
        ink, muted, line = INK, MUTED, LINE
        cols = [GREEN if r == "green" else ROLE[r] for r in roles]
    else:
        ink, muted, line = LIGHT["ink"], LIGHT["muted"], LIGHT["line"]
        cols = [LIGHT[r] for r in roles]
    doc.add(doc.text("mono-bold", n, 0, 44, 14, cols[0], tracking=1))
    doc.add(doc.text("display", title, 40, 48, 32, ink))
    doc.add(doc.text("mono", desc, W, 44, 12.5, muted, anchor="end"))
    gid = f"hg{slug}"
    stops = "".join(f'<stop offset="{i / max(1, len(cols) - 1) * .5:.2f}" stop-color="{c}"/>' for i, c in enumerate(cols))
    doc.add_def(gid, f'<linearGradient id="{gid}" x1="0" x2="1">{stops}<stop offset="1" stop-color="{line}"/></linearGradient>')
    doc.add(f'<rect x="0" y="66" width="{W}" height="2" rx="1" fill="url(#{gid})"/>')
    return doc.render()


BUTTONS = [
    ("email", "Email me", True),
    ("linkedin", "LinkedIn", False),
    ("leetcode", "LeetCode", False),
    ("portfolio", "Portfolio", False),
]


def button(slug, label, primary) -> str:
    size, h = 16, 48
    tw = measure("body-bold", label, size)
    aw = measure("mono", "↗", 15)
    W = int(tw + aw + 20 + 44)
    doc = Doc(W, h, label)
    if primary:
        gid = "bgrad"
        doc.add_def(gid, f'<linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{ROLE["web"]}"/>'
                         f'<stop offset=".5" stop-color="{ROLE["3d"]}"/><stop offset="1" stop-color="{ROLE["ai"]}"/></linearGradient>')
        doc.add(f'<rect x="1" y="1" width="{W - 2}" height="{h - 2}" rx="{(h - 2) / 2}" fill="{INK}" stroke="url(#{gid})" stroke-width="2"/>')
        fg = BG
    else:
        doc.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="{(h - 1) / 2}" fill="{PANEL}" stroke="{LINE}"/>')
        fg = INK
    doc.add(doc.text("body-bold", label, 22, h / 2 + 5.6, size, fg))
    doc.add(doc.text("mono", "↗", 22 + tw + 10, h / 2 + 5.2, 15, fg if primary else MUTED))
    return doc.render()


PROMPTS = ["AI engineering intern: LLMs, RAG, agents", "full-stack intern: Next.js + Node", "let's build something that ships"]


def footer() -> str:
    W, H = 1000, 250
    P = 12.0
    doc = Doc(W, H, "Your turn — send a prompt: i.m.paarthgupta@gmail.com. Open to AI engineering and full-stack internships.")
    doc.add(card(doc))
    doc.add(f'<clipPath id="fclip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17"/></clipPath>')
    doc.add('<g clip-path="url(#fclip)">')
    doc.add_def("fg1", f'<radialGradient id="fg1" cx="50%" cy="120%" r="70%"><stop offset="0" stop-color="{ROLE["agent"]}" stop-opacity=".22"/>'
                       f'<stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>')
    doc.add(f'<rect width="{W}" height="{H}" fill="url(#fg1)"/></g>')
    doc.add(doc.text("mono", "END OF CONTEXT", W / 2, 50, 11, DIM, anchor="middle", tracking=2))
    doc.add(doc.text("display", "Your turn. Send a prompt.", W / 2, 96, 36, INK, anchor="middle"))
    bx, by, bw, bh = 150, 124, 700, 56
    doc.add_def("pb", f'<linearGradient id="pb" x1="0" x2="1"><stop offset="0" stop-color="{ROLE["ai"]}"/>'
                      f'<stop offset=".5" stop-color="{ROLE["agent"]}"/><stop offset="1" stop-color="{ROLE["web"]}"/></linearGradient>')
    doc.add(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16" fill="{PANEL}" stroke="url(#pb)" stroke-width="1.5"/>')
    # send button
    doc.add(f'<circle cx="{bx + bw - 30}" cy="{by + bh / 2}" r="17" fill="url(#pb)"/>'
            f'<path d="M{bx + bw - 37} {by + bh / 2} h13 m-5 -6 l6 6 l-6 6" fill="none" stroke="{BG}" stroke-width="2.4" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')
    tx, ty = bx + 24, by + bh / 2 + 5.5
    seg = P / len(PROMPTS)
    caret_pts = [(0, "transform:translateX(0px)")]
    for k, text in enumerate(PROMPTS):
        s0 = k * seg
        runs, width = doc.glyph_runs("mono", text, tx, ty, 15.5)
        assert width < bw - 90, "prompt too long"
        for i, (ch, mk, gx, adv) in enumerate(runs):
            if not mk:
                continue
            ti = s0 + 0.2 + i * 0.045
            kf = track(doc, P, [(0, "opacity:0"), (ti, "opacity:0"), (ti + .01, "opacity:1"), (s0 + seg - .4, "opacity:1"),
                                (s0 + seg - .39, "opacity:0")])
            doc.add(f'<g fill="{INK}" opacity="{1 if k == 0 else 0}" style="{anim(kf, P)}">{mk}</g>')
            caret_pts += [(ti, f"transform:translateX({num(gx - tx)}px)"), (ti + .01, f"transform:translateX({num(gx - tx + adv)}px)")]
        caret_pts += [(s0 + seg - .4, f"transform:translateX({num(width)}px)"), (s0 + seg - .39, "transform:translateX(0px)")]
    blink = track(doc, 1.0, [(0, "opacity:1"), (0.5, "opacity:1"), (0.51, "opacity:0"), (1.0, "opacity:0")])
    w0 = measure("mono", PROMPTS[0], 15.5)
    doc.add(f'<g transform="translate({num(w0)} 0)" style="{anim(track(doc, P, caret_pts), P)}">'
            f'<rect x="{tx + 2}" y="{ty - 16}" width="2.5" height="21" fill="{INK}" style="{anim(blink, 1.0)}"/></g>')
    doc.add(doc.text("mono", "i.m.paarthgupta@gmail.com  ·  linkedin.com/in/paarth-gupta  ·  IST (UTC+5:30)", W / 2, 216, 13, INK_2,
                     anchor="middle"))
    return doc.render()


def build_all():
    out = [(f"h-{slug}.svg", header(slug, n, t, d, r)) for slug, n, t, d, r in HEADERS]
    out += [(f"h-{slug}-light.svg", header(slug, n, t, d, r, "light")) for slug, n, t, d, r in HEADERS]
    out += [(f"btn-{slug}.svg", button(slug, label, p)) for slug, label, p in BUTTONS]
    out.append(("footer.svg", footer()))
    return out
