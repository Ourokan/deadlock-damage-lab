# Counter items in the sim (phantom and up)

Built 2026-10-24T16:52:30Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.472 | +0.147 | +0.391 | Mo & Krill +0.55, Mina +0.40, Grey Talon +0.39 | 2 heroes |
| Reactive Barrier | 1,600 | +0.189 | +0.118 | +0.186 | Grey Talon +0.26, Paige +0.22, Calico +0.21 | 2 heroes |
| Debuff Reducer | 1,600 | +0.145 | +0.091 | +0.126 | Wraith +0.20, Holliday +0.09, Paige +0.07 | 0 heroes |
| Bullet Resilience | 3,200 | +0.253 | +0.079 | +0.274 | Haze +0.46, Rat King +0.44, Paige +0.24 | 0 heroes |
| Dispel Magic | 3,200 | +0.241 | +0.075 | +0.213 | Mirage +0.57, Mo & Krill +0.31, Infernus +0.25 | 4 heroes |
| Healbane | 1,600 | +0.119 | +0.074 | +0.138 | Mo & Krill +0.21, Deadman Danny +0.15, Mirage +0.13 | 10 heroes |
| Witchmail | 6,400 | +0.461 | +0.072 | +0.411 | Mo & Krill +0.42, Wraith +0.30, Paige +0.28 | 0 heroes |
| Indomitable | 6,400 | +0.450 | +0.071 | +0.444 | Wraith +0.56, Vyper +0.56, Grey Talon +0.53 | 0 heroes |
| Spellbreaker | 6,400 | +0.443 | +0.069 | +0.443 | Grey Talon +0.56, Mo & Krill +0.53, Sinclair +0.34 | 0 heroes |
| Divine Barrier | 6,400 | +0.366 | +0.058 | +0.345 | Grey Talon +0.40, Vindicta +0.30, Wraith +0.27 | 0 heroes |
| Plated Armor | 6,400 | +0.312 | +0.049 | +0.430 | Haze +0.74, Holliday +0.62, Wraith +0.58 | 0 heroes |
| Return Fire | 1,600 | +0.072 | +0.045 | +0.224 | Rat King +0.23, Grey Talon +0.18, Wraith +0.17 | 0 heroes |
| Counterspell | 3,200 | +0.118 | +0.037 | +0.131 | Ivy +0.14, Rat King +0.10, The Doorman +0.10 | 1 heroes |
| Unstoppable | 6,400 | +0.147 | +0.023 | +0.249 | Wraith +0.21, Rem +0.18, Solomon +0.17 | 0 heroes |
| Metal Skin | 3,200 | +0.069 | +0.021 | +0.305 | Wraith +0.65, Haze +0.35, Vyper +0.34 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.25 (+0.47), Metal Skin +0.09 (+0.40), Healbane +0.06 (+0.19)
- **Seven**: Unstoppable +0.14 (+0.39), Metal Skin +0.08 (+0.39), Healbane +0.07 (+0.21)
- **Vindicta**: Divine Barrier +0.30 (+0.65), Plated Armor +0.21 (+0.64), Bullet Resilience +0.19 (+0.46)
- **Lady Geist**: Return Fire +0.04 (+0.27), Healbane +0.02 (+0.16), Counterspell -0.05 (+0.08)
- **Abrams**: Unstoppable +0.17 (+0.42), Reactive Barrier +0.07 (+0.25), Indomitable +0.06 (+0.50)
- **Wraith**: Metal Skin +0.65 (+0.96), Plated Armor +0.58 (+1.01), Indomitable +0.56 (+1.01)
- **McGinnis**: Healbane +0.04 (+0.18), Counterspell +0.01 (+0.14), Debuff Reducer -0.02 (+0.10)
- **Paradox**: Spellbreaker +0.13 (+0.57), Indomitable -0.05 (+0.40), Reactive Barrier -0.07 (+0.11)
- **Dynamo**: Reactive Barrier +0.16 (+0.34), Indomitable +0.11 (+0.55), Witchmail +0.11 (+0.52)
- **Kelvin**: Witchmail +0.09 (+0.50), Healbane +0.09 (+0.22), Spirit Resilience +0.08 (+0.48)
- **Haze**: Plated Armor +0.74 (+1.17), Bullet Resilience +0.46 (+0.73), Metal Skin +0.35 (+0.65)
- **Holliday**: Plated Armor +0.62 (+1.05), Indomitable +0.42 (+0.86), Spellbreaker +0.23 (+0.67)
- **Bebop**: Spellbreaker +0.07 (+0.51), Healbane +0.06 (+0.19), Witchmail +0.03 (+0.44)
- **Calico**: Spirit Resilience +0.29 (+0.68), Indomitable +0.27 (+0.71), Divine Barrier +0.27 (+0.61)
- **Grey Talon**: Spellbreaker +0.56 (+1.00), Indomitable +0.53 (+0.97), Divine Barrier +0.40 (+0.75)
- **Mo & Krill**: Spirit Resilience +0.55 (+0.94), Spellbreaker +0.53 (+0.98), Witchmail +0.42 (+0.83)
- **Shiv**: Healbane -0.03 (+0.11), Return Fire -0.06 (+0.17), Counterspell -0.09 (+0.04)
- **Ivy**: Metal Skin +0.28 (+0.58), Plated Armor +0.24 (+0.67), Dispel Magic +0.21 (+0.42)
- **Warden**: Dispel Magic +0.04 (+0.25), Bullet Resilience +0.02 (+0.29), Healbane +0.02 (+0.16)
- **Yamato**: Healbane -0.05 (+0.09), Debuff Reducer -0.09 (+0.04), Counterspell -0.10 (+0.03)
- **Lash**: Spellbreaker +0.10 (+0.55), Counterspell -0.01 (+0.13), Debuff Reducer -0.01 (+0.12)
- **Viscous**: Healbane -0.00 (+0.14), Counterspell -0.02 (+0.11), Reactive Barrier -0.04 (+0.15)
- **Pocket**: Spirit Resilience +0.13 (+0.52), Spellbreaker +0.11 (+0.55), Witchmail +0.09 (+0.50)
- **Mirage**: Dispel Magic +0.57 (+0.78), Spellbreaker +0.22 (+0.66), Plated Armor +0.18 (+0.61)
- **Vyper**: Indomitable +0.56 (+1.00), Plated Armor +0.36 (+0.79), Metal Skin +0.34 (+0.64)
- **Sinclair**: Indomitable +0.44 (+0.89), Spellbreaker +0.34 (+0.78), Spirit Resilience +0.30 (+0.69)
- **Mina**: Spirit Resilience +0.40 (+0.79), Spellbreaker +0.31 (+0.75), Witchmail +0.25 (+0.66)
- **Drifter**: Dispel Magic +0.15 (+0.36), Return Fire -0.01 (+0.22), Reactive Barrier -0.03 (+0.16)
- **Venator**: Return Fire +0.11 (+0.33), Metal Skin +0.04 (+0.34), Reactive Barrier +0.00 (+0.19)
- **Victor**: Healbane +0.09 (+0.22), Dispel Magic +0.01 (+0.22), Spirit Resilience -0.05 (+0.34)
- **Paige**: Indomitable +0.36 (+0.81), Spellbreaker +0.29 (+0.73), Spirit Resilience +0.28 (+0.67)
- **The Doorman**: Indomitable +0.36 (+0.81), Spirit Resilience +0.32 (+0.71), Witchmail +0.21 (+0.63)
- **Billy**: Healbane -0.03 (+0.10), Counterspell -0.05 (+0.08), Debuff Reducer -0.05 (+0.07)
- **Graves**: Return Fire +0.06 (+0.28), Counterspell -0.08 (+0.05), Debuff Reducer -0.09 (+0.04)
- **Apollo**: Debuff Reducer -0.10 (+0.03), Healbane -0.10 (+0.04), Counterspell -0.11 (+0.02)
- **Deadman Danny**: Healbane +0.15 (+0.28), Witchmail +0.05 (+0.46), Counterspell +0.03 (+0.16)
- **Rem**: Unstoppable +0.18 (+0.43), Healbane +0.08 (+0.22), Debuff Reducer +0.05 (+0.18)
- **Silver**: Unstoppable -0.01 (+0.24), Dispel Magic -0.01 (+0.20), Healbane -0.01 (+0.12)
- **Celeste**: Spirit Resilience +0.05 (+0.44), Healbane -0.05 (+0.09), Witchmail -0.06 (+0.35)
- **Rat King**: Plated Armor +0.45 (+0.88), Bullet Resilience +0.44 (+0.71), Metal Skin +0.28 (+0.59)
- **Solomon**: Reactive Barrier +0.18 (+0.36), Unstoppable +0.17 (+0.42), Spirit Resilience +0.17 (+0.56)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.412 | +0.129 | +0.340 | Mina +0.64, Grey Talon +0.45, Wraith +0.41 | 7 heroes |
| Reactive Barrier | 1,600 | +0.142 | +0.088 | +0.139 | Wraith +0.27, Mina +0.24, Paige +0.19 | 2 heroes |
| Debuff Reducer | 1,600 | +0.115 | +0.072 | +0.098 | Wraith +0.20, Lash +0.12, Dynamo +0.09 | 1 heroes |
| Indomitable | 6,400 | +0.383 | +0.060 | +0.376 | Wraith +0.61, Vyper +0.53, Paige +0.43 | 0 heroes |
| Spellbreaker | 6,400 | +0.370 | +0.058 | +0.372 | Grey Talon +0.48, Mina +0.44, Holliday +0.42 | 0 heroes |
| Bullet Resilience | 3,200 | +0.179 | +0.056 | +0.198 | Haze +0.44, Rat King +0.27, Paige +0.21 | 0 heroes |
| Witchmail | 6,400 | +0.358 | +0.056 | +0.311 | Wraith +0.39, Mina +0.34, The Doorman +0.23 | 0 heroes |
| Dispel Magic | 3,200 | +0.177 | +0.055 | +0.148 | Mina +0.30, Mirage +0.30, Infernus +0.27 | 7 heroes |
| Healbane | 1,600 | +0.084 | +0.052 | +0.104 | Mo & Krill +0.15, Wraith +0.12, Deadman Danny +0.12 | 14 heroes |
| Divine Barrier | 6,400 | +0.259 | +0.041 | +0.240 | Wraith +0.27, Mina +0.23, Paige +0.21 | 1 heroes |
| Plated Armor | 6,400 | +0.217 | +0.034 | +0.326 | Haze +0.76, Holliday +0.69, Wraith +0.51 | 0 heroes |
| Counterspell | 3,200 | +0.060 | +0.019 | +0.074 | Wraith +0.14, Mina +0.09, The Doorman +0.07 | 1 heroes |
| Unstoppable | 6,400 | +0.105 | +0.016 | +0.206 | Paige +0.29, Rem +0.22, Wraith +0.20 | 1 heroes |
| Return Fire | 1,600 | +0.021 | +0.013 | +0.168 | Wraith +0.17, Venator +0.15, Rat King +0.13 | 0 heroes |
| Metal Skin | 3,200 | +0.035 | +0.011 | +0.264 | Wraith +0.70, Haze +0.43, Infernus +0.29 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Metal Skin +0.29 (+0.55), Dispel Magic +0.27 (+0.42), Healbane +0.07 (+0.17)
- **Seven**: Witchmail +0.05 (+0.36), Spirit Resilience +0.03 (+0.37), Counterspell +0.01 (+0.08)
- **Vindicta**: Divine Barrier +0.13 (+0.37), Return Fire +0.07 (+0.24), Plated Armor +0.06 (+0.38)
- **Lady Geist**: Return Fire +0.07 (+0.24), Healbane -0.03 (+0.07), Counterspell -0.07 (+0.01)
- **Abrams**: Unstoppable +0.13 (+0.34), Reactive Barrier +0.04 (+0.18), Dispel Magic +0.04 (+0.19)
- **Wraith**: Metal Skin +0.70 (+0.96), Indomitable +0.61 (+0.99), Plated Armor +0.51 (+0.83)
- **McGinnis**: Spirit Resilience +0.17 (+0.51), Witchmail +0.16 (+0.47), Healbane +0.09 (+0.19)
- **Paradox**: Spellbreaker -0.03 (+0.34), Return Fire -0.05 (+0.11), Counterspell -0.06 (+0.01)
- **Dynamo**: Witchmail +0.17 (+0.48), Indomitable +0.14 (+0.51), Spirit Resilience +0.10 (+0.44)
- **Kelvin**: Witchmail +0.02 (+0.33), Healbane +0.01 (+0.11), Counterspell -0.00 (+0.07)
- **Haze**: Plated Armor +0.76 (+1.08), Bullet Resilience +0.44 (+0.64), Metal Skin +0.43 (+0.69)
- **Holliday**: Plated Armor +0.69 (+1.02), Spellbreaker +0.42 (+0.80), Indomitable +0.41 (+0.78)
- **Bebop**: Healbane +0.04 (+0.15), Counterspell -0.02 (+0.06), Debuff Reducer -0.06 (+0.04)
- **Calico**: Spirit Resilience +0.25 (+0.59), Reactive Barrier +0.16 (+0.30), Divine Barrier +0.16 (+0.40)
- **Grey Talon**: Spellbreaker +0.48 (+0.85), Spirit Resilience +0.45 (+0.79), Indomitable +0.19 (+0.57)
- **Mo & Krill**: Spellbreaker +0.40 (+0.77), Spirit Resilience +0.26 (+0.60), Healbane +0.15 (+0.25)
- **Shiv**: Counterspell -0.02 (+0.06), Healbane -0.03 (+0.07), Return Fire -0.04 (+0.13)
- **Ivy**: Healbane +0.07 (+0.18), Metal Skin +0.03 (+0.30), Bullet Resilience +0.02 (+0.21)
- **Warden**: Dispel Magic +0.13 (+0.27), Bullet Resilience +0.06 (+0.25), Healbane +0.03 (+0.13)
- **Yamato**: Healbane -0.03 (+0.08), Counterspell -0.05 (+0.03), Debuff Reducer -0.08 (+0.02)
- **Lash**: Spellbreaker +0.27 (+0.64), Indomitable +0.22 (+0.59), Dispel Magic +0.14 (+0.29)
- **Viscous**: Spellbreaker +0.16 (+0.53), Healbane -0.01 (+0.10), Reactive Barrier -0.03 (+0.11)
- **Pocket**: Spirit Resilience +0.10 (+0.44), Spellbreaker +0.08 (+0.45), Witchmail +0.08 (+0.39)
- **Mirage**: Dispel Magic +0.30 (+0.44), Metal Skin +0.15 (+0.41), Spellbreaker +0.09 (+0.46)
- **Vyper**: Indomitable +0.53 (+0.90), Plated Armor +0.30 (+0.62), Metal Skin +0.25 (+0.51)
- **Sinclair**: Indomitable +0.24 (+0.62), Spirit Resilience +0.16 (+0.50), Spellbreaker +0.13 (+0.51)
- **Mina**: Spirit Resilience +0.64 (+0.98), Spellbreaker +0.44 (+0.81), Witchmail +0.34 (+0.65)
- **Drifter**: Dispel Magic +0.12 (+0.27), Return Fire +0.02 (+0.19), Counterspell -0.02 (+0.06)
- **Venator**: Return Fire +0.15 (+0.32), Reactive Barrier +0.06 (+0.20), Metal Skin +0.06 (+0.32)
- **Victor**: Healbane +0.10 (+0.20), Counterspell -0.03 (+0.05), Witchmail -0.08 (+0.23)
- **Paige**: Indomitable +0.43 (+0.80), Unstoppable +0.29 (+0.50), Spirit Resilience +0.25 (+0.59)
- **The Doorman**: Indomitable +0.42 (+0.80), Spirit Resilience +0.31 (+0.65), Witchmail +0.23 (+0.54)
- **Billy**: Healbane -0.00 (+0.10), Return Fire -0.04 (+0.13), Counterspell -0.04 (+0.03)
- **Graves**: Return Fire +0.06 (+0.23), Counterspell -0.04 (+0.04), Reactive Barrier -0.05 (+0.08)
- **Apollo**: Healbane -0.05 (+0.05), Counterspell -0.06 (+0.01), Dispel Magic -0.10 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.17 (+0.51), Healbane +0.12 (+0.22), Unstoppable +0.11 (+0.32)
- **Rem**: Unstoppable +0.22 (+0.42), Indomitable +0.20 (+0.58), Reactive Barrier +0.05 (+0.19)
- **Silver**: Dispel Magic +0.06 (+0.20), Debuff Reducer +0.03 (+0.13), Reactive Barrier +0.02 (+0.15)
- **Celeste**: Spirit Resilience +0.05 (+0.39), Dispel Magic -0.02 (+0.13), Witchmail -0.03 (+0.28)
- **Rat King**: Bullet Resilience +0.27 (+0.47), Plated Armor +0.26 (+0.59), Metal Skin +0.14 (+0.40)
- **Solomon**: Spirit Resilience +0.34 (+0.68), Spellbreaker +0.33 (+0.70), Divine Barrier +0.20 (+0.44)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.402 | +0.126 | +0.328 | Lash +0.51, Mina +0.44, Holliday +0.41 | 11 heroes |
| Reactive Barrier | 1,600 | +0.130 | +0.081 | +0.127 | Grey Talon +0.22, Holliday +0.19, Wraith +0.16 | 1 heroes |
| Indomitable | 6,400 | +0.357 | +0.056 | +0.349 | Holliday +0.66, Wraith +0.55, The Doorman +0.49 | 0 heroes |
| Debuff Reducer | 1,600 | +0.088 | +0.055 | +0.071 | Holliday +0.25, Lash +0.23, Sinclair +0.12 | 0 heroes |
| Witchmail | 6,400 | +0.346 | +0.054 | +0.303 | Wraith +0.33, Mina +0.26, Paige +0.22 | 1 heroes |
| Dispel Magic | 3,200 | +0.168 | +0.052 | +0.138 | Lash +0.31, Mina +0.29, Mo & Krill +0.20 | 9 heroes |
| Spellbreaker | 6,400 | +0.327 | +0.051 | +0.327 | Holliday +0.53, Lash +0.46, Mina +0.39 | 0 heroes |
| Healbane | 1,600 | +0.078 | +0.049 | +0.095 | Ivy +0.15, Haze +0.11, Bebop +0.09 | 13 heroes |
| Bullet Resilience | 3,200 | +0.155 | +0.048 | +0.174 | Haze +0.50, Holliday +0.18, Wraith +0.17 | 0 heroes |
| Divine Barrier | 6,400 | +0.207 | +0.032 | +0.190 | Grey Talon +0.24, Holliday +0.17, Mina +0.16 | 2 heroes |
| Plated Armor | 6,400 | +0.205 | +0.032 | +0.317 | Haze +0.83, Holliday +0.82, Wraith +0.36 | 0 heroes |
| Unstoppable | 6,400 | +0.100 | +0.016 | +0.195 | Rem +0.30, Haze +0.28, Holliday +0.24 | 3 heroes |
| Metal Skin | 3,200 | +0.041 | +0.013 | +0.271 | Wraith +0.67, Haze +0.57, Vyper +0.33 | 0 heroes |
| Counterspell | 3,200 | +0.036 | +0.011 | +0.052 | Holliday +0.13, The Doorman +0.07, Lash +0.07 | 1 heroes |
| Return Fire | 1,600 | +0.007 | +0.004 | +0.155 | Wraith +0.13, Graves +0.10, Venator +0.10 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.08 (+0.22), Healbane +0.06 (+0.16), Metal Skin +0.04 (+0.31)
- **Seven**: Unstoppable +0.16 (+0.35), Spirit Resilience +0.14 (+0.46), Witchmail +0.07 (+0.37)
- **Vindicta**: Dispel Magic +0.02 (+0.16), Plated Armor +0.01 (+0.33), Return Fire +0.00 (+0.16)
- **Lady Geist**: Return Fire +0.08 (+0.23), Counterspell -0.03 (+0.02), Healbane -0.06 (+0.04)
- **Abrams**: Reactive Barrier -0.01 (+0.12), Dispel Magic -0.01 (+0.13), Divine Barrier -0.04 (+0.15)
- **Wraith**: Metal Skin +0.67 (+0.94), Indomitable +0.55 (+0.90), Plated Armor +0.36 (+0.68)
- **McGinnis**: Healbane +0.05 (+0.15), Witchmail +0.03 (+0.33), Spirit Resilience +0.03 (+0.36)
- **Paradox**: Dispel Magic +0.09 (+0.23), Unstoppable +0.05 (+0.24), Indomitable +0.00 (+0.35)
- **Dynamo**: Healbane -0.00 (+0.09), Debuff Reducer -0.00 (+0.07), Counterspell -0.01 (+0.04)
- **Kelvin**: Healbane +0.05 (+0.14), Counterspell +0.02 (+0.07), Spirit Resilience -0.00 (+0.32)
- **Haze**: Plated Armor +0.83 (+1.14), Metal Skin +0.57 (+0.84), Bullet Resilience +0.50 (+0.68)
- **Holliday**: Plated Armor +0.82 (+1.14), Indomitable +0.66 (+1.01), Spellbreaker +0.53 (+0.85)
- **Bebop**: Healbane +0.09 (+0.19), Counterspell -0.03 (+0.02), Return Fire -0.05 (+0.11)
- **Calico**: Spirit Resilience +0.07 (+0.40), Reactive Barrier +0.04 (+0.17), Indomitable +0.01 (+0.36)
- **Grey Talon**: Spellbreaker +0.32 (+0.65), Divine Barrier +0.24 (+0.43), Reactive Barrier +0.22 (+0.35)
- **Mo & Krill**: Spirit Resilience +0.38 (+0.71), Spellbreaker +0.33 (+0.66), Dispel Magic +0.20 (+0.34)
- **Shiv**: Counterspell -0.04 (+0.01), Healbane -0.04 (+0.06), Return Fire -0.05 (+0.11)
- **Ivy**: Healbane +0.15 (+0.24), Metal Skin +0.11 (+0.38), Bullet Resilience +0.02 (+0.19)
- **Warden**: Healbane +0.03 (+0.13), Dispel Magic +0.03 (+0.17), Counterspell +0.01 (+0.06)
- **Yamato**: Healbane -0.03 (+0.07), Counterspell -0.03 (+0.02), Debuff Reducer -0.06 (+0.02)
- **Lash**: Spirit Resilience +0.51 (+0.84), Spellbreaker +0.46 (+0.78), Indomitable +0.45 (+0.80)
- **Viscous**: Reactive Barrier +0.13 (+0.25), Divine Barrier +0.08 (+0.27), Spellbreaker +0.07 (+0.40)
- **Pocket**: Spirit Resilience +0.03 (+0.36), Counterspell +0.01 (+0.06), Divine Barrier -0.01 (+0.18)
- **Mirage**: Dispel Magic +0.17 (+0.31), Counterspell +0.02 (+0.07), Metal Skin +0.01 (+0.28)
- **Vyper**: Indomitable +0.45 (+0.80), Metal Skin +0.33 (+0.60), Plated Armor +0.27 (+0.59)
- **Sinclair**: Indomitable +0.26 (+0.61), Spirit Resilience +0.14 (+0.47), Spellbreaker +0.14 (+0.46)
- **Mina**: Spirit Resilience +0.44 (+0.77), Spellbreaker +0.39 (+0.72), Dispel Magic +0.29 (+0.43)
- **Drifter**: Dispel Magic +0.07 (+0.21), Counterspell +0.02 (+0.07), Return Fire +0.01 (+0.17)
- **Venator**: Unstoppable +0.15 (+0.34), Return Fire +0.10 (+0.25), Reactive Barrier +0.03 (+0.15)
- **Victor**: Healbane +0.07 (+0.16), Dispel Magic -0.04 (+0.10), Counterspell -0.04 (+0.01)
- **Paige**: Spirit Resilience +0.27 (+0.60), Unstoppable +0.23 (+0.43), Witchmail +0.22 (+0.52)
- **The Doorman**: Indomitable +0.49 (+0.84), Spirit Resilience +0.26 (+0.59), Divine Barrier +0.12 (+0.31)
- **Billy**: Healbane -0.01 (+0.09), Counterspell -0.03 (+0.02), Debuff Reducer -0.05 (+0.02)
- **Graves**: Return Fire +0.10 (+0.26), Counterspell -0.03 (+0.02), Debuff Reducer -0.05 (+0.02)
- **Apollo**: Healbane -0.03 (+0.07), Counterspell -0.05 (+0.01), Debuff Reducer -0.07 (+0.00)
- **Deadman Danny**: Healbane -0.03 (+0.07), Counterspell -0.04 (+0.01), Debuff Reducer -0.04 (+0.03)
- **Rem**: Unstoppable +0.30 (+0.50), Debuff Reducer +0.06 (+0.13), Reactive Barrier +0.02 (+0.15)
- **Silver**: Dispel Magic +0.02 (+0.16), Debuff Reducer +0.01 (+0.08), Reactive Barrier +0.01 (+0.13)
- **Celeste**: Spirit Resilience +0.17 (+0.50), Healbane +0.01 (+0.11), Counterspell +0.00 (+0.06)
- **Rat King**: Plated Armor +0.21 (+0.53), Metal Skin +0.16 (+0.43), Bullet Resilience +0.16 (+0.33)
- **Solomon**: Spirit Resilience +0.37 (+0.70), Spellbreaker +0.34 (+0.67), Divine Barrier +0.15 (+0.34)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.359 | +0.112 | +0.279 | Rem +0.54, Solomon +0.52, Lash +0.45 | 13 heroes |
| Reactive Barrier | 1,600 | +0.113 | +0.070 | +0.111 | Solomon +0.24, Paige +0.20, Rem +0.17 | 0 heroes |
| Debuff Reducer | 1,600 | +0.099 | +0.062 | +0.081 | Lash +0.15, Wraith +0.11, Dynamo +0.11 | 0 heroes |
| Indomitable | 6,400 | +0.354 | +0.055 | +0.350 | The Doorman +0.77, Wraith +0.68, Vyper +0.44 | 1 heroes |
| Dispel Magic | 3,200 | +0.169 | +0.053 | +0.140 | Mirage +0.27, Mina +0.23, Lash +0.22 | 9 heroes |
| Spellbreaker | 6,400 | +0.327 | +0.051 | +0.327 | Lash +0.49, Solomon +0.45, Paige +0.41 | 0 heroes |
| Healbane | 1,600 | +0.080 | +0.050 | +0.095 | Bebop +0.17, McGinnis +0.10, Yamato +0.08 | 9 heroes |
| Witchmail | 6,400 | +0.305 | +0.048 | +0.266 | Rem +0.55, Paige +0.39, Solomon +0.32 | 3 heroes |
| Bullet Resilience | 3,200 | +0.132 | +0.041 | +0.151 | Haze +0.42, Rat King +0.17, Venator +0.07 | 0 heroes |
| Plated Armor | 6,400 | +0.191 | +0.030 | +0.307 | Haze +0.87, Wraith +0.33, Holliday +0.28 | 3 heroes |
| Divine Barrier | 6,400 | +0.160 | +0.025 | +0.146 | Solomon +0.27, Paige +0.20, Rem +0.17 | 3 heroes |
| Unstoppable | 6,400 | +0.151 | +0.024 | +0.251 | Rem +0.55, Paige +0.45, Haze +0.22 | 6 heroes |
| Metal Skin | 3,200 | +0.044 | +0.014 | +0.275 | Wraith +0.56, Haze +0.37, Rat King +0.22 | 0 heroes |
| Counterspell | 3,200 | +0.020 | +0.006 | +0.040 | Lash +0.07, Paige +0.06, Bebop +0.05 | 1 heroes |
| Return Fire | 1,600 | -0.021 | -0.013 | +0.126 | Graves +0.16, Rat King +0.12, Lash +0.09 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.20 (+0.45), Metal Skin +0.15 (+0.42), Dispel Magic +0.11 (+0.25)
- **Seven**: Spellbreaker +0.16 (+0.48), Spirit Resilience +0.01 (+0.29), Metal Skin +0.00 (+0.28)
- **Vindicta**: Bullet Resilience +0.07 (+0.22), Healbane +0.07 (+0.16), Plated Armor +0.05 (+0.36)
- **Lady Geist**: Return Fire +0.06 (+0.18), Healbane +0.01 (+0.10), Counterspell -0.02 (+0.02)
- **Abrams**: Unstoppable +0.03 (+0.28), Counterspell +0.00 (+0.04), Debuff Reducer -0.04 (+0.04)
- **Wraith**: Indomitable +0.68 (+1.03), Metal Skin +0.56 (+0.83), Spellbreaker +0.35 (+0.68)
- **McGinnis**: Spirit Resilience +0.24 (+0.52), Witchmail +0.20 (+0.46), Healbane +0.10 (+0.19)
- **Paradox**: Unstoppable +0.04 (+0.29), Return Fire +0.00 (+0.13), Dispel Magic -0.01 (+0.13)
- **Dynamo**: Debuff Reducer +0.11 (+0.19), Unstoppable +0.04 (+0.29), Dispel Magic +0.00 (+0.14)
- **Kelvin**: Healbane +0.05 (+0.14), Counterspell +0.03 (+0.07), Debuff Reducer -0.02 (+0.06)
- **Haze**: Plated Armor +0.87 (+1.18), Bullet Resilience +0.42 (+0.57), Metal Skin +0.37 (+0.65)
- **Holliday**: Plated Armor +0.28 (+0.59), Indomitable +0.20 (+0.55), Spellbreaker +0.16 (+0.48)
- **Bebop**: Healbane +0.17 (+0.27), Spirit Resilience +0.14 (+0.42), Witchmail +0.10 (+0.36)
- **Calico**: Counterspell -0.02 (+0.02), Reactive Barrier -0.03 (+0.08), Witchmail -0.03 (+0.23)
- **Grey Talon**: Spellbreaker +0.18 (+0.50), Witchmail +0.12 (+0.39), Spirit Resilience +0.11 (+0.39)
- **Mo & Krill**: Healbane +0.01 (+0.10), Dispel Magic -0.01 (+0.13), Counterspell -0.02 (+0.02)
- **Shiv**: Counterspell -0.01 (+0.03), Return Fire -0.05 (+0.08), Healbane -0.05 (+0.05)
- **Ivy**: Divine Barrier +0.07 (+0.22), Spirit Resilience +0.05 (+0.33), Reactive Barrier +0.04 (+0.15)
- **Warden**: Witchmail +0.15 (+0.42), Spirit Resilience +0.08 (+0.36), Bullet Resilience +0.06 (+0.21)
- **Yamato**: Healbane +0.08 (+0.17), Counterspell +0.01 (+0.05), Debuff Reducer -0.04 (+0.04)
- **Lash**: Spellbreaker +0.49 (+0.82), Spirit Resilience +0.45 (+0.73), Indomitable +0.40 (+0.75)
- **Viscous**: Spellbreaker +0.07 (+0.40), Healbane +0.04 (+0.13), Spirit Resilience +0.03 (+0.31)
- **Pocket**: Divine Barrier +0.04 (+0.19), Witchmail +0.02 (+0.29), Spirit Resilience +0.02 (+0.29)
- **Mirage**: Dispel Magic +0.27 (+0.41), Spellbreaker +0.07 (+0.40), Metal Skin +0.07 (+0.34)
- **Vyper**: Indomitable +0.44 (+0.79), Plated Armor +0.18 (+0.49), Metal Skin +0.16 (+0.43)
- **Sinclair**: Indomitable +0.23 (+0.58), Spellbreaker +0.13 (+0.46), Debuff Reducer +0.07 (+0.16)
- **Mina**: Spirit Resilience +0.29 (+0.57), Spellbreaker +0.25 (+0.58), Dispel Magic +0.23 (+0.38)
- **Drifter**: Dispel Magic +0.19 (+0.33), Spellbreaker +0.07 (+0.39), Return Fire +0.04 (+0.16)
- **Venator**: Metal Skin +0.22 (+0.49), Unstoppable +0.18 (+0.43), Bullet Resilience +0.07 (+0.23)
- **Victor**: Healbane +0.05 (+0.15), Counterspell -0.04 (-0.00), Debuff Reducer -0.06 (+0.02)
- **Paige**: Unstoppable +0.45 (+0.70), Spirit Resilience +0.43 (+0.71), Spellbreaker +0.41 (+0.74)
- **The Doorman**: Indomitable +0.77 (+1.12), Spirit Resilience +0.41 (+0.69), Witchmail +0.28 (+0.55)
- **Billy**: Counterspell +0.02 (+0.06), Divine Barrier -0.01 (+0.14), Healbane -0.02 (+0.07)
- **Graves**: Spirit Resilience +0.18 (+0.46), Return Fire +0.16 (+0.28), Witchmail +0.12 (+0.38)
- **Apollo**: Counterspell -0.04 (+0.00), Healbane -0.06 (+0.04), Debuff Reducer -0.07 (+0.01)
- **Deadman Danny**: Counterspell -0.07 (-0.03), Healbane -0.09 (+0.01), Return Fire -0.11 (+0.02)
- **Rem**: Witchmail +0.55 (+0.81), Unstoppable +0.55 (+0.80), Spirit Resilience +0.54 (+0.82)
- **Silver**: Dispel Magic +0.03 (+0.17), Debuff Reducer +0.01 (+0.10), Reactive Barrier -0.01 (+0.10)
- **Celeste**: Spirit Resilience +0.22 (+0.50), Witchmail +0.14 (+0.40), Healbane +0.07 (+0.16)
- **Rat King**: Metal Skin +0.22 (+0.49), Bullet Resilience +0.17 (+0.32), Return Fire +0.12 (+0.25)
- **Solomon**: Spirit Resilience +0.52 (+0.80), Spellbreaker +0.45 (+0.77), Witchmail +0.32 (+0.59)
