# Gun time by build, per hero (2026-11-07, opt-in, off)

Question: Mechanics.gun_lean slows every hero's gun by one curve, exp(-0.028 x spirit item souls / 1000). The Ivy
work (PR #222) found her leftover gap depends on the build: gun Ivys shoot more than the sim, spirit Ivys less. Does
the single curve miss real gun-vs-spirit shooting per hero?

Data: fresh 4,000-match Phantom+ sample (2026-11-06, 43k player-matches; API damage series, so the post-11-05 replay
gap does not touch it). `scripts/gun_calib/gun_build.py --sample ... --dump PATH` (~13 min on 4 cores).

Measure: within hero and match frac (30/60/90%), players split at the median spirit item souls; slope = change of
real minus sim log odds of the gun share from the low to the high half, per 1000 spirit souls.

- Pooled over heroes the curve is right (rows-weighted mean slope 0.000), but per hero the slopes are real: the two
  halves of the matches (even/odd ids) agree, r 0.61. Rows-weighted mean |slope| 0.0245 / 0.0193 (even / odd).
- Shoot less on spirit builds than the curve: McGinnis (-0.11 / -0.08), Nurse, Ivy, Holliday, Grey Talon, Bebop,
  Kelvin, Doorman. Keep shooting: Silver (+0.08 / +0.07), Baba, Mo & Krill, Viscous, Seven, Violet, Warden.

Fix tried: `Mechanics.gun_lean_hero`, per hero k = 0.028 - slope x n / (n + 1000) (clipped 0..0.1), applied around
the hero's center (mean spirit item souls in the sample) so the hero's average gun time stays put
(`mechanics.gun_uptime`, at most 1). Data: data/gun_lean_hero.json (`gun_build.py --fit-hero DUMP OUT`).

- First version without the center moved heroes' average gun time (McGinnis 0.19 -> 0.15 vs real 0.18): whole-match
  audit 0.0191 -> 0.0198. Dropped for the centered one.
- Split-half (fit on one half, gun_build on the other): |slope| 0.0193 -> 0.0156 and 0.0245 -> 0.0217, 29-30 of 44
  heroes better. Whole-match damage audit on the fresh sample 0.0191 -> 0.0191.
- sim_vs_win (post-hotfix pools, 27k + 37k, both runs same pools/edges):

| budget | hero half | all | within slot and tier |
|---|---|---|---|
| 27k | even | 0.334 -> 0.326 | 0.381 -> 0.380 |
| 27k | odd | 0.351 -> 0.352 | 0.385 -> 0.388 |
| 37k | even | 0.311 -> 0.299 | 0.358 -> 0.352 |
| 37k | odd | 0.329 -> 0.318 | 0.368 -> 0.365 |

37k drops in both halves, so the mechanic ships OFF (no score change, no rerun). Per-hero within changes are mixed
(Seven -0.030, Mirage -0.016 ... Danny +0.017, Haze +0.013), no clean subset.

Left: the build split is real in the damage mix but steering the gun by it makes late item ranking worse; the gap
may be what gun-build players do besides shooting longer (positions, targets), not gun time itself.
