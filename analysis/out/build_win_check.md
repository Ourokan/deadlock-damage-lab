# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-10-26, 166,971 Ritualist+ matches (refreshed 2026-10-28T12:07:06Z).

- Recommended item slots with data: 1997; mean edge +1.5 (popular builds +0.1); clearly positive 1402, clearly negative 9.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 4 | Solomon -2.4, McGinnis -1.8 |
| Stalker | weapon 2 | 2 | Billy -1.7 |
| Kinetic Dash | weapon 2 | 2 | Deadman Danny -4.4 |
| Guardian Ward | vitality 2 | 1 | Paige -0.9 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 7 | Paradox +3.8, Pocket +2.7, Mina +2.5, Billy +2.3, Violet +2.2, Shiv +1.7, Apollo +1.7 |
| Fleetfoot | weapon 2 | 7 | Baba +4.2, Seven +2.6, Vyper +1.9, Vindicta +1.8, Warden +1.8, Rat King +1.6, Venator +1.6 |
| Mystic Expansion | spirit 1 | 6 | Baba +2.0, Kelvin +1.8, Dynamo +1.6, Billy +1.6, Sinclair +1.5, Celeste +1.5 |
| Duration Extender | spirit 2 | 6 | Rat King +3.3, Silver +2.7, Violet +2.4, Vindicta +2.2, McGinnis +1.7, Drifter +1.5 |
| Magic Carpet | spirit 4 | 6 | Lash +5.7, Solomon +4.0, Rem +3.8, Sinclair +2.9, Venator +2.7, Graves +2.5 |
| Colossus | vitality 4 | 5 | Rat King +2.6, Bebop +2.4, Billy +1.8, Yamato +1.7, Abrams +1.7 |
| Sprint Boots | vitality 1 | 5 | Victor +3.1, Lady Geist +2.3, Venator +1.9, Kelvin +1.9, Infernus +1.8 |
| Superior Cooldown | spirit 3 | 3 | Paradox +1.7, Baba +1.6, Holliday +1.6 |
| Compress Cooldown | spirit 2 | 3 | Lash +1.7, Deadman Danny +1.7, Baba +1.6 |
| Enduring Speed | vitality 2 | 3 | Billy +1.5, Haze +1.5, Lady Geist +1.5 |
| Witchmail | vitality 4 | 3 | Dynamo +3.0, Violet +2.0, Mo & Krill +2.0 |
| Refresher | spirit 4 | 3 | Yamato +2.0, Paige +1.6, Victor +1.6 |
| Spellslinger | weapon 4 | 3 | Venator +2.1, Wraith +1.9, Vindicta +1.6 |
| Spirit Burn | spirit 4 | 2 | Mina +1.9, Calico +1.6 |
| Frenzy | weapon 4 | 2 | Drifter +2.2, Lady Geist +1.9 |
| Lucky Shot | weapon 4 | 2 | Holliday +2.0, Haze +1.6 |
| Warp Stone | vitality 3 | 2 | Victor +1.9, Infernus +1.5 |
| Indomitable | vitality 4 | 2 | Lash +1.9, McGinnis +1.9 |
| Mystic Reverb | spirit 4 | 2 | Violet +3.3, Solomon +2.5 |
| Stamina Mastery | vitality 3 | 1 | Apollo +1.6 |
| Slowing Bullets | weapon 2 | 1 | Bebop +1.7 |
| Hollow Point | weapon 3 | 1 | Deadman Danny +2.2 |
| Grit | vitality 1 | 1 | Deadman Danny +1.7 |
| Healing Tempo | vitality 4 | 1 | Dynamo +1.9 |
| Spiritual Overflow | weapon 4 | 1 | Graves +1.7 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.1 |
| Spellbreaker | vitality 4 | 1 | Infernus +1.8 |
| Dispel Magic | vitality 3 | 1 | Ivy +2.1 |
| Rapid Rounds | weapon 1 | 1 | Ivy +1.6 |
| Infuser | vitality 4 | 1 | Lady Geist +3.1 |
| Silencer | weapon 4 | 1 | Lady Geist +2.3 |
| Siphon Bullets | vitality 4 | 1 | Lash +1.9 |
| Glass Cannon | weapon 4 | 1 | Paradox +1.5 |
| Extra Stamina | vitality 1 | 1 | Rat King +3.0 |
| Arcane Surge | spirit 2 | 1 | Rat King +2.9 |
| Spirit Rend | weapon 3 | 1 | Seven +1.6 |
| Monster Rounds | weapon 1 | 1 | Seven +1.5 |
| Phantom Strike | vitality 4 | 1 | Silver +2.4 |
| Extra Health | vitality 1 | 1 | Sinclair +1.6 |
| High-Velocity Rounds | weapon 1 | 1 | The Doorman +1.9 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.2 |
| Boundless Spirit | spirit 4 | 1 | Wraith +1.8 |

