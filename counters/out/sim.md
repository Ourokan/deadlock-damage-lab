# Counter items in the sim (phantom and up)

Built 2026-11-09T00:03:40Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.198 | +0.062 | +0.137 | Lash +0.21, Deadman Danny +0.18, The Doorman +0.17 | 1 heroes |
| Divine Barrier | 6,400 | +0.294 | +0.047 | +0.138 | Lash +0.16, Viscous +0.16, The Doorman +0.16 | 0 heroes |
| Dispel Magic | 3,200 | +0.097 | +0.030 | +0.089 | Mirage +0.38, Paradox +0.16, Lash +0.12 | 4 heroes |
| Indomitable | 6,400 | +0.174 | +0.028 | +0.165 | Vyper +0.31, The Doorman +0.24, Deadman Danny +0.21 | 0 heroes |
| Healbane | 1,600 | +0.041 | +0.025 | +0.088 | Graves +0.12, Yamato +0.08, Nurse Harrow +0.07 | 22 heroes |
| Reactive Barrier | 1,600 | +0.035 | +0.021 | +0.055 | Paradox +0.15, Deadman Danny +0.14, Graves +0.10 | 2 heroes |
| Debuff Reducer | 1,600 | +0.025 | +0.016 | +0.084 | Holliday +0.11, Vyper +0.10, Venator +0.08 | 0 heroes |
| Witchmail | 6,400 | +0.099 | +0.015 | +0.212 | Deadman Danny +0.21, Lash +0.18, The Doorman +0.14 | 0 heroes |
| Bullet Resilience | 3,200 | +0.044 | +0.014 | +0.112 | Venator +0.27, Paradox +0.17, Lash +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.085 | +0.013 | +0.186 | Deadman Danny +0.22, Lash +0.21, Wraith +0.16 | 0 heroes |
| Plated Armor | 6,400 | +0.004 | +0.001 | +0.146 | Holliday +0.20, Paradox +0.13, Wraith +0.13 | 0 heroes |
| Counterspell | 3,200 | -0.013 | -0.004 | +0.079 | Lash +0.12, Viscous +0.07, Deadman Danny +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.053 | -0.008 | +0.148 | Deadman Danny +0.15, Lash +0.11, Paradox +0.11 | 0 heroes |
| Metal Skin | 3,200 | -0.179 | -0.056 | +0.122 | Wraith +0.23, Paradox +0.20, Lash +0.17 | 0 heroes |
| Return Fire | 1,600 | -0.190 | -0.119 | +0.089 | Paradox +0.13, The Doorman +0.07, Wraith +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.07 (+0.16), Spellbreaker +0.05 (+0.24), Unstoppable +0.04 (+0.19)
- **Seven**: Healbane +0.00 (+0.09), Witchmail -0.02 (+0.19), Spirit Resilience -0.02 (+0.11)
- **Vindicta**: Divine Barrier -0.00 (+0.13), Counterspell -0.00 (+0.08), Healbane -0.01 (+0.08)
- **Lady Geist**: Return Fire +0.02 (+0.11), Divine Barrier -0.01 (+0.13), Counterspell -0.01 (+0.07)
- **Abrams**: Indomitable +0.18 (+0.35), Divine Barrier +0.12 (+0.26), Witchmail +0.07 (+0.29)
- **Wraith**: Metal Skin +0.23 (+0.35), Indomitable +0.19 (+0.35), Spellbreaker +0.16 (+0.35)
- **McGinnis**: Counterspell +0.04 (+0.12), Healbane +0.02 (+0.11), Spirit Resilience +0.02 (+0.16)
- **Paradox**: Metal Skin +0.20 (+0.32), Indomitable +0.17 (+0.34), Bullet Resilience +0.17 (+0.28)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.03 (+0.05), Reactive Barrier -0.04 (+0.02)
- **Kelvin**: Witchmail +0.02 (+0.23), Healbane +0.00 (+0.09), Spirit Resilience -0.00 (+0.14)
- **Haze**: Indomitable +0.12 (+0.28), Plated Armor +0.10 (+0.25), Unstoppable +0.08 (+0.23)
- **Holliday**: Plated Armor +0.20 (+0.34), Spellbreaker +0.13 (+0.32), Debuff Reducer +0.11 (+0.20)
- **Bebop**: Healbane +0.01 (+0.10), Counterspell +0.00 (+0.08), Divine Barrier -0.00 (+0.14)
- **Calico**: Spellbreaker +0.07 (+0.26), Divine Barrier +0.07 (+0.20), Spirit Resilience +0.04 (+0.18)
- **Grey Talon**: Unstoppable +0.06 (+0.21), Reactive Barrier +0.05 (+0.11), Debuff Reducer +0.04 (+0.13)
- **Mo & Krill**: Spellbreaker +0.06 (+0.25), Healbane +0.03 (+0.12), Spirit Resilience +0.03 (+0.17)
- **Shiv**: Healbane -0.01 (+0.08), Return Fire -0.01 (+0.08), Divine Barrier -0.02 (+0.12)
- **Ivy**: Indomitable +0.04 (+0.21), Unstoppable +0.02 (+0.17), Debuff Reducer +0.00 (+0.09)
- **Warden**: Debuff Reducer -0.01 (+0.08), Return Fire -0.01 (+0.08), Counterspell -0.02 (+0.06)
- **Yamato**: Healbane +0.08 (+0.17), Spellbreaker +0.04 (+0.23), Return Fire +0.04 (+0.13)
- **Lash**: Spirit Resilience +0.21 (+0.35), Spellbreaker +0.21 (+0.39), Witchmail +0.18 (+0.39)
- **Viscous**: Divine Barrier +0.16 (+0.30), Spirit Resilience +0.10 (+0.23), Spellbreaker +0.08 (+0.27)
- **Pocket**: Witchmail +0.14 (+0.35), Spirit Resilience +0.11 (+0.25), Spellbreaker +0.08 (+0.27)
- **Mirage**: Dispel Magic +0.38 (+0.47), Spellbreaker +0.07 (+0.25), Spirit Resilience +0.06 (+0.19)
- **Vyper**: Indomitable +0.31 (+0.47), Debuff Reducer +0.10 (+0.19), Unstoppable +0.08 (+0.23)
- **Sinclair**: Indomitable +0.12 (+0.29), Spellbreaker +0.05 (+0.24), Unstoppable +0.04 (+0.19)
- **Mina**: Return Fire +0.01 (+0.10), Counterspell -0.01 (+0.06), Divine Barrier -0.02 (+0.12)
- **Drifter**: Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.07), Healbane -0.03 (+0.06)
- **Venator**: Bullet Resilience +0.27 (+0.38), Debuff Reducer +0.08 (+0.17), Unstoppable +0.08 (+0.23)
- **Victor**: Spirit Resilience +0.12 (+0.26), Spellbreaker +0.10 (+0.29), Witchmail +0.01 (+0.22)
- **Paige**: Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.07), Healbane -0.02 (+0.07)
- **The Doorman**: Indomitable +0.24 (+0.40), Spirit Resilience +0.17 (+0.31), Divine Barrier +0.16 (+0.30)
- **Billy**: Spirit Resilience +0.06 (+0.20), Spellbreaker +0.06 (+0.25), Healbane +0.04 (+0.13)
- **Graves**: Healbane +0.12 (+0.21), Reactive Barrier +0.10 (+0.16), Witchmail +0.09 (+0.30)
- **Apollo**: Reactive Barrier +0.01 (+0.06), Counterspell -0.04 (+0.04), Healbane -0.05 (+0.04)
- **Deadman Danny**: Spellbreaker +0.22 (+0.40), Witchmail +0.21 (+0.43), Indomitable +0.21 (+0.38)
- **Rem**: Counterspell -0.02 (+0.06), Reactive Barrier -0.03 (+0.03), Return Fire -0.04 (+0.05)
- **Silver**: Dispel Magic +0.07 (+0.16), Indomitable +0.04 (+0.21), Reactive Barrier +0.02 (+0.08)
- **Celeste**: Spirit Resilience +0.12 (+0.26), Witchmail +0.10 (+0.32), Dispel Magic +0.05 (+0.14)
- **Rat King**: Return Fire +0.01 (+0.10), Counterspell -0.01 (+0.07), Divine Barrier -0.01 (+0.12)
- **Solomon**: Reactive Barrier -0.02 (+0.03), Counterspell -0.02 (+0.05), Return Fire -0.03 (+0.06)
- **Violet**: Unstoppable +0.06 (+0.21), Return Fire +0.03 (+0.12), Witchmail +0.03 (+0.24)
- **Nurse Harrow**: Healbane +0.07 (+0.16), Reactive Barrier -0.00 (+0.05), Counterspell -0.03 (+0.05)
- **Baba**: Healbane -0.01 (+0.08), Reactive Barrier -0.02 (+0.04), Counterspell -0.03 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.193 | +0.060 | +0.140 | Lash +0.43, Pocket +0.21, Celeste +0.17 | 10 heroes |
| Divine Barrier | 6,400 | +0.225 | +0.036 | +0.104 | Lash +0.25, Paradox +0.13, Abrams +0.09 | 0 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.064 | Mirage +0.30, Lash +0.10, Paradox +0.10 | 9 heroes |
| Indomitable | 6,400 | +0.164 | +0.026 | +0.130 | Vyper +0.40, Wraith +0.17, Abrams +0.17 | 0 heroes |
| Spellbreaker | 6,400 | +0.123 | +0.019 | +0.165 | Lash +0.36, Holliday +0.18, Wraith +0.14 | 0 heroes |
| Healbane | 1,600 | +0.029 | +0.018 | +0.066 | Yamato +0.12, Abrams +0.09, Infernus +0.06 | 23 heroes |
| Witchmail | 6,400 | +0.111 | +0.017 | +0.183 | Lash +0.29, Celeste +0.16, Pocket +0.09 | 1 heroes |
| Reactive Barrier | 1,600 | +0.020 | +0.013 | +0.042 | Paradox +0.12, Abrams +0.11, The Doorman +0.10 | 3 heroes |
| Bullet Resilience | 3,200 | +0.018 | +0.005 | +0.076 | Venator +0.18, Paradox +0.14, Lash +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.004 | +0.002 | +0.066 | Holliday +0.16, Rem +0.13, Vyper +0.08 | 0 heroes |
| Plated Armor | 6,400 | +0.009 | +0.001 | +0.103 | Holliday +0.23, Paradox +0.11, Lash +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.030 | -0.009 | +0.044 | Lash +0.05, Abrams +0.04, Nurse Harrow +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.078 | -0.012 | +0.113 | Holliday +0.14, Abrams +0.12, Rem +0.12 | 0 heroes |
| Metal Skin | 3,200 | -0.199 | -0.062 | +0.088 | Wraith +0.27, Lash +0.18, Paradox +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.200 | -0.125 | +0.062 | Paradox +0.11, Lash +0.07, Vindicta +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.09 (+0.25), Unstoppable +0.08 (+0.19), Dispel Magic +0.08 (+0.14)
- **Seven**: Witchmail +0.03 (+0.21), Healbane -0.01 (+0.06), Counterspell -0.01 (+0.03)
- **Vindicta**: Return Fire +0.04 (+0.11), Divine Barrier +0.04 (+0.15), Witchmail +0.03 (+0.21)
- **Lady Geist**: Spirit Resilience +0.10 (+0.24), Spellbreaker +0.10 (+0.27), Divine Barrier +0.05 (+0.15)
- **Abrams**: Indomitable +0.17 (+0.30), Unstoppable +0.12 (+0.24), Reactive Barrier +0.11 (+0.15)
- **Wraith**: Metal Skin +0.27 (+0.36), Indomitable +0.17 (+0.30), Spellbreaker +0.14 (+0.30)
- **McGinnis**: Spirit Resilience +0.01 (+0.15), Healbane -0.02 (+0.05), Counterspell -0.02 (+0.02)
- **Paradox**: Bullet Resilience +0.14 (+0.21), Metal Skin +0.13 (+0.22), Divine Barrier +0.13 (+0.23)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.04 (+0.00)
- **Kelvin**: Spirit Resilience +0.04 (+0.18), Witchmail -0.00 (+0.18), Dispel Magic -0.02 (+0.05)
- **Haze**: Indomitable +0.10 (+0.23), Plated Armor +0.08 (+0.18), Unstoppable +0.06 (+0.17)
- **Holliday**: Plated Armor +0.23 (+0.33), Spellbreaker +0.18 (+0.34), Debuff Reducer +0.16 (+0.22)
- **Bebop**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Return Fire -0.02 (+0.04)
- **Calico**: Reactive Barrier +0.08 (+0.12), Divine Barrier +0.03 (+0.14), Dispel Magic +0.02 (+0.09)
- **Grey Talon**: Unstoppable +0.10 (+0.21), Debuff Reducer +0.06 (+0.13), Spellbreaker +0.05 (+0.21)
- **Mo & Krill**: Spellbreaker +0.08 (+0.25), Unstoppable +0.08 (+0.19), Spirit Resilience +0.04 (+0.18)
- **Shiv**: Bullet Resilience +0.06 (+0.13), Plated Armor +0.03 (+0.13), Divine Barrier +0.02 (+0.12)
- **Ivy**: Unstoppable +0.07 (+0.18), Indomitable +0.04 (+0.17), Bullet Resilience +0.02 (+0.10)
- **Warden**: Return Fire +0.03 (+0.10), Divine Barrier -0.00 (+0.10), Debuff Reducer -0.01 (+0.06)
- **Yamato**: Healbane +0.12 (+0.18), Debuff Reducer +0.02 (+0.09), Counterspell +0.01 (+0.05)
- **Lash**: Spirit Resilience +0.43 (+0.57), Spellbreaker +0.36 (+0.53), Witchmail +0.29 (+0.48)
- **Viscous**: Divine Barrier +0.02 (+0.13), Counterspell +0.01 (+0.06), Debuff Reducer -0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.21 (+0.35), Witchmail +0.09 (+0.27), Spellbreaker +0.06 (+0.22)
- **Mirage**: Dispel Magic +0.30 (+0.36), Spirit Resilience +0.06 (+0.20), Spellbreaker +0.05 (+0.21)
- **Vyper**: Indomitable +0.40 (+0.53), Spellbreaker +0.10 (+0.26), Debuff Reducer +0.08 (+0.15)
- **Sinclair**: Indomitable +0.12 (+0.25), Spellbreaker +0.00 (+0.17), Reactive Barrier -0.00 (+0.04)
- **Mina**: Counterspell +0.01 (+0.05), Divine Barrier +0.00 (+0.11), Plated Armor -0.00 (+0.10)
- **Drifter**: Return Fire +0.01 (+0.08), Counterspell +0.00 (+0.05), Healbane +0.00 (+0.07)
- **Venator**: Bullet Resilience +0.18 (+0.26), Debuff Reducer +0.06 (+0.13), Unstoppable +0.04 (+0.15)
- **Victor**: Spellbreaker +0.07 (+0.24), Spirit Resilience +0.06 (+0.20), Healbane +0.02 (+0.08)
- **Paige**: Counterspell -0.00 (+0.04), Return Fire -0.02 (+0.04), Healbane -0.03 (+0.04)
- **The Doorman**: Indomitable +0.13 (+0.26), Reactive Barrier +0.10 (+0.14), Divine Barrier +0.09 (+0.19)
- **Billy**: Counterspell +0.00 (+0.04), Healbane -0.00 (+0.06), Dispel Magic -0.01 (+0.05)
- **Graves**: Metal Skin +0.07 (+0.16), Reactive Barrier +0.05 (+0.09), Witchmail +0.04 (+0.23)
- **Apollo**: Reactive Barrier +0.02 (+0.06), Counterspell -0.01 (+0.03), Healbane -0.02 (+0.04)
- **Deadman Danny**: Indomitable +0.09 (+0.22), Spirit Resilience +0.08 (+0.22), Witchmail +0.07 (+0.25)
- **Rem**: Debuff Reducer +0.13 (+0.19), Unstoppable +0.12 (+0.23), Spellbreaker +0.04 (+0.21)
- **Silver**: Dispel Magic +0.08 (+0.15), Debuff Reducer +0.02 (+0.09), Reactive Barrier +0.02 (+0.06)
- **Celeste**: Spirit Resilience +0.17 (+0.31), Witchmail +0.16 (+0.34), Spellbreaker +0.07 (+0.23)
- **Rat King**: Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.04), Bullet Resilience -0.02 (+0.05)
- **Solomon**: Reactive Barrier -0.01 (+0.03), Counterspell -0.01 (+0.03), Return Fire -0.03 (+0.03)
- **Violet**: Unstoppable +0.06 (+0.18), Witchmail +0.06 (+0.24), Healbane +0.04 (+0.11)
- **Nurse Harrow**: Healbane +0.06 (+0.12), Counterspell +0.03 (+0.07), Divine Barrier +0.01 (+0.12)
- **Baba**: Unstoppable -0.00 (+0.11), Healbane -0.01 (+0.06), Counterspell -0.01 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.180 | +0.056 | +0.139 | Lash +0.41, Deadman Danny +0.21, Viscous +0.18 | 13 heroes |
| Divine Barrier | 6,400 | +0.188 | +0.029 | +0.092 | Lash +0.16, Calico +0.08, Viscous +0.08 | 2 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.052 | Mirage +0.24, Lash +0.12, Infernus +0.11 | 11 heroes |
| Indomitable | 6,400 | +0.164 | +0.026 | +0.133 | Vyper +0.36, Wraith +0.21, Deadman Danny +0.19 | 0 heroes |
| Spellbreaker | 6,400 | +0.142 | +0.022 | +0.180 | Lash +0.38, Wraith +0.18, Holliday +0.17 | 0 heroes |
| Healbane | 1,600 | +0.027 | +0.017 | +0.063 | Mo & Krill +0.08, Infernus +0.08, Yamato +0.05 | 25 heroes |
| Witchmail | 6,400 | +0.097 | +0.015 | +0.170 | Lash +0.20, Deadman Danny +0.17, Violet +0.11 | 1 heroes |
| Debuff Reducer | 1,600 | +0.007 | +0.005 | +0.072 | Holliday +0.18, Bebop +0.17, Grey Talon +0.14 | 0 heroes |
| Bullet Resilience | 3,200 | +0.013 | +0.004 | +0.061 | Venator +0.21, Vindicta +0.11, Haze +0.10 | 1 heroes |
| Plated Armor | 6,400 | +0.009 | +0.001 | +0.095 | Holliday +0.20, Haze +0.12, Deadman Danny +0.10 | 0 heroes |
| Reactive Barrier | 1,600 | -0.009 | -0.005 | +0.033 | Deadman Danny +0.13, Vyper +0.06, Calico +0.06 | 2 heroes |
| Counterspell | 3,200 | -0.036 | -0.011 | +0.033 | Grey Talon +0.03, Yamato +0.02, Vindicta +0.02 | 1 heroes |
| Unstoppable | 6,400 | -0.072 | -0.011 | +0.122 | Mo & Krill +0.22, Haze +0.17, Grey Talon +0.16 | 3 heroes |
| Metal Skin | 3,200 | -0.198 | -0.062 | +0.084 | Wraith +0.22, Haze +0.11, Lash +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.195 | -0.122 | +0.058 | Haze +0.11, Vindicta +0.05, Vyper +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.16), Spellbreaker +0.10 (+0.28), Healbane +0.08 (+0.14)
- **Seven**: Witchmail +0.10 (+0.27), Spirit Resilience +0.07 (+0.21), Indomitable +0.07 (+0.20)
- **Vindicta**: Bullet Resilience +0.11 (+0.17), Plated Armor +0.08 (+0.17), Divine Barrier +0.07 (+0.17)
- **Lady Geist**: Spirit Resilience +0.06 (+0.19), Divine Barrier +0.04 (+0.14), Witchmail +0.04 (+0.21)
- **Abrams**: Unstoppable +0.07 (+0.19), Dispel Magic +0.06 (+0.11), Reactive Barrier +0.02 (+0.06)
- **Wraith**: Metal Skin +0.22 (+0.30), Indomitable +0.21 (+0.34), Spellbreaker +0.18 (+0.36)
- **McGinnis**: Spirit Resilience +0.02 (+0.16), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05)
- **Paradox**: Witchmail +0.05 (+0.22), Dispel Magic +0.05 (+0.10), Return Fire +0.04 (+0.10)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.04 (-0.00)
- **Kelvin**: Healbane +0.02 (+0.08), Counterspell +0.01 (+0.04), Spirit Resilience +0.00 (+0.14)
- **Haze**: Indomitable +0.19 (+0.32), Unstoppable +0.17 (+0.29), Plated Armor +0.12 (+0.22)
- **Holliday**: Plated Armor +0.20 (+0.29), Debuff Reducer +0.18 (+0.25), Spellbreaker +0.17 (+0.35)
- **Bebop**: Debuff Reducer +0.17 (+0.24), Unstoppable +0.14 (+0.26), Spellbreaker +0.12 (+0.30)
- **Calico**: Spirit Resilience +0.09 (+0.23), Divine Barrier +0.08 (+0.17), Indomitable +0.06 (+0.20)
- **Grey Talon**: Unstoppable +0.16 (+0.28), Debuff Reducer +0.14 (+0.22), Spellbreaker +0.12 (+0.30)
- **Mo & Krill**: Unstoppable +0.22 (+0.34), Spellbreaker +0.10 (+0.28), Healbane +0.08 (+0.14)
- **Shiv**: Bullet Resilience +0.05 (+0.11), Divine Barrier +0.03 (+0.12), Plated Armor +0.02 (+0.12)
- **Ivy**: Unstoppable +0.02 (+0.14), Indomitable +0.02 (+0.15), Metal Skin +0.01 (+0.09)
- **Warden**: Debuff Reducer +0.00 (+0.07), Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Yamato**: Healbane +0.05 (+0.11), Witchmail +0.03 (+0.20), Debuff Reducer +0.03 (+0.10)
- **Lash**: Spirit Resilience +0.41 (+0.55), Spellbreaker +0.38 (+0.56), Witchmail +0.20 (+0.37)
- **Viscous**: Spirit Resilience +0.18 (+0.32), Spellbreaker +0.08 (+0.26), Divine Barrier +0.08 (+0.17)
- **Pocket**: Spirit Resilience +0.07 (+0.21), Witchmail +0.03 (+0.20), Counterspell -0.01 (+0.03)
- **Mirage**: Dispel Magic +0.24 (+0.29), Metal Skin +0.01 (+0.10), Debuff Reducer +0.01 (+0.08)
- **Vyper**: Indomitable +0.36 (+0.49), Spellbreaker +0.08 (+0.26), Debuff Reducer +0.07 (+0.15)
- **Sinclair**: Indomitable +0.14 (+0.28), Unstoppable +0.09 (+0.21), Debuff Reducer +0.03 (+0.10)
- **Mina**: Divine Barrier +0.08 (+0.17), Witchmail +0.06 (+0.23), Spirit Resilience +0.06 (+0.20)
- **Drifter**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02), Return Fire -0.02 (+0.04)
- **Venator**: Bullet Resilience +0.21 (+0.27), Plated Armor +0.06 (+0.15), Unstoppable +0.04 (+0.16)
- **Victor**: Spellbreaker +0.05 (+0.23), Healbane +0.03 (+0.10), Spirit Resilience +0.03 (+0.17)
- **Paige**: Counterspell +0.01 (+0.04), Divine Barrier -0.01 (+0.08), Witchmail -0.02 (+0.15)
- **The Doorman**: Indomitable +0.12 (+0.26), Witchmail +0.10 (+0.27), Divine Barrier +0.04 (+0.13)
- **Billy**: Indomitable +0.02 (+0.15), Healbane +0.01 (+0.07), Reactive Barrier +0.01 (+0.04)
- **Graves**: Return Fire +0.04 (+0.10), Reactive Barrier +0.02 (+0.05), Counterspell +0.01 (+0.04)
- **Apollo**: Healbane +0.02 (+0.08), Reactive Barrier +0.01 (+0.05), Counterspell -0.01 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.21 (+0.34), Indomitable +0.19 (+0.32), Witchmail +0.17 (+0.34)
- **Rem**: Debuff Reducer +0.10 (+0.17), Unstoppable +0.08 (+0.20), Spellbreaker +0.02 (+0.20)
- **Silver**: Dispel Magic +0.05 (+0.10), Reactive Barrier +0.04 (+0.08), Bullet Resilience +0.03 (+0.09)
- **Celeste**: Witchmail +0.09 (+0.26), Spirit Resilience +0.07 (+0.21), Healbane +0.05 (+0.11)
- **Rat King**: Return Fire -0.00 (+0.06), Bullet Resilience -0.01 (+0.05), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.03 (+0.06), Return Fire +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Violet**: Witchmail +0.11 (+0.28), Divine Barrier +0.05 (+0.14), Unstoppable +0.03 (+0.15)
- **Nurse Harrow**: Divine Barrier +0.07 (+0.16), Witchmail +0.05 (+0.22), Healbane +0.04 (+0.10)
- **Baba**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (+0.01)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.162 | +0.051 | +0.143 | The Doorman +0.48, Viscous +0.36, Deadman Danny +0.36 | 16 heroes |
| Indomitable | 6,400 | +0.187 | +0.029 | +0.165 | Wraith +0.40, Deadman Danny +0.28, Vyper +0.25 | 2 heroes |
| Dispel Magic | 3,200 | +0.089 | +0.028 | +0.060 | Mirage +0.33, Lash +0.21, Paradox +0.14 | 10 heroes |
| Spellbreaker | 6,400 | +0.162 | +0.025 | +0.200 | Deadman Danny +0.30, Holliday +0.27, Wraith +0.22 | 0 heroes |
| Divine Barrier | 6,400 | +0.154 | +0.024 | +0.084 | Viscous +0.26, The Doorman +0.13, Lash +0.11 | 2 heroes |
| Healbane | 1,600 | +0.027 | +0.017 | +0.060 | Lady Geist +0.12, Yamato +0.07, The Doorman +0.06 | 22 heroes |
| Witchmail | 6,400 | +0.103 | +0.016 | +0.175 | The Doorman +0.33, Deadman Danny +0.32, Paradox +0.17 | 1 heroes |
| Debuff Reducer | 1,600 | +0.009 | +0.006 | +0.093 | Holliday +0.25, Paige +0.20, Grey Talon +0.15 | 0 heroes |
| Bullet Resilience | 3,200 | +0.010 | +0.003 | +0.057 | Viscous +0.14, Vindicta +0.14, Paradox +0.09 | 1 heroes |
| Plated Armor | 6,400 | +0.004 | +0.001 | +0.098 | Viscous +0.12, Vindicta +0.12, Haze +0.11 | 4 heroes |
| Unstoppable | 6,400 | -0.062 | -0.010 | +0.156 | Paige +0.27, Holliday +0.21, Paradox +0.20 | 5 heroes |
| Reactive Barrier | 1,600 | -0.016 | -0.010 | +0.037 | The Doorman +0.14, Paradox +0.08, Deadman Danny +0.07 | 2 heroes |
| Counterspell | 3,200 | -0.040 | -0.013 | +0.029 | Viscous +0.09, The Doorman +0.06, Lash +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.199 | -0.062 | +0.081 | Wraith +0.19, Viscous +0.16, Paradox +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.191 | -0.120 | +0.050 | Vindicta +0.11, Viscous +0.11, Paradox +0.09 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.17 (+0.33), Spellbreaker +0.13 (+0.33), Dispel Magic +0.09 (+0.15)
- **Seven**: Witchmail +0.04 (+0.21), Healbane +0.00 (+0.06), Indomitable -0.00 (+0.16)
- **Vindicta**: Bullet Resilience +0.14 (+0.20), Plated Armor +0.12 (+0.22), Return Fire +0.11 (+0.16)
- **Lady Geist**: Healbane +0.12 (+0.19), Spirit Resilience +0.09 (+0.23), Witchmail +0.06 (+0.24)
- **Abrams**: Dispel Magic +0.04 (+0.10), Debuff Reducer +0.01 (+0.11), Healbane +0.01 (+0.07)
- **Wraith**: Indomitable +0.40 (+0.57), Spellbreaker +0.22 (+0.42), Metal Skin +0.19 (+0.27)
- **McGinnis**: Spirit Resilience +0.02 (+0.16), Healbane -0.00 (+0.06), Dispel Magic -0.01 (+0.05)
- **Paradox**: Unstoppable +0.20 (+0.35), Witchmail +0.17 (+0.35), Metal Skin +0.14 (+0.22)
- **Dynamo**: Healbane -0.01 (+0.05), Counterspell -0.01 (+0.01), Reactive Barrier -0.04 (-0.00)
- **Kelvin**: Spirit Resilience +0.03 (+0.17), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Haze**: Unstoppable +0.17 (+0.33), Plated Armor +0.11 (+0.21), Bullet Resilience +0.08 (+0.13)
- **Holliday**: Spellbreaker +0.27 (+0.47), Debuff Reducer +0.25 (+0.34), Unstoppable +0.21 (+0.36)
- **Bebop**: Debuff Reducer +0.14 (+0.24), Unstoppable +0.10 (+0.26), Spellbreaker +0.07 (+0.27)
- **Calico**: Spirit Resilience +0.14 (+0.29), Divine Barrier +0.05 (+0.13), Reactive Barrier +0.03 (+0.07)
- **Grey Talon**: Spirit Resilience +0.24 (+0.38), Spellbreaker +0.21 (+0.41), Witchmail +0.16 (+0.34)
- **Mo & Krill**: Spellbreaker +0.11 (+0.31), Unstoppable +0.07 (+0.23), Debuff Reducer +0.07 (+0.17)
- **Shiv**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.07 (+0.15), Plated Armor +0.04 (+0.14)
- **Ivy**: Unstoppable +0.19 (+0.34), Indomitable +0.12 (+0.29), Debuff Reducer +0.09 (+0.18)
- **Warden**: Return Fire +0.02 (+0.07), Divine Barrier +0.01 (+0.10), Witchmail +0.00 (+0.18)
- **Yamato**: Healbane +0.07 (+0.13), Counterspell +0.01 (+0.04), Return Fire -0.01 (+0.03)
- **Lash**: Spirit Resilience +0.31 (+0.45), Dispel Magic +0.21 (+0.27), Witchmail +0.17 (+0.34)
- **Viscous**: Spirit Resilience +0.36 (+0.51), Divine Barrier +0.26 (+0.34), Spellbreaker +0.21 (+0.41)
- **Pocket**: Spirit Resilience +0.02 (+0.16), Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.02)
- **Mirage**: Dispel Magic +0.33 (+0.39), Unstoppable +0.16 (+0.32), Metal Skin +0.10 (+0.18)
- **Vyper**: Indomitable +0.25 (+0.41), Metal Skin +0.04 (+0.13), Plated Armor +0.04 (+0.14)
- **Sinclair**: Indomitable +0.20 (+0.37), Debuff Reducer +0.06 (+0.15), Spellbreaker +0.05 (+0.25)
- **Mina**: Divine Barrier +0.03 (+0.11), Counterspell +0.01 (+0.03), Return Fire -0.01 (+0.04)
- **Drifter**: Dispel Magic +0.09 (+0.15), Reactive Barrier +0.01 (+0.04), Debuff Reducer -0.00 (+0.09)
- **Venator**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.04 (+0.12), Counterspell -0.02 (+0.01)
- **Victor**: Spellbreaker +0.07 (+0.27), Spirit Resilience +0.07 (+0.21), Healbane +0.06 (+0.12)
- **Paige**: Unstoppable +0.27 (+0.43), Debuff Reducer +0.20 (+0.29), Spellbreaker +0.10 (+0.30)
- **The Doorman**: Spirit Resilience +0.48 (+0.62), Witchmail +0.33 (+0.50), Indomitable +0.24 (+0.41)
- **Billy**: Reactive Barrier +0.02 (+0.06), Healbane -0.02 (+0.04), Counterspell -0.03 (+0.00)
- **Graves**: Return Fire +0.04 (+0.09), Metal Skin +0.03 (+0.12), Reactive Barrier +0.03 (+0.07)
- **Apollo**: Reactive Barrier +0.02 (+0.06), Healbane +0.02 (+0.08), Counterspell -0.01 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.36 (+0.50), Witchmail +0.32 (+0.49), Spellbreaker +0.30 (+0.50)
- **Rem**: Divine Barrier +0.10 (+0.19), Spirit Resilience +0.06 (+0.21), Witchmail +0.02 (+0.20)
- **Silver**: Dispel Magic +0.10 (+0.16), Metal Skin +0.07 (+0.15), Bullet Resilience +0.06 (+0.11)
- **Celeste**: Witchmail +0.12 (+0.30), Spirit Resilience +0.06 (+0.20), Plated Armor +0.05 (+0.15)
- **Rat King**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02), Metal Skin -0.01 (+0.07)
- **Solomon**: Counterspell -0.00 (+0.03), Reactive Barrier -0.01 (+0.03), Return Fire -0.02 (+0.03)
- **Violet**: Witchmail +0.08 (+0.25), Dispel Magic +0.06 (+0.12), Spirit Resilience +0.05 (+0.19)
- **Nurse Harrow**: Spirit Resilience +0.18 (+0.32), Divine Barrier +0.05 (+0.13), Healbane +0.02 (+0.08)
- **Baba**: Counterspell +0.01 (+0.04), Healbane +0.01 (+0.07), Debuff Reducer -0.01 (+0.09)
