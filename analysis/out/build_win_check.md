# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-05, 42,632 Ritualist+ matches (refreshed 2026-11-06T19:50:00Z).

- Recommended item slots with data: 1956; mean edge +1.1 (popular builds +0.1); clearly positive 581, clearly negative 4.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 3 | Paige -1.6 |
| Kinetic Dash | weapon 2 | 1 | Warden -3.8 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 8 | Pocket +2.9, Drifter +2.5, Apollo +2.4, Deadman Danny +2.2, Celeste +2.2, Mina +2.2, Silver +2.2, Victor +1.9 |
| Spirit Burn | spirit 4 | 8 | Graves +2.4, Ivy +2.2, Mina +2.1, Vindicta +2.0, Sinclair +1.9, Bebop +1.7, Paige +1.7, Drifter +1.6 |
| Fleetfoot | weapon 2 | 6 | Haze +2.0, McGinnis +2.0, Vindicta +1.9, Drifter +1.9, Seven +1.7, Warden +1.5 |
| Sprint Boots | vitality 1 | 5 | Lady Geist +2.7, Kelvin +2.2, Abrams +1.6, Haze +1.6, Ivy +1.5 |
| Torment Pulse | spirit 3 | 5 | Victor +2.6, Warden +2.2, Mo & Krill +2.2, Celeste +2.1, Calico +1.7 |
| Colossus | vitality 4 | 4 | Yamato +3.0, Rat King +2.7, Warden +2.3, Billy +2.2 |
| Surge of Power | spirit 3 | 4 | Wraith +3.1, Warden +2.6, Violet +2.4, Haze +1.9 |
| Silencer | weapon 4 | 3 | Infernus +2.1, Drifter +1.7, Haze +1.6 |
| Lucky Shot | weapon 4 | 3 | Holliday +2.9, Haze +1.9, Venator +1.7 |
| Magic Carpet | spirit 4 | 3 | Lash +4.1, Solomon +3.3, Sinclair +2.4 |
| Duration Extender | spirit 2 | 2 | Abrams +1.9, Kelvin +1.6 |
| Extra Health | vitality 1 | 2 | Warden +2.0, Bebop +1.9 |
| Superior Cooldown | spirit 3 | 2 | Shiv +2.0, Bebop +1.5 |
| Grit | vitality 1 | 2 | Deadman Danny +2.5, Graves +1.6 |
| Mystic Burst | spirit 1 | 1 | Celeste +1.5 |
| Siphon Bullets | vitality 4 | 1 | Drifter +2.0 |
| Spirit Strike | spirit 1 | 1 | Drifter +1.6 |
| Recharging Rush | weapon 2 | 1 | Dynamo +2.6 |
| Cheat Death | vitality 4 | 1 | Dynamo +2.2 |
| Headshot Booster | weapon 1 | 1 | Dynamo +2.0 |
| Diviner's Kevlar | vitality 4 | 1 | Graves +2.4 |
| Rapid Recharge | spirit 3 | 1 | Haze +1.9 |
| Bullet Resist Shredder | spirit 2 | 1 | Holliday +1.8 |
| Mystic Expansion | spirit 1 | 1 | Kelvin +1.6 |
| Superior Duration | spirit 3 | 1 | Lady Geist +2.3 |
| Monster Rounds | weapon 1 | 1 | Seven +2.0 |
| Warp Stone | vitality 3 | 1 | Victor +1.8 |
| Lifestrike | vitality 3 | 1 | Viscous +1.9 |
| Glass Cannon | weapon 4 | 1 | Vyper +2.2 |
| Indomitable | vitality 4 | 1 | Wraith +1.7 |

## Per hero

### Abrams
- never picked: Duration Extender +1.9, Sprint Boots +1.6

### Apollo
- never picked: Ethereal Shift +2.4

### Baba

### Bebop
- never picked: Extra Health +1.9, Spirit Burn +1.7, Superior Cooldown +1.5

### Billy
- never picked: Colossus +2.2

### Calico
- never picked: Torment Pulse +1.7

### Celeste
- never picked: Ethereal Shift +2.2, Torment Pulse +2.1, Mystic Burst +1.5

### Deadman Danny
- never picked: Grit +2.5, Ethereal Shift +2.2

### Drifter
- never picked: Ethereal Shift +2.5, Siphon Bullets +2.0, Fleetfoot +1.9, Silencer +1.7, Spirit Burn +1.6, Spirit Strike +1.6

### Dynamo
- never picked: Recharging Rush +2.6, Cheat Death +2.2, Headshot Booster +2.0

### Graves
- never picked: Spirit Burn +2.4, Diviner's Kevlar +2.4, Grit +1.6

### Grey Talon

### Haze
- never picked: Fleetfoot +2.0, Rapid Recharge +1.9, Lucky Shot +1.9, Surge of Power +1.9, Sprint Boots +1.6, Silencer +1.6

### Holliday
- never picked: Lucky Shot +2.9, Bullet Resist Shredder +1.8

### Infernus
- never picked: Silencer +2.1

### Ivy
- never picked: Spirit Burn +2.2, Sprint Boots +1.5

### Kelvin
- never picked: Sprint Boots +2.2, Mystic Expansion +1.6, Duration Extender +1.6

### Lady Geist
- never picked: Sprint Boots +2.7, Superior Duration +2.3

### Lash
- never picked: Magic Carpet +4.1

### McGinnis
- never picked: Fleetfoot +2.0

### Mina
- never picked: Ethereal Shift +2.2, Spirit Burn +2.1

### Mirage

### Mo & Krill
- never picked: Torment Pulse +2.2

### Nurse Harrow

### Paige
- 18k: Arcane Surge -1.6
- 27k: Arcane Surge -1.6
- 37k: Arcane Surge -1.6
- never picked: Spirit Burn +1.7

### Paradox

### Pocket
- never picked: Ethereal Shift +2.9

### Rat King
- never picked: Colossus +2.7

### Rem

### Seven
- never picked: Monster Rounds +2.0, Fleetfoot +1.7

### Shiv
- never picked: Superior Cooldown +2.0

### Silver
- never picked: Ethereal Shift +2.2

### Sinclair
- never picked: Magic Carpet +2.4, Spirit Burn +1.9

### Solomon
- never picked: Magic Carpet +3.3

### The Doorman

### Venator
- never picked: Lucky Shot +1.7

### Victor
- never picked: Torment Pulse +2.6, Ethereal Shift +1.9, Warp Stone +1.8

### Vindicta
- never picked: Spirit Burn +2.0, Fleetfoot +1.9

### Violet
- never picked: Surge of Power +2.4

### Viscous
- never picked: Lifestrike +1.9

### Vyper
- never picked: Glass Cannon +2.2

### Warden
- 27k: Kinetic Dash -3.8
- never picked: Surge of Power +2.6, Colossus +2.3, Torment Pulse +2.2, Extra Health +2.0, Fleetfoot +1.5

### Wraith
- never picked: Surge of Power +3.1, Indomitable +1.7

### Yamato
- never picked: Colossus +3.0

