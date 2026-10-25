# Sim vs real damage mix audit

Sample: 600 matches, 5627 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.23 | 0.29 / 0.42 | 0.16 / 0.10 | 0.29 / 0.25 | 0.13 |
| Mirage | 45 | 0.31 / 0.36 | 0.48 / 0.39 | 0.17 / 0.22 | 0.02 / 0.03 | 0.11 |
| Rem | 23 | 0.25 / 0.25 | 0.54 / 0.45 | 0.16 / 0.25 | 0.04 / 0.05 | 0.10 |
| The Doorman | 2 | 0.20 / 0.14 | 0.57 / 0.53 | 0.22 / 0.29 | 0.01 / 0.04 | 0.10 |
| Warden | 33 | 0.52 / 0.46 | 0.31 / 0.36 | 0.11 / 0.16 | 0.03 / 0.02 | 0.09 |
| Paradox | 168 | 0.24 / 0.26 | 0.48 / 0.41 | 0.23 / 0.27 | 0.03 / 0.05 | 0.09 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.32 | 0.17 / 0.24 | 0.18 / 0.19 | 0.08 |
| Vyper | 78 | 0.46 / 0.51 | 0.26 / 0.20 | 0.25 / 0.27 | 0.02 / 0.02 | 0.08 |
| McGinnis | 49 | 0.20 / 0.15 | 0.64 / 0.68 | 0.12 / 0.14 | 0.02 / 0.00 | 0.07 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.49 | 0.27 / 0.33 | 0.02 / 0.00 | 0.06 |
| Seven | 95 | 0.20 / 0.23 | 0.66 / 0.62 | 0.10 / 0.12 | 0.02 / 0.02 | 0.06 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.47 | 0.28 / 0.29 | 0.05 / 0.08 | 0.06 |
| Calico | 110 | 0.13 / 0.13 | 0.38 / 0.36 | 0.31 / 0.37 | 0.15 / 0.14 | 0.06 |
| Pocket | 117 | 0.14 / 0.12 | 0.66 / 0.63 | 0.16 / 0.22 | 0.02 / 0.02 | 0.06 |
| Victor | 129 | 0.15 / 0.17 | 0.64 / 0.59 | 0.16 / 0.20 | 0.03 / 0.03 | 0.06 |
| Kelvin | 12 | 0.09 / 0.12 | 0.65 / 0.67 | 0.22 / 0.20 | 0.02 / 0.02 | 0.05 |
| Paige | 58 | 0.35 / 0.39 | 0.50 / 0.46 | 0.11 / 0.12 | 0.03 / 0.02 | 0.05 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.46 | 0.05 / 0.05 | 0.01 / 0.01 | 0.05 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.33 | 0.26 / 0.31 | 0.04 / 0.04 | 0.05 |
| Solomon | 42 | 0.37 / 0.38 | 0.54 / 0.50 | 0.07 / 0.09 | 0.01 / 0.02 | 0.05 |
| Infernus | 173 | 0.23 / 0.24 | 0.60 / 0.56 | 0.13 / 0.17 | 0.03 / 0.02 | 0.05 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.58 | 0.17 / 0.18 | 0.04 / 0.05 | 0.04 |
| Violet | 4 | 0.29 / 0.25 | 0.65 / 0.69 | 0.02 / 0.03 | 0.01 / 0.01 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.47 | 0.17 / 0.13 | 0.11 / 0.11 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.08 | 0.47 / 0.51 | 0.39 / 0.37 | 0.05 / 0.04 | 0.04 |
| Abrams | 138 | 0.23 / 0.26 | 0.20 / 0.21 | 0.13 / 0.12 | 0.42 / 0.40 | 0.04 |
| Deadman Danny | 357 | 0.16 / 0.13 | 0.63 / 0.64 | 0.18 / 0.21 | 0.01 / 0.01 | 0.04 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.54 | 0.12 / 0.09 | 0.02 / 0.02 | 0.04 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.57 | 0.19 / 0.21 | 0.05 / 0.03 | 0.04 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.73 | 0.02 / 0.03 | 0.03 / 0.05 | 0.04 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.34 | 0.10 / 0.13 | 0.10 / 0.11 | 0.04 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.39 | 0.03 / 0.02 | 0.07 / 0.09 | 0.03 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.60 | 0.06 / 0.09 | 0.03 / 0.03 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.48 | 0.16 / 0.15 | 0.08 / 0.08 | 0.03 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.40 | 0.14 / 0.15 | 0.22 / 0.24 | 0.03 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.50 | 0.16 / 0.18 | 0.01 / 0.01 | 0.03 |
| Wraith | 283 | 0.32 / 0.32 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.65 | 0.19 / 0.21 | 0.01 / 0.01 | 0.02 |
| Holliday | 73 | 0.27 / 0.29 | 0.54 / 0.54 | 0.13 / 0.12 | 0.05 / 0.05 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.29 | 0.62 / 0.64 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Dynamo | 53 | 0.23 / 0.23 | 0.62 / 0.63 | 0.08 / 0.09 | 0.05 / 0.04 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.57 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Rat King | 424 | 0.33 / 0.32 | 0.57 / 0.57 | 0.03 / 0.03 | 0.05 / 0.06 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| McGinnis | Mini Turret | ability | 0.467 | 0.536 | 0.68 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.197 | 1.70 |
| The Doorman | Tankbuster | item | 0.165 | 0.226 | 0.53 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.259 | 0.64 |
| Kelvin | Arctic Beam | ability | 0.397 | 0.399 | 1.33 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.294 | 0.70 |
| Paradox | Express Shot | item | 0.027 | 0.089 | 0.33 |
| Apollo | Flawless Advance | ability | 0.141 | 0.204 | 0.64 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.033 | 2.42 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.113 | 0.48 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.062 | 0.27 |
| Abrams | MELEE | melee | 0.424 | 0.398 | 1.21 |
| Victor | Pain Battery | ability | 0.276 | 0.231 | 1.31 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.147 | 0.61 |
| Vyper | Lethal Venom | ability | 0.112 | 0.066 | 1.90 |
| Rem | Tankbuster | item | 0.063 | 0.116 | 0.54 |
| Vindicta | Assassinate | ability | 0.162 | 0.119 | 1.49 |
| Mo & Krill | Tankbuster | item | 0.061 | 0.023 | 2.90 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.285 | 1.22 |
| Violet | Living Ink | ability | 0.277 | 0.294 | 0.81 |
| Warden | Last Stand | ability | 0.138 | 0.173 | 0.70 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.269 | 1.24 |
| Celeste | Shining Wonder | ability | 0.170 | 0.140 | 1.40 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.024 | 2.64 |
| The Doorman | MELEE | melee | 0.011 | 0.037 | 0.22 |
| Infernus | Flame Dash | ability | 0.216 | 0.175 | 1.30 |
| Seven | Lightning Ball | ability | 0.198 | 0.174 | 1.32 |
| Sinclair | Audience Participation | ability | 0.194 | 0.255 | 0.81 |
| Viscous | Splatter | ability | 0.285 | 0.268 | 1.21 |
| Deadman Danny | Tankbuster | item | 0.079 | 0.107 | 0.61 |
| Rem | Decay | item | 0.026 | 0.061 | 0.43 |
| Pocket | Tankbuster | item | 0.079 | 0.110 | 0.63 |
| Paige | Bookwyrm | ability | 0.320 | 0.307 | 1.17 |
| Rem | Pillow Toss | ability | 0.410 | 0.366 | 1.13 |
| Violet | Abstract Landscape | ability | 0.169 | 0.188 | 0.78 |
| Pocket | Affliction | ability | 0.120 | 0.147 | 0.73 |
| Seven | Power Surge | ability | 0.205 | 0.191 | 1.25 |
| Solomon | Rook Battery | ability | 0.167 | 0.132 | 1.31 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1520 | 1.039 | 0.929 | 1.12 |
| Mystic Burst | 1462 | 0.283 | 0.262 | 1.08 |
| Quicksilver Reload | 1105 | 0.171 | 0.161 | 1.06 |
| Toxic Bullets | 862 | 0.532 | 0.547 | 0.97 |
| Stalker | 790 | 0.219 | 0.221 | 0.99 |
| Spirit Snatch | 709 | 0.367 | 0.304 | 1.21 |
| Ricochet | 695 | 0.156 | 0.181 | 0.86 |
| Spirit Burn | 574 | 0.770 | 0.605 | 1.27 |
| Torment Pulse | 569 | 1.358 | 1.388 | 0.98 |
| Spirit Strike | 561 | 0.233 | 0.211 | 1.10 |
| Express Shot | 552 | 0.677 | 0.674 | 1.00 |
| Siphon Bullets | 521 | 0.248 | 0.253 | 0.98 |
| Escalating Exposure | 520 | 0.875 | 0.852 | 1.03 |
| Tesla Bullets | 509 | 0.480 | 0.478 | 1.00 |
| Cold Front | 505 | 0.447 | 0.446 | 1.00 |
| Mystic Shot | 495 | 0.385 | 0.377 | 1.02 |
| Headhunter | 407 | 0.440 | 0.439 | 1.00 |
| Melee Charge | 379 | 0.240 | 0.102 | 2.35 |
| Capacitor | 375 | 0.696 | 0.705 | 0.99 |
| Headshot Booster | 370 | 0.215 | 0.197 | 1.09 |
| Mercurial Magnum | 339 | 0.295 | 0.297 | 0.99 |
| Rebuttal | 210 | 0.063 | 0.049 | 1.28 |
| Mystic Reverb | 204 | 1.313 | 1.182 | 1.11 |
| Lucky Shot | 200 | 0.397 | 0.228 | 1.74 |
| Arctic Blast | 171 | 1.325 | 0.784 | 1.69 |
| Split Shot | 170 | 0.257 | 0.253 | 1.02 |
| Crushing Fists | 143 | 0.303 | 0.101 | 3.02 |
| Phantom Strike | 123 | 0.311 | 0.223 | 1.40 |
| Decay | 107 | 1.538 | 1.665 | 0.92 |
| Scourge | 105 | 2.027 | 2.114 | 0.96 |
| Return Fire | 92 | 0.439 | 0.123 | 3.56 |
| Alchemical Fire | 68 | 0.874 | 0.865 | 1.01 |
| Focus Lens | 36 | 0.957 | 0.839 | 1.14 |
| Lightning Scroll | 35 | 0.373 | 0.366 | 1.02 |
| Silence Wave | 26 | 0.209 | 0.206 | 1.01 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.046 | 6.22 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.063 | 4.75 |
| Rat King | Return Fire | 41 | 0.389 | 0.096 | 4.06 |
| Mo & Krill | Tankbuster | 118 | 3.292 | 0.845 | 3.90 |
| Drifter | Melee Charge | 68 | 0.211 | 0.055 | 3.84 |
| Calico | Melee Charge | 27 | 0.170 | 0.048 | 3.53 |
| Bebop | Spirit Snatch | 191 | 0.342 | 0.101 | 3.38 |
| Yamato | Melee Charge | 57 | 0.207 | 0.067 | 3.09 |
| Warden | Quicksilver Reload | 25 | 0.077 | 0.231 | 0.34 |
| Bebop | Spirit Strike | 186 | 0.274 | 0.098 | 2.79 |
| Paradox | Express Shot | 143 | 0.229 | 0.604 | 0.38 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.153 | 2.61 |
| Haze | Lucky Shot | 91 | 0.492 | 0.202 | 2.44 |
| Vyper | Quicksilver Reload | 31 | 0.057 | 0.134 | 0.43 |
| Calico | Mystic Shot | 30 | 0.381 | 0.880 | 0.43 |
| Billy | Crushing Fists | 31 | 0.319 | 0.144 | 2.22 |
| Bebop | Tankbuster | 43 | 1.252 | 2.775 | 0.45 |
| Abrams | Melee Charge | 129 | 0.306 | 0.148 | 2.06 |
| Mo & Krill | Quicksilver Reload | 150 | 0.843 | 0.420 | 2.01 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.183 | 1.97 |
| Holliday | Tankbuster | 48 | 0.959 | 0.497 | 1.93 |
| Pocket | Cold Front | 59 | 0.339 | 0.639 | 0.53 |
| Deadman Danny | Cold Front | 46 | 0.236 | 0.434 | 0.54 |
| Seven | Toxic Bullets | 30 | 0.366 | 0.672 | 0.55 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.190 | 1.80 |
| Deadman Danny | Toxic Bullets | 144 | 0.871 | 0.485 | 1.80 |
| Billy | Melee Charge | 48 | 0.242 | 0.136 | 1.78 |
| Venator | Siphon Bullets | 77 | 0.200 | 0.113 | 1.77 |
| Graves | Torment Pulse | 79 | 0.505 | 0.890 | 0.57 |
| Infernus | Quicksilver Reload | 30 | 0.105 | 0.185 | 0.57 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.790 | 1.74 |
| Shiv | Cold Front | 21 | 0.381 | 0.221 | 1.72 |
| Drifter | Tankbuster | 101 | 0.587 | 0.348 | 1.69 |
| Lash | Spirit Burn | 69 | 0.946 | 0.571 | 1.66 |
| Yamato | Mystic Shot | 35 | 0.364 | 0.599 | 0.61 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.108 | 1.63 |
| Shiv | Spirit Strike | 38 | 0.172 | 0.276 | 0.62 |
| Venator | Ricochet | 36 | 0.114 | 0.182 | 0.63 |
| Yamato | Spirit Strike | 48 | 0.224 | 0.356 | 0.63 |
| Shiv | Express Shot | 125 | 0.882 | 0.559 | 1.58 |
