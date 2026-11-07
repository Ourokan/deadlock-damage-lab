# Kill stacks: Glass Cannon and Trophy Collector (2026-11-07)

Question (loop: items ranked furthest from their real win edge, post-hotfix pools 10-31..11-05, shipped edges):
which under-ranked items miss a real mechanism? Two items grow with kills, and the duel has no kills, so the sim gave
them their flat stats only (items_fx_extra listed "Glass Cannon stacks" as not modeled):

- Glass Cannon: +7% fire rate and +2 ammo per hero kill, a death takes one stack off (max 8). Sim gain per 1000
  souls 0.0045 at 27k, lowest of the T4 weapon items but Armor Piercer, real edge +0.66 pt (above the tier).
- Trophy Collector: +0.75% ability range and radius per kill or assist, kept through death (max 16), plus sprint and
  soul income. Second-largest "under" gap at 27k (z -1.24) after Golden Goose Egg.

## Real stacks

`sim/scripts/mechanics/kill_stacks.py` on the post-hotfix stat timelines (fight_rate_post, 10-31..11-06, 22.5k
Phantom+ matches): from the buy to the sale or match end, stacks follow kills, deaths and assists between snapshots,
weighted by the holder's hero damage in each interval, per net worth bin.

| net worth | Glass Cannon (3,949 holders) | halves | Trophy Collector (42,624) | halves |
|---|---|---|---|---|
| 10-20k | 0.36 | 0.34 / 0.38 | 4.70 | 4.69 / 4.71 |
| 20-30k | 0.58 | 0.62 / 0.54 | 8.95 | 8.96 / 8.95 |
| 30-40k | 0.98 | 1.01 / 0.95 | 12.62 | 12.61 / 12.63 |
| 40-50k | 1.53 | 1.60 / 1.44 | 14.63 | 14.66 / 14.60 |
| 50-60k | 2.04 | 2.07 / 2.02 | 15.43 | 15.42 / 15.43 |

Glass Cannon holders sit at about one stack (+7% fire rate) through the mid game: kills and deaths mostly cancel.
Trophy holders reach 9-13 stacks (+7-9% range and radius) by 27-37k.

`build.KILL_STACKS_BY_NW` holds these curves (bin centres, linear between); `compute_stats` adds the stacks' fire
rate and ammo (Glass Cannon) or ability range (Trophy Collector) at the build's net worth.

## Win check

sim_vs_win within slot and tier (hero halves), local pools and shipped edges. No popular build holds Glass Cannon,
so its rows alone change (spliced, exact); Trophy sits in 13-14 heroes' popular builds, so those were full reruns.

| | 27k within | halves | 37k within | halves |
|---|---|---|---|---|
| baseline | 0.3839 | 0.3724 / 0.3969 | 0.3631 | 0.3558 / 0.3716 |
| Glass Cannon stacks | 0.3842 | 0.3727 / 0.3972 | 0.3637 | 0.3565 / 0.3721 |
| + Trophy Collector stacks | 0.3853 | 0.3735 / 0.3984 | 0.3642 | **0.3550** / 0.3746 |

Glass Cannon: sim gain 0.0045 -> 0.0060 at 27k, up in both halves at both budgets: **shipped**.
Trophy Collector: its gap shrinks (27k z -1.24 -> -0.87, 37k -1.29 -> -0.74) and 27k rises in both halves, but 37k
falls in one half (and 37k all pairs 0.3207 -> 0.3194), so it is measured and left out of `KILL_STACK_ITEMS`.
Glass Cannon's Bullet Slow Proc (build-up) is still not modeled (slows show no measurable real value,
slow_items_value).
