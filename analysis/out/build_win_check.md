# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-13, 101,677 Ritualist+ matches (refreshed 2026-11-14T01:47:33Z).

- Recommended item slots with data: 1891; mean edge +0.9 (popular builds +0.2); clearly positive 760, clearly negative 24.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Kinetic Dash | weapon 2 | 9 | Warden -4.5, Haze -2.4, Celeste -2.3 |
| Escalating Exposure | spirit 4 | 4 | Victor -1.7, Kelvin -0.9 |
| Stalker | weapon 2 | 3 | Yamato -1.4 |
| Decay | spirit 3 | 2 | Ivy -2.0 |
| Mystic Shot | weapon 2 | 2 | Lash -1.3 |
| Guardian Ward | vitality 2 | 2 | Solomon -2.3, Paige -0.9 |
| Sprint Boots | vitality 1 | 1 | Mina -4.5 |
| Boundless Spirit | spirit 4 | 1 | Solomon -1.7 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 9 | Calico +3.1, Pocket +3.0, Venator +2.5, Celeste +2.5, Shiv +2.2, Deadman Danny +2.1, Mina +2.1, Apollo +2.0, Victor +2.0 |
| Colossus | vitality 4 | 8 | Warden +3.4, Viscous +3.1, Yamato +3.0, Mo & Krill +2.8, Rat King +2.5, Apollo +2.4, Billy +2.2, Abrams +1.9 |
| Mystic Reverb | spirit 4 | 7 | Deadman Danny +3.4, Grey Talon +3.1, The Doorman +3.1, Sinclair +2.7, Yamato +2.6, Viscous +2.2, Solomon +2.0 |
| Frenzy | weapon 4 | 6 | Venator +3.8, Abrams +3.6, Warden +3.3, Lady Geist +3.0, Rat King +2.8, Billy +2.1 |
| Spirit Burn | spirit 4 | 5 | Infernus +3.4, Ivy +2.5, Vindicta +2.5, Nurse Harrow +2.1, Drifter +1.5 |
| Duration Extender | spirit 2 | 4 | Abrams +1.8, Silver +1.8, Drifter +1.6, Kelvin +1.6 |
| Dispel Magic | vitality 3 | 4 | Kelvin +1.8, Mo & Krill +1.7, Abrams +1.6, Venator +1.5 |
| Mystic Expansion | spirit 1 | 4 | Lady Geist +3.0, Baba +1.9, Billy +1.9, Celeste +1.5 |
| Siphon Bullets | vitality 4 | 4 | Haze +2.5, Lash +2.3, Drifter +1.9, Graves +1.6 |
| Magic Carpet | spirit 4 | 4 | Lash +4.4, Graves +4.2, Solomon +2.9, Sinclair +2.5 |
| Spirit Lifesteal | vitality 2 | 4 | Vyper +3.0, Grey Talon +2.5, Mina +2.4, Graves +2.3 |
| Witchmail | vitality 4 | 4 | Mo & Krill +1.9, Kelvin +1.9, Lady Geist +1.8, Warden +1.5 |
| Berserker | weapon 3 | 3 | Shiv +1.9, Yamato +1.8, Abrams +1.6 |
| Extra Health | vitality 1 | 3 | Warden +1.7, Yamato +1.6, Billy +1.5 |
| Superior Cooldown | spirit 3 | 3 | Shiv +2.2, Celeste +2.1, Calico +1.9 |
| Scourge | spirit 4 | 3 | Graves +2.5, Rem +2.0, Victor +1.9 |
| Silencer | weapon 4 | 3 | Graves +2.1, Infernus +2.0, Wraith +1.9 |
| Extra Spirit | spirit 1 | 3 | Wraith +3.7, Graves +1.9, Haze +1.6 |
| Grit | vitality 1 | 3 | Ivy +2.0, Graves +1.7, Wraith +1.6 |
| Diviner's Kevlar | vitality 4 | 3 | Mirage +3.2, Holliday +2.5, Sinclair +1.9 |
| Surge of Power | spirit 3 | 3 | Vyper +2.6, Violet +2.5, Sinclair +2.5 |
| Debuff Reducer | vitality 2 | 2 | Abrams +2.0, Silver +1.9 |
| Spirit Strike | spirit 1 | 2 | Bebop +2.1, Baba +1.6 |
| Healing Tempo | vitality 4 | 2 | Haze +2.4, McGinnis +2.0 |
| Sprint Boots | vitality 1 | 2 | Haze +2.1, Warden +1.8 |
| Monster Rounds | weapon 1 | 2 | Kelvin +1.8, Seven +1.8 |
| Warp Stone | vitality 3 | 2 | Lady Geist +3.8, Victor +3.1 |
| Spirit Shredder | weapon 2 | 2 | Wraith +2.1, Mina +1.5 |
| Slowing Bullets | weapon 2 | 2 | Silver +2.4, Warden +1.8 |
| Fleetfoot | weapon 2 | 2 | Victor +2.7, Vyper +1.7 |
| Enduring Speed | vitality 2 | 1 | Abrams +1.5 |
| Hunter's Aura | weapon 3 | 1 | Bebop +1.7 |
| Hollow Point | weapon 3 | 1 | Drifter +1.6 |
| Indomitable | vitality 4 | 1 | Dynamo +1.6 |
| Rapid Recharge | spirit 3 | 1 | Haze +3.5 |
| Mercurial Magnum | spirit 4 | 1 | Haze +1.7 |
| Lucky Shot | weapon 4 | 1 | Ivy +2.0 |
| Mystic Burst | spirit 1 | 1 | Lady Geist +2.0 |
| Stamina Mastery | vitality 3 | 1 | McGinnis +2.0 |
| Mystic Vulnerability | spirit 2 | 1 | Mo & Krill +1.8 |
| Lightning Scroll | spirit 4 | 1 | Seven +2.3 |
| Superior Duration | spirit 3 | 1 | Silver +2.7 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.6 |
| Spellslinger | weapon 4 | 1 | Wraith +2.5 |

