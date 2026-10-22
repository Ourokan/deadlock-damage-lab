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
