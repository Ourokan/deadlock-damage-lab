# Damage items over-rated within their tier: damage elasticity (2026-10-27)

Question (follow-up of `cooldown_items.md`): within a slot and tier the overall score ranks damage items (spirit T3
Decay, Spirit Snatch, Tankbuster) far above their real win edge. Why?

## Real holders' damage moves half as much as the sim's

Per item, the sim's damage gain (log of damage before death with the item over the popular build's, mean over heroes,
`analysis/scripts/sim_vs_win.py --out`) against real holders' hero damage per minute over matched non-holders (log
ratio, `sim/scripts/fight_rate/holder_rates.py` on the 74k Phantom+ stat timelines, same hero, net worth and game
time). Least squares over 141 items (`sim/scripts/fight_rate/damage_slope.py`):

| Budget | Slope | Even / odd match ids |
|---|---|---|
| 27k | 0.51 | 0.52 / 0.51 |
| 37k | 0.45 | 0.44 / 0.47 |

A build whose duel damage is 20% higher has real holders dealing ~10% more per minute. The score counted the full
20%, while its real-data factors (death rate, team value, movement, map time) are measured at real size, so damage
items outscored same-tier items whose value sits in those factors.

## Change

`overall_search.DAMAGE_ELASTICITY = 0.5`: the score counts (damage before death / the popular build's) ^ 0.5, the
other factors as before. Damage numbers on the site are unchanged; only the ranking moves. The "Why it's here" tab
reports damage's share of a score change at the same power.

## sim_vs_win (blend off), all heroes

| | 27k before | 27k after | 37k before | 37k after |
|---|---|---|---|---|
| All pairs | 0.180 | 0.217 | 0.183 | 0.218 |
| Within slot and tier | 0.220 | 0.258 | 0.209 | 0.244 |
| Damage items | 0.083 | 0.114 | 0.109 | 0.140 |
| Edges clear of noise | 0.275 | 0.316 | | 0.289 |
| Per item | 0.258 | 0.306 | 0.236 | 0.291 |

Split by hero id parity both halves improve at both budgets (27k within-tier 0.226 / 0.213 -> 0.261 / 0.254).
The win correlation peaks lower (0.3-0.4), but 0.5 is the measured real response, not a value fitted to the wins.

## Overall builds, 8 heroes at 27k (blend on)

Haze, Vindicta, Lash, Seven, Bebop, Abrams, Pocket, Wraith: mean real edge of the held items +1.38 -> +1.62 points
(up on 4, down on 4), damage before dying -18% (Abrams 1351 -> 871, below the popular build's 1086). Out: Headhunter
(4 of 8), Spirit Strike, Mystic Shot, Titanic Magazine, Melee Charge; in: Restorative Locket (4), Frenzy, Healing Nova,
Stalker. Restorative Locket now leads the sim gain list with a ~0 real edge: a follow-up for its value.
