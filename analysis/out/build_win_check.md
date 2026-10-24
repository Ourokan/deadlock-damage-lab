# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-10-23, 143,568 Ritualist+ matches (refreshed 2026-10-24T20:26:10Z).

- Recommended item slots with data: 1901; mean edge +1.2 (popular builds +0.0); clearly positive 1033, clearly negative 39.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Decay | spirit 3 | 13 | Nurse Harrow -3.1, McGinnis -3.0, Rem -2.7, Solomon -2.4 |
| Spirit Snatch | spirit 3 | 12 | Billy -2.2, Apollo -1.5, Abrams -1.1 |
| Stalker | weapon 2 | 2 | Billy -1.9 |
| Fortitude | vitality 3 | 2 | Deadman Danny -1.1 |
| Rapid Recharge | spirit 3 | 2 | Dynamo -1.8 |
| Escalating Exposure | spirit 4 | 2 | Victor -1.8, Kelvin -1.1 |
| Guardian Ward | vitality 2 | 2 | Paige -0.9 |
| Arcane Surge | spirit 2 | 1 | Kelvin -1.6 |
| Tankbuster | spirit 3 | 1 | Pocket -1.1 |
| Transcendent Cooldown | spirit 4 | 1 | Pocket -1.0 |
| Toxic Bullets | weapon 3 | 1 | Wraith -1.0 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Cheat Death | vitality 4 | 22 | Mo & Krill +4.0, Paige +3.8, Rem +3.5, Graves +3.4, Kelvin +3.4, Mirage +3.2, Deadman Danny +3.2, Wraith +3.2, Vindicta +3.2, Shiv +3.2, Grey Talon +3.1, Rat King +3.0, Vyper +3.0, Yamato +3.0, Bebop +3.0, Holliday +2.9, Nurse Harrow +2.9, Infernus +2.8, Lady Geist +2.7, Dynamo +2.5, Haze +2.5, Pocket +2.4 |
| Magic Carpet | spirit 4 | 10 | Lash +5.7, Solomon +4.4, Rem +4.0, Kelvin +3.0, Sinclair +3.0, McGinnis +3.0, Paradox +2.9, Paige +2.9, Graves +2.9, Dynamo +2.8 |
| Witchmail | vitality 4 | 9 | Lady Geist +3.2, Kelvin +3.2, Dynamo +3.0, Warden +3.0, Infernus +2.9, Victor +2.8, Lash +2.6, Bebop +2.1, Mo & Krill +1.8 |
| Spirit Burn | spirit 4 | 6 | The Doorman +2.6, Victor +2.1, Infernus +2.0, Paradox +2.0, Mina +1.8, Calico +1.7 |
| Sprint Boots | vitality 1 | 6 | Victor +3.4, Lady Geist +2.5, Infernus +1.8, Kelvin +1.8, Wraith +1.7, Venator +1.6 |
| Silencer | weapon 4 | 5 | Bebop +3.4, Infernus +3.3, Billy +2.6, Wraith +2.5, Ivy +1.7 |
| Ethereal Shift | spirit 4 | 5 | Pocket +3.2, Paradox +3.0, Mina +2.8, Infernus +2.7, Shiv +2.0 |
| Mystic Expansion | spirit 1 | 4 | Sinclair +1.8, Abrams +1.7, Dynamo +1.6, Celeste +1.5 |
| Greater Expansion | spirit 3 | 4 | Billy +2.5, Seven +2.0, Rat King +2.0, Paradox +1.6 |
| Duration Extender | spirit 2 | 4 | Rat King +3.5, Silver +3.2, Vindicta +2.2, Drifter +1.8 |
| Fleetfoot | weapon 2 | 4 | Seven +2.4, Vindicta +1.9, Warden +1.6, Rat King +1.5 |
| Colossus | vitality 4 | 3 | Rat King +2.5, Billy +2.0, Abrams +2.0 |
| Slowing Bullets | weapon 2 | 3 | Silver +2.1, Rat King +2.1, Bebop +1.7 |
| Compress Cooldown | spirit 2 | 3 | Deadman Danny +2.0, Lash +1.9, Mina +1.5 |
| Frenzy | weapon 4 | 3 | Victor +2.9, Drifter +2.5, Rat King +1.8 |
| Lucky Shot | weapon 4 | 3 | Ivy +2.7, Holliday +2.0, Vyper +1.7 |
| Refresher | spirit 4 | 3 | Yamato +2.0, Victor +1.6, Paige +1.5 |
| Enduring Speed | vitality 2 | 2 | Billy +1.5, Haze +1.5 |
| Grit | vitality 1 | 2 | Rat King +2.9, Deadman Danny +1.7 |
| Hollow Point | weapon 3 | 2 | Vyper +2.6, Drifter +2.1 |
| Superior Cooldown | spirit 3 | 2 | Drifter +2.0, Holliday +1.8 |
| Healing Tempo | vitality 4 | 2 | Haze +3.1, Dynamo +2.1 |
| Siphon Bullets | vitality 4 | 2 | Haze +2.7, Victor +2.2 |
| Warp Stone | vitality 3 | 2 | Victor +2.1, Infernus +1.5 |
| Boundless Spirit | spirit 4 | 2 | Wraith +2.1, McGinnis +1.5 |
| Lightning Scroll | spirit 4 | 2 | Paige +2.1, Seven +1.7 |
| Spellslinger | weapon 4 | 2 | Venator +2.3, Vindicta +1.8 |
| Stamina Mastery | vitality 3 | 1 | Apollo +1.7 |
| Diviner's Kevlar | vitality 4 | 1 | Deadman Danny +5.0 |
| High-Velocity Rounds | weapon 1 | 1 | Deadman Danny +4.5 |
| Toxic Bullets | weapon 3 | 1 | Deadman Danny +2.3 |
| Transcendent Cooldown | spirit 4 | 1 | Drifter +2.0 |
| Glass Cannon | weapon 4 | 1 | Drifter +1.8 |
| Divine Barrier | vitality 4 | 1 | Dynamo +2.5 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.3 |
| Mercurial Magnum | spirit 4 | 1 | Haze +1.7 |
| Quicksilver Reload | spirit 2 | 1 | Holliday +2.0 |
| Scourge | spirit 4 | 1 | Infernus +2.7 |
| Spellbreaker | vitality 4 | 1 | Infernus +2.0 |
| Dispel Magic | vitality 3 | 1 | Ivy +2.3 |
| Swift Striker | weapon 2 | 1 | Ivy +1.8 |
| Indomitable | vitality 4 | 1 | Lash +1.9 |
| Alchemical Fire | weapon 3 | 1 | Paradox +2.0 |
| Arcane Surge | spirit 2 | 1 | Rat King +3.0 |
| Extra Stamina | vitality 1 | 1 | Rat King +2.9 |
| Monster Rounds | weapon 1 | 1 | Seven +1.8 |
| Phantom Strike | vitality 4 | 1 | Silver +2.7 |
| Long Range | weapon 2 | 1 | Solomon +1.6 |
| Escalating Exposure | spirit 4 | 1 | Solomon +1.6 |
| Spirit Shredder | weapon 2 | 1 | Solomon +1.6 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.1 |
| Rapid Rounds | weapon 1 | 1 | Wraith +1.8 |
| Mystic Regeneration | spirit 1 | 1 | Yamato +2.8 |

