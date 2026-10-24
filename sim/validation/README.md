# Combat model validation

How far the step 2 fight model (`deadsim`) can be trusted, checked against hand calculations and 400 real
ranked matches (badge 60+, current patch, 2026-10-13; `matches_sample.jsonl.gz`, 4,800 player-matches).

## What it is checked against

| Check | Script | Result |
|---|---|---|
| Hand-calculated mechanics (resist stacking, falloff, headshots, reload gaps, CDR, spirit scaling, procs) | `tests/test_mechanics.py` | 19 tests pass |
| Static stats vs in-game stat snapshots (38,587 snapshots, every ~3 min of every match) | `scripts/validate_stats.py` | max health within 1 HP 72%, spirit power exact 74%, weapon damage % exact 72% |
| Real aim inputs | `scripts/build_skill_defaults.py` | per-hero hero-only accuracy / headshot percentiles + fight distance in `data/skill_defaults.json` |
| Damage mix by source (gun, each ability, each item) vs the real damage matrix | `scripts/landing_rates.py` | 119 of 129 abilities within 0.2-2x of real after fixes; gun share within 10 points for 26 of 40 heroes |
| Item proc rates vs wiki per-hero numbers | `tests/test_mechanics.py` | Toxic Bullets build-up within 5% of wiki for Wraith and Ivy |

## Formulas the data pinned down

- **Level:** net worth runs 600 souls ahead of the souls that count toward level, so level = level table at
  (net worth − 600) and boons = level − 1. True level = ability points + 4; this matches 97% of snapshots.
  (The first version used boons = level − 2 from raw net worth, which was right early and one boon short after
  ~15k souls.)
- **Health / spirit / weapon %:** see the docstring of `deadsim/build.py`. The remaining misses are items whose
  bonus is conditional or stacking (Hollow Point, Berserker, Enchanter's Emblem, Cultist Sacrifice, Battle Vest);
  those are handled by item effects in fights, not static stats. In-game spirit power is shown floored.
- **Item proc build-up** (Toxic Bullets, Silencer, Inhibitor, Spiritual Overflow): build-up per bullet =
  BuildUpPerShot% × hero base bullet damage × 1.4 × falloff, fitted to deadlock.wiki's per-hero numbers.
  The raw 1.28%/hit made Toxic Bullets take ~79 hits; real is ~10-20.
- **Burst guns** (Seven, Paradox, Lash, Sinclair): one trigger pull every cycle_time + burst × intra-burst time,
  matching the data's bullets/second (the first version fired twice as fast).
  **Spin-up guns** (McGinnis, Victor) speed up toward their spun-up cycle time while firing.
- **Ability upgrades:** `abilities.json` merged upgrade tiers and lost the flat part when a tier gave both
  "+22 damage" and "+0.2 spirit scaling" (63 abilities). `deadsim/data.py` now rebuilds upgrades from
  `raw/items.json` with their types; `CastCtx.val()` applies scale upgrades.

## Real damage mix and ability landing rates

The Deadlock API has no per-ability hit/miss data. Instead `scripts/landing_rates.py` replays each player's real
build (items and net worth at 30/60/90% of the match, real gun accuracy and headshot rate) against a real enemy
from the same match at the same moment, with abilities always landing, and compares each ability's damage
relative to gun damage with the real damage matrix:

    landing = (real ability dmg / real gun dmg) / (sim ability dmg / sim gun dmg)

Output: `data/landing_rates.json` (per hero, per ability) and `damage_shares.json` (real vs sim share of every
source). Median landing is 0.59. `Skill.ability_landing` applies the factors in fights;
`accuracy.hero_default_skill(hero)` loads them by default (`landing=False` to turn off).

What the factor contains, so it is not read as pure aim: missed skillshots, partial time in zones and DoTs,
casts on creeps, and the fact that every sim duel starts with all cooldowns ready while real match totals
include gun time spent waiting on cooldowns. Long-cooldown ultimates therefore come out low (0.2-0.4) even when
modeled correctly. Factors above 1 are mostly abilities that hit several heroes in real team fights
(Pocket Barrage 1.7, Shiv Slice and Dice 1.5, Celeste Shining Wonder 1.4).

The comparison found and fixed real bugs in about 20 heroes (examples: Haze Fixation proc dealing 40 × spirit,
Shiv knife bleed at 12 × spirit, Paige +1400% fire rate, Doorman barrier × spirit, Kelvin and Holliday scaling
counted twice, ultimates that never came into range at duel distance, damage booked under the wrong name).

## Items

`item_shares.json` compares each item's share of all hero damage, real vs sim. After the build-up fix Toxic Bullets
went from 0% to 0.83% (real 0.67%); Headhunter 0.67% vs 0.55%, Tankbuster 1.5% vs 2.5%, Spirit Burn 0.43% vs
0.58%. Underrated: Torment Pulse (0.28% vs 1.12%), Mystic Reverb (0.10% vs 0.54%), Capacitor (0.11% vs 0.72%).
Those handlers should be reviewed before build search leans on them.

Mystic Shot (sim 0.67% vs real 0.34%) was fixed 2026-10-14. Measured as Mystic Shot / gun damage to enemy heroes
while the item is held (full damage matrix of 80 matches, 126 holders): real 0.32, sim 0.45. Per-proc damage and the
8 s cooldown match the game data; the gap was that every sim fight opened with the proc ready, while in real games
62% of Mystic Shot damage lands on creeps and troopers, so the cooldown is usually part spent when a hero fight
starts. Its cooldown now starts mid-cycle (random point with an rng), giving 0.31. Other cooldown-gated on-hit procs
start ready too, but they come out underrated, so they were left alone.

Coverage: 115 of 173 shop items have an effect handler on top of their always-on stats (37 of 50 actives); the
rest are pure stat items or effects with no value in a fixed-distance 1v1 (list at the top of
`deadsim/items_fx_extra.py`). Proc thresholds are read from the game data (Mystic Burst 80, Tankbuster 165 damage
per ability hit). Outgoing healing amp (Healing Booster, Healing Tempo) applies to ability heals, lifesteal and
item heals; regen amp to regen.

## Melee

The API has no melee hit counts, so `scripts/landing_rates.py --fit-melee` fits each hero's landed basic melee
hits per second (`data/melee_rates.json`) so that sim melee/gun damage matches the real damage matrix. It
converged in 3 passes. Abrams lands 0.29 rotation melees/s plus a heavy melee after every Shoulder Charge that
connects (melee is 40% of his real damage), Billy 0.22, Venator 0.19, Drifter
0.16, Apollo 0.12, and the median hero 0.03. Assumptions: 30% of melees are heavy; a light melee stops the
gun for 0.6 s and a heavy for 1.1 s. Melee items have handlers: Melee Charge, Crushing Fists, Spirit Snatch,
Spirit Strike, Lifestrike, Melee Lifesteal. `accuracy.hero_default_skill` loads the rate; users can set their own
with `hero_default_skill(hero, melee_rate_override=0.5, heavy_share=0.4)` (or `Skill(melee_rate=..., heavy_share=...)`).
`Skill.combo_melee` (on by default) adds Abrams' charge into heavy melee combo on top of the rate.

### Melee follows the build

The fitted rate is the hero's average player, but players who buy melee items melee more. `scripts/melee_items_fit.py`
replays every player's real build (30/60/90% of the match) at the hero's average rate and compares real melee/gun
damage with the sim's, grouped by how many melee items the player held (Melee Charge, Crushing Fists, Lifestrike,
Melee Lifesteal, Spirit Snatch, Spirit Strike, Rebuttal). The sim already gives those items their per-hit damage, so
what is left is how often the player lands melees. Fit with hero fixed effects (within-hero comparison), 3,600
player-matches, `data/melee_items.json`:

