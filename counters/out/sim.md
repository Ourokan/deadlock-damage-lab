# Counter items in the sim (phantom and up)

Built 2026-11-10T21:47:08Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.197 | +0.062 | +0.133 | Lady Geist +0.21, Lash +0.20, Deadman Danny +0.18 | 0 heroes |
| Divine Barrier | 6,400 | +0.256 | +0.041 | +0.129 | Lash +0.16, Viscous +0.16, Abrams +0.13 | 0 heroes |
| Dispel Magic | 3,200 | +0.101 | +0.032 | +0.086 | Mirage +0.37, Paradox +0.14, Lash +0.10 | 4 heroes |
| Indomitable | 6,400 | +0.154 | +0.024 | +0.137 | Abrams +0.22, The Doorman +0.21, Wraith +0.18 | 0 heroes |
| Debuff Reducer | 1,600 | +0.026 | +0.016 | +0.083 | Holliday +0.11, Vyper +0.11, Venator +0.09 | 0 heroes |
| Witchmail | 6,400 | +0.103 | +0.016 | +0.207 | Deadman Danny +0.19, Lash +0.18, Lady Geist +0.15 | 0 heroes |
| Bullet Resilience | 3,200 | +0.048 | +0.015 | +0.105 | Venator +0.27, Paradox +0.16, Lash +0.15 | 0 heroes |
| Spellbreaker | 6,400 | +0.083 | +0.013 | +0.182 | Deadman Danny +0.21, Lash +0.20, Lady Geist +0.19 | 0 heroes |
| Reactive Barrier | 1,600 | +0.018 | +0.011 | +0.040 | Deadman Danny +0.14, Graves +0.10, Abrams +0.06 | 2 heroes |
| Healbane | 1,600 | +0.007 | +0.004 | +0.082 | Lady Geist +0.11, Graves +0.10, Yamato +0.07 | 22 heroes |
| Plated Armor | 6,400 | +0.004 | +0.001 | +0.139 | Holliday +0.23, Wraith +0.13, Lash +0.12 | 0 heroes |
| Counterspell | 3,200 | -0.029 | -0.009 | +0.073 | Lash +0.09, Deadman Danny +0.07, Graves +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.058 | -0.009 | +0.139 | Deadman Danny +0.16, Lash +0.10, Paradox +0.09 | 0 heroes |
| Metal Skin | 3,200 | -0.181 | -0.057 | +0.118 | Wraith +0.23, Paradox +0.20, Lash +0.17 | 0 heroes |
| Return Fire | 1,600 | -0.192 | -0.120 | +0.087 | Deadman Danny +0.10, Paradox +0.09, Lady Geist +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.04 (+0.13), Spellbreaker +0.03 (+0.21), Unstoppable +0.03 (+0.17)
- **Seven**: Healbane -0.00 (+0.08), Reactive Barrier -0.02 (+0.02), Counterspell -0.03 (+0.04)
- **Vindicta**: Divine Barrier -0.00 (+0.12), Counterspell -0.01 (+0.07), Healbane -0.01 (+0.08)
- **Lady Geist**: Spirit Resilience +0.21 (+0.34), Spellbreaker +0.19 (+0.37), Witchmail +0.15 (+0.35)
- **Abrams**: Indomitable +0.22 (+0.35), Divine Barrier +0.13 (+0.26), Witchmail +0.09 (+0.29)
- **Wraith**: Metal Skin +0.23 (+0.34), Indomitable +0.18 (+0.31), Spellbreaker +0.15 (+0.34)
- **McGinnis**: Healbane +0.05 (+0.13), Spirit Resilience +0.01 (+0.14), Reactive Barrier +0.00 (+0.04)
- **Paradox**: Metal Skin +0.20 (+0.32), Indomitable +0.17 (+0.30), Bullet Resilience +0.16 (+0.27)
- **Dynamo**: Healbane +0.00 (+0.08), Counterspell -0.03 (+0.05), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Witchmail +0.02 (+0.23), Healbane +0.01 (+0.09), Spirit Resilience +0.01 (+0.14)
- **Haze**: Indomitable +0.07 (+0.21), Plated Armor +0.06 (+0.20), Bullet Resilience +0.04 (+0.15)
- **Holliday**: Plated Armor +0.23 (+0.37), Spellbreaker +0.14 (+0.32), Debuff Reducer +0.11 (+0.19)
- **Bebop**: Healbane +0.02 (+0.11), Counterspell +0.00 (+0.08), Return Fire -0.01 (+0.08)
- **Calico**: Spellbreaker +0.08 (+0.26), Divine Barrier +0.05 (+0.18), Spirit Resilience +0.05 (+0.18)
- **Grey Talon**: Unstoppable +0.06 (+0.20), Debuff Reducer +0.04 (+0.12), Reactive Barrier +0.04 (+0.08)
- **Mo & Krill**: Spellbreaker +0.07 (+0.25), Witchmail +0.04 (+0.25), Spirit Resilience +0.04 (+0.17)
- **Shiv**: Healbane -0.00 (+0.08), Return Fire -0.01 (+0.08), Divine Barrier -0.02 (+0.11)
- **Ivy**: Indomitable +0.08 (+0.22), Unstoppable +0.03 (+0.17), Debuff Reducer +0.01 (+0.09)
- **Warden**: Return Fire +0.01 (+0.09), Debuff Reducer +0.00 (+0.08), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.07 (+0.15), Debuff Reducer +0.06 (+0.14), Unstoppable +0.05 (+0.19)
- **Lash**: Spirit Resilience +0.20 (+0.34), Spellbreaker +0.20 (+0.38), Witchmail +0.18 (+0.39)
- **Viscous**: Divine Barrier +0.16 (+0.29), Spirit Resilience +0.09 (+0.22), Spellbreaker +0.08 (+0.26)
- **Pocket**: Return Fire +0.01 (+0.09), Counterspell +0.01 (+0.08), Witchmail +0.00 (+0.21)
- **Mirage**: Dispel Magic +0.37 (+0.46), Spellbreaker +0.12 (+0.30), Spirit Resilience +0.12 (+0.25)
- **Vyper**: Debuff Reducer +0.11 (+0.19), Unstoppable +0.09 (+0.23), Spellbreaker +0.08 (+0.26)
- **Sinclair**: Indomitable +0.15 (+0.28), Spellbreaker +0.07 (+0.25), Unstoppable +0.06 (+0.20)
- **Mina**: Return Fire +0.01 (+0.10), Counterspell -0.01 (+0.06), Witchmail -0.02 (+0.19)
- **Drifter**: Reactive Barrier -0.01 (+0.02), Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.07)
- **Venator**: Bullet Resilience +0.27 (+0.37), Debuff Reducer +0.09 (+0.17), Unstoppable +0.08 (+0.22)
- **Victor**: Spirit Resilience +0.11 (+0.24), Spellbreaker +0.10 (+0.28), Witchmail -0.01 (+0.20)
- **Paige**: Reactive Barrier -0.01 (+0.03), Counterspell -0.01 (+0.06), Return Fire -0.02 (+0.07)
- **The Doorman**: Indomitable +0.21 (+0.35), Spirit Resilience +0.17 (+0.30), Witchmail +0.15 (+0.35)
- **Billy**: Spellbreaker +0.02 (+0.21), Spirit Resilience +0.02 (+0.16), Plated Armor +0.01 (+0.14)
- **Graves**: Healbane +0.10 (+0.18), Reactive Barrier +0.10 (+0.14), Metal Skin +0.09 (+0.21)
- **Apollo**: Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.04), Healbane -0.04 (+0.04)
- **Deadman Danny**: Spellbreaker +0.21 (+0.39), Witchmail +0.19 (+0.40), Spirit Resilience +0.18 (+0.31)
- **Rem**: Healbane -0.01 (+0.07), Reactive Barrier -0.02 (+0.02), Counterspell -0.02 (+0.05)
- **Silver**: Dispel Magic +0.08 (+0.17), Reactive Barrier +0.04 (+0.08), Debuff Reducer +0.01 (+0.10)
- **Celeste**: Spirit Resilience +0.15 (+0.28), Witchmail +0.12 (+0.32), Dispel Magic +0.06 (+0.14)
- **Rat King**: Return Fire +0.00 (+0.09), Counterspell -0.01 (+0.06), Divine Barrier -0.01 (+0.12)
- **Solomon**: Reactive Barrier -0.00 (+0.04), Counterspell -0.03 (+0.05), Return Fire -0.03 (+0.06)
- **Violet**: Return Fire +0.06 (+0.14), Unstoppable +0.06 (+0.19), Witchmail +0.03 (+0.23)
- **Nurse Harrow**: Healbane +0.04 (+0.12), Reactive Barrier +0.01 (+0.04), Counterspell -0.05 (+0.03)
- **Baba**: Reactive Barrier -0.00 (+0.04), Healbane -0.00 (+0.08), Counterspell -0.02 (+0.06)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.198 | +0.062 | +0.140 | Lash +0.42, Celeste +0.22, Pocket +0.18 | 10 heroes |
| Divine Barrier | 6,400 | +0.208 | +0.033 | +0.096 | Lash +0.24, Paradox +0.10, Abrams +0.09 | 1 heroes |
| Dispel Magic | 3,200 | +0.088 | +0.027 | +0.061 | Mirage +0.25, Silver +0.12, Paradox +0.09 | 9 heroes |
| Indomitable | 6,400 | +0.144 | +0.023 | +0.102 | Wraith +0.19, The Doorman +0.17, Abrams +0.13 | 0 heroes |
| Spellbreaker | 6,400 | +0.123 | +0.019 | +0.165 | Lash +0.36, Holliday +0.20, Lady Geist +0.17 | 0 heroes |
| Witchmail | 6,400 | +0.118 | +0.018 | +0.183 | Lash +0.30, Celeste +0.19, Deadman Danny +0.10 | 1 heroes |
| Bullet Resilience | 3,200 | +0.024 | +0.007 | +0.073 | Venator +0.20, Paradox +0.14, Lash +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.006 | +0.004 | +0.065 | Holliday +0.18, Rem +0.12, Vyper +0.07 | 0 heroes |
| Plated Armor | 6,400 | +0.012 | +0.002 | +0.104 | Holliday +0.27, Paradox +0.10, Lash +0.10 | 0 heroes |
| Reactive Barrier | 1,600 | +0.001 | +0.001 | +0.022 | Abrams +0.08, Deadman Danny +0.07, Holliday +0.06 | 4 heroes |
| Healbane | 1,600 | -0.002 | -0.001 | +0.065 | Abrams +0.08, Yamato +0.07, Infernus +0.06 | 23 heroes |
| Unstoppable | 6,400 | -0.079 | -0.012 | +0.111 | Holliday +0.16, Abrams +0.12, Rem +0.12 | 0 heroes |
| Counterspell | 3,200 | -0.042 | -0.013 | +0.044 | Lash +0.05, Nurse Harrow +0.03, Abrams +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.199 | -0.062 | +0.087 | Wraith +0.26, Lash +0.17, Paradox +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.200 | -0.125 | +0.064 | Paradox +0.08, Lash +0.06, Deadman Danny +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.10 (+0.26), Unstoppable +0.10 (+0.21), Dispel Magic +0.07 (+0.14)
- **Seven**: Witchmail +0.03 (+0.22), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Divine Barrier +0.05 (+0.15), Return Fire +0.04 (+0.11), Witchmail +0.03 (+0.22)
- **Lady Geist**: Spellbreaker +0.17 (+0.34), Spirit Resilience +0.14 (+0.28), Witchmail +0.09 (+0.27)
- **Abrams**: Indomitable +0.13 (+0.23), Unstoppable +0.12 (+0.23), Spirit Resilience +0.10 (+0.24)
- **Wraith**: Metal Skin +0.26 (+0.35), Indomitable +0.19 (+0.29), Spellbreaker +0.13 (+0.30)
- **McGinnis**: Spirit Resilience -0.01 (+0.14), Healbane -0.01 (+0.06), Reactive Barrier -0.01 (+0.01)
- **Paradox**: Metal Skin +0.15 (+0.24), Bullet Resilience +0.14 (+0.21), Indomitable +0.11 (+0.21)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.00)
- **Kelvin**: Spirit Resilience +0.09 (+0.23), Witchmail +0.04 (+0.23), Spellbreaker +0.02 (+0.19)
- **Haze**: Indomitable +0.09 (+0.19), Plated Armor +0.06 (+0.16), Unstoppable +0.04 (+0.15)
- **Holliday**: Plated Armor +0.27 (+0.38), Spellbreaker +0.20 (+0.37), Debuff Reducer +0.18 (+0.24)
- **Bebop**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01)
- **Calico**: Divine Barrier +0.05 (+0.15), Spirit Resilience +0.04 (+0.18), Dispel Magic +0.02 (+0.08)
- **Grey Talon**: Unstoppable +0.09 (+0.21), Debuff Reducer +0.05 (+0.11), Spellbreaker +0.04 (+0.21)
- **Mo & Krill**: Spellbreaker +0.08 (+0.25), Unstoppable +0.08 (+0.19), Spirit Resilience +0.04 (+0.18)
- **Shiv**: Bullet Resilience +0.06 (+0.13), Metal Skin +0.04 (+0.13), Plated Armor +0.03 (+0.14)
- **Ivy**: Unstoppable +0.03 (+0.14), Indomitable +0.01 (+0.12), Debuff Reducer +0.01 (+0.07)
- **Warden**: Return Fire +0.02 (+0.09), Divine Barrier -0.00 (+0.09), Unstoppable -0.01 (+0.10)
- **Yamato**: Healbane +0.07 (+0.14), Debuff Reducer -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Lash**: Spirit Resilience +0.42 (+0.56), Spellbreaker +0.36 (+0.53), Witchmail +0.30 (+0.49)
- **Viscous**: Divine Barrier +0.03 (+0.13), Counterspell +0.01 (+0.05), Healbane -0.00 (+0.06)
- **Pocket**: Spirit Resilience +0.18 (+0.32), Witchmail +0.06 (+0.24), Spellbreaker +0.05 (+0.22)
- **Mirage**: Dispel Magic +0.25 (+0.31), Metal Skin +0.05 (+0.14), Spirit Resilience +0.03 (+0.17)
- **Vyper**: Spellbreaker +0.08 (+0.25), Debuff Reducer +0.07 (+0.14), Unstoppable +0.06 (+0.18)
- **Sinclair**: Indomitable +0.10 (+0.20), Reactive Barrier +0.01 (+0.03), Spellbreaker +0.00 (+0.17)
- **Mina**: Counterspell +0.00 (+0.05), Return Fire -0.01 (+0.06), Plated Armor -0.01 (+0.09)
- **Drifter**: Return Fire +0.01 (+0.07), Counterspell -0.00 (+0.04), Healbane -0.01 (+0.06)
- **Venator**: Bullet Resilience +0.20 (+0.27), Debuff Reducer +0.07 (+0.13), Unstoppable +0.05 (+0.16)
- **Victor**: Spirit Resilience +0.10 (+0.24), Spellbreaker +0.07 (+0.24), Healbane +0.02 (+0.09)
- **Paige**: Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01), Return Fire -0.03 (+0.04)
- **The Doorman**: Indomitable +0.17 (+0.28), Spirit Resilience +0.10 (+0.24), Spellbreaker +0.09 (+0.26)
- **Billy**: Healbane +0.00 (+0.07), Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.05)
- **Graves**: Metal Skin +0.06 (+0.15), Reactive Barrier +0.05 (+0.07), Return Fire +0.04 (+0.10)
- **Apollo**: Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (-0.00), Healbane -0.03 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.10 (+0.24), Witchmail +0.10 (+0.28), Indomitable +0.08 (+0.18)
- **Rem**: Debuff Reducer +0.12 (+0.19), Unstoppable +0.12 (+0.23), Spellbreaker +0.04 (+0.20)
- **Silver**: Dispel Magic +0.12 (+0.18), Reactive Barrier +0.04 (+0.06), Debuff Reducer +0.01 (+0.08)
- **Celeste**: Spirit Resilience +0.22 (+0.36), Witchmail +0.19 (+0.37), Spellbreaker +0.10 (+0.27)
- **Rat King**: Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.01)
- **Solomon**: Reactive Barrier -0.01 (+0.01), Return Fire -0.01 (+0.05), Counterspell -0.02 (+0.03)
- **Violet**: Unstoppable +0.07 (+0.18), Witchmail +0.06 (+0.25), Healbane +0.05 (+0.11)
- **Nurse Harrow**: Healbane +0.06 (+0.13), Divine Barrier +0.06 (+0.16), Witchmail +0.04 (+0.22)
- **Baba**: Healbane -0.00 (+0.06), Unstoppable -0.00 (+0.11), Reactive Barrier -0.00 (+0.02)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.190 | +0.059 | +0.148 | Lash +0.37, Deadman Danny +0.23, Viscous +0.20 | 13 heroes |
| Dispel Magic | 3,200 | +0.089 | +0.028 | +0.054 | Mirage +0.22, Lash +0.15, Infernus +0.09 | 10 heroes |
| Divine Barrier | 6,400 | +0.173 | +0.027 | +0.086 | Viscous +0.09, Lash +0.09, Mina +0.08 | 2 heroes |
| Indomitable | 6,400 | +0.143 | +0.023 | +0.104 | Haze +0.22, Wraith +0.22, The Doorman +0.18 | 0 heroes |
| Spellbreaker | 6,400 | +0.142 | +0.022 | +0.181 | Lash +0.41, Wraith +0.18, Holliday +0.17 | 0 heroes |
| Witchmail | 6,400 | +0.108 | +0.017 | +0.179 | Deadman Danny +0.17, Lash +0.17, Graves +0.16 | 1 heroes |
| Bullet Resilience | 3,200 | +0.018 | +0.006 | +0.061 | Venator +0.22, Haze +0.11, Vindicta +0.11 | 1 heroes |
| Debuff Reducer | 1,600 | +0.006 | +0.004 | +0.066 | Holliday +0.17, Grey Talon +0.14, Rem +0.11 | 0 heroes |
| Plated Armor | 6,400 | +0.013 | +0.002 | +0.099 | Holliday +0.21, Haze +0.13, Deadman Danny +0.09 | 0 heroes |
| Healbane | 1,600 | -0.006 | -0.004 | +0.068 | Mo & Krill +0.08, Infernus +0.08, Violet +0.07 | 25 heroes |
| Unstoppable | 6,400 | -0.075 | -0.012 | +0.118 | Mo & Krill +0.23, Haze +0.19, Grey Talon +0.15 | 3 heroes |
| Counterspell | 3,200 | -0.048 | -0.015 | +0.034 | Viscous +0.04, Calico +0.03, Kelvin +0.03 | 1 heroes |
| Reactive Barrier | 1,600 | -0.025 | -0.015 | +0.017 | Deadman Danny +0.10, Grey Talon +0.05, Silver +0.05 | 2 heroes |
| Metal Skin | 3,200 | -0.196 | -0.061 | +0.088 | Wraith +0.20, Graves +0.15, Haze +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.195 | -0.122 | +0.057 | Haze +0.12, Venator +0.06, Vindicta +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.15), Spellbreaker +0.09 (+0.27), Healbane +0.08 (+0.14)
- **Seven**: Witchmail +0.09 (+0.26), Spirit Resilience +0.07 (+0.22), Healbane +0.02 (+0.08)
- **Vindicta**: Bullet Resilience +0.11 (+0.17), Divine Barrier +0.08 (+0.16), Plated Armor +0.07 (+0.17)
- **Lady Geist**: Spirit Resilience +0.10 (+0.25), Healbane +0.04 (+0.11), Spellbreaker +0.03 (+0.21)
- **Abrams**: Unstoppable +0.07 (+0.19), Dispel Magic +0.04 (+0.09), Reactive Barrier +0.03 (+0.04)
- **Wraith**: Indomitable +0.22 (+0.32), Metal Skin +0.20 (+0.29), Spellbreaker +0.18 (+0.36)
- **McGinnis**: Spirit Resilience +0.09 (+0.23), Witchmail +0.04 (+0.21), Counterspell +0.02 (+0.05)
- **Paradox**: Dispel Magic +0.06 (+0.11), Return Fire +0.05 (+0.11), Indomitable +0.04 (+0.15)
- **Dynamo**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (-0.00)
- **Kelvin**: Spirit Resilience +0.05 (+0.20), Counterspell +0.03 (+0.06), Reactive Barrier -0.01 (+0.01)
- **Haze**: Indomitable +0.22 (+0.33), Unstoppable +0.19 (+0.30), Plated Armor +0.13 (+0.23)
- **Holliday**: Plated Armor +0.21 (+0.31), Spellbreaker +0.17 (+0.35), Debuff Reducer +0.17 (+0.24)
- **Bebop**: Healbane +0.04 (+0.11), Counterspell +0.02 (+0.05), Divine Barrier +0.02 (+0.10)
- **Calico**: Spirit Resilience +0.12 (+0.27), Divine Barrier +0.04 (+0.13), Dispel Magic +0.03 (+0.09)
- **Grey Talon**: Unstoppable +0.15 (+0.27), Debuff Reducer +0.14 (+0.20), Spellbreaker +0.12 (+0.30)
- **Mo & Krill**: Unstoppable +0.23 (+0.35), Spellbreaker +0.10 (+0.28), Healbane +0.08 (+0.14)
- **Shiv**: Bullet Resilience +0.06 (+0.12), Divine Barrier +0.01 (+0.10), Plated Armor +0.01 (+0.11)
- **Ivy**: Unstoppable +0.07 (+0.19), Indomitable +0.05 (+0.16), Debuff Reducer +0.04 (+0.10)
- **Warden**: Debuff Reducer +0.01 (+0.08), Return Fire +0.00 (+0.06), Bullet Resilience -0.01 (+0.06)
- **Yamato**: Healbane +0.05 (+0.12), Witchmail +0.04 (+0.22), Debuff Reducer +0.03 (+0.10)
- **Lash**: Spellbreaker +0.41 (+0.59), Spirit Resilience +0.37 (+0.52), Witchmail +0.17 (+0.35)
- **Viscous**: Spirit Resilience +0.20 (+0.35), Spellbreaker +0.10 (+0.28), Divine Barrier +0.09 (+0.18)
- **Pocket**: Spirit Resilience +0.04 (+0.19), Witchmail +0.01 (+0.19), Counterspell -0.01 (+0.02)
- **Mirage**: Dispel Magic +0.22 (+0.28), Metal Skin +0.03 (+0.11), Plated Armor +0.01 (+0.11)
- **Vyper**: Unstoppable +0.09 (+0.21), Spellbreaker +0.07 (+0.25), Debuff Reducer +0.05 (+0.12)
- **Sinclair**: Indomitable +0.16 (+0.26), Unstoppable +0.09 (+0.21), Debuff Reducer +0.03 (+0.10)
- **Mina**: Divine Barrier +0.08 (+0.17), Witchmail +0.06 (+0.24), Spirit Resilience +0.06 (+0.21)
- **Drifter**: Healbane +0.00 (+0.07), Counterspell -0.00 (+0.03), Return Fire -0.01 (+0.05)
- **Venator**: Bullet Resilience +0.22 (+0.28), Plated Armor +0.07 (+0.17), Return Fire +0.06 (+0.12)
- **Victor**: Spellbreaker +0.05 (+0.23), Healbane +0.03 (+0.10), Spirit Resilience +0.03 (+0.17)
- **Paige**: Counterspell +0.00 (+0.04), Divine Barrier -0.00 (+0.09), Reactive Barrier -0.01 (+0.01)
- **The Doorman**: Indomitable +0.18 (+0.28), Spirit Resilience +0.12 (+0.26), Witchmail +0.09 (+0.27)
- **Billy**: Reactive Barrier +0.03 (+0.05), Healbane +0.01 (+0.08), Debuff Reducer -0.00 (+0.07)
- **Graves**: Spirit Resilience +0.20 (+0.35), Witchmail +0.16 (+0.34), Metal Skin +0.15 (+0.24)
- **Apollo**: Counterspell -0.00 (+0.03), Reactive Barrier -0.01 (+0.00), Healbane -0.01 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.23 (+0.38), Witchmail +0.17 (+0.35), Reactive Barrier +0.10 (+0.12)
- **Rem**: Debuff Reducer +0.11 (+0.17), Unstoppable +0.08 (+0.20), Spellbreaker +0.01 (+0.20)
- **Silver**: Dispel Magic +0.05 (+0.10), Reactive Barrier +0.05 (+0.07), Bullet Resilience +0.02 (+0.08)
- **Celeste**: Witchmail +0.07 (+0.25), Spirit Resilience +0.07 (+0.22), Healbane +0.05 (+0.12)
- **Rat King**: Return Fire +0.00 (+0.06), Bullet Resilience -0.01 (+0.06), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.03 (+0.05), Return Fire +0.01 (+0.07), Counterspell -0.02 (+0.02)
- **Violet**: Healbane +0.07 (+0.13), Witchmail +0.05 (+0.23), Spirit Resilience +0.02 (+0.17)
- **Nurse Harrow**: Spirit Resilience +0.04 (+0.19), Divine Barrier +0.04 (+0.12), Witchmail +0.04 (+0.22)
- **Baba**: Healbane -0.00 (+0.06), Reactive Barrier -0.01 (+0.01), Counterspell -0.01 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.194 | +0.061 | +0.142 | Lash +0.44, Deadman Danny +0.36, The Doorman +0.28 | 15 heroes |
| Dispel Magic | 3,200 | +0.096 | +0.030 | +0.062 | Lash +0.25, Mirage +0.20, Drifter +0.13 | 11 heroes |
| Spellbreaker | 6,400 | +0.164 | +0.026 | +0.205 | Deadman Danny +0.29, Lash +0.25, Grey Talon +0.20 | 0 heroes |
| Indomitable | 6,400 | +0.162 | +0.025 | +0.130 | Wraith +0.37, The Doorman +0.27, Sinclair +0.15 | 3 heroes |
| Divine Barrier | 6,400 | +0.158 | +0.025 | +0.080 | Lash +0.18, Viscous +0.12, Graves +0.09 | 2 heroes |
| Witchmail | 6,400 | +0.112 | +0.018 | +0.180 | Lash +0.28, Deadman Danny +0.28, The Doorman +0.23 | 1 heroes |
| Debuff Reducer | 1,600 | +0.011 | +0.007 | +0.096 | Paige +0.20, Grey Talon +0.16, Bebop +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | +0.018 | +0.006 | +0.065 | Venator +0.18, Vindicta +0.13, Paradox +0.10 | 1 heroes |
| Plated Armor | 6,400 | +0.007 | +0.001 | +0.103 | Vindicta +0.12, Haze +0.12, Graves +0.10 | 3 heroes |
| Healbane | 1,600 | -0.011 | -0.007 | +0.061 | Yamato +0.06, Mo & Krill +0.06, Lady Geist +0.06 | 21 heroes |
| Unstoppable | 6,400 | -0.059 | -0.009 | +0.160 | Paige +0.27, Ivy +0.17, Haze +0.16 | 5 heroes |
| Counterspell | 3,200 | -0.050 | -0.015 | +0.033 | Lash +0.08, Graves +0.07, Deadman Danny +0.04 | 1 heroes |
| Reactive Barrier | 1,600 | -0.034 | -0.021 | +0.019 | Graves +0.13, Deadman Danny +0.10, Billy +0.04 | 2 heroes |
| Metal Skin | 3,200 | -0.199 | -0.062 | +0.083 | Wraith +0.15, Paradox +0.15, Silver +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.189 | -0.118 | +0.056 | Graves +0.11, Vindicta +0.11, Paradox +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.14 (+0.30), Spellbreaker +0.09 (+0.30), Dispel Magic +0.09 (+0.15)
- **Seven**: Witchmail +0.08 (+0.26), Reactive Barrier +0.03 (+0.05), Healbane +0.03 (+0.09)
- **Vindicta**: Bullet Resilience +0.13 (+0.20), Plated Armor +0.12 (+0.22), Return Fire +0.11 (+0.17)
- **Lady Geist**: Spirit Resilience +0.06 (+0.21), Healbane +0.06 (+0.12), Spellbreaker -0.00 (+0.20)
- **Abrams**: Unstoppable +0.01 (+0.17), Healbane +0.01 (+0.07), Dispel Magic +0.01 (+0.07)
- **Wraith**: Indomitable +0.37 (+0.50), Spellbreaker +0.18 (+0.39), Metal Skin +0.15 (+0.24)
- **McGinnis**: Spirit Resilience +0.03 (+0.17), Witchmail -0.00 (+0.18), Dispel Magic -0.00 (+0.06)
- **Paradox**: Witchmail +0.17 (+0.35), Unstoppable +0.16 (+0.32), Metal Skin +0.15 (+0.23)
- **Dynamo**: Healbane -0.00 (+0.06), Reactive Barrier -0.02 (+0.00), Counterspell -0.02 (+0.01)
- **Kelvin**: Spirit Resilience +0.06 (+0.21), Healbane +0.04 (+0.10), Reactive Barrier +0.01 (+0.03)
- **Haze**: Unstoppable +0.16 (+0.32), Plated Armor +0.12 (+0.22), Bullet Resilience +0.08 (+0.15)
- **Holliday**: Debuff Reducer +0.05 (+0.15), Spellbreaker +0.05 (+0.25), Reactive Barrier +0.01 (+0.03)
- **Bebop**: Debuff Reducer +0.16 (+0.25), Unstoppable +0.11 (+0.27), Spellbreaker +0.09 (+0.29)
- **Calico**: Spirit Resilience +0.04 (+0.18), Divine Barrier +0.01 (+0.09), Reactive Barrier -0.01 (+0.01)
- **Grey Talon**: Spellbreaker +0.20 (+0.40), Spirit Resilience +0.19 (+0.33), Debuff Reducer +0.16 (+0.26)
- **Mo & Krill**: Indomitable +0.13 (+0.26), Spellbreaker +0.13 (+0.33), Unstoppable +0.12 (+0.28)
- **Shiv**: Bullet Resilience +0.09 (+0.16), Divine Barrier +0.05 (+0.13), Return Fire +0.04 (+0.10)
- **Ivy**: Unstoppable +0.17 (+0.33), Indomitable +0.14 (+0.27), Debuff Reducer +0.07 (+0.16)
- **Warden**: Debuff Reducer +0.01 (+0.11), Healbane +0.01 (+0.07), Bullet Resilience +0.01 (+0.07)
- **Yamato**: Healbane +0.06 (+0.12), Counterspell +0.00 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Lash**: Spirit Resilience +0.44 (+0.58), Witchmail +0.28 (+0.46), Dispel Magic +0.25 (+0.31)
- **Viscous**: Spirit Resilience +0.22 (+0.36), Divine Barrier +0.12 (+0.20), Spellbreaker +0.10 (+0.31)
- **Pocket**: Spirit Resilience -0.02 (+0.13), Reactive Barrier -0.03 (-0.01), Return Fire -0.03 (+0.02)
- **Mirage**: Dispel Magic +0.20 (+0.26), Spellbreaker +0.06 (+0.26), Reactive Barrier -0.02 (-0.00)
- **Vyper**: Debuff Reducer +0.13 (+0.23), Unstoppable +0.09 (+0.25), Spellbreaker +0.06 (+0.27)
- **Sinclair**: Indomitable +0.15 (+0.28), Spellbreaker +0.09 (+0.29), Spirit Resilience +0.07 (+0.21)
- **Mina**: Divine Barrier +0.02 (+0.10), Counterspell +0.00 (+0.04), Return Fire -0.01 (+0.05)
- **Drifter**: Dispel Magic +0.13 (+0.19), Reactive Barrier +0.03 (+0.05), Debuff Reducer +0.01 (+0.11)
- **Venator**: Bullet Resilience +0.18 (+0.24), Metal Skin +0.10 (+0.18), Plated Armor +0.05 (+0.15)
- **Victor**: Spellbreaker +0.07 (+0.27), Healbane +0.05 (+0.12), Spirit Resilience +0.03 (+0.17)
- **Paige**: Unstoppable +0.27 (+0.43), Debuff Reducer +0.20 (+0.29), Spellbreaker +0.10 (+0.30)
- **The Doorman**: Spirit Resilience +0.28 (+0.43), Indomitable +0.27 (+0.40), Witchmail +0.23 (+0.41)
- **Billy**: Reactive Barrier +0.04 (+0.06), Healbane +0.03 (+0.09), Counterspell +0.01 (+0.04)
- **Graves**: Reactive Barrier +0.13 (+0.15), Spirit Resilience +0.12 (+0.26), Dispel Magic +0.11 (+0.18)
- **Apollo**: Healbane +0.02 (+0.08), Reactive Barrier -0.02 (+0.00), Counterspell -0.02 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.36 (+0.50), Spellbreaker +0.29 (+0.50), Witchmail +0.28 (+0.46)
- **Rem**: Divine Barrier +0.07 (+0.15), Spirit Resilience +0.06 (+0.21), Witchmail +0.01 (+0.19)
- **Silver**: Metal Skin +0.12 (+0.20), Dispel Magic +0.11 (+0.17), Bullet Resilience +0.04 (+0.11)
- **Celeste**: Witchmail +0.11 (+0.29), Spirit Resilience +0.08 (+0.22), Healbane +0.02 (+0.08)
- **Rat King**: Healbane +0.00 (+0.06), Metal Skin -0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.01 (+0.03), Return Fire +0.01 (+0.06), Counterspell -0.00 (+0.03)
- **Violet**: Witchmail +0.09 (+0.27), Dispel Magic +0.04 (+0.10), Spirit Resilience +0.03 (+0.17)
- **Nurse Harrow**: Spirit Resilience +0.12 (+0.27), Divine Barrier +0.04 (+0.12), Witchmail +0.03 (+0.21)
- **Baba**: Counterspell +0.01 (+0.04), Healbane +0.01 (+0.07), Reactive Barrier -0.01 (+0.01)
