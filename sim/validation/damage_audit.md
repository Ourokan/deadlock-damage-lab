# Sim vs real damage mix audit

Sample: 600 matches, 5623 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| The Doorman | 2 | 0.20 / 0.12 | 0.57 / 0.71 | 0.22 / 0.13 | 0.01 / 0.04 | 0.17 |
| Apollo | 6 | 0.24 / 0.24 | 0.29 / 0.45 | 0.16 / 0.09 | 0.29 / 0.22 | 0.16 |
| Mo & Krill | 176 | 0.07 / 0.08 | 0.47 / 0.56 | 0.39 / 0.31 | 0.05 / 0.04 | 0.10 |
| Mirage | 45 | 0.31 / 0.34 | 0.48 / 0.39 | 0.17 / 0.22 | 0.02 / 0.03 | 0.10 |
| Graves | 151 | 0.20 / 0.21 | 0.50 / 0.44 | 0.27 / 0.35 | 0.02 / 0.00 | 0.09 |
| Kelvin | 12 | 0.09 / 0.11 | 0.65 / 0.71 | 0.22 / 0.16 | 0.02 / 0.02 | 0.09 |
| Nurse Harrow | 347 | 0.29 / 0.34 | 0.61 / 0.52 | 0.06 / 0.08 | 0.03 / 0.04 | 0.09 |
| Viscous | 29 | 0.13 / 0.17 | 0.51 / 0.52 | 0.28 / 0.20 | 0.05 / 0.08 | 0.08 |
| Warden | 33 | 0.52 / 0.46 | 0.31 / 0.38 | 0.11 / 0.13 | 0.03 / 0.03 | 0.08 |
| Vyper | 78 | 0.46 / 0.53 | 0.26 / 0.22 | 0.25 / 0.23 | 0.02 / 0.02 | 0.08 |
| McGinnis | 49 | 0.20 / 0.15 | 0.64 / 0.71 | 0.12 / 0.12 | 0.02 / 0.00 | 0.07 |
| Paradox | 168 | 0.24 / 0.27 | 0.48 / 0.44 | 0.23 / 0.24 | 0.03 / 0.05 | 0.06 |
| Deadman Danny | 357 | 0.16 / 0.14 | 0.63 / 0.69 | 0.18 / 0.16 | 0.01 / 0.01 | 0.06 |
| Rem | 23 | 0.25 / 0.29 | 0.54 / 0.55 | 0.16 / 0.11 | 0.04 / 0.05 | 0.06 |
| Seven | 95 | 0.20 / 0.23 | 0.66 / 0.62 | 0.10 / 0.12 | 0.02 / 0.02 | 0.05 |
| Bebop | 254 | 0.18 / 0.17 | 0.56 / 0.62 | 0.19 / 0.18 | 0.05 / 0.03 | 0.05 |
| Holliday | 73 | 0.27 / 0.30 | 0.54 / 0.55 | 0.13 / 0.09 | 0.05 / 0.06 | 0.05 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.63 | 0.16 / 0.21 | 0.02 / 0.02 | 0.05 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.35 | 0.17 / 0.20 | 0.18 / 0.20 | 0.05 |
| Sinclair | 20 | 0.17 / 0.19 | 0.76 / 0.72 | 0.02 / 0.03 | 0.03 / 0.06 | 0.05 |
| Solomon | 42 | 0.37 / 0.41 | 0.54 / 0.53 | 0.07 / 0.04 | 0.01 / 0.02 | 0.05 |
| Victor | 129 | 0.15 / 0.18 | 0.64 / 0.59 | 0.16 / 0.17 | 0.03 / 0.04 | 0.05 |
| Celeste | 77 | 0.16 / 0.19 | 0.61 / 0.61 | 0.17 / 0.14 | 0.04 / 0.05 | 0.04 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.02 | 0.04 |
| Paige | 58 | 0.35 / 0.38 | 0.50 / 0.48 | 0.11 / 0.12 | 0.03 / 0.03 | 0.04 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.57 | 0.13 / 0.17 | 0.03 / 0.02 | 0.04 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.59 | 0.25 / 0.22 | 0.03 / 0.03 | 0.04 |
| Drifter | 186 | 0.26 / 0.27 | 0.44 / 0.46 | 0.17 / 0.14 | 0.11 / 0.12 | 0.04 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.14 | 0.08 / 0.09 | 0.04 |
| Abrams | 138 | 0.23 / 0.25 | 0.20 / 0.21 | 0.13 / 0.12 | 0.42 / 0.41 | 0.03 |
| Grey Talon | 103 | 0.31 / 0.29 | 0.49 / 0.52 | 0.16 / 0.17 | 0.01 / 0.01 | 0.03 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.40 | 0.14 / 0.15 | 0.22 / 0.25 | 0.03 |
| Venator | 257 | 0.48 / 0.50 | 0.40 / 0.39 | 0.03 / 0.01 | 0.07 / 0.08 | 0.03 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.32 | 0.15 / 0.14 | 0.03 |
| Wraith | 283 | 0.32 / 0.32 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.03 |
| Lady Geist | 37 | 0.29 / 0.31 | 0.62 / 0.61 | 0.05 / 0.04 | 0.03 / 0.03 | 0.02 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.08 | 0.05 / 0.04 | 0.02 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.35 | 0.26 / 0.27 | 0.04 / 0.04 | 0.02 |
| Vindicta | 131 | 0.44 / 0.45 | 0.49 / 0.49 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Silver | 100 | 0.41 / 0.42 | 0.37 / 0.37 | 0.10 / 0.11 | 0.10 / 0.10 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.66 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.56 | 0.03 / 0.03 | 0.05 / 0.06 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| McGinnis | Mini Turret | ability | 0.467 | 0.562 | 0.65 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.167 | 0.27 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.103 | 0.14 |
| The Doorman | Call Bell | ability | 0.475 | 0.443 | 0.65 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.273 | 0.63 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.236 | 1.51 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.315 | 0.68 |
| Victor | Pain Battery | ability | 0.276 | 0.216 | 1.49 |
| Apollo | Flawless Advance | ability | 0.141 | 0.217 | 0.63 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.236 | 1.36 |
| Paradox | Express Shot | item | 0.027 | 0.084 | 0.36 |
| Bebop | Hyper Beam | ability | 0.129 | 0.188 | 0.63 |
| Rem | Tankbuster | item | 0.063 | 0.020 | 3.65 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.018 | 3.90 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.156 | 0.60 |
| Warden | Last Stand | ability | 0.138 | 0.187 | 0.66 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.288 | 1.28 |
| Apollo | MELEE | melee | 0.287 | 0.219 | 1.28 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.319 | 0.80 |
| Kelvin | Arctic Beam | ability | 0.397 | 0.439 | 1.17 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.042 | 2.01 |
| The Doorman | MELEE | melee | 0.011 | 0.038 | 0.18 |
| The Doorman | Tankbuster | item | 0.165 | 0.068 | 1.47 |
| Holliday | Tankbuster | item | 0.060 | 0.023 | 2.84 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.295 | 1.21 |
| Viscous | Splatter | ability | 0.285 | 0.298 | 1.21 |
| Vyper | Split Shot | item | 0.110 | 0.075 | 1.69 |
| Celeste | Shining Wonder | ability | 0.170 | 0.147 | 1.40 |
| Solomon | Tankbuster | item | 0.046 | 0.015 | 3.31 |
| Viscous | Tankbuster | item | 0.069 | 0.039 | 2.23 |
| Abrams | MELEE | melee | 0.424 | 0.407 | 1.14 |
| Seven | Lightning Ball | ability | 0.198 | 0.175 | 1.29 |
| Celeste | Tankbuster | item | 0.030 | 0.007 | 5.33 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.110 | 1.44 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.302 | 1.16 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.270 | 1.19 |
| Seven | Power Surge | ability | 0.205 | 0.188 | 1.26 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.107 | 1.39 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1519 | 1.039 | 0.729 | 1.43 |
| Mystic Burst | 1461 | 0.284 | 0.232 | 1.22 |
| Quicksilver Reload | 1105 | 0.171 | 0.153 | 1.12 |
| Toxic Bullets | 861 | 0.533 | 0.544 | 0.98 |
| Stalker | 790 | 0.219 | 0.219 | 1.00 |
| Spirit Snatch | 709 | 0.367 | 0.305 | 1.20 |
| Ricochet | 695 | 0.156 | 0.177 | 0.88 |
| Spirit Burn | 574 | 0.770 | 0.672 | 1.15 |
| Torment Pulse | 569 | 1.358 | 1.018 | 1.33 |
| Spirit Strike | 561 | 0.233 | 0.216 | 1.08 |
| Express Shot | 552 | 0.677 | 0.670 | 1.01 |
| Siphon Bullets | 521 | 0.248 | 0.245 | 1.01 |
| Escalating Exposure | 520 | 0.875 | 0.850 | 1.03 |
| Tesla Bullets | 509 | 0.480 | 0.481 | 1.00 |
| Cold Front | 505 | 0.447 | 0.405 | 1.10 |
| Mystic Shot | 495 | 0.385 | 0.382 | 1.01 |
| Headhunter | 407 | 0.440 | 0.438 | 1.00 |
| Melee Charge | 379 | 0.240 | 0.106 | 2.26 |
| Capacitor | 375 | 0.696 | 0.692 | 1.01 |
| Headshot Booster | 370 | 0.215 | 0.197 | 1.09 |
| Mercurial Magnum | 339 | 0.295 | 0.294 | 1.01 |
| Rebuttal | 210 | 0.063 | 0.041 | 1.52 |
| Mystic Reverb | 204 | 1.313 | 1.249 | 1.05 |
| Lucky Shot | 200 | 0.397 | 0.228 | 1.74 |
| Arctic Blast | 171 | 1.325 | 0.739 | 1.79 |
| Split Shot | 170 | 0.257 | 0.250 | 1.03 |
| Crushing Fists | 143 | 0.303 | 0.099 | 3.07 |
| Phantom Strike | 123 | 0.311 | 0.213 | 1.46 |
| Decay | 107 | 1.538 | 1.325 | 1.16 |
| Scourge | 105 | 2.027 | 1.880 | 1.08 |
| Return Fire | 92 | 0.439 | 0.116 | 3.79 |
| Alchemical Fire | 68 | 0.874 | 0.530 | 1.65 |
| Focus Lens | 36 | 0.957 | 0.893 | 1.07 |
| Lightning Scroll | 35 | 0.373 | 0.320 | 1.17 |
| Silence Wave | 26 | 0.209 | 0.300 | 0.70 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.045 | 6.38 |
| Celeste | Tankbuster | 29 | 1.268 | 0.208 | 6.09 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.050 | 6.00 |
| Rat King | Return Fire | 41 | 0.389 | 0.082 | 4.72 |
| Solomon | Tankbuster | 26 | 0.578 | 0.129 | 4.47 |
| Yamato | Melee Charge | 57 | 0.207 | 0.047 | 4.40 |
| Vindicta | Mystic Burst | 25 | 0.107 | 0.026 | 4.03 |
| Calico | Melee Charge | 27 | 0.170 | 0.045 | 3.75 |
| Drifter | Melee Charge | 68 | 0.211 | 0.057 | 3.70 |
| Holliday | Tankbuster | 48 | 0.959 | 0.263 | 3.64 |
| Bebop | Spirit Snatch | 191 | 0.342 | 0.122 | 2.79 |
| Paradox | Express Shot | 143 | 0.229 | 0.607 | 0.38 |
| Mo & Krill | Quicksilver Reload | 150 | 0.843 | 0.328 | 2.57 |
| Bebop | Spirit Strike | 186 | 0.274 | 0.109 | 2.52 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.159 | 2.51 |
| Haze | Lucky Shot | 91 | 0.492 | 0.210 | 2.34 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.159 | 2.26 |
| Warden | Quicksilver Reload | 25 | 0.077 | 0.171 | 0.45 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.641 | 2.15 |
| Billy | Crushing Fists | 31 | 0.319 | 0.149 | 2.15 |
| Deadman Danny | Cold Front | 46 | 0.236 | 0.499 | 0.47 |
| Mo & Krill | Tankbuster | 118 | 3.292 | 1.587 | 2.07 |
| Vyper | Quicksilver Reload | 31 | 0.057 | 0.118 | 0.49 |
| Venator | Siphon Bullets | 77 | 0.200 | 0.098 | 2.05 |
| Holliday | Mystic Burst | 33 | 0.200 | 0.098 | 2.05 |
| Calico | Mystic Shot | 30 | 0.381 | 0.759 | 0.50 |
| Mo & Krill | Arctic Blast | 25 | 3.043 | 1.537 | 1.98 |
| Deadman Danny | Toxic Bullets | 144 | 0.871 | 0.452 | 1.93 |
| Shiv | Spirit Strike | 38 | 0.172 | 0.328 | 0.52 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.181 | 1.89 |
| Pocket | Cold Front | 59 | 0.339 | 0.636 | 0.53 |
| Mo & Krill | Torment Pulse | 161 | 3.578 | 1.909 | 1.87 |
| Abrams | Melee Charge | 129 | 0.306 | 0.163 | 1.87 |
| Billy | Melee Charge | 48 | 0.242 | 0.131 | 1.85 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.098 | 1.80 |
| Lash | Spirit Burn | 69 | 0.946 | 0.531 | 1.78 |
| Vyper | Split Shot | 69 | 0.321 | 0.185 | 1.74 |
| Seven | Toxic Bullets | 30 | 0.366 | 0.631 | 0.58 |
| Shiv | Cold Front | 21 | 0.381 | 0.229 | 1.66 |
| Mo & Krill | Cold Front | 120 | 1.307 | 0.791 | 1.65 |
