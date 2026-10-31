# Price of a death in the overall score (2026-10-29)

Question: after #209 (range reach), which items does the overall score still rank furthest from their real Phantom+
win edge within their slot and tier, and why?

## Biggest gaps before (sim gain vs real edge, both centred within hero x slot x tier, in standard deviations, 27k / 37k)

| Sim under real | gap | Sim over real | gap |
|---|---|---|---|
| Golden Goose Egg | -4.1 / -4.2 | Extra Charge | +1.8 / +2.3 |
| Superior Cooldown | -1.7 / -2.0 | Decay | +1.8 / +1.9 |
| High-Velocity Rounds | -1.2 / -2.0 | Capacitor | +1.8 / +1.8 |
| Debuff Reducer | -1.6 / -1.5 | Mystic Shot | +1.7 / +1.8 |
| Slowing Bullets | -1.2 / -1.7 | Heroic Aura | +1.8 / +1.6 |
| Trophy Collector, Counterspell, Superior Duration, Ballistic Enchantment | -1.1 to -1.2 | Monster Rounds | +1.2 / +1.8 |

## Taking the score apart

On the sim_vs_win rows the score is exactly damage ratio ^ DAMAGE_ELASTICITY x map time x team value x death rate x
focus x farm (pure item multipliers; residual 0). Correlation of each part with the real edge within slot and tier
at 27k: death rate +0.32, damage +0.20, focus +0.15, team +0.12, map +0.05, farm +0.01; least squares of the edge on
the parts weighs the death rate part 2.4x (2.1-2.8 per hero half) the damage part.

## Real data: what a death costs next to damage

`sim/scripts/fight_rate/death_price.py HOLDER_RATES.json` (holder_rates.py on fight_rate_ext, 140 items, healing items
out, centred within slot and tier), win points per log ratio:

| | dealt | deaths / ka | ka | taken | death : dealt |
|---|---|---|---|---|---|
| 27k all | +6.9 | -14.2 | -8.5 | -4.6 | 2.06 |
| 27k even / odd match ids | +7.1 / +6.7 | -14.3 / -13.4 | | | 2.03 / 2.01 |
| 37k all | +7.4 | -12.4 | -5.4 | -4.8 | 1.66 |
| 37k even / odd | +7.5 / +7.7 | -11.2 / -12.4 | | | 1.50 / 1.62 |

The score moved ~1x a log change of real damage dealt (DAMAGE_ELASTICITY 0.5 on the sim gain, which real holders show
0.51x of) but only 0.33x a log change of the death ratio: death_rate_value priced a death at the game time it takes
(respawn + walk back + bounty: d L / (c + d L) = 0.33 at mid game). A real death also loses the fight and what the
team would have taken with it. Real ratio 1.7-2.1, score 0.33.

## Change (gamma 1.5 + tier-1 out from 27k by default, Tyler's pick 2026-10-29)

- `overall_search.DEATH_RATE_GAMMA` (2 tested): death_rate_value ^ gamma. The real ratio alone would take ~5; sim_vs_win peaks
  at 2 (37k) and 2-3 (27k), below it because the duel's damage before death already holds part of a death's cost.
- `overall_search.DEATH_RATE_T1_FROM` (27000 tested): tier-1 items left out of the death ratios from the 27k table up. Their
  leftover holders are low-farm players on teams ahead (`tier1_death_rate.md`): kills + assists 1.07-1.15x at
  27k/37k (Monster Rounds 1.08, Close Quarters 1.07, Extra Charge 1.07; ~1.0 at 10-18k), so deaths / ka gave them a
  bonus the gamma would double. Alone it was flat (2026-10-28, within -0.0004); with the gamma it is what lets 27k gain.

Offline grid (exact on the old rows), within slot and tier (hero halves):

| gamma | 27k, T1 kept | 27k, T1 out | 37k |
|---|---|---|---|
| 1 (main) | 0.352 (0.343 / 0.360) | 0.360 | 0.332 |
| 2 | 0.379 | 0.403 (0.396 / 0.411) | 0.343 (offline; full run 0.377) |
| 3 | 0.382 | 0.420 | 0.334 |

## Results (full sim_vs_win runs with gamma 2 + T1_FROM 27000, blend off, all heroes)

| | all pairs | within slot and tier | within, hero halves | edges clear of noise | per item |
|---|---|---|---|---|---|
| 27k main | 0.317 | 0.352 | 0.343 / 0.360 | 0.445 | 0.452 |
| 27k new | 0.371 | 0.403 | 0.396 / 0.411 | 0.511 | 0.520 |
| 37k main | 0.304 | 0.332 | 0.324 / 0.340 | 0.420 | 0.426 |
| 37k new | 0.346 | 0.377 | 0.369 / 0.384 | 0.474 | 0.484 |

Gaps (27k / 37k): Extra Charge +1.8 / +2.3 -> +0.1 / +0.4, Monster Rounds +1.2 / +1.8 -> -0.3 / -0.2, Close Quarters
+1.2 / +1.1 -> +0.4 / 0.0, Rebuttal -1.3 / -0.5 -> -0.6 / -0.2, Golden Goose Egg -4.1 -> -3.2, Cheat Death -0.5 -> +0.4.
Still over: Heroic Aura (+2.3, real edge +1.8 pt, sign right), Spirit Shielding +1.7 / +2.0, Divine Barrier +1.8 / +1.6,
Capacitor, Decay, Mystic Shot (no mechanism found, see earlier write-ups). Still under: Golden Goose Egg, Superior
Cooldown, Trophy Collector, Slowing Bullets, Ballistic Enchantment, Debuff Reducer, Counterspell.

Gamma 1.5 (exact rescale of the gamma 2 rows): within 27k 0.386 (0.379 / 0.393), 37k 0.362 (0.355 / 0.368).

## Best builds (overall_search, 16 heroes at 27k, main vs each setting)

| | summed real edge of the best build, mean change | damage before death, mean / median / worst |
|---|---|---|
| gamma 2 | -0.32 | 0.966 / 1.000 / 0.70 (Dynamo; Abrams 0.86, Haze 0.87, Wraith 1.32) |
| gamma 1.5 | +0.13 | 0.967 / 1.000 / 0.68 (Abrams; Yamato 0.83, McGinnis 0.78) |

Dynamo at gamma 2 swaps Alchemical Fire / Arcane Surge / Fortitude / Mystic Reverb for Divine Barrier, Duration
Extender, Mystic Shot, Spirit Snatch (edge -4.2 on him) and Stalker. Marginal items rank much more like real wins, but
the searched builds get no closer to real wins and deal less damage (Tyler's main use is damage); the choice went to
Tyler (below). `sim_vs_win.py --death-gamma 2` reproduces
the check (it sets DEATH_RATE_T1_FROM 27000 with any gamma other than 1).

Decision (Tyler, 2026-10-29): the middle setting, DEATH_RATE_GAMMA 1.5 with DEATH_RATE_T1_FROM 27000, on by default
(sim_vs_win within 27k 0.352 -> 0.386, 37k 0.332 -> 0.362; rerun requested).
