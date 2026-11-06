# Counter items in the sim (phantom and up)

Built 2026-11-06T22:54:20Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.192 | +0.060 | +0.128 | Lash +0.27, The Doorman +0.15, Victor +0.14 | 1 heroes |
| Divine Barrier | 6,400 | +0.303 | +0.048 | +0.133 | Lash +0.20, The Doorman +0.13, Graves +0.09 | 0 heroes |
| Indomitable | 6,400 | +0.181 | +0.029 | +0.153 | Vyper +0.33, The Doorman +0.21, Abrams +0.19 | 0 heroes |
| Reactive Barrier | 1,600 | +0.045 | +0.028 | +0.053 | Deadman Danny +0.13, The Doorman +0.12, Graves +0.11 | 2 heroes |
| Dispel Magic | 3,200 | +0.089 | +0.028 | +0.085 | Mirage +0.40, Lash +0.17, Paradox +0.09 | 4 heroes |
| Healbane | 1,600 | +0.040 | +0.025 | +0.089 | Graves +0.10, Yamato +0.06, Billy +0.06 | 21 heroes |
| Bullet Resilience | 3,200 | +0.061 | +0.019 | +0.103 | Venator +0.23, Lash +0.18, Paradox +0.13 | 0 heroes |
| Debuff Reducer | 1,600 | +0.025 | +0.015 | +0.080 | Holliday +0.11, Vyper +0.11, Lash +0.08 | 0 heroes |
| Witchmail | 6,400 | +0.097 | +0.015 | +0.199 | Lash +0.21, The Doorman +0.17, Deadman Danny +0.15 | 0 heroes |
| Spellbreaker | 6,400 | +0.089 | +0.014 | +0.171 | Lash +0.25, The Doorman +0.15, Deadman Danny +0.15 | 0 heroes |
| Plated Armor | 6,400 | +0.009 | +0.001 | +0.136 | Holliday +0.21, Lash +0.15, Deadman Danny +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.002 | -0.001 | +0.074 | Lash +0.09, Graves +0.09, Deadman Danny +0.06 | 0 heroes |
| Unstoppable | 6,400 | -0.049 | -0.008 | +0.138 | Lash +0.13, Deadman Danny +0.13, Vyper +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.172 | -0.054 | +0.110 | Lash +0.19, Paradox +0.14, Wraith +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.173 | -0.108 | +0.086 | Paradox +0.10, Deadman Danny +0.08, Lash +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.05 (+0.14), Spellbreaker +0.04 (+0.21), Healbane +0.04 (+0.13)
- **Seven**: Healbane -0.01 (+0.08), Witchmail -0.03 (+0.17), Counterspell -0.03 (+0.04)
- **Vindicta**: Divine Barrier +0.00 (+0.14), Counterspell -0.00 (+0.07), Witchmail -0.01 (+0.19)
- **Lady Geist**: Return Fire -0.00 (+0.09), Healbane -0.02 (+0.07), Counterspell -0.02 (+0.05)
- **Abrams**: Indomitable +0.19 (+0.34), Reactive Barrier +0.09 (+0.14), Divine Barrier +0.08 (+0.21)
- **Wraith**: Indomitable +0.16 (+0.31), Metal Skin +0.13 (+0.24), Spellbreaker +0.10 (+0.27)
- **McGinnis**: Counterspell +0.03 (+0.10), Spirit Resilience +0.01 (+0.14), Healbane +0.01 (+0.10)
- **Paradox**: Metal Skin +0.14 (+0.25), Bullet Resilience +0.13 (+0.23), Return Fire +0.10 (+0.18)
- **Dynamo**: Healbane -0.00 (+0.09), Counterspell -0.03 (+0.04), Reactive Barrier -0.04 (+0.01)
- **Kelvin**: Healbane -0.01 (+0.08), Counterspell -0.01 (+0.06), Witchmail -0.01 (+0.19)
- **Haze**: Indomitable +0.11 (+0.27), Plated Armor +0.10 (+0.23), Unstoppable +0.07 (+0.21)
- **Holliday**: Plated Armor +0.21 (+0.34), Spellbreaker +0.13 (+0.30), Debuff Reducer +0.11 (+0.19)
- **Bebop**: Healbane +0.01 (+0.10), Counterspell +0.00 (+0.08), Divine Barrier -0.01 (+0.13)
- **Calico**: Spellbreaker +0.09 (+0.26), Divine Barrier +0.08 (+0.21), Spirit Resilience +0.06 (+0.19)
- **Grey Talon**: Unstoppable +0.08 (+0.22), Reactive Barrier +0.07 (+0.12), Spellbreaker +0.06 (+0.24)
- **Mo & Krill**: Spellbreaker +0.10 (+0.27), Spirit Resilience +0.05 (+0.18), Witchmail +0.04 (+0.24)
- **Shiv**: Return Fire -0.01 (+0.07), Healbane -0.01 (+0.08), Spirit Resilience -0.02 (+0.10)
- **Ivy**: Indomitable +0.08 (+0.23), Unstoppable +0.05 (+0.19), Debuff Reducer +0.01 (+0.09)
- **Warden**: Return Fire -0.00 (+0.08), Debuff Reducer -0.00 (+0.08), Counterspell -0.01 (+0.06)
- **Yamato**: Healbane +0.06 (+0.15), Debuff Reducer +0.04 (+0.12), Spellbreaker +0.02 (+0.19)
- **Lash**: Spirit Resilience +0.27 (+0.40), Spellbreaker +0.25 (+0.43), Witchmail +0.21 (+0.41)
- **Viscous**: Divine Barrier +0.03 (+0.16), Return Fire +0.03 (+0.12), Counterspell +0.02 (+0.09)
- **Pocket**: Dispel Magic +0.08 (+0.17), Spirit Resilience +0.07 (+0.20), Witchmail +0.07 (+0.27)
- **Mirage**: Dispel Magic +0.40 (+0.48), Spirit Resilience +0.10 (+0.23), Spellbreaker +0.10 (+0.27)
- **Vyper**: Indomitable +0.33 (+0.48), Debuff Reducer +0.11 (+0.19), Spellbreaker +0.10 (+0.28)
- **Sinclair**: Spellbreaker +0.05 (+0.22), Indomitable +0.01 (+0.17), Debuff Reducer -0.01 (+0.07)
- **Mina**: Return Fire +0.00 (+0.09), Spirit Resilience -0.00 (+0.13), Spellbreaker -0.01 (+0.16)
- **Drifter**: Counterspell -0.01 (+0.06), Return Fire -0.02 (+0.07), Healbane -0.02 (+0.07)
- **Venator**: Bullet Resilience +0.23 (+0.33), Divine Barrier +0.09 (+0.22), Plated Armor +0.09 (+0.22)
- **Victor**: Spirit Resilience +0.14 (+0.26), Spellbreaker +0.11 (+0.29), Witchmail +0.03 (+0.23)
- **Paige**: Return Fire -0.02 (+0.07), Counterspell -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **The Doorman**: Indomitable +0.21 (+0.36), Witchmail +0.17 (+0.37), Spirit Resilience +0.15 (+0.28)
- **Billy**: Healbane +0.06 (+0.15), Spirit Resilience +0.05 (+0.18), Spellbreaker +0.04 (+0.21)
- **Graves**: Witchmail +0.11 (+0.31), Reactive Barrier +0.11 (+0.16), Metal Skin +0.10 (+0.21)
- **Apollo**: Reactive Barrier +0.01 (+0.06), Indomitable -0.00 (+0.15), Unstoppable -0.01 (+0.13)
- **Deadman Danny**: Indomitable +0.17 (+0.32), Spellbreaker +0.15 (+0.32), Witchmail +0.15 (+0.34)
- **Rem**: Reactive Barrier -0.01 (+0.04), Healbane -0.02 (+0.07), Dispel Magic -0.02 (+0.06)
- **Silver**: Dispel Magic +0.08 (+0.17), Indomitable +0.05 (+0.20), Reactive Barrier +0.01 (+0.07)
- **Celeste**: Spirit Resilience +0.13 (+0.26), Witchmail +0.11 (+0.31), Plated Armor +0.05 (+0.18)
- **Rat King**: Return Fire +0.00 (+0.09), Counterspell -0.01 (+0.06), Divine Barrier -0.01 (+0.12)
- **Solomon**: Counterspell -0.03 (+0.05), Reactive Barrier -0.03 (+0.02), Healbane -0.04 (+0.05)
- **Violet**: Unstoppable +0.04 (+0.18), Witchmail +0.03 (+0.23), Return Fire +0.02 (+0.11)
- **Nurse Harrow**: Healbane +0.04 (+0.13), Witchmail -0.02 (+0.18), Reactive Barrier -0.02 (+0.03)
- **Baba**: Healbane -0.01 (+0.08), Reactive Barrier -0.02 (+0.03), Counterspell -0.03 (+0.05)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.185 | +0.058 | +0.132 | Lash +0.42, Pocket +0.21, Wraith +0.15 | 10 heroes |
| Divine Barrier | 6,400 | +0.230 | +0.037 | +0.099 | Lash +0.26, The Doorman +0.12, Paradox +0.08 | 0 heroes |
| Indomitable | 6,400 | +0.171 | +0.027 | +0.129 | Vyper +0.42, Wraith +0.20, The Doorman +0.17 | 0 heroes |
| Dispel Magic | 3,200 | +0.078 | +0.024 | +0.057 | Mirage +0.31, Silver +0.09, Lash +0.08 | 9 heroes |
| Spellbreaker | 6,400 | +0.124 | +0.019 | +0.157 | Lash +0.36, Holliday +0.16, Wraith +0.12 | 0 heroes |
| Healbane | 1,600 | +0.030 | +0.019 | +0.066 | Lady Geist +0.09, Yamato +0.08, Infernus +0.05 | 25 heroes |
| Reactive Barrier | 1,600 | +0.029 | +0.018 | +0.035 | The Doorman +0.13, Calico +0.09, Paradox +0.06 | 3 heroes |
| Witchmail | 6,400 | +0.111 | +0.017 | +0.177 | Lash +0.27, Wraith +0.13, The Doorman +0.11 | 1 heroes |
| Bullet Resilience | 3,200 | +0.027 | +0.009 | +0.074 | Venator +0.21, Lash +0.12, Paradox +0.09 | 0 heroes |
| Plated Armor | 6,400 | +0.015 | +0.002 | +0.105 | Holliday +0.19, Wraith +0.16, Venator +0.09 | 0 heroes |
| Debuff Reducer | 1,600 | +0.002 | +0.002 | +0.064 | Holliday +0.15, Rem +0.12, Vyper +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.019 | -0.006 | +0.040 | Lash +0.05, Paradox +0.05, Vyper +0.02 | 1 heroes |
| Unstoppable | 6,400 | -0.076 | -0.012 | +0.110 | Holliday +0.14, Rem +0.11, Abrams +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.192 | -0.060 | +0.090 | Wraith +0.27, Lash +0.17, Venator +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.183 | -0.115 | +0.059 | Paradox +0.08, The Doorman +0.07, Lash +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.07 (+0.22), Dispel Magic +0.06 (+0.12), Unstoppable +0.06 (+0.17)
- **Seven**: Witchmail +0.06 (+0.24), Healbane +0.02 (+0.09), Spirit Resilience -0.00 (+0.13)
- **Vindicta**: Divine Barrier +0.05 (+0.15), Return Fire +0.05 (+0.11), Witchmail +0.03 (+0.21)
- **Lady Geist**: Spirit Resilience +0.12 (+0.25), Healbane +0.09 (+0.15), Spellbreaker +0.09 (+0.24)
- **Abrams**: Indomitable +0.10 (+0.23), Unstoppable +0.10 (+0.21), Dispel Magic +0.07 (+0.13)
- **Wraith**: Metal Skin +0.27 (+0.36), Indomitable +0.20 (+0.33), Plated Armor +0.16 (+0.26)
- **McGinnis**: Spirit Resilience +0.01 (+0.14), Healbane -0.02 (+0.05), Counterspell -0.02 (+0.02)
- **Paradox**: Bullet Resilience +0.09 (+0.16), Divine Barrier +0.08 (+0.18), Return Fire +0.08 (+0.14)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.03 (+0.16), Healbane -0.01 (+0.06), Witchmail -0.01 (+0.17)
- **Haze**: Indomitable +0.08 (+0.21), Plated Armor +0.08 (+0.19), Bullet Resilience +0.06 (+0.13)
- **Holliday**: Plated Armor +0.19 (+0.29), Spellbreaker +0.16 (+0.32), Debuff Reducer +0.15 (+0.22)
- **Bebop**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.03), Return Fire -0.02 (+0.04)
- **Calico**: Reactive Barrier +0.09 (+0.12), Divine Barrier +0.04 (+0.14), Dispel Magic +0.03 (+0.08)
- **Grey Talon**: Unstoppable +0.09 (+0.20), Debuff Reducer +0.05 (+0.12), Spellbreaker +0.05 (+0.20)
- **Mo & Krill**: Spellbreaker +0.10 (+0.26), Unstoppable +0.08 (+0.19), Dispel Magic +0.05 (+0.11)
- **Shiv**: Bullet Resilience +0.06 (+0.13), Return Fire +0.02 (+0.08), Metal Skin +0.02 (+0.11)
- **Ivy**: Unstoppable +0.08 (+0.19), Indomitable +0.05 (+0.18), Debuff Reducer +0.01 (+0.08)
- **Warden**: Return Fire +0.04 (+0.10), Divine Barrier +0.02 (+0.11), Debuff Reducer +0.01 (+0.07)
- **Yamato**: Healbane +0.08 (+0.14), Debuff Reducer +0.06 (+0.12), Unstoppable +0.04 (+0.15)
- **Lash**: Spirit Resilience +0.42 (+0.55), Spellbreaker +0.36 (+0.52), Witchmail +0.27 (+0.44)
- **Viscous**: Divine Barrier +0.02 (+0.12), Counterspell +0.01 (+0.05), Healbane -0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.21 (+0.34), Witchmail +0.09 (+0.27), Spellbreaker +0.08 (+0.23)
- **Mirage**: Dispel Magic +0.31 (+0.37), Spirit Resilience +0.06 (+0.19), Spellbreaker +0.04 (+0.20)
- **Vyper**: Indomitable +0.42 (+0.54), Spellbreaker +0.11 (+0.27), Debuff Reducer +0.10 (+0.17)
- **Sinclair**: Indomitable +0.05 (+0.18), Return Fire +0.00 (+0.06), Debuff Reducer +0.00 (+0.07)
- **Mina**: Counterspell +0.02 (+0.06), Return Fire +0.01 (+0.07), Divine Barrier -0.01 (+0.09)
- **Drifter**: Healbane +0.01 (+0.08), Counterspell -0.00 (+0.04), Return Fire -0.03 (+0.03)
- **Venator**: Bullet Resilience +0.21 (+0.29), Metal Skin +0.11 (+0.20), Plated Armor +0.09 (+0.20)
- **Victor**: Spellbreaker +0.06 (+0.22), Spirit Resilience +0.06 (+0.19), Healbane +0.01 (+0.08)
- **Paige**: Counterspell +0.01 (+0.05), Return Fire -0.01 (+0.05), Healbane -0.01 (+0.05)
- **The Doorman**: Indomitable +0.17 (+0.30), Reactive Barrier +0.13 (+0.17), Spirit Resilience +0.13 (+0.26)
- **Billy**: Healbane +0.01 (+0.08), Spirit Resilience +0.01 (+0.14), Counterspell -0.00 (+0.04)
- **Graves**: Metal Skin +0.06 (+0.15), Reactive Barrier +0.06 (+0.09), Witchmail +0.05 (+0.23)
- **Apollo**: Reactive Barrier +0.06 (+0.09), Indomitable +0.05 (+0.18), Unstoppable +0.00 (+0.12)
- **Deadman Danny**: Indomitable +0.12 (+0.25), Spirit Resilience +0.10 (+0.24), Witchmail +0.09 (+0.27)
- **Rem**: Debuff Reducer +0.12 (+0.18), Unstoppable +0.11 (+0.22), Spellbreaker +0.04 (+0.20)
- **Silver**: Dispel Magic +0.09 (+0.14), Indomitable +0.05 (+0.17), Reactive Barrier +0.03 (+0.07)
- **Celeste**: Spirit Resilience +0.08 (+0.21), Witchmail +0.08 (+0.26), Dispel Magic +0.06 (+0.12)
- **Rat King**: Return Fire +0.03 (+0.09), Bullet Resilience +0.02 (+0.10), Counterspell +0.01 (+0.05)
- **Solomon**: Counterspell -0.01 (+0.03), Healbane -0.02 (+0.05), Reactive Barrier -0.02 (+0.02)
- **Violet**: Unstoppable +0.04 (+0.15), Return Fire +0.01 (+0.07), Healbane +0.01 (+0.08)
- **Nurse Harrow**: Healbane +0.04 (+0.11), Counterspell -0.00 (+0.04), Divine Barrier -0.01 (+0.09)
- **Baba**: Unstoppable +0.01 (+0.12), Healbane -0.00 (+0.06), Debuff Reducer -0.01 (+0.06)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.172 | +0.054 | +0.141 | Lash +0.30, Deadman Danny +0.27, Wraith +0.17 | 14 heroes |
| Divine Barrier | 6,400 | +0.176 | +0.028 | +0.089 | Viscous +0.11, Lash +0.10, Vindicta +0.09 | 2 heroes |
| Indomitable | 6,400 | +0.169 | +0.027 | +0.128 | Vyper +0.36, Wraith +0.26, Deadman Danny +0.19 | 0 heroes |
| Dispel Magic | 3,200 | +0.083 | +0.026 | +0.053 | Mirage +0.23, Paradox +0.12, Lash +0.11 | 11 heroes |
| Spellbreaker | 6,400 | +0.138 | +0.021 | +0.164 | Lash +0.31, Deadman Danny +0.21, Wraith +0.18 | 0 heroes |
| Healbane | 1,600 | +0.027 | +0.017 | +0.058 | Mo & Krill +0.08, Infernus +0.06, Nurse Harrow +0.05 | 24 heroes |
| Witchmail | 6,400 | +0.100 | +0.016 | +0.172 | Deadman Danny +0.16, Wraith +0.16, Lash +0.13 | 1 heroes |
| Bullet Resilience | 3,200 | +0.018 | +0.006 | +0.058 | Venator +0.15, Vindicta +0.12, Haze +0.07 | 1 heroes |
| Plated Armor | 6,400 | +0.013 | +0.002 | +0.093 | Holliday +0.20, Wraith +0.14, Vindicta +0.08 | 0 heroes |
| Reactive Barrier | 1,600 | +0.002 | +0.001 | +0.031 | Wraith +0.09, Graves +0.09, Paradox +0.09 | 2 heroes |
| Debuff Reducer | 1,600 | +0.002 | +0.001 | +0.064 | Holliday +0.18, Grey Talon +0.15, Wraith +0.11 | 0 heroes |
| Counterspell | 3,200 | -0.025 | -0.008 | +0.033 | Graves +0.07, Vindicta +0.02, Paradox +0.02 | 1 heroes |
| Unstoppable | 6,400 | -0.073 | -0.011 | +0.113 | Mo & Krill +0.25, Grey Talon +0.16, Holliday +0.15 | 3 heroes |
| Metal Skin | 3,200 | -0.191 | -0.060 | +0.083 | Wraith +0.21, Lash +0.10, Paradox +0.08 | 0 heroes |
| Return Fire | 1,600 | -0.177 | -0.111 | +0.055 | Graves +0.10, Venator +0.07, Vindicta +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.17), Spellbreaker +0.10 (+0.26), Unstoppable +0.06 (+0.18)
- **Seven**: Witchmail +0.07 (+0.24), Indomitable +0.03 (+0.16), Healbane +0.01 (+0.07)
- **Vindicta**: Bullet Resilience +0.12 (+0.18), Divine Barrier +0.09 (+0.17), Plated Armor +0.08 (+0.17)
- **Lady Geist**: Healbane +0.03 (+0.09), Return Fire -0.00 (+0.05), Counterspell -0.02 (+0.01)
- **Abrams**: Unstoppable +0.08 (+0.20), Dispel Magic +0.05 (+0.10), Counterspell +0.02 (+0.05)
- **Wraith**: Indomitable +0.26 (+0.39), Metal Skin +0.21 (+0.29), Spellbreaker +0.18 (+0.34)
- **McGinnis**: Spirit Resilience +0.04 (+0.18), Witchmail +0.03 (+0.20), Healbane -0.00 (+0.05)
- **Paradox**: Dispel Magic +0.12 (+0.17), Spirit Resilience +0.10 (+0.24), Reactive Barrier +0.09 (+0.12)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (-0.00)
- **Kelvin**: Spirit Resilience +0.06 (+0.20), Dispel Magic +0.06 (+0.11), Witchmail +0.01 (+0.18)
- **Haze**: Indomitable +0.14 (+0.26), Unstoppable +0.13 (+0.24), Bullet Resilience +0.07 (+0.13)
- **Holliday**: Plated Armor +0.20 (+0.30), Debuff Reducer +0.18 (+0.24), Spellbreaker +0.17 (+0.34)
- **Bebop**: Healbane +0.03 (+0.09), Metal Skin +0.01 (+0.10), Return Fire -0.00 (+0.05)
- **Calico**: Spirit Resilience +0.08 (+0.22), Indomitable +0.06 (+0.18), Divine Barrier +0.05 (+0.14)
- **Grey Talon**: Unstoppable +0.16 (+0.27), Spellbreaker +0.15 (+0.32), Debuff Reducer +0.15 (+0.21)
- **Mo & Krill**: Unstoppable +0.25 (+0.36), Spellbreaker +0.13 (+0.30), Spirit Resilience +0.11 (+0.25)
- **Shiv**: Bullet Resilience +0.06 (+0.12), Divine Barrier +0.03 (+0.12), Plated Armor +0.02 (+0.12)
- **Ivy**: Unstoppable +0.02 (+0.13), Healbane +0.00 (+0.06), Indomitable +0.00 (+0.13)
- **Warden**: Debuff Reducer +0.01 (+0.08), Return Fire +0.01 (+0.07), Bullet Resilience -0.00 (+0.06)
- **Yamato**: Witchmail +0.05 (+0.22), Spellbreaker +0.04 (+0.21), Spirit Resilience +0.02 (+0.16)
- **Lash**: Spellbreaker +0.31 (+0.48), Spirit Resilience +0.30 (+0.45), Witchmail +0.13 (+0.30)
- **Viscous**: Spirit Resilience +0.13 (+0.28), Divine Barrier +0.11 (+0.20), Spellbreaker +0.07 (+0.23)
- **Pocket**: Spirit Resilience +0.12 (+0.26), Witchmail +0.07 (+0.24), Counterspell +0.01 (+0.04)
- **Mirage**: Dispel Magic +0.23 (+0.28), Debuff Reducer +0.01 (+0.08), Plated Armor +0.01 (+0.10)
- **Vyper**: Indomitable +0.36 (+0.48), Spellbreaker +0.09 (+0.26), Debuff Reducer +0.07 (+0.14)
- **Sinclair**: Indomitable +0.13 (+0.26), Unstoppable +0.05 (+0.16), Debuff Reducer +0.04 (+0.10)
- **Mina**: Divine Barrier +0.07 (+0.16), Spirit Resilience +0.05 (+0.19), Witchmail +0.03 (+0.20)
- **Drifter**: Witchmail +0.04 (+0.21), Debuff Reducer -0.00 (+0.06), Metal Skin -0.00 (+0.08)
- **Venator**: Bullet Resilience +0.15 (+0.20), Metal Skin +0.08 (+0.16), Return Fire +0.07 (+0.13)
- **Victor**: Spellbreaker +0.04 (+0.21), Spirit Resilience +0.00 (+0.14), Healbane -0.01 (+0.05)
- **Paige**: Counterspell +0.00 (+0.04), Divine Barrier -0.01 (+0.08), Return Fire -0.01 (+0.04)
- **The Doorman**: Indomitable +0.13 (+0.25), Witchmail +0.10 (+0.27), Divine Barrier +0.05 (+0.14)
- **Billy**: Healbane +0.01 (+0.07), Counterspell -0.02 (+0.01), Return Fire -0.02 (+0.03)
- **Graves**: Return Fire +0.10 (+0.15), Reactive Barrier +0.09 (+0.12), Divine Barrier +0.08 (+0.17)
- **Apollo**: Healbane +0.03 (+0.09), Reactive Barrier -0.01 (+0.03), Counterspell -0.01 (+0.03)
- **Deadman Danny**: Spirit Resilience +0.27 (+0.41), Spellbreaker +0.21 (+0.37), Indomitable +0.19 (+0.31)
- **Rem**: Debuff Reducer +0.09 (+0.16), Unstoppable +0.06 (+0.18), Spellbreaker +0.02 (+0.18)
- **Silver**: Dispel Magic +0.05 (+0.10), Reactive Barrier +0.05 (+0.08), Bullet Resilience +0.04 (+0.10)
- **Celeste**: Witchmail +0.06 (+0.23), Healbane +0.04 (+0.10), Spirit Resilience +0.04 (+0.18)
- **Rat King**: Return Fire -0.00 (+0.05), Bullet Resilience -0.01 (+0.05), Counterspell -0.01 (+0.02)
- **Solomon**: Return Fire +0.02 (+0.07), Counterspell +0.00 (+0.04), Healbane +0.00 (+0.06)
- **Violet**: Witchmail +0.08 (+0.25), Healbane +0.04 (+0.10), Return Fire +0.01 (+0.06)
- **Nurse Harrow**: Healbane +0.05 (+0.11), Divine Barrier +0.00 (+0.09), Counterspell -0.02 (+0.01)
- **Baba**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.01)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.169 | +0.053 | +0.148 | The Doorman +0.49, Lash +0.37, Viscous +0.31 | 17 heroes |
| Indomitable | 6,400 | +0.197 | +0.031 | +0.167 | Wraith +0.42, Vyper +0.26, The Doorman +0.24 | 3 heroes |
| Dispel Magic | 3,200 | +0.091 | +0.028 | +0.054 | Mirage +0.33, Lash +0.16, Silver +0.13 | 11 heroes |
| Spellbreaker | 6,400 | +0.167 | +0.026 | +0.202 | Grey Talon +0.29, Deadman Danny +0.27, Wraith +0.22 | 0 heroes |
| Divine Barrier | 6,400 | +0.122 | +0.019 | +0.090 | Viscous +0.22, Nurse Harrow +0.15, The Doorman +0.14 | 2 heroes |
| Healbane | 1,600 | +0.030 | +0.018 | +0.067 | Lady Geist +0.08, Victor +0.07, Sinclair +0.06 | 23 heroes |
| Witchmail | 6,400 | +0.107 | +0.017 | +0.178 | The Doorman +0.31, Deadman Danny +0.29, Lash +0.17 | 1 heroes |
| Bullet Resilience | 3,200 | +0.023 | +0.007 | +0.064 | Vindicta +0.15, Viscous +0.12, Haze +0.09 | 1 heroes |
| Debuff Reducer | 1,600 | +0.009 | +0.006 | +0.096 | Grey Talon +0.22, Paige +0.18, Holliday +0.17 | 0 heroes |
| Plated Armor | 6,400 | +0.010 | +0.002 | +0.101 | Vindicta +0.13, Viscous +0.12, Haze +0.11 | 3 heroes |
| Reactive Barrier | 1,600 | -0.003 | -0.002 | +0.037 | The Doorman +0.12, Calico +0.09, Wraith +0.08 | 2 heroes |
| Unstoppable | 6,400 | -0.055 | -0.009 | +0.168 | Grey Talon +0.25, Paige +0.24, Ivy +0.21 | 5 heroes |
| Counterspell | 3,200 | -0.029 | -0.009 | +0.033 | Viscous +0.07, Lash +0.05, Sinclair +0.05 | 1 heroes |
| Metal Skin | 3,200 | -0.181 | -0.057 | +0.096 | Wraith +0.26, Viscous +0.13, Venator +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.171 | -0.107 | +0.055 | Vindicta +0.12, Paradox +0.08, Viscous +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.31), Spellbreaker +0.13 (+0.33), Dispel Magic +0.09 (+0.14)
- **Seven**: Witchmail +0.07 (+0.25), Reactive Barrier +0.00 (+0.04), Healbane -0.00 (+0.06)
- **Vindicta**: Bullet Resilience +0.15 (+0.21), Plated Armor +0.13 (+0.23), Return Fire +0.12 (+0.17)
- **Lady Geist**: Healbane +0.08 (+0.15), Spirit Resilience +0.06 (+0.21), Witchmail +0.02 (+0.20)
- **Abrams**: Dispel Magic +0.00 (+0.06), Healbane -0.01 (+0.06), Unstoppable -0.01 (+0.16)
- **Wraith**: Indomitable +0.42 (+0.58), Metal Skin +0.26 (+0.35), Spellbreaker +0.22 (+0.43)
- **McGinnis**: Spirit Resilience +0.04 (+0.18), Counterspell -0.01 (+0.03), Healbane -0.02 (+0.05)
- **Paradox**: Dispel Magic +0.13 (+0.19), Indomitable +0.12 (+0.29), Unstoppable +0.12 (+0.29)
- **Dynamo**: Counterspell -0.02 (+0.01), Healbane -0.03 (+0.04), Reactive Barrier -0.04 (-0.00)
- **Kelvin**: Spirit Resilience +0.04 (+0.19), Healbane -0.01 (+0.06), Counterspell -0.01 (+0.02)
- **Haze**: Unstoppable +0.16 (+0.33), Plated Armor +0.11 (+0.21), Bullet Resilience +0.09 (+0.15)
- **Holliday**: Spellbreaker +0.22 (+0.42), Debuff Reducer +0.17 (+0.27), Unstoppable +0.16 (+0.32)
- **Bebop**: Debuff Reducer +0.12 (+0.22), Unstoppable +0.07 (+0.24), Spellbreaker +0.06 (+0.26)
- **Calico**: Reactive Barrier +0.09 (+0.13), Divine Barrier +0.06 (+0.15), Dispel Magic +0.05 (+0.10)
- **Grey Talon**: Spirit Resilience +0.29 (+0.44), Spellbreaker +0.29 (+0.49), Unstoppable +0.25 (+0.41)
- **Mo & Krill**: Spellbreaker +0.11 (+0.31), Indomitable +0.07 (+0.24), Debuff Reducer +0.06 (+0.16)
- **Shiv**: Metal Skin +0.07 (+0.16), Bullet Resilience +0.06 (+0.12), Divine Barrier +0.04 (+0.13)
- **Ivy**: Unstoppable +0.21 (+0.38), Debuff Reducer +0.05 (+0.15), Indomitable +0.03 (+0.20)
- **Warden**: Spirit Resilience +0.02 (+0.17), Divine Barrier +0.01 (+0.10), Counterspell +0.00 (+0.04)
- **Yamato**: Spirit Resilience +0.09 (+0.23), Spellbreaker +0.04 (+0.25), Healbane +0.04 (+0.11)
- **Lash**: Spirit Resilience +0.37 (+0.52), Spellbreaker +0.19 (+0.39), Witchmail +0.17 (+0.35)
- **Viscous**: Spirit Resilience +0.31 (+0.46), Divine Barrier +0.22 (+0.31), Spellbreaker +0.16 (+0.36)
- **Pocket**: Spirit Resilience +0.09 (+0.24), Witchmail -0.01 (+0.17), Return Fire -0.01 (+0.05)
- **Mirage**: Dispel Magic +0.33 (+0.38), Unstoppable +0.10 (+0.26), Metal Skin +0.05 (+0.15)
- **Vyper**: Indomitable +0.26 (+0.42), Plated Armor +0.07 (+0.17), Bullet Resilience +0.04 (+0.10)
- **Sinclair**: Indomitable +0.21 (+0.38), Debuff Reducer +0.09 (+0.19), Spellbreaker +0.08 (+0.28)
- **Mina**: Divine Barrier +0.02 (+0.11), Counterspell -0.00 (+0.03), Return Fire -0.02 (+0.03)
- **Drifter**: Dispel Magic +0.00 (+0.06), Healbane -0.00 (+0.07), Return Fire -0.00 (+0.05)
- **Venator**: Metal Skin +0.11 (+0.21), Bullet Resilience +0.08 (+0.14), Plated Armor +0.02 (+0.12)
- **Victor**: Healbane +0.07 (+0.14), Spellbreaker +0.04 (+0.25), Spirit Resilience +0.04 (+0.19)
- **Paige**: Unstoppable +0.24 (+0.40), Debuff Reducer +0.18 (+0.28), Spellbreaker +0.08 (+0.28)
- **The Doorman**: Spirit Resilience +0.49 (+0.64), Witchmail +0.31 (+0.49), Indomitable +0.24 (+0.41)
- **Billy**: Healbane +0.03 (+0.09), Reactive Barrier +0.01 (+0.05), Counterspell -0.00 (+0.03)
- **Graves**: Healbane +0.01 (+0.08), Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Apollo**: Reactive Barrier +0.02 (+0.06), Healbane +0.02 (+0.08), Counterspell +0.00 (+0.04)
- **Deadman Danny**: Witchmail +0.29 (+0.47), Spirit Resilience +0.29 (+0.44), Spellbreaker +0.27 (+0.48)
- **Rem**: Divine Barrier +0.09 (+0.18), Spirit Resilience +0.06 (+0.21), Witchmail +0.02 (+0.19)
- **Silver**: Dispel Magic +0.13 (+0.19), Bullet Resilience +0.05 (+0.12), Indomitable +0.04 (+0.21)
- **Celeste**: Witchmail +0.11 (+0.29), Plated Armor +0.04 (+0.15), Dispel Magic +0.03 (+0.08)
- **Rat King**: Healbane -0.01 (+0.06), Counterspell -0.02 (+0.01), Bullet Resilience -0.02 (+0.04)
- **Solomon**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.04), Reactive Barrier -0.01 (+0.02)
- **Violet**: Witchmail +0.07 (+0.25), Indomitable +0.03 (+0.20), Spirit Resilience -0.00 (+0.15)
- **Nurse Harrow**: Spirit Resilience +0.19 (+0.33), Divine Barrier +0.15 (+0.24), Bullet Resilience +0.07 (+0.13)
- **Baba**: Counterspell +0.02 (+0.05), Reactive Barrier +0.00 (+0.04), Healbane -0.01 (+0.06)
