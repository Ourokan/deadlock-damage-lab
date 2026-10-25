# Sim vs real damage mix audit

Sample: 600 matches, 5859 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| The Doorman | 2 | 0.20 / 0.12 | 0.57 / 0.37 | 0.22 / 0.49 | 0.01 / 0.03 | 0.28 |
| Rem | 23 | 0.25 / 0.25 | 0.54 / 0.46 | 0.16 / 0.24 | 0.04 / 0.04 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.11 | 0.08 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.22 | 0.04 / 0.05 | 0.07 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.06 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.44 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Warden | 33 | 0.52 / 0.50 | 0.31 / 0.37 | 0.11 / 0.11 | 0.03 / 0.02 | 0.06 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.45 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Violet | 4 | 0.29 / 0.26 | 0.65 / 0.69 | 0.02 / 0.04 | 0.01 / 0.01 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.50 | 0.07 / 0.08 | 0.01 / 0.02 | 0.05 |
| Kelvin | 12 | 0.09 / 0.09 | 0.65 / 0.63 | 0.22 / 0.27 | 0.02 / 0.01 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.12 | 0.04 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.57 | 0.17 / 0.15 | 0.17 / 0.16 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.29 | 0.49 / 0.49 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.48 | 0.17 / 0.20 | 0.02 / 0.02 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.68 | 0.10 / 0.09 | 0.02 / 0.02 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.75 | 0.02 / 0.03 | 0.03 / 0.04 | 0.02 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.36 | 0.10 / 0.12 | 0.10 / 0.10 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.42 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.16 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.60 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.18 | 0.18 / 0.19 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.27 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Paige | 58 | 0.35 / 0.35 | 0.50 / 0.51 | 0.11 / 0.12 | 0.03 / 0.02 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.22 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.62 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.07 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| The Doorman | Tankbuster | item | 0.165 | 0.401 | 0.24 |
| McGinnis | Mini Turret | ability | 0.467 | 0.564 | 0.67 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.15 |
| Vindicta | Assassinate | ability | 0.162 | 0.108 | 1.68 |
| Rem | Tankbuster | item | 0.063 | 0.123 | 0.51 |
| The Doorman | Mystic Burst | item | 0.013 | 0.046 | 0.17 |
| The Doorman | Call Bell | ability | 0.475 | 0.239 | 1.18 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.304 | 1.22 |
| Viscous | Express Shot | item | 0.052 | 0.019 | 3.23 |
| Solomon | Develop Queen | ability | 0.141 | 0.100 | 1.51 |
| Celeste | Shining Wonder | ability | 0.170 | 0.136 | 1.39 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.097 | 1.48 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.084 | 0.53 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.045 | 0.31 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.177 | 0.74 |
| Pocket | Affliction | ability | 0.120 | 0.157 | 0.73 |
| Warden | Last Stand | ability | 0.138 | 0.174 | 0.76 |
| Solomon | Rook Battery | ability | 0.167 | 0.135 | 1.33 |
| Violet | Living Ink | ability | 0.277 | 0.289 | 0.85 |
| Viscous | MELEE | melee | 0.047 | 0.089 | 0.61 |
| Rem | Decay | item | 0.026 | 0.056 | 0.46 |
| Violet | Abstract Landscape | ability | 0.169 | 0.188 | 0.80 |
| Viscous | Splatter | ability | 0.285 | 0.289 | 1.15 |
| Sinclair | Spectral Assistant | ability | 0.200 | 0.175 | 1.21 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.092 | 1.41 |
| Rem | Pillow Toss | ability | 0.410 | 0.378 | 1.09 |
| Mina | Nox Nostra | ability | 0.128 | 0.157 | 0.79 |
| Viscous | Puddle Punch | ability | 0.123 | 0.107 | 1.34 |
| Paradox | Tankbuster | item | 0.074 | 0.053 | 1.62 |
| Lash | Ground Strike | ability | 0.350 | 0.350 | 1.11 |
| Shiv | Killing Blow | ability | 0.056 | 0.032 | 1.86 |
| Rem | Naptime | ability | 0.115 | 0.086 | 1.35 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.139 | 0.79 |
| Haze | Bullet Dance | ability | 0.124 | 0.151 | 0.81 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.172 | 1.19 |
| Baba | MELEE | melee | 0.124 | 0.114 | 1.28 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.305 | 1.10 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.225 | 0.88 |
| Calico | MELEE | melee | 0.149 | 0.125 | 1.22 |
| Violet | Still Life | ability | 0.150 | 0.161 | 0.83 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1567 | 1.053 | 0.851 | 1.24 |
| Mystic Burst | 1530 | 0.293 | 0.240 | 1.22 |
| Quicksilver Reload | 1105 | 0.171 | 0.142 | 1.21 |
| Toxic Bullets | 862 | 0.532 | 0.529 | 1.01 |
| Spirit Snatch | 854 | 0.412 | 0.406 | 1.01 |
| Stalker | 793 | 0.219 | 0.204 | 1.07 |
| Torment Pulse | 727 | 1.677 | 1.434 | 1.17 |
| Spirit Strike | 707 | 0.293 | 0.304 | 0.96 |
| Ricochet | 695 | 0.156 | 0.177 | 0.88 |
| Spirit Burn | 593 | 0.777 | 0.566 | 1.37 |
| Express Shot | 552 | 0.677 | 0.493 | 1.37 |
| Escalating Exposure | 547 | 0.894 | 0.902 | 0.99 |
| Siphon Bullets | 521 | 0.248 | 0.242 | 1.03 |
| Cold Front | 517 | 0.455 | 0.423 | 1.08 |
| Tesla Bullets | 509 | 0.480 | 0.478 | 1.00 |
| Mystic Shot | 498 | 0.385 | 0.358 | 1.07 |
| Melee Charge | 431 | 0.255 | 0.113 | 2.25 |
| Headhunter | 407 | 0.440 | 0.439 | 1.00 |
| Capacitor | 375 | 0.696 | 0.696 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.193 | 1.11 |
| Mercurial Magnum | 339 | 0.295 | 0.288 | 1.03 |
| Rebuttal | 217 | 0.064 | 0.049 | 1.30 |
| Mystic Reverb | 204 | 1.313 | 1.529 | 0.86 |
| Lucky Shot | 200 | 0.397 | 0.228 | 1.74 |
| Arctic Blast | 171 | 1.325 | 0.796 | 1.67 |
| Split Shot | 170 | 0.257 | 0.255 | 1.01 |
| Crushing Fists | 147 | 0.307 | 0.110 | 2.80 |
| Phantom Strike | 124 | 0.313 | 0.226 | 1.38 |
| Scourge | 112 | 2.098 | 1.917 | 1.09 |
| Decay | 107 | 1.538 | 1.644 | 0.94 |
| Return Fire | 96 | 0.445 | 0.140 | 3.19 |
| Alchemical Fire | 88 | 1.003 | 1.169 | 0.86 |
| Focus Lens | 36 | 0.957 | 0.890 | 1.07 |
| Lightning Scroll | 35 | 0.373 | 0.374 | 1.00 |
| Silence Wave | 26 | 0.209 | 0.201 | 1.04 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.041 | 7.00 |
| Apollo | Melee Charge | 58 | 0.421 | 0.078 | 5.41 |
| Rat King | Return Fire | 41 | 0.389 | 0.097 | 4.01 |
| Drifter | Melee Charge | 68 | 0.211 | 0.054 | 3.90 |
| Billy | Crushing Fists | 31 | 0.319 | 0.094 | 3.40 |
| Calico | Melee Charge | 27 | 0.170 | 0.056 | 3.01 |
| Baba | Torment Pulse | 138 | 5.029 | 1.804 | 2.79 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.210 | 2.63 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.090 | 2.53 |
| Haze | Lucky Shot | 91 | 0.492 | 0.198 | 2.48 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.136 | 2.20 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.166 | 2.17 |
| Paradox | Tankbuster | 146 | 0.656 | 0.342 | 1.92 |
| Billy | Melee Charge | 48 | 0.242 | 0.127 | 1.91 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.210 | 1.90 |
| Lash | Spirit Burn | 69 | 0.946 | 0.503 | 1.88 |
| Yamato | Melee Charge | 57 | 0.207 | 0.112 | 1.85 |
| Apollo | Mystic Burst | 66 | 0.616 | 0.334 | 1.84 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.097 | 1.82 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.109 | 1.77 |
| Drifter | Tankbuster | 101 | 0.587 | 0.342 | 1.72 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.239 | 0.61 |
| Abrams | Melee Charge | 129 | 0.306 | 0.189 | 1.61 |
| Calico | Arctic Blast | 102 | 1.394 | 0.872 | 1.60 |
| Bebop | Tankbuster | 43 | 1.252 | 0.784 | 1.59 |
| Shiv | Express Shot | 125 | 0.882 | 0.561 | 1.57 |
| Infernus | Ricochet | 66 | 0.110 | 0.172 | 0.64 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.263 | 1.56 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.204 | 1.54 |
| Yamato | Express Shot | 46 | 0.925 | 0.602 | 1.54 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.326 | 1.52 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.187 | 0.66 |
| Mina | Spirit Burn | 110 | 0.926 | 0.637 | 1.45 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.949 | 1.45 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.236 | 1.45 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.164 | 1.43 |
| Apollo | Tankbuster | 47 | 2.276 | 1.619 | 1.41 |
| Apollo | Torment Pulse | 23 | 1.999 | 1.424 | 1.40 |
| Lash | Tankbuster | 193 | 1.645 | 1.179 | 1.40 |
| Wraith | Ricochet | 185 | 0.133 | 0.184 | 0.72 |
