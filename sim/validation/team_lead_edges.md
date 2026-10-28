# Team lead in the real item win edges and holder ratios (2026-10-28)

Question (follow-up of `tier1_death_rate.md`): late tier-1 holders' kills + assists edge is mostly their team's net
worth lead, and matching the holder ratios on the lead lowered sim_vs_win. Do the real win edges, which sim_vs_win
compares with, carry team lead too, and would lead-free edges be a fairer target?

**Result: no. The edges are already matched on the lead at the purchase and are the right target; every way of taking
more lead out of the edges or the holder ratios fits the sim worse. Nothing shipped but tools; the score is
unchanged.**

## The edges

`item_win_edge.py` matches every purchase on the team item-souls lead at the purchase (2,500-soul buckets), so the
win edges compare buyers at the same game state when they buy. `analysis/scripts/edge_lead_check.py` redoes the
Ritualist+ events (cache 09-30 to 10-14) with more lead keys. 156 items with >= 2,000 matched buyers, all-hero edge:

| Lead stratum | r vs shipped definition | spread of edges (sd) | mean change |
|---|---|---|---|
| none | 0.88 | 2.48 pt | 0.97 pt |
| at the purchase (shipped) | 1 | 1.49 pt | - |
| at the purchase, 1,000-soul buckets | 0.996 | 1.48 pt | 0.09 pt |
| 5 min after the purchase | 0.91 | 0.96 pt | 0.56 pt |
| 10 min after the purchase | 0.91 | 0.80 pt | 0.59 pt |
| at the purchase and 10 min after | 0.88 | 0.76 pt | 0.63 pt |

Without the lead stratum tier-3/4 items move most (Mercurial Magnum -1.4 -> -5.6, Ricochet -0.8 -> -4.7, Blood
Tribute +1.5 -> +6.2): who buys them when ahead or behind. Finer buckets change nothing, so the purchase-time
matching is complete. Matched on the lead after the purchase, half the spread goes: Blood Tribute, Witchmail, Lucky
Shot, Alchemical Fire lose 1-1.5 pt, Disarming Hex, Metal Skin, Golden Goose Egg, Decay gain 2.5-4: half of what an
item does for winning shows up as lead in the next 10 minutes.

## The holder ratios

`fit_fight_rate.py --match lead` vs the shipped tables, log ratio change by tier (37k; 27k the same shape, half the
size):

| Rate | r | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|---|
| deaths / kills + assists | 0.80 | +0.087 | +0.024 | +0.005 | -0.006 |
| kills + assists | 0.83 | -0.051 | -0.015 | -0.003 | +0.004 |
| damage taken (focus) | 0.98 | +0.017 | +0.004 | +0.001 | -0.001 |
| team damage share | 0.994 | +0.004 | +0.001 | 0 | -0.001 |
| jungle souls (farm) | 0.98 | -0.020 | -0.005 | -0.002 | 0 |

The lead is in kills + assists, so in the death / ka factor, and almost only for tier-1 items. Focus and farm barely
carry it. `--lead-lag S` matches on the lead S seconds before the interval: 600 s keeps a third of the tier-1 shift
(+0.025), 1,200 s none (+0.003). The lead the ratios carry was built in the last ~10 minutes, alongside the fights
the items are in.

## sim_vs_win against each

Rows from `sim_vs_win.py --out` at 27k / 37k (main, af89aa8), rescaled by `analysis/scripts/sim_vs_win_offline.py`
(exact: death rate, focus and farm are pure item multipliers). Within slot and tier with hero halves.

| Holder tables | Target edges | 27k all | 27k within (halves) | 27k item | 37k all | 37k within (halves) | 37k item |
|---|---|---|---|---|---|---|---|
| shipped | shipped (10-02 to 10-26) | 0.298 | 0.334 (0.328 / 0.341) | 0.437 | 0.285 | 0.316 (0.309 / 0.322) | 0.415 |
| shipped | cache, lead at purchase | 0.295 | 0.326 | 0.410 | 0.284 | 0.306 | 0.385 |
| shipped | cache, finer lead | 0.295 | 0.328 | 0.411 | 0.284 | 0.309 | 0.385 |
| shipped | cache, no lead | 0.224 | 0.232 | 0.307 | 0.208 | 0.217 | 0.276 |
| shipped | cache, lead 10 min after | 0.213 | 0.246 | 0.301 | 0.217 | 0.237 | 0.296 |
| shipped | cache, lead at and 10 min after | 0.222 | 0.256 | 0.318 | 0.219 | 0.240 | 0.307 |
| lead-matched | shipped | 0.235 | 0.301 | 0.339 | 0.217 | 0.287 | 0.302 |
| lead-matched | cache, lead at and 10 min after | 0.174 | 0.251 | 0.241 | 0.128 | 0.208 | 0.171 |
| lead 10 min earlier | shipped | 0.285 | 0.327 (0.321 / 0.334) | 0.417 | 0.269 | 0.310 (0.302 / 0.317) | 0.385 |
| lead 20 min earlier | shipped | 0.2983 | 0.3346 (0.3280 / 0.3411) | 0.439 | 0.2857 | 0.3188 (0.3127 / 0.3250) | 0.417 |

- Unmatched edges fit the sim far worse, so the lead the matching removes is game state the sim rightly ignores, and
  the edges don't need more of it removed.
- Edges matched on the lead after the purchase fit worse as well: the sim agrees with the part of an item's edge
  that becomes lead. That lead is the item's effect, not bias, so the after-purchase variants are not a fairer target.
- Lead-matched holder tables lose against every target, the lead-free pair included: matching on the concurrent lead
  takes out the items' own fights (over-control), not only the late tier-1 holders' team state.
- The lead 20 min earlier is a pre-purchase control for late items and changes the ratios by < 0.5%: +0.003 within
  37k on both halves but 27k all -0.0001. Within noise and fails the keep rule; not shipped.

## What is shipped

Tools only: `analysis/scripts/edge_lead_check.py` (event cache `analysis/work/edge_lead/` in the shared folder),
`analysis/scripts/sim_vs_win_offline.py` (target edges / holder tables swapped on saved sim_vs_win rows, seconds) and
`fit_fight_rate.py --lead-lag S`.

Lead: the shipped edges are the right target. The tier-1 death rate bonus stays an open item that needs a mechanism
(why low-farm players on teams ahead keep cheap items), not a different lead control.
