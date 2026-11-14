# Counter items in the sim (phantom and up)

Built 2026-11-14T03:42:45Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.155 | +0.048 | +0.133 | Lash +0.21, The Doorman +0.19, Lady Geist +0.17 | 0 heroes |
| Divine Barrier | 6,400 | +0.257 | +0.041 | +0.127 | Lash +0.17, Viscous +0.15, The Doorman +0.13 | 0 heroes |
| Dispel Magic | 3,200 | +0.092 | +0.029 | +0.082 | Mirage +0.37, Lash +0.11, Silver +0.11 | 4 heroes |
| Indomitable | 6,400 | +0.166 | +0.026 | +0.135 | The Doorman +0.24, Abrams +0.20, Wraith +0.18 | 0 heroes |
| Reactive Barrier | 1,600 | +0.037 | +0.024 | +0.039 | Graves +0.11, Deadman Danny +0.10, Abrams +0.08 | 2 heroes |
| Bullet Resilience | 3,200 | +0.049 | +0.015 | +0.103 | Venator +0.21, Lash +0.15, Paradox +0.11 | 0 heroes |
| Witchmail | 6,400 | +0.098 | +0.015 | +0.205 | Lash +0.19, The Doorman +0.16, Deadman Danny +0.15 | 0 heroes |
| Healbane | 1,600 | +0.023 | +0.014 | +0.081 | Graves +0.10, Lady Geist +0.08, Yamato +0.07 | 23 heroes |
| Spellbreaker | 6,400 | +0.085 | +0.013 | +0.181 | Lady Geist +0.21, Lash +0.21, The Doorman +0.17 | 0 heroes |
| Debuff Reducer | 1,600 | +0.021 | +0.013 | +0.080 | Holliday +0.12, Vyper +0.11, Venator +0.08 | 0 heroes |
| Plated Armor | 6,400 | +0.035 | +0.005 | +0.137 | Holliday +0.23, Wraith +0.17, Lash +0.12 | 0 heroes |
| Unstoppable | 6,400 | +0.018 | +0.003 | +0.141 | Deadman Danny +0.11, Holliday +0.10, Lash +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.012 | -0.004 | +0.073 | Lash +0.09, Graves +0.08, Viscous +0.06 | 1 heroes |
| Metal Skin | 3,200 | -0.068 | -0.021 | +0.117 | Wraith +0.25, Lash +0.19, Paradox +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.085 | -0.053 | +0.087 | Paradox +0.10, The Doorman +0.07, Wraith +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.04 (+0.12), Spellbreaker +0.03 (+0.21), Unstoppable +0.02 (+0.16)
- **Seven**: Healbane -0.00 (+0.08), Reactive Barrier -0.02 (+0.02), Witchmail -0.03 (+0.18)
- **Vindicta**: Divine Barrier -0.00 (+0.12), Witchmail -0.02 (+0.19), Return Fire -0.02 (+0.07)
- **Lady Geist**: Spellbreaker +0.21 (+0.39), Spirit Resilience +0.17 (+0.30), Witchmail +0.10 (+0.30)
- **Abrams**: Indomitable +0.20 (+0.33), Divine Barrier +0.11 (+0.24), Witchmail +0.09 (+0.29)
- **Wraith**: Metal Skin +0.25 (+0.37), Indomitable +0.18 (+0.32), Plated Armor +0.17 (+0.30)
- **McGinnis**: Spirit Resilience -0.00 (+0.13), Healbane -0.01 (+0.07), Return Fire -0.02 (+0.07)
- **Paradox**: Metal Skin +0.12 (+0.24), Bullet Resilience +0.11 (+0.21), Return Fire +0.10 (+0.19)
- **Dynamo**: Healbane -0.02 (+0.06), Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.04)
- **Kelvin**: Witchmail +0.02 (+0.22), Spirit Resilience +0.01 (+0.14), Counterspell -0.00 (+0.07)
- **Haze**: Indomitable +0.12 (+0.26), Unstoppable +0.08 (+0.22), Plated Armor +0.03 (+0.17)
- **Holliday**: Plated Armor +0.23 (+0.36), Spellbreaker +0.15 (+0.33), Debuff Reducer +0.12 (+0.20)
- **Bebop**: Healbane +0.04 (+0.12), Counterspell +0.01 (+0.08), Divine Barrier -0.00 (+0.13)
- **Calico**: Spellbreaker +0.07 (+0.25), Divine Barrier +0.06 (+0.19), Spirit Resilience +0.05 (+0.18)
- **Grey Talon**: Unstoppable +0.07 (+0.21), Reactive Barrier +0.04 (+0.08), Debuff Reducer +0.04 (+0.12)
- **Mo & Krill**: Spellbreaker +0.08 (+0.26), Witchmail +0.07 (+0.27), Unstoppable +0.05 (+0.19)
- **Shiv**: Return Fire +0.01 (+0.10), Healbane +0.01 (+0.09), Counterspell -0.01 (+0.06)
- **Ivy**: Indomitable +0.08 (+0.21), Unstoppable +0.03 (+0.17), Bullet Resilience +0.01 (+0.12)
- **Warden**: Debuff Reducer -0.01 (+0.07), Return Fire -0.01 (+0.08), Counterspell -0.02 (+0.05)
- **Yamato**: Healbane +0.07 (+0.15), Witchmail +0.03 (+0.24), Return Fire +0.02 (+0.11)
- **Lash**: Spirit Resilience +0.21 (+0.34), Spellbreaker +0.21 (+0.39), Witchmail +0.19 (+0.40)
- **Viscous**: Divine Barrier +0.15 (+0.27), Metal Skin +0.10 (+0.22), Spirit Resilience +0.10 (+0.23)
- **Pocket**: Witchmail +0.02 (+0.22), Counterspell +0.01 (+0.09), Return Fire +0.01 (+0.10)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spellbreaker +0.13 (+0.31), Spirit Resilience +0.12 (+0.25)
- **Vyper**: Debuff Reducer +0.11 (+0.19), Unstoppable +0.09 (+0.24), Spellbreaker +0.08 (+0.26)
- **Sinclair**: Indomitable +0.10 (+0.23), Spellbreaker +0.09 (+0.27), Unstoppable +0.07 (+0.21)
- **Mina**: Return Fire +0.02 (+0.10), Counterspell -0.01 (+0.06), Witchmail -0.02 (+0.19)
- **Drifter**: Return Fire +0.01 (+0.10), Bullet Resilience -0.01 (+0.10), Counterspell -0.01 (+0.07)
- **Venator**: Bullet Resilience +0.21 (+0.32), Debuff Reducer +0.08 (+0.16), Unstoppable +0.06 (+0.20)
- **Victor**: Spirit Resilience +0.12 (+0.25), Spellbreaker +0.09 (+0.27), Healbane -0.01 (+0.08)
- **Paige**: Counterspell -0.02 (+0.06), Reactive Barrier -0.02 (+0.02), Healbane -0.02 (+0.06)
- **The Doorman**: Indomitable +0.24 (+0.37), Spirit Resilience +0.19 (+0.33), Spellbreaker +0.17 (+0.35)
- **Billy**: Spellbreaker +0.02 (+0.20), Spirit Resilience +0.02 (+0.15), Healbane -0.01 (+0.08)
- **Graves**: Reactive Barrier +0.11 (+0.15), Metal Skin +0.11 (+0.23), Witchmail +0.11 (+0.31)
- **Apollo**: Healbane -0.03 (+0.05), Counterspell -0.04 (+0.04), Reactive Barrier -0.04 (+0.00)
- **Deadman Danny**: Spellbreaker +0.15 (+0.34), Witchmail +0.15 (+0.36), Spirit Resilience +0.14 (+0.27)
- **Rem**: Healbane -0.02 (+0.07), Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.04)
- **Silver**: Dispel Magic +0.11 (+0.19), Reactive Barrier +0.04 (+0.08), Bullet Resilience +0.01 (+0.12)
- **Celeste**: Spirit Resilience +0.15 (+0.29), Witchmail +0.12 (+0.33), Spellbreaker +0.07 (+0.26)
- **Rat King**: Return Fire +0.02 (+0.10), Bullet Resilience -0.00 (+0.10), Divine Barrier -0.01 (+0.12)
- **Solomon**: Reactive Barrier -0.01 (+0.03), Healbane -0.02 (+0.06), Return Fire -0.03 (+0.06)
- **Violet**: Unstoppable +0.06 (+0.20), Return Fire +0.05 (+0.14), Witchmail +0.02 (+0.23)
- **Nurse Harrow**: Healbane +0.05 (+0.13), Reactive Barrier -0.00 (+0.04), Counterspell -0.03 (+0.04)
- **Baba**: Reactive Barrier -0.00 (+0.04), Healbane -0.00 (+0.08), Counterspell -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.155 | +0.049 | +0.147 | Lash +0.37, Celeste +0.21, Pocket +0.17 | 9 heroes |
| Divine Barrier | 6,400 | +0.191 | +0.030 | +0.098 | Lash +0.23, Abrams +0.12, Paradox +0.12 | 1 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.064 | Mirage +0.25, Holliday +0.12, Abrams +0.11 | 10 heroes |
| Indomitable | 6,400 | +0.158 | +0.025 | +0.108 | Wraith +0.20, The Doorman +0.20, Abrams +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.132 | +0.021 | +0.178 | Lash +0.34, Holliday +0.21, Lady Geist +0.19 | 0 heroes |
| Witchmail | 6,400 | +0.114 | +0.018 | +0.186 | Lash +0.28, Celeste +0.18, Graves +0.10 | 1 heroes |
| Reactive Barrier | 1,600 | +0.021 | +0.013 | +0.022 | Abrams +0.11, Deadman Danny +0.06, Holliday +0.05 | 3 heroes |
| Healbane | 1,600 | +0.015 | +0.009 | +0.061 | Yamato +0.09, Lady Geist +0.07, Infernus +0.07 | 23 heroes |
| Bullet Resilience | 3,200 | +0.025 | +0.008 | +0.073 | Venator +0.20, Paradox +0.15, Lash +0.12 | 1 heroes |
| Plated Armor | 6,400 | +0.041 | +0.006 | +0.097 | Paradox +0.12, Lash +0.10, Wraith +0.10 | 0 heroes |
| Debuff Reducer | 1,600 | +0.005 | +0.003 | +0.071 | Holliday +0.22, Rem +0.13, Vyper +0.10 | 0 heroes |
| Unstoppable | 6,400 | -0.005 | -0.001 | +0.114 | Holliday +0.20, Abrams +0.15, Rem +0.13 | 0 heroes |
| Counterspell | 3,200 | -0.025 | -0.008 | +0.044 | Lash +0.09, Abrams +0.05, Calico +0.04 | 1 heroes |
| Metal Skin | 3,200 | -0.086 | -0.027 | +0.091 | Wraith +0.26, Lash +0.18, Paradox +0.18 | 0 heroes |
| Return Fire | 1,600 | -0.093 | -0.059 | +0.064 | Lash +0.10, Paradox +0.08, Abrams +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.10 (+0.21), Dispel Magic +0.09 (+0.15), Spellbreaker +0.09 (+0.27)
- **Seven**: Witchmail +0.03 (+0.22), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Vindicta**: Divine Barrier +0.05 (+0.14), Return Fire +0.04 (+0.10), Witchmail +0.03 (+0.21)
- **Lady Geist**: Spellbreaker +0.19 (+0.37), Spirit Resilience +0.17 (+0.32), Witchmail +0.08 (+0.27)
- **Abrams**: Indomitable +0.16 (+0.27), Unstoppable +0.15 (+0.26), Divine Barrier +0.12 (+0.22)
- **Wraith**: Metal Skin +0.26 (+0.35), Indomitable +0.20 (+0.31), Spellbreaker +0.14 (+0.32)
- **McGinnis**: Spirit Resilience +0.08 (+0.23), Witchmail +0.02 (+0.21), Healbane +0.00 (+0.06)
- **Paradox**: Metal Skin +0.18 (+0.27), Bullet Resilience +0.15 (+0.22), Plated Armor +0.12 (+0.22)
- **Dynamo**: Healbane +0.03 (+0.09), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.00)
- **Kelvin**: Spirit Resilience +0.08 (+0.23), Witchmail +0.04 (+0.23), Spellbreaker +0.02 (+0.19)
- **Haze**: Indomitable +0.08 (+0.18), Plated Armor +0.06 (+0.15), Unstoppable +0.04 (+0.15)
- **Holliday**: Debuff Reducer +0.22 (+0.29), Spellbreaker +0.21 (+0.38), Unstoppable +0.20 (+0.31)
- **Bebop**: Healbane +0.01 (+0.07), Counterspell -0.00 (+0.04), Reactive Barrier -0.02 (+0.01)
- **Calico**: Divine Barrier +0.10 (+0.20), Spirit Resilience +0.08 (+0.22), Witchmail +0.05 (+0.23)
- **Grey Talon**: Unstoppable +0.10 (+0.22), Debuff Reducer +0.06 (+0.13), Spellbreaker +0.05 (+0.22)
- **Mo & Krill**: Spellbreaker +0.09 (+0.27), Unstoppable +0.09 (+0.21), Dispel Magic +0.05 (+0.11)
- **Shiv**: Bullet Resilience +0.09 (+0.16), Plated Armor +0.05 (+0.15), Return Fire +0.04 (+0.11)
- **Ivy**: Unstoppable +0.02 (+0.14), Indomitable +0.02 (+0.13), Debuff Reducer +0.00 (+0.08)
- **Warden**: Divine Barrier +0.02 (+0.12), Return Fire +0.00 (+0.07), Bullet Resilience +0.00 (+0.07)
- **Yamato**: Healbane +0.09 (+0.15), Debuff Reducer +0.02 (+0.09), Counterspell +0.01 (+0.05)
- **Lash**: Spirit Resilience +0.37 (+0.52), Spellbreaker +0.34 (+0.52), Witchmail +0.28 (+0.46)
- **Viscous**: Divine Barrier +0.03 (+0.13), Counterspell +0.01 (+0.05), Bullet Resilience -0.00 (+0.07)
- **Pocket**: Spirit Resilience +0.17 (+0.32), Witchmail +0.08 (+0.27), Dispel Magic +0.05 (+0.11)
- **Mirage**: Dispel Magic +0.25 (+0.31), Metal Skin +0.03 (+0.12), Spirit Resilience +0.02 (+0.17)
- **Vyper**: Debuff Reducer +0.10 (+0.17), Unstoppable +0.09 (+0.20), Spellbreaker +0.08 (+0.25)
- **Sinclair**: Indomitable +0.16 (+0.27), Spellbreaker +0.04 (+0.22), Debuff Reducer +0.02 (+0.09)
- **Mina**: Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.04), Reactive Barrier -0.02 (+0.01)
- **Drifter**: Counterspell +0.00 (+0.04), Healbane +0.00 (+0.06), Reactive Barrier -0.00 (+0.02)
- **Venator**: Bullet Resilience +0.20 (+0.27), Debuff Reducer +0.06 (+0.13), Unstoppable +0.04 (+0.15)
- **Victor**: Spirit Resilience +0.09 (+0.24), Spellbreaker +0.07 (+0.24), Healbane +0.00 (+0.06)
- **Paige**: Counterspell -0.00 (+0.04), Reactive Barrier -0.01 (+0.01), Divine Barrier -0.02 (+0.08)
- **The Doorman**: Indomitable +0.20 (+0.31), Spirit Resilience +0.11 (+0.26), Witchmail +0.08 (+0.27)
- **Billy**: Healbane +0.00 (+0.06), Counterspell -0.00 (+0.04), Reactive Barrier -0.01 (+0.01)
- **Graves**: Metal Skin +0.12 (+0.21), Witchmail +0.10 (+0.28), Spirit Resilience +0.09 (+0.24)
- **Apollo**: Healbane -0.01 (+0.05), Reactive Barrier -0.02 (+0.00), Counterspell -0.02 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.09 (+0.24), Witchmail +0.06 (+0.25), Reactive Barrier +0.06 (+0.08)
- **Rem**: Unstoppable +0.13 (+0.25), Debuff Reducer +0.13 (+0.20), Spellbreaker +0.04 (+0.22)
- **Silver**: Dispel Magic +0.09 (+0.15), Reactive Barrier +0.03 (+0.06), Debuff Reducer -0.01 (+0.06)
- **Celeste**: Spirit Resilience +0.21 (+0.35), Witchmail +0.18 (+0.37), Metal Skin +0.09 (+0.18)
- **Rat King**: Return Fire +0.00 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Solomon**: Reactive Barrier -0.01 (+0.01), Counterspell -0.02 (+0.02), Return Fire -0.02 (+0.04)
- **Violet**: Indomitable +0.09 (+0.20), Witchmail +0.05 (+0.24), Return Fire +0.03 (+0.10)
- **Nurse Harrow**: Divine Barrier +0.05 (+0.14), Spirit Resilience +0.03 (+0.18), Counterspell +0.03 (+0.07)
- **Baba**: Unstoppable +0.02 (+0.13), Healbane +0.00 (+0.06), Reactive Barrier -0.01 (+0.01)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.140 | +0.044 | +0.136 | Lash +0.29, Deadman Danny +0.18, Graves +0.18 | 12 heroes |
| Dispel Magic | 3,200 | +0.081 | +0.025 | +0.050 | Mirage +0.23, Infernus +0.14, Lash +0.08 | 10 heroes |
| Divine Barrier | 6,400 | +0.160 | +0.025 | +0.081 | Viscous +0.12, Lash +0.08, Mina +0.08 | 2 heroes |
| Indomitable | 6,400 | +0.148 | +0.023 | +0.094 | Wraith +0.25, Sinclair +0.21, The Doorman +0.17 | 0 heroes |
| Spellbreaker | 6,400 | +0.139 | +0.022 | +0.170 | Lash +0.29, Holliday +0.16, Wraith +0.14 | 0 heroes |
| Witchmail | 6,400 | +0.099 | +0.015 | +0.174 | Graves +0.16, Lash +0.16, Deadman Danny +0.14 | 1 heroes |
| Healbane | 1,600 | +0.013 | +0.008 | +0.064 | Lady Geist +0.08, Mo & Krill +0.08, Nurse Harrow +0.07 | 25 heroes |
| Plated Armor | 6,400 | +0.041 | +0.006 | +0.092 | Holliday +0.19, Wraith +0.10, Vindicta +0.07 | 0 heroes |
| Bullet Resilience | 3,200 | +0.017 | +0.005 | +0.053 | Venator +0.19, Vindicta +0.10, Paradox +0.05 | 1 heroes |
| Debuff Reducer | 1,600 | +0.003 | +0.002 | +0.064 | Holliday +0.14, Grey Talon +0.13, Rem +0.12 | 0 heroes |
| Unstoppable | 6,400 | -0.007 | -0.001 | +0.108 | Haze +0.17, Mo & Krill +0.17, Grey Talon +0.14 | 4 heroes |
| Reactive Barrier | 1,600 | -0.008 | -0.005 | +0.014 | Deadman Danny +0.11, Grey Talon +0.06, Silver +0.04 | 2 heroes |
| Counterspell | 3,200 | -0.032 | -0.010 | +0.031 | Kelvin +0.02, Paradox +0.02, Vyper +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.086 | -0.027 | +0.084 | Wraith +0.28, Graves +0.13, Lash +0.08 | 0 heroes |
| Return Fire | 1,600 | -0.088 | -0.055 | +0.056 | Wraith +0.10, Paradox +0.07, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.14 (+0.19), Spellbreaker +0.08 (+0.25), Unstoppable +0.06 (+0.17)
- **Seven**: Witchmail +0.09 (+0.26), Spirit Resilience +0.07 (+0.20), Reactive Barrier +0.01 (+0.03)
- **Vindicta**: Bullet Resilience +0.10 (+0.16), Plated Armor +0.07 (+0.16), Return Fire +0.05 (+0.10)
- **Lady Geist**: Healbane +0.08 (+0.14), Spellbreaker +0.07 (+0.24), Spirit Resilience +0.05 (+0.19)
- **Abrams**: Unstoppable +0.06 (+0.16), Dispel Magic +0.04 (+0.09), Spirit Resilience +0.01 (+0.15)
- **Wraith**: Metal Skin +0.28 (+0.36), Indomitable +0.25 (+0.35), Spellbreaker +0.14 (+0.31)
- **McGinnis**: Spirit Resilience +0.09 (+0.23), Witchmail +0.04 (+0.21), Spellbreaker +0.00 (+0.17)
- **Paradox**: Dispel Magic +0.07 (+0.12), Return Fire +0.07 (+0.12), Indomitable +0.06 (+0.16)
- **Dynamo**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.01 (+0.00)
- **Kelvin**: Spirit Resilience +0.05 (+0.18), Counterspell +0.02 (+0.05), Healbane +0.00 (+0.07)
- **Haze**: Unstoppable +0.17 (+0.28), Indomitable +0.07 (+0.16), Plated Armor +0.04 (+0.14)
- **Holliday**: Plated Armor +0.19 (+0.28), Spellbreaker +0.16 (+0.33), Debuff Reducer +0.14 (+0.20)
- **Bebop**: Healbane +0.05 (+0.11), Divine Barrier +0.03 (+0.11), Counterspell +0.01 (+0.04)
- **Calico**: Spirit Resilience +0.13 (+0.26), Divine Barrier +0.05 (+0.13), Dispel Magic +0.02 (+0.07)
- **Grey Talon**: Unstoppable +0.14 (+0.25), Debuff Reducer +0.13 (+0.19), Spellbreaker +0.10 (+0.27)
- **Mo & Krill**: Unstoppable +0.17 (+0.28), Spellbreaker +0.10 (+0.27), Healbane +0.08 (+0.14)
- **Shiv**: Bullet Resilience +0.05 (+0.10), Divine Barrier +0.02 (+0.10), Plated Armor +0.02 (+0.11)
- **Ivy**: Indomitable +0.06 (+0.15), Unstoppable +0.03 (+0.14), Metal Skin +0.03 (+0.11)
- **Warden**: Debuff Reducer +0.02 (+0.08), Return Fire +0.00 (+0.06), Bullet Resilience +0.00 (+0.05)
- **Yamato**: Witchmail +0.07 (+0.24), Healbane +0.06 (+0.12), Spirit Resilience +0.06 (+0.19)
- **Lash**: Spirit Resilience +0.29 (+0.43), Spellbreaker +0.29 (+0.46), Witchmail +0.16 (+0.33)
- **Viscous**: Divine Barrier +0.12 (+0.20), Spirit Resilience +0.12 (+0.25), Spellbreaker +0.08 (+0.25)
- **Pocket**: Spirit Resilience +0.05 (+0.18), Witchmail +0.03 (+0.20), Return Fire -0.01 (+0.05)
- **Mirage**: Dispel Magic +0.23 (+0.28), Spellbreaker +0.06 (+0.23), Healbane +0.00 (+0.07)
- **Vyper**: Spellbreaker +0.09 (+0.26), Debuff Reducer +0.06 (+0.12), Unstoppable +0.05 (+0.16)
- **Sinclair**: Indomitable +0.21 (+0.31), Unstoppable +0.08 (+0.19), Debuff Reducer +0.06 (+0.13)
- **Mina**: Divine Barrier +0.08 (+0.16), Witchmail +0.07 (+0.24), Spirit Resilience +0.06 (+0.20)
- **Drifter**: Healbane -0.00 (+0.06), Reactive Barrier -0.00 (+0.01), Return Fire -0.00 (+0.05)
- **Venator**: Bullet Resilience +0.19 (+0.24), Plated Armor +0.07 (+0.16), Debuff Reducer +0.06 (+0.12)
- **Victor**: Healbane +0.02 (+0.08), Spirit Resilience +0.01 (+0.15), Spellbreaker +0.01 (+0.18)
- **Paige**: Counterspell +0.01 (+0.04), Divine Barrier -0.00 (+0.08), Reactive Barrier -0.01 (+0.01)
- **The Doorman**: Indomitable +0.17 (+0.26), Spirit Resilience +0.12 (+0.25), Witchmail +0.08 (+0.25)
- **Billy**: Reactive Barrier +0.03 (+0.04), Debuff Reducer +0.01 (+0.08), Counterspell +0.01 (+0.04)
- **Graves**: Spirit Resilience +0.18 (+0.32), Witchmail +0.16 (+0.34), Metal Skin +0.13 (+0.21)
- **Apollo**: Counterspell -0.00 (+0.03), Healbane -0.01 (+0.06), Reactive Barrier -0.01 (+0.00)
- **Deadman Danny**: Spirit Resilience +0.18 (+0.32), Witchmail +0.14 (+0.31), Spellbreaker +0.14 (+0.31)
- **Rem**: Debuff Reducer +0.12 (+0.18), Unstoppable +0.10 (+0.21), Spellbreaker +0.03 (+0.20)
- **Silver**: Reactive Barrier +0.04 (+0.06), Dispel Magic +0.04 (+0.09), Divine Barrier +0.03 (+0.11)
- **Celeste**: Spirit Resilience +0.10 (+0.23), Witchmail +0.08 (+0.26), Healbane +0.05 (+0.11)
- **Rat King**: Bullet Resilience +0.00 (+0.06), Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.03 (+0.05), Debuff Reducer -0.01 (+0.06), Counterspell -0.02 (+0.02)
- **Violet**: Witchmail +0.12 (+0.29), Divine Barrier +0.07 (+0.15), Unstoppable +0.05 (+0.15)
- **Nurse Harrow**: Healbane +0.07 (+0.14), Spirit Resilience +0.03 (+0.17), Divine Barrier +0.03 (+0.11)
- **Baba**: Reactive Barrier -0.00 (+0.01), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.134 | +0.042 | +0.138 | Lash +0.49, The Doorman +0.37, Viscous +0.30 | 17 heroes |
| Dispel Magic | 3,200 | +0.088 | +0.027 | +0.055 | Mirage +0.19, The Doorman +0.15, Lash +0.14 | 11 heroes |
| Indomitable | 6,400 | +0.166 | +0.026 | +0.115 | Wraith +0.32, The Doorman +0.22, Mo & Krill +0.20 | 2 heroes |
| Spellbreaker | 6,400 | +0.161 | +0.025 | +0.192 | Lash +0.31, Grey Talon +0.22, Deadman Danny +0.19 | 0 heroes |
| Divine Barrier | 6,400 | +0.148 | +0.023 | +0.080 | Lash +0.21, Viscous +0.15, Mo & Krill +0.08 | 2 heroes |
| Witchmail | 6,400 | +0.101 | +0.016 | +0.168 | Lash +0.31, Violet +0.19, The Doorman +0.18 | 1 heroes |
| Healbane | 1,600 | +0.011 | +0.007 | +0.062 | Victor +0.09, Mo & Krill +0.08, Violet +0.06 | 23 heroes |
| Plated Armor | 6,400 | +0.040 | +0.006 | +0.100 | Haze +0.14, Vindicta +0.13, Lash +0.11 | 3 heroes |
| Bullet Resilience | 3,200 | +0.019 | +0.006 | +0.060 | Vindicta +0.16, Lash +0.12, Haze +0.11 | 1 heroes |
| Debuff Reducer | 1,600 | +0.007 | +0.004 | +0.088 | Bebop +0.22, Grey Talon +0.21, Holliday +0.15 | 0 heroes |
| Unstoppable | 6,400 | +0.008 | +0.001 | +0.144 | Grey Talon +0.21, Paradox +0.20, Haze +0.19 | 5 heroes |
| Reactive Barrier | 1,600 | -0.016 | -0.010 | +0.015 | Deadman Danny +0.08, Lash +0.06, Grey Talon +0.04 | 2 heroes |
| Counterspell | 3,200 | -0.034 | -0.011 | +0.031 | Lash +0.13, Viscous +0.06, Violet +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.087 | -0.027 | +0.083 | Lash +0.27, Wraith +0.13, Paradox +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.082 | -0.051 | +0.053 | Lash +0.14, Vindicta +0.11, Haze +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.18 (+0.33), Spellbreaker +0.15 (+0.34), Dispel Magic +0.11 (+0.16)
- **Seven**: Witchmail +0.11 (+0.28), Counterspell +0.02 (+0.05), Healbane +0.01 (+0.07)
- **Vindicta**: Bullet Resilience +0.16 (+0.22), Plated Armor +0.13 (+0.23), Return Fire +0.11 (+0.16)
- **Lady Geist**: Spellbreaker +0.09 (+0.29), Healbane +0.06 (+0.12), Spirit Resilience +0.06 (+0.20)
- **Abrams**: Unstoppable +0.05 (+0.19), Reactive Barrier +0.02 (+0.03), Dispel Magic +0.00 (+0.06)
- **Wraith**: Indomitable +0.32 (+0.43), Spellbreaker +0.17 (+0.36), Metal Skin +0.13 (+0.22)
- **McGinnis**: Spirit Resilience +0.03 (+0.17), Dispel Magic +0.03 (+0.08), Witchmail +0.03 (+0.19)
- **Paradox**: Unstoppable +0.20 (+0.34), Indomitable +0.18 (+0.29), Metal Skin +0.12 (+0.21)
- **Dynamo**: Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (-0.00), Healbane -0.02 (+0.04)
- **Kelvin**: Spirit Resilience +0.04 (+0.18), Healbane +0.01 (+0.07), Reactive Barrier -0.01 (+0.01)
- **Haze**: Unstoppable +0.19 (+0.34), Plated Armor +0.14 (+0.24), Bullet Resilience +0.11 (+0.17)
- **Holliday**: Debuff Reducer +0.15 (+0.24), Spellbreaker +0.15 (+0.34), Unstoppable +0.11 (+0.26)
- **Bebop**: Debuff Reducer +0.22 (+0.31), Unstoppable +0.18 (+0.33), Spellbreaker +0.14 (+0.33)
- **Calico**: Spirit Resilience +0.02 (+0.16), Counterspell -0.00 (+0.03), Divine Barrier -0.01 (+0.08)
- **Grey Talon**: Spellbreaker +0.22 (+0.41), Spirit Resilience +0.22 (+0.36), Unstoppable +0.21 (+0.36)
- **Mo & Krill**: Indomitable +0.20 (+0.32), Spellbreaker +0.19 (+0.38), Spirit Resilience +0.18 (+0.32)
- **Shiv**: Bullet Resilience +0.08 (+0.14), Return Fire +0.05 (+0.10), Metal Skin +0.03 (+0.11)
- **Ivy**: Reactive Barrier +0.01 (+0.02), Unstoppable +0.00 (+0.15), Bullet Resilience -0.00 (+0.06)
- **Warden**: Plated Armor +0.10 (+0.20), Debuff Reducer +0.06 (+0.14), Spellbreaker +0.05 (+0.24)
- **Yamato**: Healbane +0.04 (+0.10), Counterspell +0.01 (+0.04), Reactive Barrier -0.00 (+0.01)
- **Lash**: Spirit Resilience +0.49 (+0.63), Spellbreaker +0.31 (+0.50), Witchmail +0.31 (+0.47)
- **Viscous**: Spirit Resilience +0.30 (+0.44), Divine Barrier +0.15 (+0.23), Spellbreaker +0.14 (+0.33)
- **Pocket**: Spirit Resilience +0.00 (+0.14), Reactive Barrier -0.01 (+0.00), Return Fire -0.01 (+0.04)
- **Mirage**: Dispel Magic +0.19 (+0.25), Spellbreaker +0.05 (+0.25), Reactive Barrier -0.01 (+0.00)
- **Vyper**: Debuff Reducer +0.13 (+0.22), Unstoppable +0.09 (+0.23), Spellbreaker +0.05 (+0.24)
- **Sinclair**: Indomitable +0.14 (+0.26), Spellbreaker +0.08 (+0.28), Debuff Reducer +0.01 (+0.10)
- **Mina**: Divine Barrier +0.03 (+0.11), Spirit Resilience +0.03 (+0.17), Witchmail +0.01 (+0.18)
- **Drifter**: Dispel Magic +0.09 (+0.14), Reactive Barrier +0.02 (+0.04), Debuff Reducer +0.01 (+0.10)
- **Venator**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.01 (+0.09), Reactive Barrier -0.02 (-0.00)
- **Victor**: Spellbreaker +0.09 (+0.28), Healbane +0.09 (+0.15), Spirit Resilience +0.04 (+0.18)
- **Paige**: Counterspell +0.01 (+0.04), Witchmail +0.01 (+0.18), Divine Barrier +0.01 (+0.09)
- **The Doorman**: Spirit Resilience +0.37 (+0.51), Indomitable +0.22 (+0.34), Witchmail +0.18 (+0.34)
- **Billy**: Reactive Barrier +0.04 (+0.06), Counterspell +0.00 (+0.03), Healbane +0.00 (+0.06)
- **Graves**: Return Fire +0.02 (+0.08), Metal Skin +0.01 (+0.10), Reactive Barrier +0.01 (+0.03)
- **Apollo**: Counterspell +0.01 (+0.04), Reactive Barrier -0.01 (+0.00), Healbane -0.02 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.25 (+0.39), Spellbreaker +0.19 (+0.39), Witchmail +0.12 (+0.29)
- **Rem**: Spirit Resilience +0.07 (+0.20), Spellbreaker +0.04 (+0.23), Healbane +0.03 (+0.09)
- **Silver**: Metal Skin +0.12 (+0.20), Dispel Magic +0.11 (+0.16), Bullet Resilience +0.04 (+0.10)
- **Celeste**: Spirit Resilience +0.08 (+0.22), Witchmail +0.06 (+0.23), Healbane +0.01 (+0.07)
- **Rat King**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.02), Reactive Barrier -0.01 (+0.00)
- **Solomon**: Reactive Barrier +0.02 (+0.04), Return Fire +0.01 (+0.07), Divine Barrier +0.00 (+0.08)
- **Violet**: Witchmail +0.19 (+0.36), Dispel Magic +0.13 (+0.19), Spirit Resilience +0.11 (+0.25)
- **Nurse Harrow**: Spirit Resilience +0.19 (+0.32), Witchmail +0.03 (+0.20), Divine Barrier +0.03 (+0.11)
- **Baba**: Unstoppable +0.02 (+0.16), Counterspell +0.01 (+0.04), Healbane +0.01 (+0.08)
