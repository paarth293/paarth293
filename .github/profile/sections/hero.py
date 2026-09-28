"""Hero: "paarth-1" -- me, presented like an AI model you can try.

Right: an LLM chat. A recruiter's question is typed, three chunks of my
résumé are retrieved with similarity scores, and a cited answer streams in
word by word. Three questions cycle (22.5 s loop). Answers are written from
my résumé and repos; the panel is labelled as an illustration.

Static frame (reduced motion / no animation): question 1, fully answered.
"""
from __future__ import annotations

from design.doc import Doc, num
from design.kit import (BG, PANEL, PANEL_2, LINE, INK, INK_2, MUTED, DIM, GREEN, ACCENT, ROLE, card, chip, mix)
from design.motion import track, anim
from design.type import measure, wrap

W, H = 1000, 540
SEG = 7.5
T = SEG * 3
D = 0.6

QA = [
    {"q": "what does paarth build?",
     "chunks": [("résumé § projects", .94), ("résumé § skills", .90), ("résumé § experience", .83)],
     "a": "LLM products, end to end: RAG pipelines, multi-agent systems and the Next.js + Node apps that stream their answers.",
     "cite": ["[1] projects", "[2] skills"]},
    {"q": "is he production-ready?",
     "chunks": [("résumé § experience", .96), ("résumé § summary", .88), ("résumé § skills", .84)],
     "a": "Yes. He ships a live SaaS at Language Metrics: React, Node/Express, PostgreSQL + Prisma, JWT auth and Razorpay payments.",
     "cite": ["[1] experience"]},
    {"q": "why hire him for AI?",
     "chunks": [("résumé § projects", .95), ("résumé § certifications", .89), ("résumé § achievements", .85)],
     "a": "His agents are built not to hallucinate: consensus voting, grounding checks, offline RAG and agent memory. Oracle-certified in agentic AI.",
     "cite": ["[1] projects", "[2] certifications"]},
]


def times(k: int) -> dict[str, float]:
    s = k * SEG
    return {"s": s, "type": s + 0.3, "retr": s + 1.8, "gen": s + 3.0, "words": s + 3.2,
            "cite": s + 5.2, "off": s + 7.0, "end": s + 7.35}


def show(doc, a, b, fade=0.25):
    return track(doc, T, [(0, "opacity:0"), (a, "opacity:0"), (a + fade, "opacity:1"), (b, "opacity:1"), (b + .3, "opacity:0")])


def build() -> str:
    doc = Doc(W, H, "Paarth Gupta — AI and full-stack engineer: LLMs, RAG, agentic AI, Next.js and Node.js. "
                    "An animated chat answers recruiter questions using retrieval over his résumé.")
    doc.style(".fc{transform-box:fill-box;transform-origin:50% 50%}.sx{transform-box:fill-box;transform-origin:0 50%}")
    doc.add(card(doc))
    doc.add(f'<clipPath id="hc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="8"/></clipPath><g clip-path="url(#hc)">')
    _left(doc)
    _chat(doc)
    doc.add("</g>")
    return doc.render()


