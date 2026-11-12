# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-10, 80,471 Ritualist+ matches (refreshed 2026-11-12T19:10:22Z).

- Recommended item slots with data: 1878; mean edge +0.8 (popular builds +0.1); clearly positive 690, clearly negative 17.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Kinetic Dash | weapon 2 | 10 | Warden -4.5, Seven -4.2, Celeste -2.0, Haze -1.8 |
| Escalating Exposure | spirit 4 | 5 | Victor -1.7, Kelvin -1.2 |
| Boundless Spirit | spirit 4 | 1 | Apollo -1.7 |
| Guardian Ward | vitality 2 | 1 | Solomon -2.3 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 9 | Pocket +2.8, Deadman Danny +2.6, Celeste +2.5, Calico +2.5, Venator +2.4, Mina +2.1, Apollo +2.0, Victor +1.8, Shiv +1.7 |
| Mystic Reverb | spirit 4 | 7 | Bebop +4.4, Deadman Danny +3.6, Grey Talon +2.8, Sinclair +2.5, Yamato +2.3, Viscous +2.3, Shiv +1.6 |
| Colossus | vitality 4 | 6 | Yamato +3.2, Viscous +3.2, Mo & Krill +3.0, Warden +2.9, Apollo +2.7, Abrams +2.0 |
| Spirit Burn | spirit 4 | 6 | Infernus +3.4, Ivy +2.7, Vindicta +2.4, Graves +2.3, Mina +1.6, Drifter +1.5 |
| Berserker | weapon 3 | 4 | Yamato +1.8, Billy +1.7, Shiv +1.7, Abrams +1.6 |
| Dispel Magic | vitality 3 | 4 | Mo & Krill +2.0, Kelvin +1.8, Billy +1.7, Yamato +1.6 |
| Magic Carpet | spirit 4 | 4 | Lash +4.2, Graves +3.9, Solomon +2.8, Sinclair +1.9 |
| Silencer | weapon 4 | 4 | Graves +2.1, Wraith +1.9, Haze +1.7, Vyper +1.6 |
| Frenzy | weapon 4 | 4 | Venator +3.3, Lady Geist +2.9, Warden +2.7, Rat King +2.1 |
| Lucky Shot | weapon 4 | 3 | Calico +2.3, Ivy +2.0, Venator +1.7 |
| Superior Cooldown | spirit 3 | 3 | Celeste +2.2, Calico +1.9, Drifter +1.6 |
| Grit | vitality 1 | 3 | Deadman Danny +1.9, Drifter +1.9, Graves +1.7 |
| Spirit Lifesteal | vitality 2 | 3 | Wraith +1.9, Shiv +1.8, Deadman Danny +1.6 |
| Siphon Bullets | vitality 4 | 3 | Haze +2.6, Drifter +2.3, Lash +2.0 |
| Scourge | spirit 4 | 3 | Graves +2.7, Victor +2.1, Rem +2.0 |
| Extra Spirit | spirit 1 | 3 | Wraith +3.2, Vyper +2.4, Graves +1.7 |
| Witchmail | vitality 4 | 3 | Victor +3.1, Mo & Krill +2.1, Warden +1.6 |
| Debuff Reducer | vitality 2 | 2 | Abrams +2.3, Billy +1.6 |
| Duration Extender | spirit 2 | 2 | Abrams +1.9, Kelvin +1.8 |
| Mystic Expansion | spirit 1 | 2 | Baba +2.0, Celeste +1.5 |
| Extra Health | vitality 1 | 2 | Warden +1.8, Bebop +1.8 |
| Melee Charge | weapon 2 | 2 | Yamato +2.6, Billy +1.6 |
| Warp Stone | vitality 3 | 2 | Lady Geist +3.1, Victor +2.7 |
| Sprint Boots | vitality 1 | 2 | Warden +1.8, Mo & Krill +1.6 |
| Slowing Bullets | weapon 2 | 2 | Silver +1.7, Warden +1.6 |
| Spirit Strike | spirit 1 | 1 | Bebop +2.1 |
| Hunter's Aura | weapon 3 | 1 | Bebop +1.5 |
| Spiritual Overflow | weapon 4 | 1 | Graves +1.6 |
| Recharging Rush | weapon 2 | 1 | Haze +3.0 |
| Rapid Recharge | spirit 3 | 1 | Haze +3.0 |
| Diviner's Kevlar | vitality 4 | 1 | Holliday +2.6 |
| Compress Cooldown | spirit 2 | 1 | Lady Geist +1.9 |
| Extra Stamina | vitality 1 | 1 | Lash +1.5 |
| Stamina Mastery | vitality 3 | 1 | McGinnis +2.2 |
| Mystic Vulnerability | spirit 2 | 1 | Mo & Krill +1.5 |
| Lightning Scroll | spirit 4 | 1 | Seven +1.9 |
| Monster Rounds | weapon 1 | 1 | Seven +1.7 |
| Fleetfoot | weapon 2 | 1 | Victor +2.4 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.3 |
| Bullet Lifesteal | vitality 2 | 1 | Vindicta +2.0 |
| Surge of Power | spirit 3 | 1 | Violet +2.4 |
| Lifestrike | vitality 3 | 1 | Viscous +3.2 |
| Quicksilver Reload | spirit 2 | 1 | Warden +2.4 |
| Spellslinger | weapon 4 | 1 | Wraith +2.2 |
| Tesla Bullets | weapon 3 | 1 | Wraith +1.9 |

