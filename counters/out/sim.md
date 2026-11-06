# Counter items in the sim (phantom and up)

Built 2026-11-06T20:51:40Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.207 | +0.065 | +0.116 | Lash +0.31, Deadman Danny +0.21, The Doorman +0.20 | 1 heroes |
| Divine Barrier | 6,400 | +0.328 | +0.052 | +0.126 | Lash +0.23, Graves +0.16, The Doorman +0.12 | 0 heroes |
| Dispel Magic | 3,200 | +0.109 | +0.034 | +0.073 | Mirage +0.32, Pocket +0.14, Lash +0.13 | 3 heroes |
| Indomitable | 6,400 | +0.186 | +0.029 | +0.142 | Vyper +0.31, Deadman Danny +0.25, Abrams +0.22 | 0 heroes |
| Reactive Barrier | 1,600 | +0.041 | +0.026 | +0.054 | Deadman Danny +0.21, Graves +0.18, Abrams +0.10 | 2 heroes |
| Witchmail | 6,400 | +0.141 | +0.022 | +0.190 | Lash +0.24, Deadman Danny +0.21, Graves +0.19 | 0 heroes |
| Debuff Reducer | 1,600 | +0.030 | +0.018 | +0.069 | Holliday +0.12, Deadman Danny +0.11, Vyper +0.09 | 0 heroes |
| Spellbreaker | 6,400 | +0.089 | +0.014 | +0.153 | Lash +0.28, Deadman Danny +0.26, Holliday +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | -0.006 | -0.002 | +0.088 | Deadman Danny +0.19, Venator +0.16, Lash +0.13 | 0 heroes |
| Plated Armor | 6,400 | -0.050 | -0.008 | +0.119 | Holliday +0.26, Deadman Danny +0.23, Lash +0.13 | 0 heroes |
| Unstoppable | 6,400 | -0.063 | -0.010 | +0.127 | Deadman Danny +0.21, Holliday +0.12, Ivy +0.11 | 0 heroes |
| Counterspell | 3,200 | -0.034 | -0.011 | +0.069 | Deadman Danny +0.12, Pocket +0.10, Lash +0.08 | 1 heroes |
| Healbane | 1,600 | -0.043 | -0.027 | +0.082 | Graves +0.09, Lash +0.09, McGinnis +0.07 | 20 heroes |
| Metal Skin | 3,200 | -0.175 | -0.055 | +0.095 | Lash +0.20, Graves +0.18, Wraith +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.185 | -0.116 | +0.080 | Deadman Danny +0.13, Pocket +0.09, Graves +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.07 (+0.14), Spellbreaker +0.04 (+0.19), Spirit Resilience +0.03 (+0.14)
- **Seven**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Witchmail -0.03 (+0.16)
- **Vindicta**: Return Fire -0.00 (+0.08), Divine Barrier -0.01 (+0.12), Counterspell -0.02 (+0.05)
- **Lady Geist**: Healbane +0.04 (+0.12), Counterspell +0.03 (+0.09), Return Fire +0.02 (+0.10)
- **Abrams**: Indomitable +0.22 (+0.36), Unstoppable +0.11 (+0.23), Divine Barrier +0.10 (+0.23)
- **Wraith**: Indomitable +0.17 (+0.31), Metal Skin +0.15 (+0.24), Spellbreaker +0.11 (+0.27)
- **McGinnis**: Healbane +0.07 (+0.15), Counterspell +0.02 (+0.09), Return Fire +0.02 (+0.10)
- **Paradox**: Metal Skin +0.09 (+0.18), Bullet Resilience +0.08 (+0.17), Return Fire +0.07 (+0.15)
- **Dynamo**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.04 (+0.01)
- **Kelvin**: Healbane -0.01 (+0.07), Counterspell -0.02 (+0.04), Dispel Magic -0.04 (+0.04)
- **Haze**: Indomitable +0.11 (+0.25), Unstoppable +0.08 (+0.21), Plated Armor +0.04 (+0.15)
- **Holliday**: Plated Armor +0.26 (+0.38), Spellbreaker +0.16 (+0.32), Debuff Reducer +0.12 (+0.19)
- **Bebop**: Healbane +0.03 (+0.11), Counterspell +0.02 (+0.09), Divine Barrier +0.00 (+0.13)
- **Calico**: Spellbreaker +0.08 (+0.23), Divine Barrier +0.05 (+0.17), Spirit Resilience +0.02 (+0.14)
- **Grey Talon**: Unstoppable +0.07 (+0.20), Spellbreaker +0.07 (+0.22), Reactive Barrier +0.06 (+0.11)
- **Mo & Krill**: Spellbreaker +0.07 (+0.23), Spirit Resilience +0.04 (+0.16), Dispel Magic +0.03 (+0.11)
- **Shiv**: Return Fire -0.01 (+0.07), Healbane -0.01 (+0.07), Bullet Resilience -0.02 (+0.07)
- **Ivy**: Indomitable +0.14 (+0.28), Unstoppable +0.11 (+0.24), Debuff Reducer +0.02 (+0.09)
- **Warden**: Debuff Reducer +0.01 (+0.08), Return Fire +0.01 (+0.09), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.05 (+0.13), Counterspell -0.02 (+0.04), Debuff Reducer -0.04 (+0.03)
- **Lash**: Spirit Resilience +0.31 (+0.43), Spellbreaker +0.28 (+0.44), Witchmail +0.24 (+0.43)
- **Viscous**: Counterspell +0.03 (+0.10), Return Fire +0.03 (+0.11), Divine Barrier +0.01 (+0.14)
- **Pocket**: Dispel Magic +0.14 (+0.21), Spirit Resilience +0.13 (+0.25), Bullet Resilience +0.12 (+0.21)
- **Mirage**: Dispel Magic +0.32 (+0.39), Spellbreaker +0.07 (+0.23), Spirit Resilience +0.04 (+0.16)
- **Vyper**: Indomitable +0.31 (+0.45), Spellbreaker +0.11 (+0.27), Debuff Reducer +0.09 (+0.16)
- **Sinclair**: Indomitable +0.19 (+0.33), Spellbreaker +0.06 (+0.22), Debuff Reducer +0.04 (+0.10)
- **Mina**: Return Fire +0.01 (+0.09), Spirit Resilience +0.00 (+0.12), Counterspell -0.01 (+0.06)
- **Drifter**: Counterspell -0.01 (+0.06), Healbane -0.01 (+0.07), Return Fire -0.01 (+0.07)
- **Venator**: Bullet Resilience +0.16 (+0.25), Debuff Reducer +0.05 (+0.12), Unstoppable +0.04 (+0.17)
- **Victor**: Healbane -0.00 (+0.08), Spirit Resilience -0.00 (+0.11), Spellbreaker -0.02 (+0.13)
- **Paige**: Counterspell -0.01 (+0.06), Return Fire -0.01 (+0.07), Healbane -0.02 (+0.06)
- **The Doorman**: Spirit Resilience +0.20 (+0.31), Indomitable +0.18 (+0.33), Witchmail +0.15 (+0.33)
- **Billy**: Healbane +0.05 (+0.13), Spirit Resilience +0.05 (+0.16), Spellbreaker +0.05 (+0.20)
- **Graves**: Witchmail +0.19 (+0.38), Reactive Barrier +0.18 (+0.24), Metal Skin +0.18 (+0.28)
- **Apollo**: Reactive Barrier -0.00 (+0.05), Unstoppable -0.01 (+0.11), Indomitable -0.01 (+0.13)
- **Deadman Danny**: Spellbreaker +0.26 (+0.41), Indomitable +0.25 (+0.39), Plated Armor +0.23 (+0.35)
- **Rem**: Healbane -0.02 (+0.06), Debuff Reducer -0.02 (+0.04), Counterspell -0.02 (+0.04)
- **Silver**: Dispel Magic +0.06 (+0.14), Debuff Reducer -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **Celeste**: Spirit Resilience +0.08 (+0.19), Witchmail +0.07 (+0.26), Healbane +0.01 (+0.09)
- **Rat King**: Return Fire +0.01 (+0.09), Bullet Resilience +0.00 (+0.09), Metal Skin -0.01 (+0.09)
- **Solomon**: Counterspell -0.02 (+0.05), Healbane -0.03 (+0.05), Return Fire -0.03 (+0.05)
- **Violet**: Return Fire -0.00 (+0.08), Witchmail -0.01 (+0.18), Healbane -0.02 (+0.06)
- **Nurse Harrow**: Healbane -0.00 (+0.08), Return Fire -0.03 (+0.05), Counterspell -0.04 (+0.03)
- **Baba**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Debuff Reducer -0.03 (+0.04)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.189 | +0.059 | +0.106 | Lash +0.31, Deadman Danny +0.19, Graves +0.19 | 10 heroes |
| Divine Barrier | 6,400 | +0.245 | +0.039 | +0.091 | Lash +0.14, Graves +0.14, Viscous +0.08 | 0 heroes |
| Dispel Magic | 3,200 | +0.104 | +0.033 | +0.057 | Mirage +0.24, Lash +0.16, Graves +0.12 | 6 heroes |
| Indomitable | 6,400 | +0.175 | +0.028 | +0.114 | Vyper +0.35, Deadman Danny +0.19, Wraith +0.18 | 0 heroes |
| Witchmail | 6,400 | +0.150 | +0.024 | +0.153 | Graves +0.22, Deadman Danny +0.14, Lash +0.10 | 0 heroes |
| Spellbreaker | 6,400 | +0.121 | +0.019 | +0.130 | Lash +0.30, Holliday +0.15, Vyper +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | +0.023 | +0.015 | +0.038 | Graves +0.15, Deadman Danny +0.11, Grey Talon +0.07 | 4 heroes |
| Debuff Reducer | 1,600 | +0.009 | +0.006 | +0.058 | Holliday +0.12, Vyper +0.11, Wraith +0.09 | 0 heroes |
| Plated Armor | 6,400 | -0.044 | -0.007 | +0.086 | Holliday +0.19, Graves +0.15, Wraith +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | -0.038 | -0.012 | +0.060 | Venator +0.17, Shiv +0.08, Paradox +0.06 | 0 heroes |
| Unstoppable | 6,400 | -0.088 | -0.014 | +0.101 | Ivy +0.15, Abrams +0.15, Holliday +0.11 | 0 heroes |
| Counterspell | 3,200 | -0.048 | -0.015 | +0.043 | Graves +0.05, Viscous +0.04, Billy +0.03 | 1 heroes |
| Healbane | 1,600 | -0.062 | -0.039 | +0.063 | Yamato +0.05, Graves +0.04, Abrams +0.03 | 25 heroes |
| Metal Skin | 3,200 | -0.196 | -0.061 | +0.074 | Graves +0.18, Wraith +0.15, Venator +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.192 | -0.120 | +0.060 | Paradox +0.07, Wraith +0.07, Graves +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.08 (+0.21), Dispel Magic +0.07 (+0.13), Unstoppable +0.06 (+0.16)
- **Seven**: Witchmail +0.03 (+0.19), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03)
- **Vindicta**: Divine Barrier +0.04 (+0.14), Return Fire +0.03 (+0.09), Witchmail +0.03 (+0.18)
- **Lady Geist**: Return Fire +0.05 (+0.11), Bullet Resilience +0.01 (+0.07), Counterspell -0.00 (+0.04)
- **Abrams**: Unstoppable +0.15 (+0.25), Indomitable +0.14 (+0.25), Dispel Magic +0.10 (+0.15)
- **Wraith**: Indomitable +0.18 (+0.30), Metal Skin +0.15 (+0.22), Plated Armor +0.09 (+0.18)
- **McGinnis**: Spirit Resilience +0.01 (+0.12), Healbane -0.00 (+0.06), Counterspell -0.02 (+0.02)
- **Paradox**: Return Fire +0.07 (+0.13), Bullet Resilience +0.06 (+0.12), Divine Barrier +0.06 (+0.15)
- **Dynamo**: Healbane +0.00 (+0.07), Counterspell -0.02 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience -0.00 (+0.11), Healbane -0.01 (+0.05), Dispel Magic -0.02 (+0.04)
- **Haze**: Indomitable +0.08 (+0.19), Unstoppable +0.06 (+0.16), Plated Armor +0.05 (+0.13)
- **Holliday**: Plated Armor +0.19 (+0.28), Spellbreaker +0.15 (+0.28), Debuff Reducer +0.12 (+0.18)
- **Bebop**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Divine Barrier -0.02 (+0.07)
- **Calico**: Reactive Barrier +0.05 (+0.09), Divine Barrier +0.03 (+0.12), Spirit Resilience +0.02 (+0.12)
- **Grey Talon**: Unstoppable +0.10 (+0.20), Spellbreaker +0.09 (+0.22), Witchmail +0.08 (+0.23)
- **Mo & Krill**: Spellbreaker +0.09 (+0.23), Unstoppable +0.09 (+0.19), Dispel Magic +0.03 (+0.09)
- **Shiv**: Bullet Resilience +0.08 (+0.14), Plated Armor +0.05 (+0.13), Metal Skin +0.04 (+0.12)
- **Ivy**: Unstoppable +0.15 (+0.25), Indomitable +0.14 (+0.25), Debuff Reducer +0.03 (+0.09)
- **Warden**: Return Fire +0.04 (+0.10), Divine Barrier +0.02 (+0.11), Witchmail +0.02 (+0.17)
- **Yamato**: Healbane +0.05 (+0.11), Debuff Reducer +0.02 (+0.08), Counterspell +0.00 (+0.04)
- **Lash**: Spirit Resilience +0.31 (+0.41), Spellbreaker +0.30 (+0.43), Dispel Magic +0.16 (+0.22)
- **Viscous**: Divine Barrier +0.08 (+0.17), Spirit Resilience +0.05 (+0.16), Debuff Reducer +0.04 (+0.10)
- **Pocket**: Spirit Resilience +0.18 (+0.28), Spellbreaker +0.06 (+0.19), Witchmail +0.05 (+0.20)
- **Mirage**: Dispel Magic +0.24 (+0.29), Spirit Resilience +0.04 (+0.15), Spellbreaker +0.03 (+0.16)
- **Vyper**: Indomitable +0.35 (+0.46), Debuff Reducer +0.11 (+0.17), Spellbreaker +0.11 (+0.24)
- **Sinclair**: Indomitable +0.05 (+0.17), Return Fire -0.01 (+0.05), Debuff Reducer -0.01 (+0.05)
- **Mina**: Witchmail +0.00 (+0.16), Counterspell +0.00 (+0.04), Return Fire -0.00 (+0.06)
- **Drifter**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.04), Reactive Barrier -0.02 (+0.02)
- **Venator**: Bullet Resilience +0.17 (+0.23), Metal Skin +0.12 (+0.20), Plated Armor +0.07 (+0.16)
- **Victor**: Spellbreaker +0.08 (+0.21), Spirit Resilience +0.07 (+0.17), Healbane +0.01 (+0.08)
- **Paige**: Counterspell -0.01 (+0.04), Return Fire -0.02 (+0.04), Healbane -0.02 (+0.04)
- **The Doorman**: Indomitable +0.09 (+0.20), Divine Barrier +0.07 (+0.16), Reactive Barrier +0.06 (+0.10)
- **Billy**: Counterspell +0.03 (+0.08), Spirit Resilience +0.02 (+0.13), Dispel Magic +0.01 (+0.07)
- **Graves**: Witchmail +0.22 (+0.37), Spirit Resilience +0.19 (+0.29), Metal Skin +0.18 (+0.25)
- **Apollo**: Reactive Barrier +0.03 (+0.07), Counterspell -0.01 (+0.03), Indomitable -0.01 (+0.10)
- **Deadman Danny**: Indomitable +0.19 (+0.31), Spirit Resilience +0.19 (+0.29), Witchmail +0.14 (+0.29)
- **Rem**: Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.02), Healbane -0.03 (+0.04)
- **Silver**: Dispel Magic +0.04 (+0.10), Debuff Reducer +0.02 (+0.08), Indomitable +0.01 (+0.12)
- **Celeste**: Witchmail +0.09 (+0.24), Spirit Resilience +0.08 (+0.19), Dispel Magic +0.03 (+0.08)
- **Rat King**: Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.03), Bullet Resilience -0.01 (+0.05)
- **Solomon**: Return Fire -0.02 (+0.04), Counterspell -0.02 (+0.02), Healbane -0.03 (+0.04)
- **Violet**: Healbane +0.01 (+0.07), Return Fire +0.01 (+0.07), Counterspell -0.00 (+0.04)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Counterspell -0.03 (+0.02), Reactive Barrier -0.03 (+0.01)
- **Baba**: Unstoppable +0.06 (+0.16), Debuff Reducer +0.01 (+0.07), Healbane -0.01 (+0.05)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.197 | +0.061 | +0.136 | Lash +0.35, Deadman Danny +0.21, The Doorman +0.14 | 14 heroes |
| Divine Barrier | 6,400 | +0.230 | +0.036 | +0.096 | Lash +0.13, Viscous +0.11, Nurse Harrow +0.08 | 2 heroes |
| Dispel Magic | 3,200 | +0.106 | +0.033 | +0.053 | Mirage +0.22, Lash +0.18, Infernus +0.12 | 11 heroes |
| Indomitable | 6,400 | +0.179 | +0.029 | +0.122 | Wraith +0.25, Vyper +0.25, Deadman Danny +0.19 | 0 heroes |
| Witchmail | 6,400 | +0.143 | +0.022 | +0.164 | Deadman Danny +0.17, Lash +0.15, Celeste +0.13 | 1 heroes |
| Spellbreaker | 6,400 | +0.141 | +0.022 | +0.154 | Lash +0.36, Grey Talon +0.20, Holliday +0.19 | 0 heroes |
| Debuff Reducer | 1,600 | +0.010 | +0.006 | +0.063 | Grey Talon +0.18, Holliday +0.18, Rem +0.09 | 0 heroes |
| Reactive Barrier | 1,600 | -0.006 | -0.004 | +0.034 | Deadman Danny +0.11, Wraith +0.10, Graves +0.09 | 3 heroes |
| Plated Armor | 6,400 | -0.038 | -0.006 | +0.099 | Holliday +0.20, Wraith +0.12, Deadman Danny +0.09 | 0 heroes |
| Unstoppable | 6,400 | -0.080 | -0.013 | +0.113 | Mo & Krill +0.23, Grey Talon +0.19, Holliday +0.14 | 3 heroes |
| Bullet Resilience | 3,200 | -0.046 | -0.014 | +0.064 | Venator +0.16, Vindicta +0.11, Shiv +0.08 | 1 heroes |
| Counterspell | 3,200 | -0.053 | -0.017 | +0.037 | Nurse Harrow +0.05, Deadman Danny +0.05, The Doorman +0.03 | 1 heroes |
| Healbane | 1,600 | -0.064 | -0.040 | +0.059 | Nurse Harrow +0.08, Mo & Krill +0.07, Infernus +0.04 | 23 heroes |
| Metal Skin | 3,200 | -0.188 | -0.059 | +0.086 | Wraith +0.18, Lash +0.12, Shiv +0.08 | 0 heroes |
| Return Fire | 1,600 | -0.187 | -0.117 | +0.052 | Venator +0.06, Vindicta +0.06, Paradox +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.17), Spellbreaker +0.11 (+0.26), Unstoppable +0.05 (+0.16)
- **Seven**: Witchmail +0.02 (+0.19), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03)
- **Vindicta**: Bullet Resilience +0.11 (+0.18), Divine Barrier +0.07 (+0.17), Plated Armor +0.07 (+0.17)
- **Lady Geist**: Return Fire +0.04 (+0.09), Healbane +0.04 (+0.10), Counterspell +0.02 (+0.06)
- **Abrams**: Unstoppable +0.09 (+0.20), Dispel Magic +0.03 (+0.08), Healbane +0.01 (+0.07)
- **Wraith**: Indomitable +0.25 (+0.37), Metal Skin +0.18 (+0.26), Spellbreaker +0.15 (+0.30)
- **McGinnis**: Spirit Resilience +0.09 (+0.23), Healbane +0.02 (+0.08), Witchmail +0.01 (+0.17)
- **Paradox**: Dispel Magic +0.09 (+0.15), Spirit Resilience +0.08 (+0.22), Divine Barrier +0.08 (+0.17)
- **Dynamo**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.04 (-0.01)
- **Kelvin**: Spirit Resilience +0.10 (+0.24), Dispel Magic +0.08 (+0.13), Witchmail +0.04 (+0.20)
- **Haze**: Indomitable +0.08 (+0.20), Plated Armor +0.06 (+0.16), Unstoppable +0.06 (+0.17)
- **Holliday**: Plated Armor +0.20 (+0.30), Spellbreaker +0.19 (+0.34), Debuff Reducer +0.18 (+0.24)
- **Bebop**: Healbane +0.01 (+0.07), Metal Skin -0.02 (+0.07), Counterspell -0.02 (+0.02)
- **Calico**: Spirit Resilience +0.09 (+0.22), Reactive Barrier +0.07 (+0.10), Indomitable +0.07 (+0.19)
- **Grey Talon**: Spellbreaker +0.20 (+0.35), Unstoppable +0.19 (+0.30), Debuff Reducer +0.18 (+0.25)
- **Mo & Krill**: Unstoppable +0.23 (+0.34), Spellbreaker +0.14 (+0.29), Spirit Resilience +0.09 (+0.23)
- **Shiv**: Bullet Resilience +0.08 (+0.14), Metal Skin +0.08 (+0.16), Plated Armor +0.05 (+0.14)
- **Ivy**: Unstoppable +0.09 (+0.20), Indomitable +0.04 (+0.16), Debuff Reducer +0.03 (+0.09)
- **Warden**: Debuff Reducer +0.03 (+0.09), Return Fire +0.02 (+0.07), Healbane +0.01 (+0.07)
- **Yamato**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Debuff Reducer -0.01 (+0.05)
- **Lash**: Spellbreaker +0.36 (+0.51), Spirit Resilience +0.35 (+0.49), Dispel Magic +0.18 (+0.23)
- **Viscous**: Spirit Resilience +0.14 (+0.27), Divine Barrier +0.11 (+0.20), Spellbreaker +0.07 (+0.23)
- **Pocket**: Spirit Resilience +0.12 (+0.26), Witchmail +0.01 (+0.18), Spellbreaker +0.00 (+0.16)
- **Mirage**: Dispel Magic +0.22 (+0.28), Debuff Reducer +0.01 (+0.07), Healbane -0.00 (+0.06)
- **Vyper**: Indomitable +0.25 (+0.37), Debuff Reducer +0.06 (+0.12), Bullet Resilience +0.04 (+0.11)
- **Sinclair**: Indomitable +0.13 (+0.25), Debuff Reducer +0.02 (+0.08), Spellbreaker +0.02 (+0.17)
- **Mina**: Divine Barrier +0.04 (+0.14), Spirit Resilience +0.01 (+0.15), Counterspell +0.01 (+0.04)
- **Drifter**: Witchmail +0.07 (+0.24), Spirit Resilience +0.04 (+0.18), Healbane +0.03 (+0.09)
- **Venator**: Bullet Resilience +0.16 (+0.22), Metal Skin +0.07 (+0.16), Return Fire +0.06 (+0.12)
- **Victor**: Spirit Resilience +0.01 (+0.14), Dispel Magic -0.01 (+0.04), Counterspell -0.02 (+0.02)
- **Paige**: Counterspell -0.00 (+0.03), Healbane -0.02 (+0.04), Return Fire -0.02 (+0.03)
- **The Doorman**: Indomitable +0.18 (+0.30), Spirit Resilience +0.14 (+0.28), Witchmail +0.11 (+0.27)
- **Billy**: Reactive Barrier +0.03 (+0.06), Indomitable +0.02 (+0.14), Counterspell -0.00 (+0.03)
- **Graves**: Spirit Resilience +0.10 (+0.24), Witchmail +0.09 (+0.25), Reactive Barrier +0.09 (+0.12)
- **Apollo**: Healbane +0.00 (+0.06), Reactive Barrier +0.00 (+0.03), Counterspell -0.01 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.21 (+0.34), Indomitable +0.19 (+0.31), Witchmail +0.17 (+0.34)
- **Rem**: Debuff Reducer +0.09 (+0.16), Unstoppable +0.06 (+0.18), Spellbreaker +0.02 (+0.17)
- **Silver**: Dispel Magic +0.07 (+0.12), Indomitable +0.06 (+0.18), Reactive Barrier +0.04 (+0.08)
- **Celeste**: Witchmail +0.13 (+0.29), Spirit Resilience +0.09 (+0.22), Dispel Magic +0.02 (+0.07)
- **Rat King**: Return Fire -0.00 (+0.05), Bullet Resilience -0.01 (+0.06), Healbane -0.01 (+0.04)
- **Solomon**: Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Violet**: Healbane +0.03 (+0.09), Witchmail +0.03 (+0.20), Unstoppable +0.02 (+0.13)
- **Nurse Harrow**: Divine Barrier +0.08 (+0.18), Healbane +0.08 (+0.14), Counterspell +0.05 (+0.09)
- **Baba**: Unstoppable -0.00 (+0.11), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.194 | +0.061 | +0.151 | Lash +0.48, The Doorman +0.44, Grey Talon +0.29 | 16 heroes |
| Dispel Magic | 3,200 | +0.115 | +0.036 | +0.056 | Mirage +0.29, Drifter +0.17, Lash +0.14 | 11 heroes |
| Indomitable | 6,400 | +0.204 | +0.032 | +0.157 | Wraith +0.38, Vyper +0.25, The Doorman +0.19 | 2 heroes |
| Divine Barrier | 6,400 | +0.179 | +0.028 | +0.086 | Lash +0.24, Viscous +0.20, The Doorman +0.16 | 3 heroes |
| Spellbreaker | 6,400 | +0.168 | +0.026 | +0.192 | Grey Talon +0.32, Lash +0.32, Holliday +0.23 | 0 heroes |
| Witchmail | 6,400 | +0.146 | +0.023 | +0.168 | The Doorman +0.31, Lash +0.27, Deadman Danny +0.20 | 2 heroes |
| Debuff Reducer | 1,600 | +0.013 | +0.008 | +0.088 | Holliday +0.26, Grey Talon +0.22, Paige +0.18 | 0 heroes |
| Plated Armor | 6,400 | -0.054 | -0.009 | +0.084 | Vindicta +0.13, Vyper +0.12, Wraith +0.09 | 3 heroes |
| Unstoppable | 6,400 | -0.065 | -0.010 | +0.152 | Paige +0.26, Grey Talon +0.25, Holliday +0.23 | 7 heroes |
| Reactive Barrier | 1,600 | -0.021 | -0.013 | +0.034 | The Doorman +0.12, Paradox +0.07, Deadman Danny +0.07 | 2 heroes |
| Bullet Resilience | 3,200 | -0.052 | -0.016 | +0.057 | Vindicta +0.15, Lash +0.09, Venator +0.08 | 1 heroes |
| Counterspell | 3,200 | -0.061 | -0.019 | +0.029 | Viscous +0.06, Rem +0.05, Paradox +0.04 | 1 heroes |
| Healbane | 1,600 | -0.069 | -0.043 | +0.054 | Rem +0.07, Yamato +0.07, Victor +0.06 | 21 heroes |
| Metal Skin | 3,200 | -0.181 | -0.057 | +0.093 | Wraith +0.24, Lash +0.19, Venator +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.181 | -0.113 | +0.051 | Vindicta +0.10, Paradox +0.09, Viscous +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.14 (+0.33), Unstoppable +0.12 (+0.28), Dispel Magic +0.11 (+0.16)
- **Seven**: Witchmail +0.00 (+0.17), Healbane -0.00 (+0.05), Counterspell -0.00 (+0.02)
- **Vindicta**: Bullet Resilience +0.15 (+0.21), Plated Armor +0.13 (+0.22), Return Fire +0.10 (+0.15)
- **Lady Geist**: Spirit Resilience +0.08 (+0.23), Healbane +0.06 (+0.11), Witchmail +0.03 (+0.20)
- **Abrams**: Dispel Magic +0.04 (+0.10), Debuff Reducer +0.02 (+0.10), Reactive Barrier +0.01 (+0.05)
- **Wraith**: Indomitable +0.38 (+0.53), Metal Skin +0.24 (+0.34), Spellbreaker +0.21 (+0.40)
- **McGinnis**: Spirit Resilience +0.05 (+0.20), Witchmail +0.01 (+0.17), Counterspell -0.00 (+0.03)
- **Paradox**: Unstoppable +0.18 (+0.34), Witchmail +0.14 (+0.31), Dispel Magic +0.12 (+0.18)
- **Dynamo**: Counterspell -0.01 (+0.02), Healbane -0.01 (+0.04), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.26 (+0.41), Spellbreaker +0.05 (+0.25), Witchmail +0.05 (+0.22)
- **Haze**: Unstoppable +0.20 (+0.35), Return Fire +0.06 (+0.11), Indomitable +0.05 (+0.21)
- **Holliday**: Debuff Reducer +0.26 (+0.34), Unstoppable +0.23 (+0.38), Spellbreaker +0.23 (+0.42)
- **Bebop**: Debuff Reducer +0.16 (+0.25), Unstoppable +0.13 (+0.28), Spellbreaker +0.09 (+0.28)
- **Calico**: Reactive Barrier +0.03 (+0.07), Dispel Magic +0.01 (+0.07), Divine Barrier +0.01 (+0.09)
- **Grey Talon**: Spellbreaker +0.32 (+0.51), Spirit Resilience +0.29 (+0.44), Unstoppable +0.25 (+0.40)
- **Mo & Krill**: Healbane +0.05 (+0.10), Dispel Magic +0.04 (+0.10), Debuff Reducer +0.02 (+0.11)
- **Shiv**: Bullet Resilience +0.07 (+0.12), Metal Skin +0.06 (+0.15), Plated Armor +0.05 (+0.13)
- **Ivy**: Unstoppable +0.07 (+0.23), Indomitable +0.04 (+0.19), Dispel Magic +0.01 (+0.06)
- **Warden**: Healbane +0.01 (+0.07), Plated Armor +0.01 (+0.09), Divine Barrier +0.00 (+0.09)
- **Yamato**: Healbane +0.07 (+0.12), Counterspell +0.00 (+0.03), Witchmail +0.00 (+0.17)
- **Lash**: Spirit Resilience +0.48 (+0.63), Spellbreaker +0.32 (+0.51), Witchmail +0.27 (+0.44)
- **Viscous**: Spirit Resilience +0.27 (+0.42), Divine Barrier +0.20 (+0.29), Witchmail +0.15 (+0.32)
- **Pocket**: Spirit Resilience +0.14 (+0.29), Witchmail -0.00 (+0.17), Return Fire -0.01 (+0.04)
- **Mirage**: Dispel Magic +0.29 (+0.34), Unstoppable +0.10 (+0.25), Metal Skin +0.07 (+0.16)
- **Vyper**: Indomitable +0.25 (+0.41), Plated Armor +0.12 (+0.20), Bullet Resilience +0.04 (+0.10)
- **Sinclair**: Indomitable +0.15 (+0.31), Spellbreaker +0.03 (+0.22), Return Fire +0.01 (+0.06)
- **Mina**: Counterspell +0.01 (+0.04), Divine Barrier +0.01 (+0.10), Spirit Resilience -0.01 (+0.14)
- **Drifter**: Dispel Magic +0.17 (+0.23), Unstoppable +0.08 (+0.23), Debuff Reducer +0.04 (+0.13)
- **Venator**: Metal Skin +0.12 (+0.21), Bullet Resilience +0.08 (+0.14), Plated Armor +0.03 (+0.11)
- **Victor**: Spirit Resilience +0.08 (+0.23), Healbane +0.06 (+0.12), Spellbreaker +0.05 (+0.24)
- **Paige**: Unstoppable +0.26 (+0.41), Debuff Reducer +0.18 (+0.27), Spellbreaker +0.08 (+0.27)
- **The Doorman**: Spirit Resilience +0.44 (+0.59), Witchmail +0.31 (+0.48), Indomitable +0.19 (+0.35)
- **Billy**: Reactive Barrier +0.05 (+0.08), Counterspell +0.02 (+0.05), Dispel Magic +0.01 (+0.06)
- **Graves**: Return Fire +0.03 (+0.08), Reactive Barrier +0.01 (+0.05), Metal Skin +0.01 (+0.10)
- **Apollo**: Healbane +0.01 (+0.06), Reactive Barrier +0.00 (+0.04), Counterspell -0.00 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.28 (+0.43), Witchmail +0.20 (+0.37), Spellbreaker +0.19 (+0.39)
- **Rem**: Divine Barrier +0.08 (+0.17), Healbane +0.07 (+0.13), Spirit Resilience +0.06 (+0.21)
- **Silver**: Dispel Magic +0.09 (+0.15), Bullet Resilience +0.04 (+0.10), Metal Skin +0.04 (+0.13)
- **Celeste**: Witchmail +0.09 (+0.25), Healbane +0.04 (+0.09), Plated Armor -0.01 (+0.08)
- **Rat King**: Healbane +0.01 (+0.06), Counterspell -0.01 (+0.02), Debuff Reducer -0.01 (+0.07)
- **Solomon**: Return Fire +0.00 (+0.05), Counterspell +0.00 (+0.03), Reactive Barrier -0.01 (+0.02)
- **Violet**: Witchmail +0.03 (+0.20), Return Fire +0.01 (+0.06), Divine Barrier +0.01 (+0.09)
- **Nurse Harrow**: Spirit Resilience +0.10 (+0.25), Divine Barrier +0.08 (+0.16), Bullet Resilience +0.06 (+0.11)
- **Baba**: Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05), Reactive Barrier -0.02 (+0.01)
