# Counter items in the sim (phantom and up)

Built 2026-11-10T15:47:28Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.131 | Lash +0.22, Deadman Danny +0.18, The Doorman +0.16 | 1 heroes |
| Divine Barrier | 6,400 | +0.253 | +0.040 | +0.127 | Lash +0.16, Abrams +0.13, The Doorman +0.13 | 0 heroes |
| Dispel Magic | 3,200 | +0.101 | +0.032 | +0.086 | Mirage +0.40, Paradox +0.14, Lash +0.12 | 4 heroes |
| Indomitable | 6,400 | +0.155 | +0.025 | +0.137 | The Doorman +0.24, Abrams +0.22, Wraith +0.18 | 0 heroes |
| Witchmail | 6,400 | +0.102 | +0.016 | +0.205 | Lash +0.19, Deadman Danny +0.19, The Doorman +0.14 | 0 heroes |
| Bullet Resilience | 3,200 | +0.049 | +0.015 | +0.106 | Venator +0.27, Paradox +0.16, Lash +0.15 | 0 heroes |
| Debuff Reducer | 1,600 | +0.023 | +0.015 | +0.083 | Holliday +0.12, Vyper +0.11, Venator +0.09 | 0 heroes |
| Healbane | 1,600 | +0.021 | +0.013 | +0.081 | Graves +0.10, Yamato +0.07, McGinnis +0.07 | 22 heroes |
| Spellbreaker | 6,400 | +0.082 | +0.013 | +0.180 | Lash +0.21, Deadman Danny +0.21, Wraith +0.16 | 0 heroes |
| Reactive Barrier | 1,600 | +0.017 | +0.010 | +0.037 | Deadman Danny +0.13, Graves +0.10, Holliday +0.07 | 2 heroes |
| Plated Armor | 6,400 | +0.002 | +0.000 | +0.139 | Holliday +0.22, Wraith +0.13, Lash +0.13 | 0 heroes |
| Counterspell | 3,200 | -0.018 | -0.006 | +0.075 | Lash +0.10, Graves +0.07, McGinnis +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.053 | -0.008 | +0.139 | Deadman Danny +0.16, Lash +0.12, Holliday +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.181 | -0.057 | +0.118 | Wraith +0.23, Paradox +0.19, Lash +0.18 | 0 heroes |
| Return Fire | 1,600 | -0.190 | -0.118 | +0.088 | Paradox +0.09, Deadman Danny +0.07, Holliday +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.06 (+0.14), Spellbreaker +0.04 (+0.22), Unstoppable +0.04 (+0.18)
- **Seven**: Healbane -0.00 (+0.08), Reactive Barrier -0.02 (+0.02), Spirit Resilience -0.02 (+0.11)
- **Vindicta**: Divine Barrier -0.00 (+0.13), Counterspell -0.00 (+0.07), Healbane -0.00 (+0.08)
- **Lady Geist**: Return Fire +0.03 (+0.11), Divine Barrier +0.00 (+0.13), Counterspell -0.00 (+0.07)
- **Abrams**: Indomitable +0.22 (+0.35), Divine Barrier +0.13 (+0.26), Witchmail +0.09 (+0.30)
- **Wraith**: Metal Skin +0.23 (+0.35), Indomitable +0.18 (+0.32), Spellbreaker +0.16 (+0.34)
- **McGinnis**: Healbane +0.07 (+0.15), Counterspell +0.07 (+0.14), Spirit Resilience +0.06 (+0.19)
- **Paradox**: Metal Skin +0.19 (+0.31), Indomitable +0.17 (+0.30), Bullet Resilience +0.16 (+0.26)
- **Dynamo**: Healbane +0.00 (+0.08), Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.04)
- **Kelvin**: Witchmail +0.03 (+0.23), Healbane +0.01 (+0.09), Spirit Resilience +0.01 (+0.14)
- **Haze**: Indomitable +0.07 (+0.21), Plated Armor +0.06 (+0.20), Bullet Resilience +0.04 (+0.15)
- **Holliday**: Plated Armor +0.22 (+0.36), Spellbreaker +0.13 (+0.31), Debuff Reducer +0.12 (+0.20)
- **Bebop**: Healbane +0.03 (+0.11), Counterspell +0.01 (+0.08), Divine Barrier -0.01 (+0.12)
- **Calico**: Spellbreaker +0.07 (+0.25), Divine Barrier +0.05 (+0.18), Spirit Resilience +0.05 (+0.18)
- **Grey Talon**: Unstoppable +0.07 (+0.21), Reactive Barrier +0.04 (+0.08), Debuff Reducer +0.04 (+0.13)
- **Mo & Krill**: Spellbreaker +0.07 (+0.25), Spirit Resilience +0.04 (+0.17), Witchmail +0.04 (+0.25)
- **Shiv**: Healbane -0.00 (+0.08), Return Fire -0.01 (+0.08), Divine Barrier -0.02 (+0.11)
- **Ivy**: Indomitable +0.08 (+0.22), Unstoppable +0.03 (+0.17), Debuff Reducer +0.00 (+0.09)
- **Warden**: Return Fire +0.00 (+0.09), Debuff Reducer -0.00 (+0.08), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.07 (+0.15), Debuff Reducer +0.05 (+0.13), Unstoppable +0.05 (+0.19)
- **Lash**: Spirit Resilience +0.22 (+0.35), Spellbreaker +0.21 (+0.39), Witchmail +0.19 (+0.39)
- **Viscous**: Divine Barrier +0.06 (+0.19), Healbane +0.04 (+0.12), Debuff Reducer +0.03 (+0.12)
- **Pocket**: Return Fire +0.01 (+0.10), Counterspell +0.01 (+0.09), Witchmail +0.01 (+0.21)
- **Mirage**: Dispel Magic +0.40 (+0.49), Spellbreaker +0.14 (+0.31), Spirit Resilience +0.13 (+0.27)
- **Vyper**: Debuff Reducer +0.11 (+0.19), Unstoppable +0.09 (+0.23), Spellbreaker +0.08 (+0.26)
- **Sinclair**: Indomitable +0.14 (+0.28), Spellbreaker +0.07 (+0.25), Unstoppable +0.05 (+0.19)
- **Mina**: Return Fire +0.01 (+0.10), Counterspell -0.01 (+0.06), Reactive Barrier -0.02 (+0.02)
- **Drifter**: Reactive Barrier -0.01 (+0.02), Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.07)
- **Venator**: Bullet Resilience +0.27 (+0.38), Debuff Reducer +0.09 (+0.18), Unstoppable +0.09 (+0.23)
- **Victor**: Spirit Resilience +0.11 (+0.25), Spellbreaker +0.10 (+0.28), Witchmail +0.01 (+0.21)
- **Paige**: Reactive Barrier -0.01 (+0.03), Counterspell -0.02 (+0.06), Healbane -0.02 (+0.06)
- **The Doorman**: Indomitable +0.24 (+0.38), Spirit Resilience +0.16 (+0.29), Spellbreaker +0.15 (+0.33)
- **Billy**: Spellbreaker +0.03 (+0.21), Spirit Resilience +0.02 (+0.15), Witchmail +0.01 (+0.21)
- **Graves**: Healbane +0.10 (+0.18), Reactive Barrier +0.10 (+0.13), Metal Skin +0.09 (+0.21)
- **Apollo**: Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.04), Healbane -0.04 (+0.04)
- **Deadman Danny**: Spellbreaker +0.21 (+0.38), Witchmail +0.19 (+0.39), Spirit Resilience +0.18 (+0.31)
- **Rem**: Healbane -0.01 (+0.07), Reactive Barrier -0.02 (+0.01), Counterspell -0.03 (+0.05)
- **Silver**: Dispel Magic +0.07 (+0.15), Reactive Barrier +0.03 (+0.07), Debuff Reducer +0.00 (+0.08)
- **Celeste**: Spirit Resilience +0.15 (+0.28), Witchmail +0.12 (+0.33), Plated Armor +0.06 (+0.20)
- **Rat King**: Return Fire +0.00 (+0.09), Counterspell -0.01 (+0.06), Divine Barrier -0.01 (+0.11)
- **Solomon**: Reactive Barrier -0.00 (+0.04), Counterspell -0.03 (+0.05), Return Fire -0.03 (+0.06)
- **Violet**: Return Fire +0.06 (+0.14), Unstoppable +0.05 (+0.19), Witchmail +0.03 (+0.23)
- **Nurse Harrow**: Healbane +0.04 (+0.12), Reactive Barrier +0.01 (+0.05), Counterspell -0.04 (+0.03)
- **Baba**: Reactive Barrier +0.00 (+0.04), Healbane -0.00 (+0.08), Counterspell -0.02 (+0.06)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.141 | Lash +0.42, Celeste +0.22, Pocket +0.18 | 10 heroes |
| Divine Barrier | 6,400 | +0.218 | +0.035 | +0.096 | Lash +0.23, Paradox +0.09, The Doorman +0.09 | 0 heroes |
| Dispel Magic | 3,200 | +0.089 | +0.028 | +0.063 | Mirage +0.28, Paradox +0.11, Silver +0.10 | 9 heroes |
| Indomitable | 6,400 | +0.146 | +0.023 | +0.104 | Wraith +0.19, The Doorman +0.18, Abrams +0.13 | 0 heroes |
| Spellbreaker | 6,400 | +0.124 | +0.019 | +0.168 | Lash +0.36, Holliday +0.18, Wraith +0.12 | 0 heroes |
| Witchmail | 6,400 | +0.117 | +0.018 | +0.183 | Lash +0.29, Celeste +0.18, The Doorman +0.09 | 1 heroes |
| Bullet Resilience | 3,200 | +0.024 | +0.007 | +0.074 | Venator +0.19, Paradox +0.14, Lash +0.11 | 0 heroes |
| Healbane | 1,600 | +0.012 | +0.007 | +0.064 | Yamato +0.09, Abrams +0.08, Infernus +0.06 | 23 heroes |
| Plated Armor | 6,400 | +0.010 | +0.002 | +0.105 | Holliday +0.24, Paradox +0.10, Haze +0.09 | 0 heroes |
| Debuff Reducer | 1,600 | +0.002 | +0.001 | +0.066 | Holliday +0.16, Rem +0.12, Vyper +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | +0.001 | +0.001 | +0.020 | Abrams +0.08, Graves +0.06, Deadman Danny +0.06 | 3 heroes |
| Counterspell | 3,200 | -0.034 | -0.011 | +0.044 | Lash +0.04, Nurse Harrow +0.04, Abrams +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.074 | -0.012 | +0.114 | Holliday +0.14, Abrams +0.12, Rem +0.11 | 0 heroes |
| Metal Skin | 3,200 | -0.198 | -0.062 | +0.089 | Wraith +0.25, Lash +0.17, Paradox +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.198 | -0.124 | +0.063 | Paradox +0.08, Lash +0.06, Holliday +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.10 (+0.26), Unstoppable +0.09 (+0.21), Dispel Magic +0.07 (+0.13)
- **Seven**: Witchmail +0.03 (+0.22), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Divine Barrier +0.05 (+0.15), Return Fire +0.05 (+0.11), Witchmail +0.03 (+0.22)
- **Lady Geist**: Spirit Resilience +0.11 (+0.25), Spellbreaker +0.11 (+0.28), Healbane +0.04 (+0.11)
- **Abrams**: Indomitable +0.13 (+0.23), Unstoppable +0.12 (+0.23), Spirit Resilience +0.10 (+0.24)
- **Wraith**: Metal Skin +0.25 (+0.34), Indomitable +0.19 (+0.29), Spellbreaker +0.12 (+0.29)
- **McGinnis**: Spirit Resilience -0.01 (+0.13), Healbane -0.01 (+0.05), Reactive Barrier -0.01 (+0.01)
- **Paradox**: Bullet Resilience +0.14 (+0.22), Metal Skin +0.14 (+0.23), Indomitable +0.12 (+0.22)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.00)
- **Kelvin**: Spirit Resilience +0.06 (+0.20), Witchmail +0.02 (+0.20), Spellbreaker -0.00 (+0.17)
- **Haze**: Indomitable +0.12 (+0.23), Plated Armor +0.09 (+0.19), Unstoppable +0.06 (+0.18)
- **Holliday**: Plated Armor +0.24 (+0.35), Spellbreaker +0.18 (+0.35), Debuff Reducer +0.16 (+0.22)
- **Bebop**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01)
- **Calico**: Divine Barrier +0.06 (+0.15), Spirit Resilience +0.05 (+0.19), Dispel Magic +0.02 (+0.08)
- **Grey Talon**: Unstoppable +0.09 (+0.20), Debuff Reducer +0.05 (+0.11), Spellbreaker +0.04 (+0.21)
- **Mo & Krill**: Spellbreaker +0.08 (+0.25), Unstoppable +0.08 (+0.19), Spirit Resilience +0.04 (+0.18)
- **Shiv**: Bullet Resilience +0.06 (+0.14), Metal Skin +0.04 (+0.13), Plated Armor +0.03 (+0.14)
- **Ivy**: Unstoppable +0.11 (+0.22), Debuff Reducer +0.06 (+0.12), Indomitable +0.04 (+0.15)
- **Warden**: Return Fire +0.02 (+0.09), Divine Barrier -0.00 (+0.09), Debuff Reducer -0.01 (+0.05)
- **Yamato**: Healbane +0.09 (+0.15), Debuff Reducer +0.00 (+0.07), Counterspell -0.01 (+0.04)
- **Lash**: Spirit Resilience +0.42 (+0.56), Spellbreaker +0.36 (+0.53), Witchmail +0.29 (+0.47)
- **Viscous**: Divine Barrier +0.03 (+0.13), Counterspell +0.01 (+0.06), Healbane +0.00 (+0.07)
- **Pocket**: Spirit Resilience +0.18 (+0.33), Witchmail +0.06 (+0.24), Spellbreaker +0.05 (+0.22)
- **Mirage**: Dispel Magic +0.28 (+0.35), Spirit Resilience +0.04 (+0.18), Metal Skin +0.03 (+0.12)
- **Vyper**: Spellbreaker +0.08 (+0.25), Debuff Reducer +0.07 (+0.14), Unstoppable +0.06 (+0.17)
- **Sinclair**: Indomitable +0.10 (+0.21), Reactive Barrier +0.01 (+0.03), Spellbreaker -0.00 (+0.17)
- **Mina**: Counterspell +0.00 (+0.05), Return Fire -0.00 (+0.06), Divine Barrier -0.01 (+0.08)
- **Drifter**: Return Fire +0.01 (+0.07), Counterspell -0.00 (+0.04), Healbane -0.00 (+0.06)
- **Venator**: Bullet Resilience +0.19 (+0.27), Debuff Reducer +0.07 (+0.13), Unstoppable +0.05 (+0.16)
- **Victor**: Spirit Resilience +0.07 (+0.21), Spellbreaker +0.07 (+0.24), Healbane +0.03 (+0.09)
- **Paige**: Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01), Return Fire -0.03 (+0.04)
- **The Doorman**: Indomitable +0.18 (+0.28), Spirit Resilience +0.11 (+0.25), Spellbreaker +0.10 (+0.27)
- **Billy**: Healbane +0.00 (+0.07), Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.06)
- **Graves**: Metal Skin +0.07 (+0.16), Reactive Barrier +0.06 (+0.08), Return Fire +0.04 (+0.10)
- **Apollo**: Return Fire -0.01 (+0.06), Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (+0.00)
- **Deadman Danny**: Spirit Resilience +0.10 (+0.24), Witchmail +0.09 (+0.27), Indomitable +0.06 (+0.17)
- **Rem**: Debuff Reducer +0.12 (+0.19), Unstoppable +0.11 (+0.23), Spellbreaker +0.03 (+0.20)
- **Silver**: Dispel Magic +0.10 (+0.16), Reactive Barrier +0.02 (+0.04), Debuff Reducer +0.01 (+0.07)
- **Celeste**: Spirit Resilience +0.22 (+0.36), Witchmail +0.18 (+0.36), Spellbreaker +0.09 (+0.26)
- **Rat King**: Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Solomon**: Reactive Barrier -0.01 (+0.01), Return Fire -0.01 (+0.05), Counterspell -0.02 (+0.03)
- **Violet**: Unstoppable +0.06 (+0.17), Witchmail +0.05 (+0.24), Healbane +0.05 (+0.11)
- **Nurse Harrow**: Healbane +0.06 (+0.12), Divine Barrier +0.06 (+0.15), Counterspell +0.04 (+0.08)
- **Baba**: Healbane +0.00 (+0.06), Reactive Barrier -0.00 (+0.02), Counterspell -0.00 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.187 | +0.059 | +0.147 | Lash +0.37, Deadman Danny +0.25, Viscous +0.19 | 13 heroes |
| Dispel Magic | 3,200 | +0.092 | +0.029 | +0.058 | Mirage +0.24, Graves +0.14, Infernus +0.10 | 11 heroes |
| Divine Barrier | 6,400 | +0.181 | +0.028 | +0.086 | Graves +0.11, Mina +0.09, Vindicta +0.08 | 2 heroes |
| Indomitable | 6,400 | +0.146 | +0.023 | +0.108 | Haze +0.22, Wraith +0.21, The Doorman +0.18 | 0 heroes |
| Spellbreaker | 6,400 | +0.146 | +0.023 | +0.189 | Lash +0.39, Wraith +0.17, Holliday +0.17 | 0 heroes |
| Witchmail | 6,400 | +0.105 | +0.016 | +0.173 | Deadman Danny +0.18, Lash +0.16, Graves +0.14 | 1 heroes |
| Bullet Resilience | 3,200 | +0.018 | +0.006 | +0.061 | Venator +0.21, Vindicta +0.11, Haze +0.11 | 1 heroes |
| Healbane | 1,600 | +0.009 | +0.005 | +0.064 | Mo & Krill +0.08, Infernus +0.08, Violet +0.07 | 25 heroes |
| Debuff Reducer | 1,600 | +0.006 | +0.004 | +0.072 | Bebop +0.18, Holliday +0.17, Grey Talon +0.14 | 0 heroes |
| Plated Armor | 6,400 | +0.011 | +0.002 | +0.101 | Holliday +0.20, Haze +0.12, Deadman Danny +0.10 | 0 heroes |
| Unstoppable | 6,400 | -0.066 | -0.010 | +0.128 | Mo & Krill +0.23, Haze +0.18, Grey Talon +0.16 | 3 heroes |
| Counterspell | 3,200 | -0.040 | -0.013 | +0.033 | Vyper +0.03, Calico +0.03, Grey Talon +0.03 | 1 heroes |
| Reactive Barrier | 1,600 | -0.024 | -0.015 | +0.018 | Deadman Danny +0.12, Graves +0.07, Grey Talon +0.06 | 2 heroes |
| Metal Skin | 3,200 | -0.196 | -0.061 | +0.088 | Wraith +0.20, Graves +0.14, Haze +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.193 | -0.121 | +0.057 | Haze +0.12, Paradox +0.06, Venator +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.16), Spellbreaker +0.09 (+0.28), Healbane +0.08 (+0.15)
- **Seven**: Witchmail +0.10 (+0.27), Spirit Resilience +0.08 (+0.22), Healbane +0.02 (+0.08)
- **Vindicta**: Bullet Resilience +0.11 (+0.17), Divine Barrier +0.08 (+0.17), Plated Armor +0.07 (+0.17)
- **Lady Geist**: Spirit Resilience +0.11 (+0.26), Healbane +0.06 (+0.12), Spellbreaker +0.04 (+0.23)
- **Abrams**: Unstoppable +0.07 (+0.20), Dispel Magic +0.05 (+0.11), Reactive Barrier +0.03 (+0.05)
- **Wraith**: Indomitable +0.21 (+0.32), Metal Skin +0.20 (+0.28), Spellbreaker +0.17 (+0.36)
- **McGinnis**: Spirit Resilience +0.00 (+0.15), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.00)
- **Paradox**: Return Fire +0.06 (+0.12), Dispel Magic +0.06 (+0.11), Witchmail +0.05 (+0.22)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (-0.00)
- **Kelvin**: Healbane +0.02 (+0.09), Counterspell +0.01 (+0.05), Spirit Resilience +0.01 (+0.16)
- **Haze**: Indomitable +0.22 (+0.33), Unstoppable +0.18 (+0.31), Plated Armor +0.12 (+0.23)
- **Holliday**: Plated Armor +0.20 (+0.30), Debuff Reducer +0.17 (+0.24), Spellbreaker +0.17 (+0.36)
- **Bebop**: Debuff Reducer +0.18 (+0.25), Unstoppable +0.15 (+0.27), Spellbreaker +0.12 (+0.30)
- **Calico**: Spirit Resilience +0.12 (+0.27), Divine Barrier +0.04 (+0.13), Dispel Magic +0.03 (+0.09)
- **Grey Talon**: Unstoppable +0.16 (+0.29), Debuff Reducer +0.14 (+0.22), Spellbreaker +0.12 (+0.31)
- **Mo & Krill**: Unstoppable +0.23 (+0.36), Spellbreaker +0.09 (+0.28), Healbane +0.08 (+0.15)
- **Shiv**: Bullet Resilience +0.05 (+0.11), Divine Barrier +0.01 (+0.10), Plated Armor +0.01 (+0.11)
- **Ivy**: Unstoppable +0.06 (+0.19), Indomitable +0.06 (+0.17), Debuff Reducer +0.03 (+0.11)
- **Warden**: Debuff Reducer +0.00 (+0.08), Return Fire +0.00 (+0.06), Counterspell -0.00 (+0.03)
- **Yamato**: Healbane +0.05 (+0.12), Debuff Reducer +0.03 (+0.10), Witchmail +0.03 (+0.20)
- **Lash**: Spellbreaker +0.39 (+0.58), Spirit Resilience +0.37 (+0.51), Witchmail +0.16 (+0.34)
- **Viscous**: Spirit Resilience +0.19 (+0.33), Spellbreaker +0.08 (+0.26), Divine Barrier +0.06 (+0.15)
- **Pocket**: Spirit Resilience +0.05 (+0.19), Witchmail +0.01 (+0.18), Counterspell -0.01 (+0.02)
- **Mirage**: Dispel Magic +0.24 (+0.30), Metal Skin +0.02 (+0.11), Healbane -0.00 (+0.06)
- **Vyper**: Unstoppable +0.09 (+0.22), Spellbreaker +0.07 (+0.26), Debuff Reducer +0.05 (+0.12)
- **Sinclair**: Indomitable +0.14 (+0.25), Unstoppable +0.00 (+0.13), Debuff Reducer -0.01 (+0.07)
- **Mina**: Divine Barrier +0.09 (+0.17), Witchmail +0.07 (+0.24), Spirit Resilience +0.06 (+0.21)
- **Drifter**: Healbane +0.01 (+0.07), Counterspell -0.00 (+0.03), Reactive Barrier -0.01 (+0.00)
- **Venator**: Bullet Resilience +0.21 (+0.28), Plated Armor +0.06 (+0.16), Return Fire +0.05 (+0.11)
- **Victor**: Spellbreaker +0.05 (+0.23), Healbane +0.03 (+0.10), Spirit Resilience +0.03 (+0.17)
- **Paige**: Counterspell +0.01 (+0.04), Divine Barrier +0.00 (+0.09), Reactive Barrier -0.01 (+0.01)
- **The Doorman**: Indomitable +0.18 (+0.29), Spirit Resilience +0.12 (+0.27), Witchmail +0.10 (+0.27)
- **Billy**: Reactive Barrier +0.02 (+0.04), Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Graves**: Spirit Resilience +0.16 (+0.31), Metal Skin +0.14 (+0.23), Dispel Magic +0.14 (+0.19)
- **Apollo**: Healbane +0.02 (+0.08), Counterspell -0.00 (+0.03), Reactive Barrier -0.01 (+0.00)
- **Deadman Danny**: Spirit Resilience +0.25 (+0.40), Witchmail +0.18 (+0.35), Reactive Barrier +0.12 (+0.14)
- **Rem**: Debuff Reducer +0.10 (+0.18), Unstoppable +0.07 (+0.20), Spellbreaker +0.01 (+0.20)
- **Silver**: Dispel Magic +0.06 (+0.12), Reactive Barrier +0.05 (+0.07), Bullet Resilience +0.02 (+0.08)
- **Celeste**: Witchmail +0.09 (+0.26), Spirit Resilience +0.07 (+0.22), Healbane +0.05 (+0.12)
- **Rat King**: Return Fire +0.00 (+0.06), Bullet Resilience -0.01 (+0.06), Counterspell -0.01 (+0.03)
- **Solomon**: Reactive Barrier +0.01 (+0.03), Return Fire +0.01 (+0.06), Counterspell -0.02 (+0.02)
- **Violet**: Healbane +0.07 (+0.13), Witchmail +0.06 (+0.24), Spirit Resilience +0.02 (+0.17)
- **Nurse Harrow**: Spirit Resilience +0.05 (+0.19), Witchmail +0.04 (+0.22), Healbane +0.04 (+0.11)
- **Baba**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.01 (+0.01)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.166 | +0.052 | +0.139 | Lash +0.39, Deadman Danny +0.37, The Doorman +0.33 | 16 heroes |
| Dispel Magic | 3,200 | +0.094 | +0.029 | +0.060 | Mirage +0.33, Lash +0.18, Silver +0.14 | 11 heroes |
| Indomitable | 6,400 | +0.166 | +0.026 | +0.131 | Wraith +0.39, The Doorman +0.27, Sinclair +0.21 | 2 heroes |
| Spellbreaker | 6,400 | +0.161 | +0.025 | +0.199 | Deadman Danny +0.32, Grey Talon +0.23, Wraith +0.20 | 0 heroes |
| Divine Barrier | 6,400 | +0.139 | +0.022 | +0.077 | Lash +0.14, Viscous +0.13, The Doorman +0.10 | 2 heroes |
| Witchmail | 6,400 | +0.108 | +0.017 | +0.172 | Deadman Danny +0.32, The Doorman +0.24, Lash +0.19 | 1 heroes |
| Bullet Resilience | 3,200 | +0.017 | +0.005 | +0.062 | Vindicta +0.14, Venator +0.11, Paradox +0.11 | 1 heroes |
| Healbane | 1,600 | +0.007 | +0.004 | +0.064 | Lady Geist +0.12, Celeste +0.09, Yamato +0.07 | 21 heroes |
| Debuff Reducer | 1,600 | +0.006 | +0.004 | +0.091 | Paige +0.21, Grey Talon +0.17, Bebop +0.16 | 0 heroes |
| Plated Armor | 6,400 | +0.005 | +0.001 | +0.102 | Haze +0.12, Vindicta +0.12, Celeste +0.07 | 3 heroes |
| Unstoppable | 6,400 | -0.056 | -0.009 | +0.158 | Paige +0.28, Grey Talon +0.20, Haze +0.17 | 5 heroes |
| Counterspell | 3,200 | -0.044 | -0.014 | +0.030 | Lash +0.06, Celeste +0.06, Viscous +0.03 | 1 heroes |
| Reactive Barrier | 1,600 | -0.033 | -0.020 | +0.016 | Deadman Danny +0.07, Celeste +0.06, Grey Talon +0.04 | 2 heroes |
| Metal Skin | 3,200 | -0.197 | -0.061 | +0.088 | Wraith +0.19, Paradox +0.16, Silver +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.189 | -0.118 | +0.052 | Vindicta +0.11, Paradox +0.10, Lash +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.31), Spellbreaker +0.11 (+0.31), Dispel Magic +0.09 (+0.15)
- **Seven**: Witchmail +0.06 (+0.23), Reactive Barrier +0.00 (+0.02), Counterspell +0.00 (+0.03)
- **Vindicta**: Bullet Resilience +0.14 (+0.20), Plated Armor +0.12 (+0.22), Return Fire +0.11 (+0.16)
- **Lady Geist**: Healbane +0.12 (+0.18), Spirit Resilience +0.09 (+0.23), Witchmail +0.08 (+0.26)
- **Abrams**: Dispel Magic +0.02 (+0.08), Unstoppable +0.01 (+0.17), Healbane +0.01 (+0.07)
- **Wraith**: Indomitable +0.39 (+0.52), Spellbreaker +0.20 (+0.40), Metal Skin +0.19 (+0.28)
- **McGinnis**: Spirit Resilience +0.02 (+0.16), Dispel Magic +0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Paradox**: Metal Skin +0.16 (+0.25), Unstoppable +0.16 (+0.32), Witchmail +0.14 (+0.31)
- **Dynamo**: Healbane -0.01 (+0.06), Reactive Barrier -0.01 (+0.00), Counterspell -0.02 (+0.01)
- **Kelvin**: Spirit Resilience +0.03 (+0.16), Healbane +0.00 (+0.07), Reactive Barrier -0.00 (+0.01)
- **Haze**: Unstoppable +0.17 (+0.33), Plated Armor +0.12 (+0.23), Bullet Resilience +0.09 (+0.15)
- **Holliday**: Spellbreaker +0.06 (+0.26), Debuff Reducer +0.06 (+0.15), Reactive Barrier +0.01 (+0.03)
- **Bebop**: Debuff Reducer +0.16 (+0.25), Unstoppable +0.11 (+0.27), Spellbreaker +0.08 (+0.28)
- **Calico**: Spirit Resilience +0.04 (+0.18), Reactive Barrier -0.01 (+0.01), Divine Barrier -0.01 (+0.07)
- **Grey Talon**: Spellbreaker +0.23 (+0.43), Unstoppable +0.20 (+0.36), Spirit Resilience +0.20 (+0.34)
- **Mo & Krill**: Spellbreaker +0.15 (+0.35), Debuff Reducer +0.13 (+0.22), Unstoppable +0.12 (+0.27)
- **Shiv**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.06 (+0.15), Plated Armor +0.03 (+0.14)
- **Ivy**: Unstoppable +0.17 (+0.33), Indomitable +0.15 (+0.28), Debuff Reducer +0.09 (+0.18)
- **Warden**: Divine Barrier +0.03 (+0.11), Spirit Resilience +0.01 (+0.15), Bullet Resilience +0.01 (+0.07)
- **Yamato**: Healbane +0.07 (+0.13), Counterspell +0.01 (+0.04), Reactive Barrier +0.00 (+0.02)
- **Lash**: Spirit Resilience +0.39 (+0.53), Witchmail +0.19 (+0.36), Spellbreaker +0.19 (+0.38)
- **Viscous**: Spirit Resilience +0.25 (+0.38), Divine Barrier +0.13 (+0.21), Spellbreaker +0.09 (+0.29)
- **Pocket**: Spirit Resilience +0.02 (+0.16), Return Fire -0.00 (+0.05), Reactive Barrier -0.01 (+0.01)
- **Mirage**: Dispel Magic +0.33 (+0.39), Unstoppable +0.10 (+0.26), Debuff Reducer +0.08 (+0.17)
- **Vyper**: Plated Armor +0.07 (+0.17), Bullet Resilience +0.05 (+0.11), Metal Skin +0.02 (+0.11)
- **Sinclair**: Indomitable +0.21 (+0.34), Debuff Reducer +0.07 (+0.16), Spellbreaker +0.05 (+0.25)
- **Mina**: Divine Barrier +0.01 (+0.09), Counterspell +0.00 (+0.03), Return Fire -0.01 (+0.04)
- **Drifter**: Dispel Magic +0.11 (+0.17), Reactive Barrier +0.02 (+0.03), Debuff Reducer +0.00 (+0.09)
- **Venator**: Bullet Resilience +0.11 (+0.17), Metal Skin +0.05 (+0.14), Return Fire +0.00 (+0.05)
- **Victor**: Spellbreaker +0.09 (+0.29), Healbane +0.05 (+0.12), Spirit Resilience +0.05 (+0.19)
- **Paige**: Unstoppable +0.28 (+0.44), Debuff Reducer +0.21 (+0.30), Spellbreaker +0.11 (+0.31)
- **The Doorman**: Spirit Resilience +0.33 (+0.47), Indomitable +0.27 (+0.40), Witchmail +0.24 (+0.41)
- **Billy**: Reactive Barrier +0.03 (+0.04), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Graves**: Return Fire +0.04 (+0.09), Reactive Barrier +0.03 (+0.04), Witchmail +0.02 (+0.19)
- **Apollo**: Healbane +0.02 (+0.08), Reactive Barrier -0.01 (+0.00), Counterspell -0.02 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.37 (+0.51), Witchmail +0.32 (+0.50), Spellbreaker +0.32 (+0.52)
- **Rem**: Spirit Resilience +0.09 (+0.23), Divine Barrier +0.09 (+0.17), Witchmail +0.03 (+0.20)
- **Silver**: Dispel Magic +0.14 (+0.20), Metal Skin +0.11 (+0.20), Bullet Resilience +0.05 (+0.11)
- **Celeste**: Witchmail +0.16 (+0.33), Spirit Resilience +0.15 (+0.29), Healbane +0.09 (+0.15)
- **Rat King**: Healbane -0.01 (+0.06), Counterspell -0.01 (+0.02), Metal Skin -0.01 (+0.08)
- **Solomon**: Return Fire +0.02 (+0.07), Reactive Barrier +0.01 (+0.02), Counterspell +0.00 (+0.03)
- **Violet**: Witchmail +0.08 (+0.26), Spirit Resilience +0.05 (+0.19), Dispel Magic +0.05 (+0.11)
- **Nurse Harrow**: Spirit Resilience +0.18 (+0.32), Healbane +0.05 (+0.12), Witchmail +0.04 (+0.22)
- **Baba**: Counterspell +0.01 (+0.04), Healbane +0.00 (+0.07), Reactive Barrier -0.00 (+0.01)
