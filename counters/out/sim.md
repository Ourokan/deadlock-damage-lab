# Counter items in the sim (phantom and up)

Built 2026-11-09T04:15:38Z by `counters/scripts/export_sim.py`. Each hero's most popular real build gets the item added on top and is scored with the overall test (net damage dealt before dying against every hero's typical real build at that net worth; sustain, movement, mechanics and counterplay on). Gain = overall score change, weighted by how often each hero reaches that net worth; the overall score also multiplies in the item's real per-hero win edge (overall_search win_value), so items real buyers lose with score low on Gain even when the sim likes them. *Sim mean* = the same without the win edge (mean of vs over enemies). *Vs enemy* = the change in that one matchup's damage before dying, as a share of the popular build's mean over all matchups (so its enemy-weighted mean is the gain); *lift* = vs enemy minus the item's mean over all enemies.

## 18,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.199 | +0.062 | +0.140 | Lash +0.22, Deadman Danny +0.18, The Doorman +0.16 | 1 heroes |
| Divine Barrier | 6,400 | +0.264 | +0.042 | +0.135 | Lash +0.17, Viscous +0.16, Abrams +0.13 | 0 heroes |
| Dispel Magic | 3,200 | +0.098 | +0.031 | +0.091 | Mirage +0.38, Paradox +0.16, Lash +0.12 | 4 heroes |
| Indomitable | 6,400 | +0.167 | +0.026 | +0.149 | The Doorman +0.24, Abrams +0.21, Wraith +0.18 | 0 heroes |
| Healbane | 1,600 | +0.041 | +0.026 | +0.089 | Graves +0.12, Yamato +0.09, McGinnis +0.06 | 22 heroes |
| Reactive Barrier | 1,600 | +0.028 | +0.017 | +0.042 | Deadman Danny +0.14, Graves +0.11, Holliday +0.07 | 2 heroes |
| Debuff Reducer | 1,600 | +0.026 | +0.016 | +0.085 | Holliday +0.12, Vyper +0.10, Venator +0.08 | 0 heroes |
| Witchmail | 6,400 | +0.101 | +0.016 | +0.216 | Deadman Danny +0.20, Lash +0.18, Pocket +0.15 | 0 heroes |
| Bullet Resilience | 3,200 | +0.045 | +0.014 | +0.115 | Venator +0.27, Paradox +0.16, Lash +0.16 | 0 heroes |
| Spellbreaker | 6,400 | +0.086 | +0.013 | +0.190 | Deadman Danny +0.21, Lash +0.21, Wraith +0.15 | 0 heroes |
| Plated Armor | 6,400 | +0.006 | +0.001 | +0.151 | Holliday +0.22, Wraith +0.13, Paradox +0.13 | 0 heroes |
| Counterspell | 3,200 | -0.013 | -0.004 | +0.079 | Lash +0.10, Graves +0.08, Deadman Danny +0.07 | 0 heroes |
| Unstoppable | 6,400 | -0.052 | -0.008 | +0.151 | Deadman Danny +0.15, Lash +0.11, Vyper +0.10 | 0 heroes |
| Metal Skin | 3,200 | -0.178 | -0.056 | +0.127 | Wraith +0.23, Paradox +0.20, Lash +0.18 | 0 heroes |
| Return Fire | 1,600 | -0.190 | -0.119 | +0.091 | Paradox +0.11, Deadman Danny +0.07, Holliday +0.06 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.06 (+0.15), Spellbreaker +0.04 (+0.23), Unstoppable +0.03 (+0.18)
- **Seven**: Healbane -0.00 (+0.09), Spirit Resilience -0.03 (+0.11), Reactive Barrier -0.03 (+0.02)
- **Vindicta**: Divine Barrier -0.00 (+0.13), Counterspell -0.00 (+0.08), Healbane -0.01 (+0.08)
- **Lady Geist**: Return Fire +0.02 (+0.11), Divine Barrier +0.01 (+0.14), Counterspell -0.00 (+0.08)
- **Abrams**: Indomitable +0.21 (+0.36), Divine Barrier +0.13 (+0.26), Witchmail +0.08 (+0.30)
- **Wraith**: Metal Skin +0.23 (+0.35), Indomitable +0.18 (+0.33), Spellbreaker +0.15 (+0.34)
- **McGinnis**: Counterspell +0.07 (+0.15), Healbane +0.06 (+0.15), Spirit Resilience +0.05 (+0.19)
- **Paradox**: Metal Skin +0.20 (+0.33), Indomitable +0.17 (+0.32), Bullet Resilience +0.16 (+0.28)
- **Dynamo**: Healbane +0.01 (+0.10), Counterspell -0.03 (+0.05), Reactive Barrier -0.03 (+0.01)
- **Kelvin**: Witchmail +0.02 (+0.24), Healbane +0.01 (+0.10), Spirit Resilience +0.01 (+0.14)
- **Haze**: Indomitable +0.13 (+0.28), Plated Armor +0.10 (+0.25), Unstoppable +0.08 (+0.23)
- **Holliday**: Plated Armor +0.22 (+0.37), Spellbreaker +0.13 (+0.32), Debuff Reducer +0.12 (+0.21)
- **Bebop**: Healbane +0.00 (+0.09), Counterspell +0.00 (+0.08), Divine Barrier -0.00 (+0.13)
- **Calico**: Spellbreaker +0.08 (+0.27), Divine Barrier +0.06 (+0.19), Spirit Resilience +0.05 (+0.19)
- **Grey Talon**: Unstoppable +0.06 (+0.21), Debuff Reducer +0.04 (+0.13), Reactive Barrier +0.04 (+0.08)
- **Mo & Krill**: Spellbreaker +0.07 (+0.26), Witchmail +0.04 (+0.25), Spirit Resilience +0.04 (+0.18)
- **Shiv**: Return Fire -0.01 (+0.08), Healbane -0.01 (+0.08), Divine Barrier -0.02 (+0.11)
- **Ivy**: Indomitable +0.07 (+0.22), Unstoppable +0.03 (+0.18), Healbane +0.00 (+0.09)
- **Warden**: Return Fire +0.00 (+0.09), Debuff Reducer -0.00 (+0.08), Counterspell -0.01 (+0.07)
- **Yamato**: Healbane +0.09 (+0.18), Debuff Reducer +0.06 (+0.14), Spellbreaker +0.05 (+0.24)
- **Lash**: Spirit Resilience +0.22 (+0.36), Spellbreaker +0.21 (+0.40), Metal Skin +0.18 (+0.31)
- **Viscous**: Divine Barrier +0.16 (+0.29), Spirit Resilience +0.09 (+0.23), Spellbreaker +0.08 (+0.27)
- **Pocket**: Witchmail +0.15 (+0.36), Spirit Resilience +0.13 (+0.27), Spellbreaker +0.10 (+0.29)
- **Mirage**: Dispel Magic +0.38 (+0.48), Spellbreaker +0.07 (+0.26), Spirit Resilience +0.05 (+0.19)
- **Vyper**: Spellbreaker +0.11 (+0.30), Debuff Reducer +0.10 (+0.19), Unstoppable +0.10 (+0.25)
- **Sinclair**: Indomitable +0.13 (+0.28), Spellbreaker +0.06 (+0.25), Unstoppable +0.04 (+0.20)
- **Mina**: Return Fire +0.01 (+0.10), Counterspell -0.02 (+0.06), Reactive Barrier -0.03 (+0.02)
- **Drifter**: Reactive Barrier -0.02 (+0.02), Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.07)
- **Venator**: Bullet Resilience +0.27 (+0.38), Debuff Reducer +0.08 (+0.17), Unstoppable +0.08 (+0.23)
- **Victor**: Spirit Resilience +0.12 (+0.26), Spellbreaker +0.10 (+0.29), Witchmail +0.00 (+0.22)
- **Paige**: Reactive Barrier -0.01 (+0.03), Counterspell -0.02 (+0.06), Return Fire -0.02 (+0.07)
- **The Doorman**: Indomitable +0.24 (+0.39), Spirit Resilience +0.16 (+0.30), Spellbreaker +0.14 (+0.33)
- **Billy**: Spellbreaker +0.05 (+0.24), Spirit Resilience +0.04 (+0.18), Healbane +0.03 (+0.12)
- **Graves**: Healbane +0.12 (+0.21), Reactive Barrier +0.11 (+0.16), Metal Skin +0.10 (+0.23)
- **Apollo**: Reactive Barrier -0.03 (+0.01), Counterspell -0.03 (+0.04), Healbane -0.04 (+0.05)
- **Deadman Danny**: Spellbreaker +0.21 (+0.40), Witchmail +0.20 (+0.41), Spirit Resilience +0.18 (+0.32)
- **Rem**: Counterspell -0.02 (+0.06), Reactive Barrier -0.03 (+0.01), Return Fire -0.04 (+0.05)
- **Silver**: Dispel Magic +0.07 (+0.16), Reactive Barrier +0.04 (+0.08), Debuff Reducer +0.01 (+0.10)
- **Celeste**: Spirit Resilience +0.14 (+0.28), Witchmail +0.12 (+0.33), Plated Armor +0.05 (+0.20)
- **Rat King**: Return Fire +0.00 (+0.09), Counterspell -0.01 (+0.07), Divine Barrier -0.01 (+0.12)
- **Solomon**: Reactive Barrier -0.01 (+0.04), Counterspell -0.03 (+0.05), Return Fire -0.03 (+0.06)
- **Violet**: Return Fire +0.05 (+0.14), Unstoppable +0.05 (+0.20), Witchmail +0.03 (+0.24)
- **Nurse Harrow**: Healbane +0.04 (+0.13), Reactive Barrier +0.01 (+0.05), Counterspell -0.05 (+0.03)
- **Baba**: Reactive Barrier -0.00 (+0.04), Healbane -0.01 (+0.08), Counterspell -0.02 (+0.06)

