"""Rebuild every image in ../../assets from source. Run: python .github/profile/build_all.py"""
from __future__ import annotations
import importlib, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "assets"))


def write(name: str, svg: str) -> None:
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  {name:32s} {len(svg.encode())/1024:6.1f} KB")


def main(only: list[str]) -> None:
    from sections import hero
    jobs = {"hero": lambda: write("hero.svg", hero.build())}
    for mod in ("layers", "modelcard", "embed", "experience", "evidence", "chrome", "skyline", "readme"):
        try:
            m = importlib.import_module(f"sections.{mod}")
        except ModuleNotFoundError:
            continue
        jobs[mod] = (lambda m=m: [write(n, s) for n, s in m.build_all()])
    for name, job in jobs.items():
        if only and name not in only:
            continue
        # the skyline is owned by sync_activity.py once real data exists;
        # a routine rebuild must not swap it back to the sample
        if name == "skyline" and "skyline" not in only and os.path.exists(os.path.join(OUT, "skyline.svg")):
            print("  skyline.svg                      (kept — synced by sync_activity.py)")
            continue
        t = time.time()
        job()
    print("done")


if __name__ == "__main__":
    main(sys.argv[1:])
