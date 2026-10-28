# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Warden | 33 | 0.52 / 0.47 | 0.31 / 0.37 | 0.11 / 0.12 | 0.03 / 0.03 | 0.06 |
| Dynamo | 53 | 0.23 / 0.25 | 0.62 / 0.58 | 0.08 / 0.09 | 0.05 / 0.05 | 0.04 |
| Calico | 110 | 0.13 / 0.12 | 0.38 / 0.40 | 0.31 / 0.32 | 0.15 / 0.15 | 0.03 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.29 | 0.04 / 0.03 | 0.03 |
| Silver | 100 | 0.41 / 0.39 | 0.37 / 0.37 | 0.10 / 0.12 | 0.10 / 0.11 | 0.03 |
| Celeste | 77 | 0.16 / 0.14 | 0.61 / 0.62 | 0.17 / 0.18 | 0.04 / 0.04 | 0.03 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.50 | 0.16 / 0.18 | 0.01 / 0.01 | 0.03 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.39 | 0.17 / 0.18 | 0.18 / 0.19 | 0.03 |
| Abrams | 138 | 0.23 / 0.21 | 0.20 / 0.20 | 0.13 / 0.13 | 0.42 / 0.44 | 0.03 |
| Billy | 93 | 0.21 / 0.19 | 0.41 / 0.42 | 0.14 / 0.15 | 0.22 / 0.23 | 0.03 |
| Violet | 376 | 0.19 / 0.21 | 0.67 / 0.65 | 0.10 / 0.10 | 0.02 / 0.02 | 0.03 |
| Paradox | 168 | 0.24 / 0.23 | 0.48 / 0.50 | 0.23 / 0.24 | 0.03 / 0.02 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.31 | 0.62 / 0.59 | 0.05 / 0.05 | 0.03 / 0.04 | 0.02 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.57 | 0.16 / 0.15 | 0.05 / 0.05 | 0.02 |
| Seven | 95 | 0.20 / 0.22 | 0.66 / 0.65 | 0.10 / 0.10 | 0.02 / 0.02 | 0.02 |
| Wraith | 283 | 0.32 / 0.31 | 0.41 / 0.42 | 0.24 / 0.25 | 0.01 / 0.01 | 0.02 |
| Vyper | 78 | 0.46 / 0.46 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.62 | 0.16 / 0.17 | 0.03 / 0.03 | 0.02 |
| Viscous | 29 | 0.13 / 0.14 | 0.51 / 0.51 | 0.28 / 0.27 | 0.05 / 0.05 | 0.02 |
| Kelvin | 80 | 0.08 / 0.07 | 0.70 / 0.70 | 0.17 / 0.18 | 0.03 / 0.03 | 0.02 |
| Baba | 146 | 0.07 / 0.06 | 0.54 / 0.54 | 0.25 / 0.25 | 0.12 / 0.14 | 0.02 |
| Bebop | 254 | 0.18 / 0.17 | 0.56 / 0.57 | 0.19 / 0.20 | 0.05 / 0.05 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.59 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Holliday | 73 | 0.27 / 0.27 | 0.54 / 0.53 | 0.13 / 0.14 | 0.05 / 0.06 | 0.02 |
| Apollo | 92 | 0.11 / 0.10 | 0.53 / 0.53 | 0.17 / 0.16 | 0.17 / 0.19 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.01 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.50 | 0.12 / 0.12 | 0.02 / 0.01 | 0.01 |
| Nurse Harrow | 347 | 0.29 / 0.29 | 0.61 / 0.62 | 0.06 / 0.05 | 0.03 / 0.03 | 0.01 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.61 | 0.13 / 0.13 | 0.03 / 0.03 | 0.01 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.47 | 0.39 / 0.41 | 0.05 / 0.05 | 0.01 |
| Venator | 257 | 0.38 / 0.37 | 0.50 / 0.50 | 0.03 / 0.04 | 0.07 / 0.08 | 0.01 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.64 | 0.18 / 0.18 | 0.01 / 0.01 | 0.01 |
| Solomon | 136 | 0.25 / 0.24 | 0.64 / 0.64 | 0.08 / 0.08 | 0.02 / 0.02 | 0.01 |
| Vindicta | 131 | 0.44 / 0.43 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.01 |
| Mirage | 45 | 0.31 / 0.32 | 0.48 / 0.48 | 0.17 / 0.17 | 0.02 / 0.02 | 0.01 |
| Sinclair | 55 | 0.12 / 0.12 | 0.79 / 0.78 | 0.04 / 0.04 | 0.03 / 0.04 | 0.01 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.61 | 0.17 / 0.17 | 0.03 / 0.04 | 0.01 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.50 | 0.27 / 0.28 | 0.02 / 0.02 | 0.01 |
| Shiv | 209 | 0.27 / 0.27 | 0.48 / 0.49 | 0.16 / 0.15 | 0.08 / 0.08 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.57 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.66 | 0.19 / 0.19 | 0.01 / 0.01 | 0.01 |
| Drifter | 186 | 0.26 / 0.26 | 0.44 / 0.44 | 0.17 / 0.17 | 0.11 / 0.11 | 0.01 |
| McGinnis | 49 | 0.20 / 0.20 | 0.64 / 0.64 | 0.12 / 0.12 | 0.02 / 0.02 | 0.01 |
| Paige | 135 | 0.29 / 0.29 | 0.59 / 0.59 | 0.07 / 0.08 | 0.03 / 0.03 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Kelvin | Arctic Beam | ability | 0.402 | 0.408 | 0.84 |
| Dynamo | Kinetic Pulse | ability | 0.444 | 0.425 | 1.14 |
| Warden | Last Stand | ability | 0.138 | 0.175 | 0.71 |
| Abrams | MELEE | melee | 0.424 | 0.441 | 0.90 |
| Warden | Alchemical Flask | ability | 0.129 | 0.156 | 0.75 |
| Dynamo | Singularity | ability | 0.179 | 0.154 | 1.27 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.293 | 0.87 |
| Billy | Bashdown | ability | 0.309 | 0.323 | 0.88 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.202 | 0.82 |
| Victor | Aura of Suffering | ability | 0.306 | 0.337 | 0.89 |
| Violet | Abstract Landscape | ability | 0.174 | 0.157 | 1.22 |
| Viscous | Goo Ball | ability | 0.107 | 0.086 | 1.37 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.167 | 1.18 |
| Graves | Borrowed Decree | ability | 0.195 | 0.215 | 0.87 |
| Rem | Pillow Toss | ability | 0.437 | 0.441 | 1.07 |
| Violet | Living Ink | ability | 0.261 | 0.257 | 1.12 |
| Baba | MELEE | melee | 0.124 | 0.141 | 0.82 |
| Grey Talon | Charged Shot | ability | 0.351 | 0.359 | 0.93 |
| Wraith | Card Trick | ability | 0.280 | 0.295 | 0.91 |
| Celeste | Shining Wonder | ability | 0.170 | 0.178 | 0.86 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.036 | 1.57 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.323 | 0.92 |
| Billy | MELEE | melee | 0.223 | 0.229 | 0.89 |
| Calico | Gloom Bombs | ability | 0.182 | 0.187 | 0.87 |
| The Doorman | Call Bell | ability | 0.474 | 0.468 | 1.05 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.217 | 0.89 |
| Victor | Pain Battery | ability | 0.276 | 0.248 | 1.09 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.125 | 0.83 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.289 | 0.92 |
| Vyper | Split Shot | item | 0.110 | 0.091 | 1.22 |
| Apollo | MELEE | melee | 0.171 | 0.188 | 0.90 |
| Solomon | Setup Bishop | ability | 0.307 | 0.314 | 0.94 |
| Seven | Storm Cloud | ability | 0.202 | 0.197 | 1.10 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.125 | 1.15 |
| Viscous | Puddle Punch | ability | 0.123 | 0.115 | 1.17 |
| Venator | Consecrating Grenade | ability | 0.147 | 0.162 | 0.89 |
| Abrams | Siphon Life | ability | 0.107 | 0.118 | 0.85 |
| Haze | Fixation | ability | 0.304 | 0.294 | 1.06 |
| Silver | MELEE | melee | 0.101 | 0.113 | 0.85 |
| Vindicta | Crow Familiar | ability | 0.155 | 0.171 | 0.90 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1933 | 0.139 | 0.145 | 0.96 |
| Mystic Burst | 1657 | 0.050 | 0.046 | 1.08 |
| Quicksilver Reload | 1100 | 0.037 | 0.033 | 1.12 |
| Toxic Bullets | 888 | 0.113 | 0.105 | 1.07 |
| Spirit Snatch | 863 | 0.065 | 0.067 | 0.97 |
| Torment Pulse | 822 | 0.154 | 0.152 | 1.01 |
| Spirit Burn | 819 | 0.085 | 0.092 | 0.92 |
| Stalker | 795 | 0.051 | 0.049 | 1.04 |
| Ricochet | 747 | 0.050 | 0.065 | 0.76 |
| Escalating Exposure | 694 | 0.109 | 0.115 | 0.95 |
| Mystic Shot | 676 | 0.062 | 0.063 | 0.99 |
| Spirit Strike | 648 | 0.046 | 0.046 | 0.98 |
| Siphon Bullets | 592 | 0.086 | 0.099 | 0.86 |
| Express Shot | 563 | 0.121 | 0.119 | 1.02 |
| Cold Front | 526 | 0.056 | 0.059 | 0.96 |
| Tesla Bullets | 505 | 0.138 | 0.129 | 1.07 |
| Melee Charge | 443 | 0.047 | 0.046 | 1.01 |
| Headhunter | 414 | 0.090 | 0.085 | 1.06 |
| Capacitor | 403 | 0.205 | 0.206 | 1.00 |
| Headshot Booster | 394 | 0.045 | 0.042 | 1.07 |
| Mercurial Magnum | 359 | 0.103 | 0.100 | 1.03 |
| Mystic Reverb | 242 | 0.166 | 0.216 | 0.77 |
| Rebuttal | 238 | 0.013 | 0.015 | 0.87 |
| Lucky Shot | 229 | 0.142 | 0.107 | 1.32 |
| Arctic Blast | 184 | 0.139 | 0.144 | 0.96 |
| Split Shot | 181 | 0.089 | 0.082 | 1.09 |
| Crushing Fists | 170 | 0.055 | 0.053 | 1.04 |
| Scourge | 151 | 0.159 | 0.177 | 0.90 |
| Phantom Strike | 141 | 0.050 | 0.054 | 0.93 |
| Decay | 135 | 0.173 | 0.181 | 0.96 |
| Alchemical Fire | 113 | 0.127 | 0.151 | 0.84 |
| Return Fire | 99 | 0.093 | 0.025 | 3.79 |
| Lightning Scroll | 59 | 0.039 | 0.036 | 1.07 |
| Focus Lens | 45 | 0.105 | 0.105 | 1.01 |
| Silence Wave | 33 | 0.046 | 0.051 | 0.90 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Rat King | Return Fire | 44 | 0.099 | 0.028 | 3.56 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.022 | 2.12 |
| Venator | Ricochet | 41 | 0.060 | 0.098 | 0.61 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.029 | 1.61 |
| Venator | Siphon Bullets | 86 | 0.096 | 0.145 | 0.66 |
| Drifter | Spirit Burn | 43 | 0.072 | 0.048 | 1.48 |
| Haze | Lucky Shot | 99 | 0.154 | 0.105 | 1.46 |
| Infernus | Ricochet | 75 | 0.026 | 0.039 | 0.69 |
| Mina | Toxic Bullets | 99 | 0.078 | 0.054 | 1.45 |
| Wraith | Ricochet | 198 | 0.041 | 0.058 | 0.70 |
| Nurse Harrow | Ricochet | 140 | 0.025 | 0.036 | 0.71 |
| Mirage | Ricochet | 34 | 0.041 | 0.057 | 0.72 |
| Apollo | Mystic Burst | 65 | 0.052 | 0.038 | 1.38 |
| Grey Talon | Mystic Reverb | 26 | 0.154 | 0.212 | 0.73 |
| Kelvin | Spirit Burn | 27 | 0.103 | 0.142 | 0.73 |
| Viscous | Spirit Snatch | 20 | 0.096 | 0.071 | 1.36 |
| Nurse Harrow | Toxic Bullets | 85 | 0.152 | 0.114 | 1.34 |
| Grey Talon | Spirit Burn | 45 | 0.088 | 0.116 | 0.76 |
| Haze | Ricochet | 214 | 0.067 | 0.089 | 0.76 |
| Apollo | Melee Charge | 57 | 0.045 | 0.034 | 1.32 |
| Shiv | Lucky Shot | 52 | 0.142 | 0.109 | 1.31 |
| Viscous | Mystic Burst | 20 | 0.064 | 0.050 | 1.29 |
| Lash | Mystic Burst | 201 | 0.061 | 0.047 | 1.29 |
| Paradox | Headshot Booster | 44 | 0.043 | 0.034 | 1.28 |
| Mirage | Escalating Exposure | 22 | 0.100 | 0.127 | 0.79 |
| Lash | Mystic Reverb | 22 | 0.170 | 0.211 | 0.81 |
| Vyper | Split Shot | 70 | 0.144 | 0.118 | 1.22 |
| Deadman Danny | Toxic Bullets | 147 | 0.099 | 0.082 | 1.22 |
| Victor | Escalating Exposure | 105 | 0.134 | 0.162 | 0.82 |
| Paradox | Spirit Burn | 49 | 0.072 | 0.087 | 0.83 |
| Bebop | Mystic Reverb | 30 | 0.146 | 0.175 | 0.83 |
| Mo & Krill | Escalating Exposure | 27 | 0.108 | 0.090 | 1.19 |
| Pocket | Spirit Burn | 99 | 0.082 | 0.097 | 0.84 |
| Nurse Harrow | Decay | 41 | 0.220 | 0.187 | 1.17 |
| Paradox | Mystic Burst | 70 | 0.050 | 0.043 | 1.17 |
| Mo & Krill | Arctic Blast | 27 | 0.120 | 0.139 | 0.86 |
| Mo & Krill | Mystic Burst | 170 | 0.071 | 0.062 | 1.15 |
| Calico | Scourge | 23 | 0.180 | 0.207 | 0.87 |
| Grey Talon | Tankbuster | 90 | 0.129 | 0.148 | 0.87 |
| Vindicta | Mystic Burst | 24 | 0.037 | 0.043 | 0.87 |
