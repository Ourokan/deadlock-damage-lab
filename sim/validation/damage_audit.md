# Sim vs real damage mix audit

Sample: 600 matches, 6429 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Rem | 23 | 0.25 / 0.25 | 0.54 / 0.47 | 0.16 / 0.25 | 0.04 / 0.04 | 0.09 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.73 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.11 | 0.08 |
| Warden | 33 | 0.52 / 0.48 | 0.31 / 0.38 | 0.11 / 0.10 | 0.03 / 0.02 | 0.07 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.08 | 0.07 |
| Vindicta | 131 | 0.44 / 0.49 | 0.49 / 0.45 | 0.05 / 0.05 | 0.01 / 0.01 | 0.06 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.21 | 0.04 / 0.04 | 0.06 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.43 | 0.23 / 0.24 | 0.03 / 0.05 | 0.06 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.58 | 0.17 / 0.15 | 0.17 / 0.15 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.04 |
| Calico | 110 | 0.13 / 0.13 | 0.38 / 0.40 | 0.31 / 0.34 | 0.15 / 0.13 | 0.04 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.69 | 0.17 / 0.20 | 0.03 / 0.02 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.48 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.34 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.10 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Sinclair | 20 | 0.17 / 0.19 | 0.76 / 0.74 | 0.02 / 0.03 | 0.03 / 0.04 | 0.04 |
| Holliday | 73 | 0.27 / 0.27 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Silver | 100 | 0.41 / 0.40 | 0.37 / 0.35 | 0.10 / 0.13 | 0.10 / 0.11 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.47 | 0.17 / 0.20 | 0.02 / 0.02 | 0.03 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.41 | 0.03 |
| Dynamo | 53 | 0.23 / 0.23 | 0.62 / 0.64 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.68 | 0.10 / 0.09 | 0.02 / 0.02 | 0.02 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.21 | 0.01 / 0.01 | 0.02 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.18 | 0.18 / 0.19 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.19 | 0.05 / 0.06 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Paige | 58 | 0.35 / 0.36 | 0.50 / 0.50 | 0.11 / 0.12 | 0.03 / 0.02 | 0.02 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.60 | 0.17 / 0.18 | 0.03 / 0.04 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.23 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.63 | 0.05 / 0.04 | 0.03 / 0.02 | 0.02 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.02 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.41 | 0.03 / 0.02 | 0.07 / 0.07 | 0.02 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.02 |
| Solomon | 136 | 0.25 / 0.25 | 0.64 / 0.63 | 0.08 / 0.08 | 0.02 / 0.02 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| McGinnis | Mini Turret | ability | 0.467 | 0.570 | 0.66 |
| Baba | Torment Pulse | item | 0.170 | 0.093 | 2.16 |
| Vindicta | Assassinate | ability | 0.162 | 0.106 | 1.73 |
| Warden | Last Stand | ability | 0.138 | 0.199 | 0.64 |
| Rem | Tankbuster | item | 0.063 | 0.124 | 0.50 |
| Sinclair | Vexing Bolt | ability | 0.317 | 0.294 | 1.21 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.302 | 1.21 |
| Sinclair | Spectral Assistant | ability | 0.200 | 0.169 | 1.33 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.177 | 0.75 |
| Pocket | Affliction | ability | 0.120 | 0.158 | 0.72 |
| Viscous | Express Shot | item | 0.052 | 0.025 | 2.58 |
| Celeste | Shining Wonder | ability | 0.170 | 0.142 | 1.33 |
| Viscous | Splatter | ability | 0.285 | 0.294 | 1.18 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.101 | 1.40 |
| Viscous | Goo Ball | ability | 0.107 | 0.086 | 1.52 |
| Rem | Decay | item | 0.026 | 0.057 | 0.45 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.273 | 1.16 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.227 | 0.85 |
| Viscous | Puddle Punch | ability | 0.123 | 0.112 | 1.34 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.093 | 1.38 |
| Paradox | Tankbuster | item | 0.074 | 0.053 | 1.61 |
| Mina | Nox Nostra | ability | 0.128 | 0.155 | 0.80 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.170 | 1.21 |
| Abrams | MELEE | melee | 0.424 | 0.414 | 1.08 |
| Haze | Bullet Dance | ability | 0.124 | 0.152 | 0.80 |
| Viscous | MELEE | melee | 0.047 | 0.085 | 0.68 |
| Shiv | Killing Blow | ability | 0.056 | 0.034 | 1.77 |
| Rem | Naptime | ability | 0.115 | 0.087 | 1.31 |
| Baba | MELEE | melee | 0.124 | 0.114 | 1.28 |
| Vindicta | Crow Familiar | ability | 0.155 | 0.144 | 1.22 |
| Rem | Pillow Toss | ability | 0.410 | 0.378 | 1.08 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.136 | 0.81 |
| Lash | Ground Strike | ability | 0.350 | 0.352 | 1.08 |
| Apollo | MELEE | melee | 0.171 | 0.151 | 1.18 |
| Graves | Jar of Dead | ability | 0.212 | 0.234 | 0.89 |
| The Doorman | Call Bell | ability | 0.474 | 0.461 | 1.06 |
| Calico | MELEE | melee | 0.149 | 0.126 | 1.19 |
| Lady Geist | Malice | ability | 0.144 | 0.171 | 0.86 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.321 | 0.92 |
| Kelvin | MELEE | melee | 0.034 | 0.018 | 2.06 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1865 | 1.087 | 0.862 | 1.26 |
| Mystic Burst | 1669 | 0.292 | 0.238 | 1.23 |
| Quicksilver Reload | 1114 | 0.171 | 0.142 | 1.21 |
| Toxic Bullets | 875 | 0.530 | 0.533 | 0.99 |
| Spirit Snatch | 856 | 0.411 | 0.411 | 1.00 |
| Torment Pulse | 812 | 1.622 | 1.289 | 1.26 |
| Stalker | 794 | 0.219 | 0.208 | 1.05 |
| Spirit Strike | 710 | 0.291 | 0.300 | 0.97 |
| Ricochet | 695 | 0.156 | 0.179 | 0.87 |
| Spirit Burn | 675 | 0.827 | 0.590 | 1.40 |
| Mystic Shot | 673 | 0.407 | 0.350 | 1.16 |
| Escalating Exposure | 605 | 0.928 | 0.900 | 1.03 |
| Express Shot | 553 | 0.677 | 0.481 | 1.41 |
| Cold Front | 521 | 0.453 | 0.433 | 1.05 |
| Siphon Bullets | 521 | 0.248 | 0.239 | 1.03 |
| Tesla Bullets | 509 | 0.480 | 0.479 | 1.00 |
| Melee Charge | 433 | 0.255 | 0.114 | 2.24 |
| Headhunter | 410 | 0.439 | 0.442 | 0.99 |
| Capacitor | 375 | 0.696 | 0.695 | 1.00 |
| Headshot Booster | 374 | 0.214 | 0.194 | 1.10 |
| Mercurial Magnum | 340 | 0.296 | 0.286 | 1.03 |
| Rebuttal | 232 | 0.064 | 0.054 | 1.19 |
| Mystic Reverb | 207 | 1.320 | 1.572 | 0.84 |
| Lucky Shot | 200 | 0.397 | 0.225 | 1.76 |
| Arctic Blast | 171 | 1.325 | 0.815 | 1.63 |
| Split Shot | 170 | 0.257 | 0.249 | 1.03 |
| Crushing Fists | 147 | 0.307 | 0.114 | 2.69 |
| Decay | 126 | 1.500 | 1.615 | 0.93 |
| Phantom Strike | 125 | 0.315 | 0.228 | 1.38 |
| Scourge | 117 | 2.095 | 1.837 | 1.14 |
| Alchemical Fire | 105 | 0.971 | 1.036 | 0.94 |
| Return Fire | 96 | 0.445 | 0.126 | 3.54 |
| Lightning Scroll | 41 | 0.376 | 0.297 | 1.27 |
| Focus Lens | 39 | 0.941 | 0.857 | 1.10 |
| Silence Wave | 29 | 0.232 | 0.199 | 1.16 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.048 | 5.97 |
| Apollo | Melee Charge | 58 | 0.421 | 0.082 | 5.13 |
| Rat King | Return Fire | 41 | 0.389 | 0.083 | 4.70 |
| Drifter | Melee Charge | 68 | 0.211 | 0.054 | 3.90 |
| Billy | Crushing Fists | 31 | 0.319 | 0.103 | 3.10 |
| Baba | Torment Pulse | 138 | 5.029 | 1.795 | 2.80 |
| Calico | Melee Charge | 27 | 0.170 | 0.063 | 2.70 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.212 | 2.60 |
| Haze | Lucky Shot | 91 | 0.492 | 0.198 | 2.48 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.092 | 2.45 |
| Violet | Torment Pulse | 69 | 0.825 | 0.366 | 2.26 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.170 | 2.12 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.143 | 2.09 |
| Billy | Melee Charge | 48 | 0.242 | 0.124 | 1.96 |
| Paradox | Tankbuster | 146 | 0.656 | 0.337 | 1.95 |
| Apollo | Mystic Burst | 66 | 0.616 | 0.327 | 1.88 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.223 | 1.79 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.099 | 1.79 |
| Yamato | Melee Charge | 57 | 0.207 | 0.118 | 1.75 |
| Drifter | Tankbuster | 101 | 0.587 | 0.338 | 1.74 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.112 | 1.72 |
| Lash | Spirit Burn | 69 | 0.946 | 0.557 | 1.70 |
| Kelvin | Escalating Exposure | 40 | 4.081 | 2.455 | 1.66 |
| Abrams | Melee Charge | 129 | 0.306 | 0.185 | 1.65 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.233 | 0.61 |
| Bebop | Tankbuster | 43 | 1.252 | 0.776 | 1.61 |
| Shiv | Express Shot | 125 | 0.882 | 0.555 | 1.59 |
| Violet | Mystic Burst | 66 | 0.227 | 0.144 | 1.57 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.262 | 1.56 |
| Bebop | Mystic Burst | 110 | 0.313 | 0.203 | 1.54 |
| Calico | Arctic Blast | 102 | 1.394 | 0.906 | 1.54 |
| Solomon | Spirit Burn | 23 | 1.019 | 0.662 | 1.54 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.323 | 1.54 |
| Infernus | Ricochet | 66 | 0.110 | 0.170 | 0.65 |
| Yamato | Express Shot | 46 | 0.925 | 0.605 | 1.53 |
| Mina | Spirit Burn | 110 | 0.926 | 0.609 | 1.52 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.186 | 0.66 |
| Violet | Tankbuster | 206 | 1.178 | 0.781 | 1.51 |
| Paradox | Mystic Shot | 62 | 0.342 | 0.231 | 1.48 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.163 | 1.44 |
