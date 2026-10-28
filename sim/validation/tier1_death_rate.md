# Cheap items' death rate bonus: why, and the fixes tried (2026-10-28)

Question (follow-up of `ballistic_stacks.md`): holders of almost every tier-1 item get more kills + assists per
minute at 27-37k, so the deaths-per-engagement factor (`overall_search.DEATH_PER_KA`, #171) rewards the tier-1
items whose deaths ratio clears |z| 3 (Extra Charge, Monster Rounds, Close Quarters) and not the others. Halving the
tier-1 factors lifts sim_vs_win but has no game reason. Is there a principled fix?

**Result: the cause is found, but no principled fix keeps sim_vs_win. Nothing shipped; the score is unchanged.**

## Why late tier-1 holders fight more

Holder shares (`sim/data/fight_rate.json`, intervals holding the item at each search band): tier-1 items peak at 10k
and are mostly sold by 27-37k (Extra Charge 15% -> 7% -> 4% at 10k / 37k / 50k, Restorative Shot 15% -> 4% -> 1%).
Their deaths / ka ratio falls with that (Close Quarters 1.01 at 10k, 0.92 at 37k; Monster Rounds 1.02 -> 0.88), so
the bonus belongs to the players who still hold a cheap item late, not to the item.

`sim/scripts/fight_rate/holder_controls.py` (74k Phantom+ matches, fight_rate_ext) redoes the holder comparison with
one more stratum each. Mean log ratio over the 23 tier-1 items, 37k band (match-id halves):

| Extra stratum | Kills + assists | Deaths |
|---|---|---|
| none (shipped tables) | +0.063 / +0.060 | +0.011 |
| previous interval's kills + assists | +0.058 / +0.056 | +0.014 |
| souls gained over the previous interval | +0.062 / +0.059 | +0.007 |
| number of items held | +0.019 / +0.022 | -0.014 |
| **team net worth lead** | **+0.017 / +0.016** | +0.045 |
| team lead and items held | -0.008 / -0.013 | +0.006 |

27k is the same shape (+0.032 -> +0.001 / +0.006 with the lead). Not momentum: at the same own net worth, the late
holders of cheap items are mostly low-farm players on teams that are ahead, and get kills + assists from that.
Matched on the lead, the items lose their bonus (deaths / ka at 37k: Monster Rounds 0.877 -> 0.989, Extra Charge
0.890 -> 0.972, Close Quarters 0.917 -> 1.019, Extra Spirit 0.941 -> 1.012), and Rebuttal goes from 1.016 to 1.044.

## Fixes tried (sim_vs_win rows rescaled offline, exact for these pure item multipliers)

Main on this branch: 27k all pairs 0.2982, within slot and tier 0.3341 (hero halves 0.3359 / 0.3326), per item
0.4371; 37k 0.2847, 0.3156 (0.3179 / 0.3138), 0.4148.

| Variant | 27k all | 27k within (halves) | 27k item | 37k all | 37k within (halves) | 37k item |
|---|---|---|---|---|---|---|
| refit matched on team lead (death rate only) | 0.258 | 0.310 (0.313 / 0.307) | 0.375 | 0.241 | 0.297 (0.302 / 0.292) | 0.349 |
| refit matched on team lead (death, focus, farm) | 0.235 | 0.301 | 0.339 | 0.217 | 0.287 | 0.303 |
| refit matched on items held (death rate only) | 0.288 | 0.325 | 0.420 | 0.272 | 0.305 | 0.396 |
| ratios centred on their tier's mean | 0.294 | 0.334 (0.337 / 0.333) | 0.431 | 0.277 | 0.317 (0.322 / 0.312) | 0.405 |
| centred on slot and tier | 0.288 | 0.332 | 0.417 | 0.273 | 0.318 | 0.395 |
| shrinkage (empirical Bayes) instead of the z cutoff | 0.214 | 0.255 | 0.312 | 0.272 | 0.278 | 0.371 |
| tier-centred shrinkage, no cutoff | 0.265 | 0.280 | 0.363 | 0.264 | 0.278 | 0.357 |
| ratios from the item's peak-share budget | 0.270 | 0.304 | 0.371 | 0.251 | 0.291 | 0.341 |
| leftover items (share < half its peak): skipped | 0.2984 | 0.3337 (0.3362 / 0.3315) | 0.4378 | 0.2815 | 0.3277 (0.3338 / 0.3223) | 0.4161 |
| leftover items: deaths per minute | 0.289 | 0.326 | 0.422 | 0.270 | 0.315 | 0.395 |
| leftover items: lead-matched ratios | 0.286 | 0.326 | 0.417 | 0.262 | 0.316 | 0.383 |
| reference: no tier-1 ratios at all | 0.2990 | 0.3417 (0.3477 / 0.3362) | 0.4412 | 0.2776 | 0.3224 (0.3286 / 0.3168) | 0.4105 |
| reference: tier-1 ratios ^ 0.5 | 0.3003 | 0.3400 (0.3440 / 0.3363) | 0.4434 | 0.2849 | 0.3226 (0.3268 / 0.3190) | 0.4213 |

Every variant that takes the game state out of the ratios (lead or items held, peak budget, tier centring)
lowers sim_vs_win, most of all the lead refit, the right fix on the data. So the shipped holder ratios line up with
real win edges partly because both carry who is winning, not only what the item does. Skipping leftover items
is the only rule with a reason that lifts 37k within slot and tier on both hero halves (+0.012), but it lowers 37k
all pairs (0.285 -> 0.282) and 27k within (0.3341 -> 0.3337), so it fails the keep rule too.

## What is shipped

Tools only, no data or score change: `fit_fight_rate.py --match lead|items [--out FILE]` (default `none` rebuilds
the shipped tables) and `holder_controls.py`.

Lead: the holder ratios' agreement with win edges rides on team state that the score, which compares builds at an
equal game state, has no term for. The tier-1 overrating within tier 1 (Extra Charge, Monster Rounds, Close
Quarters) stays.
