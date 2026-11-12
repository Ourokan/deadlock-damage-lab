# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-31 to 2026-11-10, 80,471 Ritualist+ matches (refreshed 2026-11-12T00:45:46Z).

- Recommended item slots with data: 1892; mean edge +1.3 (popular builds +0.1); clearly positive 1072, clearly negative 6.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Kinetic Dash | weapon 2 | 5 | Warden -4.5, Seven -4.2, Celeste -2.0, Haze -1.8 |
| Escalating Exposure | spirit 4 | 1 | Victor -1.7 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 9 | Pocket +2.8, Deadman Danny +2.6, Celeste +2.5, Calico +2.5, Venator +2.4, Mina +2.1, Apollo +2.0, Victor +1.8, Shiv +1.7 |
| Magic Carpet | spirit 4 | 4 | Lash +4.2, Graves +3.9, Solomon +2.8, Sinclair +1.9 |
| Mystic Expansion | spirit 1 | 3 | Lady Geist +3.1, Baba +2.0, Celeste +1.5 |
| Duration Extender | spirit 2 | 2 | Abrams +1.9, Kelvin +1.8 |
| Grit | vitality 1 | 2 | Baba +2.7, Deadman Danny +1.9 |
| Lucky Shot | weapon 4 | 2 | Calico +2.3, Ivy +2.0 |
| Siphon Bullets | vitality 4 | 2 | Drifter +2.3, Venator +1.9 |
| Spirit Burn | spirit 4 | 2 | Vindicta +2.4, Drifter +1.5 |
| Warp Stone | vitality 3 | 2 | Lady Geist +3.1, Victor +2.7 |
| Witchmail | vitality 4 | 2 | Mo & Krill +2.1, Warden +1.6 |
| Sprint Boots | vitality 1 | 2 | Warden +1.8, Mo & Krill +1.6 |
| Mystic Reverb | spirit 4 | 2 | Viscous +2.3, Shiv +1.6 |
| Spirit Strike | spirit 1 | 1 | Bebop +2.1 |
| Superior Cooldown | spirit 3 | 1 | Drifter +1.6 |
| Spiritual Overflow | weapon 4 | 1 | Graves +1.6 |
| Rapid Recharge | spirit 3 | 1 | Haze +3.0 |
| Extra Stamina | vitality 1 | 1 | Lash +1.5 |
| Stamina Mastery | vitality 3 | 1 | McGinnis +2.2 |
| Colossus | vitality 4 | 1 | Mo & Krill +3.0 |
| Monster Rounds | weapon 1 | 1 | Seven +1.7 |
| Slowing Bullets | weapon 2 | 1 | Silver +1.7 |
| Fleetfoot | weapon 2 | 1 | Victor +2.4 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.3 |
| Spellslinger | weapon 4 | 1 | Wraith +2.2 |
| Silencer | weapon 4 | 1 | Wraith +1.9 |

## Per hero

### Abrams
- never picked: Duration Extender +1.9

### Apollo
- never picked: Ethereal Shift +2.0

### Baba
- never picked: Grit +2.7, Mystic Expansion +2.0

### Bebop
- never picked: Spirit Strike +2.1

### Billy

### Calico
- never picked: Ethereal Shift +2.5, Lucky Shot +2.3

### Celeste
- 27k: Kinetic Dash -2.0
- never picked: Ethereal Shift +2.5, Mystic Expansion +1.5

### Deadman Danny
- never picked: Ethereal Shift +2.6, Grit +1.9

### Drifter
- never picked: Siphon Bullets +2.3, Superior Cooldown +1.6, Spirit Burn +1.5

### Dynamo

### Graves
- never picked: Magic Carpet +3.9, Spiritual Overflow +1.6

### Grey Talon

### Haze
- 37k: Kinetic Dash -1.8
- never picked: Rapid Recharge +3.0

### Holliday

### Infernus

### Ivy
- never picked: Lucky Shot +2.0

### Kelvin
- never picked: Duration Extender +1.8

### Lady Geist
- never picked: Mystic Expansion +3.1, Warp Stone +3.1

### Lash
- never picked: Magic Carpet +4.2, Extra Stamina +1.5

### McGinnis
- never picked: Stamina Mastery +2.2

### Mina
- never picked: Ethereal Shift +2.1

### Mirage

### Mo & Krill
- never picked: Colossus +3.0, Witchmail +2.1, Sprint Boots +1.6

### Nurse Harrow

### Paige

### Paradox

### Pocket
- never picked: Ethereal Shift +2.8

### Rat King

### Rem

### Seven
- 27k: Kinetic Dash -4.2
- never picked: Monster Rounds +1.7

### Shiv
- never picked: Ethereal Shift +1.7, Mystic Reverb +1.6

### Silver
- never picked: Slowing Bullets +1.7

### Sinclair
- never picked: Magic Carpet +1.9

### Solomon
- never picked: Magic Carpet +2.8

### The Doorman

### Venator
- never picked: Ethereal Shift +2.4, Siphon Bullets +1.9

### Victor
- 50k: Escalating Exposure -1.7
- never picked: Warp Stone +2.7, Fleetfoot +2.4, Ethereal Shift +1.8

### Vindicta
- never picked: Spirit Burn +2.4, Extended Magazine +2.3

### Violet

### Viscous
- never picked: Mystic Reverb +2.3

### Vyper

### Warden
- 27k: Kinetic Dash -4.5
- 37k: Kinetic Dash -4.5
- never picked: Sprint Boots +1.8, Witchmail +1.6

### Wraith
- never picked: Spellslinger +2.2, Silencer +1.9

### Yamato

