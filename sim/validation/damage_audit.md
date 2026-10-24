# Sim vs real damage mix audit

Sample: 600 matches, 5623 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.22 | 0.29 / 0.42 | 0.16 / 0.11 | 0.29 / 0.25 | 0.13 |
| Rem | 23 | 0.25 / 0.24 | 0.54 / 0.45 | 0.16 / 0.25 | 0.04 / 0.05 | 0.10 |
| Mirage | 45 | 0.31 / 0.35 | 0.48 / 0.40 | 0.17 / 0.22 | 0.02 / 0.03 | 0.10 |
| Warden | 33 | 0.52 / 0.46 | 0.31 / 0.36 | 0.11 / 0.15 | 0.03 / 0.02 | 0.09 |
| The Doorman | 2 | 0.20 / 0.11 | 0.57 / 0.61 | 0.22 / 0.26 | 0.01 / 0.03 | 0.09 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.33 | 0.17 / 0.24 | 0.18 / 0.20 | 0.08 |
| Paradox | 168 | 0.24 / 0.26 | 0.48 / 0.42 | 0.23 / 0.27 | 0.03 / 0.05 | 0.08 |
| McGinnis | 49 | 0.20 / 0.15 | 0.64 / 0.69 | 0.12 / 0.14 | 0.02 / 0.00 | 0.07 |
| Victor | 129 | 0.15 / 0.18 | 0.64 / 0.58 | 0.16 / 0.20 | 0.03 / 0.04 | 0.07 |
| Vyper | 78 | 0.46 / 0.50 | 0.26 / 0.22 | 0.25 / 0.26 | 0.02 / 0.02 | 0.06 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.63 | 0.16 / 0.22 | 0.02 / 0.02 | 0.06 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.49 | 0.27 / 0.33 | 0.02 / 0.00 | 0.06 |
| Calico | 110 | 0.13 / 0.13 | 0.38 / 0.36 | 0.31 / 0.37 | 0.15 / 0.14 | 0.06 |
| Seven | 95 | 0.20 / 0.23 | 0.66 / 0.62 | 0.10 / 0.12 | 0.02 / 0.02 | 0.06 |
| Kelvin | 12 | 0.09 / 0.11 | 0.65 / 0.68 | 0.22 / 0.19 | 0.02 / 0.02 | 0.06 |
| Bebop | 254 | 0.18 / 0.16 | 0.56 / 0.59 | 0.19 / 0.21 | 0.05 / 0.03 | 0.06 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.47 | 0.28 / 0.29 | 0.05 / 0.08 | 0.06 |
| Sinclair | 20 | 0.17 / 0.19 | 0.76 / 0.72 | 0.02 / 0.04 | 0.03 / 0.05 | 0.05 |
| Solomon | 42 | 0.37 / 0.38 | 0.54 / 0.50 | 0.07 / 0.09 | 0.01 / 0.02 | 0.05 |
| Paige | 58 | 0.35 / 0.38 | 0.50 / 0.47 | 0.11 / 0.13 | 0.03 / 0.02 | 0.05 |
| Mo & Krill | 176 | 0.07 / 0.08 | 0.47 / 0.51 | 0.39 / 0.37 | 0.05 / 0.04 | 0.05 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.34 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.47 | 0.17 / 0.14 | 0.11 / 0.11 | 0.04 |
| Deadman Danny | 357 | 0.16 / 0.13 | 0.63 / 0.65 | 0.18 / 0.21 | 0.01 / 0.01 | 0.04 |
| Abrams | 138 | 0.23 / 0.26 | 0.20 / 0.21 | 0.13 / 0.12 | 0.42 / 0.40 | 0.04 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.29 | 0.49 / 0.51 | 0.16 / 0.18 | 0.01 / 0.01 | 0.04 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.57 | 0.13 / 0.17 | 0.03 / 0.02 | 0.04 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.59 | 0.17 / 0.18 | 0.04 / 0.04 | 0.04 |
| Venator | 257 | 0.48 / 0.50 | 0.40 / 0.39 | 0.03 / 0.02 | 0.07 / 0.09 | 0.03 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.35 | 0.10 / 0.13 | 0.10 / 0.10 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.48 | 0.16 / 0.14 | 0.08 / 0.08 | 0.03 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.65 | 0.19 / 0.21 | 0.01 / 0.01 | 0.03 |
| Wraith | 283 | 0.32 / 0.32 | 0.41 / 0.40 | 0.24 / 0.27 | 0.01 / 0.01 | 0.03 |
| Holliday | 73 | 0.27 / 0.29 | 0.54 / 0.54 | 0.13 / 0.12 | 0.05 / 0.05 | 0.03 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.40 | 0.14 / 0.15 | 0.22 / 0.24 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.31 | 0.62 / 0.62 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Dynamo | 53 | 0.23 / 0.23 | 0.62 / 0.63 | 0.08 / 0.10 | 0.05 / 0.04 | 0.02 |
| Vindicta | 131 | 0.44 / 0.45 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.56 | 0.03 / 0.03 | 0.05 / 0.06 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.25 | 0.03 / 0.03 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| McGinnis | Mini Turret | ability | 0.467 | 0.549 | 0.67 |
| The Doorman | Call Bell | ability | 0.475 | 0.384 | 0.67 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.089 | 0.14 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.137 | 0.29 |
| The Doorman | Tankbuster | item | 0.165 | 0.196 | 0.46 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.256 | 0.64 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.295 | 0.69 |
| Victor | Pain Battery | ability | 0.276 | 0.212 | 1.49 |
| Paradox | Express Shot | item | 0.027 | 0.087 | 0.33 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.238 | 1.37 |
| Apollo | Flawless Advance | ability | 0.141 | 0.197 | 0.65 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.017 | 4.02 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.150 | 0.59 |
| Bebop | Hyper Beam | ability | 0.129 | 0.180 | 0.65 |
| Kelvin | Arctic Beam | ability | 0.397 | 0.417 | 1.21 |
| Abrams | MELEE | melee | 0.424 | 0.399 | 1.20 |
| Warden | Last Stand | ability | 0.138 | 0.182 | 0.67 |
| Rem | Tankbuster | item | 0.063 | 0.115 | 0.54 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.040 | 1.96 |
| Mo & Krill | Tankbuster | item | 0.061 | 0.022 | 2.92 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.309 | 0.81 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.292 | 1.22 |
| Deadman Danny | Tankbuster | item | 0.079 | 0.108 | 0.59 |
| Celeste | Shining Wonder | ability | 0.170 | 0.142 | 1.38 |
| Rem | Decay | item | 0.026 | 0.061 | 0.41 |
| Viscous | Splatter | ability | 0.285 | 0.268 | 1.20 |
| Seven | Lightning Ball | ability | 0.198 | 0.176 | 1.29 |
| Pocket | Tankbuster | item | 0.079 | 0.112 | 0.64 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.260 | 1.21 |
| The Doorman | Mystic Burst | item | 0.013 | 0.032 | 0.22 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.291 | 1.16 |
| Seven | Power Surge | ability | 0.205 | 0.188 | 1.25 |
| Infernus | Flame Dash | ability | 0.216 | 0.183 | 1.22 |
| Pocket | Affliction | ability | 0.120 | 0.146 | 0.75 |
| Vyper | Lethal Venom | ability | 0.112 | 0.086 | 1.42 |
| Rem | Naptime | ability | 0.115 | 0.082 | 1.38 |
| Yamato | Stalker | item | 0.040 | 0.066 | 0.57 |
| Paige | Bookwyrm | ability | 0.320 | 0.311 | 1.12 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1519 | 1.039 | 0.945 | 1.10 |
| Mystic Burst | 1461 | 0.284 | 0.261 | 1.09 |
| Quicksilver Reload | 1105 | 0.171 | 0.152 | 1.12 |
| Toxic Bullets | 861 | 0.533 | 0.544 | 0.98 |
| Stalker | 790 | 0.219 | 0.217 | 1.01 |
| Spirit Snatch | 709 | 0.367 | 0.303 | 1.21 |
| Ricochet | 695 | 0.156 | 0.182 | 0.86 |
| Spirit Burn | 574 | 0.770 | 0.661 | 1.16 |
| Torment Pulse | 569 | 1.358 | 1.351 | 1.00 |
| Spirit Strike | 561 | 0.233 | 0.214 | 1.09 |
| Express Shot | 552 | 0.677 | 0.661 | 1.02 |
| Siphon Bullets | 521 | 0.248 | 0.246 | 1.01 |
| Escalating Exposure | 520 | 0.875 | 0.838 | 1.04 |
| Tesla Bullets | 509 | 0.480 | 0.479 | 1.00 |
| Cold Front | 505 | 0.447 | 0.443 | 1.01 |
| Mystic Shot | 495 | 0.385 | 0.379 | 1.01 |
| Headhunter | 407 | 0.440 | 0.436 | 1.01 |
| Melee Charge | 379 | 0.240 | 0.103 | 2.32 |
| Capacitor | 375 | 0.696 | 0.690 | 1.01 |
| Headshot Booster | 370 | 0.215 | 0.196 | 1.10 |
| Mercurial Magnum | 339 | 0.295 | 0.294 | 1.00 |
| Rebuttal | 210 | 0.063 | 0.044 | 1.44 |
| Mystic Reverb | 204 | 1.313 | 1.289 | 1.02 |
| Lucky Shot | 200 | 0.397 | 0.229 | 1.74 |
| Arctic Blast | 171 | 1.325 | 0.868 | 1.53 |
| Split Shot | 170 | 0.257 | 0.262 | 0.98 |
| Crushing Fists | 143 | 0.303 | 0.093 | 3.27 |
| Phantom Strike | 123 | 0.311 | 0.208 | 1.49 |
| Decay | 107 | 1.538 | 1.322 | 1.16 |
| Scourge | 105 | 2.027 | 2.009 | 1.01 |
| Return Fire | 92 | 0.439 | 0.116 | 3.78 |
| Alchemical Fire | 68 | 0.874 | 0.866 | 1.01 |
| Focus Lens | 36 | 0.957 | 0.899 | 1.06 |
| Lightning Scroll | 35 | 0.373 | 0.324 | 1.15 |
| Silence Wave | 26 | 0.209 | 0.598 | 0.35 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.043 | 6.74 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.052 | 5.74 |
| Rat King | Return Fire | 41 | 0.389 | 0.088 | 4.41 |
| Mo & Krill | Tankbuster | 118 | 3.292 | 0.846 | 3.89 |
| Mo & Krill | Rebuttal | 22 | 0.160 | 0.042 | 3.86 |
| Drifter | Melee Charge | 68 | 0.211 | 0.055 | 3.81 |
| Calico | Melee Charge | 27 | 0.170 | 0.047 | 3.63 |
| Yamato | Melee Charge | 57 | 0.207 | 0.059 | 3.50 |
| Bebop | Spirit Snatch | 191 | 0.342 | 0.108 | 3.15 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.137 | 2.91 |
| Warden | Quicksilver Reload | 25 | 0.077 | 0.222 | 0.35 |
| Bebop | Spirit Strike | 186 | 0.274 | 0.102 | 2.69 |
| Paradox | Express Shot | 143 | 0.229 | 0.608 | 0.38 |
| Haze | Lucky Shot | 91 | 0.492 | 0.205 | 2.39 |
| Vyper | Quicksilver Reload | 31 | 0.057 | 0.136 | 0.42 |
| Calico | Mystic Shot | 30 | 0.381 | 0.882 | 0.43 |
| Billy | Crushing Fists | 31 | 0.319 | 0.142 | 2.25 |
| Bebop | Tankbuster | 43 | 1.252 | 2.619 | 0.48 |
| Abrams | Melee Charge | 129 | 0.306 | 0.154 | 1.99 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.185 | 1.95 |
| Mo & Krill | Quicksilver Reload | 150 | 0.843 | 0.433 | 1.95 |
| Billy | Melee Charge | 48 | 0.242 | 0.126 | 1.92 |
| Deadman Danny | Cold Front | 46 | 0.236 | 0.449 | 0.53 |
| Venator | Siphon Bullets | 77 | 0.200 | 0.106 | 1.88 |
| Pocket | Cold Front | 59 | 0.339 | 0.627 | 0.54 |
| Holliday | Tankbuster | 48 | 0.959 | 0.527 | 1.82 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.127 | 1.79 |
| Infernus | Quicksilver Reload | 30 | 0.105 | 0.188 | 0.56 |
| Seven | Toxic Bullets | 30 | 0.366 | 0.651 | 0.56 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.192 | 1.78 |
| Shiv | Cold Front | 21 | 0.381 | 0.214 | 1.77 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.778 | 1.77 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.136 | 1.72 |
| Yamato | Mystic Shot | 35 | 0.364 | 0.620 | 0.59 |
| Shiv | Spirit Strike | 38 | 0.172 | 0.290 | 0.59 |
| Deadman Danny | Toxic Bullets | 144 | 0.871 | 0.518 | 1.68 |
| Graves | Torment Pulse | 79 | 0.505 | 0.837 | 0.60 |
| Shiv | Express Shot | 125 | 0.882 | 0.534 | 1.65 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.108 | 1.63 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.199 | 0.62 |
