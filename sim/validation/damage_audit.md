# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.18 | 0.12 / 0.12 | 0.09 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.73 | 0.12 / 0.09 | 0.02 / 0.00 | 0.09 |
| Warden | 33 | 0.52 / 0.47 | 0.31 / 0.39 | 0.11 / 0.11 | 0.03 / 0.02 | 0.08 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.07 |
| Apollo | 92 | 0.11 / 0.12 | 0.53 / 0.58 | 0.17 / 0.15 | 0.17 / 0.16 | 0.05 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.58 | 0.17 / 0.19 | 0.04 / 0.05 | 0.05 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.47 | 0.17 / 0.14 | 0.11 / 0.11 | 0.04 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.10 | 0.02 / 0.01 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.34 | 0.26 / 0.30 | 0.04 / 0.04 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.52 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Calico | 110 | 0.13 / 0.14 | 0.38 / 0.40 | 0.31 / 0.33 | 0.15 / 0.13 | 0.04 |
| Sinclair | 55 | 0.12 / 0.15 | 0.79 / 0.76 | 0.04 / 0.04 | 0.03 / 0.04 | 0.04 |
| Silver | 100 | 0.41 / 0.39 | 0.37 / 0.39 | 0.10 / 0.12 | 0.10 / 0.10 | 0.04 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.08 | 0.02 / 0.01 | 0.04 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.70 | 0.17 / 0.20 | 0.03 / 0.02 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.47 | 0.17 / 0.20 | 0.02 / 0.02 | 0.03 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.52 | 0.13 / 0.14 | 0.05 / 0.05 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.15 | 0.08 / 0.08 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Lash | 216 | 0.13 / 0.15 | 0.58 / 0.59 | 0.25 / 0.23 | 0.03 / 0.03 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.64 | 0.08 / 0.08 | 0.05 / 0.04 | 0.03 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.20 | 0.05 / 0.06 | 0.03 |
| Paige | 135 | 0.29 / 0.31 | 0.59 / 0.58 | 0.07 / 0.08 | 0.03 / 0.02 | 0.03 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.03 |
| Rem | 57 | 0.20 / 0.22 | 0.58 / 0.59 | 0.16 / 0.16 | 0.05 / 0.04 | 0.03 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.19 | 0.18 / 0.19 | 0.03 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.03 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.02 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.48 | 0.39 / 0.41 | 0.05 / 0.03 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.20 | 0.13 / 0.12 | 0.42 / 0.44 | 0.02 |
| Paradox | 168 | 0.24 / 0.24 | 0.48 / 0.48 | 0.23 / 0.24 | 0.03 / 0.04 | 0.02 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.60 | 0.17 / 0.18 | 0.03 / 0.04 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| Grey Talon | 103 | 0.31 / 0.31 | 0.49 / 0.49 | 0.16 / 0.18 | 0.01 / 0.01 | 0.02 |
| Venator | 257 | 0.48 / 0.50 | 0.40 / 0.40 | 0.03 / 0.02 | 0.07 / 0.08 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.15 | 0.22 / 0.23 | 0.02 |
| Vindicta | 131 | 0.44 / 0.44 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Pocket | 117 | 0.14 / 0.14 | 0.66 / 0.67 | 0.16 / 0.16 | 0.02 / 0.02 | 0.02 |
| Solomon | 136 | 0.25 / 0.26 | 0.64 / 0.63 | 0.08 / 0.08 | 0.02 / 0.02 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.62 | 0.05 / 0.05 | 0.03 / 0.02 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.19 | 0.01 / 0.01 | 0.01 |
| Victor | 129 | 0.15 / 0.16 | 0.64 / 0.64 | 0.16 / 0.16 | 0.03 / 0.03 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| McGinnis | Mini Turret | ability | 0.467 | 0.571 | 0.67 |
| Sinclair | Vexing Bolt | ability | 0.351 | 0.295 | 1.46 |
| Baba | Torment Pulse | item | 0.170 | 0.095 | 2.17 |
| Warden | Last Stand | ability | 0.138 | 0.211 | 0.59 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.090 | 1.59 |
| Celeste | Shining Wonder | ability | 0.170 | 0.145 | 1.37 |
| Pocket | Affliction | ability | 0.120 | 0.160 | 0.73 |
| Viscous | Express Shot | item | 0.052 | 0.024 | 2.61 |
| Viscous | Splatter | ability | 0.285 | 0.295 | 1.17 |
| Viscous | Goo Ball | ability | 0.107 | 0.085 | 1.53 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.275 | 1.15 |
| Shiv | Killing Blow | ability | 0.056 | 0.030 | 2.03 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.192 | 1.23 |
| Paige | Bookwyrm | ability | 0.376 | 0.362 | 1.11 |
| Viscous | MELEE | melee | 0.047 | 0.087 | 0.65 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.175 | 1.23 |
| The Doorman | Call Bell | ability | 0.474 | 0.462 | 1.08 |
| Viscous | Puddle Punch | ability | 0.123 | 0.111 | 1.35 |
| Haze | Bullet Dance | ability | 0.124 | 0.152 | 0.79 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.229 | 0.86 |
| Mina | Nox Nostra | ability | 0.128 | 0.155 | 0.81 |
| Holliday | Powder Keg | ability | 0.397 | 0.385 | 1.08 |
| Baba | MELEE | melee | 0.124 | 0.116 | 1.28 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.138 | 0.80 |
| Apollo | MELEE | melee | 0.171 | 0.156 | 1.18 |
| Lash | Ground Strike | ability | 0.350 | 0.356 | 1.08 |
| Silver | ability_werewolf_frenzy | ability | 0.096 | 0.116 | 0.78 |
| Solomon | Develop Queen | ability | 0.161 | 0.141 | 1.19 |
| Haze | Fixation | ability | 0.304 | 0.322 | 0.92 |
| Graves | Jar of Dead | ability | 0.212 | 0.230 | 0.89 |
| Vyper | Split Shot | item | 0.110 | 0.090 | 1.25 |
| Kelvin | MELEE | melee | 0.034 | 0.018 | 2.07 |
| Victor | Pain Battery | ability | 0.276 | 0.262 | 1.09 |
| Warden | Alchemical Flask | ability | 0.129 | 0.139 | 0.84 |
| Calico | MELEE | melee | 0.149 | 0.130 | 1.17 |
| Celeste | Light Eater | ability | 0.220 | 0.234 | 1.10 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.320 | 0.93 |
| Pocket | Barrage | ability | 0.260 | 0.233 | 1.09 |
| Shiv | Slice and Dice | ability | 0.145 | 0.136 | 1.16 |
| Baba | Granny Long Legs | ability | 0.103 | 0.102 | 1.23 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1890 | 0.138 | 0.132 | 1.05 |
| Mystic Burst | 1692 | 0.050 | 0.044 | 1.14 |
| Quicksilver Reload | 1114 | 0.037 | 0.030 | 1.23 |
| Toxic Bullets | 875 | 0.113 | 0.117 | 0.96 |
| Spirit Snatch | 857 | 0.065 | 0.066 | 0.98 |
| Torment Pulse | 814 | 0.154 | 0.133 | 1.16 |
| Stalker | 794 | 0.051 | 0.048 | 1.05 |
| Spirit Strike | 711 | 0.046 | 0.047 | 0.98 |
| Ricochet | 700 | 0.050 | 0.058 | 0.86 |
| Spirit Burn | 687 | 0.084 | 0.077 | 1.09 |
| Mystic Shot | 673 | 0.062 | 0.059 | 1.05 |
| Escalating Exposure | 610 | 0.110 | 0.110 | 1.00 |
| Express Shot | 558 | 0.121 | 0.107 | 1.13 |
| Cold Front | 525 | 0.057 | 0.058 | 0.97 |
| Siphon Bullets | 521 | 0.086 | 0.085 | 1.00 |
| Tesla Bullets | 509 | 0.139 | 0.134 | 1.04 |
| Melee Charge | 434 | 0.047 | 0.029 | 1.64 |
| Headhunter | 410 | 0.090 | 0.090 | 1.00 |
| Capacitor | 375 | 0.206 | 0.198 | 1.04 |
| Headshot Booster | 375 | 0.044 | 0.038 | 1.18 |
| Mercurial Magnum | 340 | 0.103 | 0.096 | 1.08 |
| Rebuttal | 236 | 0.013 | 0.012 | 1.05 |
| Mystic Reverb | 211 | 0.166 | 0.203 | 0.81 |
| Lucky Shot | 201 | 0.142 | 0.080 | 1.77 |
| Arctic Blast | 172 | 0.141 | 0.103 | 1.36 |
| Split Shot | 170 | 0.090 | 0.088 | 1.02 |
| Crushing Fists | 148 | 0.055 | 0.031 | 1.78 |
| Decay | 135 | 0.173 | 0.208 | 0.83 |
| Phantom Strike | 125 | 0.050 | 0.043 | 1.16 |
| Scourge | 122 | 0.158 | 0.162 | 0.98 |
| Alchemical Fire | 111 | 0.126 | 0.154 | 0.82 |
| Return Fire | 96 | 0.094 | 0.029 | 3.30 |
| Lightning Scroll | 49 | 0.039 | 0.032 | 1.23 |
| Focus Lens | 39 | 0.105 | 0.099 | 1.06 |
| Silence Wave | 33 | 0.046 | 0.048 | 0.97 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Apollo | Melee Charge | 58 | 0.045 | 0.010 | 4.37 |
| Rat King | Return Fire | 41 | 0.101 | 0.027 | 3.74 |
| Drifter | Crushing Fists | 25 | 0.049 | 0.013 | 3.64 |
| Drifter | Melee Charge | 68 | 0.035 | 0.011 | 3.14 |
| Haze | Lucky Shot | 92 | 0.153 | 0.062 | 2.47 |
| Billy | Crushing Fists | 31 | 0.050 | 0.021 | 2.42 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.022 | 2.18 |
| Nurse Harrow | Ricochet | 135 | 0.025 | 0.052 | 0.49 |
| Yamato | Crushing Fists | 30 | 0.050 | 0.026 | 1.88 |
| Baba | Torment Pulse | 138 | 0.249 | 0.134 | 1.86 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.025 | 1.82 |
| Violet | Torment Pulse | 69 | 0.103 | 0.058 | 1.78 |
| Billy | Melee Charge | 48 | 0.044 | 0.025 | 1.73 |
| Violet | Mystic Burst | 66 | 0.044 | 0.027 | 1.64 |
| Drifter | Tankbuster | 101 | 0.108 | 0.070 | 1.53 |
| Apollo | Mystic Burst | 66 | 0.052 | 0.034 | 1.51 |
| Wraith | Ricochet | 185 | 0.041 | 0.062 | 0.67 |
| Infernus | Ricochet | 66 | 0.027 | 0.039 | 0.68 |
| Drifter | Mystic Burst | 96 | 0.041 | 0.028 | 1.47 |
| Calico | Arctic Blast | 102 | 0.155 | 0.109 | 1.42 |
| Shiv | Express Shot | 125 | 0.255 | 0.181 | 1.41 |
| Drifter | Spirit Burn | 42 | 0.070 | 0.051 | 1.39 |
| Haze | Tesla Bullets | 47 | 0.129 | 0.094 | 1.37 |
| Paradox | Headshot Booster | 42 | 0.042 | 0.031 | 1.36 |
| Shiv | Lucky Shot | 45 | 0.143 | 0.109 | 1.31 |
| Lash | Mystic Burst | 210 | 0.061 | 0.047 | 1.31 |
| Venator | Ricochet | 36 | 0.057 | 0.074 | 0.77 |
| Abrams | Phantom Strike | 58 | 0.046 | 0.035 | 1.30 |
| Mina | Spirit Burn | 110 | 0.091 | 0.071 | 1.29 |
| Violet | Tankbuster | 207 | 0.144 | 0.112 | 1.29 |
| Yamato | Express Shot | 46 | 0.158 | 0.124 | 1.27 |
| Vyper | Split Shot | 69 | 0.144 | 0.116 | 1.24 |
| Mirage | Ricochet | 33 | 0.041 | 0.051 | 0.81 |
| Abrams | Melee Charge | 129 | 0.068 | 0.054 | 1.24 |
| Violet | Mystic Shot | 170 | 0.073 | 0.059 | 1.23 |
| Holliday | Headshot Booster | 31 | 0.040 | 0.033 | 1.22 |
| Mo & Krill | Mystic Burst | 174 | 0.072 | 0.061 | 1.19 |
| Bebop | Mystic Reverb | 24 | 0.143 | 0.169 | 0.84 |
| Mo & Krill | Quicksilver Reload | 150 | 0.058 | 0.049 | 1.18 |
| Lash | Spirit Burn | 69 | 0.082 | 0.069 | 1.18 |
