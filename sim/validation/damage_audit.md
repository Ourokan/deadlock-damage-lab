# Sim vs real damage mix audit

Sample: 600 matches, 6575 player-matches (phantom_sample.jsonl.gz). Model: hero_default_skill(badge=91, counterplay=True) with each player's real aim. Duels: 3 per player-match, 20 s max, real builds both sides, real nearby enemies (extra_targets).

## Heroes by how far the damage mix is off

Shares of damage to enemy heroes. Distance = half the summed absolute share gaps (0 = same mix).

| Hero | n | gun real / sim | abilities | items | melee | distance |
|---|---|---|---|---|---|---|
| Warden | 33 | 0.52 / 0.47 | 0.31 / 0.40 | 0.11 / 0.10 | 0.03 / 0.02 | 0.09 |
| Baba | 146 | 0.07 / 0.08 | 0.54 / 0.61 | 0.25 / 0.19 | 0.12 / 0.12 | 0.09 |
| McGinnis | 49 | 0.20 / 0.16 | 0.64 / 0.72 | 0.12 / 0.10 | 0.02 / 0.00 | 0.08 |
| Viscous | 29 | 0.13 / 0.16 | 0.51 / 0.49 | 0.28 / 0.25 | 0.05 / 0.09 | 0.07 |
| Celeste | 77 | 0.16 / 0.18 | 0.61 / 0.56 | 0.17 / 0.21 | 0.04 / 0.04 | 0.07 |
| Paradox | 168 | 0.24 / 0.28 | 0.48 / 0.43 | 0.23 / 0.23 | 0.03 / 0.05 | 0.06 |
| Apollo | 92 | 0.11 / 0.11 | 0.53 / 0.58 | 0.17 / 0.15 | 0.17 / 0.15 | 0.05 |
| Haze | 324 | 0.35 / 0.34 | 0.50 / 0.55 | 0.12 / 0.09 | 0.02 / 0.01 | 0.05 |
| Drifter | 186 | 0.26 / 0.28 | 0.44 / 0.46 | 0.17 / 0.15 | 0.11 / 0.11 | 0.04 |
| Calico | 110 | 0.13 / 0.13 | 0.38 / 0.39 | 0.31 / 0.34 | 0.15 / 0.13 | 0.04 |
| Grey Talon | 103 | 0.31 / 0.30 | 0.49 / 0.48 | 0.16 / 0.20 | 0.01 / 0.01 | 0.04 |
| Mo & Krill | 176 | 0.07 / 0.07 | 0.47 / 0.46 | 0.39 / 0.43 | 0.05 / 0.03 | 0.04 |
| Graves | 151 | 0.20 / 0.19 | 0.50 / 0.53 | 0.27 / 0.28 | 0.02 / 0.00 | 0.04 |
| Kelvin | 80 | 0.08 / 0.09 | 0.70 / 0.69 | 0.17 / 0.20 | 0.03 / 0.02 | 0.04 |
| Sinclair | 55 | 0.12 / 0.15 | 0.79 / 0.76 | 0.04 / 0.04 | 0.03 / 0.04 | 0.04 |
| Holliday | 73 | 0.27 / 0.28 | 0.54 / 0.51 | 0.13 / 0.15 | 0.05 / 0.05 | 0.04 |
| Silver | 100 | 0.41 / 0.39 | 0.37 / 0.38 | 0.10 / 0.12 | 0.10 / 0.11 | 0.04 |
| Violet | 376 | 0.19 / 0.20 | 0.67 / 0.70 | 0.10 / 0.08 | 0.02 / 0.01 | 0.04 |
| Ivy | 116 | 0.32 / 0.31 | 0.36 / 0.35 | 0.26 / 0.29 | 0.04 / 0.04 | 0.03 |
| Mirage | 45 | 0.31 / 0.30 | 0.48 / 0.47 | 0.17 / 0.20 | 0.02 / 0.02 | 0.03 |
| Seven | 95 | 0.20 / 0.20 | 0.66 / 0.69 | 0.10 / 0.09 | 0.02 / 0.01 | 0.03 |
| Shiv | 209 | 0.27 / 0.29 | 0.48 / 0.47 | 0.16 / 0.16 | 0.08 / 0.08 | 0.03 |
| Yamato | 131 | 0.24 / 0.24 | 0.38 / 0.38 | 0.17 / 0.19 | 0.18 / 0.19 | 0.03 |
| Vyper | 78 | 0.46 / 0.47 | 0.26 / 0.28 | 0.25 / 0.24 | 0.02 / 0.01 | 0.03 |
| Paige | 135 | 0.29 / 0.31 | 0.59 / 0.58 | 0.07 / 0.08 | 0.03 / 0.02 | 0.03 |
| Deadman Danny | 357 | 0.16 / 0.15 | 0.63 / 0.63 | 0.18 / 0.20 | 0.01 / 0.01 | 0.03 |
| Wraith | 283 | 0.32 / 0.33 | 0.41 / 0.40 | 0.24 / 0.26 | 0.01 / 0.01 | 0.03 |
| Dynamo | 53 | 0.23 / 0.24 | 0.62 / 0.63 | 0.08 / 0.08 | 0.05 / 0.04 | 0.03 |
| Infernus | 173 | 0.23 / 0.23 | 0.60 / 0.59 | 0.13 / 0.15 | 0.03 / 0.02 | 0.02 |
| Rem | 57 | 0.20 / 0.21 | 0.58 / 0.59 | 0.16 / 0.16 | 0.05 / 0.04 | 0.02 |
| Bebop | 254 | 0.18 / 0.18 | 0.56 / 0.56 | 0.19 / 0.20 | 0.05 / 0.06 | 0.02 |
| Victor | 129 | 0.15 / 0.16 | 0.64 / 0.62 | 0.16 / 0.18 | 0.03 / 0.03 | 0.02 |
| Nurse Harrow | 347 | 0.29 / 0.28 | 0.61 / 0.62 | 0.06 / 0.07 | 0.03 / 0.03 | 0.02 |
| The Doorman | 38 | 0.16 / 0.17 | 0.62 / 0.60 | 0.17 / 0.18 | 0.03 / 0.04 | 0.02 |
| Abrams | 138 | 0.23 / 0.24 | 0.20 / 0.20 | 0.13 / 0.13 | 0.42 / 0.43 | 0.02 |
| Lash | 216 | 0.13 / 0.14 | 0.58 / 0.58 | 0.25 / 0.24 | 0.03 / 0.03 | 0.02 |
| Billy | 93 | 0.21 / 0.20 | 0.41 / 0.41 | 0.14 / 0.16 | 0.22 / 0.23 | 0.02 |
| Pocket | 117 | 0.14 / 0.13 | 0.66 / 0.66 | 0.16 / 0.18 | 0.02 / 0.02 | 0.02 |
| Venator | 257 | 0.48 / 0.50 | 0.40 / 0.40 | 0.03 / 0.02 | 0.07 / 0.08 | 0.02 |
| Vindicta | 131 | 0.44 / 0.44 | 0.49 / 0.50 | 0.05 / 0.05 | 0.01 / 0.01 | 0.02 |
| Solomon | 136 | 0.25 / 0.26 | 0.64 / 0.63 | 0.08 / 0.08 | 0.02 / 0.02 | 0.02 |
| Lady Geist | 37 | 0.29 / 0.30 | 0.62 / 0.62 | 0.05 / 0.04 | 0.03 / 0.02 | 0.01 |
| Mina | 198 | 0.12 / 0.12 | 0.66 / 0.67 | 0.19 / 0.20 | 0.01 / 0.01 | 0.01 |
| Rat King | 424 | 0.33 / 0.33 | 0.57 / 0.58 | 0.03 / 0.02 | 0.05 / 0.05 | 0.01 |

