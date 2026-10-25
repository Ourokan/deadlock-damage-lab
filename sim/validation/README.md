# Combat model validation

How far the step 2 fight model (`deadsim`) can be trusted, checked against hand calculations and 400 real
ranked matches (badge 60+, current patch, 2026-10-13; `matches_sample.jsonl.gz`, 4,800 player-matches), and since
2026-10-24 against 600 Phantom+ matches (`phantom_sample.jsonl.gz`, see "Damage mix audit against Phantom+").

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
phases cleanse the first DoT in exactly that share of fights. 13-17% of ranked players hold it from
27k souls up, so DoT builds (Decay, Toxic Bullets, burn abilities) were overvalued before.

Per enemy source (2026-10-24, `counters/scripts/cleanse_real.py`, Phantom+, 2200 matches with a Dispel holder, 5400
Infernus windows): the same pairing for every enemy damage source, ratio = holders / teammates without Dispel.
Holders get shot more by Infernus (gun 1.16, Napalm 1.17), so read each source against those: **Afterburn 0.73
(0.63 of Napalm)**, **Toxic Bullets 0.70 (0.61 of Infernus' gun; 0.68 of gun from every dealer)**, Escalating
Exposure 0.72, Decay 0.80 of gun, Crow Familiar 0.86 and Fire Scarabs 0.87 of their owners' gun, Flame Dash's ground
trail 1.03 (not purged). Holders die 21% less to Infernus (kills per window 0.79) and 11% less to anyone. So players
spend Dispel on the DoTs an enemy's gun keeps re-applying, and much less on Decay. Model since then:
- Hero DoTs that tick on their own (Afterburn, Crow Familiar's bleed, Fire Scarabs) register with
  `CastCtx.dot_track` and stop on a purge (`dot_live`); before, Dispel could not touch them, so it had no value
  against Infernus (counter sim: -0.03 extra vs Infernus at 27k, +0.24 after).
- Build-up DoTs (Afterburn and Toxic Bullets, `buildup=True`) draw with `Skill.dot_cleanse_share_buildup`, fitted
  by `scripts/fit_dispel_buildup.py` to Afterburn / Napalm (`validation/dispel/buildup_fit_91.json`): the fit sits
  at its ceiling, 1.0. Even cleansing every one, the 30 s fixed-window duel removes only 25% of Afterburn (real 37%):
  Infernus re-ignites within seconds and Dispel has a 45 s cooldown, while a real 3-minute window holds several
  short fights (a 13 s duel removes 30%). So 1.0 is a lower bound, not a measured share, and Dispel's value
  against Infernus (+0.24 extra in the counter sim) is the most this model can give, still short of real. Other
  DoTs keep `dot_cleanse_share` (Decay fit). Only Phantom+ is measured, so every badge uses it.
- Toxic Bullets check (same duel design, 300 real (Toxic holder, Dispel holder) snapshot pairs, Toxic damage per
  gun damage, Dispel holder vs the same build without Dispel): 0.98 at the Decay share it had before, 0.92 at the
  build-up share of 1.0; real 0.68. So moving it to the build-up share goes toward real and still falls short. A
  Toxic Bullets build loses about 6% of its Toxic damage against Dispel holders (13-17% of players from 27k up).
- Dispel purges Afterburn's build-up meter too.

Counterspell, same pairing (`cleanse_real.py Counterspell`, 2200 matches, 62k windows): ability damage taken 0.965
for non-ultimates and 0.98 for ultimates vs gun damage 0.96 (Counterspell can't block guns): no measurable block.
Against Lash, the hero that triggers it most (x2.1): Death Slam 1.00 (CI 0.95-1.06), Ground Strike 1.00, Flog 1.00,
and holders die to Lash as often (1.03). A few slow-detonation abilities do drop (Sticky Bomb 0.82, Gloom Bombs 0.73,
Affliction 0.79 of gun), too few casts to move the total. `Skill.spell_parry_rate_ult` (new, ultimates) and
`spell_parry_rate` are fitted by `scripts/fit_counterspell.py` (`validation/counterspell/fit_91.json`, set by
`accuracy.spell_parry_rates` in `hero_default_skill`): both are 0 (was a hand-set 0.05), the grid floor: the real
targets (1.004 non-ult, 1.025 ult, against gun) sit above what a zero rate gives, so the fit clips there and its
"CI" is that clip, not a tight bound. The data says no measurable block, and Counterspell is worth its +50 HP and
spirit power. A parried cast stays blocked for
`mechanics.PARRIED_CAST_SPAN` (3.5 s), so a rate set by hand can block Death Slam, whose slam lands 2.6 s after the
grab (it never could before). So the sim's
verdict that Counterspell is the weakest defensive item per soul matches real Phantom+ play (win edge -0.8 points).

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
| Split Shot | during the active each landed gun bullet adds 0.73 copies on the main target and 0.73 x nearby enemies (at most 1) on others (replays; 2.8 x accuracy before 2026-10-24, see "Vyper") | Split Shot dmg / gun dmg of holders | 0.271 | 0.266 |
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

## Damage mix audit against Phantom+ (2026-10-24)

`scripts/damage_audit.py` checks the model as the searches use it (fitted landing factors, item factors,
counterplay, mechanics, melee by build) against a fresh sample: 600 Phantom+ ranked matches of the last 5 days
(`phantom_sample.jsonl.gz`, from `scripts/fetch_validation.py --api 91 5`, 5,115 player-matches). Each player's real
build and real aim duel a real enemy at 30/60/90% of the match; the damage mix (gun / abilities / items / melee) and
every source are compared with the damage matrix. It fits nothing. Output: `damage_audit.md` / `damage_audit.json`.
The sample now also keeps each source's cumulative damage at every damage-matrix sample (`damage_series`), so item
damage can be divided by the gun damage dealt while the item was owned.

Found and fixed:
- **Nurse Harrow** (347 player-matches, 3rd most played) had no landing factors and no melee rate: she is newer than
  the 2026-10-13 sample. Fitted on the Phantom+ sample (Leech Therapy 1.81 / 1.37 with mechanics, Lurking Terrors
  1.37 / 1.18, melee 0.03 hits/s). Mix distance 0.15 -> 0.09.
- **Silver's wolf form** (Go For The Throat, Mauling Leap, Tail Whack) had no landing factors: the game books them
  under their own classes (`ability_werewolf_frenzy`...), which the fit never matched (`landing_rates.ALIASES`). Fitted
  0.5 / 0.47 / 0.8. Mix distance 0.10 -> 0.02.
- **Sinclair's Audience Participation**: the game books the copied ultimate under the enemy hero's class, so the fit
  found no real damage and stored 0.0 (applied as 0.05), and the engine then skipped the factor because the copy is
  named "Audience Participation (X)". Real classes of other heroes now map to it (`landing_rates.COPY_ULT`) and the
  copy uses its factor (`Ability.landing_key`). Small sample (20), still 0.05 off.
- **Ability sub-sources skipped their landing factor**: the fit pools "Setup Bishop squares", "Ira Domini (blessed)",
  "Serrated Knives (rage)", "Mini Turret (wall)"... with their ability, but the engine applied the factor only to the
  exact ability name. With mechanics on, refits had pushed Setup Bishop to 0.02 and Ira Domini to 0.03 to make up for
  it. The engine now falls back to the ability's factor (`engine.damage`); Solomon, Venator, Celeste and Sinclair were
  refit from scratch on the Phantom+ sample. Celeste's Shining Wonder was 1.5 (clipped from 1.9) and is 0.5 now: real
  Phantom+ players get 0.4x of what the sim gave it.
- **Capacitor's shock** never fired for 40 s after its active: both shared one cooldown timer. Real/sim was 4.7, now
  0.99 (Ivy 0.105 -> 0.018, Wraith 0.061 -> 0.012).
- **Siphon Bullets** only lowered the target's max health, so a hurt target lost nothing. The game books the stolen
  health as damage (0.24 per gun damage for holders); the sim now deals it (item factor 0.38).
- **Melee Charge** damage was counted as melee by the fit (`sim_key` matched "melee" before item names).
- **Item factors** (`data/item_landing.json`) were biased low for items bought late: real item damage was divided by
  the whole match's gun damage, while the sim divided by gun damage of the duels holding the item. They also fought
  with abilities always landing, so on-ability procs fired too often. Refit with gun damage while owned and the
  searches' ability factors (`python3 scripts/item_landing.py 4 --sample validation/phantom_sample.jsonl.gz`; ability
  refits: `python3 scripts/refit_landing_heroes.py --sample validation/phantom_sample.jsonl.gz HERO ...`). Applied factors that changed: Scourge 0.63 -> 1,
  Lightning Scroll 0.71 -> 1, Quicksilver 0.86 -> 1, Phantom Strike 0.89 -> 1, Tesla Bullets 0.92 -> 1, Mystic Shot
  0.75 -> 0.91, Headhunter 0.75 -> 0.92, Mercurial Magnum 0.83 -> 0.89, Focus Lens 0.32 -> 0.59 (min holders 40 -> 30
  to keep it; 36 holders, low confidence), Stalker 1 -> 0.77, Capacitor 1 -> 0.95, Siphon Bullets 1 -> 0.38.

Result: the player-weighted mix distance went 0.069 -> 0.051, and no item with 30+ holders is now overrated by more
than 2% except Silence Wave (25 holders, 0.71). What is left in the table is mostly bookkeeping or team fights, not
1v1 damage:
- the game books amp bonuses under the item (Escalating Exposure, Express Shot, Rabbit Hex's amp; Melee Charge and
  Crushing Fists probably their melee bonus too), the sim under the hit. This is why Shiv, Paige, Kelvin, Seven, Victor
  and McGinnis show a lower item share in the sim;
- items and abilities that hit several heroes in team fights come out above 1 and are left alone: Mystic Reverb 3.9,
  Return Fire 3.9, Tankbuster 2.0, Arctic Blast 1.9, Ricochet (0 in a 1v1). Paradox (0.14) and Mo & Krill (0.12)
  are mostly this.
- Graves and Deadman Danny joined the audit on 2026-10-24 once their guns were calibrated from replays (next section).

### Area items' hits on other heroes (2026-10-24)

Mo & Krill's items were all 1.5-2.6x under real (holders only: Torment Pulse 1.87, Tankbuster 2.07, Cold Front 1.65).
Torment Pulse's uptime on the main target is right (real 45% of its pulses land on the fight's main target, sim
47% at his 10 m duel distance), so the gap is the other heroes. In 110 Phantom+ replays (every hero-vs-hero
DamageEvent, kept in the project folder analysis/work/replay_damage; `scripts/team/area_hits.py`) a fight's main
target is the hero who took most of the attacker's gun damage, and per item other / main = damage on every other hero
/ damage on the main target. Single-target gun procs (Toxic Bullets, Mystic Shot) give 0.44 from target switching
alone; an area item's extra hits per main hit is its other / main minus that:

| Item | other / main | extra hits per main hit | position count used before |
|---|---|---|---|
| Mystic Reverb | 1.24 | 0.80 | 0.41 |
| Alchemical Fire | 1.20 | 0.76 | 0.20 |
| Scourge | 0.95 | 0.51 | 0.07 |
| Torment Pulse | 0.89 | 0.45 | 0.06 |
| Capacitor | 0.74 | 0.30 | 0.20 |
| Arctic Blast | 0.71 | 0.27 | 0.21 |
| Cold Front | 0.67 | 0.24 | 0.07 |
| Tesla Bullets | 0.50 | 0.06 | 0.14 |

The position count (team_value.json "positions": other enemies within the radius at 1 s samples, at 27k) misses most
of it for items around the holder: most position fight seconds are approach and poke at 15-20 m, while these items
fire in the brawl. Torment Pulse's other / main is about the same for every holder (Mo & Krill 0.85, Celeste 1.05,
Graves 0.90, Victor 0.77), so one pooled value per item. `data/area_hits.json` (`mechanics.area_extra`) now gives
the overall search's area items their extra damage (position count as fallback) and the audit adds the same to the
sim's item damage. Item factors refit: Mystic Reverb 1.08 -> 0.60, Scourge 1.06 -> 0.70, Capacitor 0.90 -> 0.69,
Torment Pulse 1.33 -> 0.92, Alchemical Fire 1.61 -> 0.92, Cold Front 1.10 -> 0.89, Tesla Bullets 0.96 -> 0.90,
Arctic Blast 1.76 -> 1.38 (unused); every area item's holders-only real / sim is now 1.00-1.03 except Arctic Blast
1.41. In the search (at 27k), an item's value is its duel damage x factor x (1 + extra): Torment Pulse 1.06 -> 1.33
of its duel damage, Alchemical Fire 1.20 -> 1.61, Arctic Blast 1.21 -> 1.27, Cold Front 1.07 -> 1.10, Scourge
1.07 -> 1.06, Tesla Bullets 1.09 -> 0.95, Capacitor 1.08 -> 0.90, Mystic Reverb 1.41 -> 1.08 (the sim's echo on the
main target is too strong). Mo & Krill distance 0.100 -> 0.071;
Victor 0.047 -> 0.065 and Graves 0.091 -> 0.097 (their per-hero Torment Pulse share is now over real, the
whole-match vs mid-game duel bias); player-weighted 0.0446 -> 0.0445. The patch rerun does not refit area_hits.json
(it needs replay queries): rerun area_hits.py on fresh replays after a big patch, then item_landing.py, since the item factors were fitted with these extra hits in the sim.
The extra hits were first one pooled value per item, the same at every net worth; by fight start time they grew
later in the match (Cold Front 0.14 at 0-15 min vs 0.38 at 25+), so early Cold Front or Capacitor builds were
over-valued.

