# Sim vs real damage mix audit

Sample: 600 matches, 5623 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides.

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.23 | 0.29 / 0.46 | 0.16 / 0.09 | 0.29 / 0.22 | 0.17 |
| The Doorman | 2 | 0.20 / 0.14 | 0.57 / 0.70 | 0.22 / 0.13 | 0.01 / 0.04 | 0.15 |
| Paradox | 168 | 0.24 / 0.33 | 0.48 / 0.51 | 0.23 / 0.11 | 0.03 / 0.04 | 0.14 |
| Viscous | 29 | 0.13 / 0.18 | 0.51 / 0.56 | 0.28 / 0.16 | 0.05 / 0.07 | 0.12 |
| Mo & Krill | 176 | 0.07 / 0.09 | 0.47 / 0.58 | 0.39 / 0.29 | 0.05 / 0.04 | 0.12 |
| Shiv | 209 | 0.27 / 0.33 | 0.48 / 0.53 | 0.16 / 0.06 | 0.08 / 0.08 | 0.11 |
| Kelvin | 12 | 0.09 / 0.16 | 0.65 / 0.68 | 0.22 / 0.14 | 0.02 / 0.02 | 0.11 |
| Deadman Danny | 357 | 0.16 / 0.19 | 0.63 / 0.70 | 0.18 / 0.09 | 0.01 / 0.01 | 0.10 |
| Vyper | 78 | 0.46 / 0.55 | 0.26 / 0.26 | 0.25 / 0.17 | 0.02 / 0.02 | 0.09 |
| Paige | 58 | 0.35 / 0.40 | 0.50 / 0.55 | 0.11 / 0.03 | 0.03 / 0.02 | 0.09 |
| Warden | 33 | 0.52 / 0.45 | 0.31 / 0.38 | 0.11 / 0.13 | 0.03 / 0.02 | 0.09 |
| Graves | 151 | 0.20 / 0.20 | 0.50 / 0.45 | 0.27 / 0.34 | 0.02 / 0.00 | 0.08 |
| Nurse Harrow | 347 | 0.29 / 0.35 | 0.61 / 0.54 | 0.06 / 0.06 | 0.03 / 0.04 | 0.08 |
| McGinnis | 49 | 0.20 / 0.19 | 0.64 / 0.71 | 0.12 / 0.08 | 0.02 / 0.01 | 0.07 |
| Seven | 95 | 0.20 / 0.22 | 0.66 / 0.71 | 0.10 / 0.05 | 0.02 / 0.02 | 0.06 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.56 | 0.12 / 0.06 | 0.02 / 0.02 | 0.06 |
| Rem | 23 | 0.25 / 0.29 | 0.54 / 0.55 | 0.16 / 0.10 | 0.04 / 0.05 | 0.06 |
| Bebop | 254 | 0.18 / 0.16 | 0.56 / 0.62 | 0.19 / 0.17 | 0.05 / 0.03 | 0.06 |
| Celeste | 77 | 0.16 / 0.19 | 0.61 / 0.63 | 0.17 / 0.12 | 0.04 / 0.05 | 0.06 |
| Mirage | 45 | 0.31 / 0.35 | 0.48 / 0.44 | 0.17 / 0.17 | 0.02 / 0.03 | 0.06 |
| Holliday | 73 | 0.27 / 0.30 | 0.54 / 0.55 | 0.13 / 0.09 | 0.05 / 0.06 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.54 | 0.07 / 0.04 | 0.01 / 0.02 | 0.05 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.60 | 0.25 / 0.22 | 0.03 / 0.03 | 0.04 |
| Sinclair | 20 | 0.17 / 0.19 | 0.76 / 0.73 | 0.02 / 0.02 | 0.03 / 0.05 | 0.04 |
| Drifter | 186 | 0.26 / 0.27 | 0.44 / 0.46 | 0.17 / 0.14 | 0.11 / 0.12 | 0.04 |
| Victor | 129 | 0.15 / 0.18 | 0.64 / 0.64 | 0.16 / 0.13 | 0.03 / 0.04 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.53 | 0.16 / 0.15 | 0.01 / 0.01 | 0.04 |
| Abrams | 138 | 0.23 / 0.25 | 0.20 / 0.21 | 0.13 / 0.12 | 0.42 / 0.41 | 0.03 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.65 | 0.16 / 0.19 | 0.02 / 0.02 | 0.03 |
| Infernus | 173 | 0.23 / 0.25 | 0.60 / 0.61 | 0.13 / 0.12 | 0.03 / 0.02 | 0.03 |
| Venator | 257 | 0.48 / 0.51 | 0.40 / 0.40 | 0.03 / 0.01 | 0.07 / 0.08 | 0.03 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.40 | 0.14 / 0.15 | 0.22 / 0.25 | 0.03 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.32 | 0.15 / 0.14 | 0.03 |
| Silver | 100 | 0.41 / 0.44 | 0.37 / 0.37 | 0.10 / 0.09 | 0.10 / 0.10 | 0.03 |
| Lady Geist | 37 | 0.29 / 0.31 | 0.62 / 0.63 | 0.05 / 0.03 | 0.03 / 0.03 | 0.03 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.40 | 0.17 / 0.17 | 0.18 / 0.18 | 0.03 |
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
| Kelvin | Arctic Beam | ability | 0.397 | 0.382 | 1.94 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.171 | 0.31 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.099 | 0.17 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.258 | 0.51 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.293 | 1.58 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.294 | 1.49 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.241 | 1.49 |
| Vyper | Split Shot | item | 0.110 | 0.049 | 2.70 |
| Apollo | Flawless Advance | ability | 0.141 | 0.218 | 0.61 |
| The Doorman | Tankbuster | item | 0.165 | 0.062 | 1.92 |
| The Doorman | Call Bell | ability | 0.475 | 0.425 | 0.80 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.042 | 2.86 |
| Rem | Tankbuster | item | 0.063 | 0.015 | 5.00 |
| Bebop | Hyper Beam | ability | 0.129 | 0.195 | 0.60 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.162 | 0.56 |
| Warden | Last Stand | ability | 0.138 | 0.193 | 0.62 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.320 | 0.79 |
| Paradox | Tankbuster | item | 0.074 | 0.037 | 2.73 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.295 | 1.27 |
| Seven | Power Surge | ability | 0.205 | 0.154 | 1.43 |
| Viscous | Goo Ball | ability | 0.107 | 0.075 | 1.94 |
| Seven | Storm Cloud | ability | 0.202 | 0.279 | 0.78 |
| Paradox | Mystic Reverb | item | 0.063 | 0.029 | 3.01 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.264 | 1.26 |
| Apollo | MELEE | melee | 0.287 | 0.216 | 1.24 |
| Holliday | Tankbuster | item | 0.060 | 0.024 | 2.76 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.298 | 1.21 |
| Deadman Danny | Tankbuster | item | 0.079 | 0.046 | 2.12 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1519 | 1.039 | 0.498 | 2.08 |
| Mystic Burst | 1461 | 0.284 | 0.177 | 1.60 |
| Quicksilver Reload | 1105 | 0.171 | 0.155 | 1.11 |
| Toxic Bullets | 861 | 0.533 | 0.464 | 1.15 |
| Stalker | 790 | 0.219 | 0.218 | 1.00 |
| Spirit Snatch | 709 | 0.367 | 0.306 | 1.20 |
| Ricochet | 695 | 0.156 | 0.000 | - |
| Spirit Burn | 574 | 0.770 | 0.608 | 1.27 |
| Torment Pulse | 569 | 1.358 | 1.091 | 1.25 |
| Spirit Strike | 561 | 0.233 | 0.218 | 1.07 |
| Express Shot | 552 | 0.677 | 0.000 | - |
| Siphon Bullets | 521 | 0.248 | 0.252 | 0.98 |
| Escalating Exposure | 520 | 0.875 | 0.000 | - |
| Tesla Bullets | 509 | 0.480 | 0.497 | 0.96 |
| Cold Front | 505 | 0.447 | 0.385 | 1.16 |
| Mystic Shot | 495 | 0.385 | 0.400 | 0.96 |
| Headhunter | 407 | 0.440 | 0.439 | 1.00 |
| Melee Charge | 379 | 0.240 | 0.104 | 2.30 |
| Capacitor | 375 | 0.696 | 0.744 | 0.94 |
| Headshot Booster | 370 | 0.215 | 0.182 | 1.18 |
| Mercurial Magnum | 339 | 0.295 | 0.294 | 1.01 |
| Rebuttal | 210 | 0.063 | 0.040 | 1.56 |
| Mystic Reverb | 204 | 1.313 | 0.717 | 1.83 |
| Lucky Shot | 200 | 0.397 | 0.197 | 2.01 |
| Arctic Blast | 171 | 1.325 | 0.714 | 1.85 |
| Split Shot | 170 | 0.257 | 0.199 | 1.29 |
| Crushing Fists | 143 | 0.303 | 0.094 | 3.24 |
| Phantom Strike | 123 | 0.311 | 0.209 | 1.49 |
| Decay | 107 | 1.538 | 1.266 | 1.21 |
| Scourge | 105 | 2.027 | 1.939 | 1.04 |
| Return Fire | 92 | 0.439 | 0.116 | 3.79 |
| Alchemical Fire | 68 | 0.874 | 0.542 | 1.61 |
| Focus Lens | 36 | 0.957 | 0.828 | 1.16 |
| Lightning Scroll | 35 | 0.373 | 0.336 | 1.11 |
| Silence Wave | 26 | 0.209 | 0.296 | 0.70 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Yamato | Crushing Fists | 30 | 0.299 | 0.027 | 10.94 |
| Celeste | Tankbuster | 29 | 1.268 | 0.187 | 6.79 |
| Drifter | Crushing Fists | 25 | 0.287 | 0.055 | 5.23 |
| Yamato | Melee Charge | 57 | 0.207 | 0.043 | 4.84 |
| Rat King | Return Fire | 41 | 0.389 | 0.086 | 4.54 |
| Solomon | Tankbuster | 26 | 0.578 | 0.132 | 4.39 |
| Vindicta | Mystic Burst | 25 | 0.107 | 0.026 | 4.09 |
| Drifter | Melee Charge | 68 | 0.211 | 0.054 | 3.86 |
| Deadman Danny | Toxic Bullets | 144 | 0.871 | 0.237 | 3.67 |
| Paradox | Mystic Reverb | 86 | 1.290 | 0.356 | 3.62 |
| Paradox | Tankbuster | 146 | 0.656 | 0.182 | 3.61 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.154 | 3.59 |
| Holliday | Tankbuster | 48 | 0.959 | 0.273 | 3.52 |
| Calico | Melee Charge | 27 | 0.170 | 0.050 | 3.38 |
| Bebop | Spirit Snatch | 191 | 0.342 | 0.120 | 2.85 |
| Vyper | Split Shot | 69 | 0.321 | 0.116 | 2.76 |
| Viscous | Mystic Burst | 20 | 0.425 | 0.158 | 2.69 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.129 | 2.65 |
| Deadman Danny | Tankbuster | 310 | 1.204 | 0.465 | 2.59 |
| Mo & Krill | Tankbuster | 118 | 3.292 | 1.289 | 2.55 |
| Mo & Krill | Quicksilver Reload | 150 | 0.843 | 0.331 | 2.55 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.157 | 2.54 |
| Bebop | Spirit Strike | 186 | 0.274 | 0.110 | 2.48 |
| Calico | Mystic Shot | 30 | 0.381 | 0.939 | 0.41 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.072 | 2.43 |
| Celeste | Mystic Burst | 34 | 0.251 | 0.107 | 2.35 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.213 | 2.33 |
| Deadman Danny | Mystic Burst | 207 | 0.278 | 0.119 | 2.32 |
| Haze | Lucky Shot | 91 | 0.492 | 0.214 | 2.30 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.161 | 2.23 |
| Holliday | Mystic Burst | 33 | 0.200 | 0.090 | 2.22 |
| Warden | Quicksilver Reload | 25 | 0.077 | 0.171 | 0.45 |
| Vyper | Mercurial Magnum | 58 | 0.288 | 0.134 | 2.14 |
| Billy | Crushing Fists | 31 | 0.319 | 0.150 | 2.13 |
| Vyper | Quicksilver Reload | 31 | 0.057 | 0.121 | 0.47 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.668 | 2.06 |
| Venator | Siphon Bullets | 77 | 0.200 | 0.103 | 1.94 |
| Shiv | Spirit Strike | 38 | 0.172 | 0.333 | 0.52 |
| Billy | Melee Charge | 48 | 0.242 | 0.125 | 1.94 |
| Mo & Krill | Arctic Blast | 25 | 3.043 | 1.581 | 1.93 |