## Per hero

### Abrams
- never picked: Colossus +1.7

### Apollo
- never picked: Ethereal Shift +1.7, Stamina Mastery +1.6

### Baba
- never picked: Fleetfoot +4.2, Mystic Expansion +2.0, Superior Cooldown +1.6, Compress Cooldown +1.6

### Bebop
- never picked: Colossus +2.4, Slowing Bullets +1.7

### Billy
- 27k: Stalker -1.7
- 50k: Stalker -1.7
- never picked: Ethereal Shift +2.3, Colossus +1.8, Mystic Expansion +1.6, Enduring Speed +1.5

### Calico
- never picked: Spirit Burn +1.6

### Celeste
- never picked: Mystic Expansion +1.5

### Deadman Danny
- 18k: Kinetic Dash -4.4
- 37k: Kinetic Dash -4.4
- never picked: Hollow Point +2.2, Compress Cooldown +1.7, Grit +1.7

### Drifter
- never picked: Frenzy +2.2, Duration Extender +1.5

### Dynamo
- never picked: Witchmail +3.0, Healing Tempo +1.9, Mystic Expansion +1.6

### Graves
- never picked: Magic Carpet +2.5, Spiritual Overflow +1.7

### Grey Talon

### Haze
- never picked: Rapid Recharge +2.1, Lucky Shot +1.6, Enduring Speed +1.5

### Holliday
- never picked: Lucky Shot +2.0, Superior Cooldown +1.6

### Infernus
- never picked: Sprint Boots +1.8, Spellbreaker +1.8, Warp Stone +1.5

### Ivy
- never picked: Dispel Magic +2.1, Rapid Rounds +1.6

### Kelvin
- never picked: Sprint Boots +1.9, Mystic Expansion +1.8

### Lady Geist
- never picked: Infuser +3.1, Silencer +2.3, Sprint Boots +2.3, Frenzy +1.9, Enduring Speed +1.5

### Lash
- never picked: Magic Carpet +5.7, Indomitable +1.9, Siphon Bullets +1.9, Compress Cooldown +1.7

### McGinnis
- 18k: Arcane Surge -1.8
- 27k: Arcane Surge -1.8
- 37k: Arcane Surge -1.8
- never picked: Indomitable +1.9, Duration Extender +1.7

### Mina
- never picked: Ethereal Shift +2.5, Spirit Burn +1.9

### Mirage

### Mo & Krill
- never picked: Witchmail +2.0

### Nurse Harrow

### Paige
- 10k: Guardian Ward -0.9
- never picked: Refresher +1.6

### Paradox
- never picked: Ethereal Shift +3.8, Superior Cooldown +1.7, Glass Cannon +1.5

### Pocket
- never picked: Ethereal Shift +2.7

### Rat King
- never picked: Duration Extender +3.3, Extra Stamina +3.0, Arcane Surge +2.9, Colossus +2.6, Fleetfoot +1.6

### Rem
- never picked: Magic Carpet +3.8

### Seven
- never picked: Fleetfoot +2.6, Spirit Rend +1.6, Monster Rounds +1.5

### Shiv
- never picked: Ethereal Shift +1.7

### Silver
- never picked: Duration Extender +2.7, Phantom Strike +2.4

### Sinclair
- never picked: Magic Carpet +2.9, Extra Health +1.6, Mystic Expansion +1.5

### Solomon
- 27k: Arcane Surge -2.4
- never picked: Magic Carpet +4.0, Mystic Reverb +2.5

### The Doorman
- never picked: High-Velocity Rounds +1.9

### Venator
- never picked: Magic Carpet +2.7, Spellslinger +2.1, Sprint Boots +1.9, Fleetfoot +1.6

### Victor
- never picked: Sprint Boots +3.1, Warp Stone +1.9, Refresher +1.6

### Vindicta
- never picked: Duration Extender +2.2, Extended Magazine +2.2, Fleetfoot +1.8, Spellslinger +1.6

### Violet
- never picked: Mystic Reverb +3.3, Duration Extender +2.4, Ethereal Shift +2.2, Witchmail +2.0

### Viscous

### Vyper
- never picked: Fleetfoot +1.9

### Warden
- never picked: Fleetfoot +1.8

### Wraith
- never picked: Spellslinger +1.9, Boundless Spirit +1.8

### Yamato
- never picked: Refresher +2.0, Colossus +1.7

