# Deadlock Damage Lab

A combat simulator for Deadlock item builds, and a web page for testing them. Pick a hero and items, set up a
target (a training dummy with your own HP and resists, or an enemy hero with items) and see how much damage the
build really does over 5, 15 and 30 seconds, at real ranked aim.

Live site: https://tylernodell.github.io/deadlock-damage-lab/ (deployed from `main` by `.github/workflows/pages.yml`).

## What's here

| Folder | What it is |
|---|---|
| `sim/` | `deadsim`, the combat model: guns, all hero abilities, ~90 item effects, fitted to real match data. `sim/validation/README.md` lists what it gets right and what it doesn't model yet. |
| `damage/` | Damage test against a configurable dummy (`dummy.py`) and the search for the most damaging builds per hero and net worth (`out/`). |
| `search/` | 1v1 duel build search against real player builds, per rank bracket (`out/`). |
| `survival/` | Tank builds that survive longest while keeping their damage (`out/`). |
| `counters/` | Counter-item analysis from real matches. |
| `data/` | Game data (`game/`) and the scripts that pull it and real player builds from the Deadlock API. |
| `web/` | The static site. The damage test runs the real Python sim in the browser with Pyodide. |

Everything is Python 3.12+ standard library only.

```python
import sys; sys.path[:0] = ["sim", "damage"]
from dummy import Dummy, damage_test
damage_test("Haze", ["Mercurial Magnum", "Toxic Bullets"], souls=27000,
            dummy=Dummy(hero="Abrams", items=["Bullet Resilience", "Extra Health"]))
```

## Data not in the repo
Real player builds (`data/builds/player_builds/`, ~1 GB) and the searches' `work/` folders are too big for git.
`data/scripts/fetch_builds.py` and `fetch_analytics.py` rebuild them from the Deadlock API.
`data/builds/aggregates/per_hero/` here keeps only the most played ability order per hero, which is all the sim reads.

## Run the site locally
```
python3 web/build.py --pyodide <extracted pyodide-core-0.26.4 folder>
cd web && python3 -m http.server
```
