# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-10-25, 159,532 Ritualist+ matches (refreshed 2026-10-27T07:28:58Z).

- Recommended item slots with data: 1983; mean edge +1.4 (popular builds +0.1); clearly positive 1357, clearly negative 13.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 7 | Grey Talon -4.9, Solomon -2.3, McGinnis -1.7 |
| Stalker | weapon 2 | 3 | Billy -1.8 |
| Kinetic Dash | weapon 2 | 2 | Deadman Danny -4.2 |
| Guardian Ward | vitality 2 | 1 | Paige -0.9 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Fleetfoot | weapon 2 | 7 | Baba +4.3, Seven +2.5, Vindicta +1.9, Vyper +1.9, Warden +1.9, Rat King +1.6, Venator +1.5 |
| Ethereal Shift | spirit 4 | 6 | Paradox +3.7, Pocket +2.9, Mina +2.5, Billy +2.4, Violet +2.1, Shiv +1.7 |
| Duration Extender | spirit 2 | 6 | Rat King +3.4, Silver +2.8, Violet +2.5, Vindicta +2.3, McGinnis +1.7, Drifter +1.6 |
| Magic Carpet | spirit 4 | 6 | Lash +5.6, Rem +4.2, Solomon +4.1, Sinclair +3.0, Venator +2.9, Graves +2.6 |
| Sprint Boots | vitality 1 | 5 | Victor +3.1, Lady Geist +2.3, Kelvin +1.9, Venator +1.8, Infernus +1.6 |
| Spirit Burn | spirit 4 | 4 | Solomon +2.5, Mina +1.9, Calico +1.7, Bebop +1.5 |
| Silencer | weapon 4 | 4 | Lady Geist +2.2, Haze +2.0, Graves +1.9, Vyper +1.5 |
| Mystic Expansion | spirit 1 | 3 | Kelvin +1.9, Baba +1.8, Dynamo +1.6 |
| Compress Cooldown | spirit 2 | 3 | Deadman Danny +1.8, Lash +1.7, Baba +1.6 |
| Grit | vitality 1 | 3 | Rat King +2.9, Deadman Danny +1.7, Violet +1.6 |
| Spellslinger | weapon 4 | 3 | Venator +2.2, Wraith +1.9, Vindicta +1.8 |
| Witchmail | vitality 4 | 2 | Bebop +2.2, Mo & Krill +1.9 |
| Frenzy | weapon 4 | 2 | Lady Geist +2.0, Rat King +1.7 |
| Refresher | spirit 4 | 2 | Yamato +1.9, Paige +1.6 |
| Stamina Mastery | vitality 3 | 1 | Apollo +1.6 |
| Superior Cooldown | spirit 3 | 1 | Baba +1.7 |
| Colossus | vitality 4 | 1 | Bebop +2.5 |
| Slowing Bullets | weapon 2 | 1 | Bebop +1.5 |
| Glass Cannon | weapon 4 | 1 | Drifter +1.7 |
| Healing Tempo | vitality 4 | 1 | Dynamo +2.0 |
| Rapid Recharge | spirit 3 | 1 | Haze +1.9 |
| Enduring Speed | vitality 2 | 1 | Haze +1.6 |
| Lucky Shot | weapon 4 | 1 | Haze +1.6 |
| Spellbreaker | vitality 4 | 1 | Infernus +1.7 |
| Dispel Magic | vitality 3 | 1 | Ivy +2.1 |
| Indomitable | vitality 4 | 1 | Lash +1.9 |
| Extra Stamina | vitality 1 | 1 | Rat King +2.9 |
| Arcane Surge | spirit 2 | 1 | Rat King +2.9 |
| Monster Rounds | weapon 1 | 1 | Seven +1.6 |
| Scourge | spirit 4 | 1 | Shiv +1.6 |
| Phantom Strike | vitality 4 | 1 | Silver +2.4 |
| Warp Stone | vitality 3 | 1 | Victor +1.9 |
| Diviner's Kevlar | vitality 4 | 1 | Vindicta +2.2 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.1 |
| Vampiric Burst | vitality 4 | 1 | Vindicta +1.6 |
| Boundless Spirit | spirit 4 | 1 | Wraith +1.9 |

