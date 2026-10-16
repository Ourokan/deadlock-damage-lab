# Dummy damage search

The item builds that turn a souls budget into the most damage for each hero, against a training dummy. This is
separate from the duel search in `/mnt/project-files/search`: nothing shoots back and nobody wins.

## Custom damage test (for the web page)

`dummy.py` is the entry point step 4 exposes. The user sets up a dummy (HP, bullet/spirit/melee resist, or a hero
with items) and a build for any hero, then gets damage at chosen marks, DPS, damage by source, a 0.5 s timeline and
time to kill:

```python
import sys; sys.path[:0] = ["/mnt/project-files/sim", "/mnt/project-files/damage"]
from dummy import Dummy, damage_test
damage_test("Haze", ["Mercurial Magnum", "Toxic Bullets"], souls=27000,
            dummy=Dummy(hero="Abrams", items=["Bullet Resilience", "Extra Health"], immortal=False))
```
The precomputed search below uses the same function.

## Setup
- **Dummy**: never acts, has no resists or items, and refills to full instead of dying, so overkill counts. Its HP is
  the weighted median max HP of real typical builds at that budget, because some items scale off target HP
  (Tankbuster, Spirit Burn and similar).
- **Attacker**: the step 2 sim (`/mnt/project-files/sim`) at ranked median hero aim and headshot rate, with real
  ability landing and melee rates. It casts abilities on cooldown, uses actives, and stands at the hero's real
  median fight distance.
- **Budgets**: net worth 10k, 18k, 27k, 37k and 50k. Item spend is capped at the share real players hold in items
  (same as the duel search). Max 12 items, and no item together with its own component.
- **Objectives**, all from one 30 s run: damage by 5 s (`burst_5s`), by 15 s (`fight_15s`) and by 30 s
  (`sustained_30s`).
- **Search**: one per objective, starting from the most popular real build. Each round values every candidate item
  added and every owned item removed, tries 1-for-1, 2-for-1, 1-for-2 and add moves, and keeps the best. Up to
  8 rounds.

## Outputs (`out/`)
`index.json` (best vs popular per hero x budget x objective), `heroes/<id>.json` (top 10 builds per objective
with damage, DPS and damage by source, each best-build item's loss when removed, and every candidate item's damage
per 1000 souls when added to the popular build), `summary.csv`. Item names and costs are in
`/mnt/project-files/search/out/items.json`.

## Limits
- Every run starts with all cooldowns ready, so burst numbers include a full rotation, ultimates included.
- The dummy doesn't move. Skillshots use real landing rates, but the gun uses hero accuracy, not dummy accuracy.
- Effects that depend on the target's current HP restart each time the dummy refills.
- Same model gaps as the duel search (`search/README.md`): no movement, multi-target items do nothing, and some
  item effects aren't modeled (`effect_modeled` in items.json).

`python3 scripts/dummy_search.py --workers 4 && python3 scripts/export.py` (resumes from `work/jobs`).
