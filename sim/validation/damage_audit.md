# Sim vs real damage mix audit

Sample: 600 matches, 5623 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides.

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.23 | 0.29 / 0.46 | 0.16 / 0.09 | 0.29 / 0.22 | 0.17 |
| The Doorman | 2 | 0.20 / 0.14 | 0.57 / 0.70 | 0.22 / 0.13 | 0.01 / 0.04 | 0.15 |
| Mo & Krill | 176 | 0.07 / 0.08 | 0.47 / 0.56 | 0.39 / 0.31 | 0.05 / 0.04 | 0.10 |
| Vyper | 78 | 0.46 / 0.55 | 0.26 / 0.26 | 0.25 / 0.17 | 0.02 / 0.02 | 0.09 |
| Graves | 151 | 0.20 / 0.21 | 0.50 / 0.44 | 0.27 / 0.35 | 0.02 / 0.00 | 0.09 |
| Kelvin | 12 | 0.09 / 0.12 | 0.65 / 0.70 | 0.22 / 0.17 | 0.02 / 0.02 | 0.09 |
| Warden | 33 | 0.52 / 0.46 | 0.31 / 0.37 | 0.11 / 0.14 | 0.03 / 0.02 | 0.08 |
| Mirage | 45 | 0.31 / 0.35 | 0.48 / 0.41 | 0.17 / 0.20 | 0.02 / 0.03 | 0.08 |
| Viscous | 29 | 0.13 / 0.17 | 0.51 / 0.52 | 0.28 / 0.20 | 0.05 / 0.08 | 0.08 |
| Nurse Harrow | 347 | 0.29 / 0.35 | 0.61 / 0.53 | 0.06 / 0.07 | 0.03 / 0.04 | 0.08 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.71 | 0.12 / 0.12 | 0.02 / 0.00 | 0.07 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.56 | 0.12 / 0.06 | 0.02 / 0.02 | 0.06 |
| Paradox | 168 | 0.24 / 0.27 | 0.48 / 0.44 | 0.23 / 0.24 | 0.03 / 0.05 | 0.06 |
| Seven | 95 | 0.20 / 0.23 | 0.66 / 0.62 | 0.10 / 0.12 | 0.02 / 0.02 | 0.06 |
| Deadman Danny | 357 | 0.16 / 0.14 | 0.63 / 0.69 | 0.18 / 0.16 | 0.01 / 0.01 | 0.06 |
| Rem | 23 | 0.25 / 0.29 | 0.54 / 0.55 | 0.16 / 0.11 | 0.04 / 0.05 | 0.06 |
| Bebop | 254 | 0.18 / 0.17 | 0.56 / 0.62 | 0.19 / 0.18 | 0.05 / 0.03 | 0.06 |
| Holliday | 73 | 0.27 / 0.30 | 0.54 / 0.55 | 0.13 / 0.09 | 0.05 / 0.06 | 0.05 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.35 | 0.17 / 0.20 | 0.18 / 0.20 | 0.05 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.63 | 0.16 / 0.21 | 0.02 / 0.02 | 0.05 |
| Sinclair | 20 | 0.17 / 0.19 | 0.76 / 0.72 | 0.02 / 0.03 | 0.03 / 0.06 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.54 | 0.07 / 0.04 | 0.01 / 0.02 | 0.05 |
| Victor | 129 | 0.15 / 0.18 | 0.64 / 0.59 | 0.16 / 0.17 | 0.03 / 0.04 | 0.05 |
| Celeste | 77 | 0.16 / 0.19 | 0.61 / 0.61 | 0.17 / 0.14 | 0.04 / 0.05 | 0.05 |
| Paige | 58 | 0.35 / 0.38 | 0.50 / 0.48 | 0.11 / 0.12 | 0.03 / 0.03 | 0.04 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.58 | 0.13 / 0.16 | 0.03 / 0.02 | 0.04 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.59 | 0.25 / 0.22 | 0.03 / 0.03 | 0.04 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.14 | 0.08 / 0.09 | 0.04 |
| Drifter | 186 | 0.26 / 0.27 | 0.44 / 0.46 | 0.17 / 0.14 | 0.11 / 0.12 | 0.04 |
| Abrams | 138 | 0.23 / 0.25 | 0.20 / 0.21 | 0.13 / 0.12 | 0.42 / 0.41 | 0.03 |
| Grey Talon | 103 | 0.31 / 0.29 | 0.49 / 0.52 | 0.16 / 0.17 | 0.01 / 0.01 | 0.03 |
| Venator | 257 | 0.48 / 0.51 | 0.40 / 0.40 | 0.03 / 0.01 | 0.07 / 0.08 | 0.03 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.40 | 0.14 / 0.15 | 0.22 / 0.25 | 0.03 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.32 | 0.15 / 0.14 | 0.03 |
| Lady Geist | 37 | 0.29 / 0.31 | 0.62 / 0.62 | 0.05 / 0.04 | 0.03 / 0.03 | 0.02 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.35 | 0.26 / 0.27 | 0.04 / 0.04 | 0.02 |
| Dynamo | 53 | 0.23 / 0.23 | 0.62 / 0.64 | 0.08 / 0.08 | 0.05 / 0.04 | 0.02 |
| Silver | 100 | 0.41 / 0.42 | 0.37 / 0.37 | 0.10 / 0.11 | 0.10 / 0.10 | 0.02 |
| Vindicta | 131 | 0.44 / 0.45 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.66 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.56 | 0.03 / 0.03 | 0.05 / 0.06 | 0.01 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.41 | 0.24 / 0.25 | 0.01 / 0.01 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| McGinnis | Mini Turret | ability | 0.467 | 0.562 | 0.66 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.172 | 0.31 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.100 | 0.17 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.239 | 1.50 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.273 | 0.64 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.314 | 0.69 |
| The Doorman | Call Bell | ability | 0.475 | 0.428 | 0.78 |
| Apollo | Flawless Advance | ability | 0.141 | 0.220 | 0.60 |
| Victor | Pain Battery | ability | 0.276 | 0.215 | 1.50 |
| Vyper | Split Shot | item | 0.110 | 0.047 | 2.76 |
| The Doorman | Tankbuster | item | 0.165 | 0.066 | 1.77 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.160 | 0.56 |
| Bebop | Hyper Beam | ability | 0.129 | 0.190 | 0.62 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.247 | 1.34 |
| Paradox | Express Shot | item | 0.027 | 0.083 | 0.36 |
| Kelvin | Arctic Beam | ability | 0.397 | 0.433 | 1.21 |
| Rem | Tankbuster | item | 0.063 | 0.020 | 3.62 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.018 | 3.87 |
| Warden | Last Stand | ability | 0.138 | 0.185 | 0.66 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.293 | 1.27 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.318 | 0.80 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.042 | 2.00 |
| Viscous | Splatter | ability | 0.285 | 0.297 | 1.24 |
| Holliday | Tankbuster | item | 0.060 | 0.024 | 2.86 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.296 | 1.21 |
| Apollo | MELEE | melee | 0.287 | 0.218 | 1.22 |
| The Doorman | MELEE | melee | 0.011 | 0.037 | 0.21 |
| Viscous | Tankbuster | item | 0.069 | 0.039 | 2.28 |
| Celeste | Shining Wonder | ability | 0.170 | 0.147 | 1.39 |
| Abrams | MELEE | melee | 0.424 | 0.406 | 1.14 |
| Solomon | Tankbuster | item | 0.046 | 0.015 | 3.29 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.269 | 1.22 |
| Seven | Lightning Ball | ability | 0.198 | 0.175 | 1.29 |
| Celeste | Tankbuster | item | 0.030 | 0.007 | 5.32 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.110 | 1.44 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.302 | 1.16 |
| Seven | Power Surge | ability | 0.205 | 0.186 | 1.26 |
| Kelvin | Torment Pulse | item | 0.057 | 0.034 | 2.21 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1519 | 1.039 | 0.725 | 1.43 |
| Mystic Burst | 1461 | 0.284 | 0.232 | 1.22 |
| Quicksilver Reload | 1105 | 0.171 | 0.154 | 1.11 |
| Toxic Bullets | 861 | 0.533 | 0.545 | 0.98 |
| Stalker | 790 | 0.219 | 0.219 | 1.00 |
| Spirit Snatch | 709 | 0.367 | 0.305 | 1.20 |
| Ricochet | 695 | 0.156 | 0.000 | - |
| Spirit Burn | 574 | 0.770 | 0.669 | 1.15 |
| Torment Pulse | 569 | 1.358 | 1.021 | 1.33 |
| Spirit Strike | 561 | 0.233 | 0.215 | 1.08 |
| Express Shot | 552 | 0.677 | 0.659 | 1.03 |
| Siphon Bullets | 521 | 0.248 | 0.247 | 1.00 |
| Escalating Exposure | 520 | 0.875 | 0.854 | 1.02 |
| Tesla Bullets | 509 | 0.480 | 0.481 | 1.00 |
| Cold Front | 505 | 0.447 | 0.403 | 1.11 |
| Mystic Shot | 495 | 0.385 | 0.383 | 1.00 |
| Headhunter | 407 | 0.440 | 0.436 | 1.01 |
| Melee Charge | 379 | 0.240 | 0.106 | 2.27 |
| Capacitor | 375 | 0.696 | 0.693 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.197 | 1.10 |
| Mercurial Magnum | 339 | 0.295 | 0.295 | 1.00 |
| Rebuttal | 210 | 0.063 | 0.044 | 1.44 |
| Mystic Reverb | 204 | 1.313 | 1.234 | 1.06 |
| Lucky Shot | 200 | 0.397 | 0.227 | 1.75 |
| Arctic Blast | 171 | 1.325 | 0.740 | 1.79 |
| Split Shot | 170 | 0.257 | 0.206 | 1.25 |
| Crushing Fists | 143 | 0.303 | 0.098 | 3.08 |
| Phantom Strike | 123 | 0.311 | 0.213 | 1.46 |
| Decay | 107 | 1.538 | 1.312 | 1.17 |
| Scourge | 105 | 2.027 | 1.859 | 1.09 |
| Return Fire | 92 | 0.439 | 0.114 | 3.86 |
| Alchemical Fire | 68 | 0.874 | 0.530 | 1.65 |
| Focus Lens | 36 | 0.957 | 0.896 | 1.07 |
| Lightning Scroll | 35 | 0.373 | 0.317 | 1.18 |
| Silence Wave | 26 | 0.209 | 0.301 | 0.69 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Yamato | Crushing Fists | 30 | 0.299 | 0.041 | 7.25 |
| Celeste | Tankbuster | 29 | 1.268 | 0.207 | 6.13 |
| Drifter | Crushing Fists | 25 | 0.287 | 0.054 | 5.27 |
| Rat King | Return Fire | 41 | 0.389 | 0.081 | 4.78 |
| Solomon | Tankbuster | 26 | 0.578 | 0.131 | 4.41 |
| Vindicta | Mystic Burst | 25 | 0.107 | 0.025 | 4.21 |
| Yamato | Melee Charge | 57 | 0.207 | 0.050 | 4.15 |
| Drifter | Melee Charge | 68 | 0.211 | 0.054 | 3.88 |
| Holliday | Tankbuster | 48 | 0.959 | 0.262 | 3.65 |
| Calico | Melee Charge | 27 | 0.170 | 0.052 | 3.25 |
| Vyper | Split Shot | 69 | 0.321 | 0.113 | 2.84 |
| Bebop | Spirit Snatch | 191 | 0.342 | 0.122 | 2.79 |
| Paradox | Express Shot | 143 | 0.229 | 0.597 | 0.38 |
| Mo & Krill | Quicksilver Reload | 150 | 0.843 | 0.328 | 2.57 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.156 | 2.56 |
| Bebop | Spirit Strike | 186 | 0.274 | 0.108 | 2.54 |
| Haze | Lucky Shot | 91 | 0.492 | 0.214 | 2.29 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.160 | 2.25 |
| Warden | Quicksilver Reload | 25 | 0.077 | 0.170 | 0.46 |
| Billy | Crushing Fists | 31 | 0.319 | 0.146 | 2.18 |
| Vyper | Mercurial Magnum | 58 | 0.288 | 0.134 | 2.15 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.643 | 2.14 |
| Deadman Danny | Cold Front | 46 | 0.236 | 0.500 | 0.47 |
| Vyper | Quicksilver Reload | 31 | 0.057 | 0.121 | 0.47 |
| Mo & Krill | Tankbuster | 118 | 3.292 | 1.573 | 2.09 |
| Calico | Mystic Shot | 30 | 0.381 | 0.774 | 0.49 |
| Venator | Siphon Bullets | 77 | 0.200 | 0.099 | 2.02 |
| Holliday | Mystic Burst | 33 | 0.200 | 0.099 | 2.02 |
| Mo & Krill | Arctic Blast | 25 | 3.043 | 1.552 | 1.96 |
| Deadman Danny | Toxic Bullets | 144 | 0.871 | 0.450 | 1.94 |
| Billy | Melee Charge | 48 | 0.242 | 0.128 | 1.89 |
| Shiv | Spirit Strike | 38 | 0.172 | 0.323 | 0.53 |
| Mo & Krill | Torment Pulse | 161 | 3.578 | 1.906 | 1.88 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.182 | 1.88 |
| Pocket | Cold Front | 59 | 0.339 | 0.636 | 0.53 |
| Abrams | Melee Charge | 129 | 0.306 | 0.163 | 1.88 |
| Lash | Spirit Burn | 69 | 0.946 | 0.521 | 1.81 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.098 | 1.80 |
| Seven | Toxic Bullets | 30 | 0.366 | 0.639 | 0.57 |
| Shiv | Cold Front | 21 | 0.381 | 0.226 | 1.69 |
