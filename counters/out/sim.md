# Counter items in the sim (phantom and up)

Built 2026-11-08T15:46:10Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.130 | Lash +0.20, Deadman Danny +0.19, The Doorman +0.17 | 1 heroes |
| Divine Barrier | 6,400 | +0.286 | +0.045 | +0.129 | Lash +0.16, The Doorman +0.15, Abrams +0.12 | 0 heroes |
| Dispel Magic | 3,200 | +0.088 | +0.028 | +0.083 | Mirage +0.38, Lash +0.12, Deadman Danny +0.11 | 4 heroes |
| Indomitable | 6,400 | +0.173 | +0.027 | +0.157 | Vyper +0.31, The Doorman +0.23, Deadman Danny +0.21 | 0 heroes |
| Healbane | 1,600 | +0.040 | +0.025 | +0.086 | Graves +0.12, Yamato +0.08, Nurse Harrow +0.07 | 22 heroes |
| Reactive Barrier | 1,600 | +0.033 | +0.020 | +0.052 | Deadman Danny +0.14, Graves +0.11, The Doorman +0.10 | 2 heroes |
| Witchmail | 6,400 | +0.099 | +0.015 | +0.205 | Deadman Danny +0.21, Lash +0.17, Pocket +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.022 | +0.014 | +0.078 | Holliday +0.12, Vyper +0.11, Venator +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | +0.044 | +0.014 | +0.105 | Venator +0.28, Lash +0.15, Deadman Danny +0.12 | 0 heroes |
| Spellbreaker | 6,400 | +0.080 | +0.012 | +0.176 | Deadman Danny +0.22, Lash +0.21, Wraith +0.15 | 0 heroes |
| Plated Armor | 6,400 | +0.007 | +0.001 | +0.139 | Holliday +0.20, Deadman Danny +0.12, Wraith +0.12 | 0 heroes |
| Counterspell | 3,200 | -0.006 | -0.002 | +0.075 | Lash +0.11, Graves +0.08, Deadman Danny +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.057 | -0.009 | +0.140 | Deadman Danny +0.15, Lash +0.11, Holliday +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.182 | -0.057 | +0.114 | Wraith +0.22, Lash +0.17, Paradox +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.187 | -0.117 | +0.085 | Paradox +0.09, Deadman Danny +0.06, The Doorman +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.07 (+0.15), Spellbreaker +0.06 (+0.23), Unstoppable +0.05 (+0.18)
- **Seven**: Healbane -0.00 (+0.09), Spirit Resilience -0.01 (+0.12), Witchmail -0.01 (+0.19)
- **Vindicta**: Divine Barrier +0.00 (+0.13), Counterspell -0.00 (+0.07), Healbane -0.00 (+0.08)
- **Lady Geist**: Return Fire +0.02 (+0.10), Divine Barrier -0.00 (+0.13), Counterspell -0.01 (+0.07)
- **Abrams**: Indomitable +0.19 (+0.35), Divine Barrier +0.12 (+0.25), Witchmail +0.08 (+0.28)
- **Wraith**: Metal Skin +0.22 (+0.33), Indomitable +0.18 (+0.33), Spellbreaker +0.15 (+0.33)
- **McGinnis**: Counterspell +0.04 (+0.12), Spirit Resilience +0.03 (+0.16), Healbane +0.03 (+0.11)
- **Paradox**: Metal Skin +0.13 (+0.25), Bullet Resilience +0.11 (+0.22), Return Fire +0.09 (+0.18)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.03 (+0.05), Reactive Barrier -0.04 (+0.02)
- **Kelvin**: Witchmail +0.01 (+0.21), Healbane +0.00 (+0.09), Counterspell -0.01 (+0.07)
- **Haze**: Indomitable +0.12 (+0.28), Plated Armor +0.11 (+0.24), Unstoppable +0.08 (+0.22)
- **Holliday**: Plated Armor +0.20 (+0.34), Spellbreaker +0.13 (+0.31), Debuff Reducer +0.12 (+0.19)
- **Bebop**: Healbane +0.01 (+0.10), Counterspell +0.00 (+0.08), Divine Barrier -0.00 (+0.13)
- **Calico**: Spellbreaker +0.08 (+0.25), Divine Barrier +0.08 (+0.20), Spirit Resilience +0.05 (+0.18)
- **Grey Talon**: Unstoppable +0.06 (+0.20), Reactive Barrier +0.06 (+0.11), Debuff Reducer +0.05 (+0.13)
- **Mo & Krill**: Spellbreaker +0.06 (+0.24), Spirit Resilience +0.04 (+0.17), Healbane +0.03 (+0.12)
- **Shiv**: Return Fire -0.00 (+0.08), Healbane -0.01 (+0.08), Divine Barrier -0.01 (+0.11)
- **Ivy**: Indomitable +0.05 (+0.20), Unstoppable +0.03 (+0.17), Debuff Reducer +0.01 (+0.09)
- **Warden**: Debuff Reducer -0.00 (+0.07), Return Fire -0.00 (+0.08), Counterspell -0.02 (+0.06)
- **Yamato**: Healbane +0.08 (+0.17), Spellbreaker +0.05 (+0.23), Debuff Reducer +0.05 (+0.13)
- **Lash**: Spellbreaker +0.21 (+0.38), Spirit Resilience +0.20 (+0.33), Witchmail +0.17 (+0.38)
- **Viscous**: Divine Barrier -0.01 (+0.12), Healbane -0.04 (+0.05), Return Fire -0.04 (+0.05)
- **Pocket**: Witchmail +0.14 (+0.34), Spirit Resilience +0.12 (+0.24), Spellbreaker +0.09 (+0.26)
- **Mirage**: Dispel Magic +0.38 (+0.46), Spellbreaker +0.07 (+0.25), Spirit Resilience +0.06 (+0.19)
- **Vyper**: Indomitable +0.31 (+0.47), Debuff Reducer +0.11 (+0.18), Unstoppable +0.09 (+0.23)
- **Sinclair**: Indomitable +0.13 (+0.29), Spellbreaker +0.06 (+0.24), Unstoppable +0.04 (+0.18)
- **Mina**: Return Fire +0.01 (+0.10), Divine Barrier -0.01 (+0.12), Counterspell -0.01 (+0.06)
- **Drifter**: Counterspell -0.02 (+0.05), Return Fire -0.02 (+0.06), Healbane -0.02 (+0.06)
- **Venator**: Bullet Resilience +0.28 (+0.38), Debuff Reducer +0.09 (+0.17), Unstoppable +0.09 (+0.23)
- **Victor**: Spirit Resilience +0.12 (+0.25), Spellbreaker +0.11 (+0.28), Witchmail +0.01 (+0.22)
- **Paige**: Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.07), Reactive Barrier -0.02 (+0.03)
- **The Doorman**: Indomitable +0.23 (+0.38), Spirit Resilience +0.17 (+0.30), Divine Barrier +0.15 (+0.28)
- **Billy**: Spellbreaker +0.06 (+0.24), Spirit Resilience +0.06 (+0.19), Healbane +0.04 (+0.13)
- **Graves**: Healbane +0.12 (+0.20), Reactive Barrier +0.11 (+0.16), Metal Skin +0.10 (+0.21)
- **Apollo**: Reactive Barrier +0.01 (+0.06), Counterspell -0.03 (+0.04), Healbane -0.04 (+0.04)
- **Deadman Danny**: Spellbreaker +0.22 (+0.40), Witchmail +0.21 (+0.42), Indomitable +0.21 (+0.37)
- **Rem**: Reactive Barrier -0.01 (+0.04), Healbane -0.02 (+0.07), Dispel Magic -0.02 (+0.06)
- **Silver**: Dispel Magic +0.08 (+0.16), Indomitable +0.04 (+0.20), Reactive Barrier +0.02 (+0.07)
- **Celeste**: Spirit Resilience +0.13 (+0.26), Witchmail +0.12 (+0.32), Spellbreaker +0.04 (+0.22)
- **Rat King**: Return Fire +0.01 (+0.09), Divine Barrier -0.01 (+0.12), Counterspell -0.01 (+0.06)
- **Solomon**: Reactive Barrier -0.02 (+0.03), Counterspell -0.02 (+0.05), Return Fire -0.03 (+0.06)
- **Violet**: Unstoppable +0.06 (+0.20), Witchmail +0.03 (+0.24), Return Fire +0.03 (+0.12)
- **Nurse Harrow**: Healbane +0.07 (+0.15), Reactive Barrier +0.00 (+0.05), Counterspell -0.02 (+0.05)
- **Baba**: Healbane -0.01 (+0.07), Reactive Barrier -0.02 (+0.03), Counterspell -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.193 | +0.060 | +0.135 | Lash +0.36, Pocket +0.20, Celeste +0.20 | 10 heroes |
| Divine Barrier | 6,400 | +0.207 | +0.033 | +0.100 | Lash +0.22, The Doorman +0.12, Paradox +0.09 | 0 heroes |
| Indomitable | 6,400 | +0.165 | +0.026 | +0.126 | Vyper +0.41, Wraith +0.17, The Doorman +0.16 | 0 heroes |
| Dispel Magic | 3,200 | +0.077 | +0.024 | +0.063 | Mirage +0.31, Abrams +0.11, Silver +0.08 | 9 heroes |
| Spellbreaker | 6,400 | +0.122 | +0.019 | +0.163 | Lash +0.33, Holliday +0.17, Wraith +0.14 | 0 heroes |
| Healbane | 1,600 | +0.029 | +0.018 | +0.066 | Yamato +0.13, Lady Geist +0.08, Infernus +0.05 | 23 heroes |
| Witchmail | 6,400 | +0.114 | +0.018 | +0.183 | Lash +0.24, Celeste +0.17, The Doorman +0.11 | 1 heroes |
| Reactive Barrier | 1,600 | +0.019 | +0.012 | +0.039 | The Doorman +0.13, Calico +0.09, Abrams +0.08 | 3 heroes |
| Bullet Resilience | 3,200 | +0.019 | +0.006 | +0.074 | Venator +0.19, Paradox +0.11, Lash +0.08 | 0 heroes |
| Debuff Reducer | 1,600 | +0.005 | +0.003 | +0.068 | Holliday +0.15, Rem +0.12, Vyper +0.08 | 0 heroes |
| Plated Armor | 6,400 | +0.015 | +0.002 | +0.101 | Holliday +0.22, Wraith +0.10, Paradox +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.020 | -0.006 | +0.046 | Paradox +0.05, Yamato +0.05, Lash +0.02 | 1 heroes |
| Unstoppable | 6,400 | -0.078 | -0.012 | +0.113 | Holliday +0.13, Abrams +0.12, Rem +0.12 | 0 heroes |
| Metal Skin | 3,200 | -0.199 | -0.062 | +0.088 | Wraith +0.28, Lash +0.14, Paradox +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.196 | -0.123 | +0.059 | Paradox +0.09, Vindicta +0.05, Lash +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.08 (+0.14), Spellbreaker +0.07 (+0.23), Unstoppable +0.06 (+0.17)
- **Seven**: Witchmail +0.08 (+0.26), Healbane +0.02 (+0.08), Spirit Resilience +0.01 (+0.15)
- **Vindicta**: Return Fire +0.05 (+0.11), Divine Barrier +0.05 (+0.15), Witchmail +0.03 (+0.22)
- **Lady Geist**: Spirit Resilience +0.14 (+0.28), Spellbreaker +0.10 (+0.26), Healbane +0.08 (+0.15)
- **Abrams**: Indomitable +0.15 (+0.27), Unstoppable +0.12 (+0.23), Dispel Magic +0.11 (+0.17)
- **Wraith**: Metal Skin +0.28 (+0.37), Indomitable +0.17 (+0.30), Spellbreaker +0.14 (+0.31)
- **McGinnis**: Spirit Resilience +0.03 (+0.16), Healbane +0.03 (+0.09), Dispel Magic +0.01 (+0.07)
- **Paradox**: Bullet Resilience +0.11 (+0.18), Metal Skin +0.10 (+0.18), Return Fire +0.09 (+0.15)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.04 (+0.00)
- **Kelvin**: Spirit Resilience +0.05 (+0.18), Witchmail +0.00 (+0.19), Dispel Magic -0.01 (+0.05)
- **Haze**: Indomitable +0.10 (+0.22), Plated Armor +0.08 (+0.18), Unstoppable +0.05 (+0.17)
- **Holliday**: Plated Armor +0.22 (+0.32), Spellbreaker +0.17 (+0.33), Debuff Reducer +0.15 (+0.22)
- **Bebop**: Healbane +0.01 (+0.08), Counterspell -0.02 (+0.03), Divine Barrier -0.02 (+0.08)
- **Calico**: Reactive Barrier +0.09 (+0.12), Divine Barrier +0.04 (+0.14), Dispel Magic +0.02 (+0.09)
- **Grey Talon**: Unstoppable +0.09 (+0.21), Debuff Reducer +0.05 (+0.12), Spellbreaker +0.04 (+0.20)
- **Mo & Krill**: Unstoppable +0.08 (+0.19), Spellbreaker +0.08 (+0.24), Dispel Magic +0.04 (+0.11)
- **Shiv**: Bullet Resilience +0.05 (+0.12), Plated Armor +0.02 (+0.12), Divine Barrier +0.01 (+0.11)
- **Ivy**: Unstoppable +0.10 (+0.21), Debuff Reducer +0.05 (+0.12), Indomitable +0.01 (+0.14)
- **Warden**: Return Fire +0.04 (+0.10), Divine Barrier +0.02 (+0.12), Debuff Reducer +0.01 (+0.08)
- **Yamato**: Healbane +0.13 (+0.19), Debuff Reducer +0.07 (+0.14), Counterspell +0.05 (+0.10)
- **Lash**: Spirit Resilience +0.36 (+0.49), Spellbreaker +0.33 (+0.49), Witchmail +0.24 (+0.42)
- **Viscous**: Divine Barrier +0.03 (+0.13), Counterspell +0.01 (+0.05), Healbane -0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.20 (+0.34), Witchmail +0.08 (+0.26), Spellbreaker +0.05 (+0.21)
- **Mirage**: Dispel Magic +0.31 (+0.37), Spirit Resilience +0.07 (+0.21), Spellbreaker +0.05 (+0.22)
- **Vyper**: Indomitable +0.41 (+0.53), Spellbreaker +0.10 (+0.26), Debuff Reducer +0.08 (+0.15)
- **Sinclair**: Indomitable +0.13 (+0.25), Spellbreaker +0.01 (+0.17), Reactive Barrier +0.00 (+0.04)
- **Mina**: Counterspell +0.02 (+0.06), Divine Barrier +0.01 (+0.11), Return Fire +0.01 (+0.07)
- **Drifter**: Healbane +0.00 (+0.07), Counterspell -0.00 (+0.04), Reactive Barrier -0.02 (+0.02)
- **Venator**: Bullet Resilience +0.19 (+0.27), Debuff Reducer +0.06 (+0.13), Unstoppable +0.05 (+0.16)
- **Victor**: Spirit Resilience +0.08 (+0.21), Spellbreaker +0.07 (+0.23), Healbane +0.00 (+0.07)
- **Paige**: Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.05), Divine Barrier -0.02 (+0.08)
- **The Doorman**: Indomitable +0.16 (+0.29), Reactive Barrier +0.13 (+0.16), Divine Barrier +0.12 (+0.22)
- **Billy**: Counterspell -0.00 (+0.04), Healbane -0.00 (+0.06), Dispel Magic -0.01 (+0.05)
- **Graves**: Metal Skin +0.06 (+0.15), Reactive Barrier +0.05 (+0.09), Witchmail +0.04 (+0.22)
- **Apollo**: Reactive Barrier +0.03 (+0.07), Counterspell -0.00 (+0.04), Indomitable -0.01 (+0.11)
- **Deadman Danny**: Indomitable +0.10 (+0.23), Witchmail +0.08 (+0.26), Spirit Resilience +0.07 (+0.21)
- **Rem**: Debuff Reducer +0.12 (+0.19), Unstoppable +0.12 (+0.23), Spellbreaker +0.04 (+0.20)
- **Silver**: Dispel Magic +0.08 (+0.15), Indomitable +0.02 (+0.15), Reactive Barrier +0.02 (+0.06)
- **Celeste**: Spirit Resilience +0.20 (+0.33), Witchmail +0.17 (+0.36), Spellbreaker +0.08 (+0.25)
- **Rat King**: Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.03), Bullet Resilience -0.03 (+0.04)
- **Solomon**: Reactive Barrier -0.01 (+0.03), Return Fire -0.02 (+0.04), Counterspell -0.02 (+0.02)
- **Violet**: Unstoppable +0.07 (+0.18), Witchmail +0.06 (+0.25), Healbane +0.04 (+0.11)
- **Nurse Harrow**: Healbane +0.05 (+0.11), Counterspell +0.02 (+0.07), Witchmail +0.01 (+0.20)
- **Baba**: Unstoppable +0.01 (+0.13), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.185 | +0.058 | +0.144 | Lash +0.41, Deadman Danny +0.18, Paradox +0.14 | 13 heroes |
| Divine Barrier | 6,400 | +0.190 | +0.030 | +0.093 | Lash +0.19, Paradox +0.12, Calico +0.08 | 2 heroes |
| Indomitable | 6,400 | +0.166 | +0.026 | +0.133 | Vyper +0.35, Wraith +0.21, Haze +0.19 | 0 heroes |
| Dispel Magic | 3,200 | +0.078 | +0.024 | +0.054 | Mirage +0.24, Lash +0.15, Paradox +0.15 | 11 heroes |
| Spellbreaker | 6,400 | +0.139 | +0.022 | +0.174 | Lash +0.39, Wraith +0.18, Holliday +0.17 | 0 heroes |
| Healbane | 1,600 | +0.029 | +0.018 | +0.065 | Mo & Krill +0.08, Infernus +0.07, Yamato +0.05 | 25 heroes |
| Witchmail | 6,400 | +0.102 | +0.016 | +0.175 | Lash +0.21, Deadman Danny +0.15, Paradox +0.11 | 1 heroes |
| Bullet Resilience | 3,200 | +0.016 | +0.005 | +0.064 | Venator +0.20, Vindicta +0.10, Haze +0.10 | 1 heroes |
| Debuff Reducer | 1,600 | +0.005 | +0.003 | +0.066 | Holliday +0.18, Grey Talon +0.14, Rem +0.10 | 0 heroes |
| Plated Armor | 6,400 | +0.017 | +0.003 | +0.097 | Holliday +0.19, Haze +0.12, Deadman Danny +0.10 | 0 heroes |
| Reactive Barrier | 1,600 | -0.008 | -0.005 | +0.034 | Deadman Danny +0.12, Paradox +0.12, Vyper +0.06 | 2 heroes |
| Counterspell | 3,200 | -0.027 | -0.008 | +0.034 | Paradox +0.04, Grey Talon +0.02, Drifter +0.02 | 1 heroes |
| Unstoppable | 6,400 | -0.074 | -0.011 | +0.116 | Mo & Krill +0.23, Haze +0.18, Grey Talon +0.15 | 3 heroes |
| Metal Skin | 3,200 | -0.196 | -0.061 | +0.090 | Wraith +0.21, Lash +0.11, Haze +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.188 | -0.117 | +0.061 | Haze +0.11, Paradox +0.08, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.16), Spellbreaker +0.10 (+0.28), Healbane +0.07 (+0.14)
- **Seven**: Witchmail +0.09 (+0.27), Spirit Resilience +0.07 (+0.22), Indomitable +0.05 (+0.18)
- **Vindicta**: Bullet Resilience +0.10 (+0.17), Plated Armor +0.07 (+0.17), Divine Barrier +0.07 (+0.16)
- **Lady Geist**: Spirit Resilience +0.05 (+0.20), Divine Barrier +0.04 (+0.13), Witchmail +0.04 (+0.21)
- **Abrams**: Unstoppable +0.08 (+0.19), Dispel Magic +0.06 (+0.12), Reactive Barrier +0.03 (+0.06)
- **Wraith**: Metal Skin +0.21 (+0.30), Indomitable +0.21 (+0.34), Spellbreaker +0.18 (+0.35)
- **McGinnis**: Spirit Resilience +0.02 (+0.16), Counterspell -0.01 (+0.02), Healbane -0.02 (+0.05)
- **Paradox**: Dispel Magic +0.15 (+0.20), Spirit Resilience +0.14 (+0.29), Reactive Barrier +0.12 (+0.15)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.04 (-0.00)
- **Kelvin**: Healbane +0.02 (+0.08), Counterspell +0.00 (+0.04), Spirit Resilience -0.00 (+0.14)
- **Haze**: Indomitable +0.19 (+0.32), Unstoppable +0.18 (+0.30), Plated Armor +0.12 (+0.22)
- **Holliday**: Plated Armor +0.19 (+0.29), Debuff Reducer +0.18 (+0.25), Spellbreaker +0.17 (+0.35)
- **Bebop**: Healbane +0.03 (+0.09), Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.05)
- **Calico**: Spirit Resilience +0.08 (+0.23), Divine Barrier +0.08 (+0.17), Indomitable +0.06 (+0.19)
- **Grey Talon**: Unstoppable +0.15 (+0.27), Debuff Reducer +0.14 (+0.21), Spellbreaker +0.13 (+0.31)
- **Mo & Krill**: Unstoppable +0.23 (+0.34), Spellbreaker +0.11 (+0.28), Healbane +0.08 (+0.14)
- **Shiv**: Bullet Resilience +0.05 (+0.11), Divine Barrier +0.03 (+0.12), Plated Armor +0.02 (+0.11)
- **Ivy**: Unstoppable +0.01 (+0.13), Indomitable +0.01 (+0.14), Healbane -0.01 (+0.06)
- **Warden**: Debuff Reducer +0.00 (+0.07), Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Yamato**: Healbane +0.05 (+0.11), Debuff Reducer +0.03 (+0.10), Witchmail +0.02 (+0.20)
- **Lash**: Spirit Resilience +0.41 (+0.56), Spellbreaker +0.39 (+0.56), Witchmail +0.21 (+0.39)
- **Viscous**: Spirit Resilience +0.14 (+0.29), Spellbreaker +0.09 (+0.26), Divine Barrier +0.07 (+0.16)
- **Pocket**: Spirit Resilience +0.10 (+0.25), Witchmail +0.04 (+0.22), Counterspell -0.00 (+0.03)
- **Mirage**: Dispel Magic +0.24 (+0.29), Debuff Reducer +0.02 (+0.09), Metal Skin +0.01 (+0.10)
- **Vyper**: Indomitable +0.35 (+0.48), Spellbreaker +0.08 (+0.26), Debuff Reducer +0.08 (+0.15)
- **Sinclair**: Indomitable +0.14 (+0.28), Unstoppable +0.10 (+0.21), Debuff Reducer +0.04 (+0.11)
- **Mina**: Divine Barrier +0.07 (+0.17), Spirit Resilience +0.05 (+0.19), Witchmail +0.04 (+0.21)
- **Drifter**: Counterspell +0.02 (+0.05), Healbane +0.02 (+0.08), Witchmail +0.02 (+0.19)
- **Venator**: Bullet Resilience +0.20 (+0.27), Plated Armor +0.06 (+0.15), Unstoppable +0.04 (+0.16)
- **Victor**: Spellbreaker +0.06 (+0.23), Healbane +0.03 (+0.10), Spirit Resilience +0.02 (+0.17)
- **Paige**: Counterspell +0.01 (+0.05), Divine Barrier +0.00 (+0.10), Return Fire -0.01 (+0.05)
- **The Doorman**: Indomitable +0.11 (+0.24), Witchmail +0.10 (+0.27), Reactive Barrier +0.03 (+0.06)
- **Billy**: Healbane +0.01 (+0.07), Reactive Barrier +0.00 (+0.04), Indomitable -0.01 (+0.12)
- **Graves**: Return Fire +0.04 (+0.10), Reactive Barrier +0.02 (+0.05), Counterspell +0.01 (+0.04)
- **Apollo**: Healbane +0.01 (+0.08), Reactive Barrier +0.01 (+0.04), Counterspell -0.01 (+0.03)
- **Deadman Danny**: Indomitable +0.19 (+0.32), Spirit Resilience +0.18 (+0.32), Witchmail +0.15 (+0.33)
- **Rem**: Debuff Reducer +0.10 (+0.17), Unstoppable +0.08 (+0.20), Spellbreaker +0.02 (+0.19)
- **Silver**: Dispel Magic +0.05 (+0.11), Reactive Barrier +0.05 (+0.08), Bullet Resilience +0.03 (+0.09)
- **Celeste**: Witchmail +0.08 (+0.26), Spirit Resilience +0.06 (+0.20), Healbane +0.04 (+0.10)
- **Rat King**: Return Fire -0.00 (+0.06), Bullet Resilience -0.01 (+0.06), Counterspell -0.01 (+0.03)
- **Solomon**: Counterspell -0.00 (+0.03), Return Fire -0.01 (+0.06), Reactive Barrier -0.02 (+0.02)
- **Violet**: Witchmail +0.10 (+0.28), Divine Barrier +0.05 (+0.15), Unstoppable +0.04 (+0.15)
- **Nurse Harrow**: Divine Barrier +0.07 (+0.16), Healbane +0.04 (+0.10), Witchmail +0.04 (+0.21)
- **Baba**: Healbane -0.01 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (+0.01)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.166 | +0.052 | +0.139 | The Doorman +0.50, Deadman Danny +0.36, Lash +0.31 | 16 heroes |
| Indomitable | 6,400 | +0.191 | +0.030 | +0.167 | Wraith +0.38, Deadman Danny +0.28, Vyper +0.26 | 3 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.059 | Mirage +0.34, Lash +0.21, Paradox +0.18 | 11 heroes |
| Divine Barrier | 6,400 | +0.165 | +0.026 | +0.082 | The Doorman +0.14, Lash +0.12, Viscous +0.12 | 2 heroes |
| Spellbreaker | 6,400 | +0.164 | +0.026 | +0.203 | Deadman Danny +0.31, Holliday +0.28, Grey Talon +0.21 | 0 heroes |
| Healbane | 1,600 | +0.028 | +0.018 | +0.064 | Lady Geist +0.12, Yamato +0.06, The Doorman +0.05 | 21 heroes |
| Witchmail | 6,400 | +0.106 | +0.017 | +0.176 | The Doorman +0.34, Deadman Danny +0.31, Lash +0.20 | 1 heroes |
| Debuff Reducer | 1,600 | +0.008 | +0.005 | +0.090 | Holliday +0.24, Paige +0.21, Grey Talon +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | +0.013 | +0.004 | +0.059 | Vindicta +0.14, Venator +0.10, Haze +0.08 | 1 heroes |
| Plated Armor | 6,400 | +0.015 | +0.002 | +0.102 | Vindicta +0.12, Haze +0.11, Paradox +0.08 | 4 heroes |
| Unstoppable | 6,400 | -0.059 | -0.009 | +0.158 | Paige +0.28, Holliday +0.20, Paradox +0.18 | 5 heroes |
| Counterspell | 3,200 | -0.030 | -0.009 | +0.032 | The Doorman +0.05, Paradox +0.04, Viscous +0.03 | 1 heroes |
| Reactive Barrier | 1,600 | -0.017 | -0.011 | +0.033 | The Doorman +0.15, Deadman Danny +0.07, Paradox +0.06 | 2 heroes |
| Metal Skin | 3,200 | -0.199 | -0.062 | +0.083 | Wraith +0.16, Paradox +0.15, Mirage +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.183 | -0.115 | +0.053 | Vindicta +0.12, Paradox +0.10, The Doorman +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.17 (+0.33), Spellbreaker +0.13 (+0.33), Dispel Magic +0.09 (+0.15)
- **Seven**: Witchmail +0.06 (+0.24), Healbane +0.01 (+0.07), Counterspell +0.00 (+0.04)
- **Vindicta**: Bullet Resilience +0.14 (+0.20), Plated Armor +0.12 (+0.23), Return Fire +0.12 (+0.17)
- **Lady Geist**: Healbane +0.12 (+0.19), Spirit Resilience +0.09 (+0.23), Witchmail +0.06 (+0.24)
- **Abrams**: Dispel Magic +0.02 (+0.08), Counterspell +0.00 (+0.03), Healbane -0.01 (+0.05)
- **Wraith**: Indomitable +0.38 (+0.55), Spellbreaker +0.20 (+0.40), Metal Skin +0.16 (+0.24)
- **McGinnis**: Spirit Resilience +0.03 (+0.17), Dispel Magic +0.01 (+0.07), Counterspell -0.00 (+0.03)
- **Paradox**: Unstoppable +0.18 (+0.34), Dispel Magic +0.18 (+0.24), Indomitable +0.16 (+0.32)
- **Dynamo**: Healbane -0.01 (+0.05), Counterspell -0.02 (+0.01), Reactive Barrier -0.04 (-0.00)
- **Kelvin**: Spirit Resilience +0.04 (+0.18), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Haze**: Unstoppable +0.17 (+0.33), Plated Armor +0.11 (+0.21), Bullet Resilience +0.08 (+0.14)
- **Holliday**: Spellbreaker +0.28 (+0.48), Debuff Reducer +0.24 (+0.33), Unstoppable +0.20 (+0.36)
- **Bebop**: Debuff Reducer +0.15 (+0.24), Unstoppable +0.11 (+0.27), Spellbreaker +0.08 (+0.28)
- **Calico**: Spirit Resilience +0.15 (+0.29), Divine Barrier +0.05 (+0.13), Reactive Barrier +0.04 (+0.07)
- **Grey Talon**: Spirit Resilience +0.26 (+0.40), Spellbreaker +0.21 (+0.42), Witchmail +0.17 (+0.35)
- **Mo & Krill**: Spellbreaker +0.11 (+0.32), Unstoppable +0.08 (+0.24), Debuff Reducer +0.08 (+0.17)
- **Shiv**: Metal Skin +0.07 (+0.15), Bullet Resilience +0.07 (+0.13), Divine Barrier +0.04 (+0.12)
- **Ivy**: Unstoppable +0.18 (+0.33), Indomitable +0.12 (+0.29), Debuff Reducer +0.10 (+0.19)
- **Warden**: Divine Barrier +0.03 (+0.11), Spirit Resilience +0.03 (+0.17), Return Fire +0.02 (+0.07)
- **Yamato**: Healbane +0.06 (+0.12), Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.03)
- **Lash**: Spirit Resilience +0.31 (+0.45), Dispel Magic +0.21 (+0.27), Witchmail +0.20 (+0.37)
- **Viscous**: Spirit Resilience +0.24 (+0.37), Divine Barrier +0.12 (+0.21), Spellbreaker +0.07 (+0.27)
- **Pocket**: Spirit Resilience +0.02 (+0.16), Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.02)
- **Mirage**: Dispel Magic +0.34 (+0.40), Unstoppable +0.16 (+0.32), Metal Skin +0.10 (+0.18)
- **Vyper**: Indomitable +0.26 (+0.42), Plated Armor +0.05 (+0.15), Metal Skin +0.05 (+0.13)
- **Sinclair**: Indomitable +0.22 (+0.39), Debuff Reducer +0.07 (+0.16), Spellbreaker +0.04 (+0.25)
- **Mina**: Divine Barrier +0.03 (+0.11), Counterspell +0.00 (+0.03), Spirit Resilience -0.01 (+0.13)
- **Drifter**: Dispel Magic +0.02 (+0.08), Healbane -0.01 (+0.06), Return Fire -0.01 (+0.05)
- **Venator**: Bullet Resilience +0.10 (+0.16), Metal Skin +0.07 (+0.15), Return Fire +0.02 (+0.07)
- **Victor**: Spellbreaker +0.07 (+0.27), Spirit Resilience +0.05 (+0.19), Healbane +0.05 (+0.11)
- **Paige**: Unstoppable +0.28 (+0.44), Debuff Reducer +0.21 (+0.30), Spellbreaker +0.10 (+0.30)
- **The Doorman**: Spirit Resilience +0.50 (+0.64), Witchmail +0.34 (+0.51), Indomitable +0.25 (+0.42)
- **Billy**: Reactive Barrier +0.03 (+0.06), Healbane -0.02 (+0.04), Counterspell -0.02 (+0.01)
- **Graves**: Witchmail +0.04 (+0.21), Metal Skin +0.01 (+0.10), Healbane +0.01 (+0.08)
- **Apollo**: Reactive Barrier +0.03 (+0.06), Healbane +0.01 (+0.08), Counterspell -0.01 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.36 (+0.50), Witchmail +0.31 (+0.49), Spellbreaker +0.31 (+0.51)
- **Rem**: Divine Barrier +0.11 (+0.19), Spirit Resilience +0.07 (+0.21), Witchmail +0.03 (+0.21)
- **Silver**: Dispel Magic +0.11 (+0.17), Metal Skin +0.07 (+0.15), Bullet Resilience +0.06 (+0.12)
- **Celeste**: Witchmail +0.13 (+0.31), Spirit Resilience +0.07 (+0.21), Plated Armor +0.05 (+0.16)
- **Rat King**: Healbane +0.00 (+0.06), Metal Skin -0.01 (+0.08), Counterspell -0.01 (+0.02)
- **Solomon**: Counterspell -0.00 (+0.03), Reactive Barrier -0.01 (+0.02), Return Fire -0.02 (+0.03)
- **Violet**: Witchmail +0.08 (+0.26), Dispel Magic +0.06 (+0.12), Spirit Resilience +0.05 (+0.19)
- **Nurse Harrow**: Spirit Resilience +0.19 (+0.33), Divine Barrier +0.04 (+0.12), Healbane +0.01 (+0.08)
- **Baba**: Counterspell +0.01 (+0.04), Healbane +0.01 (+0.07), Debuff Reducer +0.00 (+0.09)
