# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-10-24, 151,478 Ritualist+ matches (refreshed 2026-10-26T10:03:10Z).

- Recommended item slots with data: 1994; mean edge +1.1 (popular builds +0.0); clearly positive 1178, clearly negative 16.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Spirit Snatch | spirit 3 | 5 | Apollo -1.4 |
| Kinetic Dash | weapon 2 | 4 | Deadman Danny -4.3 |
| Escalating Exposure | spirit 4 | 3 | Victor -1.7, Kelvin -1.1 |
| Stalker | weapon 2 | 2 | Billy -1.8 |
| Active Reload | weapon 2 | 1 | Haze -0.9 |
| Toxic Bullets | weapon 3 | 1 | Wraith -1.0 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Diviner's Kevlar | vitality 4 | 13 | Rat King +6.6, Paige +3.7, Holliday +3.6, Solomon +3.5, Nurse Harrow +3.5, Mo & Krill +3.0, Calico +2.7, Yamato +2.4, Vindicta +2.2, Silver +2.1, Baba +2.1, Graves +2.1, Mina +1.9 |
| Fleetfoot | weapon 2 | 7 | Baba +4.4, Seven +2.3, Vindicta +1.9, Vyper +1.7, Warden +1.7, Rat King +1.6, Venator +1.5 |
| Superior Cooldown | spirit 3 | 6 | Drifter +2.2, Yamato +2.1, Paradox +1.9, Baba +1.8, Holliday +1.7, Grey Talon +1.6 |
| Witchmail | vitality 4 | 6 | Kelvin +3.0, Lady Geist +3.0, Victor +2.8, Dynamo +2.8, Bebop +2.1, Mo & Krill +2.0 |
| Magic Carpet | spirit 4 | 6 | Lash +5.5, Solomon +4.2, Rem +4.1, Sinclair +3.0, Venator +2.9, Graves +2.6 |
| Silencer | weapon 4 | 6 | Infernus +3.1, Warden +2.8, Wraith +2.6, Haze +1.9, Ivy +1.9, Graves +1.8 |
| Sprint Boots | vitality 1 | 6 | Victor +3.1, Lady Geist +2.4, Kelvin +1.9, Infernus +1.7, Venator +1.7, Wraith +1.6 |
| Ethereal Shift | spirit 4 | 5 | Pocket +3.0, Mina +2.6, Billy +2.5, Violet +2.1, Shiv +1.9 |
| Duration Extender | spirit 2 | 5 | Rat King +3.4, Silver +2.7, Vindicta +2.2, Violet +2.2, Drifter +1.7 |
| Mystic Expansion | spirit 1 | 4 | Kelvin +1.9, Baba +1.9, Dynamo +1.7, Celeste +1.6 |
| Compress Cooldown | spirit 2 | 3 | Deadman Danny +1.8, Baba +1.7, Lash +1.7 |
| Frenzy | weapon 4 | 3 | Bebop +3.4, Victor +2.8, Rat King +1.7 |
| Spirit Burn | spirit 4 | 3 | Infernus +2.3, Calico +1.6, Bebop +1.6 |
| Grit | vitality 1 | 3 | Rat King +2.8, Violet +1.8, Deadman Danny +1.7 |
| Spellslinger | weapon 4 | 3 | Venator +2.2, Wraith +1.9, Vindicta +1.9 |
| Greater Expansion | spirit 3 | 2 | Rat King +1.9, Baba +1.6 |
| Slowing Bullets | weapon 2 | 2 | Silver +1.9, Bebop +1.7 |
| High-Velocity Rounds | weapon 1 | 2 | Deadman Danny +4.5, Holliday +1.6 |
| Long Range | weapon 2 | 2 | Deadman Danny +1.6, Solomon +1.5 |
| Healing Tempo | vitality 4 | 2 | Haze +3.0, Dynamo +2.0 |
| Lucky Shot | weapon 4 | 2 | Holliday +1.8, Haze +1.5 |
| Warp Stone | vitality 3 | 2 | Victor +1.8, Infernus +1.7 |
| Siphon Bullets | vitality 4 | 2 | Victor +2.3, Lash +2.0 |
| Stamina Mastery | vitality 3 | 1 | Apollo +1.6 |
| Colossus | vitality 4 | 1 | Billy +2.0 |
| Reactive Barrier | vitality 2 | 1 | Calico +1.6 |
| Hollow Point | weapon 3 | 1 | Deadman Danny +2.3 |
| Glass Cannon | weapon 4 | 1 | Drifter +1.8 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.0 |
| Enduring Speed | vitality 2 | 1 | Haze +1.5 |
| Quicksilver Reload | spirit 2 | 1 | Holliday +1.7 |
| Spellbreaker | vitality 4 | 1 | Infernus +1.9 |
| Dispel Magic | vitality 3 | 1 | Ivy +2.2 |
| Swift Striker | weapon 2 | 1 | Ivy +1.5 |
| Infuser | vitality 4 | 1 | Lady Geist +2.8 |
| Lightning Scroll | spirit 4 | 1 | Paige +1.8 |
| Arcane Surge | spirit 2 | 1 | Rat King +2.9 |
| Extra Stamina | vitality 1 | 1 | Rat King +2.8 |
| Monster Rounds | weapon 1 | 1 | Seven +1.7 |
| Phantom Strike | vitality 4 | 1 | Silver +2.5 |
| Spirit Resilience | vitality 3 | 1 | Victor +2.2 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.0 |
| Mercurial Magnum | spirit 4 | 1 | Vindicta +1.6 |
| Boundless Spirit | spirit 4 | 1 | Wraith +2.0 |
| Refresher | spirit 4 | 1 | Yamato +1.9 |

