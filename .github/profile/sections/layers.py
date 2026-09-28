"""One engineer, every layer of an AI product.

Six layers from the Next.js interface down to the models. A request travels
down the spine, the answer streams back up as tokens. Every "shipped in"
entry is taken from the repo's own code or dependencies.
"""
from __future__ import annotations

from design.doc import Doc, num
from design.kit import BG, PANEL, PANEL_2, LINE, INK, INK_2, MUTED, DIM, ROLE, card, mix
from design.motion import track, anim

LAYERS = [
    ("INTERFACE", "Next.js · React · TypeScript · Tailwind · SSE streaming", "MandateOS · ClauseGuard · PromptForge"),
    ("API", "Node.js · Express · FastAPI · REST · JWT · RBAC", "Language Metrics · Knowledge-Agent"),
    ("AGENTS", "LangGraph · LangChain · tool calls · consensus voting · LLM-as-judge", "ClauseGuard · Knowledge-Agent · Drishti"),
    ("RETRIEVAL", "RAG · embeddings · Qdrant · ChromaDB · sqlite-vec + FTS5 hybrid", "Knowledge-Agent · TrueBrain · Drishti"),
    ("DATA", "PostgreSQL · Prisma · Drizzle · Supabase · Neon · SQLite", "Language Metrics · MandateOS"),
    ("MODELS", "Groq · Ollama (local, offline) · prompt engineering · RAGAS eval", "Knowledge-Agent · Drishti"),
]


def colors():
    w, a, r = ROLE["web"], ROLE["agent"], ROLE["ai"]
    return [w, mix(w, a, .5), a, mix(a, r, .35), mix(a, r, .7), r]


def build_all():
    W = 1000
    top, rh, gap = 92, 70, 12
    H = top + len(LAYERS) * (rh + gap) + 34
    P = 6.0
    doc = Doc(W, H, "Every layer of an AI product: interface (Next.js, React, TypeScript), API (Node.js, Express, FastAPI), "
                    "agents (LangGraph, LangChain), retrieval (RAG, Qdrant, ChromaDB, sqlite-vec), data (PostgreSQL, Prisma, "
                    "Drizzle, Supabase) and models (Groq, Ollama) — each shipped in a real project.")
    doc.add(card(doc))
    doc.add(doc.text("display", "One engineer, every layer of an AI product", 40, 52, 26, INK, max_width=660))
    doc.add(doc.text("mono", "↓ request", W - 190, 50, 11.5, ROLE["web"]))
    doc.add(doc.text("mono", "↑ tokens", W - 100, 50, 11.5, ROLE["ai"]))
    cols = colors()
    spine_x = 60
    y_first = top + rh / 2
    y_last = top + (len(LAYERS) - 1) * (rh + gap) + rh / 2
    doc.add(f'<line x1="{spine_x}" y1="{num(y_first)}" x2="{spine_x}" y2="{num(y_last)}" stroke="{LINE}" stroke-width="2"/>')

    down_t = [(0.2 + i * 0.42) for i in range(len(LAYERS))]
    up_t = [(3.0 + (len(LAYERS) - 1 - i) * 0.42) for i in range(len(LAYERS))]
    for i, (name, tools, shipped) in enumerate(LAYERS):
        y = top + i * (rh + gap)
        c = cols[i]
        glow = track(doc, P, [(0, f"stroke:{LINE}"), (down_t[i], f"stroke:{LINE}"), (down_t[i] + .1, f"stroke:{ROLE['web']}"),
                              (down_t[i] + .5, f"stroke:{LINE}"), (up_t[i], f"stroke:{LINE}"), (up_t[i] + .1, f"stroke:{ROLE['ai']}"),
                              (up_t[i] + .5, f"stroke:{LINE}")])
        doc.add(f'<rect x="84" y="{y}" width="{W - 124}" height="{rh}" rx="12" fill="{PANEL}" stroke="{LINE}" '
                f'stroke-width="1.5" style="{anim(glow, P)}"/>')
        doc.add(f'<rect x="84" y="{y + 14}" width="4" height="{rh - 28}" rx="2" fill="{c}"/>')
        doc.add(f'<circle cx="{spine_x}" cy="{num(y + rh / 2)}" r="7" fill="{BG}" stroke="{c}" stroke-width="2.5"/>')
        doc.add(doc.text("mono-bold", f"{i + 1:02d}  {name}", 106, y + 28, 11.5, c, tracking=1.3))
        doc.add(doc.text("mono", tools, 106, y + 52, 12.5, INK, max_width=522, where=f"layer tools {name}"))
        doc.add(f'<line x1="642" y1="{y + 16}" x2="642" y2="{y + rh - 16}" stroke="{LINE}"/>')
        doc.add(doc.text("mono", "SHIPPED IN", 658, y + 28, 10, DIM, tracking=1.2))
        doc.add(doc.text("body", shipped, 658, y + 51, 14, INK_2, max_width=W - 56 - 658, where=f"layer shipped {name}"))

    # request down, tokens up
    pts_down = [(0, f"transform:translate({spine_x}px,{num(y_first)}px);opacity:0"),
                (0.15, f"transform:translate({spine_x}px,{num(y_first)}px);opacity:1")]
    for i in range(len(LAYERS)):
        pts_down.append((down_t[i] + .05, f"transform:translate({spine_x}px,{num(top + i * (rh + gap) + rh / 2)}px);opacity:1"))
    pts_down.append((down_t[-1] + .3, f"transform:translate({spine_x}px,{num(y_last)}px);opacity:0"))
    doc.add(f'<circle r="5" fill="{ROLE["web"]}" opacity="0" style="{anim(track(doc, P, pts_down), P)}"/>')
    pts_up = [(0, f"transform:translate({spine_x}px,{num(y_last)}px);opacity:0"),
              (2.9, f"transform:translate({spine_x}px,{num(y_last)}px);opacity:0")]
    for i in reversed(range(len(LAYERS))):
        pts_up.append((up_t[i] + .05, f"transform:translate({spine_x}px,{num(top + i * (rh + gap) + rh / 2)}px);opacity:1"))
    pts_up.append((up_t[0] + .3, f"transform:translate({spine_x}px,{num(y_first)}px);opacity:0"))
    # three trailing "tokens"
    for k in range(3):
        shifted = [(min(P, t + k * .12), d) for t, d in pts_up]
        doc.add(f'<rect x="-4" y="-4" width="8" height="8" rx="2" fill="{ROLE["ai"]}" opacity="0" '
                f'style="{anim(track(doc, P, shifted), P)}"/>')
    return [("layers.svg", doc.render())]
