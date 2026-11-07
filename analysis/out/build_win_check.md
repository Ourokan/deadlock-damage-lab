# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-05, 41,449 Ritualist+ matches (refreshed 2026-11-07T09:19:29Z).

- Recommended item slots with data: 1827; mean edge +0.8 (popular builds +0.1); clearly positive 757, clearly negative 4.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 4 | Paige -1.6 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 8 | Pocket +3.0, Drifter +2.4, Apollo +2.3, Celeste +2.2, Silver +2.2, Mina +2.2, Deadman Danny +2.1, Victor +1.9 |
| Fleetfoot | weapon 2 | 6 | McGinnis +2.1, Haze +2.1, Vindicta +2.0, Drifter +2.0, Seven +1.8, Warden +1.7 |
| Sprint Boots | vitality 1 | 5 | Lady Geist +2.7, Kelvin +2.1, Haze +1.7, Abrams +1.6, Ivy +1.6 |
| Magic Carpet | spirit 4 | 4 | Lash +4.0, Solomon +3.5, Venator +2.8, Sinclair +2.6 |
| Spirit Burn | spirit 4 | 3 | Ivy +2.3, Vindicta +2.0, Drifter +1.7 |
| Duration Extender | spirit 2 | 2 | Abrams +1.8, Kelvin +1.5 |
| Siphon Bullets | vitality 4 | 1 | Drifter +2.0 |
| Lucky Shot | weapon 4 | 1 | Haze +1.9 |
| Extra Spirit | spirit 1 | 1 | Haze +1.7 |
| Mystic Reverb | spirit 4 | 1 | Rat King +2.1 |
| Monster Rounds | weapon 1 | 1 | Seven +1.8 |
| Warp Stone | vitality 3 | 1 | Victor +1.7 |
| Colossus | vitality 4 | 1 | Warden +2.2 |

## Per hero

### Abrams
- never picked: Duration Extender +1.8, Sprint Boots +1.6

### Apollo
- never picked: Ethereal Shift +2.3

### Baba

### Bebop

### Billy

### Calico

### Celeste
- never picked: Ethereal Shift +2.2

### Deadman Danny
- never picked: Ethereal Shift +2.1

### Drifter
- never picked: Ethereal Shift +2.4, Siphon Bullets +2.0, Fleetfoot +2.0, Spirit Burn +1.7

### Dynamo

### Graves

### Grey Talon

### Haze
- never picked: Fleetfoot +2.1, Lucky Shot +1.9, Sprint Boots +1.7, Extra Spirit +1.7

### Holliday

### Infernus

### Ivy
- never picked: Spirit Burn +2.3, Sprint Boots +1.6

### Kelvin
- never picked: Sprint Boots +2.1, Duration Extender +1.5

### Lady Geist
- never picked: Sprint Boots +2.7

### Lash
- never picked: Magic Carpet +4.0

### McGinnis
- never picked: Fleetfoot +2.1

### Mina
- never picked: Ethereal Shift +2.2

### Mirage

### Mo & Krill

### Nurse Harrow

### Paige
- 18k: Arcane Surge -1.6
- 27k: Arcane Surge -1.6
- 37k: Arcane Surge -1.6
- 50k: Arcane Surge -1.6

### Paradox

### Pocket
- never picked: Ethereal Shift +3.0

### Rat King
- never picked: Mystic Reverb +2.1

### Rem

### Seven
- never picked: Monster Rounds +1.8, Fleetfoot +1.8

### Shiv

### Silver
- never picked: Ethereal Shift +2.2

### Sinclair
- never picked: Magic Carpet +2.6

### Solomon
- never picked: Magic Carpet +3.5

### The Doorman

### Venator
- never picked: Magic Carpet +2.8

### Victor
- never picked: Ethereal Shift +1.9, Warp Stone +1.7

### Vindicta
- never picked: Spirit Burn +2.0, Fleetfoot +2.0

### Violet

### Viscous

### Vyper

### Warden
- never picked: Colossus +2.2, Fleetfoot +1.7

### Wraith

### Yamato

