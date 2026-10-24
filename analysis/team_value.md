# Team value in the overall score (2026-10-24)

The real win check (analysis/out/build_win_check.md) found the overall search never picked items that win real
games: Heroic Aura, Mystic Reverb, Cheat Death, Magic Carpet. The overall score is a 1v1 (damage dealt before dying
against real enemy builds), so anything that reaches a teammate or a second enemy was worth nothing in it. This
change gives the sim itself a team part, fitted to real Phantom+ games.

## How many teammates and enemies are really close (fitted)

`sim/scripts/team/fit_team.py` reads 1 s positions of 400 Phantom+ matches (956k hero fight seconds, same fight
definition as the fight range fit) and writes `sim/data/team_value.json` "positions": per budget bin, the mean
number of teammates within R m of a fighting hero, the share of seconds with at least one, and the other enemies
within R m of its target or of itself. At 27k souls:

| radius | teammates within | any teammate | other enemies near the target | other enemies near me |
|---|---|---|---|---|
| 8 m | 0.25 | 0.21 | 0.14 | 0.04 |
| 16 m | 0.64 | 0.44 | 0.41 | 0.21 |
| 35 m | 1.54 | 0.74 | 1.16 | 0.90 |

12% of fight seconds are a true 1v1 (no one else within 40 m). Ricochet's 13 m bounce radius gives 0.30 other
enemies, close to the 0.23 bounces per hit measured from real Ricochet damage earlier (sim-mechanics).

## Area items

Damage that area items deal in the duel is also dealt to the real mean number of other enemies inside their area
(added to damage before dying): around the target Mystic Reverb (16 m, +0.41), Alchemical Fire (10 m, +0.20),
Capacitor (+0.20), Tesla Bullets (+0.14); around the holder Arctic Blast (+0.21), Scourge and Cold Front (+0.07),
Torment Pulse (+0.06). Ricochet and Split Shot now hit the other enemies through the duel's `extra_targets`
(Ricochet used to be worth 0 in the overall score). Hero abilities are unchanged: their landing factors were fitted
to real damage, which already counts every target hit.

## Ally items (3v3 team fights)

`sim/scripts/team/team_value.py` puts each ally item on one hero of 40 random 3v3 lineups (the overall search's popular Phantom+ builds, Phantom+
skills, both targeting modes, 12 and 20 m) and compares the item's swing with and without everything that reaches
teammates (`team_fight(allies=False)`). The team-only part, as a share of the holder's own damage, is scaled by the
real teammates in reach above, and the overall score is multiplied by 1 + the sum. Fits inside their 95% band count 0
(the search would chase lucky noise). Score factor per item:

| item | 10k | 18k | 27k | 37k | 50k |
|---|---|---|---|---|---|
| Divine Barrier | 1.40 | 1.20 | 1.17 | 1.12 | 1.00 |
| Healing Nova | 1.14 | 1.15 | 1.11 | 1.08 | 1.06 |
| Heroic Aura | 1.08 | 1.13 | 1.12 | 1.13 | 1.07 |
| Restorative Locket | 1.13 | 1.11 | 1.08 | 1.06 | 1.00 |
| Guardian Ward | 1.11 | 1.09 | 1.06 | 1.04 | 1.00 |
| Rescue Beam | 1.07 | 1.07 | 1.07 | 1.04 | 1.00 |
| Hunter's Aura | 1.00 | 1.02 | 1.01 | 1.00 | 1.00 |

Heroic Aura's passive (17% bullet resist to nearby teammates) was missing from the team fight sim and is added; it is
most of the item's team value (team-only 0.02 of the holder's damage without it, 0.12 with it at 27k).

## Checked against real games

Teammates of holders, matched on the holder's hero, net worth and game length (457k Phantom+ player-games,
2026-09-30 to 10-13):

| item | teammates' deaths / 10 min | teammates' kills+assists / 10 min |
|---|---|---|
| Divine Barrier | -4.6% | +5.0% |
| Healing Nova | -4.9% | +3.3% |
| Rescue Beam | -4.8% | +3.0% |
| Heroic Aura | -3.3% | +3.3% |
| Restorative Locket | -2.2% | +2.7% |
| Guardian Ward | -1.8% | +1.7% |
| Hunter's Aura | -0.4% | +1.2% |
| Cheat Death | +1.5% | -0.7% |
| Mystic Reverb | +1.3% | -1.8% |
| selfish items (Siphon, Boundless Spirit, Ricochet, Spirit Burn) | +2 to +3.5% | -1 to -5% |

The ally items the sim now values are the ones whose holders' teammates really die less and join more kills, in
about the same order (Hunter's Aura smallest). Holders of supports are a selected group, so the real numbers are a
direction check, not the fit. Cheat Death and Mystic Reverb show no teammate effect at all: they are not team items.

- **Cheat Death**: its holders die 3% less themselves (z 4.6) but join 1.3 points fewer kills, about the same as
  Magic Carpet. Its value is staying alive, which the duel already scores; its positive win edge stays in the
  score through the real win-edge blend.
- **Mystic Reverb**: real damage is 3.9x the sim's per gun damage (damage audit). Other enemies in its 16 m area
  explain 1.4x of that; the rest is the sim's trigger (one echo per hit of 100+ damage) under-firing, a follow-up.
- **Magic Carpet** is a movement item (already in movement_value) and has no team part.

Refresh: each patch rerun refits the ally item values (team_value.py on the new patch's popular Phantom+ builds,
~15 min on 4 cores, no API queries) in its data job and commits team_value.json with the results. The positions are a
static snapshot (the match paths live in the project files): rerun fit_team.py after a map change.

## Mystic Reverb fix (follow-up)

The sim read MaxHealthDamage (10%) as a cap on the echo; the game's label is "Current Health Bonus Damage", so the
echo is 50% of the triggering damage plus 10% of the target's current health. Imbued hits under MinimumDamage (100)
now add up until they reach it, so DoT and multi-hit imbues trigger it. Damage audit (600 Phantom+ matches): real /
sim Mystic Reverb damage per gun damage 3.80 -> 1.82; the 16 m area (x1.41 at 27k, in the overall score, not in
the 1v1 audit) leaves about 1.3. Infernus still imbues it on Napalm (highest listed damage), which rarely deals
100.
