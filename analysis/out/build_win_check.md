# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-11-02, 216,997 Ritualist+ matches (refreshed 2026-11-03T02:32:35Z).

- Recommended item slots with data: 1994; mean edge +1.7 (popular builds +0.1); clearly positive 1491, clearly negative 19.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 8 | Victor -6.0, Lash -2.5, McGinnis -1.3, Dynamo -1.2 |
| Stalker | weapon 2 | 7 | Calico -2.4, Billy -1.1 |
| Spirit Snatch | spirit 3 | 2 | Apollo -1.0 |
| Kinetic Dash | weapon 2 | 2 | Deadman Danny -4.6, Celeste -1.6 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Fleetfoot | weapon 2 | 10 | Baba +4.6, Nurse Harrow +2.5, Vyper +2.5, Seven +2.4, Kelvin +2.3, Vindicta +1.8, Rat King +1.7, Warden +1.6, Haze +1.5, Venator +1.5 |
| Ethereal Shift | spirit 4 | 9 | Paradox +3.9, Pocket +2.8, Silver +2.5, Mina +2.5, Violet +2.4, Shiv +1.9, Celeste +1.7, Drifter +1.7, Victor +1.6 |
| Duration Extender | spirit 2 | 8 | Rat King +3.4, Silver +2.5, Baba +2.4, Vindicta +2.2, Violet +2.1, Drifter +1.7, Viscous +1.5, Kelvin +1.5 |
| Sprint Boots | vitality 1 | 7 | Victor +3.2, Lady Geist +2.6, Kelvin +2.2, Venator +1.8, Infernus +1.8, Wraith +1.6, Vindicta +1.6 |
| Colossus | vitality 4 | 5 | Rat King +2.5, Viscous +2.5, Bebop +2.4, Calico +2.3, Yamato +1.9 |
| Frenzy | weapon 4 | 5 | Victor +3.1, Shiv +2.3, Lady Geist +2.3, Drifter +1.9, Rat King +1.6 |
| Magic Carpet | spirit 4 | 5 | Lash +5.8, Solomon +4.1, Rem +3.3, Sinclair +3.0, Graves +2.5 |
| Silencer | weapon 4 | 4 | Infernus +2.8, Wraith +2.7, Lady Geist +2.3, Haze +1.9 |
| Witchmail | vitality 4 | 3 | Kelvin +2.5, Mo & Krill +2.3, Bebop +1.7 |
| Spirit Burn | spirit 4 | 3 | Infernus +2.6, Mina +1.8, Bebop +1.5 |
| Mystic Expansion | spirit 1 | 3 | Dynamo +1.9, Kelvin +1.8, Billy +1.6 |
| Enduring Speed | vitality 2 | 3 | Lady Geist +1.8, Billy +1.6, Haze +1.5 |
| Grit | vitality 1 | 3 | Rat King +2.9, Graves +1.8, Deadman Danny +1.7 |
| Siphon Bullets | vitality 4 | 3 | Lash +2.2, Victor +2.2, Graves +1.5 |
| Lucky Shot | weapon 4 | 3 | Ivy +2.7, Holliday +2.2, Haze +1.7 |
| Scourge | spirit 4 | 2 | Rem +1.6, Apollo +1.6 |
| Slowing Bullets | weapon 2 | 2 | Warden +2.1, Bebop +1.6 |
| Debuff Reducer | vitality 2 | 2 | Mo & Krill +1.6, Bebop +1.6 |
| Compress Cooldown | spirit 2 | 2 | Deadman Danny +1.8, Mina +1.6 |
| Healing Tempo | vitality 4 | 2 | Dynamo +1.8, McGinnis +1.6 |
| Indomitable | vitality 4 | 2 | McGinnis +2.0, Dynamo +1.7 |
| Spiritual Overflow | weapon 4 | 2 | Mina +1.7, Graves +1.7 |
| Warp Stone | vitality 3 | 2 | Victor +2.4, Infernus +1.8 |
| Dispel Magic | vitality 3 | 2 | Ivy +1.8, Rat King +1.6 |
| Extra Health | vitality 1 | 2 | Warden +2.0, Sinclair +1.8 |
| Spellslinger | weapon 4 | 2 | Wraith +2.3, Venator +2.1 |
| Refresher | spirit 4 | 2 | Yamato +2.1, Victor +1.7 |
| Superior Cooldown | spirit 3 | 1 | Baba +1.5 |
| Ballistic Enchantment | weapon 3 | 1 | Billy +3.3 |
| Point Blank | weapon 3 | 1 | Calico +1.8 |
| Hollow Point | weapon 3 | 1 | Deadman Danny +2.0 |
| Long Range | weapon 2 | 1 | Deadman Danny +1.5 |
| Diviner's Kevlar | vitality 4 | 1 | Graves +1.9 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.8 |
| Spellbreaker | vitality 4 | 1 | Infernus +1.5 |
| Stamina Mastery | vitality 3 | 1 | McGinnis +1.7 |
| Glass Cannon | weapon 4 | 1 | Paradox +1.7 |
| Extra Stamina | vitality 1 | 1 | Rat King +3.3 |
| Arcane Surge | spirit 2 | 1 | Rat King +3.1 |
| Monster Rounds | weapon 1 | 1 | Seven +1.7 |
| Lightning Scroll | spirit 4 | 1 | Seven +1.5 |
| Phantom Strike | vitality 4 | 1 | Silver +2.1 |
| Spirit Rend | weapon 3 | 1 | Solomon +1.8 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.2 |
| Mystic Reverb | spirit 4 | 1 | Violet +3.5 |
| Rapid Rounds | weapon 1 | 1 | Warden +1.6 |
| Boundless Spirit | spirit 4 | 1 | Wraith +1.6 |