| Melee items held | Gun heroes (rate < 0.08) | Melee heroes (Abrams, Billy, Drifter, Shiv, Calico, Yamato, Venator, Silver, Apollo) |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 1.86x (90% CI 1.49-2.12), **used 1.49x** | 1.07x (0.86-1.41), **used 1x** |
| 2+ | 3.80x (2.53-4.80, 40 players), **used 2.53x** | 1.51x (1.19-2.02), **used 1.19x** |

This compares players who chose melee items with players who didn't, so part of the gap is selection: players who
like to melee buy the items. Fights therefore use each multiplier's 90% lower bound, never below 1 ("used" in the
JSON). That is a conservative middle between "the item changes nothing about how you play" and "you play like
today's holders", and it keeps the thinnest group (gun heroes with 2+ items) from driving build search.

`accuracy.melee_rates_by_items(hero)` turns this into three rates per hero, scaled so the hero's real mix of builds
still averages to its fitted rate (Haze 0.013 / 0.019 / 0.032 hits/s, Abrams 0.256 / 0.256 / 0.304).
`hero_default_skill` stores the multipliers in `Skill.melee_item_mult` and `fight.make_fighter` (duels and team
fights) scales `melee_rate` by the one that matches the build (so a caller's own `melee_rate`, 0 included, is scaled,
never replaced; heroes missing from the fit keep the flat rate), so adding Lifestrike to a build also makes its holder melee more. A user-set
`melee_rate_override` turns this off. `melee_items_fit.py --check` reruns with the used rates: real/sim per group is
then 0.93-1.15 (the conservative bound leaves gun heroes with 2+ items 15% under real); with the average rate it
was up to 1.9x off.

Items with MeleeDistanceScale lunge heavy melees that much farther (game data: Melee Charge 50%, Crushing Fists 60%,
Runed Gauntlets 150%; the largest held counts): with movement on,
a chaser lands heavies on a runner from that much farther (`mechanics.melee_reach`). Lifestrike's slow was
already in the movement model.

