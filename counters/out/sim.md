# Counter items in the sim (phantom and up)

Built 2026-10-25T21:56:56Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.235 | +0.073 | +0.126 | Lash +0.24, Wraith +0.16, Drifter +0.12 | 1 heroes |
| Divine Barrier | 6,400 | +0.373 | +0.060 | +0.099 | Wraith +0.18, Lash +0.17, Mina +0.09 | 0 heroes |
| Dispel Magic | 3,200 | +0.140 | +0.044 | +0.078 | Mirage +0.34, Infernus +0.11, Lash +0.08 | 4 heroes |
| Debuff Reducer | 1,600 | +0.062 | +0.039 | +0.054 | Wraith +0.12, Vyper +0.06, Grey Talon +0.06 | 0 heroes |
| Witchmail | 6,400 | +0.219 | +0.034 | +0.186 | Wraith +0.16, Lash +0.12, Deadman Danny +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | +0.053 | +0.034 | +0.051 | Wraith +0.16, Violet +0.08, Paradox +0.07 | 2 heroes |
| Indomitable | 6,400 | +0.197 | +0.031 | +0.146 | The Doorman +0.31, Vyper +0.31, Wraith +0.30 | 0 heroes |
| Spellbreaker | 6,400 | +0.152 | +0.024 | +0.149 | Lash +0.23, Wraith +0.19, Deadman Danny +0.14 | 0 heroes |
| Healbane | 1,600 | +0.037 | +0.023 | +0.081 | Billy +0.07, Infernus +0.06, Nurse Harrow +0.05 | 11 heroes |
| Bullet Resilience | 3,200 | +0.042 | +0.013 | +0.090 | Wraith +0.13, Venator +0.10, Paradox +0.10 | 0 heroes |
| Counterspell | 3,200 | +0.016 | +0.005 | +0.067 | Wraith +0.08, Billy +0.06, Vyper +0.05 | 1 heroes |
| Plated Armor | 6,400 | +0.025 | +0.004 | +0.127 | Holliday +0.23, Wraith +0.19, Haze +0.12 | 0 heroes |
| Unstoppable | 6,400 | +0.007 | +0.001 | +0.121 | Wraith +0.14, Ivy +0.10, Rem +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.092 | -0.029 | +0.111 | Wraith +0.26, Drifter +0.14, Lash +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.138 | -0.086 | +0.063 | Wraith +0.08, Lady Geist +0.05, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.19), Unstoppable +0.07 (+0.19), Spirit Resilience +0.06 (+0.19)
- **Seven**: Healbane -0.01 (+0.07), Counterspell -0.02 (+0.05), Witchmail -0.03 (+0.16)
- **Vindicta**: Divine Barrier +0.05 (+0.15), Return Fire +0.05 (+0.11), Bullet Resilience +0.04 (+0.13)
- **Lady Geist**: Return Fire +0.05 (+0.12), Divine Barrier +0.03 (+0.13), Witchmail +0.03 (+0.21)
- **Abrams**: Indomitable +0.16 (+0.30), Unstoppable +0.06 (+0.18), Divine Barrier +0.04 (+0.13)
- **Wraith**: Indomitable +0.30 (+0.45), Metal Skin +0.26 (+0.37), Spellbreaker +0.19 (+0.34)
- **McGinnis**: Spirit Resilience +0.05 (+0.17), Return Fire -0.00 (+0.06), Healbane -0.01 (+0.08)
- **Paradox**: Metal Skin +0.12 (+0.23), Bullet Resilience +0.10 (+0.19), Plated Armor +0.09 (+0.22)
- **Dynamo**: Healbane +0.02 (+0.10), Counterspell -0.02 (+0.05), Return Fire -0.04 (+0.03)
- **Kelvin**: Healbane +0.00 (+0.08), Counterspell -0.01 (+0.06), Debuff Reducer -0.01 (+0.04)
- **Haze**: Plated Armor +0.12 (+0.25), Indomitable +0.09 (+0.24), Bullet Resilience +0.07 (+0.16)
- **Holliday**: Plated Armor +0.23 (+0.36), Spellbreaker +0.04 (+0.19), Debuff Reducer +0.04 (+0.10)
- **Bebop**: Witchmail +0.05 (+0.24), Bullet Resilience +0.05 (+0.13), Divine Barrier +0.05 (+0.14)
- **Calico**: Divine Barrier +0.03 (+0.13), Spellbreaker +0.02 (+0.17), Debuff Reducer +0.01 (+0.07)
- **Grey Talon**: Indomitable +0.08 (+0.23), Reactive Barrier +0.07 (+0.12), Spellbreaker +0.06 (+0.21)
- **Mo & Krill**: Spellbreaker +0.11 (+0.26), Spirit Resilience +0.07 (+0.19), Dispel Magic +0.05 (+0.13)
- **Shiv**: Healbane -0.01 (+0.07), Return Fire -0.02 (+0.05), Spirit Resilience -0.04 (+0.09)
- **Ivy**: Unstoppable +0.10 (+0.22), Indomitable +0.06 (+0.21), Debuff Reducer +0.01 (+0.07)
- **Warden**: Return Fire +0.04 (+0.11), Counterspell +0.02 (+0.08), Bullet Resilience +0.01 (+0.10)
- **Yamato**: Healbane +0.03 (+0.11), Debuff Reducer -0.04 (+0.02), Counterspell -0.04 (+0.03)
- **Lash**: Spirit Resilience +0.24 (+0.36), Spellbreaker +0.23 (+0.38), Divine Barrier +0.17 (+0.27)
- **Viscous**: Return Fire +0.00 (+0.06), Counterspell -0.00 (+0.07), Healbane -0.00 (+0.08)
- **Pocket**: Witchmail +0.04 (+0.22), Return Fire +0.04 (+0.10), Spirit Resilience +0.03 (+0.15)
- **Mirage**: Dispel Magic +0.34 (+0.42), Spellbreaker +0.08 (+0.23), Healbane -0.01 (+0.07)
- **Vyper**: Indomitable +0.31 (+0.46), Spellbreaker +0.11 (+0.26), Debuff Reducer +0.06 (+0.12)
- **Sinclair**: Spellbreaker +0.05 (+0.19), Indomitable +0.04 (+0.19), Return Fire +0.04 (+0.10)
- **Mina**: Divine Barrier +0.09 (+0.19), Spirit Resilience +0.08 (+0.21), Spellbreaker +0.07 (+0.22)
- **Drifter**: Metal Skin +0.14 (+0.25), Spirit Resilience +0.12 (+0.25), Witchmail +0.10 (+0.29)
- **Venator**: Bullet Resilience +0.10 (+0.19), Metal Skin +0.05 (+0.16), Plated Armor +0.04 (+0.17)
- **Victor**: Healbane +0.00 (+0.08), Debuff Reducer -0.03 (+0.02), Reactive Barrier -0.04 (+0.02)
- **Paige**: Healbane +0.01 (+0.09), Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.06)
- **The Doorman**: Indomitable +0.31 (+0.46), Reactive Barrier -0.01 (+0.04), Return Fire -0.02 (+0.04)
- **Billy**: Healbane +0.07 (+0.15), Counterspell +0.06 (+0.13), Debuff Reducer +0.05 (+0.11)
- **Graves**: Metal Skin +0.10 (+0.21), Witchmail +0.10 (+0.28), Spirit Resilience +0.10 (+0.22)
- **Apollo**: Spirit Resilience +0.01 (+0.14), Spellbreaker -0.02 (+0.13), Divine Barrier -0.03 (+0.07)
- **Deadman Danny**: Spellbreaker +0.14 (+0.28), Indomitable +0.13 (+0.28), Witchmail +0.11 (+0.30)
- **Rem**: Unstoppable +0.10 (+0.22), Indomitable +0.08 (+0.23), Healbane -0.01 (+0.07)
- **Silver**: Dispel Magic +0.07 (+0.14), Metal Skin -0.00 (+0.11), Reactive Barrier -0.01 (+0.04)
- **Celeste**: Spirit Resilience +0.10 (+0.22), Witchmail +0.07 (+0.26), Plated Armor +0.04 (+0.16)
- **Rat King**: Return Fire +0.01 (+0.08), Counterspell +0.01 (+0.08), Bullet Resilience -0.01 (+0.08)
- **Solomon**: Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.06), Healbane -0.02 (+0.06)
- **Violet**: Unstoppable +0.08 (+0.21), Reactive Barrier +0.08 (+0.13), Spirit Resilience +0.07 (+0.19)
- **Nurse Harrow**: Healbane +0.05 (+0.13), Counterspell -0.01 (+0.06), Return Fire -0.02 (+0.04)
- **Baba**: Healbane +0.02 (+0.10), Counterspell -0.01 (+0.05), Return Fire -0.01 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.218 | +0.068 | +0.117 | Lash +0.24, Pocket +0.20, Graves +0.15 | 10 heroes |
| Dispel Magic | 3,200 | +0.128 | +0.040 | +0.068 | Mirage +0.29, Lash +0.11, Paradox +0.09 | 7 heroes |
| Divine Barrier | 6,400 | +0.245 | +0.039 | +0.080 | Vindicta +0.24, Lash +0.15, Mina +0.10 | 1 heroes |
| Witchmail | 6,400 | +0.215 | +0.034 | +0.165 | Graves +0.17, Lash +0.15, Pocket +0.12 | 0 heroes |
| Indomitable | 6,400 | +0.175 | +0.028 | +0.129 | Vyper +0.41, The Doorman +0.33, Wraith +0.22 | 0 heroes |
| Debuff Reducer | 1,600 | +0.039 | +0.025 | +0.046 | Wraith +0.08, Vyper +0.05, Pocket +0.05 | 1 heroes |
| Spellbreaker | 6,400 | +0.151 | +0.024 | +0.124 | Lash +0.20, Pocket +0.11, Wraith +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | +0.038 | +0.024 | +0.043 | Wraith +0.11, Vyper +0.07, Paradox +0.07 | 4 heroes |
| Healbane | 1,600 | +0.017 | +0.010 | +0.078 | Lash +0.09, Haze +0.06, Pocket +0.04 | 17 heroes |
| Bullet Resilience | 3,200 | +0.024 | +0.007 | +0.076 | Vindicta +0.24, Paradox +0.14, Haze +0.10 | 0 heroes |
| Plated Armor | 6,400 | +0.027 | +0.004 | +0.113 | Vindicta +0.22, Holliday +0.16, Haze +0.15 | 0 heroes |
| Counterspell | 3,200 | -0.007 | -0.002 | +0.045 | Lash +0.06, Deadman Danny +0.06, Pocket +0.05 | 1 heroes |
| Unstoppable | 6,400 | -0.018 | -0.003 | +0.102 | Abrams +0.17, Ivy +0.14, Rem +0.14 | 0 heroes |
| Metal Skin | 3,200 | -0.106 | -0.033 | +0.098 | Wraith +0.20, Paradox +0.19, Lash +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.145 | -0.091 | +0.056 | Wraith +0.07, Vindicta +0.06, Paradox +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.16), Unstoppable +0.04 (+0.14), Healbane +0.03 (+0.10)
- **Seven**: Witchmail +0.03 (+0.19), Counterspell +0.00 (+0.05), Healbane +0.00 (+0.08)
- **Vindicta**: Divine Barrier +0.24 (+0.32), Bullet Resilience +0.24 (+0.32), Plated Armor +0.22 (+0.33)
- **Lady Geist**: Return Fire +0.06 (+0.12), Divine Barrier +0.05 (+0.13), Metal Skin +0.04 (+0.13)
- **Abrams**: Unstoppable +0.17 (+0.27), Indomitable +0.05 (+0.18), Dispel Magic +0.04 (+0.11)
- **Wraith**: Indomitable +0.22 (+0.35), Metal Skin +0.20 (+0.30), Reactive Barrier +0.11 (+0.15)
- **McGinnis**: Healbane +0.00 (+0.08), Counterspell -0.01 (+0.04), Return Fire -0.02 (+0.04)
- **Paradox**: Metal Skin +0.19 (+0.28), Bullet Resilience +0.14 (+0.22), Plated Armor +0.14 (+0.25)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.01 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.02 (+0.13), Dispel Magic -0.00 (+0.06), Healbane -0.01 (+0.07)
- **Haze**: Plated Armor +0.15 (+0.26), Bullet Resilience +0.10 (+0.18), Indomitable +0.10 (+0.23)
- **Holliday**: Plated Armor +0.16 (+0.27), Indomitable +0.05 (+0.17), Spellbreaker +0.04 (+0.16)
- **Bebop**: Witchmail +0.07 (+0.23), Counterspell +0.04 (+0.08), Plated Armor +0.04 (+0.15)
- **Calico**: Reactive Barrier +0.03 (+0.07), Divine Barrier -0.01 (+0.07), Spirit Resilience -0.01 (+0.11)
- **Grey Talon**: Reactive Barrier +0.03 (+0.07), Indomitable +0.03 (+0.15), Debuff Reducer +0.03 (+0.07)
- **Mo & Krill**: Unstoppable +0.08 (+0.19), Spellbreaker +0.05 (+0.17), Debuff Reducer +0.03 (+0.07)
- **Shiv**: Bullet Resilience +0.01 (+0.09), Divine Barrier +0.01 (+0.09), Plated Armor +0.01 (+0.12)
- **Ivy**: Unstoppable +0.14 (+0.24), Indomitable +0.04 (+0.17), Debuff Reducer +0.00 (+0.05)
- **Warden**: Return Fire +0.02 (+0.08), Counterspell -0.00 (+0.04), Debuff Reducer -0.02 (+0.03)
- **Yamato**: Healbane +0.03 (+0.11), Debuff Reducer -0.03 (+0.02), Counterspell -0.04 (+0.00)
- **Lash**: Spirit Resilience +0.24 (+0.36), Spellbreaker +0.20 (+0.32), Divine Barrier +0.15 (+0.23)
- **Viscous**: Return Fire -0.01 (+0.05), Counterspell -0.02 (+0.03), Healbane -0.02 (+0.05)
- **Pocket**: Spirit Resilience +0.20 (+0.31), Witchmail +0.12 (+0.28), Spellbreaker +0.11 (+0.24)
- **Mirage**: Dispel Magic +0.29 (+0.36), Spellbreaker +0.03 (+0.16), Metal Skin +0.03 (+0.13)
- **Vyper**: Indomitable +0.41 (+0.54), Metal Skin +0.13 (+0.23), Spellbreaker +0.10 (+0.22)
- **Sinclair**: Indomitable +0.10 (+0.23), Spellbreaker +0.04 (+0.17), Return Fire +0.01 (+0.07)
- **Mina**: Spirit Resilience +0.14 (+0.26), Witchmail +0.11 (+0.27), Divine Barrier +0.10 (+0.18)
- **Drifter**: Witchmail +0.10 (+0.26), Metal Skin +0.08 (+0.18), Spirit Resilience +0.08 (+0.20)
- **Venator**: Bullet Resilience +0.09 (+0.17), Metal Skin +0.04 (+0.14), Plated Armor +0.04 (+0.15)
- **Victor**: Spellbreaker +0.08 (+0.20), Spirit Resilience +0.05 (+0.17), Healbane +0.01 (+0.09)
- **Paige**: Return Fire +0.00 (+0.06), Counterspell +0.00 (+0.05), Healbane -0.02 (+0.06)
- **The Doorman**: Indomitable +0.33 (+0.46), Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Billy**: Spirit Resilience +0.02 (+0.14), Spellbreaker -0.01 (+0.12), Return Fire -0.01 (+0.04)
- **Graves**: Witchmail +0.17 (+0.33), Spirit Resilience +0.15 (+0.27), Metal Skin +0.12 (+0.22)
- **Apollo**: Spellbreaker +0.05 (+0.18), Divine Barrier +0.03 (+0.11), Witchmail +0.02 (+0.19)
- **Deadman Danny**: Spellbreaker +0.11 (+0.23), Witchmail +0.10 (+0.27), Indomitable +0.09 (+0.22)
- **Rem**: Unstoppable +0.14 (+0.24), Indomitable +0.12 (+0.24), Counterspell -0.01 (+0.03)
- **Silver**: Dispel Magic +0.07 (+0.14), Metal Skin +0.00 (+0.10), Healbane -0.02 (+0.06)
- **Celeste**: Witchmail +0.08 (+0.24), Spirit Resilience +0.07 (+0.19), Spellbreaker +0.04 (+0.16)
- **Rat King**: Return Fire -0.01 (+0.04), Counterspell -0.02 (+0.03), Bullet Resilience -0.02 (+0.06)
- **Solomon**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.02)
- **Violet**: Unstoppable +0.10 (+0.20), Dispel Magic +0.06 (+0.13), Indomitable +0.05 (+0.18)
- **Nurse Harrow**: Healbane +0.00 (+0.08), Spirit Resilience +0.00 (+0.12), Counterspell -0.01 (+0.03)
- **Baba**: Unstoppable +0.00 (+0.11), Healbane +0.00 (+0.08), Counterspell -0.01 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.200 | +0.063 | +0.108 | Lash +0.16, Grey Talon +0.16, Mina +0.14 | 13 heroes |
| Divine Barrier | 6,400 | +0.265 | +0.042 | +0.059 | Vindicta +0.21, Paradox +0.13, Wraith +0.10 | 2 heroes |
| Dispel Magic | 3,200 | +0.110 | +0.034 | +0.053 | Mirage +0.24, Violet +0.15, Infernus +0.13 | 9 heroes |
| Witchmail | 6,400 | +0.199 | +0.031 | +0.154 | Wraith +0.12, Lash +0.11, Paradox +0.10 | 1 heroes |
| Indomitable | 6,400 | +0.176 | +0.028 | +0.126 | Vyper +0.42, The Doorman +0.34, Wraith +0.26 | 0 heroes |
| Spellbreaker | 6,400 | +0.151 | +0.024 | +0.120 | Grey Talon +0.19, Paradox +0.15, Wraith +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.026 | +0.016 | +0.035 | Grey Talon +0.11, Wraith +0.06, Holliday +0.06 | 0 heroes |
| Reactive Barrier | 1,600 | +0.024 | +0.015 | +0.037 | Wraith +0.13, Violet +0.11, Paradox +0.10 | 5 heroes |
| Plated Armor | 6,400 | +0.018 | +0.003 | +0.103 | Vindicta +0.21, Holliday +0.19, Wraith +0.15 | 0 heroes |
| Bullet Resilience | 3,200 | -0.004 | -0.001 | +0.061 | Vindicta +0.22, Paradox +0.14, Wraith +0.06 | 1 heroes |
| Healbane | 1,600 | -0.006 | -0.004 | +0.059 | Viscous +0.06, Yamato +0.05, Infernus +0.05 | 16 heroes |
| Unstoppable | 6,400 | -0.027 | -0.004 | +0.096 | Rem +0.23, Violet +0.22, Ivy +0.18 | 3 heroes |
| Counterspell | 3,200 | -0.023 | -0.007 | +0.029 | Vyper +0.05, Paradox +0.03, Lash +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.111 | -0.035 | +0.094 | Wraith +0.22, Paradox +0.18, Mirage +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.151 | -0.094 | +0.045 | Paradox +0.09, Wraith +0.05, Haze +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.14 (+0.23), Dispel Magic +0.13 (+0.18), Spellbreaker +0.13 (+0.25)
- **Seven**: Witchmail +0.06 (+0.21), Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Vindicta**: Bullet Resilience +0.22 (+0.28), Divine Barrier +0.21 (+0.27), Plated Armor +0.21 (+0.31)
- **Lady Geist**: Return Fire +0.03 (+0.08), Divine Barrier +0.02 (+0.08), Bullet Resilience +0.01 (+0.07)
- **Abrams**: Unstoppable +0.10 (+0.20), Dispel Magic +0.04 (+0.09), Healbane +0.04 (+0.09)
- **Wraith**: Indomitable +0.26 (+0.39), Metal Skin +0.22 (+0.32), Plated Armor +0.15 (+0.25)
- **McGinnis**: Healbane -0.01 (+0.05), Counterspell -0.01 (+0.02), Spirit Resilience -0.02 (+0.09)
- **Paradox**: Metal Skin +0.18 (+0.28), Spellbreaker +0.15 (+0.27), Bullet Resilience +0.14 (+0.20)
- **Dynamo**: Healbane +0.03 (+0.09), Counterspell -0.00 (+0.03), Debuff Reducer -0.02 (+0.01)
- **Kelvin**: Counterspell +0.01 (+0.04), Healbane -0.00 (+0.06), Debuff Reducer -0.01 (+0.03)
- **Haze**: Plated Armor +0.12 (+0.22), Indomitable +0.10 (+0.23), Unstoppable +0.09 (+0.18)
- **Holliday**: Plated Armor +0.19 (+0.29), Spellbreaker +0.06 (+0.18), Debuff Reducer +0.06 (+0.10)
- **Bebop**: Healbane +0.02 (+0.08), Metal Skin +0.01 (+0.11), Divine Barrier -0.00 (+0.06)
- **Calico**: Reactive Barrier +0.02 (+0.05), Divine Barrier +0.00 (+0.06), Spellbreaker -0.00 (+0.12)
- **Grey Talon**: Spellbreaker +0.19 (+0.31), Unstoppable +0.16 (+0.26), Spirit Resilience +0.16 (+0.27)
- **Mo & Krill**: Unstoppable +0.09 (+0.19), Spellbreaker +0.05 (+0.17), Dispel Magic +0.03 (+0.08)
- **Shiv**: Metal Skin +0.05 (+0.14), Bullet Resilience +0.04 (+0.10), Plated Armor +0.04 (+0.14)
- **Ivy**: Unstoppable +0.18 (+0.28), Indomitable +0.12 (+0.25), Dispel Magic +0.05 (+0.10)
- **Warden**: Return Fire +0.02 (+0.06), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Yamato**: Healbane +0.05 (+0.11), Debuff Reducer +0.01 (+0.05), Counterspell +0.01 (+0.04)
- **Lash**: Spirit Resilience +0.16 (+0.27), Spellbreaker +0.13 (+0.25), Witchmail +0.11 (+0.26)
- **Viscous**: Healbane +0.06 (+0.12), Return Fire +0.04 (+0.08), Divine Barrier +0.03 (+0.09)
- **Pocket**: Spirit Resilience +0.04 (+0.15), Counterspell +0.01 (+0.04), Return Fire +0.00 (+0.05)
- **Mirage**: Dispel Magic +0.24 (+0.30), Metal Skin +0.14 (+0.24), Spellbreaker +0.04 (+0.16)
- **Vyper**: Indomitable +0.42 (+0.55), Spellbreaker +0.10 (+0.22), Reactive Barrier +0.09 (+0.13)
- **Sinclair**: Indomitable +0.16 (+0.28), Debuff Reducer +0.04 (+0.08), Unstoppable +0.04 (+0.14)
- **Mina**: Spirit Resilience +0.14 (+0.25), Divine Barrier +0.09 (+0.15), Spellbreaker +0.08 (+0.20)
- **Drifter**: Spirit Resilience +0.12 (+0.22), Witchmail +0.06 (+0.21), Metal Skin +0.05 (+0.15)
- **Venator**: Bullet Resilience +0.05 (+0.11), Metal Skin +0.05 (+0.14), Debuff Reducer +0.02 (+0.06)
- **Victor**: Spirit Resilience +0.04 (+0.15), Healbane +0.03 (+0.09), Spellbreaker +0.02 (+0.14)
- **Paige**: Counterspell +0.01 (+0.04), Return Fire -0.00 (+0.05), Witchmail -0.01 (+0.15)
- **The Doorman**: Indomitable +0.34 (+0.47), Counterspell -0.01 (+0.02), Reactive Barrier -0.01 (+0.02)
- **Billy**: Spellbreaker +0.01 (+0.13), Reactive Barrier +0.00 (+0.04), Counterspell -0.00 (+0.03)
- **Graves**: Return Fire +0.02 (+0.06), Witchmail +0.01 (+0.17), Metal Skin +0.01 (+0.10)
- **Apollo**: Spirit Resilience +0.10 (+0.21), Counterspell -0.03 (+0.00), Spellbreaker -0.03 (+0.09)
- **Deadman Danny**: Witchmail +0.10 (+0.25), Indomitable +0.10 (+0.22), Spellbreaker +0.08 (+0.20)
- **Rem**: Unstoppable +0.23 (+0.32), Debuff Reducer -0.01 (+0.03), Counterspell -0.01 (+0.02)
- **Silver**: Dispel Magic +0.09 (+0.15), Metal Skin -0.00 (+0.09), Healbane -0.00 (+0.06)
- **Celeste**: Dispel Magic +0.09 (+0.14), Witchmail +0.06 (+0.22), Healbane +0.03 (+0.09)
- **Rat King**: Return Fire -0.01 (+0.04), Counterspell -0.01 (+0.02), Healbane -0.02 (+0.04)
- **Solomon**: Return Fire +0.01 (+0.05), Counterspell -0.01 (+0.02), Debuff Reducer -0.02 (+0.02)
- **Violet**: Unstoppable +0.22 (+0.31), Dispel Magic +0.15 (+0.20), Indomitable +0.13 (+0.25)
- **Nurse Harrow**: Healbane +0.04 (+0.10), Counterspell +0.00 (+0.03), Debuff Reducer -0.02 (+0.02)
- **Baba**: Healbane -0.00 (+0.06), Counterspell -0.00 (+0.03), Return Fire -0.01 (+0.04)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.233 | +0.073 | +0.124 | Lash +0.38, Deadman Danny +0.26, Grey Talon +0.16 | 14 heroes |
| Dispel Magic | 3,200 | +0.126 | +0.039 | +0.070 | Drifter +0.27, Mirage +0.25, Lash +0.18 | 9 heroes |
| Divine Barrier | 6,400 | +0.201 | +0.031 | +0.055 | Vindicta +0.30, Lash +0.19, Calico +0.11 | 3 heroes |
| Indomitable | 6,400 | +0.188 | +0.030 | +0.133 | The Doorman +0.44, Vyper +0.35, Deadman Danny +0.18 | 1 heroes |
| Witchmail | 6,400 | +0.190 | +0.030 | +0.146 | Lash +0.22, Deadman Danny +0.22, Vindicta +0.18 | 2 heroes |
| Spellbreaker | 6,400 | +0.179 | +0.028 | +0.141 | Lash +0.28, Deadman Danny +0.25, Grey Talon +0.18 | 0 heroes |
| Debuff Reducer | 1,600 | +0.033 | +0.020 | +0.050 | Grey Talon +0.13, Paige +0.08, Bebop +0.07 | 0 heroes |
| Unstoppable | 6,400 | +0.023 | +0.004 | +0.150 | Paige +0.31, Wraith +0.23, Rem +0.20 | 8 heroes |
| Plated Armor | 6,400 | +0.011 | +0.002 | +0.104 | Vindicta +0.40, Deadman Danny +0.16, Vyper +0.14 | 2 heroes |
| Reactive Barrier | 1,600 | -0.002 | -0.001 | +0.034 | Deadman Danny +0.10, Vyper +0.09, Drifter +0.08 | 3 heroes |
| Healbane | 1,600 | -0.003 | -0.002 | +0.058 | Dynamo +0.07, Yamato +0.05, Vindicta +0.04 | 13 heroes |
| Bullet Resilience | 3,200 | -0.015 | -0.005 | +0.059 | Vindicta +0.31, Lash +0.12, Paradox +0.06 | 0 heroes |
| Counterspell | 3,200 | -0.027 | -0.008 | +0.030 | Grey Talon +0.06, Vyper +0.04, Vindicta +0.03 | 1 heroes |
| Metal Skin | 3,200 | -0.108 | -0.034 | +0.100 | Lash +0.24, Mirage +0.21, Vyper +0.18 | 0 heroes |
| Return Fire | 1,600 | -0.157 | -0.098 | +0.041 | Paradox +0.07, Holliday +0.06, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.30), Indomitable +0.05 (+0.18), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.03 (+0.17), Counterspell +0.01 (+0.04), Healbane -0.01 (+0.05)
- **Vindicta**: Plated Armor +0.40 (+0.51), Bullet Resilience +0.31 (+0.37), Divine Barrier +0.30 (+0.35)
- **Lady Geist**: Bullet Resilience +0.05 (+0.11), Healbane +0.02 (+0.08), Metal Skin +0.02 (+0.12)
- **Abrams**: Unstoppable +0.06 (+0.21), Healbane +0.04 (+0.10), Debuff Reducer +0.00 (+0.05)
- **Wraith**: Unstoppable +0.23 (+0.38), Metal Skin +0.15 (+0.26), Indomitable +0.14 (+0.28)
- **McGinnis**: Spirit Resilience +0.02 (+0.14), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Paradox**: Dispel Magic +0.12 (+0.19), Unstoppable +0.12 (+0.27), Metal Skin +0.11 (+0.21)
- **Dynamo**: Healbane +0.07 (+0.13), Return Fire +0.00 (+0.04), Counterspell -0.00 (+0.03)
- **Kelvin**: Spirit Resilience +0.14 (+0.26), Witchmail +0.05 (+0.20), Spellbreaker +0.03 (+0.17)
- **Haze**: Unstoppable +0.18 (+0.33), Indomitable +0.05 (+0.19), Plated Armor +0.04 (+0.15)
- **Holliday**: Spellbreaker +0.07 (+0.21), Debuff Reducer +0.06 (+0.11), Return Fire +0.06 (+0.10)
- **Bebop**: Debuff Reducer +0.07 (+0.12), Spellbreaker +0.07 (+0.21), Indomitable +0.02 (+0.15)
- **Calico**: Spirit Resilience +0.12 (+0.24), Divine Barrier +0.11 (+0.16), Reactive Barrier +0.07 (+0.10)
- **Grey Talon**: Spellbreaker +0.18 (+0.32), Spirit Resilience +0.16 (+0.29), Debuff Reducer +0.13 (+0.18)
- **Mo & Krill**: Unstoppable +0.04 (+0.19), Spellbreaker +0.02 (+0.16), Healbane +0.01 (+0.06)
- **Shiv**: Divine Barrier +0.06 (+0.12), Metal Skin +0.05 (+0.15), Bullet Resilience +0.05 (+0.11)
- **Ivy**: Unstoppable +0.17 (+0.32), Indomitable +0.12 (+0.26), Debuff Reducer +0.05 (+0.10)
- **Warden**: Metal Skin +0.03 (+0.13), Return Fire +0.03 (+0.07), Healbane +0.01 (+0.07)
- **Yamato**: Healbane +0.05 (+0.11), Reactive Barrier +0.01 (+0.05), Indomitable +0.01 (+0.15)
- **Lash**: Spirit Resilience +0.38 (+0.51), Spellbreaker +0.28 (+0.42), Metal Skin +0.24 (+0.34)
- **Viscous**: Witchmail +0.09 (+0.23), Spirit Resilience +0.08 (+0.21), Divine Barrier +0.07 (+0.13)
- **Pocket**: Spirit Resilience +0.07 (+0.19), Witchmail +0.05 (+0.20), Spellbreaker +0.01 (+0.16)
- **Mirage**: Dispel Magic +0.25 (+0.32), Metal Skin +0.21 (+0.31), Spellbreaker +0.00 (+0.14)
- **Vyper**: Indomitable +0.35 (+0.48), Metal Skin +0.18 (+0.28), Plated Armor +0.14 (+0.25)
- **Sinclair**: Indomitable +0.16 (+0.29), Spellbreaker +0.08 (+0.22), Reactive Barrier +0.06 (+0.09)
- **Mina**: Counterspell +0.01 (+0.04), Divine Barrier +0.01 (+0.06), Spirit Resilience +0.00 (+0.13)
- **Drifter**: Dispel Magic +0.27 (+0.34), Reactive Barrier +0.08 (+0.11), Metal Skin +0.06 (+0.16)
- **Venator**: Metal Skin +0.12 (+0.22), Bullet Resilience +0.04 (+0.10), Debuff Reducer +0.00 (+0.05)
- **Victor**: Spellbreaker +0.08 (+0.22), Healbane +0.02 (+0.08), Spirit Resilience +0.02 (+0.14)
- **Paige**: Unstoppable +0.31 (+0.46), Debuff Reducer +0.08 (+0.13), Counterspell +0.00 (+0.03)
- **The Doorman**: Indomitable +0.44 (+0.58), Counterspell +0.00 (+0.03), Return Fire -0.01 (+0.03)
- **Billy**: Spellbreaker -0.01 (+0.14), Reactive Barrier -0.01 (+0.02), Return Fire -0.01 (+0.03)
- **Graves**: Spirit Resilience +0.05 (+0.17), Witchmail +0.03 (+0.18), Return Fire +0.02 (+0.07)
- **Apollo**: Spirit Resilience -0.02 (+0.11), Reactive Barrier -0.02 (+0.01), Counterspell -0.03 (+0.00)
- **Deadman Danny**: Spirit Resilience +0.26 (+0.39), Spellbreaker +0.25 (+0.39), Witchmail +0.22 (+0.37)
- **Rem**: Unstoppable +0.20 (+0.35), Counterspell -0.01 (+0.02), Return Fire -0.01 (+0.03)
- **Silver**: Dispel Magic +0.06 (+0.13), Debuff Reducer +0.00 (+0.05), Reactive Barrier -0.00 (+0.03)
- **Celeste**: Witchmail +0.04 (+0.19), Spirit Resilience +0.04 (+0.16), Dispel Magic +0.03 (+0.10)
- **Rat King**: Return Fire +0.02 (+0.06), Counterspell -0.00 (+0.03), Healbane -0.01 (+0.05)
- **Solomon**: Return Fire +0.02 (+0.07), Reactive Barrier +0.01 (+0.04), Counterspell +0.00 (+0.03)
- **Violet**: Unstoppable +0.09 (+0.24), Spirit Resilience +0.05 (+0.18), Indomitable +0.05 (+0.18)
- **Nurse Harrow**: Dispel Magic +0.16 (+0.23), Spirit Resilience +0.10 (+0.22), Witchmail +0.08 (+0.22)
- **Baba**: Witchmail +0.03 (+0.17), Unstoppable +0.02 (+0.17), Healbane +0.02 (+0.08)