## Per hero

### Abrams

### Apollo
- 37k: Spirit Snatch -1.0
- 50k: Spirit Snatch -1.0
- never picked: Scourge +1.6

### Baba
- never picked: Fleetfoot +4.6, Duration Extender +2.4, Superior Cooldown +1.5

### Bebop
- never picked: Colossus +2.4, Witchmail +1.7, Slowing Bullets +1.6, Debuff Reducer +1.6, Spirit Burn +1.5

### Billy
- 27k: Stalker -1.1
- 37k: Stalker -1.1
- 50k: Stalker -1.1
- never picked: Ballistic Enchantment +3.3, Mystic Expansion +1.6, Enduring Speed +1.6

### Calico
- 18k: Stalker -2.4
- 27k: Stalker -2.4
- 37k: Stalker -2.4
- 50k: Stalker -2.4
- never picked: Colossus +2.3, Point Blank +1.8

### Celeste
- 27k: Kinetic Dash -1.6
- never picked: Ethereal Shift +1.7

### Deadman Danny
- 18k: Kinetic Dash -4.6
- never picked: Hollow Point +2.0, Compress Cooldown +1.8, Grit +1.7, Long Range +1.5

### Drifter
- never picked: Frenzy +1.9, Duration Extender +1.7, Ethereal Shift +1.7

### Dynamo
- 18k: Arcane Surge -1.2
- 50k: Arcane Surge -1.2
- never picked: Mystic Expansion +1.9, Healing Tempo +1.8, Indomitable +1.7

### Graves
- never picked: Magic Carpet +2.5, Diviner's Kevlar +1.9, Grit +1.8, Spiritual Overflow +1.7, Siphon Bullets +1.5

### Grey Talon

### Haze
- never picked: Rapid Recharge +2.8, Silencer +1.9, Lucky Shot +1.7, Enduring Speed +1.5, Fleetfoot +1.5

### Holliday
- never picked: Lucky Shot +2.2

### Infernus
- never picked: Silencer +2.8, Spirit Burn +2.6, Warp Stone +1.8, Sprint Boots +1.8, Spellbreaker +1.5

### Ivy
- never picked: Lucky Shot +2.7, Dispel Magic +1.8

### Kelvin
- never picked: Witchmail +2.5, Fleetfoot +2.3, Sprint Boots +2.2, Mystic Expansion +1.8, Duration Extender +1.5

### Lady Geist
- never picked: Sprint Boots +2.6, Silencer +2.3, Frenzy +2.3, Enduring Speed +1.8

### Lash
- 27k: Arcane Surge -2.5
- 50k: Arcane Surge -2.5
- never picked: Magic Carpet +5.8, Siphon Bullets +2.2

### McGinnis
- 27k: Arcane Surge -1.3
- 50k: Arcane Surge -1.3
- never picked: Indomitable +2.0, Stamina Mastery +1.7, Healing Tempo +1.6

### Mina
- never picked: Ethereal Shift +2.5, Spirit Burn +1.8, Spiritual Overflow +1.7, Compress Cooldown +1.6

### Mirage

### Mo & Krill
- never picked: Witchmail +2.3, Debuff Reducer +1.6

### Nurse Harrow
- never picked: Fleetfoot +2.5

### Paige

### Paradox
- never picked: Ethereal Shift +3.9, Glass Cannon +1.7

### Pocket
- never picked: Ethereal Shift +2.8

### Rat King
- never picked: Duration Extender +3.4, Extra Stamina +3.3, Arcane Surge +3.1, Grit +2.9, Colossus +2.5, Fleetfoot +1.7, Frenzy +1.6, Dispel Magic +1.6

### Rem
- never picked: Magic Carpet +3.3, Scourge +1.6

### Seven
- never picked: Fleetfoot +2.4, Monster Rounds +1.7, Lightning Scroll +1.5

### Shiv
- never picked: Frenzy +2.3, Ethereal Shift +1.9

### Silver
- never picked: Ethereal Shift +2.5, Duration Extender +2.5, Phantom Strike +2.1

### Sinclair
- never picked: Magic Carpet +3.0, Extra Health +1.8

### Solomon
- never picked: Magic Carpet +4.1, Spirit Rend +1.8

### The Doorman

### Venator
- never picked: Spellslinger +2.1, Sprint Boots +1.8, Fleetfoot +1.5

### Victor
- 18k: Arcane Surge -6.0
- 50k: Arcane Surge -6.0
- never picked: Sprint Boots +3.2, Frenzy +3.1, Warp Stone +2.4, Siphon Bullets +2.2, Refresher +1.7, Ethereal Shift +1.6

### Vindicta
- never picked: Extended Magazine +2.2, Duration Extender +2.2, Fleetfoot +1.8, Sprint Boots +1.6

### Violet
- never picked: Mystic Reverb +3.5, Ethereal Shift +2.4, Duration Extender +2.1

### Viscous
- never picked: Colossus +2.5, Duration Extender +1.5

### Vyper
- never picked: Fleetfoot +2.5

### Warden
- never picked: Slowing Bullets +2.1, Extra Health +2.0, Rapid Rounds +1.6, Fleetfoot +1.6

### Wraith
- never picked: Silencer +2.7, Spellslinger +2.3, Boundless Spirit +1.6, Sprint Boots +1.6

### Yamato
- never picked: Refresher +2.1, Colossus +1.9

