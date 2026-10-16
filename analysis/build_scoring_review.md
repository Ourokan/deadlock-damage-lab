# Why the builds favour some items, and the new "overall" score

Review of the step 3 searches (duel builds in `search/`, dummy damage builds in `damage/`) asked for by Tyler on
2026-10-16: why some items get picked over others, and whether utility, counterplay, hero stat scaling and the
investment spikes are counted. Patch 09-29-2026.

## Short version
- The **damage builds** (dummy search, the site's main tab) chase only damage into a dummy that never moves,
  never cleanses and never shoots back. So they spend ~0 souls on vitality (330 of 27k at 27k vs 6.7k in the popular
  build), and they lean on items the dummy can't punish: Alchemical Fire for its full 5 s, Mercurial Magnum,
  Focus Lens, Refresher, Shadow Weave, Escalating Exposure, Toxic Bullets, Mystic Shot.
- Two of those were also simply **over-modeled**: compared with real matches (same builds replayed in the sim), the
  sim gave Mercurial Magnum 5.5x its real damage and Focus Lens 2.7x. Toxic Bullets (1.9x), Scourge (1.6x),
  Mystic Shot (1.3x) and Headhunter (1.3x) were high too.
- Every fight started with **every cooldown ready**, which made Refresher (300 s cooldown) look like it doubles every
  fight.
- **Hero scaling and the spikes are already in the model.** Per-level (boon) growth of bullet damage, health and
  spirit power and all 11 investment thresholds per slot are applied (`sim/deadsim/build.py`). The biggest spike is
  at 4,800 souls in a slot (weapon +18% -> +46% weapon damage, vitality +20% -> +38% base health, spirit
  +19 -> +38 spirit power). Best builds almost never stop just short of it (6-8% of slots sit at 3,200-4,799, same as
  real builds). The damage objective simply gave the vitality spike no value, because health doesn't add damage.
- The **duel builds** already count survival (win rate vs real builds), and they keep vitality near popular levels.

## What changed
New objective **overall = damage dealt before dying**, against each of the 41 typical real enemy builds at that
net worth, with the enemy fighting back and counterplay switched on:

| Piece | How it counts |
|---|---|
| Damage | Full sim: gun, abilities, items, melee, at ranked median aim and real ability landing rates. |
| Survivability | You deal damage only while alive. The enemy's damage is doubled (two people on you) so the popular builds live a median ~14 s, close to the real median time to kill (~13 s). More health, resists, lifesteal and the vitality spike = more time = more damage. |
| Utility | Stuns, silences, disarms, slows and heal cuts count when they cut the enemy's damage to you. Movement, escape, vision and team heals are still not counted (see the win-edge table for those). |
| Counterplay | The enemy uses its real build: its resists, its Dispel Magic cleansing your Decay or Toxic Bullets, its Metal Skin. Targets walk out of Alchemical Fire after 2 s (1.5 s from Ascendant). Items the sim over-predicts versus real matches are scaled down to the real level. Active items with cooldowns over 60 s (Refresher...) are ready only in their share of fights (60 s assumed between fights). |

Code: `damage/scripts/overall_search.py`, sim switch `hero_default_skill(..., counterplay=True)` in
`sim/deadsim/accuracy.py` (off by default, so older results reproduce), item factors in
`sim/data/item_landing.json` (`sim/scripts/item_landing.py`).

### Item damage, real vs sim (holders only, item damage per gun damage)
Factor = real / sim. Used only when below 1. Items above 1 get more in real games mostly from hitting several heroes
in team fights, which a 1v1 should not count.

| Item | Holders | Factor |
|---|---:|---:|
| Mercurial Magnum | 310 | 0.18 |
| Focus Lens | 44 | 0.37 |
| Toxic Bullets | 342 | 0.53 |
| Scourge | 116 | 0.63 |
| Silence Wave | 31 | (too few holders, not used) |
| Mystic Shot | 311 | 0.76 |
| Headhunter | 334 | 0.77 |
| Lightning Scroll | 54 | 0.81 |
| Quicksilver Reload | 820 | 0.84 |
| Decay | 45 | 1.00 |
| Alchemical Fire | 55 | 1.70 |
| Torment Pulse / Capacitor / Mystic Reverb | 205-350 | 3.1 / 3.5 / 6.5 (sim under-models them) |

Alchemical Fire note: real players get *more* fire damage per gun damage than the sim gives with the target standing
in it the whole time, almost surely from hitting several heroes in team fights. The 2 s walk-out rule is a 1v1
assumption (Tyler's point), not something the data shows. Its real win edge is also positive (+1.6, below).

## Real-game check: win edge of every item
`analysis/out/item_win_edge.md` (script `analysis/scripts/item_win_edge.py`): 227,561 ranked matches. For each
first purchase, the win rate versus players of the same hero buying another item of the same slot and tier in the
same 5-minute window, at the same team souls lead and own souls position. Observational, so trust direction more
than size, and items bought while behind (Disarming Hex, Metal Skin, Decay) look worse than they are.

The real data agrees with the fixes: the dummy search's favourites mostly don't win more games.

| Dummy favourite | Real edge (pts) | | Utility / defensive item | Real edge (pts) |
|---|---:|---|---|---:|
| Mercurial Magnum | -0.9 | | Diviner's Kevlar | +2.9 |
| Refresher | -0.7 | | Heroic Aura | +2.9 |
| Shadow Weave | -1.1 | | Magic Carpet | +3.6 |
| Focus Lens | -0.4 (n.s.) | | Cheat Death | +2.4 |
| Boundless Spirit | -1.1 | | Witchmail | +1.9 |
| Decay | -2.6 | | Ethereal Shift | +1.9 |
| Toxic Bullets | -0.3 (n.s.) | | Spirit Resilience | +1.5 |
| Escalating Exposure | +0.1 (n.s.) | | Superior Duration | +1.5 |
| Alchemical Fire | +1.6 | | Spirit Rend | +1.3 |

Magic Carpet, Heroic Aura, Ethereal Shift and Healing Nova are movement / team items the sim can't value at all.

## Results of the overall search (all 41 heroes x 5 budgets)
Outputs: `damage/out/overall/` (`index.json`, `summary.csv`, `heroes/<id>_<budget>.json` with the top 10 builds,
`items.md` with item counts per budget). Medians over heroes:

| Net worth | Overall best vs popular (damage before death) | Damage-best vs popular (same test) | Time alive: overall best / popular / damage-best | Overall best's dummy damage vs popular |
|---|---:|---:|---|---:|
| 10k | 1.49x | 1.08x | 16.4 / 12.6 / 10.6 s | 1.13x |
| 18k | 1.73x | 1.11x | 20.6 / 15.0 / 11.1 s | 1.38x |
| 27k | 1.84x | 1.14x | 21.4 / 16.2 / 10.1 s | 1.44x |
| 37k | 2.28x | 1.36x | 23.6 / 15.0 / 10.6 s | 1.59x |
| 50k | 2.54x | 1.61x | 23.2 / 14.0 / 11.6 s | 1.65x |

The old damage-best builds hit the dummy 2.3x harder than popular at 27k, but against real enemies they die in
~10 s and end up only 1.14x popular. The overall builds give up some dummy damage (1.44x popular instead of 2.3x),
live ~5 s longer than popular, and deal 1.84x popular's damage before dying.

What moved at 27k (count of 41 heroes holding the item, overall / damage-best / popular):
- Out: Alchemical Fire 0 / 22 / 0, Mercurial Magnum and Refresher gone, Toxic Bullets 6 / 21 / 3,
  Escalating Exposure 16 / 31 / 4, Focus Lens 7 / 13 / 0, Titanic Magazine 9 / 17 / 7.
- In: Enchanter's Emblem 27 / 6 / 10, Spirit Sap 25 / 3 / 1, Spirit Resilience 13 / 0 / 7, Headhunter 16 / 3 / 5,
  Diviner's Kevlar 10 / 0 / 0, Spirit Rend 10 / 2 / 0, Spirit Lifesteal 8 / 0 / 5, Silence Wave 7 / 0 / 0.
- Kept: Mystic Shot 28 / 29 / 5, Decay 26 / 20 / 0.
- Vitality spend is back to the popular level (6.4k vs 6.7k at 27k; damage-best had 0.3k).

Examples at 27k (damage before death, overall best / popular / damage-best):
- Haze: Focus Lens, Burst Fire, Diviner's Kevlar, Bullet Resist Shredder, Decay, Kinetic Dash, Swift Striker
  (2,715 / 843 / 660; the damage-best Haze build lives 3.8 s).
- Infernus: Spirit Lifesteal, Spirit Sap, Fury Trance, Spirit Resilience, Titanic Magazine, Superior Duration,
  Decay, Toxic Bullets, Spirit Rend (3,811 / 2,110 / 1,624).
- Abrams: Mystic Shot, Spirit Sap, Lifestrike, Escalating Exposure, Spirit Snatch, Toxic Bullets, Enchanter's
  Emblem, Spirit Rend (6,551 / 4,046 / 4,317).

### Where the sim and real games still disagree
- **Decay** (26 of 41 overall builds; real edge -2.6), **Silence Wave** (-2.8) and **Rusted Barrel** (-4.8) rate well
  in the sim. They're bought mostly while behind, which makes their real edge look worse than it is, but Decay's
  real damage factor is only fitted on 45 holders. They're worth a closer look before we trust them.
- **Movement and team items** (Magic Carpet +3.6, Heroic Aura +2.9, Ethereal Shift +1.9, Healing Nova +1.7) win
  real games, but the 1v1 sim gives them nothing. The mechanics module's escape/chase movement (off) is the
  closest thing we have.
- The **2 s Alchemical Fire walk-out** and **60 s between fights** are assumptions. With Alchemical Fire at
  2 s it drops out of every overall build. Real data says it does well (+1.6 edge, more damage than the sim gives),
  probably from team fights.
