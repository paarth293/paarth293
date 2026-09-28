# Profile design source

Every image on the profile README is generated from this folder. Nothing is
drawn by hand and nothing loads from a third-party service.

```
.github/profile/
├── config.py          ← all links (portfolio, repos, LinkedIn, email). Edit this first.
├── build_all.py       ← regenerates README.md + every image in /assets
├── sync_activity.py   ← redraws assets/skyline.svg from your real contribution calendar
├── design/            ← type engine (fonts → vector outlines), palette, 3D projection, motion
├── sections/          ← one module per part of the page (hero, roles, work, experience, …)
└── fonts/             ← Bricolage Grotesque, Instrument Sans, Geist Mono (SIL OFL, licences included)
```

## Change something

1. Edit the words in the relevant `sections/*.py` file (project cards are in
   `sections/work.py`, the three role panels in `sections/roles.py`,
   experience/timeline/stats in `sections/experience.py`), or a link in `config.py`.
2. Push. The **Rebuild profile images** workflow regenerates everything and commits it.

To build locally instead: `pip install fonttools` then `python .github/profile/build_all.py`.

## Guard rails

The build fails loudly instead of shipping a broken image:

* every text run is measured with the real font metrics; if it doesn't fit its
  box, the build stops and names the text (`LayoutError`);
* a character missing from the fonts stops the build instead of rendering a blank box;
* the skyline sync never replaces a good image with an empty one — on any error
  it keeps the previous file and exits cleanly.

## Motion

All animation is CSS inside the SVGs, so it plays on GitHub (no JavaScript).
Each animated element's static attributes form a complete still frame, and every
file honours `prefers-reduced-motion`: with motion off you get that still frame.
