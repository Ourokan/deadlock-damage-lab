# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge, lowered for items the hero seldom buys) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

Edges: patch 09-29-2026, matches 2026-10-02 to 2026-10-30, 196,292 Ritualist+ matches (refreshed 2026-10-31T01:31:53Z).

- Recommended item slots with data: 1998; mean edge +1.7 (popular builds +0.0); clearly positive 1490, clearly negative 11.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Arcane Surge | spirit 2 | 5 | Grey Talon -5.5, Ivy -3.0, McGinnis -1.5, Dynamo -1.2 |
| Stalker | weapon 2 | 3 | Billy -1.6 |
| Kinetic Dash | weapon 2 | 2 | Deadman Danny -4.9 |
| Fortitude | vitality 3 | 1 | Deadman Danny -1.4 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Ethereal Shift | spirit 4 | 10 | Paradox +3.7, Pocket +2.7, Mina +2.5, Silver +2.5, Violet +2.5, Billy +2.5, Shiv +1.9, Apollo +1.7, Victor +1.6, Celeste +1.5 |
| Fleetfoot | weapon 2 | 8 | Baba +4.5, Seven +2.4, Vyper +2.4, Kelvin +2.3, Warden +2.1, Vindicta +1.7, Rat King +1.7, Venator +1.6 |
| Duration Extender | spirit 2 | 8 | Rat King +3.4, Silver +2.4, Baba +2.3, Vindicta +2.3, Violet +2.2, Drifter +1.8, McGinnis +1.7, Kelvin +1.5 |
| Witchmail | vitality 4 | 6 | Kelvin +3.4, Dynamo +3.0, Baba +2.8, Mo & Krill +2.2, Apollo +2.2, Bebop +1.9 |
| Sprint Boots | vitality 1 | 6 | Victor +3.3, Lady Geist +2.3, Kelvin +2.2, Infernus +1.9, Venator +1.8, Wraith +1.6 |
| Frenzy | weapon 4 | 5 | Warden +3.1, Victor +2.8, Drifter +2.2, Lady Geist +2.1, Rat King +1.6 |
| Magic Carpet | spirit 4 | 5 | Lash +6.0, Solomon +4.0, Rem +3.4, Sinclair +3.0, Graves +2.4 |
| Colossus | vitality 4 | 4 | Bebop +2.8, Rat King +2.4, Billy +2.0, Abrams +1.6 |
| Mystic Expansion | spirit 1 | 4 | Billy +1.8, Dynamo +1.8, Kelvin +1.8, Celeste +1.6 |
| Spirit Burn | spirit 4 | 3 | Solomon +2.5, Mina +1.8, Bebop +1.5 |
| Enduring Speed | vitality 2 | 3 | Lady Geist +1.6, Billy +1.6, Haze +1.6 |
| Indomitable | vitality 4 | 3 | Lash +2.4, McGinnis +2.1, Calico +2.0 |
| Compress Cooldown | spirit 2 | 3 | Deadman Danny +1.8, Mina +1.7, Lash +1.6 |
| Grit | vitality 1 | 3 | Rat King +2.9, Graves +1.7, Deadman Danny +1.6 |
| Superior Cooldown | spirit 3 | 3 | Drifter +2.2, Paradox +1.7, Grey Talon +1.5 |
| Warp Stone | vitality 3 | 3 | Victor +2.1, Violet +1.6, Infernus +1.5 |
| Refresher | spirit 4 | 3 | Yamato +2.2, Victor +1.6, Paige +1.5 |
| Spellslinger | weapon 4 | 3 | Wraith +2.0, Venator +1.9, Vindicta +1.5 |
| Stamina Mastery | vitality 3 | 2 | McGinnis +1.6, Apollo +1.6 |
| Spellbreaker | vitality 4 | 2 | Infernus +2.0, Billy +1.6 |
| Healing Tempo | vitality 4 | 2 | Dynamo +2.0, McGinnis +1.7 |
| Spiritual Overflow | weapon 4 | 2 | Haze +2.0, Graves +1.6 |
| Lucky Shot | weapon 4 | 2 | Holliday +1.9, Haze +1.5 |
| Silencer | weapon 4 | 2 | Infernus +3.0, Lady Geist +2.3 |
| Dispel Magic | vitality 3 | 2 | Ivy +1.9, Rat King +1.5 |
| Siphon Bullets | vitality 4 | 2 | Victor +2.4, Lash +2.0 |
| Lightning Scroll | spirit 4 | 2 | Paige +1.7, Seven +1.5 |
| Spirit Strike | spirit 1 | 1 | Bebop +2.0 |
| Debuff Reducer | vitality 2 | 1 | Bebop +1.5 |
| Hollow Point | weapon 3 | 1 | Deadman Danny +2.2 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.4 |
| Escalating Exposure | spirit 4 | 1 | Holliday +1.6 |
| Extra Stamina | vitality 1 | 1 | Rat King +3.2 |
| Arcane Surge | spirit 2 | 1 | Rat King +3.0 |
| Spirit Rend | weapon 3 | 1 | Seven +1.7 |
| Phantom Strike | vitality 4 | 1 | Silver +2.2 |
| Extra Health | vitality 1 | 1 | Sinclair +1.9 |
| Extended Magazine | weapon 1 | 1 | Vindicta +2.0 |
| Mystic Reverb | spirit 4 | 1 | Violet +3.3 |
| Rapid Rounds | weapon 1 | 1 | Warden +1.5 |
| Boundless Spirit | spirit 4 | 1 | Wraith +1.6 |

