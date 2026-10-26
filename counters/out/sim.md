# Counter items in the sim (phantom and up)

Built 2026-10-26T23:52:19Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.221 | +0.069 | +0.118 | Lash +0.28, Deadman Danny +0.16, Wraith +0.16 | 1 heroes |
| Divine Barrier | 6,400 | +0.404 | +0.065 | +0.096 | Lash +0.26, Wraith +0.16, Calico +0.13 | 0 heroes |
| Dispel Magic | 3,200 | +0.139 | +0.043 | +0.075 | Mirage +0.37, Infernus +0.11, Paradox +0.10 | 4 heroes |
| Debuff Reducer | 1,600 | +0.065 | +0.041 | +0.058 | Wraith +0.08, Deadman Danny +0.08, Calico +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.057 | +0.036 | +0.055 | Wraith +0.14, Deadman Danny +0.14, The Doorman +0.09 | 2 heroes |
| Witchmail | 6,400 | +0.224 | +0.035 | +0.191 | Lash +0.19, Deadman Danny +0.18, Wraith +0.17 | 0 heroes |
| Indomitable | 6,400 | +0.190 | +0.030 | +0.140 | Vyper +0.30, Wraith +0.29, Deadman Danny +0.22 | 0 heroes |
| Healbane | 1,600 | +0.037 | +0.023 | +0.087 | Nurse Harrow +0.06, Deadman Danny +0.05, Infernus +0.04 | 11 heroes |
| Spellbreaker | 6,400 | +0.147 | +0.023 | +0.145 | Lash +0.32, Deadman Danny +0.21, Wraith +0.17 | 0 heroes |
| Bullet Resilience | 3,200 | +0.037 | +0.012 | +0.089 | Wraith +0.14, Paradox +0.13, Lash +0.11 | 0 heroes |
| Counterspell | 3,200 | +0.017 | +0.005 | +0.070 | Deadman Danny +0.08, Calico +0.07, Wraith +0.05 | 1 heroes |
| Plated Armor | 6,400 | +0.028 | +0.004 | +0.125 | Holliday +0.22, Wraith +0.16, Deadman Danny +0.15 | 0 heroes |
| Unstoppable | 6,400 | -0.001 | -0.000 | +0.112 | Deadman Danny +0.16, Abrams +0.12, Wraith +0.12 | 0 heroes |
| Metal Skin | 3,200 | -0.094 | -0.029 | +0.108 | Wraith +0.24, Lash +0.24, Paradox +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.128 | -0.080 | +0.078 | Deadman Danny +0.07, The Doorman +0.06, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.19), Unstoppable +0.06 (+0.17), Spirit Resilience +0.05 (+0.17)
- **Seven**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.03 (+0.02)
- **Vindicta**: Witchmail +0.02 (+0.21), Divine Barrier +0.01 (+0.11), Return Fire +0.01 (+0.08)
- **Lady Geist**: Return Fire +0.04 (+0.12), Healbane +0.02 (+0.10), Counterspell +0.01 (+0.08)
- **Abrams**: Indomitable +0.14 (+0.28), Unstoppable +0.12 (+0.23), Divine Barrier +0.06 (+0.16)
- **Wraith**: Indomitable +0.29 (+0.43), Metal Skin +0.24 (+0.35), Spellbreaker +0.17 (+0.32)
- **McGinnis**: Spirit Resilience +0.00 (+0.12), Return Fire -0.00 (+0.08), Healbane -0.01 (+0.07)
- **Paradox**: Metal Skin +0.15 (+0.26), Bullet Resilience +0.13 (+0.22), Indomitable +0.13 (+0.27)
- **Dynamo**: Healbane +0.00 (+0.09), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane +0.00 (+0.09), Counterspell -0.01 (+0.06), Dispel Magic -0.02 (+0.06)
- **Haze**: Plated Armor +0.09 (+0.21), Indomitable +0.06 (+0.20), Bullet Resilience +0.05 (+0.14)
- **Holliday**: Plated Armor +0.22 (+0.34), Reactive Barrier +0.03 (+0.09), Debuff Reducer +0.03 (+0.09)
- **Bebop**: Divine Barrier +0.03 (+0.12), Witchmail +0.02 (+0.22), Bullet Resilience +0.02 (+0.11)
- **Calico**: Spellbreaker +0.13 (+0.27), Divine Barrier +0.13 (+0.22), Spirit Resilience +0.11 (+0.23)
- **Grey Talon**: Debuff Reducer +0.04 (+0.10), Reactive Barrier +0.04 (+0.10), Spellbreaker +0.04 (+0.18)
- **Mo & Krill**: Spellbreaker +0.15 (+0.29), Spirit Resilience +0.09 (+0.20), Witchmail +0.08 (+0.27)
- **Shiv**: Healbane -0.01 (+0.08), Return Fire -0.01 (+0.07), Debuff Reducer -0.03 (+0.03)
- **Ivy**: Unstoppable +0.11 (+0.23), Indomitable +0.08 (+0.22), Dispel Magic +0.00 (+0.08)
- **Warden**: Return Fire +0.01 (+0.09), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.04)
- **Yamato**: Healbane +0.02 (+0.10), Debuff Reducer -0.04 (+0.02), Counterspell -0.04 (+0.03)
- **Lash**: Spellbreaker +0.32 (+0.47), Spirit Resilience +0.28 (+0.40), Divine Barrier +0.26 (+0.35)
- **Viscous**: Healbane -0.02 (+0.07), Divine Barrier -0.02 (+0.08), Counterspell -0.03 (+0.05)
- **Pocket**: Spirit Resilience +0.06 (+0.18), Witchmail +0.05 (+0.24), Spellbreaker +0.04 (+0.18)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spirit Resilience +0.06 (+0.18), Spellbreaker +0.06 (+0.20)
- **Vyper**: Indomitable +0.30 (+0.44), Debuff Reducer +0.05 (+0.11), Spellbreaker +0.03 (+0.18)
- **Sinclair**: Indomitable +0.09 (+0.23), Spellbreaker +0.02 (+0.16), Unstoppable +0.01 (+0.13)
- **Mina**: Return Fire +0.03 (+0.11), Witchmail +0.02 (+0.21), Counterspell +0.01 (+0.08)
- **Drifter**: Witchmail +0.04 (+0.23), Return Fire +0.04 (+0.12), Counterspell +0.04 (+0.11)
- **Venator**: Bullet Resilience +0.08 (+0.17), Metal Skin +0.01 (+0.12), Divine Barrier +0.01 (+0.11)
- **Victor**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Dispel Magic -0.04 (+0.03)
- **Paige**: Healbane -0.01 (+0.08), Counterspell -0.02 (+0.05), Return Fire -0.03 (+0.05)
- **The Doorman**: Indomitable +0.16 (+0.30), Witchmail +0.11 (+0.31), Spirit Resilience +0.10 (+0.22)
- **Billy**: Spirit Resilience +0.04 (+0.16), Spellbreaker +0.04 (+0.18), Healbane +0.04 (+0.12)
- **Graves**: Witchmail +0.09 (+0.28), Spirit Resilience +0.09 (+0.20), Metal Skin +0.08 (+0.19)
- **Apollo**: Healbane +0.00 (+0.09), Debuff Reducer -0.04 (+0.01), Reactive Barrier -0.05 (+0.01)
- **Deadman Danny**: Indomitable +0.22 (+0.36), Spellbreaker +0.21 (+0.36), Witchmail +0.18 (+0.37)
- **Rem**: Witchmail +0.01 (+0.20), Unstoppable -0.00 (+0.11), Debuff Reducer -0.01 (+0.05)
- **Silver**: Dispel Magic +0.05 (+0.13), Metal Skin -0.00 (+0.11), Return Fire -0.01 (+0.06)
- **Celeste**: Spirit Resilience +0.10 (+0.22), Witchmail +0.10 (+0.29), Dispel Magic +0.04 (+0.12)
- **Rat King**: Counterspell +0.01 (+0.08), Bullet Resilience -0.00 (+0.09), Return Fire -0.01 (+0.07)
- **Solomon**: Counterspell -0.01 (+0.06), Return Fire -0.02 (+0.06), Healbane -0.02 (+0.07)
- **Violet**: Return Fire +0.04 (+0.11), Healbane -0.02 (+0.07), Counterspell -0.04 (+0.03)
- **Nurse Harrow**: Healbane +0.06 (+0.14), Return Fire +0.01 (+0.08), Counterspell -0.02 (+0.05)
- **Baba**: Healbane +0.00 (+0.09), Debuff Reducer -0.02 (+0.04), Counterspell -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.206 | +0.065 | +0.113 | Lash +0.36, Pocket +0.24, Deadman Danny +0.21 | 10 heroes |
| Divine Barrier | 6,400 | +0.251 | +0.040 | +0.061 | Lash +0.20, Wraith +0.13, The Doorman +0.10 | 1 heroes |
| Dispel Magic | 3,200 | +0.110 | +0.034 | +0.049 | Mirage +0.31, Infernus +0.09, Graves +0.09 | 7 heroes |
| Witchmail | 6,400 | +0.206 | +0.032 | +0.156 | Graves +0.18, Lash +0.16, Pocket +0.14 | 0 heroes |
| Indomitable | 6,400 | +0.158 | +0.026 | +0.113 | Vyper +0.33, Wraith +0.28, The Doorman +0.14 | 0 heroes |
| Spellbreaker | 6,400 | +0.142 | +0.022 | +0.116 | Lash +0.35, Deadman Danny +0.15, Pocket +0.15 | 0 heroes |
| Debuff Reducer | 1,600 | +0.033 | +0.021 | +0.040 | Wraith +0.09, Pocket +0.05, Vyper +0.04 | 1 heroes |
| Reactive Barrier | 1,600 | +0.032 | +0.020 | +0.039 | Wraith +0.12, Graves +0.12, Deadman Danny +0.08 | 4 heroes |
| Plated Armor | 6,400 | +0.020 | +0.003 | +0.100 | Deadman Danny +0.23, Wraith +0.14, Paradox +0.10 | 0 heroes |
| Bullet Resilience | 3,200 | +0.006 | +0.002 | +0.062 | Venator +0.13, Paradox +0.12, Wraith +0.10 | 0 heroes |
| Healbane | 1,600 | -0.001 | -0.001 | +0.066 | Yamato +0.05, Bebop +0.05, Wraith +0.03 | 17 heroes |
| Counterspell | 3,200 | -0.010 | -0.003 | +0.043 | Pocket +0.06, Lash +0.04, Wraith +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.032 | -0.005 | +0.085 | Mo & Krill +0.12, Ivy +0.10, Haze +0.09 | 0 heroes |
| Metal Skin | 3,200 | -0.118 | -0.037 | +0.084 | Wraith +0.22, Paradox +0.16, Graves +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.147 | -0.092 | +0.055 | Wraith +0.07, Paradox +0.06, The Doorman +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.14), Unstoppable +0.04 (+0.12), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.04 (+0.20), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Witchmail +0.06 (+0.21), Divine Barrier +0.04 (+0.10), Counterspell +0.04 (+0.08)
- **Lady Geist**: Return Fire +0.05 (+0.10), Divine Barrier +0.03 (+0.09), Bullet Resilience +0.03 (+0.09)
- **Abrams**: Unstoppable +0.08 (+0.17), Indomitable +0.07 (+0.18), Healbane +0.03 (+0.10)
- **Wraith**: Indomitable +0.28 (+0.40), Metal Skin +0.22 (+0.30), Spellbreaker +0.14 (+0.26)
- **McGinnis**: Spirit Resilience +0.08 (+0.19), Healbane +0.01 (+0.07), Spellbreaker +0.01 (+0.12)
- **Paradox**: Metal Skin +0.16 (+0.24), Bullet Resilience +0.12 (+0.18), Plated Armor +0.10 (+0.20)
- **Dynamo**: Healbane +0.00 (+0.07), Counterspell -0.02 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Debuff Reducer -0.02 (+0.02)
- **Haze**: Indomitable +0.11 (+0.22), Plated Armor +0.09 (+0.19), Unstoppable +0.09 (+0.18)
- **Holliday**: Return Fire +0.04 (+0.09), Debuff Reducer +0.03 (+0.07), Indomitable +0.03 (+0.14)
- **Bebop**: Healbane +0.05 (+0.11), Counterspell +0.01 (+0.05), Metal Skin +0.00 (+0.09)
- **Calico**: Reactive Barrier +0.05 (+0.08), Divine Barrier +0.03 (+0.09), Spellbreaker +0.02 (+0.14)
- **Grey Talon**: Debuff Reducer +0.04 (+0.08), Spellbreaker +0.03 (+0.14), Reactive Barrier +0.02 (+0.06)
- **Mo & Krill**: Unstoppable +0.12 (+0.21), Dispel Magic +0.05 (+0.10), Spellbreaker +0.04 (+0.16)
- **Shiv**: Metal Skin +0.04 (+0.12), Divine Barrier +0.04 (+0.10), Bullet Resilience +0.03 (+0.09)
- **Ivy**: Unstoppable +0.10 (+0.19), Indomitable +0.09 (+0.20), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.07), Debuff Reducer -0.00 (+0.04), Counterspell -0.01 (+0.04)
- **Yamato**: Healbane +0.05 (+0.12), Counterspell +0.01 (+0.05), Debuff Reducer +0.00 (+0.04)
- **Lash**: Spirit Resilience +0.36 (+0.48), Spellbreaker +0.35 (+0.47), Divine Barrier +0.20 (+0.26)
- **Viscous**: Healbane +0.01 (+0.08), Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.24 (+0.35), Spellbreaker +0.15 (+0.26), Witchmail +0.14 (+0.29)
- **Mirage**: Dispel Magic +0.31 (+0.36), Spellbreaker +0.02 (+0.14), Spirit Resilience +0.02 (+0.13)
- **Vyper**: Indomitable +0.33 (+0.44), Metal Skin +0.05 (+0.13), Debuff Reducer +0.04 (+0.08)
- **Sinclair**: Indomitable +0.08 (+0.19), Spellbreaker +0.01 (+0.13), Return Fire +0.00 (+0.06)
- **Mina**: Witchmail +0.02 (+0.18), Divine Barrier +0.02 (+0.08), Spirit Resilience +0.02 (+0.13)
- **Drifter**: Witchmail +0.07 (+0.23), Bullet Resilience +0.04 (+0.10), Spirit Resilience +0.03 (+0.14)
- **Venator**: Bullet Resilience +0.13 (+0.19), Metal Skin +0.09 (+0.18), Plated Armor +0.06 (+0.16)
- **Victor**: Spellbreaker +0.04 (+0.16), Spirit Resilience +0.01 (+0.13), Healbane +0.01 (+0.08)
- **Paige**: Return Fire +0.01 (+0.07), Counterspell +0.00 (+0.05), Healbane -0.01 (+0.05)
- **The Doorman**: Spirit Resilience +0.15 (+0.26), Indomitable +0.14 (+0.25), Witchmail +0.11 (+0.27)
- **Billy**: Spirit Resilience +0.01 (+0.12), Counterspell -0.00 (+0.04), Spellbreaker -0.00 (+0.11)
- **Graves**: Witchmail +0.18 (+0.33), Metal Skin +0.14 (+0.22), Spirit Resilience +0.13 (+0.25)
- **Apollo**: Reactive Barrier +0.04 (+0.07), Unstoppable +0.00 (+0.09), Indomitable -0.00 (+0.11)
- **Deadman Danny**: Plated Armor +0.23 (+0.33), Spirit Resilience +0.21 (+0.32), Spellbreaker +0.15 (+0.27)
- **Rem**: Counterspell -0.00 (+0.04), Reactive Barrier -0.01 (+0.03), Divine Barrier -0.01 (+0.05)
- **Silver**: Dispel Magic +0.04 (+0.08), Return Fire +0.01 (+0.06), Metal Skin +0.00 (+0.09)
- **Celeste**: Witchmail +0.01 (+0.17), Spirit Resilience -0.00 (+0.11), Healbane -0.01 (+0.06)
- **Rat King**: Return Fire -0.01 (+0.05), Bullet Resilience -0.01 (+0.06), Counterspell -0.01 (+0.03)
- **Solomon**: Return Fire +0.00 (+0.06), Counterspell -0.02 (+0.02), Debuff Reducer -0.02 (+0.02)
- **Violet**: Return Fire +0.03 (+0.09), Witchmail +0.03 (+0.18), Healbane +0.01 (+0.08)
- **Nurse Harrow**: Healbane +0.02 (+0.08), Dispel Magic -0.02 (+0.03), Counterspell -0.03 (+0.01)
- **Baba**: Healbane +0.01 (+0.08), Unstoppable +0.01 (+0.09), Debuff Reducer -0.01 (+0.03)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.204 | +0.064 | +0.119 | Lash +0.26, Deadman Danny +0.25, The Doorman +0.15 | 14 heroes |
| Divine Barrier | 6,400 | +0.266 | +0.042 | +0.057 | Lash +0.20, Vindicta +0.12, Paradox +0.11 | 2 heroes |
| Dispel Magic | 3,200 | +0.121 | +0.038 | +0.062 | Mirage +0.29, Lash +0.28, Paradox +0.13 | 9 heroes |
| Witchmail | 6,400 | +0.199 | +0.031 | +0.154 | Lash +0.18, Paradox +0.14, The Doorman +0.12 | 1 heroes |
| Indomitable | 6,400 | +0.175 | +0.029 | +0.126 | Vyper +0.37, Wraith +0.29, Deadman Danny +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.159 | +0.025 | +0.128 | Lash +0.38, Deadman Danny +0.17, Wraith +0.15 | 0 heroes |
| Debuff Reducer | 1,600 | +0.033 | +0.020 | +0.043 | Grey Talon +0.09, Vyper +0.07, Wraith +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | +0.021 | +0.013 | +0.035 | Deadman Danny +0.09, Wraith +0.09, The Doorman +0.08 | 5 heroes |
| Plated Armor | 6,400 | +0.031 | +0.005 | +0.112 | Deadman Danny +0.25, Wraith +0.15, Holliday +0.12 | 0 heroes |
| Bullet Resilience | 3,200 | -0.010 | -0.003 | +0.059 | Lash +0.11, Venator +0.11, Vindicta +0.11 | 1 heroes |
| Healbane | 1,600 | -0.007 | -0.004 | +0.060 | Abrams +0.04, Nurse Harrow +0.04, Infernus +0.04 | 15 heroes |
| Unstoppable | 6,400 | -0.028 | -0.004 | +0.093 | Abrams +0.15, Grey Talon +0.11, Paige +0.11 | 3 heroes |
| Counterspell | 3,200 | -0.019 | -0.006 | +0.034 | Yamato +0.04, The Doorman +0.03, Vindicta +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.107 | -0.033 | +0.099 | Wraith +0.25, Lash +0.18, Paradox +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.147 | -0.092 | +0.052 | Wraith +0.09, Paradox +0.06, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.17), Spellbreaker +0.10 (+0.23), Unstoppable +0.09 (+0.19)
- **Seven**: Witchmail +0.05 (+0.21), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03)
- **Vindicta**: Divine Barrier +0.12 (+0.18), Bullet Resilience +0.11 (+0.16), Plated Armor +0.09 (+0.21)
- **Lady Geist**: Return Fire +0.04 (+0.09), Divine Barrier +0.02 (+0.08), Metal Skin +0.02 (+0.12)
- **Abrams**: Unstoppable +0.15 (+0.25), Dispel Magic +0.08 (+0.14), Healbane +0.04 (+0.10)
- **Wraith**: Indomitable +0.29 (+0.42), Metal Skin +0.25 (+0.35), Plated Armor +0.15 (+0.26)
- **McGinnis**: Spirit Resilience +0.05 (+0.17), Witchmail +0.02 (+0.18), Return Fire +0.02 (+0.07)
- **Paradox**: Witchmail +0.14 (+0.29), Dispel Magic +0.13 (+0.19), Metal Skin +0.11 (+0.21)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell +0.00 (+0.04), Return Fire -0.03 (+0.02)
- **Kelvin**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02), Spirit Resilience -0.02 (+0.10)
- **Haze**: Indomitable +0.09 (+0.22), Plated Armor +0.08 (+0.19), Unstoppable +0.07 (+0.16)
- **Holliday**: Plated Armor +0.12 (+0.23), Debuff Reducer +0.03 (+0.07), Return Fire +0.02 (+0.08)
- **Bebop**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.02), Return Fire -0.02 (+0.03)
- **Calico**: Reactive Barrier +0.03 (+0.07), Spirit Resilience +0.03 (+0.15), Divine Barrier +0.02 (+0.08)
- **Grey Talon**: Spellbreaker +0.14 (+0.27), Unstoppable +0.11 (+0.21), Indomitable +0.10 (+0.23)
- **Mo & Krill**: Unstoppable +0.09 (+0.18), Spirit Resilience +0.05 (+0.17), Spellbreaker +0.05 (+0.17)
- **Shiv**: Metal Skin +0.06 (+0.16), Bullet Resilience +0.03 (+0.09), Divine Barrier +0.03 (+0.09)
- **Ivy**: Unstoppable +0.10 (+0.19), Indomitable +0.05 (+0.18), Debuff Reducer +0.03 (+0.07)
- **Warden**: Return Fire +0.03 (+0.09), Counterspell +0.02 (+0.06), Debuff Reducer +0.01 (+0.05)
- **Yamato**: Reactive Barrier +0.08 (+0.11), Counterspell +0.04 (+0.08), Debuff Reducer +0.04 (+0.08)
- **Lash**: Spellbreaker +0.38 (+0.51), Dispel Magic +0.28 (+0.34), Spirit Resilience +0.26 (+0.38)
- **Viscous**: Divine Barrier -0.00 (+0.06), Counterspell -0.01 (+0.02), Bullet Resilience -0.02 (+0.04)
- **Pocket**: Spirit Resilience +0.08 (+0.20), Witchmail +0.03 (+0.18), Spellbreaker +0.00 (+0.13)
- **Mirage**: Dispel Magic +0.29 (+0.35), Spirit Resilience +0.01 (+0.13), Healbane +0.00 (+0.07)
- **Vyper**: Indomitable +0.37 (+0.50), Debuff Reducer +0.07 (+0.11), Unstoppable +0.06 (+0.15)
- **Sinclair**: Indomitable +0.13 (+0.26), Return Fire +0.00 (+0.06), Unstoppable -0.00 (+0.09)
- **Mina**: Spirit Resilience +0.08 (+0.20), Witchmail +0.06 (+0.22), Spellbreaker +0.04 (+0.17)
- **Drifter**: Spirit Resilience +0.07 (+0.19), Witchmail +0.06 (+0.21), Bullet Resilience +0.03 (+0.09)
- **Venator**: Bullet Resilience +0.11 (+0.17), Metal Skin +0.09 (+0.19), Plated Armor +0.03 (+0.14)
- **Victor**: Healbane +0.04 (+0.10), Spellbreaker +0.01 (+0.14), Spirit Resilience +0.00 (+0.12)
- **Paige**: Unstoppable +0.11 (+0.21), Debuff Reducer +0.05 (+0.09), Counterspell -0.00 (+0.03)
- **The Doorman**: Spirit Resilience +0.15 (+0.27), Indomitable +0.14 (+0.27), Witchmail +0.12 (+0.27)
- **Billy**: Healbane -0.00 (+0.06), Reactive Barrier -0.01 (+0.03), Counterspell -0.01 (+0.02)
- **Graves**: Return Fire +0.03 (+0.08), Witchmail +0.03 (+0.18), Metal Skin +0.01 (+0.11)
- **Apollo**: Counterspell +0.00 (+0.04), Healbane -0.00 (+0.06), Unstoppable -0.00 (+0.09)
- **Deadman Danny**: Plated Armor +0.25 (+0.37), Spirit Resilience +0.25 (+0.37), Spellbreaker +0.17 (+0.30)
- **Rem**: Debuff Reducer +0.06 (+0.10), Unstoppable +0.05 (+0.14), Counterspell -0.00 (+0.03)
- **Silver**: Dispel Magic +0.08 (+0.15), Indomitable +0.04 (+0.17), Divine Barrier +0.03 (+0.09)
- **Celeste**: Witchmail +0.05 (+0.21), Dispel Magic +0.04 (+0.10), Spellbreaker +0.02 (+0.15)
- **Rat King**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.03), Bullet Resilience -0.01 (+0.05)
- **Solomon**: Return Fire +0.01 (+0.06), Reactive Barrier -0.00 (+0.03), Counterspell -0.00 (+0.03)
- **Violet**: Witchmail +0.07 (+0.23), Return Fire +0.03 (+0.08), Healbane +0.02 (+0.08)
- **Nurse Harrow**: Healbane +0.04 (+0.10), Counterspell -0.00 (+0.03), Debuff Reducer -0.03 (+0.02)
- **Baba**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02), Unstoppable -0.02 (+0.08)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.241 | +0.075 | +0.133 | Lash +0.55, Deadman Danny +0.35, The Doorman +0.31 | 15 heroes |
| Dispel Magic | 3,200 | +0.118 | +0.037 | +0.062 | Mirage +0.27, Silver +0.23, Lash +0.19 | 9 heroes |
| Indomitable | 6,400 | +0.209 | +0.034 | +0.155 | Wraith +0.28, Vyper +0.27, The Doorman +0.23 | 1 heroes |
| Witchmail | 6,400 | +0.196 | +0.031 | +0.152 | Lash +0.26, The Doorman +0.20, Deadman Danny +0.13 | 2 heroes |
| Spellbreaker | 6,400 | +0.174 | +0.027 | +0.136 | Lash +0.44, Deadman Danny +0.21, Grey Talon +0.18 | 0 heroes |
| Divine Barrier | 6,400 | +0.173 | +0.027 | +0.058 | Lash +0.26, Vindicta +0.14, The Doorman +0.13 | 3 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.046 | Lash +0.10, Grey Talon +0.10, Rem +0.07 | 0 heroes |
| Plated Armor | 6,400 | +0.015 | +0.002 | +0.103 | Deadman Danny +0.18, Vindicta +0.15, Lash +0.14 | 2 heroes |
| Reactive Barrier | 1,600 | +0.002 | +0.001 | +0.038 | Calico +0.12, Drifter +0.11, The Doorman +0.09 | 3 heroes |
| Unstoppable | 6,400 | -0.005 | -0.001 | +0.117 | Haze +0.26, Infernus +0.22, Grey Talon +0.19 | 8 heroes |
| Bullet Resilience | 3,200 | -0.023 | -0.007 | +0.056 | Lash +0.16, Venator +0.09, Vindicta +0.08 | 0 heroes |
| Healbane | 1,600 | -0.011 | -0.007 | +0.055 | Lady Geist +0.05, Nurse Harrow +0.04, Victor +0.04 | 14 heroes |
| Counterspell | 3,200 | -0.025 | -0.008 | +0.033 | Lash +0.12, The Doorman +0.07, Viscous +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.102 | -0.032 | +0.108 | Lash +0.24, Silver +0.20, Wraith +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.151 | -0.094 | +0.050 | The Doorman +0.07, Wraith +0.06, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.22 (+0.33), Dispel Magic +0.06 (+0.12), Spellbreaker +0.04 (+0.17)
- **Seven**: Witchmail +0.06 (+0.21), Counterspell -0.01 (+0.02), Spirit Resilience -0.01 (+0.12)
- **Vindicta**: Plated Armor +0.15 (+0.25), Divine Barrier +0.14 (+0.19), Bullet Resilience +0.08 (+0.13)
- **Lady Geist**: Healbane +0.05 (+0.10), Metal Skin +0.01 (+0.12), Bullet Resilience +0.01 (+0.07)
- **Abrams**: Unstoppable +0.10 (+0.21), Spellbreaker +0.05 (+0.18), Dispel Magic +0.04 (+0.10)
- **Wraith**: Indomitable +0.28 (+0.43), Metal Skin +0.16 (+0.27), Witchmail +0.07 (+0.22)
- **McGinnis**: Healbane +0.03 (+0.09), Counterspell +0.00 (+0.04), Spirit Resilience -0.02 (+0.12)
- **Paradox**: Unstoppable +0.18 (+0.30), Witchmail +0.09 (+0.24), Dispel Magic +0.08 (+0.14)
- **Dynamo**: Healbane +0.02 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.11 (+0.24), Spellbreaker +0.02 (+0.16), Witchmail +0.02 (+0.17)
- **Haze**: Unstoppable +0.26 (+0.38), Indomitable +0.08 (+0.24), Plated Armor +0.07 (+0.17)
- **Holliday**: Spellbreaker +0.05 (+0.19), Return Fire +0.03 (+0.08), Debuff Reducer +0.02 (+0.07)
- **Bebop**: Debuff Reducer +0.05 (+0.10), Spellbreaker +0.01 (+0.14), Healbane +0.01 (+0.06)
- **Calico**: Spirit Resilience +0.14 (+0.28), Divine Barrier +0.12 (+0.18), Reactive Barrier +0.12 (+0.16)
- **Grey Talon**: Unstoppable +0.19 (+0.31), Spellbreaker +0.18 (+0.31), Spirit Resilience +0.14 (+0.27)
- **Mo & Krill**: Unstoppable +0.06 (+0.18), Dispel Magic +0.04 (+0.10), Healbane +0.04 (+0.09)
- **Shiv**: Bullet Resilience +0.04 (+0.09), Metal Skin +0.03 (+0.14), Divine Barrier +0.02 (+0.08)
- **Ivy**: Unstoppable +0.14 (+0.26), Indomitable +0.09 (+0.24), Debuff Reducer +0.04 (+0.09)
- **Warden**: Plated Armor +0.03 (+0.13), Metal Skin +0.02 (+0.13), Healbane +0.02 (+0.07)
- **Yamato**: Reactive Barrier +0.06 (+0.10), Indomitable +0.04 (+0.19), Debuff Reducer +0.04 (+0.08)
- **Lash**: Spirit Resilience +0.55 (+0.68), Spellbreaker +0.44 (+0.58), Witchmail +0.26 (+0.41)
- **Viscous**: Divine Barrier +0.06 (+0.12), Counterspell +0.02 (+0.06), Debuff Reducer +0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.10 (+0.23), Witchmail +0.03 (+0.18), Spellbreaker +0.01 (+0.14)
- **Mirage**: Dispel Magic +0.27 (+0.33), Metal Skin +0.09 (+0.19), Plated Armor +0.02 (+0.12)
- **Vyper**: Indomitable +0.27 (+0.42), Plated Armor +0.13 (+0.23), Metal Skin +0.07 (+0.17)
- **Sinclair**: Indomitable +0.15 (+0.30), Spellbreaker +0.08 (+0.22), Reactive Barrier +0.06 (+0.09)
- **Mina**: Return Fire -0.00 (+0.05), Divine Barrier -0.00 (+0.06), Witchmail -0.01 (+0.14)
- **Drifter**: Indomitable +0.20 (+0.36), Spirit Resilience +0.18 (+0.31), Spellbreaker +0.11 (+0.25)
- **Venator**: Metal Skin +0.12 (+0.23), Bullet Resilience +0.09 (+0.14), Plated Armor +0.02 (+0.12)
- **Victor**: Spellbreaker +0.10 (+0.24), Spirit Resilience +0.06 (+0.19), Healbane +0.04 (+0.10)
- **Paige**: Counterspell +0.00 (+0.03), Return Fire -0.01 (+0.04), Healbane -0.02 (+0.04)
- **The Doorman**: Spirit Resilience +0.31 (+0.44), Indomitable +0.23 (+0.39), Witchmail +0.20 (+0.35)
- **Billy**: Healbane -0.01 (+0.05), Counterspell -0.01 (+0.02), Return Fire -0.02 (+0.03)
- **Graves**: Return Fire +0.02 (+0.07), Reactive Barrier -0.01 (+0.03), Counterspell -0.02 (+0.01)
- **Apollo**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02), Bullet Resilience -0.02 (+0.04)
- **Deadman Danny**: Spirit Resilience +0.35 (+0.48), Spellbreaker +0.21 (+0.34), Plated Armor +0.18 (+0.29)
- **Rem**: Debuff Reducer +0.07 (+0.11), Spellbreaker +0.04 (+0.17), Divine Barrier -0.00 (+0.05)
- **Silver**: Dispel Magic +0.23 (+0.30), Metal Skin +0.20 (+0.31), Indomitable +0.18 (+0.33)
- **Celeste**: Witchmail +0.09 (+0.25), Spirit Resilience +0.09 (+0.23), Healbane +0.04 (+0.10)
- **Rat King**: Return Fire -0.01 (+0.04), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.04)
- **Solomon**: Reactive Barrier -0.00 (+0.04), Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.04)
- **Violet**: Return Fire +0.03 (+0.08), Witchmail +0.02 (+0.18), Healbane -0.00 (+0.05)
- **Nurse Harrow**: Dispel Magic +0.10 (+0.17), Spirit Resilience +0.10 (+0.23), Bullet Resilience +0.05 (+0.10)
- **Baba**: Healbane -0.00 (+0.05), Counterspell -0.01 (+0.03), Debuff Reducer -0.03 (+0.02)
