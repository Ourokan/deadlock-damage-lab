# Counter items in the sim (phantom and up)

Built 2026-10-26T07:47:39Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.236 | +0.074 | +0.127 | Lash +0.24, Wraith +0.14, Deadman Danny +0.14 | 1 heroes |
| Divine Barrier | 6,400 | +0.367 | +0.059 | +0.098 | Wraith +0.17, Lash +0.16, Calico +0.13 | 0 heroes |
| Dispel Magic | 3,200 | +0.141 | +0.044 | +0.080 | Mirage +0.37, Silver +0.12, Infernus +0.10 | 4 heroes |
| Debuff Reducer | 1,600 | +0.063 | +0.039 | +0.055 | Wraith +0.10, Deadman Danny +0.07, The Doorman +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | +0.055 | +0.036 | +0.052 | Deadman Danny +0.14, Wraith +0.14, The Doorman +0.12 | 2 heroes |
| Witchmail | 6,400 | +0.228 | +0.036 | +0.194 | Wraith +0.16, Deadman Danny +0.15, The Doorman +0.13 | 0 heroes |
| Indomitable | 6,400 | +0.190 | +0.030 | +0.139 | Wraith +0.30, Vyper +0.29, Deadman Danny +0.20 | 0 heroes |
| Healbane | 1,600 | +0.040 | +0.025 | +0.085 | Mo & Krill +0.06, Nurse Harrow +0.06, Deadman Danny +0.05 | 11 heroes |
| Spellbreaker | 6,400 | +0.153 | +0.024 | +0.150 | Lash +0.23, Deadman Danny +0.18, Wraith +0.17 | 0 heroes |
| Bullet Resilience | 3,200 | +0.043 | +0.013 | +0.090 | Wraith +0.13, Paradox +0.12, Deadman Danny +0.11 | 0 heroes |
| Counterspell | 3,200 | +0.017 | +0.005 | +0.069 | Deadman Danny +0.08, Calico +0.07, Wraith +0.07 | 1 heroes |
| Plated Armor | 6,400 | +0.027 | +0.004 | +0.129 | Holliday +0.23, Wraith +0.17, Deadman Danny +0.14 | 0 heroes |
| Unstoppable | 6,400 | +0.002 | +0.000 | +0.116 | Deadman Danny +0.15, Wraith +0.13, Abrams +0.11 | 0 heroes |
| Metal Skin | 3,200 | -0.091 | -0.029 | +0.112 | Wraith +0.24, Drifter +0.17, Paradox +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.130 | -0.081 | +0.074 | The Doorman +0.08, Deadman Danny +0.08, Wraith +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.18), Unstoppable +0.07 (+0.19), Spirit Resilience +0.04 (+0.17)
- **Seven**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.03 (+0.02)
- **Vindicta**: Divine Barrier +0.01 (+0.11), Witchmail +0.00 (+0.20), Counterspell +0.00 (+0.07)
- **Lady Geist**: Return Fire +0.05 (+0.12), Dispel Magic +0.04 (+0.12), Counterspell +0.03 (+0.10)
- **Abrams**: Indomitable +0.15 (+0.29), Unstoppable +0.11 (+0.23), Spirit Resilience +0.07 (+0.20)
- **Wraith**: Indomitable +0.30 (+0.44), Metal Skin +0.24 (+0.36), Divine Barrier +0.17 (+0.27)
- **McGinnis**: Spirit Resilience +0.03 (+0.16), Healbane -0.02 (+0.07), Debuff Reducer -0.02 (+0.03)
- **Paradox**: Metal Skin +0.14 (+0.25), Bullet Resilience +0.12 (+0.21), Indomitable +0.11 (+0.25)
- **Dynamo**: Healbane -0.01 (+0.08), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane +0.01 (+0.09), Counterspell -0.00 (+0.06), Debuff Reducer -0.01 (+0.05)
- **Haze**: Plated Armor +0.09 (+0.22), Indomitable +0.06 (+0.20), Bullet Resilience +0.05 (+0.14)
- **Holliday**: Plated Armor +0.23 (+0.36), Debuff Reducer +0.05 (+0.10), Spellbreaker +0.05 (+0.20)
- **Bebop**: Counterspell +0.02 (+0.09), Witchmail +0.02 (+0.21), Divine Barrier +0.02 (+0.12)
- **Calico**: Spellbreaker +0.13 (+0.28), Divine Barrier +0.13 (+0.23), Spirit Resilience +0.11 (+0.23)
- **Grey Talon**: Reactive Barrier +0.06 (+0.11), Indomitable +0.05 (+0.19), Spellbreaker +0.05 (+0.20)
- **Mo & Krill**: Spellbreaker +0.14 (+0.29), Spirit Resilience +0.08 (+0.21), Witchmail +0.07 (+0.26)
- **Shiv**: Healbane -0.01 (+0.08), Return Fire -0.02 (+0.06), Divine Barrier -0.03 (+0.06)
- **Ivy**: Unstoppable +0.10 (+0.21), Indomitable +0.06 (+0.20), Debuff Reducer +0.01 (+0.06)
- **Warden**: Return Fire +0.03 (+0.11), Bullet Resilience +0.02 (+0.11), Divine Barrier +0.01 (+0.11)
- **Yamato**: Healbane +0.02 (+0.11), Debuff Reducer -0.03 (+0.03), Counterspell -0.04 (+0.03)
- **Lash**: Spirit Resilience +0.24 (+0.37), Spellbreaker +0.23 (+0.38), Divine Barrier +0.16 (+0.26)
- **Viscous**: Divine Barrier -0.02 (+0.08), Counterspell -0.03 (+0.04), Debuff Reducer -0.03 (+0.03)
- **Pocket**: Witchmail +0.03 (+0.23), Spirit Resilience +0.02 (+0.15), Return Fire +0.02 (+0.09)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spellbreaker +0.09 (+0.24), Spirit Resilience +0.06 (+0.18)
- **Vyper**: Indomitable +0.29 (+0.43), Debuff Reducer +0.06 (+0.12), Spellbreaker +0.03 (+0.18)
- **Sinclair**: Indomitable +0.07 (+0.21), Spellbreaker +0.04 (+0.19), Return Fire +0.03 (+0.10)
- **Mina**: Divine Barrier +0.08 (+0.17), Spirit Resilience +0.07 (+0.20), Witchmail +0.06 (+0.26)
- **Drifter**: Metal Skin +0.17 (+0.28), Spirit Resilience +0.13 (+0.25), Witchmail +0.08 (+0.28)
- **Venator**: Bullet Resilience +0.10 (+0.19), Metal Skin +0.03 (+0.15), Debuff Reducer +0.02 (+0.07)
- **Victor**: Healbane -0.01 (+0.07), Counterspell -0.05 (+0.02), Debuff Reducer -0.05 (+0.01)
- **Paige**: Healbane -0.00 (+0.08), Counterspell -0.02 (+0.05), Return Fire -0.02 (+0.05)
- **The Doorman**: Indomitable +0.19 (+0.33), Witchmail +0.13 (+0.32), Reactive Barrier +0.12 (+0.18)
- **Billy**: Healbane +0.05 (+0.13), Counterspell +0.04 (+0.11), Spellbreaker +0.04 (+0.19)
- **Graves**: Spirit Resilience +0.12 (+0.24), Divine Barrier +0.10 (+0.19), Witchmail +0.10 (+0.29)
- **Apollo**: Reactive Barrier -0.03 (+0.02), Healbane -0.03 (+0.05), Debuff Reducer -0.06 (-0.00)
- **Deadman Danny**: Indomitable +0.20 (+0.34), Spellbreaker +0.18 (+0.33), Witchmail +0.15 (+0.34)
- **Rem**: Witchmail +0.02 (+0.22), Dispel Magic -0.00 (+0.08), Indomitable -0.01 (+0.13)
- **Silver**: Dispel Magic +0.12 (+0.20), Reactive Barrier +0.03 (+0.08), Metal Skin +0.02 (+0.13)
- **Celeste**: Spirit Resilience +0.12 (+0.25), Witchmail +0.09 (+0.28), Plated Armor +0.05 (+0.18)
- **Rat King**: Counterspell +0.00 (+0.07), Bullet Resilience +0.00 (+0.09), Return Fire -0.00 (+0.07)
- **Solomon**: Return Fire -0.00 (+0.07), Counterspell -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **Violet**: Return Fire +0.02 (+0.09), Witchmail +0.02 (+0.21), Healbane -0.02 (+0.07)
- **Nurse Harrow**: Healbane +0.06 (+0.14), Counterspell -0.01 (+0.06), Dispel Magic -0.03 (+0.05)
- **Baba**: Healbane +0.02 (+0.10), Counterspell -0.02 (+0.05), Return Fire -0.03 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.212 | +0.066 | +0.112 | Lash +0.26, Pocket +0.19, Graves +0.16 | 10 heroes |
| Divine Barrier | 6,400 | +0.242 | +0.039 | +0.068 | Lash +0.16, Vindicta +0.12, Wraith +0.11 | 1 heroes |
| Dispel Magic | 3,200 | +0.120 | +0.038 | +0.060 | Mirage +0.30, Silver +0.12, Lash +0.12 | 7 heroes |
| Witchmail | 6,400 | +0.208 | +0.033 | +0.159 | Graves +0.17, Lash +0.17, Pocket +0.10 | 0 heroes |
| Indomitable | 6,400 | +0.156 | +0.025 | +0.110 | Vyper +0.33, Wraith +0.21, Deadman Danny +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.036 | +0.022 | +0.042 | Wraith +0.07, Vyper +0.06, Lash +0.05 | 1 heroes |
| Spellbreaker | 6,400 | +0.143 | +0.022 | +0.117 | Lash +0.21, Wraith +0.12, Pocket +0.10 | 0 heroes |
| Reactive Barrier | 1,600 | +0.035 | +0.022 | +0.041 | Wraith +0.11, Deadman Danny +0.08, The Doorman +0.08 | 4 heroes |
| Healbane | 1,600 | +0.012 | +0.008 | +0.074 | Lash +0.10, Haze +0.04, Pocket +0.04 | 17 heroes |
| Bullet Resilience | 3,200 | +0.018 | +0.006 | +0.070 | Paradox +0.13, Lash +0.12, Vindicta +0.12 | 0 heroes |
| Plated Armor | 6,400 | +0.021 | +0.003 | +0.106 | Haze +0.14, Holliday +0.14, Paradox +0.12 | 0 heroes |
| Counterspell | 3,200 | -0.008 | -0.003 | +0.043 | Deadman Danny +0.06, Lash +0.06, Vindicta +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.031 | -0.005 | +0.087 | Abrams +0.20, Ivy +0.13, Mo & Krill +0.11 | 0 heroes |
| Metal Skin | 3,200 | -0.113 | -0.035 | +0.090 | Wraith +0.21, Paradox +0.17, Lash +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.143 | -0.089 | +0.059 | Vindicta +0.07, Lash +0.06, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.15), Unstoppable +0.04 (+0.12), Healbane +0.02 (+0.10)
- **Seven**: Witchmail +0.03 (+0.19), Healbane +0.00 (+0.08), Counterspell +0.00 (+0.04)
- **Vindicta**: Divine Barrier +0.12 (+0.19), Bullet Resilience +0.12 (+0.19), Plated Armor +0.10 (+0.20)
- **Lady Geist**: Return Fire +0.05 (+0.11), Divine Barrier +0.02 (+0.09), Healbane +0.01 (+0.08)
- **Abrams**: Unstoppable +0.20 (+0.28), Dispel Magic +0.10 (+0.17), Indomitable +0.05 (+0.16)
- **Wraith**: Indomitable +0.21 (+0.33), Metal Skin +0.21 (+0.30), Spellbreaker +0.12 (+0.24)
- **McGinnis**: Spirit Resilience +0.00 (+0.11), Counterspell +0.00 (+0.04), Dispel Magic -0.00 (+0.06)
- **Paradox**: Metal Skin +0.17 (+0.26), Bullet Resilience +0.13 (+0.20), Plated Armor +0.12 (+0.23)
- **Dynamo**: Healbane +0.01 (+0.08), Counterspell -0.02 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.01 (+0.12), Dispel Magic +0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Haze**: Plated Armor +0.14 (+0.24), Bullet Resilience +0.09 (+0.16), Indomitable +0.09 (+0.20)
- **Holliday**: Plated Armor +0.14 (+0.24), Indomitable +0.03 (+0.14), Spellbreaker +0.03 (+0.14)
- **Bebop**: Divine Barrier +0.04 (+0.11), Witchmail +0.04 (+0.20), Counterspell +0.03 (+0.07)
- **Calico**: Reactive Barrier +0.05 (+0.09), Divine Barrier +0.03 (+0.10), Spellbreaker +0.01 (+0.13)
- **Grey Talon**: Reactive Barrier +0.03 (+0.08), Spellbreaker +0.03 (+0.15), Debuff Reducer +0.03 (+0.07)
- **Mo & Krill**: Unstoppable +0.11 (+0.20), Spellbreaker +0.08 (+0.20), Dispel Magic +0.04 (+0.10)
- **Shiv**: Divine Barrier +0.02 (+0.09), Bullet Resilience +0.01 (+0.08), Return Fire -0.01 (+0.05)
- **Ivy**: Unstoppable +0.13 (+0.21), Indomitable +0.05 (+0.16), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.08), Counterspell +0.00 (+0.05), Divine Barrier -0.01 (+0.06)
- **Yamato**: Healbane +0.02 (+0.10), Counterspell -0.03 (+0.01), Debuff Reducer -0.03 (+0.01)
- **Lash**: Spirit Resilience +0.26 (+0.37), Spellbreaker +0.21 (+0.33), Witchmail +0.17 (+0.33)
- **Viscous**: Counterspell -0.01 (+0.03), Healbane -0.02 (+0.05), Divine Barrier -0.02 (+0.05)
- **Pocket**: Spirit Resilience +0.19 (+0.30), Spellbreaker +0.10 (+0.22), Witchmail +0.10 (+0.26)
- **Mirage**: Dispel Magic +0.30 (+0.37), Spellbreaker +0.02 (+0.13), Spirit Resilience +0.01 (+0.12)
- **Vyper**: Indomitable +0.33 (+0.44), Debuff Reducer +0.06 (+0.10), Spellbreaker +0.04 (+0.16)
- **Sinclair**: Indomitable +0.10 (+0.21), Spellbreaker +0.03 (+0.15), Return Fire -0.00 (+0.06)
- **Mina**: Spirit Resilience +0.13 (+0.24), Spellbreaker +0.08 (+0.19), Witchmail +0.07 (+0.22)
- **Drifter**: Metal Skin +0.11 (+0.20), Spirit Resilience +0.11 (+0.22), Witchmail +0.07 (+0.23)
- **Venator**: Bullet Resilience +0.09 (+0.16), Metal Skin +0.05 (+0.14), Plated Armor +0.03 (+0.14)
- **Victor**: Spellbreaker +0.07 (+0.18), Spirit Resilience +0.03 (+0.14), Healbane -0.00 (+0.07)
- **Paige**: Counterspell +0.00 (+0.05), Return Fire +0.00 (+0.06), Healbane -0.02 (+0.05)
- **The Doorman**: Indomitable +0.09 (+0.20), Spirit Resilience +0.09 (+0.20), Witchmail +0.08 (+0.24)
- **Billy**: Spirit Resilience +0.00 (+0.12), Spellbreaker -0.00 (+0.11), Counterspell -0.01 (+0.03)
- **Graves**: Witchmail +0.17 (+0.33), Spirit Resilience +0.16 (+0.27), Metal Skin +0.12 (+0.21)
- **Apollo**: Healbane -0.01 (+0.07), Reactive Barrier -0.01 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Deadman Danny**: Indomitable +0.12 (+0.23), Spellbreaker +0.10 (+0.21), Witchmail +0.09 (+0.25)
- **Rem**: Witchmail +0.02 (+0.18), Counterspell +0.00 (+0.05), Unstoppable -0.00 (+0.08)
- **Silver**: Dispel Magic +0.12 (+0.18), Divine Barrier +0.01 (+0.07), Reactive Barrier -0.00 (+0.04)
- **Celeste**: Witchmail +0.04 (+0.20), Spirit Resilience +0.01 (+0.12), Indomitable -0.01 (+0.10)
- **Rat King**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.03), Bullet Resilience -0.02 (+0.05)
- **Solomon**: Return Fire +0.01 (+0.06), Counterspell -0.01 (+0.03), Debuff Reducer -0.02 (+0.02)
- **Violet**: Return Fire +0.03 (+0.09), Witchmail +0.02 (+0.18), Healbane +0.01 (+0.09)
- **Nurse Harrow**: Healbane +0.03 (+0.10), Counterspell +0.00 (+0.05), Spirit Resilience -0.00 (+0.11)
- **Baba**: Return Fire +0.00 (+0.06), Healbane +0.00 (+0.08), Unstoppable -0.00 (+0.09)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.208 | +0.065 | +0.115 | Wraith +0.19, Lash +0.18, Grey Talon +0.16 | 13 heroes |
| Divine Barrier | 6,400 | +0.255 | +0.040 | +0.057 | Vindicta +0.12, Wraith +0.11, Paradox +0.09 | 2 heroes |
| Dispel Magic | 3,200 | +0.106 | +0.033 | +0.050 | Mirage +0.30, Paradox +0.11, Infernus +0.10 | 9 heroes |
| Witchmail | 6,400 | +0.206 | +0.032 | +0.161 | Wraith +0.15, Paradox +0.11, Lash +0.11 | 1 heroes |
| Indomitable | 6,400 | +0.166 | +0.027 | +0.116 | Vyper +0.35, Wraith +0.31, Grey Talon +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.151 | +0.024 | +0.119 | Grey Talon +0.19, Wraith +0.18, Lash +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.027 | +0.017 | +0.036 | Grey Talon +0.11, Vyper +0.08, Wraith +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.020 | +0.013 | +0.033 | Wraith +0.12, Grey Talon +0.10, The Doorman +0.07 | 5 heroes |
| Plated Armor | 6,400 | +0.020 | +0.003 | +0.104 | Wraith +0.19, Holliday +0.16, Haze +0.10 | 0 heroes |
| Bullet Resilience | 3,200 | -0.006 | -0.002 | +0.059 | Vindicta +0.13, Paradox +0.09, Wraith +0.09 | 1 heroes |
| Healbane | 1,600 | -0.005 | -0.003 | +0.060 | Yamato +0.06, Infernus +0.04, Vindicta +0.04 | 16 heroes |
| Unstoppable | 6,400 | -0.037 | -0.006 | +0.085 | Grey Talon +0.17, Ivy +0.16, Abrams +0.14 | 3 heroes |
| Counterspell | 3,200 | -0.020 | -0.006 | +0.032 | Yamato +0.04, Vindicta +0.04, The Doorman +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.112 | -0.035 | +0.093 | Wraith +0.27, Paradox +0.16, Lash +0.08 | 0 heroes |
| Return Fire | 1,600 | -0.148 | -0.092 | +0.049 | Wraith +0.08, Vindicta +0.06, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.13 (+0.25), Unstoppable +0.13 (+0.21), Dispel Magic +0.10 (+0.15)
- **Seven**: Witchmail +0.05 (+0.21), Healbane +0.01 (+0.07), Counterspell +0.00 (+0.04)
- **Vindicta**: Bullet Resilience +0.13 (+0.19), Divine Barrier +0.12 (+0.17), Plated Armor +0.09 (+0.20)
- **Lady Geist**: Return Fire +0.03 (+0.08), Counterspell +0.02 (+0.06), Bullet Resilience +0.01 (+0.07)
- **Abrams**: Unstoppable +0.14 (+0.22), Dispel Magic +0.07 (+0.12), Healbane +0.03 (+0.09)
- **Wraith**: Indomitable +0.31 (+0.43), Metal Skin +0.27 (+0.37), Spirit Resilience +0.19 (+0.31)
- **McGinnis**: Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05), Spirit Resilience -0.01 (+0.10)
- **Paradox**: Metal Skin +0.16 (+0.26), Dispel Magic +0.11 (+0.16), Witchmail +0.11 (+0.27)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03), Dispel Magic -0.02 (+0.03)
- **Haze**: Plated Armor +0.10 (+0.20), Indomitable +0.09 (+0.21), Unstoppable +0.09 (+0.18)
- **Holliday**: Plated Armor +0.16 (+0.27), Spellbreaker +0.05 (+0.17), Indomitable +0.05 (+0.17)
- **Bebop**: Metal Skin +0.02 (+0.11), Healbane +0.01 (+0.07), Divine Barrier +0.01 (+0.07)
- **Calico**: Reactive Barrier +0.03 (+0.07), Divine Barrier +0.03 (+0.08), Spellbreaker +0.02 (+0.14)
- **Grey Talon**: Spellbreaker +0.19 (+0.31), Unstoppable +0.17 (+0.25), Spirit Resilience +0.16 (+0.27)
- **Mo & Krill**: Unstoppable +0.12 (+0.21), Spellbreaker +0.07 (+0.19), Dispel Magic +0.04 (+0.09)
- **Shiv**: Metal Skin +0.03 (+0.13), Bullet Resilience +0.02 (+0.08), Divine Barrier +0.01 (+0.07)
- **Ivy**: Unstoppable +0.16 (+0.24), Indomitable +0.11 (+0.23), Dispel Magic +0.04 (+0.09)
- **Warden**: Return Fire +0.01 (+0.06), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Yamato**: Healbane +0.06 (+0.12), Counterspell +0.04 (+0.08), Debuff Reducer +0.04 (+0.08)
- **Lash**: Spirit Resilience +0.18 (+0.29), Spellbreaker +0.14 (+0.26), Witchmail +0.11 (+0.27)
- **Viscous**: Healbane +0.01 (+0.07), Return Fire +0.00 (+0.05), Counterspell -0.00 (+0.03)
- **Pocket**: Spirit Resilience +0.06 (+0.18), Counterspell +0.02 (+0.05), Debuff Reducer +0.01 (+0.04)
- **Mirage**: Dispel Magic +0.30 (+0.35), Spirit Resilience +0.02 (+0.14), Spellbreaker +0.02 (+0.14)
- **Vyper**: Indomitable +0.35 (+0.47), Debuff Reducer +0.08 (+0.12), Spellbreaker +0.05 (+0.17)
- **Sinclair**: Indomitable +0.15 (+0.27), Unstoppable +0.02 (+0.11), Debuff Reducer +0.01 (+0.05)
- **Mina**: Spirit Resilience +0.15 (+0.26), Divine Barrier +0.08 (+0.14), Witchmail +0.08 (+0.24)
- **Drifter**: Spirit Resilience +0.10 (+0.21), Metal Skin +0.07 (+0.17), Witchmail +0.05 (+0.21)
- **Venator**: Bullet Resilience +0.08 (+0.14), Metal Skin +0.07 (+0.16), Plated Armor +0.01 (+0.12)
- **Victor**: Spellbreaker +0.03 (+0.15), Healbane +0.03 (+0.09), Spirit Resilience +0.01 (+0.13)
- **Paige**: Counterspell +0.00 (+0.03), Return Fire -0.01 (+0.04), Healbane -0.02 (+0.04)
- **The Doorman**: Spirit Resilience +0.12 (+0.23), Indomitable +0.10 (+0.22), Witchmail +0.08 (+0.24)
- **Billy**: Reactive Barrier +0.01 (+0.04), Healbane -0.01 (+0.05), Counterspell -0.02 (+0.01)
- **Graves**: Witchmail +0.03 (+0.19), Return Fire +0.02 (+0.07), Metal Skin +0.01 (+0.11)
- **Apollo**: Healbane +0.00 (+0.06), Reactive Barrier -0.01 (+0.02), Dispel Magic -0.03 (+0.02)
- **Deadman Danny**: Spellbreaker +0.10 (+0.22), Indomitable +0.09 (+0.21), Spirit Resilience +0.08 (+0.20)
- **Rem**: Debuff Reducer +0.06 (+0.10), Unstoppable +0.06 (+0.14), Counterspell +0.00 (+0.03)
- **Silver**: Dispel Magic +0.09 (+0.14), Reactive Barrier -0.00 (+0.03), Divine Barrier -0.01 (+0.05)
- **Celeste**: Dispel Magic +0.10 (+0.15), Witchmail +0.09 (+0.25), Spirit Resilience +0.07 (+0.19)
- **Rat King**: Counterspell -0.01 (+0.02), Return Fire -0.01 (+0.04), Bullet Resilience -0.01 (+0.05)
- **Solomon**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.03), Healbane -0.01 (+0.05)
- **Violet**: Witchmail +0.06 (+0.22), Return Fire +0.03 (+0.08), Divine Barrier +0.02 (+0.08)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Counterspell +0.02 (+0.05), Dispel Magic +0.01 (+0.06)
- **Baba**: Return Fire +0.02 (+0.07), Healbane -0.01 (+0.05), Counterspell -0.01 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.232 | +0.072 | +0.123 | Lash +0.35, Deadman Danny +0.35, The Doorman +0.26 | 14 heroes |
| Dispel Magic | 3,200 | +0.122 | +0.038 | +0.067 | Mirage +0.34, Drifter +0.29, Lash +0.16 | 9 heroes |
| Divine Barrier | 6,400 | +0.193 | +0.030 | +0.051 | Lash +0.16, Calico +0.12, The Doorman +0.11 | 3 heroes |
| Witchmail | 6,400 | +0.189 | +0.030 | +0.146 | Deadman Danny +0.22, Lash +0.20, The Doorman +0.18 | 2 heroes |
| Indomitable | 6,400 | +0.179 | +0.029 | +0.125 | Vyper +0.28, The Doorman +0.23, Deadman Danny +0.19 | 1 heroes |
| Spellbreaker | 6,400 | +0.179 | +0.028 | +0.140 | Deadman Danny +0.32, Lash +0.27, Grey Talon +0.17 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.045 | Grey Talon +0.13, Paige +0.09, Rem +0.08 | 0 heroes |
| Unstoppable | 6,400 | +0.011 | +0.002 | +0.136 | Paige +0.32, Wraith +0.25, Ivy +0.18 | 8 heroes |
| Plated Armor | 6,400 | +0.009 | +0.001 | +0.101 | Deadman Danny +0.22, Vindicta +0.16, Wraith +0.14 | 2 heroes |
| Reactive Barrier | 1,600 | -0.002 | -0.001 | +0.033 | Deadman Danny +0.12, Calico +0.10, Drifter +0.08 | 3 heroes |
| Healbane | 1,600 | -0.004 | -0.003 | +0.057 | Vindicta +0.05, Infernus +0.05, Lady Geist +0.04 | 13 heroes |
| Bullet Resilience | 3,200 | -0.019 | -0.006 | +0.055 | Vindicta +0.14, Lash +0.10, Venator +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.026 | -0.008 | +0.031 | The Doorman +0.07, Wraith +0.04, Grey Talon +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.111 | -0.035 | +0.097 | Lash +0.23, Venator +0.16, Wraith +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.157 | -0.098 | +0.040 | Paradox +0.07, Vindicta +0.05, Haze +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.16 (+0.30), Dispel Magic +0.06 (+0.13), Indomitable +0.05 (+0.18)
- **Seven**: Witchmail +0.03 (+0.17), Counterspell +0.00 (+0.03), Healbane -0.01 (+0.04)
- **Vindicta**: Plated Armor +0.16 (+0.26), Bullet Resilience +0.14 (+0.19), Witchmail +0.11 (+0.26)
- **Lady Geist**: Bullet Resilience +0.05 (+0.11), Healbane +0.04 (+0.10), Dispel Magic +0.04 (+0.11)
- **Abrams**: Unstoppable +0.08 (+0.21), Indomitable +0.06 (+0.18), Divine Barrier +0.04 (+0.09)
- **Wraith**: Unstoppable +0.25 (+0.38), Metal Skin +0.16 (+0.26), Indomitable +0.16 (+0.28)
- **McGinnis**: Healbane -0.00 (+0.06), Spirit Resilience -0.01 (+0.12), Counterspell -0.02 (+0.01)
- **Paradox**: Witchmail +0.09 (+0.24), Unstoppable +0.08 (+0.22), Return Fire +0.07 (+0.11)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.00 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.14 (+0.26), Witchmail +0.05 (+0.20), Spellbreaker +0.03 (+0.17)
- **Haze**: Unstoppable +0.15 (+0.29), Indomitable +0.05 (+0.18), Return Fire +0.04 (+0.08)
- **Holliday**: Spellbreaker +0.04 (+0.18), Debuff Reducer +0.04 (+0.09), Return Fire +0.03 (+0.07)
- **Bebop**: Spellbreaker +0.10 (+0.24), Debuff Reducer +0.07 (+0.12), Indomitable +0.02 (+0.15)
- **Calico**: Spirit Resilience +0.15 (+0.28), Divine Barrier +0.12 (+0.17), Reactive Barrier +0.10 (+0.14)
- **Grey Talon**: Spellbreaker +0.17 (+0.31), Spirit Resilience +0.15 (+0.27), Debuff Reducer +0.13 (+0.17)
- **Mo & Krill**: Unstoppable +0.06 (+0.19), Spellbreaker +0.03 (+0.18), Dispel Magic +0.02 (+0.08)
- **Shiv**: Metal Skin +0.03 (+0.13), Divine Barrier +0.02 (+0.07), Bullet Resilience +0.02 (+0.08)
- **Ivy**: Unstoppable +0.18 (+0.32), Indomitable +0.14 (+0.27), Debuff Reducer +0.05 (+0.10)
- **Warden**: Return Fire +0.03 (+0.07), Metal Skin +0.03 (+0.12), Healbane +0.02 (+0.08)
- **Yamato**: Healbane +0.02 (+0.08), Reactive Barrier -0.00 (+0.03), Debuff Reducer -0.01 (+0.04)
- **Lash**: Spirit Resilience +0.35 (+0.48), Spellbreaker +0.27 (+0.41), Metal Skin +0.23 (+0.33)
- **Viscous**: Spirit Resilience +0.11 (+0.24), Divine Barrier +0.09 (+0.14), Spellbreaker +0.06 (+0.20)
- **Pocket**: Spirit Resilience +0.08 (+0.21), Witchmail +0.04 (+0.18), Spellbreaker +0.01 (+0.15)
- **Mirage**: Dispel Magic +0.34 (+0.41), Metal Skin +0.12 (+0.21), Plated Armor +0.05 (+0.15)
- **Vyper**: Indomitable +0.28 (+0.41), Plated Armor +0.08 (+0.18), Metal Skin +0.07 (+0.16)
- **Sinclair**: Indomitable +0.17 (+0.29), Spellbreaker +0.06 (+0.20), Reactive Barrier +0.05 (+0.09)
- **Mina**: Witchmail +0.02 (+0.16), Counterspell +0.02 (+0.05), Return Fire +0.01 (+0.05)
- **Drifter**: Dispel Magic +0.29 (+0.36), Reactive Barrier +0.08 (+0.11), Metal Skin +0.07 (+0.17)
- **Venator**: Metal Skin +0.16 (+0.26), Bullet Resilience +0.10 (+0.15), Plated Armor +0.03 (+0.13)
- **Victor**: Spellbreaker +0.08 (+0.22), Healbane +0.03 (+0.09), Spirit Resilience +0.02 (+0.14)
- **Paige**: Unstoppable +0.32 (+0.45), Debuff Reducer +0.09 (+0.13), Indomitable +0.01 (+0.14)
- **The Doorman**: Spirit Resilience +0.26 (+0.38), Indomitable +0.23 (+0.36), Witchmail +0.18 (+0.33)
- **Billy**: Healbane -0.01 (+0.05), Return Fire -0.01 (+0.03), Reactive Barrier -0.01 (+0.02)
- **Graves**: Witchmail +0.06 (+0.20), Spirit Resilience +0.05 (+0.18), Divine Barrier +0.02 (+0.07)
- **Apollo**: Healbane +0.02 (+0.08), Reactive Barrier -0.00 (+0.03), Divine Barrier -0.01 (+0.04)
- **Deadman Danny**: Spirit Resilience +0.35 (+0.48), Spellbreaker +0.32 (+0.46), Plated Armor +0.22 (+0.33)
- **Rem**: Debuff Reducer +0.08 (+0.13), Spellbreaker +0.05 (+0.19), Counterspell -0.00 (+0.03)
- **Silver**: Dispel Magic +0.06 (+0.13), Debuff Reducer +0.01 (+0.06), Reactive Barrier +0.01 (+0.04)
- **Celeste**: Witchmail +0.06 (+0.21), Spirit Resilience +0.06 (+0.18), Divine Barrier +0.02 (+0.07)
- **Rat King**: Return Fire +0.00 (+0.04), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.04)
- **Solomon**: Reactive Barrier +0.01 (+0.05), Counterspell +0.01 (+0.04), Return Fire +0.01 (+0.05)
- **Violet**: Witchmail +0.06 (+0.21), Return Fire +0.04 (+0.08), Spirit Resilience +0.03 (+0.15)
- **Nurse Harrow**: Dispel Magic +0.12 (+0.18), Spirit Resilience +0.10 (+0.23), Witchmail +0.04 (+0.19)
- **Baba**: Unstoppable +0.02 (+0.16), Healbane +0.01 (+0.07), Witchmail -0.00 (+0.14)
