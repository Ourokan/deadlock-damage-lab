# Items ranked furthest from real wins after #190/#191; Split Shot's fan by distance (2026-10-28)

Question: on main after Drifter's current-health bleed (#190) and the team lead check (#191), which items does the
overall score still rank furthest from their real Phantom+ win edge within slot and tier, and is there a game
mechanism behind any of them? (Golden Goose Egg / Trophy Collector income, the tier-1 death-rate bonus, Rebuttal,
Debuff Reducer, cooldown and slow items are skipped: `ballistic_stacks.md`, `tier1_death_rate.md`,
`team_lead_edges.md`, `status_focus.md`, `cooldown_items.md`.)

## Biggest gaps (sim gain vs real edge, both centred within hero x slot x tier, z units, mean over heroes)

| Sim under real | 27k | 37k | Sim over real | 27k | 37k |
|---|---|---|---|---|---|
| Golden Goose Egg | -4.0 | -4.0 | Extra Charge | +1.8 | +2.4 |
| Superior Cooldown | -1.7 | -1.9 | Decay | +1.9 | +2.0 |
| High-Velocity Rounds | -1.2 | -1.9 | Capacitor | +1.8 | +1.8 |
| Slowing Bullets | -1.2 | -1.7 | Mystic Shot | +1.6 | +1.8 |
| Debuff Reducer | -1.5 | -1.4 | Heroic Aura | +1.6 | +1.7 |
| Ballistic Enchantment | -1.2 | -1.3 | Melee Lifesteal | +1.4 | +1.7 |
| Counterspell | -1.1 | -1.2 | Disarming Hex | +1.3 | +1.5 |
| Superior Duration | -1.1 | -1.1 | Split Shot | +1.4 | +1.2 |
| | | | Divine Barrier | +1.3 | +1.2 |

Hero halves (odd / even hero id) agree within ~0.5 on every row. Per hero x item, after Golden Goose Egg the largest
gaps on both budgets are Split Shot on Infernus (+5.9 / +8.3), Haze (+5.6 / +5.5) and Vindicta (+4.2 / +4.9).

## Split Shot: the fan's hits on the target fall with distance

Split Shot fires BulletSplitShot (5) extra bullets over a 45 degree fan. The sim gave every holder the replays'
pooled 0.73 copies on the main target per landed gun bullet (`mechanics.SPLIT_PRIMARY_HIT`, 614 activations, mostly
Vyper and Wraith). The per-hero rows of that same fit (`validation/mechanics/split_shot_replays.json`) follow the
holder's median Phantom+ fight distance (`data/skill_defaults.json`) like the fan's angular size on a hero:

| Hero | Activations | Median distance | Real copies per landed bullet | 8.4 / distance |
|---|---|---|---|---|
| Yamato | 17 | 8.2 m | 1.10 | 1.03 |
| Vyper | 462 | 10.9 m | 0.76 | 0.77 |
| Wraith | 129 | 15.6 m | 0.59 | 0.54 |
| Paige | 6 | 15.8 m | 0.73 | 0.53 |

8.4 = 0.73 x 11.5 m (activation-weighted). `Mechanics.split_range` (on): the main target takes
`SPLIT_PRIMARY_HIT x SPLIT_REF_M (11.5) / the holder's median distance` copies (`mechanics.split_primary_hit`), so far
heroes no longer get close-range Vyper's 0.73: Vindicta (25.8 m) 0.33, Grey Talon 0.37, Haze 0.65, Infernus 0.56.
Side copies on other enemies are unchanged.

Damage audit (Vyper, Wraith, Yamato, Paige, Phantom+ sample): Split Shot real / sim Vyper 1.22 -> 1.19, Wraith
1.03 -> 1.17 (fewer copies at 15.6 m), damage mix distance Vyper 0.021 -> 0.018, Wraith 0.021 -> 0.019. Wraith's
hero factor refit (`item_landing_heroes.py --item "Split Shot"`): 0.581 -> 0.655; Vyper stays uncut (1.0). The
pooled factor (0.916) is left: pooled real / sim moved only 1.20 -> 1.22.

| sim_vs_win (blend off, all heroes) | all pairs | within slot and tier | within, hero halves | per item |
|---|---|---|---|---|
| 27k main | 0.2995 | 0.3338 | 0.3274 / 0.3402 | 0.4359 |
| **27k split range** | **0.3014** | **0.3360** | **0.3307 / 0.3413** | **0.4381** |
| 37k main | 0.2916 | 0.3169 | 0.3104 / 0.3237 | 0.4140 |
| **37k split range** | **0.2936** | **0.3192** | **0.3131 / 0.3256** | **0.4156** |

Every line up on both budgets and both hero halves. Split Shot's item gap +1.36 -> +1.19 (27k), +1.22 -> +1.05
(37k); Vindicta's gain per 1000 souls 0.073 -> 0.051 (damage x1.28 -> x1.20), Grey Talon 0.022 -> 0.012.
Infernus (+5.1 / +7.2) and Haze (+5.1 / +5.5) keep most of their gap: their copies proc Afterburn / Toxic Bullets
and Fixation stacks; whether real Split Shot pellets build those hero effects needs replays of their holders (few
Phantom+ buyers: none in the audit sample).

## Looked at, not changed

- **Team items (Heroic Aura, Divine Barrier over).** Both get the 3v3 team value (x1.14 at 27k) on top of the
  holder's own death-rate factor. Real teammates of holders (`sim/scripts/fight_rate/teammate_rates.py`, new: the
  other four players' deaths, kills + assists, damage and the enemy team's deaths per minute, matched on the
  holder's hero, net worth and game time, 74k matches): Divine Barrier holders' teammates die 0.916x (27k, z -20,
  match-id halves 0.912 / 0.920), Heroic Aura 0.944x, Healing Nova / Rescue Beam 0.946x, Locket 0.986x; their
  teammates deal +3-5% damage, about the size the 3v3 gives (Divine Barrier 4 x 0.051 = 0.20 of the holder's damage
  vs the 3v3's 0.18). So the team value is not over-sized. Scaling it down lowers every line (team value ^ 0.5:
  27k within 0.334 -> 0.327, 37k 0.317 -> 0.311), and a teammate factor (mates' death ratio ^ -0.5, -1) on top of
  or instead of the 3v3 value lowers them more (27k within 0.317 / 0.300). Real holders of Divine Barrier deal 0.78x
  the hero damage of non-holders (supports), which the sim's item does not cause.
- **Real damage per item instead of the sim's.** Scaling each item's score by its real holders' damage ratio over the
  elastic sim one (|z| >= 3, weight 0.25-1) lifts 37k within (0.317 -> 0.325 at 0.25) but drops 27k
  (0.334 -> 0.328): buyer type rides along, no gain on both budgets.
- **Capacitor** (+1.8): the audit matches its per-gun damage; real holders' total damage 1.005x vs sim 1.22x
  (27k), residual -0.06 on both budgets against the cross-item slope. Not a mechanism found here.
- **Decay** (+1.9): real dealt 1.096x vs sim 1.228x, on the slope; the kill weight (0.40) already cuts it. Its
  -4.4 point edge has no counterpart in holders' deaths, kills + assists or teammates (all ~1.00).

## Tools

- `sim/scripts/fight_rate/holder_rates.py` now also writes each metric's non-holder base rate (third element), for
  absolute per-minute differences.
- `sim/scripts/fight_rate/teammate_rates.py SRC OUT.json` (~10 min): the teammate table above.
