# Why our builds missed the pro top items (Night Shift #61)

Tyler, 2026-10-22: pro "Top items" (average purchases per game): Healing Booster 5.6, Radiant Regeneration 5.0,
Restorative Shot 4.2, Counterspell 3.6, Healbane 3.2, Tankbuster 3.2, Rebuttal 3.2, Dispel Magic 2.8,
Opening Rounds 2.4, Monster Rounds 2.4.

## Phantom+ ranked vs pros (player_builds 10-12..10-14, 85.8k Phantom+ players)

| Item | Phantom+ buy rate | per game (x12) | pros | median buy min | sold |
|---|---|---|---|---|---|
| Healing Booster | 22% | 2.6 | 5.6 | 12 | 10% |
| Radiant Regeneration | 16% | 1.9 | 5.0 | 9 | 1% |
| Restorative Shot | 15% | 1.9 | 4.2 | 1 | 60% |
| Counterspell | 9% | 1.1 | 3.6 | 22 | 3% |
| Healbane | 23% | 2.7 | 3.2 | 13 | 7% |
| Tankbuster | 28% | 3.4 | 3.2 | 21 | 1% |
| Rebuttal | 5% | 0.6 | 3.2 | 9 | 29% |
| Dispel Magic | 20% | 2.4 | 2.8 | 18 | 2% |
| Opening Rounds | 22% | 2.7 | 2.4 | 5 | 8% |
| Monster Rounds | 26% | 3.1 | 2.4 | 3 | 75% |

Pros buy about twice the healing ranked players do (and the chart shows Healing Booster +2.7 and Radiant +2.3 in one
week, so part of it is a fresh trend). Our best builds held almost none of them: in the live full game paths,
Healing Booster 2/42 heroes, Radiant 0/42, Healbane 0/42, Counterspell 0/42.

## What each item does in real games, and what the sim did with it

Real healing per source comes from the replay damage matrix (stat_type 1 heals, 5 regen, 2 heal prevented), 400
Phantom+ matches, sim/scripts/sustain/fit_sustain.py -> analysis/out/sustain_real.json.

- **Healing Booster** (+20% healing, +3 regen). Real: credited with 57 HP/min mid game (it amps everyone's biggest heal
  sources: medic trooper heal pickups 110-150 HP/min, base regen 60-80 HP/min). Sim: only amped the few heals inside
  one 30 s fight. **Gap: between-fight healing didn't exist.**
- **Radiant Regeneration** (heal 65 per cast, regen on spirit damage). Real: 345 HP/min mid, mostly from casting on
  creeps between fights. Sim: in-fight part only. **Same gap.**
- **Restorative Shot** (50 HP from a hero hit, 20 from NPCs, every 6 s). Real: 81 HP/min in lane. Sim: hero hits only.
  **Same gap.**
- **Healbane** (-35% enemy healing, 275 heal on kill). Real: prevents 38 HP/min and heals 38 HP/min per holder.
  Sim: the score was damage dealt to an immortal enemy, so enemy healing never mattered and no kill ever happened.
  **Worth only its 7 spirit power.**
- **Counterspell / Rebuttal**. Modeled (spell parry, parry heal + 30% damage), calibrated to Phantom+: holders log 4.8
  parries per 10 min (Counterspell) and 2.8 (Rebuttal) vs 1.2 for everyone, and Counterspell's spell parry heal fires
  ~0.2 times per 10 min. Pros time parries against key ultimates far better; not changed.
- **Dispel Magic**. Modeled (cleanses DoTs/silence/disarm, rank timing). Already picked when enemies bring debuffs.
- **Tankbuster**. Modeled (40 + 7.5% current HP, ignores resist, 14 s charge). Fine vs our pools; real buyers use
  it vs tanks, which the pooled enemy mix dilutes.
- **Opening Rounds**. Modeled vs heroes above 50%; its value on creeps/objectives (always above 50%) is not.
- **Monster Rounds**. Only its out-of-combat regen counts: NPC damage, NPC resist and the souls from farming faster
  are not in the sim (no souls economy).

## Fix (this PR)

1. **Net damage**: the overall and lane score subtract the healing the enemy got (healing undoes damage), so
   anti-heal and enemy lifesteal/regen count.
