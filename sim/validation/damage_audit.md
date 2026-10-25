# Sim vs real damage mix audit

Sample: 600 matches, 6429 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Rem | 23 | 0.25 / 0.26 | 0.54 / 0.46 | 0.16 / 0.24 | 0.04 / 0.04 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.11 | 0.08 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.22 | 0.04 / 0.05 | 0.07 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.43 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.06 |
| Warden | 33 | 0.52 / 0.50 | 0.31 / 0.37 | 0.11 / 0.10 | 0.03 / 0.02 | 0.06 |
| Vindicta | 131 | 0.44 / 0.49 | 0.49 / 0.45 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.57 | 0.17 / 0.15 | 0.17 / 0.15 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.39 | 0.31 / 0.34 | 0.15 / 0.13 | 0.04 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.69 | 0.17 / 0.20 | 0.03 / 0.02 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.49 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.29 | 0.04 / 0.04 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.48 | 0.17 / 0.19 | 0.02 / 0.02 | 0.03 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.02 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.75 | 0.02 / 0.03 | 0.03 / 0.04 | 0.03 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.36 | 0.10 / 0.12 | 0.10 / 0.10 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.60 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.42 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.16 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.18 | 0.18 / 0.19 | 0.02 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.27 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.60 | 0.17 / 0.18 | 0.03 / 0.04 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Solomon | 136 | 0.25 / 0.26 | 0.64 / 0.63 | 0.08 / 0.09 | 0.02 / 0.02 | 0.02 |
| Paige | 58 | 0.35 / 0.36 | 0.50 / 0.51 | 0.11 / 0.11 | 0.03 / 0.02 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.62 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.07 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.22 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| McGinnis | Mini Turret | ability | 0.467 | 0.564 | 0.68 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.17 |
| Vindicta | Assassinate | ability | 0.162 | 0.107 | 1.70 |
| Rem | Tankbuster | item | 0.063 | 0.122 | 0.53 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.303 | 1.22 |
| Celeste | Shining Wonder | ability | 0.170 | 0.136 | 1.40 |
| Viscous | Express Shot | item | 0.052 | 0.020 | 2.98 |
| Warden | Last Stand | ability | 0.138 | 0.177 | 0.74 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.176 | 0.75 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.100 | 1.44 |
| Pocket | Affliction | ability | 0.120 | 0.157 | 0.73 |
| Rem | Pillow Toss | ability | 0.410 | 0.375 | 1.12 |
| Viscous | MELEE | melee | 0.047 | 0.087 | 0.62 |
| Rem | Decay | item | 0.026 | 0.056 | 0.48 |
| Sinclair | Spectral Assistant | ability | 0.200 | 0.175 | 1.23 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.273 | 1.15 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.091 | 1.42 |
| Rem | Naptime | ability | 0.115 | 0.086 | 1.38 |
| Lash | Ground Strike | ability | 0.350 | 0.350 | 1.11 |
| Mina | Nox Nostra | ability | 0.128 | 0.157 | 0.79 |
| Paradox | Tankbuster | item | 0.074 | 0.053 | 1.62 |
| Viscous | Splatter | ability | 0.285 | 0.291 | 1.13 |
| Solomon | Develop Queen | ability | 0.161 | 0.133 | 1.24 |
| Viscous | Puddle Punch | ability | 0.123 | 0.107 | 1.32 |
| Shiv | Killing Blow | ability | 0.056 | 0.032 | 1.85 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.306 | 1.11 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.171 | 1.20 |
| Baba | MELEE | melee | 0.124 | 0.113 | 1.30 |
| Haze | Bullet Dance | ability | 0.124 | 0.151 | 0.81 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.225 | 0.87 |
| Abrams | MELEE | melee | 0.424 | 0.418 | 1.07 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.138 | 0.81 |
| Calico | MELEE | melee | 0.149 | 0.125 | 1.21 |
| Apollo | MELEE | melee | 0.171 | 0.155 | 1.18 |
| The Doorman | Call Bell | ability | 0.474 | 0.462 | 1.06 |
| Graves | Jar of Dead | ability | 0.212 | 0.232 | 0.89 |
| Viscous | Goo Ball | ability | 0.107 | 0.097 | 1.27 |
| Shiv | Slice and Dice | ability | 0.145 | 0.131 | 1.19 |
| Grey Talon | Tankbuster | item | 0.071 | 0.090 | 0.76 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.318 | 0.93 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1865 | 1.087 | 0.855 | 1.27 |
| Mystic Burst | 1669 | 0.292 | 0.235 | 1.24 |
| Quicksilver Reload | 1114 | 0.171 | 0.142 | 1.21 |
| Toxic Bullets | 875 | 0.530 | 0.526 | 1.01 |
| Spirit Snatch | 856 | 0.411 | 0.405 | 1.01 |
| Torment Pulse | 812 | 1.622 | 1.285 | 1.26 |
| Stalker | 794 | 0.219 | 0.203 | 1.08 |
| Spirit Strike | 710 | 0.291 | 0.303 | 0.96 |
| Ricochet | 695 | 0.156 | 0.176 | 0.89 |
| Spirit Burn | 675 | 0.827 | 0.582 | 1.42 |
| Mystic Shot | 673 | 0.407 | 0.348 | 1.17 |
| Escalating Exposure | 605 | 0.928 | 0.903 | 1.03 |
| Express Shot | 553 | 0.677 | 0.495 | 1.37 |
| Cold Front | 521 | 0.453 | 0.423 | 1.07 |
| Siphon Bullets | 521 | 0.248 | 0.242 | 1.02 |
| Tesla Bullets | 509 | 0.480 | 0.478 | 1.00 |
| Melee Charge | 433 | 0.255 | 0.113 | 2.26 |
| Headhunter | 410 | 0.439 | 0.439 | 1.00 |
| Capacitor | 375 | 0.696 | 0.693 | 1.00 |
| Headshot Booster | 374 | 0.214 | 0.192 | 1.11 |
| Mercurial Magnum | 340 | 0.296 | 0.286 | 1.03 |
| Rebuttal | 232 | 0.064 | 0.054 | 1.20 |
| Mystic Reverb | 207 | 1.320 | 1.553 | 0.85 |
| Lucky Shot | 200 | 0.397 | 0.225 | 1.76 |
| Arctic Blast | 171 | 1.325 | 0.808 | 1.64 |
| Split Shot | 170 | 0.257 | 0.251 | 1.02 |
| Crushing Fists | 147 | 0.307 | 0.110 | 2.79 |
| Decay | 126 | 1.500 | 1.632 | 0.92 |
| Phantom Strike | 125 | 0.315 | 0.228 | 1.38 |
| Scourge | 117 | 2.095 | 1.780 | 1.18 |
| Alchemical Fire | 105 | 0.971 | 1.040 | 0.93 |
| Return Fire | 96 | 0.445 | 0.135 | 3.31 |
| Lightning Scroll | 41 | 0.376 | 0.290 | 1.30 |
| Focus Lens | 39 | 0.941 | 0.828 | 1.14 |
| Silence Wave | 29 | 0.232 | 0.193 | 1.20 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.039 | 7.35 |
| Apollo | Melee Charge | 58 | 0.421 | 0.076 | 5.54 |
| Rat King | Return Fire | 41 | 0.389 | 0.095 | 4.10 |
| Drifter | Melee Charge | 68 | 0.211 | 0.054 | 3.91 |
| Billy | Crushing Fists | 31 | 0.319 | 0.099 | 3.24 |
| Calico | Melee Charge | 27 | 0.170 | 0.057 | 3.00 |
| Baba | Torment Pulse | 138 | 5.029 | 1.782 | 2.82 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.210 | 2.63 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.090 | 2.52 |
| Haze | Lucky Shot | 91 | 0.492 | 0.200 | 2.46 |
| Violet | Torment Pulse | 69 | 0.825 | 0.359 | 2.30 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.136 | 2.20 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.167 | 2.16 |
| Paradox | Tankbuster | 146 | 0.656 | 0.340 | 1.93 |
| Lash | Spirit Burn | 69 | 0.946 | 0.492 | 1.92 |
| Yamato | Melee Charge | 57 | 0.207 | 0.108 | 1.92 |
| Billy | Melee Charge | 48 | 0.242 | 0.126 | 1.92 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.213 | 1.87 |
| Apollo | Mystic Burst | 66 | 0.616 | 0.330 | 1.86 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.097 | 1.81 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.108 | 1.79 |
| Drifter | Tankbuster | 101 | 0.587 | 0.341 | 1.72 |
| Kelvin | Escalating Exposure | 40 | 4.081 | 2.413 | 1.69 |
| Abrams | Melee Charge | 129 | 0.306 | 0.189 | 1.62 |
| Bebop | Tankbuster | 43 | 1.252 | 0.785 | 1.59 |
| Violet | Mystic Burst | 66 | 0.227 | 0.143 | 1.58 |
| Shiv | Express Shot | 125 | 0.882 | 0.567 | 1.56 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.170 | 0.64 |
| Infernus | Ricochet | 66 | 0.110 | 0.172 | 0.64 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.264 | 1.55 |
| Calico | Arctic Blast | 102 | 1.394 | 0.903 | 1.54 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.203 | 1.54 |
| Yamato | Express Shot | 46 | 0.925 | 0.601 | 1.54 |
| Solomon | Spirit Burn | 23 | 1.019 | 0.667 | 1.53 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.330 | 1.50 |
| Mina | Spirit Burn | 110 | 0.926 | 0.619 | 1.50 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.184 | 0.67 |
| Violet | Tankbuster | 206 | 1.178 | 0.799 | 1.47 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.951 | 1.45 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.162 | 1.45 |
