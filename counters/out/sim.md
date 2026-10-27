# Counter items in the sim (phantom and up)

Built 2026-10-27T22:23:59Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.183 | +0.057 | +0.115 | Lash +0.27, Deadman Danny +0.21, Graves +0.10 | 1 heroes |
| Divine Barrier | 6,400 | +0.335 | +0.054 | +0.091 | Lash +0.20, Calico +0.12, Wraith +0.12 | 0 heroes |
| Dispel Magic | 3,200 | +0.095 | +0.030 | +0.072 | Mirage +0.39, Deadman Danny +0.14, Infernus +0.12 | 4 heroes |
| Reactive Barrier | 1,600 | +0.042 | +0.027 | +0.058 | Deadman Danny +0.17, Calico +0.14, Paradox +0.10 | 3 heroes |
| Indomitable | 6,400 | +0.167 | +0.027 | +0.138 | Vyper +0.26, Deadman Danny +0.26, Abrams +0.20 | 0 heroes |
| Witchmail | 6,400 | +0.146 | +0.023 | +0.196 | Deadman Danny +0.24, Lash +0.22, Wraith +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.022 | +0.014 | +0.055 | Deadman Danny +0.09, Wraith +0.08, Holliday +0.07 | 0 heroes |
| Spellbreaker | 6,400 | +0.079 | +0.012 | +0.139 | Deadman Danny +0.27, Lash +0.25, Calico +0.12 | 0 heroes |
| Bullet Resilience | 3,200 | -0.004 | -0.001 | +0.081 | Deadman Danny +0.16, Venator +0.15, Paradox +0.13 | 0 heroes |
| Healbane | 1,600 | -0.010 | -0.006 | +0.086 | Deadman Danny +0.07, Lash +0.05, Billy +0.05 | 11 heroes |
| Plated Armor | 6,400 | -0.043 | -0.007 | +0.116 | Holliday +0.22, Deadman Danny +0.21, Wraith +0.13 | 0 heroes |
| Counterspell | 3,200 | -0.027 | -0.008 | +0.069 | Deadman Danny +0.13, Wraith +0.05, Lash +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.056 | -0.009 | +0.113 | Deadman Danny +0.19, Abrams +0.11, Haze +0.09 | 0 heroes |
| Metal Skin | 3,200 | -0.154 | -0.048 | +0.094 | Lash +0.17, Wraith +0.16, Paradox +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.177 | -0.111 | +0.074 | Deadman Danny +0.11, Paradox +0.06, Lady Geist +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.12 (+0.19), Spirit Resilience +0.06 (+0.18), Unstoppable +0.05 (+0.17)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.02 (+0.04), Reactive Barrier -0.03 (+0.03)
- **Vindicta**: Return Fire +0.01 (+0.09), Witchmail -0.00 (+0.19), Counterspell -0.00 (+0.07)
- **Lady Geist**: Return Fire +0.06 (+0.13), Healbane +0.04 (+0.12), Counterspell +0.01 (+0.08)
- **Abrams**: Indomitable +0.20 (+0.33), Unstoppable +0.11 (+0.22), Spirit Resilience +0.08 (+0.20)
- **Wraith**: Indomitable +0.19 (+0.33), Metal Skin +0.16 (+0.26), Plated Armor +0.13 (+0.25)
- **McGinnis**: Healbane -0.01 (+0.08), Return Fire -0.01 (+0.06), Spirit Resilience -0.01 (+0.10)
- **Paradox**: Metal Skin +0.15 (+0.25), Bullet Resilience +0.13 (+0.21), Plated Armor +0.12 (+0.24)
- **Dynamo**: Healbane -0.01 (+0.08), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane -0.00 (+0.08), Counterspell -0.01 (+0.05), Debuff Reducer -0.02 (+0.04)
- **Haze**: Indomitable +0.10 (+0.24), Unstoppable +0.09 (+0.20), Plated Armor +0.04 (+0.16)
- **Holliday**: Plated Armor +0.22 (+0.33), Spellbreaker +0.08 (+0.22), Debuff Reducer +0.07 (+0.13)
- **Bebop**: Healbane +0.03 (+0.12), Counterspell +0.01 (+0.08), Return Fire +0.00 (+0.08)
- **Calico**: Reactive Barrier +0.14 (+0.19), Divine Barrier +0.12 (+0.21), Spellbreaker +0.12 (+0.26)
- **Grey Talon**: Debuff Reducer +0.04 (+0.10), Reactive Barrier +0.04 (+0.10), Spellbreaker +0.03 (+0.17)
- **Mo & Krill**: Spellbreaker +0.09 (+0.23), Spirit Resilience +0.06 (+0.17), Dispel Magic +0.05 (+0.12)
- **Shiv**: Divine Barrier -0.00 (+0.09), Healbane -0.01 (+0.08), Spirit Resilience -0.02 (+0.10)
- **Ivy**: Indomitable +0.08 (+0.22), Unstoppable +0.07 (+0.18), Bullet Resilience +0.01 (+0.09)
- **Warden**: Return Fire +0.02 (+0.09), Counterspell -0.01 (+0.06), Debuff Reducer -0.01 (+0.05)
- **Yamato**: Healbane +0.03 (+0.12), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.04)
- **Lash**: Spirit Resilience +0.27 (+0.39), Spellbreaker +0.25 (+0.39), Witchmail +0.22 (+0.42)
- **Viscous**: Return Fire -0.02 (+0.05), Healbane -0.03 (+0.06), Counterspell -0.04 (+0.03)
- **Pocket**: Witchmail +0.05 (+0.25), Spirit Resilience +0.04 (+0.16), Spellbreaker +0.03 (+0.17)
- **Mirage**: Dispel Magic +0.39 (+0.46), Spirit Resilience +0.10 (+0.21), Spellbreaker +0.08 (+0.22)
- **Vyper**: Indomitable +0.26 (+0.40), Debuff Reducer +0.05 (+0.10), Spellbreaker +0.02 (+0.16)
- **Sinclair**: Indomitable +0.13 (+0.27), Return Fire -0.01 (+0.06), Spellbreaker -0.01 (+0.13)
- **Mina**: Return Fire +0.02 (+0.09), Spirit Resilience -0.00 (+0.11), Witchmail -0.00 (+0.19)
- **Drifter**: Counterspell -0.01 (+0.06), Healbane -0.01 (+0.08), Return Fire -0.01 (+0.06)
- **Venator**: Bullet Resilience +0.15 (+0.23), Divine Barrier +0.09 (+0.18), Metal Skin +0.07 (+0.17)
- **Victor**: Healbane +0.02 (+0.10), Spirit Resilience +0.01 (+0.12), Dispel Magic -0.01 (+0.06)
- **Paige**: Return Fire +0.00 (+0.08), Counterspell -0.01 (+0.06), Healbane -0.03 (+0.06)
- **The Doorman**: Indomitable +0.12 (+0.25), Witchmail +0.09 (+0.29), Spirit Resilience +0.09 (+0.21)
- **Billy**: Spellbreaker +0.05 (+0.19), Healbane +0.05 (+0.13), Spirit Resilience +0.04 (+0.16)
- **Graves**: Metal Skin +0.13 (+0.22), Spirit Resilience +0.10 (+0.22), Witchmail +0.08 (+0.28)
- **Apollo**: Unstoppable +0.00 (+0.11), Healbane -0.01 (+0.08), Reactive Barrier -0.01 (+0.05)
- **Deadman Danny**: Spellbreaker +0.27 (+0.41), Indomitable +0.26 (+0.39), Witchmail +0.24 (+0.43)
- **Rem**: Debuff Reducer +0.05 (+0.11), Unstoppable +0.04 (+0.15), Spellbreaker -0.02 (+0.12)
- **Silver**: Dispel Magic +0.04 (+0.11), Debuff Reducer +0.03 (+0.09), Metal Skin +0.02 (+0.11)
- **Celeste**: Spirit Resilience +0.06 (+0.18), Witchmail +0.06 (+0.25), Dispel Magic +0.03 (+0.11)
- **Rat King**: Counterspell -0.00 (+0.06), Bullet Resilience -0.01 (+0.07), Return Fire -0.01 (+0.06)
- **Solomon**: Return Fire -0.00 (+0.07), Counterspell -0.02 (+0.04), Debuff Reducer -0.03 (+0.02)
- **Violet**: Return Fire -0.00 (+0.07), Healbane -0.01 (+0.07), Reactive Barrier -0.02 (+0.03)
- **Nurse Harrow**: Healbane +0.01 (+0.10), Return Fire -0.05 (+0.03), Dispel Magic -0.05 (+0.02)
- **Baba**: Healbane -0.00 (+0.08), Debuff Reducer -0.03 (+0.03), Unstoppable -0.03 (+0.09)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.159 | +0.050 | +0.105 | Lash +0.34, Pocket +0.26, Graves +0.15 | 9 heroes |
| Divine Barrier | 6,400 | +0.268 | +0.043 | +0.064 | Lash +0.19, Paradox +0.10, Wraith +0.07 | 1 heroes |
| Dispel Magic | 3,200 | +0.085 | +0.026 | +0.051 | Mirage +0.32, Infernus +0.10, Deadman Danny +0.09 | 6 heroes |
| Witchmail | 6,400 | +0.145 | +0.023 | +0.160 | Lash +0.16, Pocket +0.16, Deadman Danny +0.14 | 0 heroes |
| Indomitable | 6,400 | +0.134 | +0.022 | +0.106 | Vyper +0.38, Wraith +0.20, Deadman Danny +0.17 | 0 heroes |
| Spellbreaker | 6,400 | +0.096 | +0.015 | +0.110 | Lash +0.36, Pocket +0.14, Deadman Danny +0.12 | 0 heroes |
| Reactive Barrier | 1,600 | +0.017 | +0.011 | +0.032 | Paradox +0.10, Vyper +0.07, The Doorman +0.07 | 4 heroes |
| Plated Armor | 6,400 | -0.033 | -0.005 | +0.084 | Holliday +0.17, Paradox +0.10, Deadman Danny +0.09 | 0 heroes |
| Debuff Reducer | 1,600 | -0.013 | -0.008 | +0.035 | Wraith +0.07, Vyper +0.07, Grey Talon +0.04 | 1 heroes |
| Bullet Resilience | 3,200 | -0.031 | -0.010 | +0.056 | Venator +0.12, Paradox +0.11, Deadman Danny +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.034 | -0.011 | +0.045 | Deadman Danny +0.07, Vindicta +0.04, Vyper +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.077 | -0.012 | +0.086 | Abrams +0.19, Deadman Danny +0.12, Ivy +0.08 | 0 heroes |
| Healbane | 1,600 | -0.039 | -0.024 | +0.064 | Bebop +0.06, Abrams +0.05, Yamato +0.04 | 17 heroes |
| Metal Skin | 3,200 | -0.171 | -0.053 | +0.071 | Graves +0.15, Wraith +0.12, Venator +0.12 | 0 heroes |
| Return Fire | 1,600 | -0.184 | -0.115 | +0.051 | Lady Geist +0.08, Paradox +0.06, Wraith +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.10 (+0.16), Unstoppable +0.04 (+0.13), Spellbreaker +0.03 (+0.14)
- **Seven**: Witchmail +0.03 (+0.19), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Witchmail +0.06 (+0.22), Counterspell +0.04 (+0.08), Divine Barrier +0.03 (+0.10)
- **Lady Geist**: Return Fire +0.08 (+0.13), Divine Barrier +0.07 (+0.13), Bullet Resilience +0.07 (+0.12)
- **Abrams**: Unstoppable +0.19 (+0.28), Indomitable +0.11 (+0.21), Dispel Magic +0.07 (+0.12)
- **Wraith**: Indomitable +0.20 (+0.30), Metal Skin +0.12 (+0.19), Plated Armor +0.09 (+0.17)
- **McGinnis**: Spirit Resilience +0.04 (+0.15), Witchmail +0.03 (+0.19), Healbane +0.01 (+0.07)
- **Paradox**: Bullet Resilience +0.11 (+0.16), Plated Armor +0.10 (+0.19), Metal Skin +0.10 (+0.17)
- **Dynamo**: Healbane -0.01 (+0.06), Counterspell -0.01 (+0.03), Debuff Reducer -0.02 (+0.01)
- **Kelvin**: Spirit Resilience +0.07 (+0.17), Dispel Magic +0.06 (+0.11), Spellbreaker +0.05 (+0.16)
- **Haze**: Indomitable +0.08 (+0.18), Plated Armor +0.06 (+0.15), Unstoppable +0.05 (+0.14)
- **Holliday**: Plated Armor +0.17 (+0.25), Indomitable +0.06 (+0.16), Return Fire +0.05 (+0.10)
- **Bebop**: Healbane +0.06 (+0.12), Metal Skin +0.01 (+0.08), Counterspell -0.00 (+0.04)
- **Calico**: Reactive Barrier +0.05 (+0.08), Divine Barrier +0.05 (+0.11), Spellbreaker +0.02 (+0.13)
- **Grey Talon**: Spellbreaker +0.05 (+0.16), Debuff Reducer +0.04 (+0.08), Reactive Barrier +0.04 (+0.07)
- **Mo & Krill**: Unstoppable +0.08 (+0.17), Dispel Magic +0.02 (+0.07), Spellbreaker +0.02 (+0.13)
- **Shiv**: Bullet Resilience +0.03 (+0.08), Divine Barrier +0.02 (+0.08), Metal Skin +0.02 (+0.09)
- **Ivy**: Unstoppable +0.08 (+0.17), Indomitable +0.07 (+0.17), Debuff Reducer +0.01 (+0.04)
- **Warden**: Return Fire +0.03 (+0.08), Plated Armor +0.01 (+0.10), Bullet Resilience +0.01 (+0.07)
- **Yamato**: Healbane +0.04 (+0.10), Bullet Resilience +0.01 (+0.07), Witchmail +0.00 (+0.16)
- **Lash**: Spellbreaker +0.36 (+0.47), Spirit Resilience +0.34 (+0.44), Divine Barrier +0.19 (+0.26)
- **Viscous**: Return Fire +0.00 (+0.05), Healbane -0.00 (+0.06), Divine Barrier -0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.26 (+0.36), Witchmail +0.16 (+0.32), Spellbreaker +0.14 (+0.25)
- **Mirage**: Dispel Magic +0.32 (+0.37), Spirit Resilience +0.08 (+0.19), Spellbreaker +0.05 (+0.16)
- **Vyper**: Indomitable +0.38 (+0.48), Spellbreaker +0.08 (+0.19), Reactive Barrier +0.07 (+0.11)
- **Sinclair**: Indomitable +0.07 (+0.18), Return Fire +0.01 (+0.06), Reactive Barrier -0.01 (+0.02)
- **Mina**: Divine Barrier +0.03 (+0.09), Witchmail +0.03 (+0.19), Counterspell +0.03 (+0.07)
- **Drifter**: Witchmail +0.02 (+0.18), Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.04)
- **Venator**: Bullet Resilience +0.12 (+0.18), Metal Skin +0.12 (+0.19), Plated Armor +0.06 (+0.14)
- **Victor**: Spellbreaker +0.06 (+0.17), Spirit Resilience +0.06 (+0.16), Healbane -0.02 (+0.04)
- **Paige**: Return Fire -0.00 (+0.05), Counterspell -0.00 (+0.04), Healbane -0.01 (+0.05)
- **The Doorman**: Indomitable +0.09 (+0.19), Reactive Barrier +0.07 (+0.10), Spirit Resilience +0.07 (+0.17)
- **Billy**: Spirit Resilience +0.03 (+0.14), Spellbreaker +0.03 (+0.14), Healbane +0.03 (+0.09)
- **Graves**: Metal Skin +0.15 (+0.22), Spirit Resilience +0.15 (+0.25), Witchmail +0.08 (+0.24)
- **Apollo**: Reactive Barrier +0.00 (+0.03), Debuff Reducer -0.01 (+0.03), Healbane -0.01 (+0.06)
- **Deadman Danny**: Indomitable +0.17 (+0.27), Witchmail +0.14 (+0.30), Spirit Resilience +0.14 (+0.24)
- **Rem**: Counterspell -0.01 (+0.04), Unstoppable -0.01 (+0.08), Debuff Reducer -0.01 (+0.03)
- **Silver**: Dispel Magic +0.08 (+0.13), Reactive Barrier +0.06 (+0.09), Indomitable +0.04 (+0.14)
- **Celeste**: Spirit Resilience +0.06 (+0.16), Witchmail +0.05 (+0.21), Spellbreaker +0.01 (+0.12)
- **Rat King**: Return Fire -0.00 (+0.05), Bullet Resilience -0.01 (+0.05), Metal Skin -0.01 (+0.06)
- **Solomon**: Return Fire +0.01 (+0.06), Reactive Barrier -0.01 (+0.02), Counterspell -0.02 (+0.03)
- **Violet**: Healbane +0.01 (+0.08), Return Fire +0.01 (+0.06), Counterspell -0.01 (+0.03)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Debuff Reducer -0.02 (+0.02), Counterspell -0.03 (+0.02)
- **Baba**: Unstoppable +0.04 (+0.13), Healbane +0.01 (+0.08), Debuff Reducer +0.01 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.147 | +0.046 | +0.107 | Deadman Danny +0.19, The Doorman +0.17, Lash +0.17 | 14 heroes |
| Divine Barrier | 6,400 | +0.201 | +0.032 | +0.051 | The Doorman +0.09, Lash +0.09, Vindicta +0.07 | 2 heroes |
| Dispel Magic | 3,200 | +0.082 | +0.026 | +0.049 | Mirage +0.28, Infernus +0.15, Paradox +0.06 | 9 heroes |
| Indomitable | 6,400 | +0.142 | +0.023 | +0.117 | Vyper +0.36, Wraith +0.24, Sinclair +0.21 | 0 heroes |
| Witchmail | 6,400 | +0.140 | +0.022 | +0.163 | Lash +0.15, The Doorman +0.12, Deadman Danny +0.12 | 1 heroes |
| Spellbreaker | 6,400 | +0.104 | +0.016 | +0.113 | Lash +0.21, Grey Talon +0.16, Infernus +0.14 | 0 heroes |
| Reactive Barrier | 1,600 | +0.004 | +0.002 | +0.037 | Yamato +0.11, Wraith +0.08, Grey Talon +0.07 | 4 heroes |
| Plated Armor | 6,400 | -0.030 | -0.005 | +0.088 | Wraith +0.11, Yamato +0.10, Deadman Danny +0.08 | 0 heroes |
| Counterspell | 3,200 | -0.038 | -0.012 | +0.036 | Deadman Danny +0.05, Vindicta +0.03, Kelvin +0.02 | 1 heroes |
| Debuff Reducer | 1,600 | -0.021 | -0.013 | +0.043 | Grey Talon +0.11, Wraith +0.08, Paige +0.08 | 0 heroes |
| Unstoppable | 6,400 | -0.083 | -0.013 | +0.090 | Paige +0.22, Grey Talon +0.14, Abrams +0.14 | 3 heroes |
| Bullet Resilience | 3,200 | -0.044 | -0.014 | +0.052 | Venator +0.09, Wraith +0.07, Vindicta +0.07 | 1 heroes |
| Healbane | 1,600 | -0.040 | -0.025 | +0.062 | Abrams +0.05, Infernus +0.04, Victor +0.04 | 16 heroes |
| Metal Skin | 3,200 | -0.168 | -0.052 | +0.078 | Wraith +0.17, Venator +0.13, Lash +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.181 | -0.113 | +0.044 | Vindicta +0.07, Graves +0.05, Lady Geist +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.15 (+0.20), Spellbreaker +0.14 (+0.25), Unstoppable +0.08 (+0.17)
- **Seven**: Witchmail +0.00 (+0.17), Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05)
- **Vindicta**: Divine Barrier +0.07 (+0.12), Return Fire +0.07 (+0.11), Bullet Resilience +0.07 (+0.12)
- **Lady Geist**: Return Fire +0.05 (+0.09), Metal Skin +0.05 (+0.13), Bullet Resilience +0.05 (+0.10)
- **Abrams**: Unstoppable +0.14 (+0.23), Dispel Magic +0.05 (+0.10), Healbane +0.05 (+0.11)
- **Wraith**: Indomitable +0.24 (+0.36), Metal Skin +0.17 (+0.25), Spirit Resilience +0.11 (+0.22)
- **McGinnis**: Spirit Resilience +0.14 (+0.24), Witchmail +0.08 (+0.25), Spellbreaker +0.05 (+0.16)
- **Paradox**: Witchmail +0.10 (+0.27), Indomitable +0.08 (+0.20), Spellbreaker +0.08 (+0.19)
- **Dynamo**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.03), Return Fire -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.05 (+0.16), Counterspell +0.02 (+0.06), Debuff Reducer +0.01 (+0.05)
- **Haze**: Plated Armor +0.05 (+0.14), Bullet Resilience +0.04 (+0.10), Witchmail +0.04 (+0.20)
- **Holliday**: Indomitable +0.07 (+0.19), Spellbreaker +0.05 (+0.16), Debuff Reducer +0.04 (+0.08)
- **Bebop**: Healbane +0.03 (+0.10), Counterspell -0.01 (+0.02), Return Fire -0.02 (+0.03)
- **Calico**: Spirit Resilience +0.05 (+0.16), Divine Barrier +0.03 (+0.08), Reactive Barrier +0.03 (+0.07)
- **Grey Talon**: Spellbreaker +0.16 (+0.27), Unstoppable +0.14 (+0.23), Indomitable +0.11 (+0.23)
- **Mo & Krill**: Spellbreaker +0.06 (+0.17), Spirit Resilience +0.04 (+0.15), Unstoppable +0.04 (+0.12)
- **Shiv**: Metal Skin +0.05 (+0.12), Bullet Resilience +0.04 (+0.09), Plated Armor +0.03 (+0.12)
- **Ivy**: Unstoppable +0.07 (+0.16), Indomitable +0.03 (+0.14), Healbane +0.01 (+0.07)
- **Warden**: Return Fire +0.02 (+0.07), Divine Barrier +0.01 (+0.06), Counterspell +0.01 (+0.04)
- **Yamato**: Indomitable +0.13 (+0.24), Reactive Barrier +0.11 (+0.15), Plated Armor +0.10 (+0.19)
- **Lash**: Spellbreaker +0.21 (+0.32), Spirit Resilience +0.17 (+0.28), Witchmail +0.15 (+0.31)
- **Viscous**: Divine Barrier +0.03 (+0.08), Return Fire +0.02 (+0.07), Counterspell +0.01 (+0.04)
- **Pocket**: Spirit Resilience +0.09 (+0.20), Spellbreaker +0.03 (+0.15), Witchmail +0.01 (+0.18)
- **Mirage**: Dispel Magic +0.28 (+0.32), Plated Armor +0.03 (+0.12), Spirit Resilience +0.03 (+0.13)
- **Vyper**: Indomitable +0.36 (+0.48), Debuff Reducer +0.06 (+0.11), Spellbreaker +0.05 (+0.17)
- **Sinclair**: Indomitable +0.21 (+0.32), Return Fire +0.01 (+0.05), Unstoppable -0.01 (+0.08)
- **Mina**: Divine Barrier +0.03 (+0.08), Witchmail +0.03 (+0.19), Spirit Resilience +0.02 (+0.12)
- **Drifter**: Spirit Resilience +0.10 (+0.20), Witchmail +0.09 (+0.26), Spellbreaker +0.03 (+0.14)
- **Venator**: Metal Skin +0.13 (+0.20), Bullet Resilience +0.09 (+0.14), Plated Armor +0.05 (+0.14)
- **Victor**: Healbane +0.04 (+0.10), Spirit Resilience +0.03 (+0.14), Spellbreaker +0.01 (+0.12)
- **Paige**: Unstoppable +0.22 (+0.31), Debuff Reducer +0.08 (+0.12), Spellbreaker +0.01 (+0.12)
- **The Doorman**: Spirit Resilience +0.17 (+0.28), Indomitable +0.14 (+0.26), Witchmail +0.12 (+0.28)
- **Billy**: Spirit Resilience +0.03 (+0.14), Indomitable +0.03 (+0.15), Unstoppable +0.02 (+0.11)
- **Graves**: Return Fire +0.05 (+0.10), Metal Skin +0.04 (+0.12), Witchmail +0.03 (+0.20)
- **Apollo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.19 (+0.30), Indomitable +0.16 (+0.27), Spellbreaker +0.12 (+0.23)
- **Rem**: Debuff Reducer +0.05 (+0.09), Unstoppable +0.03 (+0.12), Counterspell -0.01 (+0.03)
- **Silver**: Dispel Magic +0.06 (+0.11), Reactive Barrier +0.04 (+0.07), Debuff Reducer -0.01 (+0.04)
- **Celeste**: Dispel Magic +0.02 (+0.07), Witchmail +0.01 (+0.18), Reactive Barrier -0.01 (+0.03)
- **Rat King**: Return Fire +0.00 (+0.05), Bullet Resilience -0.00 (+0.05), Plated Armor -0.00 (+0.09)
- **Solomon**: Reactive Barrier +0.01 (+0.05), Dispel Magic -0.00 (+0.04), Counterspell -0.01 (+0.03)
- **Violet**: Return Fire +0.02 (+0.06), Healbane +0.01 (+0.08), Witchmail +0.01 (+0.17)
- **Nurse Harrow**: Healbane +0.03 (+0.10), Counterspell +0.00 (+0.04), Return Fire -0.01 (+0.03)
- **Baba**: Unstoppable +0.02 (+0.11), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.181 | +0.057 | +0.145 | Lash +0.47, Deadman Danny +0.43, The Doorman +0.40 | 15 heroes |
| Divine Barrier | 6,400 | +0.204 | +0.032 | +0.053 | The Doorman +0.23, Lash +0.20, Calico +0.12 | 3 heroes |
| Indomitable | 6,400 | +0.165 | +0.027 | +0.154 | Wraith +0.33, Deadman Danny +0.27, Vyper +0.26 | 1 heroes |
| Dispel Magic | 3,200 | +0.081 | +0.025 | +0.051 | Mirage +0.29, Lash +0.24, Silver +0.20 | 9 heroes |
| Witchmail | 6,400 | +0.138 | +0.021 | +0.167 | Deadman Danny +0.34, The Doorman +0.29, Lash +0.24 | 2 heroes |
| Spellbreaker | 6,400 | +0.125 | +0.020 | +0.142 | Deadman Danny +0.36, Lash +0.34, The Doorman +0.23 | 0 heroes |
| Plated Armor | 6,400 | -0.034 | -0.005 | +0.093 | Holliday +0.24, Grey Talon +0.17, Lash +0.10 | 2 heroes |
| Unstoppable | 6,400 | -0.072 | -0.011 | +0.122 | Paige +0.28, Haze +0.27, Infernus +0.17 | 8 heroes |
| Counterspell | 3,200 | -0.041 | -0.013 | +0.029 | Lash +0.05, Drifter +0.03, Paradox +0.02 | 1 heroes |
| Bullet Resilience | 3,200 | -0.049 | -0.015 | +0.049 | Lash +0.10, Venator +0.09, Lady Geist +0.09 | 0 heroes |
| Reactive Barrier | 1,600 | -0.033 | -0.020 | +0.030 | The Doorman +0.16, Yamato +0.12, Deadman Danny +0.11 | 3 heroes |
| Debuff Reducer | 1,600 | -0.037 | -0.023 | +0.043 | Holliday +0.09, Rem +0.08, Paige +0.08 | 0 heroes |
| Healbane | 1,600 | -0.044 | -0.028 | +0.056 | Apollo +0.06, Victor +0.06, Nurse Harrow +0.05 | 14 heroes |
| Metal Skin | 3,200 | -0.162 | -0.051 | +0.096 | Wraith +0.18, Lash +0.17, Grey Talon +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.174 | -0.109 | +0.042 | Paradox +0.08, Haze +0.06, Violet +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.17 (+0.29), Dispel Magic +0.12 (+0.17), Plated Armor +0.05 (+0.15)
- **Seven**: Witchmail +0.01 (+0.18), Plated Armor -0.01 (+0.09), Counterspell -0.02 (+0.01)
- **Vindicta**: Bullet Resilience +0.06 (+0.11), Return Fire +0.04 (+0.08), Plated Armor +0.03 (+0.12)
- **Lady Geist**: Bullet Resilience +0.09 (+0.14), Metal Skin +0.08 (+0.17), Divine Barrier +0.05 (+0.11)
- **Abrams**: Unstoppable +0.03 (+0.15), Dispel Magic +0.02 (+0.07), Reactive Barrier +0.01 (+0.04)
- **Wraith**: Indomitable +0.33 (+0.48), Metal Skin +0.18 (+0.28), Spellbreaker +0.09 (+0.23)
- **McGinnis**: Spirit Resilience +0.10 (+0.24), Witchmail +0.04 (+0.20), Dispel Magic +0.01 (+0.07)
- **Paradox**: Witchmail +0.17 (+0.34), Dispel Magic +0.11 (+0.16), Unstoppable +0.11 (+0.23)
- **Dynamo**: Healbane +0.00 (+0.06), Counterspell -0.00 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.07 (+0.22), Spellbreaker +0.02 (+0.16), Healbane +0.01 (+0.06)
- **Haze**: Unstoppable +0.27 (+0.39), Indomitable +0.07 (+0.22), Bullet Resilience +0.06 (+0.11)
- **Holliday**: Plated Armor +0.24 (+0.33), Debuff Reducer +0.09 (+0.14), Spellbreaker +0.09 (+0.23)
- **Bebop**: Debuff Reducer +0.07 (+0.11), Healbane +0.03 (+0.09), Reactive Barrier +0.00 (+0.03)
- **Calico**: Spirit Resilience +0.14 (+0.28), Divine Barrier +0.12 (+0.17), Spellbreaker +0.08 (+0.22)
- **Grey Talon**: Spirit Resilience +0.33 (+0.47), Spellbreaker +0.23 (+0.37), Indomitable +0.18 (+0.33)
- **Mo & Krill**: Dispel Magic +0.03 (+0.08), Healbane +0.02 (+0.08), Counterspell -0.01 (+0.02)
- **Shiv**: Bullet Resilience +0.06 (+0.11), Divine Barrier +0.04 (+0.09), Plated Armor +0.04 (+0.13)
- **Ivy**: Unstoppable +0.16 (+0.29), Indomitable +0.05 (+0.21), Debuff Reducer +0.05 (+0.09)
- **Warden**: Bullet Resilience +0.02 (+0.07), Plated Armor +0.02 (+0.11), Divine Barrier +0.02 (+0.07)
- **Yamato**: Reactive Barrier +0.12 (+0.15), Indomitable +0.11 (+0.26), Plated Armor +0.06 (+0.15)
- **Lash**: Spirit Resilience +0.47 (+0.62), Spellbreaker +0.34 (+0.48), Witchmail +0.24 (+0.40)
- **Viscous**: Return Fire +0.05 (+0.09), Divine Barrier +0.04 (+0.09), Counterspell +0.00 (+0.03)
- **Pocket**: Spirit Resilience +0.09 (+0.23), Return Fire +0.01 (+0.05), Spellbreaker -0.01 (+0.14)
- **Mirage**: Dispel Magic +0.29 (+0.34), Metal Skin +0.07 (+0.17), Plated Armor +0.05 (+0.14)
- **Vyper**: Indomitable +0.26 (+0.42), Plated Armor +0.06 (+0.15), Bullet Resilience +0.04 (+0.09)
- **Sinclair**: Indomitable +0.19 (+0.34), Debuff Reducer +0.04 (+0.08), Spellbreaker +0.03 (+0.17)
- **Mina**: Divine Barrier -0.01 (+0.05), Counterspell -0.01 (+0.02), Return Fire -0.01 (+0.03)
- **Drifter**: Spirit Resilience +0.25 (+0.39), Witchmail +0.14 (+0.31), Counterspell +0.03 (+0.06)
- **Venator**: Metal Skin +0.13 (+0.23), Bullet Resilience +0.09 (+0.14), Plated Armor +0.05 (+0.15)
- **Victor**: Healbane +0.06 (+0.12), Spellbreaker +0.06 (+0.20), Spirit Resilience +0.06 (+0.20)
- **Paige**: Unstoppable +0.28 (+0.40), Debuff Reducer +0.08 (+0.12), Witchmail +0.01 (+0.18)
- **The Doorman**: Spirit Resilience +0.40 (+0.55), Witchmail +0.29 (+0.45), Divine Barrier +0.23 (+0.29)
- **Billy**: Reactive Barrier +0.05 (+0.08), Healbane +0.03 (+0.09), Counterspell +0.01 (+0.04)
- **Graves**: Metal Skin +0.03 (+0.13), Witchmail +0.02 (+0.19), Spirit Resilience +0.01 (+0.16)
- **Apollo**: Healbane +0.06 (+0.12), Reactive Barrier +0.02 (+0.05), Counterspell +0.01 (+0.04)
- **Deadman Danny**: Spirit Resilience +0.43 (+0.58), Spellbreaker +0.36 (+0.51), Witchmail +0.34 (+0.51)
- **Rem**: Debuff Reducer +0.08 (+0.13), Unstoppable +0.01 (+0.14), Counterspell +0.00 (+0.03)
- **Silver**: Dispel Magic +0.20 (+0.25), Metal Skin +0.15 (+0.25), Indomitable +0.15 (+0.30)
- **Celeste**: Spirit Resilience +0.10 (+0.24), Witchmail +0.10 (+0.26), Divine Barrier +0.04 (+0.09)
- **Rat King**: Return Fire -0.00 (+0.04), Healbane -0.01 (+0.04), Counterspell -0.01 (+0.02)
- **Solomon**: Return Fire +0.02 (+0.06), Counterspell +0.01 (+0.03), Reactive Barrier -0.01 (+0.02)
- **Violet**: Return Fire +0.06 (+0.10), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Nurse Harrow**: Healbane +0.05 (+0.11), Divine Barrier +0.04 (+0.09), Dispel Magic +0.02 (+0.07)
- **Baba**: Healbane +0.04 (+0.10), Unstoppable +0.02 (+0.14), Counterspell +0.02 (+0.05)
