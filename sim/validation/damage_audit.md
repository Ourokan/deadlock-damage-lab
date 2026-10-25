# Sim vs real damage mix audit

Sample: 600 matches, 5773 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| The Doorman | 2 | 0.20 / 0.11 | 0.57 / 0.37 | 0.22 / 0.50 | 0.01 / 0.03 | 0.29 |
| Apollo | 6 | 0.24 / 0.21 | 0.29 / 0.47 | 0.16 / 0.14 | 0.29 / 0.18 | 0.18 |
| Rem | 23 | 0.25 / 0.25 | 0.54 / 0.46 | 0.16 / 0.25 | 0.04 / 0.04 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.11 | 0.09 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.22 | 0.04 / 0.04 | 0.07 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.06 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.44 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Warden | 33 | 0.52 / 0.49 | 0.31 / 0.37 | 0.11 / 0.11 | 0.03 / 0.02 | 0.06 |
| Vindicta | 131 | 0.44 / 0.48 | 0.49 / 0.46 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Solomon | 42 | 0.37 / 0.40 | 0.54 / 0.50 | 0.07 / 0.08 | 0.01 / 0.02 | 0.05 |
| Violet | 4 | 0.29 / 0.26 | 0.65 / 0.69 | 0.02 / 0.04 | 0.01 / 0.01 | 0.05 |
| Kelvin | 12 | 0.09 / 0.09 | 0.65 / 0.63 | 0.22 / 0.26 | 0.02 / 0.01 | 0.04 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.12 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.29 | 0.49 / 0.49 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Deadman Danny | 357 | 0.16 / 0.14 | 0.63 / 0.67 | 0.18 / 0.18 | 0.01 / 0.01 | 0.04 |
| Silver | 100 | 0.41 / 0.40 | 0.37 / 0.36 | 0.10 / 0.13 | 0.10 / 0.11 | 0.03 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.48 | 0.17 / 0.19 | 0.02 / 0.02 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.68 | 0.10 / 0.09 | 0.02 / 0.02 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.63 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Sinclair | 20 | 0.17 / 0.18 | 0.76 / 0.75 | 0.02 / 0.03 | 0.03 / 0.04 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.42 | 0.02 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.60 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.18 | 0.18 / 0.19 | 0.02 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.23 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.63 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.27 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.07 | 0.02 |
| Paige | 58 | 0.35 / 0.35 | 0.50 / 0.51 | 0.11 / 0.12 | 0.03 / 0.02 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| The Doorman | Tankbuster | item | 0.165 | 0.409 | 0.22 |
| McGinnis | Mini Turret | ability | 0.467 | 0.562 | 0.67 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.16 |
| Apollo | Flawless Advance | ability | 0.141 | 0.214 | 0.56 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.269 | 0.65 |
| Apollo | Disengaging Sigil | ability | 0.097 | 0.165 | 0.50 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.307 | 0.71 |
| Deadman Danny | Close The Deal | ability | 0.098 | 0.031 | 2.78 |
| Rem | Tankbuster | item | 0.063 | 0.125 | 0.50 |
| Apollo | MELEE | melee | 0.287 | 0.181 | 1.35 |
| The Doorman | Mystic Burst | item | 0.013 | 0.046 | 0.16 |
| Vindicta | Assassinate | ability | 0.162 | 0.107 | 1.68 |
| The Doorman | Luggage Cart | ability | 0.075 | 0.086 | 0.47 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.305 | 1.21 |
| Apollo | Itani Lo Sahn | ability | 0.056 | 0.091 | 0.52 |
| The Doorman | Hotel Guest | ability | 0.023 | 0.046 | 0.28 |
| Viscous | Express Shot | item | 0.052 | 0.019 | 3.10 |
| Solomon | Develop Queen | ability | 0.141 | 0.101 | 1.52 |
| Celeste | Shining Wonder | ability | 0.170 | 0.136 | 1.39 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.178 | 0.74 |
| Pocket | Affliction | ability | 0.120 | 0.156 | 0.73 |
| Warden | Last Stand | ability | 0.138 | 0.174 | 0.75 |
| Rem | Decay | item | 0.026 | 0.058 | 0.45 |
| Solomon | Rook Battery | ability | 0.167 | 0.137 | 1.32 |
| Violet | Living Ink | ability | 0.277 | 0.289 | 0.85 |
| Viscous | MELEE | melee | 0.047 | 0.089 | 0.61 |
| Violet | Abstract Landscape | ability | 0.169 | 0.188 | 0.80 |
| Sinclair | Spectral Assistant | ability | 0.200 | 0.174 | 1.22 |
| Viscous | Splatter | ability | 0.285 | 0.289 | 1.15 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.092 | 1.41 |
| The Doorman | Call Bell | ability | 0.475 | 0.239 | 1.08 |
| Rem | Pillow Toss | ability | 0.410 | 0.375 | 1.10 |
| Mina | Nox Nostra | ability | 0.128 | 0.156 | 0.79 |
| Paradox | Tankbuster | item | 0.074 | 0.053 | 1.62 |
| Viscous | Puddle Punch | ability | 0.123 | 0.107 | 1.33 |
| Rem | Naptime | ability | 0.115 | 0.085 | 1.35 |
| Shiv | Killing Blow | ability | 0.056 | 0.032 | 1.85 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.223 | 0.86 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.139 | 0.79 |
| The Doorman | Mystic Shot | item | 0.034 | 0.041 | 0.45 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1522 | 1.039 | 0.840 | 1.24 |
| Mystic Burst | 1465 | 0.284 | 0.237 | 1.20 |
| Quicksilver Reload | 1105 | 0.171 | 0.143 | 1.20 |
| Toxic Bullets | 862 | 0.532 | 0.529 | 1.01 |
| Spirit Snatch | 793 | 0.400 | 0.393 | 1.02 |
| Stalker | 790 | 0.219 | 0.205 | 1.07 |
| Torment Pulse | 707 | 1.663 | 1.428 | 1.17 |
| Ricochet | 695 | 0.156 | 0.176 | 0.89 |
| Spirit Strike | 675 | 0.291 | 0.305 | 0.95 |
| Spirit Burn | 579 | 0.773 | 0.570 | 1.36 |
| Express Shot | 552 | 0.677 | 0.494 | 1.37 |
| Escalating Exposure | 542 | 0.892 | 0.902 | 0.99 |
| Siphon Bullets | 521 | 0.248 | 0.243 | 1.02 |
| Tesla Bullets | 509 | 0.480 | 0.479 | 1.00 |
| Cold Front | 505 | 0.447 | 0.421 | 1.06 |
| Mystic Shot | 497 | 0.385 | 0.360 | 1.07 |
| Headhunter | 407 | 0.440 | 0.440 | 1.00 |
| Melee Charge | 379 | 0.240 | 0.115 | 2.08 |
| Capacitor | 375 | 0.696 | 0.697 | 1.00 |
| Headshot Booster | 370 | 0.215 | 0.194 | 1.11 |
| Mercurial Magnum | 339 | 0.295 | 0.289 | 1.02 |
| Rebuttal | 212 | 0.063 | 0.050 | 1.24 |
| Mystic Reverb | 204 | 1.313 | 1.555 | 0.84 |
| Lucky Shot | 200 | 0.397 | 0.227 | 1.75 |
| Arctic Blast | 171 | 1.325 | 0.799 | 1.66 |
| Split Shot | 170 | 0.257 | 0.254 | 1.01 |
| Crushing Fists | 143 | 0.303 | 0.114 | 2.67 |
| Phantom Strike | 123 | 0.311 | 0.227 | 1.37 |
| Scourge | 110 | 2.102 | 1.936 | 1.08 |
| Decay | 107 | 1.538 | 1.660 | 0.93 |
| Return Fire | 95 | 0.449 | 0.140 | 3.22 |
| Alchemical Fire | 88 | 1.003 | 1.169 | 0.86 |
| Focus Lens | 36 | 0.957 | 0.887 | 1.08 |
| Lightning Scroll | 35 | 0.373 | 0.368 | 1.01 |
| Silence Wave | 26 | 0.209 | 0.201 | 1.04 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.045 | 6.34 |
| Rat King | Return Fire | 41 | 0.389 | 0.094 | 4.16 |
| Drifter | Melee Charge | 68 | 0.211 | 0.051 | 4.13 |
| Billy | Crushing Fists | 31 | 0.319 | 0.104 | 3.08 |
| Baba | Torment Pulse | 138 | 5.029 | 1.800 | 2.79 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.212 | 2.61 |
| Calico | Melee Charge | 27 | 0.170 | 0.067 | 2.54 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.090 | 2.52 |
| Haze | Lucky Shot | 91 | 0.492 | 0.198 | 2.49 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.131 | 2.28 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.169 | 2.13 |
| Lash | Spirit Burn | 69 | 0.946 | 0.486 | 1.95 |
| Billy | Melee Charge | 48 | 0.242 | 0.125 | 1.93 |
| Paradox | Tankbuster | 146 | 0.656 | 0.342 | 1.92 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.208 | 1.91 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.097 | 1.81 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.109 | 1.77 |
| Drifter | Tankbuster | 101 | 0.587 | 0.340 | 1.73 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.252 | 0.60 |
| Yamato | Melee Charge | 57 | 0.207 | 0.125 | 1.66 |
| Abrams | Melee Charge | 129 | 0.306 | 0.185 | 1.65 |
| Bebop | Tankbuster | 43 | 1.252 | 0.773 | 1.62 |
| Calico | Arctic Blast | 102 | 1.394 | 0.871 | 1.60 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.201 | 1.56 |
| Infernus | Ricochet | 66 | 0.110 | 0.172 | 0.64 |
| Shiv | Express Shot | 125 | 0.882 | 0.567 | 1.55 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.264 | 1.55 |
| Yamato | Express Shot | 46 | 0.925 | 0.611 | 1.51 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.330 | 1.50 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.185 | 0.67 |
| Mina | Spirit Burn | 110 | 0.926 | 0.634 | 1.46 |
| Shiv | Torment Pulse | 50 | 1.378 | 0.951 | 1.45 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.163 | 1.44 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.238 | 1.44 |
| Wraith | Ricochet | 185 | 0.133 | 0.186 | 0.71 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.402 | 1.40 |
| Lash | Tankbuster | 193 | 1.645 | 1.191 | 1.38 |
| McGinnis | Escalating Exposure | 29 | 1.974 | 1.477 | 1.34 |
| Lash | Mystic Burst | 210 | 0.391 | 0.293 | 1.33 |
| Haze | Quicksilver Reload | 24 | 0.044 | 0.057 | 0.76 |
