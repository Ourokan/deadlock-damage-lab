# Sim vs real damage mix audit

Sample: 600 matches, 5773 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.21 | 0.29 / 0.45 | 0.16 / 0.12 | 0.29 / 0.22 | 0.16 |
| The Doorman | 2 | 0.20 / 0.14 | 0.57 / 0.50 | 0.22 / 0.33 | 0.01 / 0.02 | 0.12 |
| Mirage | 45 | 0.31 / 0.35 | 0.48 / 0.38 | 0.17 / 0.23 | 0.02 / 0.03 | 0.11 |
| Kelvin | 12 | 0.09 / 0.10 | 0.65 / 0.57 | 0.22 / 0.32 | 0.02 / 0.02 | 0.10 |
| Rem | 23 | 0.25 / 0.25 | 0.54 / 0.47 | 0.16 / 0.24 | 0.04 / 0.05 | 0.09 |
| Vyper | 78 | 0.46 / 0.52 | 0.26 / 0.20 | 0.25 / 0.27 | 0.02 / 0.01 | 0.08 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.33 | 0.17 / 0.21 | 0.18 / 0.22 | 0.08 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.60 | 0.25 / 0.20 | 0.12 / 0.11 | 0.08 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.22 | 0.04 / 0.04 | 0.07 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.71 | 0.12 / 0.11 | 0.02 / 0.00 | 0.07 |
| Paige | 58 | 0.35 / 0.39 | 0.50 / 0.45 | 0.11 / 0.13 | 0.03 / 0.02 | 0.07 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.43 | 0.23 / 0.24 | 0.03 / 0.05 | 0.07 |
| Warden | 33 | 0.52 / 0.48 | 0.31 / 0.36 | 0.11 / 0.13 | 0.03 / 0.02 | 0.06 |
| Victor | 129 | 0.15 / 0.17 | 0.64 / 0.58 | 0.16 / 0.20 | 0.03 / 0.03 | 0.06 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.50 | 0.28 / 0.25 | 0.05 / 0.09 | 0.06 |
| Seven | 95 | 0.20 / 0.24 | 0.66 / 0.62 | 0.10 / 0.12 | 0.02 / 0.02 | 0.06 |
| Violet | 4 | 0.29 / 0.25 | 0.65 / 0.69 | 0.02 / 0.04 | 0.01 / 0.01 | 0.06 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.46 | 0.05 / 0.05 | 0.01 / 0.01 | 0.05 |
| Infernus | 173 | 0.23 / 0.24 | 0.60 / 0.57 | 0.13 / 0.16 | 0.03 / 0.02 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.12 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.34 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.54 | 0.12 / 0.10 | 0.02 / 0.01 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.34 | 0.10 / 0.13 | 0.10 / 0.11 | 0.04 |
| Solomon | 42 | 0.37 / 0.39 | 0.54 / 0.51 | 0.07 / 0.08 | 0.01 / 0.02 | 0.04 |
| Holliday | 73 | 0.27 / 0.27 | 0.54 / 0.52 | 0.13 / 0.16 | 0.05 / 0.05 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Deadman Danny | 357 | 0.16 / 0.14 | 0.63 / 0.67 | 0.18 / 0.18 | 0.01 / 0.01 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.49 | 0.16 / 0.19 | 0.01 / 0.01 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.09 | 0.05 / 0.03 | 0.03 |
| Venator | 257 | 0.48 / 0.51 | 0.40 / 0.40 | 0.03 / 0.02 | 0.07 / 0.06 | 0.03 |
| Sinclair | 20 | 0.17 / 0.17 | 0.76 / 0.74 | 0.02 / 0.04 | 0.03 / 0.04 | 0.03 |
| Wraith | 283 | 0.32 / 0.32 | 0.41 / 0.40 | 0.24 / 0.27 | 0.01 / 0.01 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.67 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.23 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.07 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.20 | 0.13 / 0.13 | 0.42 / 0.42 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.29 | 0.62 / 0.63 | 0.05 / 0.05 | 0.03 / 0.02 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.19 | 0.01 / 0.01 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| The Doorman | Tankbuster | item | 0.165 | 0.283 | 0.43 |
| McGinnis | Mini Turret | ability | 0.467 | 0.574 | 0.67 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.197 | 1.69 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.13 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.270 | 0.65 |
| Apollo | Flawless Advance | ability | 0.141 | 0.209 | 0.57 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.164 | 0.50 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.307 | 0.71 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.030 | 2.80 |
| Kelvin | Arctic Beam | ability | 0.397 | 0.341 | 1.26 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.117 | 0.47 |
| Victor | Pain Battery | ability | 0.276 | 0.228 | 1.36 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.063 | 0.28 |
| Vindicta | Assassinate | ability | 0.162 | 0.112 | 1.62 |
| Sinclair | Audience Participation | ability | 0.194 | 0.270 | 0.76 |
| Vyper | Lethal Venom | ability | 0.112 | 0.064 | 1.96 |
| Rem | Tankbuster | item | 0.063 | 0.117 | 0.53 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.301 | 1.23 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.333 | 0.82 |
| Celeste | Shining Wonder | ability | 0.170 | 0.132 | 1.45 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.023 | 2.83 |
| Seven | Lightning Ball | ability | 0.198 | 0.172 | 1.35 |
| Paige | Bookwyrm | ability | 0.320 | 0.299 | 1.20 |
| Violet | Living Ink | ability | 0.277 | 0.296 | 0.82 |
| Infernus | Flame Dash | ability | 0.216 | 0.178 | 1.30 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.181 | 0.73 |
| Yamato | MELEE | melee | 0.184 | 0.224 | 0.79 |
| Pocket | Affliction | ability | 0.120 | 0.156 | 0.73 |
| Warden | Last Stand | ability | 0.138 | 0.171 | 0.75 |
| Viscous | Express Shot | item | 0.052 | 0.024 | 2.56 |
| Seven | Power Surge | ability | 0.205 | 0.192 | 1.26 |
| Solomon | Rook Battery | ability | 0.167 | 0.134 | 1.33 |
| Apollo | Itani Lo Sahn | ability | 0.056 | 0.082 | 0.57 |
| Rem | Decay | item | 0.026 | 0.056 | 0.46 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.228 | 1.18 |
| Kelvin | Tankbuster | item | 0.044 | 0.080 | 0.60 |
| Viscous | MELEE | melee | 0.047 | 0.086 | 0.63 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.091 | 1.42 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1522 | 1.039 | 0.835 | 1.25 |
| Mystic Burst | 1465 | 0.284 | 0.235 | 1.21 |
| Quicksilver Reload | 1105 | 0.171 | 0.141 | 1.22 |
| Toxic Bullets | 862 | 0.532 | 0.531 | 1.00 |
| Spirit Snatch | 793 | 0.400 | 0.401 | 1.00 |
| Stalker | 790 | 0.219 | 0.207 | 1.06 |
| Torment Pulse | 707 | 1.663 | 1.433 | 1.16 |
| Ricochet | 695 | 0.156 | 0.189 | 0.83 |
| Spirit Strike | 675 | 0.291 | 0.311 | 0.93 |
| Spirit Burn | 579 | 0.773 | 0.559 | 1.38 |
| Express Shot | 552 | 0.677 | 0.502 | 1.35 |
| Escalating Exposure | 542 | 0.892 | 0.883 | 1.01 |
| Siphon Bullets | 521 | 0.248 | 0.242 | 1.02 |
| Tesla Bullets | 509 | 0.480 | 0.481 | 1.00 |
| Cold Front | 505 | 0.447 | 0.416 | 1.07 |
| Mystic Shot | 497 | 0.385 | 0.359 | 1.07 |
| Headhunter | 407 | 0.440 | 0.437 | 1.01 |
| Melee Charge | 379 | 0.240 | 0.117 | 2.05 |
| Capacitor | 375 | 0.696 | 0.698 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.195 | 1.11 |
| Mercurial Magnum | 339 | 0.295 | 0.289 | 1.02 |
| Rebuttal | 212 | 0.063 | 0.048 | 1.31 |
| Mystic Reverb | 204 | 1.313 | 1.349 | 0.97 |
| Lucky Shot | 200 | 0.397 | 0.229 | 1.73 |
| Arctic Blast | 171 | 1.325 | 0.803 | 1.65 |
| Split Shot | 170 | 0.257 | 0.250 | 1.03 |
| Crushing Fists | 143 | 0.303 | 0.119 | 2.56 |
| Phantom Strike | 123 | 0.311 | 0.227 | 1.37 |
| Scourge | 110 | 2.102 | 1.974 | 1.06 |
| Decay | 107 | 1.538 | 1.629 | 0.94 |
| Return Fire | 95 | 0.449 | 0.132 | 3.41 |
| Alchemical Fire | 88 | 1.003 | 1.145 | 0.88 |
| Focus Lens | 36 | 0.957 | 0.877 | 1.09 |
| Lightning Scroll | 35 | 0.373 | 0.361 | 1.03 |
| Silence Wave | 26 | 0.209 | 0.209 | 1.00 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.040 | 7.10 |
| Drifter | Melee Charge | 68 | 0.211 | 0.049 | 4.34 |
| Rat King | Return Fire | 41 | 0.389 | 0.091 | 4.28 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.169 | 3.26 |
| Baba | Torment Pulse | 138 | 5.029 | 1.764 | 2.85 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.081 | 2.80 |
| Billy | Crushing Fists | 31 | 0.319 | 0.114 | 2.80 |
| Calico | Melee Charge | 27 | 0.170 | 0.070 | 2.44 |
| Haze | Lucky Shot | 91 | 0.492 | 0.211 | 2.33 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.168 | 2.15 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.090 | 1.95 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.158 | 1.89 |
| Drifter | Tankbuster | 101 | 0.587 | 0.315 | 1.87 |
| Paradox | Tankbuster | 146 | 0.656 | 0.352 | 1.86 |
| Billy | Melee Charge | 48 | 0.242 | 0.133 | 1.82 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.220 | 1.82 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.106 | 1.81 |
| Mina | Spirit Burn | 110 | 0.926 | 0.512 | 1.81 |
| Venator | Ricochet | 36 | 0.114 | 0.202 | 0.57 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.211 | 0.59 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.248 | 1.65 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.190 | 1.65 |
| Calico | Arctic Blast | 102 | 1.394 | 0.862 | 1.62 |
| Abrams | Melee Charge | 129 | 0.306 | 0.194 | 1.58 |
| Bebop | Tankbuster | 43 | 1.252 | 0.796 | 1.57 |
| Infernus | Ricochet | 66 | 0.110 | 0.173 | 0.64 |
| Yamato | Melee Charge | 57 | 0.207 | 0.134 | 1.55 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.150 | 0.65 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.907 | 1.52 |
| Shiv | Express Shot | 125 | 0.882 | 0.584 | 1.51 |
| Lash | Spirit Burn | 69 | 0.946 | 0.640 | 1.48 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.231 | 1.48 |
| Viscous | Mystic Burst | 20 | 0.425 | 0.289 | 1.47 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.163 | 1.44 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.347 | 1.43 |
| Wraith | Ricochet | 185 | 0.133 | 0.185 | 0.72 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.402 | 1.39 |
| Lash | Tankbuster | 193 | 1.645 | 1.190 | 1.38 |
| Shiv | Cold Front | 21 | 0.381 | 0.275 | 1.38 |
| Vyper | Split Shot | 69 | 0.321 | 0.237 | 1.36 |
