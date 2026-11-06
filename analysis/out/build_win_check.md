# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-11-04, 231,046 Ritualist+ matches (refreshed 2026-11-06T12:44:02Z).

- Recommended item slots with data: 1989; mean edge +1.7 (popular builds +0.1); clearly positive 1514, clearly negative 23.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 10 | Lash -2.3, McGinnis -1.4, Dynamo -1.2, Paige -0.7 |
| Stalker | weapon 2 | 8 | Calico -2.4, Billy -1.2 |
| Spirit Snatch | spirit 3 | 3 | Apollo -0.9 |
| Kinetic Dash | weapon 2 | 1 | Deadman Danny -4.4 |
| Extra Regen | vitality 1 | 1 | Seven -1.2 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 11 | Paradox +4.4, Pocket +2.9, Silver +2.6, Mina +2.5, Violet +2.3, Deadman Danny +1.9, Celeste +1.8, Apollo +1.8, Drifter +1.7, Shiv +1.7, Victor +1.7 |
| Fleetfoot | weapon 2 | 11 | Baba +4.6, Kelvin +2.3, Seven +2.3, Vyper +2.3, Infernus +2.2, Vindicta +1.8, Rat King +1.6, Haze +1.6, Venator +1.6, Warden +1.5, McGinnis +1.5 |
| Duration Extender | spirit 2 | 8 | Rat King +3.4, Baba +2.4, Silver +2.4, Vindicta +2.2, Violet +2.1, Drifter +1.7, Kelvin +1.7, McGinnis +1.5 |
| Sprint Boots | vitality 1 | 7 | Victor +3.5, Lady Geist +2.9, Kelvin +2.3, Venator +1.7, Wraith +1.7, Infernus +1.6, Vindicta +1.6 |
| Colossus | vitality 4 | 6 | Viscous +2.5, Rat King +2.5, Bebop +2.4, Calico +2.2, Yamato +2.0, Billy +1.9 |
| Mystic Expansion | spirit 1 | 5 | Baba +2.5, Dynamo +1.9, Billy +1.8, Kelvin +1.8, Sinclair +1.6 |
| Magic Carpet | spirit 4 | 5 | Lash +5.9, Solomon +4.1, Sinclair +3.2, Rem +3.1, Graves +2.7 |
| Witchmail | vitality 4 | 4 | Kelvin +2.5, Mo & Krill +2.3, Violet +2.0, Bebop +1.7 |
| Silencer | weapon 4 | 4 | Infernus +3.0, Wraith +2.6, Lady Geist +2.1, Haze +1.9 |
| Scourge | spirit 4 | 4 | Paige +3.4, Victor +2.4, Nurse Harrow +2.0, Rem +1.8 |
| Slowing Bullets | weapon 2 | 3 | Warden +2.2, Rat King +1.9, Bebop +1.6 |
| Spirit Burn | spirit 4 | 3 | Mina +1.8, Bebop +1.6, Ivy +1.5 |
| Enduring Speed | vitality 2 | 3 | Lady Geist +1.8, Billy +1.7, Haze +1.5 |
| Lucky Shot | weapon 4 | 3 | Calico +2.4, Holliday +2.3, Haze +1.7 |
| Grit | vitality 1 | 3 | Rat King +2.9, Deadman Danny +1.9, Graves +1.7 |
| Frenzy | weapon 4 | 3 | Lady Geist +2.5, Drifter +1.8, Rat King +1.6 |
| Dispel Magic | vitality 3 | 3 | Graves +1.7, Ivy +1.6, Rat King +1.5 |
| Siphon Bullets | vitality 4 | 3 | Victor +2.2, Lash +2.2, Graves +1.6 |
| Debuff Reducer | vitality 2 | 2 | Mo & Krill +1.6, Bebop +1.5 |
| Healing Tempo | vitality 4 | 2 | Dynamo +1.8, McGinnis +1.7 |
| Warp Stone | vitality 3 | 2 | Victor +2.4, Infernus +1.8 |
| Spellslinger | weapon 4 | 2 | Wraith +2.3, Venator +1.9 |
| Refresher | spirit 4 | 2 | Yamato +2.2, Victor +1.6 |
| Bullet Resilience | vitality 3 | 1 | Baba +2.8 |
| Crushing Fists | weapon 4 | 1 | Bebop +1.7 |
| Reactive Barrier | vitality 2 | 1 | Calico +1.6 |
| Hollow Point | weapon 3 | 1 | Deadman Danny +2.0 |
| Compress Cooldown | spirit 2 | 1 | Deadman Danny +1.8 |
| Long Range | weapon 2 | 1 | Deadman Danny +1.5 |
| Cheat Death | vitality 4 | 1 | Dynamo +2.0 |
| Indomitable | vitality 4 | 1 | Dynamo +1.8 |
| Diviner's Kevlar | vitality 4 | 1 | Graves +2.0 |
| Spiritual Overflow | weapon 4 | 1 | Graves +1.6 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.9 |
| Stamina Mastery | vitality 3 | 1 | McGinnis +2.1 |
| Boundless Spirit | spirit 4 | 1 | McGinnis +1.8 |
| Glass Cannon | weapon 4 | 1 | Paradox +1.7 |
| Extra Stamina | vitality 1 | 1 | Rat King +3.3 |
| Arcane Surge | spirit 2 | 1 | Rat King +3.2 |
| Monster Rounds | weapon 1 | 1 | Seven +1.7 |
| Lightning Scroll | spirit 4 | 1 | Seven +1.6 |
| Phantom Strike | vitality 4 | 1 | Silver +1.9 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.4 |
| Mystic Reverb | spirit 4 | 1 | Violet +3.2 |
| Point Blank | weapon 3 | 1 | Viscous +1.7 |