`scripts/melee_value.py` measures what melee is worth on real builds: real mid/late-game snapshots of each
hero against real enemies from the same match, 30 s duels. It compares the hero's real melee rate vs none,
and each melee item vs a same-cost non-melee item on the same cases (`melee_value.json`). The HP margin is
(my HP left − enemy HP left) as a fraction of max HP. Rerun 2026-10-24 with build-based melee rates:

| Hero | Win rate from melee | Lifestrike vs Bullet Resilience | Spirit Snatch vs Bullet Resilience | Crushing Fists vs Leech | Melee Charge vs Swift Striker |
|---|---|---|---|---|---|
| Abrams | +19 pts | +0.23 | +0.22 | −0.03 | +0.03 |
| Billy | +13 pts | +0.21 | +0.21 | −0.01 | +0.08 |
| Drifter | +24 pts | +0.12 | +0.07 | −0.20 | +0.01 |
| Calico | +19 pts | +0.07 | +0.07 | −0.14 | +0.04 |
| Shiv | +8 pts | +0.08 | +0.04 | −0.15 | 0.00 |
| Yamato / Apollo / Silver | +9 / +12 / +6 pts | +0.06 / +0.04 / +0.06 | +0.14 / +0.08 / +0.03 | ≈0 | +0.01 to +0.04 |
| Gun heroes (Infernus, Haze, Venator) | 0-5 pts | −0.03 to +0.10 | −0.09 to +0.05 | −0.09 to −0.27 | −0.08 to +0.04 |

Compared with the average-rate version, melee items gained up to ~0.07 of HP margin on most melee heroes (Billy's
Melee Charge +0.03 → +0.08, Spirit Snatch +0.13 → +0.21) and stay behind for gun heroes. Melee Lifesteal and Spirit
Strike stay within ±0.09 of their comparison item. Heavy share (30%) is still an assumption: the API counts parries but not light vs heavy melees.

## Cleanses

