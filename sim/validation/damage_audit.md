# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Warden | 33 | 0.52 / 0.49 | 0.31 / 0.36 | 0.11 / 0.12 | 0.03 / 0.02 | 0.06 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.57 | 0.17 / 0.19 | 0.04 / 0.05 | 0.06 |
| Viscous | 29 | 0.13 / 0.17 | 0.51 / 0.51 | 0.28 / 0.25 | 0.05 / 0.06 | 0.05 |
| Mirage | 45 | 0.31 / 0.31 | 0.48 / 0.45 | 0.17 / 0.21 | 0.02 / 0.02 | 0.05 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.33 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.57 | 0.17 / 0.15 | 0.17 / 0.17 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.33 | 0.15 / 0.13 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.14 | 0.05 / 0.06 | 0.03 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.60 | 0.25 / 0.23 | 0.03 / 0.03 | 0.03 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.08 | 0.02 / 0.02 | 0.03 |
| Shiv | 209 | 0.27 / 0.30 | 0.48 / 0.47 | 0.16 / 0.15 | 0.08 / 0.08 | 0.03 |
| Drifter | 186 | 0.26 / 0.27 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.12 | 0.03 |
| Seven | 95 | 0.20 / 0.19 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Grey Talon | 103 | 0.31 / 0.31 | 0.49 / 0.49 | 0.16 / 0.19 | 0.01 / 0.01 | 0.03 |
| Yamato | 131 | 0.24 / 0.25 | 0.38 / 0.37 | 0.17 / 0.19 | 0.18 / 0.18 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.09 | 0.05 / 0.03 | 0.03 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.52 | 0.27 / 0.28 | 0.02 / 0.02 | 0.03 |
| McGinnis | 49 | 0.20 / 0.22 | 0.64 / 0.64 | 0.12 / 0.11 | 0.02 / 0.02 | 0.03 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.03 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.63 | 0.06 / 0.06 | 0.03 / 0.03 | 0.02 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.69 | 0.17 / 0.19 | 0.03 / 0.03 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.15 | 0.22 / 0.23 | 0.02 |
| Pocket | 117 | 0.14 / 0.14 | 0.66 / 0.68 | 0.16 / 0.16 | 0.02 / 0.02 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.27 | 0.25 / 0.24 | 0.02 / 0.02 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.20 | 0.13 / 0.12 | 0.42 / 0.43 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.20 | 0.05 / 0.05 | 0.02 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.37 | 0.10 / 0.12 | 0.10 / 0.10 | 0.02 |
| Vindicta | 131 | 0.44 / 0.44 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Paradox | 168 | 0.24 / 0.24 | 0.48 / 0.48 | 0.23 / 0.24 | 0.03 / 0.02 | 0.02 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.51 | 0.12 / 0.12 | 0.02 / 0.01 | 0.02 |
| The Doorman | 38 | 0.16 / 0.16 | 0.62 / 0.61 | 0.17 / 0.18 | 0.03 / 0.04 | 0.02 |
| Baba | 146 | 0.07 / 0.07 | 0.54 / 0.55 | 0.25 / 0.25 | 0.12 / 0.13 | 0.02 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.57 | 0.16 / 0.16 | 0.05 / 0.05 | 0.01 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.47 | 0.39 / 0.41 | 0.05 / 0.04 | 0.01 |
| Sinclair | 55 | 0.12 / 0.13 | 0.79 / 0.78 | 0.04 / 0.04 | 0.03 / 0.03 | 0.01 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.40 | 0.03 / 0.03 | 0.07 / 0.07 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.66 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Paige | 135 | 0.29 / 0.29 | 0.59 / 0.60 | 0.07 / 0.07 | 0.03 / 0.04 | 0.01 |
| Lady Geist | 37 | 0.29 / 0.29 | 0.62 / 0.62 | 0.05 / 0.05 | 0.03 / 0.03 | 0.01 |
| Solomon | 136 | 0.25 / 0.24 | 0.64 / 0.65 | 0.08 / 0.08 | 0.02 / 0.01 | 0.01 |
| Victor | 129 | 0.15 / 0.16 | 0.64 / 0.64 | 0.16 / 0.16 | 0.03 / 0.03 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Vexing Bolt | ability | 0.351 | 0.276 | 1.37 |
| Sinclair | Audience Participation | ability | 0.205 | 0.300 | 0.73 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.081 | 1.70 |
| Viscous | Goo Ball | ability | 0.107 | 0.075 | 1.79 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.238 | 1.22 |
| Pocket | Affliction | ability | 0.120 | 0.163 | 0.73 |
| Warden | Last Stand | ability | 0.138 | 0.173 | 0.75 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.106 | 1.44 |
| Viscous | Express Shot | item | 0.052 | 0.027 | 2.44 |
| Viscous | Splatter | ability | 0.285 | 0.312 | 1.15 |
| Lady Geist | Malice | ability | 0.144 | 0.181 | 0.79 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.169 | 1.25 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.226 | 0.84 |
| Holliday | Powder Keg | ability | 0.397 | 0.382 | 1.10 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.316 | 0.89 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.169 | 1.22 |
| Dynamo | Kinetic Pulse | ability | 0.444 | 0.426 | 1.09 |
| Celeste | Shining Wonder | ability | 0.170 | 0.159 | 1.24 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.274 | 1.13 |
| Celeste | Light Eater | ability | 0.220 | 0.218 | 1.16 |
| Shiv | Killing Blow | ability | 0.056 | 0.034 | 1.80 |
| McGinnis | Mini Turret | ability | 0.467 | 0.492 | 1.07 |
| Viscous | Puddle Punch | ability | 0.123 | 0.120 | 1.29 |
| Seven | Storm Cloud | ability | 0.202 | 0.225 | 0.87 |
| Graves | Jar of Dead | ability | 0.212 | 0.224 | 0.87 |
| Shiv | Slice and Dice | ability | 0.145 | 0.130 | 1.22 |
| Mirage | Toxic Bullets | item | 0.093 | 0.118 | 0.79 |
| Warden | Alchemical Flask | ability | 0.129 | 0.146 | 0.83 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.159 | 0.85 |
| Victor | Pain Battery | ability | 0.276 | 0.258 | 1.10 |
| Calico | MELEE | melee | 0.149 | 0.129 | 1.19 |
| Graves | Borrowed Decree | ability | 0.195 | 0.202 | 0.88 |
| Dynamo | Singularity | ability | 0.179 | 0.209 | 0.89 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.313 | 0.93 |
| Billy | MELEE | melee | 0.223 | 0.235 | 0.91 |
| Abrams | MELEE | melee | 0.424 | 0.427 | 1.05 |
| Solomon | Develop Queen | ability | 0.161 | 0.180 | 0.88 |
| Vyper | Split Shot | item | 0.110 | 0.091 | 1.22 |
| Pocket | Barrage | ability | 0.260 | 0.234 | 1.09 |
| Mirage | Dust Devil | ability | 0.079 | 0.099 | 0.81 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1890 | 0.138 | 0.132 | 1.04 |
| Mystic Burst | 1692 | 0.050 | 0.044 | 1.14 |
| Quicksilver Reload | 1114 | 0.037 | 0.029 | 1.24 |
| Toxic Bullets | 875 | 0.113 | 0.118 | 0.95 |
| Spirit Snatch | 857 | 0.065 | 0.065 | 0.99 |
| Torment Pulse | 814 | 0.154 | 0.146 | 1.06 |
| Stalker | 794 | 0.051 | 0.050 | 1.01 |
| Spirit Strike | 711 | 0.046 | 0.046 | 0.99 |
| Ricochet | 700 | 0.050 | 0.066 | 0.75 |
| Spirit Burn | 687 | 0.084 | 0.084 | 1.01 |
| Mystic Shot | 673 | 0.062 | 0.059 | 1.05 |
| Escalating Exposure | 610 | 0.110 | 0.109 | 1.01 |
| Express Shot | 558 | 0.121 | 0.107 | 1.13 |
| Cold Front | 525 | 0.057 | 0.060 | 0.95 |
| Siphon Bullets | 521 | 0.086 | 0.087 | 0.98 |
| Tesla Bullets | 509 | 0.139 | 0.134 | 1.04 |
| Melee Charge | 434 | 0.047 | 0.029 | 1.58 |
| Headhunter | 410 | 0.090 | 0.091 | 0.99 |
| Capacitor | 375 | 0.206 | 0.199 | 1.03 |
| Headshot Booster | 375 | 0.044 | 0.039 | 1.15 |
| Mercurial Magnum | 340 | 0.103 | 0.096 | 1.08 |
| Rebuttal | 236 | 0.013 | 0.011 | 1.22 |
| Mystic Reverb | 211 | 0.166 | 0.204 | 0.81 |
| Lucky Shot | 201 | 0.142 | 0.097 | 1.47 |
| Arctic Blast | 172 | 0.141 | 0.099 | 1.42 |
| Split Shot | 170 | 0.090 | 0.085 | 1.05 |
| Crushing Fists | 148 | 0.055 | 0.032 | 1.71 |
| Decay | 135 | 0.173 | 0.175 | 0.99 |
| Phantom Strike | 125 | 0.050 | 0.044 | 1.13 |
| Scourge | 122 | 0.158 | 0.175 | 0.90 |
| Alchemical Fire | 111 | 0.126 | 0.152 | 0.83 |
| Return Fire | 96 | 0.094 | 0.031 | 3.04 |
| Lightning Scroll | 49 | 0.039 | 0.026 | 1.50 |
| Focus Lens | 39 | 0.105 | 0.087 | 1.20 |
| Silence Wave | 33 | 0.046 | 0.049 | 0.94 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.049 | 0.011 | 4.40 |
| Apollo | Melee Charge | 58 | 0.045 | 0.012 | 3.81 |
| Drifter | Melee Charge | 68 | 0.035 | 0.009 | 3.69 |
| Rat King | Return Fire | 41 | 0.101 | 0.030 | 3.32 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.021 | 2.21 |
| Nurse Harrow | Ricochet | 135 | 0.025 | 0.049 | 0.53 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.025 | 1.88 |
| Violet | Torment Pulse | 69 | 0.103 | 0.055 | 1.87 |
| Billy | Crushing Fists | 31 | 0.050 | 0.027 | 1.82 |
| Billy | Melee Charge | 48 | 0.044 | 0.025 | 1.78 |
| Violet | Mystic Burst | 66 | 0.044 | 0.026 | 1.66 |
| Haze | Lucky Shot | 92 | 0.153 | 0.098 | 1.55 |
| Drifter | Spirit Burn | 42 | 0.070 | 0.045 | 1.54 |
| Calico | Arctic Blast | 102 | 0.155 | 0.103 | 1.51 |
| Apollo | Mystic Burst | 66 | 0.052 | 0.034 | 1.51 |
| Venator | Ricochet | 36 | 0.057 | 0.085 | 0.67 |
| Wraith | Ricochet | 185 | 0.041 | 0.061 | 0.67 |
| Infernus | Ricochet | 66 | 0.027 | 0.039 | 0.68 |
| Yamato | Crushing Fists | 30 | 0.050 | 0.035 | 1.43 |
| Shiv | Express Shot | 125 | 0.255 | 0.189 | 1.35 |
| Lash | Mystic Burst | 210 | 0.061 | 0.046 | 1.34 |
| Violet | Tankbuster | 207 | 0.144 | 0.109 | 1.33 |
| Shiv | Lucky Shot | 45 | 0.143 | 0.110 | 1.30 |
| Mo & Krill | Mystic Burst | 174 | 0.072 | 0.057 | 1.27 |
| Abrams | Phantom Strike | 58 | 0.046 | 0.036 | 1.27 |
| Paradox | Headshot Booster | 42 | 0.042 | 0.033 | 1.27 |
| Bebop | Mystic Reverb | 24 | 0.143 | 0.180 | 0.79 |
| Holliday | Headshot Booster | 31 | 0.040 | 0.032 | 1.26 |
| Haze | Ricochet | 207 | 0.067 | 0.084 | 0.80 |
| Drifter | Tankbuster | 101 | 0.108 | 0.087 | 1.24 |
| Nurse Harrow | Decay | 41 | 0.220 | 0.178 | 1.24 |
| Violet | Mystic Shot | 170 | 0.073 | 0.059 | 1.23 |
| Mo & Krill | Quicksilver Reload | 150 | 0.058 | 0.047 | 1.22 |
| Drifter | Mystic Burst | 96 | 0.041 | 0.034 | 1.22 |
| Vyper | Split Shot | 69 | 0.144 | 0.118 | 1.22 |
| Apollo | Tankbuster | 47 | 0.148 | 0.122 | 1.21 |
| Grey Talon | Mystic Reverb | 22 | 0.155 | 0.186 | 0.83 |
| Apollo | Torment Pulse | 23 | 0.163 | 0.136 | 1.20 |
| Abrams | Crushing Fists | 40 | 0.074 | 0.061 | 1.20 |
| Abrams | Melee Charge | 129 | 0.068 | 0.056 | 1.20 |