### Extra hits by game phase (2026-10-24)

150 more Phantom+ replays (matches of the validation sample where area items are bought before 20 min; 260 in all,
kept in analysis/work/replay_damage) and each fight's net worth (the match's mean player net worth at the fight's
start, from the sample's per-player stats). Too few area items are bought early to fit each item per phase, so one
phase curve for every area item: per net worth bin (own baseline), every area item's extra damage / what its pooled
extra_per_main predicts, made non-decreasing (pool adjacent violators), linear in ln net worth between bins, flat
outside. `mechanics.area_extra(name, souls)` = pooled value x curve; overall_search.area_damage passes the build's
souls, so the overall search, game paths (3k-50k stages) and lane fights use it. The audit still uses the pooled
value (it compares whole matches).

| fight net worth | 7.5k | 12.6k | 17.4k | 22.4k | 28.5k | 35.6k | 47.4k |
|---|---|---|---|---|---|---|---|
| observed / pooled | 0.21 | 0.72 | 0.93 | 1.24 | 1.07 | 1.11 | 1.15 |
| fit (95% band) | 0.21 (-0.17-0.58) | 0.72 (0.44-0.96) | 0.93 (0.68-1.10) | 1.12 (1.02-1.18) | 1.12 | 1.12 | 1.15 (1.09-1.45) |