Dispel Magic (added 2026-10-14 during step 3): its active purges enemy debuffs and DoTs (`Fighter.dispel`) and heals
250. The AI fires it at once when silenced/disarmed. Against a DoT (>= 2 s left) it fires on only
`Skill.dot_cleanse_share` of DoT episodes (drawn once while some enemy DoT runs and Dispel is ready), `Skill.dot_cleanse_delay` after it lands (reaction: 1.5 s Eternus,
3 s below). Fit (2026-10-24, `scripts/fit_dispel.py`, `validation/dispel/`): in real matches Dispel holders take 85%
of their teammates' Decay damage at Phantom+ (1500 matches, 90% CI 0.81-0.89), 87% at all ranks, 91% at Eternus+
(175 matches, CI 0.77-1.07), from `damage/scripts/decay_vs_dispel.py` with the right-aligned damage-matrix read (the
first run read arrays from the start and got 1.00). Real (Decay, Dispel) holder item snapshots from the same matches,
dueled with and without Dispel (the holder can't die, like a fixed real window), give that ratio at share 0.26
(Phantom+, CI 0.19-0.33) and 0.16 (all ranks); Eternus+ (0.13, CI 0.00-0.34) is too thin and uses the Phantom+ share.
Cleansing every DoT at the old rank timings gave 0.35
(3 s) and 0.26 (1.5 s). A share, not a longer delay, so short DoTs (burns, Toxic Bullets) can still be cleansed. Which
DoTs get cleansed is a deterministic Bernoulli started at `Skill.fight_phase`, so the overall score's spread fight
phases cleanse the first DoT in exactly that share of fights. Hero ability DoTs that schedule
their own ticks instead of using `Engine.dot`/`CastCtx.dot` are not purged. 13-17% of ranked players hold it from
27k souls up, so DoT builds (Decay, Toxic Bullets, burn abilities) were overvalued before.

## New mechanics: parry, summons, nearby enemies, movement (2026-10-15)

`deadsim/mechanics.py`, **on by default since 2026-10-16** (`mechanics.DEFAULT = Mechanics()`; it was off while the
step 3 searches ran). Turn off per fight with `duel(a, b, mechanics=None)`, or for everything with
`deadsim.mechanics.DEFAULT = None`. The dummy in `time_to_kill` doesn't run, parry or time Counterspell, and the
survival search runs with movement off (an escape would count as surviving). With it on, `hero_default_skill` landing factors switch to
`data/landing_rates_mech.json` (refit with the mechanics on; median factor x0.97, McGinnis turret x2.3).
Real data: 600 ranked matches (badge 60+, 2026-10-10..13) with full damage matrix and 1 s position/health tracks
(`scripts/mechanics/fetch_mech.py`); every number below is in `validation/mechanics/`. Damage-matrix arrays are
right-aligned (shorter arrays start later); the scripts align them. Ability damage in the matrix barely drops with
Spirit Resilience (-8% for 30% spirit resist), so before/after effects of defensive items are weak and noisy.

| Mechanic | Model | Fitted to | Real | Sim |
|---|---|---|---|---|
| Parry | defender parries `Skill.parry_rate` of incoming heavy melees: attacker stunned 2.75 s, +25% damage taken | team Parry Success vs enemy melee hits (800 teams) | 5% of hero melees parried (90% CI 2.7-7.5%); 75% of parries are vs troopers | 15% of heavies = 5% of melees |
| Rebuttal | on parry: heal + return the parried damage, +30% damage 6 s; holders parry 1.9x | parries per 3 min, holders 0.88 vs 0.47 | 0.06% of hero damage, 45 dmg per 3 min held | 0.02% (underrated ~3x) |
| Counterspell | spell parry timed vs `spell_parry_rate` of enemy aimed casts, blocks that cast for 0.8 s | same-player before/after buying, vs teammates | ability damage taken -4.6% (CI -6.4..-2.6); +50 HP alone explains ~4% (Extra Health -8%) | -2% (rate 0.05) |
| Turrets | McGinnis turrets have HP (100 + 9/boon, 35% spirit resist); the enemy shoots them (see "Targetable summons" for the fit, 2026-10-24) | replays | | turret damage -15%, landing 0.06 -> 0.14 |
| Split Shot | during the active each landed shot adds 2.8 copies on the main target (+ nearby enemies) | Split Shot dmg / gun dmg of holders | 0.271 | 0.266 |
| Ricochet | bounces 65% of each gun hit to `Mechanics.extra_targets` nearby enemies (booked as splash) | Ricochet dmg / gun dmg of holders | 0.150 = 0.23 bounces per hit | `extra_targets=0.23` gives 0.145 |
| Escape | below `flee_hp` (0.15) and losing, a fighter stops shooting and runs (sprint after 2 s, dashes); the other chases 85% of the time; escape at 40 m | isolated 1v1s where one side drops below 25% HP (11,720 episodes) | 20% escape, 80% die (of decided) | 21% / 79% |

Escape effect of each item (change in escape share; real is adjusted for hero and 5-min game-time bin, n holders in
brackets; sim adds the item to real builds; base rate 20%):

| Runner item | Real | Sim | Enemy item | Real | Sim |
|---|---|---|---|---|---|
| Warp Stone (312) | +6.5 | +5.3 | Slowing Hex (657) | -1.6 | -4.2 |
| Fleetfoot (753) | +6.0 | +3.5 | Mystic Slow (88) | -4.6 | -4.2 |
| Sprint Boots (335) | +5.6 | +2.5 | Slowing Bullets (77) | -2.7 | -2.4 |
| Enduring Speed (1426) | +3.3 | +3.9 | Cold Front (572) | -0.4 | +0.3 |
| Dispel Magic (690) | +2.8 | +1.6 | Arctic Blast (174) | +1.9 | -1.8 |
| Stamina Mastery (653) | +2.6 | +6.1 | Phantom Strike (62) | -3.1 | -1.7 |
| Extra Health (721, control) | +2.5 | +3.2 | Knockdown (119) | +1.0 | -1.7 |
| Ethereal Shift (45) | +1.2 | +1.2 | Lifestrike (506) | +0.3 | -0.6 |
| Extra Stamina (429) | +0.1 | +1.7 | | | |
| Kinetic Dash (256) | -4.4 | +0.7 | | | |
| Magic Carpet (33) | +14 | +19 | | | |
| Majestic Leap (110) | -15 | +2.5 | | | |

Standard error of the real numbers is about 1.5 pts at n=700, 2.3 at n=300, 4 at n=100. Two fixes came from this table:
Majestic Leap first had an escape leap (sim +74 pts) but real holders escape *less*: it is an engage tool, so it keeps
only its barrier. Warp Stone's full 11 m teleport gave +23; only 30% of it counts as distance (`WARP_AWAY`).

What the new mechanics change on real build pairs (1,138 duels, `impact.txt`): 11% of duels now end in an escape
(no winner), 86% of results are unchanged, 1% flip winner; speed unchanged (~12 ms per 30 s duel).

Limits: parry misses (as frequent as successes) cost nothing; light melees are never parried. McGinnis' sim gun
share stayed ~3% vs 26% real even with every shot on turrets, so her gap is elsewhere (Heavy Barrage locking the gun
at fight start, the fresh-cooldown bias). Summon targeting is now fitted to replays (next section). Nearby enemies only feed Ricochet and Split Shot (AoE abilities already carry
team-fight hits in their landing factors); splash damage never kills anyone and is reported apart
(`FightResult.a_splash`). Hero mobility abilities (grapples, teleports, flight) are not modeled; only items, base
speed, sprint and stamina. Fighters hold their distance unless someone runs, so melee gap-closing is still unvalued.
Ability slows are applied generically from SlowPercent-type properties at spirit accuracy. Real escape episodes are
"no teammate and exactly one enemy within 25 m", which is closer to a 1v1 than a team fight but not the same.

## Targetable summons (2026-10-24)

Which summons can be hurt, and how much enemies go for them, from 160 Phantom+ replays (Oct 20-24, Deadlock API demo
queries; `scripts/summons/fetch_summons.py` pulls each summon entity's spawn, despawn and health plus every hit on it,
`summon_stats.py` -> `validation/summons/summon_stats.json`). A summon counts as killed when the hits on it add up to
its health (the extracts leave `victim_health_new` empty).

Only these summons have health in the replays: Graves' zombies and Ghouls (`CNPC_NecroSkele`, 212 HP at 0-5 min to
~430 late = 180 + 8/boon), Deadheads (24 -> 62 HP = 20 + 1.3/boon), the Borrowed Decree gravestone (100 HP) and
McGinnis' Mini Turrets (131 -> 406 HP). Sinclair's Spectral Assistant, Medicinal Specter, Rat King's banner, The Cube
and Nurse Harrow's leeches sit at 1 HP and never take hero damage; Solomon's pieces, Grey Talon's owl model and the
Goo Ball have none; Rat King's rats (100 HP) and Rem's Helpers are never hit. Vindicta's crow is a projectile, not an
entity with health. So Graves and McGinnis are the only heroes whose summons the sim lets the enemy shoot.

