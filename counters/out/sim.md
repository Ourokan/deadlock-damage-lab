# Counter items in the sim (phantom and up)

Built 2026-10-25T17:04:10Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.224 | +0.070 | +0.115 | Mo & Krill +0.14, Holliday +0.12, Grey Talon +0.11 | 1 heroes |
| Divine Barrier | 6,400 | +0.321 | +0.051 | +0.083 | Vindicta +0.20, Paradox +0.12, Venator +0.10 | 0 heroes |
| Debuff Reducer | 1,600 | +0.074 | +0.046 | +0.066 | Holliday +0.16, Vyper +0.13, Sinclair +0.10 | 0 heroes |
| Dispel Magic | 3,200 | +0.141 | +0.044 | +0.079 | Mirage +0.28, Infernus +0.15, Drifter +0.12 | 4 heroes |
| Reactive Barrier | 1,600 | +0.070 | +0.044 | +0.067 | Venator +0.21, Holliday +0.10, Paradox +0.09 | 2 heroes |
| Indomitable | 6,400 | +0.237 | +0.037 | +0.184 | Holliday +0.39, The Doorman +0.32, Sinclair +0.28 | 0 heroes |
| Witchmail | 6,400 | +0.204 | +0.032 | +0.171 | Grey Talon +0.11, Vindicta +0.11, Mo & Krill +0.11 | 0 heroes |
| Healbane | 1,600 | +0.047 | +0.029 | +0.092 | Haze +0.09, Mo & Krill +0.08, Infernus +0.06 | 11 heroes |
| Spellbreaker | 6,400 | +0.155 | +0.024 | +0.151 | Holliday +0.25, Mo & Krill +0.22, Paradox +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | +0.043 | +0.014 | +0.091 | Venator +0.19, Haze +0.15, Vindicta +0.15 | 0 heroes |
| Unstoppable | 6,400 | +0.032 | +0.005 | +0.148 | Rem +0.30, Abrams +0.22, Holliday +0.17 | 0 heroes |
| Plated Armor | 6,400 | +0.029 | +0.005 | +0.132 | Holliday +0.37, Haze +0.22, Vindicta +0.16 | 0 heroes |
| Counterspell | 3,200 | +0.011 | +0.004 | +0.063 | Vyper +0.08, Vindicta +0.07, Calico +0.05 | 1 heroes |
| Metal Skin | 3,200 | -0.101 | -0.032 | +0.099 | Venator +0.19, Paradox +0.16, Haze +0.09 | 0 heroes |
| Return Fire | 1,600 | -0.126 | -0.078 | +0.079 | Venator +0.12, Paradox +0.10, Holliday +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.15 (+0.23), Spirit Resilience +0.07 (+0.19), Healbane +0.06 (+0.15)
- **Seven**: Unstoppable +0.12 (+0.26), Spirit Resilience +0.08 (+0.20), Plated Armor +0.08 (+0.21)
- **Vindicta**: Divine Barrier +0.20 (+0.29), Plated Armor +0.16 (+0.29), Bullet Resilience +0.15 (+0.24)
- **Lady Geist**: Spirit Resilience +0.10 (+0.21), Healbane +0.05 (+0.14), Witchmail +0.03 (+0.20)
- **Abrams**: Unstoppable +0.22 (+0.36), Indomitable +0.10 (+0.28), Divine Barrier +0.09 (+0.17)
- **Wraith**: Indomitable +0.17 (+0.35), Metal Skin +0.09 (+0.19), Spellbreaker +0.09 (+0.24)
- **McGinnis**: Healbane -0.02 (+0.07), Counterspell -0.02 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Paradox**: Metal Skin +0.16 (+0.26), Spellbreaker +0.16 (+0.31), Indomitable +0.14 (+0.32)
- **Dynamo**: Indomitable +0.17 (+0.35), Debuff Reducer +0.06 (+0.12), Unstoppable -0.01 (+0.13)
- **Kelvin**: Healbane +0.03 (+0.13), Spirit Resilience +0.03 (+0.14), Witchmail +0.02 (+0.19)
- **Haze**: Plated Armor +0.22 (+0.35), Bullet Resilience +0.15 (+0.24), Metal Skin +0.09 (+0.19)
- **Holliday**: Indomitable +0.39 (+0.58), Plated Armor +0.37 (+0.50), Spellbreaker +0.25 (+0.40)
- **Bebop**: Healbane +0.01 (+0.10), Counterspell -0.01 (+0.05), Witchmail -0.03 (+0.14)
- **Calico**: Divine Barrier +0.06 (+0.15), Counterspell +0.05 (+0.11), Dispel Magic +0.03 (+0.11)
- **Grey Talon**: Spellbreaker +0.13 (+0.28), Spirit Resilience +0.11 (+0.23), Indomitable +0.11 (+0.30)
- **Mo & Krill**: Spellbreaker +0.22 (+0.37), Spirit Resilience +0.14 (+0.25), Witchmail +0.11 (+0.28)
- **Shiv**: Divine Barrier +0.05 (+0.13), Healbane +0.02 (+0.12), Metal Skin +0.02 (+0.12)
- **Ivy**: Healbane +0.01 (+0.11), Counterspell -0.02 (+0.05), Unstoppable -0.02 (+0.13)
- **Warden**: Dispel Magic +0.09 (+0.17), Healbane -0.01 (+0.08), Counterspell -0.01 (+0.05)
- **Yamato**: Counterspell -0.05 (+0.02), Healbane -0.05 (+0.04), Debuff Reducer -0.06 (+0.01)
- **Lash**: Spellbreaker +0.12 (+0.27), Spirit Resilience +0.07 (+0.18), Indomitable +0.07 (+0.25)
- **Viscous**: Counterspell -0.01 (+0.05), Healbane -0.01 (+0.08), Reactive Barrier -0.01 (+0.06)
- **Pocket**: Counterspell -0.00 (+0.06), Return Fire -0.01 (+0.07), Debuff Reducer -0.02 (+0.05)
- **Mirage**: Dispel Magic +0.28 (+0.36), Spellbreaker +0.05 (+0.20), Spirit Resilience +0.02 (+0.14)
- **Vyper**: Indomitable +0.25 (+0.44), Spellbreaker +0.13 (+0.29), Debuff Reducer +0.13 (+0.19)
- **Sinclair**: Indomitable +0.28 (+0.46), Spellbreaker +0.13 (+0.29), Debuff Reducer +0.10 (+0.17)
- **Mina**: Dispel Magic +0.08 (+0.16), Reactive Barrier +0.08 (+0.14), Witchmail +0.06 (+0.24)
- **Drifter**: Dispel Magic +0.12 (+0.20), Return Fire +0.07 (+0.15), Metal Skin +0.07 (+0.16)
- **Venator**: Indomitable +0.25 (+0.43), Reactive Barrier +0.21 (+0.28), Metal Skin +0.19 (+0.29)
- **Victor**: Healbane +0.04 (+0.14), Spirit Resilience -0.01 (+0.10), Counterspell -0.02 (+0.04)
- **Paige**: Return Fire +0.04 (+0.11), Unstoppable +0.03 (+0.18), Counterspell +0.03 (+0.09)
- **The Doorman**: Indomitable +0.32 (+0.50), Counterspell -0.00 (+0.06), Return Fire -0.01 (+0.07)
- **Billy**: Counterspell +0.04 (+0.10), Healbane +0.02 (+0.11), Debuff Reducer +0.01 (+0.07)
- **Graves**: Return Fire +0.03 (+0.11), Counterspell -0.01 (+0.05), Healbane -0.03 (+0.07)
- **Apollo**: Spirit Resilience +0.00 (+0.12), Divine Barrier -0.01 (+0.08), Reactive Barrier -0.04 (+0.03)
- **Deadman Danny**: Unstoppable +0.08 (+0.23), Spirit Resilience +0.08 (+0.19), Spellbreaker +0.07 (+0.22)
- **Rem**: Unstoppable +0.30 (+0.44), Indomitable +0.25 (+0.44), Debuff Reducer +0.06 (+0.12)
- **Silver**: Dispel Magic +0.00 (+0.08), Debuff Reducer -0.02 (+0.05), Divine Barrier -0.02 (+0.06)
- **Celeste**: Spirit Resilience +0.07 (+0.19), Witchmail +0.03 (+0.20), Counterspell +0.02 (+0.08)
- **Rat King**: Return Fire +0.06 (+0.13), Counterspell -0.00 (+0.06), Divine Barrier -0.01 (+0.07)
- **Solomon**: Debuff Reducer +0.03 (+0.10), Return Fire +0.00 (+0.08), Counterspell +0.00 (+0.06)
- **Violet**: Unstoppable -0.02 (+0.13), Dispel Magic -0.04 (+0.04), Spirit Resilience -0.04 (+0.07)
- **Nurse Harrow**: Dispel Magic -0.02 (+0.06), Debuff Reducer -0.04 (+0.03), Counterspell -0.04 (+0.02)
- **Baba**: Unstoppable +0.16 (+0.31), Healbane +0.03 (+0.13), Indomitable +0.02 (+0.21)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.213 | +0.067 | +0.112 | Mina +0.24, Grey Talon +0.21, Paradox +0.13 | 10 heroes |
| Dispel Magic | 3,200 | +0.127 | +0.040 | +0.066 | Mina +0.21, Mirage +0.17, Infernus +0.15 | 7 heroes |
| Indomitable | 6,400 | +0.237 | +0.038 | +0.188 | The Doorman +0.40, Holliday +0.40, Rem +0.31 | 0 heroes |
| Divine Barrier | 6,400 | +0.218 | +0.035 | +0.064 | Vindicta +0.24, Paradox +0.18, Mina +0.15 | 1 heroes |
| Debuff Reducer | 1,600 | +0.052 | +0.033 | +0.059 | Holliday +0.17, Vyper +0.10, Rem +0.08 | 1 heroes |
| Reactive Barrier | 1,600 | +0.050 | +0.031 | +0.055 | Venator +0.18, Mina +0.17, Paradox +0.14 | 4 heroes |
| Witchmail | 6,400 | +0.196 | +0.031 | +0.147 | Mina +0.16, Vindicta +0.14, Paradox +0.13 | 0 heroes |
| Spellbreaker | 6,400 | +0.163 | +0.025 | +0.136 | Holliday +0.23, Mo & Krill +0.21, Paradox +0.17 | 0 heroes |
| Healbane | 1,600 | +0.023 | +0.014 | +0.085 | Haze +0.07, Victor +0.06, Infernus +0.06 | 17 heroes |
| Bullet Resilience | 3,200 | +0.019 | +0.006 | +0.072 | Vindicta +0.17, Haze +0.16, Venator +0.15 | 0 heroes |
| Plated Armor | 6,400 | +0.021 | +0.003 | +0.106 | Holliday +0.25, Haze +0.25, Vindicta +0.20 | 0 heroes |
| Unstoppable | 6,400 | +0.016 | +0.002 | +0.140 | Rem +0.36, Abrams +0.30, Paradox +0.20 | 0 heroes |
| Counterspell | 3,200 | -0.005 | -0.002 | +0.045 | Vyper +0.06, Paradox +0.04, Vindicta +0.04 | 1 heroes |
| Metal Skin | 3,200 | -0.113 | -0.035 | +0.090 | Venator +0.26, Paradox +0.23, Haze +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.143 | -0.089 | +0.059 | Paradox +0.12, Venator +0.10, Vindicta +0.09 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.15 (+0.22), Healbane +0.06 (+0.15), Indomitable +0.06 (+0.25)
- **Seven**: Spirit Resilience +0.13 (+0.24), Witchmail +0.09 (+0.23), Indomitable +0.05 (+0.24)
- **Vindicta**: Divine Barrier +0.24 (+0.30), Plated Armor +0.20 (+0.31), Bullet Resilience +0.17 (+0.24)
- **Lady Geist**: Spirit Resilience +0.06 (+0.17), Healbane +0.03 (+0.12), Witchmail +0.02 (+0.17)
- **Abrams**: Unstoppable +0.30 (+0.44), Spellbreaker +0.08 (+0.22), Spirit Resilience +0.08 (+0.19)
- **Wraith**: Indomitable +0.27 (+0.46), Metal Skin +0.12 (+0.21), Witchmail +0.06 (+0.21)
- **McGinnis**: Counterspell -0.01 (+0.04), Healbane -0.01 (+0.07), Debuff Reducer -0.04 (+0.02)
- **Paradox**: Indomitable +0.27 (+0.46), Metal Skin +0.23 (+0.32), Unstoppable +0.20 (+0.34)
- **Dynamo**: Indomitable +0.14 (+0.33), Debuff Reducer +0.07 (+0.13), Counterspell -0.02 (+0.03)
- **Kelvin**: Spirit Resilience +0.01 (+0.12), Healbane -0.01 (+0.07), Counterspell -0.02 (+0.03)
- **Haze**: Plated Armor +0.25 (+0.35), Bullet Resilience +0.16 (+0.24), Metal Skin +0.14 (+0.23)
- **Holliday**: Indomitable +0.40 (+0.59), Plated Armor +0.25 (+0.36), Spellbreaker +0.23 (+0.36)
- **Bebop**: Witchmail +0.03 (+0.18), Healbane +0.03 (+0.11), Counterspell +0.01 (+0.05)
- **Calico**: Reactive Barrier +0.04 (+0.09), Divine Barrier +0.03 (+0.09), Spirit Resilience -0.00 (+0.11)
- **Grey Talon**: Spirit Resilience +0.21 (+0.32), Indomitable +0.14 (+0.33), Spellbreaker +0.13 (+0.27)
- **Mo & Krill**: Spellbreaker +0.21 (+0.35), Unstoppable +0.10 (+0.24), Spirit Resilience +0.06 (+0.18)
- **Shiv**: Metal Skin +0.07 (+0.16), Divine Barrier +0.06 (+0.12), Plated Armor +0.03 (+0.13)
- **Ivy**: Unstoppable +0.01 (+0.15), Healbane +0.00 (+0.09), Counterspell -0.03 (+0.02)
- **Warden**: Dispel Magic +0.08 (+0.14), Counterspell -0.02 (+0.02), Return Fire -0.02 (+0.03)
- **Yamato**: Healbane -0.02 (+0.06), Counterspell -0.03 (+0.02), Debuff Reducer -0.05 (+0.01)
- **Lash**: Spellbreaker +0.12 (+0.26), Indomitable +0.10 (+0.28), Debuff Reducer +0.07 (+0.13)
- **Viscous**: Counterspell -0.00 (+0.05), Reactive Barrier -0.01 (+0.05), Divine Barrier -0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.06 (+0.17), Return Fire +0.03 (+0.09), Witchmail +0.02 (+0.17)
- **Mirage**: Dispel Magic +0.17 (+0.24), Metal Skin +0.01 (+0.10), Spellbreaker +0.01 (+0.14)
- **Vyper**: Indomitable +0.29 (+0.48), Debuff Reducer +0.10 (+0.15), Spellbreaker +0.07 (+0.20)
- **Sinclair**: Indomitable +0.21 (+0.40), Spellbreaker +0.11 (+0.25), Debuff Reducer +0.07 (+0.13)
- **Mina**: Spirit Resilience +0.24 (+0.35), Dispel Magic +0.21 (+0.28), Reactive Barrier +0.17 (+0.22)
- **Drifter**: Dispel Magic +0.11 (+0.18), Healbane +0.05 (+0.14), Return Fire +0.05 (+0.11)
- **Venator**: Metal Skin +0.26 (+0.35), Indomitable +0.21 (+0.40), Reactive Barrier +0.18 (+0.23)
- **Victor**: Spellbreaker +0.11 (+0.25), Spirit Resilience +0.11 (+0.22), Healbane +0.06 (+0.15)
- **Paige**: Indomitable +0.03 (+0.22), Unstoppable +0.03 (+0.17), Return Fire +0.02 (+0.08)
- **The Doorman**: Indomitable +0.40 (+0.59), Reactive Barrier +0.02 (+0.07), Witchmail +0.02 (+0.16)
- **Billy**: Healbane +0.05 (+0.13), Counterspell +0.02 (+0.06), Witchmail -0.01 (+0.14)
- **Graves**: Return Fire +0.03 (+0.09), Witchmail +0.00 (+0.15), Counterspell -0.00 (+0.04)
- **Apollo**: Spirit Resilience +0.02 (+0.14), Divine Barrier +0.02 (+0.08), Counterspell +0.01 (+0.05)
- **Deadman Danny**: Spirit Resilience +0.04 (+0.15), Spellbreaker +0.03 (+0.17), Witchmail +0.02 (+0.16)
- **Rem**: Unstoppable +0.36 (+0.50), Indomitable +0.31 (+0.50), Debuff Reducer +0.08 (+0.14)
- **Silver**: Healbane +0.02 (+0.11), Dispel Magic +0.02 (+0.09), Debuff Reducer +0.01 (+0.07)
- **Celeste**: Spirit Resilience +0.05 (+0.17), Witchmail +0.02 (+0.17), Healbane +0.02 (+0.10)
- **Rat King**: Return Fire +0.06 (+0.12), Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.06)
- **Solomon**: Debuff Reducer +0.03 (+0.09), Reactive Barrier +0.02 (+0.08), Return Fire +0.02 (+0.08)
- **Violet**: Unstoppable +0.03 (+0.17), Dispel Magic +0.01 (+0.08), Spirit Resilience -0.00 (+0.11)
- **Nurse Harrow**: Dispel Magic +0.00 (+0.07), Healbane -0.03 (+0.05), Counterspell -0.03 (+0.01)
- **Baba**: Unstoppable +0.09 (+0.23), Healbane -0.01 (+0.08), Counterspell -0.02 (+0.03)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.202 | +0.063 | +0.109 | Paradox +0.34, Mina +0.22, Grey Talon +0.11 | 13 heroes |
| Indomitable | 6,400 | +0.233 | +0.038 | +0.180 | Holliday +0.47, The Doorman +0.46, Vyper +0.26 | 0 heroes |
| Dispel Magic | 3,200 | +0.115 | +0.036 | +0.058 | Mina +0.21, Paradox +0.20, Mirage +0.15 | 9 heroes |
| Divine Barrier | 6,400 | +0.205 | +0.033 | +0.057 | Vindicta +0.23, Paradox +0.17, Mina +0.16 | 2 heroes |
| Witchmail | 6,400 | +0.188 | +0.029 | +0.143 | Paradox +0.21, Mina +0.19, Seven +0.12 | 1 heroes |
| Debuff Reducer | 1,600 | +0.045 | +0.028 | +0.055 | Holliday +0.20, Lash +0.11, Rem +0.09 | 0 heroes |
| Spellbreaker | 6,400 | +0.166 | +0.026 | +0.134 | Paradox +0.26, Holliday +0.26, Mo & Krill +0.22 | 0 heroes |
| Reactive Barrier | 1,600 | +0.038 | +0.024 | +0.052 | Mina +0.19, Venator +0.12, Paradox +0.09 | 5 heroes |
| Plated Armor | 6,400 | +0.024 | +0.004 | +0.110 | Haze +0.32, Holliday +0.29, Vindicta +0.19 | 0 heroes |
| Unstoppable | 6,400 | +0.022 | +0.004 | +0.151 | Rem +0.45, Venator +0.21, Haze +0.19 | 3 heroes |
| Healbane | 1,600 | +0.005 | +0.003 | +0.071 | Infernus +0.10, Victor +0.08, Haze +0.06 | 16 heroes |
| Bullet Resilience | 3,200 | -0.002 | -0.001 | +0.063 | Haze +0.17, Vindicta +0.17, Paradox +0.11 | 1 heroes |
| Counterspell | 3,200 | -0.019 | -0.006 | +0.033 | Paradox +0.05, Billy +0.03, Vyper +0.02 | 1 heroes |
| Metal Skin | 3,200 | -0.117 | -0.037 | +0.087 | Paradox +0.22, Haze +0.15, Mina +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.147 | -0.092 | +0.050 | Venator +0.10, Paradox +0.09, Vindicta +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.17), Healbane +0.10 (+0.17), Witchmail +0.08 (+0.22)
- **Seven**: Witchmail +0.12 (+0.26), Spirit Resilience +0.10 (+0.21), Unstoppable +0.09 (+0.24)
- **Vindicta**: Divine Barrier +0.23 (+0.29), Plated Armor +0.19 (+0.30), Bullet Resilience +0.17 (+0.23)
- **Lady Geist**: Spirit Resilience +0.05 (+0.16), Return Fire +0.04 (+0.09), Healbane +0.02 (+0.09)
- **Abrams**: Unstoppable +0.11 (+0.26), Divine Barrier +0.01 (+0.06), Spirit Resilience +0.00 (+0.11)
- **Wraith**: Indomitable +0.23 (+0.41), Metal Skin +0.10 (+0.19), Witchmail +0.10 (+0.24)
- **McGinnis**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.02), Witchmail -0.03 (+0.11)
- **Paradox**: Spirit Resilience +0.34 (+0.45), Spellbreaker +0.26 (+0.40), Indomitable +0.26 (+0.44)
- **Dynamo**: Indomitable +0.17 (+0.35), Debuff Reducer +0.08 (+0.13), Spellbreaker -0.00 (+0.13)
- **Kelvin**: Healbane +0.01 (+0.08), Counterspell +0.00 (+0.03), Return Fire -0.02 (+0.03)
- **Haze**: Plated Armor +0.32 (+0.43), Unstoppable +0.19 (+0.34), Indomitable +0.19 (+0.37)
- **Holliday**: Indomitable +0.47 (+0.65), Plated Armor +0.29 (+0.40), Spellbreaker +0.26 (+0.40)
- **Bebop**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.03), Return Fire -0.02 (+0.03)
- **Calico**: Divine Barrier -0.01 (+0.05), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.05)
- **Grey Talon**: Spellbreaker +0.16 (+0.29), Spirit Resilience +0.11 (+0.22), Indomitable +0.08 (+0.26)
- **Mo & Krill**: Spellbreaker +0.22 (+0.36), Unstoppable +0.09 (+0.24), Spirit Resilience +0.08 (+0.19)
- **Shiv**: Metal Skin +0.09 (+0.18), Divine Barrier +0.06 (+0.12), Bullet Resilience +0.06 (+0.12)
- **Ivy**: Healbane +0.04 (+0.11), Unstoppable +0.03 (+0.18), Dispel Magic -0.01 (+0.05)
- **Warden**: Dispel Magic +0.07 (+0.13), Healbane +0.00 (+0.08), Counterspell -0.01 (+0.02)
- **Yamato**: Healbane +0.02 (+0.09), Counterspell -0.02 (+0.01), Debuff Reducer -0.04 (+0.01)
- **Lash**: Indomitable +0.17 (+0.35), Spellbreaker +0.13 (+0.27), Debuff Reducer +0.11 (+0.17)
- **Viscous**: Divine Barrier +0.00 (+0.06), Counterspell +0.00 (+0.04), Reactive Barrier +0.00 (+0.05)
- **Pocket**: Counterspell +0.01 (+0.05), Spirit Resilience -0.01 (+0.10), Return Fire -0.01 (+0.04)
- **Mirage**: Dispel Magic +0.15 (+0.21), Spellbreaker +0.04 (+0.17), Metal Skin +0.00 (+0.09)
- **Vyper**: Indomitable +0.26 (+0.44), Debuff Reducer +0.07 (+0.12), Spellbreaker +0.05 (+0.18)
- **Sinclair**: Indomitable +0.21 (+0.39), Spellbreaker +0.08 (+0.22), Debuff Reducer +0.08 (+0.13)
- **Mina**: Spirit Resilience +0.22 (+0.33), Dispel Magic +0.21 (+0.27), Reactive Barrier +0.19 (+0.24)
- **Drifter**: Dispel Magic +0.07 (+0.12), Return Fire +0.02 (+0.07), Healbane +0.01 (+0.08)
- **Venator**: Unstoppable +0.21 (+0.36), Reactive Barrier +0.12 (+0.17), Indomitable +0.11 (+0.29)
- **Victor**: Healbane +0.08 (+0.16), Spellbreaker +0.08 (+0.21), Spirit Resilience +0.07 (+0.18)
- **Paige**: Return Fire +0.01 (+0.06), Unstoppable +0.01 (+0.16), Counterspell +0.01 (+0.04)
- **The Doorman**: Indomitable +0.46 (+0.64), Counterspell -0.00 (+0.03), Return Fire -0.01 (+0.04)
- **Billy**: Counterspell +0.03 (+0.06), Reactive Barrier +0.02 (+0.07), Healbane +0.01 (+0.08)
- **Graves**: Return Fire +0.02 (+0.07), Metal Skin -0.02 (+0.07), Counterspell -0.02 (+0.01)
- **Apollo**: Counterspell -0.02 (+0.02), Healbane -0.02 (+0.05), Divine Barrier -0.02 (+0.03)
- **Deadman Danny**: Spellbreaker +0.04 (+0.18), Spirit Resilience +0.04 (+0.15), Dispel Magic +0.01 (+0.07)
- **Rem**: Unstoppable +0.45 (+0.60), Debuff Reducer +0.09 (+0.14), Spellbreaker +0.01 (+0.15)
- **Silver**: Dispel Magic +0.05 (+0.10), Divine Barrier +0.02 (+0.07), Reactive Barrier -0.01 (+0.04)
- **Celeste**: Spirit Resilience +0.05 (+0.16), Healbane +0.02 (+0.09), Dispel Magic -0.01 (+0.05)
- **Rat King**: Return Fire +0.03 (+0.08), Counterspell -0.00 (+0.03), Metal Skin -0.01 (+0.08)
- **Solomon**: Debuff Reducer +0.04 (+0.10), Spellbreaker +0.02 (+0.16), Reactive Barrier +0.00 (+0.06)
- **Violet**: Dispel Magic +0.05 (+0.11), Unstoppable +0.04 (+0.19), Spirit Resilience +0.03 (+0.14)
- **Nurse Harrow**: Dispel Magic +0.02 (+0.08), Healbane -0.02 (+0.05), Counterspell -0.02 (+0.01)
- **Baba**: Unstoppable +0.10 (+0.25), Counterspell -0.01 (+0.03), Debuff Reducer -0.01 (+0.05)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.246 | +0.077 | +0.136 | Paradox +0.28, Sinclair +0.16, Violet +0.13 | 14 heroes |
| Indomitable | 6,400 | +0.290 | +0.046 | +0.231 | The Doorman +0.81, Wraith +0.50, Holliday +0.38 | 1 heroes |
| Dispel Magic | 3,200 | +0.115 | +0.036 | +0.060 | Drifter +0.17, The Doorman +0.15, Mirage +0.12 | 9 heroes |
| Debuff Reducer | 1,600 | +0.056 | +0.035 | +0.073 | Holliday +0.18, Lash +0.16, Wraith +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.210 | +0.033 | +0.170 | Holliday +0.22, Mo & Krill +0.21, Paradox +0.19 | 0 heroes |
| Witchmail | 6,400 | +0.179 | +0.028 | +0.136 | Paradox +0.25, Victor +0.14, The Doorman +0.14 | 2 heroes |
| Divine Barrier | 6,400 | +0.177 | +0.028 | +0.054 | Vindicta +0.16, The Doorman +0.12, Violet +0.09 | 3 heroes |
| Unstoppable | 6,400 | +0.104 | +0.016 | +0.241 | Paige +0.60, Rem +0.38, Paradox +0.33 | 8 heroes |
| Reactive Barrier | 1,600 | +0.018 | +0.011 | +0.054 | The Doorman +0.12, Paradox +0.09, Venator +0.09 | 3 heroes |
| Healbane | 1,600 | +0.016 | +0.010 | +0.078 | Victor +0.21, Vindicta +0.09, Infernus +0.07 | 13 heroes |
| Plated Armor | 6,400 | +0.024 | +0.004 | +0.118 | Vindicta +0.31, Haze +0.18, Wraith +0.11 | 2 heroes |
| Bullet Resilience | 3,200 | -0.008 | -0.002 | +0.068 | Haze +0.15, Vindicta +0.12, Venator +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.029 | -0.009 | +0.028 | Kelvin +0.05, Seven +0.03, Shiv +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.110 | -0.034 | +0.099 | Wraith +0.15, Seven +0.14, Haze +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.156 | -0.098 | +0.042 | Venator +0.11, Solomon +0.07, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.39), Dispel Magic +0.11 (+0.17), Spirit Resilience +0.09 (+0.22)
- **Seven**: Unstoppable +0.21 (+0.46), Indomitable +0.19 (+0.42), Metal Skin +0.14 (+0.24)
- **Vindicta**: Plated Armor +0.31 (+0.43), Divine Barrier +0.16 (+0.21), Spellbreaker +0.14 (+0.31)
- **Lady Geist**: Healbane +0.02 (+0.10), Bullet Resilience -0.01 (+0.06), Dispel Magic -0.01 (+0.05)
- **Abrams**: Unstoppable +0.13 (+0.37), Spirit Resilience +0.02 (+0.16), Divine Barrier +0.02 (+0.07)
- **Wraith**: Indomitable +0.50 (+0.73), Debuff Reducer +0.16 (+0.23), Unstoppable +0.15 (+0.39)
- **McGinnis**: Spirit Resilience +0.06 (+0.20), Witchmail +0.06 (+0.20), Healbane +0.06 (+0.14)
- **Paradox**: Unstoppable +0.33 (+0.57), Spirit Resilience +0.28 (+0.42), Witchmail +0.25 (+0.38)
- **Dynamo**: Indomitable +0.17 (+0.41), Debuff Reducer +0.09 (+0.16), Healbane +0.01 (+0.09)
- **Kelvin**: Counterspell +0.05 (+0.07), Witchmail +0.04 (+0.18), Spirit Resilience +0.04 (+0.17)
- **Haze**: Plated Armor +0.18 (+0.30), Bullet Resilience +0.15 (+0.22), Metal Skin +0.12 (+0.22)
- **Holliday**: Indomitable +0.38 (+0.61), Spellbreaker +0.22 (+0.39), Debuff Reducer +0.18 (+0.26)
- **Bebop**: Spellbreaker +0.03 (+0.20), Debuff Reducer +0.02 (+0.09), Healbane +0.02 (+0.10)
- **Calico**: Spirit Resilience +0.02 (+0.16), Divine Barrier +0.02 (+0.08), Counterspell -0.00 (+0.02)
- **Grey Talon**: Spirit Resilience +0.09 (+0.23), Spellbreaker +0.07 (+0.24), Witchmail +0.03 (+0.16)
- **Mo & Krill**: Spellbreaker +0.21 (+0.38), Healbane +0.06 (+0.14), Unstoppable +0.04 (+0.28)
- **Shiv**: Metal Skin +0.07 (+0.17), Bullet Resilience +0.06 (+0.13), Divine Barrier +0.06 (+0.11)
- **Ivy**: Healbane -0.01 (+0.07), Bullet Resilience -0.01 (+0.05), Return Fire -0.01 (+0.03)
- **Warden**: Dispel Magic -0.00 (+0.06), Healbane -0.01 (+0.07), Counterspell -0.02 (+0.01)
- **Yamato**: Healbane +0.03 (+0.11), Counterspell -0.01 (+0.02), Return Fire -0.03 (+0.01)
- **Lash**: Indomitable +0.23 (+0.46), Spellbreaker +0.17 (+0.34), Debuff Reducer +0.16 (+0.23)
- **Viscous**: Spirit Resilience +0.09 (+0.22), Divine Barrier +0.02 (+0.08), Reactive Barrier +0.01 (+0.06)
- **Pocket**: Counterspell -0.01 (+0.02), Return Fire -0.02 (+0.03), Spirit Resilience -0.02 (+0.11)
- **Mirage**: Dispel Magic +0.12 (+0.18), Metal Skin +0.02 (+0.12), Counterspell -0.00 (+0.03)
- **Vyper**: Indomitable +0.20 (+0.43), Debuff Reducer +0.04 (+0.11), Plated Armor +0.03 (+0.15)
- **Sinclair**: Indomitable +0.34 (+0.57), Spellbreaker +0.18 (+0.35), Spirit Resilience +0.16 (+0.30)
- **Mina**: Spirit Resilience +0.07 (+0.20), Divine Barrier +0.06 (+0.12), Reactive Barrier +0.05 (+0.10)
- **Drifter**: Dispel Magic +0.17 (+0.23), Witchmail +0.07 (+0.20), Unstoppable +0.06 (+0.30)
- **Venator**: Unstoppable +0.21 (+0.45), Return Fire +0.11 (+0.15), Metal Skin +0.10 (+0.20)
- **Victor**: Healbane +0.21 (+0.29), Spellbreaker +0.17 (+0.34), Witchmail +0.14 (+0.28)
- **Paige**: Unstoppable +0.60 (+0.84), Debuff Reducer +0.08 (+0.15), Indomitable +0.06 (+0.29)
- **The Doorman**: Indomitable +0.81 (+1.05), Dispel Magic +0.15 (+0.21), Witchmail +0.14 (+0.27)
- **Billy**: Reactive Barrier +0.01 (+0.07), Healbane +0.01 (+0.09), Counterspell -0.00 (+0.02)
- **Graves**: Return Fire +0.04 (+0.09), Counterspell -0.01 (+0.02), Metal Skin -0.02 (+0.08)
- **Apollo**: Spirit Resilience +0.01 (+0.14), Counterspell -0.00 (+0.02), Healbane -0.02 (+0.06)
- **Deadman Danny**: Spirit Resilience +0.05 (+0.19), Spellbreaker +0.02 (+0.19), Healbane -0.01 (+0.07)
- **Rem**: Unstoppable +0.38 (+0.62), Debuff Reducer +0.00 (+0.07), Counterspell -0.01 (+0.02)
- **Silver**: Dispel Magic +0.06 (+0.12), Divine Barrier -0.01 (+0.04), Reactive Barrier -0.01 (+0.04)
- **Celeste**: Spirit Resilience +0.03 (+0.17), Witchmail +0.02 (+0.15), Counterspell +0.01 (+0.04)
- **Rat King**: Return Fire +0.05 (+0.09), Counterspell +0.01 (+0.04), Healbane +0.01 (+0.09)
- **Solomon**: Spirit Resilience +0.10 (+0.24), Witchmail +0.09 (+0.22), Reactive Barrier +0.08 (+0.14)
- **Violet**: Unstoppable +0.14 (+0.38), Spirit Resilience +0.13 (+0.27), Divine Barrier +0.09 (+0.15)
- **Nurse Harrow**: Healbane -0.01 (+0.07), Counterspell -0.02 (+0.01), Dispel Magic -0.02 (+0.04)
- **Baba**: Unstoppable +0.21 (+0.45), Healbane +0.02 (+0.10), Counterspell +0.01 (+0.04)
