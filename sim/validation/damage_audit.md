# Sim vs real damage mix audit

Sample: 600 matches, 5773 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| The Doorman | 2 | 0.20 / 0.11 | 0.57 / 0.37 | 0.22 / 0.50 | 0.01 / 0.03 | 0.29 |
| Apollo | 6 | 0.24 / 0.22 | 0.29 / 0.50 | 0.16 / 0.11 | 0.29 / 0.17 | 0.20 |
| Rem | 23 | 0.25 / 0.25 | 0.54 / 0.46 | 0.16 / 0.24 | 0.04 / 0.04 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.11 | 0.08 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Celeste | 77 | 0.16 / 0.17 | 0.61 / 0.56 | 0.17 / 0.22 | 0.04 / 0.05 | 0.07 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.06 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.44 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Warden | 33 | 0.52 / 0.49 | 0.31 / 0.37 | 0.11 / 0.11 | 0.03 / 0.02 | 0.06 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.46 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Violet | 4 | 0.29 / 0.26 | 0.65 / 0.69 | 0.02 / 0.04 | 0.01 / 0.01 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.50 | 0.07 / 0.08 | 0.01 / 0.02 | 0.05 |
| Kelvin | 12 | 0.09 / 0.09 | 0.65 / 0.63 | 0.22 / 0.27 | 0.02 / 0.01 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.12 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.29 | 0.49 / 0.49 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.48 | 0.17 / 0.20 | 0.02 / 0.02 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.68 | 0.10 / 0.09 | 0.02 / 0.02 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.63 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.75 | 0.02 / 0.03 | 0.03 / 0.04 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.36 | 0.10 / 0.12 | 0.10 / 0.10 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.16 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.60 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.42 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.18 | 0.18 / 0.19 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.22 | 0.02 |
| Paige | 58 | 0.35 / 0.35 | 0.50 / 0.51 | 0.11 / 0.12 | 0.03 / 0.02 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.63 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.27 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.08 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| The Doorman | Tankbuster | item | 0.165 | 0.409 | 0.22 |
| McGinnis | Mini Turret | ability | 0.467 | 0.564 | 0.67 |
| Apollo | Flawless Advance | ability | 0.141 | 0.226 | 0.56 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.15 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.174 | 0.50 |
| Apollo | MELEE | melee | 0.287 | 0.172 | 1.50 |
| The Doorman | Mystic Burst | item | 0.013 | 0.046 | 0.16 |
| Vindicta | Assassinate | ability | 0.162 | 0.108 | 1.67 |
| Rem | Tankbuster | item | 0.063 | 0.123 | 0.51 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.086 | 0.47 |
| Apollo | Itani Lo Sahn | ability | 0.056 | 0.096 | 0.52 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.304 | 1.22 |
| Viscous | Express Shot | item | 0.052 | 0.019 | 3.22 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.046 | 0.28 |
| Solomon | Develop Queen | ability | 0.141 | 0.100 | 1.51 |
| Celeste | Shining Wonder | ability | 0.170 | 0.136 | 1.39 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.178 | 0.74 |
| Pocket | Affliction | ability | 0.120 | 0.156 | 0.73 |
| Warden | Last Stand | ability | 0.138 | 0.174 | 0.75 |
| Solomon | Rook Battery | ability | 0.167 | 0.135 | 1.33 |
| Violet | Living Ink | ability | 0.277 | 0.289 | 0.85 |
| Viscous | MELEE | melee | 0.047 | 0.089 | 0.61 |
| Rem | Decay | item | 0.026 | 0.056 | 0.46 |
| Violet | Abstract Landscape | ability | 0.169 | 0.188 | 0.80 |
| Viscous | Splatter | ability | 0.285 | 0.290 | 1.15 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.092 | 1.41 |
| Sinclair | Spectral Assistant | ability | 0.200 | 0.175 | 1.21 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.107 | 1.32 |
| The Doorman | Call Bell | ability | 0.475 | 0.239 | 1.08 |
| Rem | Pillow Toss | ability | 0.410 | 0.378 | 1.09 |
| Mina | Nox Nostra | ability | 0.128 | 0.157 | 0.79 |
| Viscous | Puddle Punch | ability | 0.123 | 0.107 | 1.34 |
| Paradox | Tankbuster | item | 0.074 | 0.053 | 1.61 |
| Rem | Naptime | ability | 0.115 | 0.086 | 1.35 |
| Shiv | Killing Blow | ability | 0.056 | 0.032 | 1.85 |
| Lash | Ground Strike | ability | 0.350 | 0.351 | 1.10 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.224 | 0.86 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.139 | 0.79 |
| The Doorman | Mystic Shot | item | 0.034 | 0.041 | 0.45 |
| Haze | Bullet Dance | ability | 0.124 | 0.151 | 0.81 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1522 | 1.039 | 0.841 | 1.24 |
| Mystic Burst | 1465 | 0.284 | 0.237 | 1.20 |
| Quicksilver Reload | 1105 | 0.171 | 0.142 | 1.20 |
| Toxic Bullets | 862 | 0.532 | 0.529 | 1.01 |
| Spirit Snatch | 793 | 0.400 | 0.393 | 1.02 |
| Stalker | 790 | 0.219 | 0.204 | 1.07 |
| Torment Pulse | 707 | 1.663 | 1.427 | 1.17 |
| Ricochet | 695 | 0.156 | 0.178 | 0.88 |
| Spirit Strike | 675 | 0.291 | 0.305 | 0.95 |
| Spirit Burn | 579 | 0.773 | 0.562 | 1.37 |
| Express Shot | 552 | 0.677 | 0.498 | 1.36 |
| Escalating Exposure | 542 | 0.892 | 0.901 | 0.99 |
| Siphon Bullets | 521 | 0.248 | 0.243 | 1.02 |
| Tesla Bullets | 509 | 0.480 | 0.479 | 1.00 |
| Cold Front | 505 | 0.447 | 0.419 | 1.07 |
| Mystic Shot | 497 | 0.385 | 0.359 | 1.07 |
| Headhunter | 407 | 0.440 | 0.439 | 1.00 |
| Melee Charge | 379 | 0.240 | 0.115 | 2.08 |
| Capacitor | 375 | 0.696 | 0.696 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.194 | 1.11 |
| Mercurial Magnum | 339 | 0.295 | 0.288 | 1.02 |
| Rebuttal | 212 | 0.063 | 0.050 | 1.26 |
| Mystic Reverb | 204 | 1.313 | 1.531 | 0.86 |
| Lucky Shot | 200 | 0.397 | 0.228 | 1.74 |
| Arctic Blast | 171 | 1.325 | 0.798 | 1.66 |
| Split Shot | 170 | 0.257 | 0.255 | 1.01 |
| Crushing Fists | 143 | 0.303 | 0.113 | 2.68 |
| Phantom Strike | 123 | 0.311 | 0.225 | 1.38 |
| Scourge | 110 | 2.102 | 1.930 | 1.09 |
| Decay | 107 | 1.538 | 1.658 | 0.93 |
| Return Fire | 95 | 0.449 | 0.138 | 3.24 |
| Alchemical Fire | 88 | 1.003 | 1.169 | 0.86 |
| Focus Lens | 36 | 0.957 | 0.886 | 1.08 |
| Lightning Scroll | 35 | 0.373 | 0.376 | 0.99 |
| Silence Wave | 26 | 0.209 | 0.201 | 1.04 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.041 | 7.08 |
| Drifter | Melee Charge | 68 | 0.211 | 0.052 | 4.01 |
| Rat King | Return Fire | 41 | 0.389 | 0.097 | 4.01 |
| Billy | Crushing Fists | 31 | 0.319 | 0.098 | 3.25 |
| Calico | Melee Charge | 27 | 0.170 | 0.058 | 2.95 |
| Baba | Torment Pulse | 138 | 5.029 | 1.807 | 2.78 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.210 | 2.63 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.090 | 2.53 |
| Haze | Lucky Shot | 91 | 0.492 | 0.197 | 2.50 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.135 | 2.21 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.167 | 2.16 |
| Billy | Melee Charge | 48 | 0.242 | 0.127 | 1.91 |
| Paradox | Tankbuster | 146 | 0.656 | 0.344 | 1.91 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.210 | 1.90 |
| Lash | Spirit Burn | 69 | 0.946 | 0.503 | 1.88 |
| Yamato | Melee Charge | 57 | 0.207 | 0.112 | 1.85 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.097 | 1.82 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.109 | 1.77 |
| Drifter | Tankbuster | 101 | 0.587 | 0.341 | 1.72 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.239 | 0.61 |
| Abrams | Melee Charge | 129 | 0.306 | 0.189 | 1.61 |
| Bebop | Tankbuster | 43 | 1.252 | 0.782 | 1.60 |
| Calico | Arctic Blast | 102 | 1.394 | 0.877 | 1.59 |
| Shiv | Express Shot | 125 | 0.882 | 0.565 | 1.56 |
| Infernus | Ricochet | 66 | 0.110 | 0.172 | 0.64 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.265 | 1.55 |
| Yamato | Express Shot | 46 | 0.925 | 0.602 | 1.54 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.204 | 1.53 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.188 | 0.66 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.329 | 1.51 |
| Mina | Spirit Burn | 110 | 0.926 | 0.636 | 1.46 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.953 | 1.45 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.237 | 1.44 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.163 | 1.44 |
| Venator | Ricochet | 36 | 0.114 | 0.162 | 0.71 |
| Lash | Tankbuster | 193 | 1.645 | 1.181 | 1.39 |
| Wraith | Ricochet | 185 | 0.133 | 0.184 | 0.72 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.413 | 1.38 |
| McGinnis | Escalating Exposure | 29 | 1.974 | 1.465 | 1.35 |
| Lash | Mystic Burst | 210 | 0.391 | 0.292 | 1.34 |
