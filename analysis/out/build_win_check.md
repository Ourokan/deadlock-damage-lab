# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-07, 57,326 Ritualist+ matches (refreshed 2026-11-08T20:19:51Z).

- Recommended item slots with data: 1847; mean edge +1.1 (popular builds +0.1); clearly positive 891, clearly negative 3.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Mystic Burst | spirit 1 | 1 | Bebop -1.4 |
| Arcane Surge | spirit 2 | 1 | Kelvin -1.5 |
| Escalating Exposure | spirit 4 | 1 | Victor -1.5 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 12 | Pocket +3.2, Calico +2.9, Deadman Danny +2.7, Drifter +2.6, Apollo +2.6, Mina +2.6, Silver +2.6, Celeste +2.5, Venator +2.4, Victor +2.2, Abrams +2.2, Shiv +1.5 |
| Fleetfoot | weapon 2 | 4 | Warden +2.0, Vyper +1.9, Haze +1.8, Drifter +1.5 |
| Sprint Boots | vitality 1 | 4 | Lady Geist +2.3, Kelvin +2.1, Haze +1.9, Ivy +1.5 |
| Colossus | vitality 4 | 3 | Viscous +2.9, Warden +2.8, Abrams +1.9 |
| Superior Cooldown | spirit 3 | 3 | Drifter +2.1, Bebop +1.6, Ivy +1.5 |
| Lucky Shot | weapon 4 | 3 | Ivy +3.1, Calico +2.1, Paradox +2.1 |
| Duration Extender | spirit 2 | 2 | Kelvin +1.7, Abrams +1.7 |
| Warp Stone | vitality 3 | 2 | Victor +2.6, Lady Geist +1.5 |
| Magic Carpet | spirit 4 | 2 | Lash +3.7, Solomon +2.8 |
| Grit | vitality 1 | 1 | Deadman Danny +2.2 |
| Siphon Bullets | vitality 4 | 1 | Drifter +1.9 |
| Spirit Strike | spirit 1 | 1 | Drifter +1.6 |
| Rapid Recharge | spirit 3 | 1 | Haze +1.8 |
| Frenzy | weapon 4 | 1 | Lady Geist +2.3 |
| Compress Cooldown | spirit 2 | 1 | Lady Geist +1.6 |
| Mystic Reverb | spirit 4 | 1 | Rat King +2.2 |
| Monster Rounds | weapon 1 | 1 | Seven +1.7 |
| Lightning Scroll | spirit 4 | 1 | Seven +1.6 |
| Enduring Speed | vitality 2 | 1 | Shiv +1.5 |
| Spirit Burn | spirit 4 | 1 | Vindicta +1.9 |
| Extended Magazine | weapon 1 | 1 | Vindicta +1.6 |
| Spellslinger | weapon 4 | 1 | Wraith +2.5 |

## Per hero

### Abrams
- never picked: Ethereal Shift +2.2, Colossus +1.9, Duration Extender +1.7

### Apollo
- never picked: Ethereal Shift +2.6

### Baba

### Bebop
- 27k: Mystic Burst -1.4
- never picked: Superior Cooldown +1.6

### Billy

### Calico
- never picked: Ethereal Shift +2.9, Lucky Shot +2.1

### Celeste
- never picked: Ethereal Shift +2.5

### Deadman Danny
- never picked: Ethereal Shift +2.7, Grit +2.2

### Drifter
- never picked: Ethereal Shift +2.6, Superior Cooldown +2.1, Siphon Bullets +1.9, Spirit Strike +1.6, Fleetfoot +1.5

### Dynamo

### Graves

### Grey Talon

### Haze
- never picked: Sprint Boots +1.9, Rapid Recharge +1.8, Fleetfoot +1.8

### Holliday

### Infernus

### Ivy
- never picked: Lucky Shot +3.1, Sprint Boots +1.5, Superior Cooldown +1.5

### Kelvin
- 18k: Arcane Surge -1.5
- never picked: Sprint Boots +2.1, Duration Extender +1.7

### Lady Geist
- never picked: Frenzy +2.3, Sprint Boots +2.3, Compress Cooldown +1.6, Warp Stone +1.5

### Lash
- never picked: Magic Carpet +3.7

### McGinnis

### Mina
- never picked: Ethereal Shift +2.6

### Mirage

### Mo & Krill

### Nurse Harrow

### Paige

### Paradox
- never picked: Lucky Shot +2.1

### Pocket
- never picked: Ethereal Shift +3.2

### Rat King
- never picked: Mystic Reverb +2.2

### Rem

### Seven
- never picked: Monster Rounds +1.7, Lightning Scroll +1.6

### Shiv
- never picked: Ethereal Shift +1.5, Enduring Speed +1.5

### Silver
- never picked: Ethereal Shift +2.6

### Sinclair

### Solomon
- never picked: Magic Carpet +2.8

### The Doorman

### Venator
- never picked: Ethereal Shift +2.4

### Victor
- 50k: Escalating Exposure -1.5
- never picked: Warp Stone +2.6, Ethereal Shift +2.2

### Vindicta
- never picked: Spirit Burn +1.9, Extended Magazine +1.6

### Violet

### Viscous
- never picked: Colossus +2.9

### Vyper
- never picked: Fleetfoot +1.9

### Warden
- never picked: Colossus +2.8, Fleetfoot +2.0

### Wraith
- never picked: Spellslinger +2.5

### Yamato

