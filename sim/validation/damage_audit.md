# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Warden | 33 | 0.52 / 0.48 | 0.31 / 0.36 | 0.11 / 0.12 | 0.03 / 0.02 | 0.06 |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.56 | 0.28 / 0.23 | 0.05 / 0.05 | 0.06 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.33 | 0.26 / 0.30 | 0.04 / 0.03 | 0.04 |
| Calico | 110 | 0.13 / 0.12 | 0.38 / 0.38 | 0.31 / 0.35 | 0.15 / 0.13 | 0.04 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.47 | 0.17 / 0.21 | 0.02 / 0.02 | 0.04 |
| Venator | 257 | 0.38 / 0.36 | 0.50 / 0.52 | 0.03 / 0.04 | 0.07 / 0.07 | 0.03 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.56 | 0.17 / 0.15 | 0.17 / 0.17 | 0.03 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.08 | 0.02 / 0.01 | 0.03 |
| Grey Talon | 103 | 0.31 / 0.31 | 0.49 / 0.48 | 0.16 / 0.19 | 0.01 / 0.01 | 0.03 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.52 | 0.27 / 0.27 | 0.02 / 0.02 | 0.03 |
| Silver | 100 | 0.41 / 0.39 | 0.37 / 0.38 | 0.10 / 0.12 | 0.10 / 0.10 | 0.03 |
| Holliday | 73 | 0.27 / 0.27 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.05 | 0.03 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.59 | 0.25 / 0.23 | 0.03 / 0.02 | 0.03 |
| Seven | 95 | 0.20 / 0.19 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.01 | 0.02 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.42 | 0.05 / 0.04 | 0.02 |
| Billy | 93 | 0.21 / 0.19 | 0.41 / 0.42 | 0.14 / 0.16 | 0.22 / 0.22 | 0.02 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.38 | 0.17 / 0.19 | 0.18 / 0.18 | 0.02 |
| Abrams | 138 | 0.23 / 0.22 | 0.20 / 0.20 | 0.13 / 0.14 | 0.42 / 0.43 | 0.02 |
| McGinnis | 49 | 0.20 / 0.22 | 0.64 / 0.64 | 0.12 / 0.11 | 0.02 / 0.02 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Wraith | 283 | 0.32 / 0.32 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Bebop | 254 | 0.18 / 0.17 | 0.56 / 0.57 | 0.19 / 0.20 | 0.05 / 0.05 | 0.02 |
| Drifter | 186 | 0.26 / 0.25 | 0.44 / 0.46 | 0.17 / 0.16 | 0.11 / 0.12 | 0.02 |
| Celeste | 77 | 0.16 / 0.16 | 0.61 / 0.62 | 0.17 / 0.17 | 0.04 / 0.03 | 0.02 |
| Paradox | 168 | 0.24 / 0.24 | 0.48 / 0.48 | 0.23 / 0.25 | 0.03 / 0.02 | 0.02 |
| Dynamo | 53 | 0.23 / 0.23 | 0.62 / 0.64 | 0.08 / 0.08 | 0.05 / 0.04 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.63 | 0.16 / 0.17 | 0.03 / 0.03 | 0.02 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.60 | 0.17 / 0.18 | 0.03 / 0.03 | 0.02 |
| Solomon | 136 | 0.25 / 0.23 | 0.64 / 0.65 | 0.08 / 0.08 | 0.02 / 0.01 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.02 |
| Vyper | 78 | 0.46 / 0.46 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.01 |
| Nurse Harrow | 347 | 0.29 / 0.29 | 0.61 / 0.61 | 0.06 / 0.07 | 0.03 / 0.02 | 0.01 |
| Kelvin | 80 | 0.08 / 0.08 | 0.70 / 0.70 | 0.17 / 0.18 | 0.03 / 0.03 | 0.01 |
| Shiv | 209 | 0.27 / 0.28 | 0.48 / 0.48 | 0.16 / 0.15 | 0.08 / 0.08 | 0.01 |
| Paige | 135 | 0.29 / 0.29 | 0.59 / 0.60 | 0.07 / 0.07 | 0.03 / 0.03 | 0.01 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.51 | 0.12 / 0.12 | 0.02 / 0.01 | 0.01 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.57 | 0.16 / 0.17 | 0.05 / 0.04 | 0.01 |
| Lady Geist | 37 | 0.29 / 0.29 | 0.62 / 0.62 | 0.05 / 0.05 | 0.03 / 0.03 | 0.01 |
| Vindicta | 131 | 0.44 / 0.44 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.00 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.66 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Sinclair | 55 | 0.12 / 0.13 | 0.79 / 0.78 | 0.04 / 0.04 | 0.03 / 0.03 | 0.01 |
| Baba | 146 | 0.07 / 0.07 | 0.54 / 0.54 | 0.25 / 0.25 | 0.12 / 0.13 | 0.01 |
| Pocket | 117 | 0.14 / 0.14 | 0.66 / 0.66 | 0.16 / 0.17 | 0.02 / 0.02 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Vexing Bolt | ability | 0.351 | 0.267 | 1.40 |
| Sinclair | Audience Participation | ability | 0.205 | 0.300 | 0.72 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.082 | 1.66 |
| Warden | Last Stand | ability | 0.138 | 0.180 | 0.71 |
| Viscous | Express Shot | item | 0.052 | 0.023 | 2.53 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.108 | 1.39 |
| Lady Geist | Malice | ability | 0.144 | 0.181 | 0.78 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.226 | 0.82 |
| Billy | Bashdown | ability | 0.309 | 0.317 | 0.89 |
| Shiv | Killing Blow | ability | 0.056 | 0.032 | 1.83 |
| Solomon | Develop Queen | ability | 0.161 | 0.181 | 0.83 |
| Graves | Borrowed Decree | ability | 0.195 | 0.206 | 0.86 |
| Graves | Jar of Dead | ability | 0.212 | 0.222 | 0.87 |
| Venator | Consecrating Grenade | ability | 0.147 | 0.165 | 0.84 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.176 | 1.16 |
| Warden | Alchemical Flask | ability | 0.129 | 0.143 | 0.83 |
| Abrams | MELEE | melee | 0.424 | 0.432 | 0.94 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.160 | 0.85 |
| Seven | Storm Cloud | ability | 0.202 | 0.221 | 0.89 |
| Holliday | Powder Keg | ability | 0.397 | 0.384 | 1.06 |
| Shiv | Serrated Knives | ability | 0.283 | 0.318 | 0.93 |
| McGinnis | Mini Turret | ability | 0.467 | 0.492 | 1.04 |
| Vyper | Split Shot | item | 0.110 | 0.091 | 1.20 |
| Lash | Ground Strike | ability | 0.350 | 0.361 | 1.06 |
| Dynamo | Kinetic Pulse | ability | 0.444 | 0.453 | 0.96 |
| Calico | Arctic Blast | item | 0.079 | 0.090 | 0.81 |
| Billy | MELEE | melee | 0.223 | 0.222 | 0.92 |
| Mirage | Toxic Bullets | item | 0.093 | 0.108 | 0.84 |
| Deadman Danny | Tankbuster | item | 0.079 | 0.092 | 0.82 |
| Kelvin | Tankbuster | item | 0.026 | 0.039 | 0.64 |
| Calico | Gloom Bombs | ability | 0.182 | 0.184 | 0.91 |
| Shiv | Slice and Dice | ability | 0.145 | 0.135 | 1.13 |
| Rem | Pillow Toss | ability | 0.437 | 0.438 | 1.04 |
| Baba | Torment Pulse | item | 0.170 | 0.159 | 1.10 |
| Grey Talon | Tankbuster | item | 0.071 | 0.085 | 0.83 |
| Viscous | Spirit Snatch | item | 0.042 | 0.032 | 1.47 |
| Ivy | Entangling Thorns | ability | 0.199 | 0.182 | 1.08 |
| Drifter | Stalker's Mark | ability | 0.134 | 0.144 | 0.90 |
| Seven | Lightning Ball | ability | 0.198 | 0.206 | 0.93 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.205 | 0.93 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1890 | 0.138 | 0.131 | 1.05 |
| Mystic Burst | 1692 | 0.050 | 0.044 | 1.13 |
| Quicksilver Reload | 1114 | 0.037 | 0.032 | 1.13 |
| Toxic Bullets | 875 | 0.113 | 0.118 | 0.95 |
| Spirit Snatch | 857 | 0.065 | 0.063 | 1.02 |
| Torment Pulse | 814 | 0.154 | 0.143 | 1.08 |
| Stalker | 794 | 0.051 | 0.051 | 1.00 |
| Spirit Strike | 711 | 0.046 | 0.046 | 0.98 |
| Ricochet | 700 | 0.050 | 0.067 | 0.74 |
| Spirit Burn | 687 | 0.084 | 0.085 | 0.99 |
| Mystic Shot | 673 | 0.062 | 0.059 | 1.06 |
| Escalating Exposure | 610 | 0.110 | 0.114 | 0.96 |
| Express Shot | 558 | 0.121 | 0.102 | 1.19 |
| Cold Front | 525 | 0.057 | 0.059 | 0.96 |
| Siphon Bullets | 521 | 0.086 | 0.097 | 0.89 |
| Tesla Bullets | 509 | 0.139 | 0.137 | 1.01 |
| Melee Charge | 434 | 0.047 | 0.044 | 1.05 |
| Headhunter | 410 | 0.090 | 0.089 | 1.01 |
| Capacitor | 375 | 0.206 | 0.203 | 1.01 |
| Headshot Booster | 375 | 0.044 | 0.043 | 1.02 |
| Mercurial Magnum | 340 | 0.103 | 0.097 | 1.07 |
| Rebuttal | 236 | 0.013 | 0.014 | 0.92 |
| Mystic Reverb | 211 | 0.166 | 0.204 | 0.81 |
| Lucky Shot | 201 | 0.142 | 0.105 | 1.36 |
| Arctic Blast | 172 | 0.141 | 0.139 | 1.01 |
| Split Shot | 170 | 0.090 | 0.086 | 1.05 |
| Crushing Fists | 148 | 0.055 | 0.049 | 1.11 |
| Decay | 135 | 0.173 | 0.174 | 0.99 |
| Phantom Strike | 125 | 0.050 | 0.052 | 0.96 |
| Scourge | 122 | 0.158 | 0.172 | 0.92 |
| Alchemical Fire | 111 | 0.126 | 0.136 | 0.93 |
| Return Fire | 96 | 0.094 | 0.029 | 3.29 |
| Lightning Scroll | 49 | 0.039 | 0.032 | 1.20 |
| Focus Lens | 39 | 0.105 | 0.092 | 1.14 |
| Silence Wave | 33 | 0.046 | 0.048 | 0.96 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Rat King | Return Fire | 41 | 0.101 | 0.029 | 3.54 |
| Violet | Torment Pulse | 69 | 0.103 | 0.054 | 1.92 |
| Nurse Harrow | Ricochet | 135 | 0.025 | 0.048 | 0.53 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.026 | 1.79 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.028 | 1.62 |
| Violet | Mystic Burst | 66 | 0.044 | 0.027 | 1.62 |
| Venator | Ricochet | 36 | 0.057 | 0.092 | 0.62 |
| Apollo | Melee Charge | 58 | 0.045 | 0.029 | 1.53 |
| Haze | Lucky Shot | 92 | 0.153 | 0.100 | 1.53 |
| Infernus | Ricochet | 66 | 0.027 | 0.041 | 0.65 |
| Venator | Siphon Bullets | 77 | 0.095 | 0.143 | 0.67 |
| Wraith | Ricochet | 185 | 0.041 | 0.062 | 0.67 |
| Apollo | Mystic Burst | 66 | 0.052 | 0.035 | 1.47 |
| Drifter | Crushing Fists | 25 | 0.049 | 0.035 | 1.42 |
| Drifter | Spirit Burn | 42 | 0.070 | 0.050 | 1.40 |
| Violet | Tankbuster | 207 | 0.144 | 0.105 | 1.38 |
| Shiv | Express Shot | 125 | 0.255 | 0.186 | 1.37 |
| Lash | Mystic Burst | 210 | 0.061 | 0.045 | 1.35 |
| Yamato | Express Shot | 46 | 0.158 | 0.118 | 1.33 |
| Haze | Ricochet | 207 | 0.067 | 0.088 | 0.76 |
| Viscous | Mystic Burst | 20 | 0.066 | 0.051 | 1.30 |
| Bebop | Mystic Reverb | 24 | 0.143 | 0.185 | 0.77 |
| Shiv | Lucky Shot | 45 | 0.143 | 0.111 | 1.28 |
| Yamato | Melee Charge | 57 | 0.041 | 0.051 | 0.79 |
| Yamato | Crushing Fists | 30 | 0.050 | 0.039 | 1.27 |
| Mo & Krill | Mystic Burst | 174 | 0.072 | 0.058 | 1.25 |
| Violet | Mystic Shot | 170 | 0.073 | 0.059 | 1.25 |
| Vyper | Split Shot | 69 | 0.144 | 0.118 | 1.22 |
| Drifter | Mystic Burst | 96 | 0.041 | 0.034 | 1.20 |
| Drifter | Tankbuster | 101 | 0.108 | 0.090 | 1.20 |
| Apollo | Tankbuster | 47 | 0.148 | 0.123 | 1.20 |
| Nurse Harrow | Decay | 41 | 0.220 | 0.183 | 1.20 |
| Victor | Escalating Exposure | 102 | 0.133 | 0.159 | 0.84 |
| Grey Talon | Mystic Reverb | 22 | 0.155 | 0.183 | 0.84 |
| Violet | Spirit Burn | 45 | 0.096 | 0.082 | 1.17 |
| Baba | Torment Pulse | 138 | 0.249 | 0.214 | 1.16 |
| Paige | Express Shot | 32 | 0.157 | 0.135 | 1.16 |
| Mirage | Ricochet | 33 | 0.041 | 0.047 | 0.86 |
| Deadman Danny | Express Shot | 183 | 0.114 | 0.099 | 1.16 |
| Apollo | Spirit Snatch | 66 | 0.057 | 0.049 | 1.15 |