# --------------------------------------------------------------------- left --
def _left(doc: Doc) -> None:
    x0, maxw = 48, 392
    blink = track(doc, 2.4, [(0, "opacity:1"), (1.6, "opacity:1"), (1.7, "opacity:.25"), (2.4, "opacity:.25")])
    doc.add(f'<rect x="{x0}" y="54" width="8" height="8" fill="{GREEN}" style="{anim(blink, 2.4)}"/>')
    doc.add(doc.text("mono-bold", "OPEN TO AI & FULL-STACK INTERNSHIPS", x0 + 18, 62, 11.5, GREEN, tracking=1.1,
                     max_width=maxw - 18, where="hero open"))
    doc.add(doc.text("mono-bold", "paarth-1", x0, 96, 11.5, ACCENT, tracking=0.6))
    doc.add(doc.text("mono", "  trained at KIET · deployed in production", x0 + measure("mono-bold", "paarth-1", 11.5, 0.6), 96,
                     11.5, MUTED, max_width=maxw - 70, where="hero tag"))

    doc.add(doc.text("display", "Paarth Gupta", x0 - 4, 180, 80, INK, max_width=maxw + 20, where="hero name"))
    # role line: serif italic, only "AI" carries the accent
    x = x0
    for part, col in (("AI", ACCENT), (" & full-stack engineer", INK)):
        doc.add(doc.text("serif-italic", part, x, 226, 36, col))
        x += measure("serif-italic", part, 36)
    assert x - x0 <= maxw, "role line overflow"

    for i, ln in enumerate(["I build LLM products end to end: RAG pipelines,",
                            "agents, and the Next.js + Node apps that",
                            "stream their answers to real users."]):
        doc.add(doc.text("body", ln, x0, 270 + i * 24, 16.5, INK_2, max_width=maxw, where="hero sub"))

    # domain tags
    chips = [("LLMs", "ai"), ("RAG", "ai"), ("AGENTIC AI", "agent"), ("NEXT.JS", "web"), ("NODE.JS", "web")]
    cx, cy = x0, 350
    for label, k in chips:
        s, w = chip(doc, cx, cy, label, ROLE[k], size=12, h=26, pad=10)
        doc.add(s)
        cx += w + 8
    assert cx - 8 <= x0 + maxw, "chips overflow"

    # quick stats, set in the serif
    stats = [("8.57", "CGPA"), ("1400+", "LEETCODE"), ("1st", "QUACKATHON '26")]
    sx = x0
    for big, lab in stats:
        doc.add(doc.text("display", big, sx, 438, 38, INK))
        doc.add(doc.text("mono", lab, sx, 458, 10, DIM, tracking=1.2))
        sx += max(measure("display", big, 38), measure("mono", lab, 10, 1.2)) + 34
    assert sx - 34 <= x0 + maxw, "stats overflow"
    doc.add(f'<line x1="{x0}" y1="486" x2="{x0 + maxw}" y2="486" stroke="{LINE}"/>')
    doc.add(doc.text("mono", "Full-stack intern @ Language Metrics · KIET CSE '28", x0, 512, 11.5, MUTED,
                     max_width=maxw, where="hero foot"))


