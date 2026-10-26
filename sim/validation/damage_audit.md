# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Warden | 33 | 0.52 / 0.47 | 0.31 / 0.40 | 0.11 / 0.10 | 0.03 / 0.02 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.12 | 0.09 |
| McGinnis | 49 | 0.20 / 0.15 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.01 | 0.08 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.21 | 0.04 / 0.04 | 0.07 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.07 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.05 |
| Calico | 110 | 0.13 / 0.13 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.13 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.11 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Sinclair | 55 | 0.12 / 0.15 | 0.79 / 0.76 | 0.04 / 0.04 | 0.03 / 0.04 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.31 | 0.49 / 0.48 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Apollo | 92 | 0.11 / 0.10 | 0.53 / 0.57 | 0.17 / 0.15 | 0.17 / 0.17 | 0.04 |
| Silver | 100 | 0.41 / 0.39 | 0.37 / 0.38 | 0.10 / 0.12 | 0.10 / 0.10 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.04 | 0.03 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.68 | 0.17 / 0.20 | 0.03 / 0.03 | 0.03 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.29 | 0.04 / 0.04 | 0.03 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.08 | 0.02 / 0.02 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.03 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.08 | 0.05 / 0.04 | 0.03 |
| Mirage | 45 | 0.31 / 0.31 | 0.48 / 0.47 | 0.17 / 0.19 | 0.02 / 0.02 | 0.03 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.03 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.19 | 0.18 / 0.19 | 0.03 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Paige | 135 | 0.29 / 0.31 | 0.59 / 0.58 | 0.07 / 0.08 | 0.03 / 0.03 | 0.02 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.60 | 0.17 / 0.18 | 0.03 / 0.04 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.19 | 0.13 / 0.13 | 0.42 / 0.43 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Paradox | 168 | 0.24 / 0.24 | 0.48 / 0.48 | 0.23 / 0.25 | 0.03 / 0.03 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.15 | 0.22 / 0.23 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Venator | 257 | 0.48 / 0.50 | 0.40 / 0.40 | 0.03 / 0.02 | 0.07 / 0.08 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.20 | 0.05 / 0.05 | 0.02 |
| Solomon | 136 | 0.25 / 0.26 | 0.64 / 0.63 | 0.08 / 0.08 | 0.02 / 0.02 | 0.02 |
| Vindicta | 131 | 0.44 / 0.44 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.58 | 0.16 / 0.16 | 0.05 / 0.05 | 0.01 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.61 | 0.05 / 0.05 | 0.03 / 0.03 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| McGinnis | Mini Turret | ability | 0.467 | 0.565 | 0.65 |
| Sinclair | Vexing Bolt | ability | 0.351 | 0.295 | 1.47 |
| Baba | Torment Pulse | item | 0.170 | 0.094 | 2.17 |
| Warden | Last Stand | ability | 0.138 | 0.215 | 0.58 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.090 | 1.57 |
| Celeste | Shining Wonder | ability | 0.170 | 0.141 | 1.38 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.175 | 0.74 |
| Viscous | Express Shot | item | 0.052 | 0.024 | 2.63 |
| Pocket | Affliction | ability | 0.120 | 0.158 | 0.73 |
| Viscous | Goo Ball | ability | 0.107 | 0.085 | 1.49 |
| The Doorman | Call Bell | ability | 0.474 | 0.461 | 1.09 |
| Viscous | MELEE | melee | 0.047 | 0.088 | 0.63 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.192 | 1.23 |
| Paige | Bookwyrm | ability | 0.376 | 0.357 | 1.11 |
| Viscous | Splatter | ability | 0.285 | 0.296 | 1.14 |
| Shiv | Killing Blow | ability | 0.056 | 0.030 | 2.02 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.169 | 1.23 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.269 | 1.14 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.227 | 0.85 |
| Haze | Bullet Dance | ability | 0.124 | 0.153 | 0.79 |
| Viscous | Puddle Punch | ability | 0.123 | 0.111 | 1.32 |
| Holliday | Powder Keg | ability | 0.397 | 0.383 | 1.09 |
| Mina | Nox Nostra | ability | 0.128 | 0.154 | 0.81 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.134 | 0.79 |
| Baba | MELEE | melee | 0.124 | 0.115 | 1.28 |
| Lash | Ground Strike | ability | 0.350 | 0.352 | 1.09 |
| Silver | ability_werewolf_frenzy | ability | 0.096 | 0.115 | 0.78 |
| Haze | Fixation | ability | 0.304 | 0.324 | 0.92 |
| Solomon | Develop Queen | ability | 0.161 | 0.141 | 1.18 |
| Graves | Jar of Dead | ability | 0.212 | 0.233 | 0.89 |
| Warden | Alchemical Flask | ability | 0.129 | 0.141 | 0.83 |
| Calico | MELEE | melee | 0.149 | 0.128 | 1.18 |
| Vyper | Split Shot | item | 0.110 | 0.090 | 1.25 |
| Lady Geist | Malice | ability | 0.144 | 0.168 | 0.87 |
| Pocket | Barrage | ability | 0.260 | 0.230 | 1.09 |
| Shiv | Slice and Dice | ability | 0.145 | 0.135 | 1.17 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.319 | 0.93 |
| Grey Talon | Tankbuster | item | 0.071 | 0.089 | 0.78 |
| Celeste | Light Eater | ability | 0.220 | 0.228 | 1.10 |
| Baba | Granny Long Legs | ability | 0.103 | 0.100 | 1.23 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1887 | 1.093 | 0.874 | 1.25 |
| Mystic Burst | 1691 | 0.292 | 0.245 | 1.20 |
| Quicksilver Reload | 1114 | 0.171 | 0.141 | 1.22 |
| Toxic Bullets | 875 | 0.530 | 0.526 | 1.01 |
| Spirit Snatch | 856 | 0.411 | 0.417 | 0.98 |
| Torment Pulse | 814 | 1.625 | 1.281 | 1.27 |
| Stalker | 794 | 0.219 | 0.195 | 1.12 |
| Spirit Strike | 710 | 0.291 | 0.314 | 0.93 |
| Ricochet | 695 | 0.156 | 0.181 | 0.86 |
| Spirit Burn | 685 | 0.833 | 0.624 | 1.34 |
| Mystic Shot | 673 | 0.407 | 0.345 | 1.18 |
| Escalating Exposure | 610 | 0.933 | 0.895 | 1.04 |
| Express Shot | 558 | 0.676 | 0.477 | 1.42 |
| Cold Front | 525 | 0.455 | 0.428 | 1.06 |
| Siphon Bullets | 521 | 0.248 | 0.235 | 1.05 |
| Tesla Bullets | 509 | 0.480 | 0.478 | 1.00 |
| Melee Charge | 434 | 0.254 | 0.135 | 1.89 |
| Headhunter | 410 | 0.439 | 0.436 | 1.01 |
| Capacitor | 375 | 0.696 | 0.689 | 1.01 |
| Headshot Booster | 375 | 0.213 | 0.189 | 1.13 |
| Mercurial Magnum | 340 | 0.296 | 0.285 | 1.04 |
| Rebuttal | 236 | 0.064 | 0.047 | 1.36 |
| Mystic Reverb | 211 | 1.326 | 1.510 | 0.88 |
| Lucky Shot | 200 | 0.397 | 0.219 | 1.81 |
| Arctic Blast | 171 | 1.325 | 0.816 | 1.62 |
| Split Shot | 170 | 0.257 | 0.253 | 1.01 |
| Crushing Fists | 147 | 0.307 | 0.134 | 2.29 |
| Decay | 135 | 1.566 | 1.518 | 1.03 |
| Phantom Strike | 125 | 0.315 | 0.224 | 1.41 |
| Scourge | 121 | 2.131 | 1.798 | 1.19 |
| Alchemical Fire | 111 | 0.994 | 0.956 | 1.04 |
| Return Fire | 96 | 0.445 | 0.122 | 3.64 |
| Lightning Scroll | 49 | 0.423 | 0.266 | 1.59 |
| Focus Lens | 39 | 0.941 | 0.822 | 1.15 |
| Silence Wave | 33 | 0.238 | 0.198 | 1.20 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.049 | 5.91 |
| Rat King | Return Fire | 41 | 0.389 | 0.081 | 4.80 |
| Apollo | Melee Charge | 58 | 0.421 | 0.095 | 4.43 |
| Drifter | Melee Charge | 68 | 0.211 | 0.053 | 3.97 |
| Billy | Crushing Fists | 31 | 0.319 | 0.105 | 3.04 |
| Baba | Torment Pulse | 138 | 5.029 | 1.785 | 2.82 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.115 | 2.60 |
| Haze | Lucky Shot | 91 | 0.492 | 0.197 | 2.50 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.091 | 2.50 |
| Calico | Melee Charge | 27 | 0.170 | 0.070 | 2.43 |
| Violet | Torment Pulse | 69 | 0.825 | 0.360 | 2.29 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.169 | 2.13 |
| Drifter | Tankbuster | 101 | 0.587 | 0.315 | 1.86 |
| Mo & Krill | Rebuttal | 22 | 0.160 | 0.086 | 1.86 |
| Apollo | Mystic Burst | 66 | 0.616 | 0.332 | 1.85 |
| Violet | Mystic Burst | 66 | 0.227 | 0.123 | 1.84 |
| Billy | Melee Charge | 48 | 0.242 | 0.136 | 1.79 |
| Kelvin | Escalating Exposure | 40 | 4.081 | 2.320 | 1.76 |
| Violet | Tankbuster | 206 | 1.178 | 0.672 | 1.75 |
| Lash | Spirit Burn | 69 | 0.946 | 0.541 | 1.75 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.114 | 1.70 |
| Yamato | Express Shot | 46 | 0.925 | 0.571 | 1.62 |
| Shiv | Express Shot | 125 | 0.882 | 0.549 | 1.61 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.257 | 1.60 |
| Solomon | Spirit Burn | 23 | 1.019 | 0.641 | 1.59 |
| Violet | Mystic Shot | 170 | 0.473 | 0.305 | 1.55 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.321 | 1.54 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.190 | 0.65 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.153 | 1.53 |
| Violet | Spirit Burn | 45 | 0.914 | 0.600 | 1.52 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.292 | 1.51 |
| Infernus | Ricochet | 66 | 0.110 | 0.166 | 0.66 |
| Calico | Arctic Blast | 102 | 1.394 | 0.927 | 1.50 |
| Mina | Spirit Burn | 110 | 0.926 | 0.621 | 1.49 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.940 | 1.47 |
| The Doorman | Tankbuster | 27 | 2.276 | 1.559 | 1.46 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.097 | 0.69 |
| Baba | Spirit Snatch | 84 | 2.122 | 1.460 | 1.45 |
| Venator | Ricochet | 36 | 0.114 | 0.166 | 0.69 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.280 | 1.43 |
