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

## Item buy order
`scripts/buy_order.py`, output `out/order/<id>.json` (copied by `scripts/export.py`, shown under the Best damage
builds tab). For each objective it takes the best 50k build and works out the order to buy it in: from an empty
build, buy whichever piece (a target item or one of its components) adds the most damage per soul at the net worth
you'd have when you can afford it, until the build is complete. Upgrades credit the component you hold; nothing is
sold. Each step records the net worth it's bought at (lowest net worth whose item budget covers the spend, rounded
up to 500). At each milestone (10k to 50k) it records what you hold and its damage against the best build the
search found for that exact net worth, which may use items you'd later sell. Median across heroes (15 s): 100% of
the best build at 10k, 93% at 18k, 92% at 27k, 94% at 37k. Gaps come from expensive core items bought as one lump
(Refresher, Focus Lens) and early items the 50k build drops. ~1 min for all heroes on 4 cores; it reads
`work/jobs` from `dummy_search.py` (or `out/heroes` when those aren't there) and runs in the patch reruns after the
damage search.

## Overall search (damage before dying, counterplay on)
`scripts/overall_search.py`, output `out/overall/` (`scripts/export_overall.py`). Score = damage the build deals
before it dies against each of the 41 typical real builds at that net worth: the enemy fights back with x2 damage
and never dies, 30 s cap. Survivability, CC on the enemy and the enemy's own counters (resists, Dispel Magic) all
count. Counterplay is on (`hero_default_skill(counterplay=True)`): targets leave Alchemical Fire after 2 s
(1.5 s from Ascendant), item damage the sim over-predicts versus real matches is scaled down
(`sim/data/item_landing.json`), and actives with cooldowns over 60 s are ready only in their share of fights.
Why and results: `/mnt/project-files/analysis/build_scoring_review.md`. ~3 h on 4 cores (resumes from
`work/jobs_overall`).