## Per hero

### Abrams
- never picked: Colossus +1.6

### Apollo
- never picked: Witchmail +2.2, Ethereal Shift +1.7, Stamina Mastery +1.6

### Baba
- never picked: Fleetfoot +4.5, Witchmail +2.8, Duration Extender +2.3

### Bebop
- never picked: Colossus +2.8, Spirit Strike +2.0, Witchmail +1.9, Debuff Reducer +1.5, Spirit Burn +1.5

### Billy
- 27k: Stalker -1.6
- 37k: Stalker -1.6
- 50k: Stalker -1.6
- never picked: Ethereal Shift +2.5, Colossus +2.0, Mystic Expansion +1.8, Spellbreaker +1.6, Enduring Speed +1.6

### Calico
- never picked: Indomitable +2.0

### Celeste
- never picked: Mystic Expansion +1.6, Ethereal Shift +1.5

### Deadman Danny
- 18k: Kinetic Dash -4.9
- 27k: Fortitude -1.4
- 37k: Kinetic Dash -4.9
- never picked: Hollow Point +2.2, Compress Cooldown +1.8, Grit +1.6

### Drifter
- never picked: Frenzy +2.2, Superior Cooldown +2.2, Duration Extender +1.8

### Dynamo
- 27k: Arcane Surge -1.2
- 50k: Arcane Surge -1.2
- never picked: Witchmail +3.0, Healing Tempo +2.0, Mystic Expansion +1.8

### Graves
- never picked: Magic Carpet +2.4, Grit +1.7, Spiritual Overflow +1.6

### Grey Talon
- 27k: Arcane Surge -5.5
- never picked: Superior Cooldown +1.5

### Haze
- never picked: Rapid Recharge +2.4, Spiritual Overflow +2.0, Enduring Speed +1.6, Lucky Shot +1.5

### Holliday
- never picked: Lucky Shot +1.9, Escalating Exposure +1.6

### Infernus
- never picked: Silencer +3.0, Spellbreaker +2.0, Sprint Boots +1.9, Warp Stone +1.5

### Ivy
- 37k: Arcane Surge -3.0
- never picked: Dispel Magic +1.9

### Kelvin
- never picked: Witchmail +3.4, Fleetfoot +2.3, Sprint Boots +2.2, Mystic Expansion +1.8, Duration Extender +1.5

### Lady Geist
- never picked: Sprint Boots +2.3, Silencer +2.3, Frenzy +2.1, Enduring Speed +1.6

### Lash
- never picked: Magic Carpet +6.0, Indomitable +2.4, Siphon Bullets +2.0, Compress Cooldown +1.6

### McGinnis
- 50k: Arcane Surge -1.5
- never picked: Indomitable +2.1, Duration Extender +1.7, Healing Tempo +1.7, Stamina Mastery +1.6

### Mina
- never picked: Ethereal Shift +2.5, Spirit Burn +1.8, Compress Cooldown +1.7

### Mirage

### Mo & Krill
- never picked: Witchmail +2.2

### Nurse Harrow

### Paige
- never picked: Lightning Scroll +1.7, Refresher +1.5

### Paradox
- never picked: Ethereal Shift +3.7, Superior Cooldown +1.7

### Pocket
- never picked: Ethereal Shift +2.7

### Rat King
- never picked: Duration Extender +3.4, Extra Stamina +3.2, Arcane Surge +3.0, Grit +2.9, Colossus +2.4, Fleetfoot +1.7, Frenzy +1.6, Dispel Magic +1.5

### Rem
- never picked: Magic Carpet +3.4

### Seven
- never picked: Fleetfoot +2.4, Spirit Rend +1.7, Lightning Scroll +1.5

### Shiv
- never picked: Ethereal Shift +1.9

### Silver
- never picked: Ethereal Shift +2.5, Duration Extender +2.4, Phantom Strike +2.2

### Sinclair
- never picked: Magic Carpet +3.0, Extra Health +1.9

### Solomon
- never picked: Magic Carpet +4.0, Spirit Burn +2.5

### The Doorman

### Venator
- never picked: Spellslinger +1.9, Sprint Boots +1.8, Fleetfoot +1.6

### Victor
- never picked: Sprint Boots +3.3, Frenzy +2.8, Siphon Bullets +2.4, Warp Stone +2.1, Refresher +1.6, Ethereal Shift +1.6

### Vindicta
- never picked: Duration Extender +2.3, Extended Magazine +2.0, Fleetfoot +1.7, Spellslinger +1.5

### Violet
- never picked: Mystic Reverb +3.3, Ethereal Shift +2.5, Duration Extender +2.2, Warp Stone +1.6

### Viscous

### Vyper
- never picked: Fleetfoot +2.4

### Warden
- never picked: Frenzy +3.1, Fleetfoot +2.1, Rapid Rounds +1.5

### Wraith
- never picked: Spellslinger +2.0, Sprint Boots +1.6, Boundless Spirit +1.6

### Yamato
- never picked: Refresher +2.2