| Summon (n, matches) | Real life (s, median) | Killed by an enemy hero (all / of those a hero hit) | Gun share | Non-gun ratio |
|---|---|---|---|---|
| McGinnis turret (8,199, 43) | 10.5 | 29% / 71% | 0.57 | 0.60 |
| Graves zombie / Ghoul (16,616, 99) | 9.3 | 28% / 58% | 0.67 | 1.15 |
| Deadhead (21,541, 99) | 8.6 | 40% / 90% | 0.50 | 0.14 |
| Gravestone (1,171, 99) | 17.8 | 20% / 83% (median 11 s after landing) | 0 (bullets never hurt it) | 0.05 |

Gun share = enemy gun damage on summons of that kind / (that + enemy gun damage on the owner), while one is alive.
Non-gun ratio = enemy non-gun damage (abilities, items, melee) on them / non-gun damage on the owner in the same
windows: 63% of what turrets take and 72% of what zombies take is area damage, not aimed shots.

Model (`deadsim/mechanics.py`, `data/summon_targeting.json`, refit with `scripts/summons/fit_targeting.py`):
- Each summon has its data health (+ boons). The enemy spends `focus` of its trigger pulls on the oldest living
  summon of each kind, at `acc_mult` x its hero accuracy (assumption: stationary turret 2.5x, walking zombies 2x,
  small flying Deadheads 1x). `focus` is fitted so the sim's gun share matches the real one, over duels of every
  sample McGinnis and Graves player against a real enemy build: turret 0.48, zombie 0.53, Deadhead 0.69.
- Non-gun damage the owner takes also lands on every living summon x its kind's `splash`, fitted the same way
  against the damage all summons of a kind take (turret 0.29, zombie 0.48, Deadhead 0.03, gravestone 0.05). Area
  damage is most of what zombies take in the replays.
- The gravestone can't be shot. Besides splash the enemy breaks it 11 s after it lands, 83% of the time (the real
  rate among gravestones a hero hit), as an expected value: from then on zombie spawns and the aura are scaled by
  0.17 (a single deterministic draw would break it in every fight). Once it is gone no more zombies spawn and the aura stops: in the replays zombie
  spawns drop from 0.46/s to 0.14/s after a gravestone breaks.
- A summon lives at most the real median life of those no hero killed (`life_other_s`: turret 12.8 s, zombie 10.5 s,
  Deadhead 11.1 s, gravestone 18.6 s): troopers and other heroes kill them in real games. Zombies used to live a fixed
  4.5 s (`ZOMBIE_LIFE`, still the value with mechanics off).
- `Skill.summon_focus` (default None) overrides every kind's share; `FightResult.*_summon_kind`,
  `*_hit_while_summon` and `*_summons_out` report what the fit compares.

Fit result (sim vs real): gun share turret 0.57 / 0.57, zombie 0.67 / 0.67, Deadhead 0.47 / 0.50; non-gun ratio within
0.01 for all four. Kill shares in the sim (of all summons spawned in a duel) are turret 61%, zombie 39%, Deadhead 32%
against 71% / 58% / 90% of real ones a hero hit (the gravestone's break is the expected value above). The sim spreads area damage evenly over every
summon, while real damage piles onto a few (a real Deadhead that gets hit at all almost always dies at 50 HP).

Effect on the 252 Graves and 90 McGinnis sample duels (real builds, 30 s): Graves' damage per second -1% (275 -> 271),
win share 69% -> 75% (zombies now live up to 10.5 s instead of 4.5 s and soak shots); McGinnis -18% (65 -> 53), 7% ->
6%. McGinnis' landing factors were not refit: her sim damage mix with mechanics on already matches (turret 45% of her
damage vs 44% real). Graves has no landing factors (his gun
records no accuracy in the data), and his ability mix moved: Borrowed Decree 30% -> 39% (real 29%), Jar of Dead 29%
-> 24% (real 23%), Grasping Hands 28% -> 24% (real 11%); his gun stays at 4% vs 18% real.

## Hero fight patterns (2026-10-16)