## Per hero

### Abrams

### Apollo
- 10k: Spirit Snatch -1.4
- 18k: Spirit Snatch -1.4
- 27k: Spirit Snatch -1.4
- 37k: Spirit Snatch -1.4
- 50k: Spirit Snatch -1.4
- never picked: Stamina Mastery +1.6

### Baba
- never picked: Fleetfoot +4.4, Diviner's Kevlar +2.1, Mystic Expansion +1.9, Superior Cooldown +1.8, Compress Cooldown +1.7, Greater Expansion +1.6

### Bebop
- never picked: Frenzy +3.4, Witchmail +2.1, Slowing Bullets +1.7, Spirit Burn +1.6

### Billy
- 37k: Stalker -1.8
- 50k: Stalker -1.8
- never picked: Ethereal Shift +2.5, Colossus +2.0

### Calico
- never picked: Diviner's Kevlar +2.7, Spirit Burn +1.6, Reactive Barrier +1.6

### Celeste
- never picked: Mystic Expansion +1.6

### Deadman Danny
- 10k: Kinetic Dash -4.3
- 18k: Kinetic Dash -4.3
- 37k: Kinetic Dash -4.3
- 50k: Kinetic Dash -4.3
- never picked: High-Velocity Rounds +4.5, Hollow Point +2.3, Compress Cooldown +1.8, Grit +1.7, Long Range +1.6

### Drifter
- never picked: Superior Cooldown +2.2, Glass Cannon +1.8, Duration Extender +1.7

### Dynamo
- never picked: Witchmail +2.8, Healing Tempo +2.0, Mystic Expansion +1.7

### Graves
- never picked: Magic Carpet +2.6, Diviner's Kevlar +2.1, Silencer +1.8

### Grey Talon
- never picked: Superior Cooldown +1.6

### Haze
- 50k: Active Reload -0.9
- never picked: Healing Tempo +3.0, Rapid Recharge +2.0, Silencer +1.9, Lucky Shot +1.5, Enduring Speed +1.5

### Holliday
- never picked: Diviner's Kevlar +3.6, Lucky Shot +1.8, Superior Cooldown +1.7, Quicksilver Reload +1.7, High-Velocity Rounds +1.6

### Infernus
- never picked: Silencer +3.1, Spirit Burn +2.3, Spellbreaker +1.9, Sprint Boots +1.7, Warp Stone +1.7

### Ivy
- never picked: Dispel Magic +2.2, Silencer +1.9, Swift Striker +1.5

### Kelvin
- 50k: Escalating Exposure -1.1
- never picked: Witchmail +3.0, Mystic Expansion +1.9, Sprint Boots +1.9

### Lady Geist
- never picked: Witchmail +3.0, Infuser +2.8, Sprint Boots +2.4

### Lash
- never picked: Magic Carpet +5.5, Siphon Bullets +2.0, Compress Cooldown +1.7

### McGinnis

### Mina
- never picked: Ethereal Shift +2.6, Diviner's Kevlar +1.9

### Mirage

### Mo & Krill
- never picked: Diviner's Kevlar +3.0, Witchmail +2.0

### Nurse Harrow
- never picked: Diviner's Kevlar +3.5

### Paige
- never picked: Diviner's Kevlar +3.7, Lightning Scroll +1.8

### Paradox
- never picked: Superior Cooldown +1.9

### Pocket
- never picked: Ethereal Shift +3.0

### Rat King
- never picked: Diviner's Kevlar +6.6, Duration Extender +3.4, Arcane Surge +2.9, Extra Stamina +2.8, Grit +2.8, Greater Expansion +1.9, Frenzy +1.7, Fleetfoot +1.6

### Rem
- never picked: Magic Carpet +4.1

### Seven
- never picked: Fleetfoot +2.3, Monster Rounds +1.7

### Shiv
- never picked: Ethereal Shift +1.9

### Silver
- never picked: Duration Extender +2.7, Phantom Strike +2.5, Diviner's Kevlar +2.1, Slowing Bullets +1.9

### Sinclair
- never picked: Magic Carpet +3.0

### Solomon
- never picked: Magic Carpet +4.2, Diviner's Kevlar +3.5, Long Range +1.5

### The Doorman

### Venator
- never picked: Magic Carpet +2.9, Spellslinger +2.2, Sprint Boots +1.7, Fleetfoot +1.5

### Victor
- 37k: Escalating Exposure -1.7
- 50k: Escalating Exposure -1.7
- never picked: Sprint Boots +3.1, Frenzy +2.8, Witchmail +2.8, Siphon Bullets +2.3, Spirit Resilience +2.2, Warp Stone +1.8

### Vindicta
- never picked: Duration Extender +2.2, Diviner's Kevlar +2.2, Extended Magazine +2.0, Fleetfoot +1.9, Spellslinger +1.9, Mercurial Magnum +1.6

### Violet
- never picked: Duration Extender +2.2, Ethereal Shift +2.1, Grit +1.8

### Viscous

### Vyper
- never picked: Fleetfoot +1.7

### Warden
- never picked: Silencer +2.8, Fleetfoot +1.7

### Wraith
- 50k: Toxic Bullets -1.0
- never picked: Silencer +2.6, Boundless Spirit +2.0, Spellslinger +1.9, Sprint Boots +1.6

### Yamato
- never picked: Diviner's Kevlar +2.4, Superior Cooldown +2.1, Refresher +1.9

