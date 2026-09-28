"""My skills, embedded: a 2-D "embedding space" of the stack.

Three clusters (LLM/RAG/agents, full-stack web, foundations) with a bridge
between the first two. Three queries cycle; each drops a query vector,
draws edges to its nearest neighbours and lists them. The last query --
"AI + full-stack intern" -- lands between the two clusters, which is the
point. Layout is hand-placed and labelled as an illustration.
"""
from __future__ import annotations

import math

from design.doc import Doc, num
from design.kit import BG, PANEL, PANEL_2, LINE, INK, INK_2, MUTED, DIM, GREEN, ROLE, card, mix
from design.motion import track, anim
from design.type import measure

W, H = 1000, 520
SEG, NQ = 6.0, 3
T = SEG * NQ

A, G, B, F = ROLE["ai"], ROLE["agent"], ROLE["web"], ROLE["3d"]
POINTS = {
    # LLM · RAG · agents
    "LLMs": (100, 150, A), "RAG": (185, 132, A), "LangChain": (262, 156, G), "LangGraph": (104, 204, G),
    "Ollama": (196, 190, A), "Groq": (292, 206, A), "embeddings": (92, 258, A), "Qdrant": (190, 244, A),
    "ChromaDB": (262, 270, A), "sqlite-vec": (120, 306, A), "prompt eng.": (214, 322, A),
    # bridge
    "Python": (350, 236, G), "FastAPI": (384, 282, G), "SSE": (344, 330, G), "Docker": (420, 332, G),
    # full-stack web
    "Next.js": (478, 160, B), "React": (566, 150, B), "TypeScript": (606, 196, B), "Node.js": (492, 214, B),
    "Express": (574, 244, B), "REST": (648, 262, B), "JWT": (486, 272, B), "Tailwind": (560, 294, B),
    "Razorpay": (618, 322, B), "PostgreSQL": (490, 340, B), "Prisma": (580, 366, B), "Supabase": (628, 402, B),
    # foundations
    "DSA": (84, 388, F), "Java": (150, 402, F), "C++": (218, 388, F), "OS": (282, 404, F),
    "DBMS": (96, 446, F), "Networks": (178, 450, F), "System design": (272, 452, F),
}
CLUSTERS = [("LLM · RAG · AGENTS", 190, 226, 150, 118, A), ("FULL-STACK WEB", 560, 272, 130, 150, B),
            ("FOUNDATIONS", 184, 424, 150, 50, F)]
QUERIES = [
    ("build a RAG chatbot", (236, 214), ["RAG", "embeddings", "Qdrant", "LangChain", "Ollama", "FastAPI"], A),
    ("ship a full-stack SaaS", (540, 258), ["Next.js", "Node.js", "PostgreSQL", "Prisma", "JWT", "Razorpay"], B),
    ("AI + full-stack intern", (410, 222), ["LLMs", "RAG", "LangGraph", "FastAPI", "Next.js", "Node.js"], G),
]
STATIC_Q = 2