The lowest bin is the weak point: its band includes 0 (no extra hits in lane) and reaches ~0.6, so 3k-7k builds' area value (0.21x pooled) is a soft estimate; everything from 12.6k up is clear of 0. A straight line in ln net worth fit worse (it put 0.57 at 7.5k): extra hits are low in lane, rise to ~1.1x by 22k
and stay. Pooled values with 260 replays: Mystic Reverb 0.99, Alchemical Fire 0.94, Scourge 0.62, Torment Pulse
0.48, Capacitor 0.26, Cold Front 0.19, Arctic Blast 0.18, Tesla Bullets 0.07 (110 replays: 0.80 / 0.76 / 0.51 /
0.45 / 0.30 / 0.24 / 0.27 / 0.06). Item factors refit with them (item_landing.py on phantom_sample): Mystic Reverb
0.60 -> 0.54, Alchemical Fire 0.92 -> 0.83, Scourge 0.70 -> 0.65, Capacitor 0.69 -> 0.72, Cold Front 0.89 -> 0.92,
others within 0.02; audit player-weighted distance 0.0445 -> 0.0446. Effect on an item's value in the overall fight
(vs no items, Abrams target): at 6k Cold Front (Kelvin) +0.30 -> +0.22, Capacitor (Seven) +0.57 -> +0.39, Torment
Pulse (Mo & Krill) +0.85 -> +0.69, Alchemical Fire (Infernus) +5.6 -> +3.5; at 10k 5-25% less; at 18k about the
same; at 27k+ slightly more. Rerun with fresh replays after a big patch: `python3 -I scripts/team/area_hits.py
<replay dirs> --write`, then `python3 scripts/item_landing.py 4 --sample validation/phantom_sample.jsonl.gz`
(its default sample is the old all-rank one).

## Guns with no hero accuracy: Graves and Deadman Danny (2026-10-24)

The match stats record no hero accuracy for Graves (The Teacher is a tether: Shots and Hits are always 0) and only
a partial count for Danny (Chimera Peace Bringer is a charged shot; the API counts about half the replay's hits), so
both fell back to the all-hero 26% and were left out of every fit. `scripts/gun_calib/` measures them in Phantom+
replays instead (Deadlock API demo queries, 70 matches of Oct 20-24 with one of them, 817 player-matches):

1. `fetch_guns.py` pulls one row per trigger pull (every weapon table's `m_nShotNumber` step), every hero-vs-hero
   `DamageEvent` and the API's final and per-3-min stats (`python3 -I fetch_guns.py WORK 70 4`; WORK holds the
   replay list `with_demo.json`, e.g. the summons one).
2. `gun_stats.py` counts per player shots, gun hits on enemy heroes (the hero's weapon ability id), headshots
   (`crit_damage` > 0), and shots inside fight windows (within W s of any damage between the player and an enemy
   hero). Gun damage is also taken back to base damage with the player's weapon power at that minute. Per-player
   rows: `validation/gun_calib/gun_stats.json.gz`.
3. `fit_guns.py` maps replay numbers onto the API's scale with the 395 reference players (one-bullet guns whose
   replay hits match the API's within 20%): API hero-aimed shots = 0.97 x replay shots in 4 s fight windows, with a
   per-player spread of 13% (the same ratio, 0.9-1.25, on all 29 reference heroes). Applied to Graves and Danny this
   gives their hero accuracy (`python3 scripts/gun_calib/fit_guns.py gun_stats.json validation/phantom_sample.jsonl.gz
   --write` -> `data/gun_calibration.json`, read by `hero_default_skill` / `default_distance` / `player_skill`).

| | accuracy p25 / p50 / p75 | headshots | base damage per hit | fight distance |
|---|---|---|---|---|
| Graves | 0.42 / 0.46 / 0.51 | none (the gun can't headshot) | 4.6 (sim 3.6 x 1.25, like any hero's hit) | 11.2 m |
| Deadman Danny | 0.24 / 0.28 / 0.34 | none recorded | 49.4 = 2.64 x an ordinary hit of his 15-damage bullet | 14.3 m |

- **Danny's charged shot:** every hit lands 2.64x the base damage of an ordinary hit (weapon power, headshots and
  resists out), and he fires about one shot a second while the data's gun fires four. The sim keeps the gun's base
  damage per second and fires 2.64x bigger shots 2.64x less often (`build.gun_quirks`, `charge_factor`), so on-hit
  procs fire as often as real hits. Each shot spends 2.64 rounds (clip 14 -> 5; replays show about 6 shots between
  reloads), so reload downtime stays the data gun's. Any headshot bonus is inside the factor.
- **Graves' tether** only attaches within MaxRange 20 m (the gun's own data). Beyond it a shot misses: no hit and no
  on-hit procs (`Engine.gun_reach` takes the out-of-range share of the distance spread off the hit chance; real
  Phantom+ Graves deal 2% of their bullet damage beyond 20 m). Inside it the tether has no distance falloff
  (`"falloff": false`, `Stats.gun_falloff`), see "Graves' hit damage" below. The fit's accuracy counts all his shots
  inside fights, so the out-of-range cut is taken relative to the fit distance (`Engine.hit_reach`, see "Mystic Shot
  and Torment Pulse by hero" below).
- **Patches:** the file records the gun it was fitted on (`fit_weapon`). If a patch changes either gun, the old fit
  keeps running and `build.gun_quirks` warns once per hero. Patch reruns can't refit, because that needs live
  replay queries: rerun `fetch_guns.py`, `gun_stats.py` and `fit_guns.py --write` by hand, then
  `refit_landing_heroes.py` for both heroes.
- **Cross-check:** a second, independent estimate (gun base damage per second of fighting over the gun's damage per
  second, scaled on the references) gives 0.51 for Graves and 0.27 for Danny, close to the shot-based 0.46 / 0.28.
  It is not used for the fit: its scale runs 0.5-2.3 between reference heroes (how much of a fight each spends
  shooting), against 0.9-1.25 for the shot count.
- **Landing factors** for both were refit on the Phantom+ sample with the calibrated gun as the anchor (Graves had
  none, so his abilities landed 100%): Graves Jar of Dead 0.23 / 0.25 with mechanics, Grasping Hands 0.09 / 0.10,
  Borrowed Decree 0.24 / 0.15; Danny Strix Salvo 0.44 / 0.40 (was 0.67 / 0.02), Chimera Mk1 0.33 / 0.29, Jettison Fuel
  0.47 / 0.40, Close The Deal 0.14 / 0.13.

Result on the Phantom+ audit: Graves' gun share 4% -> 18% (real 20%), mix distance 0.37 -> 0.18; Danny's gun share
25% -> 20% (real 16%), mix distance 0.37 -> 0.12 (audit table; Graves 0.16 there). Graves' damage items came out
about 2x real (fixed below); Danny's Express Shot and Tankbuster are the bookkeeping and team-fight cases above. The damage audit, ability fit and item fit now
include both heroes (`landing_rates.gun_known`).

### Graves' hit damage (2026-10-24)

Graves' on-hit items (Capacitor, Tesla Bullets, Mystic Shot, Siphon Bullets) dealt 0.42-0.51x real in the audit, as
a share of his gun damage. In the replays their proc rate per gun hit matches the sim's (Tesla 0.13 vs 0.14 per hit,
Capacitor about 0.2 like other heroes), so the hits themselves were off: the sim's Graves hit dealt 0.60x the real
one, while the other one-bullet guns sat at 0.8-1.6x (median 1.07; `scripts/gun_calib/hit_damage.py`,
`validation/gun_calib/hit_damage.json`). So he needed about 1.7x the real number of hits for his gun damage, and every
extra hit could proc. Two causes, both in the tether:

- the data's distance falloff (from 7.6 m, 50% by 17 m) cut the average hit to 0.64x at his 11.2 m spread. Real
  Graves hits show no such loss: their base damage per hit is 1.28x the data's, about the same as other heroes
  (1.25x), and 54% of his bullet damage lands at 10-20 m. The tether now has no falloff;
