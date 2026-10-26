# Counter items in the sim (phantom and up)

Built 2026-10-26T09:49:56Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.234 | +0.073 | +0.126 | Lash +0.25, Wraith +0.15, Deadman Danny +0.12 | 1 heroes |
| Divine Barrier | 6,400 | +0.374 | +0.060 | +0.099 | Wraith +0.17, Lash +0.16, Calico +0.11 | 0 heroes |
| Dispel Magic | 3,200 | +0.141 | +0.044 | +0.079 | Mirage +0.37, Silver +0.13, Infernus +0.10 | 4 heroes |
| Debuff Reducer | 1,600 | +0.064 | +0.040 | +0.056 | Wraith +0.11, Deadman Danny +0.07, Calico +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.056 | +0.036 | +0.053 | Deadman Danny +0.15, Wraith +0.14, The Doorman +0.11 | 2 heroes |
| Witchmail | 6,400 | +0.229 | +0.036 | +0.196 | Wraith +0.16, Lash +0.15, Deadman Danny +0.15 | 0 heroes |
| Indomitable | 6,400 | +0.190 | +0.030 | +0.140 | Wraith +0.30, Vyper +0.29, Deadman Danny +0.19 | 0 heroes |
| Healbane | 1,600 | +0.043 | +0.027 | +0.087 | Nurse Harrow +0.05, Mo & Krill +0.05, Deadman Danny +0.05 | 11 heroes |
| Spellbreaker | 6,400 | +0.152 | +0.024 | +0.149 | Lash +0.22, Deadman Danny +0.19, Wraith +0.17 | 0 heroes |
| Bullet Resilience | 3,200 | +0.046 | +0.014 | +0.093 | Paradox +0.14, Wraith +0.13, Deadman Danny +0.12 | 0 heroes |
| Counterspell | 3,200 | +0.017 | +0.005 | +0.069 | Deadman Danny +0.09, Wraith +0.08, Calico +0.06 | 1 heroes |
| Plated Armor | 6,400 | +0.026 | +0.004 | +0.129 | Holliday +0.23, Wraith +0.18, Deadman Danny +0.14 | 0 heroes |
| Unstoppable | 6,400 | +0.002 | +0.000 | +0.115 | Deadman Danny +0.15, Wraith +0.13, Ivy +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.091 | -0.029 | +0.112 | Wraith +0.25, Drifter +0.16, Paradox +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.129 | -0.081 | +0.074 | Wraith +0.08, The Doorman +0.07, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.18), Unstoppable +0.07 (+0.19), Spirit Resilience +0.05 (+0.17)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.03 (+0.02)
- **Vindicta**: Divine Barrier +0.01 (+0.10), Counterspell -0.00 (+0.07), Return Fire -0.00 (+0.07)
- **Lady Geist**: Return Fire +0.06 (+0.13), Dispel Magic +0.04 (+0.11), Counterspell +0.03 (+0.10)
- **Abrams**: Indomitable +0.14 (+0.28), Unstoppable +0.10 (+0.21), Spirit Resilience +0.06 (+0.18)
- **Wraith**: Indomitable +0.30 (+0.44), Metal Skin +0.25 (+0.36), Plated Armor +0.18 (+0.31)
- **McGinnis**: Spirit Resilience +0.03 (+0.16), Counterspell -0.02 (+0.05), Dispel Magic -0.02 (+0.06)
- **Paradox**: Metal Skin +0.16 (+0.27), Bullet Resilience +0.14 (+0.24), Indomitable +0.13 (+0.27)
- **Dynamo**: Healbane -0.01 (+0.08), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane -0.00 (+0.09), Counterspell -0.00 (+0.07), Debuff Reducer -0.01 (+0.04)
- **Haze**: Plated Armor +0.09 (+0.22), Indomitable +0.06 (+0.20), Bullet Resilience +0.05 (+0.14)
- **Holliday**: Plated Armor +0.23 (+0.36), Spellbreaker +0.05 (+0.20), Debuff Reducer +0.05 (+0.10)
- **Bebop**: Divine Barrier +0.02 (+0.12), Counterspell +0.02 (+0.09), Return Fire +0.02 (+0.09)
- **Calico**: Spellbreaker +0.13 (+0.27), Divine Barrier +0.11 (+0.21), Spirit Resilience +0.11 (+0.23)
- **Grey Talon**: Reactive Barrier +0.05 (+0.11), Indomitable +0.05 (+0.19), Spellbreaker +0.04 (+0.19)
- **Mo & Krill**: Spellbreaker +0.13 (+0.28), Spirit Resilience +0.08 (+0.20), Witchmail +0.06 (+0.25)
- **Shiv**: Healbane -0.01 (+0.08), Return Fire -0.02 (+0.06), Divine Barrier -0.04 (+0.06)
- **Ivy**: Unstoppable +0.10 (+0.22), Indomitable +0.06 (+0.20), Debuff Reducer +0.01 (+0.06)
- **Warden**: Return Fire +0.03 (+0.11), Bullet Resilience +0.02 (+0.11), Divine Barrier +0.01 (+0.11)
- **Yamato**: Healbane +0.02 (+0.11), Debuff Reducer -0.03 (+0.03), Counterspell -0.04 (+0.03)
- **Lash**: Spirit Resilience +0.25 (+0.38), Spellbreaker +0.22 (+0.37), Divine Barrier +0.16 (+0.26)
- **Viscous**: Divine Barrier -0.03 (+0.07), Return Fire -0.03 (+0.05), Healbane -0.03 (+0.06)
- **Pocket**: Witchmail +0.03 (+0.23), Spirit Resilience +0.03 (+0.15), Return Fire +0.02 (+0.09)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spellbreaker +0.09 (+0.24), Spirit Resilience +0.06 (+0.18)
- **Vyper**: Indomitable +0.29 (+0.43), Debuff Reducer +0.06 (+0.12), Spellbreaker +0.03 (+0.18)
- **Sinclair**: Indomitable +0.06 (+0.20), Spellbreaker +0.03 (+0.18), Return Fire +0.02 (+0.09)
- **Mina**: Divine Barrier +0.08 (+0.18), Spirit Resilience +0.07 (+0.19), Witchmail +0.06 (+0.26)
- **Drifter**: Metal Skin +0.16 (+0.28), Spirit Resilience +0.12 (+0.25), Witchmail +0.09 (+0.28)
- **Venator**: Bullet Resilience +0.10 (+0.19), Metal Skin +0.03 (+0.15), Debuff Reducer +0.02 (+0.07)
- **Victor**: Healbane -0.01 (+0.08), Counterspell -0.04 (+0.03), Reactive Barrier -0.04 (+0.01)
- **Paige**: Healbane -0.00 (+0.09), Return Fire -0.02 (+0.05), Counterspell -0.02 (+0.05)
- **The Doorman**: Indomitable +0.18 (+0.32), Witchmail +0.12 (+0.31), Reactive Barrier +0.11 (+0.17)
- **Billy**: Counterspell +0.05 (+0.12), Healbane +0.04 (+0.13), Spellbreaker +0.04 (+0.19)
- **Graves**: Spirit Resilience +0.12 (+0.24), Divine Barrier +0.09 (+0.19), Witchmail +0.09 (+0.29)
- **Apollo**: Healbane -0.03 (+0.06), Debuff Reducer -0.03 (+0.02), Counterspell -0.04 (+0.03)
- **Deadman Danny**: Spellbreaker +0.19 (+0.34), Indomitable +0.19 (+0.33), Unstoppable +0.15 (+0.26)
- **Rem**: Witchmail +0.01 (+0.21), Dispel Magic -0.00 (+0.08), Indomitable -0.01 (+0.13)
- **Silver**: Dispel Magic +0.13 (+0.20), Reactive Barrier +0.03 (+0.08), Metal Skin +0.02 (+0.13)
- **Celeste**: Spirit Resilience +0.11 (+0.23), Witchmail +0.10 (+0.30), Plated Armor +0.04 (+0.17)
- **Rat King**: Counterspell +0.00 (+0.07), Bullet Resilience -0.00 (+0.09), Return Fire -0.00 (+0.07)
- **Solomon**: Return Fire -0.01 (+0.07), Counterspell -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **Violet**: Return Fire +0.03 (+0.10), Witchmail +0.00 (+0.20), Healbane -0.01 (+0.07)
- **Nurse Harrow**: Healbane +0.05 (+0.14), Counterspell -0.02 (+0.05), Dispel Magic -0.03 (+0.05)
- **Baba**: Healbane +0.01 (+0.10), Counterspell -0.02 (+0.05), Unstoppable -0.02 (+0.09)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.210 | +0.066 | +0.110 | Lash +0.26, Pocket +0.19, Graves +0.16 | 10 heroes |
| Dispel Magic | 3,200 | +0.120 | +0.038 | +0.060 | Mirage +0.31, Lash +0.14, Silver +0.12 | 7 heroes |
| Divine Barrier | 6,400 | +0.224 | +0.036 | +0.068 | Lash +0.17, Vindicta +0.12, Wraith +0.11 | 1 heroes |
| Witchmail | 6,400 | +0.209 | +0.033 | +0.160 | Lash +0.17, Graves +0.16, Wraith +0.10 | 0 heroes |
| Indomitable | 6,400 | +0.157 | +0.025 | +0.111 | Vyper +0.33, Wraith +0.22, Deadman Danny +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.037 | +0.023 | +0.043 | Wraith +0.08, Lash +0.07, Vyper +0.06 | 1 heroes |
| Spellbreaker | 6,400 | +0.142 | +0.022 | +0.116 | Lash +0.21, Wraith +0.12, Pocket +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | +0.035 | +0.022 | +0.040 | Wraith +0.11, Deadman Danny +0.09, The Doorman +0.08 | 4 heroes |
| Healbane | 1,600 | +0.011 | +0.007 | +0.073 | Lash +0.08, Haze +0.04, Pocket +0.04 | 17 heroes |
| Bullet Resilience | 3,200 | +0.018 | +0.006 | +0.070 | Paradox +0.13, Lash +0.12, Vindicta +0.12 | 0 heroes |
| Plated Armor | 6,400 | +0.020 | +0.003 | +0.105 | Holliday +0.14, Haze +0.14, Paradox +0.12 | 0 heroes |
| Counterspell | 3,200 | -0.006 | -0.002 | +0.045 | Lash +0.08, Deadman Danny +0.08, Pocket +0.06 | 1 heroes |
| Unstoppable | 6,400 | -0.030 | -0.005 | +0.088 | Abrams +0.20, Ivy +0.13, Mo & Krill +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.113 | -0.035 | +0.090 | Wraith +0.20, Paradox +0.17, Lash +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.143 | -0.089 | +0.059 | Vindicta +0.07, Wraith +0.06, Lash +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.07 (+0.14), Unstoppable +0.03 (+0.12), Healbane +0.03 (+0.10)
- **Seven**: Witchmail +0.03 (+0.19), Counterspell -0.00 (+0.04), Healbane -0.00 (+0.07)
- **Vindicta**: Divine Barrier +0.12 (+0.19), Bullet Resilience +0.12 (+0.19), Plated Armor +0.10 (+0.20)
- **Lady Geist**: Return Fire +0.04 (+0.10), Divine Barrier +0.02 (+0.09), Healbane +0.01 (+0.09)
- **Abrams**: Unstoppable +0.20 (+0.28), Dispel Magic +0.11 (+0.17), Indomitable +0.05 (+0.16)
- **Wraith**: Indomitable +0.22 (+0.33), Metal Skin +0.20 (+0.29), Spellbreaker +0.12 (+0.23)
- **McGinnis**: Healbane +0.01 (+0.08), Spirit Resilience +0.00 (+0.11), Counterspell -0.00 (+0.04)
- **Paradox**: Metal Skin +0.17 (+0.26), Bullet Resilience +0.13 (+0.20), Plated Armor +0.12 (+0.22)
- **Dynamo**: Healbane +0.00 (+0.08), Counterspell -0.02 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.01 (+0.12), Dispel Magic -0.01 (+0.05), Healbane -0.01 (+0.06)
- **Haze**: Plated Armor +0.14 (+0.24), Bullet Resilience +0.09 (+0.16), Indomitable +0.08 (+0.19)
- **Holliday**: Plated Armor +0.14 (+0.25), Indomitable +0.03 (+0.14), Spellbreaker +0.03 (+0.15)
- **Bebop**: Witchmail +0.05 (+0.21), Divine Barrier +0.04 (+0.11), Counterspell +0.04 (+0.08)
- **Calico**: Reactive Barrier +0.05 (+0.09), Divine Barrier +0.03 (+0.09), Spellbreaker +0.02 (+0.13)
- **Grey Talon**: Spellbreaker +0.03 (+0.15), Debuff Reducer +0.03 (+0.07), Reactive Barrier +0.03 (+0.07)
- **Mo & Krill**: Unstoppable +0.10 (+0.19), Spellbreaker +0.08 (+0.19), Dispel Magic +0.04 (+0.10)
- **Shiv**: Divine Barrier +0.02 (+0.09), Bullet Resilience +0.01 (+0.08), Plated Armor -0.01 (+0.09)
- **Ivy**: Unstoppable +0.13 (+0.22), Indomitable +0.05 (+0.16), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.08), Counterspell +0.01 (+0.05), Bullet Resilience -0.01 (+0.06)
- **Yamato**: Healbane +0.02 (+0.09), Counterspell -0.03 (+0.01), Debuff Reducer -0.03 (+0.01)
- **Lash**: Spirit Resilience +0.26 (+0.37), Spellbreaker +0.21 (+0.33), Divine Barrier +0.17 (+0.24)
- **Viscous**: Counterspell -0.02 (+0.03), Healbane -0.02 (+0.05), Divine Barrier -0.03 (+0.04)
- **Pocket**: Spirit Resilience +0.19 (+0.30), Spellbreaker +0.11 (+0.22), Witchmail +0.10 (+0.26)
- **Mirage**: Dispel Magic +0.31 (+0.37), Spellbreaker +0.02 (+0.13), Spirit Resilience +0.02 (+0.13)
- **Vyper**: Indomitable +0.33 (+0.44), Debuff Reducer +0.06 (+0.10), Spellbreaker +0.04 (+0.16)
- **Sinclair**: Indomitable +0.09 (+0.21), Spellbreaker +0.02 (+0.14), Return Fire +0.00 (+0.06)
- **Mina**: Spirit Resilience +0.12 (+0.24), Spellbreaker +0.08 (+0.20), Divine Barrier +0.07 (+0.14)
- **Drifter**: Metal Skin +0.10 (+0.19), Spirit Resilience +0.10 (+0.21), Witchmail +0.07 (+0.23)
- **Venator**: Bullet Resilience +0.09 (+0.16), Metal Skin +0.05 (+0.14), Plated Armor +0.03 (+0.14)
- **Victor**: Spellbreaker +0.07 (+0.19), Spirit Resilience +0.01 (+0.12), Healbane +0.01 (+0.08)
- **Paige**: Counterspell +0.00 (+0.05), Return Fire -0.00 (+0.06), Healbane -0.02 (+0.05)
- **The Doorman**: Indomitable +0.10 (+0.21), Spirit Resilience +0.09 (+0.20), Witchmail +0.08 (+0.24)
- **Billy**: Spirit Resilience +0.00 (+0.11), Spellbreaker -0.00 (+0.11), Counterspell -0.01 (+0.03)
- **Graves**: Witchmail +0.16 (+0.32), Spirit Resilience +0.16 (+0.27), Metal Skin +0.11 (+0.20)
- **Apollo**: Healbane -0.01 (+0.06), Reactive Barrier -0.02 (+0.02), Counterspell -0.04 (+0.01)
- **Deadman Danny**: Indomitable +0.12 (+0.23), Spellbreaker +0.10 (+0.22), Unstoppable +0.10 (+0.19)
- **Rem**: Witchmail +0.02 (+0.18), Counterspell -0.00 (+0.04), Unstoppable -0.01 (+0.08)
- **Silver**: Dispel Magic +0.12 (+0.18), Divine Barrier +0.01 (+0.08), Reactive Barrier -0.00 (+0.04)
- **Celeste**: Witchmail +0.04 (+0.20), Spirit Resilience +0.02 (+0.13), Spellbreaker +0.01 (+0.12)
- **Rat King**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.03), Bullet Resilience -0.02 (+0.05)
- **Solomon**: Return Fire +0.00 (+0.06), Counterspell -0.02 (+0.03), Debuff Reducer -0.02 (+0.02)
- **Violet**: Return Fire +0.04 (+0.10), Witchmail +0.02 (+0.18), Healbane +0.01 (+0.09)
- **Nurse Harrow**: Healbane +0.03 (+0.10), Witchmail -0.00 (+0.16), Counterspell -0.01 (+0.04)
- **Baba**: Return Fire +0.00 (+0.06), Healbane +0.00 (+0.08), Unstoppable -0.00 (+0.09)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.209 | +0.065 | +0.116 | Wraith +0.19, Grey Talon +0.15, Mina +0.15 | 13 heroes |
| Divine Barrier | 6,400 | +0.256 | +0.041 | +0.056 | Vindicta +0.12, Wraith +0.12, Paradox +0.11 | 2 heroes |
| Dispel Magic | 3,200 | +0.108 | +0.034 | +0.051 | Mirage +0.29, Paradox +0.13, Infernus +0.10 | 9 heroes |
| Witchmail | 6,400 | +0.209 | +0.033 | +0.164 | Wraith +0.15, Mina +0.12, Paradox +0.11 | 1 heroes |
| Indomitable | 6,400 | +0.166 | +0.027 | +0.116 | Vyper +0.35, Wraith +0.31, Grey Talon +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.150 | +0.023 | +0.119 | Grey Talon +0.19, Wraith +0.18, Infernus +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.038 | Grey Talon +0.10, Vyper +0.07, Rem +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.021 | +0.013 | +0.034 | Wraith +0.12, Grey Talon +0.11, Paradox +0.10 | 5 heroes |
| Plated Armor | 6,400 | +0.020 | +0.003 | +0.104 | Wraith +0.19, Holliday +0.16, Haze +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | -0.005 | -0.002 | +0.059 | Vindicta +0.13, Paradox +0.09, Wraith +0.09 | 1 heroes |
| Healbane | 1,600 | -0.006 | -0.004 | +0.059 | Yamato +0.06, Infernus +0.04, Vindicta +0.04 | 16 heroes |
| Unstoppable | 6,400 | -0.036 | -0.006 | +0.085 | Grey Talon +0.17, Ivy +0.15, Abrams +0.13 | 3 heroes |
| Counterspell | 3,200 | -0.019 | -0.006 | +0.034 | Yamato +0.04, Vindicta +0.04, Nurse Harrow +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.110 | -0.035 | +0.095 | Wraith +0.27, Paradox +0.19, Drifter +0.09 | 0 heroes |
| Return Fire | 1,600 | -0.148 | -0.093 | +0.049 | Wraith +0.08, Paradox +0.07, Vindicta +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.13 (+0.21), Spellbreaker +0.12 (+0.24), Dispel Magic +0.10 (+0.15)
- **Seven**: Witchmail +0.05 (+0.21), Counterspell +0.01 (+0.04), Healbane +0.00 (+0.06)
- **Vindicta**: Bullet Resilience +0.13 (+0.19), Divine Barrier +0.12 (+0.17), Plated Armor +0.09 (+0.20)
- **Lady Geist**: Return Fire +0.05 (+0.10), Divine Barrier +0.02 (+0.08), Counterspell +0.02 (+0.05)
- **Abrams**: Unstoppable +0.13 (+0.22), Dispel Magic +0.07 (+0.12), Healbane +0.03 (+0.09)
- **Wraith**: Indomitable +0.31 (+0.43), Metal Skin +0.27 (+0.37), Plated Armor +0.19 (+0.30)
- **McGinnis**: Counterspell -0.02 (+0.01), Spirit Resilience -0.02 (+0.10), Healbane -0.02 (+0.04)
- **Paradox**: Metal Skin +0.19 (+0.29), Dispel Magic +0.13 (+0.18), Indomitable +0.12 (+0.23)
- **Dynamo**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Healbane -0.00 (+0.05), Counterspell -0.01 (+0.03), Dispel Magic -0.01 (+0.04)
- **Haze**: Indomitable +0.10 (+0.22), Unstoppable +0.10 (+0.18), Plated Armor +0.09 (+0.20)
- **Holliday**: Plated Armor +0.16 (+0.26), Debuff Reducer +0.06 (+0.10), Spellbreaker +0.06 (+0.18)
- **Bebop**: Metal Skin +0.02 (+0.12), Healbane +0.02 (+0.08), Divine Barrier +0.01 (+0.07)
- **Calico**: Reactive Barrier +0.03 (+0.06), Spellbreaker +0.02 (+0.14), Divine Barrier +0.02 (+0.08)
- **Grey Talon**: Spellbreaker +0.19 (+0.31), Unstoppable +0.17 (+0.26), Indomitable +0.16 (+0.27)
- **Mo & Krill**: Unstoppable +0.12 (+0.21), Spellbreaker +0.07 (+0.18), Dispel Magic +0.04 (+0.09)
- **Shiv**: Metal Skin +0.03 (+0.12), Bullet Resilience +0.02 (+0.08), Divine Barrier +0.01 (+0.07)
- **Ivy**: Unstoppable +0.15 (+0.24), Indomitable +0.11 (+0.23), Dispel Magic +0.03 (+0.08)
- **Warden**: Return Fire +0.02 (+0.07), Healbane +0.01 (+0.07), Metal Skin -0.01 (+0.09)
- **Yamato**: Healbane +0.06 (+0.12), Counterspell +0.04 (+0.08), Debuff Reducer +0.04 (+0.08)
- **Lash**: Spirit Resilience +0.14 (+0.26), Spellbreaker +0.12 (+0.24), Witchmail +0.10 (+0.27)
- **Viscous**: Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04), Return Fire -0.00 (+0.05)
- **Pocket**: Spirit Resilience +0.02 (+0.14), Counterspell -0.01 (+0.02), Witchmail -0.02 (+0.15)
- **Mirage**: Dispel Magic +0.29 (+0.35), Spirit Resilience +0.02 (+0.14), Spellbreaker +0.02 (+0.14)
- **Vyper**: Indomitable +0.35 (+0.46), Debuff Reducer +0.07 (+0.11), Spellbreaker +0.05 (+0.17)
- **Sinclair**: Indomitable +0.15 (+0.27), Unstoppable +0.02 (+0.11), Debuff Reducer +0.01 (+0.05)
- **Mina**: Spirit Resilience +0.15 (+0.26), Witchmail +0.12 (+0.28), Spellbreaker +0.08 (+0.20)
- **Drifter**: Spirit Resilience +0.10 (+0.22), Metal Skin +0.09 (+0.18), Witchmail +0.05 (+0.21)
- **Venator**: Bullet Resilience +0.06 (+0.12), Metal Skin +0.06 (+0.15), Plated Armor +0.01 (+0.12)
- **Victor**: Healbane +0.03 (+0.09), Spellbreaker +0.01 (+0.13), Spirit Resilience +0.00 (+0.12)
- **Paige**: Counterspell +0.00 (+0.04), Return Fire -0.01 (+0.04), Healbane -0.02 (+0.04)
- **The Doorman**: Spirit Resilience +0.12 (+0.23), Indomitable +0.10 (+0.22), Witchmail +0.07 (+0.24)
- **Billy**: Reactive Barrier +0.01 (+0.04), Healbane -0.01 (+0.05), Counterspell -0.01 (+0.02)
- **Graves**: Witchmail +0.03 (+0.19), Return Fire +0.02 (+0.07), Metal Skin +0.02 (+0.11)
- **Apollo**: Healbane +0.01 (+0.06), Reactive Barrier -0.02 (+0.02), Counterspell -0.03 (+0.01)
- **Deadman Danny**: Spellbreaker +0.11 (+0.22), Indomitable +0.09 (+0.21), Spirit Resilience +0.09 (+0.20)
- **Rem**: Unstoppable +0.06 (+0.15), Debuff Reducer +0.06 (+0.10), Counterspell +0.01 (+0.04)
- **Silver**: Dispel Magic +0.09 (+0.14), Reactive Barrier -0.00 (+0.03), Divine Barrier -0.00 (+0.05)
- **Celeste**: Dispel Magic +0.09 (+0.14), Witchmail +0.09 (+0.26), Spirit Resilience +0.07 (+0.18)
- **Rat King**: Return Fire -0.01 (+0.04), Counterspell -0.01 (+0.03), Bullet Resilience -0.01 (+0.05)
- **Solomon**: Return Fire +0.01 (+0.06), Counterspell +0.01 (+0.04), Healbane -0.00 (+0.05)
- **Violet**: Witchmail +0.06 (+0.23), Return Fire +0.04 (+0.09), Divine Barrier +0.03 (+0.09)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Counterspell +0.02 (+0.05), Dispel Magic +0.02 (+0.07)
- **Baba**: Return Fire +0.02 (+0.07), Healbane -0.00 (+0.06), Unstoppable -0.01 (+0.08)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.228 | +0.071 | +0.120 | Lash +0.34, Deadman Danny +0.31, The Doorman +0.24 | 14 heroes |
| Dispel Magic | 3,200 | +0.121 | +0.038 | +0.066 | Mirage +0.32, Drifter +0.29, Lash +0.17 | 9 heroes |
| Divine Barrier | 6,400 | +0.192 | +0.030 | +0.049 | Lash +0.17, Calico +0.12, The Doorman +0.11 | 3 heroes |
| Witchmail | 6,400 | +0.188 | +0.029 | +0.145 | Deadman Danny +0.21, Lash +0.21, The Doorman +0.18 | 2 heroes |
| Indomitable | 6,400 | +0.176 | +0.029 | +0.122 | Vyper +0.28, The Doorman +0.22, Deadman Danny +0.18 | 1 heroes |
| Spellbreaker | 6,400 | +0.176 | +0.028 | +0.137 | Deadman Danny +0.29, Lash +0.28, Grey Talon +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.046 | Grey Talon +0.10, Paige +0.09, Rem +0.08 | 0 heroes |
| Unstoppable | 6,400 | +0.011 | +0.002 | +0.136 | Paige +0.31, Wraith +0.24, Ivy +0.18 | 8 heroes |
| Healbane | 1,600 | +0.002 | +0.001 | +0.064 | Infernus +0.06, Grey Talon +0.05, Wraith +0.05 | 13 heroes |
| Plated Armor | 6,400 | +0.006 | +0.001 | +0.099 | Deadman Danny +0.18, Vindicta +0.16, Wraith +0.14 | 2 heroes |
| Reactive Barrier | 1,600 | -0.003 | -0.002 | +0.032 | Deadman Danny +0.11, Calico +0.10, Drifter +0.09 | 3 heroes |
| Bullet Resilience | 3,200 | -0.019 | -0.006 | +0.054 | Vindicta +0.14, Lash +0.13, Venator +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.024 | -0.007 | +0.033 | The Doorman +0.07, Wraith +0.04, Vindicta +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.112 | -0.035 | +0.096 | Lash +0.23, Venator +0.16, Wraith +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.153 | -0.096 | +0.045 | Paradox +0.08, Vindicta +0.05, Wraith +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.16 (+0.30), Dispel Magic +0.06 (+0.13), Indomitable +0.06 (+0.18)
- **Seven**: Witchmail +0.02 (+0.17), Counterspell -0.00 (+0.03), Reactive Barrier -0.02 (+0.01)
- **Vindicta**: Plated Armor +0.16 (+0.26), Bullet Resilience +0.14 (+0.19), Witchmail +0.12 (+0.26)
- **Lady Geist**: Bullet Resilience +0.05 (+0.10), Dispel Magic +0.04 (+0.11), Metal Skin +0.04 (+0.13)
- **Abrams**: Unstoppable +0.08 (+0.21), Indomitable +0.06 (+0.18), Spellbreaker +0.04 (+0.18)
- **Wraith**: Unstoppable +0.24 (+0.37), Indomitable +0.16 (+0.28), Metal Skin +0.15 (+0.24)
- **McGinnis**: Spirit Resilience +0.00 (+0.12), Healbane -0.01 (+0.05), Counterspell -0.02 (+0.01)
- **Paradox**: Unstoppable +0.12 (+0.26), Metal Skin +0.10 (+0.20), Dispel Magic +0.09 (+0.15)
- **Dynamo**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.14 (+0.26), Witchmail +0.05 (+0.19), Spellbreaker +0.03 (+0.17)
- **Haze**: Unstoppable +0.14 (+0.28), Indomitable +0.05 (+0.17), Return Fire +0.04 (+0.08)
- **Holliday**: Spellbreaker +0.04 (+0.17), Debuff Reducer +0.03 (+0.08), Return Fire +0.02 (+0.06)
- **Bebop**: Spellbreaker +0.11 (+0.25), Debuff Reducer +0.08 (+0.12), Indomitable +0.03 (+0.15)
- **Calico**: Spirit Resilience +0.15 (+0.27), Divine Barrier +0.12 (+0.17), Reactive Barrier +0.10 (+0.14)
- **Grey Talon**: Spellbreaker +0.14 (+0.27), Spirit Resilience +0.12 (+0.24), Debuff Reducer +0.10 (+0.15)
- **Mo & Krill**: Unstoppable +0.06 (+0.20), Spellbreaker +0.04 (+0.18), Dispel Magic +0.01 (+0.08)
- **Shiv**: Metal Skin +0.03 (+0.13), Divine Barrier +0.02 (+0.07), Bullet Resilience +0.02 (+0.08)
- **Ivy**: Unstoppable +0.18 (+0.32), Indomitable +0.14 (+0.27), Debuff Reducer +0.04 (+0.09)
- **Warden**: Metal Skin +0.04 (+0.14), Return Fire +0.04 (+0.09), Healbane +0.04 (+0.10)
- **Yamato**: Healbane +0.01 (+0.08), Reactive Barrier -0.00 (+0.03), Debuff Reducer -0.01 (+0.04)
- **Lash**: Spirit Resilience +0.34 (+0.47), Spellbreaker +0.28 (+0.41), Metal Skin +0.23 (+0.32)
- **Viscous**: Spirit Resilience +0.11 (+0.23), Divine Barrier +0.09 (+0.14), Witchmail +0.05 (+0.20)
- **Pocket**: Spirit Resilience +0.10 (+0.22), Witchmail +0.03 (+0.18), Spellbreaker +0.01 (+0.15)
- **Mirage**: Dispel Magic +0.32 (+0.39), Metal Skin +0.12 (+0.22), Plated Armor +0.06 (+0.16)
- **Vyper**: Indomitable +0.28 (+0.40), Plated Armor +0.08 (+0.18), Metal Skin +0.06 (+0.16)
- **Sinclair**: Indomitable +0.17 (+0.29), Spellbreaker +0.06 (+0.20), Reactive Barrier +0.05 (+0.09)
- **Mina**: Return Fire +0.01 (+0.06), Witchmail +0.00 (+0.15), Counterspell +0.00 (+0.04)
- **Drifter**: Dispel Magic +0.29 (+0.36), Reactive Barrier +0.09 (+0.12), Metal Skin +0.07 (+0.16)
- **Venator**: Metal Skin +0.16 (+0.26), Bullet Resilience +0.08 (+0.14), Plated Armor +0.03 (+0.13)
- **Victor**: Spellbreaker +0.09 (+0.23), Healbane +0.03 (+0.09), Spirit Resilience +0.02 (+0.14)
- **Paige**: Unstoppable +0.31 (+0.45), Debuff Reducer +0.09 (+0.13), Indomitable +0.01 (+0.14)
- **The Doorman**: Spirit Resilience +0.24 (+0.36), Indomitable +0.22 (+0.34), Witchmail +0.18 (+0.32)
- **Billy**: Reactive Barrier -0.01 (+0.02), Counterspell -0.01 (+0.02), Return Fire -0.02 (+0.03)
- **Graves**: Witchmail +0.06 (+0.20), Spirit Resilience +0.05 (+0.17), Return Fire +0.02 (+0.06)
- **Apollo**: Healbane -0.00 (+0.06), Return Fire -0.02 (+0.02), Reactive Barrier -0.03 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.31 (+0.43), Spellbreaker +0.29 (+0.43), Witchmail +0.21 (+0.35)
- **Rem**: Debuff Reducer +0.08 (+0.13), Spellbreaker +0.05 (+0.18), Divine Barrier -0.00 (+0.05)
- **Silver**: Dispel Magic +0.06 (+0.13), Debuff Reducer +0.01 (+0.06), Reactive Barrier +0.01 (+0.04)
- **Celeste**: Witchmail +0.07 (+0.21), Spirit Resilience +0.06 (+0.18), Dispel Magic +0.05 (+0.11)
- **Rat King**: Return Fire +0.01 (+0.05), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05)
- **Solomon**: Reactive Barrier +0.01 (+0.05), Counterspell +0.00 (+0.03), Return Fire +0.00 (+0.05)
- **Violet**: Witchmail +0.07 (+0.21), Return Fire +0.03 (+0.07), Spirit Resilience +0.03 (+0.15)
- **Nurse Harrow**: Dispel Magic +0.12 (+0.19), Spirit Resilience +0.10 (+0.22), Witchmail +0.05 (+0.19)
- **Baba**: Unstoppable +0.02 (+0.15), Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04)
