# Tank survival search

Which item builds keep a tank alive longest against real enemy builds, while keeping its core items and its damage.
Uses the combat model (`/mnt/project-files/sim`), real builds and opponent pools from the duel search
(`/mnt/project-files/search/work`) and the dummy damage test (`/mnt/project-files/damage`). Python stdlib only.

## Survival test (`survival.py`)

```python
import sys; sys.path[:0] = ["/mnt/project-files/sim", "/mnt/project-files/survival"]
from survival import survive
survive("Abrams", ["Extra Health", "Bullet Resilience"], souls=27000,
        enemy="Haze", enemy_items=["Mercurial Magnum", "Toxic Bullets"], focus=2)
# -> time_alive, survived, max_hp, final_hp, damage_taken (+ by source), healing, damage_dealt
```
Both sides fight normally (gun, abilities on cooldown, actives, melee) at ranked median aim with real ability
landing and melee rates, at the mean of both heroes' real fight distances. The enemy refills instead of dying, so
the tested hero keeps shooting back (lifesteal and on-hit heals count) until it dies or `max_time` (60 s) passes.
`focus` multiplies the enemy's damage: 2 stands in for being focused by two enemies of that build.

## Search (`scripts/survival_search.py`)

- **Tanks**: the 10 heroes whose real players put the largest share of item souls into vitality items (18k-37k):
  Silver, Abrams, Rat King, Victor, Venator, Bebop, Billy, Mo & Krill, Celeste, Mina. `--heroes` for others.
- **Enemies**: the 41 typical real builds at the same net worth (one per hero, weighted by how often the hero
  reaches it), from `search/work/snapshots_<budget>.json`.
- **Score**: weighted mean seconds alive at focus 2, plus 5 x HP fraction left when alive at 60 s. At focus 1,
  Abrams' popular 27k build outlives 77% of enemies to the cap, so builds could not be told apart.
  Focus 1 and 3 are reported for every top build too.
- **Core items**: items in the popular build that at least 50% of real players of the hero own at that budget.
  Every build keeps them (or an item built from them).
- **Damage rule**: dummy damage by 15 s (same dummy as the damage search) at least (1 - margin) x the popular
  build's. Margins 0%, 10% and 25%, one search each.
- **Moves**: from the popular build, value every candidate item added and every non-core item removed on the 16
  most played enemies, then try add, 1-for-1, 2-for-1 and 1-for-2 swaps that pass the damage rule on all 41.
  Up to 6 rounds. Same budget rules as the other searches (item share of net worth, max 12 items, expensive item caps).

`python3 scripts/survival_search.py --workers 4 && python3 scripts/export.py` (resumes from `work/jobs`).

## Outputs (`out/`)
`index.json` (per hero x budget x margin: popular vs best build, time alive, damage change), `heroes/<id>.json`
(top 10 builds per margin with time alive / share surviving 60 s / damage taken / healing at focus 1, 2 and 3,
per-enemy time alive, seconds lost when each non-core item is removed), `report.md` (tables with item names).

## Limits
- No movement: escape and mobility items (Warp Stone, Majestic Leap, Phantom Strike...) and breaking line of
  sight are worth nothing here, so the search drops them. Real tanks also get healed by teammates and fountains.
- "Focused by two" is the enemy's damage doubled: one enemy's debuffs, procs and cooldowns, twice the damage.
- One enemy at a time; the enemy also starts with every cooldown ready.
- Same model gaps as the other searches (`sim/validation/README.md`, `search/README.md`).

## Results (run 2026-10-14, after the sim's per-pellet on-hit fix)
At a 10% damage allowance the best build lives 10.5 s longer than the popular real build on average (focus 2),
from +0.3 s (Mina 10k) to +22 s. Most added: Enchanter's Emblem (20 of 50), Spirit Resilience (16), Metal Skin (15),
Lifestrike and Restorative Shot (8). Most dropped: Cultist Sacrifice (12), Spirit Shielding (10), Swift Striker (9),
Slowing Hex and Warp Stone (8). Full tables: `out/report.md`. The pre-fix run is kept in `work/jobs_before_pellet_fix`.
