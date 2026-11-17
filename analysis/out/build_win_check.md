# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-16, 123,746 Ritualist+ matches (refreshed 2026-11-17T03:10:25Z).

- Recommended item slots with data: 1895; mean edge +0.9 (popular builds +0.1); clearly positive 795, clearly negative 43.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Kinetic Dash | weapon 2 | 15 | Warden -4.7, Celeste -2.6, Haze -2.0, Drifter -0.8 |
| Escalating Exposure | spirit 4 | 5 | Victor -1.6, Kelvin -1.2, Lady Geist -0.7 |
| Spirit Snatch | spirit 3 | 4 | Billy -1.2 |
| Rapid Recharge | spirit 3 | 4 | Dynamo -1.1, Paige -0.7 |
| Toxic Bullets | weapon 3 | 3 | Infernus -1.1 |
| Stalker | weapon 2 | 3 | Yamato -1.5 |
| Tankbuster | spirit 3 | 2 | Deadman Danny -1.1 |
| Battle Vest | vitality 2 | 2 | Shiv -1.1, Haze -1.0 |
| Guardian Ward | vitality 2 | 2 | Solomon -1.9, Paige -0.8 |
| Express Shot | weapon 3 | 1 | Deadman Danny -1.1 |
| Sprint Boots | vitality 1 | 1 | Mina -3.9 |
| Boundless Spirit | spirit 4 | 1 | Solomon -1.5 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 10 | Calico +3.4, Infernus +2.9, Pocket +2.9, Celeste +2.6, Mina +2.6, Venator +2.5, Deadman Danny +2.1, Shiv +2.1, Victor +1.9, Apollo +1.9 |
| Mystic Reverb | spirit 4 | 9 | Bebop +4.5, Deadman Danny +3.6, The Doorman +3.1, Grey Talon +2.9, Sinclair +2.7, Yamato +2.6, Rat King +2.2, Viscous +2.0, Solomon +2.0 |
| Dispel Magic | vitality 3 | 7 | Kelvin +2.2, Billy +2.1, Celeste +1.9, Mo & Krill +1.9, Graves +1.8, Abrams +1.7, Holliday +1.5 |
| Spirit Burn | spirit 4 | 7 | Infernus +2.7, Seven +2.7, Ivy +2.6, Vindicta +2.4, Drifter +1.6, Mina +1.6, Deadman Danny +1.5 |
| Frenzy | weapon 4 | 5 | Warden +3.6, Venator +3.5, Abrams +3.3, Lady Geist +3.0, Rat King +2.8 |
| Colossus | vitality 4 | 5 | Warden +3.2, Yamato +3.1, Mo & Krill +2.6, Apollo +2.4, Abrams +1.9 |
| Superior Cooldown | spirit 3 | 5 | Calico +2.4, Celeste +1.9, Drifter +1.7, Rem +1.5, Holliday +1.5 |
| Mystic Expansion | spirit 1 | 4 | Vindicta +3.7, Baba +2.1, Billy +1.7, Celeste +1.6 |
| Spirit Lifesteal | vitality 2 | 4 | Grey Talon +2.5, Deadman Danny +2.2, Graves +2.1, Wraith +2.1 |
| Siphon Bullets | vitality 4 | 4 | Lash +2.9, Haze +2.5, Graves +1.7, Drifter +1.6 |
| Magic Carpet | spirit 4 | 4 | Lash +4.4, Graves +3.6, Solomon +3.3, Sinclair +2.6 |
| Silencer | weapon 4 | 4 | Infernus +2.4, Wraith +2.1, Haze +1.6, Graves +1.6 |
| Witchmail | vitality 4 | 4 | Victor +3.2, Kelvin +1.9, Mo & Krill +1.9, Warden +1.7 |
| Slowing Bullets | weapon 2 | 3 | Silver +2.5, Abrams +2.4, Warden +1.8 |
| Berserker | weapon 3 | 3 | Shiv +1.8, Yamato +1.5, Abrams +1.5 |
| Grit | vitality 1 | 3 | Baba +2.9, Nurse Harrow +1.6, Holliday +1.5 |
| Hollow Point | weapon 3 | 3 | Grey Talon +2.5, Drifter +1.9, Holliday +1.7 |
| Healing Tempo | vitality 4 | 3 | Haze +2.7, McGinnis +2.1, Dynamo +2.0 |
| Spiritual Overflow | weapon 4 | 3 | Mina +2.1, Graves +1.8, Haze +1.6 |
| Extra Spirit | spirit 1 | 3 | Wraith +4.3, Vyper +2.8, Haze +1.9 |
| Sprint Boots | vitality 1 | 3 | Haze +1.9, Warden +1.8, Victor +1.8 |
| Diviner's Kevlar | vitality 4 | 3 | McGinnis +3.9, Mirage +3.3, Holliday +2.4 |
| Duration Extender | spirit 2 | 2 | Kelvin +1.8, Abrams +1.7 |
| Melee Charge | weapon 2 | 2 | Yamato +3.0, Billy +1.5 |
| Lucky Shot | weapon 4 | 2 | Calico +2.4, Ivy +1.8 |
| Warp Stone | vitality 3 | 2 | Lady Geist +4.0, Victor +3.1 |
| Mystic Vulnerability | spirit 2 | 2 | Warden +1.9, Mo & Krill +1.9 |
| Scourge | spirit 4 | 2 | Victor +2.4, Rem +2.3 |
| Extra Health | vitality 1 | 2 | Yamato +1.8, Warden +1.5 |
| Enduring Speed | vitality 2 | 1 | Abrams +1.7 |
| Debuff Reducer | vitality 2 | 1 | Abrams +1.7 |
| Bullet Resilience | vitality 3 | 1 | Baba +3.0 |
| Spirit Strike | spirit 1 | 1 | Bebop +2.0 |
| Hunter's Aura | weapon 3 | 1 | Bebop +1.8 |
| Fleetfoot | weapon 2 | 1 | Drifter +1.6 |
| Indomitable | vitality 4 | 1 | Dynamo +1.6 |
| Weapon Shielding | vitality 2 | 1 | Graves +1.6 |
| Healing Booster | vitality 2 | 1 | Haze +2.5 |
| Recharging Rush | weapon 2 | 1 | Haze +2.5 |
| Mystic Burst | spirit 1 | 1 | Holliday +1.6 |
| Monster Rounds | weapon 1 | 1 | Kelvin +1.9 |
| Sharpshooter | weapon 3 | 1 | Lash +2.1 |
| Long Range | weapon 2 | 1 | Lash +2.0 |
| Stamina Mastery | vitality 3 | 1 | McGinnis +2.3 |
| Rapid Recharge | spirit 3 | 1 | Nurse Harrow +1.5 |
| Lightning Scroll | spirit 4 | 1 | Seven +2.3 |
| Melee Lifesteal | vitality 1 | 1 | Shiv +2.1 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.9 |
| Superior Duration | spirit 3 | 1 | Vindicta +1.9 |
| Surge of Power | spirit 3 | 1 | Violet +2.2 |
| Spellslinger | weapon 4 | 1 | Wraith +3.4 |