## Per hero

### Abrams
- 10k: Spirit Snatch -1.1
- 18k: Spirit Snatch -1.1
- 27k: Spirit Snatch -1.1
- 37k: Spirit Snatch -1.1
- 50k: Spirit Snatch -1.1
- never picked: Colossus +2.0, Mystic Expansion +1.7

### Apollo
- 27k: Spirit Snatch -1.5
- 37k: Spirit Snatch -1.5
- 50k: Spirit Snatch -1.5
- never picked: Stamina Mastery +1.7

### Bebop
- never picked: Silencer +3.4, Cheat Death +3.0, Witchmail +2.1, Slowing Bullets +1.7

### Billy
- 10k: Stalker -1.9
- 18k: Spirit Snatch -2.2
- 27k: Stalker -1.9, Spirit Snatch -2.2
- 37k: Spirit Snatch -2.2
- 50k: Spirit Snatch -2.2
- never picked: Silencer +2.6, Greater Expansion +2.5, Colossus +2.0, Enduring Speed +1.5

### Calico
- never picked: Spirit Burn +1.7

### Celeste
- never picked: Mystic Expansion +1.5

### Deadman Danny
- 27k: Fortitude -1.1
- 50k: Fortitude -1.1
- never picked: Diviner's Kevlar +5.0, High-Velocity Rounds +4.5, Cheat Death +3.2, Toxic Bullets +2.3, Compress Cooldown +2.0, Grit +1.7

### Drifter
- never picked: Frenzy +2.5, Hollow Point +2.1, Superior Cooldown +2.0, Transcendent Cooldown +2.0, Duration Extender +1.8, Glass Cannon +1.8

### Dynamo
- 27k: Rapid Recharge -1.8
- 37k: Rapid Recharge -1.8
- never picked: Witchmail +3.0, Magic Carpet +2.8, Cheat Death +2.5, Divine Barrier +2.5, Healing Tempo +2.1, Mystic Expansion +1.6

### Graves
- never picked: Cheat Death +3.4, Magic Carpet +2.9

### Grey Talon
- never picked: Cheat Death +3.1

