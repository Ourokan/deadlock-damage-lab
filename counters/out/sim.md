# Counter items in the sim (phantom and up)

Built 2026-11-07T19:41:23Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.197 | +0.061 | +0.133 | Lash +0.30, Deadman Danny +0.18, The Doorman +0.18 | 1 heroes |
| Divine Barrier | 6,400 | +0.287 | +0.046 | +0.137 | Lash +0.24, The Doorman +0.16, Abrams +0.12 | 0 heroes |
| Dispel Magic | 3,200 | +0.089 | +0.028 | +0.085 | Mirage +0.38, Lash +0.19, Deadman Danny +0.10 | 4 heroes |
| Indomitable | 6,400 | +0.173 | +0.027 | +0.157 | Vyper +0.31, The Doorman +0.25, Deadman Danny +0.21 | 0 heroes |
| Healbane | 1,600 | +0.043 | +0.026 | +0.092 | Graves +0.12, Lash +0.11, Yamato +0.08 | 22 heroes |
| Reactive Barrier | 1,600 | +0.034 | +0.021 | +0.053 | Deadman Danny +0.14, Graves +0.11, The Doorman +0.10 | 2 heroes |
| Witchmail | 6,400 | +0.099 | +0.015 | +0.207 | Lash +0.26, Deadman Danny +0.20, The Doorman +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.024 | +0.015 | +0.081 | Holliday +0.12, Lash +0.11, Venator +0.10 | 0 heroes |
| Bullet Resilience | 3,200 | +0.045 | +0.014 | +0.107 | Venator +0.23, Lash +0.22, Deadman Danny +0.12 | 0 heroes |
| Spellbreaker | 6,400 | +0.079 | +0.012 | +0.176 | Lash +0.29, Deadman Danny +0.22, The Doorman +0.15 | 0 heroes |
| Plated Armor | 6,400 | +0.009 | +0.001 | +0.142 | Holliday +0.21, Lash +0.18, Deadman Danny +0.12 | 0 heroes |
| Counterspell | 3,200 | -0.006 | -0.002 | +0.075 | Lash +0.12, Graves +0.09, Deadman Danny +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.056 | -0.009 | +0.142 | Lash +0.16, Deadman Danny +0.15, Holliday +0.11 | 0 heroes |
| Metal Skin | 3,200 | -0.183 | -0.057 | +0.113 | Lash +0.22, Wraith +0.14, Paradox +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.187 | -0.117 | +0.086 | Paradox +0.09, Lash +0.08, Deadman Danny +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.07 (+0.15), Spellbreaker +0.05 (+0.22), Unstoppable +0.04 (+0.18)
- **Seven**: Healbane -0.00 (+0.09), Spirit Resilience -0.01 (+0.12), Witchmail -0.02 (+0.19)
- **Vindicta**: Divine Barrier +0.00 (+0.14), Counterspell +0.00 (+0.08), Return Fire -0.00 (+0.08)
- **Lady Geist**: Return Fire +0.02 (+0.11), Healbane -0.01 (+0.09), Divine Barrier -0.01 (+0.13)
- **Abrams**: Indomitable +0.19 (+0.35), Divine Barrier +0.12 (+0.25), Witchmail +0.08 (+0.29)
- **Wraith**: Indomitable +0.16 (+0.31), Metal Skin +0.14 (+0.25), Spellbreaker +0.10 (+0.28)
- **McGinnis**: Counterspell +0.03 (+0.10), Healbane +0.02 (+0.11), Dispel Magic +0.02 (+0.10)
- **Paradox**: Metal Skin +0.13 (+0.24), Bullet Resilience +0.10 (+0.21), Return Fire +0.09 (+0.18)
- **Dynamo**: Healbane -0.00 (+0.09), Counterspell -0.03 (+0.05), Reactive Barrier -0.04 (+0.01)
- **Kelvin**: Healbane -0.00 (+0.09), Counterspell -0.01 (+0.07), Dispel Magic -0.01 (+0.07)
- **Haze**: Indomitable +0.11 (+0.27), Plated Armor +0.10 (+0.24), Unstoppable +0.07 (+0.22)
- **Holliday**: Plated Armor +0.21 (+0.35), Spellbreaker +0.14 (+0.32), Debuff Reducer +0.12 (+0.20)
- **Bebop**: Healbane +0.00 (+0.10), Counterspell +0.00 (+0.08), Divine Barrier -0.01 (+0.13)
- **Calico**: Spellbreaker +0.08 (+0.26), Divine Barrier +0.07 (+0.20), Spirit Resilience +0.05 (+0.18)
- **Grey Talon**: Unstoppable +0.06 (+0.20), Reactive Barrier +0.05 (+0.11), Debuff Reducer +0.05 (+0.13)
- **Mo & Krill**: Spellbreaker +0.10 (+0.27), Spirit Resilience +0.04 (+0.18), Healbane +0.04 (+0.13)
- **Shiv**: Return Fire -0.00 (+0.08), Healbane -0.02 (+0.08), Divine Barrier -0.02 (+0.11)
- **Ivy**: Indomitable +0.05 (+0.21), Unstoppable +0.03 (+0.17), Bullet Resilience +0.01 (+0.11)
- **Warden**: Return Fire -0.00 (+0.08), Debuff Reducer -0.00 (+0.08), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.08 (+0.18), Spellbreaker +0.04 (+0.22), Debuff Reducer +0.04 (+0.12)
- **Lash**: Spirit Resilience +0.30 (+0.43), Spellbreaker +0.29 (+0.47), Witchmail +0.26 (+0.46)
- **Viscous**: Divine Barrier -0.01 (+0.12), Return Fire -0.03 (+0.06), Healbane -0.03 (+0.06)
- **Pocket**: Witchmail +0.12 (+0.33), Spirit Resilience +0.10 (+0.23), Spellbreaker +0.06 (+0.24)
- **Mirage**: Dispel Magic +0.38 (+0.46), Spellbreaker +0.07 (+0.24), Spirit Resilience +0.06 (+0.19)
- **Vyper**: Indomitable +0.31 (+0.47), Debuff Reducer +0.10 (+0.18), Spellbreaker +0.09 (+0.27)
- **Sinclair**: Indomitable +0.12 (+0.28), Spellbreaker +0.06 (+0.24), Unstoppable +0.04 (+0.19)
- **Mina**: Return Fire +0.01 (+0.09), Spirit Resilience -0.01 (+0.13), Counterspell -0.01 (+0.06)
- **Drifter**: Return Fire -0.02 (+0.07), Counterspell -0.02 (+0.06), Healbane -0.03 (+0.07)
- **Venator**: Bullet Resilience +0.23 (+0.34), Plated Armor +0.10 (+0.24), Debuff Reducer +0.10 (+0.18)
- **Victor**: Spirit Resilience +0.13 (+0.26), Spellbreaker +0.12 (+0.29), Witchmail +0.02 (+0.23)
- **Paige**: Return Fire -0.02 (+0.07), Counterspell -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **The Doorman**: Indomitable +0.25 (+0.41), Spirit Resilience +0.18 (+0.31), Divine Barrier +0.16 (+0.30)
- **Billy**: Healbane +0.06 (+0.16), Spirit Resilience +0.04 (+0.18), Spellbreaker +0.04 (+0.21)
- **Graves**: Healbane +0.12 (+0.22), Reactive Barrier +0.11 (+0.17), Metal Skin +0.11 (+0.22)
- **Apollo**: Reactive Barrier +0.01 (+0.06), Counterspell -0.03 (+0.05), Healbane -0.04 (+0.05)
- **Deadman Danny**: Spellbreaker +0.22 (+0.40), Indomitable +0.21 (+0.36), Witchmail +0.20 (+0.41)
- **Rem**: Reactive Barrier -0.01 (+0.04), Dispel Magic -0.02 (+0.06), Healbane -0.03 (+0.07)
- **Silver**: Dispel Magic +0.08 (+0.16), Indomitable +0.04 (+0.20), Reactive Barrier +0.01 (+0.06)
- **Celeste**: Spirit Resilience +0.11 (+0.25), Witchmail +0.09 (+0.30), Spellbreaker +0.03 (+0.21)
- **Rat King**: Return Fire +0.00 (+0.09), Counterspell -0.01 (+0.06), Bullet Resilience -0.02 (+0.09)
- **Solomon**: Counterspell -0.02 (+0.05), Reactive Barrier -0.03 (+0.03), Return Fire -0.04 (+0.05)
- **Violet**: Unstoppable +0.06 (+0.20), Return Fire +0.03 (+0.12), Witchmail +0.03 (+0.23)
- **Nurse Harrow**: Counterspell -0.05 (+0.02), Healbane -0.05 (+0.04), Dispel Magic -0.08 (+0.01)
- **Baba**: Healbane -0.02 (+0.07), Reactive Barrier -0.02 (+0.03), Counterspell -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.140 | Lash +0.44, Celeste +0.19, Pocket +0.18 | 10 heroes |
| Divine Barrier | 6,400 | +0.213 | +0.034 | +0.104 | Lash +0.28, The Doorman +0.12, Venator +0.09 | 0 heroes |
| Indomitable | 6,400 | +0.166 | +0.026 | +0.129 | Vyper +0.41, Wraith +0.21, The Doorman +0.17 | 0 heroes |
| Dispel Magic | 3,200 | +0.076 | +0.024 | +0.061 | Mirage +0.31, Abrams +0.10, Silver +0.09 | 9 heroes |
| Spellbreaker | 6,400 | +0.122 | +0.019 | +0.163 | Lash +0.40, Holliday +0.17, Wraith +0.12 | 0 heroes |
| Healbane | 1,600 | +0.029 | +0.018 | +0.067 | Yamato +0.11, Lady Geist +0.08, Infernus +0.05 | 23 heroes |
| Witchmail | 6,400 | +0.114 | +0.018 | +0.183 | Lash +0.28, Celeste +0.17, Wraith +0.12 | 1 heroes |
| Reactive Barrier | 1,600 | +0.018 | +0.011 | +0.037 | The Doorman +0.14, Calico +0.09, Abrams +0.07 | 3 heroes |
| Bullet Resilience | 3,200 | +0.020 | +0.006 | +0.076 | Venator +0.21, Lash +0.11, Paradox +0.10 | 0 heroes |
| Debuff Reducer | 1,600 | +0.005 | +0.003 | +0.068 | Holliday +0.16, Rem +0.12, Vyper +0.10 | 0 heroes |
| Plated Armor | 6,400 | +0.017 | +0.003 | +0.106 | Holliday +0.21, Wraith +0.16, Venator +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.021 | -0.006 | +0.045 | Paradox +0.05, Lash +0.05, Yamato +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.078 | -0.012 | +0.112 | Holliday +0.14, Abrams +0.12, Rem +0.11 | 0 heroes |
| Metal Skin | 3,200 | -0.198 | -0.062 | +0.092 | Wraith +0.27, Lash +0.17, Venator +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.196 | -0.123 | +0.059 | Paradox +0.08, The Doorman +0.08, Lash +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.07 (+0.14), Spellbreaker +0.07 (+0.23), Unstoppable +0.06 (+0.17)
- **Seven**: Witchmail +0.06 (+0.25), Healbane +0.02 (+0.08), Spirit Resilience -0.00 (+0.14)
- **Vindicta**: Return Fire +0.05 (+0.11), Divine Barrier +0.05 (+0.15), Witchmail +0.03 (+0.21)
- **Lady Geist**: Spirit Resilience +0.13 (+0.27), Spellbreaker +0.09 (+0.25), Healbane +0.08 (+0.14)
- **Abrams**: Indomitable +0.13 (+0.26), Unstoppable +0.12 (+0.23), Dispel Magic +0.10 (+0.16)
- **Wraith**: Metal Skin +0.27 (+0.37), Indomitable +0.21 (+0.34), Plated Armor +0.16 (+0.26)
- **McGinnis**: Spirit Resilience +0.07 (+0.20), Healbane -0.01 (+0.06), Dispel Magic -0.02 (+0.05)
- **Paradox**: Bullet Resilience +0.10 (+0.17), Metal Skin +0.08 (+0.17), Return Fire +0.08 (+0.14)
- **Dynamo**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Dispel Magic +0.04 (+0.10), Spirit Resilience +0.03 (+0.17), Healbane -0.01 (+0.06)
- **Haze**: Indomitable +0.08 (+0.21), Plated Armor +0.07 (+0.18), Bullet Resilience +0.05 (+0.12)
- **Holliday**: Plated Armor +0.21 (+0.32), Spellbreaker +0.17 (+0.33), Debuff Reducer +0.16 (+0.23)
- **Bebop**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03), Bullet Resilience -0.02 (+0.05)
- **Calico**: Reactive Barrier +0.09 (+0.13), Divine Barrier +0.04 (+0.14), Dispel Magic +0.03 (+0.09)
- **Grey Talon**: Unstoppable +0.09 (+0.20), Debuff Reducer +0.05 (+0.12), Spellbreaker +0.03 (+0.20)
- **Mo & Krill**: Spellbreaker +0.11 (+0.27), Unstoppable +0.08 (+0.19), Dispel Magic +0.06 (+0.12)
- **Shiv**: Bullet Resilience +0.05 (+0.13), Plated Armor +0.02 (+0.13), Divine Barrier +0.01 (+0.12)
- **Ivy**: Unstoppable +0.09 (+0.21), Debuff Reducer +0.04 (+0.11), Indomitable +0.00 (+0.13)
- **Warden**: Return Fire +0.04 (+0.10), Divine Barrier +0.02 (+0.12), Unstoppable +0.01 (+0.13)
- **Yamato**: Healbane +0.11 (+0.18), Debuff Reducer +0.07 (+0.13), Counterspell +0.04 (+0.09)
- **Lash**: Spirit Resilience +0.44 (+0.58), Spellbreaker +0.40 (+0.56), Witchmail +0.28 (+0.46)
- **Viscous**: Divine Barrier +0.02 (+0.12), Counterspell +0.01 (+0.06), Healbane -0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.18 (+0.32), Witchmail +0.07 (+0.25), Spellbreaker +0.05 (+0.21)
- **Mirage**: Dispel Magic +0.31 (+0.37), Spirit Resilience +0.06 (+0.20), Spellbreaker +0.05 (+0.21)
- **Vyper**: Indomitable +0.41 (+0.54), Spellbreaker +0.11 (+0.27), Debuff Reducer +0.10 (+0.17)
- **Sinclair**: Indomitable +0.11 (+0.24), Reactive Barrier +0.00 (+0.04), Spellbreaker +0.00 (+0.16)
- **Mina**: Counterspell +0.01 (+0.05), Return Fire +0.01 (+0.06), Divine Barrier -0.00 (+0.10)
- **Drifter**: Healbane +0.01 (+0.08), Counterspell -0.00 (+0.04), Return Fire -0.02 (+0.04)
- **Venator**: Bullet Resilience +0.21 (+0.29), Metal Skin +0.12 (+0.21), Plated Armor +0.09 (+0.20)
- **Victor**: Spirit Resilience +0.05 (+0.19), Spellbreaker +0.05 (+0.21), Healbane +0.00 (+0.07)
- **Paige**: Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.05), Healbane -0.02 (+0.04)
- **The Doorman**: Indomitable +0.17 (+0.30), Reactive Barrier +0.14 (+0.18), Divine Barrier +0.12 (+0.22)
- **Billy**: Healbane +0.00 (+0.07), Counterspell -0.00 (+0.04), Dispel Magic -0.01 (+0.05)
- **Graves**: Metal Skin +0.06 (+0.16), Reactive Barrier +0.05 (+0.09), Witchmail +0.04 (+0.23)
- **Apollo**: Reactive Barrier +0.05 (+0.09), Indomitable +0.01 (+0.14), Unstoppable +0.00 (+0.12)
- **Deadman Danny**: Indomitable +0.10 (+0.23), Spirit Resilience +0.08 (+0.22), Witchmail +0.06 (+0.25)
- **Rem**: Debuff Reducer +0.12 (+0.18), Unstoppable +0.11 (+0.23), Spellbreaker +0.03 (+0.20)
- **Silver**: Dispel Magic +0.09 (+0.15), Indomitable +0.03 (+0.16), Reactive Barrier +0.03 (+0.06)
- **Celeste**: Spirit Resilience +0.19 (+0.33), Witchmail +0.17 (+0.35), Spellbreaker +0.08 (+0.24)
- **Rat King**: Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Solomon**: Reactive Barrier -0.01 (+0.02), Counterspell -0.02 (+0.03), Return Fire -0.02 (+0.04)
- **Violet**: Unstoppable +0.06 (+0.17), Witchmail +0.04 (+0.23), Healbane +0.04 (+0.11)
- **Nurse Harrow**: Healbane +0.03 (+0.10), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Baba**: Unstoppable +0.02 (+0.13), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.182 | +0.057 | +0.139 | Lash +0.39, Wraith +0.17, Deadman Danny +0.16 | 13 heroes |
| Divine Barrier | 6,400 | +0.205 | +0.032 | +0.091 | Lash +0.12, Paradox +0.10, Viscous +0.09 | 2 heroes |
| Indomitable | 6,400 | +0.164 | +0.026 | +0.128 | Vyper +0.39, Wraith +0.24, Deadman Danny +0.18 | 0 heroes |
| Dispel Magic | 3,200 | +0.079 | +0.025 | +0.056 | Mirage +0.23, Lash +0.16, Paradox +0.12 | 11 heroes |
| Spellbreaker | 6,400 | +0.133 | +0.021 | +0.162 | Lash +0.35, Holliday +0.18, Wraith +0.17 | 0 heroes |
| Healbane | 1,600 | +0.027 | +0.017 | +0.063 | Infernus +0.06, Mo & Krill +0.06, Nurse Harrow +0.05 | 25 heroes |
| Witchmail | 6,400 | +0.098 | +0.015 | +0.167 | Lash +0.15, Wraith +0.15, Deadman Danny +0.13 | 1 heroes |
| Bullet Resilience | 3,200 | +0.014 | +0.004 | +0.060 | Venator +0.15, Vindicta +0.10, Deadman Danny +0.08 | 1 heroes |
| Debuff Reducer | 1,600 | +0.004 | +0.003 | +0.066 | Holliday +0.18, Grey Talon +0.13, Wraith +0.11 | 0 heroes |
| Plated Armor | 6,400 | +0.015 | +0.002 | +0.094 | Holliday +0.20, Wraith +0.13, Deadman Danny +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | -0.008 | -0.005 | +0.033 | Deadman Danny +0.11, Wraith +0.10, Paradox +0.10 | 2 heroes |
| Counterspell | 3,200 | -0.026 | -0.008 | +0.035 | Deadman Danny +0.05, Paradox +0.03, Wraith +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.075 | -0.012 | +0.113 | Mo & Krill +0.24, Holliday +0.15, Grey Talon +0.14 | 3 heroes |
| Metal Skin | 3,200 | -0.198 | -0.062 | +0.084 | Wraith +0.21, Lash +0.13, Paradox +0.09 | 0 heroes |
| Return Fire | 1,600 | -0.190 | -0.119 | +0.055 | Paradox +0.07, Venator +0.06, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.17), Spellbreaker +0.11 (+0.27), Unstoppable +0.06 (+0.18)
- **Seven**: Witchmail +0.08 (+0.25), Spirit Resilience +0.06 (+0.20), Indomitable +0.04 (+0.17)
- **Vindicta**: Bullet Resilience +0.10 (+0.16), Plated Armor +0.07 (+0.16), Divine Barrier +0.06 (+0.15)
- **Lady Geist**: Healbane +0.03 (+0.09), Witchmail +0.02 (+0.18), Divine Barrier +0.02 (+0.11)
- **Abrams**: Unstoppable +0.07 (+0.19), Dispel Magic +0.06 (+0.12), Reactive Barrier +0.02 (+0.05)
- **Wraith**: Indomitable +0.24 (+0.37), Metal Skin +0.21 (+0.29), Spellbreaker +0.17 (+0.34)
- **McGinnis**: Spirit Resilience +0.06 (+0.20), Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05)
- **Paradox**: Spirit Resilience +0.13 (+0.27), Dispel Magic +0.12 (+0.18), Reactive Barrier +0.10 (+0.13)
- **Dynamo**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.04 (-0.00)
- **Kelvin**: Dispel Magic -0.00 (+0.05), Spirit Resilience -0.01 (+0.13), Counterspell -0.02 (+0.02)
- **Haze**: Indomitable +0.13 (+0.25), Unstoppable +0.11 (+0.22), Bullet Resilience +0.05 (+0.11)
- **Holliday**: Plated Armor +0.20 (+0.29), Debuff Reducer +0.18 (+0.24), Spellbreaker +0.18 (+0.34)
- **Bebop**: Healbane +0.02 (+0.09), Counterspell -0.01 (+0.02), Return Fire -0.01 (+0.04)
- **Calico**: Spirit Resilience +0.08 (+0.22), Divine Barrier +0.07 (+0.16), Indomitable +0.06 (+0.19)
- **Grey Talon**: Unstoppable +0.14 (+0.26), Spellbreaker +0.13 (+0.30), Debuff Reducer +0.13 (+0.19)
- **Mo & Krill**: Unstoppable +0.24 (+0.35), Spellbreaker +0.13 (+0.29), Spirit Resilience +0.09 (+0.23)
- **Shiv**: Bullet Resilience +0.05 (+0.11), Divine Barrier +0.03 (+0.12), Plated Armor +0.02 (+0.11)
- **Ivy**: Unstoppable +0.01 (+0.12), Healbane -0.00 (+0.06), Indomitable -0.00 (+0.13)
- **Warden**: Return Fire +0.00 (+0.06), Debuff Reducer +0.00 (+0.07), Counterspell -0.01 (+0.02)
- **Yamato**: Healbane +0.04 (+0.11), Debuff Reducer +0.02 (+0.09), Witchmail +0.02 (+0.19)
- **Lash**: Spirit Resilience +0.39 (+0.53), Spellbreaker +0.35 (+0.51), Dispel Magic +0.16 (+0.21)
- **Viscous**: Spirit Resilience +0.13 (+0.27), Divine Barrier +0.09 (+0.18), Spellbreaker +0.09 (+0.25)
- **Pocket**: Spirit Resilience +0.10 (+0.24), Witchmail +0.06 (+0.22), Counterspell +0.00 (+0.04)
- **Mirage**: Dispel Magic +0.23 (+0.29), Debuff Reducer +0.01 (+0.08), Metal Skin +0.01 (+0.10)
- **Vyper**: Indomitable +0.39 (+0.51), Spellbreaker +0.10 (+0.26), Debuff Reducer +0.09 (+0.16)
- **Sinclair**: Indomitable +0.14 (+0.27), Unstoppable +0.09 (+0.20), Debuff Reducer +0.03 (+0.10)
- **Mina**: Divine Barrier +0.07 (+0.16), Spirit Resilience +0.05 (+0.19), Witchmail +0.04 (+0.20)
- **Drifter**: Witchmail +0.02 (+0.19), Healbane +0.02 (+0.08), Counterspell +0.01 (+0.05)
- **Venator**: Bullet Resilience +0.15 (+0.21), Plated Armor +0.10 (+0.19), Metal Skin +0.07 (+0.16)
- **Victor**: Spellbreaker +0.06 (+0.22), Spirit Resilience +0.02 (+0.16), Healbane -0.01 (+0.06)
- **Paige**: Counterspell +0.01 (+0.04), Divine Barrier -0.01 (+0.08), Return Fire -0.01 (+0.04)
- **The Doorman**: Indomitable +0.10 (+0.23), Witchmail +0.09 (+0.25), Divine Barrier +0.04 (+0.13)
- **Billy**: Reactive Barrier +0.02 (+0.05), Healbane +0.02 (+0.08), Indomitable -0.00 (+0.12)
- **Graves**: Return Fire +0.03 (+0.08), Reactive Barrier +0.01 (+0.05), Counterspell +0.00 (+0.04)
- **Apollo**: Healbane +0.02 (+0.08), Reactive Barrier +0.02 (+0.05), Counterspell -0.01 (+0.03)
- **Deadman Danny**: Indomitable +0.18 (+0.30), Spirit Resilience +0.16 (+0.30), Witchmail +0.13 (+0.30)
- **Rem**: Debuff Reducer +0.10 (+0.16), Unstoppable +0.08 (+0.19), Spellbreaker +0.02 (+0.18)
- **Silver**: Dispel Magic +0.05 (+0.11), Reactive Barrier +0.05 (+0.08), Divine Barrier +0.03 (+0.12)
- **Celeste**: Witchmail +0.07 (+0.24), Spirit Resilience +0.04 (+0.18), Healbane +0.03 (+0.10)
- **Rat King**: Return Fire +0.00 (+0.06), Bullet Resilience -0.01 (+0.05), Counterspell -0.01 (+0.03)
- **Solomon**: Return Fire +0.02 (+0.08), Counterspell +0.01 (+0.04), Healbane -0.01 (+0.05)
- **Violet**: Witchmail +0.08 (+0.25), Divine Barrier +0.05 (+0.14), Unstoppable +0.03 (+0.15)
- **Nurse Harrow**: Healbane +0.05 (+0.11), Divine Barrier +0.05 (+0.14), Counterspell +0.01 (+0.05)
- **Baba**: Healbane -0.01 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.01)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.173 | +0.054 | +0.154 | The Doorman +0.48, Lash +0.37, Deadman Danny +0.33 | 16 heroes |
| Indomitable | 6,400 | +0.194 | +0.031 | +0.174 | Wraith +0.44, Deadman Danny +0.26, Vyper +0.24 | 3 heroes |
| Divine Barrier | 6,400 | +0.167 | +0.026 | +0.090 | The Doorman +0.14, Lash +0.13, Viscous +0.11 | 2 heroes |
| Dispel Magic | 3,200 | +0.083 | +0.026 | +0.057 | Mirage +0.34, Paradox +0.18, Lash +0.15 | 11 heroes |
| Spellbreaker | 6,400 | +0.167 | +0.026 | +0.210 | Deadman Danny +0.31, Grey Talon +0.31, Holliday +0.25 | 0 heroes |
| Healbane | 1,600 | +0.031 | +0.019 | +0.069 | Lady Geist +0.08, Yamato +0.06, Victor +0.06 | 21 heroes |
| Witchmail | 6,400 | +0.109 | +0.017 | +0.181 | Deadman Danny +0.31, The Doorman +0.31, Grey Talon +0.19 | 1 heroes |
| Debuff Reducer | 1,600 | +0.012 | +0.007 | +0.100 | Grey Talon +0.22, Holliday +0.21, Paige +0.19 | 0 heroes |
| Bullet Resilience | 3,200 | +0.015 | +0.005 | +0.064 | Vindicta +0.14, Venator +0.09, Haze +0.07 | 1 heroes |
| Plated Armor | 6,400 | +0.017 | +0.003 | +0.106 | Vindicta +0.13, Haze +0.10, Wraith +0.10 | 4 heroes |
| Unstoppable | 6,400 | -0.054 | -0.009 | +0.169 | Grey Talon +0.25, Paige +0.24, Holliday +0.18 | 5 heroes |
| Reactive Barrier | 1,600 | -0.015 | -0.009 | +0.039 | The Doorman +0.11, Wraith +0.09, Deadman Danny +0.07 | 2 heroes |
| Counterspell | 3,200 | -0.029 | -0.009 | +0.033 | Viscous +0.05, Yamato +0.05, Lash +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.195 | -0.061 | +0.095 | Wraith +0.25, Paradox +0.14, Venator +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.183 | -0.115 | +0.054 | Vindicta +0.12, Paradox +0.10, Wraith +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.16 (+0.33), Spellbreaker +0.13 (+0.34), Dispel Magic +0.09 (+0.15)
- **Seven**: Witchmail +0.08 (+0.26), Healbane +0.01 (+0.07), Counterspell +0.00 (+0.04)
- **Vindicta**: Bullet Resilience +0.14 (+0.21), Plated Armor +0.13 (+0.23), Return Fire +0.12 (+0.17)
- **Lady Geist**: Healbane +0.08 (+0.15), Spirit Resilience +0.05 (+0.21), Witchmail +0.04 (+0.23)
- **Abrams**: Dispel Magic +0.02 (+0.08), Spirit Resilience -0.00 (+0.15), Reactive Barrier -0.01 (+0.03)
- **Wraith**: Indomitable +0.44 (+0.62), Metal Skin +0.25 (+0.35), Spellbreaker +0.23 (+0.44)
- **McGinnis**: Spirit Resilience +0.05 (+0.21), Witchmail +0.00 (+0.18), Counterspell +0.00 (+0.03)
- **Paradox**: Dispel Magic +0.18 (+0.24), Unstoppable +0.15 (+0.32), Metal Skin +0.14 (+0.23)
- **Dynamo**: Counterspell -0.02 (+0.01), Healbane -0.03 (+0.04), Reactive Barrier -0.04 (+0.00)
- **Kelvin**: Spirit Resilience +0.02 (+0.18), Healbane -0.02 (+0.05), Counterspell -0.02 (+0.01)
- **Haze**: Unstoppable +0.16 (+0.33), Plated Armor +0.10 (+0.21), Bullet Resilience +0.07 (+0.14)
- **Holliday**: Spellbreaker +0.25 (+0.46), Debuff Reducer +0.21 (+0.31), Unstoppable +0.18 (+0.35)
- **Bebop**: Debuff Reducer +0.13 (+0.23), Unstoppable +0.08 (+0.25), Spellbreaker +0.06 (+0.27)
- **Calico**: Spirit Resilience +0.16 (+0.31), Divine Barrier +0.06 (+0.15), Reactive Barrier +0.05 (+0.09)
- **Grey Talon**: Spellbreaker +0.31 (+0.52), Spirit Resilience +0.29 (+0.44), Unstoppable +0.25 (+0.42)
- **Mo & Krill**: Spellbreaker +0.10 (+0.31), Indomitable +0.07 (+0.24), Debuff Reducer +0.06 (+0.16)
- **Shiv**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.06 (+0.16), Divine Barrier +0.04 (+0.13)
- **Ivy**: Unstoppable +0.18 (+0.35), Indomitable +0.11 (+0.28), Debuff Reducer +0.08 (+0.18)
- **Warden**: Divine Barrier +0.03 (+0.12), Spirit Resilience +0.02 (+0.18), Return Fire +0.00 (+0.06)
- **Yamato**: Healbane +0.06 (+0.13), Counterspell +0.05 (+0.08), Witchmail +0.04 (+0.22)
- **Lash**: Spirit Resilience +0.37 (+0.52), Spellbreaker +0.18 (+0.39), Dispel Magic +0.15 (+0.21)
- **Viscous**: Spirit Resilience +0.23 (+0.38), Divine Barrier +0.11 (+0.20), Spellbreaker +0.06 (+0.27)
- **Pocket**: Spirit Resilience +0.04 (+0.19), Return Fire -0.00 (+0.05), Witchmail -0.01 (+0.18)
- **Mirage**: Dispel Magic +0.34 (+0.39), Unstoppable +0.12 (+0.29), Metal Skin +0.06 (+0.16)
- **Vyper**: Indomitable +0.24 (+0.42), Plated Armor +0.05 (+0.16), Bullet Resilience +0.03 (+0.10)
- **Sinclair**: Indomitable +0.20 (+0.37), Debuff Reducer +0.05 (+0.15), Spellbreaker +0.03 (+0.24)
- **Mina**: Divine Barrier +0.03 (+0.12), Counterspell +0.00 (+0.03), Return Fire -0.01 (+0.04)
- **Drifter**: Dispel Magic +0.01 (+0.07), Healbane -0.00 (+0.07), Return Fire -0.01 (+0.05)
- **Venator**: Metal Skin +0.11 (+0.20), Bullet Resilience +0.09 (+0.15), Plated Armor +0.01 (+0.11)
- **Victor**: Healbane +0.06 (+0.13), Spellbreaker +0.03 (+0.24), Spirit Resilience +0.03 (+0.19)
- **Paige**: Unstoppable +0.24 (+0.41), Debuff Reducer +0.19 (+0.28), Spellbreaker +0.07 (+0.29)
- **The Doorman**: Spirit Resilience +0.48 (+0.63), Witchmail +0.31 (+0.49), Indomitable +0.24 (+0.42)
- **Billy**: Reactive Barrier +0.05 (+0.09), Healbane +0.01 (+0.08), Counterspell -0.00 (+0.03)
- **Graves**: Healbane +0.02 (+0.09), Return Fire +0.01 (+0.07), Witchmail +0.01 (+0.19)
- **Apollo**: Reactive Barrier +0.03 (+0.07), Healbane +0.01 (+0.08), Counterspell -0.01 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.33 (+0.48), Witchmail +0.31 (+0.49), Spellbreaker +0.31 (+0.52)
- **Rem**: Divine Barrier +0.09 (+0.18), Spirit Resilience +0.04 (+0.20), Witchmail +0.01 (+0.19)
- **Silver**: Dispel Magic +0.11 (+0.17), Bullet Resilience +0.07 (+0.13), Metal Skin +0.05 (+0.14)
- **Celeste**: Witchmail +0.11 (+0.29), Plated Armor +0.05 (+0.16), Spirit Resilience +0.05 (+0.20)
- **Rat King**: Healbane -0.01 (+0.06), Counterspell -0.01 (+0.02), Return Fire -0.02 (+0.03)
- **Solomon**: Counterspell -0.00 (+0.03), Reactive Barrier -0.01 (+0.03), Return Fire -0.02 (+0.03)
- **Violet**: Witchmail +0.08 (+0.26), Return Fire +0.06 (+0.11), Divine Barrier +0.06 (+0.15)
- **Nurse Harrow**: Spirit Resilience +0.19 (+0.35), Divine Barrier +0.02 (+0.11), Healbane +0.01 (+0.08)
- **Baba**: Counterspell +0.00 (+0.04), Healbane -0.01 (+0.06), Witchmail -0.01 (+0.17)
