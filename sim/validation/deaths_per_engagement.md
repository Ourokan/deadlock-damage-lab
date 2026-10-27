# Deaths per engagement: real death ratios divided by kills + assists (2026-10-27)

Question: after today's score changes (farm value #162, spirit-build gun rate #165, Violet #167/#168, audit cover
#169), which items does the overall score still rank furthest from their real Phantom+ win edge within their slot
and tier, and why?

## Biggest gaps (27k, sim gain vs real edge, both centred within hero x slot x tier, in standard deviations)

| Sim under real | gap | Sim over real | gap |
|---|---|---|---|
| Golden Goose Egg (sign right: -15% damage, real holders deal 0.64x; size too big) | -3.9 | Decay | +2.0 |
| Rebuttal | -2.4 | Mystic Shot | +1.8 |
| Debuff Reducer | -2.2 | Capacitor | +1.8 |
| Superior Cooldown / Duration Extender / Compress Cooldown (explained, `cooldown_items.md`) | -1.7 to -1.3 | Melee Lifesteal | +1.7 |
| Counterspell, Slowing Bullets, Dispel Magic, Extended Magazine | -1.2 to -1.1 | Healing Rite, Disarming Hex, Rusted Barrel | +1.4 |

Match-id-parity hero halves agree on every row (odd / even within 0.4).

## Cause

Taking the score apart per factor (pure item multipliers, exact on the sim_vs_win rows): Rebuttal and Debuff Reducer
lose 4.9% and 3.3% from the real death rate and focus cost factors against +1.3% / +1.5% of damage; Extended
Magazine -2.3%. Real holders of these items die more per minute (Rebuttal 1.13, Debuff Reducer 1.04, Extended
Magazine 1.04), but they also get more kills + assists per minute: they are in more fights.

`death_rate_value` is written per engagement, (c + d_pop L) / (c + d L) with d = deaths per engagement, but d was
d_pop x the holders' deaths **per minute** ratio. An item whose holders fight more looks like it gets them killed,
and an item whose holders farm (fewer fights per minute) looks safe. The fix: each item's deaths ratio divided by
its kills + assists ratio (both already in `fight_rate.json`, same holders, same matching), i.e. deaths per
engagement, with kills + assists as the engagement count.

Engagement proxies tried (27k, within slot and tier): kills + assists 0.331, hero damage dealt 0.306, damage taken
0.282 (main 0.302, no death rate at all 0.246). Exponent on the ka ratio: 0.5 0.320, **1 0.331** (the per-engagement
form, kept), 1.5 0.337, 2 0.338. Healing items stay out (putting them back with the new ratio: 0.308).

## Results (sim_vs_win, blend off, all heroes; local pools from the shared 10-14 snapshots)

| | all pairs | damage items | within slot and tier | per item | within, hero halves | all, hero halves |
|---|---|---|---|---|---|---|
| 27k main | 0.256 | 0.169 | 0.302 | 0.371 | 0.307 / 0.297 | 0.276 / 0.239 |
| **27k deaths / ka** | **0.294** | **0.182** | **0.331** | **0.429** | **0.331 / 0.331** | **0.309 / 0.281** |
| 27k, ratios from even match ids only (holder_rates.py) | 0.296 | 0.177 | 0.333 | 0.431 | 0.331 / 0.335 | 0.310 / 0.284 |
| 27k, ratios from odd match ids only (holder_rates.py) | 0.291 | 0.188 | 0.328 | 0.424 | 0.329 / 0.326 | 0.307 / 0.276 |
| 37k main | 0.236 | 0.183 | 0.278 | 0.340 | 0.287 / 0.270 | 0.256 / 0.219 |
| **37k deaths / ka** | **0.281** | **0.204** | **0.311** | **0.408** | **0.312 / 0.310** | **0.293 / 0.271** |

Death ratios that move most (27k): Divine Barrier 0.87 -> 0.79, Diviner's Kevlar 0.90 -> 0.83, Heroic Aura
0.92 -> 0.86, Monster Rounds 0.99 -> 0.91, Extended Magazine 1.04 -> 0.98; Armor Piercer 1.07 -> 1.18, Glass Cannon /
Fury Trance 1.10 -> 1.18, Cultist Sacrifice 1.02 -> 1.11, Ballistic Enchantment 1.08 -> 1.13.
Rank by mean gain per 1000 souls (27k, of 141): Monster Rounds 97 -> 12, Extra Spirit 87 -> 22, Close Quarters
73 -> 10, Extended Magazine 138 -> 75, Extra Charge 37 -> 5; Cultist Sacrifice 107 -> 133, Ricochet 39 -> 63, Rapid
Recharge 75 -> 94, Glass Cannon 92 -> 107.

## Limits

Kills + assists per minute is an association like the death ratio itself: part of it is who buys the item, and
kills + assists also predict wins directly, so some of the gain may be that rather than the per-engagement
correction (on its own, a ka ^ 0.1 factor moves within slot and tier 0.302 -> 0.302, ka ^ 0.3 down to 0.290, so the
gain is not a plain ka bonus). Farm items' holders fight less per minute, so their death ratio now rises
(Ricochet, Cultist Sacrifice); the farm value factor still credits their souls.

## Not fixed

Full 27k run with the change reproduces the offline lines exactly. Gaps after it (z units, as above): Rebuttal
-2.4 -> -1.5, Debuff Reducer -2.2 -> -1.8, Extended Magazine -1.1 -> out of the list; Golden Goose Egg -3.9 -> -4.0.
Rebuttal (kills + assists only 1.02, still the score's 140th of 141 item by mean gain) and Debuff Reducer still lose
~3-5% to the death rate and focus cost while their real edges are near zero. Golden Goose Egg: rare at 27k (737
holder windows), real holders deal 0.64x and get 0.75x kills + assists, so its low sim value has the right sign.
