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

`sim/scripts/team/team_value.py` puts each ally item on one hero of 40 random 3v3 lineups (popular builds, Phantom+
skills, both targeting modes, 12 and 20 m) and compares the item's swing with and without everything that reaches
teammates (`team_fight(allies=False)`). The team-only part, as a share of the holder's own damage, is scaled by the
real teammates in reach above, and the overall score is multiplied by 1 + the sum. Score factor per item:

| item | 10k | 18k | 27k | 37k | 50k |
|---|---|---|---|---|---|
| Divine Barrier | 1.32 | 1.18 | 1.19 | 1.17 | 1.11 |
| Healing Nova | 1.14 | 1.12 | 1.09 | 1.10 | 1.07 |
| Heroic Aura | 1.07 | 1.08 | 1.09 | 1.15 | 1.10 |
| Restorative Locket | 1.11 | 1.09 | 1.08 | 1.05 | 1.04 |
| Guardian Ward | 1.09 | 1.08 | 1.07 | 1.09 | 1.04 |
| Rescue Beam | 1.10 | 1.05 | 1.05 | 1.02 | 1.03 |
| Hunter's Aura | 1.01 | 1.01 | 1.01 | 1.01 | 1.00 |

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

Static snapshot like movement_value: rerun fit_team.py (positions, from the project's range_paths) and
team_value.py (~15 min on 4 cores) after big patches.
