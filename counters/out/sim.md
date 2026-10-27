# Counter items in the sim (phantom and up)

Built 2026-10-27T12:54:08Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.393 | +0.063 | +0.102 | Lash +0.24, Wraith +0.18, Calico +0.11 | 0 heroes |
| Spirit Resilience | 3,200 | +0.188 | +0.059 | +0.128 | Lash +0.27, Wraith +0.20, Deadman Danny +0.19 | 1 heroes |
| Dispel Magic | 3,200 | +0.094 | +0.029 | +0.080 | Mirage +0.38, Silver +0.13, Infernus +0.11 | 4 heroes |
| Indomitable | 6,400 | +0.172 | +0.027 | +0.146 | Wraith +0.33, Vyper +0.28, Deadman Danny +0.25 | 0 heroes |
| Reactive Barrier | 1,600 | +0.041 | +0.026 | +0.058 | Wraith +0.16, Deadman Danny +0.14, The Doorman +0.08 | 2 heroes |
| Witchmail | 6,400 | +0.136 | +0.021 | +0.202 | Deadman Danny +0.20, Lash +0.18, Wraith +0.17 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.061 | Wraith +0.09, Deadman Danny +0.07, Venator +0.06 | 0 heroes |
| Spellbreaker | 6,400 | +0.086 | +0.013 | +0.153 | Lash +0.31, Deadman Danny +0.24, Wraith +0.21 | 0 heroes |
| Bullet Resilience | 3,200 | +0.002 | +0.001 | +0.094 | Venator +0.16, Wraith +0.14, Paradox +0.14 | 0 heroes |
| Healbane | 1,600 | -0.005 | -0.003 | +0.089 | Nurse Harrow +0.05, Deadman Danny +0.05, Lash +0.04 | 11 heroes |
| Plated Armor | 6,400 | -0.031 | -0.005 | +0.131 | Holliday +0.22, Wraith +0.18, Deadman Danny +0.17 | 0 heroes |
| Counterspell | 3,200 | -0.024 | -0.007 | +0.074 | Deadman Danny +0.10, Calico +0.05, Drifter +0.05 | 1 heroes |
| Unstoppable | 6,400 | -0.049 | -0.008 | +0.117 | Deadman Danny +0.17, Wraith +0.14, Abrams +0.12 | 0 heroes |
| Metal Skin | 3,200 | -0.143 | -0.045 | +0.112 | Wraith +0.26, Lash +0.21, Paradox +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.170 | -0.106 | +0.082 | Wraith +0.09, Deadman Danny +0.07, Drifter +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.19), Unstoppable +0.06 (+0.18), Spirit Resilience +0.04 (+0.17)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.04 (+0.02)
- **Vindicta**: Return Fire +0.00 (+0.09), Witchmail +0.00 (+0.20), Divine Barrier +0.00 (+0.10)
- **Lady Geist**: Return Fire +0.04 (+0.13), Dispel Magic +0.03 (+0.10), Divine Barrier +0.02 (+0.12)
- **Abrams**: Indomitable +0.18 (+0.32), Unstoppable +0.12 (+0.24), Divine Barrier +0.07 (+0.17)
- **Wraith**: Indomitable +0.33 (+0.47), Metal Skin +0.26 (+0.37), Spellbreaker +0.21 (+0.37)
- **McGinnis**: Spirit Resilience +0.01 (+0.14), Return Fire -0.00 (+0.08), Counterspell -0.01 (+0.07)
- **Paradox**: Metal Skin +0.15 (+0.27), Bullet Resilience +0.14 (+0.23), Plated Armor +0.12 (+0.26)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.03 (+0.05), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Witchmail -0.00 (+0.20), Healbane -0.00 (+0.09), Spirit Resilience -0.01 (+0.12)
- **Haze**: Plated Armor +0.08 (+0.21), Bullet Resilience +0.05 (+0.14), Indomitable +0.04 (+0.18)
- **Holliday**: Plated Armor +0.22 (+0.35), Reactive Barrier +0.04 (+0.09), Debuff Reducer +0.03 (+0.09)
- **Bebop**: Divine Barrier +0.02 (+0.13), Bullet Resilience +0.02 (+0.11), Witchmail +0.01 (+0.22)
- **Calico**: Spellbreaker +0.12 (+0.27), Divine Barrier +0.11 (+0.21), Spirit Resilience +0.10 (+0.23)
- **Grey Talon**: Reactive Barrier +0.05 (+0.10), Debuff Reducer +0.04 (+0.10), Indomitable +0.03 (+0.18)
- **Mo & Krill**: Spellbreaker +0.13 (+0.28), Witchmail +0.07 (+0.28), Spirit Resilience +0.07 (+0.20)
- **Shiv**: Healbane -0.01 (+0.08), Return Fire -0.02 (+0.07), Debuff Reducer -0.04 (+0.03)
- **Ivy**: Unstoppable +0.10 (+0.22), Indomitable +0.06 (+0.21), Dispel Magic -0.01 (+0.07)
- **Warden**: Return Fire +0.00 (+0.09), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.04)
- **Yamato**: Healbane +0.02 (+0.11), Counterspell -0.04 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Lash**: Spellbreaker +0.31 (+0.47), Spirit Resilience +0.27 (+0.39), Divine Barrier +0.24 (+0.34)
- **Viscous**: Healbane -0.03 (+0.06), Divine Barrier -0.03 (+0.07), Return Fire -0.04 (+0.04)
- **Pocket**: Witchmail +0.06 (+0.26), Spirit Resilience +0.04 (+0.17), Dispel Magic +0.03 (+0.11)
- **Mirage**: Dispel Magic +0.38 (+0.46), Spellbreaker +0.07 (+0.23), Spirit Resilience +0.07 (+0.19)
- **Vyper**: Indomitable +0.28 (+0.43), Debuff Reducer +0.04 (+0.10), Unstoppable +0.02 (+0.14)
- **Sinclair**: Indomitable +0.07 (+0.22), Spellbreaker +0.01 (+0.17), Unstoppable +0.01 (+0.12)
- **Mina**: Witchmail +0.03 (+0.23), Return Fire +0.02 (+0.11), Counterspell -0.00 (+0.07)
- **Drifter**: Witchmail +0.06 (+0.26), Return Fire +0.05 (+0.14), Counterspell +0.05 (+0.12)
- **Venator**: Bullet Resilience +0.16 (+0.25), Divine Barrier +0.09 (+0.20), Metal Skin +0.07 (+0.19)
- **Victor**: Spirit Resilience +0.03 (+0.16), Healbane +0.01 (+0.10), Spellbreaker -0.00 (+0.15)
- **Paige**: Healbane -0.01 (+0.08), Counterspell -0.03 (+0.05), Return Fire -0.03 (+0.06)
- **The Doorman**: Indomitable +0.15 (+0.30), Witchmail +0.11 (+0.32), Spirit Resilience +0.10 (+0.23)
- **Billy**: Healbane +0.04 (+0.12), Spellbreaker +0.03 (+0.18), Counterspell +0.03 (+0.10)
- **Graves**: Metal Skin +0.09 (+0.20), Witchmail +0.08 (+0.28), Spirit Resilience +0.08 (+0.21)
- **Apollo**: Healbane +0.00 (+0.09), Unstoppable -0.01 (+0.11), Reactive Barrier -0.01 (+0.05)
- **Deadman Danny**: Indomitable +0.25 (+0.40), Spellbreaker +0.24 (+0.40), Witchmail +0.20 (+0.40)
- **Rem**: Witchmail -0.01 (+0.20), Dispel Magic -0.02 (+0.06), Unstoppable -0.02 (+0.10)
- **Silver**: Dispel Magic +0.13 (+0.21), Metal Skin +0.02 (+0.14), Reactive Barrier +0.02 (+0.08)
- **Celeste**: Spirit Resilience +0.09 (+0.22), Witchmail +0.08 (+0.28), Dispel Magic +0.03 (+0.11)
- **Rat King**: Counterspell +0.00 (+0.08), Bullet Resilience -0.01 (+0.09), Return Fire -0.01 (+0.07)
- **Solomon**: Return Fire -0.01 (+0.07), Counterspell -0.03 (+0.05), Reactive Barrier -0.03 (+0.03)
- **Violet**: Return Fire +0.03 (+0.11), Healbane -0.02 (+0.06), Counterspell -0.04 (+0.03)
- **Nurse Harrow**: Healbane +0.05 (+0.14), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Baba**: Healbane -0.00 (+0.08), Debuff Reducer -0.03 (+0.04), Counterspell -0.03 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.163 | +0.051 | +0.115 | Lash +0.33, Pocket +0.23, Deadman Danny +0.21 | 10 heroes |
| Divine Barrier | 6,400 | +0.256 | +0.041 | +0.063 | Lash +0.19, Wraith +0.13, The Doorman +0.10 | 1 heroes |
| Dispel Magic | 3,200 | +0.077 | +0.024 | +0.048 | Mirage +0.31, Infernus +0.10, Graves +0.09 | 7 heroes |
| Indomitable | 6,400 | +0.137 | +0.022 | +0.115 | Vyper +0.35, Wraith +0.29, Deadman Danny +0.13 | 0 heroes |
| Witchmail | 6,400 | +0.130 | +0.020 | +0.163 | Graves +0.17, Lash +0.16, Pocket +0.14 | 0 heroes |
| Spellbreaker | 6,400 | +0.101 | +0.016 | +0.121 | Lash +0.36, Deadman Danny +0.15, Wraith +0.14 | 0 heroes |
| Reactive Barrier | 1,600 | +0.022 | +0.014 | +0.042 | Graves +0.12, Wraith +0.11, Deadman Danny +0.10 | 4 heroes |
| Debuff Reducer | 1,600 | -0.004 | -0.003 | +0.041 | Wraith +0.09, Lash +0.04, The Doorman +0.04 | 1 heroes |
| Plated Armor | 6,400 | -0.024 | -0.004 | +0.102 | Deadman Danny +0.22, Wraith +0.14, Paradox +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | -0.030 | -0.009 | +0.061 | Venator +0.11, Paradox +0.11, Wraith +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.034 | -0.011 | +0.044 | Wraith +0.05, Graves +0.04, Vindicta +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.078 | -0.012 | +0.086 | Mo & Krill +0.12, Ivy +0.10, Wraith +0.09 | 0 heroes |
| Healbane | 1,600 | -0.033 | -0.021 | +0.063 | Yamato +0.08, Bebop +0.05, Graves +0.04 | 17 heroes |
| Metal Skin | 3,200 | -0.161 | -0.050 | +0.085 | Wraith +0.22, Paradox +0.16, Graves +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.179 | -0.112 | +0.056 | Wraith +0.09, Lady Geist +0.06, Paradox +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.15), Unstoppable +0.05 (+0.13), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.04 (+0.20), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Witchmail +0.06 (+0.22), Divine Barrier +0.04 (+0.10), Bullet Resilience +0.04 (+0.10)
- **Lady Geist**: Return Fire +0.06 (+0.12), Divine Barrier +0.05 (+0.12), Bullet Resilience +0.05 (+0.11)
- **Abrams**: Indomitable +0.09 (+0.21), Unstoppable +0.08 (+0.16), Healbane +0.02 (+0.09)
- **Wraith**: Indomitable +0.29 (+0.40), Metal Skin +0.22 (+0.30), Spellbreaker +0.14 (+0.26)
- **McGinnis**: Spirit Resilience +0.09 (+0.20), Return Fire +0.01 (+0.07), Dispel Magic +0.01 (+0.06)
- **Paradox**: Metal Skin +0.16 (+0.24), Bullet Resilience +0.11 (+0.17), Plated Armor +0.09 (+0.20)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.02 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.06 (+0.17), Dispel Magic +0.03 (+0.08), Counterspell +0.03 (+0.07)
- **Haze**: Indomitable +0.09 (+0.21), Plated Armor +0.08 (+0.18), Unstoppable +0.08 (+0.17)
- **Holliday**: Debuff Reducer +0.03 (+0.07), Return Fire +0.03 (+0.08), Indomitable +0.03 (+0.14)
- **Bebop**: Healbane +0.05 (+0.11), Counterspell +0.01 (+0.06), Metal Skin +0.01 (+0.10)
- **Calico**: Reactive Barrier +0.06 (+0.10), Divine Barrier +0.05 (+0.12), Spellbreaker +0.05 (+0.17)
- **Grey Talon**: Debuff Reducer +0.03 (+0.07), Reactive Barrier +0.02 (+0.06), Spellbreaker +0.02 (+0.14)
- **Mo & Krill**: Unstoppable +0.12 (+0.20), Dispel Magic +0.06 (+0.11), Spellbreaker +0.05 (+0.17)
- **Shiv**: Metal Skin +0.05 (+0.14), Bullet Resilience +0.05 (+0.11), Divine Barrier +0.05 (+0.11)
- **Ivy**: Unstoppable +0.10 (+0.18), Indomitable +0.08 (+0.19), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.08), Debuff Reducer -0.00 (+0.04), Counterspell -0.00 (+0.04)
- **Yamato**: Healbane +0.08 (+0.15), Counterspell +0.01 (+0.06), Bullet Resilience +0.01 (+0.07)
- **Lash**: Spellbreaker +0.36 (+0.48), Spirit Resilience +0.33 (+0.44), Divine Barrier +0.19 (+0.26)
- **Viscous**: Divine Barrier +0.00 (+0.07), Debuff Reducer -0.01 (+0.03), Counterspell -0.01 (+0.03)
- **Pocket**: Spirit Resilience +0.23 (+0.34), Witchmail +0.14 (+0.30), Spellbreaker +0.14 (+0.26)
- **Mirage**: Dispel Magic +0.31 (+0.35), Spirit Resilience +0.05 (+0.16), Metal Skin +0.05 (+0.13)
- **Vyper**: Indomitable +0.35 (+0.46), Metal Skin +0.06 (+0.14), Debuff Reducer +0.04 (+0.08)
- **Sinclair**: Indomitable +0.07 (+0.18), Return Fire -0.00 (+0.06), Debuff Reducer -0.02 (+0.02)
- **Mina**: Witchmail +0.04 (+0.20), Plated Armor +0.02 (+0.13), Spirit Resilience +0.02 (+0.14)
- **Drifter**: Witchmail +0.04 (+0.21), Bullet Resilience +0.01 (+0.07), Counterspell +0.00 (+0.05)
- **Venator**: Bullet Resilience +0.11 (+0.17), Metal Skin +0.11 (+0.19), Divine Barrier +0.05 (+0.11)
- **Victor**: Spirit Resilience +0.07 (+0.18), Spellbreaker +0.07 (+0.19), Dispel Magic -0.01 (+0.04)
- **Paige**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.04), Healbane -0.01 (+0.05)
- **The Doorman**: Spirit Resilience +0.16 (+0.28), Indomitable +0.12 (+0.24), Witchmail +0.10 (+0.27)
- **Billy**: Spirit Resilience +0.02 (+0.13), Counterspell -0.01 (+0.04), Spellbreaker -0.01 (+0.11)
- **Graves**: Witchmail +0.17 (+0.34), Spirit Resilience +0.13 (+0.25), Metal Skin +0.13 (+0.22)
- **Apollo**: Reactive Barrier +0.06 (+0.10), Indomitable +0.04 (+0.16), Unstoppable -0.00 (+0.08)
- **Deadman Danny**: Plated Armor +0.22 (+0.33), Spirit Resilience +0.21 (+0.32), Spellbreaker +0.15 (+0.27)
- **Rem**: Counterspell -0.00 (+0.04), Divine Barrier -0.00 (+0.06), Healbane -0.01 (+0.06)
- **Silver**: Dispel Magic +0.06 (+0.11), Metal Skin +0.05 (+0.13), Reactive Barrier +0.04 (+0.08)
- **Celeste**: Witchmail -0.00 (+0.16), Spirit Resilience -0.00 (+0.11), Healbane -0.01 (+0.06)
- **Rat King**: Bullet Resilience -0.00 (+0.06), Return Fire -0.01 (+0.05), Metal Skin -0.01 (+0.08)
- **Solomon**: Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.03), Healbane -0.02 (+0.05)
- **Violet**: Return Fire +0.04 (+0.09), Witchmail +0.02 (+0.19), Healbane +0.01 (+0.08)
- **Nurse Harrow**: Healbane -0.02 (+0.04), Dispel Magic -0.02 (+0.02), Counterspell -0.03 (+0.01)
- **Baba**: Unstoppable +0.03 (+0.11), Healbane +0.01 (+0.08), Counterspell -0.00 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.158 | +0.049 | +0.127 | Lash +0.29, Deadman Danny +0.26, The Doorman +0.12 | 14 heroes |
| Divine Barrier | 6,400 | +0.201 | +0.032 | +0.066 | Lash +0.22, Vindicta +0.12, Paradox +0.10 | 2 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.065 | Lash +0.29, Mirage +0.28, Paradox +0.11 | 9 heroes |
| Indomitable | 6,400 | +0.152 | +0.025 | +0.139 | Vyper +0.38, Wraith +0.30, Deadman Danny +0.25 | 0 heroes |
| Witchmail | 6,400 | +0.130 | +0.020 | +0.174 | Lash +0.20, Deadman Danny +0.19, Paradox +0.12 | 1 heroes |
| Spellbreaker | 6,400 | +0.112 | +0.018 | +0.140 | Lash +0.42, Deadman Danny +0.23, Paradox +0.14 | 0 heroes |
| Reactive Barrier | 1,600 | +0.008 | +0.005 | +0.042 | Deadman Danny +0.15, Yamato +0.12, Wraith +0.09 | 5 heroes |
| Plated Armor | 6,400 | -0.016 | -0.003 | +0.119 | Deadman Danny +0.23, Holliday +0.18, Wraith +0.15 | 0 heroes |
| Debuff Reducer | 1,600 | -0.009 | -0.006 | +0.048 | Grey Talon +0.09, Deadman Danny +0.08, Vyper +0.06 | 0 heroes |
| Counterspell | 3,200 | -0.036 | -0.011 | +0.038 | Deadman Danny +0.08, Drifter +0.06, Vindicta +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.077 | -0.012 | +0.105 | Deadman Danny +0.18, Abrams +0.13, Paradox +0.12 | 3 heroes |
| Bullet Resilience | 3,200 | -0.040 | -0.013 | +0.065 | Deadman Danny +0.13, Vindicta +0.11, Lash +0.10 | 1 heroes |
| Healbane | 1,600 | -0.034 | -0.021 | +0.063 | Drifter +0.07, Infernus +0.04, Abrams +0.03 | 15 heroes |
| Metal Skin | 3,200 | -0.151 | -0.047 | +0.111 | Wraith +0.25, Lash +0.19, Paradox +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.173 | -0.108 | +0.055 | Wraith +0.09, Paradox +0.06, Drifter +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.17), Unstoppable +0.10 (+0.20), Spellbreaker +0.08 (+0.22)
- **Seven**: Witchmail +0.04 (+0.21), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03)
- **Vindicta**: Divine Barrier +0.12 (+0.18), Bullet Resilience +0.11 (+0.17), Witchmail +0.08 (+0.25)
- **Lady Geist**: Return Fire +0.04 (+0.09), Bullet Resilience +0.03 (+0.09), Divine Barrier +0.03 (+0.09)
- **Abrams**: Unstoppable +0.13 (+0.24), Dispel Magic +0.06 (+0.12), Healbane +0.03 (+0.10)
- **Wraith**: Indomitable +0.30 (+0.44), Metal Skin +0.25 (+0.36), Plated Armor +0.15 (+0.27)
- **McGinnis**: Spirit Resilience +0.09 (+0.22), Witchmail +0.03 (+0.20), Spellbreaker +0.02 (+0.15)
- **Paradox**: Spellbreaker +0.14 (+0.28), Witchmail +0.12 (+0.29), Unstoppable +0.12 (+0.22)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.00 (+0.04), Return Fire -0.03 (+0.02)
- **Kelvin**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03), Spirit Resilience -0.02 (+0.10)
- **Haze**: Plated Armor +0.09 (+0.21), Indomitable +0.08 (+0.22), Unstoppable +0.06 (+0.17)
- **Holliday**: Plated Armor +0.18 (+0.30), Debuff Reducer +0.04 (+0.09), Indomitable +0.04 (+0.18)
- **Bebop**: Healbane +0.01 (+0.07), Counterspell -0.02 (+0.02), Return Fire -0.03 (+0.03)
- **Calico**: Reactive Barrier +0.06 (+0.10), Spirit Resilience +0.04 (+0.17), Divine Barrier +0.04 (+0.10)
- **Grey Talon**: Spellbreaker +0.13 (+0.27), Unstoppable +0.12 (+0.22), Debuff Reducer +0.09 (+0.14)
- **Mo & Krill**: Unstoppable +0.08 (+0.18), Spirit Resilience +0.07 (+0.19), Spellbreaker +0.05 (+0.19)
- **Shiv**: Metal Skin +0.03 (+0.15), Divine Barrier +0.02 (+0.09), Bullet Resilience +0.02 (+0.08)
- **Ivy**: Unstoppable +0.10 (+0.20), Indomitable +0.04 (+0.18), Debuff Reducer +0.01 (+0.06)
- **Warden**: Return Fire +0.03 (+0.09), Counterspell +0.02 (+0.06), Divine Barrier +0.01 (+0.08)
- **Yamato**: Reactive Barrier +0.12 (+0.16), Indomitable +0.12 (+0.26), Plated Armor +0.06 (+0.18)
- **Lash**: Spellbreaker +0.42 (+0.56), Spirit Resilience +0.29 (+0.42), Dispel Magic +0.29 (+0.36)
- **Viscous**: Divine Barrier +0.02 (+0.08), Healbane +0.01 (+0.07), Return Fire -0.00 (+0.05)
- **Pocket**: Spirit Resilience +0.10 (+0.23), Witchmail +0.03 (+0.21), Spellbreaker +0.01 (+0.15)
- **Mirage**: Dispel Magic +0.28 (+0.35), Spirit Resilience +0.02 (+0.14), Healbane +0.01 (+0.07)
- **Vyper**: Indomitable +0.38 (+0.52), Debuff Reducer +0.06 (+0.11), Unstoppable +0.05 (+0.16)
- **Sinclair**: Indomitable +0.12 (+0.26), Return Fire +0.00 (+0.06), Unstoppable -0.01 (+0.09)
- **Mina**: Witchmail +0.11 (+0.29), Spirit Resilience +0.11 (+0.24), Spellbreaker +0.06 (+0.20)
- **Drifter**: Spirit Resilience +0.10 (+0.23), Witchmail +0.08 (+0.25), Healbane +0.07 (+0.14)
- **Venator**: Metal Skin +0.10 (+0.21), Bullet Resilience +0.06 (+0.13), Divine Barrier +0.03 (+0.10)
- **Victor**: Spirit Resilience +0.02 (+0.15), Healbane +0.00 (+0.07), Spellbreaker +0.00 (+0.14)
- **Paige**: Unstoppable +0.11 (+0.21), Debuff Reducer +0.05 (+0.10), Counterspell -0.01 (+0.03)
- **The Doorman**: Spirit Resilience +0.12 (+0.25), Indomitable +0.11 (+0.25), Witchmail +0.09 (+0.26)
- **Billy**: Reactive Barrier +0.02 (+0.06), Healbane -0.01 (+0.06), Debuff Reducer -0.02 (+0.03)
- **Graves**: Return Fire +0.02 (+0.07), Witchmail +0.02 (+0.19), Counterspell +0.00 (+0.04)
- **Apollo**: Healbane -0.01 (+0.05), Reactive Barrier -0.02 (+0.02), Counterspell -0.03 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.26 (+0.39), Indomitable +0.25 (+0.39), Plated Armor +0.23 (+0.35)
- **Rem**: Debuff Reducer +0.06 (+0.11), Unstoppable +0.05 (+0.15), Counterspell -0.00 (+0.03)
- **Silver**: Dispel Magic +0.04 (+0.11), Return Fire -0.01 (+0.05), Indomitable -0.01 (+0.13)
- **Celeste**: Witchmail +0.04 (+0.22), Dispel Magic +0.04 (+0.11), Reactive Barrier +0.01 (+0.06)
- **Rat King**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.02), Bullet Resilience -0.01 (+0.05)
- **Solomon**: Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.05), Reactive Barrier -0.01 (+0.03)
- **Violet**: Witchmail +0.07 (+0.24), Return Fire +0.04 (+0.10), Healbane +0.02 (+0.08)
- **Nurse Harrow**: Healbane +0.02 (+0.09), Counterspell -0.02 (+0.02), Return Fire -0.04 (+0.02)
- **Baba**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02), Unstoppable -0.01 (+0.09)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.182 | +0.057 | +0.140 | Lash +0.56, Deadman Danny +0.35, The Doorman +0.31 | 15 heroes |
| Indomitable | 6,400 | +0.170 | +0.027 | +0.164 | Wraith +0.29, Deadman Danny +0.28, Vyper +0.26 | 1 heroes |
| Divine Barrier | 6,400 | +0.167 | +0.026 | +0.063 | Lash +0.27, Vindicta +0.12, The Doorman +0.12 | 3 heroes |
| Dispel Magic | 3,200 | +0.078 | +0.024 | +0.057 | Mirage +0.27, Silver +0.22, Lash +0.20 | 9 heroes |
| Witchmail | 6,400 | +0.122 | +0.019 | +0.163 | Lash +0.28, The Doorman +0.24, Deadman Danny +0.19 | 2 heroes |
| Spellbreaker | 6,400 | +0.121 | +0.019 | +0.143 | Lash +0.47, Deadman Danny +0.24, Grey Talon +0.18 | 0 heroes |
| Plated Armor | 6,400 | -0.028 | -0.004 | +0.102 | Lash +0.15, Vindicta +0.15, Vyper +0.14 | 2 heroes |
| Unstoppable | 6,400 | -0.074 | -0.011 | +0.116 | Haze +0.24, Infernus +0.23, Grey Talon +0.16 | 8 heroes |
| Counterspell | 3,200 | -0.040 | -0.012 | +0.032 | Lash +0.08, The Doorman +0.06, Yamato +0.04 | 1 heroes |
| Reactive Barrier | 1,600 | -0.021 | -0.013 | +0.041 | Deadman Danny +0.13, Drifter +0.13, The Doorman +0.09 | 3 heroes |
| Debuff Reducer | 1,600 | -0.022 | -0.014 | +0.046 | Grey Talon +0.10, Lash +0.10, Rem +0.07 | 0 heroes |
| Bullet Resilience | 3,200 | -0.047 | -0.015 | +0.060 | Lash +0.17, Venator +0.11, Vindicta +0.09 | 0 heroes |
| Healbane | 1,600 | -0.038 | -0.024 | +0.053 | Nurse Harrow +0.07, Lady Geist +0.06, Celeste +0.04 | 14 heroes |
| Metal Skin | 3,200 | -0.152 | -0.048 | +0.110 | Lash +0.27, Grey Talon +0.17, Silver +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.172 | -0.107 | +0.049 | Paradox +0.05, Haze +0.05, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.23 (+0.35), Dispel Magic +0.05 (+0.11), Healbane +0.04 (+0.09)
- **Seven**: Witchmail +0.06 (+0.22), Counterspell -0.01 (+0.02), Healbane -0.02 (+0.04)
- **Vindicta**: Plated Armor +0.15 (+0.25), Divine Barrier +0.12 (+0.18), Bullet Resilience +0.09 (+0.15)
- **Lady Geist**: Healbane +0.06 (+0.11), Dispel Magic +0.03 (+0.08), Metal Skin +0.02 (+0.13)
- **Abrams**: Unstoppable +0.06 (+0.17), Indomitable +0.04 (+0.20), Dispel Magic +0.03 (+0.08)
- **Wraith**: Indomitable +0.29 (+0.45), Metal Skin +0.13 (+0.24), Witchmail +0.07 (+0.24)
- **McGinnis**: Spirit Resilience +0.04 (+0.18), Healbane +0.02 (+0.07), Witchmail +0.01 (+0.18)
- **Paradox**: Witchmail +0.08 (+0.24), Unstoppable +0.07 (+0.19), Spirit Resilience +0.06 (+0.20)
- **Dynamo**: Healbane +0.02 (+0.07), Counterspell -0.00 (+0.03), Debuff Reducer -0.04 (+0.01)
- **Kelvin**: Spirit Resilience +0.07 (+0.21), Healbane +0.01 (+0.06), Spellbreaker +0.00 (+0.14)
- **Haze**: Unstoppable +0.24 (+0.36), Bullet Resilience +0.07 (+0.13), Metal Skin +0.07 (+0.18)
- **Holliday**: Spellbreaker +0.04 (+0.19), Return Fire +0.03 (+0.08), Plated Armor +0.02 (+0.12)
- **Bebop**: Debuff Reducer +0.06 (+0.10), Spellbreaker +0.03 (+0.17), Reactive Barrier +0.03 (+0.07)
- **Calico**: Spirit Resilience +0.14 (+0.28), Divine Barrier +0.11 (+0.17), Spellbreaker +0.10 (+0.24)
- **Grey Talon**: Spellbreaker +0.18 (+0.32), Metal Skin +0.17 (+0.28), Unstoppable +0.16 (+0.27)
- **Mo & Krill**: Dispel Magic +0.03 (+0.09), Unstoppable +0.03 (+0.15), Healbane +0.03 (+0.08)
- **Shiv**: Metal Skin +0.03 (+0.14), Bullet Resilience +0.02 (+0.08), Divine Barrier +0.01 (+0.07)
- **Ivy**: Unstoppable +0.14 (+0.25), Indomitable +0.08 (+0.25), Debuff Reducer +0.05 (+0.09)
- **Warden**: Plated Armor +0.06 (+0.16), Metal Skin +0.03 (+0.14), Return Fire +0.01 (+0.06)
- **Yamato**: Indomitable +0.12 (+0.29), Plated Armor +0.09 (+0.19), Counterspell +0.04 (+0.07)
- **Lash**: Spirit Resilience +0.56 (+0.70), Spellbreaker +0.47 (+0.61), Witchmail +0.28 (+0.44)
- **Viscous**: Divine Barrier +0.06 (+0.12), Witchmail +0.03 (+0.19), Return Fire +0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.08 (+0.22), Spellbreaker -0.01 (+0.14), Witchmail -0.01 (+0.15)
- **Mirage**: Dispel Magic +0.27 (+0.33), Metal Skin +0.07 (+0.18), Plated Armor -0.00 (+0.10)
- **Vyper**: Indomitable +0.26 (+0.43), Plated Armor +0.14 (+0.24), Metal Skin +0.07 (+0.18)
- **Sinclair**: Indomitable +0.14 (+0.30), Dispel Magic +0.06 (+0.12), Reactive Barrier +0.05 (+0.10)
- **Mina**: Divine Barrier +0.01 (+0.07), Plated Armor -0.01 (+0.09), Dispel Magic -0.01 (+0.04)
- **Drifter**: Indomitable +0.21 (+0.37), Spirit Resilience +0.20 (+0.34), Spellbreaker +0.13 (+0.27)
- **Venator**: Metal Skin +0.14 (+0.25), Bullet Resilience +0.11 (+0.17), Plated Armor +0.05 (+0.15)
- **Victor**: Spellbreaker +0.08 (+0.23), Spirit Resilience +0.05 (+0.19), Healbane +0.03 (+0.08)
- **Paige**: Counterspell +0.01 (+0.04), Return Fire -0.00 (+0.05), Healbane -0.01 (+0.04)
- **The Doorman**: Spirit Resilience +0.31 (+0.45), Witchmail +0.24 (+0.40), Indomitable +0.23 (+0.39)
- **Billy**: Reactive Barrier +0.07 (+0.11), Bullet Resilience +0.03 (+0.09), Plated Armor +0.03 (+0.13)
- **Graves**: Return Fire +0.02 (+0.06), Reactive Barrier -0.02 (+0.02), Counterspell -0.02 (+0.01)
- **Apollo**: Reactive Barrier +0.02 (+0.06), Healbane +0.01 (+0.06), Unstoppable -0.01 (+0.10)
- **Deadman Danny**: Spirit Resilience +0.35 (+0.49), Indomitable +0.28 (+0.44), Spellbreaker +0.24 (+0.38)
- **Rem**: Debuff Reducer +0.07 (+0.11), Spellbreaker +0.04 (+0.18), Return Fire +0.01 (+0.05)
- **Silver**: Dispel Magic +0.22 (+0.28), Metal Skin +0.15 (+0.26), Indomitable +0.11 (+0.27)
- **Celeste**: Witchmail +0.07 (+0.24), Spirit Resilience +0.07 (+0.21), Healbane +0.04 (+0.10)
- **Rat King**: Return Fire -0.01 (+0.04), Healbane -0.01 (+0.04), Counterspell -0.01 (+0.02)
- **Solomon**: Return Fire +0.00 (+0.05), Counterspell -0.00 (+0.03), Reactive Barrier -0.00 (+0.04)
- **Violet**: Return Fire +0.03 (+0.08), Witchmail +0.01 (+0.17), Divine Barrier -0.01 (+0.05)
- **Nurse Harrow**: Spirit Resilience +0.12 (+0.26), Dispel Magic +0.11 (+0.16), Divine Barrier +0.09 (+0.15)
- **Baba**: Healbane -0.00 (+0.05), Counterspell -0.01 (+0.02), Witchmail -0.01 (+0.15)