def build_all():
    doc = Doc(W, H, "My skills as an embedding space: an LLM/RAG/agents cluster (LLMs, RAG, LangChain, LangGraph, Ollama, "
                    "Qdrant, ChromaDB), a full-stack cluster (Next.js, React, TypeScript, Node.js, Express, PostgreSQL, "
                    "Prisma) joined by Python, FastAPI and SSE, and CS foundations. The query 'AI + full-stack intern' "
                    "lands between the two clusters.")
    doc.style(".fc{transform-box:fill-box;transform-origin:50% 50%}")
    doc.add(card(doc))
    doc.add(doc.text("display", "My skills, embedded", 36, 52, 26, INK))
    doc.add(doc.text("mono", "illustrative 2-D projection · k-NN to a query vector", 36, 74, 11.5, DIM))
    # plot area
    px, py, pw, ph = 36, 96, 668, 392
    doc.add(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{PANEL}" stroke="{LINE}"/>')
    grid = "".join(f'<line x1="{px + i * pw / 8:.1f}" y1="{py}" x2="{px + i * pw / 8:.1f}" y2="{py + ph}"/>' for i in range(1, 8))
    grid += "".join(f'<line x1="{px}" y1="{py + i * ph / 6:.1f}" x2="{px + pw}" y2="{py + i * ph / 6:.1f}"/>' for i in range(1, 6))
    doc.add(f'<g stroke="{GRID_C}" stroke-width="1">{grid}</g>')
    ox, oy = px - 36 + 6, py - 96 + 8      # point coords are authored relative to (36, 96)
    P = lambda name: (POINTS[name][0] + ox, POINTS[name][1] + oy)

    for label, cx, cy, rx, ry, c in CLUSTERS:
        gid = doc.uid("cl")
        doc.add_def(gid, f'<radialGradient id="{gid}"><stop offset="0" stop-color="{c}" stop-opacity=".16"/>'
                         f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
        doc.add(f'<ellipse cx="{cx + ox}" cy="{cy + oy}" rx="{rx}" ry="{ry}" fill="url(#{gid})"/>')
    for label, cx, cy, rx, ry, c in CLUSTERS:
        lx = cx + ox - measure("mono-bold", label, 10.5, 1.2) / 2
        ly = cy + oy - ry - 4 if label != "FOUNDATIONS" else cy + oy + ry - 2
        doc.add(doc.text("mono-bold", label, lx, ly, 10.5, c, tracking=1.2))

    # points
    for name, (x, y, c) in POINTS.items():
        X, Y = P(name)
        hits = [k for k, q in enumerate(QUERIES) if name in q[2]]
        style = ""
        static_r = 6 if STATIC_Q in hits else 4
        if hits:
            pts = [(0, "transform:scale(1)")]
            for k in hits:
                s = k * SEG
                pts += [(s + .7, "transform:scale(1)"), (s + 1.0, "transform:scale(1.6)"), (s + 5.4, "transform:scale(1.6)"),
                        (s + 5.8, "transform:scale(1)")]
            style = f' class="fc" style="{anim(track(doc, T, pts), T)}"'
        doc.add(f'<circle cx="{X}" cy="{Y}" r="4" fill="{c}"{style}/>')
        doc.add(doc.text("mono", name, X + 9, Y + 4, 11.5, INK_2 if hits else MUTED))

    # queries
    rx0 = 724
    for k, (qtext, (qx, qy), nn, c) in enumerate(QUERIES):
        s = k * SEG
        static = 1 if k == STATIC_Q else 0
        Qx, Qy = qx + ox, qy + oy
        seg = []
        for j, name in enumerate(nn):
            X, Y = P(name)
            L = math.hypot(X - Qx, Y - Qy)
            kf = track(doc, T, [(0, f"stroke-dashoffset:{num(L)};opacity:1"), (s + .4 + j * .08, f"stroke-dashoffset:{num(L)};opacity:1"),
                                (s + .9 + j * .08, "stroke-dashoffset:0;opacity:1"), (s + 5.4, "stroke-dashoffset:0;opacity:1"),
                                (s + 5.8, "stroke-dashoffset:0;opacity:0")])
            seg.append(f'<line x1="{Qx}" y1="{Qy}" x2="{X}" y2="{Y}" stroke="{c}" stroke-width="1.5" stroke-dasharray="{num(L)}" '
                       f'stroke-dashoffset="{0 if static else num(L)}" opacity="{static}" style="{anim(kf, T)}"/>')
        star = (f'<circle cx="{Qx}" cy="{Qy}" r="16" fill="{c}" opacity=".18"/>'
                f'<path d="M{Qx} {Qy - 10} L{Qx + 3} {Qy - 3} L{Qx + 10} {Qy} L{Qx + 3} {Qy + 3} L{Qx} {Qy + 10} '
                f'L{Qx - 3} {Qy + 3} L{Qx - 10} {Qy} L{Qx - 3} {Qy - 3} Z" fill="{INK}"/>')
        pop = track(doc, T, [(0, "opacity:0;transform:scale(.2)"), (s + .1, "opacity:0;transform:scale(.2)"),
                             (s + .45, "opacity:1;transform:scale(1)"), (s + 5.4, "opacity:1;transform:scale(1)"),
                             (s + 5.8, "opacity:0;transform:scale(1)")])
        seg.append(f'<g class="fc" opacity="{static}" style="{anim(pop, T)}">{star}</g>')
        doc.add("".join(seg))

        # side panel for this query
        panel = doc.text("mono-bold", "QUERY", rx0, 116, 11, c, tracking=1.4)
        panel += (f'<rect x="{rx0}" y="128" width="{W - 36 - rx0}" height="40" rx="10" fill="{PANEL_2}" stroke="{c}" stroke-opacity=".5"/>'
                  + doc.text("mono", qtext, rx0 + 14, 153, 13, INK, max_width=W - 36 - rx0 - 28, where="embed query"))
        panel += doc.text("mono-bold", "NEAREST NEIGHBOURS", rx0, 206, 11, DIM, tracking=1.4)
        scored = sorted(((max(0.5, 0.97 - math.hypot(P(n)[0] - Qx, P(n)[1] - Qy) / 900), n) for n in nn), reverse=True)
        for j, (score, name) in enumerate(scored):
            yy = 222 + j * 34
            panel += (f'<rect x="{rx0}" y="{yy}" width="{W - 36 - rx0}" height="28" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
                      f'<circle cx="{rx0 + 14}" cy="{yy + 14}" r="4" fill="{POINTS[name][2]}"/>'
                      + doc.text("mono", name, rx0 + 26, yy + 18.5, 12, INK)
                      + doc.text("mono", f"{score:.2f}", W - 36 - 12, yy + 18.5, 12, INK_2, anchor="end"))
        if k == STATIC_Q:
            panel += doc.text("body-bold", "↳ lands between both clusters.", rx0, 452, 14, INK)
            panel += doc.text("body", "That's the role I'm after.", rx0, 474, 14, INK_2)
        show = track(doc, T, [(0, "opacity:0"), (s + .15, "opacity:0"), (s + .45, "opacity:1"), (s + 5.4, "opacity:1"), (s + 5.8, "opacity:0")])
        doc.add(f'<g opacity="{static}" style="{anim(show, T)}">{panel}</g>')
    return [("embed.svg", doc.render())]


GRID_C = "#191C24"