- shots beyond 20 m were 0-damage hits that still procced. They now miss.

Result: Graves' hit 0.60x -> 0.92x real. After refitting his landing factors (Jar of Dead 0.28 / 0.30 with mechanics,
Grasping Hands 0.11 / 0.12, Borrowed Decree 0.29 / 0.18), the Phantom+ audit gives: gun share 0.18 -> 0.20 (real 0.20),
items 0.43 -> 0.37 (real 0.27), mix distance 0.16 -> 0.10. Real/sim went from 0.51 to 0.73 for Capacitor, 0.46 to 0.70
for Tesla Bullets, 0.42 to 0.52 for Mystic Shot and 0.45 to 0.59 for Siphon Bullets. Pooled over all holders, Tesla
Bullets is now 0.98 and Capacitor 0.94. Build-up items (Toxic Bullets) scale their build-up by the landed hit's falloff
(`Engine.hit_falloff`, 1 on the tether): Toxic Bullets 0.95. Still high: Mystic Shot and Torment Pulse (about 0.55).

### Mystic Shot and Torment Pulse by hero (2026-10-24)

The audit's per-hero source table compares the whole real match (the early game without the item included) with
duels at 30/60/90% of it, so an item bought mid-game looks overrated there: Mystic Shot and Torment Pulse read about
0.5x on Graves. `damage_audit.py` now also writes **items by hero, holders only** (real gun damage between buy and
sell, at least 20 holders; `hero_items` in the json), which doesn't have that bias. Pooled over every hero neither
item is overrated (Mystic Shot 0.96, Torment Pulse 1.24). Per hero:

- **Graves** (0.61 / 0.63 holders only) came from a double cut. His fitted accuracy already counts the real shots
  he fires beyond the tether as misses, and the sim also took the out-of-range share off his hit chance. Now the hit
  chance is scaled by reach / reach at the fit distance (`Engine.hit_reach`, `Stats.gun_fit_m` = the calibration's
  median distance), so a fight at the fitted distance keeps the fitted accuracy. Landing factors refit (with
  mechanics: Jar of Dead 0.38, Grasping Hands 0.15, Borrowed Decree 0.23). Result: Torment Pulse 0.77, Mystic Shot 0.80,
  Tesla Bullets 0.83, Capacitor 0.73, mix distance 0.10 -> 0.08, gun share still 0.20 (real 0.20).
- **Paradox's Mystic Shot** is 2.6x under. In the replays, 73% of his Mystic Shot procs on heroes land together with
  a Kinetic Carbine hit, so the Carbine now procs it (`Hit.weapon_proc`). That barely moves the ratio, because his
  gun share is too high to begin with (0.34 vs 0.24 real), which deflates every item per gun damage. That is the
  Paradox mix gap, not Mystic Shot.
- **Calico and Yamato's Mystic Shot** (0.41 / 0.57, 30-35 holders) remain high. Their mixes match closely (distance
  0.03 / 0.02), and Mystic Shot is under 3% of their damage. Not fixed.
- **Torment Pulse** is under on melee-range heroes: Shiv 2.0, Mo & Krill 1.8, Celeste 1.45. That is team fights,
  since the 9 m pulse hits every enemy nearby and a duel has one.
- Found on the way: **Deadman Danny's Toxic Bullets** built up from his charged shot as if it were an uncharged one.
  Build-up now scales with the shot (`Stats.gun_charge`): 88x -> 3.7x under. The rest is probably his ability
  bullets building it up in the game.

### Paradox's gun share, charge-up items and item bookkeeping (2026-10-24)

Paradox had the worst mix in the audit (distance 0.14): gun 0.34 of his damage vs 0.24 real, items 0.10 vs 0.23.
His gun hit itself is about right after the early game (sim 27 vs real 25 per hit after 20% of the match, replays);
the gap came from five places, all checked in the 70 Phantom+ replays (`gun_calib`):

- **Time Wall** gave +30-65% weapon damage for its whole duration. Only ~3% more of his gun hits land well above his
  local median than for heroes without such a buff, so the bonus now reaches 10% of its uptime
  (`TIMEWALL_SHOOT_THROUGH`).
- **Kinetic Carbine** was ~0.55x its real hit late in the match and made up for it with a landing factor of 2.4,
  clipped to 1.5 in fights. A real Carbine hit is 10-17x his gun hit at every stage (96 at 0-5 min, ~470 at
  20-30 min), so its weapon scaling also follows the per-level bullet damage. It also charges for MaxChargeDuration
  (2.5 s, was 1 s): the gap from his previous gun shot to a mid-fight Carbine hit is mostly 2.5-6 s. Landing factor
  now 0.93 (mechanics 0.80).
- **Mystic Burst and Tankbuster** "charge up over time": each ability hit over the threshold releases what has
  charged since the last release, up to the full amount at 14 s (Mystic Burst median 2 after <1 s, 20 after 7 s,
  39 after 14 s+; Tankbuster 7 / 75 / 188), with releases 0.2-2 s apart on the same victim. The sim fired a full
  proc on a 14 s cooldown, so multi-hit abilities (Pulse Grenade's 5 pulses) got one proc where the game gives one
  plus a trickle. Item factors: Tankbuster 1.89 -> 1.44, Mystic Burst 1.52 -> 1.22.
- **Express Shot and Escalating Exposure** are booked under the item in the game's records (an Express Shot proc
  shot, 1-2 hits for one-bullet guns, the whole doubled burst for Paradox) and were booked under the gun / the
  ability in the sim, which inflated the sim's gun share for every holder and hid the items. `Engine.damage(book=)`
  and `Engine.booking` now book them the game's way. In the default mode only the label changes; in realistic mode
  (counterplay, the searches) the booked part gets the item's factor like an item's own damage, which cuts
  Escalating Exposure's amp to 0.54x (the sim's amp is ~2x what the game books). Express Shot fits 1.02 (pooled,
  Paradox 0.40), and factors above 1 are not applied, so it is unchanged.
  Landing factors refit for the holders (Paradox, Shiv, Paige, Viscous, Yamato, Kelvin, Victor, Seven, McGinnis,
  Infernus). Deadman Danny keeps his previous factors: the refit halved them and made his audit mix worse
  (distance 0.06 -> 0.09).

