# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix). Per fifth = the same distance in each fifth of the match (real vs the duels there), and its real-damage-weighted mean: the whole-match distance lets a fifth where the sim is over offset one where it is under.

Players-weighted mean distance 0.0183, per fifth 0.0322.

| Hero | n | gun real / sim | abilities | items | melee | distance | per fifth (mean) |
|---|---|---|---|---|---|---|---|
| Yamato | 131 | 0.24 / 0.26 | 0.38 / 0.43 | 0.17 / 0.17 | 0.18 / 0.13 | 0.07 | 0.04 0.07 0.09 0.08 0.07 (0.072) |
| Warden | 33 | 0.52 / 0.47 | 0.31 / 0.37 | 0.11 / 0.12 | 0.03 / 0.03 | 0.07 | 0.10 0.12 0.02 0.08 0.10 (0.085) |
| Solomon | 136 | 0.25 / 0.19 | 0.64 / 0.71 | 0.08 / 0.07 | 0.02 / 0.01 | 0.07 | 0.11 0.15 0.09 0.05 0.03 (0.067) |
| Ivy | 116 | 0.32 / 0.34 | 0.36 / 0.33 | 0.26 / 0.27 | 0.04 / 0.04 | 0.03 | 0.04 0.05 0.07 0.03 0.03 (0.040) |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.51 | 0.17 / 0.16 | 0.02 / 0.03 | 0.03 | 0.02 0.13 0.03 0.07 0.09 (0.073) |
| Baba | 146 | 0.07 / 0.06 | 0.54 / 0.56 | 0.25 / 0.24 | 0.12 / 0.13 | 0.03 | 0.09 0.03 0.02 0.04 0.04 (0.038) |
| Calico | 110 | 0.13 / 0.12 | 0.38 / 0.40 | 0.31 / 0.32 | 0.15 / 0.15 | 0.03 | 0.05 0.02 0.03 0.03 0.05 (0.037) |
| McGinnis | 49 | 0.20 / 0.18 | 0.64 / 0.67 | 0.12 / 0.11 | 0.02 / 0.02 | 0.03 | 0.04 0.06 0.03 0.03 0.06 (0.045) |
| Nurse Harrow | 347 | 0.29 / 0.30 | 0.61 / 0.59 | 0.06 / 0.07 | 0.03 / 0.03 | 0.03 | 0.09 0.02 0.09 0.05 0.03 (0.052) |
| Drifter | 186 | 0.26 / 0.27 | 0.44 / 0.45 | 0.17 / 0.17 | 0.11 / 0.10 | 0.02 | 0.06 0.05 0.04 0.03 0.04 (0.040) |
| Abrams | 138 | 0.23 / 0.23 | 0.20 / 0.21 | 0.13 / 0.13 | 0.42 / 0.41 | 0.02 | 0.11 0.02 0.03 0.03 0.04 (0.039) |
| Viscous | 29 | 0.13 / 0.15 | 0.51 / 0.51 | 0.28 / 0.28 | 0.05 / 0.05 | 0.02 | 0.03 0.04 0.08 0.02 0.02 (0.034) |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.52 | 0.17 / 0.16 | 0.17 / 0.19 | 0.02 | 0.12 0.06 0.04 0.03 0.04 (0.048) |
| Silver | 100 | 0.41 / 0.39 | 0.37 / 0.37 | 0.10 / 0.12 | 0.10 / 0.10 | 0.02 | 0.06 0.04 0.02 0.02 0.05 (0.035) |
| Rem | 57 | 0.20 / 0.20 | 0.58 / 0.59 | 0.16 / 0.14 | 0.05 / 0.05 | 0.02 | 0.07 0.01 0.05 0.02 0.05 (0.039) |
| The Doorman | 38 | 0.16 / 0.18 | 0.62 / 0.61 | 0.17 / 0.16 | 0.03 / 0.04 | 0.02 | 0.09 0.03 0.02 0.01 0.03 (0.032) |
| Seven | 95 | 0.20 / 0.18 | 0.67 / 0.69 | 0.10 / 0.10 | 0.02 / 0.02 | 0.02 | 0.07 0.01 0.02 0.05 0.03 (0.036) |
| Pocket | 117 | 0.14 / 0.14 | 0.66 / 0.65 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 | 0.04 0.01 0.01 0.02 0.04 (0.025) |
| Bebop | 254 | 0.18 / 0.17 | 0.56 / 0.57 | 0.19 / 0.20 | 0.05 / 0.05 | 0.02 | 0.06 0.03 0.01 0.03 0.04 (0.031) |
| Grey Talon | 103 | 0.31 / 0.31 | 0.49 / 0.50 | 0.16 / 0.17 | 0.01 / 0.01 | 0.02 | 0.09 0.02 0.03 0.01 0.07 (0.043) |
| Celeste | 77 | 0.16 / 0.16 | 0.61 / 0.60 | 0.17 / 0.18 | 0.04 / 0.04 | 0.02 | 0.05 0.03 0.02 0.02 0.03 (0.025) |
| Vindicta | 131 | 0.44 / 0.43 | 0.49 / 0.51 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 | 0.13 0.03 0.03 0.04 0.06 (0.048) |
| Haze | 324 | 0.35 / 0.36 | 0.50 / 0.51 | 0.12 / 0.11 | 0.02 / 0.01 | 0.02 | 0.04 0.07 0.03 0.03 0.02 (0.030) |
| Kelvin | 80 | 0.08 / 0.08 | 0.70 / 0.71 | 0.17 / 0.16 | 0.03 / 0.03 | 0.01 | 0.10 0.07 0.02 0.01 0.01 (0.026) |
| Holliday | 73 | 0.27 / 0.27 | 0.54 / 0.54 | 0.13 / 0.14 | 0.05 / 0.04 | 0.01 | 0.06 0.03 0.04 0.01 0.04 (0.034) |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.61 | 0.13 / 0.12 | 0.03 / 0.03 | 0.01 | 0.02 0.04 0.01 0.03 0.03 (0.027) |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.25 | 0.01 / 0.01 | 0.01 | 0.03 0.03 0.02 0.01 0.02 (0.018) |
| Vyper | 78 | 0.46 / 0.46 | 0.26 / 0.26 | 0.25 / 0.25 | 0.02 / 0.01 | 0.01 | 0.19 0.05 0.04 0.01 0.04 (0.044) |
| Sinclair | 55 | 0.12 / 0.13 | 0.79 / 0.78 | 0.04 / 0.04 | 0.03 / 0.04 | 0.01 | 0.03 0.04 0.04 0.02 0.01 (0.027) |
| Venator | 257 | 0.38 / 0.37 | 0.50 / 0.51 | 0.03 / 0.04 | 0.07 / 0.07 | 0.01 | 0.06 0.06 0.01 0.01 0.03 (0.025) |
| Mo & Krill | 176 | 0.07 / 0.09 | 0.47 / 0.47 | 0.39 / 0.39 | 0.05 / 0.04 | 0.01 | 0.07 0.05 0.03 0.02 0.03 (0.033) |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.57 | 0.25 / 0.25 | 0.03 / 0.03 | 0.01 | 0.05 0.02 0.01 0.01 0.03 (0.021) |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.50 | 0.27 / 0.28 | 0.02 / 0.02 | 0.01 | 0.04 0.01 0.01 0.01 0.03 (0.019) |
| Lady Geist | 37 | 0.29 / 0.29 | 0.62 / 0.63 | 0.05 / 0.05 | 0.03 / 0.02 | 0.01 | 0.06 0.04 0.01 0.02 0.01 (0.020) |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.63 | 0.08 / 0.08 | 0.05 / 0.04 | 0.01 | 0.07 0.04 0.02 0.01 0.03 (0.030) |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.15 | 0.22 / 0.22 | 0.01 | 0.05 0.06 0.03 0.03 0.01 (0.030) |
| Violet | 376 | 0.19 / 0.19 | 0.67 / 0.68 | 0.10 / 0.10 | 0.02 / 0.02 | 0.01 | 0.02 0.01 0.01 0.01 0.02 (0.015) |
| Shiv | 209 | 0.27 / 0.27 | 0.48 / 0.49 | 0.16 / 0.15 | 0.08 / 0.08 | 0.01 | 0.03 0.02 0.02 0.04 0.01 (0.023) |
| Deadman Danny | 357 | 0.16 / 0.16 | 0.63 / 0.64 | 0.18 / 0.18 | 0.01 / 0.01 | 0.01 | 0.07 0.06 0.01 0.03 0.03 (0.034) |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.57 | 0.03 / 0.03 | 0.05 / 0.06 | 0.01 | 0.06 0.04 0.02 0.01 0.01 (0.018) |
| Paradox | 168 | 0.24 / 0.25 | 0.48 / 0.48 | 0.23 / 0.23 | 0.03 / 0.03 | 0.01 | 0.09 0.01 0.05 0.03 0.02 (0.032) |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.19 | 0.01 / 0.01 | 0.01 | 0.06 0.02 0.01 0.01 0.01 (0.015) |
| Victor | 129 | 0.15 / 0.16 | 0.64 / 0.64 | 0.16 / 0.16 | 0.03 / 0.03 | 0.01 | 0.08 0.03 0.02 0.01 0.02 (0.021) |
| Paige | 135 | 0.29 / 0.29 | 0.59 / 0.59 | 0.07 / 0.07 | 0.03 / 0.03 | 0.00 | 0.10 0.05 0.03 0.01 0.04 (0.040) |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Solomon | Setup Bishop | ability | 0.307 | 0.429 | 0.54 |
| Nurse Harrow | Lurking Terrors | ability | 0.300 | 0.169 | 1.86 |
| Mo & Krill | Tankbuster | item | 0.061 | 0.012 | 6.12 |
| Nurse Harrow | Leech Therapy | ability | 0.312 | 0.422 | 0.77 |
| Yamato | Power Slash | ability | 0.129 | 0.221 | 0.62 |
| Violet | Abstract Landscape | ability | 0.174 | 0.107 | 1.60 |
| Yamato | MELEE | melee | 0.184 | 0.126 | 1.55 |
| Sinclair | Audience Participation | ability | 0.205 | 0.158 | 1.35 |
| Warden | Last Stand | ability | 0.138 | 0.176 | 0.71 |
| The Doorman | Call Bell | ability | 0.474 | 0.458 | 1.13 |
| Viscous | Goo Ball | ability | 0.107 | 0.072 | 1.67 |
| Baba | Baba's Brew | ability | 0.071 | 0.106 | 0.60 |
| Violet | Flow State | ability | 0.066 | 0.105 | 0.61 |
| Warden | Alchemical Flask | ability | 0.129 | 0.158 | 0.74 |
| Violet | Living Ink | ability | 0.261 | 0.300 | 0.86 |
| Seven | Lightning Ball | ability | 0.198 | 0.220 | 0.82 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.164 | 0.77 |
| Mo & Krill | Scorn | ability | 0.214 | 0.208 | 1.21 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.319 | 0.89 |
| Lash | Ground Strike | ability | 0.350 | 0.339 | 1.11 |
| Ivy | Entangling Thorns | ability | 0.199 | 0.183 | 1.18 |
| Deadman Danny | Chimera Mk1 | ability | 0.202 | 0.228 | 0.87 |
| Graves | Borrowed Decree | ability | 0.195 | 0.216 | 0.86 |
| Yamato | Crimson Slash | ability | 0.113 | 0.091 | 1.32 |
| McGinnis | Mini Turret | ability | 0.467 | 0.462 | 0.94 |
| Solomon | Develop Queen | ability | 0.161 | 0.146 | 0.83 |
| Seven | Storm Cloud | ability | 0.202 | 0.212 | 0.87 |
| Yamato | Flying Slash | ability | 0.138 | 0.119 | 1.23 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.292 | 0.91 |
| Calico | Gloom Bombs | ability | 0.182 | 0.188 | 0.86 |
| Rat King | Scrap Grenade | ability | 0.361 | 0.338 | 1.08 |
| Mirage | Dust Devil | ability | 0.079 | 0.100 | 0.77 |
| Drifter | MELEE | melee | 0.114 | 0.095 | 1.25 |
| Mo & Krill | Burrow | ability | 0.150 | 0.149 | 1.18 |
| Baba | MELEE | melee | 0.124 | 0.133 | 0.83 |
| Apollo | MELEE | melee | 0.171 | 0.194 | 0.88 |
| Abrams | MELEE | melee | 0.424 | 0.411 | 1.06 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.040 | 1.46 |
| Apollo | Flawless Advance | ability | 0.285 | 0.263 | 1.08 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.156 | 0.88 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1933 | 0.139 | 0.134 | 1.04 |
| Mystic Burst | 1657 | 0.050 | 0.048 | 1.04 |
| Quicksilver Reload | 1100 | 0.037 | 0.038 | 0.97 |
| Toxic Bullets | 888 | 0.113 | 0.109 | 1.03 |
| Spirit Snatch | 863 | 0.065 | 0.066 | 0.98 |
| Torment Pulse | 822 | 0.154 | 0.151 | 1.01 |
| Spirit Burn | 819 | 0.085 | 0.089 | 0.95 |
| Stalker | 795 | 0.051 | 0.050 | 1.01 |
| Ricochet | 747 | 0.050 | 0.048 | 1.04 |
| Escalating Exposure | 694 | 0.109 | 0.108 | 1.00 |
| Mystic Shot | 676 | 0.062 | 0.064 | 0.97 |
| Spirit Strike | 648 | 0.046 | 0.047 | 0.98 |
| Siphon Bullets | 592 | 0.086 | 0.098 | 0.87 |
| Express Shot | 563 | 0.121 | 0.120 | 1.01 |
| Cold Front | 526 | 0.056 | 0.062 | 0.91 |
| Tesla Bullets | 505 | 0.138 | 0.130 | 1.06 |
| Melee Charge | 443 | 0.047 | 0.044 | 1.06 |
| Headhunter | 414 | 0.090 | 0.086 | 1.04 |
| Capacitor | 403 | 0.205 | 0.206 | 1.00 |
| Headshot Booster | 394 | 0.045 | 0.043 | 1.04 |
| Mercurial Magnum | 359 | 0.103 | 0.092 | 1.12 |
| Mystic Reverb | 242 | 0.166 | 0.214 | 0.77 |
| Rebuttal | 238 | 0.013 | 0.014 | 0.97 |
| Lucky Shot | 229 | 0.142 | 0.138 | 1.03 |
| Arctic Blast | 184 | 0.139 | 0.144 | 0.96 |
| Split Shot | 181 | 0.089 | 0.090 | 0.99 |
| Crushing Fists | 170 | 0.055 | 0.051 | 1.09 |
| Scourge | 151 | 0.159 | 0.174 | 0.91 |
| Phantom Strike | 141 | 0.050 | 0.054 | 0.93 |
| Decay | 135 | 0.173 | 0.175 | 0.99 |
| Alchemical Fire | 113 | 0.127 | 0.133 | 0.95 |
| Return Fire | 99 | 0.093 | 0.025 | 3.78 |
| Lightning Scroll | 59 | 0.039 | 0.047 | 0.83 |
| Focus Lens | 45 | 0.105 | 0.104 | 1.01 |
| Silence Wave | 33 | 0.046 | 0.050 | 0.92 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Mo & Krill | Tankbuster | 124 | 0.149 | 0.033 | 4.53 |
| Rat King | Return Fire | 44 | 0.099 | 0.028 | 3.58 |
| Mina | Toxic Bullets | 99 | 0.078 | 0.051 | 1.54 |
| Venator | Siphon Bullets | 86 | 0.096 | 0.143 | 0.67 |
| Drifter | Spirit Burn | 43 | 0.072 | 0.049 | 1.48 |
| Grey Talon | Mystic Reverb | 26 | 0.154 | 0.221 | 0.70 |
| Nurse Harrow | Ricochet | 140 | 0.025 | 0.036 | 0.70 |
| Apollo | Mystic Burst | 65 | 0.052 | 0.036 | 1.42 |
| Mo & Krill | Arctic Blast | 27 | 0.120 | 0.169 | 0.71 |
| Apollo | Melee Charge | 57 | 0.045 | 0.032 | 1.39 |
| Yamato | Crushing Fists | 31 | 0.050 | 0.037 | 1.35 |
| Mirage | Escalating Exposure | 22 | 0.100 | 0.135 | 0.74 |
| Viscous | Mystic Burst | 20 | 0.064 | 0.049 | 1.33 |
| Viscous | Spirit Snatch | 20 | 0.096 | 0.072 | 1.33 |
| Solomon | Spirit Burn | 32 | 0.096 | 0.075 | 1.27 |
| Deadman Danny | Toxic Bullets | 147 | 0.099 | 0.079 | 1.26 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.059 | 0.80 |
| Seven | Toxic Bullets | 30 | 0.063 | 0.050 | 1.24 |
| Lash | Mystic Reverb | 22 | 0.170 | 0.211 | 0.81 |
| Violet | Torment Pulse | 73 | 0.103 | 0.083 | 1.24 |
| Violet | Mystic Burst | 71 | 0.041 | 0.034 | 1.23 |
| Grey Talon | Spirit Burn | 45 | 0.088 | 0.106 | 0.82 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.038 | 1.20 |
| Mirage | Toxic Bullets | 41 | 0.161 | 0.133 | 1.20 |
| Bebop | Mystic Reverb | 30 | 0.146 | 0.175 | 0.83 |
| Paradox | Headshot Booster | 44 | 0.043 | 0.036 | 1.20 |
| Pocket | Spirit Burn | 99 | 0.082 | 0.097 | 0.84 |
| Celeste | Mystic Burst | 33 | 0.037 | 0.044 | 0.85 |
| Solomon | Mystic Burst | 49 | 0.032 | 0.038 | 0.85 |
| Calico | Scourge | 23 | 0.180 | 0.212 | 0.85 |
| Billy | Spirit Strike | 25 | 0.059 | 0.050 | 1.17 |
| Violet | Escalating Exposure | 41 | 0.084 | 0.072 | 1.17 |
| Drifter | Crushing Fists | 29 | 0.048 | 0.042 | 1.16 |
| Nurse Harrow | Toxic Bullets | 85 | 0.152 | 0.176 | 0.87 |
| Lash | Cold Front | 71 | 0.050 | 0.058 | 0.87 |
| Mo & Krill | Phantom Strike | 35 | 0.063 | 0.072 | 0.87 |
| Mo & Krill | Cold Front | 123 | 0.080 | 0.092 | 0.87 |
| Haze | Siphon Bullets | 76 | 0.101 | 0.088 | 1.15 |
| Apollo | Spirit Strike | 24 | 0.030 | 0.034 | 0.87 |
| Rat King | Siphon Bullets | 242 | 0.074 | 0.085 | 0.88 |
