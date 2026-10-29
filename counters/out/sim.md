# Counter items in the sim (phantom and up)

Built 2026-10-29T00:11:28Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.187 | +0.059 | +0.120 | Lash +0.30, Deadman Danny +0.24, Graves +0.12 | 1 heroes |
| Divine Barrier | 6,400 | +0.360 | +0.058 | +0.096 | Lash +0.25, Deadman Danny +0.12, Calico +0.12 | 0 heroes |
| Dispel Magic | 3,200 | +0.095 | +0.030 | +0.074 | Mirage +0.32, Deadman Danny +0.16, Infernus +0.13 | 3 heroes |
| Reactive Barrier | 1,600 | +0.043 | +0.027 | +0.061 | Deadman Danny +0.19, Calico +0.13, Paradox +0.09 | 3 heroes |
| Indomitable | 6,400 | +0.163 | +0.026 | +0.143 | Deadman Danny +0.28, Vyper +0.27, Abrams +0.22 | 0 heroes |
| Witchmail | 6,400 | +0.153 | +0.024 | +0.200 | Deadman Danny +0.26, Lash +0.20, Graves +0.11 | 0 heroes |
| Debuff Reducer | 1,600 | +0.032 | +0.020 | +0.071 | Deadman Danny +0.14, Vyper +0.11, Wraith +0.10 | 0 heroes |
| Spellbreaker | 6,400 | +0.087 | +0.014 | +0.157 | Deadman Danny +0.29, Lash +0.26, Holliday +0.14 | 0 heroes |
| Bullet Resilience | 3,200 | -0.003 | -0.001 | +0.085 | Deadman Danny +0.19, Venator +0.15, Lash +0.11 | 0 heroes |
| Plated Armor | 6,400 | -0.038 | -0.006 | +0.119 | Deadman Danny +0.23, Holliday +0.21, Wraith +0.13 | 0 heroes |
| Counterspell | 3,200 | -0.024 | -0.007 | +0.071 | Deadman Danny +0.15, Wraith +0.05, Lash +0.04 | 1 heroes |
| Healbane | 1,600 | -0.015 | -0.009 | +0.085 | Deadman Danny +0.08, Billy +0.04, Wraith +0.04 | 11 heroes |
| Unstoppable | 6,400 | -0.060 | -0.009 | +0.127 | Deadman Danny +0.22, Abrams +0.12, Holliday +0.11 | 0 heroes |
| Metal Skin | 3,200 | -0.164 | -0.051 | +0.098 | Lash +0.20, Wraith +0.15, Graves +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.177 | -0.111 | +0.075 | Deadman Danny +0.11, The Doorman +0.07, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.13 (+0.20), Spellbreaker +0.09 (+0.24), Unstoppable +0.06 (+0.19)
- **Seven**: Healbane -0.01 (+0.08), Counterspell -0.02 (+0.05), Metal Skin -0.03 (+0.07)
- **Vindicta**: Return Fire +0.01 (+0.08), Witchmail -0.01 (+0.19), Counterspell -0.01 (+0.06)
- **Lady Geist**: Return Fire +0.02 (+0.10), Healbane -0.00 (+0.08), Counterspell -0.01 (+0.06)
- **Abrams**: Indomitable +0.22 (+0.36), Unstoppable +0.12 (+0.25), Spirit Resilience +0.08 (+0.20)
- **Wraith**: Indomitable +0.18 (+0.32), Metal Skin +0.15 (+0.25), Plated Armor +0.13 (+0.25)
- **McGinnis**: Spirit Resilience -0.01 (+0.11), Healbane -0.01 (+0.07), Return Fire -0.02 (+0.06)
- **Paradox**: Metal Skin +0.11 (+0.21), Bullet Resilience +0.09 (+0.18), Reactive Barrier +0.09 (+0.15)
- **Dynamo**: Healbane -0.01 (+0.08), Counterspell -0.03 (+0.04), Reactive Barrier -0.05 (+0.01)
- **Kelvin**: Spirit Resilience +0.02 (+0.14), Witchmail +0.01 (+0.21), Counterspell +0.01 (+0.08)
- **Haze**: Indomitable +0.09 (+0.24), Unstoppable +0.07 (+0.19), Plated Armor +0.04 (+0.16)
- **Holliday**: Plated Armor +0.21 (+0.33), Spellbreaker +0.14 (+0.29), Unstoppable +0.11 (+0.24)
- **Bebop**: Healbane +0.03 (+0.12), Counterspell +0.01 (+0.08), Return Fire +0.00 (+0.08)
- **Calico**: Reactive Barrier +0.13 (+0.19), Divine Barrier +0.12 (+0.21), Spellbreaker +0.11 (+0.26)
- **Grey Talon**: Unstoppable +0.06 (+0.19), Debuff Reducer +0.04 (+0.11), Reactive Barrier +0.03 (+0.09)
- **Mo & Krill**: Spellbreaker +0.13 (+0.29), Spirit Resilience +0.08 (+0.20), Dispel Magic +0.07 (+0.14)
- **Shiv**: Healbane -0.02 (+0.07), Return Fire -0.03 (+0.05), Divine Barrier -0.03 (+0.07)
- **Ivy**: Indomitable +0.11 (+0.25), Unstoppable +0.08 (+0.21), Bullet Resilience +0.01 (+0.09)
- **Warden**: Return Fire +0.02 (+0.09), Debuff Reducer +0.01 (+0.08), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.03 (+0.12), Debuff Reducer -0.02 (+0.05), Counterspell -0.02 (+0.05)
- **Lash**: Spirit Resilience +0.30 (+0.42), Spellbreaker +0.26 (+0.42), Divine Barrier +0.25 (+0.34)
- **Viscous**: Counterspell -0.02 (+0.05), Healbane -0.03 (+0.05), Return Fire -0.04 (+0.04)
- **Pocket**: Spirit Resilience +0.04 (+0.16), Witchmail +0.04 (+0.24), Return Fire +0.03 (+0.10)
- **Mirage**: Dispel Magic +0.32 (+0.40), Spellbreaker +0.08 (+0.23), Plated Armor +0.06 (+0.18)
- **Vyper**: Indomitable +0.27 (+0.41), Debuff Reducer +0.11 (+0.18), Unstoppable +0.08 (+0.21)
- **Sinclair**: Indomitable +0.14 (+0.28), Spellbreaker +0.08 (+0.23), Unstoppable +0.03 (+0.16)
- **Mina**: Return Fire +0.02 (+0.10), Counterspell -0.00 (+0.07), Spirit Resilience -0.00 (+0.12)
- **Drifter**: Return Fire -0.01 (+0.07), Counterspell -0.01 (+0.06), Healbane -0.01 (+0.08)
- **Venator**: Bullet Resilience +0.15 (+0.24), Divine Barrier +0.08 (+0.18), Debuff Reducer +0.07 (+0.14)
- **Victor**: Healbane +0.02 (+0.10), Spirit Resilience -0.00 (+0.12), Dispel Magic -0.02 (+0.06)
- **Paige**: Return Fire -0.00 (+0.07), Counterspell -0.01 (+0.06), Healbane -0.03 (+0.06)
- **The Doorman**: Indomitable +0.15 (+0.29), Spirit Resilience +0.12 (+0.24), Spellbreaker +0.11 (+0.27)
- **Billy**: Spellbreaker +0.09 (+0.25), Healbane +0.04 (+0.12), Spirit Resilience +0.03 (+0.15)
- **Graves**: Metal Skin +0.14 (+0.24), Spirit Resilience +0.12 (+0.24), Witchmail +0.11 (+0.31)
- **Apollo**: Reactive Barrier +0.01 (+0.07), Unstoppable -0.00 (+0.12), Indomitable -0.01 (+0.13)
- **Deadman Danny**: Spellbreaker +0.29 (+0.45), Indomitable +0.28 (+0.42), Witchmail +0.26 (+0.46)
- **Rem**: Witchmail -0.01 (+0.19), Dispel Magic -0.01 (+0.06), Debuff Reducer -0.01 (+0.06)
- **Silver**: Dispel Magic +0.04 (+0.11), Debuff Reducer +0.03 (+0.10), Metal Skin +0.02 (+0.11)
- **Celeste**: Spirit Resilience +0.06 (+0.18), Witchmail +0.06 (+0.26), Dispel Magic +0.03 (+0.10)
- **Rat King**: Bullet Resilience +0.00 (+0.09), Return Fire +0.00 (+0.08), Metal Skin -0.00 (+0.09)
- **Solomon**: Return Fire -0.00 (+0.07), Counterspell -0.03 (+0.04), Healbane -0.04 (+0.05)
- **Violet**: Return Fire -0.00 (+0.07), Healbane -0.02 (+0.07), Counterspell -0.04 (+0.03)
- **Nurse Harrow**: Healbane +0.01 (+0.09), Counterspell -0.03 (+0.04), Return Fire -0.04 (+0.03)
- **Baba**: Healbane -0.00 (+0.08), Unstoppable -0.02 (+0.11), Debuff Reducer -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.160 | +0.050 | +0.101 | Lash +0.34, Graves +0.18, Pocket +0.18 | 10 heroes |
| Divine Barrier | 6,400 | +0.285 | +0.045 | +0.059 | Lash +0.19, The Doorman +0.10, Paradox +0.09 | 1 heroes |
| Dispel Magic | 3,200 | +0.085 | +0.027 | +0.049 | Mirage +0.27, Infernus +0.11, Deadman Danny +0.09 | 6 heroes |
| Witchmail | 6,400 | +0.146 | +0.023 | +0.152 | Lash +0.18, Graves +0.14, Deadman Danny +0.12 | 0 heroes |
| Indomitable | 6,400 | +0.140 | +0.023 | +0.104 | Vyper +0.40, Wraith +0.20, Deadman Danny +0.17 | 0 heroes |
| Spellbreaker | 6,400 | +0.101 | +0.016 | +0.122 | Lash +0.35, Vyper +0.17, Mo & Krill +0.12 | 0 heroes |
| Reactive Barrier | 1,600 | +0.022 | +0.014 | +0.036 | Deadman Danny +0.10, Vyper +0.10, The Doorman +0.09 | 4 heroes |
| Debuff Reducer | 1,600 | +0.005 | +0.004 | +0.048 | Rem +0.12, Wraith +0.11, Vyper +0.10 | 1 heroes |
| Plated Armor | 6,400 | -0.036 | -0.006 | +0.087 | Holliday +0.19, Deadman Danny +0.16, Graves +0.11 | 0 heroes |
| Bullet Resilience | 3,200 | -0.035 | -0.011 | +0.052 | Venator +0.13, Paradox +0.11, Lash +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.036 | -0.011 | +0.044 | Deadman Danny +0.09, Paradox +0.05, Vindicta +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.087 | -0.014 | +0.093 | Abrams +0.19, Vyper +0.10, Rem +0.10 | 0 heroes |
| Healbane | 1,600 | -0.043 | -0.027 | +0.066 | Nurse Harrow +0.07, Yamato +0.04, Abrams +0.04 | 17 heroes |
| Metal Skin | 3,200 | -0.184 | -0.058 | +0.069 | Graves +0.16, Paradox +0.14, Wraith +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.184 | -0.115 | +0.051 | Paradox +0.08, Graves +0.05, The Doorman +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.16), Spellbreaker +0.08 (+0.20), Unstoppable +0.06 (+0.15)
- **Seven**: Witchmail +0.01 (+0.16), Counterspell -0.01 (+0.04), Metal Skin -0.01 (+0.06)
- **Vindicta**: Witchmail +0.06 (+0.21), Counterspell +0.04 (+0.08), Divine Barrier +0.04 (+0.10)
- **Lady Geist**: Return Fire +0.04 (+0.09), Divine Barrier +0.03 (+0.08), Metal Skin +0.01 (+0.08)
- **Abrams**: Unstoppable +0.19 (+0.28), Indomitable +0.10 (+0.20), Divine Barrier +0.06 (+0.12)
- **Wraith**: Indomitable +0.20 (+0.30), Metal Skin +0.14 (+0.21), Debuff Reducer +0.11 (+0.16)
- **McGinnis**: Spirit Resilience +0.06 (+0.16), Counterspell +0.04 (+0.08), Dispel Magic +0.04 (+0.09)
- **Paradox**: Metal Skin +0.14 (+0.21), Bullet Resilience +0.11 (+0.17), Plated Armor +0.11 (+0.20)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.02 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.07 (+0.17), Dispel Magic +0.05 (+0.10), Witchmail +0.04 (+0.19)
- **Haze**: Indomitable +0.08 (+0.19), Unstoppable +0.05 (+0.15), Plated Armor +0.05 (+0.13)
- **Holliday**: Plated Armor +0.19 (+0.27), Spellbreaker +0.06 (+0.18), Indomitable +0.04 (+0.15)
- **Bebop**: Healbane +0.01 (+0.07), Return Fire -0.03 (+0.03), Counterspell -0.03 (+0.02)
- **Calico**: Divine Barrier +0.05 (+0.11), Reactive Barrier +0.05 (+0.08), Dispel Magic +0.02 (+0.07)
- **Grey Talon**: Unstoppable +0.07 (+0.16), Spellbreaker +0.06 (+0.18), Debuff Reducer +0.06 (+0.11)
- **Mo & Krill**: Spellbreaker +0.12 (+0.25), Spirit Resilience +0.10 (+0.20), Unstoppable +0.09 (+0.18)
- **Shiv**: Bullet Resilience +0.04 (+0.09), Divine Barrier +0.04 (+0.10), Metal Skin +0.02 (+0.09)
- **Ivy**: Unstoppable +0.05 (+0.14), Indomitable +0.03 (+0.14), Debuff Reducer +0.01 (+0.06)
- **Warden**: Return Fire +0.03 (+0.08), Witchmail +0.02 (+0.17), Bullet Resilience +0.01 (+0.06)
- **Yamato**: Healbane +0.04 (+0.11), Counterspell -0.01 (+0.04), Debuff Reducer -0.01 (+0.04)
- **Lash**: Spellbreaker +0.35 (+0.47), Spirit Resilience +0.34 (+0.45), Divine Barrier +0.19 (+0.25)
- **Viscous**: Divine Barrier -0.00 (+0.05), Counterspell -0.01 (+0.03), Bullet Resilience -0.01 (+0.04)
- **Pocket**: Spirit Resilience +0.18 (+0.28), Spellbreaker +0.09 (+0.21), Witchmail +0.09 (+0.24)
- **Mirage**: Dispel Magic +0.27 (+0.32), Spirit Resilience +0.09 (+0.19), Metal Skin +0.07 (+0.14)
- **Vyper**: Indomitable +0.40 (+0.50), Spellbreaker +0.17 (+0.29), Reactive Barrier +0.10 (+0.14)
- **Sinclair**: Indomitable +0.09 (+0.20), Spellbreaker +0.06 (+0.19), Unstoppable +0.05 (+0.14)
- **Mina**: Return Fire +0.01 (+0.06), Counterspell -0.00 (+0.04), Spirit Resilience -0.01 (+0.09)
- **Drifter**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.04), Return Fire -0.01 (+0.04)
- **Venator**: Bullet Resilience +0.13 (+0.18), Metal Skin +0.12 (+0.19), Plated Armor +0.05 (+0.14)
- **Victor**: Spirit Resilience +0.07 (+0.17), Spellbreaker +0.05 (+0.17), Healbane -0.02 (+0.05)
- **Paige**: Return Fire +0.01 (+0.06), Counterspell -0.00 (+0.04), Healbane -0.02 (+0.05)
- **The Doorman**: Indomitable +0.14 (+0.25), Spirit Resilience +0.13 (+0.24), Witchmail +0.11 (+0.26)
- **Billy**: Spirit Resilience +0.04 (+0.14), Counterspell +0.03 (+0.07), Healbane +0.03 (+0.10)
- **Graves**: Spirit Resilience +0.18 (+0.28), Metal Skin +0.16 (+0.23), Witchmail +0.14 (+0.29)
- **Apollo**: Healbane +0.03 (+0.10), Reactive Barrier +0.03 (+0.06), Indomitable +0.01 (+0.11)
- **Deadman Danny**: Indomitable +0.17 (+0.27), Plated Armor +0.16 (+0.25), Spirit Resilience +0.15 (+0.25)
- **Rem**: Debuff Reducer +0.12 (+0.17), Unstoppable +0.10 (+0.19), Spellbreaker +0.05 (+0.17)
- **Silver**: Reactive Barrier +0.04 (+0.08), Metal Skin +0.01 (+0.08), Debuff Reducer +0.00 (+0.05)
- **Celeste**: Spirit Resilience +0.03 (+0.13), Witchmail +0.03 (+0.18), Metal Skin -0.00 (+0.07)
- **Rat King**: Bullet Resilience -0.00 (+0.05), Return Fire -0.00 (+0.05), Metal Skin -0.01 (+0.06)
- **Solomon**: Return Fire +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Violet**: Healbane +0.02 (+0.08), Return Fire +0.02 (+0.07), Witchmail -0.01 (+0.14)
- **Nurse Harrow**: Healbane +0.07 (+0.14), Counterspell -0.01 (+0.03), Dispel Magic -0.02 (+0.03)
- **Baba**: Unstoppable +0.05 (+0.14), Healbane +0.01 (+0.07), Debuff Reducer +0.00 (+0.05)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.155 | +0.048 | +0.116 | Lash +0.33, Wraith +0.16, Deadman Danny +0.14 | 15 heroes |
| Divine Barrier | 6,400 | +0.270 | +0.043 | +0.058 | Lash +0.19, Shiv +0.06, Viscous +0.05 | 2 heroes |
| Dispel Magic | 3,200 | +0.093 | +0.029 | +0.055 | Mirage +0.26, Lash +0.23, Infernus +0.16 | 9 heroes |
| Indomitable | 6,400 | +0.151 | +0.024 | +0.124 | Vyper +0.37, Wraith +0.25, Sinclair +0.22 | 0 heroes |
| Witchmail | 6,400 | +0.142 | +0.022 | +0.162 | Lash +0.20, Wraith +0.13, The Doorman +0.10 | 1 heroes |
| Spellbreaker | 6,400 | +0.122 | +0.019 | +0.148 | Lash +0.29, Grey Talon +0.22, Wraith +0.20 | 0 heroes |
| Debuff Reducer | 1,600 | +0.012 | +0.008 | +0.065 | Grey Talon +0.16, Wraith +0.12, Paige +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | -0.001 | -0.001 | +0.035 | Yamato +0.11, Wraith +0.07, Deadman Danny +0.06 | 3 heroes |
| Plated Armor | 6,400 | -0.034 | -0.005 | +0.093 | Wraith +0.19, Yamato +0.11, Haze +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.076 | -0.012 | +0.109 | Mo & Krill +0.17, Grey Talon +0.17, Paige +0.11 | 3 heroes |
| Counterspell | 3,200 | -0.040 | -0.013 | +0.038 | Yamato +0.08, McGinnis +0.04, Deadman Danny +0.04 | 1 heroes |
| Bullet Resilience | 3,200 | -0.047 | -0.015 | +0.050 | Yamato +0.07, Vindicta +0.07, Shiv +0.07 | 1 heroes |
| Healbane | 1,600 | -0.042 | -0.026 | +0.068 | Yamato +0.11, Mo & Krill +0.06, Wraith +0.05 | 16 heroes |
| Metal Skin | 3,200 | -0.175 | -0.055 | +0.086 | Wraith +0.24, Lash +0.16, Shiv +0.07 | 0 heroes |
| Return Fire | 1,600 | -0.178 | -0.112 | +0.050 | Vindicta +0.07, Deadman Danny +0.05, Paradox +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.19 (+0.34), Dispel Magic +0.16 (+0.22), Unstoppable +0.11 (+0.22)
- **Seven**: Witchmail +0.01 (+0.18), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.01)
- **Vindicta**: Bullet Resilience +0.07 (+0.12), Return Fire +0.07 (+0.12), Plated Armor +0.06 (+0.15)
- **Lady Geist**: Return Fire +0.03 (+0.08), Healbane +0.02 (+0.09), Counterspell +0.01 (+0.05)
- **Abrams**: Unstoppable +0.08 (+0.19), Dispel Magic +0.02 (+0.07), Spirit Resilience -0.01 (+0.11)
- **Wraith**: Indomitable +0.25 (+0.38), Metal Skin +0.24 (+0.33), Spellbreaker +0.20 (+0.35)
- **McGinnis**: Spirit Resilience +0.07 (+0.19), Witchmail +0.05 (+0.21), Healbane +0.04 (+0.11)
- **Paradox**: Witchmail +0.07 (+0.23), Indomitable +0.06 (+0.18), Dispel Magic +0.05 (+0.11)
- **Dynamo**: Healbane -0.01 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.05 (+0.17), Counterspell +0.02 (+0.06), Healbane +0.00 (+0.07)
- **Haze**: Plated Armor +0.07 (+0.16), Bullet Resilience +0.05 (+0.10), Indomitable +0.05 (+0.17)
- **Holliday**: Spellbreaker +0.10 (+0.25), Debuff Reducer +0.10 (+0.17), Unstoppable +0.07 (+0.18)
- **Bebop**: Healbane +0.02 (+0.09), Return Fire -0.01 (+0.04), Metal Skin -0.02 (+0.07)
- **Calico**: Spirit Resilience +0.09 (+0.20), Reactive Barrier +0.06 (+0.09), Divine Barrier +0.05 (+0.11)
- **Grey Talon**: Spellbreaker +0.22 (+0.37), Unstoppable +0.17 (+0.28), Debuff Reducer +0.16 (+0.22)
- **Mo & Krill**: Unstoppable +0.17 (+0.28), Spellbreaker +0.14 (+0.29), Debuff Reducer +0.07 (+0.13)
- **Shiv**: Metal Skin +0.07 (+0.16), Bullet Resilience +0.07 (+0.12), Divine Barrier +0.06 (+0.12)
- **Ivy**: Unstoppable +0.05 (+0.15), Indomitable +0.01 (+0.14), Healbane -0.00 (+0.07)
- **Warden**: Return Fire +0.01 (+0.06), Debuff Reducer +0.01 (+0.08), Divine Barrier -0.01 (+0.05)
- **Yamato**: Indomitable +0.18 (+0.30), Reactive Barrier +0.11 (+0.15), Plated Armor +0.11 (+0.20)
- **Lash**: Spirit Resilience +0.33 (+0.45), Spellbreaker +0.29 (+0.44), Dispel Magic +0.23 (+0.29)
- **Viscous**: Divine Barrier +0.05 (+0.11), Return Fire +0.03 (+0.08), Counterspell +0.01 (+0.05)
- **Pocket**: Spirit Resilience +0.09 (+0.20), Witchmail +0.02 (+0.18), Spellbreaker +0.01 (+0.16)
- **Mirage**: Dispel Magic +0.26 (+0.31), Spirit Resilience +0.04 (+0.16), Plated Armor +0.02 (+0.12)
- **Vyper**: Indomitable +0.37 (+0.49), Spellbreaker +0.12 (+0.27), Debuff Reducer +0.10 (+0.17)
- **Sinclair**: Indomitable +0.22 (+0.35), Spellbreaker +0.15 (+0.30), Debuff Reducer +0.09 (+0.15)
- **Mina**: Spirit Resilience +0.06 (+0.17), Witchmail +0.05 (+0.22), Divine Barrier +0.05 (+0.10)
- **Drifter**: Witchmail +0.04 (+0.20), Healbane +0.01 (+0.08), Counterspell +0.00 (+0.04)
- **Venator**: Metal Skin +0.07 (+0.16), Bullet Resilience +0.06 (+0.11), Plated Armor +0.02 (+0.11)
- **Victor**: Spirit Resilience +0.02 (+0.14), Healbane +0.01 (+0.07), Dispel Magic -0.00 (+0.05)
- **Paige**: Unstoppable +0.11 (+0.22), Debuff Reducer +0.11 (+0.18), Spellbreaker +0.03 (+0.18)
- **The Doorman**: Indomitable +0.12 (+0.25), Witchmail +0.10 (+0.27), Spirit Resilience +0.08 (+0.20)
- **Billy**: Indomitable +0.07 (+0.20), Reactive Barrier +0.03 (+0.06), Debuff Reducer +0.03 (+0.09)
- **Graves**: Return Fire +0.04 (+0.09), Witchmail +0.02 (+0.18), Metal Skin +0.01 (+0.09)
- **Apollo**: Healbane +0.01 (+0.08), Reactive Barrier -0.00 (+0.03), Counterspell -0.01 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.14 (+0.26), Indomitable +0.13 (+0.26), Spellbreaker +0.13 (+0.27)
- **Rem**: Debuff Reducer +0.09 (+0.15), Unstoppable +0.06 (+0.17), Spellbreaker +0.03 (+0.18)
- **Silver**: Dispel Magic +0.07 (+0.12), Reactive Barrier +0.03 (+0.07), Divine Barrier +0.03 (+0.09)
- **Celeste**: Dispel Magic +0.04 (+0.10), Witchmail +0.04 (+0.20), Divine Barrier +0.01 (+0.06)
- **Rat King**: Bullet Resilience -0.01 (+0.04), Return Fire -0.01 (+0.04), Counterspell -0.01 (+0.03)
- **Solomon**: Counterspell +0.00 (+0.04), Return Fire -0.02 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Violet**: Healbane +0.01 (+0.08), Return Fire +0.01 (+0.06), Witchmail +0.00 (+0.17)
- **Nurse Harrow**: Healbane +0.02 (+0.09), Counterspell +0.01 (+0.05), Reactive Barrier -0.01 (+0.03)
- **Baba**: Unstoppable +0.00 (+0.11), Healbane +0.00 (+0.07), Return Fire -0.01 (+0.04)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.187 | +0.058 | +0.150 | Lash +0.49, The Doorman +0.41, Grey Talon +0.29 | 15 heroes |
| Divine Barrier | 6,400 | +0.234 | +0.036 | +0.060 | The Doorman +0.24, Lash +0.23, Viscous +0.19 | 3 heroes |
| Dispel Magic | 3,200 | +0.094 | +0.029 | +0.051 | Mirage +0.27, Lash +0.22, Silver +0.16 | 9 heroes |
| Indomitable | 6,400 | +0.170 | +0.027 | +0.157 | Wraith +0.35, Sinclair +0.28, Vyper +0.24 | 1 heroes |
| Spellbreaker | 6,400 | +0.153 | +0.024 | +0.194 | Lash +0.31, Grey Talon +0.29, Wraith +0.27 | 0 heroes |
| Witchmail | 6,400 | +0.143 | +0.022 | +0.167 | The Doorman +0.33, Lash +0.26, Deadman Danny +0.19 | 2 heroes |
| Debuff Reducer | 1,600 | +0.015 | +0.009 | +0.092 | Paige +0.19, Holliday +0.17, Wraith +0.13 | 0 heroes |
| Plated Armor | 6,400 | -0.040 | -0.006 | +0.098 | Holliday +0.21, Wraith +0.16, Grey Talon +0.10 | 2 heroes |
| Reactive Barrier | 1,600 | -0.014 | -0.009 | +0.039 | The Doorman +0.16, Sinclair +0.12, Yamato +0.11 | 3 heroes |
| Unstoppable | 6,400 | -0.061 | -0.009 | +0.151 | Paige +0.27, Haze +0.23, Grey Talon +0.18 | 8 heroes |
| Counterspell | 3,200 | -0.045 | -0.014 | +0.031 | Viscous +0.12, Lash +0.08, The Doorman +0.03 | 1 heroes |
| Bullet Resilience | 3,200 | -0.046 | -0.014 | +0.053 | Viscous +0.12, Lash +0.11, Venator +0.10 | 0 heroes |
| Healbane | 1,600 | -0.049 | -0.030 | +0.057 | Nurse Harrow +0.06, Victor +0.06, Vindicta +0.05 | 14 heroes |
| Metal Skin | 3,200 | -0.169 | -0.053 | +0.098 | Wraith +0.26, Lash +0.19, Silver +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.174 | -0.109 | +0.045 | Lash +0.10, Paradox +0.07, Violet +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.30), Dispel Magic +0.14 (+0.19), Spellbreaker +0.10 (+0.30)
- **Seven**: Witchmail +0.02 (+0.19), Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05)
- **Vindicta**: Bullet Resilience +0.09 (+0.14), Plated Armor +0.09 (+0.18), Divine Barrier +0.07 (+0.13)
- **Lady Geist**: Bullet Resilience +0.04 (+0.09), Counterspell +0.02 (+0.05), Healbane +0.01 (+0.06)
- **Abrams**: Dispel Magic +0.02 (+0.08), Unstoppable +0.02 (+0.17), Reactive Barrier +0.01 (+0.05)
- **Wraith**: Indomitable +0.35 (+0.51), Spellbreaker +0.27 (+0.46), Metal Skin +0.26 (+0.35)
- **McGinnis**: Spirit Resilience +0.11 (+0.26), Dispel Magic +0.02 (+0.07), Witchmail +0.01 (+0.18)
- **Paradox**: Witchmail +0.11 (+0.28), Dispel Magic +0.07 (+0.12), Return Fire +0.07 (+0.11)
- **Dynamo**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.10 (+0.25), Healbane +0.00 (+0.06), Spellbreaker +0.00 (+0.20)
- **Haze**: Unstoppable +0.23 (+0.38), Indomitable +0.06 (+0.21), Return Fire +0.05 (+0.10)
- **Holliday**: Plated Armor +0.21 (+0.30), Debuff Reducer +0.17 (+0.26), Spellbreaker +0.15 (+0.34)
- **Bebop**: Debuff Reducer +0.11 (+0.20), Unstoppable +0.04 (+0.19), Spellbreaker +0.02 (+0.22)
- **Calico**: Divine Barrier +0.12 (+0.18), Spirit Resilience +0.12 (+0.27), Reactive Barrier +0.06 (+0.10)
- **Grey Talon**: Spellbreaker +0.29 (+0.48), Spirit Resilience +0.29 (+0.44), Unstoppable +0.18 (+0.33)
- **Mo & Krill**: Dispel Magic +0.04 (+0.09), Spellbreaker +0.03 (+0.22), Healbane +0.02 (+0.08)
- **Shiv**: Metal Skin +0.05 (+0.15), Bullet Resilience +0.05 (+0.10), Plated Armor +0.04 (+0.13)
- **Ivy**: Unstoppable +0.00 (+0.15), Healbane -0.01 (+0.05), Reactive Barrier -0.02 (+0.02)
- **Warden**: Bullet Resilience +0.02 (+0.07), Divine Barrier +0.01 (+0.07), Healbane +0.01 (+0.07)
- **Yamato**: Reactive Barrier +0.11 (+0.15), Indomitable +0.08 (+0.24), Metal Skin +0.07 (+0.17)
- **Lash**: Spirit Resilience +0.49 (+0.64), Spellbreaker +0.31 (+0.50), Witchmail +0.26 (+0.42)
- **Viscous**: Spirit Resilience +0.21 (+0.36), Divine Barrier +0.19 (+0.25), Counterspell +0.12 (+0.15)
- **Pocket**: Spirit Resilience +0.07 (+0.22), Witchmail +0.01 (+0.17), Return Fire -0.01 (+0.04)
- **Mirage**: Dispel Magic +0.27 (+0.32), Metal Skin +0.08 (+0.18), Plated Armor +0.03 (+0.13)
- **Vyper**: Indomitable +0.24 (+0.39), Plated Armor +0.05 (+0.15), Bullet Resilience +0.02 (+0.07)
- **Sinclair**: Indomitable +0.28 (+0.44), Spellbreaker +0.16 (+0.35), Reactive Barrier +0.12 (+0.15)
- **Mina**: Counterspell -0.00 (+0.03), Return Fire -0.00 (+0.04), Divine Barrier -0.01 (+0.05)
- **Drifter**: Indomitable +0.10 (+0.26), Reactive Barrier +0.03 (+0.07), Debuff Reducer +0.03 (+0.12)
- **Venator**: Metal Skin +0.13 (+0.23), Bullet Resilience +0.10 (+0.15), Plated Armor +0.06 (+0.16)
- **Victor**: Healbane +0.06 (+0.11), Spirit Resilience +0.02 (+0.17), Spellbreaker -0.01 (+0.19)
- **Paige**: Unstoppable +0.27 (+0.42), Debuff Reducer +0.19 (+0.28), Spellbreaker +0.09 (+0.28)
- **The Doorman**: Spirit Resilience +0.41 (+0.56), Witchmail +0.33 (+0.50), Divine Barrier +0.24 (+0.30)
- **Billy**: Reactive Barrier +0.05 (+0.09), Healbane +0.02 (+0.08), Spirit Resilience -0.00 (+0.15)
- **Graves**: Witchmail +0.04 (+0.21), Metal Skin +0.03 (+0.13), Spirit Resilience +0.03 (+0.18)
- **Apollo**: Healbane +0.04 (+0.10), Reactive Barrier +0.03 (+0.07), Counterspell +0.01 (+0.04)
- **Deadman Danny**: Spirit Resilience +0.28 (+0.43), Witchmail +0.19 (+0.35), Indomitable +0.17 (+0.33)
- **Rem**: Debuff Reducer +0.08 (+0.17), Unstoppable +0.03 (+0.18), Spellbreaker +0.00 (+0.20)
- **Silver**: Dispel Magic +0.16 (+0.21), Metal Skin +0.14 (+0.24), Indomitable +0.11 (+0.27)
- **Celeste**: Witchmail +0.12 (+0.28), Spirit Resilience +0.09 (+0.24), Healbane +0.04 (+0.10)
- **Rat King**: Debuff Reducer +0.00 (+0.09), Return Fire -0.00 (+0.04), Healbane -0.01 (+0.04)
- **Solomon**: Counterspell +0.00 (+0.03), Return Fire -0.01 (+0.03), Healbane -0.02 (+0.03)
- **Violet**: Return Fire +0.07 (+0.11), Healbane +0.01 (+0.06), Counterspell +0.00 (+0.03)
- **Nurse Harrow**: Healbane +0.06 (+0.12), Bullet Resilience +0.02 (+0.08), Dispel Magic +0.02 (+0.07)
- **Baba**: Healbane +0.01 (+0.07), Debuff Reducer -0.00 (+0.09), Counterspell -0.00 (+0.03)
