# Sim vs real damage mix audit

Sample: 600 matches, 5773 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.24 | 0.29 / 0.45 | 0.16 / 0.12 | 0.29 / 0.18 | 0.15 |
| The Doorman | 2 | 0.20 / 0.12 | 0.57 / 0.52 | 0.22 / 0.34 | 0.01 / 0.02 | 0.13 |
| Mirage | 45 | 0.31 / 0.36 | 0.48 / 0.39 | 0.17 / 0.22 | 0.02 / 0.03 | 0.11 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.62 | 0.25 / 0.19 | 0.12 / 0.11 | 0.10 |
| Rem | 23 | 0.25 / 0.25 | 0.54 / 0.46 | 0.16 / 0.24 | 0.04 / 0.05 | 0.09 |
| Kelvin | 12 | 0.09 / 0.10 | 0.65 / 0.60 | 0.22 / 0.29 | 0.02 / 0.02 | 0.08 |
| Vyper | 78 | 0.46 / 0.51 | 0.26 / 0.20 | 0.25 / 0.27 | 0.02 / 0.02 | 0.08 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.00 | 0.07 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.53 | 0.28 / 0.23 | 0.05 / 0.07 | 0.07 |
| Paige | 58 | 0.35 / 0.39 | 0.50 / 0.45 | 0.11 / 0.13 | 0.03 / 0.02 | 0.07 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.44 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.41 | 0.31 / 0.34 | 0.15 / 0.11 | 0.06 |
| Yamato | 131 | 0.24 / 0.25 | 0.38 / 0.34 | 0.17 / 0.21 | 0.18 / 0.20 | 0.06 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.57 | 0.17 / 0.21 | 0.04 / 0.04 | 0.06 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.48 | 0.17 / 0.14 | 0.11 / 0.10 | 0.06 |
| Victor | 129 | 0.15 / 0.17 | 0.64 / 0.58 | 0.16 / 0.20 | 0.03 / 0.03 | 0.06 |
| Violet | 4 | 0.29 / 0.25 | 0.65 / 0.69 | 0.02 / 0.04 | 0.01 / 0.01 | 0.06 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.46 | 0.05 / 0.05 | 0.01 / 0.01 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.50 | 0.07 / 0.08 | 0.01 / 0.02 | 0.05 |
| Seven | 95 | 0.20 / 0.24 | 0.66 / 0.63 | 0.10 / 0.11 | 0.02 / 0.02 | 0.05 |
| Warden | 33 | 0.52 / 0.50 | 0.31 / 0.36 | 0.11 / 0.11 | 0.03 / 0.02 | 0.05 |
| Infernus | 173 | 0.23 / 0.24 | 0.60 / 0.57 | 0.13 / 0.16 | 0.03 / 0.02 | 0.04 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Abrams | 138 | 0.23 / 0.26 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.40 | 0.04 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.34 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Bebop | 254 | 0.18 / 0.19 | 0.56 / 0.59 | 0.19 / 0.18 | 0.05 / 0.04 | 0.04 |
| Deadman Danny | 357 | 0.16 / 0.14 | 0.63 / 0.67 | 0.18 / 0.18 | 0.01 / 0.01 | 0.04 |
| Silver | 100 | 0.41 / 0.42 | 0.37 / 0.35 | 0.10 / 0.12 | 0.10 / 0.10 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.49 | 0.16 / 0.19 | 0.01 / 0.01 | 0.03 |
| Dynamo | 53 | 0.23 / 0.23 | 0.62 / 0.65 | 0.08 / 0.08 | 0.05 / 0.04 | 0.03 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.74 | 0.02 / 0.03 | 0.03 / 0.04 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.15 | 0.08 / 0.08 | 0.03 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.47 | 0.39 / 0.41 | 0.05 / 0.03 | 0.02 |
| Venator | 257 | 0.48 / 0.50 | 0.40 / 0.39 | 0.03 / 0.02 | 0.07 / 0.08 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.57 | 0.25 / 0.26 | 0.03 / 0.03 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Holliday | 73 | 0.27 / 0.29 | 0.54 / 0.54 | 0.13 / 0.13 | 0.05 / 0.05 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.67 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.42 | 0.14 / 0.16 | 0.22 / 0.21 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.29 | 0.62 / 0.63 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| The Doorman | Tankbuster | item | 0.165 | 0.273 | 0.38 |
| McGinnis | Mini Turret | ability | 0.467 | 0.571 | 0.67 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.199 | 1.69 |
| Baba | Torment Pulse | item | 0.170 | 0.090 | 2.21 |
| Apollo | MELEE | melee | 0.287 | 0.184 | 1.55 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.272 | 0.64 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.308 | 0.70 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.116 | 0.40 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.031 | 2.72 |
| Apollo | Flawless Advance | ability | 0.141 | 0.219 | 0.64 |
| Kelvin | Arctic Beam | ability | 0.397 | 0.362 | 1.24 |
| Victor | Pain Battery | ability | 0.276 | 0.229 | 1.35 |
| Vindicta | Assassinate | ability | 0.162 | 0.110 | 1.65 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.157 | 0.61 |
| Abrams | MELEE | melee | 0.424 | 0.398 | 1.20 |
| Rem | Tankbuster | item | 0.063 | 0.117 | 0.53 |
| The Doorman | Call Bell | ability | 0.475 | 0.347 | 0.86 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.054 | 0.27 |
| Vyper | Lethal Venom | ability | 0.112 | 0.069 | 1.81 |
| Sinclair | Audience Participation | ability | 0.194 | 0.264 | 0.78 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.306 | 1.22 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.022 | 2.94 |
| Calico | MELEE | melee | 0.149 | 0.106 | 1.51 |
| Violet | Living Ink | ability | 0.277 | 0.296 | 0.82 |
| Solomon | Develop Queen | ability | 0.141 | 0.102 | 1.51 |
| Infernus | Flame Dash | ability | 0.216 | 0.177 | 1.30 |
| Celeste | Shining Wonder | ability | 0.170 | 0.137 | 1.40 |
| Seven | Lightning Ball | ability | 0.198 | 0.175 | 1.33 |
| Paige | Bookwyrm | ability | 0.320 | 0.302 | 1.19 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.184 | 0.74 |
| Rem | Decay | item | 0.026 | 0.062 | 0.41 |
| Viscous | Express Shot | item | 0.052 | 0.024 | 2.72 |
| Pocket | Affliction | ability | 0.120 | 0.157 | 0.72 |
| Solomon | Rook Battery | ability | 0.167 | 0.137 | 1.34 |
| Seven | Power Surge | ability | 0.205 | 0.193 | 1.26 |
| Mo & Krill | Tankbuster | item | 0.061 | 0.029 | 2.09 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.337 | 0.88 |
| Warden | Last Stand | ability | 0.138 | 0.171 | 0.77 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1522 | 1.039 | 0.775 | 1.34 |
| Mystic Burst | 1465 | 0.284 | 0.238 | 1.19 |
| Quicksilver Reload | 1105 | 0.171 | 0.144 | 1.19 |
| Toxic Bullets | 862 | 0.532 | 0.528 | 1.01 |
| Spirit Snatch | 793 | 0.400 | 0.336 | 1.19 |
| Stalker | 790 | 0.219 | 0.206 | 1.06 |
| Torment Pulse | 707 | 1.663 | 1.431 | 1.16 |
| Ricochet | 695 | 0.156 | 0.180 | 0.87 |
| Spirit Strike | 675 | 0.291 | 0.271 | 1.07 |
| Spirit Burn | 579 | 0.773 | 0.583 | 1.32 |
| Express Shot | 552 | 0.677 | 0.496 | 1.36 |
| Escalating Exposure | 542 | 0.892 | 0.882 | 1.01 |
| Siphon Bullets | 521 | 0.248 | 0.243 | 1.02 |
| Tesla Bullets | 509 | 0.480 | 0.480 | 1.00 |
| Cold Front | 505 | 0.447 | 0.417 | 1.07 |
| Mystic Shot | 497 | 0.385 | 0.360 | 1.07 |
| Headhunter | 407 | 0.440 | 0.433 | 1.02 |
| Melee Charge | 379 | 0.240 | 0.102 | 2.36 |
| Capacitor | 375 | 0.696 | 0.698 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.199 | 1.08 |
| Mercurial Magnum | 339 | 0.295 | 0.287 | 1.03 |
| Rebuttal | 212 | 0.063 | 0.045 | 1.40 |
| Mystic Reverb | 204 | 1.313 | 1.494 | 0.88 |
| Lucky Shot | 200 | 0.397 | 0.227 | 1.75 |
| Arctic Blast | 171 | 1.325 | 0.783 | 1.69 |
| Split Shot | 170 | 0.257 | 0.252 | 1.02 |
| Crushing Fists | 143 | 0.303 | 0.098 | 3.09 |
| Phantom Strike | 123 | 0.311 | 0.222 | 1.40 |
| Scourge | 110 | 2.102 | 1.936 | 1.09 |
| Decay | 107 | 1.538 | 1.682 | 0.91 |
| Return Fire | 95 | 0.449 | 0.126 | 3.55 |
| Alchemical Fire | 88 | 1.003 | 1.135 | 0.88 |
| Focus Lens | 36 | 0.957 | 0.835 | 1.15 |
| Lightning Scroll | 35 | 0.373 | 0.365 | 1.02 |
| Silence Wave | 26 | 0.209 | 0.210 | 0.99 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.043 | 6.76 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.054 | 5.59 |
| Drifter | Melee Charge | 68 | 0.211 | 0.042 | 5.05 |
| Rat King | Return Fire | 41 | 0.389 | 0.093 | 4.17 |
| Calico | Melee Charge | 27 | 0.170 | 0.052 | 3.25 |
| Yamato | Melee Charge | 57 | 0.207 | 0.069 | 3.03 |
| Baba | Torment Pulse | 138 | 5.029 | 1.749 | 2.88 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.197 | 2.80 |
| Mo & Krill | Tankbuster | 118 | 3.292 | 1.202 | 2.74 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.087 | 2.61 |
| Bebop | Spirit Strike | 186 | 0.274 | 0.108 | 2.54 |
| Haze | Lucky Shot | 91 | 0.492 | 0.195 | 2.52 |
| Billy | Crushing Fists | 31 | 0.319 | 0.129 | 2.47 |
| Drifter | Tankbuster | 101 | 0.587 | 0.243 | 2.41 |
| Billy | Melee Charge | 48 | 0.242 | 0.104 | 2.33 |
| Bebop | Spirit Snatch | 191 | 0.342 | 0.155 | 2.20 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.202 | 1.98 |
| Paradox | Tankbuster | 146 | 0.656 | 0.344 | 1.91 |
| Holliday | Tankbuster | 48 | 0.959 | 0.505 | 1.90 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.095 | 1.85 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.107 | 1.80 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.203 | 1.77 |
| Abrams | Melee Charge | 129 | 0.306 | 0.173 | 1.76 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.189 | 1.66 |
| Calico | Arctic Blast | 102 | 1.394 | 0.844 | 1.65 |
| Bebop | Tankbuster | 43 | 1.252 | 0.783 | 1.60 |
| Infernus | Ricochet | 66 | 0.110 | 0.176 | 0.63 |
| Shiv | Express Shot | 125 | 0.882 | 0.557 | 1.58 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.261 | 1.57 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.189 | 0.66 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.326 | 1.52 |
| Mina | Spirit Burn | 110 | 0.926 | 0.613 | 1.51 |
| Venator | Ricochet | 36 | 0.114 | 0.173 | 0.66 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.158 | 1.49 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.115 | 0.67 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.938 | 1.47 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.235 | 1.46 |
| Baba | Alchemical Fire | 20 | 3.002 | 2.067 | 1.45 |
| Celeste | Tankbuster | 29 | 1.268 | 0.876 | 1.45 |
| Shiv | Cold Front | 21 | 0.381 | 0.275 | 1.39 |