## Sources furthest off (share of hero damage at least 3% in real or sim)

real/sim = (real source dmg / real gun dmg) / (sim source dmg / sim gun dmg). Below 1 = the sim overrates the source against the gun.

| Hero | Source | kind | real share | sim share | real/sim |
|---|---|---|---|---|---|
| McGinnis | Mini Turret | ability | 0.467 | 0.567 | 0.66 |
| Sinclair | Vexing Bolt | ability | 0.351 | 0.295 | 1.47 |
| Baba | Torment Pulse | item | 0.170 | 0.094 | 2.17 |
| Warden | Last Stand | ability | 0.138 | 0.215 | 0.58 |
| Lady Geist | Soul Exchange | ability | 0.139 | 0.084 | 1.71 |
| Paradox | Kinetic Carbine | ability | 0.318 | 0.301 | 1.23 |
| Celeste | Shining Wonder | ability | 0.170 | 0.141 | 1.37 |
| Mo & Krill | Torment Pulse | item | 0.138 | 0.176 | 0.75 |
| Viscous | Express Shot | item | 0.052 | 0.024 | 2.66 |
| Pocket | Affliction | ability | 0.120 | 0.158 | 0.73 |
| Viscous | Splatter | ability | 0.285 | 0.296 | 1.17 |
| Viscous | Goo Ball | ability | 0.107 | 0.085 | 1.53 |
| Kelvin | Frost Grenade | ability | 0.297 | 0.273 | 1.15 |
| Sinclair | Spectral Assistant | ability | 0.191 | 0.192 | 1.23 |
| Paige | Bookwyrm | ability | 0.376 | 0.362 | 1.11 |
| Lady Geist | Essence Bomb | ability | 0.190 | 0.232 | 0.85 |
| Viscous | MELEE | melee | 0.047 | 0.088 | 0.65 |
| Paradox | Tankbuster | item | 0.074 | 0.052 | 1.66 |
| Celeste | Radiant Daggers | ability | 0.184 | 0.170 | 1.22 |
| Viscous | Puddle Punch | ability | 0.123 | 0.111 | 1.35 |
| Paradox | Pulse Grenade | ability | 0.112 | 0.093 | 1.39 |
| Haze | Bullet Dance | ability | 0.124 | 0.153 | 0.79 |
| Holliday | Powder Keg | ability | 0.397 | 0.382 | 1.09 |
| Mina | Nox Nostra | ability | 0.128 | 0.154 | 0.81 |
| Shiv | Killing Blow | ability | 0.056 | 0.034 | 1.78 |
| McGinnis | Heavy Barrage | ability | 0.136 | 0.138 | 0.80 |
| The Doorman | Call Bell | ability | 0.474 | 0.463 | 1.07 |
| Baba | MELEE | melee | 0.124 | 0.115 | 1.28 |
| Lash | Ground Strike | ability | 0.350 | 0.352 | 1.08 |
| Apollo | MELEE | melee | 0.171 | 0.153 | 1.18 |
| Haze | Fixation | ability | 0.304 | 0.324 | 0.92 |
| Graves | Jar of Dead | ability | 0.212 | 0.233 | 0.89 |
| Solomon | Develop Queen | ability | 0.161 | 0.141 | 1.18 |
| Silver | ability_werewolf_frenzy | ability | 0.096 | 0.113 | 0.80 |
| Kelvin | MELEE | melee | 0.034 | 0.017 | 2.06 |
| Lady Geist | Malice | ability | 0.144 | 0.172 | 0.87 |
| Paradox | Paradoxical Swap | ability | 0.053 | 0.039 | 1.57 |
| Victor | Pain Battery | ability | 0.276 | 0.257 | 1.09 |
| Warden | Alchemical Flask | ability | 0.129 | 0.140 | 0.84 |
| Vyper | Split Shot | item | 0.110 | 0.090 | 1.24 |

