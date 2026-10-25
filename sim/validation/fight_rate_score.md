# Real death rate in the overall score (Phantom+)

Data and tables: [fight_rate.md](fight_rate.md) (written by sim/scripts/fight_rate/fit_fight_rate.py; this page is by hand).

Across items (27k table vs the per-item mean real win edge), which real rate tracks winning:

| Holders / non-holders | r with real win edge | r with sim gain |
|---|---|---|
| Damage taken / min | -0.04 | +0.05 |
| Damage dealt / min | +0.19 | +0.54 |
| Deaths / min | -0.32 | +0.04 |
| Kills + assists / min | +0.39 | +0.62 |

Tank items' extra health goes into taking more damage per minute, and that by itself doesn't win; dying less does,
and the sim (a duel that ends at a death) didn't see it. So:

- **death_rate_value (ON)**: the score x (c + d_pop L) / (c + d L), the share of the game spent fighting (real alive
  s per engagement c, seconds a death costs L incl. the kill bounty, sim/data/death_cost.json), with d = the
  hero's real deaths per engagement x the product of the held items' death ratios from the tables below (|z| >= 3,
  movement items left out: movement_value counts their deaths already).
- **fight_value (OFF)**: an "HP budget" model, fights per minute = max health ^ the damage-taken elasticity / sim
  health lost per fight. Every exponent variant ranks items less like real wins.

analysis/scripts/sim_vs_win.py, 42 heroes, popular build + one item, Pearson with the per-hero real edge:

| Setup | 27k all pairs | 27k per item | 37k all pairs | 37k per item |
|---|---|---|---|---|
| before | 0.133 | 0.209 | 0.146 | 0.219 |
| + death_rate_value | **0.168** | **0.265** | **0.174** | **0.264** |
| + fight_value instead (HP budget, exponent 0.35-1.0) | 0.095-0.125 | 0.146-0.202 | | |

Mean sim gain rank of 141 items (27k / 37k): Cheat Death 119 -> 52 / 117 -> 54, Rebuttal 25 -> 110 / 31 -> 112,
Metal Skin 82 -> 92 / 58 -> 67, Restorative Locket 6 -> 3 / 25 -> 9, Spirit Resilience 43 -> 24 / 35 -> 17.
These are associations at equal hero, net worth and game time, not controlled effects (who buys an item rides
along); Extra Health holders die 8% more at 7.5-13.5k net worth, for one.
