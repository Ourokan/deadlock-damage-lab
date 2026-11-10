# Movement item values refit on post-hotfix games (2026-11-10)

`sim/data/movement_value.json` (the overall score's chase x escape multiplier per movement item) was a static
snapshot of patch 09-29 Phantom+ games (2026-09-30 to 10-13). The win blend and the win check both skip movement
items, so nothing checked it against real wins. It is now refit from the post-hotfix Phantom+ timelines
(`analysis/work/fight_rate_post`, 2026-10-31 to 11-06, 269,508 player rows, no KDA fetch):
`python3 analysis/scripts/kill_participation.py --post`.

| Item | old | new |
|---|---|---|
| Arcane Surge | 1.052 | 1.062 |
| Majestic Leap | 1.061 | 1.075 |
| Stalker | 1.063 | 1.034 |
| Warp Stone | 1.038 | 1.046 |
| Sprint Boots | 1.000 | 1.041 |
| Veil Walker | 1.025 | 1.041 |
| Fleetfoot | 1.019 | 1.036 |
| Kinetic Dash | 1.000 | 1.026 |
| Stamina Mastery | 1.019 | 1.021 |
| Enduring Speed | 1.032 | 1.018 |
| Ethereal Shift | 1.000 | 1.007 |
| Magic Carpet | 1.027 | 1.000 |
| Extra Stamina | 1.014 | 1.000 |

Stack caps 2: 1.078 -> 1.057, 3+: 1.120 -> 1.105. Mina's Mystic Expansion 1.044 -> 1.049.

## Check

`sim_vs_win.py --movement keep` (new flag: score movement items too; `--move-file` scores with another
movement_value.json) for old and new values, all heroes, 27k + 37k, then `sim_vs_win_raw.py` (raw day-half edges):

| split | old | new |
|---|---|---|
| 27k day half A | 0.1493 | 0.1508 (hero halves +0.0012 / +0.0018) |
| 37k day half A | 0.1434 | 0.1442 (+0.0012 / -0.0002) |
| 27k day half B | 0.1605 | 0.1638 (+0.0003 / +0.0067) |
| 37k day half B | 0.1654 | 0.1704 (+0.0053 / +0.0043) |

Shipped-edge check (movement items kept): all items 0.333 -> 0.335, clear edges 0.586 -> 0.593, per item
0.395 -> 0.402, within slot and tier 0.369 -> 0.367.

Rejected: escape measured per engagement (deaths / kills+assists, like DEATH_PER_KA) inflates every value
(Stalker 1.15, Majestic Leap 1.11) and lowers the raw check 0.013-0.016 in all four splits.

Not fixed: Arcane Surge's real edge is negative within spirit T2 on almost every hero (about -1 to -2 pt), yet its
real holders die 5% less at equal hero, net worth and game length (z 12), so its movement value went up, not down.
Its sim gain stays high from spirit power + range/duration in the duel. Movement items stay out of the win blend.
