# Cooldown items vs real wins (2026-10-27)

Question: after PR #141 (cooldown items buy fight starts with abilities ready), Superior Cooldown still ranks 106 of
141 by sim gain in `analysis/scripts/sim_vs_win.py` (27k, all heroes) but 12 by real win edge; Compress Cooldown
122 vs 22. What do real holders get that the sim misses?

## Real holders vs non-holders (74k Phantom+ matches, same hero, net worth and game time)

`sim/scripts/fight_rate/holder_rates.py` on the fuller stat timelines (`fetch_rates.py`, now with objective, farm
and team heal stats, and imbued buys kept). Superior Cooldown at 27k (107k holder intervals, both match-id halves
agree):

| Per minute | Ratio | z |
|---|---|---|
| Hero damage | 1.025 | +15 |
| Kills + assists | 1.016 | +4 |
| Deaths | 0.974 | -10 (already in the score: `death_rate_value`) |
| Souls | 1.013 | +7 (other T3/T4 spirit items 1.03-1.09) |
| Objective (boss) damage | 0.976 | -3 |
| Lane creep / jungle damage | 1.031 / 0.983 | |
| Team heals / team barriers | 1.10 / 1.15 | +7 / +14 |

- **Damage**: real holders' damage gain is in line with the sim's (across all items real log ratio = 0.34 x sim
  log ratio - 0.025; Superior Cooldown's residual +0.03, mid-pack). Out-of-fight casts don't show up as extra hero
  damage, farm or objective damage.
- **Team heals and barriers** rise 10-15%, but they average 74 HP/min against 1,429 hero damage; only Nurse, Rem,
  Kelvin, Dynamo and Paige heal teammates much, and Superior Cooldown's edges there (+0.5 to +1.2) are not its best.
- **All rates together** (least squares of item edge on the log ratios of damage, K+A, deaths, souls, damage taken
  over 131 items, R 0.50) predict -0.6 pt for Superior Cooldown, real +0.7: its edge isn't visible in any per-minute
  outcome. Its best edges are on heroes where it adds no real damage (Yamato +2.3, Calico +2.0, Holliday +1.7; real
  damage ratio 0.94-0.99).
- **Holder confound**: the 11 heroes whose popular build already holds it are skipped by `sim_vs_win`. Removing it
  from their popular builds costs 0.023 per 1000 souls, the same as adding it on the other 33 heroes (0.023).

## Why it ranks low: the comparison, not the cooldown model

The real edge is against same-slot same-tier items. In spirit T3 the sim's favourites lose real games (Decay sim #1
of 13, edge -4.5; Spirit Snatch #2, -2.5; Tankbuster #4, -1.9), so the whole tier's edges are measured against a
low bar while the sim gain isn't. Within spirit T3, Superior Cooldown is 12/13 by sim and 1/13 by edge: the gap is
the sim over-valuing damage items (damage items Pearson ~0.08), not under-valuing cooldowns.
`sim_vs_win.py` now also prints the correlation with each sim gain centred on the hero's other items of that slot and
tier: 0.220 vs 0.181 uncentred.

## Data fix: imbued buys

`fetch_rates.py` dropped every buy with an imbued ability, so imbue items were missing from `fight_rate.json`
(`death_rate_value`) or measured on a few non-imbued buys: Compress Cooldown, Mystic Expansion, Duration Extender,
Quicksilver Reload, Ballistic Enchantment, Echo Shard, Surge of Power, Mercurial Magnum, and Mystic Reverb (572 ->
30,750 holders at 27k). Refetched (`/mnt/project-files/analysis/work/fight_rate_ext`) and refit; the other items'
rates are unchanged. New deaths ratios at 27k: Mystic Reverb 0.938 (z -9.7), Ballistic Enchantment 1.076, Mystic
Expansion 1.052, Surge of Power 1.025, Duration Extender 1.028, Compress Cooldown 1.018 (z 4.8; halves 1.006 /
1.029). sim_vs_win 27k: all pairs 0.181 -> 0.181, damage items 0.078 -> 0.083, clear edges 0.274 -> 0.275, per item
0.260 -> 0.260. Compress Cooldown's holders die slightly more, so it drops (sim rank 122 -> 128).

## Not modelled

No cooldown mechanic beyond `Mechanics.cdr_ready` holds up in the real data; the win blend carries the rest of the
cooldown items' edge. Possible follow-ups: count hero abilities' ally heals and barriers in the overall score (healer
heroes only), and the damage items' over-valuation within their tier.
