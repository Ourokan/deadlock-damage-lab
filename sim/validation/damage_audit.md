# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.73 | 0.12 / 0.10 | 0.02 / 0.00 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.60 | 0.25 / 0.19 | 0.12 / 0.11 | 0.08 |
| Warden | 33 | 0.52 / 0.48 | 0.31 / 0.39 | 0.11 / 0.10 | 0.03 / 0.02 | 0.07 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.08 | 0.07 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.21 | 0.04 / 0.04 | 0.07 |
| Vindicta | 131 | 0.44 / 0.49 | 0.49 / 0.45 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.44 | 0.23 / 0.24 | 0.03 / 0.05 | 0.06 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.58 | 0.17 / 0.15 | 0.17 / 0.15 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.05 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.14 | 0.11 / 0.10 | 0.04 |
| Calico | 110 | 0.13 / 0.13 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.13 | 0.04 |
| Sinclair | 55 | 0.12 / 0.15 | 0.79 / 0.76 | 0.04 / 0.03 | 0.03 / 0.04 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.48 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.34 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.27 | 0.02 / 0.00 | 0.04 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.69 | 0.17 / 0.20 | 0.03 / 0.02 | 0.04 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.08 | 0.02 / 0.01 | 0.04 |
| Holliday | 73 | 0.27 / 0.27 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.35 | 0.10 / 0.13 | 0.10 / 0.11 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.41 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.63 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Paige | 135 | 0.29 / 0.31 | 0.59 / 0.58 | 0.07 / 0.08 | 0.03 / 0.02 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.59 | 0.16 / 0.16 | 0.05 / 0.04 | 0.03 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.19 | 0.18 / 0.19 | 0.02 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.48 | 0.17 / 0.19 | 0.02 / 0.02 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.60 | 0.17 / 0.18 | 0.03 / 0.04 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.07 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.15 | 0.22 / 0.23 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.02 |
| Solomon | 136 | 0.25 / 0.25 | 0.64 / 0.63 | 0.08 / 0.08 | 0.02 / 0.02 | 0.01 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.62 | 0.05 / 0.04 | 0.03 / 0.02 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| McGinnis | Mini Turret | ability | 0.467 | 0.572 | 0.65 |
| Sinclair | Vexing Bolt | ability | 0.351 | 0.296 | 1.47 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.16 |
| Warden | Last Stand | ability | 0.138 | 0.205 | 0.62 |
| Vindicta | Assassinate | ability | 0.162 | 0.107 | 1.70 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.083 | 1.73 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.302 | 1.21 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.176 | 0.74 |
| Celeste | Shining Wonder | ability | 0.170 | 0.141 | 1.35 |
| Pocket | Affliction | ability | 0.120 | 0.158 | 0.72 |
| Viscous | Splatter | ability | 0.285 | 0.295 | 1.18 |
| Viscous | Express Shot | item | 0.052 | 0.025 | 2.60 |
| Viscous | Goo Ball | ability | 0.107 | 0.086 | 1.53 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.191 | 1.24 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.273 | 1.14 |
| Paige | Bookwyrm | ability | 0.376 | 0.361 | 1.11 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.230 | 0.85 |
| Viscous | Puddle Punch | ability | 0.123 | 0.112 | 1.35 |
| Abrams | MELEE | melee | 0.424 | 0.413 | 1.09 |
| Paradox | Tankbuster | item | 0.074 | 0.052 | 1.62 |
| Haze | Bullet Dance | ability | 0.124 | 0.153 | 0.80 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.094 | 1.36 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.171 | 1.20 |
| Mina | Nox Nostra | ability | 0.128 | 0.154 | 0.81 |
| Apollo | MELEE | melee | 0.171 | 0.151 | 1.21 |
| Viscous | MELEE | melee | 0.047 | 0.084 | 0.68 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.137 | 0.79 |
| Baba | MELEE | melee | 0.124 | 0.114 | 1.29 |
| Vindicta | Crow Familiar | ability | 0.155 | 0.143 | 1.22 |
| Shiv | Killing Blow | ability | 0.056 | 0.035 | 1.73 |
| Haze | Fixation | ability | 0.304 | 0.324 | 0.92 |
| Graves | Jar of Dead | ability | 0.212 | 0.233 | 0.89 |
| The Doorman | Call Bell | ability | 0.474 | 0.464 | 1.06 |
| Lady Geist | Malice | ability | 0.144 | 0.173 | 0.86 |
| Lash | Ground Strike | ability | 0.350 | 0.353 | 1.07 |
| Holliday | Powder Keg | ability | 0.397 | 0.385 | 1.06 |
| Vyper | Split Shot | item | 0.110 | 0.089 | 1.25 |
| Calico | MELEE | melee | 0.149 | 0.127 | 1.18 |
| Kelvin | MELEE | melee | 0.034 | 0.017 | 2.05 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.320 | 0.93 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1887 | 1.093 | 0.846 | 1.29 |
| Mystic Burst | 1691 | 0.292 | 0.236 | 1.24 |
| Quicksilver Reload | 1114 | 0.171 | 0.142 | 1.21 |
| Toxic Bullets | 875 | 0.530 | 0.529 | 1.00 |
| Spirit Snatch | 856 | 0.411 | 0.408 | 1.01 |
| Torment Pulse | 814 | 1.625 | 1.291 | 1.26 |
| Stalker | 794 | 0.219 | 0.196 | 1.12 |
| Spirit Strike | 710 | 0.291 | 0.302 | 0.97 |
| Ricochet | 695 | 0.156 | 0.179 | 0.88 |
| Spirit Burn | 685 | 0.833 | 0.599 | 1.39 |
| Mystic Shot | 673 | 0.407 | 0.341 | 1.19 |
| Escalating Exposure | 610 | 0.933 | 0.907 | 1.03 |
| Express Shot | 558 | 0.676 | 0.485 | 1.39 |
| Cold Front | 525 | 0.455 | 0.429 | 1.06 |
| Siphon Bullets | 521 | 0.248 | 0.239 | 1.04 |
| Tesla Bullets | 509 | 0.480 | 0.477 | 1.00 |
| Melee Charge | 434 | 0.254 | 0.112 | 2.28 |
| Headhunter | 410 | 0.439 | 0.445 | 0.99 |
| Capacitor | 375 | 0.696 | 0.697 | 1.00 |
| Headshot Booster | 375 | 0.213 | 0.194 | 1.10 |
| Mercurial Magnum | 340 | 0.296 | 0.287 | 1.03 |
| Rebuttal | 236 | 0.064 | 0.043 | 1.49 |
| Mystic Reverb | 211 | 1.326 | 1.560 | 0.85 |
| Lucky Shot | 200 | 0.397 | 0.224 | 1.77 |
| Arctic Blast | 171 | 1.325 | 0.835 | 1.59 |
| Split Shot | 170 | 0.257 | 0.252 | 1.02 |
| Crushing Fists | 147 | 0.307 | 0.109 | 2.82 |
| Decay | 135 | 1.566 | 1.565 | 1.00 |
| Phantom Strike | 125 | 0.315 | 0.231 | 1.36 |
| Scourge | 121 | 2.131 | 1.821 | 1.17 |
| Alchemical Fire | 111 | 0.994 | 0.994 | 1.00 |
| Return Fire | 96 | 0.445 | 0.125 | 3.57 |
| Lightning Scroll | 49 | 0.423 | 0.272 | 1.56 |
| Focus Lens | 39 | 0.941 | 0.849 | 1.11 |
| Silence Wave | 33 | 0.238 | 0.199 | 1.20 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.044 | 6.49 |
| Apollo | Melee Charge | 58 | 0.421 | 0.075 | 5.59 |
| Rat King | Return Fire | 41 | 0.389 | 0.083 | 4.71 |
| Drifter | Melee Charge | 68 | 0.211 | 0.046 | 4.57 |
| Billy | Crushing Fists | 31 | 0.319 | 0.110 | 2.90 |
| Baba | Torment Pulse | 138 | 5.029 | 1.792 | 2.81 |
| Calico | Melee Charge | 27 | 0.170 | 0.061 | 2.78 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.214 | 2.58 |
| Haze | Lucky Shot | 91 | 0.492 | 0.196 | 2.52 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.120 | 2.48 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.092 | 2.47 |
| Violet | Torment Pulse | 69 | 0.825 | 0.364 | 2.27 |
| Billy | Melee Charge | 48 | 0.242 | 0.110 | 2.20 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.172 | 2.10 |
| Paradox | Tankbuster | 146 | 0.656 | 0.336 | 1.95 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.211 | 1.89 |
| Apollo | Mystic Burst | 66 | 0.616 | 0.327 | 1.88 |
| Violet | Mystic Burst | 66 | 0.227 | 0.122 | 1.85 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.098 | 1.80 |
| Drifter | Tankbuster | 101 | 0.587 | 0.326 | 1.80 |
| Violet | Tankbuster | 206 | 1.178 | 0.670 | 1.76 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.112 | 1.73 |
| Lash | Spirit Burn | 69 | 0.946 | 0.558 | 1.69 |
| Yamato | Melee Charge | 57 | 0.207 | 0.123 | 1.68 |
| Abrams | Melee Charge | 129 | 0.306 | 0.188 | 1.63 |
| Kelvin | Escalating Exposure | 40 | 4.081 | 2.533 | 1.61 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.194 | 0.63 |
| Solomon | Spirit Burn | 23 | 1.019 | 0.642 | 1.59 |
| Bebop | Tankbuster | 43 | 1.252 | 0.797 | 1.57 |
| Shiv | Express Shot | 125 | 0.882 | 0.562 | 1.57 |
| Yamato | Express Shot | 46 | 0.925 | 0.591 | 1.57 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.203 | 1.54 |
| Violet | Mystic Shot | 170 | 0.473 | 0.309 | 1.53 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.189 | 0.66 |
| Infernus | Ricochet | 66 | 0.110 | 0.168 | 0.66 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.327 | 1.52 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.271 | 1.51 |
| Calico | Arctic Blast | 102 | 1.394 | 0.926 | 1.51 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.303 | 1.50 |
| Violet | Spirit Burn | 45 | 0.914 | 0.619 | 1.48 |