## Per hero

### Abrams
- never picked: Frenzy +3.6, Debuff Reducer +2.0, Colossus +1.9, Duration Extender +1.8, Dispel Magic +1.6, Berserker +1.6, Enduring Speed +1.5

### Apollo
- never picked: Colossus +2.4, Ethereal Shift +2.0

### Baba
- never picked: Mystic Expansion +1.9, Spirit Strike +1.6

### Bebop
- never picked: Spirit Strike +2.1, Hunter's Aura +1.7

### Billy
- never picked: Colossus +2.2, Frenzy +2.1, Mystic Expansion +1.9, Extra Health +1.5

### Calico
- never picked: Ethereal Shift +3.1, Superior Cooldown +1.9

### Celeste
- 27k: Kinetic Dash -2.3
- 37k: Kinetic Dash -2.3
- 50k: Kinetic Dash -2.3
- never picked: Ethereal Shift +2.5, Superior Cooldown +2.1, Mystic Expansion +1.5

### Deadman Danny
- never picked: Mystic Reverb +3.4, Ethereal Shift +2.1

### Drifter
- never picked: Siphon Bullets +1.9, Hollow Point +1.6, Duration Extender +1.6, Spirit Burn +1.5

### Dynamo
- never picked: Indomitable +1.6

### Graves
- never picked: Magic Carpet +4.2, Scourge +2.5, Spirit Lifesteal +2.3, Silencer +2.1, Extra Spirit +1.9, Grit +1.7, Siphon Bullets +1.6

### Grey Talon
- never picked: Mystic Reverb +3.1, Spirit Lifesteal +2.5

### Haze
- 18k: Kinetic Dash -2.4
- 27k: Kinetic Dash -2.4
- 37k: Kinetic Dash -2.4
- never picked: Rapid Recharge +3.5, Siphon Bullets +2.5, Healing Tempo +2.4, Sprint Boots +2.1, Mercurial Magnum +1.7, Extra Spirit +1.6

