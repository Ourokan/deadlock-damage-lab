# Death cost (2026-10-25)

Question: the overall score (damage before dying in a 30 s duel) gives a death no cost beyond the damage not dealt
after it. Does charging what a real death costs make the score rank items more like real wins (Cheat Death and late
vitality win real games but are rarely picked)?

## What a death costs in real Phantom+ games

`sim/scripts/death_cost/fit_death_cost.py` -> `sim/data/death_cost.json` (600 Phantom+ matches' death details from
the match metadata, `fetch_deaths.py`; 260 of their replays from `sim/scripts/fight_length`).

| net worth | respawn | own souls / s | enemy team's kill bounty |
|---|---|---|---|
| 0-5k | 8-16 s | 13.2 | 580 (44 s of farm) |
| 10-18k | 27-38 s | 19.9 | 950 (48 s) |
| 18-27k | 50-62 s | 22.9 | 1380 (60 s) |
| 27-37k | 62-77 s | 23.6 | 1720 (73 s) |
| 37k+ | 81-87 s | 25.4 | 1560 (61 s) |

The victim loses no souls besides the farm it misses while dead (its own gain per death, -1390 at 27-37k, is about
its soul rate x respawn). Per engagement (a hero's pair fights merged within 5 s): deaths 0.15 / 0.26 / 0.22, alive
seconds per engagement 57 / 76 / 64, walk back after respawn 11 / 5 / 0 s (lane / mid / late).

## The score change (opt-in: `overall_search.DEATH_COST`)

death_value = (c + d_pop L) / (c + d L): c = alive seconds per engagement, L = respawn + walk back + bounty in seconds
of own farm, d = the hero's real deaths per engagement x the build's sim death chance / the popular build's, a sim
death at t s counting x P(a real fight is still going at t).

## Check against real wins (`analysis/scripts/sim_vs_win.py`, 42 heroes, 27k, win blend off)

| | all pairs | per item |
|---|---|---|
| no death cost (with Healing Tempo) | 0.136 | 0.216 |
| death cost, time only | 0.132 | 0.205 |
| death cost with bounty | 0.128 | 0.194 |

Cheat Death's gain per 1000 souls goes 0.020 -> 0.044 -> 0.067 (real edge +2.9), but Metal Skin (-5.8) and
Rebuttal (-2.2) rise as much.

Why: `analysis/scripts/death_check.py`. At equal hero, net worth (20-37k) and game length, real holders of tank items
die about as often per 10 minutes as non-holders (Colossus 0.99, Spirit Resilience 1.02, Plated Armor 1.02, Metal
Skin 1.06, best Diviner's Kevlar 0.90), where the sim's death chance says 0.48-0.75. Over 1158 hero x item pairs
the sim and real death ratios don't correlate (r -0.04). Real players spend survivability on fighting more, not on
dying less, so a death cost proportional to the sim's death chance overrates every tank item. Left off; the data and
switch stay for a later model that ties deaths to how players use the extra health.

## Healing Tempo (on)

Was unmodeled (empty handler). Now a heal from an ability or item (not regen or passive lifesteal) gives +35% fire
rate and +1.25 m/s for 7 s, once per second. Sim gain 0.011 -> 0.017 per 1000 souls (real edge +0.7); all pairs
0.136 -> 0.136, per item 0.214 -> 0.216.