Before this the sim cast every ready ability in slot order (1, 2, 3, ult). `deadsim/patterns.py` now gives each hero its
real combo from `data/fight_patterns.json` (on by default; `Skill(fight_pattern=False)` restores slot order):
`order` (cast priority), `ult_after` (the ultimate waits for one of these setup casts, at most 4 s) and `prefight`
(an ability used before the fight; only Mo & Krill have one: Mo arrives under Burrow and spins on the target at t=0,
Burrow's cooldown already running). Each hero file's own conditions (range, health thresholds) still apply.

Sources, scripts in `scripts/fight_patterns/`:
- **Replays** (`fetch_replays.py`, `replay_openers.py`): 158 Phantom+ replays (Oct 13-16) through the Deadlock API demo
  queries (ability cooldown starts = casts, hero-vs-hero damage events). A fight is hero damage to or from the hero
  with gaps under 8 s and at least 300 damage; 235 to 3,719 fights per hero. `order` ranks the abilities cast in at
  least 10% of fights by which usually comes first; `ult_after` lists abilities cast before the ultimate in at least
  60% of fights with one. Per-hero numbers are in each row's `replay` block.
- **Movement** (`fetch_paths.py`, `path_openers.py`): match_paths of 300 Phantom+ matches. Engage abilities show up
  as ability movement at 25-37% of fight starts for Abrams, Kelvin, Vindicta and Grey Talon. Burrow is not flagged
  as ability movement there, so Mo & Krill come from the replays.
- **Guides** (`guide_order`, `engage`, `ult`, `holds`, `notes`, `sources`): web summaries; most guide pages could not
  be opened, so they are reference only. The replays overrule them where they differ, e.g. Seven opens with Power
  Surge rather than Static Charge into Storm Cloud.

Check against the real damage mix (`fit_check.py`, mechanics on): a replay combo is used only when the sim's damage
mix with it fits the real damage matrix within 0.05 of slot order (mean |log landing factor|). Haze, Yamato,
Sinclair and Apollo fit worse with their real order, which points at gaps in those ability models, so they keep slot
order for now. The ultimate stops waiting for its setup when no setup ability is off cooldown, when either side is
below 30% health, or after 4 s. Landing factors were refit for every hero whose fights changed
(`scripts/refit_landing_heroes.py`). `tests/test_patterns.py` pins a few duels with patterns on.

Mo & Krill: Mo is underground when 26% of all fights start, 36% after laning (47% have a Burrow cast in the 10 s
before the first hit), 9-24% in lane. So "most fights" holds for committed mid-game engages more than for lane
trades; the sim models the committed engage. With it, Mo's 5 s damage on a dummy is ~14% higher at 18k souls.
Biggest 5 s damage changes elsewhere at 18k: Venator -26% (Snap Trap before Consecrating Grenade), The Doorman -21%
(Call Bell first), Pocket +10%, Mirage -7%.

Imbue target: with patterns on, imbue items go on the ability real players imbue (`imbue` in fight_patterns.json,
`scripts/fight_patterns/replay_imbues.py`). Quicksilver Reload's bonus is its own damage event on the same tick as the
imbued ability's hit, so each Quicksilver hit names the ability. 12 heroes have enough hits (20+ in 3+ matches); 6
differ from the old "highest base damage" pick: Mo & Krill Scorn (not Burrow, 99.8% of 1307 hits), Infernus Napalm,
Vindicta Crow Familiar, McGinnis Mini Turret, Warden Alchemical Flask, Graves Jar of Dead. An explicit
`Loadout.imbues` still wins.

Imbue evidence also comes from Mercurial Magnum's charge hit (same tick, 40+ damage) and Mystic Reverb's echo
(194 ticks after the triggering hit). Picks need 20+ votes in 3+ matches and an 80% majority. 18 heroes qualify;
9 differ from the old default (also Paradox Kinetic Carbine, Yamato Power Slash, Deadman Danny Chimera Mk1).

Imbue item fixes (2026-10-16):
- Mercurial Magnum's bullet bonus is "+X% Base Bullet Damage" (X = 20 + 0.38 x Spirit Power), not X flat damage.
  Replays: each proc is ~0.4-0.55 x the hero's base bullet damage (Wraith median 4, Warden 11, Holliday 31). The sim
  gave ~10x that; its real-data factor goes from 0.18 to 0.83 after the fix.
- Mystic Reverb's 22% imbued lifesteal never applied: it was added as a 0.01 s mod after engine.damage had already
  applied lifesteal. It now heals on the hit. Its real/sim damage factor drops from 6.5 to 3.6 with the replay imbue
  targets (the rest is its 16 m echo hitting other heroes in team fights).
- data/item_landing.json was refit on the current sim (fight patterns and these fixes); other factors moved by up to
  ~0.1 except Cold Front (2.1 -> 1.7).
- Frostbite Charm and Omnicharge Signet (cost 9999) appear in no real builds and are not modeled.

Scorn healing: Mo's health jumps by 1.20 x (Scorn + Mystic Burst + Quicksilver Reload damage) on the tick Scorn lands
(two Phantom+ replays, pawn health vs same-tick damage events), so Scorn's heal now counts the item procs its hit sets
off. With Mystic Burst + Quicksilver on Scorn at 18k souls, Mo heals 26% more in a 30 s duel vs Abrams (974 -> 1227).

## Haze duels and a real 1v1 benchmark (2026-10-21)

Tyler: the popular Haze build won only 28% of 27k Phantom+ duels, though Haze is a duelist. Findings:

- **Real benchmark** (`analysis/scripts/isolated_kills.py`, out: `analysis/out/isolated_kills.json`): Phantom+
  ranked, 7 days, 21.8k matches. An isolated kill has no other hero death within 15 s; only kills where killer and
  victim net worth are within 10% count (the sim gives both sides the same souls). Haze's share is 0.58-0.62 with no
  net worth filter (5th of 41) but 0.50-0.52 at equal net worth (net worth interpolated between the 3 min snapshots): most of her real edge is out-farming.
- **Gun stayed idle after a cut-short channel** (all heroes): `gun_tick` slept until the lock time it saw, so when a
  channel was interrupted (Bullet Dance stunned, Warden/Dynamo/Kelvin/Bebop/Forge/Shiv channels ended early) the
  gun stayed silent until the old lock end. It now re-checks every `GUN_POLL` = 0.1 s. Haze vs Venator: she was
  silent from 1.6 s (stun over) to her death at 4.3 s.
- **Bullet Dance landing (0.11) cut its damage but kept the full 3.9 s gun lock**, so the ult cost Haze more gun
  damage than it dealt. The factor now shortens the channel (`gun_volley(..., landed=True)` skips the damage scale).
- **Fixation's landing 0.36 was a calibration artifact:** in the calibration duels a full Bullet Dance (perfect
  accuracy) built Fixation stacks, so Fixation looked 2.5x too strong. `landing_rates.py --iterate` fits with the
  current factors applied (`refit_landing_heroes.py --iterate N`); Haze converges to Fixation 1.0, Bullet Dance
  0.17, Sleep Dagger 0.64. Iterating every hero moves many factors (some oddly: Strix Salvo 0.67 -> 0.04, Soul
  Exchange 1.2 -> 2.2) and barely changes the cross-hero fit, so only Haze was refit.