## Items (holders only, all heroes)

Item damage per gun damage while the item was owned (players who had it at a sampled point). real/sim below 1 = the sim overrates the item; above 1 is partly team fights (several heroes hit).

| Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|
| Tankbuster | 1887 | 1.093 | 0.838 | 1.30 |
| Mystic Burst | 1691 | 0.292 | 0.240 | 1.22 |
| Quicksilver Reload | 1114 | 0.171 | 0.141 | 1.22 |
| Toxic Bullets | 875 | 0.530 | 0.526 | 1.01 |
| Spirit Snatch | 856 | 0.411 | 0.412 | 1.00 |
| Torment Pulse | 814 | 1.625 | 1.286 | 1.26 |
| Stalker | 794 | 0.219 | 0.195 | 1.12 |
| Spirit Strike | 710 | 0.291 | 0.311 | 0.94 |
| Ricochet | 695 | 0.156 | 0.182 | 0.86 |
| Spirit Burn | 685 | 0.833 | 0.588 | 1.42 |
| Mystic Shot | 673 | 0.407 | 0.340 | 1.20 |
| Escalating Exposure | 610 | 0.933 | 0.896 | 1.04 |
| Express Shot | 558 | 0.676 | 0.483 | 1.40 |
| Cold Front | 525 | 0.455 | 0.429 | 1.06 |
| Siphon Bullets | 521 | 0.248 | 0.234 | 1.06 |
| Tesla Bullets | 509 | 0.480 | 0.477 | 1.00 |
| Melee Charge | 434 | 0.254 | 0.136 | 1.87 |
| Headhunter | 410 | 0.439 | 0.438 | 1.00 |
| Capacitor | 375 | 0.696 | 0.694 | 1.00 |
| Headshot Booster | 375 | 0.213 | 0.189 | 1.13 |
| Mercurial Magnum | 340 | 0.296 | 0.284 | 1.04 |
| Rebuttal | 236 | 0.064 | 0.054 | 1.18 |
| Mystic Reverb | 211 | 1.326 | 1.532 | 0.86 |
| Lucky Shot | 200 | 0.397 | 0.220 | 1.81 |
| Arctic Blast | 171 | 1.325 | 0.821 | 1.61 |
| Split Shot | 170 | 0.257 | 0.254 | 1.01 |
| Crushing Fists | 147 | 0.307 | 0.126 | 2.44 |
| Decay | 135 | 1.566 | 1.550 | 1.01 |
| Phantom Strike | 125 | 0.315 | 0.223 | 1.41 |
| Scourge | 121 | 2.131 | 1.798 | 1.19 |
| Alchemical Fire | 111 | 0.994 | 0.978 | 1.02 |
| Return Fire | 96 | 0.445 | 0.120 | 3.71 |
| Lightning Scroll | 49 | 0.423 | 0.262 | 1.61 |
| Focus Lens | 39 | 0.941 | 0.820 | 1.15 |
| Silence Wave | 33 | 0.238 | 0.205 | 1.16 |