Result (on top of the Mystic Reverb fix, #59): Paradox gun 0.33 -> 0.27 (real 0.24), items 0.11 -> 0.24 (0.23),
distance 0.14 -> 0.06; Shiv gun 0.33 -> 0.29 (0.27), distance 0.12 -> 0.04; Paige 0.09 -> 0.04; player-weighted
mix distance 0.053 -> 0.045. Over a whole match
Paradox's hit is still 1.5x real in `hit_damage.json` because the duels sample later points of the match.

Still off then: **Vyper** (gun 0.55 vs 0.46), fixed below. **Nurse Harrow** (0.35 vs 0.29) is Lurking Terrors 1.5x
under. **Warden** is the other way (0.46 vs 0.52): Last Stand is overrated (0.66).

### Vyper: Mercurial Magnum, Split Shot, Petrifying Bola (2026-10-24)

Vyper's gun share was 0.55 (real 0.46) with Split Shot 2.8x and Mercurial Magnum 2.1x under real. Every hero-vs-hero
damage event of 84 Phantom+ replays (45 with a Vyper, the rest Mercurial or Split Shot holders;
`scripts/mechanics/split_shot_replays.py`, numbers in `mechanics/split_shot_replays.json`) showed three causes:

- **Mercurial Magnum's bullet bonus lasts its 12 s buff**, not until the next reload. 82% of a Vyper holder's gun
  hits after his first proc carry it (Wraith 79%, Warden 93%, McGinnis 93%), and Vyper empties a clip in 1.7 s, so the
  sim's "until reload" gave him 24%. With the 14 s charge and 12 s buff, ~86% is what the item allows.
  Mercurial procs also ride on Split Shot pellets (17% of Vyper's Mercurial damage) and Ricochet bounces.
- **Split Shot per landed bullet:** in the 5 s after an activation (614 activations: Vyper, Wraith, Yamato, Paige)
  the main target takes 0.73 Split Shot hits per gun bullet landed on it (Vyper 0.76, Wraith 0.59), other heroes
  0.29 of that. The sim gave 2.8 x accuracy copies per landed shot on the main target, a fudge for real players spending
  more of their gun damage inside the window, and its side hits needed accuracy x 0.5 x nearby per trigger pull.
  Now: SPLIT_PRIMARY_HIT 0.73 copies per landed bullet (they proc on-hit items, as real pellets do) and
  SPLIT_SECONDARY_COVER 0.73 x nearby enemies on others (at most one per bullet, for team fights), with ~0.29 other enemies within 13 m of the target
  (`mechanics.real_nearby`, the PR #57 position counts, now shared with the overall search). The active waits until
  the holder can shoot a target that can be hurt. Pooled over all 170 holders Split Shot is now 1.00x real (was 1.25).
- **Petrifying Bola went out at 0.7 s in every duel**, petrifying the target (and stopping Vyper's gun) for 2-3 s
  right inside Split Shot's window: the sim's Vyper landed 18% of his gun damage in Split Shot windows, real 41%.
  Real bolas land a median 4.1 s into a fight (quartiles 0.7 / 9.9 s); with a target health gate (BOLA_CAST_HP 0.9)
  the sim's median is 4.4 s (1.3 / 9.6 s). It is thrown anyway BOLA_MAX_WAIT (10 s) in, for a target healed back up.

The audit now fights with the real nearby-enemy count (`Mechanics.extra_targets = real_nearby("extra", 13 m)`, as
the overall search does) and counts Ricochet / Split Shot hits on those enemies, since the real damage matrix has
every enemy hero: pooled Ricochet goes from 0 (nothing to bounce to) to 0.88x real. Item factors refit
(`item_landing.py --sample phantom_sample.jsonl.gz`): Mercurial Magnum 0.90 -> 0.83, Ricochet now 0.88, Split Shot
0.92 (was 1.24, unused). Vyper's landing factors stay: a Phantom+ refit (`refit_landing_heroes.py`) cut Lethal Venom to
0.57 and made his audit mix worse (0.070 -> 0.087).

Result: Vyper distance 0.092 -> 0.067 (gun 0.52, Split Shot holders 1.64x real, was 2.84; Mercurial 1.21x, was
2.15), Haze 0.062 -> 0.044, Warden 0.084 -> 0.076; player-weighted 0.0450 -> 0.0446. Counting
Ricochet raises Wraith (0.012 -> 0.025), Mirage and Nurse Harrow a little: their per-hero Ricochet share is now above
real, the whole-match vs 30/60/90% duel bias for a mid-game item (holders-only Ricochet is 0.88). Vyper's remaining
Split Shot gap is the window share: real fights put 41% of his gun damage in its 5 s, the sim's 20 s duels 27%
(all holders 33%; Vyper 18% before the Bola fix).

## Fight length (2026-10-24)

Real fights are shorter than the sim's duels, and they mostly end without a death. `Mechanics.fight_length` (off by
default; on in the damage audit, the landing corrections and the overall search) books every hit also x P(a real
fight is still going at its time).

**Real data** (`scripts/fight_length/fetch_fights.py` -> project folder `analysis/work/fight_length/raw`,
`fit_length.py` -> `data/fight_length.json`): every hero-vs-hero DamageEvent with the victim's health after the hit,
from the 260 Phantom+ replays of the validation sample. A fight = damage between two enemy heroes, either way, with
no gap over 5 s, at least 4 hits and damage both ways (what a duel stands for; 67% of all hero damage). Of 66.7k
fights 16% end in a death (a hit to 0 health); median length 6.6 s. The sim already ends a duel at a death, so the
curve is the Kaplan-Meier survival of the disengage time with deaths censored: S(5 s) 0.69, S(10) 0.33, S(20) 0.06,
median 7.5 s, mean 9.0 s to 30 s. By game phase (fight net worth = the two heroes' mean; lane < 10k, late > 27k)
it barely moves: mean 8.5 / 9.4 / 9.4 s. Per hero (the hero's fights, either side) means run 0.78-1.38x the pool; not
used (a pair's length is both heroes'). The gap sets the scale: 3 s gives mean 6.9 s, 8 s 11.6 s; counting
one-way runs too (91% of hero damage) 7.0 s. 5 s is about a reload plus a reposition.

**Sim:** `Engine.length_w(t)` interpolates the phase curve (`mechanics.real_length(souls)`); `Fighter.dmg_exp`,
`healed_exp`, the splash and `FightResult.a_exp` carry the expected values, `dmg_out` stays the fight's own (items
and abilities that read it are unchanged), and the booking alone leaves the fight as it was (to a death or max_time). The landing corrections below do move
the fight: abilities and items land at the corrected rate, so kill times, `time_alive` and `survived` shift with them.
A single
random cut was not used for the same reason as the range spread (whole casts would swing results). The disengage is
taken as independent of the fight's path (real players back off more when losing: not modeled).

**Landing factors:** the ability (`landing_rates_mech.json`) and item (`item_landing.json`) factors were fitted with
every hit of a 20 s duel in full, so they had absorbed the average effect of shorter fights. `length_factors.py`
gives each row a `length_corr` = (sim source / gun in full) / (the same expected), from the audit's duels, iterated
3 rounds (fighting with the corrections moves kill times and procs). `accuracy.ability_length_corr` /
`item_length_corr` apply them only to fights with `fight_length` (`make_fighter`), so the dummy page and the other
full-booking fights keep the fit as it is. Median ability correction ~0.7: under real lengths an opener counts for
more of a fight, so the same real share needs a lower factor (Vyper Lethal Venom, a ramping DoT, x1.97; Silver's
Boot Kick x0.48). Items: Toxic Bullets x1.5, Escalating Exposure x1.3 (stacks build late), Split Shot x0.58, Cold
Front x0.50 (fight openers). Rerun it after any landing refit (`item_landing.py` keeps the old corrections).

**Also fixed:** Mystic Burst / Tankbuster's MinimumDamage and Witchmail's DamageThreshold checked the hit after the
ability landing factor and reach availability, which stand for hits landing less often, not smaller hits; low-factor
abilities (The Doorman, Rem) never procced them. They now check `amount / Hit.landing`. Alone (full booking):
Tankbuster holders' real/sim 1.44 -> 1.10, Mystic Burst 1.22 -> 1.09, per-hero item median |ln| 0.268 -> 0.242, The
Doorman 0.167 -> 0.102.

**Checks** (600-match Phantom+ audit, `scripts/damage_audit.py`; `--no-length` books in full):
- Damage over time into a fight (`scripts/fight_length/profile_check.py`), share of fight damage per 2 s:
  real 0.32 / 0.20 / 0.15 / 0.11 / 0.07 / 0.05; sim expected 0.31 / 0.24 / 0.13 / 0.11 / 0.08 / 0.05; sim in full
  0.16 / 0.14 / 0.09 / 0.10 / 0.10 / 0.09. Not fitted: the rate per fight still going (opener = 1) is real 1.00 /
  0.70 / 0.64 / 0.60 / 0.59, sim 1.00 / 0.88 / 0.58 / 0.64 / 0.66 (the sim's opener lasts a little longer).
- Damage mix, player-weighted distance 0.0446 (main) -> 0.0448 (min-damage fix) -> 0.0403 (fight length), hero mean
  0.0527 -> 0.0511 -> 0.0501; holders-only items pooled median |ln real/sim| 0.08 throughout (the corrections keep
  them); per-hero items 0.268 -> 0.242 -> 0.260 (the corrections are pooled over heroes, a hero who opens with an
  item more than most moves away: Rem's Tankbuster). Most improved: Nurse Harrow 0.088 -> 0.013, Mo & Krill 0.085
  -> 0.047, Graves 0.098 -> 0.060, Lash 0.034 -> 0.016; most worse: Rem 0.039 -> 0.100 (Tankbuster, Decay), Calico
  0.030 -> 0.059, Yamato 0.059 -> 0.081.
- Vyper's gun share inside Split Shot windows (after the first use): real 0.41, sim in full 0.27, expected 0.53 (the
  sim opens every fight with it; real players don't always).
- Overall search (`damage/scripts/overall_search.py`, `FIGHT_LENGTH`), 8 heroes at 27k, with vs without: builds drop
  late sustain (Healing Nova, Restorative Locket, Escalating Resilience on 3-4 of 8) for fight openers and team items
  (Heroic Aura, Alchemical Fire, Toxic Bullets); the best builds' time alive falls ~2-8 s. Mean real win edge of the
  picked items (analysis/out/hero_item_edge.json) 1.14 -> 1.34 points. The first run picked Silence Wave on 5 of 8
  (real edge about -1.6 on every hero): it had no real-data cut (26 holders, threshold 30) and its silence landed in
  full at the opening. The threshold is now 25 and an item active's stun / silence / disarm is x its fitted factor
  (`DamageActive.cc`, realistic mode): 2 of 8 after. Decay still shows up on 2.

## Opener timing (2026-10-24)

With real fight lengths (above), Vyper's gun share inside Split Shot windows was 0.53 expected vs 0.41 real: the sim
starts every fight with every cooldown ready and casts each opener as soon as its rule allows. This measures when real
Phantom+ players' damage abilities and items land inside a fight (`scripts/fight_length/opener_timing.py`, table in
`validation/opener_timing.md`, real rows in `opener_timing_real.json.gz`; the fights of `fit_length.py`).

**Real:** half of the openers are still on cooldown from an earlier fight: the median source is ready (no hit in its
base cooldown before) at 68% of fight starts. Vyper's Split Shot is ready at 54%, is used in 51% of his fights (64%
when ready), and its first hit comes a median ~1 s in when ready; its fight damage by 2 s slice is 0.43 / 0.34 / 0.14 /
0.05, the sim's (expected) 0.65 / 0.23 / 0.11 / 0.00. Over 232 hero sources the sim puts clearly more of the damage in
the first 2 s (by 0.15+) for 69 (casts on sight: Abrams Seismic Impact, Haze Bullet Dance, Paradoxical Swap,
Quicksilver Reload on every holder, Wraith Card Trick, ...) and clearly less for 66 (its cast rules wait too long:
Calico Spirit Strike / Mystic Shot procs, Victor Pain Battery, Silver Slam Fire, Bebop Spirit Strike, Lash Death Slam,
Vyper Lethal Venom). The gun is the mirror: real 0.33 of a hero's gun damage in
the first 2 s, sim 0.23 (casts lock the gun at the start).

**Model** (`Mechanics.opener_timing`, needs `fight_length`; **off by default**): for each source the sim casts on sight
(70%+ of its first hits in the first second), `data/opener_timing.json` holds 20 equal-probability values of the real
hold before its first use (Kaplan-Meier first use given a use by 20 s, less the sim's own median first hit); items are
also pooled over heroes. Its hits are booked x the mean over those values h of P(fight still going at t + h), as if
it had opened h later; only sources with a length correction get one (the correction keeps the level). 122 hero
sources, median hold 3.3 s. The per-source timing distance to real (half the summed 2 s slice gaps) goes 0.26 -> 0.16
(85 of 122 closer; a pooled scale on the holds does no better, 0.167 at x0.9).

**With it on** (length corrections rerun, `length_factors.py`):
- The corrections lose most of their fudge: ability median 0.74 -> 0.99 (median |ln| 0.36 -> 0.26), Split Shot 0.48
  -> 0.76, Mystic Burst 0.74 -> 0.98, Tankbuster 0.69 -> 0.89, Cold Front 0.50 -> 0.71, Quicksilver Reload 0.56 -> 0.81.
- Audit: player-weighted mix 0.0403 -> 0.0399, hero mean 0.0500 -> 0.0491 (Abrams 0.043 -> 0.017, Pocket 0.060 ->
  0.047; Venator 0.034 -> 0.047, Apollo, Nurse Harrow 0.013 -> 0.022), but pooled items 0.063 -> 0.082 and per-hero
  items 0.257 -> 0.274 (the 3-round corrections leave items 2-4% off; Vyper's Split Shot holders real/sim 1.31 ->
  1.42 under the pooled correction).
- Overall search, 12 heroes at 27k: every best build changes, the mean real win edge of the picked items stays
  (1.26 -> 1.24 points) and Decay, which loses in real matches on every hero, comes in on 4 of 12 (Haze, Dynamo,
  Mo & Krill, Lady Geist); Vyper picks Silence Wave. So it stays off until the holds also move the fight itself
  (casts later in the fight path, not only in the booking) or the search's item values are rechecked with it.

**Found on the way:** `length_factors.py` skips ability rows without a "class" (rows added by
`refit_landing_heroes.py`: Graves, Nurse Harrow, Silver), so they have no length correction. Giving them one pins them
to their in-full fits and worsens their audit (Graves 0.060 -> 0.101, Nurse Harrow 0.013 -> 0.086: the uncorrected
fight-length booking happens to suit them); a refit of those three under the fight-length booking is the fix.

## Fight replay (2026-10-25)

The Real match tab replays a fight from a real match (`web/replay.js`, `bridge.replay`). Fights come from the
match's `match_paths` (1 s positions, health %, combat flags) and `death_details` in `/v1/matches/{id}/metadata`:
two enemy heroes within 50 m, one flagged in hero combat, one losing health that second; groups chain into a fight
across gaps up to 4 s, kills add victim and killer over their time to kill, fights over 40 s are cut at 2 s lulls.
Each hero starts at its real health with its items, net worth, ability unlocks and upgrades (the ability buys in the
item list) at the fight's start, its own hero accuracy from the match, at the median distance to the nearest enemy,
for the real length (max 45 s), with the real arrival, leaving and targets (see "Real timing" below; team sim, movement off). `team_fight(start_hp=)` is new;
default fights are unchanged.

**Against the real fights** (`scripts/fight_replay/check_replay.py`, 30 recent Phantom+ matches, 1,894 fights, 8,943
heroes): the first version (everyone there from the start to the end, each team focusing the enemy with the least
health) had 1.82x the deaths (3,355 vs 1,846; 60% of the real deaths are also deaths in the sim). Health lost per fight
correlated 0.89 (sim 1.35x real), per hero 0.35. In the 699 fights where only one side lost heroes the sim had more
deaths on the same side 329 times, on the other side 180, even 190. A retreat rule (a hero hit below 10-30% health
leaves the fight alive) was tried: deaths fall to 0.15-0.27x real and the side agreement gets worse (54 vs 53 at 10%),
so it was dropped.

**Real timing (2026-10-25).** Real fights are not everyone-from-the-start: 46% of heroes join after the first second
(median 5 s in) and 37% of the survivors stop fighting before the fight ends (median 3 s early)
(`scripts/fight_replay/fit_disengage.py`). Leaving is not a low-health decision: per second of fighting a hero walks
out alive 1.4-2.1% of the time at every health level (1.5% at 0-10%, 1.5% at 90-100%), while dying climbs from 0.1%
above half health to 17% below 10%. So the replay now uses the real timing instead of a rule: each hero arrives at its
first fighting second (`team_fight(join=)`: not targetable and not acting before; a side with nobody there yet waits),
a hero that lived walks out after its last fighting second (`leave=`; a hero that really died stays to the end), and
each hero shoots the enemy nearest to it in the real positions that second (`targets=`, `rpDetect` `near`), falling
back to the team focus when that enemy is out. Same 30-match benchmark, refetched (1,933 fights, 8,936 heroes, 1,791
real deaths); F1 = deaths in both / mean of the two death counts:

| replay | sim/real deaths | F1 | HP lost corr per hero | one-sided fights same/other side | HP swing corr |
|---|---|---|---|---|---|
| everyone from the start, focus weakest (old) | 1.76 | 0.423 | 0.34 | 326 / 135 | 0.13 |
| + real arrival | 1.48 | 0.451 | 0.43 | 319 / 142 | 0.20 |
| + survivors leave at their real time | 1.31 | 0.469 | 0.45 | 304 / 130 | 0.20 |
| + shoot the real nearest enemy (**site**) | **1.04** | **0.469** | **0.51** | 292 / 140 | 0.19 |
| real nearest only, no timing | 1.42 | 0.432 | 0.44 | 326 / 159 | 0.12 |
| site, leaving at the fitted flat 1.6%/s instead of real times | 0.87 | 0.400 | 0.42 | 261 / 116 | 0.20 |

The site version gets the death count right and best follows who loses health; the side agreement stays where it
was (0.68-0.71 of the one-sided fights the sim calls, within noise). The flat leave rate does worse than the real
leave times, so it is not used (a replay knows when each player left). The arrival, leave and target inputs come from the same real fights the replay is scored on: that is the point of a replay (it repeats the players' real decisions and asks what the items change), but it is not a test of predicting those decisions. Modes: `check_replay.py ... 0 <site|all0|join|leave|nearonly|hazard>`. Still missing: who comes out ahead is decided
by positioning, cover and timing the replay does not know (HP swing correlation 0.19), and half the real deaths are
still a different hero in the sim. Read a changed build against the replay with the real items, which is what the
page compares.

## Violet added (2026-10-25)

Violet (id 86, `hero_artist`) and Baba (88) are pickable and played a lot (last 3 days ~180k and ~53k player-matches)
but the API marks them `in_development`, which `data/scripts/normalize_game.py` dropped. The hero set now keeps an
in-development hero once the sim has a hero file for it (`deadsim/heroes/<class without hero_>.py`), so a new hero
never runs on generic abilities; `fetch_analytics.py` uses the same rule. Violet's model is `deadsim/heroes/artist.py`.

Real data used (Phantom+ replays: 50 matches, Oct 22-25, 32 with a Violet, 939 fights; `phantom_sample.jsonl.gz`: 424
Violet player-matches):
- Living Ink: each empowered hit is two damage events on the same tick, a gun bullet (booked under the weapon) and the
  spirit splash (booked under Living Ink), so the sim books them the same way. Each hit moves the other abilities'
  cooldown starts back 1.5 s; Living Ink's own never moves.
- Flow State: casts are at least ~21 s apart (p10 of 44 gaps, cooldown 23 s), so the Living Ink passive ("casting any
  other ability refreshes the cooldown of Flow State") is not a cooldown reset and is left out.
- Abstract Landscape: an enemy that takes its damage first does 3.7 s after the cast (median), and is hit 1.71 times
  (crossing the ink again ~1.3 s later); 1.53 enemies per cast (the landing factor holds the multi-target part).
- Casts per fight (in fights: 0.65 Living Ink, 0.28 Flow State, 0.35 Still Life, 0.10 ultimate per 10 s).
- `scripts/fight_patterns/replay_openers.py` now counts a cast only when the cooldown start equals the game time:
  cooldown cuts also change it (Violet, Witchmail). Earlier rows were built without this; their cast shares may be a
  little high for heroes whose cooldowns get cut.
- Aim: `scripts/build_skill_defaults.py --add-missing` adds rows only for heroes the file lacks, here from a fresh
  all-rank sample (`fetch_validation.py --api 60 4`, 400 matches): Violet acc p50 0.271, headshots 0.211.
- Fight pattern: replay order Still Life > Living Ink > Abstract Landscape > Flow State, but it fits the real damage
  mix worse than slot order (0.39 -> 0.47), so slot order is kept (row `dropped`).
- Fits on the Phantom+ sample: melee 0.0225 hits/s; landing (mechanics on) Living Ink 0.68, Flow State 0.47, Still
  Life 0.75, Abstract Landscape 1.18, fight-length factors 0.78-0.96 (`length_factors.py --hero`, which leaves the
  item factors alone). Sim vs real damage mix after the fit: gun 0.29/0.29, Living Ink 0.28/0.28, ultimate
  0.17/0.17, Still Life 0.15/0.15, Flow State 0.06/0.06.
- Pooled (no Violet-specific fit yet): fight range spread, fight length ratio, death cost, item win edges (the next
  patch rerun rebuilds the win edge and team values with her).

## Baba added (2026-10-25)

Baba (id 88, `hero_baba`) enters the hero set the same way as Violet (a hero file, `deadsim/heroes/baba.py`). Real
data: Phantom+ replays (89 matches, 31 with a Baba, 868 fights) and 151 Baba player-matches in `phantom_sample`.
- Threadsap steals spirit (Baba gains StolenSpiritEffectiveness % of it) and, while she holds it, each gun bullet
  that hits deals MagicDamagePerBullet spirit damage, booked as the game does under its own Threadsap source
  (`ability_baba_bubbling_brew_gun_damage`, 16% of her real damage).
- Granny Long Legs: status and melee resist; heavy melees during it are ground pounds with spirit damage. The game
  books her bench melee as `ability_baba_bench_melee`, which `landing_rates.real_key` now counts as melee.
- Baba's Brew: modeled as the scalding brew (burn + spirit shred). In replays its first damage lands 1.0 s after the
  cooldown starts, so it is thrown pre-brewed.
- Feed The Birds: full bread count, then the barrage and the hex (as a stun). Real damage starts 2.1 s after the
  cooldown starts and comes as ~4.5 hits per victim over 1.8 s.
- Fight pattern (kept, fit 0.653 slot order vs 0.654 replay order): Baba's Brew > Threadsap > Granny Long Legs >
  Feed The Birds, ultimate after Threadsap / Granny Long Legs / Baba's Brew.
- Fits: melee 0.23 hits/s; landing (mechanics on) Threadsap 0.62, Granny Long Legs 1.29, Baba's Brew 0.53, Feed The
  Birds 0.52, each with a fight-length factor. Mix in the full audit (real/sim, Baba's 146 sample players):
  Threadsap 0.23/0.25, Torment Pulse 0.17/0.12, ultimate 0.13/0.14, melee 0.12/0.14, Granny Long Legs 0.10/0.06,
  Baba's Brew 0.07/0.08, gun 0.07/0.07; class mix distance 0.025. Torment Pulse (it pays for standing next to
  enemies) is under because item fits are pooled over heroes. Granny Long Legs is under once fight length is booked
  (length factor 0.66: the landing fit alone puts it at 0.11), an open follow-up.
- The first Brew was waiting the brew time and later ones none (inverted); fixed so only repeat throws brew, and
  Baba refit after it (mix distance 0.027 -> 0.025).
- Aim: the existing row (old all-rank sample, acc p50 0.16).

## Baba's damage gaps (2026-10-25)

- Granny Long Legs was under (0.06 vs real 0.10). In 89 Phantom+ replays, 672 of Baba's 943 melee hits during it are
  ground pounds: a heavy bench-melee event on the same tick as the spirit hit, median 131 melee damage vs 62 for a
  light kick. The sim used the usual 30% heavy split, so `GLL_HEAVY_SHARE` = 0.71 now holds while it is up
  (Engine.melee_tick reads a `heavy_share` (share, until) counter). Refit: melee rate 0.24 -> 0.18 hits/s (heavies
  hit harder); landing Granny Long Legs set from the audit (1.10; landing_rates.py's own fit gives 1.62 and
  overshoots to 0.14 in the audit, whose duels use the searches' skills), the other three refit. Audit (146 Baba
  players): Granny Long Legs 0.103/0.104, every ability within 0.01, mix distance 0.037.
- Torment Pulse stays under (real 0.17, sim 0.11): not a Baba model gap. Victims per pulse match other holders in
  the replays (1.11 both), and in real fights (match_paths, 90 Baba matches) she spends 37% of fight seconds within
  its 9.5 m against the sim's 31% (1.19x). The rest comes from item factors being one pooled fit over heroes and
  capped at 1 (`item_landing`). The same check across heroes ranges 0.65x (Abrams, sim too close) to 2.45x
  (Grey Talon, sim too far): the aim-based median distance is not the real fight distance for close-range items.

## Known gaps (not yet modeled)

- **Melee movement:** melee is in fights and its rate follows the build (see "Melee" above). Melee Charge's lunge
  and Lifestrike's slow only count in chases (movement on); there is no positioning AI that dives in to melee, and
  the light/heavy split (30% heavy) is an assumption.
- **Distance:** the fight distance spreads around the hero's median (see "Range spread") as an average, not a path: there is no positioning AI (kiting to stay at range, diving with a gap closer), and ability effects inside a cast still check the median distance. Hero range checks follow the spread: cast gates through `CastCtx.within` (engage margin + walk-in) or `CastCtx.reach` (hard reach; self buffs keep the median check, since the expected wait only scales damage), in-effect radii (Frank's revive blast, Kelvin's heal, Unicorn's barrier pop, Gigawatt's storm, Ghost's tether) scale damage, heals and stun/silence durations by `CastCtx.p_in` with no cutoff at the median (the tether breaks only at p = 0), Haze's Fixation bonus and McGinnis' turret falloff average over the spread. Still at the median: melee reach (Drifter's bonus melee, Billy's Bashdown melee), Drifter's vision check (a self buff) and Paige's distance amp (scales with distance travelled). Short-range ultimates use per-hero "approach" constants to be cast.
- **Summons:** Graves' and McGinnis' summons can be shot and splashed (see "Targetable summons"); real enemies also
  hit them with area abilities aimed elsewhere, which the sim folds into the splash share. Accuracy on summons is an
  assumption. McGinnis is still the worst-matched hero (gun share 2% vs 26% real), for reasons other than turret uptime.
- **Paradox Kinetic Carbine** damage follows real hits (see "Paradox's gun share"); the charge is always full.
- **Bebop Hyper Beam** dominates any 20 s duel that starts with it ready (landing 0.06); the model matches the
  data, the gap is the fresh-cooldown bias above. (Haze Bullet Dance: fixed 2026-10-21, see "Haze duels" below.)
- **Multi-target items** (Ricochet, Split Shot) do nothing in a 1v1 without mechanics; see above. Deadman Danny's charged primary fire is
  modeled as a plain gun with fewer, bigger shots (see "Guns with no hero accuracy"); charge timing and its
  explosion radius are not.
- **Attribution:** the game books amp bonuses under the item. Express Shot and Escalating Exposure are booked the
  same way now; Siphon Bullets, Rabbit Hex's amp and Pulse Grenade's stacking amp (~2.5% of Paradox's gun damage
  in replays) are still booked under the hit's source. This affects only the item-share comparison.
- **TTK:** sim 1v1 duels between real builds take a median 19 s (28 s with landing factors) vs 13 s for real
  deaths, which are mostly team fights with several attackers. Real fights between two heroes mostly end in a
  disengage (see "Fight length"); the searches that use `fight_length` weigh late damage down instead of cutting.

## Speed

About 9 ms per 20-second duel on one core (abilities and items on), after caching. Fine for thousands of fights;
the build search will want more.

## Cast timing (2026-10-25)

Follow-up of the opener timing above: why 66 sources landed LATER in the sim than in real fights. The main cause was the
opposite of a late cast rule: the sim opened every duel with every ability, the ultimate included (~90% of duels cast
it at t=0; real Phantom+ players cast it in 17-40% of their fights by 20 s), and the ult's cast lock / channel
(Heavy Barrage, Singularity, Concussive Combustion, ...) plus the enemy's t=0 stuns kept the gun quiet for the first
~4 s: gun damage in the first 2 s was 0.20 of the gun's fight damage vs 0.32 real, and Mystic Shot and the other gun
procs followed it.

**Real cast times:** `scripts/cast_timing/fetch_ability_casts.py` (ability cooldown starts per pawn, the 259
fight-length replays; raw in the project folder `analysis/work/cast_timing/raw`), `fit_cast_timing.py real`: per
hero ability, P(first cast by t | the pair fight still going), Kaplan-Meier, a cast up to 1 s before the first hit
counts as t = 0 (`validation/cast_timing_real.json`). Pair fights, not merged engagements: the sim's duel clock is
the pair fight's (the fight-length booking is fitted on them); merged engagements put the casts ~1 s too late.

**Model:** `Mechanics.cast_timing` (ON, fights with `fight_length` and an rng or a `Skill.fight_phase`): each ability
the sim casts on sight gets its first cast held by a draw of 20 equal-probability real values (None = not cast in
that fight), less the sim's own median cast time (`data/cast_timing.json`, 109 abilities; gated abilities keep their
own timing; Mo & Krill's prefight Burrow keeps its own). Phase draws are quasi-random like `engine.unused_items`.
`length_factors.py` then keeps each source's expected level (source / gun with the current corrections in duels that
cast on sight) instead of refitting to the in-full ratios, so the holds move when damage lands, not how much the
fitted factors give; held ults need up to 10x (`KEEP_RANGE`; Hyper Beam, Blasted, Develop Queen hit it).
Rows without a class (Graves, Nurse Harrow) get a correction now too.

**Results** (on main after Violet / Baba / the Nurse Harrow refit): cast curve |real - sim| 0.40 -> 0.12 over 146
abilities (`validation/cast_timing.md`); gun damage in the first 2 s 0.20 -> 0.27 (real 0.32); sim_vs_win at 27k
all pairs 0.191 -> 0.208, per item 0.282 -> 0.323, damage items -0.024 -> +0.045; damage audit mix 0.0410 -> 0.0437
(pooled items 0.047 -> 0.049). The audit loss is mostly Tankbuster / Mystic Reverb on spirit heroes: spaced-out casts
let the linear charge-up release more per cast, and the item corrections are pooled over heroes (Grey Talon
Tankbuster 0.096 -> 0.136 of damage, real 0.071; Pocket 0.112 -> 0.150, real 0.079).

Left: damage of held casts lands later than real hits on average (opener_timing compare: real fights opened by an
ability hit put that damage at t = 0, and early casts deal more per cast than late ones); melee items (Spirit Strike,
Spirit Snatch, Melee Charge) still proc late since melee is a steady rate; a per-hero-type Tankbuster correction.
Refit after a patch that changes cooldowns: `fetch_ability_casts.py` (new replays) -> `fit_cast_timing.py real` ->
`fit --write` -> `length_factors.py --write`.