## 27,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.195 | +0.061 | +0.143 | Lash +0.41, Celeste +0.21, Pocket +0.18 | 10 heroes |
| Divine Barrier | 6,400 | +0.214 | +0.034 | +0.098 | Lash +0.23, Paradox +0.10, The Doorman +0.09 | 0 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.064 | Mirage +0.30, Paradox +0.11, Silver +0.10 | 9 heroes |
| Indomitable | 6,400 | +0.152 | +0.024 | +0.106 | Wraith +0.19, The Doorman +0.18, Abrams +0.13 | 0 heroes |
| Spellbreaker | 6,400 | +0.125 | +0.020 | +0.170 | Lash +0.37, Holliday +0.19, Wraith +0.13 | 0 heroes |
| Healbane | 1,600 | +0.029 | +0.018 | +0.066 | Abrams +0.09, Yamato +0.08, Infernus +0.06 | 23 heroes |
| Witchmail | 6,400 | +0.112 | +0.018 | +0.186 | Lash +0.29, Celeste +0.18, The Doorman +0.09 | 1 heroes |
| Reactive Barrier | 1,600 | +0.010 | +0.006 | +0.022 | Abrams +0.09, Graves +0.06, Holliday +0.06 | 3 heroes |
| Bullet Resilience | 3,200 | +0.018 | +0.006 | +0.077 | Venator +0.19, Paradox +0.15, Lash +0.10 | 0 heroes |
| Debuff Reducer | 1,600 | +0.004 | +0.002 | +0.066 | Holliday +0.17, Rem +0.13, Vyper +0.09 | 0 heroes |
| Plated Armor | 6,400 | +0.011 | +0.002 | +0.107 | Holliday +0.25, Paradox +0.10, Haze +0.09 | 0 heroes |
| Counterspell | 3,200 | -0.029 | -0.009 | +0.045 | Lash +0.04, Nurse Harrow +0.04, Abrams +0.04 | 1 heroes |
| Unstoppable | 6,400 | -0.078 | -0.012 | +0.115 | Holliday +0.15, Abrams +0.13, Rem +0.12 | 0 heroes |
| Metal Skin | 3,200 | -0.198 | -0.062 | +0.091 | Wraith +0.25, Lash +0.17, Paradox +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.200 | -0.125 | +0.065 | Paradox +0.08, Lash +0.06, Holliday +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Spellbreaker +0.10 (+0.27), Unstoppable +0.09 (+0.21), Dispel Magic +0.07 (+0.13)
- **Seven**: Witchmail +0.03 (+0.22), Healbane -0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Vindicta**: Divine Barrier +0.05 (+0.15), Return Fire +0.04 (+0.11), Witchmail +0.03 (+0.22)
- **Lady Geist**: Spirit Resilience +0.11 (+0.26), Spellbreaker +0.11 (+0.28), Healbane +0.05 (+0.11)
- **Abrams**: Indomitable +0.13 (+0.24), Unstoppable +0.13 (+0.24), Spirit Resilience +0.11 (+0.25)
- **Wraith**: Metal Skin +0.25 (+0.34), Indomitable +0.19 (+0.30), Spellbreaker +0.13 (+0.30)
- **McGinnis**: Healbane -0.01 (+0.06), Reactive Barrier -0.01 (+0.01), Spirit Resilience -0.01 (+0.13)
- **Paradox**: Metal Skin +0.15 (+0.24), Bullet Resilience +0.15 (+0.22), Indomitable +0.12 (+0.23)
- **Dynamo**: Healbane +0.02 (+0.09), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (+0.00)
- **Kelvin**: Spirit Resilience +0.05 (+0.20), Witchmail +0.01 (+0.20), Spellbreaker -0.01 (+0.16)
- **Haze**: Indomitable +0.12 (+0.23), Plated Armor +0.09 (+0.19), Unstoppable +0.07 (+0.18)
- **Holliday**: Plated Armor +0.25 (+0.36), Spellbreaker +0.19 (+0.36), Debuff Reducer +0.17 (+0.23)
- **Bebop**: Healbane +0.01 (+0.08), Counterspell -0.01 (+0.04), Reactive Barrier -0.01 (+0.01)
- **Calico**: Divine Barrier +0.06 (+0.16), Spirit Resilience +0.05 (+0.19), Spellbreaker +0.02 (+0.19)
- **Grey Talon**: Unstoppable +0.09 (+0.20), Debuff Reducer +0.04 (+0.11), Spellbreaker +0.04 (+0.21)
- **Mo & Krill**: Spellbreaker +0.08 (+0.25), Unstoppable +0.08 (+0.19), Dispel Magic +0.04 (+0.11)
- **Shiv**: Bullet Resilience +0.05 (+0.13), Plated Armor +0.02 (+0.13), Return Fire +0.01 (+0.07)
- **Ivy**: Unstoppable +0.07 (+0.19), Indomitable +0.06 (+0.17), Bullet Resilience +0.03 (+0.10)
- **Warden**: Return Fire +0.03 (+0.09), Divine Barrier -0.00 (+0.09), Debuff Reducer -0.01 (+0.06)
- **Yamato**: Healbane +0.08 (+0.15), Debuff Reducer +0.01 (+0.07), Counterspell -0.00 (+0.04)
- **Lash**: Spirit Resilience +0.41 (+0.56), Spellbreaker +0.37 (+0.54), Witchmail +0.29 (+0.47)
- **Viscous**: Divine Barrier +0.03 (+0.13), Counterspell +0.01 (+0.05), Healbane -0.01 (+0.06)
- **Pocket**: Spirit Resilience +0.18 (+0.33), Witchmail +0.05 (+0.24), Spellbreaker +0.05 (+0.22)
- **Mirage**: Dispel Magic +0.30 (+0.37), Spirit Resilience +0.06 (+0.21), Spellbreaker +0.04 (+0.21)
- **Vyper**: Spellbreaker +0.10 (+0.27), Debuff Reducer +0.09 (+0.15), Unstoppable +0.06 (+0.18)
- **Sinclair**: Indomitable +0.10 (+0.21), Reactive Barrier +0.01 (+0.03), Debuff Reducer -0.00 (+0.06)
- **Mina**: Counterspell +0.01 (+0.05), Return Fire -0.01 (+0.06), Plated Armor -0.01 (+0.10)
- **Drifter**: Return Fire +0.01 (+0.08), Counterspell -0.00 (+0.04), Healbane -0.00 (+0.06)
- **Venator**: Bullet Resilience +0.19 (+0.27), Debuff Reducer +0.07 (+0.13), Unstoppable +0.04 (+0.16)
- **Victor**: Spellbreaker +0.07 (+0.24), Spirit Resilience +0.06 (+0.21), Healbane +0.01 (+0.08)
- **Paige**: Counterspell -0.00 (+0.04), Reactive Barrier -0.01 (+0.01), Return Fire -0.02 (+0.04)
- **The Doorman**: Indomitable +0.18 (+0.29), Spirit Resilience +0.12 (+0.26), Spellbreaker +0.10 (+0.27)
- **Billy**: Healbane +0.00 (+0.07), Counterspell -0.01 (+0.04), Return Fire -0.01 (+0.06)
- **Graves**: Metal Skin +0.07 (+0.16), Reactive Barrier +0.06 (+0.08), Return Fire +0.04 (+0.11)
- **Apollo**: Return Fire -0.01 (+0.06), Counterspell -0.02 (+0.03), Reactive Barrier -0.02 (+0.00)
- **Deadman Danny**: Spirit Resilience +0.10 (+0.24), Witchmail +0.08 (+0.27), Indomitable +0.06 (+0.17)
- **Rem**: Debuff Reducer +0.13 (+0.19), Unstoppable +0.12 (+0.23), Spellbreaker +0.04 (+0.21)
- **Silver**: Dispel Magic +0.10 (+0.16), Reactive Barrier +0.02 (+0.04), Debuff Reducer +0.01 (+0.07)
- **Celeste**: Spirit Resilience +0.21 (+0.35), Witchmail +0.18 (+0.37), Spellbreaker +0.09 (+0.26)
- **Rat King**: Return Fire -0.00 (+0.06), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Solomon**: Reactive Barrier -0.01 (+0.01), Counterspell -0.01 (+0.03), Healbane -0.02 (+0.05)
- **Violet**: Unstoppable +0.06 (+0.18), Witchmail +0.06 (+0.24), Healbane +0.05 (+0.11)
- **Nurse Harrow**: Healbane +0.05 (+0.12), Divine Barrier +0.05 (+0.15), Counterspell +0.04 (+0.08)
- **Baba**: Reactive Barrier -0.00 (+0.02), Counterspell -0.00 (+0.04), Healbane -0.00 (+0.06)

