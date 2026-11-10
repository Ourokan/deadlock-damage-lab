# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-09, 72,940 Ritualist+ matches (refreshed 2026-11-10T20:13:51Z).

- Recommended item slots with data: 1892; mean edge +1.3 (popular builds +0.1); clearly positive 1024, clearly negative 9.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Kinetic Dash | weapon 2 | 8 | Holliday -4.5, Warden -4.0, Celeste -1.9, Haze -1.6 |
| Escalating Exposure | spirit 4 | 1 | Shiv -1.1 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 11 | Paradox +4.0, Pocket +2.9, Deadman Danny +2.8, Celeste +2.6, Calico +2.5, Silver +2.5, Venator +2.4, Mina +2.4, Apollo +2.2, Victor +1.9, Shiv +1.8 |
| Duration Extender | spirit 2 | 3 | Kelvin +1.9, Abrams +1.8, Drifter +1.7 |
| Mystic Expansion | spirit 1 | 3 | Lady Geist +2.8, Baba +1.8, Celeste +1.6 |
| Lucky Shot | weapon 4 | 3 | Ivy +2.4, Calico +2.2, Holliday +1.8 |
| Grit | vitality 1 | 2 | Baba +2.7, Deadman Danny +2.0 |
| Siphon Bullets | vitality 4 | 2 | Drifter +2.1, Venator +1.8 |
| Warp Stone | vitality 3 | 2 | Lady Geist +3.1, Victor +2.7 |
| Magic Carpet | spirit 4 | 2 | Lash +4.3, Solomon +3.0 |
| Mystic Reverb | spirit 4 | 2 | Sinclair +2.3, Shiv +1.5 |
| Enduring Speed | vitality 2 | 1 | Abrams +1.7 |
| Spirit Strike | spirit 1 | 1 | Drifter +1.6 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.6 |
| Stamina Mastery | vitality 3 | 1 | McGinnis +1.9 |
| Dispel Magic | vitality 3 | 1 | Mo & Krill +1.7 |
| Monster Rounds | weapon 1 | 1 | Seven +1.8 |
| Lightning Scroll | spirit 4 | 1 | Seven +1.7 |
| Berserker | weapon 3 | 1 | Shiv +1.5 |
| Spirit Burn | spirit 4 | 1 | Vindicta +2.4 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.1 |
| Lifestrike | vitality 3 | 1 | Viscous +3.0 |
| Fleetfoot | weapon 2 | 1 | Warden +1.9 |
| Witchmail | vitality 4 | 1 | Warden +1.8 |
| Sprint Boots | vitality 1 | 1 | Warden +1.7 |
| Spellslinger | weapon 4 | 1 | Wraith +2.4 |
| Silencer | weapon 4 | 1 | Wraith +1.9 |

## Per hero

### Abrams
- never picked: Duration Extender +1.8, Enduring Speed +1.7

### Apollo
- never picked: Ethereal Shift +2.2

### Baba
- never picked: Grit +2.7, Mystic Expansion +1.8

### Bebop

### Billy

### Calico
- never picked: Ethereal Shift +2.5, Lucky Shot +2.2

### Celeste
- 18k: Kinetic Dash -1.9
- 27k: Kinetic Dash -1.9
- 50k: Kinetic Dash -1.9
- never picked: Ethereal Shift +2.6, Mystic Expansion +1.6

### Deadman Danny
- never picked: Ethereal Shift +2.8, Grit +2.0

### Drifter
- never picked: Siphon Bullets +2.1, Duration Extender +1.7, Spirit Strike +1.6

### Dynamo

### Graves

### Grey Talon

### Haze
- 37k: Kinetic Dash -1.6
- never picked: Rapid Recharge +2.6

### Holliday
- 27k: Kinetic Dash -4.5
- 50k: Kinetic Dash -4.5
- never picked: Lucky Shot +1.8

### Infernus

### Ivy
- never picked: Lucky Shot +2.4

### Kelvin
- never picked: Duration Extender +1.9

### Lady Geist
- never picked: Warp Stone +3.1, Mystic Expansion +2.8

### Lash
- never picked: Magic Carpet +4.3

### McGinnis
- never picked: Stamina Mastery +1.9

### Mina
- never picked: Ethereal Shift +2.4

### Mirage

### Mo & Krill
- never picked: Dispel Magic +1.7

### Nurse Harrow

### Paige

### Paradox
- never picked: Ethereal Shift +4.0

### Pocket
- never picked: Ethereal Shift +2.9

### Rat King

### Rem

### Seven
- never picked: Monster Rounds +1.8, Lightning Scroll +1.7

### Shiv
- 50k: Escalating Exposure -1.1
- never picked: Ethereal Shift +1.8, Berserker +1.5, Mystic Reverb +1.5

### Silver
- never picked: Ethereal Shift +2.5

### Sinclair
- never picked: Mystic Reverb +2.3

### Solomon
- never picked: Magic Carpet +3.0

### The Doorman

### Venator
- never picked: Ethereal Shift +2.4, Siphon Bullets +1.8

### Victor
- never picked: Warp Stone +2.7, Ethereal Shift +1.9

### Vindicta
- never picked: Spirit Burn +2.4, Extended Magazine +2.1

### Violet

### Viscous
- never picked: Lifestrike +3.0

### Vyper

### Warden
- 27k: Kinetic Dash -4.0
- 37k: Kinetic Dash -4.0
- never picked: Fleetfoot +1.9, Witchmail +1.8, Sprint Boots +1.7

### Wraith
- never picked: Spellslinger +2.4, Silencer +1.9

### Yamato

