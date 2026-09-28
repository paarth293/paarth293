"""Contribution skyline: the last 52 weeks of GitHub activity as a 3D city.

`render(weeks, sample=...)` is used both by the local build (with sample
data, clearly labelled) and by sync_activity.py in the daily Action (with the
real calendar from the GitHub GraphQL API).

weeks: [[{"date": "YYYY-MM-DD", "count": int}, ...7 days], ...]
"""
from __future__ import annotations

import datetime as dt
import random

from design.doc import Doc, num
from design.kit import BG, PANEL, LINE, INK, INK_2, MUTED, DIM, GREEN, ROLE, card, mix, pts
from design.motion import track, anim

W, H = 1000, 404
RAMP = ["#27306A", ROLE["web"], "#9A6BFF", ROLE["3d"], ROLE["ai"]]


def ramp(t: float) -> str:
    t = max(0.0, min(1.0, t))
    seg = t * (len(RAMP) - 1)
    i = min(int(seg), len(RAMP) - 2)
    return mix(RAMP[i], RAMP[i + 1], seg - i)


def stats(weeks) -> dict:
    days = [d for w in weeks for d in w]
    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"]) if days else {"count": 0, "date": ""}
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["count"] > 0 else 0
        longest = max(longest, cur)
    current = 0
    for d in reversed(days):
        if d["count"] > 0:
            current += 1
        elif current or d is not days[-1]:
            break
    active = sum(1 for d in days if d["count"] > 0)
    return {"total": total, "best": best["count"], "best_date": best["date"], "longest": longest,
            "current": current, "active": active}