## 37,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.181 | +0.056 | +0.140 | Lash +0.37, Deadman Danny +0.25, Viscous +0.19 | 13 heroes |
| Divine Barrier | 6,400 | +0.177 | +0.028 | +0.084 | Mina +0.09, Vindicta +0.08, Lash +0.08 | 2 heroes |
| Dispel Magic | 3,200 | +0.084 | +0.026 | +0.053 | Mirage +0.25, Infernus +0.11, Lash +0.10 | 11 heroes |
| Indomitable | 6,400 | +0.149 | +0.023 | +0.104 | Haze +0.22, Wraith +0.21, The Doorman +0.17 | 0 heroes |
| Spellbreaker | 6,400 | +0.143 | +0.022 | +0.182 | Lash +0.39, Holliday +0.18, Wraith +0.18 | 0 heroes |
| Healbane | 1,600 | +0.028 | +0.017 | +0.063 | Infernus +0.08, Mo & Krill +0.08, Celeste +0.05 | 25 heroes |
| Witchmail | 6,400 | +0.097 | +0.015 | +0.170 | Deadman Danny +0.18, Lash +0.17, The Doorman +0.12 | 1 heroes |
| Debuff Reducer | 1,600 | +0.007 | +0.004 | +0.071 | Holliday +0.17, Bebop +0.17, Grey Talon +0.14 | 0 heroes |
| Bullet Resilience | 3,200 | +0.013 | +0.004 | +0.062 | Venator +0.21, Vindicta +0.11, Haze +0.11 | 1 heroes |
| Plated Armor | 6,400 | +0.009 | +0.002 | +0.096 | Holliday +0.20, Haze +0.13, Deadman Danny +0.10 | 0 heroes |
| Reactive Barrier | 1,600 | -0.016 | -0.010 | +0.018 | Deadman Danny +0.12, Vyper +0.07, Grey Talon +0.06 | 2 heroes |
| Counterspell | 3,200 | -0.035 | -0.011 | +0.034 | Calico +0.03, Grey Talon +0.02, Mo & Krill +0.02 | 1 heroes |
| Unstoppable | 6,400 | -0.071 | -0.011 | +0.124 | Mo & Krill +0.22, Haze +0.18, Grey Talon +0.16 | 3 heroes |
| Metal Skin | 3,200 | -0.198 | -0.062 | +0.084 | Wraith +0.20, Haze +0.12, Lash +0.07 | 0 heroes |
| Return Fire | 1,600 | -0.195 | -0.122 | +0.057 | Haze +0.12, Paradox +0.06, Vindicta +0.05 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Dispel Magic +0.11 (+0.16), Spellbreaker +0.09 (+0.28), Healbane +0.08 (+0.14)
- **Seven**: Witchmail +0.10 (+0.27), Spirit Resilience +0.07 (+0.21), Healbane +0.01 (+0.08)
- **Vindicta**: Bullet Resilience +0.11 (+0.17), Divine Barrier +0.08 (+0.16), Plated Armor +0.08 (+0.17)
- **Lady Geist**: Spirit Resilience +0.07 (+0.21), Divine Barrier +0.04 (+0.13), Witchmail +0.04 (+0.21)
- **Abrams**: Unstoppable +0.07 (+0.19), Dispel Magic +0.05 (+0.10), Reactive Barrier +0.04 (+0.05)
- **Wraith**: Indomitable +0.21 (+0.31), Metal Skin +0.20 (+0.28), Spellbreaker +0.18 (+0.36)
- **McGinnis**: Spirit Resilience +0.01 (+0.15), Counterspell -0.01 (+0.03), Return Fire -0.01 (+0.04)
- **Paradox**: Dispel Magic +0.06 (+0.11), Return Fire +0.06 (+0.11), Witchmail +0.05 (+0.22)
- **Dynamo**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.02 (-0.00)
- **Kelvin**: Healbane +0.02 (+0.09), Spirit Resilience +0.02 (+0.16), Counterspell +0.01 (+0.04)
- **Haze**: Indomitable +0.22 (+0.32), Unstoppable +0.18 (+0.30), Plated Armor +0.13 (+0.22)
- **Holliday**: Plated Armor +0.20 (+0.30), Spellbreaker +0.18 (+0.36), Debuff Reducer +0.17 (+0.24)
- **Bebop**: Debuff Reducer +0.17 (+0.24), Unstoppable +0.14 (+0.27), Spellbreaker +0.12 (+0.30)
- **Calico**: Spirit Resilience +0.13 (+0.27), Divine Barrier +0.05 (+0.13), Dispel Magic +0.03 (+0.08)
- **Grey Talon**: Unstoppable +0.16 (+0.28), Debuff Reducer +0.14 (+0.21), Spellbreaker +0.12 (+0.30)
- **Mo & Krill**: Unstoppable +0.22 (+0.34), Spellbreaker +0.09 (+0.28), Healbane +0.08 (+0.14)
- **Shiv**: Bullet Resilience +0.05 (+0.11), Divine Barrier +0.01 (+0.10), Plated Armor +0.01 (+0.11)
- **Ivy**: Indomitable +0.06 (+0.16), Unstoppable +0.02 (+0.15), Metal Skin +0.02 (+0.10)
- **Warden**: Debuff Reducer +0.00 (+0.08), Return Fire +0.00 (+0.06), Counterspell -0.01 (+0.03)
- **Yamato**: Healbane +0.05 (+0.11), Debuff Reducer +0.03 (+0.10), Witchmail +0.03 (+0.20)
- **Lash**: Spellbreaker +0.39 (+0.57), Spirit Resilience +0.37 (+0.51), Witchmail +0.17 (+0.34)
- **Viscous**: Spirit Resilience +0.19 (+0.33), Spellbreaker +0.08 (+0.26), Divine Barrier +0.06 (+0.14)
- **Pocket**: Spirit Resilience +0.05 (+0.19), Witchmail +0.01 (+0.18), Counterspell -0.01 (+0.02)
- **Mirage**: Dispel Magic +0.25 (+0.30), Spirit Resilience +0.02 (+0.16), Metal Skin +0.01 (+0.09)
- **Vyper**: Spellbreaker +0.09 (+0.27), Reactive Barrier +0.07 (+0.09), Debuff Reducer +0.06 (+0.13)
- **Sinclair**: Indomitable +0.16 (+0.27), Unstoppable +0.08 (+0.21), Debuff Reducer +0.03 (+0.10)
- **Mina**: Divine Barrier +0.09 (+0.17), Witchmail +0.07 (+0.24), Spirit Resilience +0.07 (+0.21)
- **Drifter**: Healbane +0.01 (+0.07), Counterspell -0.01 (+0.03), Reactive Barrier -0.01 (+0.00)
- **Venator**: Bullet Resilience +0.21 (+0.27), Plated Armor +0.06 (+0.16), Unstoppable +0.04 (+0.17)
- **Victor**: Spellbreaker +0.05 (+0.23), Healbane +0.04 (+0.10), Spirit Resilience +0.02 (+0.16)
- **Paige**: Counterspell +0.01 (+0.04), Divine Barrier +0.00 (+0.08), Reactive Barrier -0.01 (+0.01)
- **The Doorman**: Indomitable +0.17 (+0.27), Witchmail +0.12 (+0.29), Spirit Resilience +0.07 (+0.21)
- **Billy**: Reactive Barrier +0.02 (+0.04), Healbane +0.01 (+0.07), Counterspell +0.01 (+0.04)
- **Graves**: Return Fire +0.03 (+0.09), Reactive Barrier +0.03 (+0.04), Counterspell +0.01 (+0.04)
- **Apollo**: Healbane +0.02 (+0.08), Counterspell -0.00 (+0.03), Reactive Barrier -0.01 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.25 (+0.39), Witchmail +0.18 (+0.35), Reactive Barrier +0.12 (+0.14)
- **Rem**: Debuff Reducer +0.10 (+0.17), Unstoppable +0.07 (+0.20), Spellbreaker +0.01 (+0.19)
- **Silver**: Dispel Magic +0.06 (+0.12), Reactive Barrier +0.05 (+0.07), Bullet Resilience +0.02 (+0.08)
- **Celeste**: Witchmail +0.09 (+0.26), Spirit Resilience +0.07 (+0.21), Healbane +0.05 (+0.12)
- **Rat King**: Return Fire +0.00 (+0.06), Bullet Resilience -0.01 (+0.06), Counterspell -0.01 (+0.03)
- **Solomon**: Reactive Barrier +0.01 (+0.03), Return Fire +0.00 (+0.06), Spirit Resilience -0.02 (+0.12)
- **Violet**: Witchmail +0.12 (+0.29), Divine Barrier +0.06 (+0.15), Unstoppable +0.03 (+0.15)
- **Nurse Harrow**: Spirit Resilience +0.05 (+0.19), Witchmail +0.04 (+0.21), Divine Barrier +0.04 (+0.12)
- **Baba**: Healbane -0.00 (+0.06), Reactive Barrier -0.01 (+0.01), Counterspell -0.01 (+0.02)

