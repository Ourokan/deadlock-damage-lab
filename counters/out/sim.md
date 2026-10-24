# Counter items in the sim (phantom and up)

Built 2026-10-24T23:40:50Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.194 | +0.061 | +0.117 | Grey Talon +0.18, Mo & Krill +0.12, Sinclair +0.12 | 1 heroes |
| Divine Barrier | 6,400 | +0.359 | +0.057 | +0.110 | Paradox +0.19, Vindicta +0.14, Grey Talon +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.084 | +0.052 | +0.069 | Holliday +0.14, Sinclair +0.10, Dynamo +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.076 | +0.048 | +0.073 | Venator +0.19, Paradox +0.15, Grey Talon +0.10 | 1 heroes |
| Healbane | 1,600 | +0.070 | +0.044 | +0.092 | Haze +0.08, Mo & Krill +0.07, Seven +0.04 | 11 heroes |
| Dispel Magic | 3,200 | +0.116 | +0.036 | +0.085 | Mirage +0.27, Infernus +0.13, Paradox +0.13 | 4 heroes |
| Witchmail | 6,400 | +0.210 | +0.033 | +0.167 | Paradox +0.11, Grey Talon +0.10, Mo & Krill +0.09 | 0 heroes |
| Indomitable | 6,400 | +0.189 | +0.030 | +0.184 | Holliday +0.34, The Doorman +0.31, Sinclair +0.25 | 0 heroes |
| Bullet Resilience | 3,200 | +0.085 | +0.027 | +0.096 | Venator +0.17, Haze +0.13, Paradox +0.12 | 0 heroes |
| Spellbreaker | 6,400 | +0.154 | +0.024 | +0.150 | Holliday +0.22, Mo & Krill +0.21, Sinclair +0.15 | 0 heroes |
| Counterspell | 3,200 | +0.040 | +0.012 | +0.067 | Paradox +0.07, Vyper +0.06, Vindicta +0.05 | 1 heroes |
| Plated Armor | 6,400 | +0.052 | +0.008 | +0.138 | Holliday +0.33, Haze +0.20, Paradox +0.13 | 0 heroes |
| Unstoppable | 6,400 | +0.037 | +0.006 | +0.141 | Rem +0.27, Abrams +0.19, Paradox +0.18 | 0 heroes |
| Return Fire | 1,600 | -0.033 | -0.020 | +0.150 | Venator +0.20, Paradox +0.11, Rat King +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.095 | -0.030 | +0.104 | Paradox +0.21, Venator +0.16, Haze +0.10 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.13 (+0.22), Spirit Resilience +0.05 (+0.17), Healbane +0.03 (+0.13)
- **Seven**: Spirit Resilience +0.10 (+0.21), Metal Skin +0.09 (+0.20), Plated Armor +0.09 (+0.23)
- **Vindicta**: Divine Barrier +0.14 (+0.25), Plated Armor +0.12 (+0.26), Bullet Resilience +0.11 (+0.21)
- **Lady Geist**: Spirit Resilience +0.07 (+0.19), Healbane +0.02 (+0.12), Return Fire +0.02 (+0.17)
- **Abrams**: Unstoppable +0.19 (+0.33), Indomitable +0.08 (+0.27), Reactive Barrier +0.08 (+0.15)
- **Wraith**: Indomitable +0.15 (+0.34), Spellbreaker +0.08 (+0.23), Metal Skin +0.08 (+0.18)
- **McGinnis**: Healbane -0.03 (+0.07), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Paradox**: Indomitable +0.22 (+0.41), Metal Skin +0.21 (+0.31), Divine Barrier +0.19 (+0.30)
- **Dynamo**: Indomitable +0.17 (+0.35), Debuff Reducer +0.06 (+0.13), Unstoppable +0.02 (+0.16)
- **Kelvin**: Spirit Resilience +0.03 (+0.14), Healbane +0.02 (+0.11), Witchmail +0.02 (+0.19)
- **Haze**: Plated Armor +0.20 (+0.34), Bullet Resilience +0.13 (+0.23), Metal Skin +0.10 (+0.20)
- **Holliday**: Indomitable +0.34 (+0.52), Plated Armor +0.33 (+0.46), Spellbreaker +0.22 (+0.37)
- **Bebop**: Healbane +0.01 (+0.10), Counterspell -0.01 (+0.06), Witchmail -0.02 (+0.14)
- **Calico**: Reactive Barrier +0.02 (+0.09), Counterspell +0.02 (+0.09), Divine Barrier +0.00 (+0.11)
- **Grey Talon**: Spirit Resilience +0.18 (+0.29), Spellbreaker +0.14 (+0.29), Indomitable +0.13 (+0.32)
- **Mo & Krill**: Spellbreaker +0.21 (+0.36), Spirit Resilience +0.12 (+0.24), Witchmail +0.09 (+0.26)
- **Shiv**: Healbane +0.02 (+0.12), Divine Barrier +0.01 (+0.12), Metal Skin +0.01 (+0.12)
- **Ivy**: Healbane -0.00 (+0.09), Debuff Reducer -0.03 (+0.04), Unstoppable -0.03 (+0.11)
- **Warden**: Dispel Magic +0.09 (+0.18), Healbane -0.02 (+0.07), Debuff Reducer -0.02 (+0.04)
- **Yamato**: Counterspell -0.05 (+0.01), Healbane -0.05 (+0.04), Debuff Reducer -0.06 (+0.01)
- **Lash**: Spellbreaker +0.11 (+0.26), Spirit Resilience +0.04 (+0.16), Indomitable +0.04 (+0.22)
- **Viscous**: Counterspell -0.01 (+0.06), Healbane -0.01 (+0.08), Reactive Barrier -0.02 (+0.05)
- **Pocket**: Counterspell +0.02 (+0.09), Dispel Magic +0.01 (+0.09), Witchmail +0.00 (+0.17)
- **Mirage**: Dispel Magic +0.27 (+0.36), Spellbreaker +0.04 (+0.19), Healbane +0.02 (+0.11)
- **Vyper**: Indomitable +0.23 (+0.42), Spellbreaker +0.10 (+0.25), Unstoppable +0.07 (+0.21)
- **Sinclair**: Indomitable +0.25 (+0.44), Spellbreaker +0.15 (+0.30), Unstoppable +0.12 (+0.26)
- **Mina**: Dispel Magic +0.07 (+0.16), Reactive Barrier +0.06 (+0.13), Witchmail +0.05 (+0.22)
- **Drifter**: Dispel Magic +0.12 (+0.20), Return Fire +0.08 (+0.23), Divine Barrier +0.07 (+0.18)
- **Venator**: Indomitable +0.23 (+0.42), Return Fire +0.20 (+0.35), Reactive Barrier +0.19 (+0.27)
- **Victor**: Healbane +0.02 (+0.12), Counterspell -0.03 (+0.04), Spirit Resilience -0.03 (+0.09)
- **Paige**: Return Fire +0.00 (+0.15), Debuff Reducer +0.00 (+0.07), Unstoppable -0.00 (+0.14)
- **The Doorman**: Indomitable +0.31 (+0.50), Counterspell -0.01 (+0.06), Reactive Barrier -0.02 (+0.05)
- **Billy**: Divine Barrier +0.02 (+0.14), Healbane +0.01 (+0.11), Bullet Resilience +0.01 (+0.11)
- **Graves**: Return Fire +0.03 (+0.18), Counterspell -0.02 (+0.04), Healbane -0.03 (+0.06)
- **Apollo**: Spirit Resilience -0.01 (+0.10), Divine Barrier -0.04 (+0.07), Counterspell -0.05 (+0.02)
- **Deadman Danny**: Unstoppable +0.10 (+0.24), Indomitable +0.10 (+0.28), Spirit Resilience +0.07 (+0.18)
- **Rem**: Unstoppable +0.27 (+0.42), Indomitable +0.22 (+0.41), Debuff Reducer +0.05 (+0.11)
- **Silver**: Dispel Magic -0.03 (+0.06), Debuff Reducer -0.03 (+0.04), Healbane -0.03 (+0.07)
- **Celeste**: Spirit Resilience +0.07 (+0.19), Witchmail +0.04 (+0.21), Healbane +0.02 (+0.12)
- **Rat King**: Return Fire +0.10 (+0.25), Counterspell +0.00 (+0.07), Bullet Resilience -0.01 (+0.09)
- **Solomon**: Unstoppable +0.04 (+0.18), Debuff Reducer +0.01 (+0.08), Counterspell +0.00 (+0.07)
- **Nurse Harrow**: Dispel Magic +0.03 (+0.11), Counterspell +0.01 (+0.07), Witchmail -0.00 (+0.16)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.124 | Mina +0.26, Grey Talon +0.21, Holliday +0.19 | 10 heroes |
| Divine Barrier | 6,400 | +0.299 | +0.048 | +0.089 | Vindicta +0.20, Mina +0.13, Holliday +0.13 | 1 heroes |
| Debuff Reducer | 1,600 | +0.071 | +0.044 | +0.058 | Holliday +0.17, Vyper +0.10, Abrams +0.07 | 1 heroes |
| Reactive Barrier | 1,600 | +0.060 | +0.037 | +0.058 | Venator +0.17, Mina +0.15, Holliday +0.11 | 2 heroes |
| Dispel Magic | 3,200 | +0.097 | +0.030 | +0.068 | Mina +0.22, Nurse Harrow +0.19, Mirage +0.15 | 7 heroes |
| Indomitable | 6,400 | +0.189 | +0.030 | +0.184 | The Doorman +0.39, Holliday +0.37, Wraith +0.27 | 0 heroes |
| Witchmail | 6,400 | +0.188 | +0.029 | +0.146 | Mina +0.16, Holliday +0.10, Grey Talon +0.09 | 0 heroes |
| Healbane | 1,600 | +0.044 | +0.028 | +0.079 | Haze +0.07, Victor +0.06, Nurse Harrow +0.06 | 16 heroes |
| Spellbreaker | 6,400 | +0.142 | +0.022 | +0.140 | Holliday +0.23, Mo & Krill +0.19, Grey Talon +0.14 | 0 heroes |
| Bullet Resilience | 3,200 | +0.062 | +0.019 | +0.073 | Venator +0.16, Haze +0.14, Holliday +0.09 | 0 heroes |
| Counterspell | 3,200 | +0.019 | +0.006 | +0.046 | Nurse Harrow +0.06, Holliday +0.06, Vyper +0.05 | 1 heroes |
| Unstoppable | 6,400 | +0.031 | +0.005 | +0.136 | Rem +0.38, Abrams +0.30, Paradox +0.16 | 1 heroes |
| Plated Armor | 6,400 | +0.027 | +0.004 | +0.111 | Holliday +0.35, Haze +0.24, Vindicta +0.15 | 0 heroes |
| Metal Skin | 3,200 | -0.104 | -0.032 | +0.094 | Venator +0.21, Haze +0.15, Wraith +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.060 | -0.038 | +0.118 | Venator +0.16, Holliday +0.12, Rat King +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.19), Healbane +0.06 (+0.13), Indomitable +0.04 (+0.22)
- **Seven**: Spirit Resilience +0.11 (+0.23), Witchmail +0.07 (+0.22), Unstoppable +0.03 (+0.17)
- **Vindicta**: Divine Barrier +0.20 (+0.29), Plated Armor +0.15 (+0.26), Bullet Resilience +0.08 (+0.15)
- **Lady Geist**: Return Fire +0.06 (+0.18), Spirit Resilience +0.06 (+0.18), Healbane +0.02 (+0.10)
- **Abrams**: Unstoppable +0.30 (+0.43), Spellbreaker +0.09 (+0.23), Spirit Resilience +0.08 (+0.21)
- **Wraith**: Indomitable +0.27 (+0.45), Metal Skin +0.12 (+0.22), Return Fire +0.06 (+0.17)
- **McGinnis**: Counterspell -0.02 (+0.03), Healbane -0.02 (+0.06), Debuff Reducer -0.04 (+0.02)
- **Paradox**: Unstoppable +0.16 (+0.29), Indomitable +0.14 (+0.33), Spirit Resilience +0.13 (+0.25)
- **Dynamo**: Indomitable +0.21 (+0.39), Debuff Reducer +0.05 (+0.11), Healbane -0.01 (+0.07)
- **Kelvin**: Healbane +0.00 (+0.08), Spirit Resilience -0.00 (+0.12), Counterspell -0.00 (+0.04)
- **Haze**: Plated Armor +0.24 (+0.35), Indomitable +0.16 (+0.35), Metal Skin +0.15 (+0.24)
- **Holliday**: Indomitable +0.37 (+0.56), Plated Armor +0.35 (+0.46), Spellbreaker +0.23 (+0.38)
- **Bebop**: Healbane +0.01 (+0.09), Counterspell -0.01 (+0.03), Debuff Reducer -0.04 (+0.02)
- **Calico**: Reactive Barrier +0.04 (+0.10), Divine Barrier +0.01 (+0.10), Counterspell +0.00 (+0.05)
- **Grey Talon**: Spirit Resilience +0.21 (+0.33), Indomitable +0.16 (+0.34), Spellbreaker +0.14 (+0.28)
- **Mo & Krill**: Spellbreaker +0.19 (+0.33), Unstoppable +0.07 (+0.21), Spirit Resilience +0.05 (+0.17)
- **Shiv**: Metal Skin +0.09 (+0.18), Divine Barrier +0.05 (+0.14), Bullet Resilience +0.04 (+0.12)
- **Ivy**: Healbane +0.02 (+0.10), Debuff Reducer -0.02 (+0.03), Unstoppable -0.02 (+0.11)
- **Warden**: Dispel Magic +0.10 (+0.17), Healbane -0.00 (+0.08), Witchmail -0.01 (+0.14)
- **Yamato**: Healbane -0.02 (+0.06), Counterspell -0.03 (+0.01), Debuff Reducer -0.05 (+0.01)
- **Lash**: Spellbreaker +0.12 (+0.26), Indomitable +0.10 (+0.28), Debuff Reducer +0.05 (+0.11)
- **Viscous**: Counterspell -0.00 (+0.04), Reactive Barrier -0.01 (+0.05), Healbane -0.02 (+0.06)
- **Pocket**: Spirit Resilience +0.02 (+0.15), Return Fire +0.01 (+0.13), Counterspell +0.01 (+0.05)
- **Mirage**: Dispel Magic +0.15 (+0.22), Metal Skin -0.01 (+0.08), Debuff Reducer -0.02 (+0.04)
- **Vyper**: Indomitable +0.25 (+0.43), Debuff Reducer +0.10 (+0.16), Spellbreaker +0.07 (+0.21)
- **Sinclair**: Indomitable +0.20 (+0.38), Spellbreaker +0.10 (+0.24), Debuff Reducer +0.06 (+0.12)
- **Mina**: Spirit Resilience +0.26 (+0.38), Dispel Magic +0.22 (+0.29), Witchmail +0.16 (+0.31)
- **Drifter**: Dispel Magic +0.10 (+0.17), Healbane +0.05 (+0.12), Return Fire +0.04 (+0.16)
- **Venator**: Indomitable +0.21 (+0.39), Metal Skin +0.21 (+0.30), Reactive Barrier +0.17 (+0.22)
- **Victor**: Spellbreaker +0.09 (+0.23), Spirit Resilience +0.09 (+0.21), Healbane +0.06 (+0.14)
- **Paige**: Unstoppable +0.07 (+0.21), Witchmail +0.04 (+0.19), Indomitable +0.04 (+0.23)
- **The Doorman**: Indomitable +0.39 (+0.58), Reactive Barrier +0.01 (+0.07), Witchmail +0.00 (+0.15)
- **Billy**: Witchmail +0.04 (+0.18), Healbane +0.04 (+0.12), Divine Barrier +0.01 (+0.10)
- **Graves**: Return Fire +0.05 (+0.17), Metal Skin -0.01 (+0.09), Counterspell -0.01 (+0.04)
- **Apollo**: Spirit Resilience -0.02 (+0.10), Divine Barrier -0.02 (+0.07), Counterspell -0.03 (+0.01)
- **Deadman Danny**: Spellbreaker +0.03 (+0.17), Spirit Resilience +0.03 (+0.15), Divine Barrier +0.02 (+0.11)
- **Rem**: Unstoppable +0.38 (+0.52), Debuff Reducer +0.07 (+0.13), Spellbreaker -0.01 (+0.13)
- **Silver**: Debuff Reducer +0.01 (+0.07), Dispel Magic +0.01 (+0.07), Bullet Resilience +0.00 (+0.07)
- **Celeste**: Spirit Resilience +0.05 (+0.17), Witchmail +0.03 (+0.17), Dispel Magic +0.02 (+0.08)
- **Rat King**: Return Fire +0.08 (+0.20), Counterspell -0.00 (+0.04), Bullet Resilience -0.01 (+0.06)
- **Solomon**: Unstoppable +0.03 (+0.17), Return Fire +0.03 (+0.15), Debuff Reducer +0.03 (+0.09)
- **Nurse Harrow**: Dispel Magic +0.19 (+0.25), Witchmail +0.07 (+0.21), Counterspell +0.06 (+0.10)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.181 | +0.057 | +0.116 | Paradox +0.37, Mina +0.24, Nurse Harrow +0.16 | 13 heroes |
| Debuff Reducer | 1,600 | +0.068 | +0.042 | +0.055 | Holliday +0.20, Sinclair +0.14, Lash +0.13 | 0 heroes |
| Divine Barrier | 6,400 | +0.219 | +0.034 | +0.068 | Vindicta +0.21, Mina +0.15, Paradox +0.14 | 2 heroes |
| Reactive Barrier | 1,600 | +0.052 | +0.032 | +0.051 | Mina +0.17, Venator +0.11, Paradox +0.10 | 3 heroes |
| Dispel Magic | 3,200 | +0.095 | +0.030 | +0.065 | Nurse Harrow +0.21, Mina +0.21, Paradox +0.17 | 9 heroes |
| Indomitable | 6,400 | +0.183 | +0.029 | +0.176 | Holliday +0.48, The Doorman +0.47, Vyper +0.28 | 0 heroes |
| Witchmail | 6,400 | +0.185 | +0.029 | +0.143 | Paradox +0.21, Mina +0.19, Vindicta +0.11 | 1 heroes |
| Spellbreaker | 6,400 | +0.137 | +0.021 | +0.133 | Holliday +0.27, Paradox +0.25, Mo & Krill +0.22 | 0 heroes |
| Healbane | 1,600 | +0.029 | +0.018 | +0.068 | Infernus +0.07, Lady Geist +0.06, Mo & Krill +0.05 | 15 heroes |
| Bullet Resilience | 3,200 | +0.051 | +0.016 | +0.062 | Vindicta +0.16, Paradox +0.11, Venator +0.09 | 0 heroes |
| Unstoppable | 6,400 | +0.045 | +0.007 | +0.149 | Rem +0.47, Venator +0.21, Haze +0.16 | 3 heroes |
| Plated Armor | 6,400 | +0.019 | +0.003 | +0.106 | Holliday +0.30, Vindicta +0.19, Haze +0.12 | 0 heroes |
| Counterspell | 3,200 | +0.004 | +0.001 | +0.032 | Vindicta +0.06, Paradox +0.05, Billy +0.04 | 1 heroes |
| Metal Skin | 3,200 | -0.104 | -0.033 | +0.093 | Paradox +0.27, Shiv +0.10, Mina +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.071 | -0.044 | +0.106 | Vindicta +0.16, Venator +0.16, Paradox +0.11 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.13 (+0.19), Healbane +0.07 (+0.14), Spirit Resilience +0.06 (+0.18)
- **Seven**: Spirit Resilience +0.08 (+0.20), Metal Skin +0.08 (+0.17), Plated Armor +0.05 (+0.16)
- **Vindicta**: Divine Barrier +0.21 (+0.28), Plated Armor +0.19 (+0.29), Return Fire +0.16 (+0.27)
- **Lady Geist**: Healbane +0.06 (+0.12), Spirit Resilience +0.02 (+0.14), Return Fire -0.00 (+0.10)
- **Abrams**: Unstoppable +0.10 (+0.25), Spirit Resilience +0.00 (+0.12), Reactive Barrier -0.00 (+0.05)
- **Wraith**: Indomitable +0.23 (+0.41), Metal Skin +0.09 (+0.19), Witchmail +0.09 (+0.23)
- **McGinnis**: Healbane +0.01 (+0.08), Counterspell -0.00 (+0.03), Witchmail -0.03 (+0.11)
- **Paradox**: Spirit Resilience +0.37 (+0.48), Metal Skin +0.27 (+0.36), Spellbreaker +0.25 (+0.38)
- **Dynamo**: Indomitable +0.13 (+0.31), Debuff Reducer +0.05 (+0.10), Counterspell -0.02 (+0.02)
- **Kelvin**: Spirit Resilience +0.05 (+0.17), Divine Barrier +0.04 (+0.11), Witchmail +0.03 (+0.18)
- **Haze**: Unstoppable +0.16 (+0.30), Plated Armor +0.12 (+0.23), Bullet Resilience +0.09 (+0.15)
- **Holliday**: Indomitable +0.48 (+0.66), Plated Armor +0.30 (+0.41), Spellbreaker +0.27 (+0.41)
- **Bebop**: Healbane +0.02 (+0.09), Counterspell -0.01 (+0.02), Witchmail -0.03 (+0.11)
- **Calico**: Reactive Barrier +0.01 (+0.06), Counterspell +0.00 (+0.04), Divine Barrier -0.00 (+0.07)
- **Grey Talon**: Spirit Resilience +0.11 (+0.23), Spellbreaker +0.11 (+0.24), Return Fire +0.08 (+0.18)
- **Mo & Krill**: Spellbreaker +0.22 (+0.35), Unstoppable +0.10 (+0.24), Spirit Resilience +0.08 (+0.19)
- **Shiv**: Metal Skin +0.10 (+0.20), Bullet Resilience +0.07 (+0.13), Plated Armor +0.06 (+0.17)
- **Ivy**: Unstoppable +0.01 (+0.16), Healbane -0.00 (+0.06), Debuff Reducer -0.01 (+0.05)
- **Warden**: Dispel Magic +0.05 (+0.12), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.02)
- **Yamato**: Healbane +0.02 (+0.09), Counterspell -0.02 (+0.01), Reactive Barrier -0.05 (+0.00)
- **Lash**: Indomitable +0.19 (+0.37), Spellbreaker +0.15 (+0.28), Debuff Reducer +0.13 (+0.18)
- **Viscous**: Reactive Barrier +0.01 (+0.06), Counterspell +0.00 (+0.04), Divine Barrier +0.00 (+0.07)
- **Pocket**: Counterspell -0.01 (+0.03), Divine Barrier -0.01 (+0.05), Witchmail -0.02 (+0.13)
- **Mirage**: Dispel Magic +0.14 (+0.21), Spellbreaker +0.00 (+0.13), Counterspell -0.01 (+0.02)
- **Vyper**: Indomitable +0.28 (+0.46), Spellbreaker +0.06 (+0.20), Debuff Reducer +0.05 (+0.11)
- **Sinclair**: Indomitable +0.27 (+0.45), Debuff Reducer +0.14 (+0.19), Spellbreaker +0.12 (+0.26)
- **Mina**: Spirit Resilience +0.24 (+0.35), Dispel Magic +0.21 (+0.27), Witchmail +0.19 (+0.33)
- **Drifter**: Dispel Magic +0.12 (+0.18), Healbane +0.05 (+0.11), Return Fire +0.03 (+0.14)
- **Venator**: Unstoppable +0.21 (+0.36), Return Fire +0.16 (+0.26), Indomitable +0.13 (+0.31)
- **Victor**: Spirit Resilience +0.05 (+0.17), Healbane +0.02 (+0.09), Spellbreaker +0.01 (+0.14)
- **Paige**: Unstoppable +0.07 (+0.21), Indomitable +0.04 (+0.22), Return Fire +0.02 (+0.13)
- **The Doorman**: Indomitable +0.47 (+0.65), Counterspell -0.00 (+0.03), Reactive Barrier -0.02 (+0.03)
- **Billy**: Divine Barrier +0.04 (+0.11), Counterspell +0.04 (+0.07), Debuff Reducer +0.03 (+0.08)
- **Graves**: Return Fire +0.02 (+0.13), Counterspell -0.01 (+0.02), Healbane -0.02 (+0.05)
- **Apollo**: Counterspell -0.05 (-0.02), Debuff Reducer -0.06 (-0.01), Divine Barrier -0.06 (+0.00)
- **Deadman Danny**: Witchmail +0.02 (+0.16), Spirit Resilience +0.00 (+0.12), Bullet Resilience -0.00 (+0.06)
- **Rem**: Unstoppable +0.47 (+0.62), Debuff Reducer +0.09 (+0.15), Spellbreaker +0.02 (+0.15)
- **Silver**: Dispel Magic +0.03 (+0.09), Bullet Resilience +0.01 (+0.08), Divine Barrier +0.01 (+0.08)
- **Celeste**: Spirit Resilience +0.04 (+0.15), Dispel Magic +0.02 (+0.08), Healbane +0.01 (+0.08)
- **Rat King**: Return Fire +0.04 (+0.15), Counterspell -0.01 (+0.02), Plated Armor -0.01 (+0.09)
- **Solomon**: Unstoppable +0.09 (+0.24), Spirit Resilience +0.08 (+0.19), Spellbreaker +0.07 (+0.20)
- **Nurse Harrow**: Dispel Magic +0.21 (+0.28), Spirit Resilience +0.16 (+0.27), Witchmail +0.04 (+0.18)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.240 | +0.075 | +0.152 | Paradox +0.27, Nurse Harrow +0.26, Mina +0.26 | 16 heroes |
| Debuff Reducer | 1,600 | +0.082 | +0.051 | +0.071 | Holliday +0.17, Wraith +0.15, Lash +0.14 | 0 heroes |
| Indomitable | 6,400 | +0.253 | +0.040 | +0.249 | The Doorman +0.73, Wraith +0.67, Holliday +0.33 | 1 heroes |
| Reactive Barrier | 1,600 | +0.049 | +0.031 | +0.051 | Venator +0.14, Paradox +0.11, Holliday +0.07 | 2 heroes |
| Spellbreaker | 6,400 | +0.172 | +0.027 | +0.167 | Wraith +0.22, Mo & Krill +0.21, Holliday +0.21 | 0 heroes |
| Dispel Magic | 3,200 | +0.085 | +0.027 | +0.057 | Nurse Harrow +0.28, Drifter +0.17, The Doorman +0.15 | 9 heroes |
| Witchmail | 6,400 | +0.171 | +0.027 | +0.132 | Paradox +0.18, Wraith +0.08, Mina +0.08 | 2 heroes |
| Divine Barrier | 6,400 | +0.162 | +0.025 | +0.073 | The Doorman +0.11, Vindicta +0.11, Drifter +0.09 | 3 heroes |
| Healbane | 1,600 | +0.036 | +0.022 | +0.067 | Victor +0.15, Vindicta +0.12, Infernus +0.07 | 12 heroes |
| Bullet Resilience | 3,200 | +0.059 | +0.018 | +0.071 | Haze +0.15, Venator +0.12, Vindicta +0.09 | 0 heroes |
| Unstoppable | 6,400 | +0.101 | +0.016 | +0.209 | Paige +0.56, Rem +0.39, Paradox +0.27 | 8 heroes |
| Plated Armor | 6,400 | +0.028 | +0.004 | +0.124 | Haze +0.25, Vindicta +0.17, Wraith +0.10 | 1 heroes |
| Counterspell | 3,200 | -0.000 | -0.000 | +0.030 | Vindicta +0.05, Kelvin +0.05, Venator +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.090 | -0.028 | +0.112 | Venator +0.19, Haze +0.16, Wraith +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.078 | -0.049 | +0.098 | Venator +0.15, Rat King +0.08, Sinclair +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.25 (+0.46), Dispel Magic +0.09 (+0.15), Indomitable +0.09 (+0.34)
- **Seven**: Unstoppable +0.18 (+0.39), Spirit Resilience +0.13 (+0.28), Witchmail +0.07 (+0.20)
- **Vindicta**: Plated Armor +0.17 (+0.29), Healbane +0.12 (+0.18), Divine Barrier +0.11 (+0.18)
- **Lady Geist**: Healbane +0.03 (+0.09), Dispel Magic +0.01 (+0.06), Bullet Resilience +0.00 (+0.07)
- **Abrams**: Unstoppable +0.16 (+0.37), Witchmail +0.01 (+0.14), Reactive Barrier +0.01 (+0.06)
- **Wraith**: Indomitable +0.67 (+0.92), Spellbreaker +0.22 (+0.38), Debuff Reducer +0.15 (+0.22)
- **McGinnis**: Witchmail +0.06 (+0.19), Divine Barrier +0.02 (+0.10), Spirit Resilience +0.02 (+0.17)
- **Paradox**: Spirit Resilience +0.27 (+0.42), Unstoppable +0.27 (+0.47), Spellbreaker +0.20 (+0.37)
- **Dynamo**: Indomitable +0.11 (+0.36), Debuff Reducer +0.07 (+0.14), Counterspell -0.01 (+0.02)
- **Kelvin**: Witchmail +0.05 (+0.18), Counterspell +0.05 (+0.08), Healbane +0.03 (+0.10)
- **Haze**: Plated Armor +0.25 (+0.37), Metal Skin +0.16 (+0.27), Bullet Resilience +0.15 (+0.22)
- **Holliday**: Indomitable +0.33 (+0.58), Spellbreaker +0.21 (+0.37), Debuff Reducer +0.17 (+0.25)
- **Bebop**: Debuff Reducer +0.01 (+0.08), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.02)
- **Calico**: Spirit Resilience +0.01 (+0.17), Counterspell -0.01 (+0.02), Divine Barrier -0.01 (+0.07)
- **Grey Talon**: Spellbreaker +0.06 (+0.23), Spirit Resilience +0.06 (+0.21), Witchmail +0.04 (+0.17)
- **Mo & Krill**: Spellbreaker +0.21 (+0.38), Healbane +0.07 (+0.14), Unstoppable +0.07 (+0.28)
- **Shiv**: Bullet Resilience +0.04 (+0.11), Metal Skin +0.04 (+0.15), Divine Barrier +0.02 (+0.10)
- **Ivy**: Healbane -0.01 (+0.06), Debuff Reducer -0.02 (+0.06), Counterspell -0.02 (+0.01)
- **Warden**: Dispel Magic -0.00 (+0.06), Healbane -0.01 (+0.06), Counterspell -0.02 (+0.01)
- **Yamato**: Healbane +0.03 (+0.10), Counterspell -0.02 (+0.01), Reactive Barrier -0.04 (+0.01)
- **Lash**: Indomitable +0.16 (+0.41), Debuff Reducer +0.14 (+0.21), Spellbreaker +0.13 (+0.29)
- **Viscous**: Spirit Resilience +0.05 (+0.20), Reactive Barrier +0.01 (+0.06), Divine Barrier +0.01 (+0.08)
- **Pocket**: Counterspell +0.00 (+0.03), Dispel Magic -0.02 (+0.03), Return Fire -0.03 (+0.07)
- **Mirage**: Dispel Magic +0.12 (+0.17), Metal Skin +0.00 (+0.11), Healbane -0.01 (+0.06)
- **Vyper**: Indomitable +0.17 (+0.42), Plated Armor +0.05 (+0.18), Reactive Barrier +0.02 (+0.07)
- **Sinclair**: Indomitable +0.32 (+0.57), Spellbreaker +0.18 (+0.35), Debuff Reducer +0.13 (+0.20)
- **Mina**: Spirit Resilience +0.26 (+0.41), Witchmail +0.08 (+0.21), Divine Barrier +0.07 (+0.15)
- **Drifter**: Dispel Magic +0.17 (+0.23), Divine Barrier +0.09 (+0.16), Spirit Resilience +0.09 (+0.24)
- **Venator**: Unstoppable +0.19 (+0.40), Metal Skin +0.19 (+0.30), Return Fire +0.15 (+0.25)
- **Victor**: Healbane +0.15 (+0.21), Spellbreaker +0.09 (+0.26), Witchmail +0.07 (+0.20)
- **Paige**: Unstoppable +0.56 (+0.77), Debuff Reducer +0.06 (+0.13), Spellbreaker +0.04 (+0.21)
- **The Doorman**: Indomitable +0.73 (+0.98), Dispel Magic +0.15 (+0.21), Spirit Resilience +0.13 (+0.28)
- **Billy**: Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04), Divine Barrier -0.01 (+0.07)
- **Graves**: Return Fire +0.03 (+0.13), Healbane +0.00 (+0.07), Counterspell -0.02 (+0.01)
- **Apollo**: Healbane -0.01 (+0.06), Counterspell -0.02 (+0.01), Divine Barrier -0.06 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.05 (+0.20), Dispel Magic +0.04 (+0.09), Spellbreaker +0.01 (+0.18)
- **Rem**: Unstoppable +0.39 (+0.59), Debuff Reducer -0.00 (+0.07), Counterspell -0.01 (+0.02)
- **Silver**: Dispel Magic +0.06 (+0.12), Debuff Reducer -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **Celeste**: Spirit Resilience +0.06 (+0.22), Healbane +0.04 (+0.10), Witchmail +0.03 (+0.17)
- **Rat King**: Return Fire +0.08 (+0.17), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.05)
- **Solomon**: Reactive Barrier +0.07 (+0.12), Witchmail +0.07 (+0.20), Spirit Resilience +0.06 (+0.21)
- **Nurse Harrow**: Dispel Magic +0.28 (+0.34), Spirit Resilience +0.26 (+0.41), Spellbreaker +0.09 (+0.26)
