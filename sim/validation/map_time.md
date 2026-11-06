# Healing items over-rated: fountain trips that real holders don't turn into map time (2026-11-06)

Question (24/7 loop, after the post-hotfix win check, PR #215/#216): Radiant Regeneration (+2.2 z over its real
edge), Healing Nova and Healing Booster score well above their real win edges. The real-ratio terms (death rate,
damage taken, farm) skip or barely move them (`hotfix_rates.md`), so the gap had to be in the duel, the sustain
terms or team value.

## Where their score comes from (27k, popular build + item vs popular build)

| Hero | Item | Score | Damage^0.5 | of which entry health | Map time | Team value |
|---|---|---|---|---|---|---|
| Infernus | Radiant Regeneration | x1.054 | x1.024 | +0.030 | **x1.030** | 1 |
| Haze | Radiant Regeneration | x1.065 | x1.035 | +0.019 | **x1.031** | 1 |
| Abrams | Radiant Regeneration | x1.040 | x1.012 | +0.002 | **x1.030** | 1 |
| Infernus | Healing Booster | x1.033 | x1.013 | +0.002 | **x1.023** | 1 |
| Haze | Healing Booster | x1.042 | x1.019 | +0.018 | **x1.026** | 1 |
| Infernus | Healing Nova | x1.185 | x1.086 | +0.002 | x1.004 | **x1.095** |
| Abrams | Healing Nova | x1.103 | x1.016 | 0 | 1 | **x1.094** |

("of which entry health" = damage factor minus the same build fought at the popular build's entry health.) For
Radiant and Healing Booster the largest single part is `map_time`: the fountain healing real holders save
(`sustain.json fountain_saved_hp_per_min`, Radiant 24 HP/min mid, 42 late) cuts the popular build's real heal trips,
each worth TRIP_S = 40 s (an assumption, never fitted).

## Real check: do holders use the saved time?

Time not spent walking back would go to farming and fighting, so holders should farm more jungle souls than
matched non-holders. They don't (fight_rate.json `jungle`, holders / matched non-holders):

| Item | 18k | 27k | 37k |
|---|---|---|---|
| Radiant Regeneration | 0.982 | 0.985 | 0.992 |
| Healing Booster | 0.976 | 0.973 | 0.969 |
| Extra Regen | 0.989 | 0.996 | 0.986 |
| Fortitude | 1.029 | 1.020 | 1.008 |
| Bullet Lifesteal | 1.045 | 1.034 | 1.011 |
| Spirit Lifesteal | 1.033 | 1.003 | 0.969 |

So the trip saving is credited where real holders show no extra map time (Radiant, Booster, Extra Regen) as well as
where they do (Fortitude, lifesteal).

## Anti-heal (Healbane in 20 more popular builds) is not it

`sim/scripts/sustain/healbane_split.py` (post-hotfix builds 10-31..11-05, Ritualist+, same hero / 5-min bin / slot
and tier): Radiant Regeneration's edge is -3.9 +- 0.9 with no enemy Healbane, -4.6 +- 0.5 with one, -3.9 +- 0.4 with
two or more. Healing Booster -0.8 / -1.1 / -0.5. Healing Nova +1.5 +- 1.9 / +0.9 +- 1.2 / -0.4 +- 0.8 (a slope, but
inside the noise; ally heal items Rescue Beam and Locket look alike). Two or more enemy Healbanes is already the
common case. The sim applies enemy Healbane in the duel.

## Change

`overall_search.TRIP_JUNGLE_GATE` (on): an item whose real jungle ratio at the fit budget nearest the build is below 1
saves no fountain trips (`trip_gated`, `field_saving(..., souls)`). Gated at 27k: Radiant, Booster, Extra Regen; at
37k also Spirit Lifesteal. Their in-fight healing and fight-entry health are unchanged.

## sim_vs_win, within slot and tier (local post-hotfix pools 10-31..11-05, shipped edges; rows rescored offline,
`analysis/scripts/sim_vs_win_map.py` and the same with the gate; map time is a pure item multiplier, so exact)

| | 27k | 27k hero halves | 37k | 37k hero halves |
|---|---|---|---|---|
| shipped | 0.3741 | 0.3697 / 0.3795 | 0.3469 | 0.3380 / 0.3575 |
| **gate: holders farm less (ratio < 1)** | **0.3822** | **0.3754 / 0.3900** | **0.3508** | **0.3409 / 0.3626** |
| gate only clear of noise (z <= -2) | 0.3803 | 0.3745 / 0.3872 | 0.3470 | 0.3370 / 0.3588 |
| map time off for every item | 0.3871 | 0.3805 / 0.3949 | 0.3430 | 0.3356 / 0.3520 |
| map time off for heal items | 0.3894 | 0.3819 / 0.3981 | 0.3443 | 0.3359 / 0.3544 |
| TRIP_S 20 s | 0.3842 | 0.3785 / 0.3909 | 0.3461 | 0.3379 / 0.3559 |

The gate was chosen among these variants on the same pools and edges, so its gain is somewhat optimistic; it is a
sign cut (Extra Regen at 0.996 and Spirit Lifesteal at 37k fall under it on small ratios), and the stricter z <= -2 cut
keeps 27k's gain but not 37k's. Radiant and Healing Booster, the items this is about, are gated under either cut at
27k. Their ratios are the pooled pre + post hotfix fit (#216, both are hotfix-changed items).

Dropping map time lifts 27k most but lowers 37k on both halves (Fortitude and the lifesteals, whose holders do farm
more, fall under their edges). The gate is the only line up at both budgets on both hero halves. Item gaps (sim - real,
z within slot and tier, 27k / 37k): Radiant +1.44 -> ~+0.95 / +1.51 -> ~+1.0, Healing Booster +0.51 -> ~-0.1, Extra
Regen +1.27 -> lower.

## Not changed: Healing Nova

Nova's gain is 3v3 team value (x1.09) plus its own heal in the duel. Its teammate healing matches the 3v3 relative to
Rescue Beam (`ally_heal.md`, factor 1), and that ratio fell by the same 14% in real games and the sim after the hotfix
(`hotfix_rates.md`). Scaling Nova + Rescue Beam's team value down raises sim_vs_win (x0.25: 27k 0.384, 37k 0.357,
both halves), but there is no real measurement to set it from (the ally heal factors are relative to the heal items'
median), so it is left as the next lead. Real Nova holders also deal 0.85x the damage of matched non-holders
(fight_rate.json dealt, z -31; Rescue Beam 0.80) while the sim gives them +2-9%.