## 50,000 souls

| Item | Cost | Gain | Per 1k souls | Sim mean | Best vs (lift) | Already in popular build |
|---|---|---|---|---|---|---|
| Spirit Resilience | 3,200 | +0.164 | +0.051 | +0.145 | Lash +0.39, Viscous +0.39, Deadman Danny +0.37 | 16 heroes |
| Dispel Magic | 3,200 | +0.089 | +0.028 | +0.059 | Mirage +0.33, Lash +0.19, Paradox +0.15 | 10 heroes |
| Indomitable | 6,400 | +0.169 | +0.027 | +0.130 | Wraith +0.39, The Doorman +0.27, Sinclair +0.21 | 2 heroes |
| Spellbreaker | 6,400 | +0.162 | +0.025 | +0.201 | Deadman Danny +0.31, Holliday +0.26, Viscous +0.22 | 0 heroes |
| Divine Barrier | 6,400 | +0.143 | +0.022 | +0.078 | Viscous +0.24, Lash +0.14, The Doorman +0.10 | 2 heroes |
| Healbane | 1,600 | +0.028 | +0.018 | +0.063 | Lady Geist +0.11, Celeste +0.09, Yamato +0.07 | 22 heroes |
| Witchmail | 6,400 | +0.104 | +0.016 | +0.177 | Deadman Danny +0.31, The Doorman +0.24, Lash +0.19 | 1 heroes |
| Debuff Reducer | 1,600 | +0.009 | +0.005 | +0.092 | Holliday +0.24, Paige +0.21, Grey Talon +0.16 | 0 heroes |
| Bullet Resilience | 3,200 | +0.012 | +0.004 | +0.061 | Vindicta +0.14, Viscous +0.11, Paradox +0.10 | 1 heroes |
| Plated Armor | 6,400 | +0.006 | +0.001 | +0.104 | Haze +0.12, Vindicta +0.12, Viscous +0.10 | 4 heroes |
| Unstoppable | 6,400 | -0.061 | -0.009 | +0.158 | Paige +0.28, Holliday +0.22, Ivy +0.18 | 5 heroes |
| Counterspell | 3,200 | -0.039 | -0.012 | +0.030 | Viscous +0.10, Lash +0.06, Celeste +0.06 | 1 heroes |
| Reactive Barrier | 1,600 | -0.025 | -0.015 | +0.019 | Deadman Danny +0.07, Vyper +0.07, Celeste +0.06 | 2 heroes |
| Metal Skin | 3,200 | -0.197 | -0.061 | +0.089 | Wraith +0.19, Viscous +0.16, Paradox +0.15 | 0 heroes |
| Return Fire | 1,600 | -0.190 | -0.119 | +0.053 | Viscous +0.11, Vindicta +0.11, Paradox +0.11 | 0 heroes |

