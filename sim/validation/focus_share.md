# Debuff Reducer vs real wins: team share of damage taken (2026-10-28)

Question (follow-up of `status_focus.md`): after #175 Debuff Reducer is still 12th of 14 tier-2 vitality items by
sim gain at 27k (mean gain rank 119 of 141), while its real Phantom+ win edge is third of its tier (+0.30 per hero,
+1.1 pooled in `analysis/out/item_win_edge.md`). What does the score miss?

## Where its score goes (27k, Abrams)

| item | damage before death | focus value | farm value | death rate value | score |
|---|---|---|---|---|---|
| Debuff Reducer | 1.032 | 0.979 | 0.995 | 0.998 | 0.992 |
| Spirit Shielding | 1.026 | 1.018 | 0.999 | 1.025 | 1.055 |
| Spirit Lifesteal | 1.026 | 1.000 | 1.000 | 1.000 | 1.031 |

The duel credits it like its neighbours; the real holder-rate factors (`fight_rate.json`) take 2.5% off. Its holders
take 1.054x damage per minute at 27k (1.068x at 37k), farm 0.95x jungle, but also deal 1.03x and join 1.03x kills.

## Bloodier games, not only focus

The ratios are matched on hero, net worth and game time, not on the game itself. Debuff Reducer holders' enemy teams
deal 1.029x (27k) / 1.042x (37k) damage per minute: they play bloodier games (it is bought late, minute 27, often
against CC-heavy teams). `fit_fight_rate.py` now also writes each item's ratio of the player's share of its team's
damage taken in the interval (`tshare`) and of its team's jungle souls (`jshare`):

| 27k | taken / min | team share of taken | enemy team dealt / min |
|---|---|---|---|
| Debuff Reducer | 1.054 | 1.028 | 1.029 |
| Rebuttal | 1.067 | 1.038 | 1.030 |
| Return Fire | 1.031 | 1.018 | 1.016 |
| Metal Skin | 1.031 | 1.011 | 1.022 |
| Fortitude | 1.093 | 1.076 | 1.015 |
| Spirit Shielding | 0.958 | 0.961 | |

## Results (sim_vs_win, blend off, all heroes, full runs)

| | all pairs | within slot and tier | per item | within, hero halves | DR rank (tier / all) |
|---|---|---|---|---|---|
| 27k main (`taken`) | 0.297 | 0.333 | 0.435 | 0.333 / 0.334 | 12 / 119 |
| 27k `FOCUS_KEY = "tshare"` | 0.296 | 0.331 | 0.438 | 0.332 / 0.330 | 12 / 104 |
| 37k main | 0.286 | 0.317 | 0.416 | 0.315 / 0.320 | 12 / 120 |
| 37k `tshare` | 0.291 | 0.319 | 0.425 | 0.320 / 0.319 | 12 / 80 |

Offline rescales (score x new / old item factor) agreed in direction (37k within 0.323, 27k 0.332), at FOCUS_GAMMA
0.3-0.6, and with the ratios from either match-id half. 27k within slot and tier drops in both hero halves, so the team
share stays OFF (`overall_search.FOCUS_KEY = "taken"`, `sim_vs_win.py --focus-key tshare` to rerun it). Farm value
on `jshare` (share of the team's jungle) was a wash at FARM_GAMMA 0.1 (27k within 0.333, 37k 0.324 offline); raising
FARM_GAMMA lifts within at both budgets (0.2: 0.341 / 0.328 on `jungle`) but lowers Debuff Reducer and was not the
question here (FARM_GAMMA is set from the economy, see `overall_search.py`).

## The rest of the gap is in the duel

With the focus and farm factors taken out, Debuff Reducer is still 9th of 14 (27k mean gain per 1000 souls):

| item | gain | real edge |
|---|---|---|
| Spirit Shielding | +0.035 | +0.07 |
| Enchanter's Emblem | +0.035 | +0.32 |
| Bullet Lifesteal | +0.029 | -0.62 |
| Battle Vest | +0.029 | -1.09 |
| Spirit Lifesteal | +0.029 | +1.25 |
| Healing Booster | +0.023 | -1.18 |
| Healbane | +0.022 | -1.28 |
| Reactive Barrier | +0.020 | -0.19 |
| **Debuff Reducer** | **+0.019** | **+0.30** |
| Guardian Ward | +0.016 | -0.45 |
| Weapon Shielding | +0.015 | -1.67 |
| Restorative Locket | +0.013 | -0.03 |

So the tier's losers (Battle Vest, Bullet Lifesteal, Healing Booster, Healbane) are scored above it by the duel
itself. What would close it needs a real measure the data here doesn't have: how long Phantom+ players actually spend
stunned, silenced and disarmed per fight (replay modifier events), against the duel's CC from the 41 enemy builds.
The current replay extracts carry casts only.