## Per hero

### Abrams
- never picked: Frenzy +3.3, Slowing Bullets +2.4, Colossus +1.9, Enduring Speed +1.7, Debuff Reducer +1.7, Duration Extender +1.7, Dispel Magic +1.7, Berserker +1.5

### Apollo
- never picked: Colossus +2.4, Ethereal Shift +1.9

### Baba
- never picked: Bullet Resilience +3.0, Grit +2.9, Mystic Expansion +2.1

### Bebop
- never picked: Mystic Reverb +4.5, Spirit Strike +2.0, Hunter's Aura +1.8

### Billy
- 10k: Spirit Snatch -1.2
- 18k: Spirit Snatch -1.2
- 27k: Spirit Snatch -1.2
- 37k: Spirit Snatch -1.2
- never picked: Dispel Magic +2.1, Mystic Expansion +1.7, Melee Charge +1.5

### Calico
- never picked: Ethereal Shift +3.4, Lucky Shot +2.4, Superior Cooldown +2.4

### Celeste
- 10k: Kinetic Dash -2.6
- 18k: Kinetic Dash -2.6
- 27k: Kinetic Dash -2.6
- 37k: Kinetic Dash -2.6
- 50k: Kinetic Dash -2.6
- never picked: Ethereal Shift +2.6, Dispel Magic +1.9, Superior Cooldown +1.9, Mystic Expansion +1.6

### Deadman Danny
- 27k: Tankbuster -1.1
- 37k: Express Shot -1.1, Tankbuster -1.1
- never picked: Mystic Reverb +3.6, Spirit Lifesteal +2.2, Ethereal Shift +2.1, Spirit Burn +1.5

### Drifter
- 18k: Kinetic Dash -0.8
- 27k: Kinetic Dash -0.8
- 37k: Kinetic Dash -0.8
- 50k: Kinetic Dash -0.8
- never picked: Hollow Point +1.9, Superior Cooldown +1.7, Siphon Bullets +1.6, Fleetfoot +1.6, Spirit Burn +1.6

### Dynamo
- 18k: Rapid Recharge -1.1
- 27k: Rapid Recharge -1.1
- 50k: Rapid Recharge -1.1
- never picked: Healing Tempo +2.0, Indomitable +1.6

