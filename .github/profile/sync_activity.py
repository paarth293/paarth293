"""Daily job: redraw assets/skyline.svg from the real GitHub contribution calendar.

Run by .github/workflows/activity.yml. Needs only `fonttools` and a token
that can read public profile data (the workflow's built-in GITHUB_TOKEN).

Safety: if anything goes wrong -- no token, API down, unexpected response,
an empty calendar -- the existing skyline.svg is left untouched and the job
exits successfully. A bad sync can never replace a good image with a blank one.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "assets", "skyline.svg"))

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""


def fetch(login: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": f"{login}-profile-sync"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def parse(payload: dict) -> list[list[dict]]:
    if payload.get("errors"):
        raise ValueError(f"GraphQL errors: {payload['errors']}")
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[{"date": d["date"], "count": int(d["contributionCount"])} for d in w["contributionDays"]]
             for w in cal["weeks"]]
    # GitHub's first/last week can be partial; pad to full weeks so the grid stays rectangular
    import datetime as dt
    if weeks and len(weeks[0]) < 7:
        first = dt.date.fromisoformat(weeks[0][0]["date"])
        pad = [{"date": (first - dt.timedelta(days=i)).isoformat(), "count": 0} for i in range(7 - len(weeks[0]), 0, -1)]
        weeks[0] = pad + weeks[0]
    if weeks and len(weeks[-1]) < 7:
        last = dt.date.fromisoformat(weeks[-1][-1]["date"])
        weeks[-1] += [{"date": (last + dt.timedelta(days=i)).isoformat(), "count": 0} for i in range(1, 8 - len(weeks[-1]))]
    if len(weeks) < 20:
        raise ValueError(f"calendar looks wrong: only {len(weeks)} weeks")
    return weeks[-53:]


def main() -> int:
    login = os.environ.get("PROFILE_LOGIN") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "paarth293"
    token = os.environ.get("GITHUB_TOKEN", "")
    fixture = os.environ.get("SKYLINE_FIXTURE")   # for local testing
    try:
        if fixture:
            with open(fixture, encoding="utf-8") as f:
                payload = json.load(f)
        else:
            if not token:
                raise RuntimeError("GITHUB_TOKEN is not set")
            payload = fetch(login, token)
        weeks = parse(payload)
        from sections.skyline import render
        svg = render(weeks, sample=False)
    except Exception as e:  # never break the profile over a failed sync
        print(f"::warning::skyline not updated, keeping the previous image ({type(e).__name__}: {e})")
        return 0
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    total = sum(d["count"] for w in weeks for d in w)
    print(f"skyline updated: {len(weeks)} weeks, {total} contributions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
