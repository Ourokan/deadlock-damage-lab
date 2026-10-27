# Focus cost: pricing damage taken (2026-10-27)

Follow-up of `return_fire.md`. The overall duel hits every build with the same enemy damage (`FOCUS`), so a build
never pays for drawing more of the enemy team's damage. Return Fire is the clearest case: its reflect only exists
while the holder is being shot, real holders take more damage per minute and lose 5.5 win points on every hero.

## What the real data says

`sim/data/fight_rate.json` (74k Phantom+ matches' stat timelines, holders vs non-holders at the same hero, net worth
and game time) has each item's damage-taken ratio next to dealt, deaths and kills + assists. Across items, against
the all-hero matched win edge (Ritualist-Phantom bracket, `analysis/out/item_win_edge.json`, 153 items with 3000+
holders), log ratios:

| | 27k | 37k |
|---|---|---|
| r: dealt / taken / deaths / ka | +0.10 / -0.07 / -0.30 / +0.29 | +0.17 / -0.03 / -0.30 / +0.32 |
| win points, all four together | +4.6 dealt, -2.3 taken, -8.4 deaths, +9.1 ka | +5.5, -1.3, -9.0, +10.3 |

Taken alone barely tracks wins (the fight-rate memo's r -0.04), but at equal damage dealt, deaths and kills it
costs. The duel's damage term already stands in for dealt (DAMAGE_ELASTICITY) and death_rate_value for deaths;
nothing stood in for taken.

## The factor

`overall_search.focus_value`: the product of the held items' real taken ratios (|z| >= 3, clamped like the death
ratios) ^ -FOCUS_GAMMA, divided by the popular build's. Left out: movement items (as in death_rates), healing items
(HEAL_ITEMS: their holders take damage they heal back) and Cheat Death (FOCUS_SKIP: holders take 15% more because
it keeps them alive through lethal damage; with it in, Cheat Death (+2.2 pt real edge) fell from rank 19 to 56).
94 items carry a ratio at 27k, from 0.88 (Echo Shard, Diviner's Kevlar) to 1.10 (Colossus, Lifestrike).

## sim_vs_win (blend off, all heroes; local pools from the shared 10-14 snapshots, so levels differ from the CI runs)

Offline from `sim_vs_win.py --out` rows (exact: the factor is a pure item multiplier).

| 27k | all | within slot and tier | damage items | per item | within, hero halves |
|---|---|---|---|---|---|
| main | 0.223 | 0.263 | 0.108 | 0.321 | 0.252 / 0.274 |
| gamma 0.2 | 0.231 | 0.273 | 0.130 | 0.330 | 0.262 / 0.283 |
| gamma 0.4, Cheat Death in | 0.233 | 0.274 | 0.145 | 0.327 | 0.265 / 0.284 |
| **gamma 0.4 (kept)** | **0.238** | **0.278** | **0.145** | **0.335** | **0.268 / 0.288** |
| gamma 0.6 | 0.237 | 0.276 | 0.154 | 0.327 | 0.267 / 0.285 |
| gamma 1.0, Cheat Death in | 0.217 | 0.253 | 0.161 | 0.288 | 0.245 / 0.260 |

| 37k | all | within | damage items | per item | within, hero halves |
|---|---|---|---|---|---|
| main | 0.224 | 0.250 | 0.126 | 0.306 | 0.236 / 0.265 |
| gamma 0.3 | 0.227 | 0.258 | 0.159 | 0.308 | 0.247 / 0.269 |
| **gamma 0.4** | **0.225** | **0.257** | **0.166** | **0.303** | **0.247 / 0.267** |

Within slot and tier rises on both hero halves at both budgets; per item dips 0.003 at 37k. The plateau is 0.3-0.5
on every split. Ranks (27k mean gain): Return Fire 129 -> 137, Metal Skin 104 -> 110, Spirit Strike 2 -> 6,
Guardian Ward 4 -> 11; Heroic Aura stays 1 (its holders take 7% less).

## Return Fire's reflect without aim: still not kept

Tried with the focus cost on: `items_fx.ReturnFire` without the holder's gun accuracy, its pooled landing refit
twice from the audit (`item_landing_heroes.py --item "Return Fire" --pooled`, audit of the 9 heroes with RF holders:
real/sim 3.05 -> 0.49 without aim -> 0.94 after the refit, landing 3.754 -> 0.757). Its sim gain rises from 0.004 to
0.024 per 1000 souls (rank 129 -> 36) and sim_vs_win 27k falls 0.223 -> 0.209 without the focus cost, 0.220 with it
(focus cost alone 0.233); damage items 0.108 -> 0.039 / 0.087. The focus cost takes only ~1.2% off Return Fire (taken
1.031); the rest of the gap is not about focus:

- the sim's damage gain with real reflect (x1.125 damage before death) matches real holders' damage per minute
  (+5.3%) through DAMAGE_ELASTICITY (1.125 ^ 0.5 = 1.061), so the damage is right in size;
- across items, real holders' damage dealt doesn't predict their kills + assists at all (slope of log ka on log
  dealt -0.03 to 0.14 over 18-50k), so Return Fire's flat ka (0.995) is not an item-specific "damage that doesn't
  convert" signal either.

So the real reflected damage is real damage that, like most damage, wins little, and Return Fire loses for reasons
the score doesn't see. It keeps the old cut (`accuracy.LENGTH_CAP_SKIP`).