2. **Healbane kill heal**: a refill of the immortal enemy counts as a kill (engine.kill_hooks, survival._Refill).
3. **Fight entry health**: mid/late fights start at the real mean health at a hero-fight start (lane 84.5%, mid 91.4%,
   late 92.9%) for the popular build; a build that heals more in the real 20-25 s out of combat before a fight
   arrives fuller.
4. **Gap healing** (lane trades and fight entry): adds medic trooper heal pickups (amped by regen amp, so Healing
   Booster counts) and the real out-of-fight rate of farm-heal items (Radiant Regeneration, Mystic Regeneration,
   Restorative Shot, Healing Rite, Spirit/Bullet Lifesteal).
5. **Lane pressure**: both sides carry health between trades; an enemy forced to back (or killed) frees the rest of
   the lane, so out-sustaining or anti-healing a laner counts.

## Effect

Marginal value per 1000 souls (damage/scripts/item_probe.py, popular build + item, Haze/Infernus/Abrams/Seven):
Healbane x3-8 mid/late (e.g. Abrams 37k 0.010 -> 0.082), Healing Booster x2-3, Radiant Regeneration x1.5-2,
Restorative Shot x2-5, Extra Regen x5+ in mid/late.

Full game paths, same local pools (10-14 data), 4 heroes:
- before: Healbane 0/4, Healing Booster 0/4; regen only Extra Regen (Haze, Infernus lane)
- after: Healbane in 3/4 (Haze 27k+, Seven 37k+, Abrams 18k+), Healing Booster in Abrams 18k-37k, Fortitude in Haze,
  Spirit Lifesteal in Seven. Path scores vs popular rose (Haze 2.38 -> 2.83, Abrams 1.81 -> 2.12).
- Radiant Regeneration still isn't picked on these four (3200 souls; it competes with damage items at the same price).

## Still not modeled
Souls from farming and objective damage (Monster Rounds, Opening Rounds on creeps), team heals (Healing Booster on
ally heals), pro-level parry timing. Inputs are a static snapshot (sim/data/sustain.json); refit with
sim/scripts/sustain/fetch_sustain.py + fit_sustain.py after big patches.

## Calibration (2026-10-22, after the first rerun)

The first rerun put Healbane in 39 of 42 full game paths (vs ~23% of Phantom+ players) while Healing Booster,
Radiant Regeneration and Restorative Shot stayed rare. Two fixes:

- **Healbane at the real rate.** The sim prevented 6.45 HP of enemy healing per second alive (8 heroes x 18k/27k,
  sim/scripts/sustain/fit_healbane.py); real holders prevent 2.09 per second in hero combat (38 HP/min, 30% of time
  in combat). Its cut now runs at 0.324 of full strength in the overall score (Skill.item_landing["Healbane"],
  sustain.json healbane_landing), including the lane gap.
- **Heal trips saved.** The popular build makes the real ~2 heal trips per 10 min mid game (range_paths, living
  trips into base); field-heal items cut fountain healing by fountain_pass = 0.084 HP per HP/min they heal (matched
  holders vs non-holders, pooled over 9 items: Fortitude 43 HP/min less fountain, Healing Booster 22, Radiant 8...),
  more max health makes each trip go further, a trip costs 40 s (assumption). Score x time on the map. The pooled
  fit is weighted toward Radiant (largest heal); a holder-weighted mean of mid-game per-item ratios gives 0.069, so
  the pass-through is about 0.07-0.08; per-item ratios are too noisy to use alone (Restorative Shot -0.37).

Local paths (same pools, 4 heroes), main -> calibrated: Healbane 3/4 -> 0/4; Healing Booster (Abrams 18k-37k ->
Haze 37k-50k), Extra Regen in Haze 18k-27k, Restorative Shot in Abrams 18k-27k, Fortitude kept. Radiant
Regeneration still not picked on these four. Path scores ~unchanged (Haze 2.83, Infernus 2.02, Abrams 2.10,
Seven 1.80).

## Real healing data alignment (2026-10-24)

Healing items still showed up only mid game and Radiant Regeneration / Healing Booster were missing from final
builds. Cause: the damage matrix arrays are right-aligned (an item bought at 15 min has a shorter array that starts
at its first sample, sim/validation/README.md), but fit_sustain.py read them from the start. Late-game item healing
came out near 0 and mid-game rates were shifted. Corrected (Phantom+, 400 replays, HP/min while held):

