# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Warden | 33 | 0.52 / 0.49 | 0.31 / 0.36 | 0.11 / 0.12 | 0.03 / 0.02 | 0.06 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.57 | 0.17 / 0.19 | 0.04 / 0.05 | 0.05 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.50 | 0.28 / 0.25 | 0.05 / 0.06 | 0.05 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.33 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.33 | 0.15 / 0.13 | 0.04 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.47 | 0.17 / 0.21 | 0.02 / 0.02 | 0.04 |
| Apollo | 92 | 0.11 / 0.10 | 0.53 / 0.57 | 0.17 / 0.15 | 0.17 / 0.17 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.15 | 0.05 / 0.06 | 0.04 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.59 | 0.25 / 0.23 | 0.03 / 0.03 | 0.03 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.08 | 0.02 / 0.02 | 0.03 |
| Seven | 95 | 0.20 / 0.19 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Grey Talon | 103 | 0.31 / 0.31 | 0.49 / 0.48 | 0.16 / 0.19 | 0.01 / 0.01 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.15 | 0.08 / 0.08 | 0.03 |
| Yamato | 131 | 0.24 / 0.25 | 0.38 / 0.38 | 0.17 / 0.19 | 0.18 / 0.18 | 0.03 |
| Nurse Harrow | 347 | 0.29 / 0.26 | 0.61 / 0.64 | 0.06 / 0.06 | 0.03 / 0.03 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.08 | 0.05 / 0.03 | 0.03 |
| Graves | 151 | 0.20 / 0.18 | 0.50 / 0.52 | 0.27 / 0.28 | 0.02 / 0.02 | 0.03 |
| McGinnis | 49 | 0.20 / 0.22 | 0.64 / 0.64 | 0.12 / 0.11 | 0.02 / 0.02 | 0.03 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.03 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Billy | 93 | 0.21 / 0.19 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.23 | 0.02 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.69 | 0.17 / 0.19 | 0.03 / 0.03 | 0.02 |
| Drifter | 186 | 0.26 / 0.27 | 0.44 / 0.45 | 0.17 / 0.16 | 0.11 / 0.12 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.68 | 0.16 / 0.16 | 0.02 / 0.02 | 0.02 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.02 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.57 | 0.19 / 0.20 | 0.05 / 0.05 | 0.02 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.02 |
| Baba | 146 | 0.07 / 0.07 | 0.54 / 0.55 | 0.25 / 0.25 | 0.12 / 0.13 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.20 | 0.13 / 0.13 | 0.42 / 0.42 | 0.02 |
| Vindicta | 131 | 0.44 / 0.44 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Paradox | 168 | 0.24 / 0.24 | 0.48 / 0.48 | 0.23 / 0.24 | 0.03 / 0.02 | 0.02 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.51 | 0.12 / 0.12 | 0.02 / 0.01 | 0.02 |
| The Doorman | 38 | 0.16 / 0.16 | 0.62 / 0.61 | 0.17 / 0.18 | 0.03 / 0.04 | 0.02 |
| Silver | 100 | 0.41 / 0.41 | 0.37 / 0.37 | 0.10 / 0.12 | 0.10 / 0.10 | 0.02 |
| Venator | 257 | 0.48 / 0.49 | 0.40 / 0.40 | 0.03 / 0.03 | 0.07 / 0.07 | 0.01 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.47 | 0.39 / 0.41 | 0.05 / 0.04 | 0.01 |
| Sinclair | 55 | 0.12 / 0.13 | 0.79 / 0.78 | 0.04 / 0.04 | 0.03 / 0.03 | 0.01 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.57 | 0.16 / 0.16 | 0.05 / 0.05 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.01 |
| Solomon | 136 | 0.25 / 0.24 | 0.64 / 0.65 | 0.08 / 0.08 | 0.02 / 0.01 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.66 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Paige | 135 | 0.29 / 0.29 | 0.59 / 0.60 | 0.07 / 0.07 | 0.03 / 0.03 | 0.01 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.64 | 0.16 / 0.17 | 0.03 / 0.03 | 0.01 |
| Lady Geist | 37 | 0.29 / 0.29 | 0.62 / 0.62 | 0.05 / 0.05 | 0.03 / 0.03 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Vexing Bolt | ability | 0.351 | 0.272 | 1.38 |
| Sinclair | Audience Participation | ability | 0.205 | 0.298 | 0.73 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.081 | 1.71 |
| Viscous | Goo Ball | ability | 0.107 | 0.076 | 1.76 |
| Pocket | Affliction | ability | 0.120 | 0.161 | 0.72 |
| Warden | Last Stand | ability | 0.138 | 0.174 | 0.74 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.321 | 0.85 |
| Viscous | Express Shot | item | 0.052 | 0.026 | 2.53 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.107 | 1.42 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.169 | 1.25 |
| Viscous | Splatter | ability | 0.285 | 0.311 | 1.14 |
| Lady Geist | Malice | ability | 0.144 | 0.180 | 0.80 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.226 | 0.84 |
| Holliday | Powder Keg | ability | 0.397 | 0.381 | 1.10 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.274 | 1.13 |
| Dynamo | Kinetic Pulse | ability | 0.444 | 0.425 | 1.08 |
| Celeste | Light Eater | ability | 0.220 | 0.218 | 1.16 |
| Solomon | Develop Queen | ability | 0.161 | 0.185 | 0.83 |
| Shiv | Killing Blow | ability | 0.056 | 0.034 | 1.82 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.316 | 0.90 |
| Celeste | Shining Wonder | ability | 0.170 | 0.162 | 1.21 |
| Viscous | Puddle Punch | ability | 0.123 | 0.118 | 1.30 |
| Graves | Jar of Dead | ability | 0.212 | 0.224 | 0.87 |
| Seven | Storm Cloud | ability | 0.202 | 0.224 | 0.87 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.174 | 1.17 |
| Dynamo | Singularity | ability | 0.179 | 0.213 | 0.87 |
| McGinnis | Mini Turret | ability | 0.467 | 0.492 | 1.06 |
| Warden | Alchemical Flask | ability | 0.129 | 0.147 | 0.82 |
| Shiv | Slice and Dice | ability | 0.145 | 0.130 | 1.22 |
| Graves | Borrowed Decree | ability | 0.195 | 0.204 | 0.87 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.160 | 0.85 |
| Abrams | MELEE | melee | 0.424 | 0.422 | 1.06 |
| Calico | MELEE | melee | 0.149 | 0.129 | 1.18 |
| Vyper | Split Shot | item | 0.110 | 0.090 | 1.24 |
| Apollo | Itani Lo Sahn | ability | 0.100 | 0.117 | 0.82 |
| Billy | Bashdown | ability | 0.309 | 0.312 | 0.93 |
| Mirage | Toxic Bullets | item | 0.093 | 0.110 | 0.82 |
| Billy | MELEE | melee | 0.223 | 0.231 | 0.91 |
| Dynamo | MELEE | melee | 0.050 | 0.034 | 1.52 |
| Apollo | Disengaging Sigil | ability | 0.149 | 0.163 | 0.88 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1890 | 0.138 | 0.132 | 1.04 |
| Mystic Burst | 1692 | 0.050 | 0.044 | 1.14 |
| Quicksilver Reload | 1114 | 0.037 | 0.029 | 1.25 |
| Toxic Bullets | 875 | 0.113 | 0.117 | 0.96 |
| Spirit Snatch | 857 | 0.065 | 0.063 | 1.02 |
| Torment Pulse | 814 | 0.154 | 0.145 | 1.06 |
| Stalker | 794 | 0.051 | 0.050 | 1.01 |
| Spirit Strike | 711 | 0.046 | 0.046 | 1.00 |
| Ricochet | 700 | 0.050 | 0.065 | 0.76 |
| Spirit Burn | 687 | 0.084 | 0.084 | 1.00 |
| Mystic Shot | 673 | 0.062 | 0.059 | 1.06 |
| Escalating Exposure | 610 | 0.110 | 0.114 | 0.96 |
| Express Shot | 558 | 0.121 | 0.108 | 1.13 |
| Cold Front | 525 | 0.057 | 0.059 | 0.95 |
| Siphon Bullets | 521 | 0.086 | 0.087 | 0.98 |
| Tesla Bullets | 509 | 0.139 | 0.134 | 1.04 |
| Melee Charge | 434 | 0.047 | 0.042 | 1.12 |
| Headhunter | 410 | 0.090 | 0.091 | 0.99 |
| Capacitor | 375 | 0.206 | 0.199 | 1.03 |
| Headshot Booster | 375 | 0.044 | 0.038 | 1.15 |
| Mercurial Magnum | 340 | 0.103 | 0.096 | 1.08 |
| Rebuttal | 236 | 0.013 | 0.016 | 0.84 |
| Mystic Reverb | 211 | 0.166 | 0.204 | 0.81 |
| Lucky Shot | 201 | 0.142 | 0.098 | 1.45 |
| Arctic Blast | 172 | 0.141 | 0.100 | 1.41 |
| Split Shot | 170 | 0.090 | 0.084 | 1.07 |
| Crushing Fists | 148 | 0.055 | 0.047 | 1.16 |
| Decay | 135 | 0.173 | 0.174 | 1.00 |
| Phantom Strike | 125 | 0.050 | 0.045 | 1.13 |
| Scourge | 122 | 0.158 | 0.176 | 0.90 |
| Alchemical Fire | 111 | 0.126 | 0.150 | 0.84 |
| Return Fire | 96 | 0.094 | 0.031 | 3.06 |
| Lightning Scroll | 49 | 0.039 | 0.026 | 1.46 |
| Focus Lens | 39 | 0.105 | 0.089 | 1.17 |
| Silence Wave | 33 | 0.046 | 0.049 | 0.94 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Rat King | Return Fire | 41 | 0.101 | 0.030 | 3.31 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.021 | 2.23 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.024 | 1.89 |
| Violet | Torment Pulse | 69 | 0.103 | 0.055 | 1.88 |
| Nurse Harrow | Ricochet | 135 | 0.025 | 0.046 | 0.55 |
| Violet | Mystic Burst | 66 | 0.044 | 0.026 | 1.68 |
| Haze | Lucky Shot | 92 | 0.153 | 0.099 | 1.54 |
| Apollo | Mystic Burst | 66 | 0.052 | 0.035 | 1.50 |
| Drifter | Spirit Burn | 42 | 0.070 | 0.047 | 1.50 |
| Wraith | Ricochet | 185 | 0.041 | 0.061 | 0.67 |
| Calico | Arctic Blast | 102 | 0.155 | 0.104 | 1.49 |
| Venator | Ricochet | 36 | 0.057 | 0.085 | 0.67 |
| Infernus | Ricochet | 66 | 0.027 | 0.039 | 0.68 |
| Apollo | Melee Charge | 58 | 0.045 | 0.032 | 1.42 |
| Drifter | Crushing Fists | 25 | 0.049 | 0.035 | 1.41 |
| Lash | Mystic Burst | 210 | 0.061 | 0.045 | 1.34 |
| Shiv | Express Shot | 125 | 0.255 | 0.191 | 1.34 |
| Violet | Tankbuster | 207 | 0.144 | 0.108 | 1.34 |
| Holliday | Headshot Booster | 31 | 0.040 | 0.031 | 1.30 |
| Shiv | Lucky Shot | 45 | 0.143 | 0.112 | 1.28 |
| Mo & Krill | Mystic Burst | 174 | 0.072 | 0.056 | 1.28 |
| Bebop | Mystic Reverb | 24 | 0.143 | 0.182 | 0.79 |
| Yamato | Crushing Fists | 30 | 0.050 | 0.039 | 1.27 |
| Paradox | Headshot Booster | 42 | 0.042 | 0.033 | 1.27 |
| Abrams | Phantom Strike | 58 | 0.046 | 0.036 | 1.26 |
| Haze | Ricochet | 207 | 0.067 | 0.084 | 0.81 |
| Violet | Mystic Shot | 170 | 0.073 | 0.059 | 1.24 |
| Vyper | Split Shot | 69 | 0.144 | 0.117 | 1.24 |
| Nurse Harrow | Decay | 41 | 0.220 | 0.178 | 1.24 |
| Drifter | Tankbuster | 101 | 0.108 | 0.087 | 1.23 |
| Drifter | Mystic Burst | 96 | 0.041 | 0.034 | 1.23 |
| Mo & Krill | Quicksilver Reload | 150 | 0.058 | 0.047 | 1.22 |
| Apollo | Tankbuster | 47 | 0.148 | 0.122 | 1.21 |
| Yamato | Express Shot | 46 | 0.158 | 0.132 | 1.20 |
| Victor | Escalating Exposure | 102 | 0.133 | 0.158 | 0.84 |
| Grey Talon | Mystic Reverb | 22 | 0.155 | 0.182 | 0.85 |
| Apollo | Torment Pulse | 23 | 0.163 | 0.139 | 1.18 |
| Lash | Headshot Booster | 156 | 0.040 | 0.034 | 1.18 |
| Apollo | Spirit Snatch | 66 | 0.057 | 0.049 | 1.17 |
| Mo & Krill | Arctic Blast | 26 | 0.118 | 0.101 | 1.16 |
