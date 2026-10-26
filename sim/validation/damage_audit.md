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
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.39 | 0.31 / 0.34 | 0.15 / 0.13 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.34 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Sinclair | 55 | 0.12 / 0.15 | 0.79 / 0.76 | 0.04 / 0.03 | 0.03 / 0.04 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.48 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.27 | 0.02 / 0.00 | 0.04 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.69 | 0.17 / 0.20 | 0.03 / 0.02 | 0.04 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.08 | 0.02 / 0.01 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.35 | 0.10 / 0.13 | 0.10 / 0.11 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.47 | 0.17 / 0.19 | 0.02 / 0.02 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.41 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Paige | 135 | 0.29 / 0.31 | 0.59 / 0.58 | 0.07 / 0.08 | 0.03 / 0.02 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.03 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.59 | 0.16 / 0.16 | 0.05 / 0.04 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.18 | 0.18 / 0.19 | 0.02 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.60 | 0.17 / 0.18 | 0.03 / 0.04 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.23 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.02 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.07 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.02 |
| Solomon | 136 | 0.25 / 0.25 | 0.64 / 0.63 | 0.08 / 0.08 | 0.02 / 0.02 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.31 | 0.62 / 0.62 | 0.05 / 0.04 | 0.03 / 0.02 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| McGinnis | Mini Turret | ability | 0.467 | 0.572 | 0.65 |
| Sinclair | Vexing Bolt | ability | 0.351 | 0.298 | 1.46 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.17 |
| Warden | Last Stand | ability | 0.138 | 0.201 | 0.64 |
| Vindicta | Assassinate | ability | 0.162 | 0.107 | 1.70 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.083 | 1.74 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.303 | 1.20 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.176 | 0.74 |
| Pocket | Affliction | ability | 0.120 | 0.158 | 0.72 |
| Celeste | Shining Wonder | ability | 0.170 | 0.141 | 1.35 |
| Viscous | Express Shot | item | 0.052 | 0.025 | 2.58 |
| Viscous | Splatter | ability | 0.285 | 0.294 | 1.18 |
| Viscous | Goo Ball | ability | 0.107 | 0.086 | 1.52 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.272 | 1.15 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.192 | 1.23 |
| Paige | Bookwyrm | ability | 0.376 | 0.362 | 1.11 |
| Viscous | Puddle Punch | ability | 0.123 | 0.112 | 1.34 |
| Paradox | Tankbuster | item | 0.074 | 0.052 | 1.62 |
| Haze | Bullet Dance | ability | 0.124 | 0.153 | 0.79 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.230 | 0.86 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.094 | 1.36 |
| Abrams | MELEE | melee | 0.424 | 0.414 | 1.08 |
| Mina | Nox Nostra | ability | 0.128 | 0.154 | 0.80 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.171 | 1.20 |
| Viscous | MELEE | melee | 0.047 | 0.085 | 0.68 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.137 | 0.79 |
| Shiv | Killing Blow | ability | 0.056 | 0.034 | 1.76 |
| Baba | MELEE | melee | 0.124 | 0.114 | 1.29 |
| Vindicta | Crow Familiar | ability | 0.155 | 0.143 | 1.22 |
| Apollo | MELEE | melee | 0.171 | 0.151 | 1.18 |
| Lash | Ground Strike | ability | 0.350 | 0.352 | 1.08 |
| Graves | Jar of Dead | ability | 0.212 | 0.233 | 0.89 |
| Calico | MELEE | melee | 0.149 | 0.127 | 1.19 |
| Haze | Fixation | ability | 0.304 | 0.323 | 0.92 |
| The Doorman | Call Bell | ability | 0.474 | 0.463 | 1.06 |
| Holliday | Powder Keg | ability | 0.397 | 0.385 | 1.07 |
| Vyper | Split Shot | item | 0.110 | 0.089 | 1.26 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.320 | 0.93 |
| Lady Geist | Malice | ability | 0.144 | 0.173 | 0.87 |
| Kelvin | MELEE | melee | 0.034 | 0.017 | 2.06 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1887 | 1.093 | 0.849 | 1.29 |
| Mystic Burst | 1691 | 0.292 | 0.236 | 1.24 |
| Quicksilver Reload | 1114 | 0.171 | 0.141 | 1.21 |
| Toxic Bullets | 875 | 0.530 | 0.532 | 1.00 |
| Spirit Snatch | 856 | 0.411 | 0.409 | 1.00 |
| Torment Pulse | 814 | 1.625 | 1.290 | 1.26 |
| Stalker | 794 | 0.219 | 0.207 | 1.06 |
| Spirit Strike | 710 | 0.291 | 0.298 | 0.98 |
| Ricochet | 695 | 0.156 | 0.179 | 0.88 |
| Spirit Burn | 685 | 0.833 | 0.599 | 1.39 |
| Mystic Shot | 673 | 0.407 | 0.340 | 1.20 |
| Escalating Exposure | 610 | 0.933 | 0.909 | 1.03 |
| Express Shot | 558 | 0.676 | 0.486 | 1.39 |
| Cold Front | 525 | 0.455 | 0.435 | 1.05 |
| Siphon Bullets | 521 | 0.248 | 0.238 | 1.04 |
| Tesla Bullets | 509 | 0.480 | 0.477 | 1.00 |
| Melee Charge | 434 | 0.254 | 0.114 | 2.24 |
| Headhunter | 410 | 0.439 | 0.442 | 0.99 |
| Capacitor | 375 | 0.696 | 0.696 | 1.00 |
| Headshot Booster | 375 | 0.213 | 0.193 | 1.10 |
| Mercurial Magnum | 340 | 0.296 | 0.286 | 1.03 |
| Rebuttal | 236 | 0.064 | 0.055 | 1.18 |
| Mystic Reverb | 211 | 1.326 | 1.565 | 0.85 |
| Lucky Shot | 200 | 0.397 | 0.222 | 1.78 |
| Arctic Blast | 171 | 1.325 | 0.816 | 1.62 |
| Split Shot | 170 | 0.257 | 0.247 | 1.04 |
| Crushing Fists | 147 | 0.307 | 0.114 | 2.70 |
| Decay | 135 | 1.566 | 1.594 | 0.98 |
| Phantom Strike | 125 | 0.315 | 0.229 | 1.38 |
| Scourge | 121 | 2.131 | 1.817 | 1.17 |
| Alchemical Fire | 111 | 0.994 | 0.993 | 1.00 |
| Return Fire | 96 | 0.445 | 0.124 | 3.58 |
| Lightning Scroll | 49 | 0.423 | 0.266 | 1.59 |
| Focus Lens | 39 | 0.941 | 0.866 | 1.09 |
| Silence Wave | 33 | 0.238 | 0.201 | 1.18 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.049 | 5.86 |
| Apollo | Melee Charge | 58 | 0.421 | 0.082 | 5.16 |
| Rat King | Return Fire | 41 | 0.389 | 0.082 | 4.76 |
| Drifter | Melee Charge | 68 | 0.211 | 0.054 | 3.87 |
| Billy | Crushing Fists | 31 | 0.319 | 0.103 | 3.09 |
| Baba | Torment Pulse | 138 | 5.029 | 1.784 | 2.82 |
| Calico | Melee Charge | 27 | 0.170 | 0.063 | 2.68 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.214 | 2.58 |
| Haze | Lucky Shot | 91 | 0.492 | 0.197 | 2.50 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.092 | 2.46 |
| Violet | Torment Pulse | 69 | 0.825 | 0.361 | 2.29 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.170 | 2.12 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.143 | 2.09 |
| Billy | Melee Charge | 48 | 0.242 | 0.121 | 1.99 |
| Paradox | Tankbuster | 146 | 0.656 | 0.336 | 1.95 |
| Apollo | Mystic Burst | 66 | 0.616 | 0.331 | 1.86 |
| Violet | Mystic Burst | 66 | 0.227 | 0.122 | 1.85 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.218 | 1.83 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.098 | 1.79 |
| Drifter | Tankbuster | 101 | 0.587 | 0.330 | 1.78 |
| Violet | Tankbuster | 206 | 1.178 | 0.674 | 1.75 |
| Yamato | Melee Charge | 57 | 0.207 | 0.120 | 1.74 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.111 | 1.73 |
| Lash | Spirit Burn | 69 | 0.946 | 0.560 | 1.69 |
| Abrams | Melee Charge | 129 | 0.306 | 0.186 | 1.65 |
| Kelvin | Escalating Exposure | 40 | 4.081 | 2.515 | 1.62 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.215 | 0.62 |
| Bebop | Tankbuster | 43 | 1.252 | 0.776 | 1.61 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.259 | 1.58 |
| Shiv | Express Shot | 125 | 0.882 | 0.560 | 1.58 |
| Solomon | Spirit Burn | 23 | 1.019 | 0.651 | 1.56 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.202 | 1.55 |
| Violet | Mystic Shot | 170 | 0.473 | 0.307 | 1.54 |
| Yamato | Express Shot | 46 | 0.925 | 0.602 | 1.54 |
| Infernus | Ricochet | 66 | 0.110 | 0.170 | 0.65 |
| Calico | Arctic Blast | 102 | 1.394 | 0.909 | 1.53 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.324 | 1.53 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.186 | 0.67 |
| Violet | Spirit Burn | 45 | 0.914 | 0.612 | 1.49 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.232 | 1.48 |
