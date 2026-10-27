# Counter items in the sim (phantom and up)

Built 2026-10-27T20:34:17Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.185 | +0.058 | +0.119 | Lash +0.29, Deadman Danny +0.16, Wraith +0.14 | 1 heroes |
| Divine Barrier | 6,400 | +0.340 | +0.054 | +0.095 | Lash +0.23, Wraith +0.16, Venator +0.09 | 0 heroes |
| Dispel Magic | 3,200 | +0.095 | +0.030 | +0.071 | Mirage +0.39, Lash +0.12, Infernus +0.10 | 4 heroes |
| Reactive Barrier | 1,600 | +0.043 | +0.027 | +0.059 | Deadman Danny +0.13, Wraith +0.12, Calico +0.11 | 3 heroes |
| Indomitable | 6,400 | +0.168 | +0.027 | +0.139 | Vyper +0.28, Wraith +0.25, Deadman Danny +0.23 | 0 heroes |
| Witchmail | 6,400 | +0.147 | +0.023 | +0.198 | Lash +0.23, Deadman Danny +0.19, Wraith +0.14 | 0 heroes |
| Debuff Reducer | 1,600 | +0.023 | +0.015 | +0.058 | Wraith +0.09, Deadman Danny +0.08, Holliday +0.07 | 0 heroes |
| Spellbreaker | 6,400 | +0.082 | +0.013 | +0.145 | Lash +0.28, Deadman Danny +0.22, Wraith +0.17 | 0 heroes |
| Bullet Resilience | 3,200 | -0.001 | -0.000 | +0.087 | Venator +0.15, Paradox +0.11, Wraith +0.11 | 0 heroes |
| Plated Armor | 6,400 | -0.039 | -0.006 | +0.124 | Holliday +0.26, Wraith +0.18, Deadman Danny +0.16 | 0 heroes |
| Healbane | 1,600 | -0.010 | -0.006 | +0.087 | Lash +0.09, Deadman Danny +0.05, Abrams +0.05 | 11 heroes |
| Counterspell | 3,200 | -0.027 | -0.008 | +0.069 | Deadman Danny +0.09, Lash +0.09, Billy +0.05 | 1 heroes |
| Unstoppable | 6,400 | -0.057 | -0.009 | +0.110 | Deadman Danny +0.16, Abrams +0.11, Wraith +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.151 | -0.047 | +0.103 | Wraith +0.23, Lash +0.21, Paradox +0.13 | 0 heroes |
| Return Fire | 1,600 | -0.176 | -0.110 | +0.077 | Lady Geist +0.07, Lash +0.07, Deadman Danny +0.07 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.17), Unstoppable +0.05 (+0.16), Spirit Resilience +0.04 (+0.16)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.02 (+0.04), Dispel Magic -0.03 (+0.04)
- **Vindicta**: Return Fire +0.01 (+0.09), Divine Barrier +0.01 (+0.10), Witchmail +0.01 (+0.21)
- **Lady Geist**: Return Fire +0.07 (+0.15), Dispel Magic +0.04 (+0.11), Divine Barrier +0.03 (+0.12)
- **Abrams**: Indomitable +0.19 (+0.33), Unstoppable +0.11 (+0.22), Divine Barrier +0.09 (+0.18)
- **Wraith**: Indomitable +0.25 (+0.38), Metal Skin +0.23 (+0.33), Plated Armor +0.18 (+0.30)
- **McGinnis**: Spirit Resilience +0.00 (+0.12), Return Fire -0.00 (+0.07), Healbane -0.01 (+0.07)
- **Paradox**: Metal Skin +0.13 (+0.23), Bullet Resilience +0.11 (+0.20), Plated Armor +0.10 (+0.22)
- **Dynamo**: Healbane -0.01 (+0.08), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane +0.00 (+0.09), Counterspell -0.01 (+0.06), Debuff Reducer -0.02 (+0.04)
- **Haze**: Plated Armor +0.07 (+0.20), Bullet Resilience +0.04 (+0.13), Indomitable +0.02 (+0.16)
- **Holliday**: Plated Armor +0.26 (+0.39), Spellbreaker +0.10 (+0.24), Indomitable +0.09 (+0.23)
- **Bebop**: Healbane +0.02 (+0.11), Counterspell +0.02 (+0.09), Metal Skin +0.00 (+0.10)
- **Calico**: Spellbreaker +0.11 (+0.25), Reactive Barrier +0.11 (+0.17), Divine Barrier +0.09 (+0.19)
- **Grey Talon**: Reactive Barrier +0.05 (+0.11), Indomitable +0.04 (+0.18), Spellbreaker +0.04 (+0.19)
- **Mo & Krill**: Spellbreaker +0.12 (+0.27), Spirit Resilience +0.07 (+0.19), Witchmail +0.06 (+0.26)
- **Shiv**: Healbane -0.01 (+0.08), Return Fire -0.02 (+0.06), Spirit Resilience -0.03 (+0.09)
- **Ivy**: Indomitable +0.10 (+0.24), Unstoppable +0.09 (+0.20), Metal Skin +0.01 (+0.11)
- **Warden**: Return Fire +0.05 (+0.12), Bullet Resilience +0.03 (+0.11), Counterspell +0.02 (+0.09)
- **Yamato**: Healbane +0.03 (+0.12), Counterspell -0.02 (+0.04), Debuff Reducer -0.03 (+0.03)
- **Lash**: Spirit Resilience +0.29 (+0.41), Spellbreaker +0.28 (+0.43), Witchmail +0.23 (+0.43)
- **Viscous**: Healbane -0.02 (+0.07), Return Fire -0.03 (+0.05), Debuff Reducer -0.03 (+0.03)
- **Pocket**: Witchmail +0.05 (+0.25), Spirit Resilience +0.04 (+0.16), Dispel Magic +0.03 (+0.11)
- **Mirage**: Dispel Magic +0.39 (+0.46), Spirit Resilience +0.12 (+0.24), Spellbreaker +0.09 (+0.24)
- **Vyper**: Indomitable +0.28 (+0.42), Debuff Reducer +0.05 (+0.11), Spellbreaker +0.03 (+0.18)
- **Sinclair**: Indomitable +0.05 (+0.19), Spellbreaker +0.00 (+0.15), Reactive Barrier -0.01 (+0.05)
- **Mina**: Return Fire +0.02 (+0.10), Witchmail +0.01 (+0.21), Counterspell -0.00 (+0.07)
- **Drifter**: Counterspell +0.00 (+0.07), Return Fire -0.00 (+0.08), Witchmail -0.00 (+0.19)
- **Venator**: Bullet Resilience +0.15 (+0.24), Divine Barrier +0.09 (+0.19), Metal Skin +0.08 (+0.18)
- **Victor**: Spirit Resilience +0.02 (+0.14), Healbane +0.01 (+0.10), Dispel Magic -0.01 (+0.06)
- **Paige**: Return Fire +0.00 (+0.08), Counterspell -0.01 (+0.06), Reactive Barrier -0.02 (+0.03)
- **The Doorman**: Indomitable +0.12 (+0.26), Witchmail +0.09 (+0.29), Reactive Barrier +0.06 (+0.12)
- **Billy**: Counterspell +0.05 (+0.11), Spellbreaker +0.04 (+0.19), Spirit Resilience +0.04 (+0.16)
- **Graves**: Spirit Resilience +0.09 (+0.21), Metal Skin +0.08 (+0.19), Witchmail +0.08 (+0.28)
- **Apollo**: Healbane +0.01 (+0.10), Unstoppable +0.00 (+0.11), Reactive Barrier -0.02 (+0.04)
- **Deadman Danny**: Indomitable +0.23 (+0.37), Spellbreaker +0.22 (+0.37), Witchmail +0.19 (+0.39)
- **Rem**: Debuff Reducer +0.04 (+0.10), Unstoppable +0.04 (+0.15), Counterspell -0.03 (+0.04)
- **Silver**: Dispel Magic +0.07 (+0.14), Debuff Reducer +0.04 (+0.10), Indomitable +0.02 (+0.16)
- **Celeste**: Spirit Resilience +0.10 (+0.22), Witchmail +0.08 (+0.28), Dispel Magic +0.03 (+0.10)
- **Rat King**: Counterspell -0.00 (+0.07), Return Fire -0.01 (+0.07), Bullet Resilience -0.01 (+0.07)
- **Solomon**: Return Fire -0.02 (+0.06), Counterspell -0.03 (+0.04), Reactive Barrier -0.03 (+0.03)
- **Violet**: Return Fire +0.02 (+0.09), Witchmail -0.03 (+0.17), Divine Barrier -0.03 (+0.06)
- **Nurse Harrow**: Healbane +0.01 (+0.10), Return Fire -0.04 (+0.03), Dispel Magic -0.05 (+0.02)
- **Baba**: Healbane +0.00 (+0.09), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.04)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.163 | +0.051 | +0.113 | Lash +0.33, Pocket +0.23, Mina +0.15 | 9 heroes |
| Divine Barrier | 6,400 | +0.253 | +0.040 | +0.072 | Lash +0.19, Mina +0.10, Wraith +0.09 | 1 heroes |
| Dispel Magic | 3,200 | +0.086 | +0.027 | +0.055 | Mirage +0.29, Abrams +0.10, Deadman Danny +0.10 | 6 heroes |
| Witchmail | 6,400 | +0.149 | +0.023 | +0.170 | Lash +0.17, Deadman Danny +0.14, Pocket +0.12 | 0 heroes |
| Indomitable | 6,400 | +0.139 | +0.022 | +0.117 | Vyper +0.38, Wraith +0.22, Deadman Danny +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.102 | +0.016 | +0.122 | Lash +0.35, Pocket +0.14, Deadman Danny +0.12 | 0 heroes |
| Reactive Barrier | 1,600 | +0.019 | +0.012 | +0.037 | Paradox +0.09, Wraith +0.08, Silver +0.08 | 4 heroes |
| Plated Armor | 6,400 | -0.027 | -0.004 | +0.097 | Holliday +0.20, Paradox +0.11, Wraith +0.11 | 0 heroes |
| Debuff Reducer | 1,600 | -0.012 | -0.007 | +0.039 | Vyper +0.08, Wraith +0.08, Deadman Danny +0.05 | 1 heroes |
| Bullet Resilience | 3,200 | -0.027 | -0.008 | +0.067 | Paradox +0.12, Venator +0.11, Deadman Danny +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.034 | -0.011 | +0.044 | Deadman Danny +0.04, Paradox +0.03, Vindicta +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.075 | -0.012 | +0.092 | Abrams +0.18, Deadman Danny +0.12, Mo & Krill +0.11 | 0 heroes |
| Healbane | 1,600 | -0.038 | -0.024 | +0.066 | Abrams +0.05, Yamato +0.04, Wraith +0.04 | 17 heroes |
| Metal Skin | 3,200 | -0.166 | -0.052 | +0.085 | Wraith +0.19, Paradox +0.13, Lash +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.183 | -0.114 | +0.054 | Lady Geist +0.08, Wraith +0.07, Holliday +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.08 (+0.14), Unstoppable +0.04 (+0.13), Healbane +0.03 (+0.09)
- **Seven**: Witchmail +0.04 (+0.20), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Witchmail +0.04 (+0.21), Counterspell +0.03 (+0.08), Divine Barrier +0.02 (+0.10)
- **Lady Geist**: Return Fire +0.08 (+0.13), Divine Barrier +0.06 (+0.13), Metal Skin +0.05 (+0.14)
- **Abrams**: Unstoppable +0.18 (+0.27), Indomitable +0.12 (+0.24), Dispel Magic +0.10 (+0.16)
- **Wraith**: Indomitable +0.22 (+0.34), Metal Skin +0.19 (+0.27), Plated Armor +0.11 (+0.21)
- **McGinnis**: Spirit Resilience +0.09 (+0.20), Witchmail +0.02 (+0.19), Spellbreaker +0.01 (+0.13)
- **Paradox**: Metal Skin +0.13 (+0.21), Bullet Resilience +0.12 (+0.19), Plated Armor +0.11 (+0.21)
- **Dynamo**: Healbane -0.00 (+0.06), Counterspell -0.02 (+0.03), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.06 (+0.18), Dispel Magic +0.04 (+0.10), Spellbreaker +0.04 (+0.16)
- **Haze**: Indomitable +0.08 (+0.20), Plated Armor +0.07 (+0.17), Unstoppable +0.05 (+0.14)
- **Holliday**: Plated Armor +0.20 (+0.30), Indomitable +0.07 (+0.19), Return Fire +0.05 (+0.11)
- **Bebop**: Healbane +0.04 (+0.11), Metal Skin +0.01 (+0.09), Counterspell -0.01 (+0.04)
- **Calico**: Reactive Barrier +0.05 (+0.09), Divine Barrier +0.04 (+0.11), Spellbreaker +0.04 (+0.16)
- **Grey Talon**: Debuff Reducer +0.04 (+0.08), Reactive Barrier +0.03 (+0.07), Spellbreaker +0.03 (+0.15)
- **Mo & Krill**: Unstoppable +0.11 (+0.20), Spellbreaker +0.03 (+0.15), Dispel Magic +0.02 (+0.08)
- **Shiv**: Bullet Resilience +0.03 (+0.10), Divine Barrier +0.03 (+0.10), Plated Armor +0.01 (+0.11)
- **Ivy**: Unstoppable +0.10 (+0.20), Indomitable +0.08 (+0.20), Dispel Magic +0.02 (+0.07)
- **Warden**: Return Fire +0.04 (+0.09), Metal Skin +0.03 (+0.11), Plated Armor +0.03 (+0.12)
- **Yamato**: Healbane +0.04 (+0.11), Bullet Resilience +0.01 (+0.07), Counterspell +0.00 (+0.05)
- **Lash**: Spellbreaker +0.35 (+0.48), Spirit Resilience +0.33 (+0.44), Divine Barrier +0.19 (+0.26)
- **Viscous**: Divine Barrier -0.01 (+0.06), Counterspell -0.01 (+0.04), Return Fire -0.01 (+0.04)
- **Pocket**: Spirit Resilience +0.23 (+0.34), Spellbreaker +0.14 (+0.27), Witchmail +0.12 (+0.29)
- **Mirage**: Dispel Magic +0.29 (+0.35), Spirit Resilience +0.07 (+0.18), Spellbreaker +0.03 (+0.15)
- **Vyper**: Indomitable +0.38 (+0.50), Debuff Reducer +0.08 (+0.12), Metal Skin +0.08 (+0.16)
- **Sinclair**: Indomitable +0.06 (+0.17), Return Fire +0.00 (+0.05), Spellbreaker -0.02 (+0.11)
- **Mina**: Spirit Resilience +0.15 (+0.26), Spellbreaker +0.12 (+0.24), Witchmail +0.11 (+0.28)
- **Drifter**: Witchmail +0.04 (+0.21), Spirit Resilience +0.00 (+0.11), Counterspell +0.00 (+0.05)
- **Venator**: Bullet Resilience +0.11 (+0.18), Metal Skin +0.11 (+0.19), Plated Armor +0.05 (+0.15)
- **Victor**: Spirit Resilience +0.05 (+0.17), Spellbreaker +0.05 (+0.17), Healbane -0.01 (+0.05)
- **Paige**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.05), Healbane -0.01 (+0.06)
- **The Doorman**: Indomitable +0.09 (+0.21), Spirit Resilience +0.08 (+0.19), Divine Barrier +0.06 (+0.13)
- **Billy**: Spirit Resilience +0.04 (+0.15), Counterspell +0.03 (+0.07), Spellbreaker +0.03 (+0.15)
- **Graves**: Spirit Resilience +0.13 (+0.24), Witchmail +0.12 (+0.29), Metal Skin +0.11 (+0.20)
- **Apollo**: Reactive Barrier +0.01 (+0.04), Healbane -0.02 (+0.05), Unstoppable -0.02 (+0.07)
- **Deadman Danny**: Indomitable +0.16 (+0.28), Witchmail +0.14 (+0.31), Spirit Resilience +0.13 (+0.24)
- **Rem**: Counterspell -0.01 (+0.04), Unstoppable -0.01 (+0.08), Debuff Reducer -0.01 (+0.03)
- **Silver**: Reactive Barrier +0.08 (+0.12), Dispel Magic +0.07 (+0.13), Indomitable +0.03 (+0.15)
- **Celeste**: Witchmail +0.06 (+0.23), Spirit Resilience +0.04 (+0.15), Healbane +0.02 (+0.08)
- **Rat King**: Return Fire -0.01 (+0.05), Bullet Resilience -0.01 (+0.06), Counterspell -0.01 (+0.03)
- **Solomon**: Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.04), Reactive Barrier -0.02 (+0.02)
- **Violet**: Return Fire +0.03 (+0.08), Witchmail +0.02 (+0.19), Divine Barrier +0.00 (+0.07)
- **Nurse Harrow**: Healbane +0.00 (+0.07), Counterspell -0.00 (+0.04), Debuff Reducer -0.02 (+0.02)
- **Baba**: Unstoppable +0.04 (+0.13), Healbane +0.01 (+0.08), Debuff Reducer -0.00 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.153 | +0.048 | +0.120 | Deadman Danny +0.21, Lash +0.16, Drifter +0.15 | 14 heroes |
| Divine Barrier | 6,400 | +0.214 | +0.034 | +0.058 | Lash +0.11, Vindicta +0.11, Paradox +0.09 | 2 heroes |
| Dispel Magic | 3,200 | +0.085 | +0.026 | +0.053 | Mirage +0.29, Silver +0.09, Infernus +0.09 | 9 heroes |
| Indomitable | 6,400 | +0.150 | +0.024 | +0.134 | Vyper +0.40, Wraith +0.26, Deadman Danny +0.18 | 0 heroes |
| Witchmail | 6,400 | +0.143 | +0.022 | +0.170 | Lash +0.15, Deadman Danny +0.14, Paradox +0.12 | 1 heroes |
| Spellbreaker | 6,400 | +0.111 | +0.017 | +0.128 | Lash +0.23, Deadman Danny +0.16, Grey Talon +0.12 | 0 heroes |
| Reactive Barrier | 1,600 | +0.005 | +0.003 | +0.040 | Deadman Danny +0.09, Calico +0.08, Yamato +0.07 | 4 heroes |
| Plated Armor | 6,400 | -0.022 | -0.003 | +0.107 | Deadman Danny +0.17, Wraith +0.12, Haze +0.07 | 0 heroes |
| Counterspell | 3,200 | -0.038 | -0.012 | +0.038 | Calico +0.04, Vindicta +0.04, Deadman Danny +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.081 | -0.013 | +0.097 | Paige +0.21, Abrams +0.14, Grey Talon +0.12 | 3 heroes |
| Debuff Reducer | 1,600 | -0.020 | -0.013 | +0.044 | Grey Talon +0.09, Paige +0.08, Vyper +0.07 | 0 heroes |
| Bullet Resilience | 3,200 | -0.041 | -0.013 | +0.059 | Vindicta +0.10, Venator +0.09, Paradox +0.08 | 1 heroes |
| Healbane | 1,600 | -0.039 | -0.024 | +0.064 | Drifter +0.07, Yamato +0.04, Nurse Harrow +0.04 | 16 heroes |
| Metal Skin | 3,200 | -0.161 | -0.050 | +0.097 | Wraith +0.23, Paradox +0.12, Lash +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.177 | -0.111 | +0.052 | Wraith +0.07, Vindicta +0.05, Paradox +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.11 (+0.21), Dispel Magic +0.09 (+0.14), Spellbreaker +0.08 (+0.21)
- **Seven**: Witchmail +0.02 (+0.19), Counterspell -0.00 (+0.04), Healbane -0.01 (+0.05)
- **Vindicta**: Divine Barrier +0.11 (+0.17), Bullet Resilience +0.10 (+0.16), Plated Armor +0.07 (+0.18)
- **Lady Geist**: Bullet Resilience +0.04 (+0.10), Metal Skin +0.04 (+0.14), Return Fire +0.02 (+0.07)
- **Abrams**: Unstoppable +0.14 (+0.23), Dispel Magic +0.06 (+0.11), Spirit Resilience +0.03 (+0.15)
- **Wraith**: Indomitable +0.26 (+0.40), Metal Skin +0.23 (+0.33), Plated Armor +0.12 (+0.23)
- **McGinnis**: Spirit Resilience +0.13 (+0.25), Witchmail +0.05 (+0.22), Spellbreaker +0.05 (+0.18)
- **Paradox**: Witchmail +0.12 (+0.29), Metal Skin +0.12 (+0.21), Divine Barrier +0.09 (+0.15)
- **Dynamo**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.02), Debuff Reducer -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.01 (+0.13), Healbane +0.00 (+0.07), Counterspell -0.00 (+0.03)
- **Haze**: Plated Armor +0.07 (+0.18), Indomitable +0.06 (+0.20), Bullet Resilience +0.06 (+0.12)
- **Holliday**: Spellbreaker +0.10 (+0.23), Indomitable +0.09 (+0.22), Debuff Reducer +0.07 (+0.12)
- **Bebop**: Healbane +0.03 (+0.09), Counterspell -0.02 (+0.02), Return Fire -0.03 (+0.03)
- **Calico**: Spirit Resilience +0.09 (+0.21), Reactive Barrier +0.08 (+0.12), Divine Barrier +0.07 (+0.12)
- **Grey Talon**: Spellbreaker +0.12 (+0.24), Unstoppable +0.12 (+0.21), Indomitable +0.10 (+0.24)
- **Mo & Krill**: Unstoppable +0.07 (+0.16), Spirit Resilience +0.05 (+0.17), Spellbreaker +0.05 (+0.18)
- **Shiv**: Metal Skin +0.04 (+0.13), Bullet Resilience +0.04 (+0.10), Divine Barrier +0.02 (+0.08)
- **Ivy**: Unstoppable +0.11 (+0.20), Indomitable +0.07 (+0.21), Debuff Reducer +0.02 (+0.06)
- **Warden**: Return Fire +0.02 (+0.07), Bullet Resilience +0.00 (+0.06), Divine Barrier -0.01 (+0.05)
- **Yamato**: Reactive Barrier +0.07 (+0.11), Indomitable +0.05 (+0.19), Plated Armor +0.05 (+0.16)
- **Lash**: Spellbreaker +0.23 (+0.36), Spirit Resilience +0.16 (+0.28), Witchmail +0.15 (+0.32)
- **Viscous**: Return Fire +0.03 (+0.08), Divine Barrier +0.02 (+0.08), Bullet Resilience -0.00 (+0.06)
- **Pocket**: Spirit Resilience +0.08 (+0.20), Witchmail +0.02 (+0.19), Spellbreaker +0.02 (+0.14)
- **Mirage**: Dispel Magic +0.29 (+0.34), Spirit Resilience +0.03 (+0.15), Metal Skin +0.02 (+0.12)
- **Vyper**: Indomitable +0.40 (+0.54), Debuff Reducer +0.07 (+0.12), Spellbreaker +0.07 (+0.19)
- **Sinclair**: Indomitable +0.13 (+0.26), Return Fire +0.00 (+0.06), Unstoppable -0.00 (+0.09)
- **Mina**: Spirit Resilience +0.12 (+0.24), Witchmail +0.08 (+0.25), Spellbreaker +0.06 (+0.19)
- **Drifter**: Spirit Resilience +0.15 (+0.27), Witchmail +0.10 (+0.27), Healbane +0.07 (+0.13)
- **Venator**: Metal Skin +0.11 (+0.21), Bullet Resilience +0.09 (+0.15), Plated Armor +0.05 (+0.15)
- **Victor**: Spirit Resilience +0.03 (+0.15), Healbane +0.03 (+0.09), Spellbreaker +0.02 (+0.15)
- **Paige**: Unstoppable +0.21 (+0.31), Debuff Reducer +0.08 (+0.12), Spellbreaker +0.00 (+0.13)
- **The Doorman**: Spirit Resilience +0.15 (+0.27), Indomitable +0.11 (+0.25), Witchmail +0.09 (+0.26)
- **Billy**: Reactive Barrier +0.04 (+0.08), Spirit Resilience +0.01 (+0.12), Indomitable -0.00 (+0.13)
- **Graves**: Metal Skin +0.04 (+0.14), Witchmail +0.04 (+0.21), Reactive Barrier +0.03 (+0.07)
- **Apollo**: Counterspell -0.02 (+0.02), Healbane -0.03 (+0.04), Return Fire -0.03 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.21 (+0.33), Indomitable +0.18 (+0.31), Plated Armor +0.17 (+0.27)
- **Rem**: Debuff Reducer +0.06 (+0.10), Unstoppable +0.04 (+0.14), Counterspell -0.00 (+0.04)
- **Silver**: Dispel Magic +0.09 (+0.14), Reactive Barrier +0.04 (+0.08), Debuff Reducer +0.01 (+0.05)
- **Celeste**: Dispel Magic +0.04 (+0.09), Witchmail +0.03 (+0.20), Healbane -0.00 (+0.06)
- **Rat King**: Bullet Resilience -0.00 (+0.05), Return Fire -0.01 (+0.05), Plated Armor -0.01 (+0.10)
- **Solomon**: Healbane +0.03 (+0.09), Reactive Barrier +0.02 (+0.07), Counterspell +0.02 (+0.06)
- **Violet**: Witchmail +0.06 (+0.23), Return Fire +0.04 (+0.09), Divine Barrier +0.02 (+0.08)
- **Nurse Harrow**: Healbane +0.04 (+0.10), Counterspell -0.03 (+0.01), Return Fire -0.03 (+0.02)
- **Baba**: Unstoppable +0.01 (+0.11), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.178 | +0.056 | +0.139 | Lash +0.59, Deadman Danny +0.46, The Doorman +0.35 | 15 heroes |
| Divine Barrier | 6,400 | +0.181 | +0.028 | +0.053 | Lash +0.30, The Doorman +0.17, Calico +0.13 | 3 heroes |
| Indomitable | 6,400 | +0.162 | +0.026 | +0.148 | Deadman Danny +0.30, Vyper +0.27, The Doorman +0.24 | 1 heroes |
| Dispel Magic | 3,200 | +0.081 | +0.025 | +0.050 | Mirage +0.29, Lash +0.23, Silver +0.22 | 9 heroes |
| Witchmail | 6,400 | +0.135 | +0.021 | +0.160 | Deadman Danny +0.35, Lash +0.32, The Doorman +0.25 | 2 heroes |
| Spellbreaker | 6,400 | +0.124 | +0.019 | +0.139 | Lash +0.48, Deadman Danny +0.36, The Doorman +0.19 | 0 heroes |
| Plated Armor | 6,400 | -0.032 | -0.005 | +0.097 | Holliday +0.29, Lash +0.15, Vyper +0.12 | 2 heroes |
| Unstoppable | 6,400 | -0.072 | -0.011 | +0.120 | Paige +0.31, Haze +0.23, Infernus +0.21 | 8 heroes |
| Counterspell | 3,200 | -0.041 | -0.013 | +0.030 | Lash +0.12, The Doorman +0.06, Yamato +0.04 | 1 heroes |
| Bullet Resilience | 3,200 | -0.045 | -0.014 | +0.058 | Lash +0.16, Venator +0.10, Haze +0.07 | 0 heroes |
| Reactive Barrier | 1,600 | -0.032 | -0.020 | +0.031 | Yamato +0.13, The Doorman +0.13, Deadman Danny +0.11 | 3 heroes |
| Debuff Reducer | 1,600 | -0.037 | -0.023 | +0.043 | Bebop +0.12, Grey Talon +0.09, Holliday +0.09 | 0 heroes |
| Healbane | 1,600 | -0.044 | -0.028 | +0.056 | Nurse Harrow +0.09, Mo & Krill +0.06, Victor +0.05 | 14 heroes |
| Metal Skin | 3,200 | -0.160 | -0.050 | +0.102 | Lash +0.29, Grey Talon +0.18, Venator +0.14 | 0 heroes |
| Return Fire | 1,600 | -0.174 | -0.109 | +0.042 | Violet +0.11, Paradox +0.07, Haze +0.04 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.21 (+0.33), Dispel Magic +0.06 (+0.11), Indomitable +0.04 (+0.19)
- **Seven**: Witchmail +0.03 (+0.19), Healbane -0.00 (+0.05), Dispel Magic -0.01 (+0.04)
- **Vindicta**: Bullet Resilience +0.06 (+0.12), Divine Barrier +0.06 (+0.11), Plated Armor +0.05 (+0.15)
- **Lady Geist**: Metal Skin +0.06 (+0.17), Bullet Resilience +0.06 (+0.12), Return Fire +0.02 (+0.07)
- **Abrams**: Unstoppable +0.07 (+0.19), Dispel Magic +0.04 (+0.09), Indomitable +0.04 (+0.19)
- **Wraith**: Indomitable +0.20 (+0.35), Metal Skin +0.09 (+0.19), Plated Armor +0.05 (+0.15)
- **McGinnis**: Spirit Resilience +0.12 (+0.26), Healbane +0.00 (+0.06), Spellbreaker -0.00 (+0.13)
- **Paradox**: Witchmail +0.11 (+0.27), Unstoppable +0.09 (+0.21), Return Fire +0.07 (+0.11)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.07 (+0.21), Spellbreaker +0.02 (+0.16), Healbane +0.01 (+0.06)
- **Haze**: Unstoppable +0.23 (+0.35), Bullet Resilience +0.07 (+0.12), Indomitable +0.06 (+0.21)
- **Holliday**: Plated Armor +0.29 (+0.39), Debuff Reducer +0.09 (+0.13), Indomitable +0.09 (+0.23)
- **Bebop**: Debuff Reducer +0.12 (+0.17), Spellbreaker +0.08 (+0.22), Reactive Barrier +0.05 (+0.08)
- **Calico**: Divine Barrier +0.13 (+0.18), Spirit Resilience +0.12 (+0.26), Spellbreaker +0.09 (+0.23)
- **Grey Talon**: Metal Skin +0.18 (+0.28), Unstoppable +0.15 (+0.27), Spellbreaker +0.12 (+0.25)
- **Mo & Krill**: Healbane +0.06 (+0.12), Dispel Magic +0.05 (+0.10), Unstoppable +0.02 (+0.14)
- **Shiv**: Bullet Resilience +0.04 (+0.10), Metal Skin +0.03 (+0.13), Divine Barrier +0.03 (+0.08)
- **Ivy**: Unstoppable +0.19 (+0.31), Indomitable +0.13 (+0.28), Debuff Reducer +0.06 (+0.10)
- **Warden**: Plated Armor +0.05 (+0.14), Metal Skin +0.02 (+0.13), Return Fire +0.02 (+0.06)
- **Yamato**: Reactive Barrier +0.13 (+0.17), Indomitable +0.13 (+0.27), Plated Armor +0.08 (+0.18)
- **Lash**: Spirit Resilience +0.59 (+0.73), Spellbreaker +0.48 (+0.62), Witchmail +0.32 (+0.48)
- **Viscous**: Divine Barrier +0.05 (+0.10), Return Fire +0.03 (+0.07), Witchmail +0.01 (+0.17)
- **Pocket**: Spirit Resilience +0.08 (+0.22), Spellbreaker -0.00 (+0.14), Return Fire -0.01 (+0.03)
- **Mirage**: Dispel Magic +0.29 (+0.34), Metal Skin +0.08 (+0.18), Plated Armor +0.01 (+0.11)
- **Vyper**: Indomitable +0.27 (+0.42), Plated Armor +0.12 (+0.22), Metal Skin +0.06 (+0.16)
- **Sinclair**: Indomitable +0.15 (+0.30), Reactive Barrier +0.05 (+0.08), Spellbreaker +0.05 (+0.19)
- **Mina**: Divine Barrier +0.00 (+0.05), Dispel Magic -0.01 (+0.04), Return Fire -0.02 (+0.03)
- **Drifter**: Spirit Resilience +0.16 (+0.29), Witchmail +0.10 (+0.26), Counterspell +0.02 (+0.05)
- **Venator**: Metal Skin +0.14 (+0.24), Bullet Resilience +0.10 (+0.16), Plated Armor +0.06 (+0.15)
- **Victor**: Spellbreaker +0.08 (+0.22), Spirit Resilience +0.07 (+0.21), Healbane +0.05 (+0.11)
- **Paige**: Unstoppable +0.31 (+0.43), Debuff Reducer +0.08 (+0.12), Counterspell +0.00 (+0.03)
- **The Doorman**: Spirit Resilience +0.35 (+0.49), Witchmail +0.25 (+0.41), Indomitable +0.24 (+0.39)
- **Billy**: Reactive Barrier +0.07 (+0.10), Healbane +0.04 (+0.10), Counterspell +0.03 (+0.06)
- **Graves**: Return Fire +0.02 (+0.07), Healbane +0.01 (+0.07), Witchmail +0.01 (+0.17)
- **Apollo**: Reactive Barrier +0.00 (+0.03), Healbane -0.01 (+0.05), Counterspell -0.03 (+0.00)
- **Deadman Danny**: Spirit Resilience +0.46 (+0.60), Spellbreaker +0.36 (+0.50), Witchmail +0.35 (+0.51)
- **Rem**: Debuff Reducer +0.07 (+0.11), Unstoppable -0.01 (+0.11), Counterspell -0.01 (+0.02)
- **Silver**: Dispel Magic +0.22 (+0.27), Indomitable +0.17 (+0.32), Metal Skin +0.13 (+0.24)
- **Celeste**: Witchmail +0.13 (+0.29), Spirit Resilience +0.12 (+0.26), Healbane +0.04 (+0.09)
- **Rat King**: Return Fire -0.00 (+0.04), Counterspell -0.01 (+0.02), Healbane -0.01 (+0.04)
- **Solomon**: Reactive Barrier +0.00 (+0.03), Return Fire -0.02 (+0.03), Counterspell -0.02 (+0.01)
- **Violet**: Return Fire +0.11 (+0.15), Witchmail +0.02 (+0.18), Divine Barrier +0.00 (+0.06)
- **Nurse Harrow**: Spirit Resilience +0.11 (+0.25), Witchmail +0.10 (+0.26), Dispel Magic +0.10 (+0.15)
- **Baba**: Healbane +0.03 (+0.08), Counterspell +0.01 (+0.05), Unstoppable +0.00 (+0.12)
