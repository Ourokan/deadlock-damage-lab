# Counter items in the sim (phantom and up)

Built 2026-10-24T14:08:54Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change (0.10 = 10% more damage before dying), weighted by how often each hero reaches that net worth. *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|
| Return Fire | 1,600 | +0.221 | +0.138 | Rat King +0.25, Grey Talon +0.18, Wraith +0.15 | 0 heroes |
| Spirit Resilience | 3,200 | +0.401 | +0.125 | Mo & Krill +0.56, Mina +0.43, Grey Talon +0.40 | 2 heroes |
| Reactive Barrier | 1,600 | +0.190 | +0.119 | Grey Talon +0.31, Wraith +0.27, Paige +0.24 | 2 heroes |
| Metal Skin | 3,200 | +0.296 | +0.093 | Wraith +0.76, Haze +0.35, Vyper +0.34 | 0 heroes |
| Healbane | 1,600 | +0.147 | +0.092 | Ivy +0.23, Mo & Krill +0.20, Victor +0.13 | 10 heroes |
| Bullet Resilience | 3,200 | +0.282 | +0.088 | Haze +0.45, Rat King +0.44, Vyper +0.29 | 0 heroes |
| Debuff Reducer | 1,600 | +0.127 | +0.080 | Wraith +0.19, Ivy +0.10, Holliday +0.08 | 0 heroes |
| Indomitable | 6,400 | +0.451 | +0.071 | Grey Talon +0.70, Wraith +0.62, Vyper +0.56 | 0 heroes |
| Spellbreaker | 6,400 | +0.446 | +0.070 | Grey Talon +0.55, Mo & Krill +0.50, Wraith +0.38 | 0 heroes |
| Dispel Magic | 3,200 | +0.216 | +0.068 | Mo & Krill +0.30, Mina +0.28, Pocket +0.27 | 4 heroes |
| Plated Armor | 6,400 | +0.423 | +0.066 | Haze +0.75, Holliday +0.66, Wraith +0.65 | 0 heroes |
| Witchmail | 6,400 | +0.411 | +0.064 | Mo & Krill +0.42, Wraith +0.35, Mina +0.34 | 0 heroes |
| Divine Barrier | 6,400 | +0.345 | +0.055 | Grey Talon +0.41, Wraith +0.34, Vindicta +0.33 | 0 heroes |
| Counterspell | 3,200 | +0.144 | +0.045 | Ivy +0.15, Wraith +0.13, Vyper +0.12 | 1 heroes |
| Unstoppable | 6,400 | +0.257 | +0.040 | Wraith +0.21, Rem +0.17, Rat King +0.17 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Metal Skin +0.07 (+0.36), Healbane +0.04 (+0.19), Debuff Reducer -0.06 (+0.07)
- **Seven**: Unstoppable +0.14 (+0.39), Metal Skin +0.10 (+0.39), Healbane +0.07 (+0.22)
- **Vindicta**: Divine Barrier +0.33 (+0.68), Plated Armor +0.23 (+0.65), Bullet Resilience +0.23 (+0.51)
- **Lady Geist**: Return Fire +0.03 (+0.26), Healbane +0.01 (+0.16), Counterspell -0.03 (+0.11)
- **Abrams**: Unstoppable +0.16 (+0.42), Indomitable +0.07 (+0.52), Reactive Barrier +0.07 (+0.26)
- **Wraith**: Metal Skin +0.76 (+1.06), Plated Armor +0.65 (+1.07), Indomitable +0.62 (+1.07)
- **McGinnis**: Healbane +0.02 (+0.16), Counterspell -0.01 (+0.13), Debuff Reducer -0.02 (+0.10)
- **Paradox**: Spellbreaker +0.17 (+0.62), Indomitable -0.02 (+0.43), Dispel Magic -0.05 (+0.16)
- **Dynamo**: Reactive Barrier +0.15 (+0.34), Dispel Magic +0.12 (+0.33), Witchmail +0.10 (+0.52)
- **Kelvin**: Witchmail +0.11 (+0.52), Spirit Resilience +0.10 (+0.50), Healbane +0.09 (+0.24)
- **Haze**: Plated Armor +0.75 (+1.17), Bullet Resilience +0.45 (+0.73), Metal Skin +0.35 (+0.64)
- **Holliday**: Plated Armor +0.66 (+1.08), Indomitable +0.45 (+0.90), Spellbreaker +0.24 (+0.69)
- **Bebop**: Healbane +0.10 (+0.24), Witchmail +0.06 (+0.47), Counterspell +0.04 (+0.19)
- **Calico**: Spirit Resilience +0.34 (+0.74), Indomitable +0.32 (+0.77), Divine Barrier +0.26 (+0.60)
- **Grey Talon**: Indomitable +0.70 (+1.15), Spellbreaker +0.55 (+1.00), Divine Barrier +0.41 (+0.75)
- **Mo & Krill**: Spirit Resilience +0.56 (+0.96), Spellbreaker +0.50 (+0.94), Witchmail +0.42 (+0.83)
- **Shiv**: Dispel Magic -0.04 (+0.17), Healbane -0.04 (+0.10), Return Fire -0.07 (+0.15)
- **Ivy**: Healbane +0.23 (+0.38), Counterspell +0.15 (+0.30), Bullet Resilience +0.13 (+0.41)
- **Warden**: Dispel Magic +0.03 (+0.24), Bullet Resilience +0.01 (+0.30), Debuff Reducer +0.01 (+0.13)
- **Yamato**: Healbane -0.05 (+0.10), Debuff Reducer -0.07 (+0.05), Counterspell -0.08 (+0.06)
- **Lash**: Spellbreaker +0.12 (+0.57), Witchmail -0.02 (+0.39), Spirit Resilience -0.03 (+0.38)
- **Viscous**: Spellbreaker +0.01 (+0.45), Reactive Barrier -0.05 (+0.14), Healbane -0.05 (+0.10)
- **Pocket**: Dispel Magic +0.27 (+0.49), Spirit Resilience +0.14 (+0.54), Spellbreaker +0.09 (+0.53)
- **Mirage**: Spellbreaker +0.19 (+0.64), Plated Armor +0.14 (+0.56), Unstoppable +0.10 (+0.36)
- **Vyper**: Indomitable +0.56 (+1.01), Plated Armor +0.35 (+0.78), Metal Skin +0.34 (+0.64)
- **Sinclair**: Indomitable +0.27 (+0.72), Spirit Resilience +0.18 (+0.58), Spellbreaker +0.08 (+0.52)
- **Mina**: Spirit Resilience +0.43 (+0.83), Spellbreaker +0.35 (+0.80), Witchmail +0.34 (+0.75)
- **Drifter**: Dispel Magic +0.26 (+0.48), Return Fire -0.01 (+0.21), Reactive Barrier -0.04 (+0.15)
- **Venator**: Return Fire +0.10 (+0.32), Reactive Barrier +0.09 (+0.28), Unstoppable +0.02 (+0.28)
- **Victor**: Healbane +0.13 (+0.28), Dispel Magic +0.02 (+0.24), Witchmail -0.01 (+0.40)
- **Paige**: Indomitable +0.37 (+0.82), Spellbreaker +0.31 (+0.76), Spirit Resilience +0.28 (+0.69)
- **The Doorman**: Indomitable +0.38 (+0.83), Spirit Resilience +0.34 (+0.74), Witchmail +0.24 (+0.65)
- **Billy**: Counterspell -0.04 (+0.11), Healbane -0.05 (+0.10), Debuff Reducer -0.05 (+0.08)
- **Graves**: Return Fire +0.05 (+0.27), Debuff Reducer -0.07 (+0.05), Counterspell -0.08 (+0.07)
- **Apollo**: Debuff Reducer -0.10 (+0.03), Healbane -0.12 (+0.03), Counterspell -0.12 (+0.02)
- **Deadman Danny**: Dispel Magic +0.03 (+0.25), Reactive Barrier +0.03 (+0.22), Healbane +0.03 (+0.17)
- **Rem**: Unstoppable +0.17 (+0.43), Healbane +0.08 (+0.22), Debuff Reducer +0.06 (+0.19)
- **Silver**: Dispel Magic -0.04 (+0.17), Debuff Reducer -0.09 (+0.04), Healbane -0.09 (+0.06)
- **Celeste**: Spirit Resilience -0.00 (+0.40), Dispel Magic -0.06 (+0.15), Counterspell -0.09 (+0.05)
- **Rat King**: Plated Armor +0.46 (+0.88), Bullet Resilience +0.44 (+0.72), Metal Skin +0.29 (+0.59)
- **Solomon**: Spirit Resilience +0.20 (+0.60), Reactive Barrier +0.11 (+0.30), Witchmail +0.11 (+0.52)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.326 | +0.102 | Mina +0.64, Grey Talon +0.47, The Doorman +0.32 | 7 heroes |
| Return Fire | 1,600 | +0.163 | +0.102 | Wraith +0.18, Venator +0.16, Rat King +0.14 | 0 heroes |
| Reactive Barrier | 1,600 | +0.139 | +0.087 | Wraith +0.24, Mina +0.23, Paige +0.20 | 2 heroes |
| Metal Skin | 3,200 | +0.247 | +0.077 | Wraith +0.62, Haze +0.42, Vyper +0.35 | 0 heroes |
| Healbane | 1,600 | +0.100 | +0.062 | Mo & Krill +0.15, Ivy +0.09, Victor +0.09 | 14 heroes |
| Bullet Resilience | 3,200 | +0.199 | +0.062 | Haze +0.43, Rat King +0.27, Paige +0.23 | 0 heroes |
| Indomitable | 6,400 | +0.367 | +0.058 | Vyper +0.56, Wraith +0.54, Paige +0.46 | 0 heroes |
| Debuff Reducer | 1,600 | +0.089 | +0.056 | Wraith +0.14, Lash +0.12, Dynamo +0.09 | 1 heroes |
| Spellbreaker | 6,400 | +0.355 | +0.056 | Grey Talon +0.50, Holliday +0.49, Mina +0.41 | 0 heroes |
| Dispel Magic | 3,200 | +0.157 | +0.049 | McGinnis +0.41, Pocket +0.32, Mina +0.31 | 7 heroes |
| Plated Armor | 6,400 | +0.311 | +0.049 | Haze +0.76, Holliday +0.71, Wraith +0.42 | 0 heroes |
| Witchmail | 6,400 | +0.298 | +0.046 | Wraith +0.32, Mina +0.30, The Doorman +0.24 | 0 heroes |
| Divine Barrier | 6,400 | +0.238 | +0.038 | Wraith +0.24, Paige +0.23, Mina +0.23 | 1 heroes |
| Unstoppable | 6,400 | +0.200 | +0.031 | Paige +0.30, Rem +0.24, Abrams +0.19 | 1 heroes |
| Counterspell | 3,200 | +0.071 | +0.022 | Wraith +0.09, Vyper +0.07, Mina +0.07 | 1 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Metal Skin +0.25 (+0.49), Healbane +0.07 (+0.17), Dispel Magic -0.01 (+0.15)
- **Seven**: Witchmail +0.07 (+0.37), Spirit Resilience +0.05 (+0.37), Unstoppable +0.02 (+0.22)
- **Vindicta**: Divine Barrier +0.14 (+0.38), Plated Armor +0.09 (+0.40), Bullet Resilience +0.09 (+0.29)
- **Lady Geist**: Return Fire +0.08 (+0.24), Healbane -0.03 (+0.07), Counterspell -0.08 (-0.00)
- **Abrams**: Unstoppable +0.19 (+0.39), Reactive Barrier +0.04 (+0.18), Dispel Magic +0.03 (+0.19)
- **Wraith**: Metal Skin +0.62 (+0.87), Indomitable +0.54 (+0.91), Plated Armor +0.42 (+0.73)
- **McGinnis**: Dispel Magic +0.41 (+0.57), Healbane +0.03 (+0.13), Spirit Resilience +0.02 (+0.35)
- **Paradox**: Spellbreaker +0.01 (+0.36), Counterspell -0.05 (+0.02), Return Fire -0.05 (+0.11)
- **Dynamo**: Witchmail +0.19 (+0.49), Indomitable +0.18 (+0.54), Spirit Resilience +0.10 (+0.42)
- **Kelvin**: Healbane +0.01 (+0.11), Witchmail +0.01 (+0.30), Counterspell +0.01 (+0.08)
- **Haze**: Plated Armor +0.76 (+1.08), Bullet Resilience +0.43 (+0.63), Metal Skin +0.42 (+0.67)
- **Holliday**: Plated Armor +0.71 (+1.02), Spellbreaker +0.49 (+0.84), Indomitable +0.44 (+0.81)
- **Bebop**: Healbane +0.04 (+0.14), Counterspell +0.00 (+0.07), Debuff Reducer -0.01 (+0.08)
- **Calico**: Spirit Resilience +0.30 (+0.62), Divine Barrier +0.19 (+0.43), Reactive Barrier +0.19 (+0.33)
- **Grey Talon**: Spellbreaker +0.50 (+0.85), Spirit Resilience +0.47 (+0.80), Indomitable +0.22 (+0.58)
- **Mo & Krill**: Spellbreaker +0.39 (+0.75), Spirit Resilience +0.26 (+0.58), Healbane +0.15 (+0.24)
- **Shiv**: Dispel Magic -0.01 (+0.15), Counterspell -0.03 (+0.04), Healbane -0.03 (+0.07)
- **Ivy**: Healbane +0.09 (+0.19), Metal Skin -0.01 (+0.24), Reactive Barrier -0.02 (+0.12)
- **Warden**: Dispel Magic +0.12 (+0.28), Bullet Resilience +0.05 (+0.25), Plated Armor +0.04 (+0.35)
- **Yamato**: Counterspell -0.01 (+0.07), Healbane -0.02 (+0.08), Debuff Reducer -0.06 (+0.03)
- **Lash**: Spellbreaker +0.28 (+0.64), Indomitable +0.24 (+0.61), Dispel Magic +0.13 (+0.28)
- **Viscous**: Spellbreaker +0.21 (+0.57), Healbane +0.01 (+0.11), Reactive Barrier -0.02 (+0.12)
- **Pocket**: Dispel Magic +0.32 (+0.47), Spirit Resilience +0.13 (+0.46), Witchmail +0.13 (+0.43)
- **Mirage**: Spellbreaker +0.10 (+0.45), Metal Skin +0.08 (+0.33), Plated Armor +0.04 (+0.35)
- **Vyper**: Indomitable +0.56 (+0.93), Metal Skin +0.35 (+0.60), Plated Armor +0.31 (+0.62)
- **Sinclair**: Indomitable +0.14 (+0.51), Debuff Reducer +0.05 (+0.14), Spellbreaker +0.02 (+0.37)
- **Mina**: Spirit Resilience +0.64 (+0.96), Spellbreaker +0.41 (+0.76), Dispel Magic +0.31 (+0.47)
- **Drifter**: Dispel Magic +0.31 (+0.46), Return Fire +0.02 (+0.18), Spellbreaker +0.01 (+0.37)
- **Venator**: Return Fire +0.16 (+0.32), Reactive Barrier +0.06 (+0.20), Unstoppable +0.03 (+0.23)
- **Victor**: Healbane +0.09 (+0.19), Counterspell -0.04 (+0.03), Witchmail -0.09 (+0.21)
- **Paige**: Indomitable +0.46 (+0.83), Unstoppable +0.30 (+0.50), Spirit Resilience +0.30 (+0.62)
- **The Doorman**: Indomitable +0.43 (+0.80), Spirit Resilience +0.32 (+0.65), Spellbreaker +0.24 (+0.60)
- **Billy**: Healbane +0.01 (+0.11), Return Fire -0.03 (+0.13), Counterspell -0.03 (+0.04)
- **Graves**: Return Fire +0.08 (+0.24), Counterspell -0.03 (+0.04), Reactive Barrier -0.05 (+0.09)
- **Apollo**: Healbane -0.06 (+0.04), Counterspell -0.07 (+0.00), Debuff Reducer -0.10 (-0.01)
- **Deadman Danny**: Healbane +0.06 (+0.16), Spirit Resilience +0.05 (+0.37), Spellbreaker +0.01 (+0.36)
- **Rem**: Unstoppable +0.24 (+0.44), Indomitable +0.22 (+0.58), Reactive Barrier +0.05 (+0.19)
- **Silver**: Dispel Magic +0.09 (+0.24), Debuff Reducer -0.00 (+0.09), Unstoppable -0.02 (+0.18)
- **Celeste**: Counterspell -0.06 (+0.01), Healbane -0.08 (+0.02), Debuff Reducer -0.08 (+0.01)
- **Rat King**: Plated Armor +0.29 (+0.61), Bullet Resilience +0.27 (+0.47), Metal Skin +0.15 (+0.40)
- **Solomon**: Spirit Resilience +0.11 (+0.44), Reactive Barrier +0.07 (+0.21), Spellbreaker +0.06 (+0.41)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.317 | +0.099 | Mina +0.49, Holliday +0.49, Lash +0.44 | 11 heroes |
| Return Fire | 1,600 | +0.159 | +0.099 | Wraith +0.17, Haze +0.12, Holliday +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | +0.123 | +0.077 | Wraith +0.20, Grey Talon +0.19, Holliday +0.17 | 1 heroes |
| Metal Skin | 3,200 | +0.237 | +0.074 | Haze +0.57, Wraith +0.51, Vyper +0.32 | 0 heroes |
| Healbane | 1,600 | +0.113 | +0.070 | Ivy +0.23, Haze +0.16, Bebop +0.15 | 13 heroes |
| Bullet Resilience | 3,200 | +0.173 | +0.054 | Haze +0.56, Wraith +0.27, Holliday +0.17 | 0 heroes |
| Indomitable | 6,400 | +0.329 | +0.051 | Holliday +0.66, Wraith +0.55, The Doorman +0.50 | 0 heroes |
| Dispel Magic | 3,200 | +0.162 | +0.051 | McGinnis +0.32, Mo & Krill +0.26, Lash +0.25 | 9 heroes |
| Debuff Reducer | 1,600 | +0.080 | +0.050 | Holliday +0.21, Lash +0.19, Wraith +0.11 | 0 heroes |
| Spellbreaker | 6,400 | +0.300 | +0.047 | Holliday +0.54, Lash +0.46, Grey Talon +0.43 | 0 heroes |
| Plated Armor | 6,400 | +0.284 | +0.044 | Haze +0.83, Holliday +0.78, Wraith +0.42 | 0 heroes |
| Witchmail | 6,400 | +0.276 | +0.043 | Mina +0.26, Wraith +0.26, Lash +0.24 | 1 heroes |
| Unstoppable | 6,400 | +0.198 | +0.031 | Rem +0.30, Haze +0.28, Paige +0.21 | 3 heroes |
| Divine Barrier | 6,400 | +0.181 | +0.029 | Grey Talon +0.25, Wraith +0.20, Lash +0.20 | 2 heroes |
| Counterspell | 3,200 | +0.066 | +0.021 | Wraith +0.11, Holliday +0.09, The Doorman +0.07 | 1 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Metal Skin +0.06 (+0.30), Healbane +0.02 (+0.13), Debuff Reducer -0.05 (+0.03)
- **Seven**: Unstoppable +0.12 (+0.32), Spirit Resilience +0.10 (+0.42), Witchmail +0.07 (+0.35)
- **Vindicta**: Spirit Resilience +0.04 (+0.36), Plated Armor +0.04 (+0.32), Witchmail +0.03 (+0.30)
- **Lady Geist**: Return Fire +0.09 (+0.25), Counterspell -0.04 (+0.02), Healbane -0.07 (+0.05)
- **Abrams**: Unstoppable +0.01 (+0.21), Reactive Barrier -0.03 (+0.10), Dispel Magic -0.04 (+0.12)
- **Wraith**: Indomitable +0.55 (+0.88), Metal Skin +0.51 (+0.75), Plated Armor +0.42 (+0.71)
- **McGinnis**: Dispel Magic +0.32 (+0.48), Witchmail +0.01 (+0.28), Healbane +0.00 (+0.12)
- **Paradox**: Dispel Magic +0.06 (+0.22), Unstoppable +0.04 (+0.24), Debuff Reducer +0.02 (+0.10)
- **Dynamo**: Counterspell -0.01 (+0.05), Debuff Reducer -0.02 (+0.06), Healbane -0.03 (+0.09)
- **Kelvin**: Spirit Resilience +0.04 (+0.36), Healbane +0.03 (+0.15), Divine Barrier +0.02 (+0.20)
- **Haze**: Plated Armor +0.83 (+1.11), Metal Skin +0.57 (+0.81), Bullet Resilience +0.56 (+0.73)
- **Holliday**: Plated Armor +0.78 (+1.06), Indomitable +0.66 (+0.98), Spellbreaker +0.54 (+0.84)
- **Bebop**: Healbane +0.15 (+0.26), Counterspell +0.04 (+0.10), Return Fire -0.03 (+0.13)
- **Calico**: Spirit Resilience +0.10 (+0.41), Reactive Barrier +0.05 (+0.17), Counterspell +0.02 (+0.09)
- **Grey Talon**: Spellbreaker +0.43 (+0.73), Divine Barrier +0.25 (+0.43), Indomitable +0.24 (+0.57)
- **Mo & Krill**: Spellbreaker +0.33 (+0.63), Dispel Magic +0.26 (+0.42), Spirit Resilience +0.26 (+0.57)
- **Shiv**: Dispel Magic -0.01 (+0.15), Counterspell -0.03 (+0.04), Return Fire -0.03 (+0.13)
- **Ivy**: Healbane +0.23 (+0.34), Return Fire -0.03 (+0.13), Reactive Barrier -0.04 (+0.08)
- **Warden**: Healbane +0.07 (+0.18), Metal Skin +0.01 (+0.25), Counterspell -0.02 (+0.04)
- **Yamato**: Healbane -0.05 (+0.06), Counterspell -0.05 (+0.01), Debuff Reducer -0.06 (+0.02)
- **Lash**: Spellbreaker +0.46 (+0.76), Indomitable +0.44 (+0.77), Spirit Resilience +0.44 (+0.75)
- **Viscous**: Dispel Magic +0.08 (+0.25), Spellbreaker +0.07 (+0.37), Reactive Barrier +0.06 (+0.19)
- **Pocket**: Dispel Magic +0.22 (+0.39), Spirit Resilience +0.03 (+0.35), Counterspell -0.00 (+0.06)
- **Mirage**: Metal Skin +0.04 (+0.27), Spellbreaker +0.03 (+0.33), Debuff Reducer -0.02 (+0.06)
- **Vyper**: Indomitable +0.44 (+0.77), Metal Skin +0.32 (+0.55), Plated Armor +0.31 (+0.59)
- **Sinclair**: Indomitable +0.20 (+0.53), Spellbreaker +0.11 (+0.41), Debuff Reducer +0.07 (+0.15)
- **Mina**: Spirit Resilience +0.49 (+0.81), Spellbreaker +0.41 (+0.71), Witchmail +0.26 (+0.54)
- **Drifter**: Dispel Magic +0.13 (+0.29), Return Fire +0.02 (+0.18), Counterspell +0.02 (+0.08)
- **Venator**: Unstoppable +0.14 (+0.33), Return Fire +0.07 (+0.23), Counterspell -0.01 (+0.06)
- **Victor**: Healbane +0.04 (+0.15), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.03)
- **Paige**: Spirit Resilience +0.24 (+0.56), Witchmail +0.24 (+0.51), Indomitable +0.23 (+0.56)
- **The Doorman**: Indomitable +0.50 (+0.83), Spirit Resilience +0.23 (+0.54), Witchmail +0.19 (+0.47)
- **Billy**: Debuff Reducer -0.01 (+0.07), Counterspell -0.02 (+0.05), Healbane -0.03 (+0.08)
- **Graves**: Return Fire +0.08 (+0.24), Counterspell -0.04 (+0.02), Debuff Reducer -0.06 (+0.02)
- **Apollo**: Counterspell -0.03 (+0.03), Healbane -0.04 (+0.07), Debuff Reducer -0.06 (+0.02)
- **Deadman Danny**: Counterspell -0.01 (+0.05), Debuff Reducer -0.03 (+0.05), Reactive Barrier -0.04 (+0.08)
- **Rem**: Unstoppable +0.30 (+0.50), Debuff Reducer +0.05 (+0.13), Witchmail +0.05 (+0.33)
- **Silver**: Dispel Magic -0.01 (+0.15), Counterspell -0.03 (+0.03), Bullet Resilience -0.04 (+0.13)
- **Celeste**: Counterspell -0.05 (+0.02), Debuff Reducer -0.07 (+0.01), Healbane -0.07 (+0.04)
- **Rat King**: Metal Skin +0.13 (+0.36), Plated Armor +0.10 (+0.39), Bullet Resilience +0.09 (+0.26)
- **Solomon**: Spirit Resilience +0.14 (+0.46), Spellbreaker +0.13 (+0.43), Dispel Magic +0.12 (+0.28)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|
| Return Fire | 1,600 | +0.131 | +0.082 | Graves +0.14, Wraith +0.10, Rat King +0.09 | 0 heroes |
| Spirit Resilience | 3,200 | +0.262 | +0.082 | Lash +0.54, The Doorman +0.45, Rem +0.43 | 13 heroes |
| Metal Skin | 3,200 | +0.251 | +0.079 | Wraith +0.66, Haze +0.35, Vyper +0.20 | 0 heroes |
| Reactive Barrier | 1,600 | +0.097 | +0.060 | Vyper +0.20, Rem +0.18, Grey Talon +0.12 | 0 heroes |
| Healbane | 1,600 | +0.092 | +0.057 | Bebop +0.14, Yamato +0.10, McGinnis +0.08 | 9 heroes |
| Indomitable | 6,400 | +0.350 | +0.055 | Wraith +0.89, The Doorman +0.76, Vyper +0.58 | 1 heroes |
| Debuff Reducer | 1,600 | +0.083 | +0.052 | Wraith +0.21, Lash +0.13, Dynamo +0.11 | 0 heroes |
| Bullet Resilience | 3,200 | +0.151 | +0.047 | Haze +0.41, Wraith +0.22, Vyper +0.14 | 0 heroes |
| Spellbreaker | 6,400 | +0.302 | +0.047 | Lash +0.51, Wraith +0.41, Paige +0.36 | 0 heroes |
| Dispel Magic | 3,200 | +0.147 | +0.046 | Pocket +0.34, McGinnis +0.30, The Doorman +0.28 | 9 heroes |
| Plated Armor | 6,400 | +0.283 | +0.044 | Haze +0.77, Wraith +0.51, Holliday +0.35 | 3 heroes |
| Witchmail | 6,400 | +0.253 | +0.040 | Rem +0.55, The Doorman +0.38, Lash +0.32 | 3 heroes |
| Unstoppable | 6,400 | +0.249 | +0.039 | Rem +0.55, Paige +0.35, Haze +0.21 | 6 heroes |
| Divine Barrier | 6,400 | +0.137 | +0.021 | Lash +0.19, Rem +0.18, Wraith +0.17 | 3 heroes |
| Counterspell | 3,200 | +0.046 | +0.015 | Vyper +0.14, Lash +0.10, Paige +0.06 | 1 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Metal Skin +0.18 (+0.43), Unstoppable +0.12 (+0.37), Healbane +0.03 (+0.12)
- **Seven**: Spellbreaker +0.21 (+0.51), Spirit Resilience +0.11 (+0.37), Metal Skin +0.05 (+0.30)
- **Vindicta**: Healbane +0.03 (+0.13), Counterspell -0.01 (+0.04), Spellbreaker -0.01 (+0.30)
- **Lady Geist**: Return Fire +0.04 (+0.17), Counterspell +0.01 (+0.05), Healbane +0.00 (+0.09)
- **Abrams**: Unstoppable -0.00 (+0.25), Counterspell -0.03 (+0.02), Debuff Reducer -0.05 (+0.04)
- **Wraith**: Indomitable +0.89 (+1.24), Metal Skin +0.66 (+0.91), Plated Armor +0.51 (+0.79)
- **McGinnis**: Dispel Magic +0.30 (+0.45), Witchmail +0.21 (+0.46), Spirit Resilience +0.17 (+0.43)
- **Paradox**: Unstoppable +0.05 (+0.30), Return Fire +0.00 (+0.13), Spellbreaker -0.02 (+0.28)
- **Dynamo**: Debuff Reducer +0.11 (+0.19), Reactive Barrier +0.03 (+0.13), Dispel Magic +0.03 (+0.17)
- **Kelvin**: Healbane +0.07 (+0.16), Counterspell -0.00 (+0.04), Spirit Resilience -0.04 (+0.22)
- **Haze**: Plated Armor +0.77 (+1.06), Bullet Resilience +0.41 (+0.56), Metal Skin +0.35 (+0.60)
- **Holliday**: Plated Armor +0.35 (+0.64), Indomitable +0.27 (+0.62), Spellbreaker +0.16 (+0.46)
- **Bebop**: Healbane +0.14 (+0.23), Counterspell -0.01 (+0.04), Return Fire -0.04 (+0.09)
- **Calico**: Reactive Barrier +0.00 (+0.10), Spirit Resilience -0.01 (+0.25), Counterspell -0.01 (+0.03)
- **Grey Talon**: Spellbreaker +0.21 (+0.51), Witchmail +0.15 (+0.40), Spirit Resilience +0.14 (+0.40)
- **Mo & Krill**: Healbane +0.02 (+0.11), Debuff Reducer -0.02 (+0.06), Spellbreaker -0.03 (+0.27)
- **Shiv**: Counterspell -0.03 (+0.01), Dispel Magic -0.04 (+0.10), Healbane -0.05 (+0.04)
- **Ivy**: Healbane +0.02 (+0.11), Debuff Reducer -0.02 (+0.06), Counterspell -0.02 (+0.02)
- **Warden**: Witchmail +0.11 (+0.36), Spirit Resilience +0.04 (+0.30), Bullet Resilience +0.04 (+0.19)
- **Yamato**: Healbane +0.10 (+0.19), Counterspell +0.03 (+0.07), Debuff Reducer -0.02 (+0.07)
- **Lash**: Spirit Resilience +0.54 (+0.81), Spellbreaker +0.51 (+0.81), Indomitable +0.37 (+0.72)
- **Viscous**: Spirit Resilience +0.08 (+0.35), Spellbreaker +0.08 (+0.38), Witchmail +0.05 (+0.31)
- **Pocket**: Dispel Magic +0.34 (+0.49), Divine Barrier +0.08 (+0.22), Spirit Resilience +0.08 (+0.34)
- **Mirage**: Metal Skin +0.11 (+0.36), Spellbreaker +0.11 (+0.41), Debuff Reducer -0.02 (+0.06)
- **Vyper**: Indomitable +0.58 (+0.93), Plated Armor +0.28 (+0.57), Reactive Barrier +0.20 (+0.30)
- **Sinclair**: Indomitable +0.15 (+0.50), Spellbreaker +0.13 (+0.43), Debuff Reducer +0.08 (+0.16)
- **Mina**: Spirit Resilience +0.27 (+0.53), Dispel Magic +0.25 (+0.39), Witchmail +0.24 (+0.49)
- **Drifter**: Dispel Magic +0.25 (+0.39), Spellbreaker +0.07 (+0.37), Reactive Barrier +0.03 (+0.13)
- **Venator**: Unstoppable +0.15 (+0.40), Bullet Resilience +0.06 (+0.22), Reactive Barrier +0.03 (+0.13)
- **Victor**: Healbane +0.07 (+0.17), Debuff Reducer -0.01 (+0.07), Counterspell -0.03 (+0.02)
- **Paige**: Spellbreaker +0.36 (+0.67), Unstoppable +0.35 (+0.60), Spirit Resilience +0.33 (+0.59)
- **The Doorman**: Indomitable +0.76 (+1.11), Spirit Resilience +0.45 (+0.71), Witchmail +0.38 (+0.63)
- **Billy**: Divine Barrier +0.08 (+0.22), Counterspell +0.01 (+0.06), Reactive Barrier +0.01 (+0.10)
- **Graves**: Spirit Resilience +0.20 (+0.46), Witchmail +0.14 (+0.40), Return Fire +0.14 (+0.27)
- **Apollo**: Counterspell -0.06 (-0.01), Debuff Reducer -0.08 (+0.01), Healbane -0.08 (+0.01)
- **Deadman Danny**: Counterspell +0.00 (+0.05), Debuff Reducer -0.04 (+0.04), Healbane -0.05 (+0.04)
- **Rem**: Unstoppable +0.55 (+0.80), Witchmail +0.55 (+0.80), Spirit Resilience +0.43 (+0.69)
- **Silver**: Dispel Magic -0.00 (+0.14), Counterspell -0.03 (+0.02), Reactive Barrier -0.04 (+0.06)
- **Celeste**: Counterspell +0.00 (+0.05), Reactive Barrier -0.01 (+0.09), Divine Barrier -0.03 (+0.11)
- **Rat King**: Metal Skin +0.16 (+0.41), Return Fire +0.09 (+0.22), Bullet Resilience +0.03 (+0.18)
- **Solomon**: Dispel Magic +0.10 (+0.24), Spellbreaker +0.05 (+0.35), Divine Barrier +0.05 (+0.19)
