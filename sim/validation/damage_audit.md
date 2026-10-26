# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Warden | 33 | 0.52 / 0.45 | 0.31 / 0.39 | 0.11 / 0.12 | 0.03 / 0.02 | 0.09 |
| McGinnis | 49 | 0.20 / 0.15 | 0.64 / 0.73 | 0.12 / 0.10 | 0.02 / 0.01 | 0.08 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.51 | 0.28 / 0.25 | 0.05 / 0.07 | 0.05 |
| Celeste | 77 | 0.16 / 0.19 | 0.61 / 0.58 | 0.17 / 0.18 | 0.04 / 0.04 | 0.04 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.33 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.41 | 0.31 / 0.32 | 0.15 / 0.13 | 0.04 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.57 | 0.17 / 0.14 | 0.17 / 0.17 | 0.04 |
| Mirage | 45 | 0.31 / 0.31 | 0.48 / 0.46 | 0.17 / 0.20 | 0.02 / 0.02 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.14 | 0.05 / 0.06 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.08 | 0.02 / 0.02 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.15 | 0.08 / 0.08 | 0.03 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.59 | 0.25 / 0.23 | 0.03 / 0.03 | 0.03 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.21 | 0.01 / 0.01 | 0.03 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.68 | 0.17 / 0.19 | 0.03 / 0.04 | 0.03 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.52 | 0.27 / 0.28 | 0.02 / 0.02 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.09 | 0.05 / 0.04 | 0.03 |
| Yamato | 131 | 0.24 / 0.25 | 0.38 / 0.37 | 0.17 / 0.19 | 0.18 / 0.18 | 0.03 |
| Drifter | 186 | 0.26 / 0.27 | 0.44 / 0.45 | 0.17 / 0.16 | 0.11 / 0.12 | 0.03 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.63 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Baba | 146 | 0.07 / 0.07 | 0.54 / 0.55 | 0.25 / 0.24 | 0.12 / 0.13 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.02 | 0.02 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.60 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.20 | 0.13 / 0.12 | 0.42 / 0.43 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.42 | 0.14 / 0.15 | 0.22 / 0.23 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.57 | 0.19 / 0.20 | 0.05 / 0.05 | 0.02 |
| Grey Talon | 103 | 0.31 / 0.31 | 0.49 / 0.49 | 0.16 / 0.18 | 0.01 / 0.01 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.68 | 0.16 / 0.16 | 0.02 / 0.02 | 0.02 |
| Silver | 100 | 0.41 / 0.40 | 0.37 / 0.37 | 0.10 / 0.12 | 0.10 / 0.10 | 0.02 |
| Vindicta | 131 | 0.44 / 0.44 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.51 | 0.12 / 0.12 | 0.02 / 0.01 | 0.02 |
| Sinclair | 55 | 0.12 / 0.13 | 0.79 / 0.78 | 0.04 / 0.04 | 0.03 / 0.03 | 0.02 |
| Paradox | 168 | 0.24 / 0.24 | 0.48 / 0.48 | 0.23 / 0.24 | 0.03 / 0.02 | 0.01 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.58 | 0.16 / 0.16 | 0.05 / 0.05 | 0.01 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.40 | 0.03 / 0.02 | 0.07 / 0.08 | 0.01 |
| Paige | 135 | 0.29 / 0.29 | 0.59 / 0.60 | 0.07 / 0.07 | 0.03 / 0.03 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.47 | 0.39 / 0.41 | 0.05 / 0.04 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.19 | 0.01 / 0.01 | 0.01 |
| The Doorman | 38 | 0.16 / 0.16 | 0.62 / 0.61 | 0.17 / 0.18 | 0.03 / 0.04 | 0.01 |
| Victor | 129 | 0.15 / 0.16 | 0.64 / 0.64 | 0.16 / 0.15 | 0.03 / 0.03 | 0.01 |
| Solomon | 136 | 0.25 / 0.24 | 0.64 / 0.65 | 0.08 / 0.07 | 0.02 / 0.01 | 0.01 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.62 | 0.05 / 0.05 | 0.03 / 0.03 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| McGinnis | Mini Turret | ability | 0.467 | 0.577 | 0.62 |
| Sinclair | Vexing Bolt | ability | 0.351 | 0.274 | 1.39 |
| Warden | Last Stand | ability | 0.138 | 0.202 | 0.59 |
| Sinclair | Audience Participation | ability | 0.205 | 0.301 | 0.74 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.087 | 1.61 |
| Viscous | Goo Ball | ability | 0.107 | 0.075 | 1.78 |
| Pocket | Affliction | ability | 0.120 | 0.162 | 0.72 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.245 | 1.19 |
| Viscous | Express Shot | item | 0.052 | 0.027 | 2.41 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.172 | 1.26 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.230 | 0.83 |
| Viscous | Splatter | ability | 0.285 | 0.311 | 1.14 |
| Holliday | Powder Keg | ability | 0.397 | 0.382 | 1.11 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.169 | 1.23 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.316 | 0.89 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.272 | 1.13 |
| Celeste | Shining Wonder | ability | 0.170 | 0.162 | 1.24 |
| Dynamo | Kinetic Pulse | ability | 0.444 | 0.425 | 1.08 |
| Warden | Alchemical Flask | ability | 0.129 | 0.144 | 0.78 |
| Celeste | Light Eater | ability | 0.220 | 0.223 | 1.16 |
| Shiv | Killing Blow | ability | 0.056 | 0.034 | 1.79 |
| Graves | Jar of Dead | ability | 0.212 | 0.225 | 0.87 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.130 | 0.80 |
| Seven | Storm Cloud | ability | 0.202 | 0.225 | 0.87 |
| Viscous | Puddle Punch | ability | 0.123 | 0.120 | 1.28 |
| Victor | Pain Battery | ability | 0.276 | 0.258 | 1.11 |
| Solomon | Develop Queen | ability | 0.161 | 0.185 | 0.86 |
| Shiv | Slice and Dice | ability | 0.145 | 0.130 | 1.21 |
| Calico | MELEE | melee | 0.149 | 0.129 | 1.20 |
| Dynamo | Singularity | ability | 0.179 | 0.210 | 0.88 |
| Vyper | Split Shot | item | 0.110 | 0.089 | 1.26 |
| Graves | Borrowed Decree | ability | 0.195 | 0.203 | 0.88 |
| Lady Geist | Malice | ability | 0.144 | 0.168 | 0.87 |
| Mirage | Dust Devil | ability | 0.079 | 0.100 | 0.79 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.313 | 0.93 |
| Paige | Captivating Read | ability | 0.126 | 0.145 | 0.86 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.153 | 0.87 |
| Baba | Torment Pulse | item | 0.170 | 0.155 | 1.13 |
| Pocket | Barrage | ability | 0.260 | 0.233 | 1.08 |
| Rem | Pillow Toss | ability | 0.437 | 0.445 | 1.05 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1890 | 0.138 | 0.131 | 1.05 |
| Mystic Burst | 1692 | 0.050 | 0.045 | 1.12 |
| Quicksilver Reload | 1114 | 0.037 | 0.030 | 1.23 |
| Toxic Bullets | 875 | 0.113 | 0.117 | 0.96 |
| Spirit Snatch | 857 | 0.065 | 0.065 | 1.00 |
| Torment Pulse | 814 | 0.154 | 0.142 | 1.08 |
| Stalker | 794 | 0.051 | 0.050 | 1.01 |
| Spirit Strike | 711 | 0.046 | 0.046 | 0.99 |
| Ricochet | 700 | 0.050 | 0.066 | 0.76 |
| Spirit Burn | 687 | 0.084 | 0.080 | 1.05 |
| Mystic Shot | 673 | 0.062 | 0.059 | 1.05 |
| Escalating Exposure | 610 | 0.110 | 0.110 | 0.99 |
| Express Shot | 558 | 0.121 | 0.107 | 1.13 |
| Cold Front | 525 | 0.057 | 0.059 | 0.95 |
| Siphon Bullets | 521 | 0.086 | 0.086 | 0.99 |
| Tesla Bullets | 509 | 0.139 | 0.134 | 1.04 |
| Melee Charge | 434 | 0.047 | 0.029 | 1.59 |
| Headhunter | 410 | 0.090 | 0.090 | 1.00 |
| Capacitor | 375 | 0.206 | 0.199 | 1.03 |
| Headshot Booster | 375 | 0.044 | 0.038 | 1.16 |
| Mercurial Magnum | 340 | 0.103 | 0.095 | 1.09 |
| Rebuttal | 236 | 0.013 | 0.011 | 1.22 |
| Mystic Reverb | 211 | 0.166 | 0.206 | 0.81 |
| Lucky Shot | 201 | 0.142 | 0.097 | 1.47 |
| Arctic Blast | 172 | 0.141 | 0.101 | 1.39 |
| Split Shot | 170 | 0.090 | 0.086 | 1.04 |
| Crushing Fists | 148 | 0.055 | 0.031 | 1.78 |
| Decay | 135 | 0.173 | 0.180 | 0.96 |
| Phantom Strike | 125 | 0.050 | 0.044 | 1.15 |
| Scourge | 122 | 0.158 | 0.165 | 0.96 |
| Alchemical Fire | 111 | 0.126 | 0.152 | 0.83 |
| Return Fire | 96 | 0.094 | 0.030 | 3.15 |
| Lightning Scroll | 49 | 0.039 | 0.026 | 1.49 |
| Focus Lens | 39 | 0.105 | 0.087 | 1.21 |
| Silence Wave | 33 | 0.046 | 0.049 | 0.95 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.049 | 0.010 | 4.96 |
| Apollo | Melee Charge | 58 | 0.045 | 0.011 | 3.97 |
| Rat King | Return Fire | 41 | 0.101 | 0.029 | 3.45 |
| Drifter | Melee Charge | 68 | 0.035 | 0.012 | 2.89 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.021 | 2.24 |
| Nurse Harrow | Ricochet | 135 | 0.025 | 0.052 | 0.49 |
| Violet | Torment Pulse | 69 | 0.103 | 0.055 | 1.89 |
| Billy | Melee Charge | 48 | 0.044 | 0.023 | 1.87 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.025 | 1.85 |
| Billy | Crushing Fists | 31 | 0.050 | 0.027 | 1.82 |
| Yamato | Crushing Fists | 30 | 0.050 | 0.028 | 1.78 |
| Drifter | Spirit Burn | 42 | 0.070 | 0.041 | 1.70 |
| Violet | Mystic Burst | 66 | 0.044 | 0.026 | 1.69 |
| Haze | Lucky Shot | 92 | 0.153 | 0.099 | 1.55 |
| Apollo | Mystic Burst | 66 | 0.052 | 0.034 | 1.51 |
| Wraith | Ricochet | 185 | 0.041 | 0.062 | 0.67 |
| Calico | Arctic Blast | 102 | 0.155 | 0.106 | 1.47 |
| Infernus | Ricochet | 66 | 0.027 | 0.039 | 0.68 |
| Shiv | Express Shot | 125 | 0.255 | 0.181 | 1.41 |
| Venator | Ricochet | 36 | 0.057 | 0.078 | 0.73 |
| Violet | Tankbuster | 207 | 0.144 | 0.106 | 1.36 |
| Yamato | Melee Charge | 57 | 0.041 | 0.030 | 1.35 |
| Paradox | Headshot Booster | 42 | 0.042 | 0.032 | 1.33 |
| Lash | Mystic Burst | 210 | 0.061 | 0.046 | 1.31 |
| Abrams | Phantom Strike | 58 | 0.046 | 0.035 | 1.30 |
| Mirage | Ricochet | 33 | 0.041 | 0.053 | 0.77 |
| Bebop | Mystic Reverb | 24 | 0.143 | 0.184 | 0.77 |
| Shiv | Lucky Shot | 45 | 0.143 | 0.113 | 1.27 |
| Vyper | Split Shot | 69 | 0.144 | 0.115 | 1.25 |
| Yamato | Express Shot | 46 | 0.158 | 0.127 | 1.24 |
| Haze | Ricochet | 207 | 0.067 | 0.083 | 0.81 |
| Abrams | Crushing Fists | 40 | 0.074 | 0.060 | 1.22 |
| Abrams | Melee Charge | 129 | 0.068 | 0.055 | 1.22 |
| Violet | Mystic Shot | 170 | 0.073 | 0.060 | 1.22 |
| Nurse Harrow | Decay | 41 | 0.220 | 0.182 | 1.21 |
| Mo & Krill | Mystic Burst | 174 | 0.072 | 0.060 | 1.21 |
| Mo & Krill | Quicksilver Reload | 150 | 0.058 | 0.048 | 1.20 |
| Drifter | Mystic Burst | 96 | 0.041 | 0.034 | 1.19 |
| Holliday | Headshot Booster | 31 | 0.040 | 0.034 | 1.19 |
| Apollo | Tankbuster | 47 | 0.148 | 0.125 | 1.19 |
