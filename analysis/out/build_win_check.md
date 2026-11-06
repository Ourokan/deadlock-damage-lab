# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-11-05, 237,741 Ritualist+ matches (refreshed 2026-11-06T16:49:00Z).

- Recommended item slots with data: 1973; mean edge +1.7 (popular builds +0.1); clearly positive 1525, clearly negative 16.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Stalker | weapon 2 | 7 | Calico -2.3, Shiv -1.8, Billy -1.2 |
| Arcane Surge | spirit 2 | 6 | McGinnis -1.4, Dynamo -1.2, Paige -0.7 |
| Kinetic Dash | weapon 2 | 2 | Deadman Danny -4.6, Warden -4.0 |
| Spirit Snatch | spirit 3 | 1 | Apollo -0.9 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Fleetfoot | weapon 2 | 12 | Baba +4.6, Seven +2.5, Vyper +2.4, Kelvin +2.3, Infernus +2.2, Warden +1.8, Vindicta +1.7, Rat King +1.6, Victor +1.6, Haze +1.6, McGinnis +1.6, Venator +1.5 |
| Ethereal Shift | spirit 4 | 11 | Paradox +4.3, Pocket +2.9, Silver +2.5, Mina +2.4, Violet +2.3, Deadman Danny +1.9, Celeste +1.9, Apollo +1.8, Drifter +1.8, Victor +1.6, Shiv +1.6 |
| Duration Extender | spirit 2 | 8 | Rat King +3.4, Silver +2.5, Baba +2.4, Vindicta +2.2, Violet +2.1, Drifter +1.7, Kelvin +1.7, Abrams +1.5 |
| Sprint Boots | vitality 1 | 7 | Victor +3.5, Lady Geist +2.9, Kelvin +2.3, Venator +1.7, Warden +1.7, Infernus +1.7, Wraith +1.6 |
| Colossus | vitality 4 | 6 | Viscous +2.6, Rat King +2.5, Bebop +2.4, Yamato +2.1, Billy +1.9, Mo & Krill +1.9 |
| Frenzy | weapon 4 | 6 | Haze +3.3, Victor +3.1, Lady Geist +2.5, Shiv +1.9, Drifter +1.7, Rat King +1.7 |
| Mystic Expansion | spirit 1 | 5 | Baba +2.6, Dynamo +1.9, Kelvin +1.8, Billy +1.7, Sinclair +1.6 |
| Magic Carpet | spirit 4 | 5 | Lash +5.7, Solomon +4.1, Rem +3.3, Sinclair +3.1, Graves +2.8 |
| Witchmail | vitality 4 | 4 | Kelvin +2.5, Mo & Krill +2.4, Apollo +2.3, Bebop +1.7 |
| Spirit Burn | spirit 4 | 4 | Solomon +2.3, Mina +1.8, Vindicta +1.6, Bebop +1.6 |
| Lucky Shot | weapon 4 | 3 | Calico +2.5, Holliday +2.4, Haze +1.7 |
| Grit | vitality 1 | 3 | Rat King +2.9, Deadman Danny +1.9, Graves +1.7 |
| Siphon Bullets | vitality 4 | 3 | Victor +2.3, Lash +2.0, Graves +1.6 |
| Silencer | weapon 4 | 3 | Infernus +3.0, Lady Geist +2.2, Haze +1.9 |
| Spiritual Overflow | weapon 4 | 3 | Warden +1.6, Haze +1.6, Mina +1.5 |
| Debuff Reducer | vitality 2 | 2 | Bebop +1.5, Mo & Krill +1.5 |
| Enduring Speed | vitality 2 | 2 | Billy +1.7, Lady Geist +1.7 |
| Healing Tempo | vitality 4 | 2 | Dynamo +1.8, McGinnis +1.6 |
| Warp Stone | vitality 3 | 2 | Victor +2.5, Infernus +1.7 |
| Extra Health | vitality 1 | 2 | Warden +1.9, Sinclair +1.8 |
| Spellslinger | weapon 4 | 2 | Wraith +2.4, Venator +1.9 |
| Refresher | spirit 4 | 2 | Yamato +2.1, Victor +1.6 |
| Bullet Resilience | vitality 3 | 1 | Baba +2.8 |
| Crushing Fists | weapon 4 | 1 | Bebop +1.8 |
| Slowing Bullets | weapon 2 | 1 | Bebop +1.7 |
| Spellbreaker | vitality 4 | 1 | Bebop +1.5 |
| Compress Cooldown | spirit 2 | 1 | Deadman Danny +1.8 |
| Long Range | weapon 2 | 1 | Deadman Danny +1.5 |
| Transcendent Cooldown | spirit 4 | 1 | Drifter +1.5 |
| Cheat Death | vitality 4 | 1 | Dynamo +2.2 |
| Indomitable | vitality 4 | 1 | Dynamo +1.6 |
| Diviner's Kevlar | vitality 4 | 1 | Graves +1.9 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.9 |
| Weakening Headshot | weapon 2 | 1 | Haze +1.6 |
| Infuser | vitality 4 | 1 | Lady Geist +3.7 |
| Stamina Mastery | vitality 3 | 1 | McGinnis +2.5 |
| Boundless Spirit | spirit 4 | 1 | McGinnis +1.8 |
| Scourge | spirit 4 | 1 | Nurse Harrow +2.1 |
| Glass Cannon | weapon 4 | 1 | Paradox +1.5 |
| Extra Stamina | vitality 1 | 1 | Rat King +3.3 |
| Arcane Surge | spirit 2 | 1 | Rat King +3.2 |
| Monster Rounds | weapon 1 | 1 | Seven +1.9 |
| Lightning Scroll | spirit 4 | 1 | Seven +1.8 |
| Phantom Strike | vitality 4 | 1 | Silver +1.8 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.5 |
| Lifestrike | vitality 3 | 1 | Viscous +2.9 |
| Point Blank | weapon 3 | 1 | Viscous +1.8 |

