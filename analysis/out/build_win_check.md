# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-10-24, 151,478 Ritualist+ matches (refreshed 2026-10-25T11:27:20Z).

- Recommended item slots with data: 1882; mean edge +1.4 (popular builds +0.0); clearly positive 1070, clearly negative 23.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Spirit Snatch | spirit 3 | 10 | Billy -2.2, Apollo -1.4, Abrams -1.1 |
| Stalker | weapon 2 | 4 | Billy -1.8 |
| Fortitude | vitality 3 | 2 | Venator -1.0 |
| Escalating Exposure | spirit 4 | 2 | Victor -1.7 |
| Tankbuster | spirit 3 | 1 | Apollo -0.9 |
| Rapid Recharge | spirit 3 | 1 | Dynamo -1.9 |
| Decay | spirit 3 | 1 | Nurse Harrow -2.2 |
| Unstoppable | vitality 4 | 1 | Pocket -4.0 |
| Toxic Bullets | weapon 3 | 1 | Wraith -1.0 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Witchmail | vitality 4 | 9 | Kelvin +3.3, Warden +3.1, Victor +3.0, Dynamo +3.0, Lash +2.8, Infernus +2.8, Apollo +2.5, Bebop +2.2, Mo & Krill +2.0 |
| Silencer | weapon 4 | 8 | Bebop +3.5, Infernus +3.3, Warden +3.2, Mirage +3.1, Wraith +2.6, Ivy +1.9, Haze +1.9, Graves +1.8 |
| Diviner's Kevlar | vitality 4 | 7 | Rat King +6.8, Deadman Danny +4.7, Shiv +3.5, Venator +3.3, Vyper +3.0, Drifter +2.9, Silver +2.0 |
| Magic Carpet | spirit 4 | 7 | Lash +5.5, Solomon +4.2, Rem +3.9, Sinclair +3.0, Kelvin +3.0, McGinnis +2.9, Graves +2.7 |
| Fleetfoot | weapon 2 | 7 | Seven +2.4, Infernus +2.2, Vindicta +1.9, Vyper +1.7, Warden +1.7, Rat King +1.6, Venator +1.5 |
| Ethereal Shift | spirit 4 | 6 | Paradox +3.1, Pocket +3.1, Mina +2.7, Billy +2.7, Infernus +2.6, Shiv +1.9 |
| Superior Cooldown | spirit 3 | 6 | Drifter +2.3, Yamato +2.2, Calico +2.1, Paradox +1.9, Holliday +1.8, Grey Talon +1.7 |
| Sprint Boots | vitality 1 | 6 | Victor +3.3, Lady Geist +2.5, Kelvin +2.0, Infernus +1.8, Venator +1.7, Wraith +1.6 |
| Colossus | vitality 4 | 4 | Bebop +2.8, Rat King +2.5, Billy +2.0, Abrams +1.9 |
| Frenzy | weapon 4 | 4 | Haze +3.8, Bebop +3.4, Billy +3.2, Rat King +1.7 |
| Spirit Burn | spirit 4 | 4 | The Doorman +2.6, Infernus +2.4, Seven +2.3, Bebop +1.6 |
| Mystic Expansion | spirit 1 | 4 | Kelvin +2.0, Dynamo +1.7, Sinclair +1.7, Celeste +1.6 |
| Duration Extender | spirit 2 | 4 | Rat King +3.5, Silver +2.9, Vindicta +2.3, Drifter +1.7 |
| Cheat Death | vitality 4 | 4 | Solomon +3.4, Kelvin +3.3, Holliday +2.6, Dynamo +2.5 |
| Lucky Shot | weapon 4 | 4 | Vindicta +3.2, Ivy +2.7, Holliday +2.0, Haze +1.5 |
| Slowing Bullets | weapon 2 | 3 | Silver +2.0, Rat King +2.0, Bebop +1.8 |
| Grit | vitality 1 | 3 | Rat King +2.9, Graves +1.9, Deadman Danny +1.7 |
| Spirit Resilience | vitality 3 | 3 | Victor +2.2, Solomon +1.6, Deadman Danny +1.6 |
| Refresher | spirit 4 | 3 | Yamato +2.1, Victor +1.6, Paige +1.6 |
| Enduring Speed | vitality 2 | 2 | Haze +1.5, Billy +1.5 |
| Indomitable | vitality 4 | 2 | Calico +2.2, Lash +2.1 |
| Compress Cooldown | spirit 2 | 2 | Deadman Danny +1.9, Lash +1.8 |
| Mystic Reverb | spirit 4 | 2 | Kelvin +3.0, Drifter +2.6 |
| Healing Tempo | vitality 4 | 2 | Haze +3.3, Dynamo +2.2 |
| Warp Stone | vitality 3 | 2 | Victor +1.9, Infernus +1.8 |
| Extended Magazine | weapon 1 | 2 | Vindicta +2.1, Nurse Harrow +1.5 |
| Lightning Scroll | spirit 4 | 2 | Paige +1.9, Seven +1.5 |
| Scourge | spirit 4 | 2 | Sinclair +2.7, Victor +2.3 |
| Spellslinger | weapon 4 | 2 | Venator +2.3, Vindicta +1.9 |
| Stamina Mastery | vitality 3 | 1 | Apollo +1.6 |
| Spirit Strike | spirit 1 | 1 | Bebop +2.0 |
| Reactive Barrier | vitality 2 | 1 | Calico +1.7 |
| High-Velocity Rounds | weapon 1 | 1 | Deadman Danny +4.7 |
| Toxic Bullets | weapon 3 | 1 | Deadman Danny +2.3 |
| Glass Cannon | weapon 4 | 1 | Drifter +1.9 |
| Transcendent Cooldown | spirit 4 | 1 | Drifter +1.9 |
| Divine Barrier | vitality 4 | 1 | Dynamo +2.2 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.1 |
| Spellbreaker | vitality 4 | 1 | Infernus +2.0 |
| Dispel Magic | vitality 3 | 1 | Ivy +2.4 |
| Swift Striker | weapon 2 | 1 | Ivy +1.6 |
| Infuser | vitality 4 | 1 | Lady Geist +3.2 |
| Arcane Surge | spirit 2 | 1 | Rat King +3.1 |
| Extra Stamina | vitality 1 | 1 | Rat King +3.0 |
| Greater Expansion | spirit 3 | 1 | Rat King +1.9 |
| Monster Rounds | weapon 1 | 1 | Seven +1.8 |
| Phantom Strike | vitality 4 | 1 | Silver +2.6 |
| Long Range | weapon 2 | 1 | Solomon +1.6 |
| Spirit Shredder | weapon 2 | 1 | Solomon +1.5 |
| Siphon Bullets | vitality 4 | 1 | Victor +2.4 |
| Superior Duration | spirit 3 | 1 | Vindicta +2.7 |
| Boundless Spirit | spirit 4 | 1 | Wraith +2.1 |

