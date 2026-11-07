# Items changed by the 10-30 and 11-05 hotfixes (2026-11-07)

Follow-up to the hotfix ability sweep (PR #236). Which item mechanics did the hotfixes change, does the sim still
match post-hotfix real games for those items, and what is stale?

## What changed

Diff of data/game/shop_items.json across the two hotfix commits (a56e2d0 = 10-30, 8009788 = 11-05). 10-30 changed
36 items; 11-05 changed one (Healbane gained StackingPenaltyAnchorPercent 80).

- Read straight from game data, nothing to do: weapon damage on Battle Vest, Bullet Lifesteal, Fury Trance,
  Glass Cannon, Vampiric Burst; lifesteal on Bullet/Spirit Lifesteal, Infuser, Leech, Spiritual Overflow; Armor
  Piercer proc chance 55 -> 60; Express Shot alt-fire bonus 40 -> 38 (scale 1.3 -> 1.24); Lightning Scroll damage
  now scales 0.35 x spirit (item_value applies it); cooldowns of Divine Barrier, Focus Lens, Spirit Sap; anti-heal
  on Decay, Toxic Bullets, Crippling Headshot; resists and health.
- Healing items (Radiant Regeneration, Healing Booster, Healing Nova, Healbane kill heal) were handled in PR #214
  (heal_change.md) and PR #216 (hotfix_rates.md).
- Stale in the sim: **Shadow Weave** (ambush +25% fire rate and melee -> +50% weapon damage; the sim read the removed
  AmbushBonusFireRate as 0) and **Rebuttal** (ParryCooldownReduction 1.75 -> 1.25 s; the sim's parry multiplier for
  holders was measured before the hotfix).
- Not modelled: Healbane's StackingPenaltyAnchorPercent (only matters when several anti-heals stack on one target;
  the formula isn't in the data), Echo Shard's post-cast 0.5 -> 0.2 s, Point Blank slow duration, Metal Skin gravity.

## Damage audit on post-hotfix matches

damage_audit.py on the post-hotfix samples (post_hotfix_2026-11-07 + 07b, 4,103 Phantom+ matches, 44,317
player-matches), item holders, real / sim item damage share. Changed damage items: Lightning Scroll 1.05 (549
holders), Focus Lens 1.04, Toxic Bullets 1.03, Express Shot 0.98, Torment Pulse 0.99, Silence Wave 1.04: all within
~5%. Decay 1.15 (pre-hotfix audit 1.00): its damage didn't change, and its factor is already at the cap
(landing x length_corr 1.12), so not a hotfix item to refit. **Rebuttal 0.65** (1,901 holders; pre-hotfix 0.88 on
238 holders): the sim deals 1.5x real.

## Rebuttal

Whole-match parry successes per 3 min, players holding Rebuttal for over half the match vs players without it:
phantom_sample (pre-hotfix) 0.80 vs 0.38 = 2.11x (183 holders); post-hotfix samples 0.80 vs 0.44 = 1.80x (1,351
holders). The sim's Rebuttal.REBUTTAL_PARRY_MULT (1.9, from per-window rates before the hotfix) is scaled by the same
change: 1.9 x 1.80 / 2.11 = **1.62**.

sim_vs_win (post-hotfix pools, base = main at 1578040), within slot and tier, shipped edges and day-half edges:

| budget | shipped | day half A edges | day half B edges | raw edges A / B |
|---|---|---|---|---|
| 27k | 0.4396 -> 0.4396 | 0.4377 -> 0.4378 | 0.4615 -> 0.4615 | +0.0000 / +0.0000 |
| 37k | 0.4221 -> 0.4227 (hero halves +0.0005 / +0.0007) | 0.4174 -> 0.4187 | 0.4501 -> 0.4505 | +0.0005 / -0.0000 |

Kept: flat at 27k, up at 37k on both hero halves and both day halves. Rebuttal's mean sim gain -0.0156 -> -0.0168
(real edge -2.75).

## Shadow Weave (opt-in, OFF)

ShadowWeave.AMBUSH_WEAPON = True gives the ambush's +50% weapon damage for AmbushDuration (5 s). It lowers sim_vs_win
at both budgets on every edge set: within slot and tier 27k 0.4396 -> 0.4390 (-0.0006 +- 0.0003, day halves -0.0007 /
-0.0007), 37k 0.4221 -> 0.4213 (-0.0007, day halves -0.0006 / -0.0009); raw edges -0.0001 to -0.0003. Shadow Weave is
not a candidate row in the check (a movement item), so the drop comes from builds and foes that hold it. Kept off.

## Reproduce

- Diff: git show a56e2d0^:data/game/shop_items.json vs a56e2d0 vs 8009788, flatten properties per item.
- Audit: `AUDIT_OUT=... python3 scripts/damage_audit.py post.jsonl.gz` (the two post-hotfix samples concatenated,
  ~15 min on 4 cores).
- Win check: build_pool.py phantom, `sim_vs_win.py --budgets 27000,37000 --out` for base and variant (~55 min each on
  2 workers), then sim_vs_win_compare.py / sim_vs_win_raw.py with `--halves
  /mnt/project-files/analysis/work/win_edge_week`.
