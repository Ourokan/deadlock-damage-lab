# Heal items after the 10-30 hotfix: real heal rates follow the game values (2026-11-06)

Question: which items' sim value vs real win edge moved most after the late-October hotfix (10-30), and why?

## Data

This week's Ritualist+ builds after the hotfix (10-31 to 11-03, ~75k matches, fetch_builds.py; days kept in
/mnt/project-files/data/builds/player_builds/) gave week-only edges (build_win_check.hero_edges on those days),
compared with the edge snapshot through 10-30 (a56e2d0). Gap = sim gain z - real edge z, both centred within hero x
budget x slot x tier, sim rows from sim_vs_win.py on main (27k + 37k).

Moved most, and the same on 10-31 and 11-01 taken alone: healing items lost real edge (Radiant Regeneration gap
-0.2 -> +1.4 z, Mystic Regeneration +1.2, Rescue Beam, Healing Tempo, Restorative Shot, Guardian Ward), spirit damage
items gained (Surge of Power, Torment Pulse, Spirit Burn, Escalating Resilience, Fury Trance). The hotfix nerfed
heals: Radiant Regeneration 65 + 1.7/boon per cast -> 40 + 1.4, regen 0.035 -> 0.025/spirit; Healing Booster lost
its 3 regen; anti-heal up (Decay -55%, Toxic/Crippling -40%); lifesteal 13% -> 15%.

## Mechanism gap

The sim's in-fight heals read the current values, but the real per-item heal rates out of fights
(sustain.json farm_heal_hp_per_min, fountain_saved_hp_per_min, 400 Phantom+ replays) were measured before the
hotfix, so Radiant kept its old 388-475 HP/min of farm healing.

## Change

sustain.json measured_items stamps the heal values the rates were measured with (data/game before the hotfix,
sim/scripts/sustain/stamp_heal_values.py). overall_search.heal_change scales each rate by heal value now / then at
the build's boons and spirit power: Radiant 0.74-0.76, Spirit/Bullet Lifesteal 1.15, others 1.

## Results (full sim_vs_win, all heroes)

| within slot and tier | 27k all / hero half 0 / half 1 | 37k all / half 0 / half 1 |
|---|---|---|
| shipped edges (to 11-04) | 0.4086 -> 0.4089 / 0.4003 -> 0.4007 / 0.4170 -> 0.4173 | 0.3837 -> 0.3839 / 0.3762 -> 0.3767 / 0.3916 -> 0.3917 |
| post-hotfix week edges | 0.3949 -> 0.3971 / 0.3882 -> 0.3902 / 0.4018 -> 0.4041 | 0.3677 -> 0.3701 / 0.3633 -> 0.3656 / 0.3724 -> 0.3749 |

Up on every half and budget, ten times more on the post-hotfix edges. Radiant's gap 1.46 -> 1.32 z: the rest of its
fall is not the farm rate (more anti-heal and spirit builds in this week's games; svw still scores against the 10-14
popular-build pools).
