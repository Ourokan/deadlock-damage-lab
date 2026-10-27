# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Warden | 33 | 0.52 / 0.45 | 0.31 / 0.39 | 0.11 / 0.12 | 0.03 / 0.03 | 0.09 |
| Viscous | 29 | 0.13 / 0.12 | 0.51 / 0.58 | 0.28 / 0.23 | 0.05 / 0.05 | 0.07 |
| Calico | 110 | 0.13 / 0.10 | 0.38 / 0.40 | 0.31 / 0.35 | 0.15 / 0.14 | 0.06 |
| Grey Talon | 103 | 0.31 / 0.28 | 0.49 / 0.51 | 0.16 / 0.20 | 0.01 / 0.01 | 0.05 |
| Graves | 151 | 0.20 / 0.16 | 0.50 / 0.54 | 0.27 / 0.26 | 0.02 / 0.02 | 0.05 |
| Paige | 135 | 0.29 / 0.26 | 0.59 / 0.63 | 0.07 / 0.07 | 0.03 / 0.03 | 0.04 |
| Ivy | 116 | 0.32 / 0.30 | 0.36 / 0.34 | 0.26 / 0.31 | 0.04 / 0.03 | 0.04 |
| Mirage | 45 | 0.31 / 0.28 | 0.48 / 0.51 | 0.17 / 0.19 | 0.02 / 0.02 | 0.04 |
| Silver | 100 | 0.41 / 0.37 | 0.37 / 0.39 | 0.10 / 0.12 | 0.10 / 0.10 | 0.04 |
| Celeste | 77 | 0.16 / 0.14 | 0.61 / 0.63 | 0.17 / 0.18 | 0.04 / 0.04 | 0.04 |
| Paradox | 168 | 0.24 / 0.22 | 0.48 / 0.50 | 0.23 / 0.25 | 0.03 / 0.02 | 0.04 |
| Solomon | 136 | 0.25 / 0.21 | 0.64 / 0.67 | 0.08 / 0.08 | 0.02 / 0.01 | 0.04 |
| Yamato | 131 | 0.24 / 0.22 | 0.38 / 0.39 | 0.17 / 0.19 | 0.18 / 0.19 | 0.04 |
| Nurse Harrow | 347 | 0.29 / 0.27 | 0.61 / 0.64 | 0.06 / 0.07 | 0.03 / 0.02 | 0.04 |
| Apollo | 92 | 0.11 / 0.09 | 0.53 / 0.57 | 0.17 / 0.15 | 0.17 / 0.17 | 0.04 |
| Bebop | 254 | 0.18 / 0.16 | 0.56 / 0.58 | 0.19 / 0.20 | 0.05 / 0.05 | 0.03 |
| Lash | 216 | 0.13 / 0.12 | 0.58 / 0.61 | 0.25 / 0.24 | 0.03 / 0.02 | 0.03 |
| Deadman Danny | 357 | 0.16 / 0.13 | 0.63 / 0.65 | 0.18 / 0.20 | 0.01 / 0.01 | 0.03 |
| Drifter | 186 | 0.26 / 0.23 | 0.44 / 0.47 | 0.17 / 0.17 | 0.11 / 0.12 | 0.03 |
| Billy | 93 | 0.21 / 0.18 | 0.41 / 0.42 | 0.14 / 0.16 | 0.22 / 0.22 | 0.03 |
| Mo & Krill | 176 | 0.07 / 0.06 | 0.47 / 0.47 | 0.39 / 0.42 | 0.05 / 0.04 | 0.03 |
| Abrams | 138 | 0.23 / 0.21 | 0.20 / 0.20 | 0.13 / 0.14 | 0.42 / 0.44 | 0.03 |
| McGinnis | 49 | 0.20 / 0.18 | 0.64 / 0.67 | 0.12 / 0.11 | 0.02 / 0.01 | 0.03 |
| Venator | 257 | 0.38 / 0.36 | 0.50 / 0.52 | 0.03 / 0.04 | 0.07 / 0.07 | 0.03 |
| Wraith | 283 | 0.32 / 0.31 | 0.41 / 0.42 | 0.24 / 0.25 | 0.01 / 0.01 | 0.03 |
| Kelvin | 80 | 0.08 / 0.07 | 0.70 / 0.71 | 0.17 / 0.18 | 0.03 / 0.03 | 0.03 |
| Victor | 129 | 0.15 / 0.14 | 0.64 / 0.64 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Rem | 57 | 0.20 / 0.18 | 0.58 / 0.60 | 0.16 / 0.17 | 0.05 / 0.05 | 0.02 |
| Baba | 146 | 0.07 / 0.06 | 0.54 / 0.53 | 0.25 / 0.26 | 0.12 / 0.13 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.28 | 0.62 / 0.64 | 0.05 / 0.05 | 0.03 / 0.03 | 0.02 |
| Holliday | 73 | 0.27 / 0.25 | 0.54 / 0.54 | 0.13 / 0.15 | 0.05 / 0.05 | 0.02 |
| Pocket | 117 | 0.14 / 0.12 | 0.66 / 0.67 | 0.16 / 0.17 | 0.02 / 0.02 | 0.02 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.68 | 0.10 / 0.09 | 0.02 / 0.02 | 0.02 |
| Dynamo | 53 | 0.23 / 0.23 | 0.62 / 0.61 | 0.08 / 0.10 | 0.05 / 0.05 | 0.02 |
| Infernus | 173 | 0.23 / 0.21 | 0.60 / 0.61 | 0.13 / 0.14 | 0.03 / 0.03 | 0.02 |
| Vindicta | 131 | 0.44 / 0.43 | 0.49 / 0.51 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Vyper | 78 | 0.46 / 0.45 | 0.26 / 0.28 | 0.25 / 0.25 | 0.02 / 0.01 | 0.02 |
| The Doorman | 38 | 0.16 / 0.15 | 0.62 / 0.62 | 0.17 / 0.19 | 0.03 / 0.03 | 0.02 |
| Sinclair | 55 | 0.12 / 0.11 | 0.79 / 0.80 | 0.04 / 0.03 | 0.03 / 0.03 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.66 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Violet | 376 | 0.19 / 0.19 | 0.67 / 0.69 | 0.10 / 0.09 | 0.02 / 0.02 | 0.01 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.50 | 0.12 / 0.13 | 0.02 / 0.01 | 0.01 |
| Rat King | 424 | 0.33 / 0.32 | 0.57 / 0.58 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |
| Shiv | 209 | 0.27 / 0.27 | 0.48 / 0.48 | 0.16 / 0.16 | 0.08 / 0.08 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Sinclair | Audience Participation | ability | 0.205 | 0.330 | 0.57 |
| McGinnis | Mini Turret | ability | 0.467 | 0.526 | 0.83 |
| Warden | Last Stand | ability | 0.138 | 0.194 | 0.62 |
| Kelvin | Arctic Beam | ability | 0.402 | 0.410 | 0.81 |
| Paige | Bookwyrm | ability | 0.376 | 0.400 | 0.83 |
| Graves | Jar of Dead | ability | 0.212 | 0.237 | 0.75 |
| The Doorman | Call Bell | ability | 0.474 | 0.488 | 0.87 |
| Rem | Pillow Toss | ability | 0.437 | 0.457 | 0.86 |
| Lash | Ground Strike | ability | 0.350 | 0.374 | 0.84 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.162 | 0.68 |
| Lady Geist | Malice | ability | 0.144 | 0.188 | 0.72 |
| Victor | Aura of Suffering | ability | 0.306 | 0.327 | 0.83 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.084 | 1.55 |
| Calico | Gloom Bombs | ability | 0.182 | 0.193 | 0.73 |
| Graves | Borrowed Decree | ability | 0.195 | 0.214 | 0.76 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.298 | 0.82 |
| Billy | Bashdown | ability | 0.309 | 0.323 | 0.83 |
| Solomon | Develop Queen | ability | 0.161 | 0.188 | 0.73 |
| Grey Talon | Charged Shot | ability | 0.351 | 0.360 | 0.86 |
| Apollo | Flawless Advance | ability | 0.285 | 0.302 | 0.84 |
| Warden | Alchemical Flask | ability | 0.129 | 0.157 | 0.71 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.225 | 0.79 |
| Solomon | Setup Bishop | ability | 0.307 | 0.312 | 0.85 |
| Viscous | Splatter | ability | 0.285 | 0.313 | 0.85 |
| Deadman Danny | Strix Salvo | ability | 0.250 | 0.254 | 0.82 |
| Viscous | Express Shot | item | 0.052 | 0.019 | 2.57 |
| Abrams | MELEE | melee | 0.424 | 0.436 | 0.90 |
| Mirage | Djinn's Mark | ability | 0.291 | 0.310 | 0.86 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.136 | 1.29 |
| Infernus | Flame Dash | ability | 0.216 | 0.248 | 0.82 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.286 | 0.85 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.211 | 0.80 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.202 | 0.79 |
| Celeste | Shining Wonder | ability | 0.170 | 0.189 | 0.78 |
| Mo & Krill | Scorn | ability | 0.214 | 0.213 | 0.81 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.326 | 0.87 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.316 | 0.87 |
| Drifter | Rend | ability | 0.228 | 0.241 | 0.85 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.321 | 0.89 |
| Calico | Arctic Blast | item | 0.079 | 0.092 | 0.67 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1890 | 0.138 | 0.139 | 1.00 |
| Mystic Burst | 1692 | 0.050 | 0.046 | 1.09 |
| Quicksilver Reload | 1114 | 0.037 | 0.035 | 1.04 |
| Toxic Bullets | 875 | 0.113 | 0.105 | 1.07 |
| Spirit Snatch | 857 | 0.065 | 0.065 | 0.99 |
| Torment Pulse | 814 | 0.154 | 0.152 | 1.01 |
| Stalker | 794 | 0.051 | 0.051 | 0.98 |
| Spirit Strike | 711 | 0.046 | 0.049 | 0.94 |
| Ricochet | 700 | 0.050 | 0.066 | 0.75 |
| Spirit Burn | 687 | 0.084 | 0.090 | 0.94 |
| Mystic Shot | 673 | 0.062 | 0.061 | 1.01 |
| Escalating Exposure | 610 | 0.110 | 0.116 | 0.94 |
| Express Shot | 558 | 0.121 | 0.106 | 1.15 |
| Cold Front | 525 | 0.057 | 0.061 | 0.93 |
| Siphon Bullets | 521 | 0.086 | 0.100 | 0.86 |
| Tesla Bullets | 509 | 0.139 | 0.133 | 1.05 |
| Melee Charge | 434 | 0.047 | 0.046 | 1.02 |
| Headhunter | 410 | 0.090 | 0.085 | 1.06 |
| Capacitor | 375 | 0.206 | 0.204 | 1.01 |
| Headshot Booster | 375 | 0.044 | 0.042 | 1.05 |
| Mercurial Magnum | 340 | 0.103 | 0.099 | 1.05 |
| Rebuttal | 236 | 0.013 | 0.012 | 1.10 |
| Mystic Reverb | 211 | 0.166 | 0.216 | 0.77 |
| Lucky Shot | 201 | 0.142 | 0.105 | 1.35 |
| Arctic Blast | 172 | 0.141 | 0.144 | 0.98 |
| Split Shot | 170 | 0.090 | 0.083 | 1.09 |
| Crushing Fists | 148 | 0.055 | 0.051 | 1.07 |
| Decay | 135 | 0.173 | 0.188 | 0.92 |
| Phantom Strike | 125 | 0.050 | 0.053 | 0.94 |
| Scourge | 122 | 0.158 | 0.180 | 0.88 |
| Alchemical Fire | 111 | 0.126 | 0.146 | 0.87 |
| Return Fire | 96 | 0.094 | 0.026 | 3.61 |
| Lightning Scroll | 49 | 0.039 | 0.035 | 1.10 |
| Focus Lens | 39 | 0.105 | 0.096 | 1.10 |
| Silence Wave | 33 | 0.046 | 0.054 | 0.86 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Rat King | Return Fire | 41 | 0.101 | 0.026 | 3.90 |
| Nurse Harrow | Ricochet | 135 | 0.025 | 0.047 | 0.54 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.027 | 1.75 |
| Venator | Ricochet | 36 | 0.057 | 0.090 | 0.63 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.029 | 1.56 |
| Venator | Siphon Bullets | 77 | 0.095 | 0.147 | 0.65 |
| Haze | Lucky Shot | 92 | 0.153 | 0.100 | 1.52 |
| Violet | Torment Pulse | 69 | 0.103 | 0.069 | 1.51 |
| Violet | Mystic Burst | 66 | 0.044 | 0.029 | 1.49 |
| Mina | Toxic Bullets | 99 | 0.078 | 0.053 | 1.48 |
| Apollo | Melee Charge | 58 | 0.045 | 0.031 | 1.46 |
| Apollo | Mystic Burst | 66 | 0.052 | 0.036 | 1.45 |
| Wraith | Ricochet | 185 | 0.041 | 0.059 | 0.70 |
| Grey Talon | Mystic Reverb | 22 | 0.155 | 0.215 | 0.72 |
| Bebop | Mystic Reverb | 24 | 0.143 | 0.191 | 0.74 |
| Shiv | Express Shot | 125 | 0.255 | 0.191 | 1.33 |
| Lash | Mystic Burst | 210 | 0.061 | 0.046 | 1.32 |
| Haze | Ricochet | 207 | 0.067 | 0.089 | 0.76 |
| Drifter | Crushing Fists | 25 | 0.049 | 0.038 | 1.31 |
| Bebop | Tesla Bullets | 33 | 0.099 | 0.076 | 1.30 |
| Infernus | Ricochet | 66 | 0.027 | 0.035 | 0.77 |
| Grey Talon | Spirit Burn | 34 | 0.086 | 0.111 | 0.78 |
| Viscous | Mystic Burst | 20 | 0.066 | 0.051 | 1.29 |
| Shiv | Lucky Shot | 45 | 0.143 | 0.112 | 1.28 |
| Mina | Quicksilver Reload | 198 | 0.031 | 0.040 | 0.79 |
| Yamato | Express Shot | 46 | 0.158 | 0.124 | 1.26 |
| Drifter | Spirit Burn | 42 | 0.070 | 0.056 | 1.26 |
| Victor | Escalating Exposure | 102 | 0.133 | 0.165 | 0.81 |
| Vyper | Split Shot | 69 | 0.144 | 0.117 | 1.23 |
| Mo & Krill | Mystic Burst | 174 | 0.072 | 0.059 | 1.23 |
| Mirage | Ricochet | 33 | 0.041 | 0.050 | 0.82 |
| Deadman Danny | Toxic Bullets | 144 | 0.099 | 0.082 | 1.22 |
| Apollo | Tankbuster | 47 | 0.148 | 0.123 | 1.20 |
| Paige | Express Shot | 32 | 0.157 | 0.131 | 1.20 |
| Paradox | Spirit Burn | 38 | 0.072 | 0.087 | 0.83 |
| Pocket | Spirit Burn | 95 | 0.082 | 0.098 | 0.84 |
| Graves | Toxic Bullets | 122 | 0.120 | 0.101 | 1.20 |
| Violet | Tankbuster | 207 | 0.144 | 0.121 | 1.19 |
| Vindicta | Mystic Burst | 25 | 0.037 | 0.043 | 0.85 |
| Drifter | Mystic Burst | 96 | 0.041 | 0.035 | 1.17 |
