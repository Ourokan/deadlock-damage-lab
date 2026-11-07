# Why replay-accurate fixes kept lowering sim_vs_win, and heal survival (2026-11-07)

Question: on 2026-11-06/07 several replay-backed fixes held split-half on the damage audit but lowered sim_vs_win, so
they shipped off: Mystic Reverb without its current-health echo term (PR #221), Healing Nova's real team heal x3.2
(#219), real kill heals (#225), per-hero gun lean (#228), Paige / Solomon ally casts (#224), Trophy Collector stacks
(#220). Is the check too noisy on the 5x smaller post-hotfix sample, is the damage -> win mapping off, or is
something compensating?

Setup: pools from post-hotfix builds 10-31..11-05 (`search/scripts/build_pool.py phantom`), sim_vs_win 27k + 37k
for main and for each fix (~27 min a run on 4 cores), compared with `analysis/scripts/sim_vs_win_compare.py`.

## 1. Not noise

Hero halves can't tell noise from signal for a change to one item: both halves share that item's all-hero edge (the
shrinkage prior). `sim_vs_win_compare.py --halves` rebuilds the edges from alternate days of the window (10-31,
11-02, 11-04 vs 11-01, 11-03, 11-05: independent matches; per-hero edges of the halves agree r 0.82) and scores
both. Every shelved drop repeats on both day halves (within slot and tier, Pearson):

| Fix | 27k shipped / day A / day B | 37k shipped / day A / day B | Spearman 27k / 37k |
|---|---|---|---|
| Nova team heal x3.23 | -0.038 / -0.031 / -0.032 | -0.026 / -0.020 / -0.021 | -0.002 / -0.001 |
| Reverb health term off (option A) | -0.0035 / -0.0046 / -0.0036 | -0.0037 / -0.0048 / -0.0038 | -0.004 / -0.005 |
| Real kill heals | -0.0017 / -0.0014 / -0.0017 | -0.0005 / +0.0002 / -0.0001 | -0.002 / -0.001 |
| Per-hero gun lean | +0.0003 / -0.0001 / +0.0005 | -0.0044 / -0.0034 / -0.0042 | +0.001 / -0.002 |

## 2. No single compensator: three different causes

- **Pearson leverage (Nova).** sim gains are heavy-tailed (kurtosis 7-9, the top 5% of gains carry a third of the
  correlation). Nova x3.2 makes the ten largest gains at 27k all Nova (real edges -1 to -3.6), so Pearson drops 0.03
  while on ranks (Spearman, what the score is used for) Nova was already top of its tier and the drop is -0.002.
  The team heal itself is real (`nova_heal.md`); what it buys teammates in wins is not measured.
- **Reverb's real edge is not its damage.** Sim T4 spirit ranking with the term: Reverb 1st (real edge +0.88, 2nd of
  the tier); without it 7th. Its kill weight is 0.71 (its damage is followed by kills less than the holder's other
  damage), so the 10% current-health term was standing in for value the duel doesn't model, not for damage.
- **Healing items' duel survival (the common cause for the heal fixes, fixed here).** See 3.

The damage elasticity is not the cause: lowering it to 0.3 leaves the Reverb drop (-0.003) and lowers Spearman.

## 3. Healing items' duel survival doesn't show in real deaths

`sim/scripts/fight_rate/survival_slope.py` (sim_vs_win rows now carry both builds' time alive, idx 17-18): per item,
the sim's log time-alive gain against real holders' log deaths / (kills + assists) ratio (post-hotfix
`holder_rates_2026-11-06.json`), 5+ heroes:

| | other items (125) | healing items (16, `HEAL_ITEMS`) |
|---|---|---|
| 27k all / even / odd match ids | -0.56 / -0.57 / -0.56 (sd 0.16) | +0.26 / +0.24 / +0.29 (sd 0.20) |
| 37k all / even / odd | -0.55 / -0.56 / -0.52 | +0.62 / +0.54 / +0.70 (sd 0.23) |
| real dealt ~ sim damage while alive | 0.50-0.51 | 0.05-0.10 |

Other items' duel survival shows up in real deaths; healing items' does not (holders don't die less per fight, as in
`heal_deaths.md`). Healing items are already left out of `death_rate_value`, but the duel's time alive was still
counted in full through damage before death. Removing the duel survival of every item instead loses 0.03-0.04: it is
right for the rest.

## Change

`overall_search.HEAL_SURVIVAL = 0.5`: each held healing item's time-alive gain on the popular build
(`Evaluator._heal_gain`: popular + item over popular, or popular over popular - item when it holds it; one extra
evaluation per healing item per evaluator) counts ^ HEAL_SURVIVAL instead of in full; damage while alive, map time,
team value and fight entry health stay. Lane trades unchanged. 1 = the old score. Detail rows: `heal_survival`.

Measured transfer is ~0 (clamped); the check (offline, killheal rows) by HEAL_SURVIVAL:

| k | 27k shipped / A / B | 37k shipped / A / B |
|---|---|---|
| 0 | +0.009 / -0.001 / +0.013 | -0.000 / -0.009 / +0.003 |
| 0.25 | +0.011 / +0.004 / +0.014 | +0.003 / -0.004 / +0.005 |
| 0.5 | +0.010 / +0.005 / +0.012 | +0.004 / -0.000 / +0.006 |
| 0.75 | +0.006 / +0.004 / +0.008 | +0.003 / +0.001 / +0.004 |

0.5 is the one that holds on every split; 0 loses at 37k on day half A.

## Full run (main vs HEAL_SURVIVAL 0.5), within slot and tier

| | Pearson (hero halves) | Spearman (hero halves) | all pairs |
|---|---|---|---|
| 27k shipped edges | 0.379 -> 0.390 (+0.011 / +0.011) | 0.358 -> 0.374 (+0.015 / +0.018) | 0.336 -> 0.349 |
| 27k day A / day B | +0.006 / +0.013 | +0.011 / +0.017 | |
| 37k shipped edges | 0.365 -> 0.369 (+0.003 / +0.004) | 0.380 -> 0.387 (+0.005 / +0.009) | 0.323 -> 0.328 |
| 37k day A / day B | -0.000 / +0.006 | +0.002 / +0.008 | |

## The shelved fixes after it

Still off. Kill heals stay slightly under (27k about -0.003, offline): they heal every build, not only healing items.
Nova x3.2 still -0.03 Pearson / -0.002 Spearman (team value, not survival). Reverb and per-hero gun lean are not
heal-related. Judge new fixes with `sim_vs_win_compare.py --halves` (day halves + Spearman) rather than one Pearson.