### Graves
- never picked: Magic Carpet +3.6, Spirit Lifesteal +2.1, Spiritual Overflow +1.8, Dispel Magic +1.8, Siphon Bullets +1.7, Weapon Shielding +1.6, Silencer +1.6

### Grey Talon
- never picked: Mystic Reverb +2.9, Spirit Lifesteal +2.5, Hollow Point +2.5

### Haze
- 10k: Battle Vest -1.0
- 18k: Kinetic Dash -2.0
- 37k: Kinetic Dash -2.0
- never picked: Healing Tempo +2.7, Healing Booster +2.5, Siphon Bullets +2.5, Recharging Rush +2.5, Extra Spirit +1.9, Sprint Boots +1.9, Silencer +1.6, Spiritual Overflow +1.6

### Holliday
- never picked: Diviner's Kevlar +2.4, Hollow Point +1.7, Mystic Burst +1.6, Dispel Magic +1.5, Grit +1.5, Superior Cooldown +1.5

### Infernus
- 27k: Toxic Bullets -1.1
- 37k: Toxic Bullets -1.1
- 50k: Toxic Bullets -1.1
- never picked: Ethereal Shift +2.9, Spirit Burn +2.7, Silencer +2.4

### Ivy
- never picked: Spirit Burn +2.6, Lucky Shot +1.8

### Kelvin
- 37k: Escalating Exposure -1.2
- 50k: Escalating Exposure -1.2
- never picked: Dispel Magic +2.2, Witchmail +1.9, Monster Rounds +1.9, Duration Extender +1.8

### Lady Geist
- 50k: Escalating Exposure -0.7
- never picked: Warp Stone +4.0, Frenzy +3.0

### Lash
- never picked: Magic Carpet +4.4, Siphon Bullets +2.9, Sharpshooter +2.1, Long Range +2.0

### McGinnis
- never picked: Diviner's Kevlar +3.9, Stamina Mastery +2.3, Healing Tempo +2.1

### Mina
- 18k: Sprint Boots -3.9
- never picked: Ethereal Shift +2.6, Spiritual Overflow +2.1, Spirit Burn +1.6

### Mirage
- never picked: Diviner's Kevlar +3.3

### Mo & Krill
- never picked: Colossus +2.6, Dispel Magic +1.9, Mystic Vulnerability +1.9, Witchmail +1.9

### Nurse Harrow
- never picked: Grit +1.6, Rapid Recharge +1.5

### Paige
- 10k: Guardian Ward -0.8
- 50k: Rapid Recharge -0.7

### Paradox

### Pocket
- never picked: Ethereal Shift +2.9

### Rat King
- never picked: Frenzy +2.8, Mystic Reverb +2.2

### Rem
- never picked: Scourge +2.3, Superior Cooldown +1.5

### Seven
- never picked: Spirit Burn +2.7, Lightning Scroll +2.3

### Shiv
- 50k: Battle Vest -1.1
- never picked: Melee Lifesteal +2.1, Ethereal Shift +2.1, Berserker +1.8

### Silver
- never picked: Slowing Bullets +2.5

### Sinclair
- never picked: Mystic Reverb +2.7, Magic Carpet +2.6

### Solomon
- 10k: Guardian Ward -1.9
- 50k: Boundless Spirit -1.5
- never picked: Magic Carpet +3.3, Mystic Reverb +2.0

### The Doorman
- never picked: Mystic Reverb +3.1

### Venator
- never picked: Frenzy +3.5, Ethereal Shift +2.5

### Victor
- 37k: Escalating Exposure -1.6
- 50k: Escalating Exposure -1.6
- never picked: Witchmail +3.2, Warp Stone +3.1, Scourge +2.4, Ethereal Shift +1.9, Sprint Boots +1.8

### Vindicta
- never picked: Mystic Expansion +3.7, Extended Magazine +2.9, Spirit Burn +2.4, Superior Duration +1.9

### Violet
- never picked: Surge of Power +2.2

### Viscous
- never picked: Mystic Reverb +2.0

### Vyper
- never picked: Extra Spirit +2.8

### Warden
- 10k: Kinetic Dash -4.7
- 27k: Kinetic Dash -4.7
- 37k: Kinetic Dash -4.7
- 50k: Kinetic Dash -4.7
- never picked: Frenzy +3.6, Colossus +3.2, Mystic Vulnerability +1.9, Sprint Boots +1.8, Slowing Bullets +1.8, Witchmail +1.7, Extra Health +1.5

### Wraith
- never picked: Extra Spirit +4.3, Spellslinger +3.4, Silencer +2.1, Spirit Lifesteal +2.1

### Yamato
- 27k: Stalker -1.5
- 37k: Stalker -1.5
- 50k: Stalker -1.5
- never picked: Colossus +3.1, Melee Charge +3.0, Mystic Reverb +2.6, Extra Health +1.8, Berserker +1.5

