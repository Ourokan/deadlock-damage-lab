# Restorative Locket over-rated: real holders heal themselves, not teammates (2026-10-27)

Question (follow-up of `damage_elasticity.md`): after the damage elasticity change Restorative Locket had the top
mean sim gain per 1000 souls (+0.077 at 27k, 42 heroes) with a ~0 real win edge (-0.08 pt). Why?

## Where the sim gain came from

Popular 27k build + Locket (`overall_search.Evaluator` detail, Haze / Abrams / Seven / Kelvin / Lash / Wraith): score
x1.10-1.14, of which team value x1.07 (the 3v3 fit's ally heal), real death rate x1.03, damage before death x1.01-1.03.
Team value was the largest part.

## Real ally healing

`sim/scripts/team/ally_heal.py`: heals credited to the item in the damage matrix of 400 Phantom+ replays
(`fetch_sustain.py`), to the holder vs anyone else, after 9 min while held; against the 3v3 team_value.py fights
(27k popular builds) per fight minute.

| Item | Real self HP/min | Real ally HP/min | Sim ally HP / fight min | Real / sim | Factor |
|---|---|---|---|---|---|
| Healing Nova | 106 | 220 | 1459 | 0.151 | 1 |
| Rescue Beam | 84 | 132 | 926 | 0.142 | 1 |
| Restorative Locket | 118 | 6 | 623 | 0.010 | 0.07 |

The 3v3 heals the neediest teammate whenever the item is ready, and Nova and Rescue Beam holders really heal
teammates at the same rate relative to the sim. Locket holders use it on themselves: the 3v3 heals teammates 2.5x more
than the holder, real holders 0.05x. The 74k-match stat timelines agree (`holder_rates.py` on fight_rate_ext, 27k):
holders' team heal +14 HP/min (x1.18 of 79), Nova +337, Rescue Beam +191.

## Change

`overall_search.team_value` multiplies each heal item's team value by its factor (real / sim ally heal over the other
heal items', `sim/data/ally_heal.json`, `ALLY_HEAL`): Locket's team value x1.07 -> x1.005. Its self heal stays in the
duel. Barrier and aura items (Divine Barrier, Guardian Ward, Heroic Aura) have no heal data and keep theirs; their ally
shares can't be read from the heal matrix.

## sim_vs_win at 27k (blend off), all heroes

| | Before | After |
|---|---|---|
| All pairs | 0.219 | 0.219 |
| Within slot and tier | 0.258 | 0.260 |
| Per item | 0.307 | 0.309 |
| Within (hero-id halves, cost groups) | 0.2781 / 0.2724 | 0.2816 / 0.2738 |
| Locket's sim gain rank | 1 | 12 |

## Not changed: Locket's self heal (opt-in)

Real stacks persist between fights, and real holders heal themselves 118 HP/min (Nova 106), while the duel, stacking
from one enemy's casts only, heals ~24 per fight to Nova's 120-160. `items_fx.LOCKET_ENTRY_STACKS = 12` matches Nova's
ratio (Locket 124-165 per fight), but sim_vs_win doesn't move (halves 0.2822 / 0.2732, Locket rank 9), so it stays 0.

Other heal items: Healing Nova (rank 3, -0.41 pt) and Radiant Regeneration (-2.25 pt) are the next over-rated
sustain items; Nova's ally heal matches real, so its gap is elsewhere (follow-up).
