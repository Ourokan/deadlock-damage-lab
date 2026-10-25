# Sim vs real damage mix audit

Sample: 600 matches, 5623 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.24 | 0.29 / 0.44 | 0.16 / 0.13 | 0.29 / 0.20 | 0.14 |
| Mirage | 45 | 0.31 / 0.35 | 0.48 / 0.39 | 0.17 / 0.23 | 0.02 / 0.03 | 0.11 |
| Grey Talon | 103 | 0.31 / 0.26 | 0.49 / 0.46 | 0.16 / 0.26 | 0.01 / 0.01 | 0.10 |
| Pocket | 117 | 0.14 / 0.12 | 0.66 / 0.60 | 0.16 / 0.27 | 0.02 / 0.01 | 0.10 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.32 | 0.17 / 0.25 | 0.18 / 0.20 | 0.10 |
| The Doorman | 2 | 0.20 / 0.10 | 0.57 / 0.64 | 0.22 / 0.23 | 0.01 / 0.02 | 0.09 |
| Rem | 23 | 0.25 / 0.26 | 0.54 / 0.47 | 0.16 / 0.23 | 0.04 / 0.04 | 0.09 |
| McGinnis | 49 | 0.20 / 0.17 | 0.64 / 0.72 | 0.12 / 0.09 | 0.02 / 0.00 | 0.08 |
| Vyper | 78 | 0.46 / 0.51 | 0.26 / 0.21 | 0.25 / 0.27 | 0.02 / 0.02 | 0.07 |
| Kelvin | 12 | 0.09 / 0.11 | 0.65 / 0.61 | 0.22 / 0.27 | 0.02 / 0.02 | 0.07 |
| Warden | 33 | 0.52 / 0.49 | 0.31 / 0.38 | 0.11 / 0.11 | 0.03 / 0.02 | 0.07 |
| Paige | 58 | 0.35 / 0.39 | 0.50 / 0.46 | 0.11 / 0.13 | 0.03 / 0.02 | 0.07 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.35 | 0.15 / 0.10 | 0.06 |
| Viscous | 29 | 0.13 / 0.17 | 0.51 / 0.52 | 0.28 / 0.23 | 0.05 / 0.07 | 0.06 |
| Paradox | 168 | 0.24 / 0.29 | 0.48 / 0.45 | 0.23 / 0.22 | 0.03 / 0.05 | 0.06 |
| Victor | 129 | 0.15 / 0.17 | 0.64 / 0.58 | 0.16 / 0.20 | 0.03 / 0.03 | 0.06 |
| Seven | 95 | 0.20 / 0.23 | 0.66 / 0.62 | 0.10 / 0.13 | 0.02 / 0.02 | 0.06 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.48 | 0.17 / 0.14 | 0.11 / 0.10 | 0.06 |
| Abrams | 138 | 0.23 / 0.26 | 0.20 / 0.21 | 0.13 / 0.14 | 0.42 / 0.38 | 0.06 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.61 | 0.19 / 0.17 | 0.05 / 0.03 | 0.05 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.50 | 0.27 / 0.31 | 0.02 / 0.00 | 0.05 |
| Infernus | 173 | 0.23 / 0.24 | 0.60 / 0.57 | 0.13 / 0.17 | 0.03 / 0.02 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.50 | 0.07 / 0.08 | 0.01 / 0.02 | 0.05 |
| Vindicta | 131 | 0.44 / 0.47 | 0.49 / 0.46 | 0.05 / 0.06 | 0.01 / 0.01 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.58 | 0.17 / 0.18 | 0.04 / 0.04 | 0.04 |
| Deadman Danny | 357 | 0.16 / 0.13 | 0.63 / 0.65 | 0.18 / 0.21 | 0.01 / 0.01 | 0.04 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.33 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Sinclair | 20 | 0.17 / 0.19 | 0.76 / 0.73 | 0.02 / 0.03 | 0.03 / 0.04 | 0.04 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.65 | 0.19 / 0.22 | 0.01 / 0.01 | 0.03 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.35 | 0.10 / 0.13 | 0.10 / 0.10 | 0.03 |
| Wraith | 283 | 0.32 / 0.32 | 0.41 / 0.40 | 0.24 / 0.27 | 0.01 / 0.01 | 0.03 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.56 | 0.25 / 0.27 | 0.03 / 0.03 | 0.03 |
| Dynamo | 53 | 0.23 / 0.25 | 0.62 / 0.63 | 0.08 / 0.08 | 0.05 / 0.03 | 0.03 |
| Venator | 257 | 0.48 / 0.50 | 0.40 / 0.39 | 0.03 / 0.02 | 0.07 / 0.08 | 0.03 |
| Holliday | 73 | 0.27 / 0.29 | 0.54 / 0.54 | 0.13 / 0.12 | 0.05 / 0.05 | 0.03 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.47 | 0.39 / 0.41 | 0.05 / 0.03 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.42 | 0.14 / 0.16 | 0.22 / 0.21 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.63 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.48 | 0.16 / 0.16 | 0.08 / 0.08 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.61 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.57 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| The Doorman | Call Bell | ability | 0.475 | 0.400 | 0.63 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.095 | 0.13 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.146 | 0.27 |
| McGinnis | Mini Turret | ability | 0.467 | 0.569 | 0.72 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.207 | 1.58 |
| Pocket | Tankbuster | item | 0.079 | 0.150 | 0.44 |
| The Doorman | Tankbuster | item | 0.165 | 0.172 | 0.51 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.259 | 0.64 |
| Paradox | Express Shot | item | 0.027 | 0.100 | 0.32 |
| Grey Talon | Tankbuster | item | 0.071 | 0.136 | 0.44 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.298 | 0.69 |
| Kelvin | Arctic Beam | ability | 0.397 | 0.362 | 1.31 |
| Victor | Pain Battery | ability | 0.276 | 0.211 | 1.46 |
| Apollo | MELEE | melee | 0.287 | 0.198 | 1.42 |
| Abrams | MELEE | melee | 0.424 | 0.383 | 1.25 |
| Apollo | Flawless Advance | ability | 0.141 | 0.213 | 0.65 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.035 | 2.30 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.017 | 3.86 |
| Paradox | Tankbuster | item | 0.074 | 0.031 | 2.84 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.154 | 0.62 |
| Warden | Last Stand | ability | 0.138 | 0.186 | 0.69 |
| Solomon | Develop Queen | ability | 0.141 | 0.095 | 1.62 |
| Grey Talon | Mystic Reverb | item | 0.024 | 0.060 | 0.33 |
| Calico | MELEE | melee | 0.149 | 0.100 | 1.54 |
| Celeste | Shining Wonder | ability | 0.170 | 0.137 | 1.45 |
| Viscous | Splatter | ability | 0.285 | 0.298 | 1.24 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.310 | 1.21 |
| Rem | Decay | item | 0.026 | 0.066 | 0.41 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.298 | 1.20 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.330 | 0.84 |
| Vyper | Lethal Venom | ability | 0.112 | 0.076 | 1.62 |
| Vindicta | Assassinate | ability | 0.162 | 0.127 | 1.38 |
| Seven | Lightning Ball | ability | 0.198 | 0.173 | 1.30 |
| Mina | Tankbuster | item | 0.088 | 0.126 | 0.67 |
| Infernus | Flame Dash | ability | 0.216 | 0.179 | 1.26 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.244 | 1.22 |
| Rem | Tankbuster | item | 0.063 | 0.104 | 0.63 |
| Deadman Danny | Tankbuster | item | 0.079 | 0.103 | 0.63 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1519 | 1.039 | 0.956 | 1.09 |
| Mystic Burst | 1461 | 0.284 | 0.265 | 1.07 |
| Quicksilver Reload | 1105 | 0.171 | 0.161 | 1.06 |
| Toxic Bullets | 861 | 0.533 | 0.555 | 0.96 |
| Stalker | 790 | 0.219 | 0.222 | 0.99 |
| Spirit Snatch | 709 | 0.367 | 0.307 | 1.20 |
| Ricochet | 695 | 0.156 | 0.183 | 0.85 |
| Spirit Burn | 574 | 0.770 | 0.635 | 1.21 |
| Torment Pulse | 569 | 1.358 | 1.383 | 0.98 |
| Spirit Strike | 561 | 0.233 | 0.218 | 1.07 |
| Express Shot | 552 | 0.677 | 0.687 | 0.98 |
| Siphon Bullets | 521 | 0.248 | 0.252 | 0.98 |
| Escalating Exposure | 520 | 0.875 | 0.840 | 1.04 |
| Tesla Bullets | 509 | 0.480 | 0.481 | 1.00 |
| Cold Front | 505 | 0.447 | 0.445 | 1.00 |
| Mystic Shot | 495 | 0.385 | 0.381 | 1.01 |
| Headhunter | 407 | 0.440 | 0.434 | 1.01 |
| Melee Charge | 379 | 0.240 | 0.106 | 2.27 |
| Capacitor | 375 | 0.696 | 0.699 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.198 | 1.09 |
| Mercurial Magnum | 339 | 0.295 | 0.293 | 1.01 |
| Rebuttal | 210 | 0.063 | 0.042 | 1.49 |
| Mystic Reverb | 204 | 1.313 | 1.269 | 1.03 |
| Lucky Shot | 200 | 0.397 | 0.229 | 1.73 |
| Arctic Blast | 171 | 1.325 | 0.845 | 1.57 |
| Split Shot | 170 | 0.257 | 0.260 | 0.99 |
| Crushing Fists | 143 | 0.303 | 0.095 | 3.19 |
| Phantom Strike | 123 | 0.311 | 0.213 | 1.46 |
| Decay | 107 | 1.538 | 1.606 | 0.96 |
| Scourge | 105 | 2.027 | 2.142 | 0.95 |
| Return Fire | 92 | 0.439 | 0.121 | 3.64 |
| Alchemical Fire | 68 | 0.874 | 0.869 | 1.01 |
| Focus Lens | 36 | 0.957 | 0.905 | 1.06 |
| Lightning Scroll | 35 | 0.373 | 0.382 | 0.98 |
| Silence Wave | 26 | 0.209 | 0.203 | 1.03 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.024 | 12.24 |
| Drifter | Melee Charge | 68 | 0.211 | 0.047 | 4.46 |
| Rat King | Return Fire | 41 | 0.389 | 0.093 | 4.19 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.077 | 3.90 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 2.827 | 0.27 |
| Calico | Melee Charge | 27 | 0.170 | 0.046 | 3.71 |
| Paradox | Tankbuster | 146 | 0.656 | 0.194 | 3.39 |
| Yamato | Melee Charge | 57 | 0.207 | 0.062 | 3.34 |
| Billy | Crushing Fists | 31 | 0.319 | 0.105 | 3.04 |
| Bebop | Spirit Strike | 186 | 0.274 | 0.096 | 2.85 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.202 | 2.73 |
| Paradox | Express Shot | 143 | 0.229 | 0.620 | 0.37 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.086 | 2.63 |
| Mo & Krill | Rebuttal | 22 | 0.160 | 0.402 | 0.40 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.070 | 2.50 |
| Mo & Krill | Tankbuster | 118 | 3.292 | 1.320 | 2.49 |
| Haze | Lucky Shot | 91 | 0.492 | 0.208 | 2.36 |
| Bebop | Tankbuster | 43 | 1.252 | 0.539 | 2.32 |
| Paradox | Mystic Reverb | 86 | 1.290 | 0.571 | 2.26 |
| Bebop | Spirit Snatch | 191 | 0.342 | 0.151 | 2.26 |
| Vyper | Quicksilver Reload | 31 | 0.057 | 0.126 | 0.45 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.192 | 2.08 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.154 | 2.03 |
| Pocket | Tankbuster | 110 | 1.140 | 2.298 | 0.50 |
| Deadman Danny | Cold Front | 46 | 0.236 | 0.474 | 0.50 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.174 | 1.97 |
| Holliday | Tankbuster | 48 | 0.959 | 0.490 | 1.96 |
| Drifter | Tankbuster | 101 | 0.587 | 0.300 | 1.96 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.188 | 1.92 |
| Billy | Melee Charge | 48 | 0.242 | 0.126 | 1.91 |
| Venator | Siphon Bullets | 77 | 0.200 | 0.105 | 1.90 |
| McGinnis | Escalating Exposure | 29 | 1.974 | 1.058 | 1.87 |
| Deadman Danny | Toxic Bullets | 144 | 0.871 | 0.474 | 1.84 |
| Calico | Mystic Shot | 30 | 0.381 | 0.697 | 0.55 |
| Yamato | Spirit Strike | 48 | 0.224 | 0.409 | 0.55 |
| Yamato | Mystic Shot | 35 | 0.364 | 0.660 | 0.55 |
| Grey Talon | Tankbuster | 90 | 0.586 | 1.054 | 0.56 |
| Yamato | Torment Pulse | 32 | 1.066 | 1.884 | 0.57 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.790 | 1.75 |
| Abrams | Melee Charge | 129 | 0.306 | 0.176 | 1.74 |
