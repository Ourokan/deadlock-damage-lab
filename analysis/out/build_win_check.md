# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-10-27, 174,508 Ritualist+ matches (refreshed 2026-10-29T19:39:59Z).

- Recommended item slots with data: 1994; mean edge +1.6 (popular builds +0.1); clearly positive 1404, clearly negative 11.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 4 | Lash -2.5, McGinnis -1.7 |
| Stalker | weapon 2 | 3 | Billy -1.7 |
| Spirit Snatch | spirit 3 | 1 | Apollo -1.1 |
| Kinetic Dash | weapon 2 | 1 | Deadman Danny -4.6 |
| Guardian Ward | vitality 2 | 1 | Paige -0.9 |
| Extra Regen | vitality 1 | 1 | Seven -1.5 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 7 | Paradox +3.5, Pocket +2.8, Violet +2.5, Mina +2.5, Billy +2.4, Apollo +1.7, Shiv +1.7 |
| Fleetfoot | weapon 2 | 7 | Baba +4.1, Seven +2.4, Vyper +2.1, Warden +1.9, Vindicta +1.8, Rat King +1.6, Venator +1.6 |
| Duration Extender | spirit 2 | 7 | Rat King +3.4, Silver +2.7, Baba +2.5, Violet +2.4, Vindicta +2.2, McGinnis +1.7, Drifter +1.6 |
| Magic Carpet | spirit 4 | 6 | Lash +5.6, Solomon +4.0, Rem +3.3, Sinclair +2.8, Venator +2.6, Graves +2.5 |
| Sprint Boots | vitality 1 | 6 | Victor +3.1, Lady Geist +2.3, Kelvin +1.9, Infernus +1.9, Venator +1.8, Wraith +1.5 |
| Colossus | vitality 4 | 5 | Rat King +2.5, Bebop +2.4, Billy +1.9, Yamato +1.8, Abrams +1.7 |
| Mystic Expansion | spirit 1 | 4 | Baba +2.1, Kelvin +1.9, Billy +1.7, Celeste +1.5 |
| Superior Cooldown | spirit 3 | 3 | Paradox +1.8, Baba +1.6, Holliday +1.5 |
| Compress Cooldown | spirit 2 | 3 | Lash +1.7, Deadman Danny +1.7, Baba +1.6 |
| Indomitable | vitality 4 | 3 | Lash +2.0, McGinnis +1.9, Calico +1.7 |
| Frenzy | weapon 4 | 3 | Victor +2.9, Drifter +2.3, Lady Geist +2.0 |
| Lucky Shot | weapon 4 | 3 | Ivy +2.4, Holliday +2.1, Haze +1.6 |
| Refresher | spirit 4 | 3 | Yamato +2.0, Victor +1.7, Paige +1.6 |
| Spellslinger | weapon 4 | 3 | Venator +2.0, Wraith +1.9, Vindicta +1.6 |
| Witchmail | vitality 4 | 2 | Mo & Krill +2.1, Bebop +2.0 |
| Spirit Burn | spirit 4 | 2 | Mina +1.8, Bebop +1.6 |
| Enduring Speed | vitality 2 | 2 | Lady Geist +1.7, Haze +1.5 |
| Silencer | weapon 4 | 2 | Infernus +2.9, Lady Geist +2.3 |
| Warp Stone | vitality 3 | 2 | Victor +1.9, Infernus +1.5 |
| Slowing Bullets | weapon 2 | 1 | Bebop +1.7 |
| Debuff Reducer | vitality 2 | 1 | Bebop +1.6 |
| Hollow Point | weapon 3 | 1 | Deadman Danny +2.4 |
| Grit | vitality 1 | 1 | Deadman Danny +1.6 |
| Cheat Death | vitality 4 | 1 | Dynamo +2.6 |
| Healing Tempo | vitality 4 | 1 | Dynamo +2.0 |
| Spiritual Overflow | weapon 4 | 1 | Graves +1.6 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.2 |
| Escalating Exposure | spirit 4 | 1 | Holliday +1.6 |
| Spellbreaker | vitality 4 | 1 | Infernus +1.8 |
| Dispel Magic | vitality 3 | 1 | Ivy +1.9 |
| Infuser | vitality 4 | 1 | Lady Geist +3.1 |
| Siphon Bullets | vitality 4 | 1 | Lash +1.8 |
| Extra Stamina | vitality 1 | 1 | Rat King +3.0 |
| Arcane Surge | spirit 2 | 1 | Rat King +2.9 |
| Monster Rounds | weapon 1 | 1 | Seven +1.7 |
| Phantom Strike | vitality 4 | 1 | Silver +2.5 |
| Spirit Rend | weapon 3 | 1 | Solomon +1.8 |
| High-Velocity Rounds | weapon 1 | 1 | The Doorman +1.9 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.1 |
| Boundless Spirit | spirit 4 | 1 | Wraith +1.7 |