## Items by hero (holders only, at least 20 holders), furthest off first

As above, per hero. The source table above compares the whole real match with duels at 30/60/90% of it, so an item bought mid-game looks overrated there; this table doesn't have that bias.

| Hero | Item | holders | real per gun | sim per gun | real/sim |
|---|---|---|---|---|---|
| Drifter | Crushing Fists | 25 | 0.287 | 0.037 | 7.72 |
| Apollo | Melee Charge | 58 | 0.421 | 0.081 | 5.20 |
| Rat King | Return Fire | 41 | 0.389 | 0.080 | 4.86 |
| Drifter | Melee Charge | 68 | 0.211 | 0.049 | 4.27 |
| Billy | Crushing Fists | 31 | 0.319 | 0.087 | 3.66 |
| Baba | Torment Pulse | 138 | 5.029 | 1.791 | 2.81 |
| Paradox | Spirit Burn | 38 | 0.552 | 0.208 | 2.65 |
| Nurse Harrow | Quicksilver Reload | 89 | 0.227 | 0.090 | 2.52 |
| Haze | Lucky Shot | 91 | 0.492 | 0.198 | 2.49 |
| Violet | Torment Pulse | 69 | 0.825 | 0.359 | 2.29 |
| Yamato | Crushing Fists | 30 | 0.299 | 0.133 | 2.26 |
| Calico | Melee Charge | 27 | 0.170 | 0.079 | 2.15 |
| Lash | Quicksilver Reload | 154 | 0.360 | 0.170 | 2.12 |
| Paradox | Tankbuster | 146 | 0.656 | 0.330 | 1.99 |
| Apollo | Mystic Burst | 66 | 0.616 | 0.322 | 1.91 |
| Drifter | Tankbuster | 101 | 0.587 | 0.309 | 1.90 |
| Paradox | Mystic Burst | 63 | 0.176 | 0.095 | 1.86 |
| Violet | Mystic Burst | 66 | 0.227 | 0.124 | 1.83 |
| Billy | Melee Charge | 48 | 0.242 | 0.136 | 1.77 |
| Lash | Spirit Burn | 69 | 0.946 | 0.538 | 1.76 |
| Violet | Tankbuster | 206 | 1.178 | 0.673 | 1.75 |
| Drifter | Mystic Burst | 96 | 0.193 | 0.113 | 1.70 |
| Kelvin | Escalating Exposure | 40 | 4.081 | 2.429 | 1.68 |
| Drifter | Spirit Burn | 42 | 0.410 | 0.249 | 1.65 |
| Yamato | Express Shot | 46 | 0.925 | 0.565 | 1.64 |
| Solomon | Spirit Burn | 23 | 1.019 | 0.634 | 1.61 |
| Grey Talon | Mystic Reverb | 22 | 0.752 | 1.202 | 0.62 |
| Shiv | Express Shot | 125 | 0.882 | 0.559 | 1.58 |
| Shiv | Lucky Shot | 45 | 0.496 | 0.320 | 1.55 |
| Bebop | Tankbuster | 43 | 1.252 | 0.807 | 1.55 |
| Violet | Mystic Shot | 170 | 0.473 | 0.307 | 1.54 |
| Nurse Harrow | Ricochet | 130 | 0.124 | 0.191 | 0.65 |
| Mo & Krill | Rebuttal | 22 | 0.160 | 0.105 | 1.53 |
| Violet | Spirit Burn | 45 | 0.914 | 0.598 | 1.53 |
| Venator | Ricochet | 36 | 0.114 | 0.175 | 0.66 |
| Abrams | Phantom Strike | 58 | 0.235 | 0.154 | 1.52 |
| Calico | Arctic Blast | 102 | 1.394 | 0.926 | 1.51 |
| Nurse Harrow | Decay | 41 | 1.955 | 1.302 | 1.50 |
| Infernus | Ricochet | 66 | 0.110 | 0.166 | 0.67 |
| Abrams | Crushing Fists | 40 | 0.399 | 0.266 | 1.50 |
