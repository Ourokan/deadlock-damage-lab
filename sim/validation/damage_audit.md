# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Warden | 33 | 0.52 / 0.47 | 0.31 / 0.37 | 0.11 / 0.12 | 0.03 / 0.03 | 0.07 |
| Viscous | 29 | 0.13 / 0.14 | 0.51 / 0.54 | 0.28 / 0.26 | 0.05 / 0.05 | 0.03 |
| Kelvin | 80 | 0.08 / 0.08 | 0.70 / 0.67 | 0.17 / 0.20 | 0.03 / 0.03 | 0.03 |
| Calico | 110 | 0.13 / 0.12 | 0.38 / 0.40 | 0.31 / 0.32 | 0.15 / 0.15 | 0.03 |
| Grey Talon | 103 | 0.31 / 0.29 | 0.49 / 0.50 | 0.16 / 0.18 | 0.01 / 0.01 | 0.03 |
| Yamato | 131 | 0.24 / 0.23 | 0.38 / 0.39 | 0.17 / 0.18 | 0.18 / 0.18 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.50 | 0.17 / 0.16 | 0.02 / 0.03 | 0.03 |
| Billy | 93 | 0.21 / 0.19 | 0.41 / 0.42 | 0.14 / 0.15 | 0.22 / 0.23 | 0.03 |
| Abrams | 138 | 0.23 / 0.21 | 0.20 / 0.20 | 0.13 / 0.13 | 0.42 / 0.44 | 0.03 |
| Paradox | 168 | 0.24 / 0.23 | 0.48 / 0.50 | 0.23 / 0.24 | 0.03 / 0.02 | 0.03 |
| Seven | 95 | 0.20 / 0.19 | 0.66 / 0.68 | 0.10 / 0.10 | 0.02 / 0.02 | 0.02 |
| Victor | 129 | 0.15 / 0.15 | 0.64 / 0.62 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Celeste | 77 | 0.16 / 0.16 | 0.61 / 0.60 | 0.17 / 0.19 | 0.04 / 0.04 | 0.02 |
| Baba | 146 | 0.07 / 0.06 | 0.54 / 0.54 | 0.25 / 0.24 | 0.12 / 0.14 | 0.02 |
| Wraith | 283 | 0.32 / 0.31 | 0.41 / 0.42 | 0.24 / 0.25 | 0.01 / 0.01 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.59 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Pocket | 117 | 0.14 / 0.14 | 0.66 / 0.65 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.59 | 0.16 / 0.14 | 0.05 / 0.05 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.60 | 0.05 / 0.05 | 0.03 / 0.04 | 0.02 |
| Bebop | 254 | 0.18 / 0.17 | 0.56 / 0.57 | 0.19 / 0.20 | 0.05 / 0.05 | 0.02 |
| Vyper | 78 | 0.46 / 0.46 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.02 |
| Silver | 100 | 0.41 / 0.40 | 0.37 / 0.37 | 0.10 / 0.12 | 0.10 / 0.10 | 0.02 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.63 | 0.17 / 0.16 | 0.03 / 0.04 | 0.02 |
| Holliday | 73 | 0.27 / 0.27 | 0.54 / 0.53 | 0.13 / 0.14 | 0.05 / 0.06 | 0.01 |
| Nurse Harrow | 347 | 0.29 / 0.29 | 0.61 / 0.63 | 0.06 / 0.05 | 0.03 / 0.03 | 0.01 |
| Haze | 324 | 0.35 / 0.35 | 0.50 / 0.50 | 0.12 / 0.12 | 0.02 / 0.01 | 0.01 |
| Solomon | 136 | 0.25 / 0.24 | 0.64 / 0.63 | 0.08 / 0.08 | 0.02 / 0.02 | 0.01 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.61 | 0.13 / 0.13 | 0.03 / 0.03 | 0.01 |
| Vindicta | 131 | 0.44 / 0.43 | 0.49 / 0.51 | 0.05 / 0.05 | 0.01 / 0.01 | 0.01 |
| Venator | 257 | 0.38 / 0.37 | 0.50 / 0.50 | 0.03 / 0.04 | 0.07 / 0.08 | 0.01 |
| Ivy | 116 | 0.32 / 0.32 | 0.36 / 0.36 | 0.26 / 0.27 | 0.04 / 0.04 | 0.01 |
| Violet | 376 | 0.19 / 0.19 | 0.67 / 0.68 | 0.10 / 0.09 | 0.02 / 0.02 | 0.01 |
| McGinnis | 49 | 0.20 / 0.19 | 0.64 / 0.65 | 0.12 / 0.12 | 0.02 / 0.02 | 0.01 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.50 | 0.27 / 0.28 | 0.02 / 0.02 | 0.01 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.54 | 0.17 / 0.16 | 0.17 / 0.17 | 0.01 |
| Shiv | 209 | 0.27 / 0.27 | 0.48 / 0.49 | 0.16 / 0.15 | 0.08 / 0.08 | 0.01 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.47 | 0.39 / 0.40 | 0.05 / 0.05 | 0.01 |
| Sinclair | 55 | 0.12 / 0.12 | 0.79 / 0.79 | 0.04 / 0.04 | 0.03 / 0.03 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.19 | 0.01 / 0.01 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.03 | 0.05 / 0.05 | 0.01 |
| Dynamo | 53 | 0.23 / 0.23 | 0.62 / 0.62 | 0.08 / 0.08 | 0.05 / 0.05 | 0.01 |
| Drifter | 186 | 0.26 / 0.26 | 0.44 / 0.44 | 0.17 / 0.17 | 0.11 / 0.11 | 0.01 |
| Deadman Danny | 357 | 0.16 / 0.16 | 0.63 / 0.63 | 0.18 / 0.19 | 0.01 / 0.01 | 0.01 |
| Paige | 135 | 0.29 / 0.29 | 0.59 / 0.59 | 0.07 / 0.07 | 0.03 / 0.03 | 0.00 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| Warden | Last Stand | ability | 0.138 | 0.173 | 0.72 |
| Warden | Alchemical Flask | ability | 0.129 | 0.158 | 0.74 |
| Billy | Bashdown | ability | 0.309 | 0.325 | 0.87 |
| Abrams | MELEE | melee | 0.424 | 0.440 | 0.90 |
| Seven | Storm Cloud | ability | 0.202 | 0.224 | 0.85 |
| Grey Talon | Charged Shot | ability | 0.351 | 0.361 | 0.92 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.325 | 0.91 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.167 | 1.17 |
| Graves | Borrowed Decree | ability | 0.195 | 0.215 | 0.87 |
| Baba | MELEE | melee | 0.124 | 0.140 | 0.82 |
| Billy | MELEE | melee | 0.223 | 0.229 | 0.89 |
| Wraith | Card Trick | ability | 0.280 | 0.296 | 0.91 |
| Bebop | Sticky Bomb | ability | 0.277 | 0.291 | 0.91 |
| Calico | Gloom Bombs | ability | 0.182 | 0.187 | 0.87 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.127 | 0.82 |
| Victor | Shocking Reanimation | ability | 0.058 | 0.039 | 1.50 |
| Mirage | Dust Devil | ability | 0.079 | 0.098 | 0.79 |
| McGinnis | Mini Turret | ability | 0.467 | 0.479 | 0.96 |
| Seven | Lightning Ball | ability | 0.198 | 0.207 | 0.90 |
| Abrams | Siphon Life | ability | 0.107 | 0.119 | 0.84 |
| Venator | Consecrating Grenade | ability | 0.147 | 0.163 | 0.89 |
| Kelvin | Tankbuster | item | 0.026 | 0.040 | 0.62 |
| Haze | Fixation | ability | 0.304 | 0.293 | 1.06 |
| Vindicta | Crow Familiar | ability | 0.155 | 0.172 | 0.90 |
| Vyper | Split Shot | item | 0.110 | 0.094 | 1.18 |
| Calico | Leaping Slash | ability | 0.094 | 0.101 | 0.84 |
| Calico | Return to Shadows | ability | 0.107 | 0.112 | 0.85 |
| Viscous | Spirit Snatch | item | 0.042 | 0.029 | 1.51 |
| Baba | Baba's Brew | ability | 0.071 | 0.080 | 0.82 |
| Celeste | Torment Pulse | item | 0.098 | 0.110 | 0.87 |
| Grey Talon | Tankbuster | item | 0.071 | 0.081 | 0.83 |
| Yamato | Crimson Slash | ability | 0.113 | 0.121 | 0.89 |
| Baba | Threadsap | ability | 0.234 | 0.230 | 0.94 |
| Mirage | Fire Scarabs | ability | 0.112 | 0.121 | 0.90 |
| Venator | citadel_weapon_priest_crossbow | ability | 0.101 | 0.087 | 1.14 |
| Haze | Sleep Dagger | ability | 0.076 | 0.090 | 0.86 |
| Calico | MELEE | melee | 0.149 | 0.146 | 0.92 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.146 | 0.92 |
| Viscous | Tankbuster | item | 0.069 | 0.061 | 1.19 |
| Victor | Escalating Exposure | item | 0.065 | 0.076 | 0.85 |

