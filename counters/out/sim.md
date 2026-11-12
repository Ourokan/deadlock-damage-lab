# Counter items in the sim (phantom and up)

Built 2026-11-12T20:54:34Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.156 | +0.049 | +0.132 | Lash +0.22, The Doorman +0.19, Lady Geist +0.16 | 0 heroes |
| Divine Barrier | 6,400 | +0.245 | +0.039 | +0.125 | Lash +0.17, Viscous +0.15, The Doorman +0.13 | 0 heroes |
| Dispel Magic | 3,200 | +0.089 | +0.028 | +0.081 | Mirage +0.38, Lash +0.12, Silver +0.08 | 4 heroes |
| Indomitable | 6,400 | +0.162 | +0.026 | +0.131 | The Doorman +0.24, Abrams +0.20, Wraith +0.18 | 0 heroes |
| Reactive Barrier | 1,600 | +0.037 | +0.024 | +0.040 | Graves +0.12, Deadman Danny +0.10, Abrams +0.08 | 2 heroes |
| Healbane | 1,600 | +0.028 | +0.018 | +0.083 | Graves +0.09, Yamato +0.09, Lady Geist +0.06 | 22 heroes |
| Bullet Resilience | 3,200 | +0.051 | +0.016 | +0.100 | Venator +0.21, Lash +0.16, Paradox +0.13 | 0 heroes |
| Witchmail | 6,400 | +0.095 | +0.015 | +0.203 | Lash +0.20, The Doorman +0.17, Deadman Danny +0.16 | 0 heroes |
| Debuff Reducer | 1,600 | +0.022 | +0.014 | +0.079 | Holliday +0.12, Vyper +0.12, Venator +0.09 | 0 heroes |
| Spellbreaker | 6,400 | +0.084 | +0.013 | +0.179 | Lash +0.22, Lady Geist +0.20, Wraith +0.17 | 0 heroes |
| Plated Armor | 6,400 | +0.032 | +0.005 | +0.136 | Holliday +0.23, Wraith +0.16, Lash +0.13 | 0 heroes |
| Unstoppable | 6,400 | +0.018 | +0.003 | +0.136 | Deadman Danny +0.11, Holliday +0.11, Lash +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.009 | -0.003 | +0.072 | Lash +0.09, Graves +0.08, Viscous +0.06 | 0 heroes |
| Metal Skin | 3,200 | -0.069 | -0.021 | +0.116 | Wraith +0.25, Lash +0.20, Paradox +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.086 | -0.054 | +0.086 | Paradox +0.10, Holliday +0.06, Wraith +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.04 (+0.12), Spellbreaker +0.03 (+0.21), Unstoppable +0.03 (+0.16)
- **Seven**: Healbane -0.00 (+0.08), Reactive Barrier -0.02 (+0.02), Witchmail -0.02 (+0.18)
- **Vindicta**: Divine Barrier +0.00 (+0.13), Counterspell -0.01 (+0.07), Return Fire -0.01 (+0.08)
- **Lady Geist**: Spellbreaker +0.20 (+0.37), Spirit Resilience +0.16 (+0.29), Witchmail +0.09 (+0.29)
- **Abrams**: Indomitable +0.20 (+0.33), Divine Barrier +0.10 (+0.22), Witchmail +0.08 (+0.28)
- **Wraith**: Metal Skin +0.25 (+0.37), Indomitable +0.18 (+0.31), Spellbreaker +0.17 (+0.35)
- **McGinnis**: Healbane +0.03 (+0.11), Reactive Barrier +0.00 (+0.04), Spirit Resilience +0.00 (+0.13)
- **Paradox**: Metal Skin +0.16 (+0.27), Bullet Resilience +0.13 (+0.24), Indomitable +0.11 (+0.24)
- **Dynamo**: Healbane +0.00 (+0.08), Counterspell -0.02 (+0.05), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Witchmail +0.03 (+0.23), Healbane +0.02 (+0.10), Spirit Resilience +0.01 (+0.14)
- **Haze**: Indomitable +0.06 (+0.19), Plated Armor +0.04 (+0.18), Bullet Resilience +0.03 (+0.13)
- **Holliday**: Plated Armor +0.23 (+0.36), Spellbreaker +0.15 (+0.33), Debuff Reducer +0.12 (+0.20)
- **Bebop**: Healbane +0.03 (+0.12), Counterspell +0.01 (+0.08), Divine Barrier -0.01 (+0.12)
- **Calico**: Spellbreaker +0.08 (+0.26), Divine Barrier +0.07 (+0.19), Spirit Resilience +0.06 (+0.19)
- **Grey Talon**: Unstoppable +0.07 (+0.21), Reactive Barrier +0.04 (+0.08), Debuff Reducer +0.03 (+0.11)
- **Mo & Krill**: Spellbreaker +0.09 (+0.26), Witchmail +0.06 (+0.27), Unstoppable +0.06 (+0.19)
- **Shiv**: Healbane +0.01 (+0.10), Return Fire +0.01 (+0.10), Bullet Resilience -0.00 (+0.10)
- **Ivy**: Indomitable +0.09 (+0.22), Unstoppable +0.04 (+0.18), Bullet Resilience +0.01 (+0.11)
- **Warden**: Return Fire -0.00 (+0.08), Debuff Reducer -0.01 (+0.07), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.09 (+0.17), Witchmail +0.05 (+0.25), Return Fire +0.04 (+0.13)
- **Lash**: Spellbreaker +0.22 (+0.40), Spirit Resilience +0.22 (+0.35), Metal Skin +0.20 (+0.31)
- **Viscous**: Divine Barrier +0.15 (+0.27), Metal Skin +0.10 (+0.22), Spirit Resilience +0.09 (+0.22)
- **Pocket**: Return Fire +0.02 (+0.11), Counterspell +0.02 (+0.09), Witchmail +0.02 (+0.22)
- **Mirage**: Dispel Magic +0.38 (+0.46), Spellbreaker +0.14 (+0.32), Spirit Resilience +0.13 (+0.26)
- **Vyper**: Debuff Reducer +0.12 (+0.20), Unstoppable +0.10 (+0.24), Spellbreaker +0.09 (+0.27)
- **Sinclair**: Indomitable +0.11 (+0.24), Spellbreaker +0.08 (+0.26), Unstoppable +0.07 (+0.20)
- **Mina**: Return Fire +0.01 (+0.10), Counterspell -0.01 (+0.06), Reactive Barrier -0.02 (+0.02)
- **Drifter**: Reactive Barrier -0.01 (+0.03), Counterspell -0.01 (+0.06), Healbane -0.01 (+0.07)
- **Venator**: Bullet Resilience +0.21 (+0.31), Debuff Reducer +0.09 (+0.17), Unstoppable +0.07 (+0.20)
- **Victor**: Spirit Resilience +0.12 (+0.25), Spellbreaker +0.09 (+0.27), Healbane -0.01 (+0.08)
- **Paige**: Reactive Barrier -0.01 (+0.03), Counterspell -0.02 (+0.06), Healbane -0.02 (+0.06)
- **The Doorman**: Indomitable +0.24 (+0.37), Spirit Resilience +0.19 (+0.32), Spellbreaker +0.17 (+0.35)
- **Billy**: Spellbreaker +0.03 (+0.21), Spirit Resilience +0.02 (+0.15), Plated Armor -0.01 (+0.12)
- **Graves**: Reactive Barrier +0.12 (+0.16), Metal Skin +0.11 (+0.23), Witchmail +0.10 (+0.31)
- **Apollo**: Reactive Barrier -0.05 (-0.01), Counterspell -0.06 (+0.01), Healbane -0.06 (+0.02)
- **Deadman Danny**: Witchmail +0.16 (+0.36), Spellbreaker +0.15 (+0.32), Spirit Resilience +0.14 (+0.27)
- **Rem**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.05), Reactive Barrier -0.03 (+0.01)
- **Silver**: Dispel Magic +0.08 (+0.16), Reactive Barrier +0.05 (+0.09), Debuff Reducer +0.03 (+0.11)
- **Celeste**: Spirit Resilience +0.16 (+0.29), Witchmail +0.13 (+0.33), Spellbreaker +0.08 (+0.26)
- **Rat King**: Return Fire +0.01 (+0.10), Bullet Resilience +0.00 (+0.10), Divine Barrier -0.01 (+0.12)
- **Solomon**: Reactive Barrier -0.01 (+0.03), Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04)
- **Violet**: Unstoppable +0.06 (+0.19), Return Fire +0.05 (+0.13), Witchmail +0.02 (+0.22)
- **Nurse Harrow**: Healbane +0.05 (+0.13), Reactive Barrier -0.00 (+0.04), Counterspell -0.03 (+0.04)
- **Baba**: Reactive Barrier -0.01 (+0.03), Healbane -0.01 (+0.08), Counterspell -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.157 | +0.049 | +0.146 | Lash +0.45, Celeste +0.20, Pocket +0.17 | 9 heroes |
| Divine Barrier | 6,400 | +0.197 | +0.031 | +0.097 | Lash +0.27, Abrams +0.11, Paradox +0.10 | 1 heroes |
| Dispel Magic | 3,200 | +0.083 | +0.026 | +0.068 | Mirage +0.25, Lash +0.14, Holliday +0.14 | 10 heroes |
| Indomitable | 6,400 | +0.156 | +0.025 | +0.109 | Lash +0.20, Wraith +0.20, The Doorman +0.19 | 0 heroes |
| Spellbreaker | 6,400 | +0.129 | +0.020 | +0.173 | Lash +0.33, Holliday +0.23, Lady Geist +0.18 | 0 heroes |
| Witchmail | 6,400 | +0.110 | +0.017 | +0.182 | Lash +0.29, Celeste +0.18, Lady Geist +0.09 | 1 heroes |
| Reactive Barrier | 1,600 | +0.020 | +0.012 | +0.022 | Abrams +0.12, Holliday +0.08, Deadman Danny +0.06 | 4 heroes |
| Healbane | 1,600 | +0.018 | +0.011 | +0.062 | Yamato +0.10, Lady Geist +0.08, Infernus +0.07 | 23 heroes |
| Bullet Resilience | 3,200 | +0.027 | +0.009 | +0.072 | Venator +0.17, Paradox +0.14, Lash +0.11 | 1 heroes |
| Plated Armor | 6,400 | +0.039 | +0.006 | +0.098 | Paradox +0.12, Lash +0.10, Wraith +0.09 | 0 heroes |
| Debuff Reducer | 1,600 | +0.004 | +0.002 | +0.065 | Holliday +0.23, Rem +0.14, Vyper +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.003 | -0.000 | +0.116 | Holliday +0.21, Abrams +0.15, Rem +0.13 | 0 heroes |
| Counterspell | 3,200 | -0.023 | -0.007 | +0.043 | Lash +0.05, Abrams +0.05, Nurse Harrow +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.086 | -0.027 | +0.092 | Wraith +0.24, Lash +0.19, Paradox +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.096 | -0.060 | +0.060 | Paradox +0.07, The Doorman +0.05, Abrams +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.10 (+0.21), Spellbreaker +0.10 (+0.27), Dispel Magic +0.07 (+0.14)
- **Seven**: Witchmail +0.04 (+0.22), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Vindicta**: Divine Barrier +0.05 (+0.14), Return Fire +0.04 (+0.10), Witchmail +0.03 (+0.21)
- **Lady Geist**: Spellbreaker +0.18 (+0.35), Spirit Resilience +0.17 (+0.31), Witchmail +0.09 (+0.27)
- **Abrams**: Indomitable +0.15 (+0.26), Unstoppable +0.15 (+0.26), Reactive Barrier +0.12 (+0.14)
- **Wraith**: Metal Skin +0.24 (+0.33), Indomitable +0.20 (+0.31), Spellbreaker +0.14 (+0.31)
- **McGinnis**: Spirit Resilience +0.07 (+0.21), Witchmail +0.00 (+0.18), Counterspell +0.00 (+0.04)
- **Paradox**: Metal Skin +0.16 (+0.25), Bullet Resilience +0.14 (+0.21), Plated Armor +0.12 (+0.21)
- **Dynamo**: Healbane +0.02 (+0.09), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.00)
- **Kelvin**: Spirit Resilience +0.07 (+0.22), Witchmail +0.04 (+0.22), Spellbreaker +0.01 (+0.18)
- **Haze**: Indomitable +0.07 (+0.18), Plated Armor +0.05 (+0.15), Bullet Resilience +0.04 (+0.11)
- **Holliday**: Spellbreaker +0.23 (+0.40), Debuff Reducer +0.23 (+0.29), Unstoppable +0.21 (+0.33)
- **Bebop**: Healbane +0.01 (+0.07), Counterspell -0.00 (+0.04), Reactive Barrier -0.02 (+0.01)
- **Calico**: Divine Barrier +0.05 (+0.15), Spirit Resilience +0.02 (+0.17), Spellbreaker +0.01 (+0.19)
- **Grey Talon**: Unstoppable +0.10 (+0.21), Debuff Reducer +0.06 (+0.12), Spellbreaker +0.05 (+0.22)
- **Mo & Krill**: Spellbreaker +0.11 (+0.28), Unstoppable +0.09 (+0.21), Debuff Reducer +0.05 (+0.11)
- **Shiv**: Bullet Resilience +0.08 (+0.15), Plated Armor +0.04 (+0.14), Return Fire +0.04 (+0.10)
- **Ivy**: Unstoppable +0.03 (+0.14), Indomitable +0.02 (+0.13), Debuff Reducer +0.01 (+0.08)
- **Warden**: Return Fire +0.02 (+0.08), Divine Barrier +0.01 (+0.11), Debuff Reducer +0.01 (+0.07)
- **Yamato**: Healbane +0.10 (+0.17), Debuff Reducer +0.04 (+0.10), Counterspell +0.02 (+0.06)
- **Lash**: Spirit Resilience +0.45 (+0.59), Spellbreaker +0.33 (+0.51), Witchmail +0.29 (+0.47)
- **Viscous**: Divine Barrier +0.02 (+0.12), Counterspell +0.01 (+0.05), Debuff Reducer -0.00 (+0.06)
- **Pocket**: Spirit Resilience +0.17 (+0.32), Witchmail +0.07 (+0.26), Dispel Magic +0.04 (+0.11)
- **Mirage**: Dispel Magic +0.25 (+0.31), Spirit Resilience +0.03 (+0.18), Metal Skin +0.03 (+0.12)
- **Vyper**: Spellbreaker +0.11 (+0.28), Debuff Reducer +0.07 (+0.14), Unstoppable +0.05 (+0.17)
- **Sinclair**: Indomitable +0.14 (+0.25), Debuff Reducer +0.02 (+0.09), Spellbreaker +0.02 (+0.19)
- **Mina**: Return Fire +0.01 (+0.07), Counterspell -0.01 (+0.04), Reactive Barrier -0.02 (+0.01)
- **Drifter**: Return Fire +0.01 (+0.07), Counterspell -0.01 (+0.04), Healbane -0.01 (+0.05)
- **Venator**: Bullet Resilience +0.17 (+0.24), Unstoppable +0.04 (+0.16), Debuff Reducer +0.04 (+0.11)
- **Victor**: Spirit Resilience +0.11 (+0.25), Spellbreaker +0.08 (+0.25), Healbane +0.02 (+0.08)
- **Paige**: Counterspell -0.00 (+0.04), Reactive Barrier -0.02 (+0.01), Healbane -0.02 (+0.04)
- **The Doorman**: Indomitable +0.19 (+0.30), Spirit Resilience +0.12 (+0.26), Witchmail +0.09 (+0.27)
- **Billy**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.04), Reactive Barrier -0.02 (+0.01)
- **Graves**: Metal Skin +0.12 (+0.21), Spirit Resilience +0.09 (+0.23), Witchmail +0.09 (+0.27)
- **Apollo**: Healbane -0.01 (+0.05), Counterspell -0.02 (+0.02), Reactive Barrier -0.02 (+0.00)
- **Deadman Danny**: Spirit Resilience +0.07 (+0.22), Reactive Barrier +0.06 (+0.08), Witchmail +0.05 (+0.24)
- **Rem**: Debuff Reducer +0.14 (+0.20), Unstoppable +0.13 (+0.24), Spellbreaker +0.04 (+0.22)
- **Silver**: Dispel Magic +0.08 (+0.15), Reactive Barrier +0.02 (+0.04), Debuff Reducer -0.01 (+0.05)
- **Celeste**: Spirit Resilience +0.20 (+0.35), Witchmail +0.18 (+0.36), Metal Skin +0.10 (+0.19)
- **Rat King**: Return Fire +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Solomon**: Reactive Barrier -0.01 (+0.01), Return Fire -0.02 (+0.04), Counterspell -0.03 (+0.02)
- **Violet**: Witchmail +0.06 (+0.25), Unstoppable +0.06 (+0.18), Return Fire +0.04 (+0.10)
- **Nurse Harrow**: Healbane +0.06 (+0.12), Divine Barrier +0.06 (+0.16), Witchmail +0.05 (+0.23)
- **Baba**: Unstoppable +0.02 (+0.13), Debuff Reducer -0.00 (+0.06), Healbane -0.00 (+0.06)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.148 | +0.046 | +0.147 | Lash +0.36, Viscous +0.23, Deadman Danny +0.18 | 12 heroes |
| Divine Barrier | 6,400 | +0.183 | +0.029 | +0.098 | Lash +0.23, Viscous +0.16, Wraith +0.10 | 2 heroes |
| Dispel Magic | 3,200 | +0.082 | +0.026 | +0.056 | Mirage +0.22, Lash +0.22, Infernus +0.12 | 10 heroes |
| Indomitable | 6,400 | +0.158 | +0.025 | +0.115 | Wraith +0.26, Haze +0.22, Lash +0.18 | 0 heroes |
| Spellbreaker | 6,400 | +0.145 | +0.023 | +0.181 | Wraith +0.25, Lash +0.22, Viscous +0.17 | 0 heroes |
| Witchmail | 6,400 | +0.103 | +0.016 | +0.187 | Lash +0.27, Graves +0.14, Wraith +0.12 | 1 heroes |
| Healbane | 1,600 | +0.018 | +0.011 | +0.067 | Nurse Harrow +0.10, Lady Geist +0.08, Mo & Krill +0.07 | 25 heroes |
| Bullet Resilience | 3,200 | +0.029 | +0.009 | +0.072 | Lash +0.20, Venator +0.17, Haze +0.12 | 1 heroes |
| Plated Armor | 6,400 | +0.046 | +0.007 | +0.107 | Lash +0.19, Holliday +0.18, Haze +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.006 | +0.004 | +0.068 | Holliday +0.13, Grey Talon +0.13, Rem +0.13 | 0 heroes |
| Unstoppable | 6,400 | +0.002 | +0.000 | +0.124 | Mo & Krill +0.26, Haze +0.19, Grey Talon +0.13 | 4 heroes |
| Reactive Barrier | 1,600 | -0.008 | -0.005 | +0.015 | Deadman Danny +0.09, Grey Talon +0.06, Silver +0.05 | 2 heroes |
| Counterspell | 3,200 | -0.028 | -0.009 | +0.035 | Lash +0.06, Paradox +0.02, Kelvin +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.078 | -0.024 | +0.105 | Wraith +0.29, Lash +0.22, Haze +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.087 | -0.055 | +0.059 | Wraith +0.10, Haze +0.07, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.17), Spellbreaker +0.07 (+0.25), Unstoppable +0.05 (+0.18)
- **Seven**: Witchmail +0.08 (+0.26), Spirit Resilience +0.06 (+0.21), Reactive Barrier +0.01 (+0.03)
- **Vindicta**: Bullet Resilience +0.10 (+0.17), Plated Armor +0.06 (+0.17), Return Fire +0.06 (+0.12)
- **Lady Geist**: Healbane +0.08 (+0.15), Spellbreaker +0.05 (+0.23), Spirit Resilience +0.05 (+0.20)
- **Abrams**: Dispel Magic +0.04 (+0.10), Unstoppable +0.03 (+0.16), Spirit Resilience +0.02 (+0.16)
- **Wraith**: Metal Skin +0.29 (+0.39), Indomitable +0.26 (+0.37), Spellbreaker +0.25 (+0.43)
- **McGinnis**: Spirit Resilience +0.05 (+0.20), Witchmail +0.00 (+0.19), Healbane -0.00 (+0.07)
- **Paradox**: Dispel Magic +0.07 (+0.12), Return Fire +0.06 (+0.12), Indomitable +0.06 (+0.17)
- **Dynamo**: Healbane -0.00 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.00)
- **Kelvin**: Spirit Resilience +0.05 (+0.20), Counterspell +0.02 (+0.06), Healbane -0.00 (+0.06)
- **Haze**: Indomitable +0.22 (+0.34), Unstoppable +0.19 (+0.32), Plated Armor +0.14 (+0.25)
- **Holliday**: Plated Armor +0.18 (+0.29), Spellbreaker +0.14 (+0.32), Debuff Reducer +0.13 (+0.20)
- **Bebop**: Healbane +0.04 (+0.11), Divine Barrier +0.01 (+0.11), Counterspell +0.01 (+0.04)
- **Calico**: Spirit Resilience +0.12 (+0.27), Divine Barrier +0.04 (+0.14), Dispel Magic +0.03 (+0.09)
- **Grey Talon**: Unstoppable +0.13 (+0.26), Debuff Reducer +0.13 (+0.19), Spellbreaker +0.10 (+0.28)
- **Mo & Krill**: Unstoppable +0.26 (+0.38), Spellbreaker +0.15 (+0.33), Debuff Reducer +0.11 (+0.17)
- **Shiv**: Bullet Resilience +0.03 (+0.10), Divine Barrier +0.01 (+0.10), Return Fire +0.01 (+0.07)
- **Ivy**: Indomitable +0.04 (+0.15), Unstoppable +0.02 (+0.14), Metal Skin +0.01 (+0.12)
- **Warden**: Debuff Reducer +0.02 (+0.08), Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Yamato**: Healbane +0.06 (+0.13), Witchmail +0.05 (+0.23), Spirit Resilience +0.03 (+0.17)
- **Lash**: Spirit Resilience +0.36 (+0.51), Witchmail +0.27 (+0.46), Divine Barrier +0.23 (+0.33)
- **Viscous**: Spirit Resilience +0.23 (+0.38), Spellbreaker +0.17 (+0.35), Divine Barrier +0.16 (+0.25)
- **Pocket**: Spirit Resilience +0.04 (+0.18), Witchmail +0.00 (+0.19), Return Fire -0.01 (+0.05)
- **Mirage**: Dispel Magic +0.22 (+0.27), Debuff Reducer +0.02 (+0.09), Spellbreaker +0.00 (+0.18)
- **Vyper**: Spellbreaker +0.08 (+0.26), Debuff Reducer +0.05 (+0.11), Reactive Barrier +0.04 (+0.06)
- **Sinclair**: Indomitable +0.13 (+0.25), Unstoppable +0.10 (+0.22), Debuff Reducer +0.06 (+0.13)
- **Mina**: Divine Barrier +0.06 (+0.16), Spirit Resilience +0.06 (+0.20), Witchmail +0.05 (+0.24)
- **Drifter**: Healbane -0.00 (+0.06), Reactive Barrier -0.00 (+0.01), Return Fire -0.01 (+0.05)
- **Venator**: Bullet Resilience +0.17 (+0.24), Plated Armor +0.05 (+0.15), Debuff Reducer +0.03 (+0.10)
- **Victor**: Healbane +0.04 (+0.11), Spirit Resilience +0.04 (+0.19), Spellbreaker +0.04 (+0.22)
- **Paige**: Counterspell +0.00 (+0.04), Reactive Barrier -0.01 (+0.01), Divine Barrier -0.02 (+0.08)
- **The Doorman**: Indomitable +0.15 (+0.27), Spirit Resilience +0.11 (+0.26), Witchmail +0.08 (+0.26)
- **Billy**: Reactive Barrier +0.04 (+0.06), Debuff Reducer +0.02 (+0.09), Counterspell +0.02 (+0.05)
- **Graves**: Spirit Resilience +0.16 (+0.30), Witchmail +0.14 (+0.32), Metal Skin +0.11 (+0.21)
- **Apollo**: Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.00), Healbane -0.02 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.18 (+0.33), Spellbreaker +0.13 (+0.31), Witchmail +0.11 (+0.30)
- **Rem**: Debuff Reducer +0.13 (+0.19), Unstoppable +0.11 (+0.23), Spellbreaker +0.06 (+0.24)
- **Silver**: Dispel Magic +0.07 (+0.12), Reactive Barrier +0.05 (+0.06), Bullet Resilience +0.03 (+0.10)
- **Celeste**: Spirit Resilience +0.09 (+0.24), Witchmail +0.07 (+0.25), Healbane +0.05 (+0.12)
- **Rat King**: Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.01 (+0.00)
- **Solomon**: Reactive Barrier +0.03 (+0.05), Debuff Reducer -0.01 (+0.06), Counterspell -0.01 (+0.02)
- **Violet**: Witchmail +0.11 (+0.30), Divine Barrier +0.06 (+0.16), Unstoppable +0.03 (+0.15)
- **Nurse Harrow**: Healbane +0.10 (+0.17), Spirit Resilience +0.03 (+0.17), Counterspell +0.02 (+0.06)
- **Baba**: Reactive Barrier -0.01 (+0.01), Healbane -0.01 (+0.06), Counterspell -0.02 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.140 | +0.044 | +0.146 | Lash +0.49, Viscous +0.40, The Doorman +0.35 | 16 heroes |
| Indomitable | 6,400 | +0.172 | +0.027 | +0.129 | Wraith +0.40, The Doorman +0.27, Mo & Krill +0.18 | 3 heroes |
| Dispel Magic | 3,200 | +0.085 | +0.026 | +0.053 | Mirage +0.19, Lash +0.13, Infernus +0.11 | 11 heroes |
| Spellbreaker | 6,400 | +0.169 | +0.026 | +0.206 | Lash +0.31, Deadman Danny +0.26, Viscous +0.25 | 0 heroes |
| Divine Barrier | 6,400 | +0.151 | +0.024 | +0.082 | Viscous +0.23, Lash +0.22, The Doorman +0.11 | 2 heroes |
| Witchmail | 6,400 | +0.100 | +0.016 | +0.172 | Lash +0.31, The Doorman +0.25, Viscous +0.20 | 1 heroes |
| Debuff Reducer | 1,600 | +0.014 | +0.009 | +0.099 | Paige +0.21, Grey Talon +0.17, Bebop +0.17 | 0 heroes |
| Healbane | 1,600 | +0.013 | +0.008 | +0.060 | Mo & Krill +0.08, Victor +0.07, Infernus +0.06 | 21 heroes |
| Bullet Resilience | 3,200 | +0.024 | +0.007 | +0.064 | Vindicta +0.16, Haze +0.12, Lash +0.12 | 1 heroes |
| Plated Armor | 6,400 | +0.042 | +0.007 | +0.108 | Haze +0.15, Vindicta +0.12, Lash +0.10 | 3 heroes |
| Unstoppable | 6,400 | +0.019 | +0.003 | +0.164 | Paige +0.40, Infernus +0.19, Haze +0.18 | 5 heroes |
| Counterspell | 3,200 | -0.032 | -0.010 | +0.032 | Lash +0.12, Viscous +0.08, Mo & Krill +0.04 | 1 heroes |
| Reactive Barrier | 1,600 | -0.016 | -0.010 | +0.016 | Deadman Danny +0.10, Lash +0.06, Holliday +0.04 | 2 heroes |
| Metal Skin | 3,200 | -0.084 | -0.026 | +0.092 | Lash +0.27, Wraith +0.15, Silver +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.080 | -0.050 | +0.058 | Lash +0.12, Vindicta +0.10, Viscous +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.19 (+0.35), Spellbreaker +0.14 (+0.35), Dispel Magic +0.11 (+0.16)
- **Seven**: Witchmail +0.08 (+0.25), Counterspell +0.01 (+0.04), Healbane +0.01 (+0.07)
- **Vindicta**: Bullet Resilience +0.16 (+0.22), Plated Armor +0.12 (+0.23), Return Fire +0.10 (+0.16)
- **Lady Geist**: Healbane +0.05 (+0.11), Spirit Resilience +0.03 (+0.17), Spellbreaker +0.00 (+0.21)
- **Abrams**: Dispel Magic +0.03 (+0.08), Unstoppable +0.03 (+0.19), Reactive Barrier +0.02 (+0.03)
- **Wraith**: Indomitable +0.40 (+0.53), Spellbreaker +0.18 (+0.39), Metal Skin +0.15 (+0.24)
- **McGinnis**: Dispel Magic +0.02 (+0.07), Spirit Resilience +0.01 (+0.16), Witchmail -0.00 (+0.17)
- **Paradox**: Unstoppable +0.18 (+0.34), Indomitable +0.15 (+0.28), Witchmail +0.11 (+0.28)
- **Dynamo**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (+0.00)
- **Kelvin**: Spirit Resilience +0.04 (+0.19), Healbane +0.00 (+0.06), Reactive Barrier -0.01 (+0.00)
- **Haze**: Unstoppable +0.18 (+0.35), Plated Armor +0.15 (+0.26), Bullet Resilience +0.12 (+0.18)
- **Holliday**: Debuff Reducer +0.16 (+0.26), Spellbreaker +0.16 (+0.36), Unstoppable +0.11 (+0.27)
- **Bebop**: Debuff Reducer +0.17 (+0.27), Unstoppable +0.12 (+0.28), Spellbreaker +0.08 (+0.29)
- **Calico**: Spirit Resilience +0.02 (+0.16), Divine Barrier -0.01 (+0.07), Counterspell -0.02 (+0.01)
- **Grey Talon**: Spirit Resilience +0.22 (+0.37), Spellbreaker +0.22 (+0.43), Debuff Reducer +0.17 (+0.27)
- **Mo & Krill**: Spellbreaker +0.18 (+0.39), Spirit Resilience +0.18 (+0.33), Indomitable +0.18 (+0.31)
- **Shiv**: Bullet Resilience +0.08 (+0.15), Return Fire +0.04 (+0.10), Plated Armor +0.04 (+0.14)
- **Ivy**: Unstoppable +0.04 (+0.20), Plated Armor +0.02 (+0.12), Metal Skin +0.01 (+0.11)
- **Warden**: Plated Armor +0.10 (+0.21), Debuff Reducer +0.05 (+0.15), Spellbreaker +0.05 (+0.25)
- **Yamato**: Healbane +0.03 (+0.09), Counterspell -0.00 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Lash**: Spirit Resilience +0.49 (+0.64), Witchmail +0.31 (+0.49), Spellbreaker +0.31 (+0.51)
- **Viscous**: Spirit Resilience +0.40 (+0.54), Spellbreaker +0.25 (+0.46), Divine Barrier +0.23 (+0.31)
- **Pocket**: Spirit Resilience +0.01 (+0.15), Reactive Barrier -0.01 (+0.01), Return Fire -0.01 (+0.04)
- **Mirage**: Dispel Magic +0.19 (+0.24), Spellbreaker +0.04 (+0.25), Reactive Barrier -0.01 (+0.00)
- **Vyper**: Debuff Reducer +0.12 (+0.22), Unstoppable +0.08 (+0.25), Spellbreaker +0.04 (+0.24)
- **Sinclair**: Indomitable +0.17 (+0.30), Spellbreaker +0.03 (+0.23), Debuff Reducer +0.03 (+0.12)
- **Mina**: Divine Barrier +0.03 (+0.12), Spirit Resilience +0.02 (+0.17), Witchmail +0.01 (+0.18)
- **Drifter**: Dispel Magic +0.08 (+0.14), Reactive Barrier +0.03 (+0.04), Return Fire +0.00 (+0.06)
- **Venator**: Bullet Resilience +0.08 (+0.15), Metal Skin +0.06 (+0.15), Plated Armor +0.01 (+0.12)
- **Victor**: Spellbreaker +0.08 (+0.29), Healbane +0.07 (+0.13), Spirit Resilience +0.05 (+0.20)
- **Paige**: Unstoppable +0.40 (+0.56), Debuff Reducer +0.21 (+0.31), Spellbreaker +0.11 (+0.31)
- **The Doorman**: Spirit Resilience +0.35 (+0.49), Indomitable +0.27 (+0.40), Witchmail +0.25 (+0.42)
- **Billy**: Reactive Barrier +0.01 (+0.03), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05)
- **Graves**: Return Fire +0.01 (+0.07), Witchmail +0.01 (+0.18), Reactive Barrier +0.01 (+0.03)
- **Apollo**: Counterspell +0.01 (+0.04), Healbane -0.01 (+0.05), Reactive Barrier -0.01 (+0.00)
- **Deadman Danny**: Spellbreaker +0.26 (+0.47), Spirit Resilience +0.26 (+0.40), Reactive Barrier +0.10 (+0.11)
- **Rem**: Spirit Resilience +0.10 (+0.25), Divine Barrier +0.09 (+0.18), Witchmail +0.04 (+0.22)
- **Silver**: Metal Skin +0.10 (+0.20), Dispel Magic +0.10 (+0.16), Bullet Resilience +0.03 (+0.10)
- **Celeste**: Witchmail +0.12 (+0.29), Spirit Resilience +0.08 (+0.22), Plated Armor +0.03 (+0.14)
- **Rat King**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (+0.00)
- **Solomon**: Reactive Barrier +0.02 (+0.04), Counterspell +0.01 (+0.04), Return Fire +0.01 (+0.06)
- **Violet**: Witchmail +0.08 (+0.25), Divine Barrier +0.04 (+0.13), Dispel Magic +0.04 (+0.10)
- **Nurse Harrow**: Spirit Resilience +0.19 (+0.34), Healbane +0.04 (+0.10), Witchmail +0.03 (+0.21)
- **Baba**: Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04), Reactive Barrier +0.00 (+0.02)
