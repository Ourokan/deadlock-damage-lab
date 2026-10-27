# Counter items in the sim (phantom and up)

Built 2026-10-27T07:13:46Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.371 | +0.059 | +0.098 | Lash +0.27, Wraith +0.16, Calico +0.12 | 0 heroes |
| Spirit Resilience | 3,200 | +0.162 | +0.051 | +0.122 | Lash +0.28, Deadman Danny +0.18, Wraith +0.15 | 1 heroes |
| Dispel Magic | 3,200 | +0.105 | +0.033 | +0.077 | Mirage +0.39, Silver +0.13, Infernus +0.11 | 4 heroes |
| Debuff Reducer | 1,600 | +0.042 | +0.026 | +0.059 | Wraith +0.08, Deadman Danny +0.08, Grey Talon +0.05 | 0 heroes |
| Witchmail | 6,400 | +0.134 | +0.021 | +0.199 | Lash +0.20, Deadman Danny +0.19, Wraith +0.15 | 0 heroes |
| Reactive Barrier | 1,600 | +0.033 | +0.021 | +0.056 | Wraith +0.14, Deadman Danny +0.14, The Doorman +0.08 | 2 heroes |
| Indomitable | 6,400 | +0.124 | +0.020 | +0.144 | Wraith +0.29, Vyper +0.28, Deadman Danny +0.24 | 0 heroes |
| Spellbreaker | 6,400 | +0.084 | +0.013 | +0.149 | Lash +0.32, Deadman Danny +0.23, Wraith +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | -0.000 | -0.000 | +0.091 | Paradox +0.14, Wraith +0.13, Deadman Danny +0.12 | 0 heroes |
| Healbane | 1,600 | -0.001 | -0.001 | +0.087 | Nurse Harrow +0.07, Deadman Danny +0.05, Lash +0.04 | 11 heroes |
| Counterspell | 3,200 | -0.009 | -0.003 | +0.073 | Deadman Danny +0.10, Calico +0.06, Drifter +0.05 | 1 heroes |
| Plated Armor | 6,400 | -0.020 | -0.003 | +0.127 | Holliday +0.22, Deadman Danny +0.16, Wraith +0.16 | 0 heroes |
| Unstoppable | 6,400 | -0.042 | -0.006 | +0.114 | Deadman Danny +0.18, Wraith +0.12, Abrams +0.12 | 0 heroes |
| Metal Skin | 3,200 | -0.135 | -0.042 | +0.109 | Wraith +0.24, Lash +0.23, Paradox +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.157 | -0.098 | +0.077 | Deadman Danny +0.07, The Doorman +0.06, Drifter +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.19), Unstoppable +0.06 (+0.17), Spirit Resilience +0.04 (+0.17)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.04 (+0.02)
- **Vindicta**: Witchmail +0.01 (+0.21), Return Fire +0.01 (+0.09), Divine Barrier +0.01 (+0.10)
- **Lady Geist**: Return Fire +0.04 (+0.12), Healbane +0.01 (+0.10), Counterspell +0.01 (+0.08)
- **Abrams**: Indomitable +0.17 (+0.32), Unstoppable +0.12 (+0.23), Divine Barrier +0.07 (+0.17)
- **Wraith**: Indomitable +0.29 (+0.43), Metal Skin +0.24 (+0.35), Spellbreaker +0.16 (+0.31)
- **McGinnis**: Spirit Resilience +0.01 (+0.14), Return Fire -0.00 (+0.08), Counterspell -0.01 (+0.07)
- **Paradox**: Metal Skin +0.16 (+0.26), Bullet Resilience +0.14 (+0.23), Plated Armor +0.13 (+0.25)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.03 (+0.05), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Witchmail -0.00 (+0.20), Healbane -0.00 (+0.08), Spirit Resilience -0.01 (+0.12)
- **Haze**: Plated Armor +0.09 (+0.21), Bullet Resilience +0.05 (+0.14), Indomitable +0.04 (+0.19)
- **Holliday**: Plated Armor +0.22 (+0.35), Reactive Barrier +0.03 (+0.09), Debuff Reducer +0.03 (+0.09)
- **Bebop**: Witchmail +0.02 (+0.22), Divine Barrier +0.02 (+0.12), Bullet Resilience +0.02 (+0.11)
- **Calico**: Spellbreaker +0.12 (+0.27), Divine Barrier +0.12 (+0.22), Spirit Resilience +0.11 (+0.23)
- **Grey Talon**: Reactive Barrier +0.05 (+0.10), Debuff Reducer +0.05 (+0.10), Spellbreaker +0.04 (+0.19)
- **Mo & Krill**: Spellbreaker +0.14 (+0.28), Witchmail +0.08 (+0.28), Spirit Resilience +0.07 (+0.20)
- **Shiv**: Healbane -0.01 (+0.08), Return Fire -0.01 (+0.07), Debuff Reducer -0.04 (+0.02)
- **Ivy**: Unstoppable +0.10 (+0.22), Indomitable +0.07 (+0.21), Dispel Magic -0.00 (+0.08)
- **Warden**: Return Fire +0.01 (+0.09), Debuff Reducer -0.02 (+0.04), Counterspell -0.02 (+0.06)
- **Yamato**: Healbane +0.01 (+0.10), Counterspell -0.04 (+0.03), Debuff Reducer -0.04 (+0.02)
- **Lash**: Spellbreaker +0.32 (+0.47), Spirit Resilience +0.28 (+0.41), Divine Barrier +0.27 (+0.36)
- **Viscous**: Healbane -0.02 (+0.06), Divine Barrier -0.03 (+0.07), Return Fire -0.03 (+0.04)
- **Pocket**: Witchmail +0.06 (+0.26), Spirit Resilience +0.05 (+0.17), Spellbreaker +0.03 (+0.18)
- **Mirage**: Dispel Magic +0.39 (+0.47), Spellbreaker +0.08 (+0.23), Spirit Resilience +0.07 (+0.19)
- **Vyper**: Indomitable +0.28 (+0.43), Debuff Reducer +0.04 (+0.10), Unstoppable +0.02 (+0.14)
- **Sinclair**: Indomitable +0.08 (+0.23), Spellbreaker +0.02 (+0.17), Unstoppable +0.02 (+0.13)
- **Mina**: Witchmail +0.03 (+0.23), Return Fire +0.01 (+0.09), Counterspell +0.00 (+0.07)
- **Drifter**: Return Fire +0.06 (+0.13), Witchmail +0.06 (+0.25), Counterspell +0.05 (+0.12)
- **Venator**: Bullet Resilience +0.09 (+0.18), Metal Skin +0.01 (+0.12), Divine Barrier +0.01 (+0.11)
- **Victor**: Spirit Resilience +0.04 (+0.16), Healbane +0.01 (+0.10), Spellbreaker +0.00 (+0.15)
- **Paige**: Healbane -0.01 (+0.08), Return Fire -0.02 (+0.05), Counterspell -0.03 (+0.05)
- **The Doorman**: Indomitable +0.15 (+0.30), Witchmail +0.12 (+0.31), Spirit Resilience +0.10 (+0.22)
- **Billy**: Healbane +0.04 (+0.12), Spellbreaker +0.04 (+0.18), Spirit Resilience +0.04 (+0.16)
- **Graves**: Witchmail +0.09 (+0.29), Metal Skin +0.08 (+0.19), Spirit Resilience +0.08 (+0.20)
- **Apollo**: Healbane +0.01 (+0.10), Unstoppable +0.00 (+0.12), Reactive Barrier -0.02 (+0.04)
- **Deadman Danny**: Indomitable +0.24 (+0.39), Spellbreaker +0.23 (+0.38), Witchmail +0.19 (+0.39)
- **Rem**: Witchmail -0.00 (+0.20), Unstoppable -0.01 (+0.10), Dispel Magic -0.01 (+0.06)
- **Silver**: Dispel Magic +0.13 (+0.20), Reactive Barrier +0.03 (+0.08), Metal Skin +0.03 (+0.14)
- **Celeste**: Spirit Resilience +0.10 (+0.22), Witchmail +0.09 (+0.29), Dispel Magic +0.04 (+0.12)
- **Rat King**: Counterspell +0.00 (+0.08), Bullet Resilience -0.00 (+0.09), Return Fire -0.01 (+0.07)
- **Solomon**: Return Fire -0.01 (+0.07), Counterspell -0.02 (+0.05), Reactive Barrier -0.02 (+0.03)
- **Violet**: Return Fire +0.04 (+0.12), Healbane -0.02 (+0.07), Counterspell -0.04 (+0.04)
- **Nurse Harrow**: Healbane +0.07 (+0.15), Counterspell -0.02 (+0.05), Return Fire -0.03 (+0.05)
- **Baba**: Healbane -0.00 (+0.09), Debuff Reducer -0.02 (+0.03), Unstoppable -0.02 (+0.09)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.147 | +0.046 | +0.114 | Lash +0.36, Pocket +0.21, Deadman Danny +0.20 | 10 heroes |
| Divine Barrier | 6,400 | +0.209 | +0.033 | +0.061 | Lash +0.20, Wraith +0.13, The Doorman +0.10 | 1 heroes |
| Dispel Magic | 3,200 | +0.087 | +0.027 | +0.048 | Mirage +0.32, Infernus +0.10, Graves +0.08 | 7 heroes |
| Witchmail | 6,400 | +0.128 | +0.020 | +0.160 | Lash +0.17, Graves +0.17, Pocket +0.13 | 0 heroes |
| Indomitable | 6,400 | +0.102 | +0.017 | +0.113 | Vyper +0.34, Wraith +0.29, The Doorman +0.13 | 0 heroes |
| Spellbreaker | 6,400 | +0.088 | +0.014 | +0.119 | Lash +0.37, Deadman Danny +0.14, Wraith +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.017 | +0.011 | +0.041 | Wraith +0.10, Lash +0.05, The Doorman +0.04 | 1 heroes |
| Reactive Barrier | 1,600 | +0.015 | +0.009 | +0.040 | Graves +0.11, Wraith +0.11, Deadman Danny +0.10 | 4 heroes |
| Plated Armor | 6,400 | -0.021 | -0.003 | +0.100 | Deadman Danny +0.22, Wraith +0.14, Paradox +0.09 | 0 heroes |
| Bullet Resilience | 3,200 | -0.023 | -0.007 | +0.059 | Venator +0.13, Paradox +0.11, Wraith +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.026 | -0.008 | +0.043 | Wraith +0.05, Graves +0.04, Vindicta +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.066 | -0.010 | +0.084 | Mo & Krill +0.12, Ivy +0.10, Wraith +0.09 | 0 heroes |
| Healbane | 1,600 | -0.032 | -0.020 | +0.062 | Bebop +0.05, Graves +0.05, Wraith +0.04 | 17 heroes |
| Metal Skin | 3,200 | -0.150 | -0.047 | +0.084 | Wraith +0.22, Paradox +0.15, Lash +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.169 | -0.106 | +0.054 | Wraith +0.08, The Doorman +0.05, Lady Geist +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.15), Unstoppable +0.04 (+0.12), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.04 (+0.20), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Witchmail +0.06 (+0.22), Divine Barrier +0.04 (+0.10), Bullet Resilience +0.04 (+0.10)
- **Lady Geist**: Return Fire +0.04 (+0.10), Divine Barrier +0.04 (+0.10), Bullet Resilience +0.04 (+0.10)
- **Abrams**: Indomitable +0.08 (+0.20), Unstoppable +0.07 (+0.16), Healbane +0.03 (+0.09)
- **Wraith**: Indomitable +0.29 (+0.40), Metal Skin +0.22 (+0.30), Spellbreaker +0.14 (+0.26)
- **McGinnis**: Spirit Resilience +0.08 (+0.20), Return Fire +0.02 (+0.07), Healbane +0.01 (+0.07)
- **Paradox**: Metal Skin +0.15 (+0.24), Bullet Resilience +0.11 (+0.17), Plated Armor +0.09 (+0.19)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.06 (+0.17), Dispel Magic +0.03 (+0.08), Counterspell +0.03 (+0.07)
- **Haze**: Indomitable +0.10 (+0.21), Plated Armor +0.08 (+0.18), Unstoppable +0.08 (+0.17)
- **Holliday**: Return Fire +0.04 (+0.09), Debuff Reducer +0.03 (+0.08), Indomitable +0.02 (+0.14)
- **Bebop**: Healbane +0.05 (+0.11), Counterspell +0.02 (+0.06), Metal Skin +0.01 (+0.09)
- **Calico**: Reactive Barrier +0.03 (+0.07), Divine Barrier +0.03 (+0.09), Spellbreaker +0.02 (+0.14)
- **Grey Talon**: Debuff Reducer +0.03 (+0.07), Reactive Barrier +0.02 (+0.06), Spellbreaker +0.02 (+0.14)
- **Mo & Krill**: Unstoppable +0.12 (+0.20), Spellbreaker +0.05 (+0.17), Dispel Magic +0.05 (+0.09)
- **Shiv**: Metal Skin +0.05 (+0.14), Divine Barrier +0.05 (+0.11), Bullet Resilience +0.05 (+0.10)
- **Ivy**: Unstoppable +0.10 (+0.18), Indomitable +0.08 (+0.19), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.08), Counterspell -0.00 (+0.04), Debuff Reducer -0.00 (+0.04)
- **Yamato**: Healbane +0.02 (+0.08), Debuff Reducer -0.02 (+0.02), Bullet Resilience -0.02 (+0.04)
- **Lash**: Spellbreaker +0.37 (+0.48), Spirit Resilience +0.36 (+0.47), Divine Barrier +0.20 (+0.26)
- **Viscous**: Divine Barrier +0.00 (+0.06), Debuff Reducer -0.01 (+0.03), Bullet Resilience -0.01 (+0.05)
- **Pocket**: Spirit Resilience +0.21 (+0.32), Witchmail +0.13 (+0.29), Spellbreaker +0.13 (+0.25)
- **Mirage**: Dispel Magic +0.32 (+0.36), Spirit Resilience +0.05 (+0.16), Metal Skin +0.05 (+0.13)
- **Vyper**: Indomitable +0.34 (+0.46), Metal Skin +0.05 (+0.14), Debuff Reducer +0.04 (+0.08)
- **Sinclair**: Indomitable +0.08 (+0.19), Return Fire +0.00 (+0.06), Spellbreaker -0.01 (+0.11)
- **Mina**: Witchmail +0.03 (+0.19), Spirit Resilience +0.02 (+0.14), Divine Barrier +0.02 (+0.08)
- **Drifter**: Witchmail +0.04 (+0.20), Bullet Resilience +0.01 (+0.07), Counterspell +0.01 (+0.05)
- **Venator**: Bullet Resilience +0.13 (+0.19), Metal Skin +0.10 (+0.18), Plated Armor +0.07 (+0.17)
- **Victor**: Spirit Resilience +0.07 (+0.19), Spellbreaker +0.07 (+0.19), Dispel Magic -0.00 (+0.05)
- **Paige**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.04), Healbane -0.01 (+0.05)
- **The Doorman**: Spirit Resilience +0.16 (+0.28), Indomitable +0.13 (+0.24), Divine Barrier +0.10 (+0.17)
- **Billy**: Spirit Resilience +0.02 (+0.13), Spellbreaker -0.00 (+0.12), Counterspell -0.01 (+0.04)
- **Graves**: Witchmail +0.17 (+0.33), Metal Skin +0.12 (+0.21), Spirit Resilience +0.12 (+0.23)
- **Apollo**: Reactive Barrier +0.03 (+0.07), Indomitable +0.01 (+0.12), Healbane -0.01 (+0.05)
- **Deadman Danny**: Plated Armor +0.22 (+0.32), Spirit Resilience +0.20 (+0.31), Spellbreaker +0.14 (+0.26)
- **Rem**: Counterspell -0.00 (+0.04), Divine Barrier -0.00 (+0.06), Healbane -0.00 (+0.06)
- **Silver**: Dispel Magic +0.06 (+0.11), Metal Skin +0.05 (+0.14), Reactive Barrier +0.04 (+0.08)
- **Celeste**: Witchmail +0.00 (+0.16), Healbane -0.00 (+0.06), Spirit Resilience -0.01 (+0.11)
- **Rat King**: Bullet Resilience -0.00 (+0.06), Return Fire -0.00 (+0.05), Metal Skin -0.01 (+0.08)
- **Solomon**: Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05)
- **Violet**: Return Fire +0.04 (+0.09), Witchmail +0.03 (+0.19), Healbane +0.01 (+0.08)
- **Nurse Harrow**: Healbane -0.02 (+0.04), Dispel Magic -0.02 (+0.02), Counterspell -0.03 (+0.01)
- **Baba**: Unstoppable +0.03 (+0.11), Healbane +0.01 (+0.08), Counterspell -0.00 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.144 | +0.045 | +0.125 | Lash +0.25, Deadman Danny +0.25, Wraith +0.12 | 14 heroes |
| Divine Barrier | 6,400 | +0.192 | +0.030 | +0.062 | Lash +0.19, Vindicta +0.12, Wraith +0.09 | 2 heroes |
| Dispel Magic | 3,200 | +0.090 | +0.028 | +0.062 | Mirage +0.29, Lash +0.27, Paradox +0.11 | 9 heroes |
| Witchmail | 6,400 | +0.128 | +0.020 | +0.170 | Deadman Danny +0.18, Lash +0.16, Paradox +0.12 | 1 heroes |
| Indomitable | 6,400 | +0.114 | +0.018 | +0.133 | Vyper +0.38, Wraith +0.30, Deadman Danny +0.24 | 0 heroes |
| Spellbreaker | 6,400 | +0.099 | +0.015 | +0.135 | Lash +0.40, Deadman Danny +0.23, Wraith +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.016 | +0.010 | +0.045 | Grey Talon +0.09, Deadman Danny +0.07, Vyper +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | +0.006 | +0.004 | +0.039 | Deadman Danny +0.14, Yamato +0.09, Wraith +0.08 | 5 heroes |
| Plated Armor | 6,400 | -0.015 | -0.002 | +0.115 | Deadman Danny +0.22, Holliday +0.16, Wraith +0.15 | 0 heroes |
| Counterspell | 3,200 | -0.031 | -0.010 | +0.038 | Deadman Danny +0.06, Drifter +0.05, Yamato +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.062 | -0.010 | +0.101 | Deadman Danny +0.17, Abrams +0.14, Grey Talon +0.12 | 3 heroes |
| Bullet Resilience | 3,200 | -0.034 | -0.011 | +0.064 | Deadman Danny +0.12, Vindicta +0.11, Lash +0.10 | 1 heroes |
| Healbane | 1,600 | -0.034 | -0.021 | +0.061 | Drifter +0.06, Infernus +0.04, Yamato +0.04 | 15 heroes |
| Metal Skin | 3,200 | -0.144 | -0.045 | +0.107 | Wraith +0.26, Lash +0.18, Paradox +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.168 | -0.105 | +0.052 | Wraith +0.09, Paradox +0.06, Vindicta +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.16), Unstoppable +0.10 (+0.20), Spellbreaker +0.08 (+0.22)
- **Seven**: Witchmail +0.04 (+0.21), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03)
- **Vindicta**: Divine Barrier +0.12 (+0.18), Bullet Resilience +0.11 (+0.17), Witchmail +0.08 (+0.25)
- **Lady Geist**: Return Fire +0.04 (+0.09), Divine Barrier +0.03 (+0.09), Bullet Resilience +0.02 (+0.09)
- **Abrams**: Unstoppable +0.14 (+0.25), Dispel Magic +0.08 (+0.14), Healbane +0.04 (+0.10)
- **Wraith**: Indomitable +0.30 (+0.43), Metal Skin +0.26 (+0.36), Plated Armor +0.15 (+0.26)
- **McGinnis**: Spirit Resilience +0.09 (+0.21), Witchmail +0.02 (+0.19), Spellbreaker +0.01 (+0.15)
- **Paradox**: Spellbreaker +0.14 (+0.27), Witchmail +0.12 (+0.29), Unstoppable +0.11 (+0.21)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.00 (+0.04), Return Fire -0.03 (+0.02)
- **Kelvin**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03), Spirit Resilience -0.03 (+0.10)
- **Haze**: Plated Armor +0.09 (+0.20), Indomitable +0.09 (+0.22), Unstoppable +0.06 (+0.16)
- **Holliday**: Plated Armor +0.16 (+0.27), Debuff Reducer +0.03 (+0.08), Indomitable +0.03 (+0.16)
- **Bebop**: Healbane +0.01 (+0.07), Counterspell -0.02 (+0.02), Return Fire -0.03 (+0.03)
- **Calico**: Reactive Barrier +0.03 (+0.07), Divine Barrier +0.02 (+0.08), Spirit Resilience +0.01 (+0.13)
- **Grey Talon**: Spellbreaker +0.13 (+0.27), Unstoppable +0.12 (+0.22), Debuff Reducer +0.09 (+0.14)
- **Mo & Krill**: Unstoppable +0.08 (+0.18), Spirit Resilience +0.07 (+0.20), Spellbreaker +0.06 (+0.19)
- **Shiv**: Metal Skin +0.04 (+0.15), Divine Barrier +0.02 (+0.08), Bullet Resilience +0.02 (+0.09)
- **Ivy**: Unstoppable +0.10 (+0.20), Indomitable +0.05 (+0.18), Debuff Reducer +0.02 (+0.06)
- **Warden**: Return Fire +0.04 (+0.09), Counterspell +0.02 (+0.06), Divine Barrier +0.01 (+0.08)
- **Yamato**: Reactive Barrier +0.09 (+0.13), Debuff Reducer +0.05 (+0.09), Counterspell +0.04 (+0.08)
- **Lash**: Spellbreaker +0.40 (+0.54), Dispel Magic +0.27 (+0.33), Spirit Resilience +0.25 (+0.38)
- **Viscous**: Divine Barrier +0.02 (+0.08), Return Fire +0.01 (+0.06), Healbane +0.01 (+0.07)
- **Pocket**: Spirit Resilience +0.10 (+0.22), Witchmail +0.03 (+0.20), Spellbreaker +0.01 (+0.15)
- **Mirage**: Dispel Magic +0.29 (+0.36), Spirit Resilience +0.02 (+0.14), Healbane +0.01 (+0.07)
- **Vyper**: Indomitable +0.38 (+0.51), Debuff Reducer +0.07 (+0.11), Unstoppable +0.05 (+0.16)
- **Sinclair**: Indomitable +0.12 (+0.26), Return Fire +0.00 (+0.06), Unstoppable -0.01 (+0.09)
- **Mina**: Spirit Resilience +0.11 (+0.24), Witchmail +0.10 (+0.27), Divine Barrier +0.06 (+0.12)
- **Drifter**: Spirit Resilience +0.10 (+0.23), Witchmail +0.07 (+0.24), Healbane +0.06 (+0.13)
- **Venator**: Bullet Resilience +0.10 (+0.16), Metal Skin +0.09 (+0.20), Plated Armor +0.03 (+0.15)
- **Victor**: Spirit Resilience +0.02 (+0.15), Healbane +0.01 (+0.07), Spellbreaker +0.00 (+0.14)
- **Paige**: Unstoppable +0.11 (+0.21), Debuff Reducer +0.05 (+0.09), Counterspell -0.01 (+0.03)
- **The Doorman**: Spirit Resilience +0.12 (+0.24), Indomitable +0.11 (+0.25), Witchmail +0.09 (+0.26)
- **Billy**: Reactive Barrier +0.02 (+0.06), Healbane -0.01 (+0.06), Debuff Reducer -0.02 (+0.03)
- **Graves**: Witchmail +0.03 (+0.20), Return Fire +0.02 (+0.08), Counterspell +0.00 (+0.04)
- **Apollo**: Healbane -0.00 (+0.06), Reactive Barrier -0.01 (+0.03), Counterspell -0.03 (+0.00)
- **Deadman Danny**: Spirit Resilience +0.25 (+0.37), Indomitable +0.24 (+0.37), Spellbreaker +0.23 (+0.36)
- **Rem**: Debuff Reducer +0.06 (+0.11), Unstoppable +0.05 (+0.15), Counterspell -0.00 (+0.03)
- **Silver**: Dispel Magic +0.05 (+0.11), Indomitable -0.00 (+0.13), Return Fire -0.00 (+0.05)
- **Celeste**: Witchmail +0.05 (+0.22), Dispel Magic +0.05 (+0.11), Reactive Barrier +0.02 (+0.06)
- **Rat King**: Return Fire -0.01 (+0.05), Bullet Resilience -0.01 (+0.05), Counterspell -0.01 (+0.02)
- **Solomon**: Counterspell -0.00 (+0.04), Return Fire -0.01 (+0.04), Reactive Barrier -0.02 (+0.02)
- **Violet**: Witchmail +0.08 (+0.25), Return Fire +0.05 (+0.10), Healbane +0.02 (+0.08)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Counterspell -0.02 (+0.02), Return Fire -0.03 (+0.02)
- **Baba**: Healbane -0.00 (+0.06), Unstoppable -0.01 (+0.09), Counterspell -0.01 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.169 | +0.053 | +0.137 | Lash +0.56, Deadman Danny +0.35, The Doorman +0.30 | 15 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.058 | Mirage +0.28, Silver +0.21, Lash +0.20 | 9 heroes |
| Divine Barrier | 6,400 | +0.154 | +0.024 | +0.061 | Lash +0.27, Calico +0.15, Vindicta +0.12 | 3 heroes |
| Indomitable | 6,400 | +0.132 | +0.021 | +0.162 | Wraith +0.29, Deadman Danny +0.27, Vyper +0.27 | 1 heroes |
| Witchmail | 6,400 | +0.121 | +0.019 | +0.160 | Lash +0.29, The Doorman +0.24, Deadman Danny +0.19 | 2 heroes |
| Spellbreaker | 6,400 | +0.108 | +0.017 | +0.140 | Lash +0.46, Deadman Danny +0.24, Grey Talon +0.18 | 0 heroes |
| Debuff Reducer | 1,600 | +0.009 | +0.005 | +0.046 | Lash +0.11, Grey Talon +0.09, Rem +0.07 | 0 heroes |
| Plated Armor | 6,400 | -0.030 | -0.005 | +0.099 | Lash +0.15, Vindicta +0.15, Vyper +0.13 | 2 heroes |
| Unstoppable | 6,400 | -0.055 | -0.009 | +0.117 | Infernus +0.24, Haze +0.24, Grey Talon +0.15 | 8 heroes |
| Reactive Barrier | 1,600 | -0.015 | -0.009 | +0.041 | Deadman Danny +0.13, Calico +0.12, Drifter +0.12 | 3 heroes |
| Counterspell | 3,200 | -0.039 | -0.012 | +0.034 | Lash +0.12, The Doorman +0.06, Yamato +0.04 | 1 heroes |
| Bullet Resilience | 3,200 | -0.047 | -0.015 | +0.058 | Lash +0.17, Vindicta +0.10, Venator +0.08 | 0 heroes |
| Healbane | 1,600 | -0.038 | -0.024 | +0.053 | Nurse Harrow +0.07, Lady Geist +0.06, Mo & Krill +0.05 | 14 heroes |
| Metal Skin | 3,200 | -0.146 | -0.046 | +0.107 | Lash +0.26, Grey Talon +0.17, Silver +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.172 | -0.107 | +0.049 | Paradox +0.05, Vindicta +0.05, Wraith +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.24 (+0.36), Dispel Magic +0.06 (+0.12), Spellbreaker +0.04 (+0.18)
- **Seven**: Witchmail +0.06 (+0.22), Counterspell -0.01 (+0.02), Healbane -0.02 (+0.04)
- **Vindicta**: Plated Armor +0.15 (+0.25), Divine Barrier +0.12 (+0.18), Bullet Resilience +0.10 (+0.15)
- **Lady Geist**: Healbane +0.06 (+0.11), Dispel Magic +0.02 (+0.08), Metal Skin +0.02 (+0.13)
- **Abrams**: Unstoppable +0.07 (+0.19), Indomitable +0.04 (+0.20), Spellbreaker +0.03 (+0.17)
- **Wraith**: Indomitable +0.29 (+0.46), Metal Skin +0.13 (+0.24), Witchmail +0.07 (+0.23)
- **McGinnis**: Spirit Resilience +0.04 (+0.18), Healbane +0.02 (+0.07), Witchmail -0.00 (+0.16)
- **Paradox**: Unstoppable +0.09 (+0.20), Witchmail +0.08 (+0.24), Spirit Resilience +0.06 (+0.20)
- **Dynamo**: Healbane +0.02 (+0.07), Counterspell -0.01 (+0.03), Debuff Reducer -0.04 (+0.01)
- **Kelvin**: Spirit Resilience +0.07 (+0.21), Healbane +0.02 (+0.07), Spellbreaker +0.01 (+0.15)
- **Haze**: Unstoppable +0.24 (+0.35), Metal Skin +0.06 (+0.17), Bullet Resilience +0.06 (+0.12)
- **Holliday**: Spellbreaker +0.04 (+0.18), Return Fire +0.03 (+0.07), Plated Armor +0.02 (+0.12)
- **Bebop**: Debuff Reducer +0.06 (+0.10), Spellbreaker +0.03 (+0.17), Reactive Barrier +0.03 (+0.07)
- **Calico**: Spirit Resilience +0.16 (+0.29), Divine Barrier +0.15 (+0.21), Reactive Barrier +0.12 (+0.16)
- **Grey Talon**: Spellbreaker +0.18 (+0.32), Metal Skin +0.17 (+0.27), Unstoppable +0.15 (+0.27)
- **Mo & Krill**: Healbane +0.05 (+0.10), Dispel Magic +0.03 (+0.09), Unstoppable +0.03 (+0.15)
- **Shiv**: Bullet Resilience +0.03 (+0.09), Metal Skin +0.03 (+0.14), Return Fire +0.02 (+0.06)
- **Ivy**: Unstoppable +0.13 (+0.25), Indomitable +0.08 (+0.24), Debuff Reducer +0.04 (+0.09)
- **Warden**: Plated Armor +0.06 (+0.16), Metal Skin +0.04 (+0.14), Healbane +0.01 (+0.07)
- **Yamato**: Indomitable +0.07 (+0.23), Debuff Reducer +0.06 (+0.11), Plated Armor +0.05 (+0.15)
- **Lash**: Spirit Resilience +0.56 (+0.70), Spellbreaker +0.46 (+0.60), Witchmail +0.29 (+0.45)
- **Viscous**: Divine Barrier +0.06 (+0.12), Witchmail +0.02 (+0.18), Spirit Resilience +0.00 (+0.14)
- **Pocket**: Spirit Resilience +0.08 (+0.22), Spellbreaker +0.00 (+0.14), Witchmail -0.00 (+0.16)
- **Mirage**: Dispel Magic +0.28 (+0.34), Metal Skin +0.07 (+0.18), Plated Armor +0.00 (+0.10)
- **Vyper**: Indomitable +0.27 (+0.43), Plated Armor +0.13 (+0.23), Metal Skin +0.07 (+0.18)
- **Sinclair**: Indomitable +0.14 (+0.30), Dispel Magic +0.06 (+0.12), Reactive Barrier +0.06 (+0.10)
- **Mina**: Divine Barrier +0.01 (+0.07), Plated Armor -0.01 (+0.09), Dispel Magic -0.02 (+0.04)
- **Drifter**: Indomitable +0.20 (+0.37), Spirit Resilience +0.19 (+0.33), Reactive Barrier +0.12 (+0.16)
- **Venator**: Metal Skin +0.13 (+0.23), Bullet Resilience +0.08 (+0.14), Plated Armor +0.02 (+0.12)
- **Victor**: Spellbreaker +0.08 (+0.22), Spirit Resilience +0.05 (+0.19), Healbane +0.03 (+0.08)
- **Paige**: Counterspell +0.00 (+0.04), Return Fire -0.00 (+0.05), Healbane -0.01 (+0.04)
- **The Doorman**: Spirit Resilience +0.30 (+0.44), Witchmail +0.24 (+0.40), Indomitable +0.23 (+0.39)
- **Billy**: Reactive Barrier +0.07 (+0.11), Bullet Resilience +0.03 (+0.09), Plated Armor +0.02 (+0.12)
- **Graves**: Return Fire +0.02 (+0.07), Reactive Barrier -0.01 (+0.03), Counterspell -0.02 (+0.01)
- **Apollo**: Healbane +0.01 (+0.07), Reactive Barrier +0.00 (+0.05), Counterspell -0.02 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.35 (+0.49), Indomitable +0.27 (+0.44), Spellbreaker +0.24 (+0.38)
- **Rem**: Debuff Reducer +0.07 (+0.11), Spellbreaker +0.04 (+0.18), Divine Barrier -0.00 (+0.06)
- **Silver**: Dispel Magic +0.21 (+0.27), Metal Skin +0.16 (+0.27), Indomitable +0.11 (+0.27)
- **Celeste**: Witchmail +0.08 (+0.24), Spirit Resilience +0.07 (+0.21), Healbane +0.04 (+0.09)
- **Rat King**: Return Fire -0.01 (+0.04), Healbane -0.01 (+0.04), Counterspell -0.01 (+0.02)
- **Solomon**: Return Fire +0.01 (+0.06), Counterspell -0.00 (+0.03), Reactive Barrier -0.00 (+0.04)
- **Violet**: Return Fire +0.02 (+0.07), Witchmail +0.01 (+0.17), Healbane -0.01 (+0.05)
- **Nurse Harrow**: Spirit Resilience +0.12 (+0.26), Dispel Magic +0.11 (+0.17), Divine Barrier +0.09 (+0.15)
- **Baba**: Healbane +0.00 (+0.05), Witchmail -0.01 (+0.15), Counterspell -0.01 (+0.02)
