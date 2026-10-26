# Counter items in the sim (phantom and up)

Built 2026-10-26T00:03:01Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.247 | +0.077 | +0.137 | Deadman Danny +0.26, Lash +0.23, Wraith +0.16 | 1 heroes |
| Divine Barrier | 6,400 | +0.365 | +0.059 | +0.100 | Wraith +0.19, Lash +0.17, Mina +0.12 | 0 heroes |
| Dispel Magic | 3,200 | +0.143 | +0.045 | +0.081 | Mirage +0.34, Infernus +0.10, Lash +0.08 | 4 heroes |
| Debuff Reducer | 1,600 | +0.064 | +0.040 | +0.057 | Wraith +0.12, Vyper +0.06, Billy +0.05 | 0 heroes |
| Witchmail | 6,400 | +0.231 | +0.036 | +0.198 | Deadman Danny +0.26, Wraith +0.16, Lash +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | +0.056 | +0.035 | +0.053 | Wraith +0.16, Deadman Danny +0.09, Violet +0.07 | 2 heroes |
| Indomitable | 6,400 | +0.206 | +0.033 | +0.155 | Vyper +0.32, The Doorman +0.31, Wraith +0.30 | 0 heroes |
| Healbane | 1,600 | +0.042 | +0.026 | +0.086 | Billy +0.06, Nurse Harrow +0.05, Infernus +0.05 | 11 heroes |
| Spellbreaker | 6,400 | +0.163 | +0.025 | +0.160 | Deadman Danny +0.28, Lash +0.22, Wraith +0.19 | 0 heroes |
| Bullet Resilience | 3,200 | +0.049 | +0.015 | +0.096 | Wraith +0.13, Deadman Danny +0.11, Paradox +0.10 | 0 heroes |
| Counterspell | 3,200 | +0.019 | +0.006 | +0.071 | Wraith +0.07, Billy +0.06, Deadman Danny +0.05 | 1 heroes |
| Plated Armor | 6,400 | +0.033 | +0.005 | +0.136 | Holliday +0.25, Wraith +0.19, Deadman Danny +0.14 | 0 heroes |
| Unstoppable | 6,400 | +0.010 | +0.002 | +0.124 | Wraith +0.14, Deadman Danny +0.11, Ivy +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.087 | -0.027 | +0.116 | Wraith +0.26, Drifter +0.13, Lash +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.134 | -0.084 | +0.068 | Wraith +0.08, Holliday +0.06, Deadman Danny +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.18), Unstoppable +0.07 (+0.19), Spirit Resilience +0.05 (+0.19)
- **Seven**: Healbane -0.01 (+0.07), Counterspell -0.02 (+0.05), Witchmail -0.03 (+0.17)
- **Vindicta**: Divine Barrier +0.05 (+0.15), Return Fire +0.05 (+0.12), Counterspell +0.04 (+0.11)
- **Lady Geist**: Return Fire +0.04 (+0.11), Divine Barrier +0.02 (+0.12), Dispel Magic +0.02 (+0.10)
- **Abrams**: Indomitable +0.15 (+0.31), Unstoppable +0.06 (+0.18), Divine Barrier +0.03 (+0.13)
- **Wraith**: Indomitable +0.30 (+0.45), Metal Skin +0.26 (+0.38), Divine Barrier +0.19 (+0.29)
- **McGinnis**: Spirit Resilience +0.04 (+0.18), Return Fire -0.01 (+0.05), Healbane -0.01 (+0.07)
- **Paradox**: Metal Skin +0.12 (+0.23), Bullet Resilience +0.10 (+0.19), Plated Armor +0.09 (+0.22)
- **Dynamo**: Healbane +0.01 (+0.10), Counterspell -0.02 (+0.05), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane -0.00 (+0.08), Counterspell -0.01 (+0.06), Debuff Reducer -0.02 (+0.04)
- **Haze**: Plated Armor +0.11 (+0.25), Indomitable +0.08 (+0.24), Bullet Resilience +0.07 (+0.16)
- **Holliday**: Plated Armor +0.25 (+0.38), Return Fire +0.06 (+0.12), Debuff Reducer +0.05 (+0.11)
- **Bebop**: Divine Barrier +0.05 (+0.15), Witchmail +0.05 (+0.24), Counterspell +0.04 (+0.12)
- **Calico**: Divine Barrier +0.02 (+0.12), Spellbreaker +0.02 (+0.18), Debuff Reducer +0.01 (+0.07)
- **Grey Talon**: Indomitable +0.08 (+0.23), Reactive Barrier +0.07 (+0.12), Debuff Reducer +0.05 (+0.11)
- **Mo & Krill**: Spellbreaker +0.10 (+0.26), Spirit Resilience +0.06 (+0.19), Dispel Magic +0.05 (+0.13)
- **Shiv**: Healbane -0.02 (+0.07), Return Fire -0.02 (+0.05), Divine Barrier -0.04 (+0.06)
- **Ivy**: Unstoppable +0.10 (+0.23), Indomitable +0.06 (+0.21), Debuff Reducer +0.01 (+0.07)
- **Warden**: Return Fire +0.04 (+0.11), Divine Barrier +0.01 (+0.11), Counterspell +0.01 (+0.09)
- **Yamato**: Healbane +0.02 (+0.11), Debuff Reducer -0.04 (+0.02), Counterspell -0.04 (+0.03)
- **Lash**: Spirit Resilience +0.23 (+0.37), Spellbreaker +0.22 (+0.38), Divine Barrier +0.17 (+0.27)
- **Viscous**: Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.07), Healbane -0.01 (+0.08)
- **Pocket**: Return Fire +0.04 (+0.10), Witchmail +0.03 (+0.23), Spirit Resilience +0.02 (+0.16)
- **Mirage**: Dispel Magic +0.34 (+0.42), Spellbreaker +0.07 (+0.23), Healbane -0.01 (+0.07)
- **Vyper**: Indomitable +0.32 (+0.47), Spellbreaker +0.09 (+0.25), Debuff Reducer +0.06 (+0.12)
- **Sinclair**: Indomitable +0.04 (+0.19), Spellbreaker +0.04 (+0.20), Return Fire +0.03 (+0.10)
- **Mina**: Divine Barrier +0.12 (+0.22), Spirit Resilience +0.10 (+0.23), Spellbreaker +0.09 (+0.25)
- **Drifter**: Metal Skin +0.13 (+0.24), Spirit Resilience +0.11 (+0.25), Witchmail +0.09 (+0.29)
- **Venator**: Bullet Resilience +0.10 (+0.19), Metal Skin +0.04 (+0.16), Plated Armor +0.03 (+0.17)
- **Victor**: Healbane +0.01 (+0.09), Reactive Barrier -0.04 (+0.02), Debuff Reducer -0.04 (+0.02)
- **Paige**: Healbane +0.00 (+0.09), Return Fire -0.01 (+0.06), Counterspell -0.01 (+0.06)
- **The Doorman**: Indomitable +0.31 (+0.46), Reactive Barrier -0.01 (+0.04), Counterspell -0.02 (+0.05)
- **Billy**: Healbane +0.06 (+0.15), Counterspell +0.06 (+0.13), Debuff Reducer +0.05 (+0.11)
- **Graves**: Metal Skin +0.10 (+0.22), Spirit Resilience +0.09 (+0.23), Divine Barrier +0.09 (+0.19)
- **Apollo**: Healbane +0.04 (+0.13), Debuff Reducer +0.02 (+0.07), Counterspell +0.01 (+0.08)
- **Deadman Danny**: Spellbreaker +0.28 (+0.44), Witchmail +0.26 (+0.46), Spirit Resilience +0.26 (+0.40)
- **Rem**: Unstoppable +0.10 (+0.22), Indomitable +0.08 (+0.23), Healbane -0.02 (+0.07)
- **Silver**: Dispel Magic +0.07 (+0.15), Metal Skin -0.00 (+0.11), Reactive Barrier -0.01 (+0.04)
- **Celeste**: Spirit Resilience +0.09 (+0.23), Witchmail +0.06 (+0.26), Dispel Magic +0.03 (+0.12)
- **Rat King**: Return Fire +0.01 (+0.08), Counterspell +0.01 (+0.08), Bullet Resilience -0.01 (+0.09)
- **Solomon**: Return Fire +0.00 (+0.07), Counterspell -0.01 (+0.06), Healbane -0.02 (+0.06)
- **Violet**: Unstoppable +0.08 (+0.21), Reactive Barrier +0.07 (+0.13), Spirit Resilience +0.05 (+0.19)
- **Nurse Harrow**: Healbane +0.05 (+0.13), Counterspell -0.01 (+0.06), Dispel Magic -0.02 (+0.06)
- **Baba**: Healbane +0.01 (+0.10), Counterspell -0.02 (+0.05), Unstoppable -0.02 (+0.11)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.224 | +0.070 | +0.122 | Lash +0.24, Deadman Danny +0.21, Pocket +0.20 | 10 heroes |
| Divine Barrier | 6,400 | +0.244 | +0.039 | +0.077 | Vindicta +0.27, Lash +0.16, Wraith +0.11 | 1 heroes |
| Dispel Magic | 3,200 | +0.122 | +0.038 | +0.062 | Mirage +0.30, Lash +0.12, Paradox +0.10 | 7 heroes |
| Witchmail | 6,400 | +0.211 | +0.033 | +0.162 | Graves +0.16, Lash +0.16, Pocket +0.11 | 0 heroes |
| Indomitable | 6,400 | +0.174 | +0.028 | +0.128 | Vyper +0.42, The Doorman +0.33, Wraith +0.20 | 0 heroes |
| Spellbreaker | 6,400 | +0.152 | +0.024 | +0.126 | Lash +0.20, Deadman Danny +0.17, Pocket +0.12 | 0 heroes |
| Reactive Barrier | 1,600 | +0.038 | +0.024 | +0.043 | Wraith +0.11, Vyper +0.07, Paradox +0.07 | 4 heroes |
| Debuff Reducer | 1,600 | +0.038 | +0.024 | +0.044 | Wraith +0.09, Pocket +0.05, Lash +0.05 | 1 heroes |
| Healbane | 1,600 | +0.015 | +0.010 | +0.077 | Lash +0.10, Haze +0.07, Pocket +0.04 | 17 heroes |
| Bullet Resilience | 3,200 | +0.024 | +0.007 | +0.076 | Vindicta +0.26, Paradox +0.14, Haze +0.10 | 0 heroes |
| Plated Armor | 6,400 | +0.028 | +0.004 | +0.114 | Vindicta +0.23, Holliday +0.17, Haze +0.15 | 0 heroes |
| Counterspell | 3,200 | -0.008 | -0.003 | +0.043 | Lash +0.07, Vyper +0.05, Pocket +0.05 | 1 heroes |
| Unstoppable | 6,400 | -0.020 | -0.003 | +0.100 | Abrams +0.17, Ivy +0.14, Rem +0.14 | 0 heroes |
| Metal Skin | 3,200 | -0.107 | -0.034 | +0.097 | Wraith +0.20, Paradox +0.18, Lash +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.145 | -0.090 | +0.057 | Vindicta +0.07, Wraith +0.07, Pocket +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.08 (+0.14), Unstoppable +0.04 (+0.14), Healbane +0.03 (+0.10)
- **Seven**: Witchmail +0.04 (+0.20), Counterspell +0.01 (+0.05), Healbane +0.00 (+0.08)
- **Vindicta**: Divine Barrier +0.27 (+0.34), Bullet Resilience +0.26 (+0.33), Plated Armor +0.23 (+0.35)
- **Lady Geist**: Return Fire +0.06 (+0.11), Divine Barrier +0.05 (+0.12), Metal Skin +0.02 (+0.12)
- **Abrams**: Unstoppable +0.17 (+0.27), Indomitable +0.05 (+0.18), Dispel Magic +0.04 (+0.11)
- **Wraith**: Metal Skin +0.20 (+0.30), Indomitable +0.20 (+0.33), Reactive Barrier +0.11 (+0.15)
- **McGinnis**: Healbane +0.00 (+0.08), Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.04)
- **Paradox**: Metal Skin +0.18 (+0.28), Bullet Resilience +0.14 (+0.21), Plated Armor +0.14 (+0.25)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.01 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.01 (+0.13), Dispel Magic +0.00 (+0.06), Healbane -0.01 (+0.07)
- **Haze**: Plated Armor +0.15 (+0.27), Indomitable +0.10 (+0.23), Bullet Resilience +0.10 (+0.18)
- **Holliday**: Plated Armor +0.17 (+0.28), Indomitable +0.05 (+0.18), Return Fire +0.03 (+0.09)
- **Bebop**: Witchmail +0.07 (+0.23), Counterspell +0.05 (+0.09), Divine Barrier +0.04 (+0.12)
- **Calico**: Reactive Barrier +0.03 (+0.07), Divine Barrier -0.00 (+0.07), Counterspell -0.01 (+0.03)
- **Grey Talon**: Reactive Barrier +0.03 (+0.07), Indomitable +0.03 (+0.16), Debuff Reducer +0.03 (+0.07)
- **Mo & Krill**: Unstoppable +0.09 (+0.19), Spellbreaker +0.05 (+0.18), Dispel Magic +0.03 (+0.09)
- **Shiv**: Divine Barrier +0.01 (+0.09), Bullet Resilience +0.01 (+0.09), Plated Armor +0.01 (+0.12)
- **Ivy**: Unstoppable +0.14 (+0.24), Indomitable +0.04 (+0.17), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.08), Counterspell +0.00 (+0.04), Debuff Reducer -0.02 (+0.03)
- **Yamato**: Healbane +0.03 (+0.11), Debuff Reducer -0.02 (+0.02), Reactive Barrier -0.04 (+0.00)
- **Lash**: Spirit Resilience +0.24 (+0.36), Spellbreaker +0.20 (+0.33), Divine Barrier +0.16 (+0.23)
- **Viscous**: Return Fire -0.01 (+0.04), Counterspell -0.02 (+0.02), Healbane -0.02 (+0.05)
- **Pocket**: Spirit Resilience +0.20 (+0.32), Spellbreaker +0.12 (+0.24), Witchmail +0.11 (+0.27)
- **Mirage**: Dispel Magic +0.30 (+0.36), Metal Skin +0.04 (+0.13), Spellbreaker +0.03 (+0.16)
- **Vyper**: Indomitable +0.42 (+0.54), Metal Skin +0.13 (+0.23), Spellbreaker +0.09 (+0.22)
- **Sinclair**: Indomitable +0.08 (+0.21), Return Fire +0.04 (+0.10), Spellbreaker +0.01 (+0.14)
- **Mina**: Spirit Resilience +0.12 (+0.25), Witchmail +0.10 (+0.26), Divine Barrier +0.10 (+0.18)
- **Drifter**: Witchmail +0.10 (+0.26), Metal Skin +0.09 (+0.19), Spirit Resilience +0.08 (+0.20)
- **Venator**: Bullet Resilience +0.09 (+0.16), Metal Skin +0.04 (+0.14), Plated Armor +0.03 (+0.15)
- **Victor**: Spellbreaker +0.07 (+0.20), Spirit Resilience +0.04 (+0.17), Healbane +0.01 (+0.09)
- **Paige**: Counterspell +0.01 (+0.05), Return Fire +0.00 (+0.06), Healbane -0.02 (+0.06)
- **The Doorman**: Indomitable +0.33 (+0.46), Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.03)
- **Billy**: Spirit Resilience +0.01 (+0.14), Spellbreaker -0.01 (+0.11), Return Fire -0.02 (+0.04)
- **Graves**: Witchmail +0.16 (+0.33), Spirit Resilience +0.14 (+0.26), Metal Skin +0.11 (+0.21)
- **Apollo**: Healbane +0.01 (+0.08), Reactive Barrier -0.01 (+0.04), Debuff Reducer -0.02 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.21 (+0.33), Spellbreaker +0.17 (+0.30), Witchmail +0.10 (+0.26)
- **Rem**: Unstoppable +0.14 (+0.24), Indomitable +0.11 (+0.24), Counterspell -0.01 (+0.03)
- **Silver**: Dispel Magic +0.07 (+0.14), Metal Skin +0.00 (+0.10), Healbane -0.01 (+0.06)
- **Celeste**: Witchmail +0.07 (+0.24), Spirit Resilience +0.07 (+0.19), Spellbreaker +0.03 (+0.16)
- **Rat King**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.03), Bullet Resilience -0.02 (+0.05)
- **Solomon**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.03), Debuff Reducer -0.02 (+0.02)
- **Violet**: Unstoppable +0.10 (+0.20), Dispel Magic +0.06 (+0.12), Indomitable +0.05 (+0.18)
- **Nurse Harrow**: Healbane +0.00 (+0.08), Spirit Resilience -0.01 (+0.11), Divine Barrier -0.01 (+0.07)
- **Baba**: Healbane +0.00 (+0.08), Unstoppable -0.00 (+0.10), Counterspell -0.01 (+0.03)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.207 | +0.065 | +0.114 | Wraith +0.18, Deadman Danny +0.17, Lash +0.16 | 13 heroes |
| Divine Barrier | 6,400 | +0.252 | +0.040 | +0.064 | Vindicta +0.22, Wraith +0.13, Paradox +0.13 | 2 heroes |
| Dispel Magic | 3,200 | +0.113 | +0.035 | +0.056 | Mirage +0.24, Violet +0.15, Infernus +0.13 | 9 heroes |
| Witchmail | 6,400 | +0.202 | +0.032 | +0.157 | Wraith +0.14, Deadman Danny +0.13, Lash +0.10 | 1 heroes |
| Indomitable | 6,400 | +0.181 | +0.029 | +0.131 | Vyper +0.42, The Doorman +0.35, Wraith +0.29 | 0 heroes |
| Spellbreaker | 6,400 | +0.157 | +0.025 | +0.125 | Grey Talon +0.18, Wraith +0.16, Deadman Danny +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.038 | Grey Talon +0.11, Wraith +0.06, Holliday +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.027 | +0.017 | +0.041 | Wraith +0.13, Violet +0.10, Paradox +0.10 | 5 heroes |
| Plated Armor | 6,400 | +0.023 | +0.004 | +0.108 | Vindicta +0.21, Holliday +0.18, Wraith +0.17 | 0 heroes |
| Bullet Resilience | 3,200 | -0.001 | -0.000 | +0.065 | Vindicta +0.23, Paradox +0.15, Wraith +0.09 | 1 heroes |
| Healbane | 1,600 | -0.004 | -0.003 | +0.060 | Viscous +0.05, Yamato +0.05, Infernus +0.05 | 16 heroes |
| Unstoppable | 6,400 | -0.026 | -0.004 | +0.097 | Rem +0.23, Violet +0.22, Ivy +0.19 | 3 heroes |
| Counterspell | 3,200 | -0.021 | -0.006 | +0.031 | Vyper +0.05, Deadman Danny +0.04, Lady Geist +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.108 | -0.034 | +0.098 | Wraith +0.25, Paradox +0.19, Mirage +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.148 | -0.093 | +0.049 | Paradox +0.09, Wraith +0.08, Lady Geist +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.14 (+0.24), Spellbreaker +0.13 (+0.26), Dispel Magic +0.13 (+0.18)
- **Seven**: Witchmail +0.05 (+0.21), Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Vindicta**: Bullet Resilience +0.23 (+0.30), Divine Barrier +0.22 (+0.28), Plated Armor +0.21 (+0.32)
- **Lady Geist**: Return Fire +0.05 (+0.10), Divine Barrier +0.04 (+0.10), Bullet Resilience +0.03 (+0.09)
- **Abrams**: Unstoppable +0.10 (+0.20), Dispel Magic +0.04 (+0.09), Healbane +0.03 (+0.10)
- **Wraith**: Indomitable +0.29 (+0.42), Metal Skin +0.25 (+0.34), Spirit Resilience +0.18 (+0.29)
- **McGinnis**: Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05), Debuff Reducer -0.02 (+0.02)
- **Paradox**: Metal Skin +0.19 (+0.28), Bullet Resilience +0.15 (+0.21), Spellbreaker +0.14 (+0.27)
- **Dynamo**: Healbane +0.03 (+0.09), Counterspell -0.01 (+0.03), Debuff Reducer -0.02 (+0.01)
- **Kelvin**: Counterspell +0.01 (+0.04), Healbane -0.00 (+0.06), Debuff Reducer -0.01 (+0.03)
- **Haze**: Plated Armor +0.11 (+0.22), Indomitable +0.10 (+0.23), Unstoppable +0.08 (+0.18)
- **Holliday**: Plated Armor +0.18 (+0.29), Debuff Reducer +0.06 (+0.10), Spellbreaker +0.06 (+0.18)
- **Bebop**: Healbane +0.02 (+0.08), Metal Skin +0.01 (+0.11), Divine Barrier -0.01 (+0.06)
- **Calico**: Reactive Barrier +0.01 (+0.05), Divine Barrier -0.00 (+0.06), Spellbreaker -0.01 (+0.12)
- **Grey Talon**: Spellbreaker +0.18 (+0.31), Unstoppable +0.16 (+0.26), Spirit Resilience +0.15 (+0.27)
- **Mo & Krill**: Unstoppable +0.09 (+0.19), Spellbreaker +0.04 (+0.17), Dispel Magic +0.03 (+0.08)
- **Shiv**: Metal Skin +0.04 (+0.14), Bullet Resilience +0.04 (+0.10), Divine Barrier +0.03 (+0.10)
- **Ivy**: Unstoppable +0.19 (+0.28), Indomitable +0.12 (+0.25), Dispel Magic +0.05 (+0.11)
- **Warden**: Return Fire +0.01 (+0.06), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Yamato**: Healbane +0.05 (+0.11), Debuff Reducer +0.01 (+0.05), Counterspell +0.00 (+0.03)
- **Lash**: Spirit Resilience +0.16 (+0.28), Spellbreaker +0.13 (+0.25), Witchmail +0.10 (+0.26)
- **Viscous**: Healbane +0.05 (+0.11), Return Fire +0.03 (+0.08), Divine Barrier +0.02 (+0.09)
- **Pocket**: Spirit Resilience +0.05 (+0.17), Counterspell +0.02 (+0.05), Return Fire +0.00 (+0.05)
- **Mirage**: Dispel Magic +0.24 (+0.30), Metal Skin +0.14 (+0.24), Spellbreaker +0.04 (+0.16)
- **Vyper**: Indomitable +0.42 (+0.55), Spellbreaker +0.10 (+0.22), Reactive Barrier +0.09 (+0.13)
- **Sinclair**: Indomitable +0.15 (+0.28), Unstoppable +0.03 (+0.13), Debuff Reducer +0.03 (+0.06)
- **Mina**: Spirit Resilience +0.13 (+0.24), Divine Barrier +0.10 (+0.16), Witchmail +0.09 (+0.25)
- **Drifter**: Spirit Resilience +0.10 (+0.21), Witchmail +0.06 (+0.22), Metal Skin +0.05 (+0.15)
- **Venator**: Metal Skin +0.04 (+0.14), Bullet Resilience +0.04 (+0.11), Debuff Reducer +0.02 (+0.06)
- **Victor**: Healbane +0.03 (+0.09), Spirit Resilience +0.03 (+0.14), Spellbreaker +0.02 (+0.14)
- **Paige**: Counterspell +0.01 (+0.04), Return Fire -0.00 (+0.04), Healbane -0.02 (+0.04)
- **The Doorman**: Indomitable +0.35 (+0.48), Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (+0.02)
- **Billy**: Spellbreaker +0.00 (+0.13), Counterspell -0.00 (+0.03), Reactive Barrier -0.00 (+0.04)
- **Graves**: Return Fire +0.02 (+0.07), Metal Skin +0.01 (+0.11), Witchmail +0.01 (+0.17)
- **Apollo**: Counterspell +0.01 (+0.04), Healbane +0.01 (+0.07), Debuff Reducer +0.01 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.17 (+0.29), Spellbreaker +0.14 (+0.27), Indomitable +0.14 (+0.27)
- **Rem**: Unstoppable +0.23 (+0.33), Debuff Reducer -0.01 (+0.03), Counterspell -0.01 (+0.02)
- **Silver**: Dispel Magic +0.09 (+0.15), Healbane -0.00 (+0.06), Metal Skin -0.01 (+0.09)
- **Celeste**: Dispel Magic +0.08 (+0.14), Witchmail +0.06 (+0.22), Healbane +0.03 (+0.09)
- **Rat King**: Return Fire -0.01 (+0.04), Counterspell -0.01 (+0.02), Healbane -0.02 (+0.04)
- **Solomon**: Return Fire +0.00 (+0.05), Counterspell -0.01 (+0.02), Debuff Reducer -0.02 (+0.02)
- **Violet**: Unstoppable +0.22 (+0.31), Dispel Magic +0.15 (+0.20), Indomitable +0.12 (+0.25)
- **Nurse Harrow**: Healbane +0.04 (+0.10), Counterspell +0.02 (+0.05), Dispel Magic +0.01 (+0.06)
- **Baba**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.04)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.236 | +0.074 | +0.127 | Deadman Danny +0.36, Lash +0.35, Grey Talon +0.15 | 14 heroes |
| Dispel Magic | 3,200 | +0.127 | +0.040 | +0.072 | Drifter +0.27, Mirage +0.25, Nurse Harrow +0.15 | 9 heroes |
| Divine Barrier | 6,400 | +0.199 | +0.031 | +0.055 | Vindicta +0.30, Lash +0.16, Calico +0.10 | 3 heroes |
| Indomitable | 6,400 | +0.186 | +0.030 | +0.132 | The Doorman +0.45, Vyper +0.35, Sinclair +0.16 | 1 heroes |
| Witchmail | 6,400 | +0.191 | +0.030 | +0.148 | Deadman Danny +0.28, Lash +0.20, Vindicta +0.18 | 2 heroes |
| Spellbreaker | 6,400 | +0.182 | +0.028 | +0.143 | Deadman Danny +0.32, Lash +0.26, Grey Talon +0.18 | 0 heroes |
| Debuff Reducer | 1,600 | +0.031 | +0.020 | +0.048 | Grey Talon +0.13, Paige +0.09, Bebop +0.07 | 0 heroes |
| Unstoppable | 6,400 | +0.022 | +0.003 | +0.149 | Paige +0.32, Wraith +0.24, Rem +0.20 | 8 heroes |
| Plated Armor | 6,400 | +0.013 | +0.002 | +0.106 | Vindicta +0.40, Deadman Danny +0.17, Vyper +0.14 | 2 heroes |
| Reactive Barrier | 1,600 | -0.001 | -0.001 | +0.034 | Vyper +0.09, Deadman Danny +0.08, Drifter +0.08 | 3 heroes |
| Healbane | 1,600 | -0.003 | -0.002 | +0.059 | Dynamo +0.07, Deadman Danny +0.07, Yamato +0.05 | 13 heroes |
| Bullet Resilience | 3,200 | -0.015 | -0.005 | +0.059 | Vindicta +0.31, Lash +0.10, Paradox +0.06 | 0 heroes |
| Counterspell | 3,200 | -0.026 | -0.008 | +0.031 | Vyper +0.04, Celeste +0.03, Vindicta +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.108 | -0.034 | +0.101 | Lash +0.22, Mirage +0.21, Vyper +0.18 | 0 heroes |
| Return Fire | 1,600 | -0.155 | -0.097 | +0.043 | Paradox +0.07, Holliday +0.06, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.30), Indomitable +0.05 (+0.18), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.02 (+0.17), Counterspell +0.01 (+0.04), Healbane -0.01 (+0.05)
- **Vindicta**: Plated Armor +0.40 (+0.51), Bullet Resilience +0.31 (+0.37), Divine Barrier +0.30 (+0.36)
- **Lady Geist**: Bullet Resilience +0.05 (+0.11), Metal Skin +0.02 (+0.12), Healbane +0.02 (+0.08)
- **Abrams**: Unstoppable +0.06 (+0.21), Healbane +0.04 (+0.10), Debuff Reducer +0.01 (+0.05)
- **Wraith**: Unstoppable +0.24 (+0.39), Metal Skin +0.16 (+0.26), Indomitable +0.15 (+0.28)
- **McGinnis**: Spirit Resilience -0.00 (+0.12), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Paradox**: Unstoppable +0.13 (+0.28), Dispel Magic +0.12 (+0.19), Metal Skin +0.12 (+0.22)
- **Dynamo**: Healbane +0.07 (+0.13), Return Fire -0.00 (+0.04), Counterspell -0.00 (+0.03)
- **Kelvin**: Spirit Resilience +0.15 (+0.28), Witchmail +0.06 (+0.21), Spellbreaker +0.03 (+0.18)
- **Haze**: Unstoppable +0.18 (+0.33), Indomitable +0.06 (+0.19), Plated Armor +0.04 (+0.15)
- **Holliday**: Spellbreaker +0.07 (+0.21), Debuff Reducer +0.06 (+0.11), Return Fire +0.06 (+0.11)
- **Bebop**: Debuff Reducer +0.07 (+0.12), Spellbreaker +0.07 (+0.21), Indomitable +0.02 (+0.16)
- **Calico**: Spirit Resilience +0.11 (+0.24), Divine Barrier +0.10 (+0.16), Reactive Barrier +0.06 (+0.10)
- **Grey Talon**: Spellbreaker +0.18 (+0.32), Spirit Resilience +0.15 (+0.28), Debuff Reducer +0.13 (+0.18)
- **Mo & Krill**: Unstoppable +0.04 (+0.19), Spellbreaker +0.02 (+0.16), Healbane +0.01 (+0.06)
- **Shiv**: Divine Barrier +0.06 (+0.12), Metal Skin +0.05 (+0.15), Bullet Resilience +0.05 (+0.11)
- **Ivy**: Unstoppable +0.16 (+0.31), Indomitable +0.12 (+0.25), Debuff Reducer +0.05 (+0.10)
- **Warden**: Metal Skin +0.03 (+0.13), Return Fire +0.03 (+0.07), Healbane +0.01 (+0.07)
- **Yamato**: Healbane +0.05 (+0.11), Reactive Barrier +0.01 (+0.05), Indomitable +0.01 (+0.15)
- **Lash**: Spirit Resilience +0.35 (+0.48), Spellbreaker +0.26 (+0.40), Metal Skin +0.22 (+0.32)
- **Viscous**: Spirit Resilience +0.09 (+0.21), Witchmail +0.09 (+0.23), Divine Barrier +0.08 (+0.13)
- **Pocket**: Spirit Resilience +0.07 (+0.20), Witchmail +0.05 (+0.20), Spellbreaker +0.02 (+0.16)
- **Mirage**: Dispel Magic +0.25 (+0.32), Metal Skin +0.21 (+0.31), Spellbreaker -0.00 (+0.14)
- **Vyper**: Indomitable +0.35 (+0.49), Metal Skin +0.18 (+0.28), Plated Armor +0.14 (+0.25)
- **Sinclair**: Indomitable +0.16 (+0.29), Spellbreaker +0.07 (+0.22), Reactive Barrier +0.06 (+0.10)
- **Mina**: Counterspell +0.01 (+0.04), Divine Barrier +0.01 (+0.06), Return Fire -0.00 (+0.04)
- **Drifter**: Dispel Magic +0.27 (+0.34), Reactive Barrier +0.08 (+0.11), Metal Skin +0.06 (+0.16)
- **Venator**: Metal Skin +0.12 (+0.22), Bullet Resilience +0.04 (+0.10), Debuff Reducer +0.00 (+0.05)
- **Victor**: Spellbreaker +0.07 (+0.22), Healbane +0.01 (+0.07), Spirit Resilience +0.01 (+0.14)
- **Paige**: Unstoppable +0.32 (+0.47), Debuff Reducer +0.09 (+0.14), Counterspell +0.00 (+0.04)
- **The Doorman**: Indomitable +0.45 (+0.58), Counterspell +0.00 (+0.03), Return Fire -0.01 (+0.03)
- **Billy**: Spellbreaker -0.01 (+0.14), Reactive Barrier -0.01 (+0.02), Return Fire -0.01 (+0.03)
- **Graves**: Spirit Resilience +0.05 (+0.18), Witchmail +0.03 (+0.18), Return Fire +0.03 (+0.07)
- **Apollo**: Reactive Barrier +0.04 (+0.07), Healbane +0.01 (+0.07), Divine Barrier +0.00 (+0.06)
- **Deadman Danny**: Spirit Resilience +0.36 (+0.48), Spellbreaker +0.32 (+0.46), Witchmail +0.28 (+0.43)
- **Rem**: Unstoppable +0.20 (+0.35), Counterspell -0.01 (+0.02), Divine Barrier -0.01 (+0.04)
- **Silver**: Dispel Magic +0.07 (+0.14), Debuff Reducer +0.01 (+0.05), Reactive Barrier -0.00 (+0.03)
- **Celeste**: Witchmail +0.05 (+0.20), Spirit Resilience +0.05 (+0.17), Dispel Magic +0.03 (+0.10)
- **Rat King**: Return Fire +0.02 (+0.06), Counterspell -0.00 (+0.03), Healbane -0.01 (+0.05)
- **Solomon**: Return Fire +0.02 (+0.06), Reactive Barrier +0.01 (+0.04), Counterspell +0.00 (+0.03)
- **Violet**: Unstoppable +0.09 (+0.24), Spirit Resilience +0.05 (+0.18), Indomitable +0.05 (+0.18)
- **Nurse Harrow**: Dispel Magic +0.15 (+0.23), Spirit Resilience +0.09 (+0.22), Witchmail +0.04 (+0.19)
- **Baba**: Witchmail +0.03 (+0.17), Unstoppable +0.02 (+0.17), Healbane +0.02 (+0.08)
