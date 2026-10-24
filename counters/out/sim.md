# Counter items in the sim (phantom and up)

Built 2026-10-24T21:57:02Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.464 | +0.145 | +0.370 | Mo & Krill +0.58, Grey Talon +0.34, Sinclair +0.33 | 1 heroes |
| Reactive Barrier | 1,600 | +0.176 | +0.110 | +0.172 | Wraith +0.24, Solomon +0.21, Calico +0.17 | 1 heroes |
| Divine Barrier | 6,400 | +0.620 | +0.099 | +0.331 | Vindicta +0.31, Wraith +0.27, Calico +0.23 | 0 heroes |
| Debuff Reducer | 1,600 | +0.140 | +0.087 | +0.123 | Wraith +0.21, Holliday +0.09, Paige +0.08 | 0 heroes |
| Bullet Resilience | 3,200 | +0.261 | +0.081 | +0.272 | Rat King +0.46, Haze +0.41, Vindicta +0.18 | 0 heroes |
| Healbane | 1,600 | +0.128 | +0.080 | +0.151 | Mo & Krill +0.19, Wraith +0.11, Ivy +0.10 | 11 heroes |
| Dispel Magic | 3,200 | +0.245 | +0.077 | +0.209 | Mirage +0.56, Nurse Harrow +0.39, Mo & Krill +0.34 | 4 heroes |
| Witchmail | 6,400 | +0.456 | +0.071 | +0.402 | Mo & Krill +0.40, Wraith +0.30, Solomon +0.25 | 0 heroes |
| Spellbreaker | 6,400 | +0.428 | +0.067 | +0.422 | Mo & Krill +0.56, Grey Talon +0.42, Sinclair +0.36 | 0 heroes |
| Indomitable | 6,400 | +0.421 | +0.066 | +0.417 | Wraith +0.51, Holliday +0.43, Vyper +0.40 | 0 heroes |
| Plated Armor | 6,400 | +0.309 | +0.048 | +0.416 | Haze +0.73, Holliday +0.68, Wraith +0.49 | 0 heroes |
| Counterspell | 3,200 | +0.112 | +0.035 | +0.140 | Wraith +0.18, Solomon +0.11, Nurse Harrow +0.10 | 1 heroes |
| Return Fire | 1,600 | +0.034 | +0.021 | +0.229 | Rat King +0.22, Wraith +0.19, Venator +0.14 | 0 heroes |
| Metal Skin | 3,200 | +0.065 | +0.020 | +0.299 | Wraith +0.64, Haze +0.35, Rat King +0.23 | 0 heroes |
| Unstoppable | 6,400 | +0.129 | +0.020 | +0.243 | Rem +0.27, Wraith +0.22, Paige +0.20 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.21 (+0.42), Healbane +0.05 (+0.20), Metal Skin +0.04 (+0.34)
- **Seven**: Plated Armor +0.17 (+0.59), Metal Skin +0.08 (+0.38), Spirit Resilience +0.08 (+0.45)
- **Vindicta**: Divine Barrier +0.31 (+0.64), Plated Armor +0.23 (+0.65), Bullet Resilience +0.18 (+0.45)
- **Lady Geist**: Return Fire -0.02 (+0.21), Healbane -0.03 (+0.12), Counterspell -0.10 (+0.05)
- **Abrams**: Unstoppable +0.11 (+0.35), Indomitable +0.03 (+0.45), Reactive Barrier +0.02 (+0.19)
- **Wraith**: Metal Skin +0.64 (+0.93), Indomitable +0.51 (+0.93), Plated Armor +0.49 (+0.90)
- **McGinnis**: Healbane +0.04 (+0.19), Witchmail +0.01 (+0.41), Debuff Reducer -0.01 (+0.11)
- **Paradox**: Unstoppable -0.00 (+0.24), Dispel Magic -0.01 (+0.19), Indomitable -0.04 (+0.37)
- **Dynamo**: Indomitable +0.20 (+0.62), Spellbreaker +0.15 (+0.57), Witchmail +0.06 (+0.46)
- **Kelvin**: Spirit Resilience +0.10 (+0.47), Spellbreaker +0.09 (+0.51), Witchmail +0.05 (+0.45)
- **Haze**: Plated Armor +0.73 (+1.15), Bullet Resilience +0.41 (+0.68), Metal Skin +0.35 (+0.65)
- **Holliday**: Plated Armor +0.68 (+1.09), Indomitable +0.43 (+0.85), Spellbreaker +0.25 (+0.67)
- **Bebop**: Spellbreaker +0.01 (+0.43), Healbane +0.00 (+0.15), Counterspell -0.05 (+0.09)
- **Calico**: Spirit Resilience +0.27 (+0.64), Indomitable +0.25 (+0.66), Spellbreaker +0.24 (+0.66)
- **Grey Talon**: Spellbreaker +0.42 (+0.84), Indomitable +0.39 (+0.80), Spirit Resilience +0.34 (+0.71)
- **Mo & Krill**: Spirit Resilience +0.58 (+0.95), Spellbreaker +0.56 (+0.98), Witchmail +0.40 (+0.80)
- **Shiv**: Healbane -0.03 (+0.12), Return Fire -0.08 (+0.15), Counterspell -0.08 (+0.06)
- **Ivy**: Metal Skin +0.11 (+0.41), Healbane +0.10 (+0.25), Bullet Resilience +0.09 (+0.36)
- **Warden**: Dispel Magic +0.19 (+0.40), Metal Skin +0.18 (+0.48), Bullet Resilience +0.17 (+0.45)
- **Yamato**: Debuff Reducer -0.08 (+0.05), Counterspell -0.08 (+0.06), Healbane -0.09 (+0.06)
- **Lash**: Spellbreaker +0.12 (+0.54), Healbane +0.06 (+0.21), Spirit Resilience +0.04 (+0.41)
- **Viscous**: Spellbreaker +0.08 (+0.51), Reactive Barrier +0.03 (+0.20), Healbane +0.01 (+0.16)
- **Pocket**: Spirit Resilience +0.10 (+0.47), Spellbreaker +0.07 (+0.49), Witchmail +0.06 (+0.46)
- **Mirage**: Dispel Magic +0.56 (+0.77), Spellbreaker +0.18 (+0.60), Plated Armor +0.16 (+0.58)
- **Vyper**: Indomitable +0.40 (+0.82), Metal Skin +0.21 (+0.51), Plated Armor +0.21 (+0.62)
- **Sinclair**: Indomitable +0.37 (+0.78), Spellbreaker +0.36 (+0.79), Spirit Resilience +0.33 (+0.70)
- **Mina**: Spirit Resilience +0.32 (+0.69), Spellbreaker +0.23 (+0.65), Indomitable +0.20 (+0.62)
- **Drifter**: Dispel Magic +0.07 (+0.28), Return Fire +0.01 (+0.24), Debuff Reducer -0.05 (+0.07)
- **Venator**: Return Fire +0.14 (+0.37), Reactive Barrier +0.05 (+0.22), Metal Skin +0.03 (+0.33)
- **Victor**: Healbane +0.01 (+0.16), Spirit Resilience -0.13 (+0.24), Debuff Reducer -0.14 (-0.01)
- **Paige**: Indomitable +0.23 (+0.64), Witchmail +0.22 (+0.62), Unstoppable +0.20 (+0.44)
- **The Doorman**: Indomitable +0.31 (+0.73), Spirit Resilience +0.20 (+0.57), Witchmail +0.18 (+0.58)
- **Billy**: Divine Barrier -0.07 (+0.26), Counterspell -0.08 (+0.06), Unstoppable -0.08 (+0.16)
- **Graves**: Return Fire -0.02 (+0.21), Counterspell -0.07 (+0.07), Reactive Barrier -0.07 (+0.10)
- **Apollo**: Healbane -0.11 (+0.04), Debuff Reducer -0.12 (+0.00), Counterspell -0.14 (-0.00)
- **Deadman Danny**: Spellbreaker +0.14 (+0.57), Unstoppable +0.07 (+0.31), Spirit Resilience +0.06 (+0.43)
- **Rem**: Unstoppable +0.27 (+0.51), Indomitable +0.24 (+0.65), Dispel Magic +0.13 (+0.34)
- **Silver**: Dispel Magic +0.05 (+0.26), Reactive Barrier +0.02 (+0.19), Unstoppable +0.02 (+0.26)
- **Celeste**: Spirit Resilience +0.19 (+0.56), Witchmail +0.07 (+0.47), Dispel Magic +0.01 (+0.22)
- **Rat King**: Bullet Resilience +0.46 (+0.73), Plated Armor +0.45 (+0.86), Metal Skin +0.23 (+0.53)
- **Solomon**: Witchmail +0.25 (+0.65), Indomitable +0.22 (+0.64), Reactive Barrier +0.21 (+0.39)
- **Nurse Harrow**: Dispel Magic +0.39 (+0.60), Divine Barrier +0.18 (+0.51), Witchmail +0.16 (+0.56)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.377 | +0.118 | +0.296 | Mina +0.56, Nurse Harrow +0.34, The Doorman +0.33 | 10 heroes |
| Reactive Barrier | 1,600 | +0.127 | +0.080 | +0.125 | Mina +0.24, The Doorman +0.17, Wraith +0.16 | 2 heroes |
| Divine Barrier | 6,400 | +0.449 | +0.071 | +0.207 | Vindicta +0.35, Mina +0.24, The Doorman +0.17 | 1 heroes |
| Debuff Reducer | 1,600 | +0.095 | +0.060 | +0.082 | Lash +0.13, Nurse Harrow +0.13, Wraith +0.12 | 1 heroes |
| Dispel Magic | 3,200 | +0.174 | +0.054 | +0.142 | Nurse Harrow +0.77, Mina +0.33, Infernus +0.28 | 7 heroes |
| Bullet Resilience | 3,200 | +0.173 | +0.054 | +0.185 | Haze +0.53, Rat King +0.26, Vindicta +0.18 | 0 heroes |
| Witchmail | 6,400 | +0.325 | +0.051 | +0.278 | Mina +0.35, Nurse Harrow +0.29, The Doorman +0.27 | 0 heroes |
| Indomitable | 6,400 | +0.319 | +0.050 | +0.313 | Vyper +0.53, The Doorman +0.43, Wraith +0.42 | 0 heroes |
| Spellbreaker | 6,400 | +0.312 | +0.049 | +0.309 | Mina +0.39, Holliday +0.37, Grey Talon +0.32 | 0 heroes |
| Healbane | 1,600 | +0.077 | +0.048 | +0.113 | Nurse Harrow +0.21, Ivy +0.09, Haze +0.08 | 16 heroes |
| Plated Armor | 6,400 | +0.194 | +0.030 | +0.293 | Haze +0.83, Holliday +0.57, Wraith +0.31 | 0 heroes |
| Counterspell | 3,200 | +0.048 | +0.015 | +0.076 | Nurse Harrow +0.16, Mina +0.09, Wraith +0.09 | 1 heroes |
| Unstoppable | 6,400 | +0.065 | +0.010 | +0.173 | Rem +0.32, Paige +0.20, Abrams +0.15 | 1 heroes |
| Metal Skin | 3,200 | +0.012 | +0.004 | +0.235 | Wraith +0.50, Haze +0.36, Vyper +0.23 | 0 heroes |
| Return Fire | 1,600 | -0.020 | -0.013 | +0.165 | Venator +0.13, Rat King +0.11, Wraith +0.11 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.28 (+0.42), Metal Skin +0.21 (+0.44), Healbane +0.06 (+0.17)
- **Seven**: Witchmail +0.13 (+0.41), Spirit Resilience +0.10 (+0.40), Indomitable +0.06 (+0.37)
- **Vindicta**: Divine Barrier +0.35 (+0.56), Plated Armor +0.19 (+0.49), Witchmail +0.18 (+0.46)
- **Lady Geist**: Return Fire +0.06 (+0.22), Healbane -0.03 (+0.08), Debuff Reducer -0.08 (+0.00)
- **Abrams**: Unstoppable +0.15 (+0.32), Reactive Barrier +0.05 (+0.18), Dispel Magic +0.04 (+0.18)
- **Wraith**: Metal Skin +0.50 (+0.73), Indomitable +0.42 (+0.73), Plated Armor +0.31 (+0.61)
- **McGinnis**: Spirit Resilience +0.15 (+0.45), Witchmail +0.10 (+0.37), Healbane +0.05 (+0.17)
- **Paradox**: Unstoppable +0.05 (+0.22), Dispel Magic +0.04 (+0.18), Spellbreaker -0.01 (+0.30)
- **Dynamo**: Healbane +0.07 (+0.18), Debuff Reducer +0.03 (+0.11), Counterspell -0.01 (+0.06)
- **Kelvin**: Spellbreaker +0.16 (+0.46), Spirit Resilience +0.08 (+0.38), Divine Barrier -0.00 (+0.20)
- **Haze**: Plated Armor +0.83 (+1.13), Bullet Resilience +0.53 (+0.72), Metal Skin +0.36 (+0.59)
- **Holliday**: Plated Armor +0.57 (+0.86), Spellbreaker +0.37 (+0.68), Indomitable +0.36 (+0.67)
- **Bebop**: Healbane +0.02 (+0.14), Counterspell -0.01 (+0.07), Debuff Reducer -0.05 (+0.03)
- **Calico**: Spirit Resilience +0.18 (+0.47), Reactive Barrier +0.07 (+0.20), Divine Barrier +0.05 (+0.26)
- **Grey Talon**: Spellbreaker +0.32 (+0.63), Spirit Resilience +0.26 (+0.56), Indomitable +0.14 (+0.45)
- **Mo & Krill**: Spirit Resilience +0.22 (+0.51), Spellbreaker +0.21 (+0.52), Dispel Magic +0.05 (+0.20)
- **Shiv**: Healbane +0.00 (+0.12), Counterspell -0.02 (+0.05), Return Fire -0.03 (+0.14)
- **Ivy**: Healbane +0.09 (+0.20), Counterspell +0.00 (+0.08), Return Fire -0.00 (+0.16)
- **Warden**: Dispel Magic +0.14 (+0.28), Witchmail +0.12 (+0.40), Spirit Resilience +0.08 (+0.38)
- **Yamato**: Healbane -0.03 (+0.08), Counterspell -0.06 (+0.01), Debuff Reducer -0.08 (+0.00)
- **Lash**: Spellbreaker +0.28 (+0.58), Indomitable +0.16 (+0.47), Debuff Reducer +0.13 (+0.21)
- **Viscous**: Spellbreaker +0.19 (+0.50), Reactive Barrier +0.05 (+0.17), Witchmail +0.02 (+0.30)
- **Pocket**: Spellbreaker +0.10 (+0.40), Witchmail +0.09 (+0.36), Spirit Resilience +0.06 (+0.35)
- **Mirage**: Dispel Magic +0.25 (+0.39), Plated Armor +0.09 (+0.39), Spellbreaker +0.07 (+0.38)
- **Vyper**: Indomitable +0.53 (+0.85), Metal Skin +0.23 (+0.46), Reactive Barrier +0.15 (+0.27)
- **Sinclair**: Indomitable +0.31 (+0.62), Spirit Resilience +0.30 (+0.60), Spellbreaker +0.21 (+0.52)
- **Mina**: Spirit Resilience +0.56 (+0.86), Spellbreaker +0.39 (+0.70), Witchmail +0.35 (+0.62)
- **Drifter**: Dispel Magic +0.02 (+0.17), Return Fire -0.02 (+0.14), Healbane -0.04 (+0.07)
- **Venator**: Return Fire +0.13 (+0.30), Metal Skin +0.03 (+0.26), Reactive Barrier +0.01 (+0.14)
- **Victor**: Healbane +0.02 (+0.13), Counterspell -0.06 (+0.01), Witchmail -0.09 (+0.19)
- **Paige**: Spirit Resilience +0.30 (+0.59), Indomitable +0.27 (+0.59), Spellbreaker +0.21 (+0.52)
- **The Doorman**: Indomitable +0.43 (+0.75), Spirit Resilience +0.33 (+0.63), Witchmail +0.27 (+0.55)
- **Billy**: Return Fire -0.02 (+0.14), Healbane -0.03 (+0.08), Counterspell -0.04 (+0.03)
- **Graves**: Return Fire +0.03 (+0.20), Metal Skin +0.01 (+0.24), Witchmail +0.01 (+0.28)
- **Apollo**: Counterspell -0.06 (+0.02), Healbane -0.06 (+0.05), Debuff Reducer -0.07 (+0.01)
- **Deadman Danny**: Healbane -0.01 (+0.10), Debuff Reducer -0.02 (+0.06), Counterspell -0.03 (+0.05)
- **Rem**: Unstoppable +0.32 (+0.50), Debuff Reducer +0.06 (+0.14), Healbane +0.02 (+0.13)
- **Silver**: Dispel Magic +0.04 (+0.18), Reactive Barrier +0.02 (+0.14), Debuff Reducer +0.01 (+0.10)
- **Celeste**: Spirit Resilience +0.23 (+0.52), Dispel Magic +0.05 (+0.20), Witchmail +0.05 (+0.32)
- **Rat King**: Bullet Resilience +0.26 (+0.45), Plated Armor +0.24 (+0.53), Metal Skin +0.15 (+0.39)
- **Solomon**: Spirit Resilience +0.30 (+0.59), Spellbreaker +0.24 (+0.55), Reactive Barrier +0.14 (+0.27)
- **Nurse Harrow**: Dispel Magic +0.77 (+0.91), Spirit Resilience +0.34 (+0.64), Witchmail +0.29 (+0.56)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.367 | +0.115 | +0.291 | Holliday +0.51, Lash +0.46, Solomon +0.35 | 13 heroes |
| Reactive Barrier | 1,600 | +0.124 | +0.078 | +0.123 | Wraith +0.19, Holliday +0.19, Grey Talon +0.19 | 3 heroes |
| Debuff Reducer | 1,600 | +0.091 | +0.057 | +0.077 | Holliday +0.19, Lash +0.14, Wraith +0.11 | 0 heroes |
| Divine Barrier | 6,400 | +0.355 | +0.056 | +0.193 | Wraith +0.25, Lash +0.23, Vindicta +0.23 | 2 heroes |
| Dispel Magic | 3,200 | +0.178 | +0.056 | +0.146 | Nurse Harrow +0.70, Mirage +0.31, Lash +0.27 | 9 heroes |
| Witchmail | 6,400 | +0.339 | +0.053 | +0.291 | Wraith +0.31, Lash +0.30, Nurse Harrow +0.22 | 1 heroes |
| Indomitable | 6,400 | +0.330 | +0.052 | +0.322 | Holliday +0.64, Wraith +0.49, Vyper +0.48 | 0 heroes |
| Bullet Resilience | 3,200 | +0.160 | +0.050 | +0.172 | Haze +0.42, Nurse Harrow +0.24, Wraith +0.14 | 0 heroes |
| Spellbreaker | 6,400 | +0.310 | +0.048 | +0.304 | Holliday +0.55, Lash +0.45, Solomon +0.33 | 0 heroes |
| Healbane | 1,600 | +0.064 | +0.040 | +0.104 | Nurse Harrow +0.23, Mo & Krill +0.08, Infernus +0.08 | 15 heroes |
| Plated Armor | 6,400 | +0.191 | +0.030 | +0.294 | Holliday +0.77, Haze +0.53, Wraith +0.47 | 0 heroes |
| Unstoppable | 6,400 | +0.074 | +0.012 | +0.181 | Rem +0.29, Solomon +0.26, Paige +0.19 | 3 heroes |
| Counterspell | 3,200 | +0.027 | +0.008 | +0.055 | Nurse Harrow +0.12, Vyper +0.07, Paige +0.06 | 1 heroes |
| Metal Skin | 3,200 | +0.023 | +0.007 | +0.249 | Wraith +0.63, Vyper +0.31, Haze +0.22 | 0 heroes |
| Return Fire | 1,600 | -0.029 | -0.018 | +0.155 | Vindicta +0.13, Wraith +0.11, Venator +0.10 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.20 (+0.35), Healbane +0.08 (+0.18), Unstoppable +0.02 (+0.20)
- **Seven**: Metal Skin +0.14 (+0.39), Spirit Resilience +0.08 (+0.37), Dispel Magic +0.06 (+0.20)
- **Vindicta**: Divine Barrier +0.23 (+0.42), Plated Armor +0.16 (+0.46), Bullet Resilience +0.13 (+0.31)
- **Lady Geist**: Healbane +0.03 (+0.13), Return Fire -0.03 (+0.12), Counterspell -0.06 (-0.01)
- **Abrams**: Counterspell -0.03 (+0.03), Debuff Reducer -0.04 (+0.04), Unstoppable -0.04 (+0.14)
- **Wraith**: Metal Skin +0.63 (+0.88), Indomitable +0.49 (+0.81), Plated Armor +0.47 (+0.76)
- **McGinnis**: Healbane +0.00 (+0.11), Counterspell -0.02 (+0.03), Spirit Resilience -0.04 (+0.25)
- **Paradox**: Spirit Resilience +0.15 (+0.44), Unstoppable +0.09 (+0.27), Spellbreaker +0.08 (+0.38)
- **Dynamo**: Counterspell +0.02 (+0.07), Healbane +0.02 (+0.12), Debuff Reducer -0.01 (+0.07)
- **Kelvin**: Spellbreaker +0.05 (+0.36), Witchmail +0.03 (+0.32), Spirit Resilience +0.01 (+0.30)
- **Haze**: Plated Armor +0.53 (+0.83), Bullet Resilience +0.42 (+0.59), Indomitable +0.22 (+0.54)
- **Holliday**: Plated Armor +0.77 (+1.06), Indomitable +0.64 (+0.96), Spellbreaker +0.55 (+0.85)
- **Bebop**: Healbane +0.03 (+0.14), Counterspell -0.06 (-0.00), Bullet Resilience -0.08 (+0.09)
- **Calico**: Spirit Resilience +0.27 (+0.56), Spellbreaker +0.19 (+0.49), Witchmail +0.16 (+0.45)
- **Grey Talon**: Spellbreaker +0.32 (+0.63), Indomitable +0.22 (+0.54), Reactive Barrier +0.19 (+0.31)
- **Mo & Krill**: Spellbreaker +0.30 (+0.61), Dispel Magic +0.20 (+0.34), Spirit Resilience +0.18 (+0.47)
- **Shiv**: Return Fire -0.01 (+0.14), Healbane -0.02 (+0.09), Metal Skin -0.02 (+0.23)
- **Ivy**: Metal Skin +0.11 (+0.36), Plated Armor +0.05 (+0.34), Bullet Resilience +0.05 (+0.22)
- **Warden**: Healbane +0.01 (+0.12), Counterspell -0.01 (+0.05), Dispel Magic -0.02 (+0.13)
- **Yamato**: Healbane +0.01 (+0.12), Counterspell -0.01 (+0.05), Reactive Barrier -0.05 (+0.08)
- **Lash**: Spirit Resilience +0.46 (+0.75), Spellbreaker +0.45 (+0.75), Indomitable +0.38 (+0.70)
- **Viscous**: Reactive Barrier +0.08 (+0.20), Spellbreaker +0.07 (+0.37), Divine Barrier +0.04 (+0.24)
- **Pocket**: Spellbreaker +0.01 (+0.32), Counterspell -0.00 (+0.05), Spirit Resilience -0.01 (+0.28)
- **Mirage**: Dispel Magic +0.31 (+0.46), Metal Skin +0.11 (+0.36), Plated Armor +0.06 (+0.36)
- **Vyper**: Indomitable +0.48 (+0.80), Metal Skin +0.31 (+0.56), Plated Armor +0.28 (+0.58)
- **Sinclair**: Indomitable +0.29 (+0.61), Spellbreaker +0.28 (+0.59), Spirit Resilience +0.24 (+0.53)
- **Mina**: Spirit Resilience +0.34 (+0.63), Spellbreaker +0.31 (+0.62), Dispel Magic +0.19 (+0.33)
- **Drifter**: Dispel Magic +0.05 (+0.19), Return Fire -0.02 (+0.13), Counterspell -0.03 (+0.03)
- **Venator**: Unstoppable +0.17 (+0.35), Return Fire +0.10 (+0.25), Reactive Barrier +0.04 (+0.16)
- **Victor**: Healbane +0.06 (+0.16), Counterspell -0.02 (+0.03), Spirit Resilience -0.04 (+0.25)
- **Paige**: Unstoppable +0.19 (+0.37), Indomitable +0.19 (+0.51), Spirit Resilience +0.14 (+0.43)
- **The Doorman**: Indomitable +0.45 (+0.77), Spirit Resilience +0.32 (+0.61), Spellbreaker +0.19 (+0.49)
- **Billy**: Healbane -0.03 (+0.07), Counterspell -0.03 (+0.02), Debuff Reducer -0.05 (+0.03)
- **Graves**: Return Fire +0.05 (+0.21), Counterspell -0.00 (+0.05), Metal Skin -0.02 (+0.23)
- **Apollo**: Debuff Reducer -0.06 (+0.02), Counterspell -0.06 (-0.01), Healbane -0.08 (+0.02)
- **Deadman Danny**: Healbane -0.04 (+0.06), Counterspell -0.05 (+0.00), Debuff Reducer -0.07 (+0.01)
- **Rem**: Unstoppable +0.29 (+0.47), Debuff Reducer +0.03 (+0.11), Reactive Barrier +0.01 (+0.13)
- **Silver**: Dispel Magic +0.05 (+0.20), Debuff Reducer +0.01 (+0.09), Unstoppable +0.01 (+0.19)
- **Celeste**: Spirit Resilience +0.08 (+0.37), Healbane +0.07 (+0.18), Witchmail +0.06 (+0.35)
- **Rat King**: Plated Armor +0.11 (+0.40), Metal Skin +0.09 (+0.34), Return Fire +0.09 (+0.24)
- **Solomon**: Spirit Resilience +0.35 (+0.64), Spellbreaker +0.33 (+0.63), Unstoppable +0.26 (+0.44)
- **Nurse Harrow**: Dispel Magic +0.70 (+0.84), Spirit Resilience +0.29 (+0.58), Bullet Resilience +0.24 (+0.41)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.416 | +0.130 | +0.315 | Nurse Harrow +0.76, Mina +0.62, Lash +0.53 | 16 heroes |
| Reactive Barrier | 1,600 | +0.114 | +0.071 | +0.116 | Mina +0.26, Lash +0.25, Solomon +0.20 | 2 heroes |
| Debuff Reducer | 1,600 | +0.096 | +0.060 | +0.085 | Dynamo +0.23, Wraith +0.19, Holliday +0.19 | 0 heroes |
| Indomitable | 6,400 | +0.344 | +0.054 | +0.340 | The Doorman +0.64, Wraith +0.62, Lash +0.46 | 1 heroes |
| Spellbreaker | 6,400 | +0.320 | +0.050 | +0.313 | Lash +0.53, Mina +0.40, Solomon +0.34 | 0 heroes |
| Witchmail | 6,400 | +0.309 | +0.048 | +0.265 | Mina +0.34, McGinnis +0.30, Nurse Harrow +0.29 | 2 heroes |
| Bullet Resilience | 3,200 | +0.141 | +0.044 | +0.153 | Haze +0.31, Rat King +0.17, Nurse Harrow +0.08 | 0 heroes |
| Dispel Magic | 3,200 | +0.139 | +0.043 | +0.110 | Nurse Harrow +0.84, Drifter +0.34, Mina +0.25 | 9 heroes |
| Divine Barrier | 6,400 | +0.256 | +0.040 | +0.155 | Solomon +0.25, Mina +0.23, Lash +0.20 | 3 heroes |
| Healbane | 1,600 | +0.058 | +0.036 | +0.091 | Victor +0.14, Mo & Krill +0.10, Nurse Harrow +0.10 | 12 heroes |
| Plated Armor | 6,400 | +0.164 | +0.026 | +0.273 | Haze +0.46, Wraith +0.28, Vyper +0.28 | 1 heroes |
| Unstoppable | 6,400 | +0.115 | +0.018 | +0.223 | Paige +0.45, Seven +0.35, Rem +0.33 | 8 heroes |
| Metal Skin | 3,200 | +0.055 | +0.017 | +0.287 | Wraith +0.52, Haze +0.30, Seven +0.21 | 0 heroes |
| Counterspell | 3,200 | +0.012 | +0.004 | +0.042 | Lash +0.07, Nurse Harrow +0.06, Rem +0.06 | 1 heroes |
| Return Fire | 1,600 | -0.040 | -0.025 | +0.145 | Rat King +0.15, Lash +0.13, Wraith +0.13 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.16 (+0.27), Unstoppable +0.11 (+0.34), Healbane +0.07 (+0.16)
- **Seven**: Spirit Resilience +0.41 (+0.72), Unstoppable +0.35 (+0.58), Plated Armor +0.23 (+0.50)
- **Vindicta**: Dispel Magic +0.13 (+0.24), Plated Armor +0.10 (+0.37), Spirit Resilience +0.08 (+0.40)
- **Lady Geist**: Healbane +0.01 (+0.10), Counterspell -0.04 (+0.00), Bullet Resilience -0.06 (+0.10)
- **Abrams**: Counterspell -0.03 (+0.01), Debuff Reducer -0.04 (+0.04), Unstoppable -0.05 (+0.17)
- **Wraith**: Indomitable +0.62 (+0.96), Metal Skin +0.52 (+0.81), Spellbreaker +0.31 (+0.63)
- **McGinnis**: Spirit Resilience +0.45 (+0.77), Witchmail +0.30 (+0.57), Spellbreaker +0.06 (+0.38)
- **Paradox**: Unstoppable +0.22 (+0.44), Dispel Magic +0.09 (+0.20), Spellbreaker +0.02 (+0.33)
- **Dynamo**: Debuff Reducer +0.23 (+0.31), Unstoppable +0.21 (+0.43), Witchmail +0.07 (+0.33)
- **Kelvin**: Spirit Resilience +0.11 (+0.42), Healbane +0.05 (+0.14), Spellbreaker +0.04 (+0.35)
- **Haze**: Plated Armor +0.46 (+0.74), Bullet Resilience +0.31 (+0.46), Metal Skin +0.30 (+0.58)
- **Holliday**: Indomitable +0.40 (+0.74), Spellbreaker +0.33 (+0.64), Plated Armor +0.20 (+0.47)
- **Bebop**: Healbane +0.07 (+0.16), Debuff Reducer +0.00 (+0.09), Counterspell -0.01 (+0.03)
- **Calico**: Counterspell -0.02 (+0.02), Dispel Magic -0.04 (+0.07), Healbane -0.05 (+0.04)
- **Grey Talon**: Spellbreaker +0.06 (+0.37), Dispel Magic +0.02 (+0.13), Debuff Reducer +0.01 (+0.09)
- **Mo & Krill**: Spellbreaker +0.16 (+0.47), Healbane +0.10 (+0.20), Dispel Magic +0.04 (+0.15)
- **Shiv**: Counterspell -0.03 (+0.02), Bullet Resilience -0.03 (+0.13), Divine Barrier -0.03 (+0.12)
- **Ivy**: Healbane +0.05 (+0.14), Counterspell +0.03 (+0.07), Unstoppable +0.01 (+0.23)
- **Warden**: Spirit Resilience +0.06 (+0.37), Reactive Barrier +0.06 (+0.17), Witchmail +0.05 (+0.31)
- **Yamato**: Healbane +0.10 (+0.19), Reactive Barrier +0.06 (+0.17), Divine Barrier +0.02 (+0.18)
- **Lash**: Spirit Resilience +0.53 (+0.85), Spellbreaker +0.53 (+0.84), Indomitable +0.46 (+0.80)
- **Viscous**: Spellbreaker +0.12 (+0.43), Reactive Barrier +0.02 (+0.14), Witchmail +0.02 (+0.29)
- **Pocket**: Counterspell -0.01 (+0.03), Dispel Magic -0.04 (+0.07), Divine Barrier -0.04 (+0.11)
- **Mirage**: Dispel Magic +0.16 (+0.27), Metal Skin +0.12 (+0.40), Plated Armor +0.07 (+0.34)
- **Vyper**: Plated Armor +0.28 (+0.55), Indomitable +0.16 (+0.50), Metal Skin +0.14 (+0.43)
- **Sinclair**: Indomitable +0.25 (+0.59), Debuff Reducer +0.10 (+0.18), Spellbreaker +0.08 (+0.39)
- **Mina**: Spirit Resilience +0.62 (+0.93), Spellbreaker +0.40 (+0.71), Witchmail +0.34 (+0.61)
- **Drifter**: Dispel Magic +0.34 (+0.45), Divine Barrier +0.05 (+0.21), Spellbreaker +0.05 (+0.36)
- **Venator**: Return Fire +0.11 (+0.25), Unstoppable +0.07 (+0.29), Reactive Barrier +0.04 (+0.15)
- **Victor**: Healbane +0.14 (+0.23), Counterspell -0.01 (+0.03), Debuff Reducer -0.03 (+0.05)
- **Paige**: Unstoppable +0.45 (+0.67), Spirit Resilience +0.39 (+0.70), Indomitable +0.21 (+0.55)
- **The Doorman**: Indomitable +0.64 (+0.98), Spirit Resilience +0.24 (+0.55), Witchmail +0.17 (+0.44)
- **Billy**: Divine Barrier +0.01 (+0.16), Counterspell +0.00 (+0.04), Reactive Barrier -0.01 (+0.11)
- **Graves**: Return Fire +0.03 (+0.18), Healbane -0.01 (+0.08), Counterspell -0.02 (+0.02)
- **Apollo**: Healbane -0.04 (+0.05), Counterspell -0.05 (-0.00), Debuff Reducer -0.08 (+0.00)
- **Deadman Danny**: Healbane -0.03 (+0.06), Counterspell -0.04 (+0.00), Reactive Barrier -0.06 (+0.05)
- **Rem**: Unstoppable +0.33 (+0.55), Spirit Resilience +0.31 (+0.62), Witchmail +0.20 (+0.47)
- **Silver**: Dispel Magic +0.05 (+0.16), Unstoppable +0.03 (+0.25), Counterspell -0.00 (+0.04)
- **Celeste**: Spirit Resilience +0.17 (+0.48), Witchmail +0.03 (+0.30), Healbane +0.00 (+0.09)
- **Rat King**: Plated Armor +0.18 (+0.46), Bullet Resilience +0.17 (+0.33), Metal Skin +0.17 (+0.46)
- **Solomon**: Spirit Resilience +0.45 (+0.76), Spellbreaker +0.34 (+0.66), Witchmail +0.28 (+0.54)
- **Nurse Harrow**: Dispel Magic +0.84 (+0.95), Spirit Resilience +0.76 (+1.08), Witchmail +0.29 (+0.55)
