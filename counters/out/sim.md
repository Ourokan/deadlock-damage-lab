# Counter items in the sim (phantom and up)

Built 2026-10-27T14:39:36Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.392 | +0.063 | +0.097 | Lash +0.25, Wraith +0.18, Calico +0.11 | 0 heroes |
| Spirit Resilience | 3,200 | +0.185 | +0.058 | +0.121 | Lash +0.27, Wraith +0.20, Deadman Danny +0.17 | 1 heroes |
| Dispel Magic | 3,200 | +0.092 | +0.029 | +0.075 | Mirage +0.37, Silver +0.12, Paradox +0.10 | 4 heroes |
| Indomitable | 6,400 | +0.170 | +0.027 | +0.141 | Wraith +0.34, Vyper +0.28, Deadman Danny +0.23 | 0 heroes |
| Reactive Barrier | 1,600 | +0.041 | +0.026 | +0.057 | Wraith +0.16, Deadman Danny +0.12, The Doorman +0.09 | 2 heroes |
| Witchmail | 6,400 | +0.134 | +0.021 | +0.198 | Wraith +0.18, Deadman Danny +0.18, Lash +0.17 | 0 heroes |
| Debuff Reducer | 1,600 | +0.028 | +0.018 | +0.060 | Wraith +0.10, Deadman Danny +0.07, Venator +0.06 | 0 heroes |
| Spellbreaker | 6,400 | +0.083 | +0.013 | +0.148 | Lash +0.31, Deadman Danny +0.22, Wraith +0.22 | 0 heroes |
| Bullet Resilience | 3,200 | +0.000 | +0.000 | +0.091 | Wraith +0.16, Venator +0.15, Paradox +0.14 | 0 heroes |
| Healbane | 1,600 | -0.006 | -0.004 | +0.088 | Nurse Harrow +0.05, Deadman Danny +0.05, Lash +0.04 | 11 heroes |
| Plated Armor | 6,400 | -0.033 | -0.005 | +0.128 | Holliday +0.22, Wraith +0.22, Deadman Danny +0.16 | 0 heroes |
| Counterspell | 3,200 | -0.025 | -0.008 | +0.071 | Deadman Danny +0.08, Wraith +0.04, Lash +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.051 | -0.008 | +0.113 | Deadman Danny +0.16, Wraith +0.15, Abrams +0.12 | 0 heroes |
| Metal Skin | 3,200 | -0.144 | -0.045 | +0.108 | Wraith +0.26, Lash +0.21, Paradox +0.16 | 0 heroes |
| Return Fire | 1,600 | -0.170 | -0.106 | +0.082 | Wraith +0.09, Deadman Danny +0.07, Lady Geist +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.09 (+0.16), Unstoppable +0.05 (+0.16), Spirit Resilience +0.03 (+0.16)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.03 (+0.04), Reactive Barrier -0.04 (+0.02)
- **Vindicta**: Return Fire +0.01 (+0.09), Divine Barrier +0.00 (+0.10), Witchmail +0.00 (+0.20)
- **Lady Geist**: Return Fire +0.06 (+0.14), Dispel Magic +0.02 (+0.09), Divine Barrier +0.01 (+0.11)
- **Abrams**: Indomitable +0.18 (+0.32), Unstoppable +0.12 (+0.23), Divine Barrier +0.07 (+0.17)
- **Wraith**: Indomitable +0.34 (+0.48), Metal Skin +0.26 (+0.37), Spellbreaker +0.22 (+0.37)
- **McGinnis**: Spirit Resilience +0.00 (+0.12), Return Fire -0.01 (+0.08), Healbane -0.02 (+0.07)
- **Paradox**: Metal Skin +0.16 (+0.27), Bullet Resilience +0.14 (+0.23), Plated Armor +0.12 (+0.25)
- **Dynamo**: Healbane +0.01 (+0.09), Counterspell -0.03 (+0.05), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane -0.01 (+0.08), Counterspell -0.01 (+0.06), Witchmail -0.01 (+0.18)
- **Haze**: Plated Armor +0.08 (+0.21), Bullet Resilience +0.05 (+0.14), Indomitable +0.04 (+0.18)
- **Holliday**: Plated Armor +0.22 (+0.35), Reactive Barrier +0.04 (+0.10), Debuff Reducer +0.03 (+0.09)
- **Bebop**: Healbane +0.03 (+0.12), Counterspell +0.02 (+0.09), Metal Skin -0.01 (+0.10)
- **Calico**: Spellbreaker +0.12 (+0.27), Divine Barrier +0.11 (+0.21), Spirit Resilience +0.10 (+0.22)
- **Grey Talon**: Debuff Reducer +0.04 (+0.10), Reactive Barrier +0.04 (+0.10), Spellbreaker +0.03 (+0.18)
- **Mo & Krill**: Spellbreaker +0.12 (+0.27), Witchmail +0.07 (+0.27), Spirit Resilience +0.07 (+0.19)
- **Shiv**: Healbane -0.00 (+0.08), Return Fire -0.01 (+0.07), Counterspell -0.03 (+0.04)
- **Ivy**: Unstoppable +0.10 (+0.21), Indomitable +0.07 (+0.21), Dispel Magic -0.00 (+0.07)
- **Warden**: Return Fire +0.00 (+0.09), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.04)
- **Yamato**: Healbane +0.02 (+0.11), Counterspell -0.04 (+0.04), Debuff Reducer -0.05 (+0.01)
- **Lash**: Spellbreaker +0.31 (+0.46), Spirit Resilience +0.27 (+0.39), Divine Barrier +0.25 (+0.35)
- **Viscous**: Healbane -0.02 (+0.07), Return Fire -0.03 (+0.05), Divine Barrier -0.03 (+0.07)
- **Pocket**: Witchmail +0.06 (+0.25), Spirit Resilience +0.05 (+0.17), Dispel Magic +0.04 (+0.11)
- **Mirage**: Dispel Magic +0.37 (+0.45), Spellbreaker +0.07 (+0.21), Spirit Resilience +0.06 (+0.18)
- **Vyper**: Indomitable +0.28 (+0.42), Debuff Reducer +0.04 (+0.10), Unstoppable +0.02 (+0.14)
- **Sinclair**: Indomitable +0.08 (+0.22), Spellbreaker +0.02 (+0.17), Unstoppable +0.01 (+0.13)
- **Mina**: Witchmail +0.03 (+0.22), Return Fire +0.02 (+0.10), Counterspell -0.00 (+0.07)
- **Drifter**: Witchmail +0.04 (+0.24), Return Fire +0.04 (+0.12), Counterspell +0.04 (+0.11)
- **Venator**: Bullet Resilience +0.15 (+0.24), Divine Barrier +0.09 (+0.19), Metal Skin +0.08 (+0.19)
- **Victor**: Spirit Resilience +0.04 (+0.16), Spellbreaker +0.01 (+0.16), Healbane +0.01 (+0.10)
- **Paige**: Healbane -0.01 (+0.08), Counterspell -0.02 (+0.05), Return Fire -0.02 (+0.06)
- **The Doorman**: Indomitable +0.15 (+0.29), Witchmail +0.11 (+0.31), Spellbreaker +0.10 (+0.25)
- **Billy**: Spellbreaker +0.04 (+0.19), Spirit Resilience +0.04 (+0.16), Counterspell +0.04 (+0.11)
- **Graves**: Metal Skin +0.08 (+0.19), Witchmail +0.08 (+0.28), Spirit Resilience +0.08 (+0.20)
- **Apollo**: Healbane -0.00 (+0.08), Unstoppable -0.01 (+0.11), Reactive Barrier -0.01 (+0.05)
- **Deadman Danny**: Indomitable +0.23 (+0.37), Spellbreaker +0.22 (+0.37), Witchmail +0.18 (+0.38)
- **Rem**: Witchmail -0.01 (+0.19), Unstoppable -0.01 (+0.10), Dispel Magic -0.01 (+0.06)
- **Silver**: Dispel Magic +0.12 (+0.20), Reactive Barrier +0.03 (+0.09), Return Fire +0.02 (+0.10)
- **Celeste**: Spirit Resilience +0.09 (+0.22), Witchmail +0.08 (+0.28), Dispel Magic +0.04 (+0.11)
- **Rat King**: Counterspell +0.00 (+0.08), Bullet Resilience -0.01 (+0.09), Divine Barrier -0.01 (+0.09)
- **Solomon**: Return Fire -0.01 (+0.07), Counterspell -0.02 (+0.05), Reactive Barrier -0.03 (+0.03)
- **Violet**: Return Fire +0.03 (+0.11), Healbane -0.03 (+0.06), Counterspell -0.04 (+0.03)
- **Nurse Harrow**: Healbane +0.05 (+0.14), Counterspell -0.02 (+0.05), Debuff Reducer -0.04 (+0.02)
- **Baba**: Healbane -0.00 (+0.08), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.04)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.162 | +0.051 | +0.111 | Lash +0.33, Pocket +0.22, Deadman Danny +0.21 | 10 heroes |
| Divine Barrier | 6,400 | +0.244 | +0.039 | +0.059 | Lash +0.19, Wraith +0.11, The Doorman +0.09 | 1 heroes |
| Dispel Magic | 3,200 | +0.074 | +0.023 | +0.044 | Mirage +0.31, Infernus +0.10, Pocket +0.08 | 7 heroes |
| Indomitable | 6,400 | +0.134 | +0.022 | +0.109 | Vyper +0.35, Wraith +0.24, Deadman Danny +0.13 | 0 heroes |
| Witchmail | 6,400 | +0.128 | +0.020 | +0.159 | Lash +0.18, Graves +0.15, Pocket +0.15 | 0 heroes |
| Spellbreaker | 6,400 | +0.099 | +0.015 | +0.117 | Lash +0.35, Deadman Danny +0.16, Pocket +0.14 | 0 heroes |
| Reactive Barrier | 1,600 | +0.020 | +0.013 | +0.038 | Deadman Danny +0.10, Wraith +0.09, Graves +0.09 | 4 heroes |
| Debuff Reducer | 1,600 | -0.006 | -0.004 | +0.037 | Wraith +0.08, Vyper +0.05, Lash +0.04 | 1 heroes |
| Plated Armor | 6,400 | -0.026 | -0.004 | +0.098 | Deadman Danny +0.23, Wraith +0.12, Paradox +0.10 | 0 heroes |
| Bullet Resilience | 3,200 | -0.032 | -0.010 | +0.057 | Venator +0.12, Paradox +0.10, Wraith +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.036 | -0.011 | +0.040 | Vindicta +0.04, Wraith +0.03, Graves +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.080 | -0.013 | +0.081 | Mo & Krill +0.12, Ivy +0.10, Haze +0.08 | 0 heroes |
| Healbane | 1,600 | -0.034 | -0.021 | +0.062 | Yamato +0.08, Bebop +0.05, Kelvin +0.04 | 17 heroes |
| Metal Skin | 3,200 | -0.162 | -0.051 | +0.082 | Wraith +0.20, Paradox +0.15, Lash +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.180 | -0.112 | +0.053 | Wraith +0.08, Lady Geist +0.06, Paradox +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.14), Unstoppable +0.05 (+0.13), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.04 (+0.20), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Vindicta**: Witchmail +0.05 (+0.20), Counterspell +0.04 (+0.08), Divine Barrier +0.03 (+0.09)
- **Lady Geist**: Return Fire +0.06 (+0.12), Metal Skin +0.06 (+0.14), Divine Barrier +0.05 (+0.10)
- **Abrams**: Indomitable +0.09 (+0.20), Unstoppable +0.07 (+0.15), Healbane +0.02 (+0.08)
- **Wraith**: Indomitable +0.24 (+0.35), Metal Skin +0.20 (+0.28), Plated Armor +0.12 (+0.22)
- **McGinnis**: Spirit Resilience +0.08 (+0.20), Return Fire +0.02 (+0.07), Healbane +0.02 (+0.08)
- **Paradox**: Metal Skin +0.15 (+0.23), Bullet Resilience +0.10 (+0.16), Plated Armor +0.10 (+0.20)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.05 (+0.16), Healbane +0.04 (+0.11), Dispel Magic +0.03 (+0.07)
- **Haze**: Indomitable +0.09 (+0.20), Plated Armor +0.08 (+0.18), Unstoppable +0.08 (+0.16)
- **Holliday**: Return Fire +0.05 (+0.10), Indomitable +0.03 (+0.14), Debuff Reducer +0.03 (+0.07)
- **Bebop**: Healbane +0.05 (+0.11), Metal Skin +0.01 (+0.09), Counterspell -0.00 (+0.04)
- **Calico**: Reactive Barrier +0.06 (+0.10), Divine Barrier +0.05 (+0.11), Spellbreaker +0.05 (+0.17)
- **Grey Talon**: Debuff Reducer +0.03 (+0.07), Reactive Barrier +0.02 (+0.06), Spellbreaker +0.02 (+0.14)
- **Mo & Krill**: Unstoppable +0.12 (+0.20), Dispel Magic +0.05 (+0.10), Spellbreaker +0.04 (+0.16)
- **Shiv**: Metal Skin +0.04 (+0.12), Bullet Resilience +0.04 (+0.09), Divine Barrier +0.04 (+0.09)
- **Ivy**: Unstoppable +0.10 (+0.18), Indomitable +0.08 (+0.19), Debuff Reducer +0.01 (+0.05)
- **Warden**: Return Fire +0.02 (+0.08), Counterspell +0.00 (+0.04), Debuff Reducer -0.00 (+0.04)
- **Yamato**: Healbane +0.08 (+0.14), Counterspell +0.02 (+0.06), Bullet Resilience +0.02 (+0.07)
- **Lash**: Spellbreaker +0.35 (+0.47), Spirit Resilience +0.33 (+0.44), Divine Barrier +0.19 (+0.25)
- **Viscous**: Counterspell +0.01 (+0.05), Divine Barrier +0.01 (+0.06), Debuff Reducer -0.01 (+0.03)
- **Pocket**: Spirit Resilience +0.22 (+0.34), Witchmail +0.15 (+0.30), Spellbreaker +0.14 (+0.26)
- **Mirage**: Dispel Magic +0.31 (+0.36), Spirit Resilience +0.06 (+0.17), Metal Skin +0.05 (+0.13)
- **Vyper**: Indomitable +0.35 (+0.46), Metal Skin +0.06 (+0.14), Debuff Reducer +0.05 (+0.09)
- **Sinclair**: Indomitable +0.07 (+0.18), Return Fire +0.00 (+0.05), Spellbreaker -0.01 (+0.11)
- **Mina**: Witchmail +0.04 (+0.20), Plated Armor +0.02 (+0.12), Spirit Resilience +0.02 (+0.13)
- **Drifter**: Witchmail +0.04 (+0.20), Bullet Resilience +0.01 (+0.07), Counterspell +0.00 (+0.04)
- **Venator**: Bullet Resilience +0.12 (+0.17), Metal Skin +0.11 (+0.19), Divine Barrier +0.05 (+0.11)
- **Victor**: Spellbreaker +0.06 (+0.18), Spirit Resilience +0.06 (+0.17), Dispel Magic -0.01 (+0.03)
- **Paige**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.04), Healbane -0.01 (+0.05)
- **The Doorman**: Spirit Resilience +0.15 (+0.26), Indomitable +0.11 (+0.22), Witchmail +0.09 (+0.25)
- **Billy**: Spirit Resilience +0.02 (+0.13), Counterspell +0.00 (+0.04), Spellbreaker -0.00 (+0.12)
- **Graves**: Witchmail +0.15 (+0.31), Metal Skin +0.12 (+0.20), Spirit Resilience +0.11 (+0.22)
- **Apollo**: Reactive Barrier +0.06 (+0.10), Indomitable +0.05 (+0.15), Unstoppable +0.00 (+0.08)
- **Deadman Danny**: Plated Armor +0.23 (+0.33), Spirit Resilience +0.21 (+0.33), Spellbreaker +0.16 (+0.28)
- **Rem**: Counterspell +0.01 (+0.05), Divine Barrier +0.00 (+0.06), Unstoppable +0.00 (+0.08)
- **Silver**: Dispel Magic +0.08 (+0.12), Metal Skin +0.06 (+0.14), Reactive Barrier +0.03 (+0.07)
- **Celeste**: Spirit Resilience +0.05 (+0.16), Witchmail +0.01 (+0.17), Healbane -0.01 (+0.06)
- **Rat King**: Bullet Resilience -0.00 (+0.05), Return Fire -0.00 (+0.05), Metal Skin -0.01 (+0.07)
- **Solomon**: Return Fire +0.00 (+0.06), Counterspell -0.00 (+0.04), Healbane -0.02 (+0.05)
- **Violet**: Return Fire +0.04 (+0.09), Witchmail +0.03 (+0.19), Healbane +0.01 (+0.08)
- **Nurse Harrow**: Dispel Magic -0.02 (+0.02), Healbane -0.02 (+0.04), Counterspell -0.03 (+0.01)
- **Baba**: Unstoppable +0.03 (+0.11), Healbane +0.02 (+0.08), Debuff Reducer -0.00 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.158 | +0.050 | +0.128 | Lash +0.30, Deadman Danny +0.25, Wraith +0.12 | 14 heroes |
| Divine Barrier | 6,400 | +0.216 | +0.034 | +0.066 | Lash +0.22, Vindicta +0.12, Wraith +0.09 | 2 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.064 | Lash +0.30, Mirage +0.29, Paradox +0.10 | 9 heroes |
| Indomitable | 6,400 | +0.151 | +0.025 | +0.138 | Vyper +0.37, Wraith +0.29, Deadman Danny +0.24 | 0 heroes |
| Witchmail | 6,400 | +0.130 | +0.020 | +0.175 | Lash +0.19, Deadman Danny +0.18, Wraith +0.13 | 1 heroes |
| Spellbreaker | 6,400 | +0.111 | +0.017 | +0.138 | Lash +0.41, Deadman Danny +0.22, Wraith +0.14 | 0 heroes |
| Reactive Barrier | 1,600 | +0.008 | +0.005 | +0.041 | Deadman Danny +0.15, Yamato +0.11, Wraith +0.08 | 5 heroes |
| Plated Armor | 6,400 | -0.016 | -0.003 | +0.118 | Deadman Danny +0.22, Holliday +0.18, Wraith +0.15 | 0 heroes |
| Debuff Reducer | 1,600 | -0.009 | -0.006 | +0.048 | Grey Talon +0.09, Deadman Danny +0.08, Vyper +0.07 | 0 heroes |
| Counterspell | 3,200 | -0.036 | -0.011 | +0.038 | Deadman Danny +0.07, Drifter +0.05, Yamato +0.05 | 1 heroes |
| Unstoppable | 6,400 | -0.078 | -0.012 | +0.104 | Deadman Danny +0.17, Abrams +0.12, Grey Talon +0.12 | 3 heroes |
| Bullet Resilience | 3,200 | -0.040 | -0.013 | +0.065 | Deadman Danny +0.12, Vindicta +0.12, Lash +0.10 | 1 heroes |
| Healbane | 1,600 | -0.033 | -0.021 | +0.063 | Drifter +0.07, Infernus +0.04, Nurse Harrow +0.04 | 15 heroes |
| Metal Skin | 3,200 | -0.152 | -0.047 | +0.108 | Wraith +0.25, Lash +0.19, Venator +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.173 | -0.108 | +0.057 | Wraith +0.09, Paradox +0.06, Vindicta +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.16), Unstoppable +0.10 (+0.20), Spellbreaker +0.09 (+0.23)
- **Seven**: Witchmail +0.04 (+0.21), Healbane +0.00 (+0.07), Counterspell -0.01 (+0.03)
- **Vindicta**: Bullet Resilience +0.12 (+0.18), Divine Barrier +0.12 (+0.18), Witchmail +0.08 (+0.25)
- **Lady Geist**: Return Fire +0.05 (+0.10), Bullet Resilience +0.03 (+0.09), Metal Skin +0.03 (+0.13)
- **Abrams**: Unstoppable +0.12 (+0.23), Dispel Magic +0.05 (+0.11), Healbane +0.01 (+0.08)
- **Wraith**: Indomitable +0.29 (+0.43), Metal Skin +0.25 (+0.36), Plated Armor +0.15 (+0.27)
- **McGinnis**: Spirit Resilience +0.10 (+0.23), Witchmail +0.03 (+0.21), Spellbreaker +0.01 (+0.15)
- **Paradox**: Spellbreaker +0.14 (+0.28), Witchmail +0.11 (+0.29), Dispel Magic +0.10 (+0.17)
- **Dynamo**: Healbane +0.02 (+0.08), Counterspell -0.00 (+0.04), Debuff Reducer -0.04 (+0.01)
- **Kelvin**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.03), Spirit Resilience -0.03 (+0.10)
- **Haze**: Plated Armor +0.09 (+0.21), Indomitable +0.08 (+0.22), Unstoppable +0.06 (+0.17)
- **Holliday**: Plated Armor +0.18 (+0.30), Indomitable +0.03 (+0.17), Return Fire +0.03 (+0.09)
- **Bebop**: Healbane +0.02 (+0.08), Counterspell -0.02 (+0.02), Metal Skin -0.02 (+0.09)
- **Calico**: Reactive Barrier +0.05 (+0.09), Spirit Resilience +0.04 (+0.17), Divine Barrier +0.03 (+0.10)
- **Grey Talon**: Spellbreaker +0.13 (+0.27), Unstoppable +0.12 (+0.22), Debuff Reducer +0.09 (+0.14)
- **Mo & Krill**: Unstoppable +0.07 (+0.18), Spirit Resilience +0.05 (+0.18), Spellbreaker +0.04 (+0.18)
- **Shiv**: Metal Skin +0.04 (+0.14), Bullet Resilience +0.02 (+0.09), Divine Barrier +0.02 (+0.08)
- **Ivy**: Unstoppable +0.10 (+0.20), Indomitable +0.06 (+0.19), Debuff Reducer +0.01 (+0.06)
- **Warden**: Return Fire +0.02 (+0.08), Counterspell +0.01 (+0.05), Divine Barrier +0.01 (+0.08)
- **Yamato**: Reactive Barrier +0.11 (+0.15), Indomitable +0.11 (+0.24), Counterspell +0.05 (+0.09)
- **Lash**: Spellbreaker +0.41 (+0.55), Spirit Resilience +0.30 (+0.43), Dispel Magic +0.30 (+0.36)
- **Viscous**: Healbane +0.02 (+0.08), Divine Barrier +0.02 (+0.08), Counterspell +0.00 (+0.04)
- **Pocket**: Spirit Resilience +0.09 (+0.22), Witchmail +0.03 (+0.21), Spellbreaker +0.01 (+0.15)
- **Mirage**: Dispel Magic +0.29 (+0.35), Spirit Resilience +0.03 (+0.16), Metal Skin +0.02 (+0.13)
- **Vyper**: Indomitable +0.37 (+0.51), Debuff Reducer +0.07 (+0.12), Unstoppable +0.05 (+0.16)
- **Sinclair**: Indomitable +0.13 (+0.27), Return Fire +0.00 (+0.06), Unstoppable -0.01 (+0.09)
- **Mina**: Spirit Resilience +0.12 (+0.24), Witchmail +0.09 (+0.27), Divine Barrier +0.05 (+0.12)
- **Drifter**: Spirit Resilience +0.10 (+0.22), Witchmail +0.07 (+0.25), Healbane +0.07 (+0.13)
- **Venator**: Metal Skin +0.10 (+0.21), Bullet Resilience +0.08 (+0.14), Divine Barrier +0.03 (+0.10)
- **Victor**: Spirit Resilience +0.01 (+0.14), Healbane +0.01 (+0.07), Spellbreaker +0.00 (+0.14)
- **Paige**: Unstoppable +0.11 (+0.21), Debuff Reducer +0.05 (+0.10), Counterspell -0.01 (+0.03)
- **The Doorman**: Spirit Resilience +0.12 (+0.25), Indomitable +0.11 (+0.25), Witchmail +0.08 (+0.26)
- **Billy**: Reactive Barrier +0.01 (+0.05), Healbane -0.00 (+0.06), Debuff Reducer -0.01 (+0.03)
- **Graves**: Return Fire +0.02 (+0.08), Witchmail +0.02 (+0.19), Counterspell +0.01 (+0.05)
- **Apollo**: Healbane -0.01 (+0.05), Reactive Barrier -0.03 (+0.02), Counterspell -0.03 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.25 (+0.38), Indomitable +0.24 (+0.38), Plated Armor +0.22 (+0.34)
- **Rem**: Debuff Reducer +0.06 (+0.11), Unstoppable +0.04 (+0.15), Counterspell -0.00 (+0.03)
- **Silver**: Dispel Magic +0.04 (+0.11), Return Fire -0.00 (+0.06), Indomitable -0.00 (+0.14)
- **Celeste**: Witchmail +0.05 (+0.23), Dispel Magic +0.04 (+0.11), Spellbreaker +0.02 (+0.16)
- **Rat King**: Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.05), Bullet Resilience -0.02 (+0.05)
- **Solomon**: Reactive Barrier +0.01 (+0.05), Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.05)
- **Violet**: Witchmail +0.06 (+0.24), Return Fire +0.04 (+0.10), Healbane +0.03 (+0.09)
- **Nurse Harrow**: Healbane +0.04 (+0.10), Counterspell +0.00 (+0.04), Return Fire -0.03 (+0.02)
- **Baba**: Healbane -0.00 (+0.06), Unstoppable -0.01 (+0.09), Counterspell -0.01 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.179 | +0.056 | +0.135 | Lash +0.57, Deadman Danny +0.35, The Doorman +0.32 | 15 heroes |
| Indomitable | 6,400 | +0.166 | +0.027 | +0.157 | Deadman Danny +0.28, Vyper +0.27, Wraith +0.26 | 1 heroes |
| Divine Barrier | 6,400 | +0.167 | +0.026 | +0.058 | Lash +0.28, The Doorman +0.15, Calico +0.13 | 3 heroes |
| Dispel Magic | 3,200 | +0.075 | +0.023 | +0.051 | Mirage +0.28, Silver +0.22, Lash +0.21 | 9 heroes |
| Witchmail | 6,400 | +0.120 | +0.019 | +0.157 | Lash +0.31, The Doorman +0.24, Deadman Danny +0.19 | 2 heroes |
| Spellbreaker | 6,400 | +0.118 | +0.018 | +0.137 | Lash +0.46, Deadman Danny +0.24, The Doorman +0.18 | 0 heroes |
| Plated Armor | 6,400 | -0.031 | -0.005 | +0.096 | Vindicta +0.17, Lash +0.14, Vyper +0.14 | 2 heroes |
| Unstoppable | 6,400 | -0.075 | -0.012 | +0.112 | Haze +0.24, Infernus +0.23, Grey Talon +0.15 | 8 heroes |
| Counterspell | 3,200 | -0.041 | -0.013 | +0.030 | Lash +0.12, The Doorman +0.06, Yamato +0.04 | 1 heroes |
| Bullet Resilience | 3,200 | -0.048 | -0.015 | +0.056 | Lash +0.17, Vindicta +0.15, Venator +0.11 | 0 heroes |
| Reactive Barrier | 1,600 | -0.024 | -0.015 | +0.035 | Deadman Danny +0.14, Drifter +0.14, The Doorman +0.11 | 3 heroes |
| Debuff Reducer | 1,600 | -0.025 | -0.016 | +0.040 | Grey Talon +0.11, Bebop +0.07, Rem +0.07 | 0 heroes |
| Healbane | 1,600 | -0.039 | -0.024 | +0.051 | Nurse Harrow +0.07, Lady Geist +0.06, Celeste +0.04 | 14 heroes |
| Metal Skin | 3,200 | -0.154 | -0.048 | +0.105 | Lash +0.28, Grey Talon +0.17, Silver +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.173 | -0.108 | +0.046 | Paradox +0.06, Vindicta +0.05, Haze +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.23 (+0.34), Dispel Magic +0.06 (+0.11), Spellbreaker +0.04 (+0.18)
- **Seven**: Witchmail +0.06 (+0.22), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.04)
- **Vindicta**: Plated Armor +0.17 (+0.27), Bullet Resilience +0.15 (+0.21), Divine Barrier +0.12 (+0.18)
- **Lady Geist**: Healbane +0.06 (+0.11), Dispel Magic +0.03 (+0.08), Metal Skin +0.01 (+0.11)
- **Abrams**: Unstoppable +0.06 (+0.17), Indomitable +0.04 (+0.19), Dispel Magic +0.03 (+0.08)
- **Wraith**: Indomitable +0.26 (+0.42), Metal Skin +0.10 (+0.20), Return Fire +0.04 (+0.09)
- **McGinnis**: Spirit Resilience +0.04 (+0.17), Healbane +0.02 (+0.07), Witchmail +0.01 (+0.17)
- **Paradox**: Unstoppable +0.10 (+0.21), Witchmail +0.10 (+0.26), Spirit Resilience +0.07 (+0.20)
- **Dynamo**: Healbane +0.02 (+0.07), Counterspell -0.00 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.07 (+0.20), Spellbreaker +0.01 (+0.15), Healbane +0.01 (+0.06)
- **Haze**: Unstoppable +0.24 (+0.35), Metal Skin +0.07 (+0.17), Bullet Resilience +0.06 (+0.12)
- **Holliday**: Spellbreaker +0.04 (+0.18), Return Fire +0.03 (+0.07), Debuff Reducer +0.03 (+0.07)
- **Bebop**: Debuff Reducer +0.07 (+0.11), Unstoppable +0.01 (+0.12), Spellbreaker +0.00 (+0.14)
- **Calico**: Divine Barrier +0.13 (+0.18), Spirit Resilience +0.12 (+0.26), Spellbreaker +0.10 (+0.23)
- **Grey Talon**: Spellbreaker +0.17 (+0.31), Metal Skin +0.17 (+0.27), Unstoppable +0.15 (+0.27)
- **Mo & Krill**: Dispel Magic +0.04 (+0.09), Unstoppable +0.03 (+0.15), Healbane +0.03 (+0.08)
- **Shiv**: Metal Skin +0.02 (+0.13), Bullet Resilience +0.01 (+0.07), Divine Barrier +0.01 (+0.07)
- **Ivy**: Unstoppable +0.13 (+0.24), Indomitable +0.09 (+0.24), Debuff Reducer +0.05 (+0.09)
- **Warden**: Plated Armor +0.06 (+0.16), Metal Skin +0.04 (+0.14), Return Fire +0.02 (+0.07)
- **Yamato**: Indomitable +0.12 (+0.28), Plated Armor +0.09 (+0.19), Unstoppable +0.05 (+0.16)
- **Lash**: Spirit Resilience +0.57 (+0.71), Spellbreaker +0.46 (+0.60), Witchmail +0.31 (+0.47)
- **Viscous**: Divine Barrier +0.08 (+0.13), Witchmail +0.05 (+0.20), Return Fire +0.04 (+0.08)
- **Pocket**: Spirit Resilience +0.08 (+0.21), Spellbreaker +0.01 (+0.14), Witchmail +0.00 (+0.16)
- **Mirage**: Dispel Magic +0.28 (+0.33), Metal Skin +0.07 (+0.18), Plated Armor +0.01 (+0.10)
- **Vyper**: Indomitable +0.27 (+0.43), Plated Armor +0.14 (+0.24), Metal Skin +0.08 (+0.19)
- **Sinclair**: Indomitable +0.14 (+0.30), Dispel Magic +0.06 (+0.12), Reactive Barrier +0.06 (+0.09)
- **Mina**: Divine Barrier +0.01 (+0.06), Dispel Magic -0.01 (+0.04), Witchmail -0.01 (+0.14)
- **Drifter**: Indomitable +0.21 (+0.37), Spirit Resilience +0.20 (+0.34), Reactive Barrier +0.14 (+0.17)
- **Venator**: Metal Skin +0.14 (+0.24), Bullet Resilience +0.11 (+0.16), Plated Armor +0.05 (+0.15)
- **Victor**: Spellbreaker +0.09 (+0.22), Spirit Resilience +0.05 (+0.19), Healbane +0.03 (+0.08)
- **Paige**: Counterspell +0.01 (+0.04), Return Fire -0.00 (+0.04), Healbane -0.01 (+0.04)
- **The Doorman**: Spirit Resilience +0.32 (+0.46), Witchmail +0.24 (+0.40), Indomitable +0.23 (+0.39)
- **Billy**: Reactive Barrier +0.07 (+0.10), Counterspell +0.02 (+0.05), Plated Armor +0.02 (+0.12)
- **Graves**: Return Fire +0.02 (+0.07), Reactive Barrier -0.01 (+0.02), Witchmail -0.01 (+0.14)
- **Apollo**: Reactive Barrier +0.02 (+0.06), Healbane +0.01 (+0.06), Unstoppable -0.01 (+0.10)
- **Deadman Danny**: Spirit Resilience +0.35 (+0.48), Indomitable +0.28 (+0.43), Spellbreaker +0.24 (+0.38)
- **Rem**: Debuff Reducer +0.07 (+0.11), Spellbreaker +0.04 (+0.18), Return Fire +0.01 (+0.05)
- **Silver**: Dispel Magic +0.22 (+0.27), Metal Skin +0.15 (+0.26), Indomitable +0.11 (+0.27)
- **Celeste**: Witchmail +0.08 (+0.24), Spirit Resilience +0.07 (+0.20), Healbane +0.04 (+0.10)
- **Rat King**: Return Fire -0.00 (+0.04), Healbane -0.01 (+0.04), Counterspell -0.01 (+0.02)
- **Solomon**: Reactive Barrier +0.00 (+0.04), Counterspell -0.01 (+0.02), Debuff Reducer -0.01 (+0.03)
- **Violet**: Return Fire +0.03 (+0.08), Witchmail +0.01 (+0.16), Counterspell -0.00 (+0.03)
- **Nurse Harrow**: Dispel Magic +0.10 (+0.16), Spirit Resilience +0.10 (+0.24), Witchmail +0.09 (+0.24)
- **Baba**: Healbane +0.00 (+0.05), Witchmail -0.01 (+0.15), Counterspell -0.01 (+0.02)
