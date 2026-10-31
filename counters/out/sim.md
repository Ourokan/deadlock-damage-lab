# Counter items in the sim (phantom and up)

Built 2026-10-31T03:14:11Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.378 | +0.060 | +0.127 | Lash +0.22, Graves +0.15, Pocket +0.14 | 0 heroes |
| Spirit Resilience | 3,200 | +0.191 | +0.060 | +0.121 | Deadman Danny +0.27, Lash +0.27, Pocket +0.22 | 1 heroes |
| Dispel Magic | 3,200 | +0.097 | +0.030 | +0.077 | Mirage +0.31, Pocket +0.19, Deadman Danny +0.14 | 3 heroes |
| Reactive Barrier | 1,600 | +0.042 | +0.027 | +0.056 | Deadman Danny +0.18, Graves +0.13, The Doorman +0.11 | 3 heroes |
| Indomitable | 6,400 | +0.160 | +0.026 | +0.144 | Deadman Danny +0.32, Vyper +0.26, Abrams +0.23 | 0 heroes |
| Witchmail | 6,400 | +0.158 | +0.025 | +0.202 | Deadman Danny +0.29, Lash +0.21, Pocket +0.21 | 0 heroes |
| Debuff Reducer | 1,600 | +0.030 | +0.018 | +0.070 | Deadman Danny +0.12, Wraith +0.10, Holliday +0.10 | 0 heroes |
| Spellbreaker | 6,400 | +0.089 | +0.014 | +0.157 | Deadman Danny +0.33, Lash +0.24, Pocket +0.20 | 0 heroes |
| Bullet Resilience | 3,200 | -0.005 | -0.002 | +0.095 | Deadman Danny +0.25, Pocket +0.18, Venator +0.17 | 0 heroes |
| Plated Armor | 6,400 | -0.043 | -0.007 | +0.120 | Deadman Danny +0.28, Holliday +0.22, Pocket +0.18 | 0 heroes |
| Counterspell | 3,200 | -0.025 | -0.008 | +0.074 | Deadman Danny +0.14, Pocket +0.11, Wraith +0.05 | 1 heroes |
| Unstoppable | 6,400 | -0.061 | -0.010 | +0.131 | Deadman Danny +0.25, Pocket +0.15, Ivy +0.13 | 0 heroes |
| Healbane | 1,600 | -0.023 | -0.015 | +0.077 | Yamato +0.05, Celeste +0.05, Bebop +0.04 | 12 heroes |
| Metal Skin | 3,200 | -0.165 | -0.052 | +0.095 | Lash +0.19, Wraith +0.17, Graves +0.17 | 0 heroes |
| Return Fire | 1,600 | -0.176 | -0.110 | +0.081 | Deadman Danny +0.13, Wraith +0.07, The Doorman +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.07 (+0.15), Spellbreaker +0.05 (+0.20), Spirit Resilience +0.03 (+0.15)
- **Seven**: Counterspell -0.03 (+0.05), Reactive Barrier -0.03 (+0.02), Healbane -0.04 (+0.04)
- **Vindicta**: Return Fire +0.01 (+0.09), Divine Barrier -0.00 (+0.12), Counterspell -0.01 (+0.06)
- **Lady Geist**: Return Fire +0.04 (+0.12), Counterspell +0.00 (+0.08), Healbane -0.00 (+0.07)
- **Abrams**: Indomitable +0.23 (+0.37), Unstoppable +0.09 (+0.22), Spirit Resilience +0.08 (+0.20)
- **Wraith**: Indomitable +0.18 (+0.33), Metal Skin +0.17 (+0.26), Spellbreaker +0.12 (+0.28)
- **McGinnis**: Spirit Resilience +0.03 (+0.15), Counterspell +0.03 (+0.10), Dispel Magic +0.03 (+0.11)
- **Paradox**: Bullet Resilience +0.06 (+0.15), Return Fire +0.06 (+0.14), Divine Barrier +0.04 (+0.17)
- **Dynamo**: Healbane -0.02 (+0.06), Counterspell -0.04 (+0.04), Reactive Barrier -0.05 (+0.01)
- **Kelvin**: Counterspell -0.02 (+0.06), Reactive Barrier -0.03 (+0.02), Dispel Magic -0.03 (+0.04)
- **Haze**: Indomitable +0.09 (+0.23), Unstoppable +0.06 (+0.19), Plated Armor +0.03 (+0.15)
- **Holliday**: Plated Armor +0.22 (+0.34), Spellbreaker +0.11 (+0.27), Debuff Reducer +0.10 (+0.17)
- **Bebop**: Healbane +0.04 (+0.12), Counterspell +0.01 (+0.09), Divine Barrier +0.00 (+0.13)
- **Calico**: Spellbreaker +0.05 (+0.20), Divine Barrier +0.02 (+0.15), Spirit Resilience -0.00 (+0.12)
- **Grey Talon**: Unstoppable +0.05 (+0.18), Debuff Reducer +0.04 (+0.11), Spellbreaker +0.03 (+0.19)
- **Mo & Krill**: Spellbreaker +0.05 (+0.21), Spirit Resilience +0.02 (+0.14), Healbane +0.02 (+0.10)
- **Shiv**: Healbane -0.01 (+0.06), Return Fire -0.02 (+0.06), Metal Skin -0.03 (+0.07)
- **Ivy**: Indomitable +0.15 (+0.30), Unstoppable +0.13 (+0.26), Debuff Reducer +0.01 (+0.08)
- **Warden**: Return Fire -0.01 (+0.08), Debuff Reducer -0.01 (+0.06), Healbane -0.01 (+0.07)
- **Yamato**: Healbane +0.05 (+0.13), Counterspell -0.04 (+0.03), Reactive Barrier -0.05 (+0.01)
- **Lash**: Spirit Resilience +0.27 (+0.39), Spellbreaker +0.24 (+0.40), Divine Barrier +0.22 (+0.35)
- **Viscous**: Return Fire +0.00 (+0.09), Counterspell -0.00 (+0.07), Divine Barrier -0.01 (+0.12)
- **Pocket**: Spirit Resilience +0.22 (+0.34), Witchmail +0.21 (+0.41), Spellbreaker +0.20 (+0.36)
- **Mirage**: Dispel Magic +0.31 (+0.39), Spellbreaker +0.06 (+0.22), Spirit Resilience +0.05 (+0.17)
- **Vyper**: Indomitable +0.26 (+0.41), Debuff Reducer +0.09 (+0.16), Unstoppable +0.09 (+0.22)
- **Sinclair**: Indomitable +0.16 (+0.31), Spellbreaker +0.08 (+0.24), Debuff Reducer -0.01 (+0.06)
- **Mina**: Return Fire +0.01 (+0.09), Divine Barrier +0.00 (+0.13), Spirit Resilience +0.00 (+0.12)
- **Drifter**: Return Fire +0.02 (+0.10), Counterspell +0.02 (+0.09), Debuff Reducer +0.02 (+0.09)
- **Venator**: Bullet Resilience +0.17 (+0.26), Metal Skin +0.06 (+0.16), Debuff Reducer +0.06 (+0.13)
- **Victor**: Healbane -0.01 (+0.07), Spirit Resilience -0.02 (+0.10), Spellbreaker -0.04 (+0.11)
- **Paige**: Healbane -0.00 (+0.07), Return Fire -0.03 (+0.06), Counterspell -0.03 (+0.05)
- **The Doorman**: Indomitable +0.14 (+0.28), Witchmail +0.13 (+0.33), Spirit Resilience +0.12 (+0.24)
- **Billy**: Spellbreaker +0.05 (+0.21), Spirit Resilience +0.04 (+0.16), Healbane +0.03 (+0.11)
- **Graves**: Metal Skin +0.17 (+0.26), Spirit Resilience +0.15 (+0.27), Divine Barrier +0.15 (+0.27)
- **Apollo**: Reactive Barrier +0.02 (+0.07), Indomitable -0.00 (+0.14), Unstoppable -0.00 (+0.13)
- **Deadman Danny**: Spellbreaker +0.33 (+0.48), Indomitable +0.32 (+0.46), Witchmail +0.29 (+0.49)
- **Rem**: Dispel Magic -0.01 (+0.06), Witchmail -0.01 (+0.19), Debuff Reducer -0.02 (+0.05)
- **Silver**: Dispel Magic +0.09 (+0.16), Reactive Barrier +0.07 (+0.12), Metal Skin +0.06 (+0.15)
- **Celeste**: Spirit Resilience +0.09 (+0.21), Witchmail +0.07 (+0.28), Healbane +0.05 (+0.13)
- **Rat King**: Return Fire +0.01 (+0.09), Counterspell -0.00 (+0.07), Divine Barrier -0.01 (+0.12)
- **Solomon**: Counterspell -0.03 (+0.05), Healbane -0.03 (+0.05), Reactive Barrier -0.04 (+0.02)
- **Violet**: Return Fire -0.01 (+0.07), Healbane -0.02 (+0.06), Witchmail -0.03 (+0.18)
- **Nurse Harrow**: Healbane +0.02 (+0.10), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.03)
- **Baba**: Healbane +0.00 (+0.08), Unstoppable -0.01 (+0.12), Debuff Reducer -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.166 | +0.052 | +0.108 | Graves +0.25, Lash +0.21, Deadman Danny +0.18 | 9 heroes |
| Divine Barrier | 6,400 | +0.258 | +0.041 | +0.097 | Graves +0.17, Lash +0.12, Abrams +0.08 | 0 heroes |
| Dispel Magic | 3,200 | +0.087 | +0.027 | +0.054 | Mirage +0.25, Graves +0.11, Infernus +0.10 | 6 heroes |
| Witchmail | 6,400 | +0.155 | +0.024 | +0.164 | Graves +0.24, Deadman Danny +0.15, Lash +0.12 | 0 heroes |
| Indomitable | 6,400 | +0.141 | +0.023 | +0.116 | Vyper +0.38, Wraith +0.18, Deadman Danny +0.18 | 0 heroes |
| Spellbreaker | 6,400 | +0.106 | +0.017 | +0.132 | Lash +0.18, Graves +0.15, Deadman Danny +0.15 | 0 heroes |
| Reactive Barrier | 1,600 | +0.023 | +0.014 | +0.037 | Graves +0.13, Grey Talon +0.13, Deadman Danny +0.09 | 4 heroes |
| Debuff Reducer | 1,600 | +0.006 | +0.004 | +0.054 | Wraith +0.11, Grey Talon +0.10, Rem +0.10 | 1 heroes |
| Plated Armor | 6,400 | -0.041 | -0.006 | +0.088 | Graves +0.18, Paradox +0.10, Vyper +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | -0.035 | -0.011 | +0.066 | Venator +0.13, Paradox +0.13, Grey Talon +0.07 | 0 heroes |
| Counterspell | 3,200 | -0.038 | -0.012 | +0.047 | Grey Talon +0.09, Graves +0.03, Silver +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.084 | -0.013 | +0.104 | Grey Talon +0.17, Ivy +0.17, Abrams +0.16 | 0 heroes |
| Healbane | 1,600 | -0.051 | -0.032 | +0.063 | Abrams +0.06, Nurse Harrow +0.04, Seven +0.04 | 20 heroes |
| Metal Skin | 3,200 | -0.181 | -0.057 | +0.077 | Graves +0.20, Wraith +0.14, Lash +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.182 | -0.114 | +0.061 | Wraith +0.08, Paradox +0.07, Silver +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.16), Spellbreaker +0.05 (+0.19), Unstoppable +0.03 (+0.13)
- **Seven**: Witchmail +0.08 (+0.25), Healbane +0.04 (+0.10), Spirit Resilience +0.04 (+0.15)
- **Vindicta**: Divine Barrier +0.04 (+0.14), Return Fire +0.03 (+0.09), Bullet Resilience +0.02 (+0.09)
- **Lady Geist**: Return Fire +0.05 (+0.12), Divine Barrier +0.02 (+0.12), Metal Skin +0.02 (+0.09)
- **Abrams**: Unstoppable +0.16 (+0.26), Indomitable +0.11 (+0.23), Divine Barrier +0.08 (+0.18)
- **Wraith**: Indomitable +0.18 (+0.30), Metal Skin +0.14 (+0.22), Debuff Reducer +0.11 (+0.16)
- **McGinnis**: Spirit Resilience +0.05 (+0.15), Dispel Magic -0.01 (+0.05), Counterspell -0.01 (+0.04)
- **Paradox**: Metal Skin +0.13 (+0.21), Bullet Resilience +0.13 (+0.19), Plated Armor +0.10 (+0.19)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.02 (+0.02), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.04 (+0.15), Dispel Magic +0.03 (+0.08), Counterspell +0.03 (+0.07)
- **Haze**: Indomitable +0.07 (+0.18), Plated Armor +0.05 (+0.14), Unstoppable +0.04 (+0.15)
- **Holliday**: Spellbreaker +0.11 (+0.24), Debuff Reducer +0.09 (+0.14), Indomitable +0.08 (+0.20)
- **Bebop**: Divine Barrier +0.02 (+0.12), Healbane +0.02 (+0.09), Counterspell +0.01 (+0.06)
- **Calico**: Reactive Barrier +0.05 (+0.08), Divine Barrier +0.04 (+0.14), Spellbreaker +0.02 (+0.15)
- **Grey Talon**: Unstoppable +0.17 (+0.28), Spellbreaker +0.15 (+0.28), Reactive Barrier +0.13 (+0.17)
- **Mo & Krill**: Spellbreaker +0.10 (+0.23), Unstoppable +0.08 (+0.18), Debuff Reducer +0.04 (+0.09)
- **Shiv**: Bullet Resilience +0.04 (+0.11), Return Fire +0.03 (+0.09), Divine Barrier +0.02 (+0.11)
- **Ivy**: Unstoppable +0.17 (+0.27), Indomitable +0.16 (+0.27), Debuff Reducer +0.03 (+0.08)
- **Warden**: Return Fire +0.02 (+0.08), Witchmail +0.01 (+0.17), Plated Armor +0.00 (+0.09)
- **Yamato**: Spellbreaker +0.08 (+0.21), Unstoppable +0.06 (+0.17), Bullet Resilience +0.04 (+0.11)
- **Lash**: Spirit Resilience +0.21 (+0.32), Spellbreaker +0.18 (+0.31), Metal Skin +0.13 (+0.21)
- **Viscous**: Divine Barrier +0.04 (+0.14), Counterspell +0.02 (+0.06), Metal Skin +0.00 (+0.08)
- **Pocket**: Spirit Resilience +0.17 (+0.28), Spellbreaker +0.09 (+0.22), Witchmail +0.06 (+0.22)
- **Mirage**: Dispel Magic +0.25 (+0.30), Metal Skin +0.05 (+0.13), Spirit Resilience +0.05 (+0.16)
- **Vyper**: Indomitable +0.38 (+0.49), Spellbreaker +0.13 (+0.26), Metal Skin +0.09 (+0.17)
- **Sinclair**: Indomitable +0.08 (+0.19), Spellbreaker +0.02 (+0.15), Reactive Barrier +0.00 (+0.04)
- **Mina**: Divine Barrier +0.06 (+0.16), Spirit Resilience +0.05 (+0.16), Witchmail +0.04 (+0.20)
- **Drifter**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.04), Debuff Reducer -0.02 (+0.04)
- **Venator**: Bullet Resilience +0.13 (+0.20), Metal Skin +0.10 (+0.18), Plated Armor +0.04 (+0.13)
- **Victor**: Spirit Resilience +0.07 (+0.17), Spellbreaker +0.06 (+0.19), Dispel Magic -0.00 (+0.05)
- **Paige**: Counterspell -0.01 (+0.03), Healbane -0.02 (+0.05), Return Fire -0.03 (+0.03)
- **The Doorman**: Indomitable +0.08 (+0.19), Reactive Barrier +0.08 (+0.11), Spirit Resilience +0.07 (+0.17)
- **Billy**: Spirit Resilience +0.01 (+0.12), Dispel Magic +0.00 (+0.06), Plated Armor -0.00 (+0.08)
- **Graves**: Spirit Resilience +0.25 (+0.36), Witchmail +0.24 (+0.41), Metal Skin +0.20 (+0.27)
- **Apollo**: Reactive Barrier +0.01 (+0.05), Indomitable -0.02 (+0.10), Healbane -0.02 (+0.04)
- **Deadman Danny**: Spirit Resilience +0.18 (+0.29), Indomitable +0.18 (+0.30), Witchmail +0.15 (+0.31)
- **Rem**: Debuff Reducer +0.10 (+0.15), Unstoppable +0.07 (+0.18), Spellbreaker +0.06 (+0.19)
- **Silver**: Debuff Reducer +0.08 (+0.13), Dispel Magic +0.08 (+0.13), Return Fire +0.06 (+0.12)
- **Celeste**: Spirit Resilience +0.05 (+0.16), Witchmail +0.05 (+0.21), Plated Armor +0.02 (+0.11)
- **Rat King**: Return Fire -0.01 (+0.05), Counterspell -0.02 (+0.03), Bullet Resilience -0.02 (+0.04)
- **Solomon**: Return Fire -0.01 (+0.05), Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Violet**: Return Fire +0.01 (+0.07), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.04)
- **Nurse Harrow**: Healbane +0.04 (+0.10), Counterspell +0.01 (+0.06), Reactive Barrier -0.01 (+0.02)
- **Baba**: Unstoppable +0.05 (+0.15), Debuff Reducer +0.01 (+0.07), Healbane +0.00 (+0.07)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.157 | +0.049 | +0.117 | Lash +0.31, Pocket +0.19, Kelvin +0.18 | 15 heroes |
| Divine Barrier | 6,400 | +0.231 | +0.036 | +0.082 | Lash +0.17, Vindicta +0.09, The Doorman +0.07 | 2 heroes |
| Dispel Magic | 3,200 | +0.090 | +0.028 | +0.051 | Mirage +0.27, Lash +0.23, Infernus +0.15 | 9 heroes |
| Indomitable | 6,400 | +0.144 | +0.023 | +0.117 | Vyper +0.33, Wraith +0.22, The Doorman +0.19 | 0 heroes |
| Witchmail | 6,400 | +0.144 | +0.022 | +0.157 | Lash +0.16, The Doorman +0.12, Grey Talon +0.11 | 1 heroes |
| Spellbreaker | 6,400 | +0.122 | +0.019 | +0.144 | Lash +0.39, Grey Talon +0.21, Holliday +0.18 | 0 heroes |
| Debuff Reducer | 1,600 | +0.005 | +0.003 | +0.054 | Rem +0.18, Holliday +0.16, Grey Talon +0.15 | 0 heroes |
| Reactive Barrier | 1,600 | -0.001 | -0.001 | +0.035 | Deadman Danny +0.10, Grey Talon +0.09, Yamato +0.09 | 3 heroes |
| Plated Armor | 6,400 | -0.041 | -0.006 | +0.087 | Holliday +0.21, Wraith +0.08, Vindicta +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.086 | -0.013 | +0.094 | Grey Talon +0.20, Rem +0.16, Holliday +0.15 | 4 heroes |
| Counterspell | 3,200 | -0.046 | -0.015 | +0.032 | Vindicta +0.05, Yamato +0.04, Paradox +0.03 | 1 heroes |
| Bullet Resilience | 3,200 | -0.051 | -0.016 | +0.057 | Lady Geist +0.11, Shiv +0.08, Vindicta +0.08 | 1 heroes |
| Healbane | 1,600 | -0.053 | -0.033 | +0.064 | Lady Geist +0.09, Infernus +0.05, Drifter +0.05 | 18 heroes |
| Metal Skin | 3,200 | -0.179 | -0.056 | +0.076 | Lash +0.16, Wraith +0.13, Lady Geist +0.09 | 0 heroes |
| Return Fire | 1,600 | -0.178 | -0.111 | +0.055 | Vindicta +0.09, Wraith +0.07, Lady Geist +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.15 (+0.20), Spellbreaker +0.14 (+0.28), Unstoppable +0.07 (+0.16)
- **Seven**: Witchmail +0.07 (+0.23), Counterspell +0.01 (+0.05), Healbane +0.00 (+0.07)
- **Vindicta**: Return Fire +0.09 (+0.15), Divine Barrier +0.09 (+0.17), Bullet Resilience +0.08 (+0.13)
- **Lady Geist**: Bullet Resilience +0.11 (+0.17), Healbane +0.09 (+0.16), Metal Skin +0.09 (+0.16)
- **Abrams**: Unstoppable +0.07 (+0.16), Healbane +0.05 (+0.11), Dispel Magic +0.04 (+0.09)
- **Wraith**: Indomitable +0.22 (+0.34), Metal Skin +0.13 (+0.20), Spellbreaker +0.12 (+0.27)
- **McGinnis**: Spirit Resilience +0.11 (+0.23), Witchmail +0.05 (+0.21), Spellbreaker +0.05 (+0.19)
- **Paradox**: Spirit Resilience +0.10 (+0.21), Witchmail +0.09 (+0.24), Reactive Barrier +0.08 (+0.11)
- **Dynamo**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02), Debuff Reducer -0.03 (+0.03)
- **Kelvin**: Spirit Resilience +0.18 (+0.30), Witchmail +0.10 (+0.26), Spellbreaker +0.07 (+0.22)
- **Haze**: Indomitable +0.11 (+0.23), Unstoppable +0.08 (+0.18), Bullet Resilience +0.07 (+0.13)
- **Holliday**: Plated Armor +0.21 (+0.30), Spellbreaker +0.18 (+0.33), Debuff Reducer +0.16 (+0.22)
- **Bebop**: Healbane +0.03 (+0.09), Counterspell -0.01 (+0.02), Return Fire -0.02 (+0.04)
- **Calico**: Spirit Resilience +0.05 (+0.17), Reactive Barrier +0.04 (+0.07), Divine Barrier +0.04 (+0.12)
- **Grey Talon**: Spellbreaker +0.21 (+0.35), Unstoppable +0.20 (+0.29), Debuff Reducer +0.15 (+0.21)
- **Mo & Krill**: Spellbreaker +0.08 (+0.23), Debuff Reducer +0.06 (+0.11), Unstoppable +0.06 (+0.15)
- **Shiv**: Bullet Resilience +0.08 (+0.13), Metal Skin +0.07 (+0.14), Plated Armor +0.05 (+0.14)
- **Ivy**: Healbane -0.00 (+0.06), Metal Skin -0.02 (+0.06), Bullet Resilience -0.02 (+0.03)
- **Warden**: Debuff Reducer +0.02 (+0.07), Return Fire -0.00 (+0.05), Divine Barrier -0.00 (+0.08)
- **Yamato**: Indomitable +0.18 (+0.29), Reactive Barrier +0.09 (+0.13), Bullet Resilience +0.07 (+0.12)
- **Lash**: Spellbreaker +0.39 (+0.53), Spirit Resilience +0.31 (+0.42), Dispel Magic +0.23 (+0.28)
- **Viscous**: Spirit Resilience +0.09 (+0.21), Spellbreaker +0.07 (+0.22), Healbane +0.04 (+0.11)
- **Pocket**: Spirit Resilience +0.19 (+0.30), Spellbreaker +0.03 (+0.17), Witchmail +0.03 (+0.18)
- **Mirage**: Dispel Magic +0.27 (+0.32), Metal Skin +0.04 (+0.12), Spirit Resilience +0.03 (+0.15)
- **Vyper**: Indomitable +0.33 (+0.45), Spellbreaker +0.09 (+0.23), Debuff Reducer +0.07 (+0.12)
- **Sinclair**: Indomitable +0.19 (+0.31), Spellbreaker +0.07 (+0.22), Unstoppable +0.02 (+0.12)
- **Mina**: Divine Barrier +0.05 (+0.13), Witchmail +0.03 (+0.19), Spirit Resilience +0.03 (+0.15)
- **Drifter**: Witchmail +0.08 (+0.24), Debuff Reducer +0.06 (+0.11), Spirit Resilience +0.05 (+0.17)
- **Venator**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.07 (+0.15), Plated Armor +0.02 (+0.11)
- **Victor**: Spirit Resilience +0.03 (+0.15), Spellbreaker +0.01 (+0.15), Healbane +0.01 (+0.07)
- **Paige**: Counterspell +0.00 (+0.04), Divine Barrier -0.01 (+0.07), Witchmail -0.01 (+0.15)
- **The Doorman**: Indomitable +0.19 (+0.31), Spirit Resilience +0.18 (+0.29), Witchmail +0.12 (+0.28)
- **Billy**: Reactive Barrier +0.01 (+0.05), Debuff Reducer +0.01 (+0.06), Spirit Resilience +0.01 (+0.12)
- **Graves**: Return Fire +0.03 (+0.08), Metal Skin +0.02 (+0.10), Witchmail +0.01 (+0.17)
- **Apollo**: Healbane +0.01 (+0.07), Reactive Barrier +0.00 (+0.04), Counterspell -0.00 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.17 (+0.29), Spellbreaker +0.13 (+0.27), Indomitable +0.11 (+0.23)
- **Rem**: Debuff Reducer +0.18 (+0.23), Unstoppable +0.16 (+0.26), Spellbreaker +0.09 (+0.24)
- **Silver**: Dispel Magic +0.06 (+0.11), Reactive Barrier +0.03 (+0.06), Divine Barrier +0.00 (+0.08)
- **Celeste**: Witchmail +0.05 (+0.20), Healbane +0.03 (+0.09), Dispel Magic +0.00 (+0.05)
- **Rat King**: Plated Armor -0.01 (+0.08), Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.01 (+0.05), Counterspell -0.00 (+0.03), Return Fire -0.00 (+0.05)
- **Violet**: Witchmail +0.03 (+0.19), Return Fire +0.02 (+0.07), Counterspell +0.01 (+0.04)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Counterspell +0.00 (+0.04), Bullet Resilience -0.02 (+0.04)
- **Baba**: Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05), Debuff Reducer -0.01 (+0.04)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.188 | +0.059 | +0.145 | Lash +0.53, The Doorman +0.47, Viscous +0.28 | 15 heroes |
| Divine Barrier | 6,400 | +0.194 | +0.030 | +0.079 | Viscous +0.26, Lash +0.24, Nurse Harrow +0.14 | 3 heroes |
| Dispel Magic | 3,200 | +0.096 | +0.030 | +0.051 | Mirage +0.28, Lash +0.21, Silver +0.15 | 9 heroes |
| Indomitable | 6,400 | +0.160 | +0.026 | +0.139 | Wraith +0.31, The Doorman +0.29, Sinclair +0.18 | 1 heroes |
| Spellbreaker | 6,400 | +0.152 | +0.024 | +0.188 | Lash +0.33, Grey Talon +0.29, Holliday +0.19 | 0 heroes |
| Witchmail | 6,400 | +0.149 | +0.023 | +0.169 | Lash +0.24, The Doorman +0.19, Viscous +0.16 | 2 heroes |
| Debuff Reducer | 1,600 | +0.007 | +0.004 | +0.078 | Bebop +0.17, Holliday +0.16, Rem +0.14 | 0 heroes |
| Plated Armor | 6,400 | -0.048 | -0.007 | +0.091 | Holliday +0.23, Vindicta +0.10, Vyper +0.10 | 3 heroes |
| Unstoppable | 6,400 | -0.070 | -0.011 | +0.131 | Grey Talon +0.21, Haze +0.20, Infernus +0.17 | 8 heroes |
| Reactive Barrier | 1,600 | -0.019 | -0.012 | +0.025 | Yamato +0.16, Deadman Danny +0.08, Calico +0.07 | 3 heroes |
| Counterspell | 3,200 | -0.050 | -0.016 | +0.029 | Nurse Harrow +0.09, Viscous +0.05, Drifter +0.03 | 1 heroes |
| Bullet Resilience | 3,200 | -0.052 | -0.016 | +0.055 | Lady Geist +0.14, Venator +0.14, Vindicta +0.12 | 0 heroes |
| Healbane | 1,600 | -0.053 | -0.033 | +0.055 | Lady Geist +0.06, Mo & Krill +0.05, Vindicta +0.05 | 14 heroes |
| Metal Skin | 3,200 | -0.172 | -0.054 | +0.091 | Lash +0.19, Wraith +0.18, Silver +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.174 | -0.109 | +0.048 | Vindicta +0.07, Lady Geist +0.06, Viscous +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.17 (+0.30), Spellbreaker +0.16 (+0.35), Dispel Magic +0.14 (+0.19)
- **Seven**: Witchmail +0.09 (+0.26), Spirit Resilience +0.09 (+0.23), Healbane +0.01 (+0.07)
- **Vindicta**: Bullet Resilience +0.12 (+0.18), Divine Barrier +0.11 (+0.19), Plated Armor +0.10 (+0.19)
- **Lady Geist**: Bullet Resilience +0.14 (+0.19), Metal Skin +0.11 (+0.20), Plated Armor +0.08 (+0.17)
- **Abrams**: Debuff Reducer +0.01 (+0.09), Reactive Barrier +0.01 (+0.04), Dispel Magic +0.01 (+0.06)
- **Wraith**: Indomitable +0.31 (+0.45), Spellbreaker +0.18 (+0.37), Metal Skin +0.18 (+0.27)
- **McGinnis**: Spirit Resilience +0.07 (+0.22), Witchmail +0.03 (+0.20), Healbane +0.01 (+0.07)
- **Paradox**: Unstoppable +0.14 (+0.27), Witchmail +0.14 (+0.31), Dispel Magic +0.11 (+0.16)
- **Dynamo**: Counterspell -0.01 (+0.02), Healbane -0.01 (+0.04), Reactive Barrier -0.02 (+0.01)
- **Kelvin**: Spirit Resilience +0.14 (+0.28), Witchmail +0.03 (+0.19), Healbane +0.00 (+0.06)
- **Haze**: Unstoppable +0.20 (+0.33), Return Fire +0.04 (+0.09), Bullet Resilience +0.03 (+0.08)
- **Holliday**: Plated Armor +0.23 (+0.32), Spellbreaker +0.19 (+0.37), Debuff Reducer +0.16 (+0.23)
- **Bebop**: Debuff Reducer +0.17 (+0.24), Spellbreaker +0.10 (+0.29), Unstoppable +0.08 (+0.21)
- **Calico**: Spirit Resilience +0.14 (+0.29), Divine Barrier +0.09 (+0.17), Reactive Barrier +0.07 (+0.09)
- **Grey Talon**: Spellbreaker +0.29 (+0.48), Spirit Resilience +0.27 (+0.42), Unstoppable +0.21 (+0.35)
- **Mo & Krill**: Healbane +0.05 (+0.10), Dispel Magic +0.04 (+0.09), Debuff Reducer +0.02 (+0.10)
- **Shiv**: Bullet Resilience +0.07 (+0.12), Metal Skin +0.05 (+0.14), Plated Armor +0.03 (+0.12)
- **Ivy**: Unstoppable +0.04 (+0.17), Debuff Reducer +0.00 (+0.08), Healbane -0.01 (+0.05)
- **Warden**: Divine Barrier +0.01 (+0.09), Bullet Resilience +0.00 (+0.06), Healbane -0.00 (+0.05)
- **Yamato**: Reactive Barrier +0.16 (+0.19), Indomitable +0.14 (+0.28), Bullet Resilience +0.10 (+0.15)
- **Lash**: Spirit Resilience +0.53 (+0.67), Spellbreaker +0.33 (+0.52), Witchmail +0.24 (+0.41)
- **Viscous**: Spirit Resilience +0.28 (+0.42), Divine Barrier +0.26 (+0.33), Witchmail +0.16 (+0.33)
- **Pocket**: Spirit Resilience +0.11 (+0.25), Return Fire -0.01 (+0.04), Witchmail -0.01 (+0.16)
- **Mirage**: Dispel Magic +0.28 (+0.33), Metal Skin +0.05 (+0.14), Debuff Reducer +0.03 (+0.11)
- **Vyper**: Indomitable +0.16 (+0.30), Plated Armor +0.10 (+0.19), Bullet Resilience +0.05 (+0.10)
- **Sinclair**: Indomitable +0.18 (+0.32), Spellbreaker +0.14 (+0.33), Spirit Resilience +0.07 (+0.22)
- **Mina**: Divine Barrier +0.01 (+0.09), Counterspell +0.01 (+0.04), Return Fire -0.01 (+0.04)
- **Drifter**: Witchmail +0.09 (+0.26), Debuff Reducer +0.06 (+0.14), Unstoppable +0.04 (+0.17)
- **Venator**: Bullet Resilience +0.14 (+0.19), Metal Skin +0.12 (+0.22), Plated Armor +0.07 (+0.16)
- **Victor**: Spirit Resilience +0.05 (+0.19), Healbane +0.04 (+0.10), Spellbreaker +0.01 (+0.20)
- **Paige**: Witchmail +0.02 (+0.19), Counterspell +0.02 (+0.04), Divine Barrier +0.00 (+0.08)
- **The Doorman**: Spirit Resilience +0.47 (+0.61), Indomitable +0.29 (+0.43), Witchmail +0.19 (+0.36)
- **Billy**: Reactive Barrier +0.06 (+0.09), Healbane +0.02 (+0.07), Return Fire +0.02 (+0.06)
- **Graves**: Return Fire +0.04 (+0.08), Metal Skin +0.02 (+0.11), Reactive Barrier +0.01 (+0.04)
- **Apollo**: Reactive Barrier +0.04 (+0.06), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.26 (+0.40), Spellbreaker +0.18 (+0.37), Indomitable +0.15 (+0.28)
- **Rem**: Debuff Reducer +0.14 (+0.22), Unstoppable +0.08 (+0.21), Spellbreaker +0.06 (+0.25)
- **Silver**: Metal Skin +0.16 (+0.25), Dispel Magic +0.15 (+0.20), Indomitable +0.14 (+0.27)
- **Celeste**: Witchmail +0.07 (+0.24), Dispel Magic +0.02 (+0.07), Spirit Resilience +0.02 (+0.16)
- **Rat King**: Debuff Reducer +0.02 (+0.10), Healbane -0.00 (+0.05), Counterspell -0.01 (+0.02)
- **Solomon**: Counterspell +0.00 (+0.03), Reactive Barrier -0.01 (+0.02), Return Fire -0.01 (+0.03)
- **Violet**: Dispel Magic +0.00 (+0.05), Return Fire +0.00 (+0.05), Healbane +0.00 (+0.06)
- **Nurse Harrow**: Divine Barrier +0.14 (+0.21), Counterspell +0.09 (+0.12), Bullet Resilience +0.07 (+0.12)
- **Baba**: Counterspell -0.00 (+0.03), Healbane -0.00 (+0.05), Reactive Barrier -0.02 (+0.01)
