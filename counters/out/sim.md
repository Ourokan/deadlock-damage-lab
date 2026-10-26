# Counter items in the sim (phantom and up)

Built 2026-10-26T21:59:03Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.223 | +0.070 | +0.120 | Lash +0.23, Wraith +0.16, Deadman Danny +0.14 | 1 heroes |
| Divine Barrier | 6,400 | +0.405 | +0.065 | +0.094 | Wraith +0.17, Lash +0.15, Calico +0.14 | 0 heroes |
| Dispel Magic | 3,200 | +0.140 | +0.044 | +0.076 | Mirage +0.37, Infernus +0.11, Paradox +0.11 | 4 heroes |
| Debuff Reducer | 1,600 | +0.066 | +0.041 | +0.058 | Wraith +0.09, Deadman Danny +0.08, Calico +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | +0.056 | +0.036 | +0.054 | Wraith +0.15, Deadman Danny +0.14, The Doorman +0.10 | 2 heroes |
| Witchmail | 6,400 | +0.224 | +0.035 | +0.190 | Wraith +0.17, Deadman Danny +0.16, Lash +0.14 | 0 heroes |
| Indomitable | 6,400 | +0.190 | +0.030 | +0.141 | Vyper +0.30, Wraith +0.30, Deadman Danny +0.20 | 0 heroes |
| Healbane | 1,600 | +0.038 | +0.024 | +0.088 | Nurse Harrow +0.06, Mo & Krill +0.05, Billy +0.05 | 11 heroes |
| Spellbreaker | 6,400 | +0.148 | +0.023 | +0.145 | Lash +0.22, Deadman Danny +0.21, Wraith +0.18 | 0 heroes |
| Bullet Resilience | 3,200 | +0.038 | +0.012 | +0.090 | Wraith +0.15, Paradox +0.14, Deadman Danny +0.11 | 0 heroes |
| Counterspell | 3,200 | +0.018 | +0.005 | +0.071 | Deadman Danny +0.09, Calico +0.07, Wraith +0.05 | 1 heroes |
| Plated Armor | 6,400 | +0.029 | +0.004 | +0.126 | Holliday +0.24, Wraith +0.17, Deadman Danny +0.15 | 0 heroes |
| Unstoppable | 6,400 | +0.001 | +0.000 | +0.114 | Deadman Danny +0.15, Wraith +0.13, Abrams +0.13 | 0 heroes |
| Metal Skin | 3,200 | -0.096 | -0.030 | +0.105 | Wraith +0.25, Paradox +0.17, Lash +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.130 | -0.081 | +0.075 | The Doorman +0.07, Wraith +0.06, Deadman Danny +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.19), Unstoppable +0.07 (+0.18), Spirit Resilience +0.06 (+0.18)
- **Seven**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.03 (+0.02)
- **Vindicta**: Witchmail +0.01 (+0.20), Divine Barrier +0.01 (+0.11), Return Fire +0.00 (+0.08)
- **Lady Geist**: Return Fire +0.05 (+0.12), Dispel Magic +0.02 (+0.10), Counterspell +0.02 (+0.09)
- **Abrams**: Indomitable +0.15 (+0.29), Unstoppable +0.13 (+0.24), Spirit Resilience +0.07 (+0.19)
- **Wraith**: Indomitable +0.30 (+0.44), Metal Skin +0.25 (+0.36), Spellbreaker +0.18 (+0.33)
- **McGinnis**: Spirit Resilience +0.05 (+0.17), Healbane -0.01 (+0.07), Debuff Reducer -0.02 (+0.04)
- **Paradox**: Metal Skin +0.17 (+0.28), Bullet Resilience +0.14 (+0.23), Indomitable +0.13 (+0.27)
- **Dynamo**: Healbane +0.01 (+0.10), Counterspell -0.03 (+0.05), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane +0.00 (+0.09), Counterspell -0.01 (+0.06), Dispel Magic -0.02 (+0.06)
- **Haze**: Plated Armor +0.09 (+0.21), Indomitable +0.06 (+0.20), Bullet Resilience +0.05 (+0.14)
- **Holliday**: Plated Armor +0.24 (+0.37), Spellbreaker +0.05 (+0.20), Debuff Reducer +0.05 (+0.10)
- **Bebop**: Counterspell +0.02 (+0.09), Healbane +0.02 (+0.11), Return Fire +0.02 (+0.09)
- **Calico**: Spellbreaker +0.14 (+0.29), Divine Barrier +0.14 (+0.23), Spirit Resilience +0.13 (+0.25)
- **Grey Talon**: Reactive Barrier +0.08 (+0.13), Spellbreaker +0.07 (+0.21), Indomitable +0.06 (+0.20)
- **Mo & Krill**: Spellbreaker +0.13 (+0.28), Spirit Resilience +0.09 (+0.20), Witchmail +0.07 (+0.26)
- **Shiv**: Healbane -0.00 (+0.09), Return Fire -0.01 (+0.07), Debuff Reducer -0.03 (+0.03)
- **Ivy**: Unstoppable +0.11 (+0.23), Indomitable +0.07 (+0.21), Dispel Magic +0.01 (+0.09)
- **Warden**: Return Fire +0.01 (+0.09), Counterspell -0.01 (+0.06), Dispel Magic -0.03 (+0.05)
- **Yamato**: Healbane +0.02 (+0.11), Debuff Reducer -0.04 (+0.02), Counterspell -0.05 (+0.02)
- **Lash**: Spirit Resilience +0.23 (+0.35), Spellbreaker +0.22 (+0.36), Divine Barrier +0.15 (+0.24)
- **Viscous**: Debuff Reducer -0.03 (+0.03), Counterspell -0.03 (+0.04), Return Fire -0.03 (+0.05)
- **Pocket**: Witchmail +0.04 (+0.23), Spirit Resilience +0.03 (+0.15), Spellbreaker +0.02 (+0.16)
- **Mirage**: Dispel Magic +0.37 (+0.44), Spirit Resilience +0.06 (+0.18), Spellbreaker +0.05 (+0.20)
- **Vyper**: Indomitable +0.30 (+0.44), Debuff Reducer +0.05 (+0.11), Spellbreaker +0.04 (+0.18)
- **Sinclair**: Indomitable +0.11 (+0.25), Spellbreaker +0.01 (+0.16), Unstoppable +0.01 (+0.12)
- **Mina**: Spirit Resilience +0.10 (+0.22), Divine Barrier +0.08 (+0.17), Spellbreaker +0.08 (+0.22)
- **Drifter**: Witchmail +0.01 (+0.20), Counterspell +0.00 (+0.07), Return Fire +0.00 (+0.08)
- **Venator**: Bullet Resilience +0.10 (+0.19), Metal Skin +0.04 (+0.14), Divine Barrier +0.02 (+0.11)
- **Victor**: Healbane -0.01 (+0.08), Counterspell -0.05 (+0.03), Debuff Reducer -0.05 (+0.01)
- **Paige**: Healbane -0.01 (+0.08), Counterspell -0.02 (+0.05), Return Fire -0.02 (+0.06)
- **The Doorman**: Indomitable +0.18 (+0.32), Spellbreaker +0.12 (+0.26), Spirit Resilience +0.12 (+0.23)
- **Billy**: Counterspell +0.05 (+0.12), Healbane +0.05 (+0.13), Spellbreaker +0.04 (+0.19)
- **Graves**: Spirit Resilience +0.09 (+0.21), Witchmail +0.09 (+0.28), Metal Skin +0.08 (+0.19)
- **Apollo**: Healbane -0.01 (+0.08), Reactive Barrier -0.04 (+0.01), Debuff Reducer -0.05 (+0.01)
- **Deadman Danny**: Spellbreaker +0.21 (+0.36), Indomitable +0.20 (+0.35), Witchmail +0.16 (+0.35)
- **Rem**: Unstoppable +0.00 (+0.12), Witchmail +0.00 (+0.19), Debuff Reducer -0.00 (+0.05)
- **Silver**: Dispel Magic +0.03 (+0.11), Metal Skin +0.01 (+0.12), Debuff Reducer -0.02 (+0.04)
- **Celeste**: Witchmail +0.11 (+0.30), Spirit Resilience +0.11 (+0.23), Dispel Magic +0.04 (+0.12)
- **Rat King**: Counterspell +0.00 (+0.07), Return Fire -0.01 (+0.07), Bullet Resilience -0.01 (+0.08)
- **Solomon**: Return Fire -0.01 (+0.07), Counterspell -0.01 (+0.06), Healbane -0.02 (+0.07)
- **Violet**: Return Fire +0.02 (+0.09), Healbane -0.02 (+0.07), Witchmail -0.04 (+0.15)
- **Nurse Harrow**: Healbane +0.06 (+0.15), Return Fire +0.02 (+0.09), Counterspell -0.03 (+0.04)
- **Baba**: Healbane +0.01 (+0.09), Debuff Reducer -0.02 (+0.04), Unstoppable -0.02 (+0.09)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.199 | +0.062 | +0.106 | Lash +0.27, Pocket +0.22, Deadman Danny +0.20 | 10 heroes |
| Divine Barrier | 6,400 | +0.258 | +0.041 | +0.059 | Lash +0.16, Wraith +0.11, The Doorman +0.10 | 1 heroes |
| Dispel Magic | 3,200 | +0.109 | +0.034 | +0.048 | Mirage +0.30, Pocket +0.11, Infernus +0.09 | 7 heroes |
| Witchmail | 6,400 | +0.203 | +0.032 | +0.153 | Graves +0.17, Lash +0.14, Deadman Danny +0.14 | 0 heroes |
| Indomitable | 6,400 | +0.152 | +0.025 | +0.107 | Vyper +0.34, Wraith +0.23, The Doorman +0.14 | 0 heroes |
| Spellbreaker | 6,400 | +0.136 | +0.021 | +0.110 | Lash +0.23, Deadman Danny +0.17, Pocket +0.13 | 0 heroes |
| Reactive Barrier | 1,600 | +0.030 | +0.019 | +0.036 | Deadman Danny +0.10, Graves +0.10, Wraith +0.09 | 4 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.036 | Pocket +0.07, Wraith +0.07, Vyper +0.06 | 1 heroes |
| Plated Armor | 6,400 | +0.018 | +0.003 | +0.098 | Deadman Danny +0.24, Wraith +0.12, Haze +0.09 | 0 heroes |
| Healbane | 1,600 | -0.004 | -0.003 | +0.062 | Pocket +0.07, Bebop +0.04, Yamato +0.03 | 17 heroes |
| Counterspell | 3,200 | -0.015 | -0.004 | +0.037 | Pocket +0.07, Vindicta +0.05, The Doorman +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.037 | -0.006 | +0.080 | Mo & Krill +0.13, Ivy +0.12, Haze +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.120 | -0.037 | +0.081 | Wraith +0.20, Lash +0.15, Paradox +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.152 | -0.095 | +0.049 | Pocket +0.08, Wraith +0.06, The Doorman +0.06 | 0 heroes |
| Bullet Resilience | 3,200 | +0.000 | +0.000 | +0.056 | Paradox +0.10, Venator +0.09, Wraith +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.14), Unstoppable +0.05 (+0.13), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.03 (+0.18), Healbane +0.00 (+0.06), Counterspell -0.00 (+0.03)
- **Vindicta**: Witchmail +0.06 (+0.22), Divine Barrier +0.05 (+0.11), Counterspell +0.05 (+0.09)
- **Lady Geist**: Metal Skin +0.07 (+0.15), Bullet Resilience +0.06 (+0.12), Divine Barrier +0.06 (+0.12)
- **Abrams**: Unstoppable +0.07 (+0.15), Indomitable +0.07 (+0.18), Healbane +0.03 (+0.09)
- **Wraith**: Indomitable +0.23 (+0.33), Metal Skin +0.20 (+0.28), Spellbreaker +0.12 (+0.23)
- **McGinnis**: Dispel Magic -0.01 (+0.04), Counterspell -0.01 (+0.03), Debuff Reducer -0.01 (+0.02)
- **Paradox**: Metal Skin +0.14 (+0.23), Bullet Resilience +0.10 (+0.15), Plated Armor +0.09 (+0.19)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.02 (+0.02), Debuff Reducer -0.02 (+0.01)
- **Kelvin**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Dispel Magic -0.01 (+0.04)
- **Haze**: Indomitable +0.10 (+0.20), Unstoppable +0.10 (+0.18), Plated Armor +0.09 (+0.19)
- **Holliday**: Debuff Reducer +0.04 (+0.07), Return Fire +0.04 (+0.09), Indomitable +0.03 (+0.14)
- **Bebop**: Healbane +0.04 (+0.10), Metal Skin +0.01 (+0.09), Counterspell -0.01 (+0.03)
- **Calico**: Reactive Barrier +0.04 (+0.08), Divine Barrier +0.02 (+0.08), Spellbreaker +0.01 (+0.12)
- **Grey Talon**: Debuff Reducer +0.04 (+0.07), Spellbreaker +0.04 (+0.15), Unstoppable +0.02 (+0.10)
- **Mo & Krill**: Unstoppable +0.13 (+0.21), Spellbreaker +0.06 (+0.17), Dispel Magic +0.04 (+0.09)
- **Shiv**: Bullet Resilience +0.04 (+0.10), Metal Skin +0.04 (+0.12), Divine Barrier +0.04 (+0.09)
- **Ivy**: Unstoppable +0.12 (+0.20), Indomitable +0.09 (+0.20), Debuff Reducer +0.02 (+0.05)
- **Warden**: Return Fire +0.02 (+0.07), Counterspell +0.00 (+0.04), Debuff Reducer -0.01 (+0.03)
- **Yamato**: Healbane +0.03 (+0.10), Counterspell -0.02 (+0.02), Debuff Reducer -0.02 (+0.02)
- **Lash**: Spirit Resilience +0.27 (+0.38), Spellbreaker +0.23 (+0.34), Divine Barrier +0.16 (+0.22)
- **Viscous**: Return Fire -0.02 (+0.03), Counterspell -0.02 (+0.02), Debuff Reducer -0.02 (+0.02)
- **Pocket**: Spirit Resilience +0.22 (+0.33), Spellbreaker +0.13 (+0.24), Witchmail +0.11 (+0.27)
- **Mirage**: Dispel Magic +0.30 (+0.35), Spellbreaker +0.02 (+0.13), Spirit Resilience +0.02 (+0.12)
- **Vyper**: Indomitable +0.34 (+0.44), Debuff Reducer +0.06 (+0.10), Metal Skin +0.06 (+0.14)
- **Sinclair**: Indomitable +0.08 (+0.19), Spellbreaker +0.01 (+0.12), Debuff Reducer -0.00 (+0.03)
- **Mina**: Spirit Resilience +0.10 (+0.21), Divine Barrier +0.08 (+0.14), Witchmail +0.08 (+0.23)
- **Drifter**: Witchmail +0.08 (+0.23), Spirit Resilience +0.04 (+0.15), Dispel Magic +0.04 (+0.09)
- **Venator**: Bullet Resilience +0.09 (+0.15), Metal Skin +0.05 (+0.14), Plated Armor +0.03 (+0.13)
- **Victor**: Spellbreaker +0.04 (+0.15), Healbane +0.02 (+0.08), Spirit Resilience -0.01 (+0.10)
- **Paige**: Return Fire +0.01 (+0.06), Counterspell +0.01 (+0.05), Healbane -0.01 (+0.06)
- **The Doorman**: Spirit Resilience +0.15 (+0.26), Indomitable +0.14 (+0.25), Divine Barrier +0.10 (+0.16)
- **Billy**: Spirit Resilience +0.01 (+0.12), Spellbreaker -0.01 (+0.10), Counterspell -0.01 (+0.03)
- **Graves**: Witchmail +0.17 (+0.32), Spirit Resilience +0.12 (+0.23), Metal Skin +0.11 (+0.20)
- **Apollo**: Reactive Barrier +0.04 (+0.07), Indomitable +0.00 (+0.11), Unstoppable +0.00 (+0.08)
- **Deadman Danny**: Plated Armor +0.24 (+0.34), Spirit Resilience +0.20 (+0.30), Spellbreaker +0.17 (+0.28)
- **Rem**: Unstoppable +0.00 (+0.08), Counterspell -0.00 (+0.04), Witchmail -0.00 (+0.15)
- **Silver**: Dispel Magic +0.02 (+0.07), Return Fire +0.01 (+0.06), Metal Skin +0.00 (+0.08)
- **Celeste**: Witchmail +0.03 (+0.18), Spirit Resilience +0.02 (+0.12), Spellbreaker +0.01 (+0.12)
- **Rat King**: Return Fire -0.00 (+0.05), Bullet Resilience -0.00 (+0.05), Counterspell -0.01 (+0.03)
- **Solomon**: Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.03), Debuff Reducer -0.02 (+0.02)
- **Violet**: Witchmail +0.03 (+0.18), Return Fire +0.03 (+0.08), Divine Barrier +0.01 (+0.06)
- **Nurse Harrow**: Healbane -0.02 (+0.04), Dispel Magic -0.02 (+0.02), Counterspell -0.03 (+0.01)
- **Baba**: Healbane +0.02 (+0.08), Unstoppable +0.01 (+0.09), Debuff Reducer -0.00 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.203 | +0.064 | +0.119 | Deadman Danny +0.30, Lash +0.20, Wraith +0.14 | 14 heroes |
| Divine Barrier | 6,400 | +0.285 | +0.045 | +0.059 | Vindicta +0.14, Lash +0.13, Wraith +0.11 | 2 heroes |
| Dispel Magic | 3,200 | +0.123 | +0.038 | +0.063 | Mirage +0.27, Lash +0.25, Paradox +0.14 | 9 heroes |
| Witchmail | 6,400 | +0.208 | +0.033 | +0.162 | Deadman Danny +0.18, Lash +0.16, Paradox +0.12 | 1 heroes |
| Indomitable | 6,400 | +0.173 | +0.028 | +0.124 | Vyper +0.36, Wraith +0.30, Deadman Danny +0.19 | 0 heroes |
| Spellbreaker | 6,400 | +0.157 | +0.025 | +0.127 | Lash +0.26, Deadman Danny +0.21, Wraith +0.16 | 0 heroes |
| Debuff Reducer | 1,600 | +0.036 | +0.022 | +0.046 | Grey Talon +0.09, Vyper +0.07, Wraith +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | +0.023 | +0.015 | +0.037 | Deadman Danny +0.12, Wraith +0.10, The Doorman +0.08 | 5 heroes |
| Plated Armor | 6,400 | +0.035 | +0.005 | +0.115 | Deadman Danny +0.30, Wraith +0.16, Vindicta +0.11 | 0 heroes |
| Healbane | 1,600 | -0.004 | -0.003 | +0.063 | Yamato +0.06, Nurse Harrow +0.05, Vindicta +0.04 | 15 heroes |
| Bullet Resilience | 3,200 | -0.010 | -0.003 | +0.059 | Vindicta +0.14, Lady Geist +0.08, Venator +0.08 | 1 heroes |
| Unstoppable | 6,400 | -0.029 | -0.004 | +0.094 | Abrams +0.16, Paige +0.12, Grey Talon +0.12 | 3 heroes |
| Counterspell | 3,200 | -0.018 | -0.006 | +0.035 | Deadman Danny +0.06, Vindicta +0.04, The Doorman +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.107 | -0.033 | +0.099 | Wraith +0.26, Paradox +0.15, Lash +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.148 | -0.092 | +0.051 | Wraith +0.08, Vindicta +0.07, Paradox +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.17), Spellbreaker +0.10 (+0.22), Unstoppable +0.09 (+0.19)
- **Seven**: Witchmail +0.05 (+0.21), Healbane +0.00 (+0.07), Counterspell -0.00 (+0.03)
- **Vindicta**: Divine Barrier +0.14 (+0.20), Bullet Resilience +0.14 (+0.20), Plated Armor +0.11 (+0.23)
- **Lady Geist**: Bullet Resilience +0.08 (+0.14), Divine Barrier +0.07 (+0.13), Metal Skin +0.07 (+0.17)
- **Abrams**: Unstoppable +0.16 (+0.25), Dispel Magic +0.07 (+0.13), Healbane +0.04 (+0.10)
- **Wraith**: Indomitable +0.30 (+0.42), Metal Skin +0.26 (+0.36), Plated Armor +0.16 (+0.28)
- **McGinnis**: Counterspell -0.01 (+0.02), Healbane -0.02 (+0.05), Debuff Reducer -0.03 (+0.02)
- **Paradox**: Metal Skin +0.15 (+0.25), Dispel Magic +0.14 (+0.20), Witchmail +0.12 (+0.29)
- **Dynamo**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.02), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Counterspell -0.01 (+0.02), Healbane -0.02 (+0.05), Reactive Barrier -0.03 (+0.01)
- **Haze**: Indomitable +0.09 (+0.21), Unstoppable +0.08 (+0.18), Plated Armor +0.08 (+0.20)
- **Holliday**: Plated Armor +0.11 (+0.23), Return Fire +0.02 (+0.07), Debuff Reducer +0.02 (+0.06)
- **Bebop**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.02), Return Fire -0.03 (+0.03)
- **Calico**: Reactive Barrier +0.04 (+0.08), Spirit Resilience +0.03 (+0.15), Divine Barrier +0.03 (+0.08)
- **Grey Talon**: Spellbreaker +0.14 (+0.27), Unstoppable +0.12 (+0.21), Indomitable +0.11 (+0.24)
- **Mo & Krill**: Unstoppable +0.11 (+0.20), Spellbreaker +0.04 (+0.16), Dispel Magic +0.02 (+0.08)
- **Shiv**: Metal Skin +0.04 (+0.14), Bullet Resilience +0.03 (+0.09), Divine Barrier +0.03 (+0.09)
- **Ivy**: Unstoppable +0.10 (+0.19), Indomitable +0.04 (+0.17), Debuff Reducer +0.01 (+0.06)
- **Warden**: Return Fire +0.02 (+0.07), Healbane -0.00 (+0.06), Counterspell -0.00 (+0.03)
- **Yamato**: Healbane +0.06 (+0.12), Reactive Barrier +0.02 (+0.06), Counterspell +0.02 (+0.05)
- **Lash**: Spellbreaker +0.26 (+0.39), Dispel Magic +0.25 (+0.32), Spirit Resilience +0.20 (+0.32)
- **Viscous**: Healbane +0.01 (+0.08), Return Fire -0.00 (+0.05), Counterspell -0.02 (+0.02)
- **Pocket**: Spirit Resilience +0.02 (+0.14), Witchmail -0.01 (+0.15), Counterspell -0.01 (+0.02)
- **Mirage**: Dispel Magic +0.27 (+0.34), Metal Skin +0.02 (+0.12), Healbane +0.01 (+0.07)
- **Vyper**: Indomitable +0.36 (+0.49), Debuff Reducer +0.07 (+0.12), Unstoppable +0.05 (+0.15)
- **Sinclair**: Indomitable +0.15 (+0.28), Return Fire +0.01 (+0.06), Unstoppable +0.00 (+0.10)
- **Mina**: Spirit Resilience +0.12 (+0.24), Witchmail +0.09 (+0.25), Divine Barrier +0.08 (+0.14)
- **Drifter**: Spirit Resilience +0.10 (+0.21), Witchmail +0.06 (+0.23), Bullet Resilience +0.04 (+0.10)
- **Venator**: Bullet Resilience +0.08 (+0.14), Metal Skin +0.06 (+0.16), Plated Armor +0.00 (+0.12)
- **Victor**: Healbane +0.02 (+0.09), Spellbreaker +0.00 (+0.13), Spirit Resilience -0.01 (+0.11)
- **Paige**: Unstoppable +0.12 (+0.22), Debuff Reducer +0.05 (+0.10), Counterspell -0.00 (+0.03)
- **The Doorman**: Spirit Resilience +0.13 (+0.25), Indomitable +0.12 (+0.24), Witchmail +0.10 (+0.26)
- **Billy**: Reactive Barrier +0.01 (+0.04), Healbane +0.01 (+0.07), Counterspell +0.00 (+0.04)
- **Graves**: Witchmail +0.05 (+0.22), Return Fire +0.03 (+0.08), Metal Skin +0.03 (+0.13)
- **Apollo**: Counterspell +0.01 (+0.05), Healbane +0.00 (+0.06), Divine Barrier -0.00 (+0.06)
- **Deadman Danny**: Plated Armor +0.30 (+0.42), Spirit Resilience +0.30 (+0.42), Spellbreaker +0.21 (+0.33)
- **Rem**: Unstoppable +0.06 (+0.15), Debuff Reducer +0.05 (+0.10), Counterspell -0.01 (+0.03)
- **Silver**: Dispel Magic +0.08 (+0.14), Metal Skin +0.04 (+0.14), Reactive Barrier +0.03 (+0.07)
- **Celeste**: Witchmail +0.06 (+0.22), Dispel Magic +0.04 (+0.11), Spellbreaker +0.03 (+0.15)
- **Rat King**: Return Fire -0.01 (+0.04), Counterspell -0.01 (+0.02), Bullet Resilience -0.02 (+0.04)
- **Solomon**: Return Fire +0.00 (+0.05), Reactive Barrier -0.00 (+0.04), Counterspell -0.00 (+0.03)
- **Violet**: Witchmail +0.07 (+0.23), Return Fire +0.05 (+0.10), Spirit Resilience +0.04 (+0.16)
- **Nurse Harrow**: Healbane +0.05 (+0.11), Counterspell +0.01 (+0.04), Divine Barrier -0.02 (+0.04)
- **Baba**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03), Unstoppable -0.01 (+0.08)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.229 | +0.072 | +0.123 | Lash +0.33, Deadman Danny +0.31, The Doorman +0.29 | 15 heroes |
| Dispel Magic | 3,200 | +0.114 | +0.035 | +0.058 | Mirage +0.26, Silver +0.23, Lash +0.17 | 9 heroes |
| Indomitable | 6,400 | +0.199 | +0.032 | +0.144 | Vyper +0.26, Wraith +0.26, The Doorman +0.22 | 1 heroes |
| Witchmail | 6,400 | +0.184 | +0.029 | +0.141 | Lash +0.19, The Doorman +0.18, Deadman Danny +0.11 | 2 heroes |
| Spellbreaker | 6,400 | +0.166 | +0.026 | +0.128 | Lash +0.27, Deadman Danny +0.20, The Doorman +0.17 | 0 heroes |
| Divine Barrier | 6,400 | +0.165 | +0.026 | +0.051 | Vindicta +0.17, Lash +0.16, The Doorman +0.16 | 3 heroes |
| Debuff Reducer | 1,600 | +0.024 | +0.015 | +0.041 | Grey Talon +0.09, The Doorman +0.08, Rem +0.08 | 0 heroes |
| Plated Armor | 6,400 | +0.009 | +0.002 | +0.097 | Vindicta +0.19, Deadman Danny +0.17, Vyper +0.13 | 2 heroes |
| Unstoppable | 6,400 | -0.009 | -0.001 | +0.113 | Haze +0.29, Infernus +0.24, Paradox +0.18 | 8 heroes |
| Reactive Barrier | 1,600 | -0.002 | -0.002 | +0.034 | Calico +0.11, Drifter +0.09, The Doorman +0.08 | 3 heroes |
| Bullet Resilience | 3,200 | -0.026 | -0.008 | +0.053 | Vindicta +0.11, Venator +0.09, Lash +0.08 | 0 heroes |
| Healbane | 1,600 | -0.013 | -0.008 | +0.054 | Celeste +0.07, Lady Geist +0.04, Nurse Harrow +0.04 | 14 heroes |
| Counterspell | 3,200 | -0.030 | -0.009 | +0.028 | The Doorman +0.08, Calico +0.02, Nurse Harrow +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.104 | -0.032 | +0.106 | Silver +0.20, Lash +0.20, Venator +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.153 | -0.096 | +0.048 | The Doorman +0.06, Wraith +0.05, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.24 (+0.35), Dispel Magic +0.06 (+0.12), Indomitable +0.05 (+0.20)
- **Seven**: Witchmail +0.07 (+0.21), Dispel Magic +0.01 (+0.07), Spirit Resilience +0.00 (+0.12)
- **Vindicta**: Plated Armor +0.19 (+0.29), Divine Barrier +0.17 (+0.22), Bullet Resilience +0.11 (+0.16)
- **Lady Geist**: Bullet Resilience +0.05 (+0.10), Healbane +0.04 (+0.10), Metal Skin +0.04 (+0.14)
- **Abrams**: Unstoppable +0.11 (+0.22), Spellbreaker +0.06 (+0.19), Indomitable +0.06 (+0.20)
- **Wraith**: Indomitable +0.26 (+0.40), Metal Skin +0.13 (+0.24), Return Fire +0.05 (+0.10)
- **McGinnis**: Spirit Resilience +0.01 (+0.13), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.04)
- **Paradox**: Unstoppable +0.18 (+0.29), Witchmail +0.10 (+0.24), Dispel Magic +0.09 (+0.15)
- **Dynamo**: Healbane +0.02 (+0.07), Counterspell +0.00 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.14 (+0.26), Witchmail +0.04 (+0.18), Spellbreaker +0.03 (+0.16)
- **Haze**: Unstoppable +0.29 (+0.40), Indomitable +0.10 (+0.24), Plated Armor +0.08 (+0.18)
- **Holliday**: Spellbreaker +0.06 (+0.19), Debuff Reducer +0.04 (+0.08), Reactive Barrier +0.03 (+0.06)
- **Bebop**: Debuff Reducer +0.05 (+0.09), Spellbreaker +0.01 (+0.14), Healbane +0.00 (+0.06)
- **Calico**: Spirit Resilience +0.15 (+0.28), Divine Barrier +0.13 (+0.18), Reactive Barrier +0.11 (+0.15)
- **Grey Talon**: Unstoppable +0.17 (+0.29), Spellbreaker +0.17 (+0.29), Spirit Resilience +0.13 (+0.25)
- **Mo & Krill**: Unstoppable +0.07 (+0.18), Healbane +0.03 (+0.08), Debuff Reducer +0.02 (+0.06)
- **Shiv**: Metal Skin +0.04 (+0.15), Bullet Resilience +0.03 (+0.08), Divine Barrier +0.02 (+0.07)
- **Ivy**: Unstoppable +0.14 (+0.26), Indomitable +0.09 (+0.24), Debuff Reducer +0.04 (+0.08)
- **Warden**: Plated Armor +0.02 (+0.12), Healbane +0.02 (+0.08), Bullet Resilience +0.02 (+0.07)
- **Yamato**: Healbane +0.03 (+0.08), Reactive Barrier +0.01 (+0.04), Debuff Reducer +0.01 (+0.05)
- **Lash**: Spirit Resilience +0.33 (+0.46), Spellbreaker +0.27 (+0.40), Metal Skin +0.20 (+0.30)
- **Viscous**: Divine Barrier +0.01 (+0.06), Counterspell +0.00 (+0.03), Healbane -0.00 (+0.05)
- **Pocket**: Spirit Resilience +0.12 (+0.24), Witchmail +0.05 (+0.19), Return Fire +0.03 (+0.07)
- **Mirage**: Dispel Magic +0.26 (+0.32), Metal Skin +0.07 (+0.18), Plated Armor +0.02 (+0.11)
- **Vyper**: Indomitable +0.26 (+0.40), Plated Armor +0.13 (+0.22), Metal Skin +0.07 (+0.17)
- **Sinclair**: Indomitable +0.13 (+0.27), Spellbreaker +0.06 (+0.19), Reactive Barrier +0.02 (+0.05)
- **Mina**: Divine Barrier +0.02 (+0.07), Witchmail +0.00 (+0.14), Counterspell -0.00 (+0.03)
- **Drifter**: Indomitable +0.20 (+0.35), Spirit Resilience +0.19 (+0.31), Spellbreaker +0.11 (+0.24)
- **Venator**: Metal Skin +0.13 (+0.24), Bullet Resilience +0.09 (+0.14), Plated Armor +0.01 (+0.11)
- **Victor**: Spellbreaker +0.13 (+0.26), Spirit Resilience +0.07 (+0.19), Healbane +0.03 (+0.09)
- **Paige**: Counterspell +0.01 (+0.04), Return Fire +0.00 (+0.05), Healbane -0.00 (+0.05)
- **The Doorman**: Spirit Resilience +0.29 (+0.41), Indomitable +0.22 (+0.36), Witchmail +0.18 (+0.32)
- **Billy**: Healbane -0.00 (+0.05), Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (+0.02)
- **Graves**: Return Fire +0.01 (+0.06), Reactive Barrier -0.01 (+0.03), Counterspell -0.01 (+0.01)
- **Apollo**: Healbane +0.01 (+0.07), Reactive Barrier -0.01 (+0.03), Divine Barrier -0.01 (+0.04)
- **Deadman Danny**: Spirit Resilience +0.31 (+0.44), Spellbreaker +0.20 (+0.32), Plated Armor +0.17 (+0.27)
- **Rem**: Debuff Reducer +0.08 (+0.12), Spellbreaker +0.04 (+0.17), Unstoppable +0.00 (+0.12)
- **Silver**: Dispel Magic +0.23 (+0.29), Metal Skin +0.20 (+0.31), Indomitable +0.17 (+0.32)
- **Celeste**: Spirit Resilience +0.10 (+0.22), Witchmail +0.09 (+0.23), Healbane +0.07 (+0.12)
- **Rat King**: Counterspell -0.01 (+0.02), Return Fire -0.01 (+0.04), Healbane -0.01 (+0.04)
- **Solomon**: Reactive Barrier +0.01 (+0.05), Counterspell +0.01 (+0.03), Return Fire -0.01 (+0.04)
- **Violet**: Witchmail +0.02 (+0.17), Return Fire +0.02 (+0.07), Counterspell +0.01 (+0.04)
- **Nurse Harrow**: Spirit Resilience +0.10 (+0.22), Dispel Magic +0.09 (+0.15), Healbane +0.04 (+0.10)
- **Baba**: Healbane +0.00 (+0.06), Counterspell +0.00 (+0.03), Debuff Reducer -0.02 (+0.02)
