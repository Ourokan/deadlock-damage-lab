# Sim vs real damage mix audit

Sample: 600 matches, 5773 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| The Doorman | 2 | 0.20 / 0.11 | 0.57 / 0.37 | 0.22 / 0.50 | 0.01 / 0.03 | 0.29 |
| Apollo | 6 | 0.24 / 0.22 | 0.29 / 0.49 | 0.16 / 0.12 | 0.29 / 0.17 | 0.20 |
| Mirage | 45 | 0.31 / 0.36 | 0.48 / 0.39 | 0.17 / 0.22 | 0.02 / 0.03 | 0.11 |
| Rem | 23 | 0.25 / 0.25 | 0.54 / 0.46 | 0.16 / 0.24 | 0.04 / 0.04 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.11 | 0.08 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Kelvin | 12 | 0.09 / 0.10 | 0.65 / 0.60 | 0.22 / 0.29 | 0.02 / 0.02 | 0.08 |
| Vyper | 78 | 0.46 / 0.51 | 0.26 / 0.20 | 0.25 / 0.27 | 0.02 / 0.02 | 0.08 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.22 | 0.04 / 0.05 | 0.07 |
| Paige | 58 | 0.35 / 0.39 | 0.50 / 0.45 | 0.11 / 0.13 | 0.03 / 0.02 | 0.07 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.06 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.44 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Victor | 129 | 0.15 / 0.17 | 0.64 / 0.58 | 0.16 / 0.20 | 0.03 / 0.03 | 0.06 |
| Warden | 33 | 0.52 / 0.49 | 0.31 / 0.37 | 0.11 / 0.11 | 0.03 / 0.02 | 0.06 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.45 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Violet | 4 | 0.29 / 0.26 | 0.65 / 0.69 | 0.02 / 0.04 | 0.01 / 0.01 | 0.05 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.50 | 0.07 / 0.08 | 0.01 / 0.02 | 0.05 |
| Seven | 95 | 0.20 / 0.24 | 0.66 / 0.63 | 0.10 / 0.10 | 0.02 / 0.02 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.12 | 0.04 |
| Infernus | 173 | 0.23 / 0.24 | 0.60 / 0.57 | 0.13 / 0.16 | 0.03 / 0.02 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.29 | 0.49 / 0.49 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.34 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Silver | 100 | 0.41 / 0.42 | 0.37 / 0.35 | 0.10 / 0.13 | 0.10 / 0.11 | 0.04 |
| Deadman Danny | 357 | 0.16 / 0.14 | 0.63 / 0.67 | 0.18 / 0.18 | 0.01 / 0.01 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Venator | 257 | 0.48 / 0.50 | 0.40 / 0.39 | 0.03 / 0.02 | 0.07 / 0.08 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.57 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.75 | 0.02 / 0.03 | 0.03 / 0.04 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.42 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.18 | 0.18 / 0.19 | 0.02 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.23 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.63 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| The Doorman | Tankbuster | item | 0.165 | 0.409 | 0.22 |
| Bebop | Grapple Arm | ability | 0.046 | 0.000 | - |
| McGinnis | Mini Turret | ability | 0.467 | 0.562 | 0.67 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.199 | 1.69 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.15 |
| Apollo | Flawless Advance | ability | 0.141 | 0.225 | 0.57 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.173 | 0.51 |
| Apollo | MELEE | melee | 0.287 | 0.173 | 1.50 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.270 | 0.65 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.308 | 0.71 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.031 | 2.77 |
| Vindicta | Assassinate | ability | 0.162 | 0.105 | 1.71 |
| The Doorman | Mystic Burst | item | 0.013 | 0.046 | 0.16 |
| Kelvin | Arctic Beam | ability | 0.397 | 0.358 | 1.24 |
| Victor | Pain Battery | ability | 0.276 | 0.228 | 1.36 |
| Rem | Tankbuster | item | 0.063 | 0.124 | 0.51 |
| Vyper | Lethal Venom | ability | 0.112 | 0.068 | 1.85 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.332 | 0.82 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.086 | 0.47 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.304 | 1.22 |
| Apollo | Itani Lo Sahn | ability | 0.056 | 0.096 | 0.52 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.023 | 2.86 |
| Viscous | Express Shot | item | 0.052 | 0.019 | 3.17 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.046 | 0.28 |
| Paige | Bookwyrm | ability | 0.320 | 0.302 | 1.20 |
| Seven | Lightning Ball | ability | 0.198 | 0.175 | 1.34 |
| Solomon | Develop Queen | ability | 0.141 | 0.101 | 1.50 |
| Celeste | Shining Wonder | ability | 0.170 | 0.136 | 1.40 |
| Infernus | Flame Dash | ability | 0.216 | 0.179 | 1.29 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.177 | 0.74 |
| Pocket | Affliction | ability | 0.120 | 0.156 | 0.72 |
| Warden | Last Stand | ability | 0.138 | 0.174 | 0.75 |
| Violet | Living Ink | ability | 0.277 | 0.289 | 0.85 |
| Seven | Power Surge | ability | 0.205 | 0.195 | 1.25 |
| Solomon | Rook Battery | ability | 0.167 | 0.136 | 1.32 |
| Viscous | MELEE | melee | 0.047 | 0.089 | 0.61 |
| Rem | Decay | item | 0.026 | 0.056 | 0.46 |
| Violet | Abstract Landscape | ability | 0.169 | 0.188 | 0.80 |
| Viscous | Splatter | ability | 0.285 | 0.289 | 1.14 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.092 | 1.41 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1522 | 1.039 | 0.839 | 1.24 |
| Mystic Burst | 1465 | 0.284 | 0.237 | 1.20 |
| Quicksilver Reload | 1105 | 0.171 | 0.142 | 1.20 |
| Toxic Bullets | 862 | 0.532 | 0.533 | 1.00 |
| Spirit Snatch | 793 | 0.400 | 0.393 | 1.02 |
| Stalker | 790 | 0.219 | 0.204 | 1.07 |
| Torment Pulse | 707 | 1.663 | 1.425 | 1.17 |
| Ricochet | 695 | 0.156 | 0.178 | 0.88 |
| Spirit Strike | 675 | 0.291 | 0.305 | 0.95 |
| Spirit Burn | 579 | 0.773 | 0.567 | 1.36 |
| Express Shot | 552 | 0.677 | 0.493 | 1.37 |
| Escalating Exposure | 542 | 0.892 | 0.878 | 1.02 |
| Siphon Bullets | 521 | 0.248 | 0.241 | 1.03 |
| Tesla Bullets | 509 | 0.480 | 0.480 | 1.00 |
| Cold Front | 505 | 0.447 | 0.423 | 1.06 |
| Mystic Shot | 497 | 0.385 | 0.359 | 1.07 |
| Headhunter | 407 | 0.440 | 0.437 | 1.01 |
| Melee Charge | 379 | 0.240 | 0.115 | 2.08 |
| Capacitor | 375 | 0.696 | 0.694 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.194 | 1.11 |
| Mercurial Magnum | 339 | 0.295 | 0.287 | 1.03 |
| Rebuttal | 212 | 0.063 | 0.053 | 1.18 |
| Mystic Reverb | 204 | 1.313 | 1.538 | 0.85 |
| Lucky Shot | 200 | 0.397 | 0.227 | 1.75 |
| Arctic Blast | 171 | 1.325 | 0.799 | 1.66 |
| Split Shot | 170 | 0.257 | 0.253 | 1.01 |
| Crushing Fists | 143 | 0.303 | 0.114 | 2.66 |
| Phantom Strike | 123 | 0.311 | 0.227 | 1.37 |
| Scourge | 110 | 2.102 | 1.987 | 1.06 |
| Decay | 107 | 1.538 | 1.661 | 0.93 |
| Return Fire | 95 | 0.449 | 0.133 | 3.36 |
| Alchemical Fire | 88 | 1.003 | 1.161 | 0.86 |
| Focus Lens | 36 | 0.957 | 0.889 | 1.08 |
| Lightning Scroll | 35 | 0.373 | 0.364 | 1.02 |
| Silence Wave | 26 | 0.209 | 0.200 | 1.05 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.039 | 7.36 |
| Drifter | Melee Charge | 68 | 0.211 | 0.050 | 4.19 |
| Rat King | Return Fire | 41 | 0.389 | 0.099 | 3.94 |
| Calico | Melee Charge | 27 | 0.170 | 0.051 | 3.35 |
| Billy | Crushing Fists | 31 | 0.319 | 0.098 | 3.24 |
| Baba | Torment Pulse | 138 | 5.029 | 1.801 | 2.79 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.212 | 2.60 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.091 | 2.50 |
| Haze | Lucky Shot | 91 | 0.492 | 0.197 | 2.50 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.167 | 2.16 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.142 | 2.11 |
| Billy | Melee Charge | 48 | 0.242 | 0.127 | 1.91 |
| Paradox | Tankbuster | 146 | 0.656 | 0.344 | 1.91 |
| Lash | Spirit Burn | 69 | 0.946 | 0.497 | 1.90 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.211 | 1.89 |
| Yamato | Melee Charge | 57 | 0.207 | 0.112 | 1.86 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.097 | 1.82 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.109 | 1.76 |
| Drifter | Tankbuster | 101 | 0.587 | 0.341 | 1.72 |
| Bebop | Tankbuster | 43 | 1.252 | 0.762 | 1.64 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.220 | 0.62 |
| Abrams | Melee Charge | 129 | 0.306 | 0.190 | 1.61 |
| Calico | Arctic Blast | 102 | 1.394 | 0.876 | 1.59 |
| Yamato | Express Shot | 46 | 0.925 | 0.588 | 1.57 |
| Shiv | Express Shot | 125 | 0.882 | 0.565 | 1.56 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.264 | 1.55 |
| Infernus | Ricochet | 66 | 0.110 | 0.171 | 0.65 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.202 | 1.55 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.189 | 0.66 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.328 | 1.51 |
| Mina | Spirit Burn | 110 | 0.926 | 0.625 | 1.48 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.952 | 1.45 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.237 | 1.44 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.164 | 1.43 |
| Venator | Ricochet | 36 | 0.114 | 0.161 | 0.71 |
| Wraith | Ricochet | 185 | 0.133 | 0.185 | 0.72 |
| Lash | Tankbuster | 193 | 1.645 | 1.181 | 1.39 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.415 | 1.38 |
| Haze | Tesla Bullets | 47 | 0.434 | 0.321 | 1.35 |
| McGinnis | Escalating Exposure | 29 | 1.974 | 1.472 | 1.34 |
