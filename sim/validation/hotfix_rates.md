# Real item ratios after the 10-30 hotfix (2026-11-06)

The overall score's real holder ratios (sim/data/fight_rate.json: deaths per kills + assists for death_rate_value,
damage taken for focus_value, jungle souls for farm_value) were fitted on 74k Phantom+ matches from 09-30 to 10-24,
before the 10-30 hotfix changed 36 shop items. PR #215 moved the win check to post-hotfix pools and edges (new
baseline: sim_vs_win within slot and tier 27k 0.364, 37k 0.348). This thread refit the ratios on post-hotfix games.

Data: fetch_rates.py, 2026-10-31 to 11-06 18:00 UTC, 22,459 Phantom+ matches
(/mnt/project-files/analysis/work/fight_rate_post). Win edges were also rebuilt per match-id half (post-hotfix
Ritualist+ builds), so a refit can be checked with ratios from one half against edges from the other: ratios and
edges from the same games share their noise (players on winning teams die less), which a plain refit check rewards.

## sim_vs_win, within slot and tier (rows from post-hotfix pools, rescored offline)

| ratios | 27k | 27k ratios h0 / edges h1 | 27k h1 / h0 | 37k | 37k h0 / h1 | 37k h1 / h0 |
|---|---|---|---|---|---|---|
| shipped (pre-hotfix) | 0.3647 | 0.4239 | 0.3696 | 0.3475 | 0.4003 | 0.3544 |
| post-hotfix only | 0.3428 | 0.3710 | 0.3380 | 0.3371 | - | - |
| pre + post pooled, every item | 0.3630 | 0.4182 | 0.3742 | 0.3509 | - | - |
| hotfix items post only | 0.3699 | 0.4216 | 0.3569 | - | - | - |
| **hotfix items pre + post pooled** | **0.3675** | **0.4245** | **0.3722** | **0.3472** | **0.4007** | **0.3544** |

(Cross-half columns compare with the shipped ratios against the same edge half: 0.4239 / 0.3696 at 27k, 0.4003 /
0.3544 at 37k.) Post-hotfix only: a third of the matches, fewer items clear |z| >= 3, and every line drops. Pooling
every item lifts 37k but not 27k. Refreshing only the 36 changed items from the pooled fit raises 27k on both match
halves and both hero halves (0.3551 / 0.3755 -> 0.3578 / 0.3785) and leaves 37k flat (-0.0003, cross-half +0.0004 /
0.0000). Shipped: sim/scripts/fight_rate/hotfix_items.py writes fight_rate.json with those 36 items' entries from
the pooled fit (fight_rate.json "hotfix_items" lists them).

## Healing items and Surge of Power

These ratios can't move the healing items: they are in overall_search.HEAL_ITEMS, so death_rate_value and
focus_value skip them, and their jungle ratios are inside |z| < 3. Score parts at 27k (popular build + item / popular
build): Radiant Regeneration x1.044 (death, focus, farm x1.000; real edge -4.8), Healing Nova x1.144 (farm x0.992;
the rest is 3v3 team value; edge -2.3), Healing Booster x1.035 (edge -2.4). Surge of Power x1.022, of which death
rate x0.986 and focus x1.012; it was not changed by the hotfix, and its post-hotfix death ratio (1.011, z 1.2) is
inside the noise band, so it would only drop out with the post-only refit that lowers every line.

Ally heal (sim/data/ally_heal.json): Healing Nova's teammate healing in post-hotfix timelines (holder_rates
team_heal, holders minus non-holders) fell 337 -> 291 HP/min at 27k (-13%), and the 3v3's Nova ally heal with
current game data fell 1459 -> 1248 (-14%), so real / sim is unchanged and Nova's factor stays at its cap of 1. Not
refit (the replays behind it are pre-hotfix; rerunning only moves Locket 0.072 -> 0.068).

So the healing items' overrating is in the duel, sustain and team value parts, not in these real ratios.
