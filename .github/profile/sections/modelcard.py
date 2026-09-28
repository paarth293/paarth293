"""Model card: me, documented the way an AI model is released.

Every line is from the résumé. The limitations are real (Rust and Solidity
are listed on the résumé as working knowledge).
"""
from __future__ import annotations

from design.doc import Doc, num
from design.kit import BG, PANEL, PANEL_2, LINE, INK, INK_2, MUTED, DIM, GREEN, ROLE, card, chip, mix
from design.motion import track, anim
from design.type import measure, wrap

W = 1000


def section(doc, x, y, label, color):
    doc.add(doc.text("mono-bold", label, x, y, 11, color, tracking=1.4))
    doc.add(f'<line x1="{x}" y1="{y + 10}" x2="{x + 24}" y2="{y + 10}" stroke="{color}" stroke-width="2"/>')


def build_all():
    H = 640
    doc = Doc(W, H, "Model card for Paarth Gupta. Intended use: AI engineer or full-stack intern. Training: B.Tech CSE at KIET "
                    "(CGPA 8.57), full-stack intern at Language Metrics, hackathons. Capabilities: LLM apps, RAG, agentic AI, "
                    "Next.js, Node.js, FastAPI, PostgreSQL. Evaluation: LeetCode 1400+, Quackathon 2026 track winner, Oracle "
                    "Agentic AI certified. Limitations: Rust and Solidity at working knowledge.")
    doc.add(card(doc))
    # header strip
    doc.add(f'<path d="M1 9 a8 8 0 0 1 8 -8 h{W - 18} a8 8 0 0 1 8 8 v67 h-{W - 2} z" fill="{PANEL}"/>')
    doc.add(f'<line x1="1" y1="76" x2="{W - 1}" y2="76" stroke="{LINE}"/>')
    doc.add(doc.text("mono-bold", "MODEL CARD", 36, 34, 11, DIM, tracking=2))
    doc.add(doc.text("display", "paarth-1", 36, 64, 34, INK))
    x = 36 + measure("display", "paarth-1", 34) + 16
    for label, col in (("AI ENGINEER", ROLE["ai"]), ("FULL-STACK", ROLE["web"]), ("OPEN TO INTERNSHIPS", GREEN)):
        s, w = chip(doc, x, 42, label, col, size=10.5, h=22, pad=9)
        doc.add(s)
        x += w + 8
    doc.add(doc.text("mono", "v2028 · checkpoint: B.Tech CSE, year 3", W - 36, 58, 11.5, MUTED, anchor="end"))

    L, R = 36, 520          # two columns
    CW = 444

    # --- Intended use
    y = 116
    section(doc, L, y, "INTENDED USE", ROLE["agent"])
    for i, ln in enumerate(wrap("body", "Building LLM products end to end: retrieval, agents and the full-stack app "
                                        "around them. Best deployed as an AI or full-stack engineering intern.", 16, CW)):
        doc.add(doc.text("body", ln, L, y + 36 + i * 23, 16, INK))

    # --- Training data
    y = 236
    section(doc, L, y, "TRAINING DATA", ROLE["web"])
    rows = [("2024 →", "B.Tech CSE, KIET Ghaziabad · CGPA 8.57 / 10"),
            ("AUG 2026 →", "Full-stack intern, Language Metrics (live SaaS)"),
            ("2026", "Smart India Hackathon · Quackathon (track win)"),
            ("ALWAYS", "Six public AI & full-stack repos, two deployed")]
    for i, (k, v) in enumerate(rows):
        yy = y + 38 + i * 30
        doc.add(doc.text("mono", k, L, yy, 11.5, DIM))
        doc.add(doc.text("body", v, L + 96, yy, 15, INK_2, max_width=CW - 96, where="training"))

    # --- Capabilities (chips)
    y = 408
    section(doc, L, y, "CAPABILITIES", ROLE["ai"])
    caps = [("LLM apps", "ai"), ("RAG", "ai"), ("agentic AI", "agent"), ("LangGraph", "agent"), ("prompt eng.", "ai"),
            ("Next.js", "web"), ("Node.js", "web"), ("TypeScript", "web"), ("FastAPI", "agent"), ("PostgreSQL", "web"),
            ("Prisma", "web"), ("vector DBs", "agent"), ("Docker", "web"), ("DSA · Java", "web")]
    cx, cy = L, y + 24
    for label, k in caps:
        w = measure("mono", label, 12.5) + 22
        if cx + w > L + CW:
            cx, cy = L, cy + 36
        doc.add(f'<rect x="{num(cx)}" y="{cy}" width="{num(w)}" height="28" rx="3" fill="none" '
                f'stroke="{ROLE[k]}" stroke-opacity=".4"/>' + doc.text("mono", label, cx + 11, cy + 18.5, 12.5, INK))
        cx += w + 8
    assert cy + 28 <= H - 24, "capabilities overflow"

    # --- Evaluation (right column)
    y = 116
    section(doc, R, y, "EVALUATION", GREEN)
    evals = [("LeetCode rating", "1400+", "Weekly Contest 512 · Java"),
             ("CGPA", "8.57", "out of 10 · KIET CSE"),
             ("Quackathon 2026", "1st", "track winner · team lead"),
             ("Oracle University", "cert.", "Agentic AI Foundations Associate"),
             ("Cisco", "cert.", "Networking Essentials")]
    doc.style(".bar{transform-box:fill-box;transform-origin:0 50%}")
    for i, (name, score, note) in enumerate(evals):
        yy = y + 30 + i * 58
        doc.add(f'<rect x="{R}" y="{yy}" width="{CW}" height="48" rx="4" fill="{PANEL}" stroke="{LINE}"/>')
        doc.add(doc.text("body-bold", name, R + 16, yy + 21, 15, INK))
        doc.add(doc.text("body", note, R + 16, yy + 39, 12.5, MUTED, max_width=CW - 120, where="eval note"))
        doc.add(doc.text("display", score, R + CW - 16, yy + 35, 32, INK, anchor="end"))
        # scanning highlight, one row after another
        kf = track(doc, 7.5, [(0, "opacity:0"), (i * 1.5, "opacity:0"), (i * 1.5 + .2, "opacity:1"), (i * 1.5 + 1.3, "opacity:1"),
                               (i * 1.5 + 1.5, "opacity:0")])
        doc.add(f'<rect x="{R}" y="{yy}" width="{CW}" height="48" rx="4" fill="none" stroke="{GREEN}" stroke-opacity=".7" '
                f'opacity="0" style="{anim(kf, 7.5)}"/>')

    # --- Limitations
    y = 462
    section(doc, R, y, "LIMITATIONS", ROLE["3d"])
    lims = ["Rust and Solidity: working knowledge, not production yet.",
            "Graduates 2028. Available now for internships."]
    for i, ln in enumerate(lims):
        yy = y + 38 + i * 26
        doc.add(doc.text("mono", "–", R, yy, 13, DIM))
        doc.add(doc.text("body", ln, R + 18, yy, 14.5, INK_2, max_width=CW - 18, where="limitation"))

    # --- inference footer
    doc.add(f'<line x1="36" y1="{H - 52}" x2="{W - 36}" y2="{H - 52}" stroke="{LINE}"/>')
    doc.add(doc.text("mono", "INFERENCE", 36, H - 24, 11, DIM, tracking=1.4))
    doc.add(doc.text("mono", "i.m.paarthgupta@gmail.com · replies within a day · IST (UTC+5:30) · Ghaziabad, IN",
                     130, H - 24, 12, INK_2, max_width=W - 166, where="inference"))
    return [("modelcard.svg", doc.render())]
