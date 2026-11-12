# Counter items in the sim (phantom and up)

Built 2026-11-12T00:30:52Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.130 | Lash +0.21, The Doorman +0.17, Celeste +0.15 | 0 heroes |
| Divine Barrier | 6,400 | +0.254 | +0.041 | +0.126 | Lash +0.17, Viscous +0.16, Abrams +0.13 | 0 heroes |
| Dispel Magic | 3,200 | +0.109 | +0.034 | +0.083 | Mirage +0.37, Lash +0.10, Paradox +0.10 | 4 heroes |
| Indomitable | 6,400 | +0.152 | +0.024 | +0.133 | Abrams +0.22, The Doorman +0.21, Wraith +0.18 | 0 heroes |
| Debuff Reducer | 1,600 | +0.029 | +0.018 | +0.082 | Holliday +0.11, Vyper +0.11, Venator +0.09 | 0 heroes |
| Witchmail | 6,400 | +0.100 | +0.016 | +0.205 | Lash +0.18, Deadman Danny +0.16, The Doorman +0.15 | 0 heroes |
| Bullet Resilience | 3,200 | +0.048 | +0.015 | +0.102 | Venator +0.27, Lash +0.15, Paradox +0.13 | 0 heroes |
| Spellbreaker | 6,400 | +0.080 | +0.013 | +0.178 | Lash +0.21, Lady Geist +0.19, Deadman Danny +0.17 | 0 heroes |
| Reactive Barrier | 1,600 | +0.017 | +0.010 | +0.038 | Deadman Danny +0.12, Graves +0.10, Holliday +0.06 | 2 heroes |
| Healbane | 1,600 | +0.006 | +0.004 | +0.082 | Graves +0.10, Yamato +0.07, Lady Geist +0.05 | 22 heroes |
| Plated Armor | 6,400 | +0.000 | +0.000 | +0.136 | Holliday +0.23, Wraith +0.13, Lash +0.13 | 0 heroes |
| Unstoppable | 6,400 | -0.054 | -0.008 | +0.136 | Deadman Danny +0.12, Lash +0.11, Holliday +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.040 | -0.013 | +0.073 | Lash +0.09, Graves +0.07, Deadman Danny +0.07 | 0 heroes |
| Metal Skin | 3,200 | -0.182 | -0.057 | +0.115 | Wraith +0.23, Lash +0.18, Paradox +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.193 | -0.121 | +0.085 | Paradox +0.11, Holliday +0.06, Violet +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.05 (+0.13), Spellbreaker +0.04 (+0.21), Unstoppable +0.03 (+0.17)
- **Seven**: Healbane -0.00 (+0.08), Reactive Barrier -0.02 (+0.02), Spirit Resilience -0.03 (+0.10)
- **Vindicta**: Divine Barrier -0.00 (+0.12), Counterspell -0.01 (+0.07), Healbane -0.01 (+0.08)
- **Lady Geist**: Spellbreaker +0.19 (+0.37), Spirit Resilience +0.15 (+0.28), Witchmail +0.08 (+0.28)
- **Abrams**: Indomitable +0.22 (+0.35), Divine Barrier +0.13 (+0.25), Witchmail +0.08 (+0.29)
- **Wraith**: Metal Skin +0.23 (+0.34), Indomitable +0.18 (+0.31), Spellbreaker +0.16 (+0.34)
- **McGinnis**: Healbane +0.05 (+0.13), Spirit Resilience +0.01 (+0.14), Reactive Barrier +0.00 (+0.04)
- **Paradox**: Metal Skin +0.16 (+0.27), Bullet Resilience +0.13 (+0.23), Return Fire +0.11 (+0.19)
- **Dynamo**: Healbane +0.00 (+0.08), Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.05)
- **Kelvin**: Witchmail +0.02 (+0.23), Healbane +0.01 (+0.09), Spirit Resilience +0.01 (+0.14)
- **Haze**: Indomitable +0.07 (+0.21), Plated Armor +0.06 (+0.20), Bullet Resilience +0.04 (+0.15)
- **Holliday**: Plated Armor +0.23 (+0.37), Spellbreaker +0.14 (+0.32), Debuff Reducer +0.11 (+0.20)
- **Bebop**: Healbane +0.02 (+0.11), Counterspell +0.01 (+0.08), Divine Barrier -0.01 (+0.12)
- **Calico**: Spellbreaker +0.08 (+0.26), Divine Barrier +0.06 (+0.18), Spirit Resilience +0.05 (+0.18)
- **Grey Talon**: Unstoppable +0.07 (+0.20), Debuff Reducer +0.04 (+0.12), Reactive Barrier +0.04 (+0.08)
- **Mo & Krill**: Spellbreaker +0.07 (+0.25), Witchmail +0.04 (+0.25), Spirit Resilience +0.04 (+0.17)
- **Shiv**: Healbane -0.00 (+0.08), Return Fire -0.00 (+0.08), Bullet Resilience -0.02 (+0.08)
- **Ivy**: Indomitable +0.08 (+0.22), Unstoppable +0.04 (+0.17), Debuff Reducer +0.01 (+0.09)
- **Warden**: Return Fire +0.01 (+0.09), Debuff Reducer -0.00 (+0.08), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.07 (+0.15), Debuff Reducer +0.06 (+0.14), Unstoppable +0.06 (+0.19)
- **Lash**: Spellbreaker +0.21 (+0.38), Spirit Resilience +0.21 (+0.34), Witchmail +0.18 (+0.39)
- **Viscous**: Divine Barrier +0.16 (+0.29), Spirit Resilience +0.09 (+0.22), Spellbreaker +0.08 (+0.26)
- **Pocket**: Return Fire +0.01 (+0.09), Counterspell +0.01 (+0.08), Witchmail +0.00 (+0.21)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spellbreaker +0.13 (+0.30), Spirit Resilience +0.12 (+0.25)
- **Vyper**: Debuff Reducer +0.11 (+0.19), Unstoppable +0.09 (+0.23), Spellbreaker +0.09 (+0.26)
- **Sinclair**: Indomitable +0.15 (+0.28), Spellbreaker +0.07 (+0.25), Unstoppable +0.06 (+0.20)
- **Mina**: Return Fire +0.02 (+0.10), Counterspell -0.01 (+0.06), Witchmail -0.02 (+0.19)
- **Drifter**: Reactive Barrier -0.01 (+0.02), Return Fire -0.01 (+0.07), Counterspell -0.02 (+0.06)
- **Venator**: Bullet Resilience +0.27 (+0.37), Debuff Reducer +0.09 (+0.17), Unstoppable +0.08 (+0.22)
- **Victor**: Spirit Resilience +0.11 (+0.24), Spellbreaker +0.10 (+0.28), Witchmail -0.01 (+0.20)
- **Paige**: Reactive Barrier -0.01 (+0.02), Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.06)
- **The Doorman**: Indomitable +0.21 (+0.35), Spirit Resilience +0.17 (+0.30), Witchmail +0.15 (+0.35)
- **Billy**: Spellbreaker +0.03 (+0.21), Spirit Resilience +0.03 (+0.16), Witchmail +0.01 (+0.21)
- **Graves**: Reactive Barrier +0.10 (+0.14), Healbane +0.10 (+0.18), Metal Skin +0.09 (+0.21)
- **Apollo**: Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.04), Healbane -0.04 (+0.04)
- **Deadman Danny**: Spellbreaker +0.17 (+0.35), Witchmail +0.16 (+0.36), Spirit Resilience +0.14 (+0.27)
- **Rem**: Healbane -0.01 (+0.07), Reactive Barrier -0.02 (+0.02), Counterspell -0.02 (+0.05)
- **Silver**: Dispel Magic +0.09 (+0.17), Reactive Barrier +0.05 (+0.08), Debuff Reducer +0.01 (+0.10)
- **Celeste**: Spirit Resilience +0.15 (+0.28), Witchmail +0.12 (+0.32), Dispel Magic +0.06 (+0.14)
- **Rat King**: Return Fire +0.00 (+0.09), Counterspell -0.01 (+0.06), Divine Barrier -0.01 (+0.11)
- **Solomon**: Reactive Barrier -0.00 (+0.04), Counterspell -0.03 (+0.05), Return Fire -0.03 (+0.06)
- **Violet**: Return Fire +0.06 (+0.14), Unstoppable +0.06 (+0.19), Witchmail +0.03 (+0.23)
- **Nurse Harrow**: Healbane +0.04 (+0.12), Reactive Barrier +0.01 (+0.04), Counterspell -0.04 (+0.03)
- **Baba**: Reactive Barrier -0.00 (+0.04), Healbane -0.00 (+0.08), Counterspell -0.02 (+0.06)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.143 | Lash +0.43, Celeste +0.23, Lady Geist +0.21 | 9 heroes |
| Divine Barrier | 6,400 | +0.210 | +0.033 | +0.096 | Lash +0.26, Paradox +0.10, Abrams +0.09 | 1 heroes |
| Dispel Magic | 3,200 | +0.101 | +0.032 | +0.069 | Mirage +0.24, Lash +0.15, Holliday +0.12 | 10 heroes |
| Indomitable | 6,400 | +0.144 | +0.023 | +0.105 | Lash +0.19, The Doorman +0.18, Wraith +0.17 | 0 heroes |
| Spellbreaker | 6,400 | +0.124 | +0.019 | +0.169 | Lash +0.33, Holliday +0.20, Lady Geist +0.19 | 0 heroes |
| Witchmail | 6,400 | +0.116 | +0.018 | +0.185 | Lash +0.28, Celeste +0.20, Lady Geist +0.09 | 1 heroes |
| Bullet Resilience | 3,200 | +0.022 | +0.007 | +0.070 | Venator +0.21, Paradox +0.14, Lash +0.11 | 1 heroes |
| Debuff Reducer | 1,600 | +0.008 | +0.005 | +0.064 | Holliday +0.21, Rem +0.12, Venator +0.07 | 0 heroes |
| Plated Armor | 6,400 | +0.006 | +0.001 | +0.096 | Paradox +0.12, Lash +0.10, Wraith +0.08 | 0 heroes |
| Reactive Barrier | 1,600 | +0.000 | +0.000 | +0.020 | Abrams +0.08, Deadman Danny +0.06, Holliday +0.06 | 4 heroes |
| Healbane | 1,600 | -0.004 | -0.002 | +0.065 | Lady Geist +0.09, Abrams +0.08, Yamato +0.07 | 23 heroes |
| Unstoppable | 6,400 | -0.073 | -0.011 | +0.113 | Holliday +0.19, Rem +0.12, Abrams +0.11 | 0 heroes |
| Counterspell | 3,200 | -0.054 | -0.017 | +0.044 | Lash +0.05, Nurse Harrow +0.03, Pocket +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.199 | -0.062 | +0.087 | Wraith +0.25, Lash +0.20, Paradox +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.201 | -0.126 | +0.061 | Paradox +0.07, Deadman Danny +0.05, Venator +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.10 (+0.27), Unstoppable +0.10 (+0.21), Dispel Magic +0.07 (+0.14)
- **Seven**: Witchmail +0.04 (+0.22), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Divine Barrier +0.05 (+0.15), Return Fire +0.05 (+0.11), Witchmail +0.03 (+0.22)
- **Lady Geist**: Spirit Resilience +0.21 (+0.35), Spellbreaker +0.19 (+0.36), Healbane +0.09 (+0.15)
- **Abrams**: Indomitable +0.12 (+0.23), Unstoppable +0.11 (+0.22), Spirit Resilience +0.09 (+0.23)
- **Wraith**: Metal Skin +0.25 (+0.33), Indomitable +0.17 (+0.28), Spellbreaker +0.12 (+0.29)
- **McGinnis**: Spirit Resilience +0.07 (+0.21), Witchmail +0.02 (+0.20), Healbane +0.00 (+0.07)
- **Paradox**: Metal Skin +0.15 (+0.24), Bullet Resilience +0.14 (+0.21), Indomitable +0.12 (+0.23)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.00)
- **Kelvin**: Spirit Resilience +0.07 (+0.22), Witchmail +0.03 (+0.22), Spellbreaker +0.01 (+0.18)
- **Haze**: Indomitable +0.09 (+0.20), Plated Armor +0.06 (+0.16), Bullet Resilience +0.04 (+0.11)
- **Holliday**: Debuff Reducer +0.21 (+0.27), Spellbreaker +0.20 (+0.37), Unstoppable +0.19 (+0.30)
- **Bebop**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01)
- **Calico**: Divine Barrier +0.05 (+0.15), Spirit Resilience +0.03 (+0.18), Dispel Magic +0.01 (+0.08)
- **Grey Talon**: Unstoppable +0.09 (+0.21), Debuff Reducer +0.05 (+0.11), Spellbreaker +0.04 (+0.21)
- **Mo & Krill**: Spellbreaker +0.10 (+0.26), Unstoppable +0.09 (+0.20), Dispel Magic +0.04 (+0.11)
- **Shiv**: Bullet Resilience +0.06 (+0.13), Plated Armor +0.04 (+0.13), Metal Skin +0.04 (+0.13)
- **Ivy**: Unstoppable +0.02 (+0.14), Debuff Reducer +0.01 (+0.07), Indomitable +0.00 (+0.11)
- **Warden**: Return Fire +0.02 (+0.09), Divine Barrier -0.00 (+0.09), Debuff Reducer -0.01 (+0.05)
- **Yamato**: Healbane +0.07 (+0.14), Debuff Reducer +0.00 (+0.07), Reactive Barrier -0.01 (+0.01)
- **Lash**: Spirit Resilience +0.43 (+0.58), Spellbreaker +0.33 (+0.50), Witchmail +0.28 (+0.46)
- **Viscous**: Divine Barrier +0.03 (+0.13), Counterspell +0.01 (+0.05), Healbane -0.00 (+0.06)
- **Pocket**: Spirit Resilience +0.19 (+0.33), Witchmail +0.07 (+0.25), Spellbreaker +0.06 (+0.23)
- **Mirage**: Dispel Magic +0.24 (+0.31), Metal Skin +0.04 (+0.13), Spellbreaker +0.02 (+0.19)
- **Vyper**: Spellbreaker +0.08 (+0.25), Debuff Reducer +0.07 (+0.14), Unstoppable +0.06 (+0.17)
- **Sinclair**: Indomitable +0.13 (+0.23), Spellbreaker +0.03 (+0.19), Debuff Reducer +0.02 (+0.09)
- **Mina**: Counterspell +0.00 (+0.05), Plated Armor +0.00 (+0.10), Return Fire -0.00 (+0.06)
- **Drifter**: Return Fire +0.01 (+0.07), Counterspell -0.00 (+0.04), Healbane -0.00 (+0.06)
- **Venator**: Bullet Resilience +0.21 (+0.28), Debuff Reducer +0.07 (+0.14), Unstoppable +0.06 (+0.17)
- **Victor**: Spirit Resilience +0.10 (+0.24), Spellbreaker +0.07 (+0.24), Healbane +0.02 (+0.09)
- **Paige**: Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01), Return Fire -0.03 (+0.04)
- **The Doorman**: Indomitable +0.18 (+0.28), Spirit Resilience +0.10 (+0.24), Spellbreaker +0.09 (+0.26)
- **Billy**: Healbane +0.00 (+0.07), Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.05)
- **Graves**: Metal Skin +0.11 (+0.20), Spirit Resilience +0.07 (+0.22), Witchmail +0.06 (+0.24)
- **Apollo**: Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (-0.00), Healbane -0.03 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.10 (+0.24), Witchmail +0.08 (+0.27), Indomitable +0.06 (+0.17)
- **Rem**: Debuff Reducer +0.12 (+0.19), Unstoppable +0.12 (+0.23), Spellbreaker +0.03 (+0.20)
- **Silver**: Dispel Magic +0.11 (+0.18), Reactive Barrier +0.04 (+0.06), Debuff Reducer +0.01 (+0.07)
- **Celeste**: Spirit Resilience +0.23 (+0.37), Witchmail +0.20 (+0.38), Spellbreaker +0.11 (+0.27)
- **Rat King**: Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Solomon**: Return Fire -0.01 (+0.05), Reactive Barrier -0.01 (+0.01), Counterspell -0.01 (+0.03)
- **Violet**: Unstoppable +0.07 (+0.18), Witchmail +0.06 (+0.25), Healbane +0.05 (+0.11)
- **Nurse Harrow**: Healbane +0.06 (+0.13), Divine Barrier +0.06 (+0.15), Witchmail +0.03 (+0.22)
- **Baba**: Unstoppable +0.02 (+0.13), Debuff Reducer -0.00 (+0.06), Healbane -0.00 (+0.06)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.182 | +0.057 | +0.144 | Lash +0.33, Deadman Danny +0.21, Viscous +0.19 | 12 heroes |
| Dispel Magic | 3,200 | +0.100 | +0.031 | +0.058 | Lash +0.22, Mirage +0.22, Infernus +0.11 | 10 heroes |
| Divine Barrier | 6,400 | +0.164 | +0.026 | +0.090 | Lash +0.22, Viscous +0.08, Vindicta +0.07 | 2 heroes |
| Indomitable | 6,400 | +0.146 | +0.023 | +0.111 | Wraith +0.21, Haze +0.21, Lash +0.18 | 0 heroes |
| Spellbreaker | 6,400 | +0.138 | +0.021 | +0.175 | Lash +0.21, Wraith +0.19, Holliday +0.17 | 0 heroes |
| Witchmail | 6,400 | +0.107 | +0.017 | +0.184 | Lash +0.26, Deadman Danny +0.15, Graves +0.14 | 1 heroes |
| Debuff Reducer | 1,600 | +0.012 | +0.007 | +0.070 | Holliday +0.16, Grey Talon +0.13, Rem +0.13 | 0 heroes |
| Bullet Resilience | 3,200 | +0.022 | +0.007 | +0.067 | Venator +0.21, Lash +0.20, Vindicta +0.12 | 1 heroes |
| Plated Armor | 6,400 | +0.012 | +0.002 | +0.103 | Holliday +0.21, Lash +0.18, Haze +0.12 | 0 heroes |
| Healbane | 1,600 | -0.007 | -0.005 | +0.067 | Mo & Krill +0.08, Lady Geist +0.08, Infernus +0.07 | 25 heroes |
| Unstoppable | 6,400 | -0.070 | -0.011 | +0.124 | Mo & Krill +0.21, Haze +0.17, Grey Talon +0.15 | 4 heroes |
| Reactive Barrier | 1,600 | -0.026 | -0.016 | +0.017 | Deadman Danny +0.10, Grey Talon +0.06, Silver +0.05 | 2 heroes |
| Counterspell | 3,200 | -0.058 | -0.018 | +0.039 | Lash +0.06, Viscous +0.04, Vindicta +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.193 | -0.060 | +0.096 | Wraith +0.23, Lash +0.21, Graves +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.195 | -0.122 | +0.060 | Haze +0.11, Venator +0.07, Vindicta +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.17), Spellbreaker +0.09 (+0.27), Healbane +0.07 (+0.14)
- **Seven**: Witchmail +0.08 (+0.26), Spirit Resilience +0.06 (+0.20), Reactive Barrier +0.01 (+0.03)
- **Vindicta**: Bullet Resilience +0.12 (+0.18), Plated Armor +0.08 (+0.19), Return Fire +0.07 (+0.13)
- **Lady Geist**: Healbane +0.08 (+0.15), Spellbreaker +0.05 (+0.23), Spirit Resilience +0.02 (+0.17)
- **Abrams**: Unstoppable +0.07 (+0.20), Dispel Magic +0.04 (+0.10), Reactive Barrier +0.04 (+0.05)
- **Wraith**: Metal Skin +0.23 (+0.33), Indomitable +0.21 (+0.32), Spellbreaker +0.19 (+0.36)
- **McGinnis**: Spirit Resilience +0.08 (+0.23), Witchmail +0.02 (+0.21), Counterspell +0.01 (+0.05)
- **Paradox**: Dispel Magic +0.07 (+0.12), Return Fire +0.05 (+0.11), Indomitable +0.04 (+0.15)
- **Dynamo**: Healbane +0.00 (+0.07), Counterspell -0.02 (+0.02), Reactive Barrier -0.02 (-0.00)
- **Kelvin**: Spirit Resilience +0.05 (+0.19), Counterspell +0.02 (+0.06), Debuff Reducer -0.01 (+0.06)
- **Haze**: Indomitable +0.21 (+0.32), Unstoppable +0.17 (+0.30), Plated Armor +0.12 (+0.22)
- **Holliday**: Plated Armor +0.21 (+0.31), Spellbreaker +0.17 (+0.34), Debuff Reducer +0.16 (+0.23)
- **Bebop**: Healbane +0.04 (+0.10), Divine Barrier +0.01 (+0.10), Counterspell +0.01 (+0.05)
- **Calico**: Spirit Resilience +0.11 (+0.26), Dispel Magic +0.03 (+0.09), Divine Barrier +0.03 (+0.12)
- **Grey Talon**: Unstoppable +0.15 (+0.27), Debuff Reducer +0.13 (+0.20), Spellbreaker +0.12 (+0.30)
- **Mo & Krill**: Unstoppable +0.21 (+0.34), Spellbreaker +0.12 (+0.29), Healbane +0.08 (+0.15)
- **Shiv**: Bullet Resilience +0.05 (+0.11), Divine Barrier +0.01 (+0.10), Return Fire +0.00 (+0.06)
- **Ivy**: Indomitable +0.04 (+0.15), Unstoppable +0.02 (+0.14), Metal Skin +0.01 (+0.10)
- **Warden**: Debuff Reducer +0.01 (+0.08), Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Yamato**: Healbane +0.06 (+0.13), Witchmail +0.04 (+0.23), Debuff Reducer +0.04 (+0.11)
- **Lash**: Spirit Resilience +0.33 (+0.47), Witchmail +0.26 (+0.44), Dispel Magic +0.22 (+0.28)
- **Viscous**: Spirit Resilience +0.19 (+0.33), Spellbreaker +0.10 (+0.28), Divine Barrier +0.08 (+0.17)
- **Pocket**: Spirit Resilience +0.04 (+0.18), Witchmail +0.01 (+0.19), Reactive Barrier -0.01 (+0.01)
- **Mirage**: Dispel Magic +0.22 (+0.27), Metal Skin +0.02 (+0.12), Debuff Reducer +0.02 (+0.09)
- **Vyper**: Unstoppable +0.08 (+0.21), Spellbreaker +0.08 (+0.25), Debuff Reducer +0.05 (+0.12)
- **Sinclair**: Indomitable +0.17 (+0.28), Unstoppable +0.10 (+0.22), Debuff Reducer +0.07 (+0.14)
- **Mina**: Divine Barrier +0.06 (+0.15), Witchmail +0.05 (+0.23), Spirit Resilience +0.04 (+0.19)
- **Drifter**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Venator**: Bullet Resilience +0.21 (+0.28), Debuff Reducer +0.08 (+0.15), Plated Armor +0.08 (+0.18)
- **Victor**: Spellbreaker +0.05 (+0.23), Spirit Resilience +0.03 (+0.17), Healbane +0.02 (+0.09)
- **Paige**: Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.08), Reactive Barrier -0.01 (+0.01)
- **The Doorman**: Indomitable +0.16 (+0.27), Spirit Resilience +0.11 (+0.25), Witchmail +0.08 (+0.26)
- **Billy**: Reactive Barrier +0.02 (+0.04), Healbane +0.01 (+0.08), Counterspell -0.01 (+0.03)
- **Graves**: Spirit Resilience +0.17 (+0.32), Witchmail +0.14 (+0.32), Metal Skin +0.13 (+0.22)
- **Apollo**: Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.00), Healbane -0.02 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.21 (+0.36), Witchmail +0.15 (+0.33), Reactive Barrier +0.10 (+0.11)
- **Rem**: Debuff Reducer +0.13 (+0.20), Unstoppable +0.11 (+0.24), Spellbreaker +0.06 (+0.23)
- **Silver**: Reactive Barrier +0.05 (+0.06), Dispel Magic +0.04 (+0.09), Return Fire -0.00 (+0.06)
- **Celeste**: Spirit Resilience +0.10 (+0.24), Witchmail +0.09 (+0.27), Healbane +0.05 (+0.12)
- **Rat King**: Return Fire -0.00 (+0.06), Bullet Resilience -0.01 (+0.05), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.03 (+0.05), Healbane -0.02 (+0.05), Counterspell -0.02 (+0.02)
- **Violet**: Witchmail +0.10 (+0.28), Divine Barrier +0.05 (+0.14), Unstoppable +0.05 (+0.17)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Divine Barrier +0.01 (+0.10), Spirit Resilience +0.01 (+0.15)
- **Baba**: Healbane -0.01 (+0.06), Reactive Barrier -0.01 (+0.01), Counterspell -0.02 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.172 | +0.054 | +0.142 | Lash +0.45, Viscous +0.39, The Doorman +0.34 | 16 heroes |
| Dispel Magic | 3,200 | +0.099 | +0.031 | +0.049 | Mirage +0.21, Lash +0.17, Silver +0.12 | 11 heroes |
| Spellbreaker | 6,400 | +0.161 | +0.025 | +0.202 | Lash +0.29, Viscous +0.23, Grey Talon +0.22 | 0 heroes |
| Indomitable | 6,400 | +0.159 | +0.025 | +0.123 | Wraith +0.38, The Doorman +0.28, Sinclair +0.19 | 3 heroes |
| Divine Barrier | 6,400 | +0.153 | +0.024 | +0.081 | Viscous +0.26, Lash +0.24, The Doorman +0.09 | 2 heroes |
| Witchmail | 6,400 | +0.106 | +0.017 | +0.172 | Lash +0.27, The Doorman +0.25, Viscous +0.20 | 1 heroes |
| Debuff Reducer | 1,600 | +0.016 | +0.010 | +0.094 | Paige +0.21, Grey Talon +0.17, Bebop +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | +0.018 | +0.006 | +0.062 | Vindicta +0.14, Venator +0.13, Viscous +0.11 | 1 heroes |
| Plated Armor | 6,400 | +0.004 | +0.001 | +0.103 | Haze +0.12, Vindicta +0.12, Lash +0.09 | 3 heroes |
| Healbane | 1,600 | -0.013 | -0.008 | +0.060 | Yamato +0.07, Victor +0.06, Infernus +0.06 | 21 heroes |
| Unstoppable | 6,400 | -0.056 | -0.009 | +0.158 | Paige +0.28, Paradox +0.20, Grey Talon +0.19 | 5 heroes |
| Counterspell | 3,200 | -0.064 | -0.020 | +0.031 | Viscous +0.09, Lash +0.08, Celeste +0.04 | 1 heroes |
| Reactive Barrier | 1,600 | -0.037 | -0.023 | +0.015 | Deadman Danny +0.10, Celeste +0.05, Grey Talon +0.04 | 2 heroes |
| Metal Skin | 3,200 | -0.198 | -0.062 | +0.086 | Wraith +0.18, Lash +0.17, Viscous +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.190 | -0.119 | +0.054 | Viscous +0.11, Vindicta +0.11, Lash +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.31), Dispel Magic +0.11 (+0.16), Spellbreaker +0.11 (+0.31)
- **Seven**: Witchmail +0.06 (+0.24), Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Vindicta**: Bullet Resilience +0.14 (+0.20), Plated Armor +0.12 (+0.23), Return Fire +0.11 (+0.17)
- **Lady Geist**: Healbane +0.06 (+0.12), Spirit Resilience +0.03 (+0.17), Spellbreaker +0.03 (+0.23)
- **Abrams**: Dispel Magic +0.02 (+0.07), Unstoppable +0.02 (+0.18), Healbane +0.02 (+0.08)
- **Wraith**: Indomitable +0.38 (+0.50), Spellbreaker +0.19 (+0.39), Metal Skin +0.18 (+0.26)
- **McGinnis**: Dispel Magic +0.03 (+0.08), Spirit Resilience +0.02 (+0.16), Witchmail +0.02 (+0.19)
- **Paradox**: Unstoppable +0.20 (+0.35), Witchmail +0.16 (+0.33), Indomitable +0.14 (+0.26)
- **Dynamo**: Healbane -0.00 (+0.06), Reactive Barrier -0.01 (+0.01), Counterspell -0.02 (+0.01)
- **Kelvin**: Spirit Resilience +0.03 (+0.17), Healbane +0.01 (+0.07), Reactive Barrier -0.00 (+0.01)
- **Haze**: Unstoppable +0.17 (+0.33), Plated Armor +0.12 (+0.23), Bullet Resilience +0.10 (+0.16)
- **Holliday**: Debuff Reducer +0.06 (+0.16), Spellbreaker +0.05 (+0.25), Reactive Barrier +0.01 (+0.03)
- **Bebop**: Debuff Reducer +0.16 (+0.26), Unstoppable +0.12 (+0.27), Spellbreaker +0.08 (+0.28)
- **Calico**: Spirit Resilience +0.05 (+0.19), Reactive Barrier -0.01 (+0.01), Divine Barrier -0.01 (+0.07)
- **Grey Talon**: Spellbreaker +0.22 (+0.42), Spirit Resilience +0.21 (+0.35), Unstoppable +0.19 (+0.35)
- **Mo & Krill**: Spellbreaker +0.15 (+0.35), Debuff Reducer +0.13 (+0.22), Indomitable +0.12 (+0.25)
- **Shiv**: Bullet Resilience +0.10 (+0.16), Divine Barrier +0.05 (+0.13), Plated Armor +0.05 (+0.15)
- **Ivy**: Unstoppable +0.05 (+0.20), Plated Armor +0.02 (+0.12), Healbane -0.00 (+0.06)
- **Warden**: Plated Armor +0.07 (+0.17), Debuff Reducer +0.05 (+0.14), Spellbreaker +0.03 (+0.23)
- **Yamato**: Healbane +0.07 (+0.13), Counterspell +0.02 (+0.05), Return Fire +0.01 (+0.06)
- **Lash**: Spirit Resilience +0.45 (+0.59), Spellbreaker +0.29 (+0.49), Witchmail +0.27 (+0.44)
- **Viscous**: Spirit Resilience +0.39 (+0.54), Divine Barrier +0.26 (+0.34), Spellbreaker +0.23 (+0.44)
- **Pocket**: Spirit Resilience +0.01 (+0.15), Reactive Barrier -0.01 (+0.01), Counterspell -0.01 (+0.02)
- **Mirage**: Dispel Magic +0.21 (+0.26), Spellbreaker +0.07 (+0.27), Reactive Barrier -0.02 (-0.00)
- **Vyper**: Debuff Reducer +0.15 (+0.24), Unstoppable +0.10 (+0.26), Spellbreaker +0.07 (+0.27)
- **Sinclair**: Indomitable +0.19 (+0.31), Debuff Reducer +0.06 (+0.15), Spellbreaker +0.05 (+0.25)
- **Mina**: Divine Barrier +0.01 (+0.09), Counterspell +0.01 (+0.04), Reactive Barrier -0.01 (+0.01)
- **Drifter**: Dispel Magic +0.09 (+0.14), Reactive Barrier +0.03 (+0.04), Return Fire +0.02 (+0.07)
- **Venator**: Bullet Resilience +0.13 (+0.20), Metal Skin +0.07 (+0.15), Return Fire +0.03 (+0.09)
- **Victor**: Spellbreaker +0.09 (+0.29), Healbane +0.06 (+0.12), Spirit Resilience +0.05 (+0.20)
- **Paige**: Unstoppable +0.28 (+0.44), Debuff Reducer +0.21 (+0.30), Spellbreaker +0.11 (+0.31)
- **The Doorman**: Spirit Resilience +0.34 (+0.48), Indomitable +0.28 (+0.41), Witchmail +0.25 (+0.42)
- **Billy**: Reactive Barrier +0.03 (+0.04), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Graves**: Reactive Barrier +0.03 (+0.04), Return Fire +0.02 (+0.08), Witchmail +0.00 (+0.17)
- **Apollo**: Healbane +0.02 (+0.08), Reactive Barrier -0.01 (+0.00), Bullet Resilience -0.02 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.29 (+0.43), Spellbreaker +0.21 (+0.41), Witchmail +0.16 (+0.33)
- **Rem**: Spirit Resilience +0.09 (+0.23), Divine Barrier +0.09 (+0.17), Witchmail +0.03 (+0.21)
- **Silver**: Dispel Magic +0.12 (+0.17), Metal Skin +0.12 (+0.20), Bullet Resilience +0.05 (+0.11)
- **Celeste**: Witchmail +0.14 (+0.31), Spirit Resilience +0.10 (+0.24), Plated Armor +0.06 (+0.16)
- **Rat King**: Healbane -0.00 (+0.06), Metal Skin -0.01 (+0.08), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.01 (+0.03), Counterspell +0.00 (+0.03), Return Fire -0.02 (+0.04)
- **Violet**: Witchmail +0.09 (+0.26), Dispel Magic +0.04 (+0.09), Spirit Resilience +0.04 (+0.18)
- **Nurse Harrow**: Spirit Resilience +0.19 (+0.33), Healbane +0.06 (+0.12), Witchmail +0.05 (+0.23)
- **Baba**: Counterspell +0.01 (+0.04), Healbane +0.01 (+0.07), Unstoppable -0.00 (+0.16)
