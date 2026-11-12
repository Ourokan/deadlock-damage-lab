# Counter items in the sim (phantom and up)

Built 2026-11-12T10:01:22Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.155 | +0.048 | +0.129 | Lash +0.21, The Doorman +0.17, Celeste +0.15 | 0 heroes |
| Divine Barrier | 6,400 | +0.255 | +0.041 | +0.126 | Lash +0.17, Viscous +0.14, Abrams +0.13 | 0 heroes |
| Dispel Magic | 3,200 | +0.090 | +0.028 | +0.082 | Mirage +0.37, Lash +0.10, Paradox +0.10 | 4 heroes |
| Indomitable | 6,400 | +0.163 | +0.026 | +0.132 | Abrams +0.22, The Doorman +0.22, Wraith +0.18 | 0 heroes |
| Reactive Barrier | 1,600 | +0.036 | +0.023 | +0.038 | Deadman Danny +0.12, Graves +0.10, Holliday +0.06 | 2 heroes |
| Healbane | 1,600 | +0.028 | +0.017 | +0.082 | Graves +0.10, Yamato +0.06, Lady Geist +0.05 | 22 heroes |
| Bullet Resilience | 3,200 | +0.051 | +0.016 | +0.101 | Venator +0.27, Lash +0.15, Paradox +0.13 | 0 heroes |
| Witchmail | 6,400 | +0.096 | +0.015 | +0.204 | Lash +0.18, Deadman Danny +0.16, The Doorman +0.15 | 0 heroes |
| Debuff Reducer | 1,600 | +0.023 | +0.015 | +0.082 | Holliday +0.11, Vyper +0.11, Venator +0.09 | 0 heroes |
| Spellbreaker | 6,400 | +0.083 | +0.013 | +0.177 | Lash +0.21, Lady Geist +0.19, Deadman Danny +0.17 | 0 heroes |
| Plated Armor | 6,400 | +0.032 | +0.005 | +0.135 | Holliday +0.22, Wraith +0.13, Lash +0.13 | 0 heroes |
| Unstoppable | 6,400 | +0.017 | +0.003 | +0.135 | Deadman Danny +0.12, Lash +0.11, Holliday +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.009 | -0.003 | +0.073 | Lash +0.09, Graves +0.07, Deadman Danny +0.07 | 0 heroes |
| Metal Skin | 3,200 | -0.070 | -0.022 | +0.113 | Wraith +0.23, Lash +0.18, Paradox +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.086 | -0.054 | +0.085 | Paradox +0.11, Holliday +0.06, Violet +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.05 (+0.13), Spellbreaker +0.04 (+0.21), Unstoppable +0.03 (+0.17)
- **Seven**: Healbane -0.00 (+0.08), Reactive Barrier -0.02 (+0.02), Spirit Resilience -0.03 (+0.10)
- **Vindicta**: Divine Barrier +0.00 (+0.13), Counterspell -0.01 (+0.07), Healbane -0.01 (+0.08)
- **Lady Geist**: Spellbreaker +0.19 (+0.37), Spirit Resilience +0.15 (+0.27), Witchmail +0.08 (+0.28)
- **Abrams**: Indomitable +0.22 (+0.35), Divine Barrier +0.13 (+0.25), Witchmail +0.09 (+0.29)
- **Wraith**: Metal Skin +0.23 (+0.34), Indomitable +0.18 (+0.31), Spellbreaker +0.16 (+0.33)
- **McGinnis**: Healbane +0.04 (+0.12), Spirit Resilience +0.01 (+0.14), Reactive Barrier +0.00 (+0.04)
- **Paradox**: Metal Skin +0.16 (+0.27), Bullet Resilience +0.13 (+0.23), Return Fire +0.11 (+0.19)
- **Dynamo**: Healbane +0.00 (+0.08), Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.05)
- **Kelvin**: Witchmail +0.03 (+0.23), Healbane +0.01 (+0.09), Spirit Resilience +0.01 (+0.14)
- **Haze**: Indomitable +0.07 (+0.20), Plated Armor +0.06 (+0.20), Bullet Resilience +0.04 (+0.14)
- **Holliday**: Plated Armor +0.22 (+0.35), Spellbreaker +0.14 (+0.32), Debuff Reducer +0.11 (+0.20)
- **Bebop**: Healbane +0.02 (+0.10), Counterspell +0.01 (+0.08), Divine Barrier -0.01 (+0.12)
- **Calico**: Spellbreaker +0.08 (+0.26), Divine Barrier +0.06 (+0.18), Spirit Resilience +0.05 (+0.18)
- **Grey Talon**: Unstoppable +0.07 (+0.20), Debuff Reducer +0.04 (+0.12), Reactive Barrier +0.04 (+0.08)
- **Mo & Krill**: Spellbreaker +0.07 (+0.25), Witchmail +0.04 (+0.25), Spirit Resilience +0.04 (+0.17)
- **Shiv**: Healbane -0.00 (+0.08), Return Fire -0.00 (+0.08), Bullet Resilience -0.02 (+0.08)
- **Ivy**: Indomitable +0.09 (+0.22), Unstoppable +0.04 (+0.18), Bullet Resilience +0.01 (+0.11)
- **Warden**: Return Fire +0.01 (+0.09), Debuff Reducer -0.00 (+0.08), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.06 (+0.15), Debuff Reducer +0.05 (+0.14), Unstoppable +0.05 (+0.19)
- **Lash**: Spellbreaker +0.21 (+0.38), Spirit Resilience +0.21 (+0.33), Witchmail +0.18 (+0.39)
- **Viscous**: Divine Barrier +0.14 (+0.27), Spirit Resilience +0.08 (+0.21), Spellbreaker +0.07 (+0.25)
- **Pocket**: Return Fire +0.01 (+0.09), Counterspell +0.01 (+0.08), Witchmail +0.01 (+0.21)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spellbreaker +0.13 (+0.30), Spirit Resilience +0.12 (+0.25)
- **Vyper**: Debuff Reducer +0.11 (+0.19), Unstoppable +0.08 (+0.22), Spellbreaker +0.07 (+0.25)
- **Sinclair**: Indomitable +0.15 (+0.28), Spellbreaker +0.08 (+0.26), Unstoppable +0.06 (+0.20)
- **Mina**: Return Fire +0.02 (+0.10), Counterspell -0.01 (+0.06), Spirit Resilience -0.02 (+0.11)
- **Drifter**: Reactive Barrier -0.01 (+0.02), Return Fire -0.01 (+0.07), Counterspell -0.02 (+0.06)
- **Venator**: Bullet Resilience +0.27 (+0.37), Debuff Reducer +0.09 (+0.17), Unstoppable +0.08 (+0.22)
- **Victor**: Spirit Resilience +0.11 (+0.24), Spellbreaker +0.09 (+0.27), Healbane -0.01 (+0.07)
- **Paige**: Reactive Barrier -0.01 (+0.02), Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.07)
- **The Doorman**: Indomitable +0.22 (+0.35), Spirit Resilience +0.17 (+0.30), Witchmail +0.15 (+0.35)
- **Billy**: Spellbreaker +0.03 (+0.20), Spirit Resilience +0.03 (+0.15), Witchmail +0.01 (+0.21)
- **Graves**: Reactive Barrier +0.10 (+0.14), Healbane +0.10 (+0.18), Metal Skin +0.10 (+0.21)
- **Apollo**: Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.04), Healbane -0.04 (+0.05)
- **Deadman Danny**: Spellbreaker +0.17 (+0.35), Witchmail +0.16 (+0.36), Spirit Resilience +0.15 (+0.27)
- **Rem**: Healbane -0.01 (+0.07), Reactive Barrier -0.02 (+0.02), Counterspell -0.02 (+0.05)
- **Silver**: Dispel Magic +0.09 (+0.17), Reactive Barrier +0.05 (+0.08), Debuff Reducer +0.01 (+0.09)
- **Celeste**: Spirit Resilience +0.15 (+0.28), Witchmail +0.12 (+0.33), Spellbreaker +0.06 (+0.24)
- **Rat King**: Return Fire +0.00 (+0.09), Counterspell -0.01 (+0.06), Divine Barrier -0.01 (+0.11)
- **Solomon**: Reactive Barrier -0.00 (+0.03), Counterspell -0.03 (+0.05), Return Fire -0.03 (+0.06)
- **Violet**: Return Fire +0.06 (+0.15), Unstoppable +0.06 (+0.19), Witchmail +0.03 (+0.23)
- **Nurse Harrow**: Healbane +0.05 (+0.13), Reactive Barrier -0.01 (+0.02), Counterspell -0.04 (+0.03)
- **Baba**: Reactive Barrier -0.00 (+0.04), Healbane -0.00 (+0.08), Counterspell -0.02 (+0.06)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.156 | +0.049 | +0.143 | Lash +0.43, Celeste +0.23, Lady Geist +0.20 | 9 heroes |
| Divine Barrier | 6,400 | +0.214 | +0.034 | +0.096 | Lash +0.26, Paradox +0.10, Abrams +0.09 | 1 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.069 | Mirage +0.24, Lash +0.15, Holliday +0.12 | 10 heroes |
| Indomitable | 6,400 | +0.154 | +0.024 | +0.105 | Lash +0.19, The Doorman +0.18, Wraith +0.17 | 0 heroes |
| Spellbreaker | 6,400 | +0.128 | +0.020 | +0.169 | Lash +0.33, Holliday +0.20, Lady Geist +0.19 | 0 heroes |
| Witchmail | 6,400 | +0.111 | +0.017 | +0.185 | Lash +0.28, Celeste +0.20, Lady Geist +0.09 | 1 heroes |
| Healbane | 1,600 | +0.019 | +0.012 | +0.065 | Lady Geist +0.09, Abrams +0.08, Yamato +0.07 | 23 heroes |
| Reactive Barrier | 1,600 | +0.019 | +0.012 | +0.020 | Abrams +0.08, Deadman Danny +0.06, Holliday +0.06 | 4 heroes |
| Bullet Resilience | 3,200 | +0.026 | +0.008 | +0.070 | Venator +0.21, Paradox +0.14, Lash +0.10 | 1 heroes |
| Plated Armor | 6,400 | +0.038 | +0.006 | +0.096 | Paradox +0.12, Lash +0.09, Wraith +0.08 | 0 heroes |
| Debuff Reducer | 1,600 | +0.003 | +0.002 | +0.064 | Holliday +0.21, Rem +0.12, Venator +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.004 | -0.001 | +0.113 | Holliday +0.19, Rem +0.12, Abrams +0.11 | 0 heroes |
| Counterspell | 3,200 | -0.022 | -0.007 | +0.045 | Lash +0.05, Nurse Harrow +0.04, Pocket +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.087 | -0.027 | +0.087 | Wraith +0.25, Lash +0.20, Paradox +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.095 | -0.059 | +0.061 | Paradox +0.07, Deadman Danny +0.05, Venator +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.10 (+0.27), Unstoppable +0.10 (+0.21), Dispel Magic +0.07 (+0.14)
- **Seven**: Witchmail +0.04 (+0.22), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Divine Barrier +0.05 (+0.15), Return Fire +0.05 (+0.11), Witchmail +0.03 (+0.22)
- **Lady Geist**: Spirit Resilience +0.20 (+0.35), Spellbreaker +0.19 (+0.36), Witchmail +0.09 (+0.27)
- **Abrams**: Indomitable +0.12 (+0.23), Unstoppable +0.11 (+0.22), Spirit Resilience +0.09 (+0.23)
- **Wraith**: Metal Skin +0.25 (+0.33), Indomitable +0.17 (+0.28), Spellbreaker +0.12 (+0.29)
- **McGinnis**: Spirit Resilience +0.07 (+0.21), Witchmail +0.02 (+0.20), Healbane +0.00 (+0.07)
- **Paradox**: Metal Skin +0.15 (+0.24), Bullet Resilience +0.14 (+0.21), Indomitable +0.12 (+0.23)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.00)
- **Kelvin**: Spirit Resilience +0.07 (+0.22), Witchmail +0.03 (+0.22), Spellbreaker +0.01 (+0.18)
- **Haze**: Indomitable +0.09 (+0.20), Plated Armor +0.06 (+0.16), Bullet Resilience +0.04 (+0.11)
- **Holliday**: Debuff Reducer +0.21 (+0.27), Spellbreaker +0.20 (+0.37), Unstoppable +0.19 (+0.30)
- **Bebop**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01)
- **Calico**: Divine Barrier +0.05 (+0.15), Spirit Resilience +0.03 (+0.18), Witchmail +0.01 (+0.19)
- **Grey Talon**: Unstoppable +0.09 (+0.21), Debuff Reducer +0.05 (+0.11), Spellbreaker +0.04 (+0.21)
- **Mo & Krill**: Spellbreaker +0.09 (+0.26), Unstoppable +0.09 (+0.20), Dispel Magic +0.04 (+0.11)
- **Shiv**: Bullet Resilience +0.06 (+0.13), Metal Skin +0.04 (+0.13), Plated Armor +0.04 (+0.13)
- **Ivy**: Unstoppable +0.02 (+0.14), Debuff Reducer +0.00 (+0.07), Indomitable +0.00 (+0.11)
- **Warden**: Return Fire +0.02 (+0.09), Divine Barrier -0.00 (+0.10), Debuff Reducer -0.01 (+0.05)
- **Yamato**: Healbane +0.07 (+0.14), Debuff Reducer +0.00 (+0.07), Reactive Barrier -0.01 (+0.01)
- **Lash**: Spirit Resilience +0.43 (+0.58), Spellbreaker +0.33 (+0.50), Witchmail +0.28 (+0.46)
- **Viscous**: Divine Barrier +0.03 (+0.13), Counterspell +0.01 (+0.05), Healbane -0.00 (+0.06)
- **Pocket**: Spirit Resilience +0.19 (+0.33), Witchmail +0.07 (+0.25), Spellbreaker +0.07 (+0.23)
- **Mirage**: Dispel Magic +0.24 (+0.31), Metal Skin +0.04 (+0.13), Spellbreaker +0.02 (+0.19)
- **Vyper**: Spellbreaker +0.08 (+0.25), Debuff Reducer +0.07 (+0.14), Unstoppable +0.06 (+0.17)
- **Sinclair**: Indomitable +0.13 (+0.23), Debuff Reducer +0.02 (+0.09), Spellbreaker +0.02 (+0.19)
- **Mina**: Counterspell +0.01 (+0.05), Plated Armor +0.00 (+0.10), Return Fire -0.00 (+0.06)
- **Drifter**: Return Fire +0.01 (+0.07), Healbane -0.00 (+0.06), Counterspell -0.00 (+0.04)
- **Venator**: Bullet Resilience +0.21 (+0.28), Debuff Reducer +0.07 (+0.14), Unstoppable +0.06 (+0.17)
- **Victor**: Spirit Resilience +0.09 (+0.24), Spellbreaker +0.07 (+0.24), Healbane +0.02 (+0.09)
- **Paige**: Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01), Return Fire -0.03 (+0.04)
- **The Doorman**: Indomitable +0.18 (+0.28), Spirit Resilience +0.10 (+0.24), Spellbreaker +0.09 (+0.26)
- **Billy**: Healbane +0.00 (+0.07), Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.05)
- **Graves**: Metal Skin +0.11 (+0.20), Spirit Resilience +0.07 (+0.22), Witchmail +0.06 (+0.24)
- **Apollo**: Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (-0.00), Healbane -0.03 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.10 (+0.24), Witchmail +0.08 (+0.27), Indomitable +0.06 (+0.17)
- **Rem**: Debuff Reducer +0.12 (+0.19), Unstoppable +0.12 (+0.23), Spellbreaker +0.03 (+0.20)
- **Silver**: Dispel Magic +0.11 (+0.18), Reactive Barrier +0.04 (+0.06), Healbane +0.01 (+0.08)
- **Celeste**: Spirit Resilience +0.23 (+0.37), Witchmail +0.20 (+0.38), Spellbreaker +0.11 (+0.27)
- **Rat King**: Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Solomon**: Return Fire -0.01 (+0.05), Reactive Barrier -0.01 (+0.01), Counterspell -0.01 (+0.03)
- **Violet**: Unstoppable +0.07 (+0.18), Witchmail +0.06 (+0.25), Healbane +0.05 (+0.11)
- **Nurse Harrow**: Healbane +0.06 (+0.12), Divine Barrier +0.05 (+0.15), Counterspell +0.04 (+0.09)
- **Baba**: Unstoppable +0.02 (+0.13), Healbane -0.00 (+0.06), Debuff Reducer -0.00 (+0.06)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.147 | +0.046 | +0.144 | Lash +0.33, Deadman Danny +0.21, Viscous +0.19 | 12 heroes |
| Divine Barrier | 6,400 | +0.167 | +0.026 | +0.090 | Lash +0.22, Viscous +0.09, Mina +0.07 | 2 heroes |
| Dispel Magic | 3,200 | +0.083 | +0.026 | +0.057 | Lash +0.23, Mirage +0.22, Infernus +0.11 | 10 heroes |
| Indomitable | 6,400 | +0.156 | +0.025 | +0.111 | Wraith +0.21, Haze +0.20, Lash +0.18 | 0 heroes |
| Spellbreaker | 6,400 | +0.142 | +0.022 | +0.175 | Lash +0.21, Wraith +0.19, Holliday +0.17 | 0 heroes |
| Witchmail | 6,400 | +0.102 | +0.016 | +0.184 | Lash +0.26, Deadman Danny +0.15, Graves +0.14 | 1 heroes |
| Healbane | 1,600 | +0.018 | +0.011 | +0.067 | Lady Geist +0.08, Mo & Krill +0.08, Infernus +0.07 | 25 heroes |
| Bullet Resilience | 3,200 | +0.026 | +0.008 | +0.067 | Venator +0.21, Lash +0.20, Vindicta +0.11 | 1 heroes |
| Plated Armor | 6,400 | +0.044 | +0.007 | +0.103 | Holliday +0.21, Lash +0.18, Haze +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.007 | +0.004 | +0.070 | Holliday +0.16, Grey Talon +0.14, Rem +0.13 | 0 heroes |
| Unstoppable | 6,400 | +0.002 | +0.000 | +0.124 | Mo & Krill +0.21, Haze +0.17, Grey Talon +0.15 | 4 heroes |
| Reactive Barrier | 1,600 | -0.007 | -0.004 | +0.017 | Deadman Danny +0.10, Grey Talon +0.06, Silver +0.05 | 2 heroes |
| Counterspell | 3,200 | -0.026 | -0.008 | +0.040 | Lash +0.06, Viscous +0.04, Vindicta +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.081 | -0.025 | +0.096 | Wraith +0.23, Lash +0.21, Graves +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.087 | -0.055 | +0.060 | Haze +0.11, Venator +0.07, Vindicta +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.17), Spellbreaker +0.09 (+0.27), Healbane +0.07 (+0.14)
- **Seven**: Witchmail +0.08 (+0.26), Spirit Resilience +0.06 (+0.20), Reactive Barrier +0.01 (+0.03)
- **Vindicta**: Bullet Resilience +0.11 (+0.18), Plated Armor +0.08 (+0.19), Return Fire +0.07 (+0.13)
- **Lady Geist**: Healbane +0.08 (+0.15), Spellbreaker +0.05 (+0.23), Spirit Resilience +0.02 (+0.16)
- **Abrams**: Unstoppable +0.08 (+0.20), Dispel Magic +0.04 (+0.10), Reactive Barrier +0.04 (+0.05)
- **Wraith**: Metal Skin +0.23 (+0.33), Indomitable +0.21 (+0.32), Spellbreaker +0.19 (+0.36)
- **McGinnis**: Spirit Resilience +0.09 (+0.23), Witchmail +0.03 (+0.21), Counterspell +0.01 (+0.05)
- **Paradox**: Dispel Magic +0.07 (+0.12), Return Fire +0.05 (+0.11), Spellbreaker +0.04 (+0.22)
- **Dynamo**: Healbane -0.00 (+0.07), Counterspell -0.02 (+0.02), Reactive Barrier -0.02 (-0.00)
- **Kelvin**: Spirit Resilience +0.05 (+0.19), Counterspell +0.02 (+0.06), Debuff Reducer -0.01 (+0.06)
- **Haze**: Indomitable +0.20 (+0.32), Unstoppable +0.17 (+0.30), Plated Armor +0.12 (+0.22)
- **Holliday**: Plated Armor +0.21 (+0.31), Spellbreaker +0.17 (+0.34), Debuff Reducer +0.16 (+0.23)
- **Bebop**: Healbane +0.04 (+0.10), Divine Barrier +0.01 (+0.10), Counterspell +0.01 (+0.05)
- **Calico**: Spirit Resilience +0.11 (+0.25), Dispel Magic +0.03 (+0.09), Divine Barrier +0.03 (+0.12)
- **Grey Talon**: Unstoppable +0.15 (+0.27), Debuff Reducer +0.14 (+0.20), Spellbreaker +0.12 (+0.30)
- **Mo & Krill**: Unstoppable +0.21 (+0.34), Spellbreaker +0.12 (+0.29), Debuff Reducer +0.08 (+0.15)
- **Shiv**: Bullet Resilience +0.05 (+0.11), Divine Barrier +0.01 (+0.10), Return Fire +0.00 (+0.06)
- **Ivy**: Indomitable +0.04 (+0.15), Unstoppable +0.02 (+0.14), Metal Skin +0.01 (+0.10)
- **Warden**: Debuff Reducer +0.01 (+0.08), Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Yamato**: Healbane +0.06 (+0.13), Witchmail +0.04 (+0.23), Debuff Reducer +0.04 (+0.11)
- **Lash**: Spirit Resilience +0.33 (+0.47), Witchmail +0.26 (+0.44), Dispel Magic +0.23 (+0.28)
- **Viscous**: Spirit Resilience +0.19 (+0.34), Spellbreaker +0.10 (+0.28), Divine Barrier +0.09 (+0.18)
- **Pocket**: Spirit Resilience +0.04 (+0.18), Witchmail +0.01 (+0.19), Reactive Barrier -0.01 (+0.01)
- **Mirage**: Dispel Magic +0.22 (+0.28), Metal Skin +0.02 (+0.12), Debuff Reducer +0.02 (+0.09)
- **Vyper**: Unstoppable +0.08 (+0.21), Spellbreaker +0.08 (+0.26), Debuff Reducer +0.05 (+0.12)
- **Sinclair**: Indomitable +0.15 (+0.26), Unstoppable +0.09 (+0.21), Debuff Reducer +0.06 (+0.13)
- **Mina**: Divine Barrier +0.07 (+0.16), Witchmail +0.05 (+0.23), Spirit Resilience +0.04 (+0.19)
- **Drifter**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Venator**: Bullet Resilience +0.21 (+0.28), Debuff Reducer +0.08 (+0.15), Plated Armor +0.08 (+0.18)
- **Victor**: Spellbreaker +0.06 (+0.23), Spirit Resilience +0.04 (+0.18), Healbane +0.03 (+0.10)
- **Paige**: Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.08), Reactive Barrier -0.01 (+0.01)
- **The Doorman**: Indomitable +0.16 (+0.27), Spirit Resilience +0.11 (+0.26), Witchmail +0.08 (+0.26)
- **Billy**: Reactive Barrier +0.02 (+0.04), Healbane +0.01 (+0.08), Counterspell -0.01 (+0.03)
- **Graves**: Spirit Resilience +0.17 (+0.32), Witchmail +0.14 (+0.32), Metal Skin +0.13 (+0.23)
- **Apollo**: Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.00), Healbane -0.02 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.21 (+0.36), Witchmail +0.15 (+0.33), Reactive Barrier +0.10 (+0.11)
- **Rem**: Debuff Reducer +0.13 (+0.20), Unstoppable +0.12 (+0.24), Spellbreaker +0.06 (+0.23)
- **Silver**: Reactive Barrier +0.05 (+0.06), Dispel Magic +0.04 (+0.09), Return Fire -0.00 (+0.06)
- **Celeste**: Spirit Resilience +0.10 (+0.24), Witchmail +0.09 (+0.27), Healbane +0.05 (+0.12)
- **Rat King**: Return Fire -0.00 (+0.06), Bullet Resilience -0.01 (+0.05), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.03 (+0.05), Healbane -0.02 (+0.05), Counterspell -0.02 (+0.02)
- **Violet**: Witchmail +0.09 (+0.27), Divine Barrier +0.05 (+0.14), Unstoppable +0.05 (+0.17)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Divine Barrier +0.03 (+0.12), Spirit Resilience +0.01 (+0.16)
- **Baba**: Healbane -0.01 (+0.06), Reactive Barrier -0.01 (+0.01), Counterspell -0.02 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.137 | +0.043 | +0.142 | Lash +0.44, Viscous +0.40, The Doorman +0.34 | 16 heroes |
| Indomitable | 6,400 | +0.169 | +0.027 | +0.123 | Wraith +0.38, The Doorman +0.28, Sinclair +0.18 | 3 heroes |
| Spellbreaker | 6,400 | +0.167 | +0.026 | +0.202 | Lash +0.29, Viscous +0.24, Grey Talon +0.22 | 0 heroes |
| Dispel Magic | 3,200 | +0.082 | +0.026 | +0.049 | Mirage +0.21, Lash +0.17, Silver +0.12 | 11 heroes |
| Divine Barrier | 6,400 | +0.153 | +0.024 | +0.080 | Viscous +0.26, Lash +0.24, The Doorman +0.10 | 2 heroes |
| Witchmail | 6,400 | +0.100 | +0.016 | +0.172 | Lash +0.27, The Doorman +0.25, Viscous +0.20 | 1 heroes |
| Healbane | 1,600 | +0.013 | +0.008 | +0.060 | Yamato +0.07, Victor +0.07, Infernus +0.06 | 21 heroes |
| Debuff Reducer | 1,600 | +0.012 | +0.007 | +0.094 | Paige +0.21, Grey Talon +0.17, Bebop +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | +0.023 | +0.007 | +0.062 | Vindicta +0.14, Venator +0.13, Viscous +0.11 | 1 heroes |
| Plated Armor | 6,400 | +0.040 | +0.006 | +0.103 | Haze +0.12, Vindicta +0.12, Lash +0.09 | 3 heroes |
| Unstoppable | 6,400 | +0.016 | +0.003 | +0.157 | Paige +0.28, Paradox +0.20, Grey Talon +0.19 | 5 heroes |
| Counterspell | 3,200 | -0.032 | -0.010 | +0.031 | Viscous +0.09, Lash +0.08, Celeste +0.04 | 1 heroes |
| Reactive Barrier | 1,600 | -0.017 | -0.011 | +0.015 | Deadman Danny +0.10, Celeste +0.05, Grey Talon +0.03 | 2 heroes |
| Metal Skin | 3,200 | -0.086 | -0.027 | +0.086 | Wraith +0.18, Lash +0.17, Viscous +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.082 | -0.051 | +0.054 | Viscous +0.11, Vindicta +0.11, Lash +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.16 (+0.31), Dispel Magic +0.11 (+0.16), Spellbreaker +0.11 (+0.31)
- **Seven**: Witchmail +0.05 (+0.22), Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Vindicta**: Bullet Resilience +0.14 (+0.20), Plated Armor +0.12 (+0.22), Return Fire +0.11 (+0.17)
- **Lady Geist**: Healbane +0.06 (+0.12), Spirit Resilience +0.03 (+0.17), Spellbreaker +0.03 (+0.23)
- **Abrams**: Dispel Magic +0.02 (+0.07), Unstoppable +0.02 (+0.18), Healbane +0.02 (+0.08)
- **Wraith**: Indomitable +0.38 (+0.50), Spellbreaker +0.19 (+0.39), Metal Skin +0.18 (+0.26)
- **McGinnis**: Dispel Magic +0.03 (+0.08), Spirit Resilience +0.02 (+0.16), Witchmail +0.02 (+0.19)
- **Paradox**: Unstoppable +0.20 (+0.35), Witchmail +0.16 (+0.33), Indomitable +0.14 (+0.26)
- **Dynamo**: Healbane -0.00 (+0.06), Reactive Barrier -0.01 (+0.01), Counterspell -0.02 (+0.01)
- **Kelvin**: Spirit Resilience +0.03 (+0.17), Healbane +0.01 (+0.07), Reactive Barrier -0.00 (+0.01)
- **Haze**: Unstoppable +0.17 (+0.33), Plated Armor +0.12 (+0.23), Bullet Resilience +0.10 (+0.16)
- **Holliday**: Debuff Reducer +0.06 (+0.16), Spellbreaker +0.05 (+0.25), Reactive Barrier +0.01 (+0.03)
- **Bebop**: Debuff Reducer +0.16 (+0.26), Unstoppable +0.12 (+0.27), Spellbreaker +0.07 (+0.28)
- **Calico**: Spirit Resilience +0.05 (+0.19), Reactive Barrier -0.01 (+0.01), Divine Barrier -0.01 (+0.07)
- **Grey Talon**: Spellbreaker +0.22 (+0.42), Spirit Resilience +0.20 (+0.34), Unstoppable +0.19 (+0.35)
- **Mo & Krill**: Spellbreaker +0.15 (+0.35), Debuff Reducer +0.13 (+0.22), Indomitable +0.13 (+0.25)
- **Shiv**: Bullet Resilience +0.10 (+0.16), Divine Barrier +0.05 (+0.13), Plated Armor +0.05 (+0.15)
- **Ivy**: Unstoppable +0.05 (+0.20), Plated Armor +0.02 (+0.12), Healbane -0.00 (+0.06)
- **Warden**: Plated Armor +0.07 (+0.17), Debuff Reducer +0.05 (+0.14), Spellbreaker +0.03 (+0.23)
- **Yamato**: Healbane +0.07 (+0.13), Counterspell +0.02 (+0.05), Return Fire +0.01 (+0.06)
- **Lash**: Spirit Resilience +0.44 (+0.58), Spellbreaker +0.29 (+0.49), Witchmail +0.27 (+0.44)
- **Viscous**: Spirit Resilience +0.40 (+0.54), Divine Barrier +0.26 (+0.34), Spellbreaker +0.24 (+0.44)
- **Pocket**: Spirit Resilience +0.01 (+0.15), Reactive Barrier -0.01 (+0.01), Counterspell -0.01 (+0.02)
- **Mirage**: Dispel Magic +0.21 (+0.26), Spellbreaker +0.07 (+0.27), Reactive Barrier -0.02 (-0.00)
- **Vyper**: Debuff Reducer +0.15 (+0.24), Unstoppable +0.10 (+0.26), Spellbreaker +0.07 (+0.27)
- **Sinclair**: Indomitable +0.18 (+0.30), Debuff Reducer +0.05 (+0.14), Reactive Barrier +0.03 (+0.04)
- **Mina**: Divine Barrier +0.01 (+0.09), Counterspell +0.01 (+0.04), Reactive Barrier -0.01 (+0.01)
- **Drifter**: Dispel Magic +0.09 (+0.14), Reactive Barrier +0.03 (+0.04), Return Fire +0.02 (+0.07)
- **Venator**: Bullet Resilience +0.13 (+0.20), Metal Skin +0.07 (+0.15), Return Fire +0.03 (+0.09)
- **Victor**: Spellbreaker +0.09 (+0.29), Healbane +0.07 (+0.12), Spirit Resilience +0.05 (+0.19)
- **Paige**: Unstoppable +0.28 (+0.44), Debuff Reducer +0.21 (+0.30), Spellbreaker +0.11 (+0.31)
- **The Doorman**: Spirit Resilience +0.34 (+0.48), Indomitable +0.28 (+0.40), Witchmail +0.25 (+0.42)
- **Billy**: Reactive Barrier +0.03 (+0.04), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Graves**: Reactive Barrier +0.03 (+0.04), Return Fire +0.02 (+0.08), Witchmail +0.00 (+0.17)
- **Apollo**: Healbane +0.02 (+0.08), Reactive Barrier -0.01 (+0.00), Counterspell -0.02 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.29 (+0.43), Spellbreaker +0.21 (+0.41), Witchmail +0.16 (+0.33)
- **Rem**: Spirit Resilience +0.09 (+0.23), Divine Barrier +0.09 (+0.17), Witchmail +0.03 (+0.21)
- **Silver**: Dispel Magic +0.12 (+0.17), Metal Skin +0.12 (+0.20), Bullet Resilience +0.05 (+0.11)
- **Celeste**: Witchmail +0.14 (+0.31), Spirit Resilience +0.10 (+0.24), Plated Armor +0.06 (+0.16)
- **Rat King**: Healbane -0.00 (+0.06), Metal Skin -0.01 (+0.08), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.01 (+0.03), Counterspell +0.00 (+0.03), Return Fire -0.02 (+0.04)
- **Violet**: Witchmail +0.09 (+0.26), Dispel Magic +0.04 (+0.09), Spirit Resilience +0.04 (+0.18)
- **Nurse Harrow**: Spirit Resilience +0.19 (+0.34), Healbane +0.04 (+0.10), Witchmail +0.04 (+0.21)
- **Baba**: Counterspell +0.01 (+0.04), Healbane +0.01 (+0.07), Unstoppable -0.00 (+0.16)
