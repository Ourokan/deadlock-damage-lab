# Healing items over-rated: their holders die less without winning more (2026-10-27)

Question (follow-up of `ally_heal.md`): Healing Nova (sim gain rank 2 at 27k, real edge -0.41 pt), Mystic
Regeneration (rank 3, -0.37) and Radiant Regeneration (rank 14, -2.25, 2nd of spirit T3) still scored above their
tier's items that win more. Why?

## Where their sim gain came from

Popular 27k build + the item (Haze, Abrams): besides the duel's healing and the fight entry health, the real death
rate factor (`death_rate_value`) is a large part: Mystic Regeneration x1.019 of its x1.04, Radiant x1.032 of x1.13,
Nova x1.021 of x1.20. Real holders die less (fight_rate.json at 27k: Radiant 0.90, Nova 0.93, Mystic 0.94,
Locket 0.91, Rescue Beam 0.94), and the factor turns that into more time fighting.

## Fewer deaths don't go with wins for healing items

`sim/scripts/fight_rate/heal_deaths.py` on the 74k Phantom+ stat timelines (`holder_rates.py`): per item, the log
holder / non-holder death ratio against the item's mean real win edge.

| 27k | Other items (141) | Healing items (15) |
|---|---|---|
| All matches | -11.6 pt per log death ratio, r -0.39 | +7.8, r +0.35 |
| Even match ids | -11.6, r -0.39 | +7.1, r +0.31 |
| Odd match ids | -11.0, r -0.38 | +7.9, r +0.37 |
| 37k all matches | -10.3, r -0.34 | +7.5, r +0.33 |

For other items holders who die less win more, the basis of the death rate factor. For healing items it turns: the
healing items whose holders die least (Radiant, Rescue Beam) lose, while lifesteal holders die more (Spirit 1.05,
Bullet 1.06) and Spirit Lifesteal wins (+1.2). Nova holders also deal 0.83x the damage per minute of other Nova-hero
players (z -28): fewer deaths here look like backing off and healing up, not won fights.

## Change

`overall_search.HEAL_ITEMS` (Healing Nova, Mystic / Radiant Regeneration, Extra Regen, Fortitude, Restorative Locket,
Healing Booster, Spirit / Bullet Lifesteal, Restorative Shot, Healing Rite, Rescue Beam, Leech, Siphon Bullets,
Infuser: the items credited with self healing in the sustain replays) are left out of `death_rates` like movement
items. Their healing still counts in the duel, the fight entry health and map time. `HEAL_DEATHS = True` restores.

## sim_vs_win (blend off), all heroes, both halves by hero id parity

| | 27k before | 27k after | 37k before | 37k after |
|---|---|---|---|---|
| All pairs | 0.218 | 0.225 | 0.214 | 0.221 |
| Within slot and tier | 0.260 | 0.265 | 0.244 | 0.247 |
| Per item | 0.309 | 0.322 | 0.290 | 0.301 |
| Within, even / odd heroes | 0.2645 / 0.2549 | 0.2697 / 0.2590 | 0.2477 / 0.2406 | 0.2501 / 0.2444 |

Sim gain rank at 27k: Mystic Regeneration 3 -> 22, Radiant Regeneration 14 -> 37, Restorative Locket 12 -> 74,
Rescue Beam -> 94, Spirit Lifesteal 48 -> 17 (its death penalty is gone). 37k: Radiant 9 -> 33.

## Not changed: Healing Nova

Nova stays rank 3 (gain 0.055 -> 0.047): most of it is team value (x1.10), and its holders' teammates really die
4.9% less and join 3.3% more kills (`analysis/team_value.md`), its ally heal matches the 3v3 (`ally_heal.md`). Its
real edge is -0.41 +- 2.96 (17 Phantom+ replay holders, few buyers), so it is not measurably over-rated; dropping
its team value cut the within-tier correlation (0.260 -> 0.257).