## Per hero

### Abrams
- 10k: Spirit Snatch -1.1
- 18k: Spirit Snatch -1.1
- 27k: Spirit Snatch -1.1
- 37k: Spirit Snatch -1.1
- 50k: Spirit Snatch -1.1
- never picked: Colossus +1.9

### Apollo
- 27k: Spirit Snatch -1.4
- 50k: Tankbuster -0.9, Spirit Snatch -1.4
- never picked: Witchmail +2.5, Stamina Mastery +1.6

### Bebop
- never picked: Silencer +3.5, Frenzy +3.4, Colossus +2.8, Witchmail +2.2, Spirit Strike +2.0, Slowing Bullets +1.8, Spirit Burn +1.6

### Billy
- 10k: Spirit Snatch -2.2
- 18k: Stalker -1.8, Spirit Snatch -2.2
- 27k: Stalker -1.8, Spirit Snatch -2.2
- 37k: Stalker -1.8
- 50k: Stalker -1.8
- never picked: Frenzy +3.2, Ethereal Shift +2.7, Colossus +2.0, Enduring Speed +1.5

### Calico
- never picked: Indomitable +2.2, Superior Cooldown +2.1, Reactive Barrier +1.7

### Celeste
- never picked: Mystic Expansion +1.6

### Deadman Danny
- never picked: Diviner's Kevlar +4.7, High-Velocity Rounds +4.7, Toxic Bullets +2.3, Compress Cooldown +1.9, Grit +1.7, Spirit Resilience +1.6

### Drifter
- never picked: Diviner's Kevlar +2.9, Mystic Reverb +2.6, Superior Cooldown +2.3, Glass Cannon +1.9, Transcendent Cooldown +1.9, Duration Extender +1.7

