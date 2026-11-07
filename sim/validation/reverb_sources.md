# Where Mystic Reverb holders' extra damage comes from (2026-11-07)

Question: real Mystic Reverb holders deal 1.23x the hero damage per minute of non-holders at the same hero, net worth
and game time (holder_rates, 27k band), and a regression of real dealt ratios on the sim's damage gain across items
(slope ~0.75) left Reverb with the largest positive residual of any item. Which damage source does the sim
under-produce for holders?

Script: `scripts/fight_rate/source_holders.py SAMPLE --sim [--no-health-term]`. Sample: 1,500 fresh Phantom+ ranked
matches of the last 7 days (post-hotfix, `fetch_validation.py --api 91 7`, not committed). Unit = a player's 3-minute
damage-matrix interval at 20-50k net worth; Reverb held the whole interval or not at all; matched like
real_rates.py (hero, net worth // 2500, start time // 300 s), holder-weighted. The sim side runs one audit duel
(damage_audit's model: the player's real build, aim, real tiers and a real foe at the interval midpoint, expected
over real fight lengths, area extra hits) per interval, so real and sim compare the SAME builds. 1,979 holder
intervals over 16 heroes (Paradox 702, Yamato 357, Grey Talon 229).

## Holders / non-holders by source

| source | real | sim (main) | sim (health term off + refit, PR #221 option A) |
|---|---|---|---|
| gun | 0.81 | 0.77 | 0.77 |
| abilities | 1.04 | 1.01 | 1.01 |
| other items | 1.15 | 1.11 | 1.11 |
| melee | 0.58 | 0.85 | 0.86 |
| **total** | **1.21** (halves 1.22 / 1.25) | **1.27** (1.25 / 1.29) | **1.19** (1.18 / 1.22) |
| echoes, share of holders' damage | 16.6% | 21.9% | 17.1% |
| Reverb's own gain on holders' builds (sim, same duels without it) | | 1.27 | 1.20 |

- Every non-echo source moves the same way in real games and in the sim: holders' builds shoot less (gun 0.81 vs
  0.77) and get a little more from abilities and other items. The extra damage IS the echoes (~335 per minute real).
  Melee is the one mismatch (real 0.58 vs 0.85) but it is ~11 damage per minute, 0.5% of the total.
- The sim does not under-produce holders' damage. On their real builds main over-produces it (1.27 vs 1.21) because
  the current-health echo term makes echoes 21.9% of holders' damage vs 16.6% real. Option A of PR #221 (term off,
  pooled and per-hero Reverb factors refit) lands at 1.19 and 17.1%, on both match halves.
- Per hero the echo share under option A matches real far better than main: Paradox 0.191 real / 0.229 main / 0.191 A,
  Grey Talon 0.171 / 0.238 / 0.178, Yamato 0.150 / 0.172 / 0.175, Lash 0.154 / 0.233 / 0.159, Kelvin 0.162 / 0.318 /
  0.157, Lady Geist 0.135 / 0.226 / 0.142 (validation/reverb_sources_main.json, reverb_sources_option_a.json).
- The "largest residual" was the cross-item regression, not a missing source: the sim's gain for adding Reverb to the
  popular build is 1.27x at 27k (sim_vs_win rows), about the real 1.23x. Most items' real dealt ratios move only
  0.5-0.75x their sim gain (damage_elasticity.md); Reverb's moves about fully, so it sits above the line.

Reproducing: main = commit e4c9a7d. Option A = the same commit with Mystic Reverb's pooled and per-hero rows of
/mnt/project-files/sim/reverb_health_off/option_a.patch (item_landing.json) and its items_fx change
(CURRENT_HEALTH_BONUS False) applied; `--no-health-term` alone only drops the term (1.15x, echoes 13.8%, factors not refit).
The item's own source has no holders / non-holders ratio (non-holders' base is 0): see its holders' mean.

Conclusion: no damage source to add. On damage alone, option A reproduces Reverb holders' real damage and the term in
main overshoots it; option A's sim_vs_win cost (-0.004) is Reverb's real win edge, which damage does not explain
(reverb_nondamage / reverb_win_edge notes). No model change here.
