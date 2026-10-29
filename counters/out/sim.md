# Counter items in the sim (phantom and up)

Built 2026-10-29T21:16:41Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.390 | +0.062 | +0.127 | Lash +0.22, Deadman Danny +0.12, Wraith +0.11 | 0 heroes |
| Spirit Resilience | 3,200 | +0.185 | +0.058 | +0.116 | Lash +0.29, Deadman Danny +0.23, Graves +0.12 | 1 heroes |
| Dispel Magic | 3,200 | +0.095 | +0.030 | +0.073 | Mirage +0.32, Deadman Danny +0.16, Infernus +0.12 | 3 heroes |
| Reactive Barrier | 1,600 | +0.043 | +0.028 | +0.063 | Deadman Danny +0.23, Calico +0.13, The Doorman +0.08 | 3 heroes |
| Indomitable | 6,400 | +0.161 | +0.026 | +0.140 | Deadman Danny +0.27, Vyper +0.26, Abrams +0.21 | 0 heroes |
| Witchmail | 6,400 | +0.152 | +0.024 | +0.198 | Deadman Danny +0.25, Lash +0.23, Wraith +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.033 | +0.021 | +0.073 | Deadman Danny +0.14, Vyper +0.11, Wraith +0.10 | 0 heroes |
| Spellbreaker | 6,400 | +0.086 | +0.013 | +0.153 | Deadman Danny +0.29, Lash +0.25, Holliday +0.14 | 0 heroes |
| Bullet Resilience | 3,200 | -0.004 | -0.001 | +0.084 | Deadman Danny +0.18, Venator +0.15, Lash +0.12 | 0 heroes |
| Plated Armor | 6,400 | -0.039 | -0.006 | +0.117 | Deadman Danny +0.24, Holliday +0.21, Wraith +0.12 | 0 heroes |
| Counterspell | 3,200 | -0.024 | -0.007 | +0.071 | Deadman Danny +0.15, Paradox +0.05, Wraith +0.04 | 1 heroes |
| Healbane | 1,600 | -0.015 | -0.009 | +0.085 | Deadman Danny +0.07, Billy +0.04, Celeste +0.04 | 11 heroes |
| Unstoppable | 6,400 | -0.061 | -0.009 | +0.126 | Deadman Danny +0.21, Abrams +0.12, Holliday +0.11 | 0 heroes |
| Metal Skin | 3,200 | -0.165 | -0.051 | +0.095 | Lash +0.20, Wraith +0.15, Graves +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.177 | -0.111 | +0.074 | Deadman Danny +0.10, The Doorman +0.08, Paradox +0.08 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.19), Spellbreaker +0.09 (+0.24), Unstoppable +0.06 (+0.19)
- **Seven**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.05), Metal Skin -0.03 (+0.06)
- **Vindicta**: Return Fire +0.01 (+0.08), Divine Barrier +0.00 (+0.13), Witchmail -0.01 (+0.19)
- **Lady Geist**: Return Fire +0.03 (+0.10), Healbane +0.00 (+0.09), Counterspell -0.01 (+0.06)
- **Abrams**: Indomitable +0.21 (+0.35), Unstoppable +0.12 (+0.24), Spirit Resilience +0.09 (+0.20)
- **Wraith**: Indomitable +0.18 (+0.32), Metal Skin +0.15 (+0.25), Plated Armor +0.12 (+0.24)
- **McGinnis**: Spirit Resilience -0.01 (+0.10), Healbane -0.02 (+0.07), Return Fire -0.02 (+0.05)
- **Paradox**: Metal Skin +0.10 (+0.20), Bullet Resilience +0.10 (+0.18), Indomitable +0.08 (+0.22)
- **Dynamo**: Healbane -0.01 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.05 (+0.01)
- **Kelvin**: Healbane +0.00 (+0.09), Dispel Magic -0.01 (+0.06), Counterspell -0.01 (+0.06)
- **Haze**: Indomitable +0.09 (+0.23), Unstoppable +0.06 (+0.18), Plated Armor +0.04 (+0.16)
- **Holliday**: Plated Armor +0.21 (+0.33), Spellbreaker +0.14 (+0.29), Unstoppable +0.11 (+0.24)
- **Bebop**: Healbane +0.03 (+0.12), Counterspell +0.01 (+0.08), Return Fire +0.00 (+0.08)
- **Calico**: Reactive Barrier +0.13 (+0.19), Spellbreaker +0.12 (+0.27), Divine Barrier +0.11 (+0.24)
- **Grey Talon**: Unstoppable +0.06 (+0.19), Debuff Reducer +0.04 (+0.11), Spellbreaker +0.04 (+0.19)
- **Mo & Krill**: Spellbreaker +0.13 (+0.29), Spirit Resilience +0.09 (+0.20), Dispel Magic +0.07 (+0.14)
- **Shiv**: Healbane -0.02 (+0.07), Return Fire -0.03 (+0.05), Spirit Resilience -0.03 (+0.09)
- **Ivy**: Indomitable +0.11 (+0.25), Unstoppable +0.09 (+0.22), Bullet Resilience +0.01 (+0.10)
- **Warden**: Return Fire +0.02 (+0.09), Debuff Reducer +0.00 (+0.08), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.03 (+0.12), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.05)
- **Lash**: Spirit Resilience +0.29 (+0.41), Spellbreaker +0.25 (+0.40), Witchmail +0.23 (+0.43)
- **Viscous**: Healbane -0.01 (+0.07), Counterspell -0.02 (+0.05), Return Fire -0.03 (+0.05)
- **Pocket**: Witchmail +0.01 (+0.21), Spirit Resilience +0.01 (+0.12), Bullet Resilience +0.01 (+0.09)
- **Mirage**: Dispel Magic +0.32 (+0.40), Spellbreaker +0.08 (+0.23), Plated Armor +0.06 (+0.18)
- **Vyper**: Indomitable +0.26 (+0.40), Debuff Reducer +0.11 (+0.18), Unstoppable +0.08 (+0.20)
- **Sinclair**: Indomitable +0.15 (+0.29), Spellbreaker +0.07 (+0.23), Unstoppable +0.03 (+0.15)
- **Mina**: Return Fire +0.02 (+0.10), Spirit Resilience +0.00 (+0.12), Counterspell -0.00 (+0.07)
- **Drifter**: Healbane -0.01 (+0.08), Return Fire -0.01 (+0.06), Counterspell -0.01 (+0.06)
- **Venator**: Bullet Resilience +0.15 (+0.24), Metal Skin +0.07 (+0.16), Debuff Reducer +0.07 (+0.14)
- **Victor**: Healbane -0.01 (+0.07), Spirit Resilience -0.04 (+0.08), Reactive Barrier -0.05 (+0.01)
- **Paige**: Return Fire -0.00 (+0.07), Counterspell -0.01 (+0.06), Healbane -0.03 (+0.06)
- **The Doorman**: Indomitable +0.15 (+0.28), Spellbreaker +0.12 (+0.27), Spirit Resilience +0.12 (+0.23)
- **Billy**: Spellbreaker +0.10 (+0.25), Healbane +0.04 (+0.13), Spirit Resilience +0.04 (+0.15)
- **Graves**: Metal Skin +0.14 (+0.24), Spirit Resilience +0.12 (+0.23), Witchmail +0.11 (+0.31)
- **Apollo**: Reactive Barrier +0.01 (+0.07), Unstoppable -0.00 (+0.12), Indomitable -0.01 (+0.13)
- **Deadman Danny**: Spellbreaker +0.29 (+0.44), Indomitable +0.27 (+0.41), Witchmail +0.25 (+0.45)
- **Rem**: Dispel Magic -0.01 (+0.06), Debuff Reducer -0.02 (+0.06), Witchmail -0.02 (+0.18)
- **Silver**: Dispel Magic +0.04 (+0.12), Debuff Reducer +0.03 (+0.10), Metal Skin +0.02 (+0.12)
- **Celeste**: Spirit Resilience +0.07 (+0.18), Witchmail +0.05 (+0.25), Healbane +0.04 (+0.12)
- **Rat King**: Bullet Resilience +0.01 (+0.09), Return Fire +0.01 (+0.08), Metal Skin -0.00 (+0.09)
- **Solomon**: Return Fire -0.00 (+0.07), Counterspell -0.02 (+0.05), Healbane -0.04 (+0.05)
- **Violet**: Return Fire -0.00 (+0.07), Healbane -0.02 (+0.06), Counterspell -0.04 (+0.03)
- **Nurse Harrow**: Healbane +0.01 (+0.10), Counterspell -0.04 (+0.03), Return Fire -0.04 (+0.03)
- **Baba**: Healbane -0.00 (+0.08), Unstoppable -0.02 (+0.11), Debuff Reducer -0.03 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.159 | +0.050 | +0.100 | Lash +0.36, Graves +0.18, Deadman Danny +0.17 | 10 heroes |
| Divine Barrier | 6,400 | +0.284 | +0.045 | +0.089 | Lash +0.21, Graves +0.11, Paradox +0.10 | 1 heroes |
| Dispel Magic | 3,200 | +0.083 | +0.026 | +0.044 | Mirage +0.28, Infernus +0.12, Mo & Krill +0.07 | 6 heroes |
| Witchmail | 6,400 | +0.146 | +0.023 | +0.151 | Lash +0.21, Graves +0.14, Deadman Danny +0.12 | 0 heroes |
| Indomitable | 6,400 | +0.140 | +0.023 | +0.103 | Vyper +0.40, Wraith +0.20, Deadman Danny +0.15 | 0 heroes |
| Spellbreaker | 6,400 | +0.098 | +0.015 | +0.117 | Lash +0.36, Vyper +0.18, Mo & Krill +0.13 | 0 heroes |
| Reactive Barrier | 1,600 | +0.019 | +0.012 | +0.032 | Vyper +0.11, The Doorman +0.10, Graves +0.07 | 4 heroes |
| Debuff Reducer | 1,600 | +0.006 | +0.004 | +0.048 | Rem +0.12, Wraith +0.11, Vyper +0.10 | 1 heroes |
| Plated Armor | 6,400 | -0.037 | -0.006 | +0.085 | Holliday +0.18, Deadman Danny +0.16, Graves +0.12 | 0 heroes |
| Bullet Resilience | 3,200 | -0.036 | -0.011 | +0.049 | Venator +0.13, Paradox +0.11, Lash +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.038 | -0.012 | +0.039 | McGinnis +0.05, Vindicta +0.04, Vyper +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.087 | -0.014 | +0.091 | Abrams +0.19, Vyper +0.10, Rem +0.10 | 0 heroes |
| Healbane | 1,600 | -0.046 | -0.029 | +0.061 | Yamato +0.05, Abrams +0.05, Billy +0.03 | 17 heroes |
| Metal Skin | 3,200 | -0.186 | -0.058 | +0.063 | Graves +0.16, Wraith +0.14, Paradox +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.184 | -0.115 | +0.050 | Paradox +0.06, Graves +0.05, Wraith +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.16), Spellbreaker +0.09 (+0.20), Unstoppable +0.07 (+0.16)
- **Seven**: Witchmail +0.01 (+0.16), Counterspell -0.00 (+0.04), Metal Skin -0.01 (+0.06)
- **Vindicta**: Witchmail +0.06 (+0.21), Divine Barrier +0.05 (+0.14), Counterspell +0.04 (+0.08)
- **Lady Geist**: Return Fire +0.03 (+0.08), Divine Barrier +0.02 (+0.11), Metal Skin +0.02 (+0.08)
- **Abrams**: Unstoppable +0.19 (+0.28), Indomitable +0.10 (+0.20), Divine Barrier +0.07 (+0.15)
- **Wraith**: Indomitable +0.20 (+0.30), Metal Skin +0.14 (+0.21), Debuff Reducer +0.11 (+0.16)
- **McGinnis**: Spirit Resilience +0.07 (+0.17), Dispel Magic +0.05 (+0.09), Counterspell +0.05 (+0.09)
- **Paradox**: Metal Skin +0.13 (+0.19), Bullet Resilience +0.11 (+0.16), Divine Barrier +0.10 (+0.19)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Healbane -0.00 (+0.06), Dispel Magic -0.01 (+0.04), Counterspell -0.01 (+0.03)
- **Haze**: Indomitable +0.08 (+0.19), Unstoppable +0.05 (+0.14), Plated Armor +0.05 (+0.13)
- **Holliday**: Plated Armor +0.18 (+0.27), Spellbreaker +0.07 (+0.18), Indomitable +0.04 (+0.14)
- **Bebop**: Healbane +0.00 (+0.06), Counterspell -0.02 (+0.02), Return Fire -0.02 (+0.03)
- **Calico**: Reactive Barrier +0.05 (+0.09), Divine Barrier +0.04 (+0.13), Dispel Magic +0.03 (+0.07)
- **Grey Talon**: Unstoppable +0.07 (+0.16), Spellbreaker +0.07 (+0.18), Debuff Reducer +0.06 (+0.11)
- **Mo & Krill**: Spellbreaker +0.13 (+0.24), Spirit Resilience +0.10 (+0.20), Unstoppable +0.09 (+0.18)
- **Shiv**: Bullet Resilience +0.04 (+0.09), Metal Skin +0.02 (+0.09), Divine Barrier +0.02 (+0.11)
- **Ivy**: Unstoppable +0.05 (+0.14), Indomitable +0.03 (+0.13), Debuff Reducer +0.01 (+0.06)
- **Warden**: Return Fire +0.03 (+0.08), Witchmail +0.02 (+0.17), Divine Barrier +0.02 (+0.11)
- **Yamato**: Healbane +0.05 (+0.11), Counterspell +0.00 (+0.04), Debuff Reducer -0.01 (+0.04)
- **Lash**: Spellbreaker +0.36 (+0.48), Spirit Resilience +0.36 (+0.46), Witchmail +0.21 (+0.36)
- **Viscous**: Healbane -0.01 (+0.05), Divine Barrier -0.02 (+0.07), Metal Skin -0.02 (+0.04)
- **Pocket**: Spirit Resilience +0.17 (+0.27), Witchmail +0.09 (+0.24), Spellbreaker +0.09 (+0.20)
- **Mirage**: Dispel Magic +0.28 (+0.32), Spirit Resilience +0.09 (+0.19), Metal Skin +0.08 (+0.14)
- **Vyper**: Indomitable +0.40 (+0.50), Spellbreaker +0.18 (+0.29), Reactive Barrier +0.11 (+0.14)
- **Sinclair**: Indomitable +0.08 (+0.18), Spellbreaker +0.03 (+0.14), Unstoppable +0.02 (+0.12)
- **Mina**: Return Fire +0.00 (+0.05), Dispel Magic -0.01 (+0.03), Counterspell -0.01 (+0.03)
- **Drifter**: Healbane +0.01 (+0.07), Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.04)
- **Venator**: Bullet Resilience +0.13 (+0.18), Metal Skin +0.12 (+0.18), Plated Armor +0.06 (+0.14)
- **Victor**: Spirit Resilience +0.09 (+0.19), Spellbreaker +0.08 (+0.20), Dispel Magic +0.02 (+0.06)
- **Paige**: Counterspell +0.00 (+0.04), Return Fire +0.00 (+0.05), Healbane -0.01 (+0.05)
- **The Doorman**: Indomitable +0.14 (+0.24), Spirit Resilience +0.14 (+0.24), Witchmail +0.11 (+0.26)
- **Billy**: Spirit Resilience +0.04 (+0.14), Counterspell +0.03 (+0.07), Healbane +0.03 (+0.09)
- **Graves**: Spirit Resilience +0.18 (+0.28), Metal Skin +0.16 (+0.23), Witchmail +0.14 (+0.29)
- **Apollo**: Reactive Barrier +0.03 (+0.07), Healbane +0.03 (+0.09), Counterspell +0.00 (+0.04)
- **Deadman Danny**: Spirit Resilience +0.17 (+0.27), Plated Armor +0.16 (+0.25), Indomitable +0.15 (+0.25)
- **Rem**: Debuff Reducer +0.12 (+0.17), Unstoppable +0.10 (+0.19), Spellbreaker +0.05 (+0.17)
- **Silver**: Reactive Barrier +0.05 (+0.08), Metal Skin +0.01 (+0.08), Debuff Reducer +0.00 (+0.05)
- **Celeste**: Witchmail +0.04 (+0.19), Spirit Resilience +0.03 (+0.13), Dispel Magic +0.00 (+0.05)
- **Rat King**: Bullet Resilience +0.00 (+0.05), Return Fire +0.00 (+0.05), Metal Skin -0.00 (+0.06)
- **Solomon**: Return Fire +0.01 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.02)
- **Violet**: Healbane +0.02 (+0.08), Return Fire +0.02 (+0.07), Witchmail -0.01 (+0.14)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Counterspell -0.01 (+0.03), Dispel Magic -0.02 (+0.02)
- **Baba**: Unstoppable +0.05 (+0.14), Healbane +0.02 (+0.08), Debuff Reducer +0.01 (+0.06)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.326 | +0.051 | +0.084 | Lash +0.17, Paradox +0.08, The Doorman +0.08 | 2 heroes |
| Spirit Resilience | 3,200 | +0.151 | +0.047 | +0.110 | Lash +0.31, Wraith +0.16, The Doorman +0.16 | 15 heroes |
| Dispel Magic | 3,200 | +0.092 | +0.029 | +0.053 | Mirage +0.25, Lash +0.23, Infernus +0.16 | 9 heroes |
| Indomitable | 6,400 | +0.149 | +0.024 | +0.121 | Vyper +0.37, Wraith +0.26, Sinclair +0.18 | 0 heroes |
| Witchmail | 6,400 | +0.141 | +0.022 | +0.158 | Lash +0.20, The Doorman +0.14, Wraith +0.13 | 1 heroes |
| Spellbreaker | 6,400 | +0.120 | +0.019 | +0.143 | Lash +0.28, Grey Talon +0.22, Wraith +0.20 | 0 heroes |
| Debuff Reducer | 1,600 | +0.010 | +0.006 | +0.061 | Grey Talon +0.16, Holliday +0.12, Wraith +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | -0.002 | -0.001 | +0.033 | Yamato +0.11, Wraith +0.08, Paradox +0.07 | 3 heroes |
| Plated Armor | 6,400 | -0.036 | -0.006 | +0.088 | Wraith +0.19, Yamato +0.11, Haze +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.079 | -0.012 | +0.104 | Mo & Krill +0.17, Grey Talon +0.16, Paige +0.12 | 3 heroes |
| Counterspell | 3,200 | -0.042 | -0.013 | +0.033 | Yamato +0.08, McGinnis +0.04, Vindicta +0.04 | 1 heroes |
| Bullet Resilience | 3,200 | -0.048 | -0.015 | +0.048 | Paradox +0.10, Yamato +0.07, Vindicta +0.07 | 1 heroes |
| Healbane | 1,600 | -0.045 | -0.028 | +0.062 | Yamato +0.11, Mo & Krill +0.07, Wraith +0.05 | 16 heroes |
| Metal Skin | 3,200 | -0.177 | -0.055 | +0.081 | Wraith +0.24, Lash +0.15, Shiv +0.08 | 0 heroes |
| Return Fire | 1,600 | -0.181 | -0.113 | +0.044 | Vindicta +0.07, The Doorman +0.04, Graves +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.18 (+0.32), Dispel Magic +0.16 (+0.21), Unstoppable +0.11 (+0.21)
- **Seven**: Witchmail +0.02 (+0.18), Counterspell +0.00 (+0.03), Reactive Barrier -0.02 (+0.01)
- **Vindicta**: Return Fire +0.07 (+0.12), Bullet Resilience +0.07 (+0.12), Divine Barrier +0.07 (+0.15)
- **Lady Geist**: Return Fire +0.03 (+0.08), Healbane +0.01 (+0.08), Divine Barrier +0.01 (+0.10)
- **Abrams**: Unstoppable +0.08 (+0.19), Dispel Magic +0.02 (+0.07), Spirit Resilience +0.00 (+0.11)
- **Wraith**: Indomitable +0.26 (+0.38), Metal Skin +0.24 (+0.32), Spellbreaker +0.20 (+0.35)
- **McGinnis**: Spirit Resilience +0.13 (+0.24), Witchmail +0.07 (+0.22), Bullet Resilience +0.05 (+0.10)
- **Paradox**: Witchmail +0.11 (+0.26), Bullet Resilience +0.10 (+0.14), Spirit Resilience +0.09 (+0.20)
- **Dynamo**: Healbane -0.00 (+0.06), Counterspell -0.00 (+0.03), Return Fire -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.01 (+0.12), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03)
- **Haze**: Plated Armor +0.07 (+0.16), Indomitable +0.05 (+0.17), Bullet Resilience +0.04 (+0.09)
- **Holliday**: Debuff Reducer +0.12 (+0.18), Spellbreaker +0.11 (+0.26), Unstoppable +0.08 (+0.19)
- **Bebop**: Healbane +0.03 (+0.09), Return Fire -0.00 (+0.04), Metal Skin -0.01 (+0.07)
- **Calico**: Spirit Resilience +0.09 (+0.20), Reactive Barrier +0.06 (+0.09), Divine Barrier +0.04 (+0.12)
- **Grey Talon**: Spellbreaker +0.22 (+0.36), Unstoppable +0.16 (+0.27), Debuff Reducer +0.16 (+0.22)
- **Mo & Krill**: Unstoppable +0.17 (+0.28), Spellbreaker +0.15 (+0.29), Debuff Reducer +0.07 (+0.13)
- **Shiv**: Metal Skin +0.08 (+0.16), Bullet Resilience +0.07 (+0.12), Divine Barrier +0.04 (+0.13)
- **Ivy**: Unstoppable +0.06 (+0.16), Indomitable +0.02 (+0.14), Bullet Resilience -0.00 (+0.05)
- **Warden**: Return Fire +0.02 (+0.06), Debuff Reducer +0.01 (+0.07), Counterspell -0.00 (+0.03)
- **Yamato**: Indomitable +0.17 (+0.30), Reactive Barrier +0.11 (+0.14), Healbane +0.11 (+0.17)
- **Lash**: Spirit Resilience +0.31 (+0.42), Spellbreaker +0.28 (+0.42), Dispel Magic +0.23 (+0.28)
- **Viscous**: Divine Barrier +0.06 (+0.14), Return Fire +0.03 (+0.07), Healbane -0.00 (+0.06)
- **Pocket**: Spirit Resilience +0.09 (+0.20), Witchmail +0.02 (+0.18), Return Fire +0.00 (+0.04)
- **Mirage**: Dispel Magic +0.25 (+0.31), Spirit Resilience +0.04 (+0.15), Plated Armor +0.02 (+0.11)
- **Vyper**: Indomitable +0.37 (+0.49), Spellbreaker +0.13 (+0.27), Debuff Reducer +0.11 (+0.17)
- **Sinclair**: Indomitable +0.18 (+0.30), Spellbreaker +0.11 (+0.26), Unstoppable +0.06 (+0.17)
- **Mina**: Divine Barrier +0.05 (+0.14), Witchmail +0.05 (+0.20), Spirit Resilience +0.04 (+0.15)
- **Drifter**: Witchmail +0.03 (+0.19), Healbane +0.02 (+0.08), Counterspell +0.01 (+0.04)
- **Venator**: Metal Skin +0.07 (+0.16), Bullet Resilience +0.07 (+0.11), Plated Armor +0.03 (+0.11)
- **Victor**: Spirit Resilience +0.04 (+0.15), Healbane +0.04 (+0.10), Spellbreaker -0.01 (+0.13)
- **Paige**: Unstoppable +0.12 (+0.22), Debuff Reducer +0.11 (+0.17), Spellbreaker +0.03 (+0.18)
- **The Doorman**: Indomitable +0.16 (+0.28), Spirit Resilience +0.16 (+0.27), Witchmail +0.14 (+0.30)
- **Billy**: Indomitable +0.08 (+0.20), Reactive Barrier +0.03 (+0.06), Debuff Reducer +0.03 (+0.09)
- **Graves**: Return Fire +0.04 (+0.08), Witchmail +0.02 (+0.17), Metal Skin +0.01 (+0.09)
- **Apollo**: Healbane +0.00 (+0.07), Reactive Barrier -0.00 (+0.03), Counterspell -0.01 (+0.02)
- **Deadman Danny**: Indomitable +0.08 (+0.20), Spellbreaker +0.08 (+0.22), Spirit Resilience +0.06 (+0.17)
- **Rem**: Debuff Reducer +0.10 (+0.16), Unstoppable +0.09 (+0.19), Spellbreaker +0.04 (+0.18)
- **Silver**: Dispel Magic +0.07 (+0.12), Reactive Barrier +0.03 (+0.07), Bullet Resilience +0.03 (+0.08)
- **Celeste**: Witchmail +0.05 (+0.21), Dispel Magic +0.04 (+0.10), Reactive Barrier +0.02 (+0.05)
- **Rat King**: Bullet Resilience -0.00 (+0.05), Return Fire -0.00 (+0.04), Counterspell -0.01 (+0.02)
- **Solomon**: Counterspell -0.00 (+0.03), Return Fire -0.01 (+0.03), Reactive Barrier -0.02 (+0.02)
- **Violet**: Witchmail +0.02 (+0.18), Healbane +0.01 (+0.08), Return Fire +0.01 (+0.06)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Counterspell -0.00 (+0.03), Dispel Magic -0.03 (+0.02)
- **Baba**: Unstoppable +0.01 (+0.12), Healbane +0.01 (+0.07), Return Fire +0.00 (+0.04)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.188 | +0.059 | +0.153 | Lash +0.56, The Doorman +0.49, Grey Talon +0.30 | 15 heroes |
| Divine Barrier | 6,400 | +0.214 | +0.034 | +0.087 | Viscous +0.25, Lash +0.21, The Doorman +0.12 | 3 heroes |
| Dispel Magic | 3,200 | +0.095 | +0.030 | +0.052 | Mirage +0.28, Lash +0.22, Silver +0.15 | 9 heroes |
| Indomitable | 6,400 | +0.169 | +0.027 | +0.154 | Wraith +0.37, Vyper +0.24, The Doorman +0.24 | 1 heroes |
| Spellbreaker | 6,400 | +0.154 | +0.024 | +0.195 | Lash +0.37, Grey Talon +0.28, Wraith +0.26 | 0 heroes |
| Witchmail | 6,400 | +0.143 | +0.022 | +0.168 | Lash +0.26, The Doorman +0.20, Deadman Danny +0.20 | 2 heroes |
| Debuff Reducer | 1,600 | +0.013 | +0.008 | +0.088 | Paige +0.19, Holliday +0.16, Wraith +0.14 | 0 heroes |
| Plated Armor | 6,400 | -0.040 | -0.006 | +0.098 | Holliday +0.20, Wraith +0.14, Grey Talon +0.11 | 2 heroes |
| Unstoppable | 6,400 | -0.061 | -0.009 | +0.151 | Paige +0.27, Haze +0.20, Grey Talon +0.17 | 8 heroes |
| Reactive Barrier | 1,600 | -0.015 | -0.009 | +0.036 | Yamato +0.12, Paradox +0.09, Wraith +0.07 | 3 heroes |
| Counterspell | 3,200 | -0.046 | -0.014 | +0.029 | Viscous +0.05, Nurse Harrow +0.04, Lash +0.03 | 1 heroes |
| Bullet Resilience | 3,200 | -0.047 | -0.015 | +0.051 | Venator +0.11, Lash +0.09, Vindicta +0.08 | 0 heroes |
| Healbane | 1,600 | -0.049 | -0.030 | +0.056 | Nurse Harrow +0.05, Lash +0.05, Victor +0.05 | 14 heroes |
| Metal Skin | 3,200 | -0.169 | -0.053 | +0.098 | Wraith +0.25, Lash +0.21, Viscous +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.175 | -0.109 | +0.043 | Violet +0.07, Paradox +0.06, Lash +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.31), Dispel Magic +0.14 (+0.19), Spellbreaker +0.11 (+0.31)
- **Seven**: Witchmail +0.04 (+0.21), Counterspell +0.00 (+0.03), Healbane -0.01 (+0.04)
- **Vindicta**: Divine Barrier +0.08 (+0.17), Plated Armor +0.08 (+0.18), Bullet Resilience +0.08 (+0.13)
- **Lady Geist**: Bullet Resilience +0.04 (+0.09), Counterspell +0.03 (+0.05), Healbane +0.01 (+0.07)
- **Abrams**: Unstoppable +0.03 (+0.18), Dispel Magic +0.02 (+0.08), Reactive Barrier +0.01 (+0.05)
- **Wraith**: Indomitable +0.37 (+0.52), Spellbreaker +0.26 (+0.45), Metal Skin +0.25 (+0.34)
- **McGinnis**: Spirit Resilience +0.13 (+0.28), Witchmail +0.05 (+0.22), Spellbreaker +0.02 (+0.22)
- **Paradox**: Unstoppable +0.16 (+0.31), Dispel Magic +0.15 (+0.20), Witchmail +0.14 (+0.31)
- **Dynamo**: Counterspell -0.01 (+0.02), Healbane -0.02 (+0.04), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.14 (+0.29), Spellbreaker +0.01 (+0.20), Witchmail +0.01 (+0.18)
- **Haze**: Unstoppable +0.20 (+0.35), Return Fire +0.05 (+0.09), Bullet Resilience +0.03 (+0.08)
- **Holliday**: Plated Armor +0.20 (+0.30), Debuff Reducer +0.16 (+0.25), Spellbreaker +0.15 (+0.34)
- **Bebop**: Debuff Reducer +0.11 (+0.20), Unstoppable +0.04 (+0.19), Spellbreaker +0.01 (+0.21)
- **Calico**: Spirit Resilience +0.12 (+0.27), Divine Barrier +0.11 (+0.20), Reactive Barrier +0.07 (+0.11)
- **Grey Talon**: Spirit Resilience +0.30 (+0.45), Spellbreaker +0.28 (+0.47), Unstoppable +0.17 (+0.33)
- **Mo & Krill**: Healbane +0.05 (+0.10), Dispel Magic +0.04 (+0.09), Spellbreaker +0.03 (+0.23)
- **Shiv**: Metal Skin +0.05 (+0.15), Bullet Resilience +0.05 (+0.10), Plated Armor +0.04 (+0.13)
- **Ivy**: Unstoppable +0.01 (+0.16), Healbane +0.00 (+0.06), Bullet Resilience -0.01 (+0.04)
- **Warden**: Divine Barrier +0.02 (+0.10), Bullet Resilience +0.01 (+0.06), Return Fire -0.00 (+0.04)
- **Yamato**: Reactive Barrier +0.12 (+0.16), Indomitable +0.09 (+0.24), Metal Skin +0.07 (+0.17)
- **Lash**: Spirit Resilience +0.56 (+0.71), Spellbreaker +0.37 (+0.57), Witchmail +0.26 (+0.43)
- **Viscous**: Spirit Resilience +0.27 (+0.42), Divine Barrier +0.25 (+0.33), Witchmail +0.17 (+0.34)
- **Pocket**: Spirit Resilience +0.06 (+0.21), Return Fire -0.00 (+0.04), Counterspell -0.01 (+0.02)
- **Mirage**: Dispel Magic +0.28 (+0.33), Metal Skin +0.08 (+0.18), Plated Armor +0.03 (+0.13)
- **Vyper**: Indomitable +0.24 (+0.39), Plated Armor +0.05 (+0.14), Bullet Resilience +0.02 (+0.07)
- **Sinclair**: Indomitable +0.17 (+0.32), Spellbreaker +0.14 (+0.33), Spirit Resilience +0.08 (+0.23)
- **Mina**: Divine Barrier +0.03 (+0.12), Counterspell +0.00 (+0.03), Spirit Resilience +0.00 (+0.15)
- **Drifter**: Indomitable +0.12 (+0.28), Reactive Barrier +0.05 (+0.09), Debuff Reducer +0.04 (+0.13)
- **Venator**: Metal Skin +0.13 (+0.23), Bullet Resilience +0.11 (+0.16), Plated Armor +0.06 (+0.16)
- **Victor**: Healbane +0.05 (+0.10), Spirit Resilience +0.02 (+0.17), Spellbreaker -0.01 (+0.19)
- **Paige**: Unstoppable +0.27 (+0.42), Debuff Reducer +0.19 (+0.28), Spellbreaker +0.09 (+0.28)
- **The Doorman**: Spirit Resilience +0.49 (+0.64), Indomitable +0.24 (+0.39), Witchmail +0.20 (+0.37)
- **Billy**: Reactive Barrier +0.06 (+0.09), Healbane +0.01 (+0.06), Indomitable -0.00 (+0.15)
- **Graves**: Metal Skin +0.04 (+0.13), Healbane +0.03 (+0.08), Spirit Resilience +0.02 (+0.17)
- **Apollo**: Reactive Barrier +0.04 (+0.07), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.27 (+0.42), Witchmail +0.20 (+0.37), Spellbreaker +0.16 (+0.36)
- **Rem**: Debuff Reducer +0.06 (+0.15), Unstoppable +0.01 (+0.16), Healbane -0.00 (+0.06)
- **Silver**: Dispel Magic +0.15 (+0.21), Metal Skin +0.14 (+0.24), Indomitable +0.11 (+0.27)
- **Celeste**: Witchmail +0.08 (+0.25), Spirit Resilience +0.04 (+0.19), Healbane +0.03 (+0.09)
- **Rat King**: Return Fire +0.00 (+0.05), Debuff Reducer +0.00 (+0.09), Counterspell -0.01 (+0.02)
- **Solomon**: Counterspell +0.00 (+0.03), Reactive Barrier -0.01 (+0.02), Return Fire -0.02 (+0.02)
- **Violet**: Return Fire +0.07 (+0.11), Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Nurse Harrow**: Divine Barrier +0.09 (+0.17), Witchmail +0.07 (+0.24), Healbane +0.05 (+0.11)
- **Baba**: Healbane +0.01 (+0.06), Counterspell +0.01 (+0.03), Witchmail -0.01 (+0.16)
