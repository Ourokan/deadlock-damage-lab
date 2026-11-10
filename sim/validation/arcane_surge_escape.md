# Arcane Surge: movement value without its escape part (2026-11-10)

Arcane Surge was in 50 of the Phantom+ best overall builds (the 11-09 rerun) while its real win edge within spirit T2
is -0.7 points (below 8 of the 11 other T2 spirit items) and negative on almost every hero.

## Where its sim value came from

`best_item_swaps` of those 50 builds: swapping Arcane Surge for the next-best item keeps the duel's damage before
death the same or raises it (damage^0.5 ratio 0.95-1.06, median ~0.98); the empowered cast's +20 spirit power and
+15% duration on one cast per fight add next to nothing. Its whole lead was `movement_value` 1.052 (now 1.062):
chase 1.010 (KP) x escape 1.052 (holders die 5% less at equal hero, net worth and game length, z 12; still 1.055
with the strata also split by the build's spirit share, so not a spirit-build play style).

## Check

`sim_vs_win.py --budgets 27000,37000 --movement keep` base, then `--movement only` per variant merged into the base
rows (merge reproduces the base exactly), `sim_vs_win_raw.py` (raw day-half edges, win_edge_week), raw within:

| variant | 27k A | 37k A | 27k B | 37k B |
|---|---|---|---|---|
| base (main) | 0.1509 | 0.1439 | 0.1641 | 0.1704 |
| **Arcane Surge chase only (1.0096)** | **+0.0019** | **+0.0027** | **+0.0077** | **+0.0069** |
| Arcane Surge on the deaths/ka price (1.036) | +0.0005 | +0.0007 | +0.0042 | +0.0035 |
| every movement item chase only | +0.0029 | +0.0053 | +0.0042 | +0.0046 |
| every item chase only except Arcane Surge | -0.0030 | -0.0006 | -0.0024 | -0.0031 |
| no movement value at all | +0.0029 | +0.0046 | +0.0031 | +0.0031 |
| movement items' deaths in death_rate_value + chase (MOVEMENT_RATES) | -0.0064 | -0.0025 | -0.0061 | -0.0048 |
| same, no chase | -0.0056 | -0.0022 | -0.0064 | -0.0051 |

Shipped: Arcane Surge chase only, all 8 hero halves up (+0.0004..+0.0108). The whole gain of the "all chase only"
variants is Arcane Surge's: dropping the others' escape lowers the check, so it is not a movement-wide effect (like
the healing items, whose holders die less without winning more, `HEAL_ITEMS` in overall_search.py).

`analysis/scripts/kill_participation.py` ESCAPE_OFF keeps it on refits (value_with_escape kept in the report json).
`overall_search.MOVEMENT_RATES` stays as an OFF opt-in (sim_vs_win reads SVW_MOVE_RATES=1).

Not changed: `stack_cap` (2 items 1.057, 3+ 1.105) is still measured on any movement items, Arcane Surge's escape
included. It only caps a build's product from above, and with Arcane Surge at 1.0096 a two-item build with it stays
under the cap unless the other item is above ~1.047 (only Majestic Leap, 1.075), so the effect is small.
`pipeline/smoke_test.py` checks that Arcane Surge stays under 1.02.