## Per hero

### Abrams
- never picked: Colossus +1.7

### Apollo
- 37k: Spirit Snatch -1.1
- never picked: Ethereal Shift +1.7

### Baba
- never picked: Fleetfoot +4.1, Duration Extender +2.5, Mystic Expansion +2.1, Superior Cooldown +1.6, Compress Cooldown +1.6

### Bebop
- never picked: Colossus +2.4, Witchmail +2.0, Slowing Bullets +1.7, Spirit Burn +1.6, Debuff Reducer +1.6

### Billy
- 27k: Stalker -1.7
- 37k: Stalker -1.7
- 50k: Stalker -1.7
- never picked: Ethereal Shift +2.4, Colossus +1.9, Mystic Expansion +1.7

### Calico
- never picked: Indomitable +1.7

### Celeste
- never picked: Mystic Expansion +1.5

### Deadman Danny
- 18k: Kinetic Dash -4.6
- never picked: Hollow Point +2.4, Compress Cooldown +1.7, Grit +1.6

### Drifter
- never picked: Frenzy +2.3, Duration Extender +1.6

### Dynamo
- never picked: Cheat Death +2.6, Healing Tempo +2.0

### Graves
- never picked: Magic Carpet +2.5, Spiritual Overflow +1.6

### Grey Talon

### Haze
- never picked: Rapid Recharge +2.2, Lucky Shot +1.6, Enduring Speed +1.5

### Holliday
- never picked: Lucky Shot +2.1, Escalating Exposure +1.6, Superior Cooldown +1.5

### Infernus
- never picked: Silencer +2.9, Sprint Boots +1.9, Spellbreaker +1.8, Warp Stone +1.5

### Ivy
- never picked: Lucky Shot +2.4, Dispel Magic +1.9

### Kelvin
- never picked: Sprint Boots +1.9, Mystic Expansion +1.9

### Lady Geist
- never picked: Infuser +3.1, Sprint Boots +2.3, Silencer +2.3, Frenzy +2.0, Enduring Speed +1.7

### Lash
- 27k: Arcane Surge -2.5
- never picked: Magic Carpet +5.6, Indomitable +2.0, Siphon Bullets +1.8, Compress Cooldown +1.7

### McGinnis
- 18k: Arcane Surge -1.7
- 27k: Arcane Surge -1.7
- 37k: Arcane Surge -1.7
- never picked: Indomitable +1.9, Duration Extender +1.7

### Mina
- never picked: Ethereal Shift +2.5, Spirit Burn +1.8

### Mirage

### Mo & Krill
- never picked: Witchmail +2.1

### Nurse Harrow

### Paige
- 10k: Guardian Ward -0.9
- never picked: Refresher +1.6

### Paradox
- never picked: Ethereal Shift +3.5, Superior Cooldown +1.8

### Pocket
- never picked: Ethereal Shift +2.8

### Rat King
- never picked: Duration Extender +3.4, Extra Stamina +3.0, Arcane Surge +2.9, Colossus +2.5, Fleetfoot +1.6

### Rem
- never picked: Magic Carpet +3.3

### Seven
- 10k: Extra Regen -1.5
- never picked: Fleetfoot +2.4, Monster Rounds +1.7

### Shiv
- never picked: Ethereal Shift +1.7

### Silver
- never picked: Duration Extender +2.7, Phantom Strike +2.5

### Sinclair
- never picked: Magic Carpet +2.8

### Solomon
- never picked: Magic Carpet +4.0, Spirit Rend +1.8

### The Doorman
- never picked: High-Velocity Rounds +1.9

### Venator
- never picked: Magic Carpet +2.6, Spellslinger +2.0, Sprint Boots +1.8, Fleetfoot +1.6

### Victor
- never picked: Sprint Boots +3.1, Frenzy +2.9, Warp Stone +1.9, Refresher +1.7

### Vindicta
- never picked: Duration Extender +2.2, Extended Magazine +2.1, Fleetfoot +1.8, Spellslinger +1.6

### Violet
- never picked: Ethereal Shift +2.5, Duration Extender +2.4

### Viscous

### Vyper
- never picked: Fleetfoot +2.1

### Warden
- never picked: Fleetfoot +1.9

### Wraith
- never picked: Spellslinger +1.9, Boundless Spirit +1.7, Sprint Boots +1.5

### Yamato
- never picked: Refresher +2.0, Colossus +1.8

