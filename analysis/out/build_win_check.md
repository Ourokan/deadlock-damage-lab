# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-08, 65,534 Ritualist+ matches (refreshed 2026-11-09T19:16:59Z).

- Recommended item slots with data: 1862; mean edge +1.2 (popular builds +0.1); clearly positive 966, clearly negative 13.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 9 | Victor -4.4, Mo & Krill -4.1, Kelvin -1.8, Paige -1.2 |
| Kinetic Dash | weapon 2 | 2 | Warden -3.5, Celeste -1.8 |
| Escalating Exposure | spirit 4 | 2 | Victor -1.4 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 11 | Pocket +3.1, Calico +2.8, Deadman Danny +2.8, Apollo +2.7, Silver +2.6, Venator +2.5, Drifter +2.4, Celeste +2.4, Mina +2.4, Victor +2.1, Shiv +2.0 |
| Sprint Boots | vitality 1 | 5 | Kelvin +2.6, Lady Geist +2.1, Haze +2.1, Ivy +1.8, Warden +1.8 |
| Duration Extender | spirit 2 | 4 | Abrams +1.8, Kelvin +1.8, Apollo +1.7, Drifter +1.7 |
| Colossus | vitality 4 | 3 | Viscous +3.0, Warden +2.5, Mo & Krill +2.4 |
| Grit | vitality 1 | 2 | Baba +2.8, Deadman Danny +2.3 |
| Lucky Shot | weapon 4 | 2 | Ivy +2.8, Calico +2.2 |
| Siphon Bullets | vitality 4 | 2 | Drifter +1.9, Venator +1.6 |
| Fleetfoot | weapon 2 | 2 | Warden +2.0, Haze +1.7 |
| Warp Stone | vitality 3 | 2 | Victor +2.7, Lady Geist +2.3 |
| Magic Carpet | spirit 4 | 2 | Lash +3.6, Solomon +2.8 |
| Mystic Reverb | spirit 4 | 2 | Sinclair +2.5, Rat King +2.1 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.1 |
| Extra Spirit | spirit 1 | 1 | Haze +1.5 |
| Superior Cooldown | spirit 3 | 1 | Ivy +1.7 |
| Mystic Expansion | spirit 1 | 1 | Lady Geist +2.1 |
| Compress Cooldown | spirit 2 | 1 | Lady Geist +1.8 |
| Stamina Mastery | vitality 3 | 1 | McGinnis +1.9 |
| Dispel Magic | vitality 3 | 1 | Mo & Krill +1.6 |
| Monster Rounds | weapon 1 | 1 | Seven +1.7 |
| Enduring Speed | vitality 2 | 1 | Shiv +1.6 |
| Spirit Burn | spirit 4 | 1 | Vindicta +2.3 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.1 |
| Lifestrike | vitality 3 | 1 | Viscous +2.6 |
| Witchmail | vitality 4 | 1 | Warden +1.7 |

## Per hero

### Abrams
- never picked: Duration Extender +1.8

### Apollo
- never picked: Ethereal Shift +2.7, Duration Extender +1.7

### Baba
- never picked: Grit +2.8

### Bebop

### Billy

### Calico
- never picked: Ethereal Shift +2.8, Lucky Shot +2.2

### Celeste
- 27k: Kinetic Dash -1.8
- never picked: Ethereal Shift +2.4

### Deadman Danny
- never picked: Ethereal Shift +2.8, Grit +2.3

### Drifter
- never picked: Ethereal Shift +2.4, Siphon Bullets +1.9, Duration Extender +1.7

### Dynamo

### Graves

### Grey Talon

### Haze
- never picked: Rapid Recharge +2.1, Sprint Boots +2.1, Fleetfoot +1.7, Extra Spirit +1.5

### Holliday

### Infernus

### Ivy
- never picked: Lucky Shot +2.8, Sprint Boots +1.8, Superior Cooldown +1.7

### Kelvin
- 18k: Arcane Surge -1.8
- 50k: Arcane Surge -1.8
- never picked: Sprint Boots +2.6, Duration Extender +1.8

### Lady Geist
- never picked: Warp Stone +2.3, Mystic Expansion +2.1, Sprint Boots +2.1, Compress Cooldown +1.8

### Lash
- never picked: Magic Carpet +3.6

### McGinnis
- never picked: Stamina Mastery +1.9

### Mina
- never picked: Ethereal Shift +2.4

### Mirage

### Mo & Krill
- 37k: Arcane Surge -4.1
- 50k: Arcane Surge -4.1
- never picked: Colossus +2.4, Dispel Magic +1.6

### Nurse Harrow

### Paige
- 18k: Arcane Surge -1.2
- 27k: Arcane Surge -1.2
- 37k: Arcane Surge -1.2
- 50k: Arcane Surge -1.2

### Paradox

### Pocket
- never picked: Ethereal Shift +3.1

### Rat King
- never picked: Mystic Reverb +2.1

### Rem

### Seven
- never picked: Monster Rounds +1.7

### Shiv
- never picked: Ethereal Shift +2.0, Enduring Speed +1.6

### Silver
- never picked: Ethereal Shift +2.6

### Sinclair
- never picked: Mystic Reverb +2.5

### Solomon
- never picked: Magic Carpet +2.8

### The Doorman

### Venator
- never picked: Ethereal Shift +2.5, Siphon Bullets +1.6

### Victor
- 37k: Arcane Surge -4.4, Escalating Exposure -1.4
- 50k: Escalating Exposure -1.4
- never picked: Warp Stone +2.7, Ethereal Shift +2.1

### Vindicta
- never picked: Spirit Burn +2.3, Extended Magazine +2.1

### Violet

### Viscous
- never picked: Colossus +3.0, Lifestrike +2.6

### Vyper

### Warden
- 27k: Kinetic Dash -3.5
- never picked: Colossus +2.5, Fleetfoot +2.0, Sprint Boots +1.8, Witchmail +1.7

### Wraith

### Yamato

