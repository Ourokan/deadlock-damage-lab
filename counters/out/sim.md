# Counter items in the sim (phantom and up)

Built 2026-10-25T03:38:19Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.118 | Grey Talon +0.18, Sinclair +0.13, Mo & Krill +0.12 | 1 heroes |
| Divine Barrier | 6,400 | +0.336 | +0.054 | +0.091 | Paradox +0.23, Vindicta +0.17, Sinclair +0.11 | 0 heroes |
| Debuff Reducer | 1,600 | +0.084 | +0.052 | +0.068 | Holliday +0.15, Sinclair +0.10, Paradox +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | +0.077 | +0.048 | +0.074 | Venator +0.20, Paradox +0.17, Grey Talon +0.10 | 1 heroes |
| Healbane | 1,600 | +0.069 | +0.043 | +0.091 | Haze +0.08, Mo & Krill +0.07, Infernus +0.05 | 11 heroes |
| Dispel Magic | 3,200 | +0.117 | +0.036 | +0.085 | Mirage +0.27, Paradox +0.15, Infernus +0.13 | 4 heroes |
| Witchmail | 6,400 | +0.211 | +0.033 | +0.168 | Paradox +0.12, Grey Talon +0.10, Sinclair +0.10 | 0 heroes |
| Indomitable | 6,400 | +0.191 | +0.030 | +0.186 | Holliday +0.35, The Doorman +0.31, Sinclair +0.26 | 0 heroes |
| Bullet Resilience | 3,200 | +0.086 | +0.027 | +0.097 | Venator +0.17, Paradox +0.14, Haze +0.14 | 0 heroes |
| Spellbreaker | 6,400 | +0.155 | +0.024 | +0.151 | Holliday +0.23, Mo & Krill +0.20, Paradox +0.16 | 0 heroes |
| Counterspell | 3,200 | +0.039 | +0.012 | +0.067 | Paradox +0.07, Vyper +0.06, Vindicta +0.04 | 1 heroes |
| Plated Armor | 6,400 | +0.054 | +0.009 | +0.140 | Holliday +0.34, Haze +0.21, Paradox +0.15 | 0 heroes |
| Unstoppable | 6,400 | +0.033 | +0.005 | +0.138 | Rem +0.27, Abrams +0.20, Paradox +0.19 | 0 heroes |
| Metal Skin | 3,200 | -0.095 | -0.030 | +0.104 | Paradox +0.22, Venator +0.15, Haze +0.09 | 0 heroes |
| Return Fire | 1,600 | -0.086 | -0.054 | +0.086 | Venator +0.11, Grey Talon +0.07, Paradox +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.13 (+0.22), Spirit Resilience +0.06 (+0.18), Healbane +0.05 (+0.14)
- **Seven**: Spirit Resilience +0.11 (+0.23), Plated Armor +0.08 (+0.22), Witchmail +0.08 (+0.25)
- **Vindicta**: Divine Barrier +0.17 (+0.26), Plated Armor +0.12 (+0.26), Bullet Resilience +0.11 (+0.21)
- **Lady Geist**: Spirit Resilience +0.08 (+0.20), Healbane +0.03 (+0.13), Witchmail +0.00 (+0.17)
- **Abrams**: Unstoppable +0.20 (+0.34), Indomitable +0.09 (+0.28), Reactive Barrier +0.08 (+0.15)
- **Wraith**: Indomitable +0.16 (+0.35), Spellbreaker +0.09 (+0.24), Metal Skin +0.08 (+0.19)
- **McGinnis**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.03)
- **Paradox**: Indomitable +0.23 (+0.42), Divine Barrier +0.23 (+0.32), Metal Skin +0.22 (+0.32)
- **Dynamo**: Indomitable +0.17 (+0.36), Debuff Reducer +0.07 (+0.14), Unstoppable +0.02 (+0.15)
- **Kelvin**: Spirit Resilience +0.03 (+0.14), Healbane +0.03 (+0.12), Witchmail +0.02 (+0.19)
- **Haze**: Plated Armor +0.21 (+0.35), Bullet Resilience +0.14 (+0.23), Metal Skin +0.09 (+0.20)
- **Holliday**: Indomitable +0.35 (+0.54), Plated Armor +0.34 (+0.48), Spellbreaker +0.23 (+0.38)
- **Bebop**: Healbane +0.01 (+0.10), Counterspell -0.01 (+0.06), Witchmail -0.02 (+0.14)
- **Calico**: Divine Barrier +0.03 (+0.12), Reactive Barrier +0.02 (+0.10), Counterspell +0.02 (+0.09)
- **Grey Talon**: Spirit Resilience +0.18 (+0.30), Spellbreaker +0.14 (+0.29), Indomitable +0.14 (+0.32)
- **Mo & Krill**: Spellbreaker +0.20 (+0.35), Spirit Resilience +0.12 (+0.24), Witchmail +0.09 (+0.26)
- **Shiv**: Divine Barrier +0.04 (+0.13), Healbane +0.03 (+0.12), Metal Skin +0.02 (+0.12)
- **Ivy**: Healbane +0.00 (+0.09), Unstoppable -0.03 (+0.11), Debuff Reducer -0.03 (+0.04)
- **Warden**: Dispel Magic +0.08 (+0.17), Healbane -0.02 (+0.07), Debuff Reducer -0.02 (+0.05)
- **Yamato**: Counterspell -0.05 (+0.02), Healbane -0.05 (+0.04), Debuff Reducer -0.06 (+0.01)
- **Lash**: Spellbreaker +0.10 (+0.26), Indomitable +0.04 (+0.22), Spirit Resilience +0.03 (+0.15)
- **Viscous**: Counterspell -0.01 (+0.05), Healbane -0.01 (+0.08), Reactive Barrier -0.02 (+0.05)
- **Pocket**: Counterspell -0.00 (+0.06), Return Fire -0.01 (+0.08), Debuff Reducer -0.02 (+0.05)
- **Mirage**: Dispel Magic +0.27 (+0.36), Spellbreaker +0.05 (+0.20), Healbane +0.02 (+0.11)
- **Vyper**: Indomitable +0.24 (+0.42), Spellbreaker +0.11 (+0.26), Unstoppable +0.07 (+0.20)
- **Sinclair**: Indomitable +0.26 (+0.45), Spellbreaker +0.16 (+0.31), Spirit Resilience +0.13 (+0.24)
- **Mina**: Dispel Magic +0.08 (+0.16), Reactive Barrier +0.07 (+0.14), Spirit Resilience +0.06 (+0.18)
- **Drifter**: Dispel Magic +0.12 (+0.20), Metal Skin +0.07 (+0.17), Spellbreaker +0.06 (+0.21)
- **Venator**: Indomitable +0.23 (+0.41), Reactive Barrier +0.20 (+0.27), Bullet Resilience +0.17 (+0.27)
- **Victor**: Healbane +0.03 (+0.12), Counterspell -0.03 (+0.04), Spirit Resilience -0.03 (+0.09)
- **Paige**: Unstoppable +0.03 (+0.16), Return Fire +0.02 (+0.11), Counterspell +0.02 (+0.09)
- **The Doorman**: Indomitable +0.31 (+0.50), Counterspell -0.01 (+0.06), Divine Barrier -0.01 (+0.08)
- **Billy**: Healbane +0.01 (+0.11), Counterspell +0.01 (+0.08), Witchmail +0.01 (+0.18)
- **Graves**: Return Fire +0.03 (+0.11), Counterspell -0.02 (+0.04), Healbane -0.03 (+0.06)
- **Apollo**: Divine Barrier -0.02 (+0.07), Spirit Resilience -0.02 (+0.10), Counterspell -0.06 (+0.01)
- **Deadman Danny**: Unstoppable +0.10 (+0.24), Indomitable +0.09 (+0.28), Reactive Barrier +0.06 (+0.13)
- **Rem**: Unstoppable +0.27 (+0.41), Indomitable +0.22 (+0.40), Debuff Reducer +0.05 (+0.12)
- **Silver**: Dispel Magic -0.02 (+0.07), Debuff Reducer -0.02 (+0.05), Healbane -0.03 (+0.06)
- **Celeste**: Spirit Resilience +0.06 (+0.18), Witchmail +0.03 (+0.20), Dispel Magic +0.01 (+0.09)
- **Rat King**: Return Fire +0.06 (+0.15), Counterspell -0.00 (+0.07), Divine Barrier -0.01 (+0.08)
- **Solomon**: Debuff Reducer +0.01 (+0.08), Return Fire -0.00 (+0.08), Counterspell -0.00 (+0.06)
- **Nurse Harrow**: Dispel Magic +0.03 (+0.11), Divine Barrier +0.01 (+0.10), Counterspell +0.01 (+0.07)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.198 | +0.062 | +0.127 | Mina +0.28, Grey Talon +0.21, Holliday +0.19 | 10 heroes |
| Debuff Reducer | 1,600 | +0.072 | +0.045 | +0.059 | Holliday +0.18, Vyper +0.11, Abrams +0.07 | 1 heroes |
| Divine Barrier | 6,400 | +0.279 | +0.044 | +0.071 | Vindicta +0.21, Mina +0.18, Paradox +0.08 | 1 heroes |
| Reactive Barrier | 1,600 | +0.062 | +0.039 | +0.059 | Mina +0.18, Venator +0.17, Holliday +0.12 | 2 heroes |
| Dispel Magic | 3,200 | +0.100 | +0.031 | +0.071 | Mina +0.24, Nurse Harrow +0.19, Mirage +0.15 | 7 heroes |
| Indomitable | 6,400 | +0.194 | +0.031 | +0.189 | The Doorman +0.39, Holliday +0.38, Wraith +0.28 | 0 heroes |
| Healbane | 1,600 | +0.049 | +0.030 | +0.083 | Haze +0.07, Victor +0.06, Nurse Harrow +0.06 | 16 heroes |
| Witchmail | 6,400 | +0.190 | +0.030 | +0.148 | Mina +0.18, Holliday +0.10, Grey Talon +0.09 | 0 heroes |
| Spellbreaker | 6,400 | +0.144 | +0.022 | +0.141 | Holliday +0.24, Mo & Krill +0.20, Mina +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | +0.062 | +0.019 | +0.073 | Haze +0.14, Venator +0.12, Holliday +0.09 | 0 heroes |
| Counterspell | 3,200 | +0.020 | +0.006 | +0.047 | Nurse Harrow +0.06, Holliday +0.06, Vyper +0.05 | 1 heroes |
| Unstoppable | 6,400 | +0.030 | +0.005 | +0.135 | Rem +0.39, Abrams +0.29, Holliday +0.14 | 1 heroes |
| Plated Armor | 6,400 | +0.029 | +0.004 | +0.113 | Holliday +0.37, Haze +0.25, Vindicta +0.14 | 0 heroes |
| Metal Skin | 3,200 | -0.101 | -0.032 | +0.097 | Venator +0.21, Haze +0.15, Wraith +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.106 | -0.066 | +0.064 | Venator +0.09, Holliday +0.09, Rat King +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.19), Healbane +0.06 (+0.14), Indomitable +0.04 (+0.23)
- **Seven**: Spirit Resilience +0.11 (+0.24), Witchmail +0.06 (+0.21), Unstoppable +0.06 (+0.20)
- **Vindicta**: Divine Barrier +0.21 (+0.28), Plated Armor +0.14 (+0.26), Bullet Resilience +0.07 (+0.15)
- **Lady Geist**: Spirit Resilience +0.06 (+0.18), Return Fire +0.04 (+0.10), Healbane +0.02 (+0.11)
- **Abrams**: Unstoppable +0.29 (+0.43), Spellbreaker +0.09 (+0.23), Spirit Resilience +0.08 (+0.21)
- **Wraith**: Indomitable +0.28 (+0.47), Metal Skin +0.12 (+0.22), Spellbreaker +0.06 (+0.20)
- **McGinnis**: Counterspell -0.02 (+0.03), Healbane -0.02 (+0.06), Debuff Reducer -0.04 (+0.02)
- **Paradox**: Unstoppable +0.13 (+0.27), Spirit Resilience +0.13 (+0.25), Indomitable +0.12 (+0.31)
- **Dynamo**: Indomitable +0.21 (+0.40), Debuff Reducer +0.05 (+0.11), Healbane -0.01 (+0.07)
- **Kelvin**: Healbane -0.00 (+0.08), Counterspell -0.01 (+0.04), Spirit Resilience -0.01 (+0.12)
- **Haze**: Plated Armor +0.25 (+0.36), Indomitable +0.19 (+0.37), Metal Skin +0.15 (+0.25)
- **Holliday**: Indomitable +0.38 (+0.57), Plated Armor +0.37 (+0.48), Spellbreaker +0.24 (+0.38)
- **Bebop**: Healbane +0.01 (+0.09), Counterspell -0.01 (+0.03), Return Fire -0.03 (+0.03)
- **Calico**: Reactive Barrier +0.04 (+0.10), Divine Barrier +0.03 (+0.10), Spirit Resilience +0.00 (+0.13)
- **Grey Talon**: Spirit Resilience +0.21 (+0.34), Indomitable +0.16 (+0.35), Spellbreaker +0.14 (+0.28)
- **Mo & Krill**: Spellbreaker +0.20 (+0.34), Unstoppable +0.08 (+0.21), Spirit Resilience +0.05 (+0.18)
- **Shiv**: Metal Skin +0.09 (+0.19), Divine Barrier +0.07 (+0.14), Bullet Resilience +0.04 (+0.11)
- **Ivy**: Healbane +0.02 (+0.10), Unstoppable -0.02 (+0.12), Debuff Reducer -0.03 (+0.03)
- **Warden**: Dispel Magic +0.11 (+0.18), Healbane +0.01 (+0.09), Witchmail +0.01 (+0.15)
- **Yamato**: Healbane -0.02 (+0.06), Counterspell -0.04 (+0.01), Debuff Reducer -0.05 (+0.01)
- **Lash**: Spellbreaker +0.13 (+0.28), Indomitable +0.10 (+0.29), Debuff Reducer +0.06 (+0.12)
- **Viscous**: Counterspell +0.00 (+0.05), Reactive Barrier -0.01 (+0.05), Divine Barrier -0.01 (+0.06)
- **Pocket**: Return Fire +0.02 (+0.08), Spirit Resilience +0.02 (+0.15), Counterspell -0.00 (+0.04)
- **Mirage**: Dispel Magic +0.15 (+0.22), Metal Skin -0.02 (+0.08), Debuff Reducer -0.02 (+0.04)
- **Vyper**: Indomitable +0.25 (+0.44), Debuff Reducer +0.11 (+0.17), Spellbreaker +0.08 (+0.22)
- **Sinclair**: Indomitable +0.20 (+0.39), Spellbreaker +0.11 (+0.25), Debuff Reducer +0.07 (+0.13)
- **Mina**: Spirit Resilience +0.28 (+0.41), Dispel Magic +0.24 (+0.31), Witchmail +0.18 (+0.33)
- **Drifter**: Dispel Magic +0.10 (+0.17), Healbane +0.05 (+0.13), Spellbreaker +0.03 (+0.18)
- **Venator**: Metal Skin +0.21 (+0.30), Indomitable +0.21 (+0.39), Reactive Barrier +0.17 (+0.22)
- **Victor**: Spellbreaker +0.10 (+0.24), Spirit Resilience +0.09 (+0.22), Healbane +0.06 (+0.15)
- **Paige**: Unstoppable +0.07 (+0.21), Indomitable +0.05 (+0.24), Witchmail +0.05 (+0.20)
- **The Doorman**: Indomitable +0.39 (+0.58), Divine Barrier +0.01 (+0.08), Reactive Barrier +0.01 (+0.07)
- **Billy**: Healbane +0.05 (+0.13), Counterspell +0.02 (+0.07), Witchmail -0.00 (+0.15)
- **Graves**: Return Fire +0.04 (+0.10), Metal Skin -0.00 (+0.09), Counterspell -0.01 (+0.04)
- **Apollo**: Divine Barrier +0.01 (+0.08), Spirit Resilience -0.00 (+0.12), Healbane -0.03 (+0.06)
- **Deadman Danny**: Unstoppable +0.03 (+0.17), Spellbreaker +0.03 (+0.17), Spirit Resilience +0.02 (+0.15)
- **Rem**: Unstoppable +0.39 (+0.52), Debuff Reducer +0.07 (+0.13), Spellbreaker -0.01 (+0.13)
- **Silver**: Divine Barrier +0.01 (+0.08), Debuff Reducer +0.01 (+0.07), Dispel Magic +0.01 (+0.08)
- **Celeste**: Spirit Resilience +0.05 (+0.17), Witchmail +0.03 (+0.17), Dispel Magic +0.01 (+0.08)
- **Rat King**: Return Fire +0.05 (+0.12), Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.06)
- **Solomon**: Debuff Reducer +0.03 (+0.09), Reactive Barrier +0.02 (+0.08), Counterspell +0.02 (+0.06)
- **Nurse Harrow**: Dispel Magic +0.19 (+0.26), Witchmail +0.07 (+0.22), Healbane +0.06 (+0.15)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.183 | +0.057 | +0.117 | Paradox +0.36, Mina +0.23, Nurse Harrow +0.15 | 13 heroes |
| Debuff Reducer | 1,600 | +0.068 | +0.043 | +0.056 | Holliday +0.20, Sinclair +0.15, Lash +0.13 | 0 heroes |
| Reactive Barrier | 1,600 | +0.054 | +0.034 | +0.053 | Mina +0.17, Venator +0.12, Paradox +0.11 | 3 heroes |
| Divine Barrier | 6,400 | +0.204 | +0.032 | +0.055 | Vindicta +0.23, Mina +0.16, Paradox +0.16 | 2 heroes |
| Dispel Magic | 3,200 | +0.096 | +0.030 | +0.066 | Nurse Harrow +0.21, Mina +0.21, Paradox +0.18 | 9 heroes |
| Indomitable | 6,400 | +0.186 | +0.030 | +0.179 | Holliday +0.48, The Doorman +0.46, Sinclair +0.29 | 0 heroes |
| Witchmail | 6,400 | +0.188 | +0.029 | +0.145 | Paradox +0.22, Mina +0.19, Vindicta +0.12 | 1 heroes |
| Spellbreaker | 6,400 | +0.140 | +0.022 | +0.136 | Holliday +0.27, Paradox +0.25, Mo & Krill +0.22 | 0 heroes |
| Healbane | 1,600 | +0.031 | +0.020 | +0.070 | Infernus +0.07, Lady Geist +0.05, Mo & Krill +0.05 | 15 heroes |
| Bullet Resilience | 3,200 | +0.052 | +0.016 | +0.063 | Vindicta +0.16, Paradox +0.11, Venator +0.09 | 0 heroes |
| Unstoppable | 6,400 | +0.039 | +0.006 | +0.142 | Rem +0.47, Venator +0.21, Haze +0.16 | 3 heroes |
| Plated Armor | 6,400 | +0.020 | +0.003 | +0.107 | Holliday +0.30, Vindicta +0.20, Haze +0.13 | 0 heroes |
| Counterspell | 3,200 | +0.006 | +0.002 | +0.034 | Vindicta +0.05, Paradox +0.04, Billy +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.105 | -0.033 | +0.092 | Paradox +0.27, Shiv +0.10, Mina +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.114 | -0.071 | +0.054 | Vindicta +0.11, Venator +0.09, Paradox +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.19), Healbane +0.07 (+0.14), Spirit Resilience +0.06 (+0.18)
- **Seven**: Spirit Resilience +0.06 (+0.17), Witchmail +0.06 (+0.20), Healbane +0.04 (+0.11)
- **Vindicta**: Divine Barrier +0.23 (+0.29), Plated Armor +0.20 (+0.30), Bullet Resilience +0.16 (+0.22)
- **Lady Geist**: Healbane +0.05 (+0.12), Spirit Resilience +0.02 (+0.14), Bullet Resilience -0.01 (+0.06)
- **Abrams**: Unstoppable +0.10 (+0.24), Divine Barrier +0.01 (+0.06), Spirit Resilience +0.00 (+0.12)
- **Wraith**: Indomitable +0.24 (+0.42), Metal Skin +0.10 (+0.19), Witchmail +0.09 (+0.23)
- **McGinnis**: Healbane +0.01 (+0.08), Counterspell -0.00 (+0.03), Witchmail -0.04 (+0.11)
- **Paradox**: Spirit Resilience +0.36 (+0.47), Metal Skin +0.27 (+0.37), Spellbreaker +0.25 (+0.39)
- **Dynamo**: Indomitable +0.12 (+0.30), Debuff Reducer +0.04 (+0.10), Counterspell -0.02 (+0.02)
- **Kelvin**: Spirit Resilience +0.07 (+0.18), Counterspell +0.03 (+0.07), Witchmail +0.03 (+0.18)
- **Haze**: Unstoppable +0.16 (+0.30), Plated Armor +0.13 (+0.23), Bullet Resilience +0.09 (+0.15)
- **Holliday**: Indomitable +0.48 (+0.66), Plated Armor +0.30 (+0.41), Spellbreaker +0.27 (+0.41)
- **Bebop**: Healbane +0.02 (+0.09), Counterspell -0.01 (+0.02), Return Fire -0.03 (+0.02)
- **Calico**: Divine Barrier +0.01 (+0.07), Reactive Barrier +0.01 (+0.06), Counterspell +0.00 (+0.04)
- **Grey Talon**: Spirit Resilience +0.12 (+0.24), Spellbreaker +0.12 (+0.25), Indomitable +0.07 (+0.25)
- **Mo & Krill**: Spellbreaker +0.22 (+0.36), Unstoppable +0.09 (+0.23), Spirit Resilience +0.08 (+0.20)
- **Shiv**: Metal Skin +0.10 (+0.20), Divine Barrier +0.06 (+0.12), Bullet Resilience +0.06 (+0.12)
- **Ivy**: Unstoppable +0.01 (+0.15), Healbane -0.01 (+0.06), Debuff Reducer -0.01 (+0.05)
- **Warden**: Dispel Magic +0.06 (+0.13), Healbane +0.01 (+0.08), Counterspell -0.02 (+0.02)
- **Yamato**: Healbane +0.02 (+0.09), Counterspell -0.02 (+0.01), Reactive Barrier -0.05 (+0.01)
- **Lash**: Indomitable +0.19 (+0.37), Spellbreaker +0.15 (+0.29), Debuff Reducer +0.13 (+0.18)
- **Viscous**: Divine Barrier +0.01 (+0.07), Reactive Barrier +0.00 (+0.06), Counterspell +0.00 (+0.04)
- **Pocket**: Counterspell -0.00 (+0.03), Return Fire -0.02 (+0.04), Spirit Resilience -0.02 (+0.10)
- **Mirage**: Dispel Magic +0.14 (+0.21), Spellbreaker -0.00 (+0.13), Counterspell -0.01 (+0.02)
- **Vyper**: Indomitable +0.29 (+0.47), Spellbreaker +0.07 (+0.20), Debuff Reducer +0.05 (+0.11)
- **Sinclair**: Indomitable +0.29 (+0.47), Debuff Reducer +0.15 (+0.21), Spellbreaker +0.14 (+0.28)
- **Mina**: Spirit Resilience +0.23 (+0.35), Dispel Magic +0.21 (+0.27), Witchmail +0.19 (+0.33)
- **Drifter**: Dispel Magic +0.11 (+0.18), Healbane +0.04 (+0.11), Return Fire +0.02 (+0.07)
- **Venator**: Unstoppable +0.21 (+0.36), Indomitable +0.13 (+0.31), Reactive Barrier +0.12 (+0.17)
- **Victor**: Spirit Resilience +0.05 (+0.17), Healbane +0.03 (+0.10), Spellbreaker +0.01 (+0.15)
- **Paige**: Unstoppable +0.03 (+0.18), Indomitable +0.03 (+0.20), Return Fire +0.02 (+0.08)
- **The Doorman**: Indomitable +0.46 (+0.64), Counterspell -0.00 (+0.03), Return Fire -0.01 (+0.04)
- **Billy**: Counterspell +0.03 (+0.07), Reactive Barrier +0.02 (+0.08), Debuff Reducer +0.01 (+0.07)
- **Graves**: Return Fire +0.02 (+0.08), Counterspell -0.02 (+0.02), Metal Skin -0.02 (+0.08)
- **Apollo**: Counterspell -0.02 (+0.01), Healbane -0.02 (+0.05), Divine Barrier -0.03 (+0.03)
- **Deadman Danny**: Witchmail +0.02 (+0.16), Spirit Resilience +0.01 (+0.12), Bullet Resilience -0.00 (+0.06)
- **Rem**: Unstoppable +0.47 (+0.61), Debuff Reducer +0.09 (+0.14), Spellbreaker +0.01 (+0.15)
- **Silver**: Dispel Magic +0.03 (+0.09), Divine Barrier +0.02 (+0.08), Bullet Resilience +0.01 (+0.07)
- **Celeste**: Spirit Resilience +0.04 (+0.15), Dispel Magic +0.02 (+0.09), Healbane +0.01 (+0.08)
- **Rat King**: Return Fire +0.02 (+0.08), Counterspell -0.01 (+0.02), Plated Armor -0.02 (+0.09)
- **Solomon**: Spirit Resilience +0.08 (+0.20), Spellbreaker +0.08 (+0.21), Witchmail +0.06 (+0.21)
- **Nurse Harrow**: Dispel Magic +0.21 (+0.27), Spirit Resilience +0.15 (+0.27), Witchmail +0.04 (+0.18)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.247 | +0.077 | +0.160 | Paradox +0.27, Mina +0.26, Nurse Harrow +0.25 | 16 heroes |
| Debuff Reducer | 1,600 | +0.088 | +0.055 | +0.077 | Wraith +0.18, Holliday +0.17, Lash +0.15 | 0 heroes |
| Indomitable | 6,400 | +0.260 | +0.041 | +0.256 | The Doorman +0.72, Wraith +0.71, Holliday +0.34 | 1 heroes |
| Reactive Barrier | 1,600 | +0.053 | +0.033 | +0.055 | Venator +0.14, Wraith +0.08, Solomon +0.07 | 2 heroes |
| Spellbreaker | 6,400 | +0.181 | +0.028 | +0.176 | Wraith +0.24, Paradox +0.21, Mo & Krill +0.21 | 0 heroes |
| Witchmail | 6,400 | +0.179 | +0.028 | +0.140 | Paradox +0.19, Wraith +0.11, Victor +0.11 | 2 heroes |
| Dispel Magic | 3,200 | +0.089 | +0.028 | +0.060 | Nurse Harrow +0.27, Drifter +0.17, Vindicta +0.16 | 9 heroes |
| Healbane | 1,600 | +0.038 | +0.024 | +0.070 | Victor +0.20, Vindicta +0.09, Infernus +0.07 | 12 heroes |
| Divine Barrier | 6,400 | +0.149 | +0.023 | +0.060 | Vindicta +0.14, The Doorman +0.12, Paradox +0.12 | 3 heroes |
| Bullet Resilience | 3,200 | +0.065 | +0.020 | +0.076 | Haze +0.16, Venator +0.11, Vindicta +0.11 | 0 heroes |
| Unstoppable | 6,400 | +0.104 | +0.016 | +0.212 | Paige +0.58, Rem +0.38, Paradox +0.29 | 8 heroes |
| Plated Armor | 6,400 | +0.032 | +0.005 | +0.128 | Vindicta +0.26, Haze +0.26, Wraith +0.14 | 1 heroes |
| Counterspell | 3,200 | -0.001 | -0.000 | +0.029 | Kelvin +0.05, Venator +0.03, Shiv +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.089 | -0.028 | +0.112 | Wraith +0.19, Haze +0.17, Venator +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.122 | -0.076 | +0.046 | Venator +0.10, Sinclair +0.05, Rat King +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.27 (+0.48), Dispel Magic +0.10 (+0.16), Indomitable +0.09 (+0.35)
- **Seven**: Unstoppable +0.12 (+0.33), Spirit Resilience +0.09 (+0.25), Witchmail +0.07 (+0.20)
- **Vindicta**: Plated Armor +0.26 (+0.39), Dispel Magic +0.16 (+0.22), Divine Barrier +0.14 (+0.20)
- **Lady Geist**: Healbane +0.03 (+0.10), Bullet Resilience -0.01 (+0.06), Counterspell -0.02 (+0.01)
- **Abrams**: Unstoppable +0.15 (+0.37), Divine Barrier +0.01 (+0.07), Witchmail +0.01 (+0.15)
- **Wraith**: Indomitable +0.71 (+0.96), Spellbreaker +0.24 (+0.42), Spirit Resilience +0.20 (+0.36)
- **McGinnis**: Witchmail +0.06 (+0.20), Spirit Resilience +0.02 (+0.18), Healbane +0.01 (+0.08)
- **Paradox**: Unstoppable +0.29 (+0.50), Spirit Resilience +0.27 (+0.43), Spellbreaker +0.21 (+0.39)
- **Dynamo**: Indomitable +0.13 (+0.38), Debuff Reducer +0.06 (+0.14), Counterspell -0.01 (+0.02)
- **Kelvin**: Counterspell +0.05 (+0.08), Witchmail +0.05 (+0.19), Spirit Resilience +0.03 (+0.19)
- **Haze**: Plated Armor +0.26 (+0.38), Metal Skin +0.17 (+0.28), Bullet Resilience +0.16 (+0.23)
- **Holliday**: Indomitable +0.34 (+0.59), Spellbreaker +0.20 (+0.38), Debuff Reducer +0.17 (+0.25)
- **Bebop**: Debuff Reducer +0.01 (+0.08), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.02)
- **Calico**: Divine Barrier +0.00 (+0.06), Spirit Resilience -0.00 (+0.16), Counterspell -0.00 (+0.03)
- **Grey Talon**: Spellbreaker +0.04 (+0.22), Spirit Resilience +0.03 (+0.19), Witchmail +0.02 (+0.16)
- **Mo & Krill**: Spellbreaker +0.21 (+0.38), Unstoppable +0.07 (+0.28), Healbane +0.06 (+0.13)
- **Shiv**: Metal Skin +0.04 (+0.16), Bullet Resilience +0.04 (+0.12), Divine Barrier +0.04 (+0.10)
- **Ivy**: Healbane -0.02 (+0.05), Counterspell -0.02 (+0.01), Unstoppable -0.02 (+0.19)
- **Warden**: Dispel Magic -0.00 (+0.06), Healbane -0.01 (+0.06), Counterspell -0.02 (+0.01)
- **Yamato**: Healbane +0.03 (+0.10), Counterspell -0.02 (+0.01), Return Fire -0.04 (+0.01)
- **Lash**: Indomitable +0.17 (+0.43), Debuff Reducer +0.15 (+0.23), Spellbreaker +0.14 (+0.31)
- **Viscous**: Spirit Resilience +0.05 (+0.20), Divine Barrier +0.02 (+0.08), Reactive Barrier +0.02 (+0.07)
- **Pocket**: Return Fire +0.00 (+0.05), Counterspell -0.00 (+0.03), Dispel Magic -0.04 (+0.02)
- **Mirage**: Dispel Magic +0.11 (+0.17), Metal Skin +0.00 (+0.11), Counterspell -0.01 (+0.02)
- **Vyper**: Indomitable +0.18 (+0.44), Plated Armor +0.06 (+0.19), Metal Skin +0.03 (+0.14)
- **Sinclair**: Indomitable +0.33 (+0.59), Spellbreaker +0.19 (+0.37), Debuff Reducer +0.14 (+0.22)
- **Mina**: Spirit Resilience +0.26 (+0.42), Divine Barrier +0.10 (+0.16), Witchmail +0.09 (+0.23)
- **Drifter**: Dispel Magic +0.17 (+0.23), Spirit Resilience +0.08 (+0.24), Metal Skin +0.07 (+0.18)
- **Venator**: Unstoppable +0.20 (+0.41), Metal Skin +0.15 (+0.26), Reactive Barrier +0.14 (+0.19)
- **Victor**: Healbane +0.20 (+0.27), Spellbreaker +0.13 (+0.31), Witchmail +0.11 (+0.25)
- **Paige**: Unstoppable +0.58 (+0.79), Debuff Reducer +0.06 (+0.14), Spellbreaker +0.04 (+0.22)
- **The Doorman**: Indomitable +0.72 (+0.98), Dispel Magic +0.15 (+0.21), Divine Barrier +0.12 (+0.18)
- **Billy**: Reactive Barrier +0.02 (+0.07), Healbane +0.01 (+0.08), Counterspell +0.00 (+0.03)
- **Graves**: Return Fire +0.02 (+0.06), Healbane -0.01 (+0.06), Counterspell -0.02 (+0.01)
- **Apollo**: Counterspell -0.01 (+0.02), Healbane -0.01 (+0.06), Spirit Resilience -0.04 (+0.12)
- **Deadman Danny**: Spirit Resilience +0.04 (+0.20), Dispel Magic +0.03 (+0.09), Reactive Barrier +0.01 (+0.06)
- **Rem**: Unstoppable +0.38 (+0.60), Debuff Reducer -0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Silver**: Dispel Magic +0.05 (+0.11), Divine Barrier -0.02 (+0.04), Reactive Barrier -0.02 (+0.04)
- **Celeste**: Spirit Resilience +0.06 (+0.22), Healbane +0.04 (+0.11), Witchmail +0.03 (+0.17)
- **Rat King**: Return Fire +0.05 (+0.10), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.06)
- **Solomon**: Spirit Resilience +0.08 (+0.23), Reactive Barrier +0.07 (+0.13), Witchmail +0.07 (+0.21)
- **Nurse Harrow**: Dispel Magic +0.27 (+0.33), Spirit Resilience +0.25 (+0.41), Spellbreaker +0.08 (+0.25)