- **Sleep Dagger** now wakes on any damage the sleeping target takes (DoT ticks included), via the new
  `on_any_damage_dealt` ability hook.
- Popular Haze at 27k: 28% -> 35% (18k 39%, 37k 44%).

**Still open, all heroes:** sim duel win rates of the popular builds don't correlate with the real equal-net-worth
isolated-kill shares (Spearman ~0 at 27k). The sim overrates Lady Geist (0.89 vs 0.38 real), Shiv, Deadman Danny,
Silver, Venator, Apollo, Infernus, Seven and underrates Vindicta, Mina, Calico, Wraith, Vyper. Giving ultimates
only their real cast share of fights (15-35%, `fight_patterns.json` replay `cast_share`) did not help (tested,
not kept). The real shares carry gank noise (spread 0.30-0.66 vs sim 0.10-0.91), so check single heroes first.

## Range spread (2026-10-21)

Tyler: range changes all the time in a fight while each hero tries to play at its ideal range. `mechanics.range_drift`
(on by default) models it.

**Real data** (`scripts/range/fetch_paths.py`, `fit_range.py` -> `data/fight_range.json`): 400 Phantom+ matches,
match_paths (1 s positions). A fight second = player in hero combat with the nearest living enemy within 40 m, also in
hero combat; 1v1 = no other enemy or teammate within 25 m. Over 133k 1v1 seconds the distance is lognormal-like around
the hero's median (p25 8.5 m, median 16.2, p75 25.6). A log-distance variogram over 1,766 segments of 10+ s fits an
Ornstein-Uhlenbeck process with log sd 0.76 and time constant 2.1 s: about half to twice the median, re-drawn every
few seconds. Per hero the spread is similar (log sd 0.65-0.87), so one global value is used. Heroes' medians differ
(Billy 10.6 m to Rem 23 m) and both fighters' preferences set a duel's range (fit weights 0.69 own, 0.51 enemy).

**Sim:** the hero's calibrated distance (`skill_defaults.json`, mean of both heroes in duels) is the median, and every
distance effect is the expectation over the spread (`Engine.p_within`, `spread_mean`, `reach_ready`):
- gun falloff and headshot crit bonus: averaged over the spread (crit jointly with falloff);
- Close Quarters / Point Blank and Long Range / Sharpshooter: bonus x share of time inside / outside their range;
  Torment Pulse, aura ticks, Hunter's Aura: x share of time in radius; Stalker and Restorative Locket procs at that rate;
- ability reach (`CastCtx.within`): cast at once, damage x cooldown / (cooldown + expected wait), where the wait is
  walking in when the target is in the 5 m walk-in band and drift time (tau / P(in reach)) beyond it. Range items
  shorten the wait, smoothly. Item actives with a reach (Alchemical Fire, damage actives) wait the expected time.
