# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-10-25, 159,532 Ritualist+ matches (refreshed 2026-10-27T00:08:24Z).

- Recommended item slots with data: 1972; mean edge +1.2 (popular builds +0.1); clearly positive 1164, clearly negative 24.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Spirit Snatch | spirit 3 | 5 | Apollo -1.4 |
| Arcane Surge | spirit 2 | 5 | Victor -4.9, Grey Talon -4.9, Lash -2.7, McGinnis -1.7 |
| Kinetic Dash | weapon 2 | 4 | Deadman Danny -4.2, Haze -1.0 |
| Stalker | weapon 2 | 3 | Billy -1.8 |
| Escalating Exposure | spirit 4 | 3 | Victor -1.6, Kelvin -1.0 |
| Rapid Recharge | spirit 3 | 2 | Dynamo -1.8 |
| Fortitude | vitality 3 | 1 | Deadman Danny -1.2 |
| Toxic Bullets | weapon 3 | 1 | Wraith -0.9 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Diviner's Kevlar | vitality 4 | 9 | Rat King +6.6, Paige +3.6, Solomon +3.6, Mirage +3.5, Yamato +2.4, Silver +2.3, Vindicta +2.2, Mina +2.0, Graves +1.9 |
| Silencer | weapon 4 | 7 | Infernus +2.9, Wraith +2.5, Lady Geist +2.2, Ivy +2.1, Haze +2.0, Graves +1.9, Vyper +1.5 |
| Fleetfoot | weapon 2 | 6 | Baba +4.3, Vindicta +1.9, Vyper +1.9, Warden +1.9, Rat King +1.6, Venator +1.5 |
| Superior Cooldown | spirit 3 | 6 | Drifter +2.4, Yamato +2.3, Paradox +1.8, Baba +1.7, Holliday +1.7, Grey Talon +1.5 |
| Witchmail | vitality 4 | 6 | Kelvin +3.2, Dynamo +2.9, Victor +2.9, Warden +2.9, Bebop +2.2, Mo & Krill +1.9 |
| Ethereal Shift | spirit 4 | 6 | Paradox +3.7, Pocket +2.9, Mina +2.5, Billy +2.4, Violet +2.1, Shiv +1.7 |
| Duration Extender | spirit 2 | 6 | Rat King +3.4, Silver +2.8, Violet +2.5, Vindicta +2.3, McGinnis +1.7, Drifter +1.6 |
| Magic Carpet | spirit 4 | 6 | Lash +5.6, Rem +4.2, Solomon +4.1, Sinclair +3.0, Venator +2.9, Graves +2.6 |
| Spirit Burn | spirit 4 | 5 | Deadman Danny +2.7, Mina +1.9, Calico +1.7, Viscous +1.6, Bebop +1.5 |
| Grit | vitality 1 | 5 | Rat King +2.9, Holliday +2.2, Graves +1.7, Deadman Danny +1.7, Violet +1.6 |
| Sprint Boots | vitality 1 | 5 | Victor +3.1, Lady Geist +2.3, Kelvin +1.9, Venator +1.8, Infernus +1.6 |
| Colossus | vitality 4 | 3 | Bebop +2.5, Billy +1.9, Abrams +1.7 |
| Mystic Expansion | spirit 1 | 3 | Kelvin +1.9, Baba +1.8, Dynamo +1.6 |
| Compress Cooldown | spirit 2 | 3 | Deadman Danny +1.8, Lash +1.7, Baba +1.6 |
| Slowing Bullets | weapon 2 | 3 | Rat King +1.9, Silver +1.9, Bebop +1.5 |
| Spellslinger | weapon 4 | 3 | Venator +2.2, Wraith +1.9, Vindicta +1.8 |
| Greater Expansion | spirit 3 | 2 | Rat King +1.9, Baba +1.7 |
| Indomitable | vitality 4 | 2 | Lash +1.9, Calico +1.8 |
| Lucky Shot | weapon 4 | 2 | Holliday +1.9, Haze +1.6 |
| Dispel Magic | vitality 3 | 2 | Ivy +2.1, Violet +1.9 |
| Frenzy | weapon 4 | 2 | Lady Geist +2.0, Rat King +1.7 |
| Extended Magazine | weapon 1 | 2 | Vindicta +2.1, Nurse Harrow +1.6 |
| Refresher | spirit 4 | 2 | Yamato +1.9, Paige +1.6 |
| Scourge | spirit 4 | 2 | Victor +2.3, Shiv +1.6 |
| Stamina Mastery | vitality 3 | 1 | Apollo +1.6 |
| High-Velocity Rounds | weapon 1 | 1 | Deadman Danny +4.6 |
| Long Range | weapon 2 | 1 | Deadman Danny +1.7 |
| Healing Tempo | vitality 4 | 1 | Dynamo +2.0 |
| Rapid Recharge | spirit 3 | 1 | Haze +1.9 |
| Enduring Speed | vitality 2 | 1 | Haze +1.6 |
| Quicksilver Reload | spirit 2 | 1 | Holliday +1.8 |
| Spellbreaker | vitality 4 | 1 | Infernus +1.7 |
| Swift Striker | weapon 2 | 1 | Ivy +1.5 |
| Infuser | vitality 4 | 1 | Lady Geist +3.1 |
| Extra Stamina | vitality 1 | 1 | Rat King +2.9 |
| Arcane Surge | spirit 2 | 1 | Rat King +2.9 |
| Monster Rounds | weapon 1 | 1 | Seven +1.6 |
| Phantom Strike | vitality 4 | 1 | Silver +2.4 |
| Spirit Resilience | vitality 3 | 1 | Victor +2.0 |
| Warp Stone | vitality 3 | 1 | Victor +1.9 |
| Vampiric Burst | vitality 4 | 1 | Vindicta +1.6 |
| Boundless Spirit | spirit 4 | 1 | Wraith +1.9 |

