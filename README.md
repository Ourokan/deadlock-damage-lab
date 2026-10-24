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
| `counters/` | Counter items: real-match buy triggers and win edges, and their value in the sim per enemy hero. |
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

## Automatic reruns after a patch
`.github/workflows/patch-rerun.yml` runs every 6 hours (or by hand from the Actions tab, with "force" to rerun
anyway). `pipeline/check_patch.py` pulls the game data and changelog from the Deadlock API and compares them with
`data/patch.json`, the patch the committed results were built for:

- **New patch** (a newer changelog entry): waits until 3 full days of ranked games exist on it, then reruns on
  builds from the new patch only. It reruns again when the patch reaches 7 and 14 days of games, since the duel
  brackets read 7 or 14 days.
- **Hotfix** (gameplay numbers changed, no new changelog): reruns right away on the same patch's builds.

A rerun pulls player builds (`data/scripts/fetch_builds.py`, cached between runs; the SQL endpoint allows ~20
queries an hour, so 14 days take ~3 hours and a fetch that runs out of time continues on the next run), rebuilds
the opponent pools, then reruns the searches one rank tier at a time (`.github/workflows/rerun-tier.yml`), in the
order of `pipeline/tiers.json`: Phantom and up first, then Ascendant and up, Eternus and up, and all ranks. Phantom
and up is the standard (`build_pool.PRIMARY`): its tier runs the damage, item buy order, ability order, survival, duel, overall and full game path
searches and the counter-item values (`counters/scripts/sim_counters.py`); the later tiers run the duel, overall and full game path searches in their bracket. Each tier runs on 16 machines
(`pipeline/run_shard.py --tier`), checks it finished (`pipeline/check_results.py --tier`), commits the new `out/`
folders, game data and `data/patch.json` to `main` and redeploys the site before the next tier starts, so the
standard results show up first. Only tiers listed in `enabled` run (for now just Phantom and up); the others keep
their last published results, and the site says which run they come from. If a tier fails, nothing is committed for
it and the site keeps its previous results. The site footer shows the patch and when the results were built.

Not rerun automatically: the real-match half of the counter-item analysis (`counters/` buy triggers and win
edges, patch 09-29-2026), and the sim's fitted inputs in `sim/data/`
(aim percentiles, ability landing and melee rates), which keep their 09-29-2026 fit until refitted by hand. A new
hero's abilities fall back to a generic reading of their game data until they are coded in `sim/deadsim/heroes/`.

## Run the site locally
```
python3 web/build.py --pyodide <extracted pyodide-core-0.26.4 folder>
cd web && python3 -m http.server
```
