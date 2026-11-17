# Counter items in the sim (phantom and up)

Built 2026-11-17T04:51:07Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.157 | +0.049 | +0.135 | Deadman Danny +0.23, The Doorman +0.19, Lash +0.16 | 0 heroes |
| Divine Barrier | 6,400 | +0.247 | +0.039 | +0.122 | The Doorman +0.14, Abrams +0.11, Lash +0.11 | 0 heroes |
| Dispel Magic | 3,200 | +0.090 | +0.028 | +0.080 | Mirage +0.37, Paradox +0.10, Lash +0.10 | 3 heroes |
| Indomitable | 6,400 | +0.166 | +0.026 | +0.134 | The Doorman +0.23, Abrams +0.21, Wraith +0.19 | 0 heroes |
| Reactive Barrier | 1,600 | +0.034 | +0.022 | +0.036 | Deadman Danny +0.15, Graves +0.12, Abrams +0.09 | 3 heroes |
| Witchmail | 6,400 | +0.097 | +0.015 | +0.205 | The Doorman +0.17, Deadman Danny +0.17, Pocket +0.15 | 0 heroes |
| Bullet Resilience | 3,200 | +0.046 | +0.014 | +0.096 | Venator +0.22, Paradox +0.14, Lash +0.10 | 0 heroes |
| Spellbreaker | 6,400 | +0.089 | +0.014 | +0.185 | Deadman Danny +0.20, Holliday +0.19, Lady Geist +0.17 | 0 heroes |
| Healbane | 1,600 | +0.019 | +0.012 | +0.077 | Graves +0.11, Lady Geist +0.05, Mo & Krill +0.05 | 22 heroes |
| Debuff Reducer | 1,600 | +0.017 | +0.011 | +0.074 | Holliday +0.13, Vyper +0.10, Deadman Danny +0.09 | 0 heroes |
| Plated Armor | 6,400 | +0.031 | +0.005 | +0.138 | Holliday +0.30, Deadman Danny +0.26, Wraith +0.17 | 0 heroes |
| Unstoppable | 6,400 | +0.014 | +0.002 | +0.136 | Deadman Danny +0.20, Holliday +0.13, Vyper +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.017 | -0.005 | +0.069 | Graves +0.08, Lash +0.08, Viscous +0.06 | 1 heroes |
| Metal Skin | 3,200 | -0.072 | -0.022 | +0.109 | Wraith +0.26, Paradox +0.19, Lash +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.088 | -0.055 | +0.078 | Wraith +0.09, The Doorman +0.08, Paradox +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.06 (+0.13), Spellbreaker +0.03 (+0.22), Unstoppable +0.03 (+0.16)
- **Seven**: Healbane -0.01 (+0.06), Reactive Barrier -0.02 (+0.01), Counterspell -0.03 (+0.04)
- **Vindicta**: Divine Barrier +0.01 (+0.13), Return Fire -0.01 (+0.07), Counterspell -0.01 (+0.06)
- **Lady Geist**: Spellbreaker +0.17 (+0.35), Spirit Resilience +0.15 (+0.28), Witchmail +0.06 (+0.27)
- **Abrams**: Indomitable +0.21 (+0.34), Divine Barrier +0.11 (+0.24), Spirit Resilience +0.09 (+0.23)
- **Wraith**: Metal Skin +0.26 (+0.37), Indomitable +0.19 (+0.32), Spellbreaker +0.17 (+0.35)
- **McGinnis**: Healbane +0.01 (+0.08), Spirit Resilience +0.00 (+0.14), Return Fire -0.01 (+0.07)
- **Paradox**: Metal Skin +0.19 (+0.29), Bullet Resilience +0.14 (+0.24), Indomitable +0.14 (+0.27)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.03 (+0.04), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Witchmail +0.01 (+0.22), Healbane +0.01 (+0.09), Spirit Resilience +0.00 (+0.14)
- **Haze**: Indomitable +0.12 (+0.26), Unstoppable +0.09 (+0.22), Plated Armor +0.03 (+0.17)
- **Holliday**: Plated Armor +0.30 (+0.44), Spellbreaker +0.19 (+0.37), Debuff Reducer +0.13 (+0.20)
- **Bebop**: Healbane +0.01 (+0.09), Counterspell +0.01 (+0.08), Divine Barrier +0.01 (+0.13)
- **Calico**: Spellbreaker +0.06 (+0.25), Divine Barrier +0.06 (+0.18), Spirit Resilience +0.05 (+0.18)
- **Grey Talon**: Unstoppable +0.07 (+0.21), Reactive Barrier +0.04 (+0.08), Debuff Reducer +0.04 (+0.11)
- **Mo & Krill**: Spellbreaker +0.09 (+0.27), Witchmail +0.07 (+0.28), Unstoppable +0.07 (+0.21)
- **Shiv**: Healbane +0.02 (+0.10), Return Fire +0.01 (+0.09), Bullet Resilience -0.01 (+0.09)
- **Ivy**: Indomitable +0.08 (+0.22), Unstoppable +0.04 (+0.18), Bullet Resilience +0.02 (+0.12)
- **Warden**: Return Fire -0.00 (+0.08), Debuff Reducer -0.00 (+0.07), Counterspell -0.02 (+0.05)
- **Yamato**: Witchmail +0.02 (+0.23), Spellbreaker +0.02 (+0.21), Healbane +0.01 (+0.09)
- **Lash**: Spirit Resilience +0.16 (+0.30), Spellbreaker +0.16 (+0.34), Witchmail +0.15 (+0.35)
- **Viscous**: Divine Barrier +0.07 (+0.20), Counterspell +0.06 (+0.13), Metal Skin +0.05 (+0.16)
- **Pocket**: Witchmail +0.15 (+0.36), Spirit Resilience +0.14 (+0.27), Spellbreaker +0.10 (+0.29)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spirit Resilience +0.11 (+0.24), Spellbreaker +0.09 (+0.28)
- **Vyper**: Debuff Reducer +0.10 (+0.17), Unstoppable +0.09 (+0.23), Spellbreaker +0.08 (+0.27)
- **Sinclair**: Indomitable +0.10 (+0.23), Spellbreaker +0.09 (+0.27), Unstoppable +0.07 (+0.21)
- **Mina**: Return Fire +0.02 (+0.10), Counterspell -0.01 (+0.06), Witchmail -0.01 (+0.19)
- **Drifter**: Healbane -0.01 (+0.07), Reactive Barrier -0.01 (+0.03), Return Fire -0.01 (+0.07)
- **Venator**: Bullet Resilience +0.22 (+0.31), Debuff Reducer +0.08 (+0.15), Unstoppable +0.05 (+0.19)
- **Victor**: Spirit Resilience +0.11 (+0.25), Spellbreaker +0.08 (+0.27), Healbane -0.00 (+0.08)
- **Paige**: Counterspell -0.01 (+0.05), Reactive Barrier -0.01 (+0.02), Return Fire -0.02 (+0.06)
- **The Doorman**: Indomitable +0.23 (+0.36), Spirit Resilience +0.19 (+0.32), Witchmail +0.17 (+0.37)
- **Billy**: Spellbreaker +0.03 (+0.21), Spirit Resilience +0.01 (+0.15), Healbane -0.00 (+0.08)
- **Graves**: Metal Skin +0.13 (+0.24), Witchmail +0.12 (+0.33), Reactive Barrier +0.12 (+0.16)
- **Apollo**: Healbane -0.07 (+0.01), Counterspell -0.09 (-0.02), Reactive Barrier -0.10 (-0.06)
- **Deadman Danny**: Plated Armor +0.26 (+0.40), Spirit Resilience +0.23 (+0.37), Unstoppable +0.20 (+0.33)
- **Rem**: Healbane -0.01 (+0.06), Counterspell -0.02 (+0.05), Reactive Barrier -0.03 (+0.01)
- **Silver**: Dispel Magic +0.10 (+0.18), Reactive Barrier +0.04 (+0.08), Bullet Resilience +0.01 (+0.10)
- **Celeste**: Spirit Resilience +0.16 (+0.29), Witchmail +0.12 (+0.33), Spellbreaker +0.06 (+0.25)
- **Rat King**: Return Fire +0.02 (+0.10), Bullet Resilience +0.00 (+0.10), Divine Barrier -0.01 (+0.12)
- **Solomon**: Reactive Barrier -0.01 (+0.03), Healbane -0.02 (+0.06), Return Fire -0.03 (+0.05)
- **Violet**: Unstoppable +0.03 (+0.17), Healbane +0.01 (+0.09), Return Fire +0.01 (+0.08)
- **Nurse Harrow**: Healbane +0.02 (+0.10), Reactive Barrier -0.02 (+0.01), Return Fire -0.03 (+0.05)
- **Baba**: Healbane +0.00 (+0.08), Reactive Barrier -0.00 (+0.03), Unstoppable -0.00 (+0.13)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.155 | +0.048 | +0.142 | Lash +0.35, Lady Geist +0.17, Graves +0.16 | 9 heroes |
| Divine Barrier | 6,400 | +0.196 | +0.031 | +0.100 | Lash +0.22, Graves +0.10, Abrams +0.10 | 0 heroes |
| Dispel Magic | 3,200 | +0.082 | +0.026 | +0.061 | Mirage +0.24, Abrams +0.12, Lash +0.10 | 8 heroes |
| Indomitable | 6,400 | +0.160 | +0.025 | +0.110 | Wraith +0.20, Abrams +0.20, The Doorman +0.18 | 0 heroes |
| Spellbreaker | 6,400 | +0.131 | +0.020 | +0.175 | Lash +0.33, Lady Geist +0.19, Abrams +0.12 | 0 heroes |
| Witchmail | 6,400 | +0.114 | +0.018 | +0.188 | Lash +0.25, Graves +0.18, Celeste +0.14 | 1 heroes |
| Reactive Barrier | 1,600 | +0.021 | +0.013 | +0.025 | Graves +0.11, Abrams +0.10, Deadman Danny +0.06 | 4 heroes |
| Healbane | 1,600 | +0.013 | +0.008 | +0.068 | Lady Geist +0.07, Abrams +0.06, Yamato +0.06 | 25 heroes |
| Bullet Resilience | 3,200 | +0.023 | +0.007 | +0.069 | Venator +0.17, Paradox +0.13, Lash +0.12 | 1 heroes |
| Plated Armor | 6,400 | +0.037 | +0.006 | +0.098 | Graves +0.14, Paradox +0.11, Lash +0.10 | 0 heroes |
| Debuff Reducer | 1,600 | +0.003 | +0.002 | +0.068 | Holliday +0.13, Rem +0.11, Venator +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.007 | -0.001 | +0.115 | Abrams +0.21, Mo & Krill +0.10, Holliday +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.028 | -0.009 | +0.043 | Lash +0.08, Abrams +0.04, Paradox +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.089 | -0.028 | +0.085 | Lash +0.19, Graves +0.17, Wraith +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.091 | -0.057 | +0.066 | Paradox +0.08, Lash +0.08, Graves +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.15), Unstoppable +0.09 (+0.20), Spellbreaker +0.08 (+0.25)
- **Seven**: Witchmail +0.01 (+0.20), Healbane -0.00 (+0.06), Reactive Barrier -0.02 (+0.01)
- **Vindicta**: Divine Barrier +0.04 (+0.14), Return Fire +0.04 (+0.10), Witchmail +0.02 (+0.21)
- **Lady Geist**: Spellbreaker +0.19 (+0.37), Spirit Resilience +0.17 (+0.32), Witchmail +0.08 (+0.27)
- **Abrams**: Unstoppable +0.21 (+0.33), Indomitable +0.20 (+0.31), Spellbreaker +0.12 (+0.30)
- **Wraith**: Indomitable +0.20 (+0.31), Metal Skin +0.15 (+0.23), Spellbreaker +0.10 (+0.28)
- **McGinnis**: Spirit Resilience +0.08 (+0.22), Dispel Magic +0.01 (+0.07), Healbane -0.00 (+0.06)
- **Paradox**: Bullet Resilience +0.13 (+0.20), Metal Skin +0.13 (+0.21), Indomitable +0.11 (+0.22)
- **Dynamo**: Healbane +0.01 (+0.07), Reactive Barrier -0.02 (+0.01), Counterspell -0.02 (+0.02)
- **Kelvin**: Spirit Resilience +0.07 (+0.21), Dispel Magic +0.03 (+0.09), Witchmail +0.03 (+0.21)
- **Haze**: Indomitable +0.12 (+0.23), Plated Armor +0.08 (+0.18), Unstoppable +0.07 (+0.18)
- **Holliday**: Debuff Reducer +0.13 (+0.20), Spellbreaker +0.12 (+0.29), Unstoppable +0.10 (+0.21)
- **Bebop**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.01)
- **Calico**: Divine Barrier +0.04 (+0.14), Spirit Resilience +0.03 (+0.17), Counterspell +0.01 (+0.06)
- **Grey Talon**: Unstoppable +0.08 (+0.20), Debuff Reducer +0.05 (+0.12), Reactive Barrier +0.05 (+0.07)
- **Mo & Krill**: Unstoppable +0.10 (+0.21), Spellbreaker +0.09 (+0.27), Debuff Reducer +0.05 (+0.12)
- **Shiv**: Bullet Resilience +0.07 (+0.14), Plated Armor +0.04 (+0.14), Metal Skin +0.02 (+0.11)
- **Ivy**: Indomitable +0.05 (+0.16), Bullet Resilience +0.04 (+0.10), Metal Skin +0.02 (+0.11)
- **Warden**: Metal Skin +0.03 (+0.11), Divine Barrier +0.03 (+0.13), Plated Armor +0.02 (+0.12)
- **Yamato**: Healbane +0.06 (+0.13), Witchmail +0.04 (+0.22), Spellbreaker +0.03 (+0.21)
- **Lash**: Spirit Resilience +0.35 (+0.49), Spellbreaker +0.33 (+0.51), Witchmail +0.25 (+0.44)
- **Viscous**: Divine Barrier +0.05 (+0.15), Bullet Resilience +0.02 (+0.09), Spirit Resilience +0.00 (+0.15)
- **Pocket**: Spirit Resilience +0.14 (+0.28), Witchmail +0.08 (+0.27), Spellbreaker +0.04 (+0.22)
- **Mirage**: Dispel Magic +0.24 (+0.30), Metal Skin +0.05 (+0.13), Spirit Resilience +0.02 (+0.16)
- **Vyper**: Spellbreaker +0.09 (+0.27), Unstoppable +0.05 (+0.17), Debuff Reducer +0.05 (+0.12)
- **Sinclair**: Indomitable +0.11 (+0.22), Debuff Reducer +0.01 (+0.08), Unstoppable -0.00 (+0.11)
- **Mina**: Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.04), Reactive Barrier -0.02 (+0.01)
- **Drifter**: Counterspell +0.00 (+0.04), Healbane -0.01 (+0.06), Reactive Barrier -0.01 (+0.02)
- **Venator**: Bullet Resilience +0.17 (+0.24), Debuff Reducer +0.07 (+0.14), Unstoppable +0.05 (+0.17)
- **Victor**: Spirit Resilience +0.07 (+0.21), Spellbreaker +0.07 (+0.24), Healbane +0.00 (+0.07)
- **Paige**: Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.01), Healbane -0.02 (+0.04)
- **The Doorman**: Indomitable +0.18 (+0.29), Spirit Resilience +0.16 (+0.30), Witchmail +0.07 (+0.25)
- **Billy**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Graves**: Witchmail +0.18 (+0.36), Metal Skin +0.17 (+0.26), Spirit Resilience +0.16 (+0.30)
- **Apollo**: Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (+0.01), Healbane -0.02 (+0.05)
- **Deadman Danny**: Witchmail +0.08 (+0.26), Reactive Barrier +0.06 (+0.09), Spirit Resilience +0.06 (+0.20)
- **Rem**: Debuff Reducer +0.11 (+0.17), Unstoppable +0.09 (+0.21), Spellbreaker +0.02 (+0.19)
- **Silver**: Dispel Magic +0.06 (+0.12), Reactive Barrier +0.03 (+0.05), Bullet Resilience -0.00 (+0.07)
- **Celeste**: Witchmail +0.14 (+0.33), Spirit Resilience +0.09 (+0.24), Healbane +0.04 (+0.11)
- **Rat King**: Return Fire -0.01 (+0.06), Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01)
- **Solomon**: Reactive Barrier -0.01 (+0.01), Counterspell -0.02 (+0.02), Return Fire -0.02 (+0.04)
- **Violet**: Indomitable +0.10 (+0.21), Unstoppable +0.10 (+0.21), Witchmail +0.05 (+0.24)
- **Nurse Harrow**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.04), Divine Barrier -0.01 (+0.09)
- **Baba**: Unstoppable +0.01 (+0.13), Healbane +0.00 (+0.07), Debuff Reducer -0.00 (+0.06)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.161 | +0.050 | +0.173 | Lash +0.40, Deadman Danny +0.21, Calico +0.19 | 12 heroes |
| Dispel Magic | 3,200 | +0.091 | +0.029 | +0.068 | Lash +0.22, Mirage +0.21, Wraith +0.15 | 11 heroes |
| Divine Barrier | 6,400 | +0.175 | +0.027 | +0.106 | Lash +0.25, Viscous +0.16, Wraith +0.11 | 2 heroes |
| Indomitable | 6,400 | +0.168 | +0.027 | +0.130 | Wraith +0.32, Lash +0.17, The Doorman +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.154 | +0.024 | +0.203 | Wraith +0.25, Lash +0.24, Holliday +0.18 | 0 heroes |
| Witchmail | 6,400 | +0.115 | +0.018 | +0.211 | Lash +0.28, Wraith +0.18, Graves +0.16 | 1 heroes |
| Healbane | 1,600 | +0.018 | +0.011 | +0.081 | Lady Geist +0.07, Haze +0.06, Mo & Krill +0.05 | 25 heroes |
| Bullet Resilience | 3,200 | +0.030 | +0.009 | +0.079 | Lash +0.20, Venator +0.15, Haze +0.12 | 1 heroes |
| Debuff Reducer | 1,600 | +0.012 | +0.007 | +0.084 | Paige +0.17, Holliday +0.16, Wraith +0.16 | 0 heroes |
| Plated Armor | 6,400 | +0.046 | +0.007 | +0.113 | Lash +0.19, Haze +0.15, Wraith +0.12 | 0 heroes |
| Unstoppable | 6,400 | +0.005 | +0.001 | +0.137 | Paige +0.23, Wraith +0.15, Mo & Krill +0.14 | 3 heroes |
| Reactive Barrier | 1,600 | -0.006 | -0.004 | +0.020 | Deadman Danny +0.09, Grey Talon +0.06, Holliday +0.05 | 3 heroes |
| Counterspell | 3,200 | -0.029 | -0.009 | +0.042 | Viscous +0.07, Lash +0.05, Calico +0.04 | 1 heroes |
| Metal Skin | 3,200 | -0.077 | -0.024 | +0.106 | Wraith +0.29, Lash +0.22, Graves +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.082 | -0.051 | +0.066 | Vindicta +0.10, Wraith +0.09, Viscous +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.18), Spellbreaker +0.08 (+0.28), Unstoppable +0.05 (+0.19)
- **Seven**: Witchmail +0.06 (+0.27), Healbane +0.01 (+0.09), Counterspell +0.00 (+0.04)
- **Vindicta**: Return Fire +0.10 (+0.17), Bullet Resilience +0.09 (+0.17), Divine Barrier +0.08 (+0.18)
- **Lady Geist**: Healbane +0.07 (+0.15), Spellbreaker +0.04 (+0.24), Spirit Resilience +0.02 (+0.20)
- **Abrams**: Unstoppable +0.08 (+0.22), Dispel Magic +0.08 (+0.15), Indomitable +0.03 (+0.16)
- **Wraith**: Indomitable +0.32 (+0.45), Metal Skin +0.29 (+0.40), Spellbreaker +0.25 (+0.45)
- **McGinnis**: Spirit Resilience +0.07 (+0.24), Reactive Barrier -0.01 (+0.01), Counterspell -0.01 (+0.03)
- **Paradox**: Indomitable +0.11 (+0.24), Spirit Resilience +0.11 (+0.28), Witchmail +0.09 (+0.30)
- **Dynamo**: Healbane -0.01 (+0.07), Counterspell -0.02 (+0.02), Reactive Barrier -0.02 (-0.00)
- **Kelvin**: Spirit Resilience +0.15 (+0.32), Healbane +0.05 (+0.13), Witchmail +0.04 (+0.25)
- **Haze**: Plated Armor +0.15 (+0.26), Indomitable +0.13 (+0.26), Bullet Resilience +0.12 (+0.20)
- **Holliday**: Spellbreaker +0.18 (+0.38), Debuff Reducer +0.16 (+0.24), Unstoppable +0.12 (+0.26)
- **Bebop**: Healbane +0.04 (+0.12), Reactive Barrier -0.02 (+0.00), Counterspell -0.02 (+0.03)
- **Calico**: Spirit Resilience +0.19 (+0.36), Divine Barrier +0.10 (+0.21), Witchmail +0.05 (+0.26)
- **Grey Talon**: Unstoppable +0.13 (+0.26), Debuff Reducer +0.12 (+0.21), Spellbreaker +0.11 (+0.31)
- **Mo & Krill**: Indomitable +0.15 (+0.28), Unstoppable +0.14 (+0.28), Debuff Reducer +0.14 (+0.23)
- **Shiv**: Bullet Resilience +0.02 (+0.10), Return Fire +0.01 (+0.08), Metal Skin +0.00 (+0.11)
- **Ivy**: Indomitable +0.03 (+0.16), Bullet Resilience +0.00 (+0.08), Metal Skin +0.00 (+0.11)
- **Warden**: Metal Skin +0.05 (+0.16), Return Fire +0.02 (+0.09), Dispel Magic +0.02 (+0.09)
- **Yamato**: Spellbreaker +0.06 (+0.26), Witchmail +0.04 (+0.26), Healbane +0.03 (+0.11)
- **Lash**: Spirit Resilience +0.40 (+0.57), Witchmail +0.28 (+0.49), Divine Barrier +0.25 (+0.36)
- **Viscous**: Divine Barrier +0.16 (+0.26), Spirit Resilience +0.12 (+0.29), Metal Skin +0.07 (+0.18)
- **Pocket**: Spirit Resilience +0.05 (+0.22), Witchmail +0.02 (+0.23), Dispel Magic -0.00 (+0.07)
- **Mirage**: Dispel Magic +0.21 (+0.28), Unstoppable +0.06 (+0.20), Spellbreaker +0.05 (+0.25)
- **Vyper**: Spellbreaker +0.10 (+0.31), Reactive Barrier +0.05 (+0.07), Debuff Reducer +0.04 (+0.13)
- **Sinclair**: Indomitable +0.07 (+0.20), Reactive Barrier -0.02 (-0.00), Return Fire -0.04 (+0.03)
- **Mina**: Witchmail +0.07 (+0.28), Divine Barrier +0.05 (+0.16), Plated Armor +0.03 (+0.14)
- **Drifter**: Reactive Barrier +0.01 (+0.03), Return Fire +0.00 (+0.07), Counterspell -0.00 (+0.04)
- **Venator**: Bullet Resilience +0.15 (+0.23), Debuff Reducer +0.03 (+0.11), Unstoppable +0.02 (+0.16)
- **Victor**: Spellbreaker +0.06 (+0.26), Spirit Resilience +0.04 (+0.21), Healbane +0.03 (+0.11)
- **Paige**: Unstoppable +0.23 (+0.36), Debuff Reducer +0.17 (+0.25), Spellbreaker +0.06 (+0.26)
- **The Doorman**: Indomitable +0.16 (+0.29), Spirit Resilience +0.11 (+0.29), Witchmail +0.06 (+0.28)
- **Billy**: Reactive Barrier +0.02 (+0.04), Healbane -0.00 (+0.08), Counterspell -0.01 (+0.04)
- **Graves**: Spirit Resilience +0.17 (+0.35), Witchmail +0.16 (+0.37), Metal Skin +0.15 (+0.26)
- **Apollo**: Healbane +0.04 (+0.12), Unstoppable +0.03 (+0.17), Counterspell +0.01 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.21 (+0.39), Spellbreaker +0.15 (+0.35), Reactive Barrier +0.09 (+0.11)
- **Rem**: Debuff Reducer +0.11 (+0.19), Unstoppable +0.07 (+0.21), Spellbreaker +0.02 (+0.23)
- **Silver**: Dispel Magic +0.03 (+0.09), Reactive Barrier +0.01 (+0.03), Counterspell +0.01 (+0.05)
- **Celeste**: Spirit Resilience +0.10 (+0.28), Witchmail +0.07 (+0.28), Plated Armor +0.02 (+0.13)
- **Rat King**: Return Fire -0.02 (+0.05), Counterspell -0.03 (+0.02), Reactive Barrier -0.03 (-0.01)
- **Solomon**: Reactive Barrier +0.04 (+0.06), Return Fire +0.01 (+0.08), Debuff Reducer -0.01 (+0.07)
- **Violet**: Witchmail +0.10 (+0.31), Divine Barrier +0.05 (+0.16), Unstoppable +0.02 (+0.16)
- **Nurse Harrow**: Spirit Resilience +0.05 (+0.22), Divine Barrier +0.04 (+0.15), Healbane +0.02 (+0.10)
- **Baba**: Reactive Barrier -0.00 (+0.02), Healbane -0.01 (+0.08), Counterspell -0.01 (+0.03)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.137 | +0.043 | +0.137 | The Doorman +0.39, Lash +0.36, Deadman Danny +0.36 | 20 heroes |
| Dispel Magic | 3,200 | +0.094 | +0.029 | +0.066 | Mirage +0.18, Calico +0.14, Viscous +0.12 | 11 heroes |
| Indomitable | 6,400 | +0.164 | +0.026 | +0.107 | Wraith +0.33, The Doorman +0.25, Mo & Krill +0.18 | 2 heroes |
| Spellbreaker | 6,400 | +0.160 | +0.025 | +0.189 | Deadman Danny +0.26, Rem +0.21, Lash +0.20 | 0 heroes |
| Divine Barrier | 6,400 | +0.146 | +0.023 | +0.079 | Lash +0.14, The Doorman +0.11, Vindicta +0.08 | 2 heroes |
| Witchmail | 6,400 | +0.100 | +0.016 | +0.168 | Deadman Danny +0.20, Lash +0.17, The Doorman +0.16 | 1 heroes |
| Bullet Resilience | 3,200 | +0.016 | +0.005 | +0.054 | Lash +0.10, Venator +0.10, Vindicta +0.10 | 1 heroes |
| Plated Armor | 6,400 | +0.030 | +0.005 | +0.092 | Vindicta +0.09, Wraith +0.08, Lash +0.07 | 4 heroes |
| Healbane | 1,600 | +0.007 | +0.004 | +0.061 | Victor +0.07, Lady Geist +0.06, Paradox +0.05 | 22 heroes |
| Debuff Reducer | 1,600 | +0.005 | +0.003 | +0.086 | Bebop +0.18, Mo & Krill +0.16, Grey Talon +0.15 | 0 heroes |
| Unstoppable | 6,400 | +0.002 | +0.000 | +0.136 | Infernus +0.18, Grey Talon +0.18, Mo & Krill +0.15 | 5 heroes |
| Reactive Barrier | 1,600 | -0.019 | -0.012 | +0.013 | Deadman Danny +0.09, Ivy +0.05, Holliday +0.04 | 2 heroes |
| Counterspell | 3,200 | -0.038 | -0.012 | +0.029 | Paradox +0.04, Vindicta +0.04, Lash +0.04 | 1 heroes |
| Metal Skin | 3,200 | -0.087 | -0.027 | +0.085 | Wraith +0.20, Lash +0.18, Paradox +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.083 | -0.052 | +0.048 | Vindicta +0.07, Wraith +0.07, Holliday +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.18 (+0.32), Spellbreaker +0.13 (+0.32), Dispel Magic +0.10 (+0.16)
- **Seven**: Witchmail +0.11 (+0.28), Dispel Magic +0.03 (+0.10), Spirit Resilience +0.02 (+0.16)
- **Vindicta**: Bullet Resilience +0.10 (+0.15), Plated Armor +0.09 (+0.18), Divine Barrier +0.08 (+0.16)
- **Lady Geist**: Spellbreaker +0.08 (+0.27), Healbane +0.06 (+0.12), Spirit Resilience +0.06 (+0.19)
- **Abrams**: Spirit Resilience +0.04 (+0.17), Reactive Barrier +0.04 (+0.05), Unstoppable +0.03 (+0.16)
- **Wraith**: Indomitable +0.33 (+0.44), Metal Skin +0.20 (+0.29), Spellbreaker +0.20 (+0.39)
- **McGinnis**: Dispel Magic +0.04 (+0.10), Divine Barrier +0.03 (+0.11), Spirit Resilience +0.02 (+0.16)
- **Paradox**: Metal Skin +0.14 (+0.22), Unstoppable +0.10 (+0.23), Witchmail +0.08 (+0.25)
- **Dynamo**: Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05), Reactive Barrier -0.02 (-0.00)
- **Kelvin**: Spirit Resilience +0.05 (+0.19), Healbane -0.00 (+0.06), Reactive Barrier -0.01 (+0.00)
- **Haze**: Unstoppable +0.11 (+0.25), Plated Armor +0.07 (+0.16), Bullet Resilience +0.05 (+0.10)
- **Holliday**: Spellbreaker +0.15 (+0.34), Debuff Reducer +0.13 (+0.21), Unstoppable +0.09 (+0.22)
- **Bebop**: Debuff Reducer +0.18 (+0.26), Unstoppable +0.15 (+0.28), Spellbreaker +0.08 (+0.27)
- **Calico**: Dispel Magic +0.14 (+0.21), Divine Barrier +0.08 (+0.16), Spirit Resilience +0.08 (+0.21)
- **Grey Talon**: Spirit Resilience +0.20 (+0.34), Spellbreaker +0.20 (+0.39), Unstoppable +0.18 (+0.31)
- **Mo & Krill**: Spellbreaker +0.18 (+0.37), Indomitable +0.18 (+0.28), Debuff Reducer +0.16 (+0.25)
- **Shiv**: Bullet Resilience +0.08 (+0.13), Metal Skin +0.07 (+0.16), Plated Armor +0.05 (+0.14)
- **Ivy**: Indomitable +0.12 (+0.23), Unstoppable +0.11 (+0.25), Reactive Barrier +0.05 (+0.06)
- **Warden**: Bullet Resilience +0.05 (+0.11), Plated Armor +0.05 (+0.14), Metal Skin +0.04 (+0.12)
- **Yamato**: Healbane +0.04 (+0.10), Spirit Resilience +0.04 (+0.18), Witchmail -0.01 (+0.16)
- **Lash**: Spirit Resilience +0.36 (+0.50), Spellbreaker +0.20 (+0.39), Metal Skin +0.18 (+0.27)
- **Viscous**: Dispel Magic +0.12 (+0.19), Divine Barrier +0.02 (+0.10), Spirit Resilience +0.00 (+0.14)
- **Pocket**: Spirit Resilience +0.07 (+0.21), Witchmail -0.00 (+0.17), Return Fire -0.01 (+0.04)
- **Mirage**: Dispel Magic +0.18 (+0.25), Spellbreaker +0.04 (+0.23), Reactive Barrier -0.01 (+0.00)
- **Vyper**: Debuff Reducer +0.13 (+0.22), Unstoppable +0.09 (+0.23), Spellbreaker +0.05 (+0.24)
- **Sinclair**: Indomitable +0.11 (+0.22), Dispel Magic +0.06 (+0.13), Debuff Reducer +0.04 (+0.13)
- **Mina**: Spirit Resilience +0.06 (+0.20), Divine Barrier +0.04 (+0.12), Counterspell +0.01 (+0.04)
- **Drifter**: Dispel Magic +0.07 (+0.13), Reactive Barrier +0.01 (+0.02), Debuff Reducer +0.01 (+0.09)
- **Venator**: Bullet Resilience +0.10 (+0.16), Metal Skin +0.02 (+0.11), Return Fire -0.01 (+0.04)
- **Victor**: Healbane +0.07 (+0.14), Spellbreaker +0.06 (+0.25), Spirit Resilience +0.03 (+0.17)
- **Paige**: Counterspell +0.02 (+0.04), Witchmail +0.01 (+0.18), Divine Barrier +0.01 (+0.09)
- **The Doorman**: Spirit Resilience +0.39 (+0.53), Indomitable +0.25 (+0.36), Spellbreaker +0.19 (+0.38)
- **Billy**: Reactive Barrier +0.02 (+0.03), Counterspell +0.01 (+0.04), Return Fire -0.01 (+0.03)
- **Graves**: Witchmail +0.08 (+0.24), Metal Skin +0.05 (+0.13), Healbane +0.04 (+0.10)
- **Apollo**: Bullet Resilience +0.02 (+0.07), Healbane +0.00 (+0.06), Plated Armor +0.00 (+0.09)
- **Deadman Danny**: Spirit Resilience +0.36 (+0.50), Spellbreaker +0.26 (+0.45), Witchmail +0.20 (+0.37)
- **Rem**: Spellbreaker +0.21 (+0.40), Debuff Reducer +0.12 (+0.21), Unstoppable +0.11 (+0.24)
- **Silver**: Metal Skin +0.07 (+0.15), Plated Armor +0.06 (+0.15), Dispel Magic +0.05 (+0.11)
- **Celeste**: Spirit Resilience +0.10 (+0.23), Witchmail +0.07 (+0.24), Healbane +0.01 (+0.07)
- **Rat King**: Healbane +0.00 (+0.06), Debuff Reducer -0.00 (+0.08), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.02 (+0.03), Return Fire -0.00 (+0.04), Counterspell -0.01 (+0.02)
- **Violet**: Witchmail +0.05 (+0.22), Divine Barrier +0.04 (+0.12), Spirit Resilience +0.04 (+0.18)
- **Nurse Harrow**: Spirit Resilience +0.18 (+0.31), Healbane +0.03 (+0.09), Witchmail +0.02 (+0.19)
- **Baba**: Unstoppable +0.02 (+0.16), Counterspell +0.01 (+0.04), Healbane +0.01 (+0.07)
