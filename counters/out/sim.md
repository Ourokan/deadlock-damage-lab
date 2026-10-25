# Counter items in the sim (phantom and up)

Built 2026-10-25T13:08:24Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.238 | +0.074 | +0.126 | Nurse Harrow +0.21, Grey Talon +0.12, Mo & Krill +0.12 | 1 heroes |
| Divine Barrier | 6,400 | +0.391 | +0.062 | +0.097 | Nurse Harrow +0.23, Vindicta +0.17, Paradox +0.16 | 0 heroes |
| Reactive Barrier | 1,600 | +0.093 | +0.059 | +0.082 | Nurse Harrow +0.22, Venator +0.21, Paradox +0.13 | 1 heroes |
| Debuff Reducer | 1,600 | +0.088 | +0.055 | +0.072 | Holliday +0.15, Vyper +0.11, Sinclair +0.10 | 0 heroes |
| Dispel Magic | 3,200 | +0.157 | +0.049 | +0.095 | Nurse Harrow +0.36, Mirage +0.27, Paradox +0.16 | 4 heroes |
| Healbane | 1,600 | +0.073 | +0.045 | +0.094 | Haze +0.08, Mo & Krill +0.07, Nurse Harrow +0.07 | 10 heroes |
| Indomitable | 6,400 | +0.253 | +0.040 | +0.196 | Holliday +0.36, The Doorman +0.28, Sinclair +0.27 | 0 heroes |
| Witchmail | 6,400 | +0.223 | +0.035 | +0.178 | Nurse Harrow +0.23, Paradox +0.10, Mo & Krill +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | +0.104 | +0.033 | +0.105 | Nurse Harrow +0.17, Paradox +0.16, Venator +0.15 | 0 heroes |
| Spellbreaker | 6,400 | +0.166 | +0.026 | +0.163 | Holliday +0.22, Paradox +0.20, Mo & Krill +0.19 | 0 heroes |
| Plated Armor | 6,400 | +0.068 | +0.011 | +0.148 | Holliday +0.34, Haze +0.20, Nurse Harrow +0.17 | 0 heroes |
| Counterspell | 3,200 | +0.032 | +0.010 | +0.070 | Nurse Harrow +0.15, Vyper +0.06, Calico +0.05 | 1 heroes |
| Unstoppable | 6,400 | +0.062 | +0.010 | +0.148 | Rem +0.28, Abrams +0.20, Nurse Harrow +0.17 | 0 heroes |
| Metal Skin | 3,200 | -0.093 | -0.029 | +0.114 | Paradox +0.21, Nurse Harrow +0.16, Venator +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.108 | -0.068 | +0.088 | Venator +0.11, Grey Talon +0.08, Holliday +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.22), Spirit Resilience +0.05 (+0.18), Healbane +0.05 (+0.14)
- **Seven**: Unstoppable +0.10 (+0.25), Spirit Resilience +0.07 (+0.20), Plated Armor +0.06 (+0.21)
- **Vindicta**: Divine Barrier +0.17 (+0.27), Plated Armor +0.12 (+0.27), Bullet Resilience +0.11 (+0.22)
- **Lady Geist**: Spirit Resilience +0.08 (+0.20), Healbane +0.04 (+0.14), Witchmail +0.01 (+0.19)
- **Abrams**: Unstoppable +0.20 (+0.34), Indomitable +0.09 (+0.29), Divine Barrier +0.08 (+0.17)
- **Wraith**: Indomitable +0.16 (+0.36), Spellbreaker +0.08 (+0.24), Metal Skin +0.08 (+0.19)
- **McGinnis**: Healbane -0.03 (+0.07), Counterspell -0.03 (+0.04), Debuff Reducer -0.05 (+0.02)
- **Paradox**: Metal Skin +0.21 (+0.32), Spellbreaker +0.20 (+0.36), Indomitable +0.18 (+0.37)
- **Dynamo**: Indomitable +0.13 (+0.33), Debuff Reducer +0.04 (+0.11), Unstoppable -0.02 (+0.12)
- **Kelvin**: Healbane +0.03 (+0.13), Spirit Resilience +0.03 (+0.16), Witchmail +0.02 (+0.20)
- **Haze**: Plated Armor +0.20 (+0.35), Bullet Resilience +0.13 (+0.24), Metal Skin +0.09 (+0.20)
- **Holliday**: Indomitable +0.36 (+0.55), Plated Armor +0.34 (+0.49), Spellbreaker +0.22 (+0.38)
- **Bebop**: Healbane +0.01 (+0.10), Counterspell -0.01 (+0.06), Witchmail -0.03 (+0.14)
- **Calico**: Divine Barrier +0.07 (+0.16), Counterspell +0.05 (+0.12), Dispel Magic +0.04 (+0.13)
- **Grey Talon**: Spellbreaker +0.13 (+0.29), Spirit Resilience +0.12 (+0.25), Indomitable +0.11 (+0.31)
- **Mo & Krill**: Spellbreaker +0.19 (+0.36), Spirit Resilience +0.12 (+0.24), Witchmail +0.09 (+0.27)
- **Shiv**: Divine Barrier +0.03 (+0.13), Healbane +0.02 (+0.11), Metal Skin +0.01 (+0.12)
- **Ivy**: Healbane +0.00 (+0.10), Debuff Reducer -0.03 (+0.04), Counterspell -0.03 (+0.04)
- **Warden**: Dispel Magic +0.07 (+0.17), Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04)
- **Yamato**: Healbane -0.05 (+0.04), Counterspell -0.05 (+0.02), Debuff Reducer -0.06 (+0.01)
- **Lash**: Spellbreaker +0.11 (+0.28), Spirit Resilience +0.06 (+0.18), Indomitable +0.05 (+0.25)
- **Viscous**: Counterspell -0.02 (+0.05), Healbane -0.02 (+0.08), Divine Barrier -0.03 (+0.07)
- **Pocket**: Counterspell -0.00 (+0.07), Return Fire -0.01 (+0.08), Debuff Reducer -0.02 (+0.05)
- **Mirage**: Dispel Magic +0.27 (+0.36), Spellbreaker +0.04 (+0.20), Healbane +0.02 (+0.11)
- **Vyper**: Indomitable +0.24 (+0.43), Debuff Reducer +0.11 (+0.18), Spellbreaker +0.10 (+0.27)
- **Sinclair**: Indomitable +0.27 (+0.46), Spellbreaker +0.13 (+0.29), Debuff Reducer +0.10 (+0.17)
- **Mina**: Dispel Magic +0.07 (+0.17), Reactive Barrier +0.06 (+0.14), Divine Barrier +0.06 (+0.15)
- **Drifter**: Dispel Magic +0.12 (+0.21), Spirit Resilience +0.06 (+0.19), Return Fire +0.06 (+0.15)
- **Venator**: Indomitable +0.23 (+0.43), Reactive Barrier +0.21 (+0.29), Bullet Resilience +0.15 (+0.26)
- **Victor**: Healbane +0.02 (+0.12), Counterspell -0.03 (+0.04), Spirit Resilience -0.03 (+0.09)
- **Paige**: Return Fire +0.02 (+0.11), Unstoppable +0.02 (+0.17), Counterspell +0.02 (+0.09)
- **The Doorman**: Indomitable +0.28 (+0.47), Counterspell -0.01 (+0.06), Return Fire -0.02 (+0.07)
- **Billy**: Healbane +0.02 (+0.11), Counterspell +0.01 (+0.08), Witchmail +0.00 (+0.18)
- **Graves**: Return Fire +0.03 (+0.11), Counterspell -0.02 (+0.05), Healbane -0.03 (+0.06)
- **Apollo**: Divine Barrier -0.03 (+0.07), Spirit Resilience -0.03 (+0.10), Counterspell -0.06 (+0.01)
- **Deadman Danny**: Unstoppable +0.11 (+0.25), Indomitable +0.10 (+0.30), Spellbreaker +0.06 (+0.23)
- **Rem**: Unstoppable +0.28 (+0.43), Indomitable +0.22 (+0.42), Debuff Reducer +0.05 (+0.12)
- **Silver**: Dispel Magic -0.00 (+0.09), Debuff Reducer -0.02 (+0.06), Healbane -0.03 (+0.07)
- **Celeste**: Spirit Resilience +0.05 (+0.18), Witchmail +0.02 (+0.20), Counterspell +0.00 (+0.07)
- **Rat King**: Return Fire +0.05 (+0.13), Counterspell -0.01 (+0.06), Divine Barrier -0.02 (+0.07)
- **Solomon**: Debuff Reducer +0.02 (+0.10), Return Fire -0.00 (+0.08), Counterspell -0.01 (+0.06)
- **Nurse Harrow**: Dispel Magic +0.36 (+0.45), Witchmail +0.23 (+0.41), Divine Barrier +0.23 (+0.33)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.227 | +0.071 | +0.123 | Mina +0.28, Grey Talon +0.23, Seven +0.12 | 10 heroes |
| Divine Barrier | 6,400 | +0.346 | +0.055 | +0.070 | Vindicta +0.19, Mina +0.17, Paradox +0.16 | 1 heroes |
| Dispel Magic | 3,200 | +0.134 | +0.042 | +0.075 | Mina +0.24, Nurse Harrow +0.18, Paradox +0.16 | 7 heroes |
| Reactive Barrier | 1,600 | +0.065 | +0.041 | +0.061 | Mina +0.17, Venator +0.17, Paradox +0.14 | 2 heroes |
| Debuff Reducer | 1,600 | +0.063 | +0.039 | +0.063 | Holliday +0.18, Vyper +0.09, Lash +0.07 | 1 heroes |
| Indomitable | 6,400 | +0.244 | +0.039 | +0.191 | Holliday +0.40, The Doorman +0.38, Rem +0.29 | 0 heroes |
| Witchmail | 6,400 | +0.212 | +0.033 | +0.152 | Mina +0.18, Paradox +0.11, Grey Talon +0.09 | 0 heroes |
| Healbane | 1,600 | +0.053 | +0.033 | +0.087 | Haze +0.09, Nurse Harrow +0.07, Victor +0.06 | 16 heroes |
| Spellbreaker | 6,400 | +0.172 | +0.027 | +0.143 | Holliday +0.23, Mo & Krill +0.20, Mina +0.15 | 0 heroes |
| Bullet Resilience | 3,200 | +0.068 | +0.021 | +0.076 | Haze +0.15, Paradox +0.14, Venator +0.12 | 0 heroes |
| Plated Armor | 6,400 | +0.052 | +0.008 | +0.114 | Holliday +0.26, Haze +0.23, Vindicta +0.15 | 0 heroes |
| Unstoppable | 6,400 | +0.038 | +0.006 | +0.132 | Rem +0.35, Abrams +0.29, Paradox +0.18 | 0 heroes |
| Counterspell | 3,200 | +0.011 | +0.004 | +0.049 | Nurse Harrow +0.07, Vyper +0.06, Mina +0.04 | 1 heroes |
| Metal Skin | 3,200 | -0.110 | -0.034 | +0.098 | Venator +0.21, Paradox +0.20, Haze +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.128 | -0.080 | +0.065 | Venator +0.10, Vindicta +0.06, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.19), Healbane +0.06 (+0.15), Indomitable +0.03 (+0.22)
- **Seven**: Spirit Resilience +0.12 (+0.24), Witchmail +0.08 (+0.23), Healbane +0.04 (+0.13)
- **Vindicta**: Divine Barrier +0.19 (+0.26), Plated Armor +0.15 (+0.26), Bullet Resilience +0.11 (+0.19)
- **Lady Geist**: Spirit Resilience +0.07 (+0.19), Return Fire +0.02 (+0.08), Healbane +0.02 (+0.11)
- **Abrams**: Unstoppable +0.29 (+0.42), Spirit Resilience +0.09 (+0.21), Spellbreaker +0.08 (+0.23)
- **Wraith**: Indomitable +0.27 (+0.46), Metal Skin +0.12 (+0.22), Spellbreaker +0.06 (+0.21)
- **McGinnis**: Counterspell -0.02 (+0.03), Healbane -0.02 (+0.07), Debuff Reducer -0.04 (+0.02)
- **Paradox**: Indomitable +0.25 (+0.44), Metal Skin +0.20 (+0.30), Unstoppable +0.18 (+0.31)
- **Dynamo**: Indomitable +0.08 (+0.27), Debuff Reducer +0.05 (+0.11), Unstoppable -0.02 (+0.11)
- **Kelvin**: Spirit Resilience +0.01 (+0.13), Healbane -0.02 (+0.07), Counterspell -0.02 (+0.03)
- **Haze**: Plated Armor +0.23 (+0.35), Bullet Resilience +0.15 (+0.23), Metal Skin +0.14 (+0.24)
- **Holliday**: Indomitable +0.40 (+0.59), Plated Armor +0.26 (+0.38), Spellbreaker +0.23 (+0.37)
- **Bebop**: Healbane +0.02 (+0.11), Witchmail +0.01 (+0.16), Counterspell -0.01 (+0.04)
- **Calico**: Reactive Barrier +0.04 (+0.10), Divine Barrier +0.03 (+0.10), Spirit Resilience +0.01 (+0.13)
- **Grey Talon**: Spirit Resilience +0.23 (+0.35), Indomitable +0.16 (+0.35), Spellbreaker +0.15 (+0.29)
- **Mo & Krill**: Spellbreaker +0.20 (+0.34), Unstoppable +0.08 (+0.21), Spirit Resilience +0.06 (+0.18)
- **Shiv**: Metal Skin +0.05 (+0.15), Divine Barrier +0.05 (+0.12), Plated Armor +0.02 (+0.13)
- **Ivy**: Unstoppable -0.00 (+0.13), Healbane -0.01 (+0.08), Debuff Reducer -0.04 (+0.03)
- **Warden**: Dispel Magic +0.06 (+0.14), Debuff Reducer -0.02 (+0.04), Counterspell -0.02 (+0.02)
- **Yamato**: Healbane -0.03 (+0.06), Counterspell -0.04 (+0.01), Debuff Reducer -0.06 (+0.01)
- **Lash**: Spellbreaker +0.12 (+0.27), Indomitable +0.10 (+0.29), Debuff Reducer +0.07 (+0.13)
- **Viscous**: Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.06), Reactive Barrier -0.02 (+0.05)
- **Pocket**: Spirit Resilience +0.05 (+0.17), Return Fire +0.02 (+0.08), Counterspell -0.01 (+0.04)
- **Mirage**: Dispel Magic +0.14 (+0.22), Metal Skin -0.01 (+0.08), Counterspell -0.02 (+0.03)
- **Vyper**: Indomitable +0.29 (+0.48), Debuff Reducer +0.09 (+0.16), Spellbreaker +0.07 (+0.21)
- **Sinclair**: Indomitable +0.20 (+0.39), Spellbreaker +0.11 (+0.25), Debuff Reducer +0.06 (+0.13)
- **Mina**: Spirit Resilience +0.28 (+0.41), Dispel Magic +0.24 (+0.31), Witchmail +0.18 (+0.33)
- **Drifter**: Dispel Magic +0.13 (+0.20), Return Fire +0.06 (+0.13), Healbane +0.06 (+0.15)
- **Venator**: Metal Skin +0.21 (+0.31), Indomitable +0.21 (+0.40), Reactive Barrier +0.17 (+0.23)
- **Victor**: Spellbreaker +0.10 (+0.24), Spirit Resilience +0.09 (+0.22), Healbane +0.06 (+0.15)
- **Paige**: Unstoppable +0.03 (+0.16), Indomitable +0.02 (+0.22), Return Fire +0.01 (+0.07)
- **The Doorman**: Indomitable +0.38 (+0.57), Reactive Barrier +0.01 (+0.07), Divine Barrier +0.01 (+0.08)
- **Billy**: Healbane +0.05 (+0.14), Counterspell +0.03 (+0.08), Witchmail +0.00 (+0.15)
- **Graves**: Return Fire +0.04 (+0.10), Witchmail +0.00 (+0.15), Counterspell -0.00 (+0.04)
- **Apollo**: Healbane -0.01 (+0.08), Divine Barrier -0.02 (+0.05), Spirit Resilience -0.02 (+0.10)
- **Deadman Danny**: Spirit Resilience +0.03 (+0.16), Unstoppable +0.03 (+0.17), Spellbreaker +0.03 (+0.17)
- **Rem**: Unstoppable +0.35 (+0.48), Indomitable +0.29 (+0.48), Debuff Reducer +0.06 (+0.13)
- **Silver**: Dispel Magic +0.02 (+0.09), Healbane +0.01 (+0.09), Debuff Reducer -0.00 (+0.06)
- **Celeste**: Spirit Resilience +0.05 (+0.18), Witchmail +0.02 (+0.17), Dispel Magic +0.01 (+0.09)
- **Rat King**: Return Fire +0.05 (+0.12), Counterspell -0.00 (+0.05), Divine Barrier -0.01 (+0.06)
- **Solomon**: Debuff Reducer +0.03 (+0.09), Reactive Barrier +0.02 (+0.08), Counterspell +0.02 (+0.07)
- **Nurse Harrow**: Dispel Magic +0.18 (+0.26), Witchmail +0.08 (+0.23), Healbane +0.07 (+0.16)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.210 | +0.066 | +0.115 | Paradox +0.42, Mina +0.23, Grey Talon +0.13 | 13 heroes |
| Indomitable | 6,400 | +0.238 | +0.038 | +0.182 | Holliday +0.48, The Doorman +0.46, Paradox +0.25 | 0 heroes |
| Dispel Magic | 3,200 | +0.116 | +0.036 | +0.059 | Nurse Harrow +0.22, Paradox +0.21, Mina +0.21 | 9 heroes |
| Divine Barrier | 6,400 | +0.228 | +0.036 | +0.060 | Vindicta +0.22, Paradox +0.21, Mina +0.16 | 2 heroes |
| Debuff Reducer | 1,600 | +0.052 | +0.032 | +0.056 | Holliday +0.20, Lash +0.11, Rem +0.09 | 0 heroes |
| Reactive Barrier | 1,600 | +0.052 | +0.032 | +0.054 | Mina +0.17, Paradox +0.17, Venator +0.12 | 3 heroes |
| Witchmail | 6,400 | +0.202 | +0.032 | +0.145 | Paradox +0.28, Mina +0.18, Vindicta +0.11 | 1 heroes |
| Spellbreaker | 6,400 | +0.168 | +0.026 | +0.135 | Paradox +0.28, Holliday +0.27, Mo & Krill +0.22 | 0 heroes |
| Healbane | 1,600 | +0.033 | +0.021 | +0.073 | Infernus +0.10, Victor +0.09, Haze +0.05 | 15 heroes |
| Bullet Resilience | 3,200 | +0.057 | +0.018 | +0.067 | Paradox +0.18, Haze +0.16, Vindicta +0.14 | 0 heroes |
| Plated Armor | 6,400 | +0.051 | +0.008 | +0.116 | Haze +0.31, Holliday +0.29, Vindicta +0.17 | 0 heroes |
| Unstoppable | 6,400 | +0.042 | +0.006 | +0.143 | Rem +0.46, Venator +0.21, Paradox +0.20 | 3 heroes |
| Counterspell | 3,200 | -0.004 | -0.001 | +0.035 | Paradox +0.08, Vindicta +0.05, Billy +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.114 | -0.035 | +0.094 | Paradox +0.22, Haze +0.14, Mina +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.133 | -0.083 | +0.055 | Paradox +0.13, Vindicta +0.10, Venator +0.09 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.16), Healbane +0.10 (+0.17), Spirit Resilience +0.07 (+0.18)
- **Seven**: Metal Skin +0.09 (+0.19), Spirit Resilience +0.09 (+0.21), Witchmail +0.09 (+0.24)
- **Vindicta**: Divine Barrier +0.22 (+0.28), Plated Armor +0.17 (+0.29), Bullet Resilience +0.14 (+0.21)
- **Lady Geist**: Spirit Resilience +0.05 (+0.17), Return Fire +0.03 (+0.09), Healbane +0.01 (+0.08)
- **Abrams**: Unstoppable +0.10 (+0.24), Divine Barrier +0.00 (+0.06), Spirit Resilience +0.00 (+0.12)
- **Wraith**: Indomitable +0.23 (+0.41), Metal Skin +0.09 (+0.19), Witchmail +0.08 (+0.23)
- **McGinnis**: Healbane +0.00 (+0.08), Counterspell -0.00 (+0.03), Witchmail -0.04 (+0.11)
- **Paradox**: Spirit Resilience +0.42 (+0.54), Spellbreaker +0.28 (+0.42), Witchmail +0.28 (+0.42)
- **Dynamo**: Indomitable +0.12 (+0.30), Debuff Reducer +0.05 (+0.10), Counterspell -0.02 (+0.01)
- **Kelvin**: Healbane +0.00 (+0.08), Counterspell -0.00 (+0.03), Dispel Magic -0.02 (+0.04)
- **Haze**: Plated Armor +0.31 (+0.43), Unstoppable +0.18 (+0.32), Indomitable +0.17 (+0.35)
- **Holliday**: Indomitable +0.48 (+0.66), Plated Armor +0.29 (+0.40), Spellbreaker +0.27 (+0.41)
- **Bebop**: Healbane +0.01 (+0.09), Counterspell -0.01 (+0.03), Return Fire -0.03 (+0.03)
- **Calico**: Divine Barrier -0.01 (+0.05), Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (+0.03)
- **Grey Talon**: Spellbreaker +0.18 (+0.32), Spirit Resilience +0.13 (+0.24), Indomitable +0.10 (+0.28)
- **Mo & Krill**: Spellbreaker +0.22 (+0.35), Unstoppable +0.09 (+0.23), Spirit Resilience +0.08 (+0.19)
- **Shiv**: Metal Skin +0.08 (+0.18), Divine Barrier +0.06 (+0.12), Bullet Resilience +0.05 (+0.12)
- **Ivy**: Healbane +0.03 (+0.11), Unstoppable +0.02 (+0.16), Dispel Magic -0.01 (+0.05)
- **Warden**: Dispel Magic +0.06 (+0.12), Healbane +0.00 (+0.08), Counterspell -0.02 (+0.02)
- **Yamato**: Healbane +0.01 (+0.09), Counterspell -0.02 (+0.01), Reactive Barrier -0.05 (+0.01)
- **Lash**: Indomitable +0.17 (+0.35), Spellbreaker +0.14 (+0.27), Debuff Reducer +0.11 (+0.17)
- **Viscous**: Divine Barrier +0.00 (+0.06), Reactive Barrier -0.00 (+0.05), Counterspell -0.01 (+0.03)
- **Pocket**: Counterspell -0.00 (+0.03), Return Fire -0.02 (+0.04), Dispel Magic -0.02 (+0.04)
- **Mirage**: Dispel Magic +0.15 (+0.21), Spellbreaker +0.02 (+0.16), Metal Skin +0.00 (+0.10)
- **Vyper**: Indomitable +0.25 (+0.43), Debuff Reducer +0.06 (+0.12), Spellbreaker +0.04 (+0.18)
- **Sinclair**: Indomitable +0.19 (+0.37), Spellbreaker +0.07 (+0.21), Debuff Reducer +0.07 (+0.12)
- **Mina**: Spirit Resilience +0.23 (+0.34), Dispel Magic +0.21 (+0.27), Witchmail +0.18 (+0.33)
- **Drifter**: Dispel Magic +0.07 (+0.13), Return Fire +0.02 (+0.08), Healbane +0.02 (+0.09)
- **Venator**: Unstoppable +0.21 (+0.35), Indomitable +0.12 (+0.31), Reactive Barrier +0.12 (+0.17)
- **Victor**: Healbane +0.09 (+0.17), Spellbreaker +0.09 (+0.23), Spirit Resilience +0.07 (+0.19)
- **Paige**: Unstoppable +0.01 (+0.16), Return Fire +0.00 (+0.06), Counterspell +0.00 (+0.04)
- **The Doorman**: Indomitable +0.46 (+0.64), Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.04)
- **Billy**: Counterspell +0.03 (+0.07), Reactive Barrier +0.02 (+0.07), Debuff Reducer +0.01 (+0.07)
- **Graves**: Return Fire +0.02 (+0.08), Counterspell -0.02 (+0.02), Metal Skin -0.02 (+0.08)
- **Apollo**: Counterspell -0.02 (+0.01), Healbane -0.03 (+0.05), Divine Barrier -0.03 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.03 (+0.15), Spellbreaker +0.01 (+0.14), Bullet Resilience +0.01 (+0.07)
- **Rem**: Unstoppable +0.46 (+0.60), Debuff Reducer +0.09 (+0.14), Spellbreaker +0.01 (+0.14)
- **Silver**: Dispel Magic +0.04 (+0.10), Divine Barrier +0.01 (+0.07), Reactive Barrier -0.02 (+0.04)
- **Celeste**: Spirit Resilience +0.04 (+0.15), Healbane +0.01 (+0.08), Dispel Magic -0.01 (+0.05)
- **Rat King**: Return Fire +0.02 (+0.07), Counterspell -0.01 (+0.03), Metal Skin -0.01 (+0.08)
- **Solomon**: Debuff Reducer +0.03 (+0.09), Spellbreaker +0.02 (+0.15), Counterspell +0.00 (+0.04)
- **Nurse Harrow**: Dispel Magic +0.22 (+0.28), Witchmail +0.05 (+0.20), Counterspell +0.03 (+0.06)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.252 | +0.079 | +0.141 | Nurse Harrow +0.38, Paradox +0.28, Sinclair +0.16 | 14 heroes |
| Indomitable | 6,400 | +0.297 | +0.047 | +0.235 | The Doorman +0.83, Wraith +0.50, Holliday +0.38 | 1 heroes |
| Debuff Reducer | 1,600 | +0.065 | +0.041 | +0.077 | Holliday +0.18, Lash +0.16, Wraith +0.15 | 0 heroes |
| Dispel Magic | 3,200 | +0.121 | +0.038 | +0.067 | Nurse Harrow +0.42, Paradox +0.16, Vindicta +0.15 | 9 heroes |
| Spellbreaker | 6,400 | +0.214 | +0.034 | +0.173 | Mo & Krill +0.22, Holliday +0.21, Paradox +0.21 | 0 heroes |
| Witchmail | 6,400 | +0.191 | +0.030 | +0.136 | Nurse Harrow +0.21, Paradox +0.20, The Doorman +0.14 | 2 heroes |
| Divine Barrier | 6,400 | +0.187 | +0.029 | +0.055 | Nurse Harrow +0.19, Vindicta +0.15, The Doorman +0.12 | 3 heroes |
| Healbane | 1,600 | +0.044 | +0.028 | +0.076 | Victor +0.20, Vindicta +0.09, Infernus +0.08 | 12 heroes |
| Reactive Barrier | 1,600 | +0.032 | +0.020 | +0.056 | Venator +0.13, The Doorman +0.12, Solomon +0.08 | 2 heroes |
| Unstoppable | 6,400 | +0.123 | +0.019 | +0.233 | Paige +0.62, Rem +0.38, Paradox +0.25 | 8 heroes |
| Bullet Resilience | 3,200 | +0.057 | +0.018 | +0.075 | Haze +0.15, Vindicta +0.14, Venator +0.09 | 0 heroes |
| Plated Armor | 6,400 | +0.049 | +0.008 | +0.125 | Vindicta +0.29, Nurse Harrow +0.21, Haze +0.18 | 1 heroes |
| Counterspell | 3,200 | -0.015 | -0.005 | +0.029 | Kelvin +0.05, Seven +0.03, Holliday +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.102 | -0.032 | +0.111 | Nurse Harrow +0.25, Venator +0.16, Wraith +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.145 | -0.090 | +0.045 | Venator +0.11, Solomon +0.06, Rat King +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.16 (+0.39), Dispel Magic +0.10 (+0.16), Spirit Resilience +0.08 (+0.22)
- **Seven**: Unstoppable +0.22 (+0.46), Indomitable +0.19 (+0.43), Metal Skin +0.13 (+0.24)
- **Vindicta**: Plated Armor +0.29 (+0.41), Dispel Magic +0.15 (+0.22), Divine Barrier +0.15 (+0.21)
- **Lady Geist**: Healbane +0.02 (+0.10), Bullet Resilience -0.02 (+0.06), Counterspell -0.02 (+0.01)
- **Abrams**: Unstoppable +0.14 (+0.37), Spirit Resilience +0.03 (+0.17), Divine Barrier +0.02 (+0.07)
- **Wraith**: Indomitable +0.50 (+0.74), Unstoppable +0.16 (+0.39), Debuff Reducer +0.15 (+0.23)
- **McGinnis**: Spirit Resilience +0.07 (+0.21), Witchmail +0.07 (+0.20), Healbane +0.06 (+0.14)
- **Paradox**: Spirit Resilience +0.28 (+0.42), Unstoppable +0.25 (+0.49), Spellbreaker +0.21 (+0.38)
- **Dynamo**: Indomitable +0.17 (+0.41), Debuff Reducer +0.08 (+0.16), Healbane +0.01 (+0.08)
- **Kelvin**: Counterspell +0.05 (+0.08), Witchmail +0.04 (+0.18), Spirit Resilience +0.03 (+0.17)
- **Haze**: Plated Armor +0.18 (+0.31), Bullet Resilience +0.15 (+0.23), Metal Skin +0.11 (+0.22)
- **Holliday**: Indomitable +0.38 (+0.61), Spellbreaker +0.21 (+0.38), Debuff Reducer +0.18 (+0.26)
- **Bebop**: Spellbreaker +0.04 (+0.21), Healbane +0.02 (+0.10), Debuff Reducer +0.02 (+0.09)
- **Calico**: Spirit Resilience +0.02 (+0.16), Divine Barrier +0.02 (+0.07), Counterspell -0.00 (+0.03)
- **Grey Talon**: Spirit Resilience +0.07 (+0.21), Spellbreaker +0.03 (+0.20), Witchmail +0.03 (+0.16)
- **Mo & Krill**: Spellbreaker +0.22 (+0.39), Healbane +0.06 (+0.14), Unstoppable +0.06 (+0.29)
- **Shiv**: Divine Barrier +0.05 (+0.11), Bullet Resilience +0.05 (+0.12), Metal Skin +0.05 (+0.16)
- **Ivy**: Counterspell -0.01 (+0.02), Healbane -0.02 (+0.06), Unstoppable -0.02 (+0.22)
- **Warden**: Dispel Magic -0.01 (+0.06), Healbane -0.01 (+0.06), Counterspell -0.02 (+0.01)
- **Yamato**: Healbane +0.03 (+0.10), Counterspell -0.01 (+0.02), Return Fire -0.04 (+0.01)
- **Lash**: Indomitable +0.23 (+0.47), Spellbreaker +0.17 (+0.34), Debuff Reducer +0.16 (+0.24)
- **Viscous**: Spirit Resilience +0.08 (+0.22), Divine Barrier +0.03 (+0.09), Reactive Barrier +0.02 (+0.08)
- **Pocket**: Return Fire +0.01 (+0.05), Counterspell -0.01 (+0.02), Divine Barrier -0.04 (+0.01)
- **Mirage**: Dispel Magic +0.11 (+0.18), Metal Skin +0.00 (+0.11), Counterspell -0.01 (+0.02)
- **Vyper**: Indomitable +0.20 (+0.43), Debuff Reducer +0.04 (+0.12), Plated Armor +0.03 (+0.16)
- **Sinclair**: Indomitable +0.33 (+0.57), Spellbreaker +0.17 (+0.35), Spirit Resilience +0.16 (+0.30)
- **Mina**: Spirit Resilience +0.08 (+0.22), Divine Barrier +0.06 (+0.12), Reactive Barrier +0.06 (+0.11)
- **Drifter**: Dispel Magic +0.13 (+0.20), Unstoppable +0.04 (+0.27), Spellbreaker +0.04 (+0.21)
- **Venator**: Unstoppable +0.22 (+0.45), Metal Skin +0.16 (+0.27), Reactive Barrier +0.13 (+0.18)
- **Victor**: Healbane +0.20 (+0.28), Spellbreaker +0.18 (+0.35), Witchmail +0.13 (+0.27)
- **Paige**: Unstoppable +0.62 (+0.85), Debuff Reducer +0.07 (+0.15), Indomitable +0.06 (+0.30)
- **The Doorman**: Indomitable +0.83 (+1.06), Dispel Magic +0.15 (+0.22), Witchmail +0.14 (+0.28)
- **Billy**: Healbane +0.02 (+0.09), Reactive Barrier +0.02 (+0.07), Counterspell +0.00 (+0.03)
- **Graves**: Return Fire +0.05 (+0.09), Counterspell -0.01 (+0.02), Metal Skin -0.01 (+0.10)
- **Apollo**: Spirit Resilience -0.00 (+0.14), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.06)
- **Deadman Danny**: Spirit Resilience +0.09 (+0.23), Spellbreaker +0.03 (+0.21), Dispel Magic +0.03 (+0.10)
- **Rem**: Unstoppable +0.38 (+0.62), Debuff Reducer -0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Silver**: Dispel Magic +0.04 (+0.11), Divine Barrier -0.01 (+0.04), Reactive Barrier -0.02 (+0.04)
- **Celeste**: Spirit Resilience +0.03 (+0.17), Counterspell +0.01 (+0.04), Healbane +0.01 (+0.08)
- **Rat King**: Return Fire +0.06 (+0.10), Counterspell -0.00 (+0.03), Healbane -0.00 (+0.07)
- **Solomon**: Spirit Resilience +0.12 (+0.26), Witchmail +0.09 (+0.23), Reactive Barrier +0.08 (+0.14)
- **Nurse Harrow**: Dispel Magic +0.42 (+0.48), Spirit Resilience +0.38 (+0.52), Metal Skin +0.25 (+0.36)
