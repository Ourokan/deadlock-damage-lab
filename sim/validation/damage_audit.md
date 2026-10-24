# Sim vs real damage mix audit

Sample: 600 matches, 5115 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides.

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Apollo | 6 | 0.24 / 0.25 | 0.29 / 0.45 | 0.16 / 0.09 | 0.29 / 0.21 | 0.16 |
| Paradox | 168 | 0.24 / 0.34 | 0.48 / 0.52 | 0.23 / 0.10 | 0.03 / 0.04 | 0.14 |
| Viscous | 29 | 0.13 / 0.18 | 0.51 / 0.57 | 0.28 / 0.16 | 0.05 / 0.07 | 0.12 |
| Kelvin | 12 | 0.09 / 0.17 | 0.65 / 0.68 | 0.22 / 0.13 | 0.02 / 0.02 | 0.12 |
| Mo & Krill | 176 | 0.07 / 0.09 | 0.47 / 0.58 | 0.39 / 0.29 | 0.05 / 0.04 | 0.12 |
| Shiv | 209 | 0.27 / 0.33 | 0.48 / 0.53 | 0.16 / 0.05 | 0.08 / 0.08 | 0.12 |
| The Doorman | 2 | 0.20 / 0.27 | 0.57 / 0.57 | 0.22 / 0.12 | 0.01 / 0.03 | 0.10 |
| Paige | 58 | 0.35 / 0.39 | 0.50 / 0.55 | 0.11 / 0.03 | 0.03 / 0.02 | 0.10 |
| Vyper | 78 | 0.46 / 0.55 | 0.26 / 0.26 | 0.25 / 0.17 | 0.02 / 0.02 | 0.09 |
| Warden | 33 | 0.52 / 0.46 | 0.31 / 0.38 | 0.11 / 0.13 | 0.03 / 0.02 | 0.09 |
| Nurse Harrow | 347 | 0.29 / 0.36 | 0.61 / 0.53 | 0.06 / 0.06 | 0.03 / 0.05 | 0.09 |
| Bebop | 254 | 0.18 / 0.16 | 0.56 / 0.63 | 0.19 / 0.17 | 0.05 / 0.03 | 0.07 |
| McGinnis | 49 | 0.20 / 0.20 | 0.64 / 0.71 | 0.12 / 0.08 | 0.02 / 0.01 | 0.07 |
| Seven | 95 | 0.20 / 0.22 | 0.66 / 0.71 | 0.10 / 0.05 | 0.02 / 0.02 | 0.06 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.56 | 0.12 / 0.06 | 0.02 / 0.02 | 0.06 |
| Rem | 23 | 0.25 / 0.29 | 0.54 / 0.55 | 0.16 / 0.11 | 0.04 / 0.05 | 0.06 |
| Celeste | 77 | 0.16 / 0.19 | 0.61 / 0.63 | 0.17 / 0.12 | 0.04 / 0.05 | 0.06 |
| Mirage | 45 | 0.31 / 0.34 | 0.48 / 0.44 | 0.17 / 0.17 | 0.02 / 0.03 | 0.05 |
| Holliday | 73 | 0.27 / 0.29 | 0.54 / 0.56 | 0.13 / 0.09 | 0.05 / 0.06 | 0.05 |
| Sinclair | 20 | 0.17 / 0.20 | 0.76 / 0.73 | 0.02 / 0.02 | 0.03 / 0.05 | 0.05 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.60 | 0.25 / 0.21 | 0.03 / 0.03 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.54 | 0.07 / 0.04 | 0.01 / 0.02 | 0.05 |
| Drifter | 186 | 0.26 / 0.27 | 0.44 / 0.46 | 0.17 / 0.14 | 0.11 / 0.12 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.31 | 0.49 / 0.53 | 0.16 / 0.14 | 0.01 / 0.01 | 0.04 |
| Victor | 129 | 0.15 / 0.18 | 0.64 / 0.63 | 0.16 / 0.13 | 0.03 / 0.04 | 0.04 |
| Venator | 257 | 0.48 / 0.51 | 0.40 / 0.39 | 0.03 / 0.01 | 0.07 / 0.08 | 0.03 |
| Abrams | 138 | 0.23 / 0.25 | 0.20 / 0.21 | 0.13 / 0.12 | 0.42 / 0.41 | 0.03 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.39 | 0.14 / 0.15 | 0.22 / 0.25 | 0.03 |
| Infernus | 173 | 0.23 / 0.24 | 0.60 / 0.61 | 0.13 / 0.12 | 0.03 / 0.02 | 0.03 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.65 | 0.16 / 0.19 | 0.02 / 0.02 | 0.03 |
| Lady Geist | 37 | 0.29 / 0.31 | 0.62 / 0.63 | 0.05 / 0.03 | 0.03 / 0.03 | 0.03 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.32 | 0.15 / 0.14 | 0.03 |
| Silver | 100 | 0.41 / 0.43 | 0.37 / 0.37 | 0.10 / 0.10 | 0.10 / 0.10 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.40 | 0.17 / 0.17 | 0.18 / 0.18 | 0.02 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.08 | 0.05 / 0.04 | 0.02 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.35 | 0.26 / 0.27 | 0.04 / 0.04 | 0.02 |
| Vindicta | 131 | 0.44 / 0.45 | 0.49 / 0.50 | 0.05 / 0.04 | 0.01 / 0.01 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.56 | 0.03 / 0.03 | 0.05 / 0.06 | 0.01 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.42 | 0.24 / 0.24 | 0.01 / 0.01 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.19 | 0.01 / 0.01 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Shiv | Express Shot | item | 0.086 | 0.000 | - |
| Kelvin | Escalating Exposure | item | 0.068 | 0.000 | - |
| Paige | Express Shot | item | 0.066 | 0.000 | - |
| Victor | Escalating Exposure | item | 0.065 | 0.000 | - |
| Seven | Escalating Exposure | item | 0.065 | 0.000 | - |
| McGinnis | Escalating Exposure | item | 0.055 | 0.000 | - |
| Viscous | Express Shot | item | 0.052 | 0.000 | - |
| Sinclair | Rabbit Hex | ability | 0.047 | 0.000 | - |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| The Doorman | Call Bell | ability | 0.475 | 0.347 | 1.91 |
| Infernus | Escalating Exposure | item | 0.032 | 0.000 | - |
| Yamato | Express Shot | item | 0.031 | 0.000 | - |
| Kelvin | Arctic Beam | ability | 0.397 | 0.395 | 1.91 |
| The Doorman | Tankbuster | item | 0.165 | 0.058 | 3.98 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.267 | 0.51 |
| Kelvin | Frost Grenade | ability | 0.248 | 0.289 | 1.63 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.294 | 1.51 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.239 | 1.55 |
| Bebop | Hyper Beam | ability | 0.129 | 0.202 | 0.58 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.098 | 0.33 |
| Vyper | Split Shot | item | 0.110 | 0.049 | 2.69 |
| Rem | Tankbuster | item | 0.063 | 0.015 | 4.97 |
| Apollo | MELEE | melee | 0.287 | 0.209 | 1.40 |
| Paradox | Mystic Reverb | item | 0.063 | 0.019 | 4.72 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.288 | 1.33 |
| Warden | Last Stand | ability | 0.138 | 0.192 | 0.63 |
| Apollo | Flawless Advance | ability | 0.141 | 0.216 | 0.67 |
| Seven | Power Surge | ability | 0.205 | 0.153 | 1.45 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.321 | 0.79 |
| Paradox | Tankbuster | item | 0.074 | 0.038 | 2.75 |
| Viscous | Goo Ball | ability | 0.107 | 0.075 | 1.90 |
| Seven | Storm Cloud | ability | 0.202 | 0.279 | 0.79 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.301 | 1.23 |
| McGinnis | Mini Turret | ability | 0.467 | 0.402 | 1.15 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.153 | 0.65 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.265 | 1.22 |
| Celeste | Tankbuster | item | 0.030 | 0.006 | 6.61 |
| Holliday | Tankbuster | item | 0.060 | 0.025 | 2.60 |
| Solomon | Tankbuster | item | 0.046 | 0.015 | 3.34 |
| Abrams | MELEE | melee | 0.424 | 0.406 | 1.14 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Mystic Burst | 1253 | 0.285 | 0.185 | 1.53 |
| Tankbuster | 1203 | 0.998 | 0.503 | 1.98 |
| Quicksilver Reload | 1104 | 0.171 | 0.154 | 1.11 |
| Stalker | 787 | 0.219 | 0.218 | 1.00 |
| Spirit Snatch | 709 | 0.367 | 0.303 | 1.21 |
| Ricochet | 681 | 0.155 | 0.000 | - |
| Toxic Bullets | 595 | 0.468 | 0.477 | 0.98 |
| Spirit Strike | 560 | 0.234 | 0.214 | 1.09 |
| Spirit Burn | 512 | 0.771 | 0.597 | 1.29 |
| Torment Pulse | 490 | 1.608 | 1.176 | 1.37 |
| Escalating Exposure | 485 | 0.888 | 0.000 | - |
| Siphon Bullets | 474 | 0.242 | 0.234 | 1.03 |
| Cold Front | 459 | 0.474 | 0.395 | 1.20 |
| Headhunter | 407 | 0.440 | 0.433 | 1.01 |
| Tesla Bullets | 404 | 0.439 | 0.427 | 1.03 |
| Melee Charge | 379 | 0.240 | 0.105 | 2.29 |
| Mystic Shot | 373 | 0.361 | 0.359 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.181 | 1.19 |
| Express Shot | 369 | 0.571 | 0.000 | - |
| Mercurial Magnum | 338 | 0.295 | 0.293 | 1.01 |
| Capacitor | 309 | 0.660 | 0.664 | 0.99 |
| Rebuttal | 197 | 0.063 | 0.033 | 1.90 |
| Lucky Shot | 197 | 0.391 | 0.200 | 1.95 |
| Mystic Reverb | 187 | 1.313 | 0.334 | 3.94 |
| Arctic Blast | 169 | 1.329 | 0.687 | 1.93 |
| Split Shot | 147 | 0.279 | 0.188 | 1.48 |
| Crushing Fists | 143 | 0.303 | 0.092 | 3.30 |
| Phantom Strike | 120 | 0.306 | 0.201 | 1.52 |
| Decay | 105 | 1.542 | 1.095 | 1.41 |
| Scourge | 104 | 2.035 | 1.953 | 1.04 |
| Return Fire | 92 | 0.439 | 0.113 | 3.88 |
| Alchemical Fire | 68 | 0.874 | 0.532 | 1.64 |
| Focus Lens | 36 | 0.957 | 0.837 | 1.14 |
| Lightning Scroll | 33 | 0.379 | 0.328 | 1.16 |
| Silence Wave | 25 | 0.209 | 0.297 | 0.70 |
