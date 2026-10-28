# Counter items in the sim (phantom and up)

Built 2026-10-28T19:40:59Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.364 | +0.058 | +0.092 | Lash +0.17, Calico +0.12, Wraith +0.12 | 0 heroes |
| Spirit Resilience | 3,200 | +0.185 | +0.058 | +0.115 | Deadman Danny +0.24, Lash +0.23, Graves +0.12 | 1 heroes |
| Reactive Barrier | 1,600 | +0.047 | +0.030 | +0.059 | Deadman Danny +0.19, Calico +0.14, Paradox +0.11 | 3 heroes |
| Dispel Magic | 3,200 | +0.096 | +0.030 | +0.073 | Mirage +0.37, Deadman Danny +0.16, Infernus +0.13 | 4 heroes |
| Indomitable | 6,400 | +0.158 | +0.025 | +0.139 | Deadman Danny +0.28, Vyper +0.24, Abrams +0.20 | 0 heroes |
| Witchmail | 6,400 | +0.145 | +0.023 | +0.194 | Deadman Danny +0.26, Lash +0.18, Wraith +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.070 | Deadman Danny +0.13, Wraith +0.10, Vyper +0.10 | 0 heroes |
| Spellbreaker | 6,400 | +0.086 | +0.013 | +0.152 | Deadman Danny +0.29, Lash +0.21, Mo & Krill +0.14 | 0 heroes |
| Bullet Resilience | 3,200 | -0.007 | -0.002 | +0.081 | Deadman Danny +0.18, Venator +0.16, Paradox +0.14 | 0 heroes |
| Plated Armor | 6,400 | -0.043 | -0.007 | +0.116 | Deadman Danny +0.23, Holliday +0.21, Wraith +0.13 | 0 heroes |
| Healbane | 1,600 | -0.012 | -0.007 | +0.083 | Deadman Danny +0.07, Billy +0.04, Bebop +0.04 | 11 heroes |
| Counterspell | 3,200 | -0.026 | -0.008 | +0.068 | Deadman Danny +0.15, Wraith +0.05, Paradox +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.060 | -0.009 | +0.124 | Deadman Danny +0.21, Holliday +0.11, Abrams +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.165 | -0.052 | +0.093 | Wraith +0.16, Lash +0.15, Paradox +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.178 | -0.111 | +0.071 | Deadman Danny +0.11, Paradox +0.06, Wraith +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.13 (+0.20), Spellbreaker +0.09 (+0.24), Unstoppable +0.06 (+0.19)
- **Seven**: Healbane -0.01 (+0.07), Counterspell -0.02 (+0.04), Reactive Barrier -0.03 (+0.03)
- **Vindicta**: Return Fire +0.02 (+0.09), Witchmail +0.00 (+0.20), Divine Barrier -0.01 (+0.08)
- **Lady Geist**: Return Fire -0.01 (+0.06), Healbane -0.01 (+0.07), Counterspell -0.04 (+0.03)
- **Abrams**: Indomitable +0.20 (+0.34), Unstoppable +0.10 (+0.23), Spirit Resilience +0.09 (+0.20)
- **Wraith**: Indomitable +0.19 (+0.33), Metal Skin +0.16 (+0.25), Plated Armor +0.13 (+0.25)
- **McGinnis**: Spirit Resilience -0.00 (+0.11), Healbane -0.01 (+0.07), Return Fire -0.01 (+0.06)
- **Paradox**: Metal Skin +0.15 (+0.24), Bullet Resilience +0.14 (+0.22), Plated Armor +0.12 (+0.23)
- **Dynamo**: Healbane -0.01 (+0.08), Counterspell -0.03 (+0.04), Reactive Barrier -0.05 (+0.01)
- **Kelvin**: Healbane +0.00 (+0.08), Counterspell -0.01 (+0.06), Witchmail -0.02 (+0.17)
- **Haze**: Indomitable +0.10 (+0.24), Unstoppable +0.07 (+0.20), Plated Armor +0.04 (+0.16)
- **Holliday**: Plated Armor +0.21 (+0.33), Spellbreaker +0.13 (+0.29), Unstoppable +0.11 (+0.23)
- **Bebop**: Healbane +0.04 (+0.12), Counterspell +0.01 (+0.08), Return Fire +0.01 (+0.08)
- **Calico**: Reactive Barrier +0.14 (+0.19), Divine Barrier +0.12 (+0.21), Spellbreaker +0.11 (+0.26)
- **Grey Talon**: Unstoppable +0.07 (+0.19), Debuff Reducer +0.05 (+0.12), Spellbreaker +0.05 (+0.20)
- **Mo & Krill**: Spellbreaker +0.14 (+0.29), Spirit Resilience +0.09 (+0.20), Dispel Magic +0.08 (+0.15)
- **Shiv**: Healbane -0.02 (+0.07), Divine Barrier -0.02 (+0.07), Return Fire -0.02 (+0.05)
- **Ivy**: Indomitable +0.09 (+0.23), Unstoppable +0.06 (+0.19), Metal Skin +0.01 (+0.10)
- **Warden**: Return Fire +0.02 (+0.09), Debuff Reducer +0.01 (+0.08), Counterspell -0.00 (+0.07)
- **Yamato**: Healbane +0.03 (+0.12), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.05)
- **Lash**: Spirit Resilience +0.23 (+0.34), Spellbreaker +0.21 (+0.36), Witchmail +0.18 (+0.37)
- **Viscous**: Healbane -0.01 (+0.07), Return Fire -0.01 (+0.06), Divine Barrier -0.02 (+0.07)
- **Pocket**: Spirit Resilience +0.04 (+0.16), Witchmail +0.04 (+0.24), Return Fire +0.03 (+0.10)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spirit Resilience +0.11 (+0.23), Spellbreaker +0.11 (+0.26)
- **Vyper**: Indomitable +0.24 (+0.38), Debuff Reducer +0.10 (+0.17), Unstoppable +0.07 (+0.20)
- **Sinclair**: Indomitable +0.14 (+0.28), Spellbreaker +0.08 (+0.24), Unstoppable +0.02 (+0.15)
- **Mina**: Return Fire +0.02 (+0.09), Spirit Resilience -0.00 (+0.11), Counterspell -0.01 (+0.06)
- **Drifter**: Counterspell -0.01 (+0.06), Return Fire -0.01 (+0.06), Debuff Reducer -0.01 (+0.06)
- **Venator**: Bullet Resilience +0.16 (+0.24), Divine Barrier +0.09 (+0.18), Debuff Reducer +0.07 (+0.14)
- **Victor**: Healbane +0.02 (+0.10), Spirit Resilience +0.00 (+0.12), Dispel Magic -0.01 (+0.06)
- **Paige**: Return Fire +0.00 (+0.07), Counterspell -0.01 (+0.06), Healbane -0.03 (+0.06)
- **The Doorman**: Indomitable +0.10 (+0.24), Witchmail +0.09 (+0.29), Spirit Resilience +0.09 (+0.20)
- **Billy**: Spellbreaker +0.09 (+0.24), Healbane +0.04 (+0.12), Spirit Resilience +0.04 (+0.15)
- **Graves**: Metal Skin +0.14 (+0.23), Spirit Resilience +0.12 (+0.23), Witchmail +0.11 (+0.31)
- **Apollo**: Reactive Barrier -0.00 (+0.06), Unstoppable -0.01 (+0.11), Indomitable -0.02 (+0.12)
- **Deadman Danny**: Spellbreaker +0.29 (+0.44), Indomitable +0.28 (+0.42), Witchmail +0.26 (+0.45)
- **Rem**: Debuff Reducer +0.09 (+0.16), Unstoppable +0.07 (+0.19), Spellbreaker +0.02 (+0.17)
- **Silver**: Dispel Magic +0.04 (+0.11), Debuff Reducer +0.04 (+0.11), Metal Skin +0.02 (+0.11)
- **Celeste**: Spirit Resilience +0.07 (+0.18), Witchmail +0.06 (+0.26), Dispel Magic +0.03 (+0.11)
- **Rat King**: Counterspell -0.01 (+0.06), Return Fire -0.01 (+0.06), Bullet Resilience -0.01 (+0.07)
- **Solomon**: Return Fire -0.00 (+0.07), Counterspell -0.02 (+0.04), Healbane -0.04 (+0.05)
- **Violet**: Return Fire -0.00 (+0.07), Healbane -0.02 (+0.07), Counterspell -0.04 (+0.03)
- **Nurse Harrow**: Healbane +0.01 (+0.09), Counterspell -0.05 (+0.02), Return Fire -0.05 (+0.02)
- **Baba**: Healbane -0.00 (+0.08), Debuff Reducer -0.02 (+0.05), Unstoppable -0.02 (+0.10)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.161 | +0.050 | +0.101 | Lash +0.35, Pocket +0.18, Graves +0.18 | 9 heroes |
| Divine Barrier | 6,400 | +0.296 | +0.047 | +0.064 | Lash +0.20, Paradox +0.09, Graves +0.08 | 1 heroes |
| Dispel Magic | 3,200 | +0.086 | +0.027 | +0.052 | Mirage +0.29, Infernus +0.11, Deadman Danny +0.10 | 6 heroes |
| Witchmail | 6,400 | +0.143 | +0.022 | +0.157 | Lash +0.19, Deadman Danny +0.14, Graves +0.14 | 0 heroes |
| Indomitable | 6,400 | +0.137 | +0.022 | +0.104 | Vyper +0.39, Wraith +0.19, Deadman Danny +0.17 | 0 heroes |
| Spellbreaker | 6,400 | +0.102 | +0.016 | +0.124 | Lash +0.35, Vyper +0.17, Deadman Danny +0.12 | 0 heroes |
| Reactive Barrier | 1,600 | +0.025 | +0.016 | +0.034 | Vyper +0.10, Paradox +0.09, Graves +0.07 | 4 heroes |
| Debuff Reducer | 1,600 | +0.004 | +0.002 | +0.050 | Wraith +0.10, Vyper +0.10, Holliday +0.07 | 1 heroes |
| Plated Armor | 6,400 | -0.041 | -0.006 | +0.084 | Holliday +0.14, Graves +0.12, Paradox +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | -0.035 | -0.011 | +0.056 | Venator +0.12, Paradox +0.09, Deadman Danny +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.037 | -0.011 | +0.045 | Deadman Danny +0.08, Vindicta +0.04, McGinnis +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.084 | -0.013 | +0.095 | Abrams +0.17, Deadman Danny +0.11, Vyper +0.10 | 0 heroes |
| Healbane | 1,600 | -0.039 | -0.024 | +0.064 | Bebop +0.05, Abrams +0.04, Yamato +0.04 | 17 heroes |
| Metal Skin | 3,200 | -0.183 | -0.057 | +0.071 | Graves +0.16, Wraith +0.12, Lash +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.185 | -0.115 | +0.050 | Paradox +0.06, Graves +0.05, Wraith +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.16), Spellbreaker +0.07 (+0.20), Unstoppable +0.05 (+0.15)
- **Seven**: Witchmail +0.03 (+0.19), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Witchmail +0.06 (+0.22), Counterspell +0.04 (+0.08), Divine Barrier +0.03 (+0.10)
- **Lady Geist**: Return Fire +0.04 (+0.09), Metal Skin +0.02 (+0.09), Divine Barrier +0.01 (+0.07)
- **Abrams**: Unstoppable +0.17 (+0.27), Indomitable +0.10 (+0.21), Divine Barrier +0.06 (+0.13)
- **Wraith**: Indomitable +0.19 (+0.29), Metal Skin +0.12 (+0.19), Debuff Reducer +0.10 (+0.15)
- **McGinnis**: Spirit Resilience +0.06 (+0.16), Dispel Magic +0.04 (+0.09), Counterspell +0.03 (+0.08)
- **Paradox**: Plated Armor +0.09 (+0.18), Bullet Resilience +0.09 (+0.15), Metal Skin +0.09 (+0.16)
- **Dynamo**: Healbane -0.00 (+0.06), Counterspell -0.02 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.07 (+0.17), Dispel Magic +0.06 (+0.11), Spellbreaker +0.03 (+0.16)
- **Haze**: Indomitable +0.08 (+0.19), Plated Armor +0.07 (+0.15), Unstoppable +0.05 (+0.14)
- **Holliday**: Plated Armor +0.14 (+0.23), Debuff Reducer +0.07 (+0.12), Spellbreaker +0.06 (+0.18)
- **Bebop**: Healbane +0.05 (+0.12), Metal Skin +0.00 (+0.07), Counterspell -0.00 (+0.04)
- **Calico**: Reactive Barrier +0.05 (+0.09), Divine Barrier +0.05 (+0.11), Dispel Magic +0.02 (+0.07)
- **Grey Talon**: Unstoppable +0.06 (+0.16), Spellbreaker +0.06 (+0.18), Debuff Reducer +0.06 (+0.11)
- **Mo & Krill**: Spellbreaker +0.10 (+0.22), Unstoppable +0.07 (+0.17), Dispel Magic +0.06 (+0.11)
- **Shiv**: Divine Barrier +0.03 (+0.10), Bullet Resilience +0.03 (+0.09), Metal Skin +0.02 (+0.09)
- **Ivy**: Unstoppable +0.07 (+0.17), Indomitable +0.07 (+0.17), Debuff Reducer +0.03 (+0.08)
- **Warden**: Return Fire +0.03 (+0.08), Witchmail +0.01 (+0.17), Plated Armor +0.01 (+0.09)
- **Yamato**: Healbane +0.04 (+0.11), Counterspell -0.00 (+0.04), Debuff Reducer -0.02 (+0.03)
- **Lash**: Spirit Resilience +0.35 (+0.45), Spellbreaker +0.35 (+0.47), Divine Barrier +0.20 (+0.27)
- **Viscous**: Divine Barrier +0.00 (+0.07), Return Fire +0.00 (+0.05), Counterspell -0.01 (+0.04)
- **Pocket**: Spirit Resilience +0.18 (+0.28), Spellbreaker +0.09 (+0.21), Witchmail +0.09 (+0.24)
- **Mirage**: Dispel Magic +0.29 (+0.34), Spirit Resilience +0.08 (+0.18), Spellbreaker +0.07 (+0.20)
- **Vyper**: Indomitable +0.39 (+0.49), Spellbreaker +0.17 (+0.29), Debuff Reducer +0.10 (+0.15)
- **Sinclair**: Indomitable +0.08 (+0.19), Spellbreaker +0.05 (+0.18), Unstoppable +0.04 (+0.14)
- **Mina**: Divine Barrier +0.04 (+0.10), Counterspell +0.03 (+0.07), Spirit Resilience +0.03 (+0.13)
- **Drifter**: Return Fire -0.01 (+0.04), Healbane -0.01 (+0.06), Counterspell -0.01 (+0.04)
- **Venator**: Bullet Resilience +0.12 (+0.18), Metal Skin +0.12 (+0.19), Plated Armor +0.06 (+0.14)
- **Victor**: Spirit Resilience +0.06 (+0.16), Spellbreaker +0.05 (+0.17), Healbane -0.01 (+0.05)
- **Paige**: Counterspell -0.00 (+0.04), Return Fire -0.00 (+0.05), Healbane -0.01 (+0.06)
- **The Doorman**: Indomitable +0.08 (+0.18), Reactive Barrier +0.07 (+0.10), Spirit Resilience +0.07 (+0.17)
- **Billy**: Spirit Resilience +0.04 (+0.14), Healbane +0.03 (+0.09), Counterspell +0.03 (+0.07)
- **Graves**: Spirit Resilience +0.18 (+0.28), Metal Skin +0.16 (+0.23), Witchmail +0.14 (+0.29)
- **Apollo**: Reactive Barrier +0.02 (+0.05), Healbane -0.01 (+0.06), Debuff Reducer -0.02 (+0.03)
- **Deadman Danny**: Indomitable +0.17 (+0.27), Spirit Resilience +0.15 (+0.25), Witchmail +0.14 (+0.30)
- **Rem**: Debuff Reducer -0.01 (+0.04), Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Silver**: Dispel Magic +0.07 (+0.12), Reactive Barrier +0.05 (+0.09), Indomitable +0.03 (+0.14)
- **Celeste**: Spirit Resilience +0.07 (+0.17), Witchmail +0.05 (+0.20), Spellbreaker +0.00 (+0.13)
- **Rat King**: Return Fire -0.00 (+0.05), Bullet Resilience -0.01 (+0.05), Metal Skin -0.01 (+0.06)
- **Solomon**: Return Fire +0.02 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Violet**: Healbane +0.02 (+0.08), Return Fire +0.02 (+0.07), Counterspell -0.02 (+0.03)
- **Nurse Harrow**: Healbane +0.02 (+0.09), Reactive Barrier -0.02 (+0.01), Return Fire -0.03 (+0.03)
- **Baba**: Unstoppable +0.05 (+0.15), Debuff Reducer +0.02 (+0.07), Healbane +0.01 (+0.07)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.147 | +0.046 | +0.099 | The Doorman +0.18, Lash +0.16, Mo & Krill +0.16 | 14 heroes |
| Divine Barrier | 6,400 | +0.254 | +0.040 | +0.050 | The Doorman +0.10, Lash +0.09, Mo & Krill +0.07 | 2 heroes |
| Dispel Magic | 3,200 | +0.088 | +0.027 | +0.046 | Mirage +0.26, Infernus +0.18, Mo & Krill +0.11 | 9 heroes |
| Indomitable | 6,400 | +0.144 | +0.023 | +0.114 | Vyper +0.32, Sinclair +0.27, Wraith +0.22 | 0 heroes |
| Witchmail | 6,400 | +0.134 | +0.021 | +0.156 | Lash +0.15, The Doorman +0.12, Mo & Krill +0.11 | 1 heroes |
| Spellbreaker | 6,400 | +0.114 | +0.018 | +0.130 | Grey Talon +0.23, Lash +0.19, Infernus +0.16 | 0 heroes |
| Debuff Reducer | 1,600 | +0.008 | +0.005 | +0.062 | Grey Talon +0.20, Paige +0.16, Holliday +0.10 | 0 heroes |
| Reactive Barrier | 1,600 | +0.002 | +0.001 | +0.034 | Yamato +0.11, Wraith +0.08, Mo & Krill +0.08 | 4 heroes |
| Plated Armor | 6,400 | -0.040 | -0.006 | +0.084 | Yamato +0.13, Wraith +0.09, Grey Talon +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.079 | -0.012 | +0.101 | Grey Talon +0.23, Paige +0.20, Abrams +0.10 | 3 heroes |
| Counterspell | 3,200 | -0.043 | -0.013 | +0.034 | Yamato +0.07, McGinnis +0.04, Vindicta +0.03 | 1 heroes |
| Bullet Resilience | 3,200 | -0.050 | -0.015 | +0.049 | Venator +0.10, Vindicta +0.07, Yamato +0.06 | 1 heroes |
| Healbane | 1,600 | -0.042 | -0.026 | +0.058 | Yamato +0.10, Mo & Krill +0.05, Infernus +0.05 | 16 heroes |
| Metal Skin | 3,200 | -0.180 | -0.056 | +0.073 | Wraith +0.15, Venator +0.13, Grey Talon +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.182 | -0.114 | +0.042 | Vindicta +0.07, Paradox +0.05, Graves +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.18 (+0.23), Spellbreaker +0.16 (+0.29), Unstoppable +0.09 (+0.19)
- **Seven**: Witchmail +0.01 (+0.16), Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05)
- **Vindicta**: Divine Barrier +0.07 (+0.12), Return Fire +0.07 (+0.11), Bullet Resilience +0.07 (+0.11)
- **Lady Geist**: Bullet Resilience +0.04 (+0.09), Return Fire +0.04 (+0.08), Healbane +0.03 (+0.09)
- **Abrams**: Unstoppable +0.10 (+0.20), Spirit Resilience +0.05 (+0.15), Dispel Magic +0.03 (+0.08)
- **Wraith**: Indomitable +0.22 (+0.33), Metal Skin +0.15 (+0.23), Spellbreaker +0.11 (+0.24)
- **McGinnis**: Spirit Resilience +0.09 (+0.19), Witchmail +0.06 (+0.22), Dispel Magic +0.05 (+0.10)
- **Paradox**: Witchmail +0.08 (+0.24), Indomitable +0.06 (+0.18), Dispel Magic +0.06 (+0.11)
- **Dynamo**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03), Return Fire -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.06 (+0.16), Counterspell +0.03 (+0.06), Healbane +0.01 (+0.07)
- **Haze**: Plated Armor +0.05 (+0.14), Bullet Resilience +0.04 (+0.09), Indomitable +0.04 (+0.15)
- **Holliday**: Spellbreaker +0.12 (+0.25), Debuff Reducer +0.10 (+0.16), Unstoppable +0.08 (+0.18)
- **Bebop**: Healbane +0.03 (+0.09), Return Fire -0.02 (+0.03), Counterspell -0.02 (+0.02)
- **Calico**: Spirit Resilience +0.05 (+0.14), Reactive Barrier +0.03 (+0.06), Divine Barrier +0.02 (+0.07)
- **Grey Talon**: Spellbreaker +0.23 (+0.36), Unstoppable +0.23 (+0.33), Debuff Reducer +0.20 (+0.26)
- **Mo & Krill**: Spellbreaker +0.16 (+0.29), Spirit Resilience +0.16 (+0.25), Dispel Magic +0.11 (+0.16)
- **Shiv**: Metal Skin +0.07 (+0.14), Bullet Resilience +0.05 (+0.10), Divine Barrier +0.05 (+0.10)
- **Ivy**: Unstoppable +0.05 (+0.15), Indomitable +0.02 (+0.14), Healbane +0.01 (+0.07)
- **Warden**: Debuff Reducer +0.03 (+0.09), Spellbreaker +0.02 (+0.15), Return Fire +0.02 (+0.06)
- **Yamato**: Indomitable +0.17 (+0.29), Plated Armor +0.13 (+0.22), Reactive Barrier +0.11 (+0.14)
- **Lash**: Spellbreaker +0.19 (+0.32), Spirit Resilience +0.16 (+0.26), Witchmail +0.15 (+0.31)
- **Viscous**: Divine Barrier +0.06 (+0.11), Return Fire +0.04 (+0.08), Metal Skin +0.01 (+0.09)
- **Pocket**: Spirit Resilience +0.10 (+0.20), Witchmail +0.03 (+0.18), Spellbreaker +0.03 (+0.16)
- **Mirage**: Dispel Magic +0.26 (+0.31), Spirit Resilience +0.05 (+0.15), Plated Armor +0.03 (+0.12)
- **Vyper**: Indomitable +0.32 (+0.44), Spellbreaker +0.10 (+0.23), Debuff Reducer +0.09 (+0.15)
- **Sinclair**: Indomitable +0.27 (+0.39), Spellbreaker +0.11 (+0.24), Unstoppable +0.09 (+0.19)
- **Mina**: Witchmail +0.02 (+0.18), Divine Barrier +0.02 (+0.07), Return Fire +0.01 (+0.06)
- **Drifter**: Witchmail +0.03 (+0.19), Healbane +0.02 (+0.08), Counterspell +0.00 (+0.04)
- **Venator**: Metal Skin +0.13 (+0.20), Bullet Resilience +0.10 (+0.15), Plated Armor +0.06 (+0.14)
- **Victor**: Spirit Resilience +0.03 (+0.13), Healbane +0.01 (+0.07), Dispel Magic +0.00 (+0.05)
- **Paige**: Unstoppable +0.20 (+0.30), Debuff Reducer +0.16 (+0.22), Spellbreaker +0.09 (+0.22)
- **The Doorman**: Spirit Resilience +0.18 (+0.28), Indomitable +0.14 (+0.25), Witchmail +0.12 (+0.28)
- **Billy**: Indomitable +0.05 (+0.17), Spirit Resilience +0.04 (+0.14), Spellbreaker +0.03 (+0.16)
- **Graves**: Return Fire +0.04 (+0.08), Metal Skin +0.03 (+0.10), Witchmail +0.01 (+0.17)
- **Apollo**: Healbane +0.03 (+0.09), Reactive Barrier +0.01 (+0.04), Counterspell -0.00 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.10 (+0.20), Indomitable +0.10 (+0.22), Witchmail +0.06 (+0.22)
- **Rem**: Debuff Reducer +0.09 (+0.15), Unstoppable +0.07 (+0.17), Spellbreaker +0.03 (+0.16)
- **Silver**: Dispel Magic +0.04 (+0.09), Reactive Barrier +0.02 (+0.05), Return Fire -0.01 (+0.04)
- **Celeste**: Dispel Magic +0.03 (+0.07), Witchmail +0.01 (+0.17), Reactive Barrier -0.00 (+0.03)
- **Rat King**: Return Fire +0.00 (+0.04), Plated Armor +0.00 (+0.09), Bullet Resilience +0.00 (+0.05)
- **Solomon**: Reactive Barrier -0.00 (+0.03), Counterspell -0.00 (+0.03), Healbane -0.00 (+0.05)
- **Violet**: Return Fire +0.02 (+0.06), Healbane +0.02 (+0.07), Witchmail -0.00 (+0.16)
- **Nurse Harrow**: Healbane +0.04 (+0.10), Counterspell +0.02 (+0.05), Divine Barrier -0.00 (+0.04)
- **Baba**: Unstoppable +0.03 (+0.13), Healbane +0.01 (+0.06), Counterspell -0.01 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.183 | +0.057 | +0.143 | Lash +0.45, Deadman Danny +0.42, The Doorman +0.39 | 15 heroes |
| Divine Barrier | 6,400 | +0.219 | +0.034 | +0.053 | Lash +0.23, The Doorman +0.22, Viscous +0.20 | 3 heroes |
| Dispel Magic | 3,200 | +0.093 | +0.029 | +0.049 | Mirage +0.27, Lash +0.20, Silver +0.15 | 9 heroes |
| Indomitable | 6,400 | +0.167 | +0.027 | +0.151 | Wraith +0.32, Sinclair +0.28, Deadman Danny +0.26 | 1 heroes |
| Spellbreaker | 6,400 | +0.153 | +0.024 | +0.193 | Grey Talon +0.35, Deadman Danny +0.31, Lash +0.28 | 0 heroes |
| Witchmail | 6,400 | +0.134 | +0.021 | +0.163 | Deadman Danny +0.34, The Doorman +0.30, Lash +0.22 | 2 heroes |
| Debuff Reducer | 1,600 | +0.013 | +0.008 | +0.091 | Grey Talon +0.20, Holliday +0.18, Paige +0.17 | 0 heroes |
| Plated Armor | 6,400 | -0.043 | -0.007 | +0.093 | Holliday +0.23, Grey Talon +0.17, Wraith +0.09 | 2 heroes |
| Reactive Barrier | 1,600 | -0.012 | -0.008 | +0.033 | The Doorman +0.15, Yamato +0.12, Sinclair +0.11 | 3 heroes |
| Unstoppable | 6,400 | -0.059 | -0.009 | +0.151 | Grey Talon +0.30, Paige +0.24, Haze +0.23 | 8 heroes |
| Counterspell | 3,200 | -0.046 | -0.015 | +0.030 | Viscous +0.10, Lash +0.07, Drifter +0.03 | 1 heroes |
| Bullet Resilience | 3,200 | -0.051 | -0.016 | +0.046 | Viscous +0.12, Venator +0.11, Lash +0.10 | 0 heroes |
| Healbane | 1,600 | -0.044 | -0.028 | +0.057 | Victor +0.05, Nurse Harrow +0.05, Apollo +0.04 | 14 heroes |
| Metal Skin | 3,200 | -0.170 | -0.053 | +0.096 | Wraith +0.21, Lash +0.17, Silver +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.175 | -0.109 | +0.043 | Lash +0.09, Violet +0.07, Viscous +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.30), Dispel Magic +0.14 (+0.19), Spellbreaker +0.12 (+0.31)
- **Seven**: Witchmail +0.01 (+0.17), Plated Armor -0.00 (+0.09), Healbane -0.02 (+0.04)
- **Vindicta**: Bullet Resilience +0.05 (+0.10), Return Fire +0.04 (+0.08), Healbane +0.03 (+0.08)
- **Lady Geist**: Bullet Resilience +0.04 (+0.09), Counterspell +0.03 (+0.06), Metal Skin +0.01 (+0.11)
- **Abrams**: Dispel Magic +0.03 (+0.08), Reactive Barrier +0.01 (+0.04), Healbane -0.00 (+0.05)
- **Wraith**: Indomitable +0.32 (+0.47), Metal Skin +0.21 (+0.30), Spellbreaker +0.19 (+0.38)
- **McGinnis**: Spirit Resilience +0.07 (+0.21), Dispel Magic +0.01 (+0.06), Healbane +0.01 (+0.07)
- **Paradox**: Witchmail +0.16 (+0.32), Dispel Magic +0.11 (+0.16), Divine Barrier +0.10 (+0.15)
- **Dynamo**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.08 (+0.23), Healbane +0.01 (+0.06), Dispel Magic -0.01 (+0.04)
- **Haze**: Unstoppable +0.23 (+0.38), Bullet Resilience +0.06 (+0.11), Indomitable +0.05 (+0.20)
- **Holliday**: Plated Armor +0.23 (+0.32), Debuff Reducer +0.18 (+0.27), Spellbreaker +0.16 (+0.35)
- **Bebop**: Debuff Reducer +0.16 (+0.25), Spellbreaker +0.08 (+0.27), Unstoppable +0.06 (+0.21)
- **Calico**: Spirit Resilience +0.15 (+0.29), Divine Barrier +0.13 (+0.18), Reactive Barrier +0.06 (+0.10)
- **Grey Talon**: Spellbreaker +0.35 (+0.54), Spirit Resilience +0.32 (+0.46), Unstoppable +0.30 (+0.45)
- **Mo & Krill**: Dispel Magic +0.03 (+0.08), Reactive Barrier +0.02 (+0.06), Healbane +0.02 (+0.07)
- **Shiv**: Metal Skin +0.05 (+0.15), Bullet Resilience +0.04 (+0.09), Plated Armor +0.03 (+0.12)
- **Ivy**: Unstoppable +0.09 (+0.24), Indomitable +0.02 (+0.17), Debuff Reducer +0.02 (+0.11)
- **Warden**: Bullet Resilience +0.02 (+0.07), Divine Barrier +0.02 (+0.07), Healbane +0.01 (+0.07)
- **Yamato**: Reactive Barrier +0.12 (+0.15), Indomitable +0.11 (+0.26), Plated Armor +0.07 (+0.16)
- **Lash**: Spirit Resilience +0.45 (+0.59), Spellbreaker +0.28 (+0.47), Divine Barrier +0.23 (+0.28)
- **Viscous**: Spirit Resilience +0.23 (+0.37), Divine Barrier +0.20 (+0.25), Bullet Resilience +0.12 (+0.16)
- **Pocket**: Spirit Resilience +0.10 (+0.24), Witchmail +0.02 (+0.18), Return Fire +0.00 (+0.04)
- **Mirage**: Dispel Magic +0.27 (+0.32), Metal Skin +0.08 (+0.18), Plated Armor +0.05 (+0.14)
- **Vyper**: Indomitable +0.23 (+0.38), Plated Armor +0.04 (+0.13), Bullet Resilience +0.03 (+0.07)
- **Sinclair**: Indomitable +0.28 (+0.43), Spellbreaker +0.15 (+0.35), Reactive Barrier +0.11 (+0.15)
- **Mina**: Counterspell -0.00 (+0.03), Divine Barrier -0.01 (+0.05), Return Fire -0.01 (+0.03)
- **Drifter**: Witchmail +0.06 (+0.22), Debuff Reducer +0.04 (+0.13), Unstoppable +0.04 (+0.19)
- **Venator**: Metal Skin +0.14 (+0.24), Bullet Resilience +0.11 (+0.16), Plated Armor +0.07 (+0.16)
- **Victor**: Spirit Resilience +0.06 (+0.20), Healbane +0.05 (+0.11), Spellbreaker +0.01 (+0.20)
- **Paige**: Unstoppable +0.24 (+0.39), Debuff Reducer +0.17 (+0.26), Spellbreaker +0.07 (+0.26)
- **The Doorman**: Spirit Resilience +0.39 (+0.53), Witchmail +0.30 (+0.46), Divine Barrier +0.22 (+0.27)
- **Billy**: Reactive Barrier +0.06 (+0.09), Healbane +0.03 (+0.09), Counterspell +0.01 (+0.04)
- **Graves**: Spirit Resilience +0.03 (+0.18), Metal Skin +0.03 (+0.13), Witchmail +0.03 (+0.19)
- **Apollo**: Reactive Barrier +0.04 (+0.08), Healbane +0.04 (+0.10), Counterspell +0.01 (+0.04)
- **Deadman Danny**: Spirit Resilience +0.42 (+0.56), Witchmail +0.34 (+0.50), Spellbreaker +0.31 (+0.51)
- **Rem**: Debuff Reducer +0.15 (+0.24), Unstoppable +0.07 (+0.22), Spellbreaker +0.05 (+0.24)
- **Silver**: Dispel Magic +0.15 (+0.20), Metal Skin +0.15 (+0.25), Indomitable +0.11 (+0.26)
- **Celeste**: Spirit Resilience +0.10 (+0.24), Witchmail +0.09 (+0.26), Divine Barrier +0.04 (+0.10)
- **Rat King**: Debuff Reducer +0.01 (+0.10), Return Fire -0.00 (+0.04), Healbane -0.01 (+0.04)
- **Solomon**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.03), Reactive Barrier -0.01 (+0.02)
- **Violet**: Return Fire +0.07 (+0.11), Healbane +0.01 (+0.06), Counterspell -0.00 (+0.03)
- **Nurse Harrow**: Healbane +0.05 (+0.10), Divine Barrier +0.03 (+0.08), Bullet Resilience +0.03 (+0.07)
- **Baba**: Healbane +0.04 (+0.09), Unstoppable +0.01 (+0.16), Debuff Reducer +0.01 (+0.10)
