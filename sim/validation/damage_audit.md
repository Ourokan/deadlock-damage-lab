# Sim vs real damage mix audit

Sample: 600 matches, 5859 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| The Doorman | 2 | 0.20 / 0.16 | 0.57 / 0.34 | 0.22 / 0.46 | 0.01 / 0.03 | 0.26 |
| Rem | 23 | 0.25 / 0.24 | 0.54 / 0.47 | 0.16 / 0.25 | 0.04 / 0.04 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.11 | 0.08 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.22 | 0.04 / 0.04 | 0.07 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.43 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.06 |
| Warden | 33 | 0.52 / 0.50 | 0.31 / 0.37 | 0.11 / 0.11 | 0.03 / 0.02 | 0.06 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.45 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Violet | 4 | 0.29 / 0.26 | 0.65 / 0.69 | 0.02 / 0.04 | 0.01 / 0.01 | 0.05 |
| Kelvin | 12 | 0.09 / 0.09 | 0.65 / 0.63 | 0.22 / 0.27 | 0.02 / 0.01 | 0.05 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.57 | 0.17 / 0.15 | 0.17 / 0.15 | 0.05 |
| Solomon | 42 | 0.37 / 0.39 | 0.54 / 0.50 | 0.07 / 0.08 | 0.01 / 0.02 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.47 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.12 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.29 | 0.49 / 0.49 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.47 | 0.17 / 0.20 | 0.02 / 0.02 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.35 | 0.10 / 0.13 | 0.10 / 0.11 | 0.03 |
| Seven | 95 | 0.20 / 0.21 | 0.66 / 0.68 | 0.10 / 0.09 | 0.02 / 0.02 | 0.03 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.75 | 0.02 / 0.03 | 0.03 / 0.04 | 0.03 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.41 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.63 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.19 | 0.18 / 0.19 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.16 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.60 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.07 | 0.02 |
| Paige | 58 | 0.35 / 0.35 | 0.50 / 0.51 | 0.11 / 0.12 | 0.03 / 0.02 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.27 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.15 | 0.22 / 0.23 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.62 | 0.05 / 0.04 | 0.03 / 0.02 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| The Doorman | Tankbuster | item | 0.165 | 0.371 | 0.37 |
| The Doorman | Call Bell | ability | 0.475 | 0.224 | 1.79 |
| McGinnis | Mini Turret | ability | 0.467 | 0.561 | 0.67 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.14 |
| Rem | Tankbuster | item | 0.063 | 0.125 | 0.49 |
| Vindicta | Assassinate | ability | 0.162 | 0.111 | 1.62 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.303 | 1.23 |
| Viscous | Express Shot | item | 0.052 | 0.018 | 3.27 |
| Celeste | Shining Wonder | ability | 0.170 | 0.136 | 1.41 |
| Solomon | Develop Queen | ability | 0.141 | 0.101 | 1.50 |
| The Doorman | Mystic Burst | item | 0.013 | 0.042 | 0.27 |
| Warden | Last Stand | ability | 0.138 | 0.179 | 0.74 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.096 | 1.49 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.177 | 0.74 |
| Pocket | Affliction | ability | 0.120 | 0.156 | 0.73 |
| Rem | Decay | item | 0.026 | 0.057 | 0.44 |
| Solomon | Rook Battery | ability | 0.167 | 0.136 | 1.31 |
| Violet | Living Ink | ability | 0.277 | 0.288 | 0.86 |
| Viscous | MELEE | melee | 0.047 | 0.087 | 0.62 |
| Violet | Abstract Landscape | ability | 0.169 | 0.187 | 0.81 |
| Abrams | MELEE | melee | 0.424 | 0.414 | 1.10 |
| Sinclair | Spectral Assistant | ability | 0.200 | 0.175 | 1.22 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.092 | 1.42 |
| Viscous | Splatter | ability | 0.285 | 0.291 | 1.14 |
| The Doorman | MELEE | melee | 0.011 | 0.032 | 0.30 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.142 | 0.77 |
| Mina | Nox Nostra | ability | 0.128 | 0.157 | 0.79 |
| Viscous | Puddle Punch | ability | 0.123 | 0.107 | 1.35 |
| Paradox | Tankbuster | item | 0.074 | 0.053 | 1.63 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.227 | 0.86 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.305 | 1.11 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.172 | 1.20 |
| Shiv | Killing Blow | ability | 0.056 | 0.034 | 1.77 |
| Haze | Bullet Dance | ability | 0.124 | 0.151 | 0.81 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.042 | 0.47 |
| Baba | MELEE | melee | 0.124 | 0.113 | 1.28 |
| Apollo | MELEE | melee | 0.171 | 0.154 | 1.19 |
| Lash | Ground Strike | ability | 0.350 | 0.352 | 1.09 |
| Grey Talon | Tankbuster | item | 0.071 | 0.092 | 0.72 |
| Calico | MELEE | melee | 0.149 | 0.125 | 1.21 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1567 | 1.053 | 0.850 | 1.24 |
| Mystic Burst | 1530 | 0.293 | 0.242 | 1.21 |
| Quicksilver Reload | 1105 | 0.171 | 0.142 | 1.21 |
| Toxic Bullets | 862 | 0.532 | 0.527 | 1.01 |
| Spirit Snatch | 854 | 0.412 | 0.411 | 1.00 |
| Stalker | 793 | 0.219 | 0.197 | 1.11 |
| Torment Pulse | 727 | 1.677 | 1.434 | 1.17 |
| Spirit Strike | 707 | 0.293 | 0.304 | 0.96 |
| Ricochet | 695 | 0.156 | 0.177 | 0.89 |
| Spirit Burn | 593 | 0.777 | 0.569 | 1.36 |
| Express Shot | 552 | 0.677 | 0.498 | 1.36 |
| Escalating Exposure | 547 | 0.894 | 0.894 | 1.00 |
| Siphon Bullets | 521 | 0.248 | 0.240 | 1.03 |
| Cold Front | 517 | 0.455 | 0.424 | 1.07 |
| Tesla Bullets | 509 | 0.480 | 0.477 | 1.01 |
| Mystic Shot | 498 | 0.385 | 0.360 | 1.07 |
| Melee Charge | 431 | 0.255 | 0.110 | 2.31 |
| Headhunter | 407 | 0.440 | 0.441 | 1.00 |
| Capacitor | 375 | 0.696 | 0.697 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.197 | 1.10 |
| Mercurial Magnum | 339 | 0.295 | 0.288 | 1.02 |
| Rebuttal | 217 | 0.064 | 0.040 | 1.61 |
| Mystic Reverb | 204 | 1.313 | 1.514 | 0.87 |
| Lucky Shot | 200 | 0.397 | 0.232 | 1.71 |
| Arctic Blast | 171 | 1.325 | 0.816 | 1.62 |
| Split Shot | 170 | 0.257 | 0.258 | 1.00 |
| Crushing Fists | 147 | 0.307 | 0.110 | 2.80 |
| Phantom Strike | 124 | 0.313 | 0.226 | 1.38 |
| Scourge | 112 | 2.098 | 1.955 | 1.07 |
| Decay | 107 | 1.538 | 1.589 | 0.97 |
| Return Fire | 96 | 0.445 | 0.134 | 3.32 |
| Alchemical Fire | 88 | 1.003 | 1.190 | 0.84 |
| Focus Lens | 36 | 0.957 | 0.927 | 1.03 |
| Lightning Scroll | 35 | 0.373 | 0.363 | 1.03 |
| Silence Wave | 26 | 0.209 | 0.205 | 1.02 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.043 | 6.63 |
| Apollo | Melee Charge | 58 | 0.421 | 0.073 | 5.78 |
| Drifter | Melee Charge | 68 | 0.211 | 0.044 | 4.75 |
| Rat King | Return Fire | 41 | 0.389 | 0.091 | 4.28 |
| Billy | Crushing Fists | 31 | 0.319 | 0.103 | 3.10 |
| Calico | Melee Charge | 27 | 0.170 | 0.061 | 2.78 |
| Baba | Torment Pulse | 138 | 5.029 | 1.813 | 2.77 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.210 | 2.62 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.089 | 2.55 |
| Haze | Lucky Shot | 91 | 0.492 | 0.197 | 2.49 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.122 | 2.44 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.169 | 2.13 |
| Billy | Melee Charge | 48 | 0.242 | 0.119 | 2.04 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.202 | 1.98 |
| Paradox | Tankbuster | 146 | 0.656 | 0.338 | 1.94 |
| Lash | Spirit Burn | 69 | 0.946 | 0.503 | 1.88 |
| Apollo | Mystic Burst | 66 | 0.616 | 0.328 | 1.88 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.097 | 1.82 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.110 | 1.75 |
| Drifter | Tankbuster | 101 | 0.587 | 0.336 | 1.75 |
| Abrams | Melee Charge | 129 | 0.306 | 0.185 | 1.65 |
| Yamato | Melee Charge | 57 | 0.207 | 0.128 | 1.62 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.200 | 0.63 |
| Calico | Arctic Blast | 102 | 1.394 | 0.889 | 1.57 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.263 | 1.56 |
| Shiv | Express Shot | 125 | 0.882 | 0.570 | 1.55 |
| Infernus | Ricochet | 66 | 0.110 | 0.171 | 0.65 |
| Bebop | Tankbuster | 43 | 1.252 | 0.814 | 1.54 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.190 | 0.65 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.205 | 1.53 |
| Yamato | Express Shot | 46 | 0.925 | 0.611 | 1.51 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.334 | 1.49 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.329 | 1.47 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.163 | 1.44 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.237 | 1.44 |
| Mina | Spirit Burn | 110 | 0.926 | 0.644 | 1.44 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.963 | 1.43 |
| Apollo | Tankbuster | 47 | 2.276 | 1.599 | 1.42 |
| Wraith | Ricochet | 185 | 0.133 | 0.184 | 0.72 |
| McGinnis | Escalating Exposure | 29 | 1.974 | 1.437 | 1.37 |
