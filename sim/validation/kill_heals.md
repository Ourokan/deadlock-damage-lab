# Items whose value depends on kills: Healbane kill heals, Siphon Bullets stacks (2026-11-07)

Follow-up of kill_stacks.md (Glass Cannon stacks shipped, Trophy Collector measured and left out). The sim's 1v1
fights have no other heroes to kill or die, so every item whose effect hangs on kills, assists or deaths was checked:

| item | kill / death effect | how the sim treats it | result |
|---|---|---|---|
| Glass Cannon | +fire rate, ammo per kill, -1 per death | real stacks by net worth (#220) | done |
| Trophy Collector | range, radius, souls per kill or assist | stacks measured, left out (#220); income credit hurt (ballistic_stacks.md) | no change |
| Healbane | heals HealOnKill when an enemy dies under its anti-heal | heal on the duel's own refills | measured below; boon scale fixed, real rate opt-in |
| Siphon Bullets | data still has StealPerKill 1, StackLostPerDeath 2 | temporary steal only | no permanent stacks in real games (below) |
| Cheat Death | survives a lethal hit | modeled; real holders' deaths in death_rate_value | no change |
| Golden Goose Egg | souls only while alive | income not modeled; income credit hurt twice | no change |
| Unstable Concoction, Eternal Gift | death / respawn time | legendaries, not in shop builds | no change |

## Healbane kill heals

Healbane heals its holder HealOnKill (170 + 3 per boon) whenever an enemy hero dies under its anti-heal, whoever
killed it. `sim/scripts/mechanics/kill_heals.py` fetched 800 post-hotfix Phantom+ matches with a holder (3,282
holders, ids from the fight_rate_post timelines, project folder analysis/work/kill_heals) and divides each holder's
Healbane self-heal per 180 s damage-matrix window by the boon-scaled heal at that net worth, per minute held and per
second of hero combat (sustain.json combat_share, the healbane_prevented_per_combat_s convention):

| net worth | kill heals / combat s | halves | per min held | HP/min | own kills/min | enemy deaths/min |
|---|---|---|---|---|---|---|
| 10-20k | 0.0166 | 0.0171 / 0.0162 | 0.30 | 70 | 0.19 | 1.21 |
| 20-30k | 0.0173 | 0.0168 / 0.0177 | 0.32 | 80 | 0.20 | 1.26 |
| 30-40k | 0.0186 | 0.0180 / 0.0192 | 0.37 | 95 | 0.23 | 1.43 |
| 40-50k | 0.0202 | 0.0200 / 0.0203 | 0.40 | 108 | 0.25 | 1.47 |

About a quarter of the enemy team's deaths heal the holder, and at least 38% of the heals are other players' kills
(heals 0.32 vs own kills 0.20 per minute). The sim's overall fights gave 0-13 HP of kill heal per fight (8 heroes,
27k / 37k, length-weighted): the immortal enemy's refill is the only kill, and it rarely comes early in a real-length
fight. With the real rate the same fights give 25-35 HP.

Two changes:
- the kill heal now scales with boons (`self.v("HealOnKill")`, scale_function_healing_boon_scale, as every other
  boon-scaled value); the handler read the bare 170. On, everywhere the refill heal fires.
- `Mechanics.kill_heals` (data/kill_heals.json): heals that real rate x HealOnKill through the fight in 0.5 s steps,
  with the refill heal off (the rate holds the holder's own kills). **Kept off.**

## Win check

sim_vs_win within slot and tier, hero halves (every other hero by id), pools 10-31..11-05, shipped edges:

| | 27k within | halves | 37k within | halves |
|---|---|---|---|---|
| main | 0.3842 | 0.3727 / 0.3972 | 0.3637 | 0.3565 / 0.3721 |
| boon-scaled kill heal | 0.3845 | 0.3731 / 0.3972 | 0.3640 | 0.3571 / 0.3720 |
| + real kill-heal rate | 0.3826 | 0.3703 / 0.3963 | 0.3628 | 0.3563 / 0.3705 |

The real rate lowers both budgets in both halves. Healbane's sim gain was already above its real edge (gap z +0.39 at
27k, +0.50 at 37k; real edge -0.35 / -0.32 pt) and the rate takes it to +0.46 / +0.60; and since about half the
heroes' popular builds hold Healbane, the extra heal on the popular build moves every other item's gain for them too.
The boon scale is a data fix and flat to slightly up (37k half B -0.0001), so it ships; the rate stays opt-in.

## Siphon Bullets

The item data still lists StealPerKill 1, StackLostPerDeath 2, MaxStacks 9999 (an older permanent max-health steal
per kill); the text says the steal is temporary. `sim/scripts/mechanics/siphon_kill_stacks.py` regresses max health
at each player's second-to-last snapshot (22.5k post-hotfix Phantom+ matches, 14,726 Siphon holders) on hero, net
worth, ability points, items' bonus health and kills / deaths / assists, plus kills / deaths / assists since the buy
for holders: +5.5 +- 0.9 HP per kill since the buy (halves +6.6 / +4.4), -1.7 +- 1.3 per death. A permanent stack
would be ~90 HP per kill and -180 per death, so live Siphon has no kill stacks and the sim (temporary steal only)
is right.
