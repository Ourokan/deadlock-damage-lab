# Buy rate in the overall score (2026-11-07)

Question (follow-up of worst_heroes.md): McGinnis, Rat King, Haze and Venator rank items least like real wins because
the sim rates a few items high that their players almost never buy (Haze Split Shot, McGinnis Mystic Shot, Rat King
Spirit Strike). Does a per-hero real buy-rate factor, or shrinking low-sample pairs, make the overall score rank items
more like real wins at 27k and 37k, on both halves?

## Caveat: the shipped check is contaminated by buy shares

The shipped edges (analysis/out/hero_item_edge.json) shrink rare picks toward a prior that is lowered by their buy
share (build_win_check.rarity_fit, -1.7 pt per decade below 3%). Any score factor that uses buy shares then lines up
with those edges by construction: the buy factor below lifts the usual sim_vs_win within slot and tier from
0.392 -> 0.439 (27k) and 0.371 -> 0.422 (37k), and stronger factors lift it more until the score is all share. Those
numbers measure the prior, not the sim. Edges without the rare-pick prior go the other way (rare items get the
all-hero edge, which rarity_fit showed is too high for them), so they are biased against the factor.

The fair check is analysis/scripts/sim_vs_win_raw.py: raw (unshrunk) per-hero edges from alternate days of the
item_win_edge partials (10-31..11-05, day halves A/B), inverse-variance weighted, sim gain centred within hero,
budget, slot and tier. Nothing in a raw edge uses buy shares.

## Buy factor (shipped)

overall_search.buy_value: product over held items of min(1, share / BUY_KNEE) ^ BUY_GAMMA, share = the item's
holders / the hero's holders of same-slot same-tier items at the budget, from the bracket's pools (item_usage, so
Phantom+ for the site default), floor 0.1%, movement items left out, divided by the popular build's. BUY_KNEE 0.1,
BUY_GAMMA 0.003: an item no one buys loses 1.4% of score, one at 3% of its tier 0.4%.

Raw within slot and tier, base -> buy factor (rows from a full sim_vs_win run of the code; offline rescoring matched
it to 1e-4):

| | day half A | day half B |
|---|---|---|
| 27k | 0.1568 -> 0.1615 (+0.0047; hero halves +0.006 / +0.003) | 0.1742 -> 0.1777 (+0.0034; +0.005 / +0.002) |
| 37k | 0.1521 -> 0.1557 (+0.0037; +0.004 / +0.004) | 0.1754 -> 0.1792 (+0.0038; +0.006 / +0.002) |

Strength: gamma 0.001 +0.002 everywhere, 0.006 about the same as 0.003 (one hero half +0.0005), 0.01 falls on day half
B (-0.001, one hero half -0.005). Knee 0.03 at gamma 0.003 is about half the gain. Shares from day half A edges
crossed with day half B raw edges (and the reverse) gave the same picture as pool shares.

Worst pairs (score gain per 1000 souls): Haze Split Shot 0.119 -> 0.111, McGinnis Mystic Shot 0.056 -> 0.049, Rat King
Spirit Strike 0.051 -> 0.037 at 27k. They stay above their tier's mean: the factor is mild on purpose (Tyler:
damage efficiency is the main function), so it trims rare picks rather than removing them.

## Rare-pair shrinkage (not kept)

Shrinking the sim gain of rare pairs toward the item's mean gain over heroes (weight = decades of share below 3%,
up to 1 at 0.1%) lowers the raw check at 27k on both day halves (-0.001 to -0.006) and is mixed at 37k.

## New baseline

The usual sim_vs_win (shipped edges) now reads within slot and tier 0.439 (27k) / 0.422 (37k), all pairs 0.389,
clear edges 0.597, mostly through the rare-pick prior. Compare later changes against this new baseline, and check
any change that touches buy shares with sim_vs_win_raw.py.
