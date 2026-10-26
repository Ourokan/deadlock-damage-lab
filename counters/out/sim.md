# Counter items in the sim (phantom and up)

Built 2026-10-26T03:59:16Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.239 | +0.075 | +0.130 | Lash +0.26, Wraith +0.16, Deadman Danny +0.13 | 1 heroes |
| Divine Barrier | 6,400 | +0.373 | +0.060 | +0.099 | Wraith +0.18, Lash +0.17, Graves +0.12 | 0 heroes |
| Dispel Magic | 3,200 | +0.142 | +0.044 | +0.080 | Mirage +0.37, Silver +0.11, Infernus +0.09 | 4 heroes |
| Debuff Reducer | 1,600 | +0.066 | +0.041 | +0.058 | Wraith +0.10, Deadman Danny +0.06, Vyper +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.055 | +0.036 | +0.053 | Wraith +0.15, Deadman Danny +0.14, The Doorman +0.11 | 2 heroes |
| Witchmail | 6,400 | +0.223 | +0.035 | +0.190 | Deadman Danny +0.16, Wraith +0.16, Lash +0.13 | 0 heroes |
| Indomitable | 6,400 | +0.197 | +0.031 | +0.146 | Wraith +0.30, Vyper +0.29, Deadman Danny +0.19 | 0 heroes |
| Healbane | 1,600 | +0.042 | +0.026 | +0.087 | Billy +0.06, Mo & Krill +0.06, Nurse Harrow +0.05 | 11 heroes |
| Spellbreaker | 6,400 | +0.155 | +0.024 | +0.152 | Lash +0.24, Wraith +0.18, Deadman Danny +0.18 | 0 heroes |
| Bullet Resilience | 3,200 | +0.043 | +0.013 | +0.090 | Wraith +0.13, Deadman Danny +0.11, Paradox +0.11 | 0 heroes |
| Counterspell | 3,200 | +0.018 | +0.005 | +0.069 | Deadman Danny +0.08, Wraith +0.07, Billy +0.06 | 1 heroes |
| Plated Armor | 6,400 | +0.028 | +0.004 | +0.130 | Holliday +0.24, Wraith +0.18, Deadman Danny +0.15 | 0 heroes |
| Unstoppable | 6,400 | +0.005 | +0.001 | +0.119 | Deadman Danny +0.15, Wraith +0.14, Rem +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.090 | -0.028 | +0.113 | Wraith +0.25, Drifter +0.17, Lash +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.133 | -0.083 | +0.070 | Deadman Danny +0.08, The Doorman +0.08, Wraith +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.17), Unstoppable +0.06 (+0.18), Spirit Resilience +0.04 (+0.17)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.03 (+0.02)
- **Vindicta**: Witchmail +0.02 (+0.21), Counterspell +0.02 (+0.09), Return Fire +0.01 (+0.08)
- **Lady Geist**: Return Fire +0.04 (+0.11), Divine Barrier +0.01 (+0.11), Bullet Resilience +0.01 (+0.10)
- **Abrams**: Indomitable +0.17 (+0.31), Unstoppable +0.07 (+0.19), Divine Barrier +0.04 (+0.14)
- **Wraith**: Indomitable +0.30 (+0.45), Metal Skin +0.25 (+0.37), Spellbreaker +0.18 (+0.33)
- **McGinnis**: Spirit Resilience +0.03 (+0.16), Return Fire -0.02 (+0.05), Healbane -0.02 (+0.06)
- **Paradox**: Metal Skin +0.13 (+0.24), Bullet Resilience +0.11 (+0.20), Plated Armor +0.10 (+0.23)
- **Dynamo**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane +0.00 (+0.09), Counterspell -0.01 (+0.06), Debuff Reducer -0.01 (+0.04)
- **Haze**: Plated Armor +0.09 (+0.22), Indomitable +0.07 (+0.22), Unstoppable +0.05 (+0.17)
- **Holliday**: Plated Armor +0.24 (+0.37), Debuff Reducer +0.05 (+0.11), Return Fire +0.04 (+0.11)
- **Bebop**: Divine Barrier +0.03 (+0.13), Counterspell +0.03 (+0.10), Bullet Resilience +0.03 (+0.12)
- **Calico**: Spellbreaker +0.07 (+0.22), Divine Barrier +0.07 (+0.17), Counterspell +0.05 (+0.12)
- **Grey Talon**: Reactive Barrier +0.07 (+0.12), Indomitable +0.07 (+0.21), Spellbreaker +0.06 (+0.21)
- **Mo & Krill**: Spellbreaker +0.14 (+0.29), Spirit Resilience +0.08 (+0.21), Witchmail +0.07 (+0.26)
- **Shiv**: Healbane -0.01 (+0.07), Return Fire -0.02 (+0.05), Divine Barrier -0.03 (+0.07)
- **Ivy**: Unstoppable +0.10 (+0.22), Indomitable +0.05 (+0.20), Debuff Reducer +0.01 (+0.07)
- **Warden**: Return Fire +0.04 (+0.11), Bullet Resilience +0.01 (+0.10), Counterspell +0.01 (+0.08)
- **Yamato**: Healbane +0.02 (+0.10), Counterspell -0.04 (+0.03), Debuff Reducer -0.04 (+0.01)
- **Lash**: Spirit Resilience +0.26 (+0.39), Spellbreaker +0.24 (+0.39), Divine Barrier +0.17 (+0.27)
- **Viscous**: Counterspell -0.01 (+0.06), Divine Barrier -0.02 (+0.08), Return Fire -0.02 (+0.05)
- **Pocket**: Witchmail +0.03 (+0.22), Return Fire +0.03 (+0.10), Spirit Resilience +0.03 (+0.15)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spellbreaker +0.08 (+0.24), Spirit Resilience +0.06 (+0.19)
- **Vyper**: Indomitable +0.29 (+0.44), Debuff Reducer +0.06 (+0.11), Spellbreaker +0.04 (+0.19)
- **Sinclair**: Indomitable +0.06 (+0.20), Spellbreaker +0.04 (+0.19), Return Fire +0.03 (+0.10)
- **Mina**: Divine Barrier +0.08 (+0.18), Witchmail +0.07 (+0.26), Spirit Resilience +0.07 (+0.20)
- **Drifter**: Metal Skin +0.17 (+0.28), Spirit Resilience +0.13 (+0.26), Witchmail +0.10 (+0.29)
- **Venator**: Bullet Resilience +0.11 (+0.20), Metal Skin +0.04 (+0.15), Debuff Reducer +0.02 (+0.08)
- **Victor**: Healbane +0.00 (+0.09), Reactive Barrier -0.04 (+0.02), Counterspell -0.04 (+0.03)
- **Paige**: Healbane +0.00 (+0.09), Return Fire -0.01 (+0.06), Counterspell -0.01 (+0.05)
- **The Doorman**: Indomitable +0.17 (+0.32), Reactive Barrier +0.11 (+0.17), Witchmail +0.11 (+0.30)
- **Billy**: Healbane +0.06 (+0.15), Counterspell +0.06 (+0.13), Debuff Reducer +0.05 (+0.10)
- **Graves**: Spirit Resilience +0.13 (+0.26), Divine Barrier +0.12 (+0.22), Witchmail +0.12 (+0.31)
- **Apollo**: Healbane +0.04 (+0.13), Debuff Reducer +0.01 (+0.07), Counterspell +0.01 (+0.08)
- **Deadman Danny**: Indomitable +0.19 (+0.33), Spellbreaker +0.18 (+0.33), Witchmail +0.16 (+0.35)
- **Rem**: Unstoppable +0.10 (+0.22), Indomitable +0.08 (+0.23), Healbane -0.01 (+0.07)
- **Silver**: Dispel Magic +0.11 (+0.19), Metal Skin +0.04 (+0.15), Reactive Barrier +0.02 (+0.07)
- **Celeste**: Spirit Resilience +0.11 (+0.24), Witchmail +0.07 (+0.26), Plated Armor +0.05 (+0.18)
- **Rat King**: Counterspell +0.02 (+0.09), Return Fire +0.01 (+0.08), Bullet Resilience +0.01 (+0.10)
- **Solomon**: Return Fire -0.00 (+0.07), Counterspell -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **Violet**: Spirit Resilience -0.01 (+0.12), Dispel Magic -0.01 (+0.07), Spellbreaker -0.04 (+0.11)
- **Nurse Harrow**: Healbane +0.05 (+0.13), Counterspell -0.01 (+0.05), Dispel Magic -0.02 (+0.06)
- **Baba**: Healbane +0.01 (+0.10), Unstoppable -0.02 (+0.10), Counterspell -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.210 | +0.066 | +0.110 | Lash +0.27, Pocket +0.21, Graves +0.17 | 10 heroes |
| Dispel Magic | 3,200 | +0.121 | +0.038 | +0.061 | Mirage +0.31, Lash +0.13, Silver +0.13 | 7 heroes |
| Divine Barrier | 6,400 | +0.234 | +0.037 | +0.064 | Lash +0.18, Graves +0.12, Wraith +0.11 | 1 heroes |
| Witchmail | 6,400 | +0.205 | +0.032 | +0.156 | Lash +0.18, Graves +0.18, Pocket +0.11 | 0 heroes |
| Indomitable | 6,400 | +0.162 | +0.026 | +0.115 | Vyper +0.33, Wraith +0.20, Rem +0.13 | 0 heroes |
| Debuff Reducer | 1,600 | +0.037 | +0.023 | +0.043 | Wraith +0.08, Vyper +0.05, Lash +0.05 | 1 heroes |
| Reactive Barrier | 1,600 | +0.035 | +0.022 | +0.040 | Wraith +0.11, The Doorman +0.07, Paradox +0.07 | 4 heroes |
| Spellbreaker | 6,400 | +0.141 | +0.022 | +0.115 | Lash +0.22, Wraith +0.12, Pocket +0.12 | 0 heroes |
| Healbane | 1,600 | +0.013 | +0.008 | +0.074 | Lash +0.12, Haze +0.04, Bebop +0.04 | 17 heroes |
| Bullet Resilience | 3,200 | +0.015 | +0.005 | +0.067 | Paradox +0.13, Lash +0.13, Venator +0.10 | 0 heroes |
| Plated Armor | 6,400 | +0.018 | +0.003 | +0.103 | Haze +0.15, Holliday +0.14, Paradox +0.13 | 0 heroes |
| Counterspell | 3,200 | -0.007 | -0.002 | +0.044 | Lash +0.07, Deadman Danny +0.05, Bebop +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.024 | -0.004 | +0.096 | Abrams +0.17, Rem +0.14, Ivy +0.14 | 0 heroes |
| Metal Skin | 3,200 | -0.114 | -0.036 | +0.088 | Wraith +0.21, Paradox +0.17, Lash +0.17 | 0 heroes |
| Return Fire | 1,600 | -0.145 | -0.091 | +0.056 | Vindicta +0.07, Lash +0.07, Wraith +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.08 (+0.14), Unstoppable +0.03 (+0.13), Healbane +0.03 (+0.11)
- **Seven**: Witchmail +0.04 (+0.20), Counterspell +0.00 (+0.05), Healbane +0.00 (+0.08)
- **Vindicta**: Return Fire +0.07 (+0.13), Divine Barrier +0.05 (+0.12), Witchmail +0.05 (+0.20)
- **Lady Geist**: Return Fire +0.05 (+0.11), Divine Barrier +0.05 (+0.11), Metal Skin +0.02 (+0.11)
- **Abrams**: Unstoppable +0.17 (+0.27), Dispel Magic +0.06 (+0.12), Indomitable +0.06 (+0.17)
- **Wraith**: Metal Skin +0.21 (+0.29), Indomitable +0.20 (+0.32), Plated Armor +0.12 (+0.22)
- **McGinnis**: Healbane -0.00 (+0.07), Counterspell -0.01 (+0.04), Return Fire -0.02 (+0.04)
- **Paradox**: Metal Skin +0.17 (+0.26), Plated Armor +0.13 (+0.24), Bullet Resilience +0.13 (+0.20)
- **Dynamo**: Healbane +0.00 (+0.08), Counterspell -0.02 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.02 (+0.13), Dispel Magic +0.00 (+0.06), Healbane -0.00 (+0.07)
- **Haze**: Plated Armor +0.15 (+0.25), Indomitable +0.10 (+0.22), Bullet Resilience +0.09 (+0.16)
- **Holliday**: Plated Armor +0.14 (+0.25), Spellbreaker +0.03 (+0.15), Return Fire +0.03 (+0.09)
- **Bebop**: Witchmail +0.05 (+0.21), Counterspell +0.04 (+0.09), Divine Barrier +0.04 (+0.11)
- **Calico**: Reactive Barrier +0.03 (+0.07), Divine Barrier +0.01 (+0.07), Spirit Resilience -0.01 (+0.10)
- **Grey Talon**: Reactive Barrier +0.03 (+0.07), Spellbreaker +0.03 (+0.15), Debuff Reducer +0.03 (+0.07)
- **Mo & Krill**: Unstoppable +0.12 (+0.21), Spellbreaker +0.08 (+0.20), Dispel Magic +0.04 (+0.10)
- **Shiv**: Divine Barrier +0.03 (+0.09), Return Fire +0.02 (+0.07), Bullet Resilience +0.01 (+0.08)
- **Ivy**: Unstoppable +0.14 (+0.23), Indomitable +0.05 (+0.16), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.08), Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.06)
- **Yamato**: Healbane +0.03 (+0.10), Debuff Reducer -0.04 (+0.01), Reactive Barrier -0.04 (+0.00)
- **Lash**: Spirit Resilience +0.27 (+0.38), Spellbreaker +0.22 (+0.34), Witchmail +0.18 (+0.33)
- **Viscous**: Healbane +0.00 (+0.08), Return Fire -0.00 (+0.05), Counterspell -0.02 (+0.03)
- **Pocket**: Spirit Resilience +0.21 (+0.32), Spellbreaker +0.12 (+0.23), Witchmail +0.11 (+0.27)
- **Mirage**: Dispel Magic +0.31 (+0.37), Spellbreaker +0.03 (+0.15), Spirit Resilience +0.02 (+0.13)
- **Vyper**: Indomitable +0.33 (+0.45), Debuff Reducer +0.05 (+0.10), Metal Skin +0.05 (+0.14)
- **Sinclair**: Indomitable +0.10 (+0.22), Spellbreaker +0.04 (+0.15), Return Fire +0.01 (+0.06)
- **Mina**: Spirit Resilience +0.10 (+0.21), Witchmail +0.08 (+0.23), Divine Barrier +0.07 (+0.13)
- **Drifter**: Witchmail +0.08 (+0.23), Spirit Resilience +0.08 (+0.19), Metal Skin +0.07 (+0.16)
- **Venator**: Bullet Resilience +0.10 (+0.16), Metal Skin +0.05 (+0.13), Plated Armor +0.04 (+0.14)
- **Victor**: Spellbreaker +0.08 (+0.19), Spirit Resilience +0.05 (+0.16), Dispel Magic +0.01 (+0.07)
- **Paige**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.05), Witchmail -0.02 (+0.14)
- **The Doorman**: Indomitable +0.10 (+0.21), Spirit Resilience +0.09 (+0.20), Reactive Barrier +0.07 (+0.11)
- **Billy**: Spirit Resilience +0.04 (+0.15), Spellbreaker +0.03 (+0.14), Witchmail -0.00 (+0.15)
- **Graves**: Witchmail +0.18 (+0.33), Spirit Resilience +0.17 (+0.28), Metal Skin +0.14 (+0.23)
- **Apollo**: Reactive Barrier -0.00 (+0.04), Healbane -0.01 (+0.06), Debuff Reducer -0.02 (+0.02)
- **Deadman Danny**: Indomitable +0.11 (+0.23), Spellbreaker +0.10 (+0.22), Witchmail +0.10 (+0.25)
- **Rem**: Unstoppable +0.14 (+0.24), Indomitable +0.13 (+0.24), Counterspell -0.01 (+0.03)
- **Silver**: Dispel Magic +0.13 (+0.19), Metal Skin +0.01 (+0.10), Reactive Barrier +0.00 (+0.04)
- **Celeste**: Witchmail +0.03 (+0.18), Spirit Resilience +0.02 (+0.13), Spellbreaker -0.01 (+0.11)
- **Rat King**: Return Fire -0.01 (+0.05), Bullet Resilience -0.01 (+0.05), Counterspell -0.01 (+0.03)
- **Solomon**: Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Violet**: Unstoppable +0.01 (+0.11), Healbane -0.02 (+0.06), Reactive Barrier -0.03 (+0.01)
- **Nurse Harrow**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.03), Spirit Resilience -0.02 (+0.09)
- **Baba**: Return Fire +0.01 (+0.07), Healbane +0.01 (+0.08), Unstoppable +0.00 (+0.10)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.201 | +0.063 | +0.109 | Lash +0.18, Wraith +0.17, Grey Talon +0.16 | 13 heroes |
| Divine Barrier | 6,400 | +0.242 | +0.038 | +0.053 | Wraith +0.12, Paradox +0.12, Lash +0.09 | 2 heroes |
| Dispel Magic | 3,200 | +0.105 | +0.033 | +0.048 | Mirage +0.29, Infernus +0.12, Silver +0.11 | 9 heroes |
| Witchmail | 6,400 | +0.197 | +0.031 | +0.152 | Lash +0.13, Wraith +0.13, Paradox +0.10 | 1 heroes |
| Indomitable | 6,400 | +0.163 | +0.026 | +0.114 | Vyper +0.35, Wraith +0.28, Grey Talon +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.147 | +0.023 | +0.116 | Grey Talon +0.19, Wraith +0.15, Lash +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.027 | +0.017 | +0.036 | Grey Talon +0.11, Vyper +0.08, Wraith +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.018 | +0.011 | +0.031 | Wraith +0.13, Grey Talon +0.10, Paradox +0.09 | 5 heroes |
| Plated Armor | 6,400 | +0.016 | +0.002 | +0.100 | Holliday +0.18, Wraith +0.16, Paradox +0.10 | 0 heroes |
| Bullet Resilience | 3,200 | -0.009 | -0.003 | +0.055 | Paradox +0.12, Wraith +0.09, Venator +0.07 | 1 heroes |
| Healbane | 1,600 | -0.006 | -0.004 | +0.059 | Yamato +0.05, Infernus +0.05, Nurse Harrow +0.05 | 16 heroes |
| Unstoppable | 6,400 | -0.032 | -0.005 | +0.090 | Rem +0.23, Ivy +0.17, Grey Talon +0.17 | 3 heroes |
| Counterspell | 3,200 | -0.021 | -0.006 | +0.031 | Nurse Harrow +0.03, Lash +0.03, The Doorman +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.115 | -0.036 | +0.089 | Wraith +0.24, Paradox +0.14, Lash +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.148 | -0.093 | +0.049 | Paradox +0.08, Wraith +0.07, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.14 (+0.25), Unstoppable +0.13 (+0.22), Dispel Magic +0.12 (+0.17)
- **Seven**: Witchmail +0.06 (+0.21), Healbane +0.01 (+0.07), Counterspell +0.00 (+0.04)
- **Vindicta**: Return Fire +0.05 (+0.10), Bullet Resilience +0.05 (+0.10), Divine Barrier +0.03 (+0.08)
- **Lady Geist**: Divine Barrier +0.04 (+0.10), Bullet Resilience +0.04 (+0.09), Return Fire +0.03 (+0.08)
- **Abrams**: Unstoppable +0.11 (+0.20), Dispel Magic +0.05 (+0.10), Healbane +0.04 (+0.10)
- **Wraith**: Indomitable +0.28 (+0.39), Metal Skin +0.24 (+0.33), Spirit Resilience +0.17 (+0.28)
- **McGinnis**: Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05), Debuff Reducer -0.02 (+0.02)
- **Paradox**: Metal Skin +0.14 (+0.23), Spellbreaker +0.13 (+0.24), Bullet Resilience +0.12 (+0.18)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.00 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Counterspell +0.00 (+0.04), Dispel Magic -0.01 (+0.04), Healbane -0.01 (+0.05)
- **Haze**: Indomitable +0.10 (+0.21), Unstoppable +0.10 (+0.19), Plated Armor +0.09 (+0.19)
- **Holliday**: Plated Armor +0.18 (+0.28), Spellbreaker +0.06 (+0.18), Debuff Reducer +0.06 (+0.09)
- **Bebop**: Metal Skin +0.02 (+0.11), Healbane +0.02 (+0.08), Divine Barrier +0.00 (+0.06)
- **Calico**: Reactive Barrier +0.02 (+0.05), Divine Barrier +0.01 (+0.06), Spellbreaker +0.01 (+0.12)
- **Grey Talon**: Spellbreaker +0.19 (+0.31), Unstoppable +0.17 (+0.26), Indomitable +0.16 (+0.28)
- **Mo & Krill**: Unstoppable +0.12 (+0.21), Spellbreaker +0.06 (+0.18), Dispel Magic +0.04 (+0.08)
- **Shiv**: Metal Skin +0.05 (+0.14), Bullet Resilience +0.04 (+0.09), Divine Barrier +0.03 (+0.08)
- **Ivy**: Unstoppable +0.17 (+0.26), Indomitable +0.11 (+0.23), Dispel Magic +0.05 (+0.10)
- **Warden**: Return Fire +0.01 (+0.06), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Yamato**: Healbane +0.05 (+0.11), Debuff Reducer +0.01 (+0.05), Counterspell -0.00 (+0.03)
- **Lash**: Spirit Resilience +0.18 (+0.29), Spellbreaker +0.14 (+0.26), Witchmail +0.13 (+0.28)
- **Viscous**: Healbane +0.02 (+0.08), Divine Barrier +0.02 (+0.07), Return Fire +0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.08 (+0.19), Counterspell +0.02 (+0.05), Spellbreaker +0.01 (+0.13)
- **Mirage**: Dispel Magic +0.29 (+0.34), Spirit Resilience +0.03 (+0.14), Spellbreaker +0.02 (+0.14)
- **Vyper**: Indomitable +0.35 (+0.46), Debuff Reducer +0.08 (+0.11), Spellbreaker +0.06 (+0.17)
- **Sinclair**: Indomitable +0.16 (+0.27), Spellbreaker +0.02 (+0.13), Debuff Reducer +0.01 (+0.05)
- **Mina**: Spirit Resilience +0.12 (+0.23), Divine Barrier +0.09 (+0.14), Witchmail +0.08 (+0.23)
- **Drifter**: Spirit Resilience +0.09 (+0.20), Metal Skin +0.07 (+0.16), Witchmail +0.06 (+0.21)
- **Venator**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.07 (+0.16), Plated Armor +0.02 (+0.12)
- **Victor**: Spirit Resilience +0.02 (+0.13), Healbane +0.02 (+0.08), Spellbreaker +0.01 (+0.13)
- **Paige**: Counterspell +0.00 (+0.04), Return Fire -0.00 (+0.05), Witchmail -0.01 (+0.14)
- **The Doorman**: Spirit Resilience +0.10 (+0.21), Indomitable +0.10 (+0.21), Reactive Barrier +0.07 (+0.10)
- **Billy**: Reactive Barrier +0.02 (+0.05), Spellbreaker +0.01 (+0.13), Spirit Resilience -0.00 (+0.11)
- **Graves**: Metal Skin +0.03 (+0.12), Witchmail +0.03 (+0.18), Return Fire +0.02 (+0.07)
- **Apollo**: Healbane +0.01 (+0.07), Divine Barrier +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Deadman Danny**: Spellbreaker +0.10 (+0.21), Indomitable +0.09 (+0.21), Witchmail +0.08 (+0.24)
- **Rem**: Unstoppable +0.23 (+0.32), Debuff Reducer -0.00 (+0.03), Counterspell -0.01 (+0.02)
- **Silver**: Dispel Magic +0.11 (+0.16), Metal Skin +0.03 (+0.12), Reactive Barrier +0.01 (+0.04)
- **Celeste**: Witchmail +0.10 (+0.25), Dispel Magic +0.10 (+0.14), Spirit Resilience +0.08 (+0.19)
- **Rat King**: Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.04), Bullet Resilience -0.01 (+0.04)
- **Solomon**: Return Fire +0.02 (+0.06), Counterspell +0.00 (+0.03), Healbane -0.01 (+0.05)
- **Violet**: Unstoppable +0.04 (+0.13), Dispel Magic -0.01 (+0.04), Spirit Resilience -0.01 (+0.10)
- **Nurse Harrow**: Healbane +0.05 (+0.11), Counterspell +0.03 (+0.06), Spirit Resilience +0.00 (+0.11)
- **Baba**: Return Fire +0.02 (+0.07), Healbane +0.00 (+0.06), Counterspell -0.00 (+0.03)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.239 | +0.075 | +0.130 | Lash +0.37, Deadman Danny +0.36, The Doorman +0.25 | 14 heroes |
| Dispel Magic | 3,200 | +0.128 | +0.040 | +0.073 | Mirage +0.34, Drifter +0.29, Lash +0.20 | 9 heroes |
| Divine Barrier | 6,400 | +0.202 | +0.032 | +0.052 | Lash +0.20, Calico +0.13, The Doorman +0.11 | 3 heroes |
| Witchmail | 6,400 | +0.189 | +0.030 | +0.146 | Deadman Danny +0.22, Lash +0.22, The Doorman +0.15 | 2 heroes |
| Indomitable | 6,400 | +0.180 | +0.029 | +0.126 | Vyper +0.28, The Doorman +0.22, Deadman Danny +0.18 | 1 heroes |
| Spellbreaker | 6,400 | +0.180 | +0.028 | +0.141 | Deadman Danny +0.31, Lash +0.28, Grey Talon +0.17 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.046 | Grey Talon +0.13, Paige +0.09, Bebop +0.07 | 0 heroes |
| Unstoppable | 6,400 | +0.019 | +0.003 | +0.146 | Paige +0.32, Wraith +0.25, Ivy +0.17 | 8 heroes |
| Plated Armor | 6,400 | +0.009 | +0.001 | +0.101 | Deadman Danny +0.21, Wraith +0.14, Lash +0.10 | 2 heroes |
| Reactive Barrier | 1,600 | -0.001 | -0.001 | +0.034 | Deadman Danny +0.13, Calico +0.10, Drifter +0.08 | 3 heroes |
| Healbane | 1,600 | -0.002 | -0.001 | +0.059 | Yamato +0.05, Vindicta +0.05, Infernus +0.05 | 13 heroes |
| Bullet Resilience | 3,200 | -0.017 | -0.005 | +0.057 | Vindicta +0.12, Lash +0.10, Venator +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.023 | -0.007 | +0.034 | The Doorman +0.07, Wraith +0.05, Grey Talon +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.110 | -0.034 | +0.098 | Lash +0.24, Venator +0.16, Wraith +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.155 | -0.097 | +0.043 | Paradox +0.07, Vindicta +0.05, Holliday +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.29), Dispel Magic +0.06 (+0.13), Indomitable +0.05 (+0.17)
- **Seven**: Witchmail +0.03 (+0.17), Counterspell +0.00 (+0.03), Healbane -0.01 (+0.04)
- **Vindicta**: Witchmail +0.13 (+0.27), Bullet Resilience +0.12 (+0.17), Plated Armor +0.09 (+0.20)
- **Lady Geist**: Bullet Resilience +0.06 (+0.12), Metal Skin +0.04 (+0.14), Dispel Magic +0.04 (+0.11)
- **Abrams**: Unstoppable +0.08 (+0.23), Healbane +0.04 (+0.10), Indomitable +0.02 (+0.15)
- **Wraith**: Unstoppable +0.25 (+0.40), Metal Skin +0.16 (+0.26), Indomitable +0.15 (+0.27)
- **McGinnis**: Healbane -0.01 (+0.05), Spirit Resilience -0.01 (+0.12), Counterspell -0.02 (+0.02)
- **Paradox**: Dispel Magic +0.15 (+0.22), Unstoppable +0.15 (+0.30), Metal Skin +0.11 (+0.21)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.13 (+0.26), Witchmail +0.06 (+0.21), Spellbreaker +0.04 (+0.18)
- **Haze**: Unstoppable +0.14 (+0.28), Indomitable +0.05 (+0.17), Return Fire +0.04 (+0.08)
- **Holliday**: Spellbreaker +0.06 (+0.20), Debuff Reducer +0.06 (+0.10), Return Fire +0.04 (+0.08)
- **Bebop**: Debuff Reducer +0.07 (+0.12), Spellbreaker +0.07 (+0.21), Indomitable +0.04 (+0.16)
- **Calico**: Spirit Resilience +0.13 (+0.26), Divine Barrier +0.13 (+0.18), Reactive Barrier +0.10 (+0.13)
- **Grey Talon**: Spellbreaker +0.17 (+0.31), Spirit Resilience +0.15 (+0.28), Debuff Reducer +0.13 (+0.18)
- **Mo & Krill**: Unstoppable +0.05 (+0.19), Spellbreaker +0.02 (+0.16), Debuff Reducer +0.01 (+0.05)
- **Shiv**: Metal Skin +0.05 (+0.15), Bullet Resilience +0.05 (+0.11), Divine Barrier +0.04 (+0.10)
- **Ivy**: Unstoppable +0.17 (+0.32), Indomitable +0.12 (+0.25), Debuff Reducer +0.05 (+0.09)
- **Warden**: Return Fire +0.03 (+0.07), Metal Skin +0.02 (+0.12), Healbane +0.01 (+0.07)
- **Yamato**: Healbane +0.05 (+0.11), Indomitable +0.01 (+0.14), Reactive Barrier +0.01 (+0.05)
- **Lash**: Spirit Resilience +0.37 (+0.50), Spellbreaker +0.28 (+0.42), Metal Skin +0.24 (+0.34)
- **Viscous**: Witchmail +0.10 (+0.24), Spirit Resilience +0.09 (+0.22), Divine Barrier +0.08 (+0.13)
- **Pocket**: Spirit Resilience +0.08 (+0.21), Witchmail +0.05 (+0.20), Spellbreaker +0.02 (+0.16)
- **Mirage**: Dispel Magic +0.34 (+0.41), Metal Skin +0.11 (+0.21), Plated Armor +0.04 (+0.15)
- **Vyper**: Indomitable +0.28 (+0.41), Plated Armor +0.09 (+0.19), Metal Skin +0.08 (+0.18)
- **Sinclair**: Indomitable +0.16 (+0.28), Reactive Barrier +0.06 (+0.09), Spirit Resilience +0.05 (+0.18)
- **Mina**: Counterspell +0.01 (+0.04), Divine Barrier +0.01 (+0.06), Return Fire +0.00 (+0.05)
- **Drifter**: Dispel Magic +0.29 (+0.36), Reactive Barrier +0.08 (+0.12), Witchmail +0.07 (+0.22)
- **Venator**: Metal Skin +0.16 (+0.26), Bullet Resilience +0.08 (+0.14), Plated Armor +0.03 (+0.13)
- **Victor**: Spellbreaker +0.07 (+0.21), Healbane +0.02 (+0.08), Spirit Resilience +0.01 (+0.14)
- **Paige**: Unstoppable +0.32 (+0.47), Debuff Reducer +0.09 (+0.13), Indomitable +0.02 (+0.14)
- **The Doorman**: Spirit Resilience +0.25 (+0.38), Indomitable +0.22 (+0.35), Witchmail +0.15 (+0.30)
- **Billy**: Spellbreaker +0.00 (+0.14), Reactive Barrier -0.00 (+0.03), Return Fire -0.01 (+0.03)
- **Graves**: Spirit Resilience +0.06 (+0.19), Witchmail +0.04 (+0.19), Return Fire +0.02 (+0.07)
- **Apollo**: Reactive Barrier +0.03 (+0.07), Healbane +0.01 (+0.07), Divine Barrier -0.00 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.36 (+0.49), Spellbreaker +0.31 (+0.45), Witchmail +0.22 (+0.37)
- **Rem**: Unstoppable +0.16 (+0.31), Counterspell -0.01 (+0.02), Return Fire -0.01 (+0.03)
- **Silver**: Dispel Magic +0.04 (+0.11), Debuff Reducer +0.00 (+0.05), Metal Skin -0.00 (+0.10)
- **Celeste**: Spirit Resilience +0.05 (+0.18), Witchmail +0.04 (+0.19), Dispel Magic +0.02 (+0.10)
- **Rat King**: Return Fire +0.02 (+0.06), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05)
- **Solomon**: Return Fire +0.01 (+0.06), Reactive Barrier +0.01 (+0.04), Counterspell +0.01 (+0.04)
- **Violet**: Spirit Resilience +0.01 (+0.14), Healbane +0.01 (+0.07), Dispel Magic -0.01 (+0.06)
- **Nurse Harrow**: Dispel Magic +0.10 (+0.17), Spirit Resilience +0.09 (+0.22), Witchmail +0.05 (+0.19)
- **Baba**: Unstoppable +0.03 (+0.17), Healbane +0.02 (+0.07), Witchmail +0.00 (+0.15)