| | before mid / late | after mid / late |
|---|---|---|
| Radiant Regeneration | 345 / 101 | 388 / 475 |
| Healing Booster (its amp) | 57 / 8 | 108 / 89 |
| Fortitude | 137 / 16 | 323 / 304 |
| Spirit Lifesteal | 69 / 9 | 153 / 184 |
| Healbane heal prevented per combat s | 2.09 | 3.33 (landing 0.324 -> 0.516) |

Late heal trips are now capped at the mid-game rate (late fountain healing is mostly defending next to it).
Also fixed: Celeste waited for 10% health lost before Dazzling Trick, so arriving at full health (healing items)
cost her the prism bounce on Shining Wonder; she now also casts it right before the ult (T3) and by 2.5 s.

Local full game paths, 12 heroes (the 8 with the most real Healing Booster / Radiant use + Haze, Infernus,
Abrams, Seven), heroes holding the item at 27k/37k/50k vs the real Phantom+ expectation for the same heroes:
Radiant Regeneration 0/0/0 -> 4/5/4 (real 4.5), Healing Booster 0/1/1 -> 1/1/1 (real ~6), Healbane 3/3/1 ->
1/3/3 (real ~4), Fortitude 4/4/3 -> 8/9/7 (real ~1), Spirit Lifesteal 5/4/6 -> 7/6/6 (real ~2).

Still off: Healing Booster is under-picked (ally heals it amps are not modeled in a 1v1) and Fortitude / lifesteal
are over-picked. Tried per-item fountain savings instead of the pooled pass-through: Fortitude went to 12/12 and
Radiant back to 0, so it was dropped.

## Balancing Fortitude, lifesteal and Healing Booster (2026-10-24)

Three causes of Fortitude / lifesteal / Radiant over-picks, all in the out-of-fight parts of the overall score:
- Heal trips scaled off the popular build's own fountain need. When the popular build already held field-heal
  items (Healing Booster + Radiant on Victor), its need was small, so the next item removed most of its trips
  (Fortitude x1.15 score from map time alone). Each HP/min saved now cuts the same share of the real fountain
  healing's trips, whatever the popular build holds.
- One pooled fountain pass-through credited lifesteal and Radiant with 4-5x the trip savings their real holders show.
  Each item now uses its own matched saving (holders vs non-holders, shrunk toward the pool): Fortitude ~59 HP/min,
  Healing Booster ~16, Spirit / Bullet Lifesteal 10-20, Radiant 24 mid / 42 late (was 50 / 61).
- Fight entry used the mean deficit (8.6% of max health) as if every fight started short. Real entries: half start
  full (sim/data/sustain.json entry_deficit_q). Extra gap healing now only fills the fights that start short, and
  is scaled so item holders gain what real holders gain (sim/scripts/sustain/fit_entry.py: mid 0.75, late 0.15,
  Fortitude's restore 0.6 / 1.95 of that; Fortitude +6.0 points at mid entry vs +6.0 real, was +8.1).

Overall search, 12 heroes (Victor, Celeste, Apollo, Rem, Kelvin, Yamato, Rat King, Venator, Haze, Drifter,
Infernus, Seven), heroes whose best build holds the item at 27k / 37k, before -> after, vs the real Phantom+
expectation for the same heroes (sum of each hero's holder share): Spirit Lifesteal 7/5 -> 5/3 (real 1.7/1.3),
Bullet Lifesteal 4/0 -> 1/0 (0.6/0.5), Fortitude 5/4 -> 6/3 (2.7/2.8), Healing Booster 4/3 -> 3/2 (5.0/4.8),
Radiant Regeneration 6/5 -> 0/0 (2.5/2.6), Healbane 3/3 -> 5/5 (3.6/3.6).

Still off: Healing Booster is under-picked although the 1v1 already credits it with more healing than real holders
get (its amp adds ~900 HP/min in sim fights vs at most ~350 real), so the missing value is outside the duel (ally
heals and team play). Radiant Regeneration was picked mostly for trip savings real holders don't show; its in-fight
healing matches real (~1060 vs ~1280 HP/min of combat).
