# Deadlock Damage Lab (step 4 web page prototype)

Static site, no server. Open `index.html` through any static host (or `python3 -m http.server` in this folder).

- **Damage test** (main feature): pick a hero, net worth, aim (ranked percentile or your own accuracy and headshot
  numbers) and items; set the target as a training dummy (HP, bullet/spirit/melee resist) or an enemy hero with
  items; run. Shows damage and DPS at 5/15/30 s, 15 s damage per 1,000 item souls, damage by source, a damage
  timeline and kill time. "Keep for comparison" pins up to 5 runs on the same chart and table.
- **Real match** (`match.js`): paste a match ID (or open `#match/<id>`). The page calls the Deadlock API from the
  browser (it allows any origin): the bulk `/v1/matches/metadata` endpoint first, then `/v1/matches/{id}/metadata`,
  which can fall back to Steam for matches the API hasn't stored. Pick a player, a target and a moment in the match;
  each side gets the items it held then and its net worth, the player keeps their hero accuracy from that match, and
  the sim runs their build against the target's build next to the damage-search builds they could afford, plus
  one-for-one swaps of an owned item for an equal or cheaper item from those builds.
- **Best damage builds** (`damage/out`), **Duel builds** (`search/out`, shows whichever rank brackets exist) and
  **Tank builds** (`survival/out`). Every build has a Test button that loads it into the damage test.

## How the damage test runs in the browser
The real Python sim runs live in the browser with Pyodide (CPython compiled to WebAssembly), inside a Web Worker.
Pyodide core 0.26.4 (Python 3.12) is self-hosted in `vendor/pyodide`, so no CDN is needed. `py/sim.zip` holds
`sim/deadsim`, the game data it reads, `damage/dummy.py` and `bridge.py` (the page's JSON in, `damage_test()` out).
First load downloads about 14 MB and takes about 4 s; each run after that takes about 0.2 s. Live runs match the
precomputed numbers exactly (Haze popular 27k: 1,126 / 2,445 / 3,934 both ways).

## Rebuild
`python3 build.py` after the sim or any search output changes (copies JSON into `data/`, rebuilds `py/sim.zip`,
writes `artifact.html`). Add `--pyodide <dir>` with an extracted `pyodide-core-0.26.4.tar.bz2` from the Pyodide
GitHub release to refresh `vendor/pyodide`.