## Per hero

### Abrams
- never picked: Debuff Reducer +2.3, Colossus +2.0, Duration Extender +1.9, Berserker +1.6

### Apollo
- 50k: Boundless Spirit -1.7
- never picked: Colossus +2.7, Ethereal Shift +2.0

### Baba
- never picked: Mystic Expansion +2.0

### Bebop
- never picked: Mystic Reverb +4.4, Spirit Strike +2.1, Extra Health +1.8, Hunter's Aura +1.5

### Billy
- never picked: Berserker +1.7, Dispel Magic +1.7, Debuff Reducer +1.6, Melee Charge +1.6

### Calico
- never picked: Ethereal Shift +2.5, Lucky Shot +2.3, Superior Cooldown +1.9

### Celeste
- 18k: Kinetic Dash -2.0
- 27k: Kinetic Dash -2.0
- never picked: Ethereal Shift +2.5, Superior Cooldown +2.2, Mystic Expansion +1.5

### Deadman Danny
- never picked: Mystic Reverb +3.6, Ethereal Shift +2.6, Grit +1.9, Spirit Lifesteal +1.6

### Drifter
- never picked: Siphon Bullets +2.3, Grit +1.9, Superior Cooldown +1.6, Spirit Burn +1.5

### Dynamo

### Graves
- never picked: Magic Carpet +3.9, Scourge +2.7, Spirit Burn +2.3, Silencer +2.1, Extra Spirit +1.7, Grit +1.7, Spiritual Overflow +1.6

### Grey Talon
- never picked: Mystic Reverb +2.8

### Haze
- 18k: Kinetic Dash -1.8
- 27k: Kinetic Dash -1.8
- 37k: Kinetic Dash -1.8
- never picked: Recharging Rush +3.0, Rapid Recharge +3.0, Siphon Bullets +2.6, Silencer +1.7

### Holliday
- never picked: Diviner's Kevlar +2.6

### Infernus
- never picked: Spirit Burn +3.4

### Ivy
- never picked: Spirit Burn +2.7, Lucky Shot +2.0

### Kelvin
- 37k: Escalating Exposure -1.2
- 50k: Escalating Exposure -1.2
- never picked: Dispel Magic +1.8, Duration Extender +1.8

### Lady Geist
- never picked: Warp Stone +3.1, Frenzy +2.9, Compress Cooldown +1.9

### Lash
- never picked: Magic Carpet +4.2, Siphon Bullets +2.0, Extra Stamina +1.5

### McGinnis
- never picked: Stamina Mastery +2.2

### Mina
- never picked: Ethereal Shift +2.1, Spirit Burn +1.6

### Mirage

### Mo & Krill
- never picked: Colossus +3.0, Witchmail +2.1, Dispel Magic +2.0, Sprint Boots +1.6, Mystic Vulnerability +1.5

### Nurse Harrow

### Paige

### Paradox

### Pocket
- never picked: Ethereal Shift +2.8

### Rat King
- never picked: Frenzy +2.1

### Rem
- never picked: Scourge +2.0

### Seven
- 27k: Kinetic Dash -4.2
- 37k: Kinetic Dash -4.2
- 50k: Kinetic Dash -4.2
- never picked: Lightning Scroll +1.9, Monster Rounds +1.7

### Shiv
- never picked: Spirit Lifesteal +1.8, Ethereal Shift +1.7, Berserker +1.7, Mystic Reverb +1.6

### Silver
- never picked: Slowing Bullets +1.7

### Sinclair
- never picked: Mystic Reverb +2.5, Magic Carpet +1.9

### Solomon
- 10k: Guardian Ward -2.3
- never picked: Magic Carpet +2.8

### The Doorman

### Venator
- never picked: Frenzy +3.3, Ethereal Shift +2.4, Lucky Shot +1.7

### Victor
- 27k: Escalating Exposure -1.7
- 37k: Escalating Exposure -1.7
- 50k: Escalating Exposure -1.7
- never picked: Witchmail +3.1, Warp Stone +2.7, Fleetfoot +2.4, Scourge +2.1, Ethereal Shift +1.8

### Vindicta
- never picked: Spirit Burn +2.4, Extended Magazine +2.3, Bullet Lifesteal +2.0

### Violet
- never picked: Surge of Power +2.4

### Viscous
- never picked: Lifestrike +3.2, Colossus +3.2, Mystic Reverb +2.3

### Vyper
- never picked: Extra Spirit +2.4, Silencer +1.6

### Warden
- 27k: Kinetic Dash -4.5
- 37k: Kinetic Dash -4.5
- never picked: Colossus +2.9, Frenzy +2.7, Quicksilver Reload +2.4, Extra Health +1.8, Sprint Boots +1.8, Witchmail +1.6, Slowing Bullets +1.6

### Wraith
- never picked: Extra Spirit +3.2, Spellslinger +2.2, Tesla Bullets +1.9, Spirit Lifesteal +1.9, Silencer +1.9

### Yamato
- never picked: Colossus +3.2, Melee Charge +2.6, Mystic Reverb +2.3, Berserker +1.8, Dispel Magic +1.6

