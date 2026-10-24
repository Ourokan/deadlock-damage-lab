# Deadlock Damage Lab (step 4 web page prototype)

Static site, no server. Open `index.html` through any static host (or `python3 -m http.server` in this folder).

- **Damage test** (main feature): pick a hero, net worth, aim (ranked percentile or your own accuracy and headshot
  numbers) and items; set the target as a training dummy (HP, bullet/spirit/melee resist) or an enemy hero with
  items; run. Shows damage and DPS at 5/15/30 s, 15 s damage per 1,000 item souls, damage by source, a damage
  timeline and kill time. "Keep for comparison" pins up to 5 runs on the same chart and table. The whole setup
  is kept in the address bar after each run (and "Copy link" copies it), so a link reopens and reruns the same test.
  "My own numbers" takes accuracy, headshot rate and fight distance, or loads them from a player's last 10 matches
  (`aim.js`: Steam link, ID or name -> Deadlock API match metadata, hero-only "Enemy Hero Accuracy" stats, the same
  numbers as `deadsim.accuracy.player_skill`). The page shows where those numbers sit among ranked players of the
  hero and remembers them in the browser.
- **Build maker** (`maker.js`, `bridge.maker`): build from nothing against up to five enemies. Each enemy holds what
  Phantom+ players of that hero hold most at about your net worth (`data/maker.json` from `search/out/usage.json`,
  filled most-held first up to the souls players that rich hold in items, within the tier caps). Every change runs you
  against each enemy for 15 s, both fighting back and refilling instead of dying (first lethal moment = time to kill;
  otherwise extrapolated from HP really lost). Hovering an item previews it. Suggestions check the ~36 items players of
  the hero buy most at that net worth plus utility items (or every item) in separate workers and rank them by damage
  change + survival change + utility points (`maker_utility.json`: hand-made tags; anti-heal scaled by enemy healing,
  cleanse by enemy crowd control), per 1,000 souls or overall. State lives in `#maker/...` links.
- **Real match** (`match.js`): paste a match ID (or open `#match/<id>`). The page calls the Deadlock API from the
  browser (it allows any origin): the bulk `/v1/matches/metadata` endpoint first, then `/v1/matches/{id}/metadata`,
  which can fall back to Steam for matches the API hasn't stored. Pick a player, a target and a moment in the match;
  each side gets the items it held then and its net worth, the player keeps their hero accuracy from that match, and
  the sim runs their build against the target's build next to the damage-search builds they could afford, plus
  one-for-one swaps of an owned item for an equal or cheaper item from those builds.
- **Team fight**: up to three heroes a side (each starts with its popular real build) fight in the live sim
  (`bridge.team`, `team.js`). Shows damage, damage taken, heals and shields given to teammates, kills.
- **Best damage builds** (`damage/out`, with the item buy order and the ability upgrade order for the best builds), **Duel builds** (`search/out`, shows whichever rank brackets exist) and
  **Tank builds** (`survival/out`). Every build has a Test button that loads it into the damage test.

## Phones
Under 640 px the tabs sit in a 3x3 grid, long intros fold to three lines, and every table with a text column turns
into stacked cards (`stackTables()` in `app.js` labels each number with its column). Touch screens get 36 px+ controls
and 16 px inputs (no iOS zoom on focus). On touch screens the Build maker's suggestions run on the page's sim worker
instead of a second Pyodide instance, which would cost another ~15 MB download and enough memory to make mobile
browsers reload the tab.

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
