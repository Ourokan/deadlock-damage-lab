# Items ranked furthest from real wins after #195; Melee Lifesteal joins the healing items (2026-10-28)

Question: on main after #195, which items does the overall score still rank furthest from their real Phantom+ win
edge within slot and tier, and is there a real mechanism behind any of them? Skipped as already settled: Golden Goose
Egg / Trophy Collector income, the tier-1 death-rate bonus, team lead, Return Fire, Rebuttal / Debuff Reducer, cooldown
and slow items, Capacitor / Decay (`ballistic_stacks.md`, `tier1_death_rate.md`, `team_lead_edges.md`,
`focus_cost.md`, `status_focus.md`, `cooldown_items.md`, `split_shot_range.md`).

## Biggest gaps (sim gain vs real edge, both centred within hero x slot x tier, z units, mean over heroes)

| Sim under real | 27k | 37k | Sim over real | 27k | 37k |
|---|---|---|---|---|---|
| Golden Goose Egg | -4.0 | -4.1 | Decay | +1.9 | +2.0 |
| Superior Cooldown | -1.7 | -2.0 | Extra Charge | +1.9 | +2.4 |
| Debuff Reducer | -1.5 | -1.4 | Capacitor | +1.8 | +1.8 |
| High-Velocity Rounds | -1.2 | -2.0 | Heroic Aura | +1.7 | +1.7 |
| Ballistic Enchantment | -1.2 | -1.3 | Mystic Shot | +1.6 | +1.8 |
| Slowing Bullets | -1.2 | -1.7 | Melee Lifesteal | +1.5 | +1.7 |
| Superior Duration | -1.1 | -1.1 | Disarming Hex | +1.3 | +1.5 |

## Melee Lifesteal: a healing item missing from HEAL_ITEMS

Its sim gain was mostly the focus cost read backwards: real holders take 0.945x the damage per minute of matched
non-holders (27k, z -21; 37k 0.960), so `focus_value` gave it x1.02 as if it were armour. HEAL_ITEMS (the items the
sustain replays credit with self healing, left out of the death-rate and focus factors) had Bullet and Spirit
Lifesteal but not Melee Lifesteal, though the same replays credit it with 71 HP/min.

The reason healing items are left out holds for it: across the 124 other items the real edge falls with the holders'
damage-taken ratio (-4.5 win points per log ratio at 27k, -2.7 at 37k), across the 15 healing items it doesn't (+2.3
at both). Melee Lifesteal (taken 0.945, edge -1.8) sits with the healing items, not on the other items' line (which
would put it near +0). Vampiric Burst (lifesteal active) takes 1.08x and wins less, as the other items do; adding it
lowers every line, so it stays out.

| sim_vs_win (blend off, all heroes) | all pairs | within slot and tier | within, hero halves | per item |
|---|---|---|---|---|
| 27k main | 0.3022 | 0.3366 | 0.3319 / 0.3414 | 0.4383 |
| **27k Melee Lifesteal healing** | **0.3064** | **0.3424** | **0.3366 / 0.3481** | **0.4451** |
| 37k main | 0.2946 | 0.3185 | 0.3117 / 0.3255 | 0.4150 |
| **37k Melee Lifesteal healing** | **0.2972** | **0.3239** | **0.3162 / 0.3317** | **0.4192** |
| + Vampiric Burst too, 27k | 0.3060 | 0.3407 | 0.3352 / 0.3461 | 0.4446 |

Full runs (both budgets together: all 0.298 -> 0.302, within 0.319 -> 0.325, per item 0.434 -> 0.440). Melee
Lifesteal's mean-gain rank 16 -> 110 of 141; its gap +1.5 / +1.7 -> +0.2 / +0.7.

## Looked at, not changed

- **Extra Charge** (+1.9 / +2.4). In the sim's audit duels (real builds, 1500 players, same seeds with and without
  it) the extra charge raises charged-ability casts 1.20x (in the first 3 s 1.05x); real holders cast them 1.13x as
  often per pair fight as matched non-holders (by 3 s 1.15x; 259 replays), selection included. No sign of the sim
  dumping the extra charge. On heroes with no charged ability (Mo & Krill, Solomon) its gain is only the tier-1 death
  factor (x1.03-1.04), the bonus `tier1_death_rate.md` found no fix for.
- **High-Velocity Rounds** (-1.2 / -2.0). Bullet speed isn't in the sim, so the question was whether faster bullets
  land more. New per-interval gun rates (`sim/scripts/fight_rate/gun_hit_rates.py`, 14 days of Phantom+ stat
  timelines with shots hit / missed and hero bullets hit): HVR holders' hero hits per shot are 1.02 / 1.00 / 0.98 /
  1.00x matched non-holders at 10k / 18k / 27k / 37k, like other tier-1 gun items (Close Quarters 0.97-1.00, Monster
  Rounds 0.97-1.00). Sharpshooter / Armor Piercer (same +60% speed) 1.00-1.04. No accuracy gain to model; the other
  bullet speed items have negative edges and over-ranks too. Opening Rounds holders hit 1.07x per shot at every
  band (its own bonus, not speed: Sharpshooter doesn't show it).
- **Mystic Shot** (+1.6 / +1.8): real holders deal 1.046x (27k), the sim 1.145x at the 0.5 elasticity: on the line.
- **Disarming Hex / foe disables under focus**: the duel's enemy deals x FOCUS 2, so disarming or stunning it stops
  both attackers' damage. If that were over-valuing disables, Knockdown, Silence Wave, Inhibitor, Slowing Hex would
  rank over their edges too; they sit within 0.25 z. Not the cause.