## Items (holders only, all heroes)

Item damage per all the player's damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|
| Tankbuster | 1933 | 0.139 | 0.142 | 0.97 |
| Mystic Burst | 1657 | 0.050 | 0.046 | 1.07 |
| Quicksilver Reload | 1100 | 0.037 | 0.032 | 1.13 |
| Toxic Bullets | 888 | 0.113 | 0.104 | 1.08 |
| Spirit Snatch | 863 | 0.065 | 0.066 | 0.97 |
| Torment Pulse | 822 | 0.154 | 0.152 | 1.01 |
| Spirit Burn | 819 | 0.085 | 0.092 | 0.92 |
| Stalker | 795 | 0.051 | 0.049 | 1.04 |
| Ricochet | 747 | 0.050 | 0.065 | 0.77 |
| Escalating Exposure | 694 | 0.109 | 0.115 | 0.95 |
| Mystic Shot | 676 | 0.062 | 0.061 | 1.02 |
| Spirit Strike | 648 | 0.046 | 0.046 | 0.98 |
| Siphon Bullets | 592 | 0.086 | 0.098 | 0.87 |
| Express Shot | 563 | 0.121 | 0.119 | 1.02 |
| Cold Front | 526 | 0.056 | 0.059 | 0.95 |
| Tesla Bullets | 505 | 0.138 | 0.128 | 1.07 |
| Melee Charge | 443 | 0.047 | 0.046 | 1.02 |
| Headhunter | 414 | 0.090 | 0.084 | 1.08 |
| Capacitor | 403 | 0.205 | 0.207 | 0.99 |
| Headshot Booster | 394 | 0.045 | 0.042 | 1.08 |
| Mercurial Magnum | 359 | 0.103 | 0.099 | 1.04 |
| Mystic Reverb | 242 | 0.166 | 0.213 | 0.78 |
| Rebuttal | 238 | 0.013 | 0.015 | 0.88 |
| Lucky Shot | 229 | 0.142 | 0.106 | 1.33 |
| Arctic Blast | 184 | 0.139 | 0.141 | 0.98 |
| Split Shot | 181 | 0.089 | 0.081 | 1.10 |
| Crushing Fists | 170 | 0.055 | 0.052 | 1.05 |
| Scourge | 151 | 0.159 | 0.175 | 0.91 |
| Phantom Strike | 141 | 0.050 | 0.053 | 0.94 |
| Decay | 135 | 0.173 | 0.173 | 1.00 |
| Alchemical Fire | 113 | 0.127 | 0.139 | 0.92 |
| Return Fire | 99 | 0.093 | 0.025 | 3.74 |
| Lightning Scroll | 59 | 0.039 | 0.033 | 1.17 |
| Focus Lens | 45 | 0.105 | 0.102 | 1.03 |
| Silence Wave | 33 | 0.046 | 0.051 | 0.91 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per dmg | sim per dmg | real/sim |
|---|---|---|---|---|---|
| Rat King | Return Fire | 44 | 0.099 | 0.027 | 3.65 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.047 | 0.022 | 2.15 |
| Lash | Quicksilver Reload | 154 | 0.046 | 0.029 | 1.61 |
| Venator | Ricochet | 41 | 0.060 | 0.096 | 0.63 |
| Venator | Siphon Bullets | 86 | 0.096 | 0.146 | 0.66 |
| Viscous | Spirit Snatch | 20 | 0.096 | 0.064 | 1.50 |
| Mina | Toxic Bullets | 99 | 0.078 | 0.053 | 1.48 |
| Drifter | Spirit Burn | 43 | 0.072 | 0.049 | 1.47 |
| Haze | Lucky Shot | 99 | 0.154 | 0.105 | 1.47 |
| Infernus | Ricochet | 75 | 0.026 | 0.038 | 0.69 |
| Wraith | Ricochet | 198 | 0.041 | 0.058 | 0.70 |
| Viscous | Mystic Burst | 20 | 0.064 | 0.046 | 1.39 |
| Apollo | Melee Charge | 57 | 0.045 | 0.033 | 1.37 |
| Nurse Harrow | Ricochet | 140 | 0.025 | 0.035 | 0.73 |
| Kelvin | Spirit Burn | 27 | 0.103 | 0.141 | 0.73 |
| Apollo | Mystic Burst | 65 | 0.052 | 0.038 | 1.35 |
| Nurse Harrow | Toxic Bullets | 85 | 0.152 | 0.113 | 1.34 |
| Mirage | Ricochet | 34 | 0.041 | 0.054 | 0.76 |
| Shiv | Lucky Shot | 52 | 0.142 | 0.108 | 1.32 |
| Grey Talon | Spirit Burn | 45 | 0.088 | 0.116 | 0.76 |
| Haze | Ricochet | 214 | 0.067 | 0.089 | 0.76 |
| Grey Talon | Mystic Reverb | 26 | 0.154 | 0.203 | 0.76 |
| Paradox | Headshot Booster | 44 | 0.043 | 0.033 | 1.29 |
| Lash | Mystic Burst | 201 | 0.061 | 0.048 | 1.27 |
| Mirage | Escalating Exposure | 22 | 0.100 | 0.127 | 0.79 |
| Paradox | Spirit Burn | 49 | 0.072 | 0.090 | 0.80 |
| Violet | Torment Pulse | 73 | 0.103 | 0.084 | 1.23 |
| Victor | Escalating Exposure | 105 | 0.134 | 0.164 | 0.81 |
| Violet | Mystic Burst | 71 | 0.041 | 0.034 | 1.22 |
| Lash | Mystic Reverb | 22 | 0.170 | 0.206 | 0.82 |
| Deadman Danny | Toxic Bullets | 147 | 0.099 | 0.082 | 1.21 |
| Bebop | Mystic Reverb | 30 | 0.146 | 0.175 | 0.83 |
| Nurse Harrow | Decay | 41 | 0.220 | 0.183 | 1.20 |
| Pocket | Spirit Burn | 99 | 0.082 | 0.097 | 0.84 |
| Mo & Krill | Escalating Exposure | 27 | 0.108 | 0.091 | 1.18 |
| Vyper | Split Shot | 70 | 0.144 | 0.122 | 1.18 |
| Paradox | Mystic Burst | 70 | 0.050 | 0.043 | 1.17 |
| Mirage | Toxic Bullets | 41 | 0.161 | 0.138 | 1.17 |
| Drifter | Crushing Fists | 29 | 0.048 | 0.041 | 1.16 |
| Mo & Krill | Mystic Burst | 170 | 0.071 | 0.061 | 1.16 |
