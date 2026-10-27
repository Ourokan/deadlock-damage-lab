# Counter items in the sim (phantom and up)

Built 2026-10-27T01:44:13Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.223 | +0.070 | +0.120 | Lash +0.28, Deadman Danny +0.17, Wraith +0.15 | 1 heroes |
| Divine Barrier | 6,400 | +0.406 | +0.065 | +0.097 | Lash +0.27, Wraith +0.16, Calico +0.12 | 0 heroes |
| Dispel Magic | 3,200 | +0.140 | +0.044 | +0.077 | Mirage +0.37, Silver +0.13, Infernus +0.11 | 4 heroes |
| Debuff Reducer | 1,600 | +0.067 | +0.042 | +0.059 | Wraith +0.08, Deadman Danny +0.08, Grey Talon +0.05 | 0 heroes |
| Witchmail | 6,400 | +0.233 | +0.036 | +0.199 | Lash +0.20, Deadman Danny +0.17, Wraith +0.16 | 0 heroes |
| Reactive Barrier | 1,600 | +0.057 | +0.036 | +0.055 | Wraith +0.15, Deadman Danny +0.13, The Doorman +0.08 | 2 heroes |
| Indomitable | 6,400 | +0.192 | +0.030 | +0.142 | Wraith +0.30, Vyper +0.29, Deadman Danny +0.23 | 0 heroes |
| Healbane | 1,600 | +0.038 | +0.024 | +0.087 | Nurse Harrow +0.07, Deadman Danny +0.06, Infernus +0.04 | 11 heroes |
| Spellbreaker | 6,400 | +0.149 | +0.023 | +0.147 | Lash +0.32, Deadman Danny +0.22, Wraith +0.17 | 0 heroes |
| Bullet Resilience | 3,200 | +0.038 | +0.012 | +0.090 | Wraith +0.13, Paradox +0.13, Deadman Danny +0.11 | 0 heroes |
| Counterspell | 3,200 | +0.018 | +0.006 | +0.072 | Deadman Danny +0.09, Calico +0.06, Wraith +0.04 | 1 heroes |
| Plated Armor | 6,400 | +0.029 | +0.004 | +0.126 | Holliday +0.22, Wraith +0.17, Deadman Danny +0.15 | 0 heroes |
| Unstoppable | 6,400 | +0.001 | +0.000 | +0.114 | Deadman Danny +0.17, Abrams +0.12, Wraith +0.12 | 0 heroes |
| Metal Skin | 3,200 | -0.094 | -0.029 | +0.108 | Wraith +0.24, Lash +0.24, Paradox +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.127 | -0.079 | +0.079 | Deadman Danny +0.08, The Doorman +0.06, Paradox +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.19), Unstoppable +0.06 (+0.18), Spirit Resilience +0.05 (+0.17)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.04 (+0.02)
- **Vindicta**: Return Fire +0.01 (+0.09), Divine Barrier +0.01 (+0.10), Witchmail +0.01 (+0.20)
- **Lady Geist**: Return Fire +0.04 (+0.12), Healbane +0.01 (+0.10), Counterspell +0.01 (+0.08)
- **Abrams**: Indomitable +0.14 (+0.28), Unstoppable +0.12 (+0.23), Divine Barrier +0.06 (+0.16)
- **Wraith**: Indomitable +0.30 (+0.44), Metal Skin +0.24 (+0.35), Spellbreaker +0.17 (+0.32)
- **McGinnis**: Spirit Resilience +0.00 (+0.12), Return Fire -0.00 (+0.08), Healbane -0.01 (+0.07)
- **Paradox**: Metal Skin +0.14 (+0.25), Bullet Resilience +0.13 (+0.22), Indomitable +0.12 (+0.26)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane -0.00 (+0.08), Counterspell -0.01 (+0.06), Dispel Magic -0.02 (+0.06)
- **Haze**: Plated Armor +0.09 (+0.21), Bullet Resilience +0.05 (+0.14), Indomitable +0.04 (+0.19)
- **Holliday**: Plated Armor +0.22 (+0.35), Reactive Barrier +0.03 (+0.09), Debuff Reducer +0.03 (+0.09)
- **Bebop**: Witchmail +0.03 (+0.23), Divine Barrier +0.03 (+0.13), Bullet Resilience +0.02 (+0.11)
- **Calico**: Spellbreaker +0.12 (+0.27), Divine Barrier +0.12 (+0.22), Spirit Resilience +0.11 (+0.23)
- **Grey Talon**: Debuff Reducer +0.05 (+0.11), Reactive Barrier +0.05 (+0.10), Spellbreaker +0.04 (+0.19)
- **Mo & Krill**: Spellbreaker +0.14 (+0.29), Spirit Resilience +0.08 (+0.20), Witchmail +0.08 (+0.28)
- **Shiv**: Healbane -0.01 (+0.08), Return Fire -0.01 (+0.07), Debuff Reducer -0.04 (+0.02)
- **Ivy**: Unstoppable +0.11 (+0.22), Indomitable +0.07 (+0.21), Dispel Magic -0.00 (+0.08)
- **Warden**: Return Fire +0.01 (+0.09), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.04)
- **Yamato**: Healbane +0.01 (+0.10), Counterspell -0.04 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Lash**: Spellbreaker +0.32 (+0.47), Spirit Resilience +0.28 (+0.40), Divine Barrier +0.27 (+0.36)
- **Viscous**: Healbane -0.02 (+0.07), Divine Barrier -0.02 (+0.07), Return Fire -0.03 (+0.05)
- **Pocket**: Spirit Resilience +0.05 (+0.17), Witchmail +0.05 (+0.25), Spellbreaker +0.04 (+0.18)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spirit Resilience +0.06 (+0.18), Spellbreaker +0.06 (+0.20)
- **Vyper**: Indomitable +0.29 (+0.43), Debuff Reducer +0.04 (+0.10), Spellbreaker +0.03 (+0.17)
- **Sinclair**: Indomitable +0.09 (+0.23), Spellbreaker +0.02 (+0.16), Unstoppable +0.02 (+0.13)
- **Mina**: Witchmail +0.03 (+0.23), Return Fire +0.02 (+0.10), Counterspell +0.00 (+0.08)
- **Drifter**: Witchmail +0.04 (+0.24), Return Fire +0.04 (+0.12), Counterspell +0.04 (+0.11)
- **Venator**: Bullet Resilience +0.09 (+0.18), Metal Skin +0.02 (+0.12), Divine Barrier +0.01 (+0.11)
- **Victor**: Spirit Resilience +0.03 (+0.15), Healbane +0.01 (+0.10), Spellbreaker +0.01 (+0.16)
- **Paige**: Healbane -0.01 (+0.07), Counterspell -0.02 (+0.05), Return Fire -0.03 (+0.05)
- **The Doorman**: Indomitable +0.15 (+0.30), Witchmail +0.12 (+0.31), Spirit Resilience +0.10 (+0.22)
- **Billy**: Counterspell +0.04 (+0.11), Spirit Resilience +0.04 (+0.16), Spellbreaker +0.04 (+0.18)
- **Graves**: Witchmail +0.09 (+0.29), Metal Skin +0.09 (+0.19), Spirit Resilience +0.08 (+0.20)
- **Apollo**: Healbane +0.00 (+0.09), Reactive Barrier -0.04 (+0.01), Debuff Reducer -0.04 (+0.02)
- **Deadman Danny**: Indomitable +0.23 (+0.37), Spellbreaker +0.22 (+0.36), Witchmail +0.17 (+0.37)
- **Rem**: Witchmail -0.00 (+0.20), Unstoppable -0.01 (+0.10), Dispel Magic -0.01 (+0.06)
- **Silver**: Dispel Magic +0.13 (+0.21), Metal Skin +0.03 (+0.14), Reactive Barrier +0.03 (+0.08)
- **Celeste**: Spirit Resilience +0.10 (+0.22), Witchmail +0.09 (+0.29), Dispel Magic +0.04 (+0.12)
- **Rat King**: Counterspell +0.01 (+0.08), Bullet Resilience -0.00 (+0.09), Return Fire -0.01 (+0.07)
- **Solomon**: Return Fire -0.02 (+0.06), Counterspell -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **Violet**: Return Fire +0.03 (+0.11), Healbane -0.02 (+0.07), Counterspell -0.04 (+0.03)
- **Nurse Harrow**: Healbane +0.07 (+0.16), Return Fire +0.01 (+0.09), Debuff Reducer -0.02 (+0.04)
- **Baba**: Healbane -0.00 (+0.08), Debuff Reducer -0.02 (+0.04), Counterspell -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.204 | +0.064 | +0.111 | Lash +0.37, Pocket +0.21, Deadman Danny +0.19 | 10 heroes |
| Divine Barrier | 6,400 | +0.251 | +0.040 | +0.061 | Lash +0.20, Wraith +0.13, The Doorman +0.10 | 1 heroes |
| Dispel Magic | 3,200 | +0.108 | +0.034 | +0.046 | Mirage +0.30, Infernus +0.10, Graves +0.08 | 7 heroes |
| Witchmail | 6,400 | +0.210 | +0.033 | +0.160 | Graves +0.17, Lash +0.17, Pocket +0.13 | 0 heroes |
| Indomitable | 6,400 | +0.158 | +0.025 | +0.112 | Vyper +0.34, Wraith +0.29, The Doorman +0.13 | 0 heroes |
| Spellbreaker | 6,400 | +0.143 | +0.022 | +0.117 | Lash +0.36, Wraith +0.15, Deadman Danny +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.034 | +0.021 | +0.041 | Wraith +0.10, Lash +0.05, The Doorman +0.04 | 1 heroes |
| Reactive Barrier | 1,600 | +0.033 | +0.021 | +0.040 | Graves +0.11, Wraith +0.11, The Doorman +0.09 | 4 heroes |
| Plated Armor | 6,400 | +0.019 | +0.003 | +0.099 | Deadman Danny +0.21, Wraith +0.14, Paradox +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | +0.004 | +0.001 | +0.061 | Venator +0.13, Paradox +0.12, Wraith +0.10 | 0 heroes |
| Healbane | 1,600 | -0.001 | -0.001 | +0.065 | Yamato +0.06, Pocket +0.05, Bebop +0.05 | 17 heroes |
| Counterspell | 3,200 | -0.009 | -0.003 | +0.044 | Pocket +0.05, Wraith +0.05, The Doorman +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.033 | -0.005 | +0.084 | Mo & Krill +0.12, Ivy +0.10, Wraith +0.09 | 0 heroes |
| Metal Skin | 3,200 | -0.118 | -0.037 | +0.083 | Wraith +0.22, Paradox +0.15, Lash +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.147 | -0.092 | +0.055 | Wraith +0.08, Pocket +0.06, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.15), Unstoppable +0.04 (+0.13), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.04 (+0.20), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Witchmail +0.06 (+0.22), Divine Barrier +0.04 (+0.10), Bullet Resilience +0.04 (+0.10)
- **Lady Geist**: Return Fire +0.04 (+0.09), Divine Barrier +0.03 (+0.09), Bullet Resilience +0.02 (+0.08)
- **Abrams**: Unstoppable +0.08 (+0.17), Indomitable +0.07 (+0.18), Healbane +0.04 (+0.10)
- **Wraith**: Indomitable +0.29 (+0.41), Metal Skin +0.22 (+0.31), Spellbreaker +0.15 (+0.26)
- **McGinnis**: Spirit Resilience +0.08 (+0.19), Return Fire +0.01 (+0.07), Dispel Magic +0.01 (+0.06)
- **Paradox**: Metal Skin +0.15 (+0.24), Bullet Resilience +0.12 (+0.18), Plated Armor +0.09 (+0.19)
- **Dynamo**: Healbane +0.00 (+0.07), Counterspell -0.02 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Healbane +0.01 (+0.07), Dispel Magic -0.01 (+0.04), Counterspell -0.01 (+0.04)
- **Haze**: Indomitable +0.09 (+0.21), Plated Armor +0.09 (+0.18), Unstoppable +0.08 (+0.16)
- **Holliday**: Return Fire +0.04 (+0.09), Debuff Reducer +0.03 (+0.07), Indomitable +0.03 (+0.14)
- **Bebop**: Healbane +0.05 (+0.12), Counterspell +0.02 (+0.06), Metal Skin +0.01 (+0.10)
- **Calico**: Reactive Barrier +0.03 (+0.07), Divine Barrier +0.03 (+0.09), Spellbreaker +0.02 (+0.14)
- **Grey Talon**: Debuff Reducer +0.03 (+0.07), Unstoppable +0.03 (+0.11), Spellbreaker +0.02 (+0.14)
- **Mo & Krill**: Unstoppable +0.12 (+0.20), Spellbreaker +0.05 (+0.16), Dispel Magic +0.04 (+0.09)
- **Shiv**: Metal Skin +0.05 (+0.14), Divine Barrier +0.05 (+0.11), Bullet Resilience +0.04 (+0.10)
- **Ivy**: Unstoppable +0.10 (+0.19), Indomitable +0.09 (+0.20), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.07), Debuff Reducer -0.00 (+0.04), Counterspell -0.00 (+0.04)
- **Yamato**: Healbane +0.06 (+0.12), Debuff Reducer +0.00 (+0.04), Counterspell -0.00 (+0.04)
- **Lash**: Spirit Resilience +0.37 (+0.48), Spellbreaker +0.36 (+0.48), Divine Barrier +0.20 (+0.27)
- **Viscous**: Healbane +0.01 (+0.08), Counterspell +0.00 (+0.05), Debuff Reducer -0.01 (+0.04)
- **Pocket**: Spirit Resilience +0.21 (+0.33), Witchmail +0.13 (+0.29), Spellbreaker +0.13 (+0.25)
- **Mirage**: Dispel Magic +0.30 (+0.35), Spellbreaker +0.01 (+0.13), Spirit Resilience +0.01 (+0.12)
- **Vyper**: Indomitable +0.34 (+0.45), Metal Skin +0.05 (+0.13), Debuff Reducer +0.03 (+0.07)
- **Sinclair**: Indomitable +0.09 (+0.20), Return Fire +0.00 (+0.06), Spellbreaker +0.00 (+0.12)
- **Mina**: Witchmail +0.03 (+0.19), Spirit Resilience +0.02 (+0.13), Divine Barrier +0.01 (+0.07)
- **Drifter**: Witchmail +0.04 (+0.20), Bullet Resilience +0.01 (+0.07), Counterspell -0.00 (+0.04)
- **Venator**: Bullet Resilience +0.13 (+0.19), Metal Skin +0.10 (+0.18), Plated Armor +0.07 (+0.16)
- **Victor**: Spellbreaker +0.07 (+0.19), Spirit Resilience +0.07 (+0.18), Dispel Magic +0.00 (+0.05)
- **Paige**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.05), Healbane -0.01 (+0.05)
- **The Doorman**: Spirit Resilience +0.17 (+0.28), Indomitable +0.13 (+0.24), Divine Barrier +0.10 (+0.16)
- **Billy**: Spirit Resilience +0.02 (+0.13), Spellbreaker -0.00 (+0.11), Counterspell -0.01 (+0.04)
- **Graves**: Witchmail +0.17 (+0.33), Metal Skin +0.13 (+0.22), Spirit Resilience +0.13 (+0.24)
- **Apollo**: Reactive Barrier +0.02 (+0.06), Indomitable -0.01 (+0.10), Unstoppable -0.01 (+0.07)
- **Deadman Danny**: Plated Armor +0.21 (+0.31), Spirit Resilience +0.19 (+0.30), Spellbreaker +0.14 (+0.26)
- **Rem**: Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.06), Reactive Barrier -0.01 (+0.03)
- **Silver**: Dispel Magic +0.06 (+0.11), Metal Skin +0.06 (+0.14), Reactive Barrier +0.04 (+0.08)
- **Celeste**: Witchmail +0.00 (+0.16), Healbane -0.01 (+0.06), Spirit Resilience -0.01 (+0.10)
- **Rat King**: Bullet Resilience -0.00 (+0.06), Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.03)
- **Solomon**: Return Fire -0.00 (+0.05), Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Violet**: Witchmail +0.03 (+0.19), Return Fire +0.03 (+0.09), Healbane +0.01 (+0.08)
- **Nurse Harrow**: Healbane -0.00 (+0.06), Dispel Magic -0.03 (+0.01), Return Fire -0.04 (+0.02)
- **Baba**: Unstoppable +0.03 (+0.11), Healbane +0.01 (+0.08), Debuff Reducer -0.01 (+0.03)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.206 | +0.064 | +0.121 | Lash +0.26, Deadman Danny +0.25, Wraith +0.12 | 14 heroes |
| Divine Barrier | 6,400 | +0.271 | +0.043 | +0.061 | Lash +0.20, Vindicta +0.12, Wraith +0.09 | 2 heroes |
| Dispel Magic | 3,200 | +0.120 | +0.038 | +0.061 | Lash +0.27, Mirage +0.27, Paradox +0.10 | 9 heroes |
| Witchmail | 6,400 | +0.216 | +0.034 | +0.170 | Deadman Danny +0.19, Lash +0.17, Paradox +0.12 | 1 heroes |
| Indomitable | 6,400 | +0.181 | +0.030 | +0.132 | Vyper +0.38, Wraith +0.30, Deadman Danny +0.24 | 0 heroes |
| Spellbreaker | 6,400 | +0.163 | +0.025 | +0.132 | Lash +0.40, Deadman Danny +0.24, Wraith +0.15 | 0 heroes |
| Debuff Reducer | 1,600 | +0.036 | +0.022 | +0.046 | Grey Talon +0.09, Deadman Danny +0.08, Vyper +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | +0.024 | +0.015 | +0.038 | Deadman Danny +0.14, Wraith +0.09, Yamato +0.08 | 5 heroes |
| Plated Armor | 6,400 | +0.033 | +0.005 | +0.113 | Deadman Danny +0.22, Holliday +0.16, Wraith +0.15 | 0 heroes |
| Bullet Resilience | 3,200 | -0.006 | -0.002 | +0.063 | Deadman Danny +0.12, Vindicta +0.11, Lash +0.10 | 1 heroes |
| Healbane | 1,600 | -0.005 | -0.003 | +0.063 | Drifter +0.06, Infernus +0.04, Paradox +0.04 | 15 heroes |
| Unstoppable | 6,400 | -0.021 | -0.003 | +0.101 | Deadman Danny +0.18, Abrams +0.14, Grey Talon +0.11 | 3 heroes |
| Counterspell | 3,200 | -0.015 | -0.005 | +0.038 | Deadman Danny +0.07, Drifter +0.04, Yamato +0.04 | 1 heroes |
| Metal Skin | 3,200 | -0.102 | -0.032 | +0.105 | Wraith +0.26, Lash +0.18, Paradox +0.09 | 0 heroes |
| Return Fire | 1,600 | -0.147 | -0.092 | +0.052 | Wraith +0.09, Paradox +0.07, Vindicta +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.16), Unstoppable +0.10 (+0.20), Spellbreaker +0.08 (+0.22)
- **Seven**: Witchmail +0.04 (+0.21), Healbane +0.00 (+0.07), Spirit Resilience -0.01 (+0.11)
- **Vindicta**: Divine Barrier +0.12 (+0.18), Bullet Resilience +0.11 (+0.17), Plated Armor +0.08 (+0.20)
- **Lady Geist**: Return Fire +0.04 (+0.09), Divine Barrier +0.02 (+0.08), Bullet Resilience +0.01 (+0.08)
- **Abrams**: Unstoppable +0.14 (+0.24), Dispel Magic +0.08 (+0.14), Healbane +0.04 (+0.10)
- **Wraith**: Indomitable +0.30 (+0.43), Metal Skin +0.26 (+0.37), Plated Armor +0.15 (+0.26)
- **McGinnis**: Spirit Resilience +0.08 (+0.21), Witchmail +0.03 (+0.19), Spellbreaker +0.02 (+0.15)
- **Paradox**: Witchmail +0.12 (+0.29), Spellbreaker +0.12 (+0.25), Dispel Magic +0.10 (+0.16)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell +0.00 (+0.04), Return Fire -0.03 (+0.02)
- **Kelvin**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.01)
- **Haze**: Plated Armor +0.09 (+0.20), Indomitable +0.09 (+0.22), Unstoppable +0.06 (+0.16)
- **Holliday**: Plated Armor +0.16 (+0.28), Debuff Reducer +0.04 (+0.08), Indomitable +0.03 (+0.16)
- **Bebop**: Healbane +0.01 (+0.07), Counterspell -0.02 (+0.02), Return Fire -0.03 (+0.03)
- **Calico**: Reactive Barrier +0.03 (+0.07), Divine Barrier +0.02 (+0.08), Spirit Resilience +0.01 (+0.13)
- **Grey Talon**: Spellbreaker +0.13 (+0.26), Unstoppable +0.11 (+0.21), Indomitable +0.09 (+0.22)
- **Mo & Krill**: Unstoppable +0.08 (+0.18), Spirit Resilience +0.07 (+0.19), Spellbreaker +0.05 (+0.19)
- **Shiv**: Metal Skin +0.05 (+0.16), Bullet Resilience +0.03 (+0.09), Divine Barrier +0.03 (+0.09)
- **Ivy**: Unstoppable +0.10 (+0.20), Indomitable +0.05 (+0.18), Debuff Reducer +0.02 (+0.06)
- **Warden**: Return Fire +0.04 (+0.09), Counterspell +0.02 (+0.06), Divine Barrier +0.01 (+0.08)
- **Yamato**: Reactive Barrier +0.08 (+0.12), Indomitable +0.04 (+0.17), Counterspell +0.04 (+0.08)
- **Lash**: Spellbreaker +0.40 (+0.54), Dispel Magic +0.27 (+0.33), Spirit Resilience +0.26 (+0.38)
- **Viscous**: Divine Barrier +0.00 (+0.06), Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05)
- **Pocket**: Spirit Resilience +0.06 (+0.18), Witchmail +0.01 (+0.18), Spellbreaker -0.01 (+0.13)
- **Mirage**: Dispel Magic +0.27 (+0.33), Spirit Resilience +0.02 (+0.14), Healbane +0.00 (+0.07)
- **Vyper**: Indomitable +0.38 (+0.51), Debuff Reducer +0.07 (+0.11), Unstoppable +0.06 (+0.16)
- **Sinclair**: Indomitable +0.12 (+0.25), Return Fire +0.00 (+0.06), Unstoppable -0.01 (+0.09)
- **Mina**: Spirit Resilience +0.12 (+0.24), Witchmail +0.10 (+0.27), Divine Barrier +0.05 (+0.12)
- **Drifter**: Spirit Resilience +0.08 (+0.20), Healbane +0.06 (+0.13), Witchmail +0.06 (+0.23)
- **Venator**: Bullet Resilience +0.09 (+0.15), Metal Skin +0.09 (+0.20), Plated Armor +0.03 (+0.14)
- **Victor**: Spirit Resilience +0.03 (+0.15), Spellbreaker +0.00 (+0.14), Healbane -0.00 (+0.06)
- **Paige**: Unstoppable +0.11 (+0.21), Debuff Reducer +0.05 (+0.09), Counterspell -0.01 (+0.03)
- **The Doorman**: Spirit Resilience +0.12 (+0.24), Indomitable +0.11 (+0.24), Witchmail +0.09 (+0.26)
- **Billy**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.03)
- **Graves**: Return Fire +0.03 (+0.08), Witchmail +0.02 (+0.19), Metal Skin +0.01 (+0.11)
- **Apollo**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.03), Unstoppable -0.02 (+0.08)
- **Deadman Danny**: Spirit Resilience +0.25 (+0.38), Indomitable +0.24 (+0.37), Spellbreaker +0.24 (+0.37)
- **Rem**: Debuff Reducer +0.06 (+0.10), Unstoppable +0.05 (+0.15), Counterspell -0.00 (+0.03)
- **Silver**: Dispel Magic +0.06 (+0.12), Return Fire +0.00 (+0.05), Divine Barrier -0.00 (+0.06)
- **Celeste**: Witchmail +0.05 (+0.21), Dispel Magic +0.04 (+0.11), Reactive Barrier +0.02 (+0.06)
- **Rat King**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.03), Bullet Resilience -0.01 (+0.05)
- **Solomon**: Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.02), Debuff Reducer -0.02 (+0.03)
- **Violet**: Witchmail +0.07 (+0.24), Return Fire +0.04 (+0.09), Healbane +0.02 (+0.08)
- **Nurse Harrow**: Healbane +0.04 (+0.10), Counterspell -0.01 (+0.03), Return Fire -0.03 (+0.03)
- **Baba**: Healbane -0.00 (+0.06), Unstoppable -0.01 (+0.09), Counterspell -0.02 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.244 | +0.076 | +0.136 | Lash +0.56, Deadman Danny +0.35, The Doorman +0.31 | 15 heroes |
| Dispel Magic | 3,200 | +0.115 | +0.036 | +0.059 | Mirage +0.27, Silver +0.21, Lash +0.20 | 9 heroes |
| Indomitable | 6,400 | +0.216 | +0.035 | +0.162 | Wraith +0.29, Vyper +0.27, Deadman Danny +0.27 | 1 heroes |
| Witchmail | 6,400 | +0.205 | +0.032 | +0.161 | Lash +0.28, The Doorman +0.24, Deadman Danny +0.19 | 2 heroes |
| Spellbreaker | 6,400 | +0.177 | +0.028 | +0.139 | Lash +0.46, Deadman Danny +0.24, The Doorman +0.18 | 0 heroes |
| Divine Barrier | 6,400 | +0.176 | +0.028 | +0.060 | Lash +0.26, Calico +0.15, Vindicta +0.12 | 3 heroes |
| Debuff Reducer | 1,600 | +0.030 | +0.018 | +0.046 | Lash +0.10, Grey Talon +0.09, Rem +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | +0.004 | +0.003 | +0.040 | Deadman Danny +0.13, Calico +0.12, Drifter +0.12 | 3 heroes |
| Plated Armor | 6,400 | +0.011 | +0.002 | +0.098 | Lash +0.15, Vindicta +0.15, Vyper +0.13 | 2 heroes |
| Unstoppable | 6,400 | -0.004 | -0.001 | +0.119 | Infernus +0.24, Haze +0.24, Grey Talon +0.19 | 8 heroes |
| Bullet Resilience | 3,200 | -0.022 | -0.007 | +0.057 | Lash +0.17, Vindicta +0.10, Venator +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.025 | -0.008 | +0.034 | Lash +0.12, The Doorman +0.06, Viscous +0.02 | 1 heroes |
| Healbane | 1,600 | -0.014 | -0.009 | +0.053 | Nurse Harrow +0.09, Lady Geist +0.06, Mo & Krill +0.06 | 14 heroes |
| Metal Skin | 3,200 | -0.103 | -0.032 | +0.106 | Lash +0.26, Silver +0.16, Wraith +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.152 | -0.095 | +0.049 | Vindicta +0.05, Wraith +0.05, Paradox +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.24 (+0.36), Dispel Magic +0.05 (+0.11), Spellbreaker +0.04 (+0.18)
- **Seven**: Witchmail +0.06 (+0.22), Counterspell -0.01 (+0.02), Spirit Resilience -0.02 (+0.12)
- **Vindicta**: Plated Armor +0.15 (+0.25), Divine Barrier +0.12 (+0.18), Bullet Resilience +0.10 (+0.15)
- **Lady Geist**: Healbane +0.06 (+0.11), Dispel Magic +0.02 (+0.08), Metal Skin +0.02 (+0.12)
- **Abrams**: Unstoppable +0.09 (+0.21), Spellbreaker +0.04 (+0.18), Indomitable +0.04 (+0.20)
- **Wraith**: Indomitable +0.29 (+0.45), Metal Skin +0.13 (+0.24), Witchmail +0.06 (+0.22)
- **McGinnis**: Spirit Resilience +0.03 (+0.17), Healbane +0.02 (+0.07), Counterspell -0.00 (+0.03)
- **Paradox**: Unstoppable +0.16 (+0.28), Witchmail +0.08 (+0.24), Dispel Magic +0.07 (+0.13)
- **Dynamo**: Healbane +0.02 (+0.07), Counterspell -0.01 (+0.03), Debuff Reducer -0.04 (+0.01)
- **Kelvin**: Spirit Resilience +0.11 (+0.24), Spellbreaker +0.02 (+0.16), Healbane +0.01 (+0.07)
- **Haze**: Unstoppable +0.24 (+0.36), Metal Skin +0.06 (+0.17), Bullet Resilience +0.06 (+0.12)
- **Holliday**: Spellbreaker +0.04 (+0.18), Return Fire +0.03 (+0.08), Plated Armor +0.02 (+0.12)
- **Bebop**: Debuff Reducer +0.05 (+0.10), Spellbreaker +0.02 (+0.16), Reactive Barrier +0.01 (+0.05)
- **Calico**: Spirit Resilience +0.16 (+0.29), Divine Barrier +0.15 (+0.21), Reactive Barrier +0.12 (+0.16)
- **Grey Talon**: Unstoppable +0.19 (+0.31), Spellbreaker +0.17 (+0.31), Spirit Resilience +0.12 (+0.26)
- **Mo & Krill**: Healbane +0.06 (+0.11), Unstoppable +0.04 (+0.16), Dispel Magic +0.04 (+0.09)
- **Shiv**: Metal Skin +0.03 (+0.14), Bullet Resilience +0.03 (+0.08), Divine Barrier +0.02 (+0.08)
- **Ivy**: Unstoppable +0.13 (+0.25), Indomitable +0.08 (+0.24), Debuff Reducer +0.04 (+0.09)
- **Warden**: Plated Armor +0.06 (+0.16), Metal Skin +0.04 (+0.14), Healbane +0.01 (+0.07)
- **Yamato**: Reactive Barrier +0.07 (+0.11), Indomitable +0.05 (+0.21), Debuff Reducer +0.05 (+0.09)
- **Lash**: Spirit Resilience +0.56 (+0.69), Spellbreaker +0.46 (+0.60), Witchmail +0.28 (+0.44)
- **Viscous**: Divine Barrier +0.05 (+0.11), Counterspell +0.02 (+0.06), Bullet Resilience +0.01 (+0.07)
- **Pocket**: Spirit Resilience +0.10 (+0.24), Witchmail +0.04 (+0.20), Spellbreaker +0.01 (+0.15)
- **Mirage**: Dispel Magic +0.27 (+0.33), Metal Skin +0.07 (+0.17), Plated Armor +0.01 (+0.11)
- **Vyper**: Indomitable +0.27 (+0.43), Plated Armor +0.13 (+0.23), Metal Skin +0.07 (+0.18)
- **Sinclair**: Indomitable +0.15 (+0.31), Spellbreaker +0.07 (+0.21), Dispel Magic +0.06 (+0.12)
- **Mina**: Divine Barrier +0.00 (+0.06), Plated Armor -0.01 (+0.09), Return Fire -0.01 (+0.04)
- **Drifter**: Indomitable +0.21 (+0.37), Spirit Resilience +0.19 (+0.32), Reactive Barrier +0.12 (+0.16)
- **Venator**: Metal Skin +0.13 (+0.24), Bullet Resilience +0.08 (+0.14), Plated Armor +0.02 (+0.12)
- **Victor**: Spellbreaker +0.08 (+0.22), Spirit Resilience +0.06 (+0.19), Healbane +0.04 (+0.09)
- **Paige**: Counterspell +0.00 (+0.04), Return Fire -0.01 (+0.04), Healbane -0.01 (+0.04)
- **The Doorman**: Spirit Resilience +0.31 (+0.44), Witchmail +0.24 (+0.40), Indomitable +0.24 (+0.40)
- **Billy**: Healbane -0.00 (+0.05), Return Fire -0.01 (+0.04), Reactive Barrier -0.01 (+0.03)
- **Graves**: Return Fire +0.02 (+0.07), Reactive Barrier -0.01 (+0.03), Counterspell -0.02 (+0.01)
- **Apollo**: Healbane +0.01 (+0.06), Bullet Resilience -0.01 (+0.05), Counterspell -0.02 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.35 (+0.49), Indomitable +0.27 (+0.43), Spellbreaker +0.24 (+0.38)
- **Rem**: Debuff Reducer +0.07 (+0.11), Spellbreaker +0.05 (+0.18), Divine Barrier -0.00 (+0.06)
- **Silver**: Dispel Magic +0.21 (+0.27), Metal Skin +0.16 (+0.27), Indomitable +0.11 (+0.27)
- **Celeste**: Witchmail +0.08 (+0.24), Spirit Resilience +0.08 (+0.21), Healbane +0.04 (+0.09)
- **Rat King**: Healbane -0.01 (+0.04), Return Fire -0.01 (+0.04), Counterspell -0.01 (+0.02)
- **Solomon**: Return Fire +0.01 (+0.05), Counterspell +0.00 (+0.04), Reactive Barrier -0.00 (+0.04)
- **Violet**: Return Fire +0.03 (+0.08), Witchmail +0.01 (+0.17), Healbane -0.00 (+0.05)
- **Nurse Harrow**: Spirit Resilience +0.12 (+0.25), Dispel Magic +0.11 (+0.17), Witchmail +0.09 (+0.25)
- **Baba**: Healbane +0.00 (+0.05), Counterspell -0.00 (+0.03), Witchmail -0.01 (+0.15)
