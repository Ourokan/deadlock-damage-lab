# Counter items in the sim (phantom and up)

Built 2026-11-03T04:14:06Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.424 | +0.067 | +0.125 | Lash +0.20, Graves +0.16, Deadman Danny +0.11 | 0 heroes |
| Spirit Resilience | 3,200 | +0.204 | +0.064 | +0.116 | Deadman Danny +0.29, Lash +0.27, Graves +0.16 | 1 heroes |
| Dispel Magic | 3,200 | +0.109 | +0.034 | +0.074 | Mirage +0.32, Deadman Danny +0.15, Lash +0.15 | 3 heroes |
| Reactive Barrier | 1,600 | +0.049 | +0.031 | +0.060 | Deadman Danny +0.27, Graves +0.18, Abrams +0.07 | 3 heroes |
| Indomitable | 6,400 | +0.186 | +0.030 | +0.144 | Deadman Danny +0.33, Vyper +0.30, Abrams +0.23 | 0 heroes |
| Witchmail | 6,400 | +0.144 | +0.022 | +0.195 | Deadman Danny +0.31, Lash +0.22, Graves +0.19 | 0 heroes |
| Debuff Reducer | 1,600 | +0.032 | +0.020 | +0.072 | Deadman Danny +0.14, Vyper +0.11, Holliday +0.11 | 0 heroes |
| Spellbreaker | 6,400 | +0.086 | +0.013 | +0.154 | Deadman Danny +0.34, Lash +0.25, Holliday +0.14 | 0 heroes |
| Bullet Resilience | 3,200 | -0.002 | -0.001 | +0.093 | Deadman Danny +0.25, Lash +0.18, Venator +0.16 | 0 heroes |
| Plated Armor | 6,400 | -0.043 | -0.007 | +0.121 | Deadman Danny +0.29, Holliday +0.21, Lash +0.17 | 0 heroes |
| Unstoppable | 6,400 | -0.059 | -0.009 | +0.132 | Deadman Danny +0.27, Ivy +0.13, Abrams +0.11 | 0 heroes |
| Counterspell | 3,200 | -0.033 | -0.010 | +0.070 | Deadman Danny +0.15, Lash +0.08, Pocket +0.07 | 1 heroes |
| Healbane | 1,600 | -0.042 | -0.026 | +0.080 | Yamato +0.08, Graves +0.08, Pocket +0.06 | 18 heroes |
| Metal Skin | 3,200 | -0.174 | -0.054 | +0.096 | Lash +0.19, Graves +0.19, Wraith +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.185 | -0.116 | +0.082 | Deadman Danny +0.14, Graves +0.10, Pocket +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.08 (+0.15), Spellbreaker +0.05 (+0.21), Spirit Resilience +0.04 (+0.15)
- **Seven**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Witchmail -0.03 (+0.16)
- **Vindicta**: Return Fire -0.00 (+0.08), Divine Barrier -0.00 (+0.12), Counterspell -0.02 (+0.05)
- **Lady Geist**: Return Fire -0.00 (+0.08), Healbane -0.02 (+0.06), Counterspell -0.02 (+0.05)
- **Abrams**: Indomitable +0.23 (+0.37), Unstoppable +0.11 (+0.25), Spirit Resilience +0.09 (+0.20)
- **Wraith**: Indomitable +0.18 (+0.33), Metal Skin +0.15 (+0.25), Spellbreaker +0.12 (+0.28)
- **McGinnis**: Spirit Resilience -0.02 (+0.10), Return Fire -0.02 (+0.06), Healbane -0.02 (+0.06)
- **Paradox**: Metal Skin +0.08 (+0.18), Bullet Resilience +0.08 (+0.17), Return Fire +0.07 (+0.15)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.02 (+0.05), Plated Armor -0.04 (+0.08)
- **Kelvin**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Dispel Magic -0.04 (+0.03)
- **Haze**: Indomitable +0.10 (+0.25), Unstoppable +0.07 (+0.20), Plated Armor +0.03 (+0.16)
- **Holliday**: Plated Armor +0.21 (+0.33), Spellbreaker +0.14 (+0.29), Debuff Reducer +0.11 (+0.18)
- **Bebop**: Healbane +0.03 (+0.11), Counterspell +0.01 (+0.08), Divine Barrier -0.00 (+0.12)
- **Calico**: Spellbreaker +0.08 (+0.23), Divine Barrier +0.05 (+0.17), Spirit Resilience +0.03 (+0.14)
- **Grey Talon**: Unstoppable +0.06 (+0.19), Spellbreaker +0.05 (+0.21), Debuff Reducer +0.05 (+0.12)
- **Mo & Krill**: Spellbreaker +0.06 (+0.21), Spirit Resilience +0.03 (+0.14), Dispel Magic +0.02 (+0.10)
- **Shiv**: Return Fire -0.01 (+0.07), Healbane -0.01 (+0.07), Spirit Resilience -0.02 (+0.10)
- **Ivy**: Indomitable +0.15 (+0.30), Unstoppable +0.13 (+0.26), Debuff Reducer +0.02 (+0.09)
- **Warden**: Debuff Reducer +0.01 (+0.08), Return Fire +0.01 (+0.09), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.08 (+0.16), Debuff Reducer +0.04 (+0.11), Counterspell +0.00 (+0.07)
- **Lash**: Spirit Resilience +0.27 (+0.38), Spellbreaker +0.25 (+0.40), Witchmail +0.22 (+0.41)
- **Viscous**: Counterspell +0.04 (+0.11), Return Fire +0.03 (+0.11), Divine Barrier +0.01 (+0.13)
- **Pocket**: Return Fire +0.08 (+0.16), Counterspell +0.07 (+0.14), Dispel Magic +0.07 (+0.14)
- **Mirage**: Dispel Magic +0.32 (+0.39), Spellbreaker +0.07 (+0.23), Spirit Resilience +0.05 (+0.16)
- **Vyper**: Indomitable +0.30 (+0.44), Debuff Reducer +0.11 (+0.19), Spellbreaker +0.10 (+0.25)
- **Sinclair**: Indomitable +0.14 (+0.29), Spellbreaker +0.04 (+0.20), Debuff Reducer +0.01 (+0.08)
- **Mina**: Return Fire +0.02 (+0.11), Spirit Resilience +0.01 (+0.13), Divine Barrier +0.01 (+0.14)
- **Drifter**: Healbane +0.00 (+0.09), Debuff Reducer -0.02 (+0.05), Counterspell -0.02 (+0.05)
- **Venator**: Bullet Resilience +0.16 (+0.25), Debuff Reducer +0.04 (+0.11), Unstoppable +0.03 (+0.16)
- **Victor**: Spirit Resilience -0.00 (+0.11), Healbane -0.00 (+0.08), Spellbreaker -0.03 (+0.13)
- **Paige**: Divine Barrier +0.01 (+0.14), Return Fire +0.01 (+0.09), Counterspell +0.00 (+0.07)
- **The Doorman**: Indomitable +0.14 (+0.28), Spirit Resilience +0.13 (+0.24), Spellbreaker +0.12 (+0.28)
- **Billy**: Spirit Resilience +0.05 (+0.17), Spellbreaker +0.05 (+0.20), Healbane +0.05 (+0.13)
- **Graves**: Witchmail +0.19 (+0.39), Metal Skin +0.19 (+0.28), Reactive Barrier +0.18 (+0.24)
- **Apollo**: Reactive Barrier -0.00 (+0.06), Healbane -0.02 (+0.06), Unstoppable -0.03 (+0.11)
- **Deadman Danny**: Spellbreaker +0.34 (+0.50), Indomitable +0.33 (+0.48), Witchmail +0.31 (+0.50)
- **Rem**: Counterspell -0.02 (+0.05), Debuff Reducer -0.03 (+0.04), Reactive Barrier -0.03 (+0.03)
- **Silver**: Dispel Magic +0.12 (+0.20), Indomitable +0.05 (+0.19), Metal Skin +0.04 (+0.14)
- **Celeste**: Spirit Resilience +0.08 (+0.20), Witchmail +0.06 (+0.26), Dispel Magic +0.00 (+0.08)
- **Rat King**: Return Fire +0.01 (+0.09), Counterspell -0.00 (+0.07), Divine Barrier -0.01 (+0.11)
- **Solomon**: Healbane -0.02 (+0.06), Counterspell -0.03 (+0.04), Witchmail -0.03 (+0.16)
- **Violet**: Return Fire +0.00 (+0.08), Healbane -0.01 (+0.07), Witchmail -0.02 (+0.18)
- **Nurse Harrow**: Healbane +0.01 (+0.09), Counterspell -0.04 (+0.03), Reactive Barrier -0.05 (+0.01)
- **Baba**: Healbane -0.01 (+0.07), Unstoppable -0.02 (+0.11), Debuff Reducer -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.189 | +0.059 | +0.114 | Graves +0.31, Pocket +0.29, Lash +0.22 | 9 heroes |
| Divine Barrier | 6,400 | +0.288 | +0.046 | +0.092 | Graves +0.23, Lash +0.14, Paradox +0.10 | 0 heroes |
| Dispel Magic | 3,200 | +0.102 | +0.032 | +0.052 | Mirage +0.25, Graves +0.23, Infernus +0.11 | 6 heroes |
| Indomitable | 6,400 | +0.177 | +0.028 | +0.117 | Vyper +0.38, Graves +0.22, Wraith +0.18 | 0 heroes |
| Witchmail | 6,400 | +0.155 | +0.024 | +0.162 | Graves +0.31, Lash +0.13, Grey Talon +0.12 | 0 heroes |
| Spellbreaker | 6,400 | +0.117 | +0.018 | +0.131 | Graves +0.20, Lash +0.20, Grey Talon +0.15 | 0 heroes |
| Reactive Barrier | 1,600 | +0.027 | +0.017 | +0.035 | Graves +0.25, Grey Talon +0.13, The Doorman +0.10 | 4 heroes |
| Debuff Reducer | 1,600 | +0.008 | +0.005 | +0.056 | Graves +0.13, Vyper +0.12, Grey Talon +0.10 | 1 heroes |
| Plated Armor | 6,400 | -0.035 | -0.005 | +0.092 | Graves +0.24, Holliday +0.16, Deadman Danny +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | -0.035 | -0.011 | +0.061 | Venator +0.16, Graves +0.14, Paradox +0.10 | 0 heroes |
| Unstoppable | 6,400 | -0.088 | -0.014 | +0.100 | Grey Talon +0.19, Graves +0.17, Mo & Krill +0.11 | 0 heroes |
| Counterspell | 3,200 | -0.045 | -0.014 | +0.044 | Graves +0.15, Grey Talon +0.10, Paradox +0.05 | 1 heroes |
| Healbane | 1,600 | -0.059 | -0.037 | +0.064 | Graves +0.18, Bebop +0.06, Seven +0.05 | 23 heroes |
| Metal Skin | 3,200 | -0.194 | -0.061 | +0.075 | Graves +0.26, Wraith +0.14, Lash +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.194 | -0.121 | +0.058 | Paradox +0.10, Graves +0.08, Wraith +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.17), Spellbreaker +0.08 (+0.21), Unstoppable +0.06 (+0.16)
- **Seven**: Witchmail +0.07 (+0.24), Healbane +0.05 (+0.12), Counterspell +0.02 (+0.06)
- **Vindicta**: Divine Barrier +0.04 (+0.14), Return Fire +0.04 (+0.09), Bullet Resilience +0.03 (+0.09)
- **Lady Geist**: Spirit Resilience +0.06 (+0.18), Spellbreaker +0.05 (+0.18), Return Fire +0.02 (+0.08)
- **Abrams**: Indomitable +0.15 (+0.27), Unstoppable +0.07 (+0.17), Divine Barrier +0.02 (+0.12)
- **Wraith**: Indomitable +0.18 (+0.30), Metal Skin +0.14 (+0.22), Debuff Reducer +0.10 (+0.15)
- **McGinnis**: Spirit Resilience +0.04 (+0.16), Healbane +0.02 (+0.08), Return Fire -0.00 (+0.06)
- **Paradox**: Divine Barrier +0.10 (+0.19), Return Fire +0.10 (+0.15), Bullet Resilience +0.10 (+0.16)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.04), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.05 (+0.16), Dispel Magic +0.03 (+0.08), Counterspell +0.03 (+0.07)
- **Haze**: Indomitable +0.07 (+0.19), Plated Armor +0.05 (+0.15), Unstoppable +0.05 (+0.15)
- **Holliday**: Plated Armor +0.16 (+0.25), Spellbreaker +0.11 (+0.24), Unstoppable +0.09 (+0.19)
- **Bebop**: Healbane +0.06 (+0.12), Metal Skin +0.00 (+0.08), Counterspell -0.01 (+0.04)
- **Calico**: Reactive Barrier +0.05 (+0.09), Divine Barrier +0.05 (+0.14), Spellbreaker +0.03 (+0.16)
- **Grey Talon**: Unstoppable +0.19 (+0.29), Spellbreaker +0.15 (+0.28), Reactive Barrier +0.13 (+0.17)
- **Mo & Krill**: Unstoppable +0.11 (+0.21), Spellbreaker +0.10 (+0.24), Dispel Magic +0.05 (+0.10)
- **Shiv**: Bullet Resilience +0.06 (+0.12), Return Fire +0.04 (+0.10), Divine Barrier +0.03 (+0.12)
- **Ivy**: Unstoppable +0.11 (+0.21), Indomitable +0.09 (+0.21), Debuff Reducer +0.02 (+0.08)
- **Warden**: Return Fire +0.05 (+0.10), Witchmail +0.03 (+0.19), Bullet Resilience +0.02 (+0.08)
- **Yamato**: Spellbreaker +0.07 (+0.20), Unstoppable +0.06 (+0.16), Bullet Resilience +0.04 (+0.11)
- **Lash**: Spirit Resilience +0.22 (+0.34), Spellbreaker +0.20 (+0.33), Divine Barrier +0.14 (+0.23)
- **Viscous**: Return Fire -0.01 (+0.04), Healbane -0.02 (+0.05), Counterspell -0.02 (+0.03)
- **Pocket**: Spirit Resilience +0.29 (+0.40), Spellbreaker +0.14 (+0.27), Witchmail +0.12 (+0.28)
- **Mirage**: Dispel Magic +0.25 (+0.30), Spirit Resilience +0.03 (+0.15), Spellbreaker +0.03 (+0.16)
- **Vyper**: Indomitable +0.38 (+0.49), Spellbreaker +0.13 (+0.26), Debuff Reducer +0.12 (+0.17)
- **Sinclair**: Indomitable +0.05 (+0.17), Return Fire -0.01 (+0.05), Debuff Reducer -0.01 (+0.04)
- **Mina**: Witchmail -0.00 (+0.16), Return Fire -0.01 (+0.05), Divine Barrier -0.01 (+0.08)
- **Drifter**: Spirit Resilience -0.01 (+0.11), Debuff Reducer -0.01 (+0.04), Return Fire -0.02 (+0.04)
- **Venator**: Bullet Resilience +0.16 (+0.22), Metal Skin +0.12 (+0.19), Plated Armor +0.06 (+0.15)
- **Victor**: Spellbreaker +0.07 (+0.20), Spirit Resilience +0.06 (+0.17), Healbane +0.01 (+0.08)
- **Paige**: Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.08), Return Fire -0.02 (+0.04)
- **The Doorman**: Indomitable +0.14 (+0.26), Spirit Resilience +0.13 (+0.24), Spellbreaker +0.10 (+0.23)
- **Billy**: Spellbreaker +0.01 (+0.14), Counterspell +0.01 (+0.05), Healbane +0.01 (+0.07)
- **Graves**: Witchmail +0.31 (+0.47), Spirit Resilience +0.31 (+0.42), Metal Skin +0.26 (+0.34)
- **Apollo**: Reactive Barrier +0.03 (+0.06), Counterspell -0.01 (+0.04), Indomitable -0.02 (+0.10)
- **Deadman Danny**: Indomitable +0.17 (+0.29), Spirit Resilience +0.17 (+0.28), Plated Armor +0.09 (+0.18)
- **Rem**: Witchmail -0.00 (+0.16), Dispel Magic -0.01 (+0.04), Reactive Barrier -0.02 (+0.02)
- **Silver**: Dispel Magic +0.05 (+0.10), Debuff Reducer +0.02 (+0.08), Return Fire +0.02 (+0.08)
- **Celeste**: Witchmail +0.12 (+0.28), Spirit Resilience +0.10 (+0.21), Spellbreaker +0.04 (+0.17)
- **Rat King**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.04), Bullet Resilience -0.01 (+0.05)
- **Solomon**: Return Fire -0.01 (+0.04), Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (+0.01)
- **Violet**: Return Fire +0.01 (+0.07), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03)
- **Nurse Harrow**: Dispel Magic -0.01 (+0.04), Divine Barrier -0.01 (+0.08), Counterspell -0.02 (+0.03)
- **Baba**: Unstoppable +0.06 (+0.16), Debuff Reducer +0.01 (+0.07), Healbane +0.01 (+0.07)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.196 | +0.061 | +0.139 | Lash +0.40, Deadman Danny +0.17, Paradox +0.17 | 14 heroes |
| Divine Barrier | 6,400 | +0.311 | +0.049 | +0.101 | Lash +0.13, Viscous +0.13, Paradox +0.11 | 2 heroes |
| Dispel Magic | 3,200 | +0.113 | +0.035 | +0.061 | Lash +0.22, Mirage +0.22, Infernus +0.13 | 9 heroes |
| Indomitable | 6,400 | +0.189 | +0.030 | +0.136 | Vyper +0.31, Wraith +0.25, The Doorman +0.17 | 0 heroes |
| Spellbreaker | 6,400 | +0.149 | +0.023 | +0.171 | Lash +0.36, Holliday +0.18, Deadman Danny +0.17 | 0 heroes |
| Witchmail | 6,400 | +0.146 | +0.023 | +0.169 | Lash +0.18, Wraith +0.12, Graves +0.12 | 1 heroes |
| Debuff Reducer | 1,600 | +0.017 | +0.011 | +0.072 | Holliday +0.18, Grey Talon +0.14, Wraith +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | +0.002 | +0.001 | +0.041 | Yamato +0.16, Grey Talon +0.08, Wraith +0.08 | 3 heroes |
| Plated Armor | 6,400 | -0.034 | -0.005 | +0.091 | Wraith +0.13, Vindicta +0.09, Yamato +0.08 | 0 heroes |
| Unstoppable | 6,400 | -0.077 | -0.012 | +0.118 | Haze +0.17, Grey Talon +0.15, Mo & Krill +0.14 | 4 heroes |
| Bullet Resilience | 3,200 | -0.046 | -0.014 | +0.059 | Venator +0.17, Vindicta +0.12, Lady Geist +0.09 | 1 heroes |
| Counterspell | 3,200 | -0.049 | -0.015 | +0.041 | Abrams +0.05, Nurse Harrow +0.04, Yamato +0.03 | 1 heroes |
| Healbane | 1,600 | -0.054 | -0.034 | +0.068 | Abrams +0.12, Lady Geist +0.08, Mo & Krill +0.07 | 20 heroes |
| Metal Skin | 3,200 | -0.187 | -0.058 | +0.086 | Wraith +0.21, Graves +0.13, Lash +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.184 | -0.115 | +0.062 | Paradox +0.08, Venator +0.07, Vindicta +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.13 (+0.19), Spellbreaker +0.11 (+0.28), Unstoppable +0.05 (+0.17)
- **Seven**: Indomitable +0.08 (+0.21), Witchmail +0.06 (+0.22), Debuff Reducer +0.05 (+0.12)
- **Vindicta**: Bullet Resilience +0.12 (+0.18), Plated Armor +0.09 (+0.18), Divine Barrier +0.07 (+0.17)
- **Lady Geist**: Bullet Resilience +0.09 (+0.15), Healbane +0.08 (+0.15), Metal Skin +0.07 (+0.16)
- **Abrams**: Healbane +0.12 (+0.19), Dispel Magic +0.09 (+0.16), Unstoppable +0.07 (+0.19)
- **Wraith**: Indomitable +0.25 (+0.39), Metal Skin +0.21 (+0.29), Spellbreaker +0.14 (+0.31)
- **McGinnis**: Spirit Resilience +0.11 (+0.25), Witchmail +0.07 (+0.24), Spellbreaker +0.03 (+0.20)
- **Paradox**: Spirit Resilience +0.17 (+0.31), Indomitable +0.14 (+0.27), Witchmail +0.11 (+0.28)
- **Dynamo**: Healbane -0.01 (+0.06), Counterspell -0.02 (+0.02), Reactive Barrier -0.05 (-0.00)
- **Kelvin**: Spirit Resilience +0.12 (+0.26), Dispel Magic +0.09 (+0.15), Witchmail +0.07 (+0.24)
- **Haze**: Unstoppable +0.17 (+0.29), Return Fire +0.02 (+0.08), Plated Armor +0.01 (+0.10)
- **Holliday**: Spellbreaker +0.18 (+0.35), Debuff Reducer +0.18 (+0.25), Unstoppable +0.14 (+0.26)
- **Bebop**: Healbane +0.02 (+0.09), Counterspell -0.03 (+0.01), Metal Skin -0.03 (+0.06)
- **Calico**: Spirit Resilience +0.10 (+0.24), Reactive Barrier +0.07 (+0.11), Divine Barrier +0.06 (+0.16)
- **Grey Talon**: Spellbreaker +0.17 (+0.34), Unstoppable +0.15 (+0.27), Debuff Reducer +0.14 (+0.21)
- **Mo & Krill**: Unstoppable +0.14 (+0.26), Spirit Resilience +0.08 (+0.22), Spellbreaker +0.07 (+0.24)
- **Shiv**: Bullet Resilience +0.08 (+0.14), Metal Skin +0.06 (+0.15), Plated Armor +0.05 (+0.14)
- **Ivy**: Unstoppable +0.04 (+0.16), Debuff Reducer +0.02 (+0.09), Bullet Resilience +0.01 (+0.07)
- **Warden**: Debuff Reducer +0.04 (+0.11), Return Fire +0.02 (+0.09), Counterspell +0.02 (+0.06)
- **Yamato**: Indomitable +0.17 (+0.30), Reactive Barrier +0.16 (+0.20), Spellbreaker +0.10 (+0.27)
- **Lash**: Spirit Resilience +0.40 (+0.54), Spellbreaker +0.36 (+0.53), Dispel Magic +0.22 (+0.28)
- **Viscous**: Divine Barrier +0.13 (+0.23), Spirit Resilience +0.07 (+0.21), Metal Skin +0.06 (+0.14)
- **Pocket**: Spirit Resilience +0.10 (+0.24), Witchmail +0.01 (+0.18), Return Fire -0.02 (+0.05)
- **Mirage**: Dispel Magic +0.22 (+0.28), Plated Armor +0.01 (+0.10), Metal Skin -0.00 (+0.08)
- **Vyper**: Indomitable +0.31 (+0.45), Spellbreaker +0.10 (+0.27), Debuff Reducer +0.06 (+0.13)
- **Sinclair**: Indomitable +0.11 (+0.25), Return Fire +0.01 (+0.07), Unstoppable -0.00 (+0.12)
- **Mina**: Divine Barrier +0.06 (+0.16), Witchmail +0.05 (+0.22), Spirit Resilience +0.04 (+0.18)
- **Drifter**: Healbane +0.01 (+0.08), Indomitable +0.00 (+0.14), Counterspell -0.00 (+0.04)
- **Venator**: Bullet Resilience +0.17 (+0.23), Metal Skin +0.09 (+0.18), Return Fire +0.07 (+0.13)
- **Victor**: Healbane -0.01 (+0.05), Spellbreaker -0.02 (+0.15), Counterspell -0.03 (+0.01)
- **Paige**: Counterspell -0.00 (+0.04), Healbane -0.02 (+0.05), Divine Barrier -0.02 (+0.08)
- **The Doorman**: Indomitable +0.17 (+0.31), Spirit Resilience +0.15 (+0.29), Witchmail +0.11 (+0.28)
- **Billy**: Indomitable +0.06 (+0.19), Reactive Barrier +0.02 (+0.06), Debuff Reducer -0.00 (+0.07)
- **Graves**: Spirit Resilience +0.16 (+0.30), Metal Skin +0.13 (+0.22), Witchmail +0.12 (+0.29)
- **Apollo**: Reactive Barrier +0.00 (+0.04), Healbane -0.00 (+0.07), Counterspell -0.01 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.17 (+0.31), Spellbreaker +0.17 (+0.34), Indomitable +0.11 (+0.25)
- **Rem**: Debuff Reducer +0.09 (+0.16), Unstoppable +0.07 (+0.18), Spellbreaker +0.03 (+0.20)
- **Silver**: Dispel Magic +0.07 (+0.14), Reactive Barrier +0.06 (+0.10), Divine Barrier +0.04 (+0.14)
- **Celeste**: Witchmail +0.06 (+0.23), Healbane +0.02 (+0.08), Spirit Resilience -0.01 (+0.13)
- **Rat King**: Counterspell +0.01 (+0.05), Return Fire -0.00 (+0.06), Metal Skin -0.00 (+0.08)
- **Solomon**: Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.05), Reactive Barrier -0.02 (+0.02)
- **Violet**: Return Fire +0.01 (+0.07), Witchmail +0.01 (+0.18), Healbane -0.00 (+0.07)
- **Nurse Harrow**: Healbane +0.07 (+0.13), Counterspell +0.04 (+0.08), Divine Barrier +0.03 (+0.13)
- **Baba**: Healbane -0.00 (+0.06), Debuff Reducer -0.02 (+0.05), Counterspell -0.02 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.189 | +0.059 | +0.137 | Lash +0.55, The Doorman +0.29, Grey Talon +0.26 | 16 heroes |
| Dispel Magic | 3,200 | +0.111 | +0.035 | +0.054 | Mirage +0.31, Lash +0.17, Infernus +0.12 | 10 heroes |
| Indomitable | 6,400 | +0.203 | +0.032 | +0.153 | Wraith +0.40, Grey Talon +0.16, Sinclair +0.16 | 2 heroes |
| Spellbreaker | 6,400 | +0.173 | +0.027 | +0.199 | Lash +0.33, Grey Talon +0.32, Wraith +0.28 | 0 heroes |
| Witchmail | 6,400 | +0.148 | +0.023 | +0.170 | Lash +0.19, Paradox +0.18, Grey Talon +0.17 | 2 heroes |
| Divine Barrier | 6,400 | +0.133 | +0.021 | +0.081 | Lash +0.16, Paradox +0.14, Viscous +0.13 | 3 heroes |
| Debuff Reducer | 1,600 | +0.021 | +0.013 | +0.099 | Holliday +0.18, Grey Talon +0.18, Bebop +0.18 | 0 heroes |
| Plated Armor | 6,400 | -0.039 | -0.006 | +0.102 | Holliday +0.22, Wraith +0.15, Infernus +0.09 | 2 heroes |
| Unstoppable | 6,400 | -0.061 | -0.009 | +0.161 | Grey Talon +0.29, Paige +0.23, Paradox +0.22 | 8 heroes |
| Reactive Barrier | 1,600 | -0.017 | -0.011 | +0.032 | Yamato +0.10, Paradox +0.09, Deadman Danny +0.08 | 2 heroes |
| Bullet Resilience | 3,200 | -0.050 | -0.015 | +0.060 | Vindicta +0.14, Venator +0.12, Lady Geist +0.11 | 1 heroes |
| Counterspell | 3,200 | -0.059 | -0.018 | +0.030 | Viscous +0.06, Yamato +0.06, Nurse Harrow +0.04 | 1 heroes |
| Healbane | 1,600 | -0.063 | -0.039 | +0.059 | Lady Geist +0.07, Grey Talon +0.06, Victor +0.05 | 18 heroes |
| Metal Skin | 3,200 | -0.178 | -0.056 | +0.100 | Wraith +0.24, Lash +0.14, Venator +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.181 | -0.113 | +0.053 | Vindicta +0.11, Wraith +0.08, Viscous +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.17 (+0.33), Spellbreaker +0.14 (+0.34), Dispel Magic +0.12 (+0.18)
- **Seven**: Witchmail +0.02 (+0.19), Counterspell +0.02 (+0.05), Dispel Magic +0.01 (+0.06)
- **Vindicta**: Bullet Resilience +0.14 (+0.20), Return Fire +0.11 (+0.17), Divine Barrier +0.08 (+0.16)
- **Lady Geist**: Bullet Resilience +0.11 (+0.17), Healbane +0.07 (+0.13), Metal Skin +0.06 (+0.16)
- **Abrams**: Unstoppable +0.04 (+0.20), Debuff Reducer +0.02 (+0.12), Reactive Barrier +0.01 (+0.05)
- **Wraith**: Indomitable +0.40 (+0.55), Spellbreaker +0.28 (+0.48), Metal Skin +0.24 (+0.34)
- **McGinnis**: Spirit Resilience +0.04 (+0.17), Witchmail -0.00 (+0.17), Healbane -0.00 (+0.06)
- **Paradox**: Unstoppable +0.22 (+0.38), Witchmail +0.18 (+0.35), Divine Barrier +0.14 (+0.22)
- **Dynamo**: Counterspell -0.01 (+0.02), Healbane -0.02 (+0.04), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.08 (+0.21), Witchmail +0.04 (+0.21), Spellbreaker +0.01 (+0.21)
- **Haze**: Unstoppable +0.20 (+0.36), Return Fire +0.06 (+0.11), Bullet Resilience +0.05 (+0.11)
- **Holliday**: Plated Armor +0.22 (+0.32), Spellbreaker +0.20 (+0.40), Unstoppable +0.18 (+0.34)
- **Bebop**: Debuff Reducer +0.18 (+0.28), Spellbreaker +0.09 (+0.29), Unstoppable +0.08 (+0.25)
- **Calico**: Reactive Barrier +0.08 (+0.11), Divine Barrier +0.05 (+0.13), Indomitable +0.03 (+0.18)
- **Grey Talon**: Spellbreaker +0.32 (+0.52), Unstoppable +0.29 (+0.45), Spirit Resilience +0.26 (+0.40)
- **Mo & Krill**: Healbane +0.03 (+0.09), Dispel Magic +0.03 (+0.08), Spellbreaker +0.00 (+0.20)
- **Shiv**: Bullet Resilience +0.06 (+0.12), Metal Skin +0.05 (+0.15), Plated Armor +0.03 (+0.13)
- **Ivy**: Unstoppable +0.09 (+0.25), Indomitable +0.04 (+0.19), Debuff Reducer +0.01 (+0.11)
- **Warden**: Divine Barrier +0.02 (+0.10), Bullet Resilience +0.00 (+0.06), Plated Armor -0.00 (+0.10)
- **Yamato**: Indomitable +0.12 (+0.27), Reactive Barrier +0.10 (+0.13), Metal Skin +0.06 (+0.16)
- **Lash**: Spirit Resilience +0.55 (+0.69), Spellbreaker +0.33 (+0.52), Witchmail +0.19 (+0.36)
- **Viscous**: Spirit Resilience +0.15 (+0.28), Divine Barrier +0.13 (+0.21), Witchmail +0.08 (+0.25)
- **Pocket**: Spirit Resilience +0.04 (+0.18), Witchmail +0.01 (+0.18), Return Fire -0.01 (+0.04)
- **Mirage**: Dispel Magic +0.31 (+0.37), Plated Armor +0.05 (+0.15), Spellbreaker +0.04 (+0.24)
- **Vyper**: Indomitable +0.12 (+0.27), Plated Armor +0.07 (+0.17), Bullet Resilience +0.06 (+0.12)
- **Sinclair**: Indomitable +0.16 (+0.31), Spellbreaker +0.14 (+0.34), Spirit Resilience +0.13 (+0.27)
- **Mina**: Counterspell -0.00 (+0.03), Return Fire -0.01 (+0.04), Dispel Magic -0.02 (+0.04)
- **Drifter**: Witchmail +0.04 (+0.21), Healbane +0.02 (+0.07), Counterspell -0.01 (+0.02)
- **Venator**: Bullet Resilience +0.12 (+0.18), Metal Skin +0.11 (+0.21), Plated Armor +0.04 (+0.15)
- **Victor**: Spirit Resilience +0.08 (+0.21), Healbane +0.05 (+0.11), Spellbreaker +0.04 (+0.23)
- **Paige**: Unstoppable +0.23 (+0.39), Debuff Reducer +0.17 (+0.26), Spellbreaker +0.06 (+0.26)
- **The Doorman**: Spirit Resilience +0.29 (+0.42), Indomitable +0.13 (+0.28), Witchmail +0.12 (+0.29)
- **Billy**: Reactive Barrier +0.03 (+0.07), Healbane -0.01 (+0.05), Return Fire -0.02 (+0.04)
- **Graves**: Return Fire +0.02 (+0.07), Reactive Barrier +0.01 (+0.04), Metal Skin +0.00 (+0.10)
- **Apollo**: Healbane +0.02 (+0.08), Reactive Barrier +0.01 (+0.04), Counterspell -0.01 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.17 (+0.31), Witchmail +0.12 (+0.29), Indomitable +0.12 (+0.27)
- **Rem**: Debuff Reducer +0.05 (+0.15), Unstoppable +0.01 (+0.17), Counterspell +0.00 (+0.03)
- **Silver**: Bullet Resilience +0.08 (+0.14), Dispel Magic +0.07 (+0.12), Plated Armor +0.04 (+0.14)
- **Celeste**: Spirit Resilience +0.13 (+0.27), Witchmail +0.13 (+0.30), Divine Barrier +0.06 (+0.14)
- **Rat King**: Healbane -0.01 (+0.05), Debuff Reducer -0.01 (+0.09), Counterspell -0.01 (+0.02)
- **Solomon**: Counterspell +0.00 (+0.03), Reactive Barrier -0.00 (+0.03), Return Fire -0.02 (+0.03)
- **Violet**: Return Fire +0.05 (+0.10), Divine Barrier +0.01 (+0.09), Witchmail +0.00 (+0.17)
- **Nurse Harrow**: Spirit Resilience +0.07 (+0.21), Divine Barrier +0.06 (+0.14), Healbane +0.05 (+0.11)
- **Baba**: Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04), Return Fire -0.01 (+0.05)