### Holliday
- never picked: Diviner's Kevlar +2.5

### Infernus
- never picked: Spirit Burn +3.4, Silencer +2.0

### Ivy
- 27k: Decay -2.0
- 37k: Decay -2.0
- never picked: Spirit Burn +2.5, Grit +2.0, Lucky Shot +2.0

### Kelvin
- 37k: Escalating Exposure -0.9
- 50k: Escalating Exposure -0.9
- never picked: Witchmail +1.9, Dispel Magic +1.8, Monster Rounds +1.8, Duration Extender +1.6

### Lady Geist
- never picked: Warp Stone +3.8, Frenzy +3.0, Mystic Expansion +3.0, Mystic Burst +2.0, Witchmail +1.8

### Lash
- 18k: Mystic Shot -1.3
- 27k: Mystic Shot -1.3
- never picked: Magic Carpet +4.4, Siphon Bullets +2.3

### McGinnis
- never picked: Stamina Mastery +2.0, Healing Tempo +2.0

### Mina
- 37k: Sprint Boots -4.5
- never picked: Spirit Lifesteal +2.4, Ethereal Shift +2.1, Spirit Shredder +1.5

### Mirage
- never picked: Diviner's Kevlar +3.2

### Mo & Krill
- never picked: Colossus +2.8, Witchmail +1.9, Mystic Vulnerability +1.8, Dispel Magic +1.7

### Nurse Harrow
- never picked: Spirit Burn +2.1

### Paige
- 10k: Guardian Ward -0.9

### Paradox

### Pocket
- never picked: Ethereal Shift +3.0

### Rat King
- never picked: Frenzy +2.8, Colossus +2.5

### Rem
- never picked: Scourge +2.0

### Seven
- never picked: Lightning Scroll +2.3, Monster Rounds +1.8

### Shiv
- never picked: Ethereal Shift +2.2, Superior Cooldown +2.2, Berserker +1.9

### Silver
- never picked: Superior Duration +2.7, Slowing Bullets +2.4, Debuff Reducer +1.9, Duration Extender +1.8

### Sinclair
- never picked: Mystic Reverb +2.7, Magic Carpet +2.5, Surge of Power +2.5, Diviner's Kevlar +1.9

### Solomon
- 10k: Guardian Ward -2.3
- 50k: Boundless Spirit -1.7
- never picked: Magic Carpet +2.9, Mystic Reverb +2.0

### The Doorman
- never picked: Mystic Reverb +3.1

### Venator
- never picked: Frenzy +3.8, Ethereal Shift +2.5, Dispel Magic +1.5

### Victor
- 37k: Escalating Exposure -1.7
- 50k: Escalating Exposure -1.7
- never picked: Warp Stone +3.1, Fleetfoot +2.7, Ethereal Shift +2.0, Scourge +1.9

### Vindicta
- never picked: Extended Magazine +2.6, Spirit Burn +2.5

### Violet
- never picked: Surge of Power +2.5

### Viscous
- never picked: Colossus +3.1, Mystic Reverb +2.2

### Vyper
- never picked: Spirit Lifesteal +3.0, Surge of Power +2.6, Fleetfoot +1.7

### Warden
- 10k: Kinetic Dash -4.5
- 27k: Kinetic Dash -4.5
- 37k: Kinetic Dash -4.5
- never picked: Colossus +3.4, Frenzy +3.3, Slowing Bullets +1.8, Sprint Boots +1.8, Extra Health +1.7, Witchmail +1.5

### Wraith
- never picked: Extra Spirit +3.7, Spellslinger +2.5, Spirit Shredder +2.1, Silencer +1.9, Grit +1.6

### Yamato
- 27k: Stalker -1.4
- 37k: Stalker -1.4
- 50k: Stalker -1.4
- never picked: Colossus +3.0, Mystic Reverb +2.6, Berserker +1.8, Extra Health +1.6

