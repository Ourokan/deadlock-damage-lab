# Counter items in the sim (phantom and up)

Built 2026-11-08T09:40:59Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.129 | Lash +0.21, Deadman Danny +0.18, The Doorman +0.18 | 1 heroes |
| Divine Barrier | 6,400 | +0.289 | +0.046 | +0.131 | Lash +0.16, The Doorman +0.16, Abrams +0.12 | 0 heroes |
| Dispel Magic | 3,200 | +0.088 | +0.027 | +0.083 | Mirage +0.38, Lash +0.12, Deadman Danny +0.11 | 4 heroes |
| Indomitable | 6,400 | +0.173 | +0.027 | +0.157 | Vyper +0.32, The Doorman +0.25, Deadman Danny +0.21 | 0 heroes |
| Healbane | 1,600 | +0.040 | +0.025 | +0.087 | Graves +0.13, Yamato +0.09, Nurse Harrow +0.06 | 22 heroes |
| Reactive Barrier | 1,600 | +0.033 | +0.020 | +0.052 | Deadman Danny +0.14, Graves +0.11, The Doorman +0.10 | 2 heroes |
| Witchmail | 6,400 | +0.098 | +0.015 | +0.204 | Deadman Danny +0.21, Lash +0.17, The Doorman +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.022 | +0.014 | +0.079 | Holliday +0.11, Vyper +0.10, Venator +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | +0.044 | +0.014 | +0.106 | Venator +0.27, Lash +0.15, Deadman Danny +0.12 | 0 heroes |
| Spellbreaker | 6,400 | +0.078 | +0.012 | +0.173 | Deadman Danny +0.22, Lash +0.22, The Doorman +0.15 | 0 heroes |
| Plated Armor | 6,400 | +0.007 | +0.001 | +0.138 | Holliday +0.20, Deadman Danny +0.12, Lash +0.11 | 0 heroes |
| Counterspell | 3,200 | -0.006 | -0.002 | +0.075 | Lash +0.11, Graves +0.09, Deadman Danny +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.056 | -0.009 | +0.141 | Deadman Danny +0.15, Lash +0.11, Holliday +0.09 | 0 heroes |
| Metal Skin | 3,200 | -0.184 | -0.057 | +0.111 | Lash +0.18, Wraith +0.14, Paradox +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.187 | -0.117 | +0.085 | Paradox +0.09, Deadman Danny +0.07, Graves +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.07 (+0.15), Spellbreaker +0.06 (+0.23), Unstoppable +0.04 (+0.18)
- **Seven**: Healbane +0.00 (+0.09), Spirit Resilience -0.01 (+0.12), Witchmail -0.01 (+0.19)
- **Vindicta**: Divine Barrier +0.00 (+0.13), Counterspell -0.00 (+0.07), Return Fire -0.00 (+0.08)
- **Lady Geist**: Return Fire +0.02 (+0.11), Healbane -0.00 (+0.09), Divine Barrier -0.01 (+0.12)
- **Abrams**: Indomitable +0.20 (+0.35), Divine Barrier +0.12 (+0.26), Witchmail +0.09 (+0.29)
- **Wraith**: Indomitable +0.16 (+0.31), Metal Skin +0.14 (+0.25), Spellbreaker +0.11 (+0.28)
- **McGinnis**: Counterspell +0.03 (+0.11), Dispel Magic +0.02 (+0.11), Spirit Resilience +0.02 (+0.15)
- **Paradox**: Metal Skin +0.13 (+0.25), Bullet Resilience +0.11 (+0.22), Return Fire +0.09 (+0.18)
- **Dynamo**: Healbane +0.00 (+0.09), Counterspell -0.03 (+0.04), Reactive Barrier -0.04 (+0.01)
- **Kelvin**: Healbane -0.00 (+0.08), Dispel Magic -0.01 (+0.08), Spirit Resilience -0.01 (+0.12)
- **Haze**: Indomitable +0.12 (+0.28), Plated Armor +0.11 (+0.25), Unstoppable +0.08 (+0.22)
- **Holliday**: Plated Armor +0.20 (+0.34), Spellbreaker +0.13 (+0.30), Debuff Reducer +0.11 (+0.19)
- **Bebop**: Healbane +0.01 (+0.10), Counterspell +0.00 (+0.08), Divine Barrier -0.00 (+0.13)
- **Calico**: Spellbreaker +0.09 (+0.26), Divine Barrier +0.08 (+0.21), Spirit Resilience +0.05 (+0.18)
- **Grey Talon**: Unstoppable +0.06 (+0.21), Reactive Barrier +0.05 (+0.11), Debuff Reducer +0.05 (+0.13)
- **Mo & Krill**: Spellbreaker +0.10 (+0.27), Spirit Resilience +0.04 (+0.17), Healbane +0.04 (+0.13)
- **Shiv**: Return Fire -0.00 (+0.08), Healbane -0.01 (+0.08), Divine Barrier -0.02 (+0.12)
- **Ivy**: Indomitable +0.05 (+0.20), Unstoppable +0.03 (+0.17), Debuff Reducer +0.00 (+0.08)
- **Warden**: Return Fire -0.00 (+0.08), Debuff Reducer -0.00 (+0.08), Counterspell -0.02 (+0.06)
- **Yamato**: Healbane +0.09 (+0.18), Spellbreaker +0.05 (+0.22), Return Fire +0.05 (+0.13)
- **Lash**: Spellbreaker +0.22 (+0.39), Spirit Resilience +0.21 (+0.34), Metal Skin +0.18 (+0.29)
- **Viscous**: Divine Barrier -0.01 (+0.12), Healbane -0.03 (+0.05), Return Fire -0.04 (+0.05)
- **Pocket**: Witchmail +0.12 (+0.33), Spirit Resilience +0.10 (+0.23), Spellbreaker +0.07 (+0.24)
- **Mirage**: Dispel Magic +0.38 (+0.46), Spellbreaker +0.07 (+0.24), Spirit Resilience +0.05 (+0.18)
- **Vyper**: Indomitable +0.32 (+0.47), Debuff Reducer +0.10 (+0.18), Spellbreaker +0.09 (+0.27)
- **Sinclair**: Indomitable +0.12 (+0.28), Spellbreaker +0.06 (+0.24), Unstoppable +0.04 (+0.18)
- **Mina**: Return Fire +0.01 (+0.10), Divine Barrier -0.01 (+0.12), Counterspell -0.01 (+0.06)
- **Drifter**: Return Fire -0.02 (+0.06), Counterspell -0.02 (+0.06), Healbane -0.02 (+0.06)
- **Venator**: Bullet Resilience +0.27 (+0.38), Debuff Reducer +0.09 (+0.17), Unstoppable +0.09 (+0.23)
- **Victor**: Spirit Resilience +0.13 (+0.26), Spellbreaker +0.11 (+0.28), Witchmail +0.02 (+0.22)
- **Paige**: Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.06), Reactive Barrier -0.03 (+0.03)
- **The Doorman**: Indomitable +0.25 (+0.40), Spirit Resilience +0.18 (+0.31), Divine Barrier +0.16 (+0.29)
- **Billy**: Spellbreaker +0.06 (+0.23), Healbane +0.06 (+0.15), Spirit Resilience +0.06 (+0.19)
- **Graves**: Healbane +0.13 (+0.21), Reactive Barrier +0.11 (+0.16), Metal Skin +0.11 (+0.22)
- **Apollo**: Reactive Barrier +0.01 (+0.06), Counterspell -0.03 (+0.04), Healbane -0.04 (+0.04)
- **Deadman Danny**: Spellbreaker +0.22 (+0.39), Witchmail +0.21 (+0.41), Indomitable +0.21 (+0.36)
- **Rem**: Reactive Barrier -0.01 (+0.04), Healbane -0.02 (+0.07), Dispel Magic -0.02 (+0.06)
- **Silver**: Dispel Magic +0.08 (+0.16), Indomitable +0.04 (+0.20), Reactive Barrier +0.01 (+0.06)
- **Celeste**: Spirit Resilience +0.12 (+0.24), Witchmail +0.10 (+0.30), Plated Armor +0.04 (+0.18)
- **Rat King**: Return Fire +0.01 (+0.09), Counterspell -0.01 (+0.06), Divine Barrier -0.01 (+0.12)
- **Solomon**: Counterspell -0.02 (+0.05), Reactive Barrier -0.02 (+0.03), Return Fire -0.03 (+0.06)
- **Violet**: Unstoppable +0.06 (+0.20), Return Fire +0.04 (+0.12), Witchmail +0.03 (+0.23)
- **Nurse Harrow**: Healbane +0.06 (+0.15), Reactive Barrier -0.00 (+0.05), Counterspell -0.03 (+0.05)
- **Baba**: Healbane -0.01 (+0.07), Reactive Barrier -0.02 (+0.04), Counterspell -0.02 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.194 | +0.061 | +0.138 | Lash +0.37, Celeste +0.19, Pocket +0.19 | 10 heroes |
| Divine Barrier | 6,400 | +0.208 | +0.033 | +0.099 | Lash +0.23, The Doorman +0.13, Paradox +0.09 | 0 heroes |
| Indomitable | 6,400 | +0.166 | +0.026 | +0.129 | Vyper +0.41, Wraith +0.22, The Doorman +0.18 | 0 heroes |
| Dispel Magic | 3,200 | +0.077 | +0.024 | +0.063 | Mirage +0.31, Abrams +0.10, Silver +0.09 | 9 heroes |
| Spellbreaker | 6,400 | +0.121 | +0.019 | +0.162 | Lash +0.34, Holliday +0.16, Wraith +0.12 | 0 heroes |
| Healbane | 1,600 | +0.029 | +0.018 | +0.067 | Yamato +0.13, Lady Geist +0.08, Infernus +0.05 | 23 heroes |
| Witchmail | 6,400 | +0.114 | +0.018 | +0.182 | Lash +0.24, Celeste +0.17, Wraith +0.12 | 1 heroes |
| Reactive Barrier | 1,600 | +0.018 | +0.012 | +0.038 | The Doorman +0.14, Calico +0.09, Paradox +0.07 | 3 heroes |
| Bullet Resilience | 3,200 | +0.020 | +0.006 | +0.076 | Venator +0.19, Paradox +0.10, Lash +0.09 | 0 heroes |
| Debuff Reducer | 1,600 | +0.005 | +0.003 | +0.069 | Holliday +0.15, Rem +0.12, Vyper +0.10 | 0 heroes |
| Plated Armor | 6,400 | +0.016 | +0.003 | +0.104 | Holliday +0.20, Wraith +0.16, Paradox +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.020 | -0.006 | +0.046 | Paradox +0.05, Yamato +0.05, The Doorman +0.02 | 1 heroes |
| Unstoppable | 6,400 | -0.078 | -0.012 | +0.113 | Holliday +0.13, Abrams +0.12, Rem +0.11 | 0 heroes |
| Metal Skin | 3,200 | -0.199 | -0.062 | +0.088 | Wraith +0.28, Lash +0.15, Paradox +0.09 | 0 heroes |
| Return Fire | 1,600 | -0.195 | -0.122 | +0.062 | Paradox +0.09, The Doorman +0.07, Lash +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.08 (+0.14), Spellbreaker +0.07 (+0.23), Unstoppable +0.06 (+0.17)
- **Seven**: Witchmail +0.06 (+0.25), Healbane +0.02 (+0.08), Spirit Resilience +0.00 (+0.14)
- **Vindicta**: Divine Barrier +0.05 (+0.15), Return Fire +0.05 (+0.11), Witchmail +0.03 (+0.21)
- **Lady Geist**: Spirit Resilience +0.13 (+0.27), Spellbreaker +0.09 (+0.26), Healbane +0.08 (+0.15)
- **Abrams**: Indomitable +0.13 (+0.26), Unstoppable +0.12 (+0.23), Dispel Magic +0.10 (+0.16)
- **Wraith**: Metal Skin +0.28 (+0.37), Indomitable +0.22 (+0.34), Plated Armor +0.16 (+0.26)
- **McGinnis**: Spirit Resilience +0.04 (+0.18), Healbane +0.04 (+0.10), Dispel Magic +0.01 (+0.07)
- **Paradox**: Bullet Resilience +0.10 (+0.18), Metal Skin +0.09 (+0.18), Divine Barrier +0.09 (+0.19)
- **Dynamo**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.03 (+0.17), Healbane -0.00 (+0.07), Witchmail -0.00 (+0.18)
- **Haze**: Indomitable +0.09 (+0.22), Plated Armor +0.08 (+0.18), Bullet Resilience +0.05 (+0.13)
- **Holliday**: Plated Armor +0.20 (+0.31), Spellbreaker +0.16 (+0.32), Debuff Reducer +0.15 (+0.22)
- **Bebop**: Healbane +0.01 (+0.07), Counterspell -0.02 (+0.03), Divine Barrier -0.02 (+0.08)
- **Calico**: Reactive Barrier +0.09 (+0.12), Divine Barrier +0.04 (+0.14), Dispel Magic +0.03 (+0.09)
- **Grey Talon**: Unstoppable +0.09 (+0.20), Debuff Reducer +0.05 (+0.12), Spellbreaker +0.04 (+0.20)
- **Mo & Krill**: Spellbreaker +0.11 (+0.27), Unstoppable +0.08 (+0.19), Dispel Magic +0.06 (+0.12)
- **Shiv**: Bullet Resilience +0.05 (+0.13), Plated Armor +0.02 (+0.13), Divine Barrier +0.02 (+0.12)
- **Ivy**: Unstoppable +0.10 (+0.21), Debuff Reducer +0.05 (+0.11), Indomitable +0.00 (+0.13)
- **Warden**: Return Fire +0.04 (+0.10), Divine Barrier +0.02 (+0.12), Unstoppable +0.01 (+0.12)
- **Yamato**: Healbane +0.13 (+0.19), Debuff Reducer +0.07 (+0.14), Counterspell +0.05 (+0.09)
- **Lash**: Spirit Resilience +0.37 (+0.51), Spellbreaker +0.34 (+0.50), Witchmail +0.24 (+0.42)
- **Viscous**: Divine Barrier +0.03 (+0.12), Counterspell +0.01 (+0.05), Healbane -0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.19 (+0.33), Witchmail +0.08 (+0.26), Spellbreaker +0.06 (+0.22)
- **Mirage**: Dispel Magic +0.31 (+0.37), Spirit Resilience +0.07 (+0.21), Spellbreaker +0.05 (+0.21)
- **Vyper**: Indomitable +0.41 (+0.54), Spellbreaker +0.11 (+0.27), Debuff Reducer +0.10 (+0.17)
- **Sinclair**: Indomitable +0.11 (+0.24), Reactive Barrier +0.00 (+0.04), Spellbreaker +0.00 (+0.16)
- **Mina**: Counterspell +0.01 (+0.05), Divine Barrier +0.01 (+0.10), Return Fire +0.00 (+0.07)
- **Drifter**: Healbane +0.01 (+0.08), Counterspell -0.00 (+0.04), Reactive Barrier -0.02 (+0.02)
- **Venator**: Bullet Resilience +0.19 (+0.26), Debuff Reducer +0.06 (+0.13), Unstoppable +0.04 (+0.16)
- **Victor**: Spirit Resilience +0.08 (+0.22), Spellbreaker +0.07 (+0.23), Healbane +0.00 (+0.07)
- **Paige**: Counterspell +0.00 (+0.05), Return Fire -0.01 (+0.06), Divine Barrier -0.02 (+0.08)
- **The Doorman**: Indomitable +0.18 (+0.30), Reactive Barrier +0.14 (+0.18), Divine Barrier +0.13 (+0.23)
- **Billy**: Healbane +0.00 (+0.07), Counterspell -0.00 (+0.04), Dispel Magic -0.01 (+0.05)
- **Graves**: Metal Skin +0.07 (+0.15), Reactive Barrier +0.05 (+0.09), Witchmail +0.05 (+0.23)
- **Apollo**: Reactive Barrier +0.04 (+0.07), Counterspell -0.00 (+0.04), Indomitable -0.01 (+0.12)
- **Deadman Danny**: Indomitable +0.10 (+0.23), Spirit Resilience +0.08 (+0.22), Witchmail +0.06 (+0.25)
- **Rem**: Debuff Reducer +0.12 (+0.18), Unstoppable +0.11 (+0.22), Spellbreaker +0.03 (+0.20)
- **Silver**: Dispel Magic +0.09 (+0.15), Indomitable +0.03 (+0.16), Reactive Barrier +0.02 (+0.06)
- **Celeste**: Spirit Resilience +0.19 (+0.33), Witchmail +0.17 (+0.35), Spellbreaker +0.08 (+0.25)
- **Rat King**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Solomon**: Reactive Barrier -0.02 (+0.02), Counterspell -0.02 (+0.03), Return Fire -0.02 (+0.04)
- **Violet**: Unstoppable +0.06 (+0.18), Witchmail +0.04 (+0.23), Healbane +0.04 (+0.11)
- **Nurse Harrow**: Healbane +0.05 (+0.12), Divine Barrier +0.01 (+0.11), Witchmail +0.01 (+0.19)
- **Baba**: Unstoppable +0.01 (+0.13), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.184 | +0.058 | +0.143 | Lash +0.41, Deadman Danny +0.17, Wraith +0.16 | 13 heroes |
| Divine Barrier | 6,400 | +0.196 | +0.031 | +0.094 | Lash +0.18, Paradox +0.10, Mina +0.07 | 2 heroes |
| Indomitable | 6,400 | +0.166 | +0.026 | +0.133 | Vyper +0.39, Wraith +0.23, Haze +0.19 | 0 heroes |
| Dispel Magic | 3,200 | +0.078 | +0.024 | +0.054 | Mirage +0.24, Lash +0.15, Paradox +0.13 | 11 heroes |
| Spellbreaker | 6,400 | +0.137 | +0.021 | +0.171 | Lash +0.39, Holliday +0.17, Wraith +0.16 | 0 heroes |
| Healbane | 1,600 | +0.028 | +0.018 | +0.064 | Mo & Krill +0.07, Infernus +0.06, Yamato +0.05 | 25 heroes |
| Witchmail | 6,400 | +0.101 | +0.016 | +0.173 | Lash +0.20, Wraith +0.14, Deadman Danny +0.13 | 1 heroes |
| Bullet Resilience | 3,200 | +0.017 | +0.005 | +0.066 | Venator +0.20, Vindicta +0.10, Haze +0.10 | 1 heroes |
| Debuff Reducer | 1,600 | +0.006 | +0.004 | +0.068 | Holliday +0.17, Grey Talon +0.13, Wraith +0.10 | 0 heroes |
| Plated Armor | 6,400 | +0.017 | +0.003 | +0.099 | Holliday +0.18, Haze +0.12, Wraith +0.12 | 0 heroes |
| Reactive Barrier | 1,600 | -0.007 | -0.004 | +0.037 | Deadman Danny +0.11, Paradox +0.10, Wraith +0.10 | 2 heroes |
| Counterspell | 3,200 | -0.026 | -0.008 | +0.035 | Deadman Danny +0.05, Paradox +0.04, Wraith +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.073 | -0.011 | +0.117 | Mo & Krill +0.24, Haze +0.18, Grey Talon +0.14 | 3 heroes |
| Metal Skin | 3,200 | -0.196 | -0.061 | +0.088 | Wraith +0.21, Lash +0.11, Haze +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.188 | -0.117 | +0.061 | Haze +0.11, Paradox +0.07, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.10 (+0.27), Dispel Magic +0.10 (+0.16), Unstoppable +0.06 (+0.18)
- **Seven**: Witchmail +0.08 (+0.25), Spirit Resilience +0.06 (+0.21), Indomitable +0.04 (+0.17)
- **Vindicta**: Bullet Resilience +0.10 (+0.17), Plated Armor +0.07 (+0.16), Divine Barrier +0.06 (+0.16)
- **Lady Geist**: Healbane +0.03 (+0.09), Spirit Resilience +0.02 (+0.16), Divine Barrier +0.02 (+0.11)
- **Abrams**: Unstoppable +0.07 (+0.19), Dispel Magic +0.07 (+0.12), Reactive Barrier +0.01 (+0.05)
- **Wraith**: Indomitable +0.23 (+0.36), Metal Skin +0.21 (+0.29), Spirit Resilience +0.16 (+0.31)
- **McGinnis**: Spirit Resilience +0.03 (+0.17), Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05)
- **Paradox**: Dispel Magic +0.13 (+0.19), Spirit Resilience +0.13 (+0.27), Reactive Barrier +0.10 (+0.14)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Debuff Reducer -0.04 (+0.03)
- **Kelvin**: Healbane +0.02 (+0.08), Spirit Resilience +0.00 (+0.14), Counterspell -0.00 (+0.03)
- **Haze**: Indomitable +0.19 (+0.32), Unstoppable +0.18 (+0.30), Plated Armor +0.12 (+0.22)
- **Holliday**: Plated Armor +0.18 (+0.28), Debuff Reducer +0.17 (+0.24), Spellbreaker +0.17 (+0.34)
- **Bebop**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Return Fire -0.02 (+0.04)
- **Calico**: Spirit Resilience +0.08 (+0.22), Divine Barrier +0.07 (+0.17), Indomitable +0.06 (+0.20)
- **Grey Talon**: Unstoppable +0.14 (+0.26), Spellbreaker +0.13 (+0.30), Debuff Reducer +0.13 (+0.20)
- **Mo & Krill**: Unstoppable +0.24 (+0.35), Spellbreaker +0.12 (+0.29), Spirit Resilience +0.09 (+0.23)
- **Shiv**: Bullet Resilience +0.04 (+0.11), Divine Barrier +0.02 (+0.12), Plated Armor +0.01 (+0.11)
- **Ivy**: Unstoppable +0.01 (+0.12), Indomitable -0.00 (+0.13), Healbane -0.00 (+0.06)
- **Warden**: Debuff Reducer -0.00 (+0.07), Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Yamato**: Healbane +0.05 (+0.11), Debuff Reducer +0.04 (+0.11), Witchmail +0.02 (+0.19)
- **Lash**: Spirit Resilience +0.41 (+0.55), Spellbreaker +0.39 (+0.56), Witchmail +0.20 (+0.37)
- **Viscous**: Spirit Resilience +0.13 (+0.28), Spellbreaker +0.08 (+0.25), Divine Barrier +0.06 (+0.16)
- **Pocket**: Spirit Resilience +0.09 (+0.24), Witchmail +0.05 (+0.22), Counterspell +0.00 (+0.04)
- **Mirage**: Dispel Magic +0.24 (+0.29), Debuff Reducer +0.01 (+0.08), Metal Skin +0.01 (+0.10)
- **Vyper**: Indomitable +0.39 (+0.52), Spellbreaker +0.09 (+0.26), Debuff Reducer +0.09 (+0.16)
- **Sinclair**: Indomitable +0.13 (+0.26), Unstoppable +0.09 (+0.21), Debuff Reducer +0.03 (+0.10)
- **Mina**: Divine Barrier +0.07 (+0.17), Spirit Resilience +0.05 (+0.20), Witchmail +0.04 (+0.21)
- **Drifter**: Healbane +0.02 (+0.09), Witchmail +0.02 (+0.19), Counterspell +0.02 (+0.05)
- **Venator**: Bullet Resilience +0.20 (+0.26), Plated Armor +0.05 (+0.15), Unstoppable +0.04 (+0.16)
- **Victor**: Spellbreaker +0.06 (+0.23), Healbane +0.03 (+0.09), Spirit Resilience +0.03 (+0.17)
- **Paige**: Counterspell +0.01 (+0.04), Divine Barrier -0.01 (+0.08), Return Fire -0.02 (+0.04)
- **The Doorman**: Indomitable +0.10 (+0.24), Witchmail +0.09 (+0.26), Divine Barrier +0.03 (+0.13)
- **Billy**: Healbane +0.02 (+0.08), Reactive Barrier +0.01 (+0.05), Indomitable -0.00 (+0.13)
- **Graves**: Return Fire +0.03 (+0.09), Reactive Barrier +0.01 (+0.05), Counterspell +0.00 (+0.04)
- **Apollo**: Healbane +0.02 (+0.09), Reactive Barrier +0.01 (+0.04), Counterspell -0.01 (+0.03)
- **Deadman Danny**: Indomitable +0.18 (+0.31), Spirit Resilience +0.17 (+0.31), Witchmail +0.13 (+0.30)
- **Rem**: Debuff Reducer +0.10 (+0.16), Unstoppable +0.08 (+0.19), Spellbreaker +0.02 (+0.19)
- **Silver**: Dispel Magic +0.05 (+0.11), Reactive Barrier +0.05 (+0.08), Divine Barrier +0.03 (+0.12)
- **Celeste**: Witchmail +0.06 (+0.24), Spirit Resilience +0.04 (+0.18), Healbane +0.03 (+0.10)
- **Rat King**: Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.03), Bullet Resilience -0.01 (+0.05)
- **Solomon**: Return Fire +0.01 (+0.07), Counterspell +0.00 (+0.04), Reactive Barrier -0.01 (+0.02)
- **Violet**: Witchmail +0.09 (+0.26), Divine Barrier +0.05 (+0.15), Unstoppable +0.03 (+0.15)
- **Nurse Harrow**: Divine Barrier +0.05 (+0.15), Healbane +0.04 (+0.10), Spirit Resilience +0.03 (+0.17)
- **Baba**: Healbane -0.01 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (+0.01)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.170 | +0.053 | +0.147 | The Doorman +0.48, Deadman Danny +0.34, Lash +0.31 | 16 heroes |
| Indomitable | 6,400 | +0.193 | +0.030 | +0.173 | Wraith +0.45, Deadman Danny +0.27, The Doorman +0.24 | 3 heroes |
| Dispel Magic | 3,200 | +0.085 | +0.026 | +0.060 | Mirage +0.34, Lash +0.22, Paradox +0.18 | 11 heroes |
| Divine Barrier | 6,400 | +0.168 | +0.026 | +0.087 | The Doorman +0.14, Lash +0.11, Viscous +0.11 | 2 heroes |
| Spellbreaker | 6,400 | +0.165 | +0.026 | +0.207 | Deadman Danny +0.32, Grey Talon +0.31, Holliday +0.25 | 0 heroes |
| Healbane | 1,600 | +0.028 | +0.018 | +0.063 | Lady Geist +0.09, Infernus +0.05, Victor +0.05 | 21 heroes |
| Witchmail | 6,400 | +0.108 | +0.017 | +0.179 | Deadman Danny +0.32, The Doorman +0.30, Grey Talon +0.19 | 1 heroes |
| Debuff Reducer | 1,600 | +0.011 | +0.007 | +0.098 | Grey Talon +0.23, Holliday +0.22, Paige +0.18 | 0 heroes |
| Bullet Resilience | 3,200 | +0.015 | +0.004 | +0.063 | Vindicta +0.14, Venator +0.09, Haze +0.07 | 1 heroes |
| Plated Armor | 6,400 | +0.016 | +0.003 | +0.104 | Vindicta +0.12, Wraith +0.11, Haze +0.09 | 4 heroes |
| Unstoppable | 6,400 | -0.055 | -0.009 | +0.167 | Grey Talon +0.25, Paige +0.24, Holliday +0.19 | 5 heroes |
| Reactive Barrier | 1,600 | -0.015 | -0.009 | +0.038 | The Doorman +0.11, Wraith +0.09, Deadman Danny +0.07 | 2 heroes |
| Counterspell | 3,200 | -0.030 | -0.009 | +0.030 | Viscous +0.05, Paradox +0.04, Lash +0.04 | 1 heroes |
| Metal Skin | 3,200 | -0.196 | -0.061 | +0.091 | Wraith +0.26, Paradox +0.14, Mirage +0.07 | 0 heroes |
| Return Fire | 1,600 | -0.183 | -0.115 | +0.054 | Vindicta +0.12, Paradox +0.10, Wraith +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.16 (+0.33), Spellbreaker +0.13 (+0.33), Dispel Magic +0.09 (+0.15)
- **Seven**: Witchmail +0.08 (+0.26), Healbane +0.01 (+0.08), Counterspell +0.01 (+0.04)
- **Vindicta**: Bullet Resilience +0.14 (+0.20), Plated Armor +0.12 (+0.22), Return Fire +0.12 (+0.17)
- **Lady Geist**: Healbane +0.09 (+0.15), Spirit Resilience +0.06 (+0.21), Witchmail +0.04 (+0.22)
- **Abrams**: Dispel Magic +0.02 (+0.08), Spirit Resilience +0.00 (+0.15), Healbane -0.00 (+0.06)
- **Wraith**: Indomitable +0.45 (+0.62), Metal Skin +0.26 (+0.35), Spellbreaker +0.24 (+0.44)
- **McGinnis**: Spirit Resilience +0.05 (+0.20), Dispel Magic +0.01 (+0.07), Counterspell -0.00 (+0.03)
- **Paradox**: Dispel Magic +0.18 (+0.24), Unstoppable +0.17 (+0.34), Indomitable +0.15 (+0.32)
- **Dynamo**: Counterspell -0.02 (+0.01), Healbane -0.02 (+0.04), Reactive Barrier -0.04 (-0.00)
- **Kelvin**: Spirit Resilience +0.02 (+0.16), Healbane -0.01 (+0.06), Counterspell -0.02 (+0.01)
- **Haze**: Unstoppable +0.16 (+0.33), Plated Armor +0.09 (+0.20), Bullet Resilience +0.07 (+0.14)
- **Holliday**: Spellbreaker +0.25 (+0.45), Debuff Reducer +0.22 (+0.32), Unstoppable +0.19 (+0.36)
- **Bebop**: Debuff Reducer +0.14 (+0.23), Unstoppable +0.09 (+0.26), Spellbreaker +0.07 (+0.27)
- **Calico**: Spirit Resilience +0.16 (+0.31), Divine Barrier +0.06 (+0.15), Reactive Barrier +0.05 (+0.09)
- **Grey Talon**: Spellbreaker +0.31 (+0.52), Spirit Resilience +0.30 (+0.44), Unstoppable +0.25 (+0.41)
- **Mo & Krill**: Spellbreaker +0.10 (+0.31), Debuff Reducer +0.07 (+0.16), Unstoppable +0.06 (+0.23)
- **Shiv**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.07 (+0.16), Divine Barrier +0.05 (+0.13)
- **Ivy**: Unstoppable +0.17 (+0.34), Indomitable +0.11 (+0.28), Debuff Reducer +0.09 (+0.19)
- **Warden**: Divine Barrier +0.03 (+0.12), Spirit Resilience +0.03 (+0.17), Return Fire +0.02 (+0.07)
- **Yamato**: Healbane +0.05 (+0.11), Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.04)
- **Lash**: Spirit Resilience +0.31 (+0.46), Dispel Magic +0.22 (+0.28), Witchmail +0.18 (+0.36)
- **Viscous**: Spirit Resilience +0.23 (+0.37), Divine Barrier +0.11 (+0.20), Spellbreaker +0.06 (+0.27)
- **Pocket**: Spirit Resilience +0.05 (+0.19), Return Fire -0.00 (+0.05), Witchmail -0.01 (+0.17)
- **Mirage**: Dispel Magic +0.34 (+0.40), Unstoppable +0.13 (+0.30), Metal Skin +0.07 (+0.16)
- **Vyper**: Indomitable +0.23 (+0.41), Plated Armor +0.03 (+0.14), Reactive Barrier +0.02 (+0.06)
- **Sinclair**: Indomitable +0.20 (+0.37), Debuff Reducer +0.06 (+0.15), Spellbreaker +0.03 (+0.24)
- **Mina**: Divine Barrier +0.03 (+0.11), Counterspell +0.00 (+0.03), Return Fire -0.01 (+0.04)
- **Drifter**: Dispel Magic +0.02 (+0.08), Healbane +0.01 (+0.07), Return Fire -0.00 (+0.05)
- **Venator**: Bullet Resilience +0.09 (+0.16), Metal Skin +0.06 (+0.15), Return Fire +0.02 (+0.07)
- **Victor**: Healbane +0.05 (+0.11), Spellbreaker +0.04 (+0.25), Spirit Resilience +0.03 (+0.17)
- **Paige**: Unstoppable +0.24 (+0.41), Debuff Reducer +0.18 (+0.28), Spellbreaker +0.07 (+0.28)
- **The Doorman**: Spirit Resilience +0.48 (+0.63), Witchmail +0.30 (+0.48), Indomitable +0.24 (+0.41)
- **Billy**: Reactive Barrier +0.04 (+0.08), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.02)
- **Graves**: Witchmail +0.02 (+0.20), Healbane +0.01 (+0.08), Metal Skin +0.01 (+0.10)
- **Apollo**: Reactive Barrier +0.03 (+0.07), Healbane +0.01 (+0.08), Counterspell -0.01 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.34 (+0.49), Spellbreaker +0.32 (+0.53), Witchmail +0.32 (+0.50)
- **Rem**: Divine Barrier +0.09 (+0.18), Spirit Resilience +0.04 (+0.19), Witchmail +0.00 (+0.18)
- **Silver**: Dispel Magic +0.11 (+0.17), Bullet Resilience +0.07 (+0.13), Metal Skin +0.05 (+0.14)
- **Celeste**: Witchmail +0.11 (+0.29), Plated Armor +0.05 (+0.16), Spirit Resilience +0.05 (+0.20)
- **Rat King**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02), Metal Skin -0.02 (+0.07)
- **Solomon**: Counterspell +0.00 (+0.03), Reactive Barrier -0.01 (+0.03), Return Fire -0.02 (+0.03)
- **Violet**: Witchmail +0.07 (+0.25), Dispel Magic +0.05 (+0.11), Spirit Resilience +0.04 (+0.19)
- **Nurse Harrow**: Spirit Resilience +0.20 (+0.35), Divine Barrier +0.04 (+0.12), Healbane +0.02 (+0.08)
- **Baba**: Counterspell +0.01 (+0.04), Healbane +0.00 (+0.07), Debuff Reducer -0.01 (+0.09)
