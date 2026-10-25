# Sim vs real damage mix audit

Sample: 600 matches, 5773 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.24 | 0.29 / 0.44 | 0.16 / 0.13 | 0.29 / 0.19 | 0.15 |
| The Doorman | 2 | 0.20 / 0.12 | 0.57 / 0.52 | 0.22 / 0.34 | 0.01 / 0.02 | 0.13 |
| Mirage | 45 | 0.31 / 0.36 | 0.48 / 0.39 | 0.17 / 0.23 | 0.02 / 0.03 | 0.11 |
| Pocket | 117 | 0.14 / 0.12 | 0.66 / 0.59 | 0.16 / 0.27 | 0.02 / 0.02 | 0.10 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.32 | 0.17 / 0.26 | 0.18 / 0.19 | 0.09 |
| McGinnis | 49 | 0.20 / 0.17 | 0.64 / 0.73 | 0.12 / 0.08 | 0.02 / 0.00 | 0.09 |
| Grey Talon | 103 | 0.31 / 0.28 | 0.49 / 0.46 | 0.16 / 0.24 | 0.01 / 0.01 | 0.09 |
| Vyper | 78 | 0.46 / 0.51 | 0.26 / 0.20 | 0.25 / 0.27 | 0.02 / 0.02 | 0.08 |
| Kelvin | 12 | 0.09 / 0.10 | 0.65 / 0.60 | 0.22 / 0.29 | 0.02 / 0.01 | 0.08 |
| Rem | 23 | 0.25 / 0.26 | 0.54 / 0.49 | 0.16 / 0.21 | 0.04 / 0.04 | 0.07 |
| Paradox | 168 | 0.24 / 0.29 | 0.48 / 0.45 | 0.23 / 0.21 | 0.03 / 0.05 | 0.07 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.41 | 0.31 / 0.34 | 0.15 / 0.10 | 0.07 |
| Drifter | 186 | 0.26 / 0.29 | 0.44 / 0.48 | 0.17 / 0.13 | 0.11 / 0.10 | 0.07 |
| Paige | 58 | 0.35 / 0.39 | 0.50 / 0.46 | 0.11 / 0.13 | 0.03 / 0.02 | 0.06 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.53 | 0.28 / 0.23 | 0.05 / 0.07 | 0.06 |
| Abrams | 138 | 0.23 / 0.26 | 0.20 / 0.21 | 0.13 / 0.14 | 0.42 / 0.38 | 0.06 |
| Seven | 95 | 0.20 / 0.23 | 0.66 / 0.62 | 0.10 / 0.12 | 0.02 / 0.02 | 0.06 |
| Victor | 129 | 0.15 / 0.17 | 0.64 / 0.58 | 0.16 / 0.20 | 0.03 / 0.03 | 0.06 |
| Violet | 4 | 0.29 / 0.25 | 0.65 / 0.69 | 0.02 / 0.04 | 0.01 / 0.01 | 0.06 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.46 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Solomon | 42 | 0.37 / 0.41 | 0.54 / 0.49 | 0.07 / 0.08 | 0.01 / 0.02 | 0.05 |
| Warden | 33 | 0.52 / 0.50 | 0.31 / 0.36 | 0.11 / 0.11 | 0.03 / 0.02 | 0.05 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.50 | 0.27 / 0.31 | 0.02 / 0.00 | 0.05 |
| Infernus | 173 | 0.23 / 0.24 | 0.60 / 0.57 | 0.13 / 0.17 | 0.03 / 0.02 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.05 |
| Deadman Danny | 357 | 0.16 / 0.13 | 0.63 / 0.65 | 0.18 / 0.21 | 0.01 / 0.01 | 0.04 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.59 | 0.17 / 0.18 | 0.04 / 0.04 | 0.04 |
| Silver | 100 | 0.41 / 0.42 | 0.37 / 0.35 | 0.10 / 0.13 | 0.10 / 0.10 | 0.04 |
| Bebop | 254 | 0.18 / 0.20 | 0.56 / 0.57 | 0.19 / 0.18 | 0.05 / 0.04 | 0.04 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.34 | 0.26 / 0.29 | 0.04 / 0.04 | 0.04 |
| Mina | 198 | 0.12 / 0.11 | 0.66 / 0.65 | 0.19 / 0.22 | 0.01 / 0.01 | 0.03 |
| Wraith | 283 | 0.32 / 0.32 | 0.41 / 0.40 | 0.24 / 0.27 | 0.01 / 0.01 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.65 | 0.08 / 0.08 | 0.05 / 0.03 | 0.03 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.56 | 0.25 / 0.27 | 0.03 / 0.03 | 0.03 |
| Holliday | 73 | 0.27 / 0.29 | 0.54 / 0.54 | 0.13 / 0.12 | 0.05 / 0.04 | 0.03 |
| Venator | 257 | 0.48 / 0.50 | 0.40 / 0.40 | 0.03 / 0.02 | 0.07 / 0.08 | 0.03 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.48 | 0.39 / 0.41 | 0.05 / 0.03 | 0.02 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Baba | 146 | 0.07 / 0.07 | 0.54 / 0.53 | 0.25 / 0.26 | 0.12 / 0.14 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.29 | 0.62 / 0.64 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.75 | 0.02 / 0.03 | 0.03 / 0.04 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.22 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| The Doorman | Tankbuster | item | 0.165 | 0.277 | 0.38 |
| McGinnis | Mini Turret | ability | 0.467 | 0.584 | 0.68 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.198 | 1.69 |
| Pocket | Tankbuster | item | 0.079 | 0.156 | 0.42 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.262 | 0.64 |
| Paradox | Express Shot | item | 0.027 | 0.099 | 0.33 |
| Apollo | MELEE | melee | 0.287 | 0.193 | 1.46 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.296 | 0.70 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.116 | 0.41 |
| Abrams | MELEE | melee | 0.424 | 0.380 | 1.26 |
| Kelvin | Arctic Beam | ability | 0.397 | 0.361 | 1.28 |
| Apollo | Flawless Advance | ability | 0.141 | 0.215 | 0.64 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.032 | 2.51 |
| Solomon | Develop Queen | ability | 0.141 | 0.083 | 1.88 |
| Vindicta | Assassinate | ability | 0.162 | 0.109 | 1.65 |
| Paradox | Tankbuster | item | 0.074 | 0.030 | 2.98 |
| Victor | Pain Battery | ability | 0.276 | 0.231 | 1.32 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.155 | 0.61 |
| Sinclair | Audience Participation | ability | 0.194 | 0.269 | 0.76 |
| Grey Talon | Tankbuster | item | 0.071 | 0.118 | 0.54 |
| Vyper | Lethal Venom | ability | 0.112 | 0.066 | 1.90 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.054 | 0.28 |
| Calico | MELEE | melee | 0.149 | 0.102 | 1.57 |
| Grey Talon | Mystic Reverb | item | 0.024 | 0.061 | 0.35 |
| The Doorman | Call Bell | ability | 0.475 | 0.347 | 0.87 |
| Bebop | Hyper Beam | ability | 0.129 | 0.089 | 1.64 |
| Viscous | Express Shot | item | 0.052 | 0.019 | 3.32 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.313 | 1.22 |
| Paradox | Mystic Reverb | item | 0.063 | 0.028 | 2.65 |
| Baba | Torment Pulse | item | 0.170 | 0.119 | 1.42 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.023 | 2.80 |
| Celeste | Shining Wonder | ability | 0.170 | 0.141 | 1.40 |
| Infernus | Flame Dash | ability | 0.216 | 0.176 | 1.30 |
| Seven | Lightning Ball | ability | 0.198 | 0.174 | 1.33 |
| Violet | Living Ink | ability | 0.277 | 0.292 | 0.83 |
| Mina | Tankbuster | item | 0.088 | 0.127 | 0.65 |
| Paige | Bookwyrm | ability | 0.320 | 0.304 | 1.18 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.236 | 1.22 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1522 | 1.039 | 0.932 | 1.11 |
| Mystic Burst | 1465 | 0.284 | 0.261 | 1.09 |
| Quicksilver Reload | 1105 | 0.171 | 0.162 | 1.06 |
| Toxic Bullets | 862 | 0.532 | 0.545 | 0.98 |
| Spirit Snatch | 793 | 0.400 | 0.352 | 1.14 |
| Stalker | 790 | 0.219 | 0.219 | 1.00 |
| Torment Pulse | 707 | 1.663 | 1.502 | 1.11 |
| Ricochet | 695 | 0.156 | 0.181 | 0.86 |
| Spirit Strike | 675 | 0.291 | 0.323 | 0.90 |
| Spirit Burn | 579 | 0.773 | 0.622 | 1.24 |
| Express Shot | 552 | 0.677 | 0.675 | 1.00 |
| Escalating Exposure | 542 | 0.892 | 0.868 | 1.03 |
| Siphon Bullets | 521 | 0.248 | 0.256 | 0.97 |
| Tesla Bullets | 509 | 0.480 | 0.473 | 1.01 |
| Cold Front | 505 | 0.447 | 0.445 | 1.00 |
| Mystic Shot | 497 | 0.385 | 0.374 | 1.03 |
| Headhunter | 407 | 0.440 | 0.439 | 1.00 |
| Melee Charge | 379 | 0.240 | 0.101 | 2.38 |
| Capacitor | 375 | 0.696 | 0.696 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.198 | 1.09 |
| Mercurial Magnum | 339 | 0.295 | 0.293 | 1.01 |
| Rebuttal | 212 | 0.063 | 0.047 | 1.34 |
| Mystic Reverb | 204 | 1.313 | 1.184 | 1.11 |
| Lucky Shot | 200 | 0.397 | 0.230 | 1.72 |
| Arctic Blast | 171 | 1.325 | 0.780 | 1.70 |
| Split Shot | 170 | 0.257 | 0.257 | 1.00 |
| Crushing Fists | 143 | 0.303 | 0.096 | 3.15 |
| Phantom Strike | 123 | 0.311 | 0.225 | 1.39 |
| Scourge | 110 | 2.102 | 2.163 | 0.97 |
| Decay | 107 | 1.538 | 1.696 | 0.91 |
| Return Fire | 95 | 0.449 | 0.127 | 3.53 |
| Alchemical Fire | 88 | 1.003 | 1.109 | 0.90 |
| Focus Lens | 36 | 0.957 | 0.847 | 1.13 |
| Lightning Scroll | 35 | 0.373 | 0.364 | 1.03 |
| Silence Wave | 26 | 0.209 | 0.211 | 0.99 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.030 | 9.62 |
| Drifter | Melee Charge | 68 | 0.211 | 0.045 | 4.73 |
| Calico | Melee Charge | 27 | 0.170 | 0.041 | 4.12 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.075 | 4.01 |
| Rat King | Return Fire | 41 | 0.389 | 0.101 | 3.84 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 2.847 | 0.26 |
| Paradox | Tankbuster | 146 | 0.656 | 0.185 | 3.55 |
| Yamato | Melee Charge | 57 | 0.207 | 0.062 | 3.36 |
| Bebop | Spirit Strike | 186 | 0.274 | 0.087 | 3.15 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.175 | 3.15 |
| Billy | Crushing Fists | 31 | 0.319 | 0.107 | 2.99 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.061 | 2.88 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.079 | 2.86 |
| Paradox | Mystic Reverb | 86 | 1.290 | 0.454 | 2.84 |
| Paradox | Express Shot | 143 | 0.229 | 0.603 | 0.38 |
| Haze | Lucky Shot | 91 | 0.492 | 0.197 | 2.50 |
| Mo & Krill | Tankbuster | 118 | 3.292 | 1.377 | 2.39 |
| Vyper | Quicksilver Reload | 31 | 0.057 | 0.130 | 0.44 |
| Drifter | Tankbuster | 101 | 0.587 | 0.260 | 2.25 |
| Bebop | Tankbuster | 43 | 1.252 | 0.556 | 2.25 |
| Bebop | Spirit Snatch | 191 | 0.342 | 0.153 | 2.24 |
| McGinnis | Escalating Exposure | 29 | 1.974 | 0.894 | 2.21 |
| Deadman Danny | Cold Front | 46 | 0.236 | 0.511 | 0.46 |
| Pocket | Tankbuster | 110 | 1.140 | 2.431 | 0.47 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.149 | 2.10 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.169 | 2.03 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.202 | 1.97 |
| Billy | Melee Charge | 48 | 0.242 | 0.123 | 1.96 |
| Holliday | Tankbuster | 48 | 0.959 | 0.504 | 1.90 |
| Yamato | Spirit Snatch | 41 | 0.399 | 0.739 | 0.54 |
| Yamato | Mystic Shot | 35 | 0.364 | 0.662 | 0.55 |
| Baba | Torment Pulse | 138 | 5.029 | 2.765 | 1.82 |
| Haze | Quicksilver Reload | 24 | 0.044 | 0.079 | 0.55 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.200 | 1.80 |
| Pocket | Cold Front | 59 | 0.339 | 0.607 | 0.56 |
| Abrams | Melee Charge | 129 | 0.306 | 0.171 | 1.79 |
| Calico | Mystic Shot | 30 | 0.381 | 0.680 | 0.56 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.108 | 1.78 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.780 | 1.77 |
| Yamato | Torment Pulse | 32 | 1.066 | 1.878 | 0.57 |
