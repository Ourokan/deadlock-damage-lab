# Counter items in the sim (phantom and up)

Built 2026-10-28T00:15:39Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Divine Barrier | 6,400 | +0.366 | +0.059 | +0.090 | Lash +0.17, Calico +0.12, Wraith +0.12 | 0 heroes |
| Spirit Resilience | 3,200 | +0.184 | +0.058 | +0.114 | Lash +0.22, Deadman Danny +0.22, Graves +0.10 | 1 heroes |
| Reactive Barrier | 1,600 | +0.046 | +0.030 | +0.058 | Deadman Danny +0.18, Calico +0.14, Paradox +0.10 | 3 heroes |
| Dispel Magic | 3,200 | +0.095 | +0.030 | +0.071 | Mirage +0.32, Deadman Danny +0.15, Infernus +0.13 | 4 heroes |
| Indomitable | 6,400 | +0.159 | +0.025 | +0.139 | Vyper +0.26, Deadman Danny +0.26, Abrams +0.20 | 0 heroes |
| Witchmail | 6,400 | +0.145 | +0.023 | +0.194 | Deadman Danny +0.24, Lash +0.18, Wraith +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | +0.022 | +0.014 | +0.055 | Deadman Danny +0.10, Wraith +0.08, Holliday +0.07 | 0 heroes |
| Spellbreaker | 6,400 | +0.079 | +0.012 | +0.138 | Deadman Danny +0.28, Lash +0.21, Calico +0.12 | 0 heroes |
| Bullet Resilience | 3,200 | -0.007 | -0.002 | +0.080 | Deadman Danny +0.17, Venator +0.15, Paradox +0.13 | 0 heroes |
| Plated Armor | 6,400 | -0.043 | -0.007 | +0.116 | Holliday +0.21, Deadman Danny +0.21, Wraith +0.13 | 0 heroes |
| Healbane | 1,600 | -0.011 | -0.007 | +0.085 | Deadman Danny +0.08, Billy +0.05, Lady Geist +0.04 | 11 heroes |
| Counterspell | 3,200 | -0.026 | -0.008 | +0.068 | Deadman Danny +0.13, Wraith +0.05, Billy +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.064 | -0.010 | +0.114 | Deadman Danny +0.20, Abrams +0.12, Haze +0.09 | 0 heroes |
| Metal Skin | 3,200 | -0.165 | -0.052 | +0.093 | Wraith +0.16, Paradox +0.15, Lash +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.177 | -0.111 | +0.073 | Deadman Danny +0.12, Paradox +0.06, Lady Geist +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.13 (+0.20), Spirit Resilience +0.07 (+0.18), Unstoppable +0.05 (+0.16)
- **Seven**: Healbane -0.02 (+0.07), Counterspell -0.02 (+0.04), Reactive Barrier -0.03 (+0.03)
- **Vindicta**: Return Fire +0.01 (+0.09), Witchmail -0.00 (+0.19), Counterspell -0.00 (+0.06)
- **Lady Geist**: Return Fire +0.06 (+0.13), Healbane +0.04 (+0.12), Counterspell +0.01 (+0.08)
- **Abrams**: Indomitable +0.20 (+0.34), Unstoppable +0.12 (+0.23), Spirit Resilience +0.08 (+0.19)
- **Wraith**: Indomitable +0.19 (+0.33), Metal Skin +0.16 (+0.25), Plated Armor +0.13 (+0.25)
- **McGinnis**: Spirit Resilience +0.00 (+0.12), Return Fire -0.01 (+0.06), Healbane -0.02 (+0.07)
- **Paradox**: Metal Skin +0.15 (+0.25), Bullet Resilience +0.13 (+0.21), Plated Armor +0.12 (+0.23)
- **Dynamo**: Healbane -0.01 (+0.08), Counterspell -0.03 (+0.04), Debuff Reducer -0.04 (+0.02)
- **Kelvin**: Healbane +0.00 (+0.09), Counterspell -0.01 (+0.06), Debuff Reducer -0.02 (+0.04)
- **Haze**: Indomitable +0.10 (+0.24), Unstoppable +0.09 (+0.20), Plated Armor +0.04 (+0.16)
- **Holliday**: Plated Armor +0.21 (+0.33), Spellbreaker +0.09 (+0.23), Indomitable +0.07 (+0.21)
- **Bebop**: Healbane +0.03 (+0.12), Counterspell +0.01 (+0.08), Return Fire +0.00 (+0.08)
- **Calico**: Reactive Barrier +0.14 (+0.19), Divine Barrier +0.12 (+0.21), Spellbreaker +0.12 (+0.26)
- **Grey Talon**: Debuff Reducer +0.04 (+0.10), Reactive Barrier +0.04 (+0.10), Spellbreaker +0.03 (+0.17)
- **Mo & Krill**: Spellbreaker +0.09 (+0.23), Spirit Resilience +0.06 (+0.17), Dispel Magic +0.05 (+0.12)
- **Shiv**: Divine Barrier -0.00 (+0.09), Healbane -0.01 (+0.08), Spirit Resilience -0.01 (+0.10)
- **Ivy**: Indomitable +0.09 (+0.23), Unstoppable +0.08 (+0.19), Bullet Resilience +0.01 (+0.09)
- **Warden**: Return Fire +0.02 (+0.09), Counterspell -0.01 (+0.06), Debuff Reducer -0.01 (+0.05)
- **Yamato**: Healbane +0.03 (+0.12), Counterspell -0.02 (+0.05), Debuff Reducer -0.02 (+0.04)
- **Lash**: Spirit Resilience +0.22 (+0.33), Spellbreaker +0.21 (+0.35), Witchmail +0.18 (+0.37)
- **Viscous**: Return Fire -0.02 (+0.06), Healbane -0.03 (+0.05), Counterspell -0.04 (+0.03)
- **Pocket**: Witchmail +0.05 (+0.25), Spirit Resilience +0.04 (+0.16), Spellbreaker +0.03 (+0.17)
- **Mirage**: Dispel Magic +0.32 (+0.40), Spirit Resilience +0.06 (+0.18), Spellbreaker +0.05 (+0.19)
- **Vyper**: Indomitable +0.26 (+0.40), Debuff Reducer +0.04 (+0.10), Spellbreaker +0.02 (+0.16)
- **Sinclair**: Indomitable +0.13 (+0.27), Return Fire -0.01 (+0.06), Spellbreaker -0.01 (+0.13)
- **Mina**: Return Fire +0.02 (+0.09), Spirit Resilience -0.00 (+0.11), Witchmail -0.00 (+0.19)
- **Drifter**: Counterspell -0.01 (+0.06), Return Fire -0.01 (+0.06), Healbane -0.01 (+0.08)
- **Venator**: Bullet Resilience +0.15 (+0.23), Divine Barrier +0.09 (+0.18), Metal Skin +0.07 (+0.17)
- **Victor**: Healbane +0.02 (+0.10), Spirit Resilience +0.01 (+0.12), Dispel Magic -0.01 (+0.06)
- **Paige**: Return Fire +0.00 (+0.08), Counterspell -0.01 (+0.06), Healbane -0.03 (+0.06)
- **The Doorman**: Indomitable +0.12 (+0.25), Witchmail +0.09 (+0.29), Spirit Resilience +0.09 (+0.20)
- **Billy**: Spellbreaker +0.05 (+0.19), Healbane +0.05 (+0.13), Spirit Resilience +0.04 (+0.16)
- **Graves**: Metal Skin +0.13 (+0.22), Spirit Resilience +0.10 (+0.22), Witchmail +0.09 (+0.28)
- **Apollo**: Unstoppable +0.00 (+0.11), Reactive Barrier -0.00 (+0.05), Healbane -0.01 (+0.08)
- **Deadman Danny**: Spellbreaker +0.28 (+0.41), Indomitable +0.26 (+0.40), Witchmail +0.24 (+0.44)
- **Rem**: Debuff Reducer +0.05 (+0.11), Unstoppable +0.04 (+0.15), Spellbreaker -0.02 (+0.12)
- **Silver**: Dispel Magic +0.04 (+0.11), Debuff Reducer +0.03 (+0.08), Metal Skin +0.01 (+0.11)
- **Celeste**: Spirit Resilience +0.06 (+0.18), Witchmail +0.06 (+0.26), Dispel Magic +0.04 (+0.11)
- **Rat King**: Counterspell -0.01 (+0.06), Bullet Resilience -0.01 (+0.07), Return Fire -0.01 (+0.06)
- **Solomon**: Return Fire -0.00 (+0.07), Counterspell -0.02 (+0.05), Debuff Reducer -0.03 (+0.02)
- **Violet**: Return Fire -0.00 (+0.07), Healbane -0.01 (+0.07), Reactive Barrier -0.02 (+0.03)
- **Nurse Harrow**: Healbane +0.01 (+0.10), Counterspell -0.05 (+0.02), Dispel Magic -0.05 (+0.02)
- **Baba**: Healbane -0.00 (+0.08), Debuff Reducer -0.02 (+0.03), Unstoppable -0.03 (+0.09)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.164 | +0.051 | +0.108 | Lash +0.34, Pocket +0.26, Deadman Danny +0.15 | 9 heroes |
| Divine Barrier | 6,400 | +0.301 | +0.048 | +0.065 | Lash +0.20, Paradox +0.10, Wraith +0.07 | 1 heroes |
| Dispel Magic | 3,200 | +0.086 | +0.027 | +0.052 | Mirage +0.28, Infernus +0.11, Deadman Danny +0.10 | 6 heroes |
| Witchmail | 6,400 | +0.145 | +0.023 | +0.162 | Lash +0.18, Pocket +0.17, Deadman Danny +0.15 | 0 heroes |
| Indomitable | 6,400 | +0.140 | +0.022 | +0.109 | Vyper +0.37, Wraith +0.19, Deadman Danny +0.18 | 0 heroes |
| Reactive Barrier | 1,600 | +0.024 | +0.015 | +0.033 | Paradox +0.09, The Doorman +0.07, Vyper +0.07 | 4 heroes |
| Spellbreaker | 6,400 | +0.095 | +0.015 | +0.110 | Lash +0.34, Pocket +0.15, Deadman Danny +0.12 | 0 heroes |
| Debuff Reducer | 1,600 | -0.003 | -0.002 | +0.035 | Wraith +0.07, Vyper +0.06, Grey Talon +0.04 | 1 heroes |
| Plated Armor | 6,400 | -0.039 | -0.006 | +0.087 | Holliday +0.16, Deadman Danny +0.10, Paradox +0.10 | 0 heroes |
| Bullet Resilience | 3,200 | -0.034 | -0.011 | +0.058 | Venator +0.12, Paradox +0.10, Deadman Danny +0.10 | 0 heroes |
| Counterspell | 3,200 | -0.036 | -0.011 | +0.046 | Deadman Danny +0.08, Vindicta +0.04, Vyper +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.086 | -0.014 | +0.090 | Abrams +0.21, Deadman Danny +0.13, Ivy +0.10 | 0 heroes |
| Healbane | 1,600 | -0.039 | -0.024 | +0.063 | Bebop +0.06, Abrams +0.05, Yamato +0.04 | 17 heroes |
| Metal Skin | 3,200 | -0.183 | -0.057 | +0.072 | Graves +0.15, Wraith +0.12, Venator +0.11 | 0 heroes |
| Return Fire | 1,600 | -0.184 | -0.115 | +0.052 | Lady Geist +0.08, Paradox +0.06, Wraith +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.16), Unstoppable +0.04 (+0.13), Spellbreaker +0.04 (+0.15)
- **Seven**: Witchmail +0.03 (+0.19), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.04)
- **Vindicta**: Witchmail +0.06 (+0.22), Counterspell +0.04 (+0.08), Divine Barrier +0.03 (+0.10)
- **Lady Geist**: Return Fire +0.08 (+0.13), Divine Barrier +0.06 (+0.13), Bullet Resilience +0.06 (+0.12)
- **Abrams**: Unstoppable +0.21 (+0.30), Indomitable +0.10 (+0.21), Dispel Magic +0.06 (+0.12)
- **Wraith**: Indomitable +0.19 (+0.30), Metal Skin +0.12 (+0.19), Plated Armor +0.08 (+0.17)
- **McGinnis**: Spirit Resilience +0.05 (+0.16), Witchmail +0.01 (+0.17), Healbane -0.00 (+0.06)
- **Paradox**: Bullet Resilience +0.10 (+0.16), Metal Skin +0.10 (+0.17), Plated Armor +0.10 (+0.18)
- **Dynamo**: Healbane -0.01 (+0.05), Counterspell -0.02 (+0.03), Debuff Reducer -0.02 (+0.01)
- **Kelvin**: Spirit Resilience +0.07 (+0.17), Dispel Magic +0.06 (+0.11), Spellbreaker +0.05 (+0.16)
- **Haze**: Indomitable +0.08 (+0.19), Plated Armor +0.06 (+0.15), Unstoppable +0.05 (+0.14)
- **Holliday**: Plated Armor +0.16 (+0.25), Indomitable +0.05 (+0.16), Return Fire +0.05 (+0.10)
- **Bebop**: Healbane +0.06 (+0.12), Metal Skin +0.01 (+0.08), Counterspell -0.01 (+0.04)
- **Calico**: Reactive Barrier +0.05 (+0.08), Divine Barrier +0.04 (+0.11), Spellbreaker +0.02 (+0.13)
- **Grey Talon**: Spellbreaker +0.05 (+0.16), Debuff Reducer +0.04 (+0.08), Reactive Barrier +0.04 (+0.07)
- **Mo & Krill**: Unstoppable +0.08 (+0.17), Dispel Magic +0.02 (+0.07), Spellbreaker +0.02 (+0.13)
- **Shiv**: Bullet Resilience +0.02 (+0.08), Divine Barrier +0.02 (+0.08), Metal Skin +0.01 (+0.09)
- **Ivy**: Unstoppable +0.10 (+0.19), Indomitable +0.08 (+0.19), Debuff Reducer +0.01 (+0.04)
- **Warden**: Return Fire +0.03 (+0.08), Plated Armor +0.01 (+0.10), Bullet Resilience +0.01 (+0.07)
- **Yamato**: Healbane +0.04 (+0.10), Bullet Resilience +0.02 (+0.08), Witchmail +0.01 (+0.17)
- **Lash**: Spellbreaker +0.34 (+0.45), Spirit Resilience +0.34 (+0.45), Divine Barrier +0.20 (+0.27)
- **Viscous**: Healbane -0.00 (+0.06), Return Fire -0.00 (+0.05), Debuff Reducer -0.01 (+0.03)
- **Pocket**: Spirit Resilience +0.26 (+0.37), Witchmail +0.17 (+0.33), Spellbreaker +0.15 (+0.26)
- **Mirage**: Dispel Magic +0.28 (+0.33), Spirit Resilience +0.06 (+0.17), Spellbreaker +0.05 (+0.16)
- **Vyper**: Indomitable +0.37 (+0.48), Spellbreaker +0.07 (+0.18), Reactive Barrier +0.07 (+0.10)
- **Sinclair**: Indomitable +0.07 (+0.18), Return Fire +0.01 (+0.06), Unstoppable -0.01 (+0.08)
- **Mina**: Divine Barrier +0.04 (+0.10), Spirit Resilience +0.03 (+0.14), Counterspell +0.03 (+0.07)
- **Drifter**: Witchmail +0.02 (+0.18), Return Fire -0.01 (+0.04), Counterspell -0.01 (+0.04)
- **Venator**: Bullet Resilience +0.12 (+0.18), Metal Skin +0.11 (+0.19), Plated Armor +0.05 (+0.14)
- **Victor**: Spellbreaker +0.06 (+0.17), Spirit Resilience +0.06 (+0.17), Healbane -0.01 (+0.05)
- **Paige**: Return Fire -0.01 (+0.05), Counterspell -0.01 (+0.04), Healbane -0.01 (+0.05)
- **The Doorman**: Indomitable +0.08 (+0.19), Reactive Barrier +0.07 (+0.10), Spirit Resilience +0.06 (+0.17)
- **Billy**: Spirit Resilience +0.03 (+0.14), Spellbreaker +0.03 (+0.14), Healbane +0.03 (+0.09)
- **Graves**: Metal Skin +0.15 (+0.22), Spirit Resilience +0.14 (+0.25), Witchmail +0.08 (+0.24)
- **Apollo**: Reactive Barrier +0.01 (+0.04), Healbane -0.00 (+0.06), Debuff Reducer -0.01 (+0.03)
- **Deadman Danny**: Indomitable +0.18 (+0.29), Spirit Resilience +0.15 (+0.26), Witchmail +0.15 (+0.31)
- **Rem**: Counterspell -0.01 (+0.04), Debuff Reducer -0.01 (+0.03), Unstoppable -0.01 (+0.08)
- **Silver**: Dispel Magic +0.08 (+0.13), Reactive Barrier +0.06 (+0.10), Indomitable +0.04 (+0.15)
- **Celeste**: Spirit Resilience +0.06 (+0.16), Witchmail +0.05 (+0.21), Spellbreaker +0.02 (+0.13)
- **Rat King**: Return Fire -0.00 (+0.05), Bullet Resilience -0.01 (+0.05), Metal Skin -0.01 (+0.06)
- **Solomon**: Return Fire +0.01 (+0.06), Reactive Barrier -0.01 (+0.02), Counterspell -0.02 (+0.03)
- **Violet**: Healbane +0.01 (+0.08), Return Fire +0.01 (+0.06), Counterspell -0.01 (+0.03)
- **Nurse Harrow**: Healbane +0.03 (+0.09), Reactive Barrier -0.02 (+0.02), Counterspell -0.02 (+0.03)
- **Baba**: Unstoppable +0.05 (+0.14), Healbane +0.01 (+0.08), Debuff Reducer +0.01 (+0.04)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.150 | +0.047 | +0.106 | Deadman Danny +0.20, The Doorman +0.17, Lash +0.16 | 14 heroes |
| Divine Barrier | 6,400 | +0.225 | +0.035 | +0.051 | The Doorman +0.09, Lash +0.09, Vindicta +0.07 | 2 heroes |
| Dispel Magic | 3,200 | +0.090 | +0.028 | +0.050 | Mirage +0.24, Infernus +0.18, Deadman Danny +0.07 | 9 heroes |
| Indomitable | 6,400 | +0.146 | +0.024 | +0.118 | Vyper +0.36, Wraith +0.24, Sinclair +0.21 | 0 heroes |
| Witchmail | 6,400 | +0.137 | +0.021 | +0.162 | Lash +0.15, Deadman Danny +0.12, The Doorman +0.12 | 1 heroes |
| Spellbreaker | 6,400 | +0.105 | +0.016 | +0.113 | Lash +0.20, Grey Talon +0.15, Infernus +0.15 | 0 heroes |
| Reactive Barrier | 1,600 | +0.003 | +0.002 | +0.036 | Yamato +0.12, Wraith +0.08, Deadman Danny +0.08 | 4 heroes |
| Debuff Reducer | 1,600 | -0.001 | -0.000 | +0.044 | Grey Talon +0.11, Paige +0.08, Wraith +0.08 | 0 heroes |
| Plated Armor | 6,400 | -0.038 | -0.006 | +0.088 | Yamato +0.10, Wraith +0.10, Deadman Danny +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.042 | -0.013 | +0.036 | Deadman Danny +0.06, Vindicta +0.03, Kelvin +0.03 | 1 heroes |
| Unstoppable | 6,400 | -0.083 | -0.013 | +0.091 | Paige +0.22, Abrams +0.14, Grey Talon +0.14 | 3 heroes |
| Bullet Resilience | 3,200 | -0.048 | -0.015 | +0.052 | Venator +0.09, Wraith +0.07, Vindicta +0.07 | 1 heroes |
| Healbane | 1,600 | -0.040 | -0.025 | +0.062 | Abrams +0.05, Infernus +0.04, Lady Geist +0.04 | 16 heroes |
| Metal Skin | 3,200 | -0.178 | -0.056 | +0.078 | Wraith +0.17, Venator +0.12, Grey Talon +0.10 | 0 heroes |
| Return Fire | 1,600 | -0.181 | -0.113 | +0.043 | Vindicta +0.07, Graves +0.05, Lady Geist +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.18 (+0.23), Spellbreaker +0.15 (+0.26), Unstoppable +0.09 (+0.18)
- **Seven**: Witchmail +0.00 (+0.16), Counterspell -0.01 (+0.03), Healbane -0.01 (+0.05)
- **Vindicta**: Divine Barrier +0.07 (+0.12), Return Fire +0.07 (+0.11), Bullet Resilience +0.07 (+0.12)
- **Lady Geist**: Return Fire +0.05 (+0.09), Metal Skin +0.05 (+0.13), Bullet Resilience +0.05 (+0.10)
- **Abrams**: Unstoppable +0.14 (+0.24), Dispel Magic +0.05 (+0.10), Healbane +0.05 (+0.11)
- **Wraith**: Indomitable +0.24 (+0.36), Metal Skin +0.17 (+0.24), Witchmail +0.11 (+0.28)
- **McGinnis**: Spirit Resilience +0.08 (+0.19), Witchmail +0.05 (+0.21), Spellbreaker +0.03 (+0.14)
- **Paradox**: Witchmail +0.09 (+0.25), Spellbreaker +0.06 (+0.18), Indomitable +0.06 (+0.18)
- **Dynamo**: Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02), Return Fire -0.03 (+0.01)
- **Kelvin**: Spirit Resilience +0.05 (+0.16), Counterspell +0.03 (+0.06), Debuff Reducer +0.01 (+0.05)
- **Haze**: Plated Armor +0.05 (+0.14), Bullet Resilience +0.04 (+0.09), Witchmail +0.04 (+0.20)
- **Holliday**: Indomitable +0.07 (+0.19), Spellbreaker +0.04 (+0.16), Debuff Reducer +0.03 (+0.08)
- **Bebop**: Healbane +0.03 (+0.09), Counterspell -0.02 (+0.02), Return Fire -0.02 (+0.03)
- **Calico**: Spirit Resilience +0.05 (+0.16), Divine Barrier +0.03 (+0.08), Reactive Barrier +0.03 (+0.06)
- **Grey Talon**: Spellbreaker +0.15 (+0.27), Unstoppable +0.14 (+0.23), Indomitable +0.11 (+0.23)
- **Mo & Krill**: Spellbreaker +0.06 (+0.17), Spirit Resilience +0.04 (+0.15), Unstoppable +0.04 (+0.13)
- **Shiv**: Metal Skin +0.05 (+0.12), Bullet Resilience +0.04 (+0.09), Plated Armor +0.03 (+0.12)
- **Ivy**: Unstoppable +0.07 (+0.17), Indomitable +0.03 (+0.15), Healbane +0.01 (+0.07)
- **Warden**: Return Fire +0.02 (+0.07), Divine Barrier +0.01 (+0.06), Counterspell +0.00 (+0.04)
- **Yamato**: Indomitable +0.13 (+0.25), Reactive Barrier +0.12 (+0.16), Plated Armor +0.10 (+0.19)
- **Lash**: Spellbreaker +0.20 (+0.32), Spirit Resilience +0.16 (+0.27), Witchmail +0.15 (+0.31)
- **Viscous**: Return Fire +0.02 (+0.06), Divine Barrier +0.02 (+0.07), Counterspell +0.01 (+0.04)
- **Pocket**: Spirit Resilience +0.09 (+0.19), Spellbreaker +0.03 (+0.14), Witchmail +0.02 (+0.18)
- **Mirage**: Dispel Magic +0.24 (+0.29), Plated Armor +0.03 (+0.12), Healbane +0.02 (+0.08)
- **Vyper**: Indomitable +0.36 (+0.48), Debuff Reducer +0.06 (+0.10), Spellbreaker +0.06 (+0.17)
- **Sinclair**: Indomitable +0.21 (+0.32), Return Fire +0.01 (+0.05), Unstoppable -0.01 (+0.08)
- **Mina**: Divine Barrier +0.03 (+0.08), Witchmail +0.02 (+0.19), Spirit Resilience +0.02 (+0.12)
- **Drifter**: Spirit Resilience +0.10 (+0.20), Witchmail +0.08 (+0.25), Spellbreaker +0.03 (+0.14)
- **Venator**: Metal Skin +0.12 (+0.20), Bullet Resilience +0.09 (+0.14), Plated Armor +0.05 (+0.14)
- **Victor**: Spirit Resilience +0.02 (+0.13), Spellbreaker +0.00 (+0.12), Healbane +0.00 (+0.07)
- **Paige**: Unstoppable +0.22 (+0.31), Debuff Reducer +0.08 (+0.12), Spellbreaker +0.01 (+0.12)
- **The Doorman**: Spirit Resilience +0.17 (+0.28), Indomitable +0.14 (+0.25), Witchmail +0.12 (+0.28)
- **Billy**: Spirit Resilience +0.03 (+0.14), Indomitable +0.03 (+0.15), Spellbreaker +0.02 (+0.13)
- **Graves**: Return Fire +0.05 (+0.10), Metal Skin +0.04 (+0.12), Witchmail +0.03 (+0.20)
- **Apollo**: Healbane +0.03 (+0.09), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.02)
- **Deadman Danny**: Spirit Resilience +0.20 (+0.31), Indomitable +0.16 (+0.28), Spellbreaker +0.13 (+0.24)
- **Rem**: Debuff Reducer +0.05 (+0.09), Unstoppable +0.03 (+0.12), Counterspell -0.01 (+0.03)
- **Silver**: Dispel Magic +0.06 (+0.11), Reactive Barrier +0.03 (+0.07), Debuff Reducer -0.01 (+0.04)
- **Celeste**: Dispel Magic +0.02 (+0.07), Witchmail +0.01 (+0.17), Reactive Barrier -0.01 (+0.03)
- **Rat King**: Return Fire +0.00 (+0.05), Bullet Resilience -0.00 (+0.05), Plated Armor -0.00 (+0.09)
- **Solomon**: Reactive Barrier +0.02 (+0.05), Dispel Magic -0.01 (+0.04), Counterspell -0.01 (+0.03)
- **Violet**: Return Fire +0.02 (+0.06), Healbane +0.01 (+0.07), Witchmail +0.01 (+0.17)
- **Nurse Harrow**: Healbane +0.04 (+0.10), Counterspell +0.01 (+0.05), Divine Barrier -0.01 (+0.04)
- **Baba**: Unstoppable +0.03 (+0.12), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.184 | +0.058 | +0.144 | Lash +0.45, Deadman Danny +0.42, The Doorman +0.40 | 15 heroes |
| Divine Barrier | 6,400 | +0.222 | +0.035 | +0.054 | Lash +0.24, The Doorman +0.23, Calico +0.12 | 3 heroes |
| Dispel Magic | 3,200 | +0.094 | +0.029 | +0.051 | Mirage +0.28, Lash +0.21, Silver +0.20 | 9 heroes |
| Indomitable | 6,400 | +0.168 | +0.027 | +0.153 | Wraith +0.32, Vyper +0.27, Deadman Danny +0.26 | 1 heroes |
| Witchmail | 6,400 | +0.136 | +0.021 | +0.167 | Deadman Danny +0.34, The Doorman +0.28, Lash +0.23 | 2 heroes |
| Spellbreaker | 6,400 | +0.128 | +0.020 | +0.141 | Deadman Danny +0.36, Lash +0.32, The Doorman +0.23 | 0 heroes |
| Debuff Reducer | 1,600 | -0.009 | -0.005 | +0.044 | Holliday +0.09, Rem +0.08, Paige +0.08 | 0 heroes |
| Plated Armor | 6,400 | -0.044 | -0.007 | +0.092 | Holliday +0.23, Grey Talon +0.18, Lash +0.08 | 2 heroes |
| Reactive Barrier | 1,600 | -0.013 | -0.008 | +0.031 | The Doorman +0.16, Yamato +0.12, Deadman Danny +0.10 | 3 heroes |
| Unstoppable | 6,400 | -0.071 | -0.011 | +0.124 | Paige +0.27, Haze +0.27, Infernus +0.17 | 8 heroes |
| Counterspell | 3,200 | -0.046 | -0.015 | +0.030 | Lash +0.08, Drifter +0.03, Lady Geist +0.02 | 1 heroes |
| Bullet Resilience | 3,200 | -0.049 | -0.015 | +0.049 | Lash +0.11, Venator +0.09, Lady Geist +0.09 | 0 heroes |
| Healbane | 1,600 | -0.044 | -0.028 | +0.057 | Apollo +0.06, Nurse Harrow +0.06, Victor +0.05 | 14 heroes |
| Metal Skin | 3,200 | -0.170 | -0.053 | +0.096 | Wraith +0.19, Lash +0.17, Grey Talon +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.175 | -0.109 | +0.043 | Lash +0.09, Paradox +0.08, Violet +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.17 (+0.29), Dispel Magic +0.14 (+0.19), Plated Armor +0.06 (+0.16)
- **Seven**: Witchmail +0.00 (+0.17), Plated Armor -0.01 (+0.09), Healbane -0.02 (+0.04)
- **Vindicta**: Bullet Resilience +0.06 (+0.11), Return Fire +0.04 (+0.08), Plated Armor +0.03 (+0.12)
- **Lady Geist**: Bullet Resilience +0.09 (+0.14), Metal Skin +0.08 (+0.17), Divine Barrier +0.05 (+0.11)
- **Abrams**: Unstoppable +0.03 (+0.15), Dispel Magic +0.02 (+0.07), Reactive Barrier +0.01 (+0.04)
- **Wraith**: Indomitable +0.32 (+0.48), Metal Skin +0.19 (+0.28), Spellbreaker +0.09 (+0.23)
- **McGinnis**: Spirit Resilience +0.07 (+0.22), Witchmail +0.02 (+0.19), Healbane +0.01 (+0.07)
- **Paradox**: Witchmail +0.17 (+0.34), Dispel Magic +0.12 (+0.17), Unstoppable +0.11 (+0.24)
- **Dynamo**: Healbane +0.00 (+0.06), Counterspell -0.00 (+0.03), Reactive Barrier -0.03 (+0.00)
- **Kelvin**: Spirit Resilience +0.07 (+0.22), Spellbreaker +0.02 (+0.16), Healbane +0.01 (+0.06)
- **Haze**: Unstoppable +0.27 (+0.39), Indomitable +0.07 (+0.22), Bullet Resilience +0.07 (+0.11)
- **Holliday**: Plated Armor +0.23 (+0.32), Debuff Reducer +0.09 (+0.13), Spellbreaker +0.09 (+0.23)
- **Bebop**: Debuff Reducer +0.07 (+0.11), Healbane +0.03 (+0.09), Reactive Barrier +0.00 (+0.03)
- **Calico**: Spirit Resilience +0.14 (+0.28), Divine Barrier +0.12 (+0.17), Spellbreaker +0.08 (+0.22)
- **Grey Talon**: Spirit Resilience +0.33 (+0.47), Spellbreaker +0.23 (+0.37), Indomitable +0.18 (+0.33)
- **Mo & Krill**: Dispel Magic +0.02 (+0.07), Healbane +0.02 (+0.07), Counterspell -0.01 (+0.02)
- **Shiv**: Bullet Resilience +0.06 (+0.11), Divine Barrier +0.04 (+0.09), Plated Armor +0.04 (+0.13)
- **Ivy**: Unstoppable +0.16 (+0.29), Indomitable +0.06 (+0.21), Debuff Reducer +0.04 (+0.09)
- **Warden**: Bullet Resilience +0.02 (+0.07), Plated Armor +0.02 (+0.11), Divine Barrier +0.02 (+0.07)
- **Yamato**: Reactive Barrier +0.12 (+0.15), Indomitable +0.11 (+0.27), Plated Armor +0.06 (+0.15)
- **Lash**: Spirit Resilience +0.45 (+0.60), Spellbreaker +0.32 (+0.46), Divine Barrier +0.24 (+0.29)
- **Viscous**: Return Fire +0.04 (+0.08), Divine Barrier +0.04 (+0.09), Counterspell +0.00 (+0.03)
- **Pocket**: Spirit Resilience +0.08 (+0.23), Return Fire +0.00 (+0.05), Spellbreaker -0.00 (+0.14)
- **Mirage**: Dispel Magic +0.28 (+0.33), Metal Skin +0.06 (+0.16), Plated Armor +0.05 (+0.14)
- **Vyper**: Indomitable +0.27 (+0.42), Plated Armor +0.06 (+0.15), Bullet Resilience +0.04 (+0.09)
- **Sinclair**: Indomitable +0.19 (+0.34), Debuff Reducer +0.04 (+0.08), Spellbreaker +0.03 (+0.17)
- **Mina**: Divine Barrier -0.01 (+0.05), Counterspell -0.01 (+0.02), Plated Armor -0.01 (+0.08)
- **Drifter**: Spirit Resilience +0.25 (+0.40), Witchmail +0.15 (+0.31), Counterspell +0.03 (+0.06)
- **Venator**: Metal Skin +0.13 (+0.23), Bullet Resilience +0.09 (+0.14), Plated Armor +0.05 (+0.15)
- **Victor**: Spellbreaker +0.06 (+0.20), Spirit Resilience +0.06 (+0.20), Healbane +0.05 (+0.11)
- **Paige**: Unstoppable +0.27 (+0.40), Debuff Reducer +0.08 (+0.12), Witchmail +0.01 (+0.17)
- **The Doorman**: Spirit Resilience +0.40 (+0.55), Witchmail +0.28 (+0.45), Spellbreaker +0.23 (+0.37)
- **Billy**: Reactive Barrier +0.04 (+0.08), Healbane +0.03 (+0.09), Counterspell +0.01 (+0.04)
- **Graves**: Metal Skin +0.04 (+0.13), Witchmail +0.03 (+0.20), Spirit Resilience +0.02 (+0.16)
- **Apollo**: Healbane +0.06 (+0.12), Reactive Barrier +0.02 (+0.05), Counterspell +0.01 (+0.04)
- **Deadman Danny**: Spirit Resilience +0.42 (+0.57), Spellbreaker +0.36 (+0.50), Witchmail +0.34 (+0.51)
- **Rem**: Debuff Reducer +0.08 (+0.13), Unstoppable +0.01 (+0.13), Counterspell -0.00 (+0.03)
- **Silver**: Dispel Magic +0.20 (+0.25), Metal Skin +0.15 (+0.25), Indomitable +0.14 (+0.30)
- **Celeste**: Spirit Resilience +0.10 (+0.24), Witchmail +0.09 (+0.26), Divine Barrier +0.04 (+0.09)
- **Rat King**: Return Fire -0.00 (+0.04), Healbane -0.01 (+0.04), Counterspell -0.01 (+0.02)
- **Solomon**: Return Fire +0.01 (+0.06), Counterspell +0.00 (+0.03), Reactive Barrier -0.01 (+0.02)
- **Violet**: Return Fire +0.06 (+0.10), Healbane +0.00 (+0.06), Counterspell -0.01 (+0.02)
- **Nurse Harrow**: Healbane +0.06 (+0.11), Divine Barrier +0.03 (+0.08), Bullet Resilience +0.03 (+0.08)
- **Baba**: Healbane +0.04 (+0.09), Unstoppable +0.02 (+0.14), Counterspell +0.01 (+0.04)
