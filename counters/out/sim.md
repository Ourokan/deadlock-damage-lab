# Counter items in the sim (phantom and up)

Built 2026-10-26T02:05:57Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.239 | +0.074 | +0.130 | Lash +0.25, Wraith +0.16, Deadman Danny +0.13 | 1 heroes |
| Divine Barrier | 6,400 | +0.363 | +0.058 | +0.099 | Wraith +0.18, Lash +0.17, Graves +0.10 | 0 heroes |
| Dispel Magic | 3,200 | +0.143 | +0.045 | +0.081 | Mirage +0.37, Silver +0.11, Infernus +0.09 | 4 heroes |
| Debuff Reducer | 1,600 | +0.065 | +0.041 | +0.057 | Wraith +0.11, Deadman Danny +0.06, Vyper +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.058 | +0.037 | +0.055 | Wraith +0.15, Deadman Danny +0.14, Paradox +0.09 | 2 heroes |
| Witchmail | 6,400 | +0.222 | +0.035 | +0.189 | Deadman Danny +0.17, Wraith +0.16, Lash +0.11 | 0 heroes |
| Indomitable | 6,400 | +0.199 | +0.032 | +0.148 | Wraith +0.30, The Doorman +0.30, Vyper +0.28 | 0 heroes |
| Healbane | 1,600 | +0.043 | +0.027 | +0.087 | Billy +0.06, Mo & Krill +0.05, Nurse Harrow +0.05 | 11 heroes |
| Spellbreaker | 6,400 | +0.153 | +0.024 | +0.151 | Lash +0.23, Wraith +0.19, Deadman Danny +0.18 | 0 heroes |
| Bullet Resilience | 3,200 | +0.044 | +0.014 | +0.092 | Wraith +0.13, Deadman Danny +0.11, Venator +0.11 | 0 heroes |
| Counterspell | 3,200 | +0.018 | +0.005 | +0.069 | Deadman Danny +0.08, Wraith +0.07, Billy +0.05 | 1 heroes |
| Plated Armor | 6,400 | +0.028 | +0.004 | +0.131 | Holliday +0.23, Wraith +0.18, Deadman Danny +0.15 | 0 heroes |
| Unstoppable | 6,400 | +0.009 | +0.001 | +0.123 | Deadman Danny +0.15, Wraith +0.14, Ivy +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.090 | -0.028 | +0.113 | Wraith +0.26, Paradox +0.13, Drifter +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.133 | -0.083 | +0.069 | Deadman Danny +0.08, Wraith +0.07, Holliday +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.17), Unstoppable +0.07 (+0.19), Spirit Resilience +0.05 (+0.18)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Vindicta**: Counterspell +0.02 (+0.09), Return Fire +0.01 (+0.08), Witchmail -0.00 (+0.19)
- **Lady Geist**: Return Fire +0.04 (+0.11), Divine Barrier +0.02 (+0.11), Bullet Resilience +0.01 (+0.10)
- **Abrams**: Indomitable +0.16 (+0.31), Unstoppable +0.05 (+0.18), Divine Barrier +0.03 (+0.13)
- **Wraith**: Indomitable +0.30 (+0.45), Metal Skin +0.26 (+0.37), Spellbreaker +0.19 (+0.34)
- **McGinnis**: Spirit Resilience +0.05 (+0.18), Healbane -0.01 (+0.07), Return Fire -0.02 (+0.05)
- **Paradox**: Metal Skin +0.13 (+0.24), Bullet Resilience +0.11 (+0.20), Plated Armor +0.10 (+0.23)
- **Dynamo**: Healbane +0.00 (+0.09), Counterspell -0.02 (+0.05), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane +0.00 (+0.09), Counterspell -0.01 (+0.06), Debuff Reducer -0.01 (+0.04)
- **Haze**: Plated Armor +0.09 (+0.22), Indomitable +0.06 (+0.21), Bullet Resilience +0.05 (+0.14)
- **Holliday**: Plated Armor +0.23 (+0.37), Debuff Reducer +0.05 (+0.11), Return Fire +0.05 (+0.12)
- **Bebop**: Witchmail +0.04 (+0.23), Divine Barrier +0.04 (+0.14), Counterspell +0.04 (+0.11)
- **Calico**: Divine Barrier +0.02 (+0.12), Spellbreaker +0.02 (+0.17), Counterspell +0.01 (+0.08)
- **Grey Talon**: Reactive Barrier +0.07 (+0.12), Indomitable +0.06 (+0.21), Spellbreaker +0.06 (+0.21)
- **Mo & Krill**: Spellbreaker +0.13 (+0.28), Spirit Resilience +0.08 (+0.20), Witchmail +0.06 (+0.25)
- **Shiv**: Healbane -0.02 (+0.07), Return Fire -0.02 (+0.05), Divine Barrier -0.03 (+0.07)
- **Ivy**: Unstoppable +0.10 (+0.22), Indomitable +0.06 (+0.21), Debuff Reducer +0.01 (+0.06)
- **Warden**: Return Fire +0.04 (+0.11), Bullet Resilience +0.01 (+0.10), Counterspell +0.01 (+0.08)
- **Yamato**: Healbane +0.02 (+0.10), Debuff Reducer -0.04 (+0.02), Counterspell -0.04 (+0.03)
- **Lash**: Spirit Resilience +0.25 (+0.38), Spellbreaker +0.23 (+0.38), Divine Barrier +0.17 (+0.27)
- **Viscous**: Counterspell -0.01 (+0.06), Divine Barrier -0.02 (+0.08), Return Fire -0.02 (+0.05)
- **Pocket**: Witchmail +0.04 (+0.22), Return Fire +0.03 (+0.10), Spirit Resilience +0.03 (+0.16)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spellbreaker +0.08 (+0.24), Spirit Resilience +0.05 (+0.18)
- **Vyper**: Indomitable +0.28 (+0.43), Debuff Reducer +0.06 (+0.12), Spellbreaker +0.03 (+0.18)
- **Sinclair**: Indomitable +0.05 (+0.20), Spellbreaker +0.05 (+0.20), Return Fire +0.03 (+0.10)
- **Mina**: Divine Barrier +0.08 (+0.18), Spirit Resilience +0.07 (+0.20), Witchmail +0.07 (+0.26)
- **Drifter**: Metal Skin +0.13 (+0.24), Spirit Resilience +0.11 (+0.24), Witchmail +0.09 (+0.28)
- **Venator**: Bullet Resilience +0.11 (+0.20), Metal Skin +0.05 (+0.16), Plated Armor +0.04 (+0.17)
- **Victor**: Healbane +0.00 (+0.09), Debuff Reducer -0.04 (+0.02), Reactive Barrier -0.04 (+0.01)
- **Paige**: Healbane +0.00 (+0.09), Return Fire -0.01 (+0.06), Counterspell -0.01 (+0.06)
- **The Doorman**: Indomitable +0.30 (+0.45), Reactive Barrier -0.02 (+0.04), Counterspell -0.02 (+0.05)
- **Billy**: Healbane +0.06 (+0.15), Counterspell +0.05 (+0.12), Debuff Reducer +0.04 (+0.10)
- **Graves**: Spirit Resilience +0.11 (+0.24), Divine Barrier +0.10 (+0.20), Metal Skin +0.10 (+0.21)
- **Apollo**: Healbane +0.04 (+0.13), Debuff Reducer +0.01 (+0.07), Counterspell +0.01 (+0.08)
- **Deadman Danny**: Indomitable +0.19 (+0.34), Spellbreaker +0.18 (+0.33), Witchmail +0.17 (+0.35)
- **Rem**: Unstoppable +0.09 (+0.22), Indomitable +0.07 (+0.22), Counterspell -0.02 (+0.05)
- **Silver**: Dispel Magic +0.11 (+0.19), Metal Skin +0.04 (+0.15), Reactive Barrier +0.00 (+0.06)
- **Celeste**: Spirit Resilience +0.12 (+0.25), Witchmail +0.07 (+0.26), Dispel Magic +0.05 (+0.13)
- **Rat King**: Counterspell +0.02 (+0.09), Return Fire +0.01 (+0.08), Bullet Resilience +0.01 (+0.10)
- **Solomon**: Return Fire -0.00 (+0.07), Counterspell -0.01 (+0.06), Healbane -0.03 (+0.06)
- **Violet**: Unstoppable +0.08 (+0.21), Reactive Barrier +0.08 (+0.13), Spirit Resilience +0.07 (+0.20)
- **Nurse Harrow**: Healbane +0.05 (+0.13), Counterspell -0.01 (+0.05), Dispel Magic -0.02 (+0.06)
- **Baba**: Healbane +0.01 (+0.10), Counterspell -0.02 (+0.05), Return Fire -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.210 | +0.066 | +0.110 | Lash +0.25, Pocket +0.20, Graves +0.15 | 10 heroes |
| Dispel Magic | 3,200 | +0.124 | +0.039 | +0.064 | Mirage +0.31, Silver +0.14, Lash +0.12 | 7 heroes |
| Divine Barrier | 6,400 | +0.234 | +0.037 | +0.068 | Lash +0.16, Wraith +0.11, Graves +0.10 | 1 heroes |
| Witchmail | 6,400 | +0.205 | +0.032 | +0.156 | Lash +0.16, Graves +0.16, Pocket +0.10 | 0 heroes |
| Indomitable | 6,400 | +0.167 | +0.027 | +0.121 | The Doorman +0.33, Vyper +0.32, Wraith +0.20 | 0 heroes |
| Debuff Reducer | 1,600 | +0.038 | +0.024 | +0.045 | Wraith +0.08, Vyper +0.05, Lash +0.05 | 1 heroes |
| Reactive Barrier | 1,600 | +0.037 | +0.023 | +0.042 | Wraith +0.11, Paradox +0.07, Deadman Danny +0.07 | 4 heroes |
| Spellbreaker | 6,400 | +0.143 | +0.022 | +0.117 | Lash +0.21, Wraith +0.12, Pocket +0.10 | 0 heroes |
| Healbane | 1,600 | +0.014 | +0.009 | +0.076 | Lash +0.11, Violet +0.05, Pocket +0.04 | 17 heroes |
| Bullet Resilience | 3,200 | +0.017 | +0.005 | +0.070 | Paradox +0.13, Lash +0.11, Venator +0.10 | 0 heroes |
| Plated Armor | 6,400 | +0.020 | +0.003 | +0.105 | Holliday +0.14, Haze +0.14, Paradox +0.13 | 0 heroes |
| Counterspell | 3,200 | -0.007 | -0.002 | +0.044 | Lash +0.07, Deadman Danny +0.05, Pocket +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.022 | -0.004 | +0.098 | Abrams +0.17, Ivy +0.14, Rem +0.13 | 0 heroes |
| Metal Skin | 3,200 | -0.111 | -0.035 | +0.092 | Wraith +0.20, Paradox +0.17, Lash +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.145 | -0.090 | +0.057 | Vindicta +0.07, Lash +0.07, Wraith +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.08 (+0.14), Unstoppable +0.04 (+0.14), Healbane +0.03 (+0.11)
- **Seven**: Witchmail +0.04 (+0.19), Counterspell +0.00 (+0.05), Healbane +0.00 (+0.08)
- **Vindicta**: Return Fire +0.07 (+0.13), Divine Barrier +0.05 (+0.12), Bullet Resilience +0.04 (+0.11)
- **Lady Geist**: Return Fire +0.05 (+0.11), Divine Barrier +0.05 (+0.12), Metal Skin +0.02 (+0.11)
- **Abrams**: Unstoppable +0.17 (+0.27), Indomitable +0.05 (+0.18), Dispel Magic +0.04 (+0.10)
- **Wraith**: Metal Skin +0.20 (+0.30), Indomitable +0.20 (+0.32), Spirit Resilience +0.12 (+0.23)
- **McGinnis**: Healbane +0.00 (+0.08), Counterspell -0.01 (+0.04), Spirit Resilience -0.01 (+0.10)
- **Paradox**: Metal Skin +0.17 (+0.26), Plated Armor +0.13 (+0.24), Bullet Resilience +0.13 (+0.20)
- **Dynamo**: Healbane +0.00 (+0.08), Counterspell -0.01 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.02 (+0.13), Dispel Magic -0.00 (+0.06), Healbane -0.01 (+0.07)
- **Haze**: Plated Armor +0.14 (+0.24), Bullet Resilience +0.09 (+0.16), Indomitable +0.08 (+0.20)
- **Holliday**: Plated Armor +0.14 (+0.25), Spellbreaker +0.03 (+0.15), Return Fire +0.03 (+0.09)
- **Bebop**: Witchmail +0.06 (+0.21), Divine Barrier +0.04 (+0.11), Counterspell +0.04 (+0.08)
- **Calico**: Reactive Barrier +0.03 (+0.07), Divine Barrier +0.00 (+0.07), Spirit Resilience -0.01 (+0.10)
- **Grey Talon**: Reactive Barrier +0.03 (+0.07), Spellbreaker +0.03 (+0.15), Debuff Reducer +0.03 (+0.07)
- **Mo & Krill**: Unstoppable +0.10 (+0.19), Spellbreaker +0.07 (+0.19), Dispel Magic +0.04 (+0.10)
- **Shiv**: Divine Barrier +0.02 (+0.09), Return Fire +0.02 (+0.07), Bullet Resilience +0.02 (+0.08)
- **Ivy**: Unstoppable +0.14 (+0.24), Indomitable +0.04 (+0.17), Debuff Reducer +0.00 (+0.05)
- **Warden**: Return Fire +0.02 (+0.08), Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.05)
- **Yamato**: Healbane +0.03 (+0.11), Debuff Reducer -0.02 (+0.02), Reactive Barrier -0.04 (+0.00)
- **Lash**: Spirit Resilience +0.25 (+0.36), Spellbreaker +0.21 (+0.32), Divine Barrier +0.16 (+0.23)
- **Viscous**: Healbane -0.00 (+0.07), Return Fire -0.01 (+0.05), Counterspell -0.02 (+0.03)
- **Pocket**: Spirit Resilience +0.20 (+0.31), Spellbreaker +0.10 (+0.22), Witchmail +0.10 (+0.26)
- **Mirage**: Dispel Magic +0.31 (+0.37), Spirit Resilience +0.03 (+0.14), Spellbreaker +0.03 (+0.14)
- **Vyper**: Indomitable +0.32 (+0.44), Debuff Reducer +0.05 (+0.10), Metal Skin +0.05 (+0.14)
- **Sinclair**: Indomitable +0.10 (+0.22), Spellbreaker +0.04 (+0.16), Return Fire +0.01 (+0.07)
- **Mina**: Spirit Resilience +0.11 (+0.22), Witchmail +0.07 (+0.23), Divine Barrier +0.07 (+0.14)
- **Drifter**: Witchmail +0.09 (+0.24), Metal Skin +0.08 (+0.17), Spirit Resilience +0.08 (+0.19)
- **Venator**: Bullet Resilience +0.10 (+0.17), Plated Armor +0.04 (+0.15), Metal Skin +0.04 (+0.13)
- **Victor**: Spellbreaker +0.08 (+0.20), Spirit Resilience +0.06 (+0.17), Healbane +0.01 (+0.08)
- **Paige**: Return Fire +0.00 (+0.06), Counterspell +0.00 (+0.05), Healbane -0.02 (+0.06)
- **The Doorman**: Indomitable +0.33 (+0.45), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.03)
- **Billy**: Spirit Resilience +0.03 (+0.14), Spellbreaker +0.01 (+0.12), Plated Armor -0.01 (+0.10)
- **Graves**: Witchmail +0.16 (+0.32), Spirit Resilience +0.15 (+0.26), Metal Skin +0.12 (+0.21)
- **Apollo**: Healbane +0.01 (+0.08), Reactive Barrier -0.00 (+0.04), Indomitable -0.02 (+0.10)
- **Deadman Danny**: Indomitable +0.10 (+0.22), Spellbreaker +0.09 (+0.21), Witchmail +0.09 (+0.25)
- **Rem**: Unstoppable +0.13 (+0.23), Indomitable +0.11 (+0.24), Counterspell -0.01 (+0.03)
- **Silver**: Dispel Magic +0.14 (+0.20), Metal Skin +0.04 (+0.13), Reactive Barrier +0.02 (+0.06)
- **Celeste**: Witchmail +0.03 (+0.18), Spirit Resilience +0.01 (+0.12), Healbane -0.00 (+0.07)
- **Rat King**: Return Fire -0.01 (+0.05), Bullet Resilience -0.01 (+0.05), Counterspell -0.01 (+0.03)
- **Solomon**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.02)
- **Violet**: Unstoppable +0.10 (+0.20), Dispel Magic +0.06 (+0.13), Indomitable +0.06 (+0.18)
- **Nurse Harrow**: Healbane +0.00 (+0.08), Counterspell -0.01 (+0.03), Witchmail -0.02 (+0.13)
- **Baba**: Return Fire +0.01 (+0.07), Healbane +0.00 (+0.08), Unstoppable -0.00 (+0.09)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.201 | +0.063 | +0.109 | Lash +0.17, Wraith +0.17, Grey Talon +0.15 | 13 heroes |
| Divine Barrier | 6,400 | +0.244 | +0.039 | +0.057 | Wraith +0.13, Paradox +0.11, Lash +0.09 | 2 heroes |
| Dispel Magic | 3,200 | +0.110 | +0.034 | +0.053 | Mirage +0.29, Violet +0.15, Infernus +0.13 | 9 heroes |
| Witchmail | 6,400 | +0.198 | +0.031 | +0.153 | Wraith +0.14, Lash +0.12, Paradox +0.10 | 1 heroes |
| Indomitable | 6,400 | +0.172 | +0.028 | +0.123 | Vyper +0.34, The Doorman +0.33, Wraith +0.28 | 0 heroes |
| Spellbreaker | 6,400 | +0.150 | +0.024 | +0.119 | Grey Talon +0.19, Wraith +0.16, Lash +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.038 | Grey Talon +0.11, Vyper +0.08, Wraith +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.022 | +0.014 | +0.036 | Wraith +0.13, Violet +0.11, Grey Talon +0.10 | 5 heroes |
| Plated Armor | 6,400 | +0.017 | +0.003 | +0.101 | Holliday +0.18, Wraith +0.17, Haze +0.10 | 0 heroes |
| Bullet Resilience | 3,200 | -0.007 | -0.002 | +0.058 | Paradox +0.12, Wraith +0.09, Venator +0.08 | 1 heroes |
| Healbane | 1,600 | -0.006 | -0.004 | +0.059 | Yamato +0.05, Infernus +0.05, Nurse Harrow +0.03 | 16 heroes |
| Unstoppable | 6,400 | -0.028 | -0.004 | +0.095 | Rem +0.23, Violet +0.21, Ivy +0.18 | 3 heroes |
| Counterspell | 3,200 | -0.021 | -0.007 | +0.031 | Lash +0.03, Paradox +0.03, Lady Geist +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.113 | -0.035 | +0.092 | Wraith +0.25, Paradox +0.14, Lash +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.148 | -0.093 | +0.049 | Paradox +0.09, Wraith +0.07, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.14 (+0.23), Spellbreaker +0.14 (+0.26), Dispel Magic +0.13 (+0.18)
- **Seven**: Witchmail +0.05 (+0.20), Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Vindicta**: Return Fire +0.05 (+0.10), Bullet Resilience +0.04 (+0.10), Divine Barrier +0.02 (+0.08)
- **Lady Geist**: Divine Barrier +0.05 (+0.10), Bullet Resilience +0.05 (+0.10), Return Fire +0.04 (+0.09)
- **Abrams**: Unstoppable +0.11 (+0.20), Dispel Magic +0.04 (+0.09), Healbane +0.03 (+0.09)
- **Wraith**: Indomitable +0.28 (+0.41), Metal Skin +0.25 (+0.34), Plated Armor +0.17 (+0.28)
- **McGinnis**: Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05), Debuff Reducer -0.02 (+0.02)
- **Paradox**: Metal Skin +0.14 (+0.23), Spellbreaker +0.13 (+0.25), Bullet Resilience +0.12 (+0.18)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.00 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Counterspell +0.00 (+0.04), Healbane -0.00 (+0.05), Dispel Magic -0.01 (+0.04)
- **Haze**: Plated Armor +0.10 (+0.20), Unstoppable +0.09 (+0.18), Indomitable +0.09 (+0.21)
- **Holliday**: Plated Armor +0.18 (+0.28), Spellbreaker +0.06 (+0.18), Debuff Reducer +0.06 (+0.09)
- **Bebop**: Healbane +0.02 (+0.08), Metal Skin +0.01 (+0.10), Divine Barrier -0.00 (+0.06)
- **Calico**: Reactive Barrier +0.02 (+0.05), Divine Barrier +0.00 (+0.06), Spellbreaker +0.00 (+0.12)
- **Grey Talon**: Spellbreaker +0.19 (+0.30), Unstoppable +0.16 (+0.26), Spirit Resilience +0.15 (+0.26)
- **Mo & Krill**: Unstoppable +0.11 (+0.20), Spellbreaker +0.06 (+0.17), Dispel Magic +0.03 (+0.08)
- **Shiv**: Metal Skin +0.05 (+0.15), Bullet Resilience +0.04 (+0.09), Plated Armor +0.02 (+0.13)
- **Ivy**: Unstoppable +0.18 (+0.27), Indomitable +0.11 (+0.24), Dispel Magic +0.05 (+0.10)
- **Warden**: Return Fire +0.01 (+0.06), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Yamato**: Healbane +0.05 (+0.11), Debuff Reducer +0.01 (+0.04), Counterspell -0.00 (+0.03)
- **Lash**: Spirit Resilience +0.17 (+0.28), Spellbreaker +0.14 (+0.26), Witchmail +0.12 (+0.27)
- **Viscous**: Healbane +0.03 (+0.09), Return Fire +0.02 (+0.07), Divine Barrier +0.02 (+0.07)
- **Pocket**: Spirit Resilience +0.06 (+0.17), Counterspell +0.02 (+0.05), Return Fire +0.00 (+0.05)
- **Mirage**: Dispel Magic +0.29 (+0.34), Spirit Resilience +0.03 (+0.14), Spellbreaker +0.02 (+0.14)
- **Vyper**: Indomitable +0.34 (+0.47), Debuff Reducer +0.08 (+0.11), Spellbreaker +0.06 (+0.17)
- **Sinclair**: Indomitable +0.15 (+0.27), Spellbreaker +0.02 (+0.14), Debuff Reducer +0.01 (+0.05)
- **Mina**: Spirit Resilience +0.13 (+0.23), Divine Barrier +0.08 (+0.14), Witchmail +0.07 (+0.22)
- **Drifter**: Spirit Resilience +0.09 (+0.20), Witchmail +0.06 (+0.21), Metal Skin +0.06 (+0.15)
- **Venator**: Bullet Resilience +0.08 (+0.13), Metal Skin +0.07 (+0.16), Plated Armor +0.03 (+0.13)
- **Victor**: Spirit Resilience +0.04 (+0.15), Healbane +0.03 (+0.09), Spellbreaker +0.02 (+0.14)
- **Paige**: Counterspell +0.00 (+0.04), Return Fire -0.00 (+0.04), Witchmail -0.02 (+0.14)
- **The Doorman**: Indomitable +0.33 (+0.45), Counterspell -0.01 (+0.02), Return Fire -0.02 (+0.03)
- **Billy**: Spellbreaker +0.01 (+0.13), Reactive Barrier +0.01 (+0.05), Spirit Resilience +0.00 (+0.11)
- **Graves**: Return Fire +0.02 (+0.07), Witchmail +0.01 (+0.17), Metal Skin +0.01 (+0.10)
- **Apollo**: Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04), Divine Barrier +0.01 (+0.06)
- **Deadman Danny**: Spellbreaker +0.09 (+0.21), Witchmail +0.08 (+0.23), Indomitable +0.08 (+0.20)
- **Rem**: Unstoppable +0.23 (+0.32), Debuff Reducer -0.00 (+0.04), Counterspell -0.01 (+0.02)
- **Silver**: Dispel Magic +0.12 (+0.17), Metal Skin +0.03 (+0.12), Counterspell +0.01 (+0.04)
- **Celeste**: Witchmail +0.10 (+0.25), Dispel Magic +0.09 (+0.14), Spirit Resilience +0.07 (+0.18)
- **Rat King**: Counterspell -0.01 (+0.02), Return Fire -0.01 (+0.04), Bullet Resilience -0.02 (+0.04)
- **Solomon**: Return Fire +0.00 (+0.05), Counterspell -0.01 (+0.02), Debuff Reducer -0.02 (+0.02)
- **Violet**: Unstoppable +0.21 (+0.31), Dispel Magic +0.15 (+0.20), Indomitable +0.13 (+0.25)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Counterspell +0.02 (+0.05), Spirit Resilience -0.00 (+0.11)
- **Baba**: Return Fire +0.02 (+0.07), Healbane +0.00 (+0.06), Counterspell -0.00 (+0.03)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.234 | +0.073 | +0.125 | Lash +0.38, Deadman Danny +0.36, Grey Talon +0.15 | 14 heroes |
| Dispel Magic | 3,200 | +0.125 | +0.039 | +0.070 | Mirage +0.34, Drifter +0.29, Lash +0.18 | 9 heroes |
| Divine Barrier | 6,400 | +0.195 | +0.030 | +0.051 | Lash +0.18, Calico +0.11, Viscous +0.08 | 3 heroes |
| Indomitable | 6,400 | +0.181 | +0.029 | +0.127 | The Doorman +0.43, Vyper +0.28, Deadman Danny +0.17 | 1 heroes |
| Witchmail | 6,400 | +0.185 | +0.029 | +0.142 | Deadman Danny +0.23, Lash +0.21, Vindicta +0.11 | 2 heroes |
| Spellbreaker | 6,400 | +0.176 | +0.028 | +0.138 | Deadman Danny +0.31, Lash +0.27, Grey Talon +0.18 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.046 | Grey Talon +0.13, Paige +0.09, Bebop +0.07 | 0 heroes |
| Unstoppable | 6,400 | +0.019 | +0.003 | +0.146 | Paige +0.31, Wraith +0.25, Ivy +0.17 | 8 heroes |
| Plated Armor | 6,400 | +0.008 | +0.001 | +0.101 | Deadman Danny +0.21, Wraith +0.14, Lash +0.11 | 2 heroes |
| Reactive Barrier | 1,600 | -0.002 | -0.001 | +0.034 | Deadman Danny +0.12, Drifter +0.09, Wraith +0.08 | 3 heroes |
| Healbane | 1,600 | -0.003 | -0.002 | +0.058 | Yamato +0.05, Infernus +0.05, Vindicta +0.05 | 13 heroes |
| Bullet Resilience | 3,200 | -0.017 | -0.005 | +0.057 | Vindicta +0.12, Lash +0.11, Venator +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.026 | -0.008 | +0.031 | Wraith +0.03, Grey Talon +0.03, Nurse Harrow +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.110 | -0.035 | +0.098 | Lash +0.23, Wraith +0.16, Venator +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.156 | -0.097 | +0.043 | Paradox +0.07, Vindicta +0.05, Holliday +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.30), Dispel Magic +0.06 (+0.13), Indomitable +0.05 (+0.18)
- **Seven**: Witchmail +0.03 (+0.17), Counterspell +0.00 (+0.04), Healbane -0.01 (+0.04)
- **Vindicta**: Bullet Resilience +0.12 (+0.18), Witchmail +0.11 (+0.25), Plated Armor +0.10 (+0.20)
- **Lady Geist**: Bullet Resilience +0.06 (+0.12), Metal Skin +0.04 (+0.13), Dispel Magic +0.03 (+0.10)
- **Abrams**: Unstoppable +0.07 (+0.22), Healbane +0.04 (+0.10), Debuff Reducer +0.01 (+0.05)
- **Wraith**: Unstoppable +0.25 (+0.40), Metal Skin +0.16 (+0.25), Indomitable +0.15 (+0.28)
- **McGinnis**: Healbane -0.00 (+0.06), Spirit Resilience -0.00 (+0.12), Counterspell -0.01 (+0.02)
- **Paradox**: Dispel Magic +0.12 (+0.19), Unstoppable +0.12 (+0.27), Metal Skin +0.10 (+0.20)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.02), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.14 (+0.27), Witchmail +0.07 (+0.21), Spellbreaker +0.04 (+0.18)
- **Haze**: Unstoppable +0.14 (+0.29), Indomitable +0.05 (+0.17), Return Fire +0.04 (+0.08)
- **Holliday**: Spellbreaker +0.06 (+0.20), Debuff Reducer +0.05 (+0.10), Return Fire +0.04 (+0.08)
- **Bebop**: Debuff Reducer +0.07 (+0.12), Spellbreaker +0.07 (+0.21), Indomitable +0.03 (+0.15)
- **Calico**: Spirit Resilience +0.12 (+0.24), Divine Barrier +0.11 (+0.16), Reactive Barrier +0.07 (+0.11)
- **Grey Talon**: Spellbreaker +0.18 (+0.31), Spirit Resilience +0.15 (+0.28), Debuff Reducer +0.13 (+0.18)
- **Mo & Krill**: Unstoppable +0.04 (+0.19), Spellbreaker +0.02 (+0.16), Debuff Reducer +0.01 (+0.05)
- **Shiv**: Metal Skin +0.06 (+0.16), Bullet Resilience +0.05 (+0.11), Divine Barrier +0.05 (+0.10)
- **Ivy**: Unstoppable +0.17 (+0.32), Indomitable +0.12 (+0.25), Debuff Reducer +0.05 (+0.09)
- **Warden**: Return Fire +0.03 (+0.07), Metal Skin +0.02 (+0.12), Healbane +0.01 (+0.07)
- **Yamato**: Healbane +0.05 (+0.11), Reactive Barrier +0.01 (+0.05), Indomitable +0.01 (+0.14)
- **Lash**: Spirit Resilience +0.38 (+0.50), Spellbreaker +0.27 (+0.41), Metal Skin +0.23 (+0.32)
- **Viscous**: Witchmail +0.10 (+0.24), Spirit Resilience +0.09 (+0.21), Divine Barrier +0.08 (+0.13)
- **Pocket**: Spirit Resilience +0.07 (+0.20), Witchmail +0.05 (+0.19), Spellbreaker +0.02 (+0.15)
- **Mirage**: Dispel Magic +0.34 (+0.41), Metal Skin +0.11 (+0.21), Plated Armor +0.04 (+0.14)
- **Vyper**: Indomitable +0.28 (+0.41), Plated Armor +0.09 (+0.19), Metal Skin +0.08 (+0.17)
- **Sinclair**: Indomitable +0.15 (+0.28), Reactive Barrier +0.06 (+0.09), Spirit Resilience +0.06 (+0.18)
- **Mina**: Counterspell +0.01 (+0.04), Divine Barrier +0.01 (+0.06), Return Fire +0.00 (+0.04)
- **Drifter**: Dispel Magic +0.29 (+0.36), Reactive Barrier +0.09 (+0.13), Metal Skin +0.07 (+0.17)
- **Venator**: Metal Skin +0.16 (+0.25), Bullet Resilience +0.08 (+0.14), Plated Armor +0.03 (+0.13)
- **Victor**: Spellbreaker +0.07 (+0.21), Healbane +0.02 (+0.08), Spirit Resilience +0.01 (+0.14)
- **Paige**: Unstoppable +0.31 (+0.46), Debuff Reducer +0.09 (+0.13), Indomitable +0.01 (+0.13)
- **The Doorman**: Indomitable +0.43 (+0.56), Counterspell +0.00 (+0.03), Reactive Barrier -0.01 (+0.02)
- **Billy**: Spellbreaker +0.00 (+0.14), Reactive Barrier -0.00 (+0.03), Return Fire -0.01 (+0.03)
- **Graves**: Spirit Resilience +0.05 (+0.17), Witchmail +0.03 (+0.18), Return Fire +0.02 (+0.07)
- **Apollo**: Reactive Barrier +0.04 (+0.07), Healbane +0.01 (+0.07), Divine Barrier +0.00 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.36 (+0.49), Spellbreaker +0.31 (+0.45), Witchmail +0.23 (+0.37)
- **Rem**: Unstoppable +0.17 (+0.31), Counterspell -0.01 (+0.02), Return Fire -0.01 (+0.03)
- **Silver**: Dispel Magic +0.04 (+0.11), Debuff Reducer -0.00 (+0.05), Return Fire -0.01 (+0.04)
- **Celeste**: Spirit Resilience +0.05 (+0.18), Witchmail +0.04 (+0.18), Dispel Magic +0.02 (+0.09)
- **Rat King**: Return Fire +0.02 (+0.06), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05)
- **Solomon**: Return Fire +0.02 (+0.06), Reactive Barrier +0.00 (+0.04), Counterspell +0.00 (+0.03)
- **Violet**: Unstoppable +0.09 (+0.23), Spirit Resilience +0.05 (+0.18), Indomitable +0.05 (+0.17)
- **Nurse Harrow**: Spirit Resilience +0.09 (+0.22), Dispel Magic +0.09 (+0.16), Witchmail +0.05 (+0.19)
- **Baba**: Unstoppable +0.02 (+0.17), Healbane +0.02 (+0.08), Witchmail +0.01 (+0.15)
