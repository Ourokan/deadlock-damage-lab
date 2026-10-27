# Farm value: souls an item earns between fights (2026-10-27)

Question: after tonight's score changes (damage elasticity, Locket ally heal, healing items' death rates, focus
cost), which items does the overall score still rank furthest from their real win edge, and why?

## Biggest gaps (27k, sim gain vs real edge, both centred within hero x slot x tier, in standard deviations)

| Sim over real | gap | Sim under real | gap |
|---|---|---|---|
| Rusted Barrel | -2.2 | Golden Goose Egg (sim right in sign, too negative in size) | +4.6 |
| Decay | -2.1 | Rebuttal | +2.2 |
| Melee Lifesteal | -1.8 | Debuff Reducer | +2.0 |
| Disarming Hex | -1.8 | Superior Cooldown / Duration, Compress Cooldown (explained, `cooldown_items.md`) | +1.8 to +1.3 |
| Capacitor | -1.7 | Slowing Bullets (no real slow effect, `slow-items`) | +1.2 |
| Spirit Strike, Metal Skin, Split Shot | -1.7 to -1.4 | Counterspell, Ballistic Enchantment | +1.2 |

## What lines up with the misses

Every per-minute rate of real holders vs non-holders (`holder_rates.py` on the 74k Phantom+ timelines, same hero,
net worth and game time), centred within slot and tier across 130 items, against the per-item residual real edge
(edge - beta x sim gain), match-id halves alike:

| rate | r with residual (all / even / odd matches) |
|---|---|
| deaths | -0.26 / -0.24 / -0.27 (already in the score: death_rate_value) |
| kills + assists | +0.26 / +0.25 / +0.25 |
| jungle souls (souls from neutral camps) | +0.21 / +0.17 / +0.18 |
| boss damage | +0.23 / +0.20 / +0.18 |
| damage taken | -0.07 (already in: focus_value) |

As score factors (offline on sim_vs_win rows, exact for a pure item multiplier): kills + assists and boss damage
lift some lines and drop others or one hero half; total souls lifts within-tier but drops all pairs and per item
(lane souls go the other way); jungle souls lift every line on both hero halves and both match halves of the
ratios. Items holders clear camps fastest with: Ricochet 1.31, Escalating Exposure / Glass Cannon / Cultist
Sacrifice 1.11, Crushing Fists 1.10; slowest: Cursed Relic 0.88, Focus Lens 0.90, Decay / Rusted Barrel / Disarming
Hex 0.91 (27k). Single-target hero items farm slowly, so the over-rated counters and Decay get a real cost the duel
never saw. The score counted no farming at all (the old docstring listed it as not counted).

## The factor

`overall_search.farm_value`: the product of the held items' jungle ratios (`fight_rate.json` "jungle", now written
by `fit_fight_rate.py`; |z| >= 3, movement items left out, clamped like the death ratios) ^ FARM_GAMMA, over the
popular build's. FARM_GAMMA from the economy, not from wins: jungle souls ~220 / min at 20-36k net worth (15% of all
souls), ~8.7 min of game left (median), 1000 souls worth ~0.07 of the score (each hero's best next item, median
sim_vs_win gain), so an item farming x r adds ~0.13 (r - 1) by the game's end, ~half that averaged over the rest of
the game: gamma ~0.1.

## sim_vs_win (blend off, all heroes; local pools from the shared 10-14 snapshots)

| 27k | all | within slot and tier | per item | within, hero halves |
|---|---|---|---|---|
| main | 0.241 | 0.281 | 0.341 | 0.282 / 0.280 |
| gamma 0.05 | 0.246 | 0.288 | 0.349 | 0.288 / 0.287 |
| **gamma 0.1 (kept, full run)** | **0.250** | **0.294** | **0.356** | **0.294 / 0.293** |
| gamma 0.2 | 0.255 | 0.302 | 0.363 | 0.303 / 0.301 |
| gamma 0.3 | 0.256 | 0.305 | 0.361 | 0.306 / 0.303 |
| gamma 0.5 | 0.247 | 0.294 | 0.337 | 0.296 / 0.292 |

| 37k | all | within | per item | within, hero halves |
|---|---|---|---|---|
| main | 0.229 | 0.261 | 0.308 | 0.258 / 0.265 |
| **gamma 0.1** | **0.229** | **0.266** | **0.311** | **0.261 / 0.271** |
| gamma 0.2 | 0.223 | 0.264 | 0.303 | 0.257 / 0.270 |
| gamma 0.5 | 0.178 | 0.215 | 0.228 | 0.205 / 0.227 |

27k full run with the factor: damage items 0.145 -> 0.158, edges clear of noise 0.352 -> 0.378. Jungle ratios from
each match-id half alone give the same 27k lines within 0.003. 37k peaks at the economy-sized 0.1; 27k would take
more (the association is bigger than the souls are worth: who farms with these items rides along), not used.
Ranks (27k mean gain per 1000 souls): Rusted Barrel 75 -> 121, Disarming Hex 95 -> 105, Ricochet 77 -> 51,
Cultist Sacrifice 124 -> 111, Melee Lifesteal 4 -> 9; Decay 10 -> 11 and Heroic Aura 1 stay.

## Limits

The jungle ratio is a holder vs non-holder association, not a controlled item effect: the metric was picked
because it lines up with the win-edge misses, and part of it is who farms with these items and when (the sim_vs_win
gain keeps growing past the economy-sized weight at 27k). FARM_GAMMA 0.1 credits only the souls' worth, so most of
that association is left out; the 37k gain (+0.005 within) is small, and the rerun's build changes (Rusted Barrel,
Decay, Disarming Hex out of some builds) are where to look for side effects.

## Looked at, not changed

- Melee Lifesteal is credited with self healing in the sustain replays (71 HP/min, `upgrade_lifestrike_gauntlets`)
  but isn't in HEAL_ITEMS, so its low taken ratio lifts it through the focus cost. Adding it raises within-tier
  0.281 -> 0.288, but adding every lifesteal item the replays credit lowers it (0.275): no group rule, left alone.
- Rusted Barrel / Disarming Hex / Metal Skin: still under real after this; earlier threads put the rest on buy
  context (bought against fed gun heroes), which the score can't see.