# --------------------------------------------------------------------- chat --
def _chat(doc: Doc) -> None:
    px, py, pw, ph = 470, 30, 500, 480
    doc.add(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="{PANEL}" stroke="{LINE}"/>')
    doc.add(f'<line x1="{px}" y1="{py + 44}" x2="{px + pw}" y2="{py + 44}" stroke="{LINE}"/>')
    doc.add(doc.text("mono", "paarth-1 — rag over résumé.md", px + 20, py + 26.5, 12, INK_2))
    blink = track(doc, 1.6, [(0, "opacity:1"), (0.8, "opacity:.3"), (1.6, "opacity:1")])
    doc.add(f'<rect x="{px + pw - 98}" y="{py + 18}" width="7" height="7" fill="{GREEN}" style="{anim(blink, 1.6)}"/>')
    doc.add(doc.text("mono", "streaming", px + pw - 84, py + 26.5, 11.5, GREEN))

    ix, iw = px + 24, pw - 48
    qsize = 14
    qmax = max(measure("mono", qa["q"], qsize) for qa in QA)
    bw = qmax + 40

    for k, qa in enumerate(QA):
        t = times(k)
        static = 1 if k == 0 else 0
        seg_group = []
        # --- question bubble (width grows with the typed text) ---
        qw = measure("mono", qa["q"], qsize)
        bx = px + pw - 24 - (qw + 32)
        by = py + 64
        bub = show(doc, t["type"] - .2, t["off"])
        seg_group.append(f'<g opacity="{static}" style="{anim(bub, T, D)}">'
                         f'<rect x="{num(bx)}" y="{by}" width="{num(qw + 32)}" height="38" rx="4" fill="{PANEL_2}" '
                         f'stroke="{INK_2}" stroke-opacity=".35"/></g>')
        runs, _ = doc.glyph_runs("mono", qa["q"], bx + 16, by + 24, qsize)
        for i, (ch, mk, gx, adv) in enumerate(runs):
            if not mk:
                continue
            ti = t["type"] + i * 0.05
            kf = track(doc, T, [(0, "opacity:0"), (ti, "opacity:0"), (ti + .01, "opacity:1"), (t["off"], "opacity:1"), (t["off"] + .3, "opacity:0")])
            seg_group.append(f'<g fill="{INK}" opacity="{static}" style="{anim(kf, T, D)}">{mk}</g>')
        seg_group.append(f'<g opacity="{static}" style="{anim(bub, T, D)}">'
                         + doc.text("mono", "you", bx - 10, by + 24, 11, DIM, anchor="end") + "</g>")

        # --- retrieval ---
        ry = py + 132
        lab = doc.text("mono-bold", "01 RETRIEVE", ix, ry, 11, ROLE["agent"], tracking=1.2) + \
            doc.text("mono", "top-k = 3 · cosine", ix + 104, ry, 11, DIM)
        seg_group.append(f'<g opacity="{static}" style="{anim(show(doc, t["retr"], t["off"]), T, D)}">{lab}</g>')
        for j, (name, score) in enumerate(qa["chunks"]):
            cy = ry + 14 + j * 34
            a = t["retr"] + 0.25 + j * 0.3
            row = (f'<rect x="{ix}" y="{cy}" width="{iw}" height="28" rx="4" fill="{PANEL_2}" stroke="{LINE}"/>'
                   f'<rect x="{ix + 12}" y="{cy + 8}" width="9" height="12" rx="2" fill="none" stroke="{MUTED}" stroke-width="1.2"/>'
                   + doc.text("mono", name, ix + 30, cy + 18.5, 12, INK_2)
                   + doc.text("mono-bold", f"{score:.2f}", ix + iw - 12, cy + 18.5, 12, INK, anchor="end"))
            barw = 90
            bx2 = ix + iw - 58 - barw
            row += f'<rect x="{bx2}" y="{cy + 12}" width="{barw}" height="4" rx="2" fill="{LINE}"/>'
            fill = track(doc, T, [(0, "transform:scaleX(0)"), (a, "transform:scaleX(0)"), (a + .5, "transform:scaleX(1)"),
                                  (t["off"], "transform:scaleX(1)")])
            row += (f'<rect x="{bx2}" y="{cy + 12}" width="{num(barw * score)}" height="4" rx="2" fill="{ROLE["agent"]}" class="sx" '
                    f'style="{anim(fill, T, D)}"/>')
            seg_group.append(f'<g opacity="{static}" style="{anim(show(doc, a, t["off"]), T, D)}">{row}</g>')

        # --- generation ---
        gy = ry + 138
        lab = doc.text("mono-bold", "02 GENERATE", ix, gy, 11, ROLE["ai"], tracking=1.2) + \
            doc.text("mono", "streaming · grounded · cited", ix + 104, gy, 11, DIM)
        seg_group.append(f'<g opacity="{static}" style="{anim(show(doc, t["gen"], t["off"]), T, D)}">{lab}</g>')
        lines = wrap("body", qa["a"], 16.5, iw)
        assert len(lines) <= 4, f"answer too long: {qa['q']}"
        wi = 0
        for li, ln in enumerate(lines):
            yy = gy + 30 + li * 26
            xx = ix
            for word in ln.split(" "):
                a = t["words"] + wi * 0.065
                kf = track(doc, T, [(0, "opacity:0"), (a, "opacity:0"), (a + .12, "opacity:1"), (t["off"], "opacity:1"), (t["off"] + .3, "opacity:0")])
                seg_group.append(f'<g opacity="{static}" style="{anim(kf, T, D)}">{doc.text("body", word, xx, yy, 16.5, INK)}</g>')
                xx += measure("body", word + " ", 16.5)
                wi += 1
        # caret that rides at the end of the stream
        # citations
        cx = ix
        cy2 = gy + 30 + len(lines) * 26 + 6
        cites = ""
        for c in qa["cite"]:
            s, w = chip(doc, cx, cy2, c, ROLE["agent"], fkey="mono", size=11, h=22, pad=9)
            cites += s
            cx += w + 8
        seg_group.append(f'<g opacity="{static}" style="{anim(show(doc, t["cite"], t["off"]), T, D)}">{cites}</g>')
        doc.add("".join(seg_group))

    doc.add(doc.text("mono", "illustrative demo · answers written from my résumé and repos", px + pw / 2, py + ph - 16,
                     10.5, DIM, anchor="middle"))
