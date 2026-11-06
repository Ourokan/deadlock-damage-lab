# Divine Barrier: barrier real holders give teammates (2026-11-06)

Question: on the fresh Phantom+ win edges (patch 09-29 hotfix, 231k matches through 11-04), which items does the
overall score rank furthest from their real win edge within their slot and tier, and why?

## Biggest gaps before (sim gain vs real edge, both centred within hero x slot x tier, z units, 27k / 37k)

| Sim under real | gap | Sim over real | gap |
|---|---|---|---|
| Golden Goose Egg | -2.8 / -2.7 | Heroic Aura | +2.1 / +1.8 |
| Trophy Collector | -1.8 / -1.8 | Capacitor | +2.1 / +1.9 |
| Superior Cooldown | -1.7 / -2.1 | Divine Barrier | +1.7 / +1.7 |
| Debuff Reducer | -1.6 / -1.4 | Decay | +1.7 / +1.9 |
| Ballistic Enchantment | -1.5 / -1.5 | Mystic Shot | +1.7 / +1.9 |
| Counterspell, Slowing Bullets | -1.2 to -2.1 | Spirit Shielding | +1.5 / +1.8 |

sim_vs_win on main: within slot and tier (both budgets) 0.359; per budget, edges also centred: 27k 0.406, 37k 0.382.

## Where Divine Barrier's score comes from

Log score parts at 27k over the popular builds (mean over heroes): team value +0.126, death rate +0.103, map +0.010,
focus +0.007, damage -0.010. Heroic Aura is the only other item with team value that large (+0.129). The 3v3
(team_value.py) casts Divine Barrier on the neediest teammate whenever it is ready; ally_heal.py (#151) already
scales heal items by what real holders give teammates, but barrier items had no data and kept 1.

## Real: barrier given to teammates

holder_rates.py on fight_rate_ext (74k matches; `teammate_barriering`, `player_barriering`), holders vs non-holders at
the same hero, net worth and game time, extra HP/min = (ratio - 1) x the non-holders' base:

| | to teammates 27k | even / odd match ids | 37k | own barrier 27k |
|---|---|---|---|---|
| Divine Barrier | +172 | +172 / +173 | +197 | +212 |
| Guardian Ward | +16 | +17 / +15 | 0 | +31 |
| Healing Nova (team heal) | +337 | +338 / +336 | +362 | |
| Rescue Beam (team heal) | +191 | +195 / +188 | +213 | |

The 3v3 at 27k gives 1341 HP of ally barrier per fight minute with Divine Barrier (Nova 1203 heal, Rescue Beam 824).
Real / 3v3: Divine Barrier 0.128, Nova 0.280, Rescue Beam 0.233. Over the heal items' median, Divine Barrier's
factor is 0.50: real holders put about half of the barrier on themselves (that part already counts in the duel and
the death rate). Guardian Ward measures 0.115.

## Change

`sim/scripts/team/ally_barrier.py HOLDER_RATES.json` writes the barrier items into `sim/data/ally_heal.json`
(overall_search.team_value already multiplies by it; ally_heal.py now keeps those entries when rerun). Applied to
Divine Barrier only (factor 0.5). Guardian Ward is recorded (`measured_factor` 0.115) but keeps 1: it already ranks
under its edge from its other parts (-1.2 z at 27k), and cutting it lowers every line (offline 27k within 0.3805 ->
0.3760 with both, 0.3832 with Divine Barrier alone).

## Results (full sim_vs_win, all heroes, 27k + 37k)

| | all pairs | within slot and tier | edges clear of noise | per item |
|---|---|---|---|---|
| main | 0.321 | 0.359 | 0.440 | 0.487 |
| Divine Barrier 0.5 | 0.321 | 0.361 | 0.439 | 0.488 |

Per budget (edges centred too), hero halves: 27k 0.406 (0.406 / 0.407) -> 0.409 (0.409 / 0.409), 37k 0.382
(0.382 / 0.381) -> 0.384 (0.385 / 0.383). Divine Barrier's gap +1.74 / +1.66 -> +1.09 / +0.98 z. Small but on both
halves of heroes, and the real measure agrees on both match-id halves.

Not changed: Heroic Aura (largest gap; its team value is an aura plus an active that leaves no barrier/heal stat to
measure; sign right, edge +3.2 pts). Earlier tries not to repeat: team value ^0.5 and teammate death factors
(split_shot_range.md).

Holder rates used: /mnt/project-files/analysis/work/holder_rates/holder_rates_2026-11-06.json.
