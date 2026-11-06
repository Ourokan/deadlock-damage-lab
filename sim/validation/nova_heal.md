# Healing Nova: what real casts give teammates (2026-11-06)

Question (loop follow-up of map_time.md): after #217, Healing Nova still ranks well above its real win edge
(post-hotfix gap z about +2), and most of its gain is 3v3 team value (x1.095 at 27k). ally_heal.py only says Nova's
real ally heal per minute sits at the median of the heal items, which has no absolute anchor. Does a real Nova cast
heal teammates less than the score credits (overheal, teammates who die anyway, out-of-fight casts)?

## Real casts (replays)

`sim/scripts/team/fetch_nova.py` ran one demo query per match on 132 post-hotfix Phantom+ matches with a Nova buy
(builds 10-31..11-05, replay salt present; raw in `/mnt/project-files/analysis/work/nova_heal/raw`, bulk metadata
timelines of the same matches in `timelines.jsonl.gz`). Replays have no heal events, so `nova_heal.py` reads heals
from pawn health: per cast and per living teammate, health change + health lost to damage over the 2.75 s heal, minus
the mean of the same over the 2.75 s before and after (lifesteal, regen and other heals in the fight). Positions at
the cast: world = cell x 512 + vec, Source units (inches).

| per cast (1,197 casts) | real | half A / B | 3v3 (team_value.py fights, 27k) |
|---|---|---|---|
| in a fight (hero damage within 4 s) | 0.92 | 0.92 / 0.92 | always |
| full heal on a deep-deficit target | 405 | 429 / 372 | |
| teammates in reach (18 m) | 1.16 | 1.18 / 1.14 | 2 (huddle), scored at 0.74 (positions) |
| ally heal received | 376 | 377 / 375 | 458 at 2 teammates = 170 at 0.74 |
| overheal in reach | 0.28 | 0.30 / 0.23 | 0.49 |
| ally heal on teammates dying within 10 s | 0.09 | 0.08 / 0.11 | 0.20 |
| self heal | 171 | 166 / 177 | 217 |

Heal received vs distance: 375-530 out to 16 m, about 0 past 32 m (the control windows work). Real players cast
Nova when teammates are near and hurt, so they reach more teammates per cast than the average fight second
(positions' 0.74 within 18 m) and waste less of it than the 3v3, which casts the moment anyone drops below half.

## Absolute anchor: ally heal per holder damage

Both sides per the holder's own hero damage in the same games (real: in-fight Nova ally heal over the held time /
player_damage over the held time, 132 holders, 0.52 casts per held minute; 3v3: ally heal / holder damage per fight):

- real 0.222 (halves 0.238 / 0.207)
- 3v3 0.185 at 2 teammates; what the score credits after the reach scaling: 0.185 x 0.74 / 2 = 0.069
- real / credited = **3.2** (3.4 / 3.0)

Self heal per own damage: real 0.106, overall-score duel 0.139 (12 heroes x 4 foes, 27k): 1.3x, small.

So Nova's team heal is not over-credited: real teammates get about 3x the heal the score gives them, fewer of
those HP are wasted on full or doomed teammates than in the 3v3, and 95% of it lands in fights.

## Win check

Pools 10-31..11-05 (local build_pool.py phantom), shipped edges; sim_vs_win within slot and tier (hero halves),
rescored offline (`analysis/scripts/sim_vs_win_team.py`, exact for a team value change):

| Nova team value | 27k within | halves | 37k within | halves |
|---|---|---|---|---|
| shipped (x1) | 0.3835 | 0.3777 / 0.3904 | 0.3508 | 0.3416 / 0.3616 |
| x3.2 (measured) | 0.3441 | 0.3430 / 0.3459 | 0.3168 | 0.3134 / 0.3210 |
| x0.5 | 0.3881 | 0.3813 / 0.3959 | 0.3546 | 0.3444 / 0.3666 |
| x0 | 0.3905 | 0.3829 / 0.3993 | 0.3565 | 0.3455 / 0.3695 |

The measured scale lowers the win check by 0.04 at both budgets and both halves. Cutting Nova's team value raises it,
but the replays say the opposite of a cut, so nothing is changed in the score: Nova's gap to its real edge (-2.3 pt
real, sim gain rank ~6) is not too much heal. The real heal is there; HP healed into teammates just doesn't turn into
wins the way the 3v3 swing assumes (same pattern as heal_deaths.md: healing items' real death ratios don't track
wins). A cut would be a fudge without a mechanism; left for Tyler to decide if wanted.

## Tools

- `sim/scripts/team/fetch_nova.py OUT IDS.json [workers]`: demo query per match (~1 min each, 2 x 4 workers ~90/h).
- `sim/scripts/team/nova_heal.py RAW [--half 0|1] [--sim] [--dist] [--write]`: real per-cast table, per-damage anchor
  (needs `timelines.jsonl.gz` next to RAW), `--sim` the instrumented 3v3, `--write` records the measured fields in
  `sim/data/ally_heal.json` (Healing Nova `measured_factor`; the applied `factor` is unchanged).
- `analysis/scripts/sim_vs_win_team.py ROWS "Healing Nova=k"`: exact offline team value rescoring of sim_vs_win rows.