A single random distance path was tried first and dropped: in a 30 s fight with 8-10 s cooldowns a fraction of a
second decides a whole extra cast, so an item's value on one path swung by +-200 damage (Greater Expansion on Mina:
mean +35, sd 200 over 12 paths). Melee keeps its fitted per-second rate; escapes still move the distance.

**Checks:**
- Real bullet-hit distance histogram ("Outgoing Bullet Dist", creeps included) vs the sim (`range/bullet_dist_check.py`):
  share of hits at 0-10 / 10-20 / 20-30 / 30-40 m is real 0.35 / 0.35 / 0.19 / 0.07, fixed distance 0.17 / 0.79 /
  0.04 / 0, spread 0.34 / 0.33 / 0.16 / 0.17 (the 40 m cap piles the far tail into the last bucket).
- Damage mix (`range/drift_check.py`, each model with its own refit landing factors, `range/refit_landing_drift.py`):
  mean |ln(real/sim)| of ability and melee vs gun ratios 0.073 fixed, 0.076 spread: the same, landing factors absorb
  the average.
- Tradeoff: the spread is not better calibrated than the fixed distance on damage mix (landing factors absorb the
  average either way); what it buys is smooth item values and radius/range items that pay part of the time (item share
  error down, Torment Pulse right). The ability wait `tau / p` is a heuristic, not the OU first-passage time; at
  p near 0 it drives an ability's damage factor towards 0 where fixed distance never cast it.
- Item share of all hero damage (24 items above 0.1%): mean |ln(sim/real)| 0.48 fixed -> 0.42 spread. Torment Pulse
  0.42% -> 1.04% (real 1.12%), Cold Front 0.25% -> 0.49% (real 0.41%); Stalker overshoots (0.48% -> 1.21%, real 0.64%).
- Popular 27k builds on the dummy: median 30 s damage -7% (Lady Geist -26%, Deadman Danny -25%; Vindicta +24%, Victor +22%,
  Calico +15% from Torment Pulse / close-range items). Item value on the dummy (median over heroes): Close Quarters
  +24 -> +80, Sharpshooter +316 -> +320, Long Range +197 -> +154, Point Blank +316 -> +296. Close/long range bonuses use
  the joint expectation with falloff (`Engine.band_corr`): paid where the target actually is, not at the average falloff.

## Known gaps (not yet modeled)

- **Melee movement:** melee is in fights and its rate follows the build (see "Melee" above). Melee Charge's lunge
  and Lifestrike's slow only count in chases (movement on); there is no positioning AI that dives in to melee, and
  the light/heavy split (30% heavy) is an assumption.
- **Distance:** the fight distance spreads around the hero's median (see "Range spread") as an average, not a path: there is no positioning AI (kiting to stay at range, diving with a gap closer), and ability effects inside a cast still check the median distance. Hero range checks follow the spread: cast gates through `CastCtx.within` (engage margin + walk-in) or `CastCtx.reach` (hard reach; self buffs keep the median check, since the expected wait only scales damage), in-effect radii (Frank's revive blast, Kelvin's heal, Unicorn's barrier pop, Gigawatt's storm, Ghost's tether) scale damage, heals and stun/silence durations by `CastCtx.p_in` with no cutoff at the median (the tether breaks only at p = 0), Haze's Fixation bonus and McGinnis' turret falloff average over the spread. Still at the median: melee reach (Drifter's bonus melee, Billy's Bashdown melee), Drifter's vision check (a self buff) and Paige's distance amp (scales with distance travelled). Short-range ultimates use per-hero "approach" constants to be cast.
- **Summons:** Graves' and McGinnis' summons can be shot and splashed (see "Targetable summons"); real enemies also
  hit them with area abilities aimed elsewhere, which the sim folds into the splash share. Accuracy on summons is an
  assumption. McGinnis is still the worst-matched hero (gun share 2% vs 26% real), for reasons other than turret uptime.
- **Paradox Kinetic Carbine** damage formula is a low-confidence reading of the data (landing 2.95).
- **Bebop Hyper Beam** dominates any 20 s duel that starts with it ready (landing 0.06); the model matches the
  data, the gap is the fresh-cooldown bias above. (Haze Bullet Dance: fixed 2026-10-21, see "Haze duels" below.)
- **Multi-target items** (Ricochet, Split Shot) do nothing in a 1v1 without mechanics; see above. Deadman Danny's charged primary fire is
  modeled as a plain gun.
- **Attribution:** the game books amp bonuses (Escalating Exposure, Express Shot, Siphon Bullets) under the item;
  the sim books them under the hit's source. This affects only the item-share comparison.
- **TTK:** sim 1v1 duels between real builds take a median 19 s (28 s with landing factors) vs 13 s for real
  deaths, which are mostly team fights with several attackers.

## Speed

About 9 ms per 20-second duel on one core (abilities and items on), after caching. Fine for thousands of fights;
the build search will want more.
