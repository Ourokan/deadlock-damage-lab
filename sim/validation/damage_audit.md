# Sim vs real damage mix audit

Sample: 600 matches, 5623 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides.

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.23 | 0.29 / 0.46 | 0.16 / 0.09 | 0.29 / 0.22 | 0.17 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.39 | 0.27 / 0.43 | 0.02 / 0.00 | 0.16 |
| Paradox | 168 | 0.24 / 0.34 | 0.48 / 0.52 | 0.23 / 0.10 | 0.03 / 0.04 | 0.14 |
| The Doorman | 2 | 0.20 / 0.14 | 0.57 / 0.69 | 0.22 / 0.13 | 0.01 / 0.04 | 0.14 |
| Viscous | 29 | 0.13 / 0.18 | 0.51 / 0.57 | 0.28 / 0.16 | 0.05 / 0.07 | 0.13 |
| Mo & Krill | 176 | 0.07 / 0.09 | 0.47 / 0.58 | 0.39 / 0.29 | 0.05 / 0.04 | 0.12 |
| Shiv | 209 | 0.27 / 0.33 | 0.48 / 0.53 | 0.16 / 0.05 | 0.08 / 0.08 | 0.12 |
| Kelvin | 12 | 0.09 / 0.16 | 0.65 / 0.68 | 0.22 / 0.13 | 0.02 / 0.02 | 0.12 |
| Deadman Danny | 357 | 0.16 / 0.20 | 0.63 / 0.71 | 0.18 / 0.08 | 0.01 / 0.01 | 0.12 |
| Vyper | 78 | 0.46 / 0.55 | 0.26 / 0.26 | 0.25 / 0.17 | 0.02 / 0.02 | 0.09 |
| Paige | 58 | 0.35 / 0.40 | 0.50 / 0.55 | 0.11 / 0.03 | 0.03 / 0.02 | 0.09 |
| Warden | 33 | 0.52 / 0.45 | 0.31 / 0.38 | 0.11 / 0.13 | 0.03 / 0.02 | 0.09 |
| Nurse Harrow | 347 | 0.29 / 0.35 | 0.61 / 0.54 | 0.06 / 0.06 | 0.03 / 0.04 | 0.08 |
| McGinnis | 49 | 0.20 / 0.19 | 0.64 / 0.72 | 0.12 / 0.08 | 0.02 / 0.01 | 0.07 |
| Bebop | 254 | 0.18 / 0.17 | 0.56 / 0.63 | 0.19 / 0.17 | 0.05 / 0.03 | 0.07 |
| Rem | 23 | 0.25 / 0.29 | 0.54 / 0.55 | 0.16 / 0.10 | 0.04 / 0.05 | 0.06 |
| Seven | 95 | 0.20 / 0.22 | 0.66 / 0.71 | 0.10 / 0.05 | 0.02 / 0.02 | 0.06 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.56 | 0.12 / 0.06 | 0.02 / 0.02 | 0.06 |
| Celeste | 77 | 0.16 / 0.19 | 0.61 / 0.63 | 0.17 / 0.12 | 0.04 / 0.05 | 0.06 |
| Mirage | 45 | 0.31 / 0.35 | 0.48 / 0.44 | 0.17 / 0.17 | 0.02 / 0.03 | 0.06 |
| Holliday | 73 | 0.27 / 0.30 | 0.54 / 0.56 | 0.13 / 0.09 | 0.05 / 0.06 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.54 | 0.07 / 0.04 | 0.01 / 0.02 | 0.05 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.60 | 0.25 / 0.21 | 0.03 / 0.03 | 0.05 |
| Sinclair | 20 | 0.17 / 0.19 | 0.76 / 0.73 | 0.02 / 0.02 | 0.03 / 0.05 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.54 | 0.16 / 0.14 | 0.01 / 0.01 | 0.04 |
| Drifter | 186 | 0.26 / 0.27 | 0.44 / 0.46 | 0.17 / 0.14 | 0.11 / 0.12 | 0.04 |
| Victor | 129 | 0.15 / 0.18 | 0.64 / 0.63 | 0.16 / 0.13 | 0.03 / 0.04 | 0.04 |
| Abrams | 138 | 0.23 / 0.25 | 0.20 / 0.21 | 0.13 / 0.12 | 0.42 / 0.41 | 0.03 |
| Infernus | 173 | 0.23 / 0.25 | 0.60 / 0.61 | 0.13 / 0.12 | 0.03 / 0.02 | 0.03 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.65 | 0.16 / 0.19 | 0.02 / 0.02 | 0.03 |
| Venator | 257 | 0.48 / 0.51 | 0.40 / 0.40 | 0.03 / 0.01 | 0.07 / 0.08 | 0.03 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.40 | 0.14 / 0.15 | 0.22 / 0.25 | 0.03 |
| Lady Geist | 37 | 0.29 / 0.31 | 0.62 / 0.63 | 0.05 / 0.03 | 0.03 / 0.03 | 0.03 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.32 | 0.15 / 0.14 | 0.03 |
| Silver | 100 | 0.41 / 0.44 | 0.37 / 0.37 | 0.10 / 0.09 | 0.10 / 0.10 | 0.03 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.40 | 0.17 / 0.17 | 0.18 / 0.18 | 0.02 |
| Dynamo | 53 | 0.23 / 0.23 | 0.62 / 0.64 | 0.08 / 0.08 | 0.05 / 0.04 | 0.02 |
| Vindicta | 131 | 0.44 / 0.44 | 0.49 / 0.50 | 0.05 / 0.04 | 0.01 / 0.01 | 0.02 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.35 | 0.26 / 0.27 | 0.04 / 0.04 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.56 | 0.03 / 0.03 | 0.05 / 0.06 | 0.01 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.42 | 0.24 / 0.24 | 0.01 / 0.01 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.19 | 0.01 / 0.01 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Shiv | Express Shot | item | 0.086 | 0.000 | - |
| Kelvin | Escalating Exposure | item | 0.068 | 0.000 | - |
| Paige | Express Shot | item | 0.066 | 0.000 | - |
| Victor | Escalating Exposure | item | 0.065 | 0.000 | - |
| Seven | Escalating Exposure | item | 0.065 | 0.000 | - |
| McGinnis | Escalating Exposure | item | 0.055 | 0.000 | - |
| Viscous | Express Shot | item | 0.052 | 0.000 | - |
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| Deadman Danny | Express Shot | item | 0.044 | 0.000 | - |
| Infernus | Escalating Exposure | item | 0.032 | 0.000 | - |
| Yamato | Express Shot | item | 0.031 | 0.000 | - |
| Kelvin | Arctic Beam | ability | 0.397 | 0.392 | 1.87 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.163 | 0.33 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.100 | 0.17 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.258 | 0.51 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.292 | 1.57 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.297 | 1.49 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.241 | 1.50 |
| Vyper | Split Shot | item | 0.110 | 0.048 | 2.70 |
| Apollo | Flawless Advance | ability | 0.141 | 0.218 | 0.61 |
| The Doorman | Tankbuster | item | 0.165 | 0.062 | 1.92 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.041 | 2.96 |
| The Doorman | Call Bell | ability | 0.475 | 0.429 | 0.80 |
| Rem | Tankbuster | item | 0.063 | 0.015 | 5.00 |
| Bebop | Hyper Beam | ability | 0.129 | 0.196 | 0.60 |
| Paradox | Mystic Reverb | item | 0.063 | 0.018 | 4.70 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.162 | 0.56 |
| Warden | Last Stand | ability | 0.138 | 0.193 | 0.62 |
| Graves | Tesla Bullets | item | 0.052 | 0.102 | 0.46 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.322 | 0.79 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.295 | 1.27 |
| Paradox | Tankbuster | item | 0.074 | 0.038 | 2.73 |
| Seven | Power Surge | ability | 0.205 | 0.154 | 1.43 |
| Viscous | Goo Ball | ability | 0.107 | 0.075 | 1.94 |
| Seven | Storm Cloud | ability | 0.202 | 0.279 | 0.78 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.263 | 1.26 |
| Graves | Capacitor | item | 0.055 | 0.098 | 0.51 |
| Apollo | MELEE | melee | 0.287 | 0.216 | 1.24 |
| Graves | Mystic Shot | item | 0.033 | 0.072 | 0.42 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1519 | 1.039 | 0.497 | 2.09 |
| Mystic Burst | 1461 | 0.284 | 0.177 | 1.60 |
| Quicksilver Reload | 1105 | 0.171 | 0.155 | 1.11 |
| Toxic Bullets | 861 | 0.533 | 0.416 | 1.28 |
| Stalker | 790 | 0.219 | 0.218 | 1.00 |
| Spirit Snatch | 709 | 0.367 | 0.306 | 1.20 |
| Ricochet | 695 | 0.156 | 0.000 | - |
| Spirit Burn | 574 | 0.770 | 0.611 | 1.26 |
| Torment Pulse | 569 | 1.358 | 1.169 | 1.16 |
| Spirit Strike | 561 | 0.233 | 0.218 | 1.07 |
| Express Shot | 552 | 0.677 | 0.000 | - |
| Siphon Bullets | 521 | 0.248 | 0.256 | 0.97 |
| Escalating Exposure | 520 | 0.875 | 0.000 | - |
| Tesla Bullets | 509 | 0.480 | 0.531 | 0.90 |
| Cold Front | 505 | 0.447 | 0.384 | 1.16 |
| Mystic Shot | 495 | 0.385 | 0.420 | 0.92 |
| Headhunter | 407 | 0.440 | 0.440 | 1.00 |
| Melee Charge | 379 | 0.240 | 0.104 | 2.30 |
| Capacitor | 375 | 0.696 | 0.783 | 0.89 |
| Headshot Booster | 370 | 0.215 | 0.182 | 1.19 |
| Mercurial Magnum | 339 | 0.295 | 0.294 | 1.00 |
| Rebuttal | 210 | 0.063 | 0.041 | 1.51 |
| Mystic Reverb | 204 | 1.313 | 0.345 | 3.80 |
| Lucky Shot | 200 | 0.397 | 0.197 | 2.01 |
| Arctic Blast | 171 | 1.325 | 0.713 | 1.86 |
| Split Shot | 170 | 0.257 | 0.193 | 1.33 |
| Crushing Fists | 143 | 0.303 | 0.093 | 3.26 |
| Phantom Strike | 123 | 0.311 | 0.208 | 1.49 |
| Decay | 107 | 1.538 | 1.278 | 1.20 |
| Scourge | 105 | 2.027 | 1.942 | 1.04 |
| Return Fire | 92 | 0.439 | 0.115 | 3.83 |
| Alchemical Fire | 68 | 0.874 | 0.542 | 1.61 |
| Focus Lens | 36 | 0.957 | 0.828 | 1.16 |
| Lightning Scroll | 35 | 0.373 | 0.349 | 1.07 |
| Silence Wave | 26 | 0.209 | 0.294 | 0.71 |
