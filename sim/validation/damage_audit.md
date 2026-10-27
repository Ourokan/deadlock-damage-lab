# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.55 | 0.28 / 0.22 | 0.05 / 0.06 | 0.07 |
| Warden | 33 | 0.52 / 0.47 | 0.31 / 0.37 | 0.11 / 0.12 | 0.03 / 0.03 | 0.06 |
| Dynamo | 53 | 0.23 / 0.25 | 0.62 / 0.58 | 0.08 / 0.10 | 0.05 / 0.05 | 0.04 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.53 | 0.27 / 0.26 | 0.02 / 0.02 | 0.04 |
| Drifter | 186 | 0.26 / 0.24 | 0.44 / 0.47 | 0.17 / 0.16 | 0.11 / 0.12 | 0.03 |
| Calico | 110 | 0.13 / 0.12 | 0.38 / 0.40 | 0.31 / 0.32 | 0.15 / 0.15 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.48 | 0.16 / 0.14 | 0.08 / 0.08 | 0.03 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.29 | 0.04 / 0.03 | 0.03 |
| Silver | 100 | 0.41 / 0.39 | 0.37 / 0.37 | 0.10 / 0.12 | 0.10 / 0.11 | 0.03 |
| Celeste | 77 | 0.16 / 0.14 | 0.61 / 0.63 | 0.17 / 0.18 | 0.04 / 0.04 | 0.03 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.50 | 0.16 / 0.18 | 0.01 / 0.01 | 0.03 |
| Abrams | 138 | 0.23 / 0.21 | 0.20 / 0.20 | 0.13 / 0.13 | 0.42 / 0.44 | 0.02 |
| Paradox | 168 | 0.24 / 0.23 | 0.48 / 0.50 | 0.23 / 0.24 | 0.03 / 0.02 | 0.02 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.40 | 0.17 / 0.17 | 0.18 / 0.19 | 0.02 |
| Billy | 93 | 0.21 / 0.19 | 0.41 / 0.42 | 0.14 / 0.15 | 0.22 / 0.23 | 0.02 |
| Violet | 376 | 0.19 / 0.21 | 0.67 / 0.65 | 0.10 / 0.10 | 0.02 / 0.02 | 0.02 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.57 | 0.16 / 0.15 | 0.05 / 0.05 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Baba | 146 | 0.07 / 0.06 | 0.54 / 0.54 | 0.25 / 0.24 | 0.12 / 0.14 | 0.02 |
| Wraith | 283 | 0.32 / 0.31 | 0.41 / 0.42 | 0.24 / 0.25 | 0.01 / 0.01 | 0.02 |
| Kelvin | 80 | 0.08 / 0.07 | 0.70 / 0.70 | 0.17 / 0.18 | 0.03 / 0.03 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.62 | 0.16 / 0.17 | 0.03 / 0.03 | 0.02 |
| Seven | 95 | 0.20 / 0.21 | 0.66 / 0.66 | 0.10 / 0.10 | 0.02 / 0.02 | 0.02 |
| Bebop | 254 | 0.18 / 0.17 | 0.56 / 0.57 | 0.19 / 0.20 | 0.05 / 0.05 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.59 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.53 | 0.17 / 0.16 | 0.17 / 0.19 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.60 | 0.05 / 0.05 | 0.03 / 0.04 | 0.01 |
| Holliday | 73 | 0.27 / 0.27 | 0.54 / 0.53 | 0.13 / 0.14 | 0.05 / 0.06 | 0.01 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.01 |
| Haze | 324 | 0.35 / 0.36 | 0.50 / 0.50 | 0.12 / 0.12 | 0.02 / 0.01 | 0.01 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.61 | 0.13 / 0.13 | 0.03 / 0.03 | 0.01 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.47 | 0.39 / 0.41 | 0.05 / 0.04 | 0.01 |
| Venator | 257 | 0.38 / 0.37 | 0.50 / 0.50 | 0.03 / 0.04 | 0.07 / 0.08 | 0.01 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.61 | 0.17 / 0.16 | 0.03 / 0.04 | 0.01 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.64 | 0.18 / 0.18 | 0.01 / 0.01 | 0.01 |
| Solomon | 136 | 0.25 / 0.24 | 0.64 / 0.64 | 0.08 / 0.08 | 0.02 / 0.02 | 0.01 |
| Nurse Harrow | 347 | 0.29 / 0.29 | 0.61 / 0.62 | 0.06 / 0.05 | 0.03 / 0.03 | 0.01 |
| Vindicta | 131 | 0.44 / 0.43 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.01 |
| Mirage | 45 | 0.31 / 0.31 | 0.48 / 0.49 | 0.17 / 0.17 | 0.02 / 0.02 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.57 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |
| Sinclair | 55 | 0.12 / 0.12 | 0.79 / 0.79 | 0.04 / 0.04 | 0.03 / 0.03 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.66 | 0.19 / 0.19 | 0.01 / 0.01 | 0.01 |
| McGinnis | 49 | 0.20 / 0.20 | 0.64 / 0.64 | 0.12 / 0.12 | 0.02 / 0.02 | 0.01 |
| Paige | 135 | 0.29 / 0.29 | 0.59 / 0.59 | 0.07 / 0.08 | 0.03 / 0.03 | 0.00 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Audience Participation | ability | 0.205 | 0.301 | 0.68 |
| Kelvin | Arctic Beam | ability | 0.402 | 0.410 | 0.82 |
| Sinclair | Vexing Bolt | ability | 0.351 | 0.295 | 1.19 |
| Warden | Last Stand | ability | 0.138 | 0.177 | 0.71 |
| Dynamo | Kinetic Pulse | ability | 0.444 | 0.426 | 1.14 |
| Graves | Jar of Dead | ability | 0.212 | 0.240 | 0.80 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.293 | 0.85 |
| Drifter | Rend | ability | 0.228 | 0.253 | 0.83 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.151 | 1.27 |
| Warden | Alchemical Flask | ability | 0.129 | 0.156 | 0.75 |
| Viscous | Express Shot | item | 0.052 | 0.025 | 2.32 |
| Dynamo | Singularity | ability | 0.179 | 0.154 | 1.28 |
| Abrams | MELEE | melee | 0.424 | 0.440 | 0.91 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.203 | 0.82 |
| Billy | Bashdown | ability | 0.309 | 0.322 | 0.89 |
| Victor | Aura of Suffering | ability | 0.306 | 0.339 | 0.89 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.162 | 1.20 |
| Violet | Abstract Landscape | ability | 0.174 | 0.157 | 1.22 |
| Violet | Living Ink | ability | 0.261 | 0.257 | 1.12 |
| Rem | Pillow Toss | ability | 0.437 | 0.440 | 1.07 |
| The Doorman | Call Bell | ability | 0.474 | 0.469 | 1.06 |
| Baba | MELEE | melee | 0.124 | 0.142 | 0.82 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.036 | 1.61 |
| Wraith | Card Trick | ability | 0.280 | 0.295 | 0.92 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.323 | 0.92 |
| Celeste | Shining Wonder | ability | 0.170 | 0.179 | 0.86 |
| Calico | Gloom Bombs | ability | 0.182 | 0.188 | 0.87 |
| Shiv | Express Shot | item | 0.086 | 0.068 | 1.35 |
| Viscous | Spirit Snatch | item | 0.042 | 0.025 | 1.86 |
| Grey Talon | Charged Shot | ability | 0.351 | 0.359 | 0.93 |
| Victor | Pain Battery | ability | 0.276 | 0.248 | 1.10 |
| Billy | MELEE | melee | 0.223 | 0.229 | 0.90 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.217 | 0.89 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.126 | 0.83 |
| Shiv | Serrated Knives | ability | 0.283 | 0.277 | 1.09 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.289 | 0.92 |
| Vyper | Split Shot | item | 0.110 | 0.091 | 1.22 |
| Graves | Grasping Hands | ability | 0.088 | 0.099 | 0.80 |
| Drifter | Stalker's Mark | ability | 0.134 | 0.142 | 0.86 |
| Apollo | MELEE | melee | 0.171 | 0.188 | 0.90 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1933 | 0.139 | 0.143 | 0.97 |
| Mystic Burst | 1657 | 0.050 | 0.045 | 1.10 |
| Quicksilver Reload | 1100 | 0.037 | 0.032 | 1.14 |
| Toxic Bullets | 888 | 0.113 | 0.104 | 1.09 |
| Spirit Snatch | 863 | 0.065 | 0.066 | 0.98 |
| Torment Pulse | 822 | 0.154 | 0.150 | 1.03 |
| Spirit Burn | 819 | 0.085 | 0.092 | 0.92 |
| Stalker | 795 | 0.051 | 0.048 | 1.05 |
| Ricochet | 747 | 0.050 | 0.065 | 0.76 |
| Escalating Exposure | 694 | 0.109 | 0.116 | 0.94 |
| Mystic Shot | 676 | 0.062 | 0.062 | 1.00 |
| Spirit Strike | 648 | 0.046 | 0.047 | 0.98 |
| Siphon Bullets | 592 | 0.086 | 0.099 | 0.87 |
| Express Shot | 563 | 0.121 | 0.103 | 1.18 |
| Cold Front | 526 | 0.056 | 0.059 | 0.96 |
| Tesla Bullets | 505 | 0.138 | 0.127 | 1.09 |
| Melee Charge | 443 | 0.047 | 0.046 | 1.02 |
| Headhunter | 414 | 0.090 | 0.085 | 1.06 |
| Capacitor | 403 | 0.205 | 0.203 | 1.01 |
| Headshot Booster | 394 | 0.045 | 0.042 | 1.07 |
| Mercurial Magnum | 359 | 0.103 | 0.100 | 1.03 |
| Mystic Reverb | 242 | 0.166 | 0.214 | 0.77 |
| Rebuttal | 238 | 0.013 | 0.015 | 0.85 |
| Lucky Shot | 229 | 0.142 | 0.105 | 1.35 |
| Arctic Blast | 184 | 0.139 | 0.143 | 0.97 |
| Split Shot | 181 | 0.089 | 0.081 | 1.10 |
| Crushing Fists | 170 | 0.055 | 0.052 | 1.05 |
| Scourge | 151 | 0.159 | 0.177 | 0.90 |
| Phantom Strike | 141 | 0.050 | 0.054 | 0.93 |
| Decay | 135 | 0.173 | 0.186 | 0.93 |
| Alchemical Fire | 113 | 0.127 | 0.142 | 0.89 |
| Return Fire | 99 | 0.093 | 0.025 | 3.77 |
| Lightning Scroll | 59 | 0.039 | 0.035 | 1.10 |
| Focus Lens | 45 | 0.105 | 0.104 | 1.01 |
| Silence Wave | 33 | 0.046 | 0.051 | 0.91 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Rat King | Return Fire | 44 | 0.099 | 0.028 | 3.57 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.022 | 2.14 |
| Mo & Krill | Rebuttal | 22 | 0.009 | 0.020 | 0.48 |
| Viscous | Spirit Snatch | 20 | 0.096 | 0.056 | 1.71 |
| Venator | Ricochet | 41 | 0.060 | 0.098 | 0.61 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.029 | 1.61 |
| Venator | Siphon Bullets | 86 | 0.096 | 0.145 | 0.66 |
| Haze | Lucky Shot | 99 | 0.154 | 0.104 | 1.47 |
| Nurse Harrow | Ricochet | 140 | 0.025 | 0.037 | 0.68 |
| Infernus | Ricochet | 75 | 0.026 | 0.038 | 0.69 |
| Mina | Toxic Bullets | 99 | 0.078 | 0.054 | 1.45 |
| Viscous | Mystic Burst | 20 | 0.064 | 0.045 | 1.44 |
| Wraith | Ricochet | 198 | 0.041 | 0.058 | 0.70 |
| Yamato | Express Shot | 47 | 0.157 | 0.113 | 1.40 |
| Mirage | Ricochet | 34 | 0.041 | 0.057 | 0.72 |
| Apollo | Mystic Burst | 65 | 0.052 | 0.037 | 1.38 |
| Kelvin | Spirit Burn | 27 | 0.103 | 0.141 | 0.73 |
| Grey Talon | Mystic Reverb | 26 | 0.154 | 0.210 | 0.73 |
| Grey Talon | Spirit Burn | 45 | 0.088 | 0.117 | 0.75 |
| Shiv | Lucky Shot | 52 | 0.142 | 0.107 | 1.33 |
| Shiv | Express Shot | 125 | 0.255 | 0.192 | 1.33 |
| Apollo | Melee Charge | 57 | 0.045 | 0.034 | 1.32 |
| Haze | Ricochet | 214 | 0.067 | 0.089 | 0.76 |
| Drifter | Spirit Burn | 43 | 0.072 | 0.054 | 1.32 |
| Nurse Harrow | Toxic Bullets | 85 | 0.152 | 0.117 | 1.30 |
| Lash | Mystic Burst | 201 | 0.061 | 0.047 | 1.29 |
| Paradox | Headshot Booster | 44 | 0.043 | 0.034 | 1.28 |
| Mirage | Escalating Exposure | 22 | 0.100 | 0.127 | 0.79 |
| Lash | Mystic Reverb | 22 | 0.170 | 0.210 | 0.81 |
| Deadman Danny | Toxic Bullets | 147 | 0.099 | 0.081 | 1.22 |
| Vyper | Split Shot | 70 | 0.144 | 0.118 | 1.22 |
| Victor | Escalating Exposure | 105 | 0.134 | 0.163 | 0.82 |
| Paradox | Spirit Burn | 49 | 0.072 | 0.088 | 0.82 |
| Drifter | Mystic Burst | 92 | 0.041 | 0.034 | 1.21 |
| Mo & Krill | Mystic Burst | 170 | 0.071 | 0.059 | 1.21 |
| Graves | Tesla Bullets | 100 | 0.136 | 0.113 | 1.21 |
| Bebop | Mystic Reverb | 30 | 0.146 | 0.174 | 0.84 |
| Pocket | Spirit Burn | 99 | 0.082 | 0.097 | 0.84 |
| Yamato | Melee Charge | 61 | 0.041 | 0.048 | 0.85 |
| Drifter | Crushing Fists | 29 | 0.048 | 0.041 | 1.17 |