### Dynamo
- 27k: Rapid Recharge -1.9
- never picked: Witchmail +3.0, Cheat Death +2.5, Divine Barrier +2.2, Healing Tempo +2.2, Mystic Expansion +1.7

### Graves
- never picked: Magic Carpet +2.7, Grit +1.9, Silencer +1.8

### Grey Talon
- never picked: Superior Cooldown +1.7

### Haze
- never picked: Frenzy +3.8, Healing Tempo +3.3, Rapid Recharge +2.1, Silencer +1.9, Enduring Speed +1.5, Lucky Shot +1.5

### Holliday
- never picked: Cheat Death +2.6, Lucky Shot +2.0, Superior Cooldown +1.8

### Infernus
- never picked: Silencer +3.3, Witchmail +2.8, Ethereal Shift +2.6, Spirit Burn +2.4, Fleetfoot +2.2, Spellbreaker +2.0, Sprint Boots +1.8, Warp Stone +1.8

### Ivy
- never picked: Lucky Shot +2.7, Dispel Magic +2.4, Silencer +1.9, Swift Striker +1.6

### Kelvin
- never picked: Cheat Death +3.3, Witchmail +3.3, Mystic Reverb +3.0, Magic Carpet +3.0, Sprint Boots +2.0, Mystic Expansion +2.0

### Lady Geist
- never picked: Infuser +3.2, Sprint Boots +2.5

### Lash
- never picked: Magic Carpet +5.5, Witchmail +2.8, Indomitable +2.1, Compress Cooldown +1.8

### McGinnis
- never picked: Magic Carpet +2.9

### Mina
- never picked: Ethereal Shift +2.7

### Mirage
- never picked: Silencer +3.1

### Mo & Krill
- never picked: Witchmail +2.0

### Nurse Harrow
- 37k: Decay -2.2
- never picked: Extended Magazine +1.5

### Paige
- never picked: Lightning Scroll +1.9, Refresher +1.6

### Paradox
- never picked: Ethereal Shift +3.1, Superior Cooldown +1.9

### Pocket
- 50k: Unstoppable -4.0
- never picked: Ethereal Shift +3.1

### Rat King
- never picked: Diviner's Kevlar +6.8, Duration Extender +3.5, Arcane Surge +3.1, Extra Stamina +3.0, Grit +2.9, Colossus +2.5, Slowing Bullets +2.0, Greater Expansion +1.9

### Rem
- never picked: Magic Carpet +3.9

### Seven
- never picked: Fleetfoot +2.4, Spirit Burn +2.3, Monster Rounds +1.8, Lightning Scroll +1.5

### Shiv
- never picked: Diviner's Kevlar +3.5, Ethereal Shift +1.9

### Silver
- never picked: Duration Extender +2.9, Phantom Strike +2.6, Slowing Bullets +2.0, Diviner's Kevlar +2.0

### Sinclair
- never picked: Magic Carpet +3.0, Scourge +2.7, Mystic Expansion +1.7

### Solomon
- never picked: Magic Carpet +4.2, Cheat Death +3.4, Spirit Resilience +1.6, Long Range +1.6, Spirit Shredder +1.5

### The Doorman
- never picked: Spirit Burn +2.6

### Venator
- 18k: Fortitude -1.0
- 27k: Fortitude -1.0
- never picked: Diviner's Kevlar +3.3, Spellslinger +2.3, Sprint Boots +1.7, Fleetfoot +1.5

### Victor
- 37k: Escalating Exposure -1.7
- 50k: Escalating Exposure -1.7
- never picked: Sprint Boots +3.3, Witchmail +3.0, Siphon Bullets +2.4, Scourge +2.3, Spirit Resilience +2.2, Warp Stone +1.9, Refresher +1.6

### Vindicta
- never picked: Lucky Shot +3.2, Superior Duration +2.7, Duration Extender +2.3, Extended Magazine +2.1, Spellslinger +1.9, Fleetfoot +1.9

### Viscous

### Vyper
- never picked: Diviner's Kevlar +3.0, Fleetfoot +1.7

### Warden
- never picked: Silencer +3.2, Witchmail +3.1, Fleetfoot +1.7

### Wraith
- 50k: Toxic Bullets -1.0
- never picked: Silencer +2.6, Boundless Spirit +2.1, Sprint Boots +1.6

### Yamato
- never picked: Superior Cooldown +2.2, Refresher +2.1