Best counter per enemy hero (highest lift; matchup change in brackets):

- **Infernus**: Unstoppable +0.15 (+0.31), Spellbreaker +0.11 (+0.31), Dispel Magic +0.09 (+0.15)
- **Seven**: Witchmail +0.06 (+0.23), Healbane +0.00 (+0.07), Reactive Barrier +0.00 (+0.02)
- **Vindicta**: Bullet Resilience +0.14 (+0.20), Plated Armor +0.12 (+0.22), Return Fire +0.11 (+0.16)
- **Lady Geist**: Healbane +0.11 (+0.18), Spirit Resilience +0.08 (+0.23), Witchmail +0.08 (+0.25)
- **Abrams**: Dispel Magic +0.04 (+0.10), Reactive Barrier +0.03 (+0.05), Debuff Reducer +0.02 (+0.11)
- **Wraith**: Indomitable +0.39 (+0.52), Spellbreaker +0.20 (+0.40), Metal Skin +0.19 (+0.28)
- **McGinnis**: Spirit Resilience +0.01 (+0.16), Dispel Magic -0.01 (+0.05), Counterspell -0.01 (+0.02)
- **Paradox**: Unstoppable +0.17 (+0.33), Metal Skin +0.15 (+0.24), Dispel Magic +0.15 (+0.21)
- **Dynamo**: Healbane -0.01 (+0.06), Counterspell -0.01 (+0.02), Reactive Barrier -0.02 (+0.00)
- **Kelvin**: Spirit Resilience +0.02 (+0.17), Healbane +0.01 (+0.07), Reactive Barrier -0.01 (+0.01)
- **Haze**: Unstoppable +0.17 (+0.33), Plated Armor +0.12 (+0.23), Bullet Resilience +0.09 (+0.15)
- **Holliday**: Spellbreaker +0.26 (+0.46), Debuff Reducer +0.24 (+0.34), Unstoppable +0.22 (+0.37)
- **Bebop**: Debuff Reducer +0.15 (+0.25), Unstoppable +0.11 (+0.27), Spellbreaker +0.08 (+0.28)
- **Calico**: Spirit Resilience +0.04 (+0.19), Divine Barrier -0.01 (+0.07), Reactive Barrier -0.01 (+0.01)
- **Grey Talon**: Spellbreaker +0.22 (+0.42), Spirit Resilience +0.20 (+0.34), Unstoppable +0.17 (+0.32)
- **Mo & Krill**: Spellbreaker +0.12 (+0.32), Indomitable +0.09 (+0.22), Unstoppable +0.08 (+0.24)
- **Shiv**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.06 (+0.15), Plated Armor +0.04 (+0.14)
- **Ivy**: Unstoppable +0.18 (+0.34), Indomitable +0.16 (+0.29), Debuff Reducer +0.09 (+0.18)
- **Warden**: Divine Barrier +0.02 (+0.10), Return Fire +0.02 (+0.07), Witchmail +0.01 (+0.18)
- **Yamato**: Healbane +0.07 (+0.13), Counterspell +0.01 (+0.04), Reactive Barrier -0.00 (+0.02)
- **Lash**: Spirit Resilience +0.39 (+0.53), Witchmail +0.19 (+0.37), Spellbreaker +0.19 (+0.39)
- **Viscous**: Spirit Resilience +0.39 (+0.53), Divine Barrier +0.24 (+0.32), Spellbreaker +0.22 (+0.43)
- **Pocket**: Spirit Resilience +0.01 (+0.16), Return Fire -0.00 (+0.05), Counterspell -0.01 (+0.03)
- **Mirage**: Dispel Magic +0.33 (+0.39), Unstoppable +0.16 (+0.31), Metal Skin +0.09 (+0.18)
- **Vyper**: Plated Armor +0.10 (+0.20), Reactive Barrier +0.07 (+0.09), Bullet Resilience +0.06 (+0.13)
- **Sinclair**: Indomitable +0.21 (+0.34), Debuff Reducer +0.06 (+0.15), Spellbreaker +0.04 (+0.24)
- **Mina**: Divine Barrier +0.01 (+0.09), Counterspell +0.00 (+0.04), Return Fire -0.01 (+0.05)
- **Drifter**: Dispel Magic +0.09 (+0.15), Reactive Barrier +0.01 (+0.03), Return Fire -0.00 (+0.05)
- **Venator**: Bullet Resilience +0.07 (+0.13), Metal Skin +0.03 (+0.12), Reactive Barrier -0.01 (+0.01)
- **Victor**: Spellbreaker +0.10 (+0.30), Spirit Resilience +0.06 (+0.20), Healbane +0.06 (+0.12)
- **Paige**: Unstoppable +0.28 (+0.44), Debuff Reducer +0.21 (+0.30), Spellbreaker +0.11 (+0.31)
- **The Doorman**: Spirit Resilience +0.33 (+0.48), Indomitable +0.27 (+0.40), Witchmail +0.24 (+0.42)
- **Billy**: Reactive Barrier +0.02 (+0.04), Healbane +0.01 (+0.07), Counterspell -0.01 (+0.02)
- **Graves**: Reactive Barrier +0.04 (+0.06), Return Fire +0.03 (+0.08), Metal Skin +0.01 (+0.10)
- **Apollo**: Healbane +0.02 (+0.08), Counterspell -0.01 (+0.02), Reactive Barrier -0.01 (+0.01)
- **Deadman Danny**: Spirit Resilience +0.37 (+0.51), Witchmail +0.31 (+0.49), Spellbreaker +0.31 (+0.51)
- **Rem**: Spirit Resilience +0.09 (+0.23), Divine Barrier +0.09 (+0.17), Witchmail +0.03 (+0.20)
- **Silver**: Dispel Magic +0.12 (+0.18), Metal Skin +0.11 (+0.20), Bullet Resilience +0.05 (+0.11)
- **Celeste**: Witchmail +0.16 (+0.33), Spirit Resilience +0.14 (+0.29), Healbane +0.09 (+0.15)
- **Rat King**: Healbane -0.01 (+0.06), Counterspell -0.01 (+0.02), Metal Skin -0.01 (+0.08)
- **Solomon**: Return Fire +0.01 (+0.06), Reactive Barrier +0.00 (+0.02), Counterspell -0.00 (+0.03)
- **Violet**: Witchmail +0.08 (+0.26), Spirit Resilience +0.05 (+0.19), Dispel Magic +0.04 (+0.10)
- **Nurse Harrow**: Spirit Resilience +0.18 (+0.33), Healbane +0.05 (+0.11), Witchmail +0.04 (+0.22)
- **Baba**: Counterspell +0.01 (+0.04), Healbane +0.01 (+0.07), Reactive Barrier -0.00 (+0.01)