def render(weeks, *, sample: bool = False) -> str:
    st = stats(weeks)
    doc = Doc(W, H, f"GitHub activity, last 52 weeks: {st['total']} contributions, longest streak {st['longest']} days, "
                    f"best day {st['best']} contributions. Drawn as an isometric city." + (" (sample data)" if sample else ""))
    doc.add(card(doc))
    # header stats
    doc.add(doc.text("display", "The last 52 weeks", 40, 64, 28, INK))
    items = [(f"{st['total']:,}", "CONTRIBUTIONS"), (f"{st['longest']}d", "LONGEST STREAK"),
             (f"{st['best']}", "BEST DAY"), (f"{st['active']}", "ACTIVE DAYS")]
    x = 40
    for v, lab in items:
        doc.add(doc.text("display", v, x, 112, 26, INK))
        doc.add(doc.text("mono", lab, x, 132, 10.5, DIM, tracking=1.2))
        x += 150
    if sample:
        doc.add(doc.text("mono", "SAMPLE DATA · REPLACED ON FIRST SYNC", W - 40, 60, 11, ROLE["3d"], anchor="end", tracking=1))
    else:
        today = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y").upper()
        doc.add(doc.text("mono", f"SYNCED {today}", W - 40, 60, 11, MUTED, anchor="end", tracking=1))
    # legend
    lx = W - 40 - 5 * 18 - 70
    doc.add(doc.text("mono", "less", lx - 8, 88, 10.5, DIM, anchor="end"))
    for i in range(5):
        doc.add(f'<rect x="{lx + i * 18}" y="78" width="14" height="14" rx="3" fill="{ramp(i / 4)}"/>')
    doc.add(doc.text("mono", "more", lx + 5 * 18 + 4, 88, 10.5, DIM))

    # oblique projection: x = week (right, slightly down), y = weekday (back, up-right), z = up
    n = len(weeks)
    ax, ay_ = (1.0, 0.085), (0.58, -0.30)   # unit week / weekday axes
    maxc = max([d["count"] for w in weeks for d in w] + [1])
    zmax = 104.0
    region = (40, 150, 920, 236)            # everything, incl. tallest bar + labels, lives here
    corners = [(-0.3, -0.3), (n + 0.3, -0.3), (n + 0.3, 7.3), (-0.3, 7.3)]
    ux = [a * ax[0] + b * ay_[0] for a, b in corners]
    uy = [a * ax[1] + b * ay_[1] for a, b in corners]
    s = region[2] / (max(ux) - min(ux))
    s = min(s, (region[3] - zmax - 14) / (max(uy) - min(uy)))
    X, Y = (s * ax[0], s * ax[1]), (s * ay_[0], s * ay_[1])
    ox = region[0] - s * min(ux) + (region[2] - s * (max(ux) - min(ux))) / 2
    oy = region[1] + zmax - s * min(uy)

    def P(x, y, z=0.0):
        return ox + x * X[0] + y * Y[0], oy + x * X[1] + y * Y[1] - z

    # ground plate
    plate = [P(-0.3, -0.3), P(n + 0.3, -0.3), P(n + 0.3, 7.3), P(-0.3, 7.3)]
    doc.add(f'<polygon points="{pts(plate)}" fill="#101218" stroke="{LINE}"/>')
    edge = [P(-0.3, -0.3), P(n + 0.3, -0.3), P(n + 0.3, -0.3, -6), P(-0.3, -0.3, -6)]
    doc.add(f'<polygon points="{pts(edge)}" fill="#171A22"/>')

    fw = 0.72
    cells = []
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week):
            cells.append((wi, di, day["count"]))
    # painter: back rows first, then left to right
    cells.sort(key=lambda c: (-c[1], c[0]))
    groups: dict[int, list[str]] = {}
    for wi, di, c in cells:
        x0, y0 = wi + (1 - fw) / 2, di + (1 - fw) / 2
        if c == 0:
            poly = [P(x0, y0), P(x0 + fw, y0), P(x0 + fw, y0 + fw), P(x0, y0 + fw)]
            groups.setdefault(wi, []).append(f'<polygon points="{pts(poly)}" fill="#1A1D27"/>')
            continue
        t = (c / maxc) ** 0.6
        z = 5 + t * zmax
        col = ramp(t)
        top = [P(x0, y0, z), P(x0 + fw, y0, z), P(x0 + fw, y0 + fw, z), P(x0, y0 + fw, z)]
        front = [P(x0, y0), P(x0 + fw, y0), P(x0 + fw, y0, z), P(x0, y0, z)]
        right = [P(x0 + fw, y0), P(x0 + fw, y0 + fw), P(x0 + fw, y0 + fw, z), P(x0 + fw, y0, z)]
        groups.setdefault(wi, []).append(
            f'<polygon points="{pts(front)}" fill="{mix(BG, col, .55)}"/>'
            f'<polygon points="{pts(right)}" fill="{mix(BG, col, .35)}"/>'
            f'<polygon points="{pts(top)}" fill="{col}"/>')
    # draw in painter order, but wrap each week's pieces so they rise together
    rise = track(doc, 1, [(0, "opacity:0;transform:translateY(18px)"), (1, "opacity:1;transform:translateY(0px)")])
    # Weeks overlap in depth, so painter order must be global; animate per piece with a week-based delay.
    body = []
    for wi, di, c in cells:
        piece = groups[wi].pop(0)
        body.append(f'<g style="{anim(rise, 0.7, round(0.1 + wi * 0.022, 3), loop=False, ease="cubic-bezier(.2,.8,.2,1)")}">{piece}</g>')
    doc.add("".join(body))

    # month labels along the front edge
    seen = set()
    for wi, week in enumerate(weeks):
        d = dt.date.fromisoformat(week[0]["date"])
        key = (d.year, d.month)
        if d.day <= 7 and key not in seen:
            seen.add(key)
            lx_, ly_ = P(wi + 0.1, -0.9)
            doc.add(doc.text("mono", d.strftime("%b").upper(), lx_, ly_ + 12, 10.5, DIM))
    # today marker
    tx, ty = P(n - 0.5, 7.6)
    pulse = track(doc, 2.0, [(0, "opacity:.9;transform:scale(1)"), (1.6, "opacity:0;transform:scale(2.8)"), (2.0, "opacity:0;transform:scale(2.8)")])
    doc.style(".pl{transform-box:fill-box;transform-origin:50% 50%}")
    doc.add(f'<circle cx="{num(tx)}" cy="{num(ty)}" r="4" fill="{GREEN}"/>'
            f'<circle cx="{num(tx)}" cy="{num(ty)}" r="4" fill="none" stroke="{GREEN}" class="pl" opacity="0" style="{anim(pulse, 2.0)}"/>')
    doc.add(doc.text("mono", "today", tx - 10, ty + 4, 10.5, GREEN, anchor="end"))
    return doc.render()


def sample_weeks(seed: int = 5, end: dt.date | None = None):
    """Plausible-looking placeholder calendar, used only until the first sync."""
    rng = random.Random(seed)
    end = end or dt.date(2026, 9, 26)
    start = end - dt.timedelta(days=end.weekday() + 1) - dt.timedelta(weeks=52)
    weeks = []
    d = start
    for w in range(53):
        week = []
        for k in range(7):
            ramp_up = 1.0 + 2.2 * (w / 52) ** 2
            burst = 3.2 if 20 <= w <= 24 else (2.4 if w >= 45 else 1.0)
            base = rng.random() < (0.35 + 0.4 * (w / 52))
            c = int(base * rng.expovariate(1 / (2.2 * ramp_up * burst)))
            if k in (0, 6) and rng.random() < .5:
                c //= 2
            week.append({"date": d.isoformat(), "count": c})
            d += dt.timedelta(days=1)
        weeks.append(week)
    return weeks


def build_all():
    return [("skyline.svg", render(sample_weeks(), sample=True))]