## Per hero

### Abrams
- never picked: Duration Extender +1.5

### Apollo
- 27k: Spirit Snatch -0.9
- never picked: Witchmail +2.3, Ethereal Shift +1.8

### Baba
- never picked: Fleetfoot +4.6, Bullet Resilience +2.8, Mystic Expansion +2.6, Duration Extender +2.4

### Bebop
- never picked: Colossus +2.4, Crushing Fists +1.8, Slowing Bullets +1.7, Witchmail +1.7, Spirit Burn +1.6, Debuff Reducer +1.5, Spellbreaker +1.5

### Billy
- 27k: Stalker -1.2
- 37k: Stalker -1.2
- 50k: Stalker -1.2
- never picked: Colossus +1.9, Mystic Expansion +1.7, Enduring Speed +1.7

### Calico
- 10k: Stalker -2.3
- 18k: Stalker -2.3
- 27k: Stalker -2.3
- never picked: Lucky Shot +2.5

### Celeste
- never picked: Ethereal Shift +1.9

### Deadman Danny
- 18k: Kinetic Dash -4.6
- never picked: Ethereal Shift +1.9, Grit +1.9, Compress Cooldown +1.8, Long Range +1.5

### Drifter
- never picked: Ethereal Shift +1.8, Duration Extender +1.7, Frenzy +1.7, Transcendent Cooldown +1.5

### Dynamo
- 37k: Arcane Surge -1.2
- 50k: Arcane Surge -1.2
- never picked: Cheat Death +2.2, Mystic Expansion +1.9, Healing Tempo +1.8, Indomitable +1.6

### Graves
- never picked: Magic Carpet +2.8, Diviner's Kevlar +1.9, Grit +1.7, Siphon Bullets +1.6

### Grey Talon

### Haze
- never picked: Frenzy +3.3, Rapid Recharge +2.9, Silencer +1.9, Lucky Shot +1.7, Weakening Headshot +1.6, Fleetfoot +1.6, Spiritual Overflow +1.6

### Holliday
- never picked: Lucky Shot +2.4

### Infernus
- never picked: Silencer +3.0, Fleetfoot +2.2, Warp Stone +1.7, Sprint Boots +1.7

### Ivy

### Kelvin
- never picked: Witchmail +2.5, Sprint Boots +2.3, Fleetfoot +2.3, Mystic Expansion +1.8, Duration Extender +1.7

### Lady Geist
- never picked: Infuser +3.7, Sprint Boots +2.9, Frenzy +2.5, Silencer +2.2, Enduring Speed +1.7

### Lash
- never picked: Magic Carpet +5.7, Siphon Bullets +2.0

### McGinnis
- 27k: Arcane Surge -1.4
- never picked: Stamina Mastery +2.5, Boundless Spirit +1.8, Healing Tempo +1.6, Fleetfoot +1.6

### Mina
- never picked: Ethereal Shift +2.4, Spirit Burn +1.8, Spiritual Overflow +1.5

### Mirage

### Mo & Krill
- never picked: Witchmail +2.4, Colossus +1.9, Debuff Reducer +1.5

### Nurse Harrow
- never picked: Scourge +2.1

### Paige
- 18k: Arcane Surge -0.7
- 27k: Arcane Surge -0.7
- 37k: Arcane Surge -0.7

### Paradox
- never picked: Ethereal Shift +4.3, Glass Cannon +1.5

### Pocket
- never picked: Ethereal Shift +2.9

### Rat King
- never picked: Duration Extender +3.4, Extra Stamina +3.3, Arcane Surge +3.2, Grit +2.9, Colossus +2.5, Frenzy +1.7, Fleetfoot +1.6

### Rem
- never picked: Magic Carpet +3.3

### Seven
- never picked: Fleetfoot +2.5, Monster Rounds +1.9, Lightning Scroll +1.8

### Shiv
- 18k: Stalker -1.8
- never picked: Frenzy +1.9, Ethereal Shift +1.6

### Silver
- never picked: Ethereal Shift +2.5, Duration Extender +2.5, Phantom Strike +1.8

### Sinclair
- never picked: Magic Carpet +3.1, Extra Health +1.8, Mystic Expansion +1.6

### Solomon
- never picked: Magic Carpet +4.1, Spirit Burn +2.3

### The Doorman

### Venator
- never picked: Spellslinger +1.9, Sprint Boots +1.7, Fleetfoot +1.5

### Victor
- never picked: Sprint Boots +3.5, Frenzy +3.1, Warp Stone +2.5, Siphon Bullets +2.3, Ethereal Shift +1.6, Fleetfoot +1.6, Refresher +1.6

### Vindicta
- never picked: Extended Magazine +2.5, Duration Extender +2.2, Fleetfoot +1.7, Spirit Burn +1.6

### Violet
- never picked: Ethereal Shift +2.3, Duration Extender +2.1

### Viscous
- never picked: Lifestrike +2.9, Colossus +2.6, Point Blank +1.8

### Vyper
- never picked: Fleetfoot +2.4

### Warden
- 27k: Kinetic Dash -4.0
- never picked: Extra Health +1.9, Fleetfoot +1.8, Sprint Boots +1.7, Spiritual Overflow +1.6

### Wraith
- never picked: Spellslinger +2.4, Sprint Boots +1.6

### Yamato
- never picked: Colossus +2.1, Refresher +2.1

