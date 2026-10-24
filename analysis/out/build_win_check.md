# Recommended builds vs real win edge

Per-hero real win edge (Ritualist+, current patch builds, matched on hero/time/lead/own souls, vs other same-slot same-tier items, shrunk toward the item's all-hero edge) for every item in the Phantom+ "Best overall" builds. Clearly negative = upper 95% bound < 0. Script `analysis/scripts/build_win_check.py`.

- Recommended item slots with data: 1855; mean edge -0.3 (popular builds +0.0); clearly positive 218, clearly negative 282.

Findings 2026-10-24 (one-off checks, not rerun by this script):
- Sim marginal item value (popular Phantom+ build + item, overall score per soul, z-scored within slot/tier) vs real per-hero edge, 16 heroes x 27k/37k, 4,515 pairs: Pearson 0.05, Spearman 0.07. The 1v1 damage-before-death score does not rank items the way real wins do.
- Sim loves / real hates: Metal Skin, Decay, Rusted Barrel, Return Fire, Capacitor, Arctic Blast, Rebuttal, Stalker, Silence Wave. Real loves / sim hates: Heroic Aura, Blood Tribute, Mystic Reverb, Cheat Death, Greater Expansion, Divine Barrier (team auras, AoE, death saves: outside a 1v1).
- Decay ticks running on past a refill (the immortal enemy's 'kill') are not the cause: ending them moves Decay's value < 1%. Its sim damage matches real (real/sim 1.39); the damage just doesn't turn into wins.
- Real edges are robust to matching: lead buckets 1,000 instead of 2,500 souls and own-souls buckets 750 instead of 1,500 give item edges correlated 0.99 with these. Items bought while behind still lose at equal lead (mean lead at purchase vs edge r = 0.5), so part of a negative edge may be unobserved game state (deaths, enemy picks), not the item.

## Recommended items that lose real games (hero x budget count)

| Item | slot/tier | builds | heroes (edge) |
|---|---|---:|---|
| Decay | spirit 3 | 116 | Dynamo -4.9, The Doorman -4.3, Holliday -4.2, Paige -4.2, Yamato -4.0, Abrams -4.0, Ivy -4.0, Kelvin -3.8, Billy -3.8, Calico -3.7, Sinclair -3.7, Bebop -3.6, Apollo -3.6, Haze -3.5, Celeste -3.5, Deadman Danny -3.5, Mo & Krill -3.5, Seven -3.4, Mina -3.4, Wraith -3.4, Vyper -3.3, Warden -3.3, Mirage -3.3, McGinnis -3.3, Grey Talon -3.2, Solomon -3.2, Lady Geist -3.2, Infernus -3.1, Viscous -2.7, Graves -2.4, Rem -2.4 |
| Return Fire | vitality 2 | 24 | Wraith -3.9, Kelvin -3.8, Mo & Krill -3.8, Bebop -3.6, Haze -3.5, Warden -3.5, Grey Talon -3.5, Vindicta -3.5, Venator -3.5, Paige -3.3, Rem -3.2, McGinnis -3.2, Mina -3.2, Viscous -3.2, Ivy -3.1, Rat King -2.9 |
| Spirit Snatch | spirit 3 | 14 | Billy -1.7, Abrams -1.5, Apollo -1.3 |
| Radiant Regeneration | spirit 3 | 12 | Lady Geist -3.8, Apollo -2.1, Victor -1.6 |
| Toxic Bullets | weapon 3 | 10 | Rat King -3.7, Bebop -3.0, Silver -2.5, Ivy -2.2, Drifter -1.8 |
| Healing Booster | vitality 2 | 8 | Lady Geist -3.2, Apollo -1.3, Victor -1.0 |
| Stalker | weapon 2 | 7 | Shiv -2.6, Billy -2.4 |
| Rusted Barrel | spirit 1 | 7 | Vindicta -4.8, Lash -4.3, Billy -4.2, Pocket -4.2, Infernus -3.8, Solomon -3.4, Drifter -3.1 |
| Rapid Recharge | spirit 3 | 7 | Celeste -2.6, Shiv -1.8, Dynamo -1.5, Ivy -1.2 |
| Escalating Exposure | spirit 4 | 7 | Victor -2.2, Shiv -1.4, Kelvin -1.2 |
| Disarming Hex | spirit 3 | 6 | Graves -7.3, Pocket -6.9, Mina -6.7, Seven -6.5, Bebop -5.4, Rem -5.0 |
| Swift Striker | weapon 2 | 6 | Rat King -1.6, Vindicta -0.9, Haze -0.7 |
| Metal Skin | vitality 3 | 6 | The Doorman -6.2, Viscous -6.0, Vyper -5.8, Vindicta -5.6, Mina -5.1 |
| Mystic Shot | weapon 2 | 5 | Paradox -1.7, Yamato -1.2 |
| Escalating Resilience | weapon 3 | 5 | Rat King -2.1, Venator -1.7 |
| Tankbuster | spirit 3 | 4 | Bebop -1.9, Lash -1.2, Pocket -1.1 |
| Unstoppable | vitality 4 | 4 | Pocket -3.8, Dynamo -3.8, Haze -2.0 |
| Active Reload | weapon 2 | 4 | Haze -0.8 |
| Spirit Lifesteal | vitality 2 | 3 | Infernus -0.8 |
| Suppressor | spirit 2 | 3 | Paige -2.6, Mirage -1.6 |
| Boundless Spirit | spirit 4 | 3 | Sinclair -2.1, Solomon -1.8, Viscous -1.7 |
| Spirit Sap | spirit 2 | 2 | Drifter -2.8 |
| Spiritual Overflow | weapon 4 | 2 | Vindicta -2.7, Infernus -1.1 |
| Recharging Rush | weapon 2 | 2 | Rat King -1.4 |
| Improved Spirit | spirit 2 | 2 | Sinclair -1.6 |
| Dispel Magic | vitality 3 | 1 | Apollo -1.1 |
| Bullet Lifesteal | vitality 2 | 1 | Haze -0.8 |
| Fury Trance | vitality 3 | 1 | Haze -2.7 |
| Silence Wave | spirit 3 | 1 | Holliday -3.3 |
| Sharpshooter | weapon 3 | 1 | Paradox -1.6 |
| Transcendent Cooldown | spirit 4 | 1 | Pocket -1.3 |
| Plated Armor | vitality 4 | 1 | Shiv -2.0 |
| Battle Vest | vitality 2 | 1 | Venator -0.9 |
| Cultist Sacrifice | weapon 3 | 1 | Venator -2.4 |
| Crippling Headshot | weapon 4 | 1 | Venator -2.8 |
| Opening Rounds | weapon 2 | 1 | Vindicta -1.5 |
| Mercurial Magnum | spirit 4 | 1 | Wraith -2.4 |
| Rebuttal | vitality 1 | 1 | Yamato -2.3 |

## Strong items the sim never picks (edge >= +1.5, lower 95% bound > 0)

| Item | slot/tier | heroes | heroes (edge) |
|---|---|---:|---|
| Magic Carpet | spirit 4 | 16 | Lash +5.1, Solomon +4.7, Rem +3.7, McGinnis +3.7, Abrams +3.4, Paige +3.3, Kelvin +3.2, Venator +3.2, Deadman Danny +3.1, Pocket +3.1, Sinclair +3.1, Warden +3.1, Holliday +3.1, Ivy +3.1, Graves +3.0, Dynamo +3.0 |
| Heroic Aura | weapon 3 | 15 | Rat King +3.8, Sinclair +3.6, Victor +3.5, Rem +3.5, Lash +3.2, McGinnis +3.2, Dynamo +3.1, Abrams +3.1, Bebop +2.9, Mo & Krill +2.9, Vindicta +2.8, The Doorman +2.7, Billy +2.3, Ivy +2.3, Paige +2.3 |
| Mystic Reverb | spirit 4 | 13 | Bebop +4.5, Lash +4.2, Mina +3.7, Kelvin +3.5, Pocket +3.4, Apollo +3.2, Shiv +3.1, Victor +3.1, Grey Talon +2.9, The Doorman +2.9, Paige +2.6, Holliday +2.5, Sinclair +2.5 |
| Cheat Death | vitality 4 | 10 | Rem +3.3, Kelvin +3.1, Vindicta +3.0, Drifter +3.0, Graves +3.0, Mina +2.8, Wraith +2.6, Paige +2.5, Dynamo +2.3, Pocket +2.0 |
| Frenzy | weapon 4 | 8 | Abrams +3.6, Vyper +3.4, Billy +3.3, Haze +3.2, Bebop +3.0, Drifter +2.7, Rat King +2.6, Venator +2.2 |
| Greater Expansion | spirit 3 | 8 | Infernus +3.2, Seven +2.1, Lady Geist +2.1, Mo & Krill +1.9, Abrams +1.9, Rat King +1.8, Paradox +1.6, Billy +1.5 |
| Witchmail | vitality 4 | 8 | Kelvin +4.4, Dynamo +3.8, Apollo +3.4, Lady Geist +3.4, Victor +3.3, Infernus +2.7, Shiv +2.3, Mo & Krill +2.2 |
| Silencer | weapon 4 | 8 | Infernus +4.6, Billy +3.9, Mirage +3.6, Shiv +3.0, Bebop +2.9, Graves +2.5, Wraith +2.5, Vyper +2.0 |
| Spirit Burn | spirit 4 | 8 | McGinnis +3.2, Solomon +3.0, Seven +2.8, Infernus +2.8, Viscous +2.4, The Doorman +2.4, Ivy +1.9, Paradox +1.8 |
| Diviner's Kevlar | vitality 4 | 7 | Rat King +6.0, Seven +3.3, Billy +3.1, Paige +3.1, Dynamo +2.8, Graves +2.8, Silver +1.8 |
| Debuff Reducer | vitality 2 | 6 | Abrams +2.8, Drifter +2.5, Silver +2.4, Billy +1.9, Victor +1.9, Mo & Krill +1.7 |
| Bullet Resist Shredder | spirit 2 | 6 | Drifter +4.6, Lash +4.3, Yamato +3.8, Seven +2.9, Wraith +2.2, Billy +1.6 |
| Grit | vitality 1 | 6 | Rat King +2.7, Infernus +2.6, Graves +2.5, Calico +2.1, McGinnis +2.0, Rem +1.5 |
| Scourge | spirit 4 | 6 | Infernus +3.5, Paige +3.1, Celeste +3.0, Shiv +2.5, Rat King +2.2, Victor +2.2 |
| Fleetfoot | weapon 2 | 6 | Victor +2.4, Wraith +2.1, Warden +2.1, Vyper +1.9, Vindicta +1.7, Venator +1.6 |
| Mystic Expansion | spirit 1 | 5 | Victor +2.4, Abrams +2.2, Sinclair +1.9, Kelvin +1.6, Celeste +1.5 |
| Spirit Resilience | vitality 3 | 5 | Wraith +2.6, Holliday +2.5, Dynamo +2.3, Solomon +1.8, Abrams +1.6 |
| Duration Extender | spirit 2 | 5 | Silver +3.9, Rat King +3.4, Vindicta +2.4, Drifter +2.3, Ivy +1.7 |
| Hollow Point | weapon 3 | 5 | Grey Talon +3.6, Ivy +2.6, Paradox +2.2, Drifter +2.1, Haze +2.0 |
| Ethereal Shift | spirit 4 | 5 | Pocket +3.4, Paradox +2.7, Infernus +2.6, Mina +2.2, Shiv +1.7 |
| Sprint Boots | vitality 1 | 5 | Victor +3.7, Lady Geist +2.5, Kelvin +2.4, Mo & Krill +2.1, Wraith +1.7 |
| Colossus | vitality 4 | 4 | Bebop +3.3, Rat King +2.7, Billy +1.7, Abrams +1.7 |
| Torment Pulse | spirit 3 | 4 | Bebop +3.1, Apollo +2.6, Shiv +2.3, Ivy +2.2 |
| Melee Charge | weapon 2 | 4 | Yamato +3.4, Apollo +2.6, Bebop +2.1, Drifter +2.0 |
| Restorative Locket | vitality 2 | 4 | Silver +3.3, Bebop +2.7, Rem +1.9, Shiv +1.6 |
| Hunter's Aura | weapon 3 | 4 | Rat King +6.1, Billy +2.6, Bebop +2.3, Drifter +2.0 |
| Superior Cooldown | spirit 3 | 4 | Drifter +2.5, Yamato +2.2, Calico +2.0, Celeste +1.8 |
| Dispel Magic | vitality 3 | 4 | Drifter +2.4, Ivy +2.1, Yamato +1.8, Venator +1.6 |
| Extra Spirit | spirit 1 | 4 | Wraith +2.6, Victor +1.9, Pocket +1.8, Graves +1.6 |
| Enduring Speed | vitality 2 | 3 | Billy +1.8, Vindicta +1.6, Abrams +1.6 |
| Slowing Bullets | weapon 2 | 3 | Rat King +2.3, Bebop +1.9, Silver +1.8 |
| Spirit Shielding | vitality 2 | 3 | Rat King +2.6, Graves +1.6, Billy +1.5 |
| Lucky Shot | weapon 4 | 3 | Vindicta +3.4, Calico +2.8, Venator +1.7 |
| Weakening Headshot | weapon 2 | 3 | Vindicta +2.8, Paradox +2.6, Haze +2.1 |
| Siphon Bullets | vitality 4 | 3 | Warden +2.1, Haze +2.0, Lash +1.8 |
| High-Velocity Rounds | weapon 1 | 3 | Paige +2.7, Victor +1.9, Holliday +1.8 |
| Healing Nova | vitality 3 | 3 | Paige +2.5, Ivy +1.9, Rem +1.8 |
| Spirit Shredder | weapon 2 | 3 | Wraith +2.8, Lady Geist +2.7, Mina +2.1 |
| Compress Cooldown | spirit 2 | 3 | Lash +1.9, Victor +1.8, Yamato +1.7 |
| Superior Duration | spirit 3 | 3 | Rat King +2.9, Silver +2.9, Vindicta +2.8 |
| Spellslinger | weapon 4 | 3 | Wraith +1.9, Vindicta +1.9, Venator +1.9 |
| Berserker | weapon 3 | 2 | Billy +2.2, Abrams +1.9 |
| Mystic Regeneration | spirit 1 | 2 | Yamato +2.5, Bebop +1.8 |
| Divine Barrier | vitality 4 | 2 | Rat King +3.7, Dynamo +3.0 |
| Alchemical Fire | weapon 3 | 2 | Holliday +2.4, Paradox +2.0 |
| Infuser | vitality 4 | 2 | Lady Geist +3.6, Infernus +1.8 |
| Warp Stone | vitality 3 | 2 | Victor +2.2, Infernus +1.5 |
| Tesla Bullets | weapon 3 | 2 | Wraith +2.8, Ivy +2.1 |
| Mystic Vulnerability | spirit 2 | 2 | Lady Geist +1.9, Solomon +1.7 |
| Guardian Ward | vitality 2 | 2 | Rat King +5.2, Mo & Krill +2.0 |
| Close Quarters | weapon 1 | 2 | Viscous +2.4, Rem +1.9 |
| Monster Rounds | weapon 1 | 2 | Wraith +1.8, Seven +1.6 |
| Extra Health | vitality 1 | 2 | Yamato +2.6, Sinclair +1.9 |
| Blood Tribute | weapon 3 | 2 | Vindicta +3.4, Vyper +2.8 |
| Melee Lifesteal | vitality 1 | 1 | Bebop +2.2 |
| Lifestrike | vitality 3 | 1 | Bebop +1.8 |
| Spirit Strike | spirit 1 | 1 | Bebop +1.5 |
| Indomitable | vitality 4 | 1 | Calico +2.0 |
| Stamina Mastery | vitality 3 | 1 | Deadman Danny +2.4 |
| Glass Cannon | weapon 4 | 1 | Drifter +1.8 |
| Healing Tempo | vitality 4 | 1 | Haze +3.0 |
| Rapid Recharge | spirit 3 | 1 | Haze +2.3 |
| Recharging Rush | weapon 2 | 1 | Haze +1.9 |
| Reactive Barrier | vitality 2 | 1 | Holliday +1.9 |
| Restorative Shot | weapon 1 | 1 | Holliday +1.9 |
| Echo Shard | spirit 4 | 1 | Ivy +2.3 |
| Swift Striker | weapon 2 | 1 | Ivy +1.6 |
| Headshot Booster | weapon 1 | 1 | Lash +1.9 |
| Improved Spirit | spirit 2 | 1 | Pocket +1.6 |
| Arcane Surge | spirit 2 | 1 | Rat King +2.6 |
| Extra Stamina | vitality 1 | 1 | Rat King +2.5 |
| Phantom Strike | vitality 4 | 1 | Silver +2.1 |
| Long Range | weapon 2 | 1 | Solomon +1.7 |
| Extended Magazine | weapon 1 | 1 | Vindicta +1.9 |
| Spirit Lifesteal | vitality 2 | 1 | Vyper +2.0 |
| Rapid Rounds | weapon 1 | 1 | Wraith +2.2 |
| Boundless Spirit | spirit 4 | 1 | Wraith +1.7 |
| Refresher | spirit 4 | 1 | Yamato +1.8 |

## Per hero

### Abrams
- 10k: Spirit Snatch -1.5
- 18k: Spirit Snatch -1.5
- 27k: Spirit Snatch -1.5
- 37k: Decay -4.0, Spirit Snatch -1.5
- 50k: Decay -4.0, Spirit Snatch -1.5
- never picked: Frenzy +3.6, Magic Carpet +3.4, Heroic Aura +3.1, Debuff Reducer +2.8, Mystic Expansion +2.2, Berserker +1.9, Greater Expansion +1.9, Colossus +1.7

### Apollo
- 18k: Healing Booster -1.3, Decay -3.6, Spirit Snatch -1.3
- 27k: Healing Booster -1.3, Radiant Regeneration -2.1, Decay -3.6, Spirit Snatch -1.3
- 37k: Radiant Regeneration -2.1, Spirit Snatch -1.3
- 50k: Decay -3.6, Spirit Snatch -1.3, Dispel Magic -1.1
- never picked: Witchmail +3.4, Mystic Reverb +3.2, Torment Pulse +2.6, Melee Charge +2.6

### Bebop
- 10k: Return Fire -3.6
- 18k: Decay -3.6, Return Fire -3.6
- 27k: Decay -3.6, Return Fire -3.6
- 37k: Disarming Hex -5.4, Decay -3.6, Toxic Bullets -3.0
- 50k: Tankbuster -1.9, Decay -3.6, Return Fire -3.6
- never picked: Mystic Reverb +4.5, Colossus +3.3, Torment Pulse +3.1, Frenzy +3.0, Silencer +2.9, Heroic Aura +2.9, Restorative Locket +2.7, Hunter's Aura +2.3

### Billy
- 10k: Spirit Snatch -1.7
- 18k: Stalker -2.4, Rusted Barrel -4.2, Spirit Snatch -1.7
- 27k: Stalker -2.4, Spirit Snatch -1.7
- 37k: Stalker -2.4, Decay -3.8, Spirit Snatch -1.7
- 50k: Stalker -2.4, Decay -3.8, Spirit Snatch -1.7
- never picked: Silencer +3.9, Frenzy +3.3, Diviner's Kevlar +3.1, Hunter's Aura +2.6, Heroic Aura +2.3, Berserker +2.2, Debuff Reducer +1.9, Enduring Speed +1.8

### Calico
- 10k: Decay -3.7
- 18k: Decay -3.7
- 27k: Decay -3.7
- 37k: Decay -3.7
- 50k: Decay -3.7
- never picked: Lucky Shot +2.8, Grit +2.1, Superior Cooldown +2.0, Indomitable +2.0

### Celeste
- 27k: Decay -3.5
- 37k: Decay -3.5
- 50k: Rapid Recharge -2.6, Decay -3.5
- never picked: Scourge +3.0, Superior Cooldown +1.8, Mystic Expansion +1.5

### Deadman Danny
- 10k: Decay -3.5
- 18k: Decay -3.5
- never picked: Magic Carpet +3.1, Stamina Mastery +2.4

### Drifter
- 18k: Spirit Sap -2.8
- 37k: Spirit Sap -2.8, Rusted Barrel -3.1, Toxic Bullets -1.8
- 50k: Toxic Bullets -1.8
- never picked: Bullet Resist Shredder +4.6, Cheat Death +3.0, Frenzy +2.7, Debuff Reducer +2.5, Superior Cooldown +2.5, Dispel Magic +2.4, Duration Extender +2.3, Hollow Point +2.1

### Dynamo
- 10k: Decay -4.9
- 18k: Rapid Recharge -1.5, Decay -4.9
- 27k: Rapid Recharge -1.5, Decay -4.9
- 37k: Rapid Recharge -1.5, Decay -4.9
- 50k: Rapid Recharge -1.5, Decay -4.9, Unstoppable -3.8
- never picked: Witchmail +3.8, Heroic Aura +3.1, Magic Carpet +3.0, Divine Barrier +3.0, Diviner's Kevlar +2.8, Cheat Death +2.3, Spirit Resilience +2.3

### Graves
- 27k: Decay -2.4
- 50k: Disarming Hex -7.3, Decay -2.4
- never picked: Magic Carpet +3.0, Cheat Death +3.0, Diviner's Kevlar +2.8, Grit +2.5, Silencer +2.5, Extra Spirit +1.6, Spirit Shielding +1.6

### Grey Talon
- 18k: Decay -3.2
- 27k: Decay -3.2, Return Fire -3.5
- 37k: Decay -3.2
- 50k: Decay -3.2
- never picked: Hollow Point +3.6, Mystic Reverb +2.9

### Haze
- 10k: Return Fire -3.5
- 18k: Active Reload -0.8, Swift Striker -0.7
- 27k: Active Reload -0.8, Bullet Lifesteal -0.8, Decay -3.5, Swift Striker -0.7
- 37k: Active Reload -0.8, Swift Striker -0.7
- 50k: Active Reload -0.8, Fury Trance -2.7, Unstoppable -2.0
- never picked: Frenzy +3.2, Healing Tempo +3.0, Rapid Recharge +2.3, Weakening Headshot +2.1, Siphon Bullets +2.0, Hollow Point +2.0, Recharging Rush +1.9

### Holliday
- 18k: Decay -4.2
- 27k: Decay -4.2
- 37k: Decay -4.2
- 50k: Silence Wave -3.3, Decay -4.2
- never picked: Magic Carpet +3.1, Mystic Reverb +2.5, Spirit Resilience +2.5, Alchemical Fire +2.4, Reactive Barrier +1.9, Restorative Shot +1.9, High-Velocity Rounds +1.8

### Infernus
- 10k: Spirit Lifesteal -0.8, Decay -3.1
- 18k: Spirit Lifesteal -0.8, Rusted Barrel -3.8, Decay -3.1
- 27k: Spirit Lifesteal -0.8, Decay -3.1
- 37k: Decay -3.1
- 50k: Spiritual Overflow -1.1, Decay -3.1
- never picked: Silencer +4.6, Scourge +3.5, Greater Expansion +3.2, Spirit Burn +2.8, Witchmail +2.7, Grit +2.6, Ethereal Shift +2.6, Infuser +1.8

### Ivy
- 10k: Decay -4.0
- 18k: Decay -4.0, Return Fire -3.1
- 27k: Decay -4.0, Toxic Bullets -2.2
- 37k: Decay -4.0, Toxic Bullets -2.2
- 50k: Rapid Recharge -1.2, Decay -4.0, Toxic Bullets -2.2
- never picked: Magic Carpet +3.1, Hollow Point +2.6, Heroic Aura +2.3, Echo Shard +2.3, Torment Pulse +2.2, Tesla Bullets +2.1, Dispel Magic +2.1, Spirit Burn +1.9

### Kelvin
- 10k: Decay -3.8
- 18k: Decay -3.8, Return Fire -3.8
- 27k: Escalating Exposure -1.2, Decay -3.8
- 37k: Escalating Exposure -1.2, Decay -3.8
- 50k: Escalating Exposure -1.2, Decay -3.8
- never picked: Witchmail +4.4, Mystic Reverb +3.5, Magic Carpet +3.2, Cheat Death +3.1, Sprint Boots +2.4, Mystic Expansion +1.6

### Lady Geist
- 10k: Radiant Regeneration -3.8
- 18k: Healing Booster -3.2, Radiant Regeneration -3.8
- 27k: Healing Booster -3.2, Radiant Regeneration -3.8
- 37k: Healing Booster -3.2, Radiant Regeneration -3.8
- 50k: Radiant Regeneration -3.8, Decay -3.2
- never picked: Infuser +3.6, Witchmail +3.4, Spirit Shredder +2.7, Sprint Boots +2.5, Greater Expansion +2.1, Mystic Vulnerability +1.9

### Lash
- 18k: Rusted Barrel -4.3
- 37k: Tankbuster -1.2
- never picked: Magic Carpet +5.1, Bullet Resist Shredder +4.3, Mystic Reverb +4.2, Heroic Aura +3.2, Headshot Booster +1.9, Compress Cooldown +1.9, Siphon Bullets +1.8

### McGinnis
- 10k: Decay -3.3
- 18k: Decay -3.3, Return Fire -3.2
- 27k: Decay -3.3
- 37k: Decay -3.3
- 50k: Decay -3.3
- never picked: Magic Carpet +3.7, Heroic Aura +3.2, Spirit Burn +3.2, Grit +2.0

### Mina
- 10k: Decay -3.4
- 18k: Decay -3.4, Return Fire -3.2
- 27k: Decay -3.4
- 37k: Metal Skin -5.1, Decay -3.4, Return Fire -3.2
- 50k: Disarming Hex -6.7, Decay -3.4
- never picked: Mystic Reverb +3.7, Cheat Death +2.8, Ethereal Shift +2.2, Spirit Shredder +2.1

### Mirage
- 10k: Decay -3.3
- 18k: Decay -3.3
- 27k: Suppressor -1.6, Decay -3.3
- 37k: Decay -3.3
- never picked: Silencer +3.6

### Mo & Krill
- 18k: Decay -3.5, Return Fire -3.8
- 27k: Decay -3.5
- 37k: Decay -3.5
- 50k: Decay -3.5
- never picked: Heroic Aura +2.9, Witchmail +2.2, Sprint Boots +2.1, Guardian Ward +2.0, Greater Expansion +1.9, Debuff Reducer +1.7

### Nurse Harrow

### Paige
- 10k: Suppressor -2.6
- 18k: Decay -4.2, Return Fire -3.3
- 27k: Suppressor -2.6, Decay -4.2
- 37k: Decay -4.2
- 50k: Decay -4.2
- never picked: Magic Carpet +3.3, Scourge +3.1, Diviner's Kevlar +3.1, High-Velocity Rounds +2.7, Mystic Reverb +2.6, Healing Nova +2.5, Cheat Death +2.5, Heroic Aura +2.3

### Paradox
- 50k: Mystic Shot -1.7, Sharpshooter -1.6
- never picked: Ethereal Shift +2.7, Weakening Headshot +2.6, Hollow Point +2.2, Alchemical Fire +2.0, Spirit Burn +1.8, Greater Expansion +1.6

### Pocket
- 27k: Tankbuster -1.1, Unstoppable -3.8
- 37k: Tankbuster -1.1, Rusted Barrel -4.2
- 50k: Transcendent Cooldown -1.3, Disarming Hex -6.9, Unstoppable -3.8
- never picked: Mystic Reverb +3.4, Ethereal Shift +3.4, Magic Carpet +3.1, Cheat Death +2.0, Extra Spirit +1.8, Improved Spirit +1.6

### Rat King
- 18k: Return Fire -2.9
- 27k: Recharging Rush -1.4, Escalating Resilience -2.1, Swift Striker -1.6
- 37k: Escalating Resilience -2.1, Toxic Bullets -3.7
- 50k: Recharging Rush -1.4, Escalating Resilience -2.1
- never picked: Hunter's Aura +6.1, Diviner's Kevlar +6.0, Guardian Ward +5.2, Heroic Aura +3.8, Divine Barrier +3.7, Duration Extender +3.4, Superior Duration +2.9, Grit +2.7

### Rem
- 10k: Decay -2.4
- 18k: Decay -2.4
- 27k: Decay -2.4, Return Fire -3.2
- 37k: Decay -2.4
- 50k: Disarming Hex -5.0, Decay -2.4
- never picked: Magic Carpet +3.7, Heroic Aura +3.5, Cheat Death +3.3, Close Quarters +1.9, Restorative Locket +1.9, Healing Nova +1.8, Grit +1.5

### Seven
- 18k: Decay -3.4
- 27k: Decay -3.4
- 37k: Decay -3.4
- 50k: Disarming Hex -6.5, Decay -3.4
- never picked: Diviner's Kevlar +3.3, Bullet Resist Shredder +2.9, Spirit Burn +2.8, Greater Expansion +2.1, Monster Rounds +1.6

### Shiv
- 18k: Stalker -2.6
- 27k: Stalker -2.6, Rapid Recharge -1.8, Escalating Exposure -1.4
- 37k: Stalker -2.6
- 50k: Escalating Exposure -1.4, Plated Armor -2.0
- never picked: Mystic Reverb +3.1, Silencer +3.0, Scourge +2.5, Torment Pulse +2.3, Witchmail +2.3, Ethereal Shift +1.7, Restorative Locket +1.6

### Silver
- 27k: Toxic Bullets -2.5
- 37k: Toxic Bullets -2.5
- 50k: Toxic Bullets -2.5
- never picked: Duration Extender +3.9, Restorative Locket +3.3, Superior Duration +2.9, Debuff Reducer +2.4, Phantom Strike +2.1, Diviner's Kevlar +1.8, Slowing Bullets +1.8

### Sinclair
- 10k: Improved Spirit -1.6
- 18k: Improved Spirit -1.6
- 27k: Decay -3.7
- 37k: Decay -3.7
- 50k: Boundless Spirit -2.1, Decay -3.7
- never picked: Heroic Aura +3.6, Magic Carpet +3.1, Mystic Reverb +2.5, Mystic Expansion +1.9, Extra Health +1.9

### Solomon
- 10k: Decay -3.2
- 18k: Rusted Barrel -3.4, Decay -3.2
- 27k: Decay -3.2
- 37k: Decay -3.2
- 50k: Boundless Spirit -1.8, Decay -3.2
- never picked: Magic Carpet +4.7, Spirit Burn +3.0, Spirit Resilience +1.8, Long Range +1.7, Mystic Vulnerability +1.7

### The Doorman
- 10k: Decay -4.3
- 27k: Decay -4.3
- 37k: Decay -4.3
- 50k: Metal Skin -6.2
- never picked: Mystic Reverb +2.9, Heroic Aura +2.7, Spirit Burn +2.4

### Venator
- 18k: Battle Vest -0.9, Escalating Resilience -1.7
- 27k: Escalating Resilience -1.7
- 37k: Cultist Sacrifice -2.4, Return Fire -3.5
- 50k: Crippling Headshot -2.8
- never picked: Magic Carpet +3.2, Frenzy +2.2, Spellslinger +1.9, Lucky Shot +1.7, Dispel Magic +1.6, Fleetfoot +1.6

### Victor
- 10k: Radiant Regeneration -1.6
- 18k: Radiant Regeneration -1.6
- 27k: Healing Booster -1.0, Radiant Regeneration -1.6
- 37k: Healing Booster -1.0, Radiant Regeneration -1.6, Escalating Exposure -2.2
- 50k: Healing Booster -1.0, Radiant Regeneration -1.6, Escalating Exposure -2.2
- never picked: Sprint Boots +3.7, Heroic Aura +3.5, Witchmail +3.3, Mystic Reverb +3.1, Mystic Expansion +2.4, Fleetfoot +2.4, Warp Stone +2.2, Scourge +2.2

### Vindicta
- 10k: Return Fire -3.5
- 18k: Return Fire -3.5
- 27k: Metal Skin -5.6, Return Fire -3.5, Swift Striker -0.9
- 37k: Opening Rounds -1.5, Return Fire -3.5, Swift Striker -0.9
- 50k: Metal Skin -5.6, Spiritual Overflow -2.7, Rusted Barrel -4.8, Return Fire -3.5
- never picked: Lucky Shot +3.4, Blood Tribute +3.4, Cheat Death +3.0, Heroic Aura +2.8, Weakening Headshot +2.8, Superior Duration +2.8, Duration Extender +2.4, Extended Magazine +1.9

### Viscous
- 10k: Decay -2.7
- 18k: Decay -2.7
- 27k: Decay -2.7, Return Fire -3.2
- 37k: Decay -2.7
- 50k: Metal Skin -6.0, Boundless Spirit -1.7, Decay -2.7
- never picked: Spirit Burn +2.4, Close Quarters +2.4

### Vyper
- 10k: Decay -3.3
- 18k: Decay -3.3
- 27k: Metal Skin -5.8, Decay -3.3
- never picked: Frenzy +3.4, Blood Tribute +2.8, Silencer +2.0, Spirit Lifesteal +2.0, Fleetfoot +1.9

### Warden
- 10k: Decay -3.3
- 18k: Decay -3.3
- 27k: Decay -3.3
- 37k: Decay -3.3, Return Fire -3.5
- 50k: Decay -3.3
- never picked: Magic Carpet +3.1, Siphon Bullets +2.1, Fleetfoot +2.1

### Wraith
- 10k: Decay -3.4
- 18k: Decay -3.4, Return Fire -3.9
- 27k: Decay -3.4
- 37k: Decay -3.4
- 50k: Decay -3.4, Mercurial Magnum -2.4
- never picked: Spirit Shredder +2.8, Tesla Bullets +2.8, Extra Spirit +2.6, Cheat Death +2.6, Spirit Resilience +2.6, Silencer +2.5, Bullet Resist Shredder +2.2, Rapid Rounds +2.2

### Yamato
- 18k: Mystic Shot -1.2, Rebuttal -2.3
- 27k: Mystic Shot -1.2, Decay -4.0
- 37k: Mystic Shot -1.2, Decay -4.0
- 50k: Mystic Shot -1.2, Decay -4.0
- never picked: Bullet Resist Shredder +3.8, Melee Charge +3.4, Extra Health +2.6, Mystic Regeneration +2.5, Superior Cooldown +2.2, Refresher +1.8, Dispel Magic +1.8, Compress Cooldown +1.7

