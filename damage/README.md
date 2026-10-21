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
  (same as the duel search). Max 12 items, no item together with its own component, and
  no more 3200+ / 6400+ soul items than 9 in 10 Phantom+ players hold at that net worth (search README, Rules).
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
(Refresher, Focus Lens) and early items the 50k build drops. ~1 min for all heroes on 4 cores. It reads
`work/jobs` from `dummy_search.py` (`--use-published` reads `out/heroes` instead, for local runs) and runs in the
patch reruns after the damage search.

## Ability upgrade order
`scripts/skill_order.py`, output `out/skill/<id>.json` (copied by `scripts/export.py`, shown under the Raw damage
builds tab next to the buy order). Everywhere else the sim levels abilities in the most played real order (Oracle and
up, `deadsim.fight.popular_ability_order`). This searches the order instead, per hero and objective, on each net
worth's best build. Ability points follow the game: an unlock at levels 1, 3, 5 and 8, a point at every other level
(32 in all), upgrades cost 1, 2 and 5 points, and an order buys strictly in sequence, so it saves points when its next
upgrade is a tier 3 (`deadsim.fight.abilities_for_order`). The milestones (10k to 50k: 12, 20, 24, 28 and 32
points) each take the tier spread with the most damage relative to the popular order's, under one rule: a single
order has to pass through all of them. The popular order is one of the candidates, so the summed gain is never
negative, though one milestone can give up a little for more at others. An upgrade never counts as a loss (each
spread scores as the best spread it contains), so the order can't win by skipping an upgrade the sim's cast logic
happens to play worse with; rows where that happens are flagged. Unlocks keep the popular order's sequence, since
all four come by ~3.8k souls. The damage test takes the order too (`ability_order`, the Test buttons on this card
load it). Duels, the overall score, survival and team fights still use the popular order. ~1 min per hero on one
core. It reads `work/jobs` (`--use-published` reads `out/heroes`) and runs in the patch reruns after the buy order.

## Overall search (damage before dying, counterplay on)
`scripts/overall_search.py`, output `out/overall/` (`scripts/export_overall.py`). Score = damage the build deals
before it dies against each of the 41 typical real builds at that net worth: the enemy fights back with x2 damage
and never dies, 30 s cap. Survivability, CC on the enemy and the enemy's own counters (resists, Dispel Magic) all
count. Counterplay is on (`hero_default_skill(counterplay=True)`): targets leave Alchemical Fire after 2 s
(1.5 s from Ascendant), item damage the sim over-predicts versus real matches is scaled down
(`sim/data/item_landing.json`), and actives with cooldowns over 60 s are ready only in their share of fights.
Why and results: `/mnt/project-files/analysis/build_scoring_review.md`. ~3 h on 4 cores (resumes from
`work/jobs_overall`).

## Full game build paths
`scripts/game_path.py`, output `out/path/` (`scripts/export_path.py`, shown in the Full game builds tab). One build
per hero that grows from 0 souls to 50k net worth, for Tyler's ask (2026-10-21): flow from 0 souls to high souls, value at
every stage, hit the investment spikes, agency through the whole game. Each stage (3k/6k early game, from `build_pool.EARLY_BUDGETS` pools, then 10k/18k/27k/37k/50k) is scored
with the overall test above, relative to the popular build at that net worth. A stage keeps the previous stage's
items: upgrading a held component is free, selling refunds half (the other half stays spent) and must beat the best
keep-everything build by 0.03 per item sold. Path score = mean stage score with the weakest stage counted twice.
Two starts at 3k (the best 3k build, and one built from the late game target's items and components) are each grown
with a constrained local search (fill the new souls by value per soul, then swaps on the 16-enemy screening pool,
confirmed on all 41); the best path wins. The buy order (from nothing) takes the piece with the most fight value per
soul against the next stage's enemies, counting two pieces as a pair when only together they cross a slot threshold
(800/1600/2400/3200/4800... souls in a slot; 4800 is the big jump), and lists every spike it reaches. Reads
`work/jobs_overall_<bracket>` when present (late game target, and the best build per stage alone for comparison).
Runs per rank tier in the patch reruns after the overall search.

Laning phase (Tyler, 2026-10-21: in lane, regen and other healing can be worth more than pure health). One 30 s fight
never lets regen pay off, so 3k and 6k are scored as a lane (`overall_search.lane_fight`, `LaneEvaluator`): up to 5
trades of 4 s against each enemy build (enemy damage x1), health carried from one trade to the next. In the 25 s gap
between trades the hero heals its health regen for the whole gap, out-of-combat regen after 10 s and Fortitude's % of
max health after its restore delay (all with regen amp). Under 25% health before a trade it backs, and the rest of
the lane is lost; a death ends it too. Score = damage dealt over the lane vs the popular build's. 10k (end of lane) is
half lane, half the 30 s fight (`MixEvaluator`). Trade length, gap, out-of-combat delay and the back threshold are
assumptions, not fitted to replays; with them the popular builds lose about a third of their health per trade and play
about 60-70% of the lane. Effect at Haze 3k on top of Extra Spirit: Extra Health goes from the best pick in the 30 s
fight (+46%) to below Extra Regen and Healing Booster in the lane (+8% vs +16% / +26%).

