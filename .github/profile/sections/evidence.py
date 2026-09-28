"""Evidence: six repositories as one compact strip (the page is about me;
the projects are the proof). Descriptions come from each repo's README/code."""
from __future__ import annotations

from design.doc import Doc, num
from design.kit import BG, PANEL, LINE, INK, INK_2, MUTED, DIM, GREEN, ROLE, card, mix
from design.motion import track, anim
from design.type import wrap, measure

REPOS = [
    ("MandateOS", "Cryptographic control plane for AI-agent payments on Razorpay: Ed25519-signed mandates, 8-gate checks.",
     [("NEXT.JS 16", "web"), ("TYPESCRIPT", "web"), ("AGENTS", "agent")], True),
    ("ClauseGuard", "Multi-agent contract analysis that can't invent a clause: 3-run consensus plus grounding checks.",
     [("NEXT.JS", "web"), ("FASTAPI", "agent"), ("LLM", "ai")], True),
    ("Knowledge-Agent", "RAG over your documents: Qdrant retrieval, a LangGraph agent on Groq, evaluated with RAGAS.",
     [("RAG", "ai"), ("LANGGRAPH", "agent"), ("FASTAPI", "agent")], False),
    ("TrueBrain", "Long-term memory for coding agents: SQLite with sqlite-vec + FTS5 hybrid search.",
     [("MEMORY", "ai"), ("PYTHON", "agent")], False),
    ("PromptForge", "Plain English to a validated agent tool schema in 14 stages, with a SHA-256 audit chain.",
     [("NEXT.JS", "web"), ("FASTAPI", "agent")], False),
    ("Drishti", "Air-gapped agentic workbench for a refinery, local models via Ollama. SIH 2026 team build.",
     [("OFFLINE RAG", "ai"), ("OLLAMA", "ai")], False),
]


def build_all():
    W, gap, cols = 1000, 16, 3
    cw, ch = (W - gap * (cols - 1)) / cols, 150
    rows = (len(REPOS) + cols - 1) // cols
    H = int(rows * ch + (rows - 1) * gap)
    doc = Doc(W, H, "Six repositories: MandateOS and ClauseGuard (both live), Knowledge-Agent, TrueBrain, PromptForge, Drishti.")
    doc.style(".fc{transform-box:fill-box;transform-origin:50% 50%}")
    for i, (name, desc, tags, live) in enumerate(REPOS):
        x = (i % cols) * (cw + gap)
        y = (i // cols) * (ch + gap)
        doc.add(card(doc, x, y, cw, ch, r=14))
        doc.add(doc.text("display", name, x + 20, y + 38, 21, INK, max_width=cw - 110, where="evidence name"))
        if live:
            doc.add(f'<rect x="{num(x + cw - 74)}" y="{y + 20}" width="56" height="22" rx="11" fill="{mix(BG, GREEN, .16)}" '
                    f'stroke="{GREEN}" stroke-opacity=".5"/>')
            pulse = track(doc, 1.8, [(0, "opacity:1"), (0.9, "opacity:.3"), (1.8, "opacity:1")])
            doc.add(f'<circle cx="{num(x + cw - 62)}" cy="{y + 31}" r="3.5" fill="{GREEN}" style="{anim(pulse, 1.8)}"/>')
            doc.add(doc.text("mono-bold", "LIVE", x + cw - 54, y + 35, 10.5, GREEN, tracking=1))
        else:
            doc.add(doc.text("mono", "↗", x + cw - 22, y + 36, 14, DIM, anchor="end"))
        lines = wrap("body", desc, 13.5, cw - 40)
        assert len(lines) <= 3, name
        for j, ln in enumerate(lines):
            doc.add(doc.text("body", ln, x + 20, y + 64 + j * 19, 13.5, INK_2))
        tx = x + 20
        for label, k in tags:
            w = measure("mono-bold", label, 10, 0.8) + 16
            doc.add(f'<rect x="{num(tx)}" y="{y + ch - 34}" width="{num(w)}" height="20" rx="10" fill="{mix(BG, ROLE[k], .14)}"/>'
                    + doc.text("mono-bold", label, tx + 8, y + ch - 20.5, 10, ROLE[k], tracking=0.8))
            tx += w + 6
    return [("evidence.svg", doc.render())]