## Per hero

### Abrams
- never picked: Colossus +1.7

### Apollo
- 10k: Spirit Snatch -1.4
- 18k: Spirit Snatch -1.4
- 27k: Spirit Snatch -1.4
- 37k: Spirit Snatch -1.4
- 50k: Spirit Snatch -1.4
- never picked: Stamina Mastery +1.6

### Baba
- never picked: Fleetfoot +4.3, Mystic Expansion +1.8, Greater Expansion +1.7, Superior Cooldown +1.7, Compress Cooldown +1.6

### Bebop
- never picked: Colossus +2.5, Witchmail +2.2, Slowing Bullets +1.5, Spirit Burn +1.5

### Billy
- 27k: Stalker -1.8
- 37k: Stalker -1.8
- 50k: Stalker -1.8
- never picked: Ethereal Shift +2.4, Colossus +1.9

### Calico
- never picked: Indomitable +1.8, Spirit Burn +1.7

### Celeste

### Deadman Danny
- 18k: Fortitude -1.2, Kinetic Dash -4.2
- 37k: Kinetic Dash -4.2
- 50k: Kinetic Dash -4.2
- never picked: High-Velocity Rounds +4.6, Spirit Burn +2.7, Compress Cooldown +1.8, Long Range +1.7, Grit +1.7

### Drifter
- never picked: Superior Cooldown +2.4, Duration Extender +1.6

### Dynamo
- 27k: Rapid Recharge -1.8
- 50k: Rapid Recharge -1.8
- never picked: Witchmail +2.9, Healing Tempo +2.0, Mystic Expansion +1.6

### Graves
- never picked: Magic Carpet +2.6, Diviner's Kevlar +1.9, Silencer +1.9, Grit +1.7

### Grey Talon
- 18k: Arcane Surge -4.9
- never picked: Superior Cooldown +1.5

### Haze
- 37k: Kinetic Dash -1.0
- never picked: Silencer +2.0, Rapid Recharge +1.9, Enduring Speed +1.6, Lucky Shot +1.6

### Holliday
- never picked: Grit +2.2, Lucky Shot +1.9, Quicksilver Reload +1.8, Superior Cooldown +1.7

### Infernus
- never picked: Silencer +2.9, Spellbreaker +1.7, Sprint Boots +1.6

### Ivy
- never picked: Silencer +2.1, Dispel Magic +2.1, Swift Striker +1.5

### Kelvin
- 50k: Escalating Exposure -1.0
- never picked: Witchmail +3.2, Sprint Boots +1.9, Mystic Expansion +1.9

### Lady Geist
- never picked: Infuser +3.1, Sprint Boots +2.3, Silencer +2.2, Frenzy +2.0

### Lash
- 50k: Arcane Surge -2.7
- never picked: Magic Carpet +5.6, Indomitable +1.9, Compress Cooldown +1.7

### McGinnis
- 18k: Arcane Surge -1.7
- 37k: Arcane Surge -1.7
- never picked: Duration Extender +1.7

### Mina
- never picked: Ethereal Shift +2.5, Diviner's Kevlar +2.0, Spirit Burn +1.9

### Mirage
- never picked: Diviner's Kevlar +3.5

### Mo & Krill
- never picked: Witchmail +1.9

### Nurse Harrow
- never picked: Extended Magazine +1.6

### Paige
- never picked: Diviner's Kevlar +3.6, Refresher +1.6

### Paradox
- never picked: Ethereal Shift +3.7, Superior Cooldown +1.8

### Pocket
- never picked: Ethereal Shift +2.9

### Rat King
- never picked: Diviner's Kevlar +6.6, Duration Extender +3.4, Extra Stamina +2.9, Arcane Surge +2.9, Grit +2.9, Slowing Bullets +1.9, Greater Expansion +1.9, Frenzy +1.7

### Rem
- never picked: Magic Carpet +4.2

### Seven
- never picked: Monster Rounds +1.6

### Shiv
- never picked: Ethereal Shift +1.7, Scourge +1.6

### Silver
- never picked: Duration Extender +2.8, Phantom Strike +2.4, Diviner's Kevlar +2.3, Slowing Bullets +1.9

### Sinclair
- never picked: Magic Carpet +3.0

### Solomon
- never picked: Magic Carpet +4.1, Diviner's Kevlar +3.6

### The Doorman

### Venator
- never picked: Magic Carpet +2.9, Spellslinger +2.2, Sprint Boots +1.8, Fleetfoot +1.5

### Victor
- 37k: Arcane Surge -4.9, Escalating Exposure -1.6
- 50k: Escalating Exposure -1.6
- never picked: Sprint Boots +3.1, Witchmail +2.9, Scourge +2.3, Spirit Resilience +2.0, Warp Stone +1.9

### Vindicta
- never picked: Duration Extender +2.3, Diviner's Kevlar +2.2, Extended Magazine +2.1, Fleetfoot +1.9, Spellslinger +1.8, Vampiric Burst +1.6

### Violet
- never picked: Duration Extender +2.5, Ethereal Shift +2.1, Dispel Magic +1.9, Grit +1.6

### Viscous
- never picked: Spirit Burn +1.6

### Vyper
- never picked: Fleetfoot +1.9, Silencer +1.5

### Warden
- never picked: Witchmail +2.9, Fleetfoot +1.9

### Wraith
- 50k: Toxic Bullets -0.9
- never picked: Silencer +2.5, Spellslinger +1.9, Boundless Spirit +1.9

### Yamato
- never picked: Diviner's Kevlar +2.4, Superior Cooldown +2.3, Refresher +1.9

