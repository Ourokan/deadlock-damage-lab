# Items ranked furthest from real wins after #171-#183; Ballistic Enchantment stacks (2026-10-28)

Question: on main after deaths per engagement (#171), status focus (#175), alt-fire Express Shot (#178/#180) and the
CC study (#183), which items does the overall score still rank furthest from their real Phantom+ win edge within
their slot and tier, and why? (Rebuttal and Debuff Reducer skipped: `status_focus.md`, `focus_share.md`, `cc_time.md`.)

## Biggest gaps (sim gain vs real edge, both centred within hero x slot x tier, z units, mean over heroes)

| Sim under real | 27k | 37k | Sim over real | 27k | 37k |
|---|---|---|---|---|---|
| Golden Goose Egg (sign right) | -4.0 | -4.0 | Extra Charge | +1.8 | +2.4 |
| Superior Cooldown (explained, `cooldown_items.md`) | -1.6 | -2.0 | Decay | +1.9 | +2.0 |
| High-Velocity Rounds | -1.3 | -2.0 | Capacitor | +1.8 | +1.8 |
| Slowing Bullets (no real slow effect, `slow-items`) | -1.3 | -1.7 | Mystic Shot | +1.6 | +1.8 |
| Ballistic Enchantment | -1.3 | -1.4 | Melee Lifesteal | +1.4 | +1.7 |
| Trophy Collector | -1.2 | -1.2 | Heroic Aura | +1.6 | +1.6 |
| Weakening Headshot, Grit, Compress Cooldown | -1.2 to -1.1 | | Monster Rounds | | +1.7 |

Hero halves (odd / even hero id) agree within 0.4 on every row.

## Ballistic Enchantment: one stack in a duel, ~2 in real fights

Real holders deal 1.152x the hero damage per minute of non-holders at 27k (same hero, net worth, game time;
`holder_rates.py`, z +44), the sim's build 1.055x: of 141 items the furthest above the cross-item line of real on
sim damage (slope 0.59, residual +0.11). The item gives +20% weapon damage **per unique enemy hero** the imbued
ability damaged in the last 20 s; the sim's handler refreshed one +20% buff, and a duel has one enemy anyway.

`scripts/team/ballistic_stacks.py` (260 Phantom+ replays, hero-vs-hero damage events): at each gun hit on a hero, the
distinct heroes each of the attacker's abilities damaged in the last 20 s, kept where at least one (the sim's holder
has its stack exactly then), gun-damage weighted. Area abilities carry 1.5-2.8 (Aura of Suffering 2.60, Malice
2.40, Essence Bomb 1.96, Fixation 1.94, Scrap Grenade 1.69), single-target ones 1.00 (Telekinesis, Bloodletting);
pooled 1.44. Match-id halves agree (Malice 2.39 / 2.42, Fixation 1.96 / 1.93). `Mechanics.ballistic_stacks` (on):
the stack is worth WeaponPowerPerStack x that count (`data/ballistic_stacks.json`, 1 for abilities without a row).

| sim_vs_win (blend off, all heroes) | all pairs | within slot and tier | within, hero halves | per item |
|---|---|---|---|---|
| 27k main | 0.2975 | 0.3330 | 0.3343 / 0.3319 | 0.4356 |
| **27k ballistic stacks** | **0.2976** | **0.3332** | **0.3344 / 0.3321** | **0.4357** |
| 37k main | 0.2859 | 0.3170 | 0.3193 / 0.3151 | 0.4171 |
| **37k ballistic stacks** | **0.2860** | **0.3171** | **0.3194 / 0.3151** | **0.4172** |

Small: the sim's damage gain moves 1.055 -> 1.061 (Lady Geist 1426 -> 1458 before death, Wraith 583 -> 594),
and the rank gap -1.27 -> -1.23 (27k). The rest of the real 1.15x is not in reach: non-hero stacks (+5% per creep
or neutral the ability hits, up to 8) are not in the hero-only replay extracts, and real holders also die 1.08x per
minute with 0.95x kills + assists, which the death rate factor charges (0.959). Offline, scaling only Ballistic
Enchantment's damage gain up to the real 1.15x lifts within slot and tier 0.333 -> 0.334 (27k), 0.317 -> 0.318
(37k): even the full real damage would not close its gap.

## Looked at, not changed

- **Golden Goose Egg / Trophy Collector soul income.** The score has no term for souls an item pays directly
  (GGE +80 / min, Trophy Collector stacks; real holders earn 1.04x / 1.11x souls per minute, 27k). Crediting that at
  the economy's worth (total souls ratio ^ 0.2-1.0, GGE and Trophy Collector only) lowers every line (27k within
  0.333 -> 0.332 at 0.2, 0.324 at 1.0, all match-id halves alike): GGE's very low sim value is what tracks its
  real edge (-1.75 z within tier 1 spirit, sign right). Its sim value also drags the other tier-1 spirit items'
  centred gains up (Extra Charge, Rusted Barrel, Spirit Strike).
- **Cheap items' real-rate factors.** Real holders of almost every tier-1 item get more kills + assists per minute
  at 27-37k (1.02-1.16x, tier mean log ratio -0.05 deaths per ka at 37k), so the deaths-per-ka factor rewards the
  tier-1 items whose deaths ratio clears |z| 3 (Extra Charge 1.03 / 1.04, Monster Rounds 1.03 / 1.04, Restorative
  Shot, Extra Regen) and not the others (High-Velocity Rounds, Close Quarters, Grit). The death rate factor's
  correlation with the item gap is +0.47 / +0.52 in tier 1, ~0 in tiers 3-4. Offline variants (rows rescaled, exact
  for a pure item multiplier): tier-1 factors ^ 0.5 lifts 27k within 0.333 -> 0.337, 37k 0.317 -> 0.326 on both hero
  halves; gating on the deaths / ka ratio's own z instead of the deaths z drops it to 0.280 / 0.260; ka centred
  within tier or slot and tier 0.329-0.331 / 0.313-0.315; cost-scaled exponents (cost / 3200 or / 6400) worse at 27k.
  The tier-1 halving has no mechanism behind it (picked by the check), so it is not shipped; the lead is why
  late tier-1 holders fight more (who keeps a cheap item at 27k+). Followed up in `tier1_death_rate.md`: they are
  low-farm players on teams that are ahead; no principled fix keeps sim_vs_win.
- **High-Velocity Rounds** (+60% bullet speed is not modelled): real holders deal 1.003 / 1.010x (sim 1.018x), so
  the sim does not under-count its damage; its real edge comes with more kills + assists (1.04 / 1.07x), which
  only the death-rate gate above touches.
- **Capacitor** sim damage 1.19x vs real holders 0.99x (37k) while its per-gun damage in the audit matches (1.01):
  the real dealt ratio is against other tier-4 holders, so this reads as who buys it, not a model miss.
