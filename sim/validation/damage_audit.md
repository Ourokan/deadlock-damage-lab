# Sim vs real damage mix audit

Sample: 600 matches, 5859 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| The Doorman | 2 | 0.20 / 0.16 | 0.57 / 0.34 | 0.22 / 0.46 | 0.01 / 0.03 | 0.26 |
| Rem | 23 | 0.25 / 0.24 | 0.54 / 0.47 | 0.16 / 0.25 | 0.04 / 0.04 | 0.09 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.73 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.11 | 0.08 |
| Warden | 33 | 0.52 / 0.48 | 0.31 / 0.38 | 0.11 / 0.10 | 0.03 / 0.02 | 0.07 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.07 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.21 | 0.04 / 0.04 | 0.07 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.44 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Vindicta | 131 | 0.44 / 0.49 | 0.49 / 0.45 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.58 | 0.17 / 0.15 | 0.17 / 0.15 | 0.05 |
| Violet | 4 | 0.29 / 0.26 | 0.65 / 0.69 | 0.02 / 0.04 | 0.01 / 0.01 | 0.05 |
| Kelvin | 12 | 0.09 / 0.09 | 0.65 / 0.63 | 0.22 / 0.27 | 0.02 / 0.02 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.48 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.47 | 0.17 / 0.15 | 0.11 / 0.11 | 0.04 |
| Calico | 110 | 0.13 / 0.13 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.13 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.34 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.27 | 0.02 / 0.00 | 0.04 |
| Sinclair | 20 | 0.17 / 0.19 | 0.76 / 0.74 | 0.02 / 0.03 | 0.03 / 0.04 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.35 | 0.10 / 0.13 | 0.10 / 0.11 | 0.03 |
| Solomon | 42 | 0.37 / 0.38 | 0.54 / 0.52 | 0.07 / 0.08 | 0.01 / 0.02 | 0.03 |
| Seven | 95 | 0.20 / 0.21 | 0.66 / 0.68 | 0.10 / 0.09 | 0.02 / 0.02 | 0.03 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.41 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.19 | 0.18 / 0.19 | 0.03 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.21 | 0.01 / 0.01 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.48 | 0.17 / 0.19 | 0.02 / 0.02 | 0.03 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.27 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Paige | 58 | 0.35 / 0.35 | 0.50 / 0.51 | 0.11 / 0.12 | 0.03 / 0.02 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.15 | 0.22 / 0.23 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.02 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.08 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.59 | 0.03 / 0.02 | 0.05 / 0.05 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.63 | 0.05 / 0.04 | 0.03 / 0.02 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| The Doorman | Tankbuster | item | 0.165 | 0.371 | 0.37 |
| The Doorman | Call Bell | ability | 0.475 | 0.224 | 1.79 |
| McGinnis | Mini Turret | ability | 0.467 | 0.570 | 0.65 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.13 |
| Rem | Tankbuster | item | 0.063 | 0.126 | 0.47 |
| Warden | Last Stand | ability | 0.138 | 0.201 | 0.64 |
| Vindicta | Assassinate | ability | 0.162 | 0.106 | 1.71 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.302 | 1.21 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.292 | 1.21 |
| The Doorman | Mystic Burst | item | 0.013 | 0.042 | 0.27 |
| Sinclair | Spectral Assistant | ability | 0.200 | 0.168 | 1.32 |
| Viscous | Splatter | ability | 0.285 | 0.293 | 1.20 |
| Viscous | Express Shot | item | 0.052 | 0.023 | 2.78 |
| Celeste | Shining Wonder | ability | 0.170 | 0.139 | 1.36 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.177 | 0.74 |
| Pocket | Affliction | ability | 0.120 | 0.158 | 0.72 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.098 | 1.44 |
| Rem | Decay | item | 0.026 | 0.057 | 0.43 |
| Viscous | Goo Ball | ability | 0.107 | 0.086 | 1.55 |
| Solomon | Rook Battery | ability | 0.167 | 0.131 | 1.32 |
| Violet | Living Ink | ability | 0.277 | 0.287 | 0.87 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.228 | 0.84 |
| The Doorman | MELEE | melee | 0.011 | 0.032 | 0.30 |
| Viscous | Puddle Punch | ability | 0.123 | 0.112 | 1.36 |
| Violet | Abstract Landscape | ability | 0.169 | 0.187 | 0.82 |
| Abrams | MELEE | melee | 0.424 | 0.413 | 1.09 |
| Paradox | Tankbuster | item | 0.074 | 0.053 | 1.61 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.093 | 1.37 |
| Mina | Nox Nostra | ability | 0.128 | 0.155 | 0.80 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.170 | 1.20 |
| Haze | Bullet Dance | ability | 0.124 | 0.152 | 0.80 |
| Viscous | MELEE | melee | 0.047 | 0.085 | 0.68 |
| Apollo | MELEE | melee | 0.171 | 0.152 | 1.21 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.137 | 0.79 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.042 | 0.47 |
| Shiv | Killing Blow | ability | 0.056 | 0.034 | 1.75 |
| Lady Geist | Malice | ability | 0.144 | 0.174 | 0.84 |
| Graves | Jar of Dead | ability | 0.212 | 0.235 | 0.88 |
| Baba | MELEE | melee | 0.124 | 0.114 | 1.26 |
| Vindicta | Crow Familiar | ability | 0.155 | 0.145 | 1.20 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1567 | 1.053 | 0.859 | 1.23 |
| Mystic Burst | 1530 | 0.293 | 0.243 | 1.20 |
| Quicksilver Reload | 1105 | 0.171 | 0.143 | 1.20 |
| Toxic Bullets | 862 | 0.532 | 0.535 | 0.99 |
| Spirit Snatch | 854 | 0.412 | 0.412 | 1.00 |
| Stalker | 793 | 0.219 | 0.197 | 1.11 |
| Torment Pulse | 727 | 1.677 | 1.437 | 1.17 |
| Spirit Strike | 707 | 0.293 | 0.304 | 0.96 |
| Ricochet | 695 | 0.156 | 0.180 | 0.87 |
| Spirit Burn | 593 | 0.777 | 0.574 | 1.35 |
| Express Shot | 552 | 0.677 | 0.483 | 1.40 |
| Escalating Exposure | 547 | 0.894 | 0.895 | 1.00 |
| Siphon Bullets | 521 | 0.248 | 0.240 | 1.03 |
| Cold Front | 517 | 0.455 | 0.427 | 1.06 |
| Tesla Bullets | 509 | 0.480 | 0.477 | 1.00 |
| Mystic Shot | 498 | 0.385 | 0.360 | 1.07 |
| Melee Charge | 431 | 0.255 | 0.113 | 2.26 |
| Headhunter | 407 | 0.440 | 0.444 | 0.99 |
| Capacitor | 375 | 0.696 | 0.700 | 0.99 |
| Headshot Booster | 370 | 0.215 | 0.196 | 1.10 |
| Mercurial Magnum | 339 | 0.295 | 0.289 | 1.02 |
| Rebuttal | 217 | 0.064 | 0.041 | 1.58 |
| Mystic Reverb | 204 | 1.313 | 1.559 | 0.84 |
| Lucky Shot | 200 | 0.397 | 0.231 | 1.72 |
| Arctic Blast | 171 | 1.325 | 0.819 | 1.62 |
| Split Shot | 170 | 0.257 | 0.254 | 1.01 |
| Crushing Fists | 147 | 0.307 | 0.108 | 2.85 |
| Phantom Strike | 124 | 0.313 | 0.228 | 1.37 |
| Scourge | 112 | 2.098 | 1.982 | 1.06 |
| Decay | 107 | 1.538 | 1.597 | 0.96 |
| Return Fire | 96 | 0.445 | 0.134 | 3.32 |
| Alchemical Fire | 88 | 1.003 | 1.174 | 0.85 |
| Focus Lens | 36 | 0.957 | 0.919 | 1.04 |
| Lightning Scroll | 35 | 0.373 | 0.373 | 1.00 |
| Silence Wave | 26 | 0.209 | 0.206 | 1.01 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.043 | 6.62 |
| Apollo | Melee Charge | 58 | 0.421 | 0.077 | 5.43 |
| Drifter | Melee Charge | 68 | 0.211 | 0.046 | 4.56 |
| Rat King | Return Fire | 41 | 0.389 | 0.090 | 4.33 |
| Billy | Crushing Fists | 31 | 0.319 | 0.102 | 3.12 |
| Baba | Torment Pulse | 138 | 5.029 | 1.827 | 2.75 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.212 | 2.60 |
| Calico | Melee Charge | 27 | 0.170 | 0.066 | 2.59 |
| Haze | Lucky Shot | 91 | 0.492 | 0.195 | 2.52 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.120 | 2.48 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.092 | 2.48 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.170 | 2.12 |
| Billy | Melee Charge | 48 | 0.242 | 0.115 | 2.10 |
| Paradox | Tankbuster | 146 | 0.656 | 0.338 | 1.94 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.209 | 1.90 |
| Apollo | Mystic Burst | 66 | 0.616 | 0.327 | 1.88 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.098 | 1.80 |
| Drifter | Tankbuster | 101 | 0.587 | 0.335 | 1.75 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.283 | 0.59 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.113 | 1.70 |
| Lash | Spirit Burn | 69 | 0.946 | 0.568 | 1.67 |
| Yamato | Melee Charge | 57 | 0.207 | 0.126 | 1.65 |
| Abrams | Melee Charge | 129 | 0.306 | 0.188 | 1.63 |
| Shiv | Express Shot | 125 | 0.882 | 0.554 | 1.59 |
| Bebop | Tankbuster | 43 | 1.252 | 0.796 | 1.57 |
| Yamato | Express Shot | 46 | 0.925 | 0.593 | 1.56 |
| Calico | Arctic Blast | 102 | 1.394 | 0.893 | 1.56 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.193 | 0.64 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.321 | 1.54 |
| Infernus | Ricochet | 66 | 0.110 | 0.169 | 0.66 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.205 | 1.53 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.271 | 1.51 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.319 | 1.48 |
| Mina | Spirit Burn | 110 | 0.926 | 0.629 | 1.47 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.233 | 1.47 |
| Viscous | Mystic Burst | 20 | 0.425 | 0.295 | 1.44 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.166 | 1.42 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.974 | 1.42 |
| Apollo | Tankbuster | 47 | 2.276 | 1.623 | 1.40 |
| Wraith | Ricochet | 185 | 0.133 | 0.185 | 0.71 |