## Per hero

### Abrams

### Apollo
- never picked: Stamina Mastery +1.6

### Baba
- never picked: Fleetfoot +4.3, Mystic Expansion +1.8, Superior Cooldown +1.7, Compress Cooldown +1.6

### Bebop
- never picked: Colossus +2.5, Witchmail +2.2, Slowing Bullets +1.5, Spirit Burn +1.5

### Billy
- 27k: Stalker -1.8
- 37k: Stalker -1.8
- 50k: Stalker -1.8
- never picked: Ethereal Shift +2.4

### Calico
- never picked: Spirit Burn +1.7

### Celeste

### Deadman Danny
- 18k: Kinetic Dash -4.2
- 27k: Kinetic Dash -4.2
- never picked: Compress Cooldown +1.8, Grit +1.7

### Drifter
- never picked: Glass Cannon +1.7, Duration Extender +1.6

### Dynamo
- never picked: Healing Tempo +2.0, Mystic Expansion +1.6

### Graves
- never picked: Magic Carpet +2.6, Silencer +1.9

### Grey Talon
- 18k: Arcane Surge -4.9
- 37k: Arcane Surge -4.9
- 50k: Arcane Surge -4.9

### Haze
- never picked: Silencer +2.0, Rapid Recharge +1.9, Enduring Speed +1.6, Lucky Shot +1.6

### Holliday

### Infernus
- never picked: Spellbreaker +1.7, Sprint Boots +1.6

### Ivy
- never picked: Dispel Magic +2.1

### Kelvin
- never picked: Sprint Boots +1.9, Mystic Expansion +1.9

### Lady Geist
- never picked: Sprint Boots +2.3, Silencer +2.2, Frenzy +2.0

### Lash
- never picked: Magic Carpet +5.6, Indomitable +1.9, Compress Cooldown +1.7

### McGinnis
- 18k: Arcane Surge -1.7
- 27k: Arcane Surge -1.7
- 37k: Arcane Surge -1.7
- never picked: Duration Extender +1.7

### Mina
- never picked: Ethereal Shift +2.5, Spirit Burn +1.9

### Mirage

### Mo & Krill
- never picked: Witchmail +1.9

### Nurse Harrow

### Paige
- 10k: Guardian Ward -0.9
- never picked: Refresher +1.6

### Paradox
- never picked: Ethereal Shift +3.7

### Pocket
- never picked: Ethereal Shift +2.9

### Rat King
- never picked: Duration Extender +3.4, Extra Stamina +2.9, Arcane Surge +2.9, Grit +2.9, Frenzy +1.7, Fleetfoot +1.6

### Rem
- never picked: Magic Carpet +4.2

### Seven
- never picked: Fleetfoot +2.5, Monster Rounds +1.6

### Shiv
- never picked: Ethereal Shift +1.7, Scourge +1.6

### Silver
- never picked: Duration Extender +2.8, Phantom Strike +2.4

### Sinclair
- never picked: Magic Carpet +3.0

### Solomon
- 50k: Arcane Surge -2.3
- never picked: Magic Carpet +4.1, Spirit Burn +2.5

### The Doorman

### Venator
- never picked: Magic Carpet +2.9, Spellslinger +2.2, Sprint Boots +1.8, Fleetfoot +1.5

### Victor
- never picked: Sprint Boots +3.1, Warp Stone +1.9

### Vindicta
- never picked: Duration Extender +2.3, Diviner's Kevlar +2.2, Extended Magazine +2.1, Fleetfoot +1.9, Spellslinger +1.8, Vampiric Burst +1.6

### Violet
- never picked: Duration Extender +2.5, Ethereal Shift +2.1, Grit +1.6

### Viscous

### Vyper
- never picked: Fleetfoot +1.9, Silencer +1.5

### Warden
- never picked: Fleetfoot +1.9

### Wraith
- never picked: Spellslinger +1.9, Boundless Spirit +1.9

### Yamato
- never picked: Refresher +1.9

