# Real use of non-damage active items (Phantom+)

260 Phantom+ replays (fight_length raw + item casts, fetch_item_casts.py). Use = the fighter casts the item from 2 s before the fight's first hit to 1 s after its last (engagement: a fighter's fights with enemy heroes, sim/scripts/fight_length, merged when they overlap or follow within 5 s). Sim use = the overall search's fight, P(the fight is still going at the first cast). Factor = real / sim, shrunk toward 1 (tau 0.39), max 1.

| Item | Real use | Sim use | Raw | Factor | Holder-matches | Engagements |
|---|---|---|---|---|---|---|
| Rescue Beam | 0.15 | 0.53 | 0.28 +- 0.03 | **0.28** | 46 | 382 |
| Cursed Relic | 0.39 | 0.95 | 0.42 +- 0.02 | **0.42** | 113 | 632 |
| Knockdown | 0.45 | 1.00 | 0.45 +- 0.02 | **0.45** | 145 | 1285 |
| Cultist Sacrifice | 0.46 | 1.00 | 0.46 +- 0.01 | **0.46** | 372 | 6332 |
| Vampiric Burst | 0.52 | 1.00 | 0.52 +- 0.02 | **0.52** | 81 | 499 |
| Heroic Aura | 0.56 | 1.00 | 0.56 +- 0.02 | **0.56** | 110 | 1077 |
| Infuser | 0.59 | 1.00 | 0.59 +- 0.02 | **0.59** | 76 | 740 |
| Guardian Ward | 0.36 | 0.62 | 0.59 +- 0.03 | **0.59** | 157 | 1714 |
| Grit | 0.43 | 0.67 | 0.64 +- 0.02 | **0.64** | 587 | 3487 |
| Disarming Hex | 0.68 | 0.99 | 0.68 +- 0.03 | **0.68** | 91 | 736 |
| Healing Nova | 0.31 | 0.45 | 0.69 +- 0.07 | **0.70** | 17 | 211 |
| Divine Barrier | 0.42 | 0.60 | 0.71 +- 0.05 | **0.71** | 102 | 563 |
| Spirit Sap | 0.71 | 1.00 | 0.71 +- 0.02 | **0.71** | 49 | 753 |
| Restorative Locket | 0.33 | 0.46 | 0.73 +- 0.03 | **0.73** | 111 | 1656 |
| Rusted Barrel | 0.73 | 0.99 | 0.74 +- 0.02 | **0.74** | 99 | 1533 |
| Unstoppable | 0.36 | 0.47 | 0.77 +- 0.02 | **0.77** | 329 | 2023 |
| Fury Trance | 0.53 | 0.61 | 0.87 +- 0.08 | **0.87** | 20 | 253 |
| Colossus | 0.55 | 0.63 | 0.87 +- 0.06 | **0.87** | 46 | 241 |
| Metal Skin | 0.49 | 0.43 | 1.12 +- 0.04 | **1.00** | 163 | 1195 |
