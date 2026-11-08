# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-06, 49,834 Ritualist+ matches (refreshed 2026-11-08T07:55:27Z).

- Recommended item slots with data: 1837; mean edge +0.9 (popular builds +0.1); clearly positive 819, clearly negative 3.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 3 | Paige -1.2 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 10 | Pocket +3.2, Calico +3.0, Celeste +2.6, Deadman Danny +2.4, Mina +2.4, Silver +2.4, Drifter +2.2, Venator +2.2, Apollo +2.2, Victor +2.0 |
| Sprint Boots | vitality 1 | 5 | Lady Geist +2.4, Kelvin +2.2, Ivy +1.7, Haze +1.7, Abrams +1.6 |
| Fleetfoot | weapon 2 | 5 | McGinnis +1.9, Vyper +1.9, Warden +1.9, Haze +1.7, Drifter +1.7 |
| Colossus | vitality 4 | 3 | Warden +2.4, Apollo +2.4, Abrams +1.5 |
| Magic Carpet | spirit 4 | 3 | Lash +4.2, Solomon +3.1, Sinclair +2.4 |
| Duration Extender | spirit 2 | 2 | Kelvin +1.8, Abrams +1.8 |
| Siphon Bullets | vitality 4 | 2 | Drifter +2.0, Venator +1.6 |
| Silencer | weapon 4 | 2 | Wraith +1.7, Drifter +1.5 |
| Warp Stone | vitality 3 | 2 | Victor +2.2, Infernus +1.5 |
| Spirit Burn | spirit 4 | 2 | Ivy +2.4, Vindicta +2.1 |
| Glass Cannon | weapon 4 | 1 | Deadman Danny +2.3 |
| Superior Cooldown | spirit 3 | 1 | Drifter +2.2 |
| Rapid Recharge | spirit 3 | 1 | Haze +1.7 |
| Extra Spirit | spirit 1 | 1 | Haze +1.6 |
| Mystic Reverb | spirit 4 | 1 | Rat King +2.1 |
| Monster Rounds | weapon 1 | 1 | Seven +1.9 |
| Witchmail | vitality 4 | 1 | Shiv +1.7 |
| Spellslinger | weapon 4 | 1 | Wraith +2.2 |

## Per hero

### Abrams
- never picked: Duration Extender +1.8, Sprint Boots +1.6, Colossus +1.5

### Apollo
- never picked: Colossus +2.4, Ethereal Shift +2.2

### Baba

### Bebop

### Billy

### Calico
- never picked: Ethereal Shift +3.0

### Celeste
- never picked: Ethereal Shift +2.6

### Deadman Danny
- never picked: Ethereal Shift +2.4, Glass Cannon +2.3

### Drifter
- never picked: Ethereal Shift +2.2, Superior Cooldown +2.2, Siphon Bullets +2.0, Fleetfoot +1.7, Silencer +1.5

### Dynamo

### Graves

### Grey Talon

### Haze
- never picked: Rapid Recharge +1.7, Fleetfoot +1.7, Sprint Boots +1.7, Extra Spirit +1.6

### Holliday

### Infernus
- never picked: Warp Stone +1.5

### Ivy
- never picked: Spirit Burn +2.4, Sprint Boots +1.7

### Kelvin
- never picked: Sprint Boots +2.2, Duration Extender +1.8

### Lady Geist
- never picked: Sprint Boots +2.4

### Lash
- never picked: Magic Carpet +4.2

### McGinnis
- never picked: Fleetfoot +1.9

### Mina
- never picked: Ethereal Shift +2.4

### Mirage

### Mo & Krill

### Nurse Harrow

### Paige
- 18k: Arcane Surge -1.2
- 27k: Arcane Surge -1.2
- 37k: Arcane Surge -1.2

### Paradox

### Pocket
- never picked: Ethereal Shift +3.2

### Rat King
- never picked: Mystic Reverb +2.1

### Rem

### Seven
- never picked: Monster Rounds +1.9

### Shiv
- never picked: Witchmail +1.7

### Silver
- never picked: Ethereal Shift +2.4

### Sinclair
- never picked: Magic Carpet +2.4

### Solomon
- never picked: Magic Carpet +3.1

### The Doorman

### Venator
- never picked: Ethereal Shift +2.2, Siphon Bullets +1.6

### Victor
- never picked: Warp Stone +2.2, Ethereal Shift +2.0

### Vindicta
- never picked: Spirit Burn +2.1

### Violet

### Viscous

### Vyper
- never picked: Fleetfoot +1.9

### Warden
- never picked: Colossus +2.4, Fleetfoot +1.9

### Wraith
- never picked: Spellslinger +2.2, Silencer +1.7

### Yamato