## Per hero

### Abrams

### Apollo
- 27k: Spirit Snatch -0.9
- 37k: Spirit Snatch -0.9
- 50k: Spirit Snatch -0.9
- never picked: Ethereal Shift +1.8

### Baba
- never picked: Fleetfoot +4.6, Bullet Resilience +2.8, Mystic Expansion +2.5, Duration Extender +2.4

### Bebop
- never picked: Colossus +2.4, Crushing Fists +1.7, Witchmail +1.7, Slowing Bullets +1.6, Spirit Burn +1.6, Debuff Reducer +1.5

### Billy
- 27k: Stalker -1.2
- 37k: Stalker -1.2
- 50k: Stalker -1.2
- never picked: Colossus +1.9, Mystic Expansion +1.8, Enduring Speed +1.7

### Calico
- 10k: Stalker -2.4
- 18k: Stalker -2.4
- 27k: Stalker -2.4
- 37k: Stalker -2.4
- 50k: Stalker -2.4
- never picked: Lucky Shot +2.4, Colossus +2.2, Reactive Barrier +1.6

### Celeste
- never picked: Ethereal Shift +1.8

### Deadman Danny
- 18k: Kinetic Dash -4.4
- never picked: Hollow Point +2.0, Grit +1.9, Ethereal Shift +1.9, Compress Cooldown +1.8, Long Range +1.5

### Drifter
- never picked: Frenzy +1.8, Ethereal Shift +1.7, Duration Extender +1.7

### Dynamo
- 27k: Arcane Surge -1.2
- 37k: Arcane Surge -1.2
- 50k: Arcane Surge -1.2
- never picked: Cheat Death +2.0, Mystic Expansion +1.9, Healing Tempo +1.8, Indomitable +1.8

### Graves
- never picked: Magic Carpet +2.7, Diviner's Kevlar +2.0, Grit +1.7, Dispel Magic +1.7, Siphon Bullets +1.6, Spiritual Overflow +1.6

### Grey Talon

### Haze
- never picked: Rapid Recharge +2.9, Silencer +1.9, Lucky Shot +1.7, Fleetfoot +1.6, Enduring Speed +1.5

### Holliday
- never picked: Lucky Shot +2.3

### Infernus
- never picked: Silencer +3.0, Fleetfoot +2.2, Warp Stone +1.8, Sprint Boots +1.6

### Ivy
- never picked: Dispel Magic +1.6, Spirit Burn +1.5

### Kelvin
- never picked: Witchmail +2.5, Fleetfoot +2.3, Sprint Boots +2.3, Mystic Expansion +1.8, Duration Extender +1.7

### Lady Geist
- never picked: Sprint Boots +2.9, Frenzy +2.5, Silencer +2.1, Enduring Speed +1.8

### Lash
- 50k: Arcane Surge -2.3
- never picked: Magic Carpet +5.9, Siphon Bullets +2.2

### McGinnis
- 27k: Arcane Surge -1.4
- 37k: Arcane Surge -1.4
- never picked: Stamina Mastery +2.1, Boundless Spirit +1.8, Healing Tempo +1.7, Fleetfoot +1.5, Duration Extender +1.5

### Mina
- never picked: Ethereal Shift +2.5, Spirit Burn +1.8

### Mirage

### Mo & Krill
- never picked: Witchmail +2.3, Debuff Reducer +1.6

### Nurse Harrow
- never picked: Scourge +2.0

### Paige
- 18k: Arcane Surge -0.7
- 27k: Arcane Surge -0.7
- 37k: Arcane Surge -0.7
- 50k: Arcane Surge -0.7
- never picked: Scourge +3.4

### Paradox
- never picked: Ethereal Shift +4.4, Glass Cannon +1.7

### Pocket
- never picked: Ethereal Shift +2.9

### Rat King
- never picked: Duration Extender +3.4, Extra Stamina +3.3, Arcane Surge +3.2, Grit +2.9, Colossus +2.5, Slowing Bullets +1.9, Fleetfoot +1.6, Frenzy +1.6

### Rem
- never picked: Magic Carpet +3.1, Scourge +1.8

### Seven
- 10k: Extra Regen -1.2
- never picked: Fleetfoot +2.3, Monster Rounds +1.7, Lightning Scroll +1.6

### Shiv
- never picked: Ethereal Shift +1.7

### Silver
- never picked: Ethereal Shift +2.6, Duration Extender +2.4, Phantom Strike +1.9

### Sinclair
- never picked: Magic Carpet +3.2, Mystic Expansion +1.6

### Solomon
- never picked: Magic Carpet +4.1

### The Doorman

### Venator
- never picked: Spellslinger +1.9, Sprint Boots +1.7, Fleetfoot +1.6

### Victor
- never picked: Sprint Boots +3.5, Scourge +2.4, Warp Stone +2.4, Siphon Bullets +2.2, Ethereal Shift +1.7, Refresher +1.6

### Vindicta
- never picked: Extended Magazine +2.4, Duration Extender +2.2, Fleetfoot +1.8, Sprint Boots +1.6

### Violet
- never picked: Mystic Reverb +3.2, Ethereal Shift +2.3, Duration Extender +2.1, Witchmail +2.0

### Viscous
- never picked: Colossus +2.5, Point Blank +1.7

### Vyper
- never picked: Fleetfoot +2.3

### Warden
- never picked: Slowing Bullets +2.2, Fleetfoot +1.5

### Wraith
- never picked: Silencer +2.6, Spellslinger +2.3, Sprint Boots +1.7

### Yamato
- never picked: Refresher +2.2, Colossus +2.0

