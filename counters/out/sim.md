# Counter items in the sim (phantom and up)

Built 2026-10-27T16:31:18Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.360 | +0.058 | +0.094 | Lash +0.25, Wraith +0.14, Paradox +0.11 | 0 heroes |
| Spirit Resilience | 3,200 | +0.183 | +0.057 | +0.118 | Lash +0.28, Deadman Danny +0.16, Wraith +0.15 | 1 heroes |
| Dispel Magic | 3,200 | +0.090 | +0.028 | +0.072 | Mirage +0.37, Paradox +0.10, Infernus +0.10 | 4 heroes |
| Indomitable | 6,400 | +0.167 | +0.027 | +0.136 | Vyper +0.29, Wraith +0.24, Deadman Danny +0.22 | 0 heroes |
| Reactive Barrier | 1,600 | +0.039 | +0.025 | +0.054 | Deadman Danny +0.12, Wraith +0.12, The Doorman +0.09 | 2 heroes |
| Witchmail | 6,400 | +0.132 | +0.021 | +0.194 | Deadman Danny +0.18, Lash +0.17, Wraith +0.15 | 0 heroes |
| Debuff Reducer | 1,600 | +0.028 | +0.018 | +0.059 | Wraith +0.07, Deadman Danny +0.07, Holliday +0.07 | 0 heroes |
| Spellbreaker | 6,400 | +0.081 | +0.013 | +0.143 | Lash +0.31, Deadman Danny +0.22, Wraith +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | -0.001 | -0.001 | +0.088 | Venator +0.16, Paradox +0.14, Wraith +0.12 | 0 heroes |
| Healbane | 1,600 | -0.007 | -0.004 | +0.086 | Deadman Danny +0.05, Abrams +0.04, Lash +0.04 | 11 heroes |
| Plated Armor | 6,400 | -0.034 | -0.005 | +0.124 | Holliday +0.26, Wraith +0.17, Deadman Danny +0.16 | 0 heroes |
| Counterspell | 3,200 | -0.025 | -0.008 | +0.070 | Deadman Danny +0.08, Billy +0.04, Lash +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.053 | -0.008 | +0.107 | Deadman Danny +0.15, Abrams +0.12, Wraith +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.146 | -0.046 | +0.104 | Lash +0.22, Wraith +0.22, Paradox +0.17 | 0 heroes |
| Return Fire | 1,600 | -0.172 | -0.107 | +0.078 | Lady Geist +0.07, The Doorman +0.06, Deadman Danny +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.17), Unstoppable +0.05 (+0.16), Spirit Resilience +0.04 (+0.15)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.04 (+0.02)
- **Vindicta**: Return Fire +0.01 (+0.09), Witchmail +0.01 (+0.20), Divine Barrier +0.01 (+0.10)
- **Lady Geist**: Return Fire +0.07 (+0.14), Dispel Magic +0.02 (+0.09), Divine Barrier +0.02 (+0.11)
- **Abrams**: Indomitable +0.20 (+0.33), Unstoppable +0.12 (+0.23), Divine Barrier +0.10 (+0.19)
- **Wraith**: Indomitable +0.24 (+0.38), Metal Skin +0.22 (+0.32), Plated Armor +0.17 (+0.30)
- **McGinnis**: Spirit Resilience +0.00 (+0.12), Return Fire -0.01 (+0.07), Healbane -0.02 (+0.07)
- **Paradox**: Metal Skin +0.17 (+0.27), Bullet Resilience +0.14 (+0.23), Plated Armor +0.13 (+0.25)
- **Dynamo**: Healbane +0.01 (+0.10), Counterspell -0.02 (+0.05), Return Fire -0.04 (+0.04)
- **Kelvin**: Healbane -0.00 (+0.09), Witchmail -0.01 (+0.19), Spirit Resilience -0.01 (+0.11)
- **Haze**: Plated Armor +0.07 (+0.20), Bullet Resilience +0.05 (+0.13), Indomitable +0.03 (+0.16)
- **Holliday**: Plated Armor +0.26 (+0.38), Indomitable +0.09 (+0.23), Spellbreaker +0.09 (+0.24)
- **Bebop**: Healbane +0.03 (+0.12), Counterspell +0.02 (+0.09), Bullet Resilience +0.00 (+0.09)
- **Calico**: Spellbreaker +0.11 (+0.25), Divine Barrier +0.10 (+0.19), Spirit Resilience +0.08 (+0.20)
- **Grey Talon**: Reactive Barrier +0.04 (+0.10), Debuff Reducer +0.04 (+0.10), Spellbreaker +0.04 (+0.18)
- **Mo & Krill**: Spellbreaker +0.12 (+0.27), Spirit Resilience +0.07 (+0.19), Witchmail +0.06 (+0.26)
- **Shiv**: Healbane -0.01 (+0.08), Return Fire -0.02 (+0.06), Spirit Resilience -0.04 (+0.08)
- **Ivy**: Unstoppable +0.10 (+0.20), Indomitable +0.07 (+0.21), Dispel Magic -0.00 (+0.07)
- **Warden**: Return Fire +0.01 (+0.08), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.04)
- **Yamato**: Healbane +0.02 (+0.11), Counterspell -0.02 (+0.05), Debuff Reducer -0.04 (+0.02)
- **Lash**: Spellbreaker +0.31 (+0.45), Spirit Resilience +0.28 (+0.39), Divine Barrier +0.25 (+0.35)
- **Viscous**: Healbane -0.02 (+0.07), Return Fire -0.03 (+0.05), Debuff Reducer -0.03 (+0.03)
- **Pocket**: Witchmail +0.06 (+0.25), Spirit Resilience +0.05 (+0.17), Spellbreaker +0.04 (+0.18)
- **Mirage**: Dispel Magic +0.37 (+0.44), Spellbreaker +0.07 (+0.21), Spirit Resilience +0.06 (+0.18)
- **Vyper**: Indomitable +0.29 (+0.43), Debuff Reducer +0.05 (+0.11), Spellbreaker +0.04 (+0.18)
- **Sinclair**: Indomitable +0.10 (+0.23), Return Fire +0.02 (+0.09), Spellbreaker +0.02 (+0.16)
- **Mina**: Return Fire +0.02 (+0.09), Witchmail +0.02 (+0.21), Counterspell -0.00 (+0.07)
- **Drifter**: Counterspell +0.01 (+0.08), Return Fire +0.01 (+0.09), Witchmail +0.00 (+0.20)
- **Venator**: Bullet Resilience +0.16 (+0.24), Divine Barrier +0.10 (+0.19), Metal Skin +0.08 (+0.19)
- **Victor**: Spirit Resilience +0.02 (+0.13), Healbane +0.01 (+0.10), Spellbreaker -0.01 (+0.13)
- **Paige**: Return Fire -0.01 (+0.07), Healbane -0.01 (+0.08), Counterspell -0.02 (+0.05)
- **The Doorman**: Indomitable +0.16 (+0.29), Witchmail +0.13 (+0.32), Spellbreaker +0.11 (+0.25)
- **Billy**: Spellbreaker +0.04 (+0.19), Counterspell +0.04 (+0.11), Spirit Resilience +0.04 (+0.16)
- **Graves**: Metal Skin +0.08 (+0.19), Witchmail +0.08 (+0.28), Spirit Resilience +0.08 (+0.20)
- **Apollo**: Healbane +0.01 (+0.09), Unstoppable +0.01 (+0.11), Reactive Barrier -0.02 (+0.04)
- **Deadman Danny**: Indomitable +0.22 (+0.36), Spellbreaker +0.22 (+0.36), Witchmail +0.18 (+0.38)
- **Rem**: Dispel Magic +0.00 (+0.08), Witchmail -0.00 (+0.19), Counterspell -0.01 (+0.06)
- **Silver**: Dispel Magic +0.07 (+0.14), Indomitable +0.04 (+0.17), Debuff Reducer +0.03 (+0.09)
- **Celeste**: Spirit Resilience +0.09 (+0.21), Witchmail +0.08 (+0.27), Dispel Magic +0.03 (+0.10)
- **Rat King**: Counterspell +0.00 (+0.07), Return Fire -0.01 (+0.07), Bullet Resilience -0.01 (+0.08)
- **Solomon**: Return Fire -0.00 (+0.07), Counterspell -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **Violet**: Return Fire +0.03 (+0.11), Healbane -0.03 (+0.06), Counterspell -0.04 (+0.03)
- **Nurse Harrow**: Healbane +0.03 (+0.11), Counterspell -0.02 (+0.05), Return Fire -0.03 (+0.04)
- **Baba**: Healbane +0.00 (+0.09), Unstoppable -0.02 (+0.09), Debuff Reducer -0.02 (+0.04)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.161 | +0.050 | +0.110 | Lash +0.33, Pocket +0.23, Deadman Danny +0.21 | 10 heroes |
| Divine Barrier | 6,400 | +0.234 | +0.037 | +0.060 | Lash +0.20, Wraith +0.10, Graves +0.09 | 1 heroes |
| Dispel Magic | 3,200 | +0.075 | +0.023 | +0.044 | Mirage +0.31, Graves +0.10, Infernus +0.09 | 7 heroes |
| Indomitable | 6,400 | +0.135 | +0.022 | +0.110 | Vyper +0.34, Wraith +0.23, Deadman Danny +0.13 | 0 heroes |
| Witchmail | 6,400 | +0.129 | +0.020 | +0.161 | Lash +0.17, Graves +0.16, Deadman Danny +0.14 | 0 heroes |
| Spellbreaker | 6,400 | +0.098 | +0.015 | +0.115 | Lash +0.35, Deadman Danny +0.16, Pocket +0.14 | 0 heroes |
| Reactive Barrier | 1,600 | +0.019 | +0.012 | +0.036 | Graves +0.11, Deadman Danny +0.10, The Doorman +0.08 | 4 heroes |
| Debuff Reducer | 1,600 | -0.006 | -0.004 | +0.036 | Wraith +0.08, Vyper +0.06, Grey Talon +0.04 | 1 heroes |
| Plated Armor | 6,400 | -0.027 | -0.004 | +0.095 | Deadman Danny +0.22, Wraith +0.11, Graves +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | -0.032 | -0.010 | +0.057 | Venator +0.12, Paradox +0.10, Wraith +0.07 | 0 heroes |
| Counterspell | 3,200 | -0.036 | -0.011 | +0.040 | Graves +0.05, Vindicta +0.04, Lady Geist +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.081 | -0.013 | +0.078 | Mo & Krill +0.11, Ivy +0.10, Abrams +0.07 | 0 heroes |
| Healbane | 1,600 | -0.033 | -0.021 | +0.062 | Kelvin +0.05, Bebop +0.05, Yamato +0.05 | 17 heroes |
| Metal Skin | 3,200 | -0.163 | -0.051 | +0.080 | Wraith +0.19, Paradox +0.15, Graves +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.180 | -0.113 | +0.052 | Wraith +0.07, Paradox +0.05, Graves +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.14), Unstoppable +0.05 (+0.13), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.04 (+0.20), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Vindicta**: Witchmail +0.05 (+0.21), Counterspell +0.04 (+0.08), Divine Barrier +0.03 (+0.09)
- **Lady Geist**: Divine Barrier +0.05 (+0.11), Metal Skin +0.05 (+0.13), Return Fire +0.05 (+0.10)
- **Abrams**: Indomitable +0.09 (+0.20), Unstoppable +0.07 (+0.15), Healbane +0.04 (+0.10)
- **Wraith**: Indomitable +0.23 (+0.34), Metal Skin +0.19 (+0.27), Plated Armor +0.11 (+0.20)
- **McGinnis**: Spirit Resilience +0.08 (+0.19), Witchmail +0.02 (+0.18), Return Fire +0.02 (+0.07)
- **Paradox**: Metal Skin +0.15 (+0.23), Bullet Resilience +0.10 (+0.16), Plated Armor +0.09 (+0.19)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.05 (+0.16), Healbane +0.05 (+0.11), Dispel Magic +0.03 (+0.08)
- **Haze**: Indomitable +0.08 (+0.19), Plated Armor +0.07 (+0.17), Unstoppable +0.06 (+0.14)
- **Holliday**: Indomitable +0.08 (+0.19), Spellbreaker +0.03 (+0.14), Return Fire +0.02 (+0.08)
- **Bebop**: Healbane +0.05 (+0.11), Metal Skin +0.01 (+0.09), Counterspell -0.00 (+0.04)
- **Calico**: Reactive Barrier +0.05 (+0.09), Divine Barrier +0.05 (+0.11), Spellbreaker +0.04 (+0.16)
- **Grey Talon**: Debuff Reducer +0.04 (+0.08), Unstoppable +0.03 (+0.11), Reactive Barrier +0.03 (+0.06)
- **Mo & Krill**: Unstoppable +0.11 (+0.19), Dispel Magic +0.05 (+0.10), Spellbreaker +0.04 (+0.15)
- **Shiv**: Bullet Resilience +0.06 (+0.11), Divine Barrier +0.05 (+0.11), Plated Armor +0.03 (+0.13)
- **Ivy**: Unstoppable +0.10 (+0.18), Indomitable +0.07 (+0.18), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.07), Debuff Reducer +0.00 (+0.04), Counterspell +0.00 (+0.04)
- **Yamato**: Healbane +0.05 (+0.11), Bullet Resilience +0.00 (+0.06), Counterspell -0.00 (+0.04)
- **Lash**: Spellbreaker +0.35 (+0.46), Spirit Resilience +0.33 (+0.44), Divine Barrier +0.20 (+0.26)
- **Viscous**: Divine Barrier +0.01 (+0.07), Counterspell +0.00 (+0.04), Healbane -0.00 (+0.06)
- **Pocket**: Spirit Resilience +0.23 (+0.34), Spellbreaker +0.14 (+0.26), Witchmail +0.12 (+0.28)
- **Mirage**: Dispel Magic +0.31 (+0.35), Spirit Resilience +0.05 (+0.16), Metal Skin +0.04 (+0.12)
- **Vyper**: Indomitable +0.34 (+0.45), Metal Skin +0.06 (+0.14), Debuff Reducer +0.06 (+0.09)
- **Sinclair**: Indomitable +0.06 (+0.18), Return Fire +0.00 (+0.05), Spellbreaker -0.01 (+0.11)
- **Mina**: Witchmail +0.03 (+0.19), Spirit Resilience +0.03 (+0.14), Divine Barrier +0.02 (+0.08)
- **Drifter**: Witchmail +0.04 (+0.20), Counterspell +0.00 (+0.04), Dispel Magic +0.00 (+0.05)
- **Venator**: Bullet Resilience +0.12 (+0.17), Metal Skin +0.11 (+0.19), Divine Barrier +0.05 (+0.11)
- **Victor**: Spirit Resilience +0.06 (+0.17), Spellbreaker +0.06 (+0.17), Healbane -0.01 (+0.05)
- **Paige**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.04), Healbane -0.01 (+0.05)
- **The Doorman**: Spirit Resilience +0.14 (+0.25), Indomitable +0.11 (+0.22), Divine Barrier +0.09 (+0.15)
- **Billy**: Spirit Resilience +0.03 (+0.14), Spellbreaker +0.01 (+0.12), Counterspell -0.00 (+0.04)
- **Graves**: Witchmail +0.16 (+0.33), Metal Skin +0.14 (+0.21), Spirit Resilience +0.13 (+0.24)
- **Apollo**: Reactive Barrier +0.06 (+0.10), Indomitable +0.04 (+0.15), Unstoppable +0.01 (+0.09)
- **Deadman Danny**: Plated Armor +0.22 (+0.32), Spirit Resilience +0.21 (+0.32), Spellbreaker +0.16 (+0.27)
- **Rem**: Unstoppable +0.01 (+0.09), Counterspell +0.01 (+0.05), Divine Barrier +0.00 (+0.06)
- **Silver**: Dispel Magic +0.08 (+0.12), Metal Skin +0.03 (+0.11), Indomitable +0.03 (+0.14)
- **Celeste**: Witchmail +0.07 (+0.23), Spirit Resilience +0.01 (+0.12), Healbane -0.00 (+0.06)
- **Rat King**: Bullet Resilience -0.00 (+0.06), Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.03)
- **Solomon**: Return Fire -0.00 (+0.05), Counterspell -0.00 (+0.04), Healbane -0.02 (+0.05)
- **Violet**: Return Fire +0.04 (+0.09), Witchmail +0.02 (+0.18), Healbane +0.01 (+0.08)
- **Nurse Harrow**: Healbane -0.03 (+0.04), Dispel Magic -0.03 (+0.02), Counterspell -0.03 (+0.01)
- **Baba**: Unstoppable +0.05 (+0.13), Healbane +0.02 (+0.08), Debuff Reducer +0.00 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.156 | +0.049 | +0.123 | Lash +0.30, Deadman Danny +0.25, The Doorman +0.15 | 14 heroes |
| Divine Barrier | 6,400 | +0.205 | +0.032 | +0.063 | Lash +0.23, Vindicta +0.12, Paradox +0.11 | 2 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.064 | Lash +0.30, Mirage +0.28, Silver +0.11 | 9 heroes |
| Indomitable | 6,400 | +0.150 | +0.024 | +0.135 | Vyper +0.38, Wraith +0.28, Deadman Danny +0.24 | 0 heroes |
| Witchmail | 6,400 | +0.128 | +0.020 | +0.171 | Lash +0.19, Deadman Danny +0.18, Paradox +0.12 | 1 heroes |
| Spellbreaker | 6,400 | +0.110 | +0.017 | +0.134 | Lash +0.41, Deadman Danny +0.22, Grey Talon +0.14 | 0 heroes |
| Reactive Barrier | 1,600 | +0.006 | +0.004 | +0.038 | Deadman Danny +0.14, Yamato +0.08, Wraith +0.08 | 5 heroes |
| Plated Armor | 6,400 | -0.018 | -0.003 | +0.113 | Deadman Danny +0.22, Holliday +0.18, Wraith +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | -0.011 | -0.007 | +0.045 | Grey Talon +0.09, Vyper +0.09, Wraith +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.037 | -0.011 | +0.037 | Deadman Danny +0.07, Vindicta +0.04, Calico +0.03 | 1 heroes |
| Bullet Resilience | 3,200 | -0.040 | -0.012 | +0.066 | Vindicta +0.11, Deadman Danny +0.11, Lash +0.10 | 1 heroes |
| Unstoppable | 6,400 | -0.080 | -0.012 | +0.101 | Deadman Danny +0.17, Grey Talon +0.12, Abrams +0.12 | 3 heroes |
| Healbane | 1,600 | -0.033 | -0.021 | +0.063 | Nurse Harrow +0.11, Yamato +0.05, Infernus +0.03 | 15 heroes |
| Metal Skin | 3,200 | -0.155 | -0.048 | +0.100 | Wraith +0.24, Lash +0.20, Venator +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.174 | -0.109 | +0.054 | Wraith +0.09, Paradox +0.07, Vindicta +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.10 (+0.20), Dispel Magic +0.09 (+0.15), Spellbreaker +0.08 (+0.22)
- **Seven**: Witchmail +0.04 (+0.21), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03)
- **Vindicta**: Divine Barrier +0.12 (+0.18), Bullet Resilience +0.11 (+0.18), Plated Armor +0.08 (+0.19)
- **Lady Geist**: Return Fire +0.05 (+0.10), Metal Skin +0.03 (+0.13), Bullet Resilience +0.02 (+0.08)
- **Abrams**: Unstoppable +0.12 (+0.22), Dispel Magic +0.07 (+0.13), Healbane +0.02 (+0.08)
- **Wraith**: Indomitable +0.28 (+0.41), Metal Skin +0.24 (+0.34), Plated Armor +0.14 (+0.26)
- **McGinnis**: Spirit Resilience +0.09 (+0.22), Witchmail +0.07 (+0.24), Spellbreaker +0.04 (+0.17)
- **Paradox**: Spellbreaker +0.14 (+0.27), Witchmail +0.12 (+0.29), Divine Barrier +0.11 (+0.18)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.00 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Healbane -0.00 (+0.06), Counterspell -0.01 (+0.02), Spirit Resilience -0.02 (+0.10)
- **Haze**: Plated Armor +0.08 (+0.19), Indomitable +0.07 (+0.21), Unstoppable +0.06 (+0.16)
- **Holliday**: Plated Armor +0.18 (+0.29), Indomitable +0.04 (+0.17), Return Fire +0.03 (+0.08)
- **Bebop**: Healbane +0.02 (+0.08), Counterspell -0.02 (+0.02), Metal Skin -0.02 (+0.08)
- **Calico**: Reactive Barrier +0.04 (+0.08), Spirit Resilience +0.04 (+0.16), Divine Barrier +0.03 (+0.09)
- **Grey Talon**: Spellbreaker +0.14 (+0.28), Unstoppable +0.12 (+0.22), Indomitable +0.12 (+0.25)
- **Mo & Krill**: Unstoppable +0.08 (+0.18), Spirit Resilience +0.05 (+0.17), Spellbreaker +0.05 (+0.18)
- **Shiv**: Bullet Resilience +0.04 (+0.10), Metal Skin +0.03 (+0.13), Divine Barrier +0.02 (+0.08)
- **Ivy**: Unstoppable +0.08 (+0.18), Indomitable +0.04 (+0.18), Debuff Reducer +0.00 (+0.05)
- **Warden**: Return Fire +0.02 (+0.07), Counterspell +0.01 (+0.05), Divine Barrier +0.01 (+0.07)
- **Yamato**: Reactive Barrier +0.08 (+0.11), Indomitable +0.06 (+0.19), Healbane +0.05 (+0.11)
- **Lash**: Spellbreaker +0.41 (+0.54), Dispel Magic +0.30 (+0.37), Spirit Resilience +0.30 (+0.42)
- **Viscous**: Return Fire +0.03 (+0.09), Divine Barrier +0.02 (+0.08), Healbane +0.01 (+0.07)
- **Pocket**: Spirit Resilience +0.10 (+0.22), Witchmail +0.04 (+0.21), Spellbreaker +0.01 (+0.15)
- **Mirage**: Dispel Magic +0.28 (+0.35), Spirit Resilience +0.03 (+0.16), Metal Skin +0.02 (+0.12)
- **Vyper**: Indomitable +0.38 (+0.51), Debuff Reducer +0.09 (+0.13), Unstoppable +0.05 (+0.15)
- **Sinclair**: Indomitable +0.13 (+0.26), Return Fire +0.00 (+0.06), Unstoppable -0.01 (+0.09)
- **Mina**: Spirit Resilience +0.12 (+0.24), Witchmail +0.09 (+0.26), Divine Barrier +0.06 (+0.12)
- **Drifter**: Spirit Resilience +0.05 (+0.17), Witchmail +0.04 (+0.21), Counterspell +0.01 (+0.04)
- **Venator**: Metal Skin +0.11 (+0.21), Bullet Resilience +0.07 (+0.14), Plated Armor +0.03 (+0.15)
- **Victor**: Healbane +0.02 (+0.09), Spirit Resilience +0.02 (+0.14), Spellbreaker +0.02 (+0.15)
- **Paige**: Unstoppable +0.11 (+0.21), Debuff Reducer +0.05 (+0.10), Counterspell -0.01 (+0.03)
- **The Doorman**: Spirit Resilience +0.15 (+0.27), Indomitable +0.11 (+0.24), Witchmail +0.08 (+0.25)
- **Billy**: Reactive Barrier +0.02 (+0.05), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Graves**: Witchmail +0.02 (+0.19), Metal Skin +0.01 (+0.11), Counterspell +0.00 (+0.04)
- **Apollo**: Healbane -0.03 (+0.03), Counterspell -0.04 (+0.00), Return Fire -0.04 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.25 (+0.37), Indomitable +0.24 (+0.37), Spellbreaker +0.22 (+0.35)
- **Rem**: Debuff Reducer +0.06 (+0.10), Unstoppable +0.04 (+0.14), Counterspell -0.00 (+0.04)
- **Silver**: Dispel Magic +0.11 (+0.17), Reactive Barrier +0.04 (+0.08), Debuff Reducer +0.01 (+0.06)
- **Celeste**: Witchmail +0.07 (+0.24), Dispel Magic +0.04 (+0.10), Reactive Barrier +0.01 (+0.05)
- **Rat King**: Return Fire -0.01 (+0.05), Bullet Resilience -0.01 (+0.06), Counterspell -0.01 (+0.03)
- **Solomon**: Reactive Barrier +0.00 (+0.04), Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.04)
- **Violet**: Witchmail +0.05 (+0.22), Return Fire +0.04 (+0.10), Healbane +0.03 (+0.09)
- **Nurse Harrow**: Healbane +0.11 (+0.17), Return Fire +0.02 (+0.08), Counterspell +0.00 (+0.04)
- **Baba**: Unstoppable +0.01 (+0.11), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.178 | +0.056 | +0.133 | Lash +0.58, Deadman Danny +0.35, The Doorman +0.34 | 15 heroes |
| Indomitable | 6,400 | +0.165 | +0.027 | +0.155 | Deadman Danny +0.27, Vyper +0.27, Wraith +0.25 | 1 heroes |
| Divine Barrier | 6,400 | +0.165 | +0.026 | +0.057 | Lash +0.29, The Doorman +0.15, Vindicta +0.12 | 3 heroes |
| Dispel Magic | 3,200 | +0.076 | +0.024 | +0.053 | Mirage +0.27, Silver +0.22, Lash +0.21 | 9 heroes |
| Witchmail | 6,400 | +0.119 | +0.018 | +0.155 | Lash +0.32, The Doorman +0.24, Deadman Danny +0.19 | 2 heroes |
| Spellbreaker | 6,400 | +0.118 | +0.018 | +0.135 | Lash +0.46, Deadman Danny +0.24, The Doorman +0.18 | 0 heroes |
| Plated Armor | 6,400 | -0.033 | -0.005 | +0.092 | Vindicta +0.17, Lash +0.15, Vyper +0.13 | 2 heroes |
| Unstoppable | 6,400 | -0.077 | -0.012 | +0.109 | Haze +0.22, Infernus +0.22, Grey Talon +0.17 | 8 heroes |
| Counterspell | 3,200 | -0.040 | -0.013 | +0.031 | Lash +0.12, The Doorman +0.06, Yamato +0.03 | 1 heroes |
| Bullet Resilience | 3,200 | -0.048 | -0.015 | +0.057 | Lash +0.17, Vindicta +0.15, Venator +0.10 | 0 heroes |
| Reactive Barrier | 1,600 | -0.024 | -0.015 | +0.035 | Deadman Danny +0.14, Yamato +0.12, Drifter +0.12 | 3 heroes |
| Debuff Reducer | 1,600 | -0.025 | -0.016 | +0.040 | Grey Talon +0.10, Rem +0.08, Yamato +0.07 | 0 heroes |
| Healbane | 1,600 | -0.039 | -0.024 | +0.052 | Nurse Harrow +0.08, Mo & Krill +0.06, Lady Geist +0.05 | 14 heroes |
| Metal Skin | 3,200 | -0.155 | -0.049 | +0.100 | Lash +0.28, Grey Talon +0.18, Venator +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.174 | -0.109 | +0.043 | Paradox +0.06, Vindicta +0.05, Wraith +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.22 (+0.33), Dispel Magic +0.06 (+0.11), Spellbreaker +0.04 (+0.17)
- **Seven**: Witchmail +0.07 (+0.23), Counterspell +0.00 (+0.03), Healbane -0.00 (+0.05)
- **Vindicta**: Plated Armor +0.17 (+0.26), Bullet Resilience +0.15 (+0.20), Divine Barrier +0.12 (+0.18)
- **Lady Geist**: Healbane +0.05 (+0.10), Dispel Magic +0.02 (+0.08), Plated Armor +0.01 (+0.11)
- **Abrams**: Unstoppable +0.07 (+0.18), Dispel Magic +0.04 (+0.10), Divine Barrier +0.03 (+0.09)
- **Wraith**: Indomitable +0.25 (+0.40), Metal Skin +0.09 (+0.19), Plated Armor +0.05 (+0.14)
- **McGinnis**: Spirit Resilience +0.03 (+0.16), Healbane +0.02 (+0.08), Witchmail +0.01 (+0.17)
- **Paradox**: Witchmail +0.14 (+0.30), Unstoppable +0.12 (+0.23), Spirit Resilience +0.08 (+0.22)
- **Dynamo**: Healbane +0.02 (+0.07), Counterspell -0.01 (+0.03), Return Fire -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.07 (+0.20), Spellbreaker +0.02 (+0.15), Healbane +0.01 (+0.06)
- **Haze**: Unstoppable +0.22 (+0.33), Bullet Resilience +0.05 (+0.11), Indomitable +0.04 (+0.20)
- **Holliday**: Spellbreaker +0.04 (+0.18), Return Fire +0.03 (+0.07), Debuff Reducer +0.02 (+0.06)
- **Bebop**: Debuff Reducer +0.06 (+0.10), Healbane +0.01 (+0.06), Unstoppable -0.00 (+0.10)
- **Calico**: Divine Barrier +0.12 (+0.18), Spirit Resilience +0.12 (+0.25), Spellbreaker +0.09 (+0.23)
- **Grey Talon**: Metal Skin +0.18 (+0.28), Unstoppable +0.17 (+0.28), Spellbreaker +0.13 (+0.26)
- **Mo & Krill**: Healbane +0.06 (+0.11), Dispel Magic +0.03 (+0.09), Unstoppable +0.03 (+0.14)
- **Shiv**: Bullet Resilience +0.05 (+0.10), Metal Skin +0.03 (+0.13), Divine Barrier +0.03 (+0.08)
- **Ivy**: Unstoppable +0.13 (+0.24), Indomitable +0.08 (+0.24), Debuff Reducer +0.05 (+0.09)
- **Warden**: Plated Armor +0.06 (+0.15), Metal Skin +0.04 (+0.14), Return Fire +0.02 (+0.06)
- **Yamato**: Reactive Barrier +0.12 (+0.16), Indomitable +0.10 (+0.26), Plated Armor +0.07 (+0.16)
- **Lash**: Spirit Resilience +0.58 (+0.71), Spellbreaker +0.46 (+0.60), Witchmail +0.32 (+0.48)
- **Viscous**: Divine Barrier +0.05 (+0.11), Return Fire +0.03 (+0.07), Witchmail +0.02 (+0.18)
- **Pocket**: Spirit Resilience +0.08 (+0.21), Spellbreaker +0.00 (+0.14), Return Fire -0.01 (+0.03)
- **Mirage**: Dispel Magic +0.27 (+0.33), Metal Skin +0.07 (+0.17), Plated Armor +0.01 (+0.10)
- **Vyper**: Indomitable +0.27 (+0.42), Plated Armor +0.13 (+0.22), Metal Skin +0.06 (+0.16)
- **Sinclair**: Indomitable +0.14 (+0.29), Dispel Magic +0.06 (+0.11), Reactive Barrier +0.06 (+0.09)
- **Mina**: Divine Barrier +0.00 (+0.06), Return Fire -0.01 (+0.03), Dispel Magic -0.01 (+0.04)
- **Drifter**: Indomitable +0.19 (+0.35), Spirit Resilience +0.18 (+0.32), Spellbreaker +0.12 (+0.25)
- **Venator**: Metal Skin +0.14 (+0.24), Bullet Resilience +0.10 (+0.16), Plated Armor +0.06 (+0.15)
- **Victor**: Spellbreaker +0.08 (+0.22), Spirit Resilience +0.05 (+0.19), Healbane +0.03 (+0.08)
- **Paige**: Counterspell +0.01 (+0.04), Return Fire +0.00 (+0.04), Witchmail -0.00 (+0.15)
- **The Doorman**: Spirit Resilience +0.34 (+0.47), Witchmail +0.24 (+0.39), Indomitable +0.23 (+0.38)
- **Billy**: Reactive Barrier +0.07 (+0.10), Healbane +0.04 (+0.09), Counterspell +0.03 (+0.06)
- **Graves**: Return Fire +0.02 (+0.06), Witchmail -0.01 (+0.14), Reactive Barrier -0.01 (+0.02)
- **Apollo**: Healbane -0.00 (+0.05), Reactive Barrier -0.02 (+0.01), Counterspell -0.03 (+0.00)
- **Deadman Danny**: Spirit Resilience +0.35 (+0.49), Indomitable +0.27 (+0.43), Spellbreaker +0.24 (+0.38)
- **Rem**: Debuff Reducer +0.08 (+0.12), Spellbreaker +0.04 (+0.18), Unstoppable +0.01 (+0.12)
- **Silver**: Dispel Magic +0.22 (+0.27), Indomitable +0.16 (+0.32), Metal Skin +0.14 (+0.24)
- **Celeste**: Witchmail +0.10 (+0.26), Spirit Resilience +0.06 (+0.19), Healbane +0.04 (+0.09)
- **Rat King**: Return Fire -0.00 (+0.04), Healbane -0.01 (+0.04), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.00 (+0.04), Return Fire -0.01 (+0.03), Debuff Reducer -0.01 (+0.03)
- **Violet**: Return Fire +0.03 (+0.08), Witchmail +0.01 (+0.16), Counterspell -0.00 (+0.03)
- **Nurse Harrow**: Spirit Resilience +0.10 (+0.24), Dispel Magic +0.10 (+0.15), Witchmail +0.10 (+0.25)
- **Baba**: Healbane -0.00 (+0.05), Counterspell -0.01 (+0.02), Unstoppable -0.01 (+0.10)
