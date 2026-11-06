# Post-hotfix builds window (2026-11-06)

The 10-30 hotfix changed 36 shop items (heal nerfs, Decay -55%, Toxic/Crippling -40%, lifesteal up) without a new
changelog entry, so the builds window stayed at the patch start (09-30). The Phantom+ pools (newest 14 days) mixed 8
pre-hotfix days with 6 post-hotfix ones, the real win edges pooled 10-02..11-04, and the local sim_vs_win check
still used pools from 10-14.

Change: patch.json `meta_start` = first day after a big hotfix (check_patch.BIG_HOTFIX_ITEMS = 10 shop items; the
11-05 hotfix changed 1 item + 19 abilities and doesn't count). Once it has 3 full days (patch_state.META_MIN_DAYS)
patch_state.build_days starts there, so build_pool, refresh_win_edge and the 7/14-day marks use post-hotfix games
only. Set to 2026-10-31 by hand for the 10-30 hotfix.

## What moved

Popular Phantom+ builds, 10-14 pools vs 10-31..11-04 (27k and 37k): 22% of items changed. Added most: Healbane
(20 builds), Battle Vest, Extra Regen, Tankbuster, Spirit Resilience. Dropped most: Healing Booster (13), Monster
Rounds, Sharpshooter, Radiant Regeneration, Arcane Surge.

Real edges, post-hotfix 10-31..11-05 (42.6k Ritualist+ matches) vs shipped (10-02..11-04, 231k), mean over heroes:
Radiant Regeneration -2.3 -> -4.5 pt, Mystic Regen -0.5 -> -2.1, Healing Booster -0.9 -> -2.1, Healing Nova -0.9 ->
-2.0, Guardian Ward -0.4 -> -2.0; Surge of Power -2.2 -> +0.8, Healbane -0.7 -> +0.2, Decay -4.1 -> -2.7, Opening
Rounds -1.1 -> 0.0. Heroic Aura +2.1 -> +2.2 (unchanged).

## sim_vs_win (Pearson, within slot and tier / all pairs / clear edges)

| pools | edges | 27k within | 37k within | 27k all | 27k clear (n) |
|---|---|---|---|---|---|
| 10-14 | shipped 10-02..11-04 | 0.383 | 0.357 | 0.330 | 0.452 (1644) |
| 10-31..11-04 | shipped | 0.379 | 0.360 | 0.342 | 0.462 (1636) |
| 10-14 | post-hotfix | 0.372 | 0.342 | 0.323 | 0.598 (608) |
| 10-31..11-04 | post-hotfix | **0.364** | **0.348** | 0.327 | 0.595 (608) |

Fresh pools alone: flat. Post-hotfix edges: within -0.015 / -0.012, but clear edges r 0.45 -> 0.60. The edges come
from 5x fewer matches, so a third as many clear the noise band and all-pair correlations fall from noise alone;
the score's real-data factors (death, focus, farm ratios in fight_rate.json) were also fitted on pre-hotfix games.
New baseline for later threads: the last row.

Item gaps (per-item z of mean sim gain minus z of mean edge), post-hotfix edges: sim over Disarming Hex +2.5,
Healing Nova +2.4, Arctic Blast +2.3, Express Shot +2.2, Radiant Regeneration +2.2 (was +0.6), Metal Skin,
Spirit Shielding, Capacitor +2.1, Heroic Aura +1.9 (was +2.0: real edge high too, sim ranks it top), Healing
Booster +0.9 (was +0.2), Decay +2.1 (was +3.2); sim under Golden Goose Egg -3.9, Glass Cannon -1.9, Trophy
Collector -1.8, Lucky Shot, Extra Health, Surge of Power -1.5 (was +0.2).
