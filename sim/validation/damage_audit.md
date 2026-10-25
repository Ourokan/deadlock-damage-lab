# Sim vs real damage mix audit

Sample: 600 matches, 5773 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| The Doorman | 2 | 0.20 / 0.11 | 0.57 / 0.37 | 0.22 / 0.50 | 0.01 / 0.03 | 0.29 |
| Apollo | 6 | 0.24 / 0.22 | 0.29 / 0.50 | 0.16 / 0.11 | 0.29 / 0.17 | 0.20 |
| Rem | 23 | 0.25 / 0.25 | 0.54 / 0.47 | 0.16 / 0.24 | 0.04 / 0.04 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.11 | 0.08 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.33 | 0.17 / 0.21 | 0.18 / 0.22 | 0.08 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.22 | 0.04 / 0.05 | 0.07 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.06 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.44 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Warden | 33 | 0.52 / 0.49 | 0.31 / 0.37 | 0.11 / 0.11 | 0.03 / 0.02 | 0.06 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.45 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Violet | 4 | 0.29 / 0.26 | 0.65 / 0.69 | 0.02 / 0.03 | 0.01 / 0.01 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.50 | 0.07 / 0.08 | 0.01 / 0.02 | 0.05 |
| Kelvin | 12 | 0.09 / 0.09 | 0.65 / 0.63 | 0.22 / 0.27 | 0.02 / 0.01 | 0.05 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.12 | 0.04 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.49 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Deadman Danny | 357 | 0.16 / 0.14 | 0.63 / 0.67 | 0.18 / 0.18 | 0.01 / 0.01 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.63 | 0.06 / 0.07 | 0.03 / 0.03 | 0.03 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.74 | 0.02 / 0.03 | 0.03 / 0.04 | 0.03 |
| Seven | 95 | 0.20 / 0.21 | 0.66 / 0.68 | 0.10 / 0.09 | 0.02 / 0.02 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.08 | 0.05 / 0.04 | 0.03 |
| Mirage | 45 | 0.31 / 0.31 | 0.48 / 0.48 | 0.17 / 0.19 | 0.02 / 0.02 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.36 | 0.10 / 0.12 | 0.10 / 0.10 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.60 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.42 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.27 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.23 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.63 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Paige | 58 | 0.35 / 0.35 | 0.50 / 0.51 | 0.11 / 0.12 | 0.03 / 0.02 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.07 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| The Doorman | Tankbuster | item | 0.165 | 0.409 | 0.22 |
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| McGinnis | Mini Turret | ability | 0.467 | 0.564 | 0.67 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.15 |
| Apollo | Flawless Advance | ability | 0.141 | 0.226 | 0.56 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.174 | 0.50 |
| Apollo | MELEE | melee | 0.287 | 0.172 | 1.50 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.270 | 0.66 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.308 | 0.71 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.030 | 2.80 |
| The Doorman | Mystic Burst | item | 0.013 | 0.046 | 0.16 |
| Rem | Tankbuster | item | 0.063 | 0.124 | 0.50 |
| Vindicta | Assassinate | ability | 0.162 | 0.108 | 1.67 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.086 | 0.47 |
| Sinclair | Audience Participation | ability | 0.194 | 0.263 | 0.79 |
| Apollo | Itani Lo Sahn | ability | 0.056 | 0.096 | 0.52 |
| Celeste | Shining Wonder | ability | 0.170 | 0.132 | 1.44 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.305 | 1.22 |
| Viscous | Express Shot | item | 0.052 | 0.019 | 3.23 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.046 | 0.28 |
| Solomon | Develop Queen | ability | 0.141 | 0.101 | 1.51 |
| Violet | Living Ink | ability | 0.277 | 0.294 | 0.83 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.178 | 0.74 |
| Yamato | MELEE | melee | 0.184 | 0.224 | 0.79 |
| Warden | Last Stand | ability | 0.138 | 0.175 | 0.75 |
| Pocket | Affliction | ability | 0.120 | 0.156 | 0.73 |
| Solomon | Rook Battery | ability | 0.167 | 0.136 | 1.32 |
| Rem | Decay | item | 0.026 | 0.057 | 0.46 |
| Viscous | MELEE | melee | 0.047 | 0.089 | 0.61 |
| Viscous | Splatter | ability | 0.285 | 0.289 | 1.15 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.092 | 1.41 |
| The Doorman | Call Bell | ability | 0.475 | 0.239 | 1.08 |
| Mina | Nox Nostra | ability | 0.128 | 0.157 | 0.79 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.301 | 1.12 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.322 | 0.89 |
| Paradox | Tankbuster | item | 0.074 | 0.054 | 1.60 |
| Viscous | Puddle Punch | ability | 0.123 | 0.108 | 1.33 |
| Sinclair | Spectral Assistant | ability | 0.200 | 0.180 | 1.19 |
| Shiv | Killing Blow | ability | 0.056 | 0.033 | 1.84 |
| Violet | Abstract Landscape | ability | 0.169 | 0.181 | 0.83 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1518 | 1.040 | 0.847 | 1.23 |
| Mystic Burst | 1464 | 0.284 | 0.237 | 1.19 |
| Quicksilver Reload | 1103 | 0.171 | 0.143 | 1.20 |
| Toxic Bullets | 852 | 0.534 | 0.527 | 1.01 |
| Spirit Snatch | 793 | 0.400 | 0.394 | 1.02 |
| Stalker | 790 | 0.219 | 0.207 | 1.06 |
| Torment Pulse | 706 | 1.665 | 1.435 | 1.16 |
| Ricochet | 684 | 0.156 | 0.179 | 0.87 |
| Spirit Strike | 675 | 0.291 | 0.308 | 0.94 |
| Spirit Burn | 576 | 0.773 | 0.569 | 1.36 |
| Express Shot | 550 | 0.676 | 0.502 | 1.35 |
| Escalating Exposure | 539 | 0.896 | 0.905 | 0.99 |
| Siphon Bullets | 514 | 0.248 | 0.246 | 1.01 |
| Tesla Bullets | 508 | 0.480 | 0.479 | 1.00 |
| Cold Front | 505 | 0.447 | 0.417 | 1.07 |
| Mystic Shot | 497 | 0.385 | 0.363 | 1.06 |
| Headhunter | 406 | 0.440 | 0.440 | 1.00 |
| Melee Charge | 379 | 0.240 | 0.117 | 2.06 |
| Capacitor | 373 | 0.697 | 0.699 | 1.00 |
| Headshot Booster | 369 | 0.215 | 0.194 | 1.11 |
| Mercurial Magnum | 339 | 0.295 | 0.289 | 1.02 |
| Rebuttal | 212 | 0.063 | 0.044 | 1.43 |
| Mystic Reverb | 203 | 1.312 | 1.506 | 0.87 |
| Lucky Shot | 198 | 0.396 | 0.228 | 1.74 |
| Split Shot | 170 | 0.257 | 0.252 | 1.02 |
| Arctic Blast | 170 | 1.325 | 0.801 | 1.66 |
| Crushing Fists | 143 | 0.303 | 0.117 | 2.59 |
| Phantom Strike | 122 | 0.311 | 0.228 | 1.36 |
| Scourge | 108 | 2.062 | 1.890 | 1.09 |
| Decay | 107 | 1.538 | 1.657 | 0.93 |
| Return Fire | 95 | 0.449 | 0.140 | 3.20 |
| Alchemical Fire | 88 | 1.003 | 1.172 | 0.86 |
| Lightning Scroll | 35 | 0.373 | 0.369 | 1.01 |
| Focus Lens | 34 | 0.960 | 0.894 | 1.07 |
| Silence Wave | 26 | 0.209 | 0.203 | 1.03 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.041 | 7.02 |
| Drifter | Melee Charge | 68 | 0.211 | 0.053 | 4.01 |
| Rat King | Return Fire | 41 | 0.389 | 0.099 | 3.95 |
| Billy | Crushing Fists | 31 | 0.319 | 0.104 | 3.07 |
| Calico | Melee Charge | 27 | 0.170 | 0.058 | 2.94 |
| Baba | Torment Pulse | 138 | 5.029 | 1.803 | 2.79 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.211 | 2.61 |
| Haze | Lucky Shot | 90 | 0.493 | 0.194 | 2.55 |
| Nurse Harrow | Quicksilver Reload | 87 | 0.228 | 0.093 | 2.45 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.166 | 2.17 |
| Billy | Melee Charge | 48 | 0.242 | 0.127 | 1.91 |
| Paradox | Tankbuster | 146 | 0.656 | 0.346 | 1.90 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.211 | 1.89 |
| Lash | Spirit Burn | 69 | 0.946 | 0.502 | 1.88 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.096 | 1.83 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.166 | 1.81 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.109 | 1.77 |
| Drifter | Tankbuster | 101 | 0.587 | 0.345 | 1.70 |
| Abrams | Melee Charge | 129 | 0.306 | 0.189 | 1.62 |
| Nurse Harrow | Ricochet | 120 | 0.118 | 0.189 | 0.63 |
| Calico | Arctic Blast | 101 | 1.397 | 0.882 | 1.58 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.187 | 0.63 |
| Bebop | Tankbuster | 43 | 1.252 | 0.797 | 1.57 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.261 | 1.57 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.203 | 1.54 |
| Shiv | Express Shot | 124 | 0.880 | 0.571 | 1.54 |
| Infernus | Ricochet | 65 | 0.110 | 0.170 | 0.65 |
| Yamato | Melee Charge | 57 | 0.207 | 0.135 | 1.54 |
| Shiv | Lucky Shot | 44 | 0.494 | 0.330 | 1.50 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.942 | 1.46 |
| Mina | Spirit Burn | 110 | 0.926 | 0.637 | 1.45 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.238 | 1.44 |
| Venator | Ricochet | 36 | 0.114 | 0.162 | 0.71 |
| Abrams | Phantom Strike | 57 | 0.233 | 0.166 | 1.40 |
| Wraith | Ricochet | 185 | 0.133 | 0.185 | 0.71 |
| Lash | Tankbuster | 193 | 1.645 | 1.188 | 1.38 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.417 | 1.38 |
| Haze | Tesla Bullets | 47 | 0.434 | 0.323 | 1.34 |
| Shiv | Cold Front | 21 | 0.381 | 0.284 | 1.34 |
| McGinnis | Escalating Exposure | 29 | 1.974 | 1.476 | 1.34 |