### Haze
- never picked: Healing Tempo +3.1, Siphon Bullets +2.7, Cheat Death +2.5, Rapid Recharge +2.3, Mercurial Magnum +1.7, Enduring Speed +1.5

### Holliday
- never picked: Cheat Death +2.9, Quicksilver Reload +2.0, Lucky Shot +2.0, Superior Cooldown +1.8

### Infernus
- never picked: Silencer +3.3, Witchmail +2.9, Cheat Death +2.8, Scourge +2.7, Ethereal Shift +2.7, Spirit Burn +2.0, Spellbreaker +2.0, Sprint Boots +1.8

### Ivy
- never picked: Lucky Shot +2.7, Dispel Magic +2.3, Swift Striker +1.8, Silencer +1.7

### Kelvin
- 37k: Arcane Surge -1.6
- 50k: Escalating Exposure -1.1
- never picked: Cheat Death +3.4, Witchmail +3.2, Magic Carpet +3.0, Sprint Boots +1.8

### Lady Geist
- never picked: Witchmail +3.2, Cheat Death +2.7, Sprint Boots +2.5

### Lash
- never picked: Magic Carpet +5.7, Witchmail +2.6, Indomitable +1.9, Compress Cooldown +1.9

### McGinnis
- 10k: Decay -3.0
- 18k: Decay -3.0
- 27k: Decay -3.0
- 37k: Decay -3.0
- 50k: Decay -3.0
- never picked: Magic Carpet +3.0, Boundless Spirit +1.5

### Mina
- never picked: Ethereal Shift +2.8, Spirit Burn +1.8, Compress Cooldown +1.5

### Mirage
- never picked: Cheat Death +3.2

### Mo & Krill
- never picked: Cheat Death +4.0, Witchmail +1.8

### Nurse Harrow
- 18k: Decay -3.1
- never picked: Cheat Death +2.9

### Paige
- 10k: Guardian Ward -0.9
- 18k: Guardian Ward -0.9
- never picked: Cheat Death +3.8, Magic Carpet +2.9, Lightning Scroll +2.1, Refresher +1.5

### Paradox
- never picked: Ethereal Shift +3.0, Magic Carpet +2.9, Alchemical Fire +2.0, Spirit Burn +2.0, Greater Expansion +1.6

### Pocket
- 37k: Tankbuster -1.1
- 50k: Transcendent Cooldown -1.0
- never picked: Ethereal Shift +3.2, Cheat Death +2.4

### Rat King
- never picked: Duration Extender +3.5, Arcane Surge +3.0, Cheat Death +3.0, Extra Stamina +2.9, Grit +2.9, Colossus +2.5, Slowing Bullets +2.1, Greater Expansion +2.0

### Rem
- 10k: Decay -2.7
- 18k: Decay -2.7
- 27k: Decay -2.7
- 37k: Decay -2.7
- 50k: Decay -2.7
- never picked: Magic Carpet +4.0, Cheat Death +3.5

### Seven
- never picked: Fleetfoot +2.4, Greater Expansion +2.0, Monster Rounds +1.8, Lightning Scroll +1.7

### Shiv
- never picked: Cheat Death +3.2, Ethereal Shift +2.0

### Silver
- never picked: Duration Extender +3.2, Phantom Strike +2.7, Slowing Bullets +2.1

### Sinclair
- never picked: Magic Carpet +3.0, Mystic Expansion +1.8

### Solomon
- 10k: Decay -2.4
- 27k: Decay -2.4
- never picked: Magic Carpet +4.4, Long Range +1.6, Escalating Exposure +1.6, Spirit Shredder +1.6

### The Doorman
- never picked: Spirit Burn +2.6

### Venator
- never picked: Spellslinger +2.3, Sprint Boots +1.6

### Victor
- 50k: Escalating Exposure -1.8
- never picked: Sprint Boots +3.4, Frenzy +2.9, Witchmail +2.8, Siphon Bullets +2.2, Spirit Burn +2.1, Warp Stone +2.1, Refresher +1.6

### Vindicta
- never picked: Cheat Death +3.2, Duration Extender +2.2, Extended Magazine +2.1, Fleetfoot +1.9, Spellslinger +1.8

### Viscous

### Vyper
- never picked: Cheat Death +3.0, Hollow Point +2.6, Lucky Shot +1.7

### Warden
- never picked: Witchmail +3.0, Fleetfoot +1.6

### Wraith
- 50k: Toxic Bullets -1.0
- never picked: Cheat Death +3.2, Silencer +2.5, Boundless Spirit +2.1, Rapid Rounds +1.8, Sprint Boots +1.7

### Yamato
- never picked: Cheat Death +3.0, Mystic Regeneration +2.8, Refresher +2.0

