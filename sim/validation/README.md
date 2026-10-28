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

### Melee rates refit to the audit

`landing_rates.py` fits in its own model (abilities at 100%, no mechanics, the older all-ranks sample), so by
2026-10-26 some heroes' rates were stale in the model the searches use: in the damage audit Paradox meleed 1.6x his
real melee/gun damage (0.63x), Bebop 1.3x, while Kelvin, McGinnis and Violet meleed half or less. Hit sizes are not
the cause: every hero's light melee in the replays is 0.93-1.03x the sim's formula (`scripts/mechanics/melee_scaling.py`).
`scripts/melee_audit_fit.py` scales a hero's rate by the audit's MELEE real/sim (2 rounds). Split-half (fit on even
match ids, audit odd, and reverse) kept 11 heroes with a lower mix distance both ways: Paradox (0.030 -> 0.019),
Bebop, Kelvin, Violet, Paige, Mo & Krill, Nurse Harrow, Lady Geist, Rem, Apollo, McGinnis. Infernus, Calico, Grey
Talon, Dynamo, Baba, Wraith and Deadman Danny were worse or flat on one half and keep their rates. Those rows carry
`audit_fit` and a `landing_rates.py --fit-melee` run leaves them alone.

Stale-fit sweep (2026-10-26): Graves had no melee row at all (sim melee 0, real 2.4% of his damage); fitted to
0.020/s, his mix distance 0.039 -> 0.023. Viscous (not tried above) passed split-half (0.063 -> 0.042 / 0.081 ->
0.068 held out) and was refit (0.042 -> 0.024/s, mix 0.066 -> 0.051).

### Stale ability corrections

Most heroes' ability `length_corr` came from `length_factors.py` runs before the later model changes (melee scaling
#107, real cast reader #108, execute timing #113, Paradox pokes #114, melee rates #117). `scripts/ability_corr_heroes.py
--split` refit every hero (43) on one half of the sample (even/odd match ids, 3 rounds) and audited the other half,
both ways, keeping a hero only if the held-out per-source distance fell on both halves and the mix distance rose by at
most 0.002. Only Haze (sources 0.038 -> 0.021 / 0.039 -> 0.024; Bullet Dance corr 1.92 -> 1.48, it dealt 1.25x real)
and Mina (0.046 -> 0.032 / 0.026 -> 0.021; Nox Nostra 2.46 -> 2.00) passed; every other hero was worse or mixed on a
held-out half, so their corrections still fit. Pocket's sources halved both ways but his mix rose 0.005 on one half:
left as is. With the melee rows above and the four heroes' item factors refit once (`item_landing_heroes.py --hero`),
the whole audit on main after #116: mix 0.0274 -> 0.0263, per-source 0.0257 -> 0.0239 (Haze 0.044 -> 0.031, Graves
0.041 -> 0.025, Viscous 0.066 -> 0.051). `analysis/scripts/sim_vs_win.py` 27k all heroes: 0.173 -> 0.172, per item
0.249 -> 0.248 (flat).

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
order (re-checked under cast timing in "Yamato, Sinclair, Apollo" below). The ultimate stops waiting for its setup when no setup ability is off cooldown, when either side is
below 30% health, or after 4 s. Landing factors were refit for every hero whose fights changed
(`scripts/refit_landing_heroes.py`). `tests/test_patterns.py` pins a few duels with patterns on.

**Yamato, Sinclair, Apollo (2026-10-25, on top of cast timing #86/#90).** `scripts/fight_patterns/combo_check.py`
runs the damage audit's duels per pattern variant and compares the sim's casts with the fight_patterns replays (cast
share weighted by the real chance the fight still goes on, first-cast share, median first cast) plus the audit mix.
- Yamato: Shadow Transformation is not held by cast timing (it is not cast on sight) and came at 1.2 s in 90% of
  fights; it now waits until all the other unlocked abilities are on cooldown: 7.3 s in 36% (replays 9 s, 26%).
  It also casts below 35% health, and 16 s into the fight at the latest (a slow or silenced kit never gets all three
  on cooldown; 12 s cast it in 41% of fights, 16 s gives 36% at 7.3 s with mix 0.019).
  combo_check's survival weight is clamped to [0, 1] and starts at t = 0 for precasts (first-cast shares had gone
  outside [0, 1]).
- Sinclair: Rabbit Hex's damage amp on his own hits is booked under Rabbit Hex (`engine.BOOKED_AMPS`; the mod tag
  carries the caster), as the damage matrix lists ~5% of his damage under it though it deals none itself.
- Acceptance rule under cast timing (fight_patterns.json `_doc`): a replay combo is on when combo_check, with 20+
  audit players with gun data, gives it an ability log error and mix distance no worse than slot order and a timing
  error at least 0.03 better. Sinclair's combo is within noise (20 players: timing 0.429 -> 0.418, log error
  0.146 -> 0.141; the timing error moves ~0.05 between runs) and Apollo's has 6 players and no cast_timing rows (his abilities land at t=0, real 3-5 s in), so
  both keep slot order; the Rabbit Hex booking and the Sinclair refit stay.
- Haze: a Bullet Dance hold on Fixation stacks helped before cast timing, but now compounds with its held cast
  (cast share 0.16 vs real 0.23), so Haze is unchanged.
Refit for Yamato and Sinclair: `refit_landing_heroes.py --iterate 3 --sample validation/phantom_sample.jsonl.gz`, then
`length_factors.py --write --refit --no-cast-timing --hero X`, then `length_factors.py --write --hero X` (keep mode).
Damage mix distance (audit) main (with #91) -> this: Yamato 0.080 -> 0.020, Sinclair 0.027 -> 0.024, Apollo 0.201
(unchanged), Haze 0.043 -> 0.044; other heroes 0.0432 -> 0.0430.
Also fixed: Nurse Harrow's specter heal hook didn't take engine.heal's `origin` (#93), so a lifesteal heal during
Wretched Vapors crashed the duel (103 audit duels on main).

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

## Per-hero item factors (2026-10-25)

- The pooled item factors (`item_landing`) fit every holder at once, so they follow the heroes that buy an item most.
  Per hero the audit's holders-only table was far off in both directions: Torment Pulse real/sim 0.57 on Graves and
  0.64 on Yamato (sim too high) to 1.75 on Shiv and 2.1 on Baba (sim too low), Cold Front 0.53 on Danny and Pocket,
  Stalker 0.68 on Bebop and Yamato. Hero x item error (holder-weighted mean |ln real/sim|) 0.338, radius items 0.313.
- Fight distance is not the cause. In 400 Phantom+ match_paths matches the share of fight seconds with the nearest
  enemy within 9.5 m is 0.54x the sim's for Abrams (aim-based median 7.3 m, real fights centred near 14 m) and up to
  2x for Grey Talon and Vindicta. Making item radii follow each hero's real fight distance (a per-hero radius scale
  fitted to those shares, pooled factors rescaled) left the per-hero gaps as wide: radius items 0.313 -> 0.323, and
  on held-out halves it made the per-hero factors below worse too (0.249 -> 0.255). Not shipped. Team fights explain
  little: replays' other-hero / main-target ratio for Torment Pulse runs 0.71 (Bebop) to 1.12 (Baba) around the
  pooled 0.92, a few percent of the gap.
- Fix: `scripts/item_landing_heroes.py` takes the audit's hero x item rows (>= 20 holders) and sets that hero's factor
  to current x (real/sim)^(n/(n+20)), same 0.25-1 cap as the pooled ones (item_landing.json "heroes", read by
  `accuracy.item_landing(hero)`; `HERO_ITEM_LANDING = False` turns it off). Under-booked items can only rise to an
  uncut 1 (Shiv and Baba Torment Pulse 0.90 -> 1), so what is left above 1 stays out of 1v1s on purpose.
- Split-half check (fit on even match ids, audit the odd ones and the other way round): hero x item error 0.338 ->
  0.250, radius items 0.317 -> 0.179, damage-mix distance 0.0417 -> 0.0383. Shrinkage priors 0 / 20 / 40 / 80 gave
  0.249 / 0.250 / 0.260 / 0.277. Full sample after the fit (118 rows): hero x item 0.338 -> 0.215, radius items
  0.313 -> 0.135, mix distance 0.041 -> 0.037 (Graves 0.060 -> 0.043, Yamato 0.081 -> 0.058, Calico 0.058 -> 0.041).
- sim_vs_win (all heroes at 27k): all pairs Pearson 0.176 -> 0.173, damage items -0.025 -> -0.020, edges clear of
  noise 0.257 -> 0.254, per item 0.268 -> 0.268: flat.
- Rerun order after a big patch: item_landing.py, damage_audit.py, item_landing_heroes.py --write (it starts from the
  audit's residuals, so run it once per audit, not twice in a row on the same audit).

## Known gaps (not yet modeled)

- **Melee movement:** melee is in fights and its rate follows the build (see "Melee" above). Melee Charge's lunge
  and Lifestrike's slow only count in chases (movement on); there is no positioning AI that dives in to melee, and
  the light/heavy split (30% heavy) is an assumption.
- **Distance:** the fight distance spreads around the hero's median (see "Range spread") as an average, not a path: there is no positioning AI (kiting to stay at range, diving with a gap closer), and ability effects inside a cast still check the median distance. Hero range checks follow the spread: cast gates through `CastCtx.within` (engage margin + walk-in) or `CastCtx.reach` (hard reach; self buffs keep the median check, since the expected wait only scales damage), in-effect radii (Frank's revive blast, Kelvin's heal, Unicorn's barrier pop, Gigawatt's storm, Ghost's tether) scale damage, heals and stun/silence durations by `CastCtx.p_in` with no cutoff at the median (the tether breaks only at p = 0), Haze's Fixation bonus and McGinnis' turret falloff average over the spread. Still at the median: melee reach (Drifter's bonus melee, Billy's Bashdown melee), Drifter's vision check (a self buff) and Paige's distance amp (scales with distance travelled). Short-range ultimates use per-hero "approach" constants to be cast.
- **Summons:** Graves' and McGinnis' summons can be shot and splashed (see "Targetable summons"); real enemies also
  hit them with area abilities aimed elsewhere, which the sim folds into the splash share. Accuracy on summons is an
  assumption. McGinnis is still the worst-matched hero (gun share 2% vs 26% real), for reasons other than turret uptime.
- **Paradox Kinetic Carbine** is one big hit per fight; real Paradox lands about twice as many hits per gun damage at
  ~0.6x the size (see "Paradox's Carbine count"). Its total is right, the procs that ride on the count (Tankbuster,
  Mystic Burst, Mystic Shot) are not.
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

**Results** (main with Violet / Baba / the Nurse Harrow refit): cast curve |real - sim| 0.40 -> 0.12 over 146
abilities (`validation/cast_timing.md`); gun damage in the first 2 s 0.20 -> 0.27 (real 0.32); sim_vs_win at 27k
all pairs 0.181 -> 0.205, per item 0.277 -> 0.303, damage items -0.018 -> +0.028, edges clear of noise 0.265 ->
0.283; damage audit mix 0.0409 -> 0.0428 (pooled items unchanged, 0.083 -> 0.084). The audit loss is mostly
Tankbuster / Mystic Reverb on spirit heroes: spaced-out casts let the linear charge-up release more per cast, and
the item corrections are pooled over heroes (Grey Talon Tankbuster share 0.096 -> 0.136, real 0.071).
On main after the per-hero item factors (#85), refit with `item_landing_heroes.py --write` after the keep run:
sim_vs_win all pairs 0.178 -> 0.205, per item 0.277 -> 0.302, damage items -0.014 -> +0.026, edges clear of noise
0.261 -> 0.282; damage audit mix 0.0367 -> 0.0377 (the per-hero factors take back most of the Tankbuster loss).

Holds are `AbilityState.held_until`, not the cooldown: Witchmail / Runed Gauntlets cuts and Refresher's reset see a
held ability as ready, so they neither waste a cut on it nor release a "not cast" draw. `length_factors.py` keep mode
is one-shot: it marks the files (meta `cast_timing_kept`) and refuses to rescale them again. Abilities without a
`cast_timing.json` entry (gated ones, Violet and Baba, new abilities after a patch) keep the sim's own timing.

Refit after a patch that changes cooldowns: `fetch_ability_casts.py` (new replays) -> `fit_cast_timing.py real` ->
`fit --write` -> `length_factors.py --write` starting from the factors before the keep run -> `item_landing_heroes.py
--write` (not wired into the patch rerun: `cast_timing.json` and the corrections are static snapshots like
`opener_timing.json`).

### Holds on hit time, precast openers, melee item openers (2026-10-25)

After the cast holds, `opener_timing.py compare` still put 143 of 262 sources > 0.5 s later than real. The sim's
casts followed the real ones, and the cast -> hit time matched too (real median from the replays: Kinetic Carbine
2.3 s vs sim 2.5, Sticky Bomb 3.5 / 3.5, Concussive Combustion 3.25 / 3.25), but the real cast curve lost the fights a
charged or fused ability opens: its cast comes more than PRE_S before the fight's first hit (which is its own hit),
so that fight counted a later cast or none. Paradox's Carbine put 61% of its fight damage in the first 2 s real, 0%
in the sim.

- `fit_cast_timing.py real` now also gives each damage ability its median cast -> hit time (`hit_lag_s`) and a due
  curve (`due_by`): when the first cast's damage lands, counted from the fight's first hit, taking casts up to
  LAG_MAX before the fight whose hit lands from PRE_S before it on.
- `holds()` (PRECAST): for those abilities the holds are the due curve less the sim's median cast and cast -> hit
  time (`_lg` from the audit duels), down to -(cast -> hit time). A negative hold is `mechanics.precast`: after both
  fight starts the ability is cast that long before t = 0 (its charge and gun lock fall before the fight), if its rule
  allows; otherwise it waits for the first chance. 94 of 113 held abilities have some precast values.
- `Mechanics.melee_timing` (on): a melee item holder (Spirit Strike, Spirit Snatch, Melee Charge, Crushing Fists)
  lands one full melee hit at a time drawn from the real holders' first proc (`data/melee_timing.json`,
  `scripts/fight_length/melee_timing.py`, pooled over heroes: 11-19% by 1 s, 64-76% by 20 s), heavy for Melee Charge /
  Crushing Fists; later melee ticks that land pay it back (`counters["melee_debt"]`), so a long fight keeps the fitted
  rate and a short one gets up to one hit more (audit pooled melee share 2.43 -> 2.57, real 2.67). Before, the first melee came at 2.5 s as a fraction of a hit, and holders' procs waited for the weights to
  add up.

Results (main with cast timing -> this, refit in the same order as above): opener timing sources > 0.5 s late
143 -> 124, mean shift -0.78 -> -0.59 s (Carbine first-2 s share 0.00 -> 0.49, real 0.61; Spirit Strike on Bebop
0.00 -> 0.38, real 0.59); damage audit mix 0.0377 -> 0.0372, per-source |log ratio| 0.137 -> 0.124, items 0.102 ->
0.083; sim_vs_win at 27k all pairs 0.205 -> 0.217, damage items 0.026 -> 0.099, per item 0.302 -> 0.309, edges clear
of noise 0.282 -> 0.275. Precast alone: 0.215 / audit 0.0389.

Left: gated abilities keep their own timing (Lash's Death Slam waits ~4 s for its combo, real 62% of its damage in
the first 2 s); precasts that fail their range rule (half of Sticky Bomb's) wait for the fight.

### Combo-held ultimates on real timing

An ultimate with a setup (`patterns.Plan.allows`, ult_after: Lash's Death Slam after Grapple, ...) waited up to
SETUP_WAIT = 4 s for the setup even when its first cast was already held to the real cast time, so the real timing
was counted twice (Death Slam 0% of its damage in the first 2 s, real 62%).

- A first cast held by `mechanics.cast_timing` (`AbilityState.timed`, no casts yet) skips the wait; later casts wait
  as before. A setup ability that is itself held (`held_until`) no longer counts as castable, so it doesn't block.
- `fit_cast_timing.py fit` measures the sim's own timing twice: with the wait (all abilities, as before) and with
  `patterns.ULT_WAIT = False` (only for ultimates that aren't cast on sight with the wait). One run without the wait
  shifted other abilities and lost their holds (Lash's Flog, Grapple, Ground Strike).
- `mechanics.precast` goes earliest first and sees a free gun at its cast time (a later precast's gun lock, or the
  fight-start lock, turned down Death Slam's), and restores the lock when the cast is refused.

Results (main -> this, same refit order): held abilities 113 -> 114 (Death Slam); Death Slam first-2 s share 0.00 ->
0.51 (real 0.62); opener timing sources > 0.5 s late 124 -> 118, mean shift -0.59 -> -0.53 s; Carbine hits by 1 s
22% -> 30%; damage audit mix 0.0380 -> 0.0375; sim_vs_win at 27k (correlation, higher is better) all pairs 0.215 ->
0.213, damage items 0.097 -> 0.093, per item 0.308 -> 0.311, edges clear of noise 0.272 -> 0.276 (flat within noise).

Left: health-gated executes (Killing Blow, Assassinate, Close The Deal, Lethal Venom) need the enemy's real
fight-entry health (sim duels start full); resource gates (Slam Fire rage, Pain Battery, Djinn's Mark stacks) still
land 2-7 s later than real.

### Fight entry health (opt-in), Pain Battery and Slam Fire on real timing

Health-gated abilities (Killing Blow, Assassinate, Close The Deal, Lethal Venom) wait for the target to drop below
their threshold from full health, while real fights start with the target already short (sustain.json
entry_deficit_q: about half start full, a quarter 15%+ short); Slam Fire waited for the last shell, Pain Battery
started empty.

- `Mechanics.entry_hp` (**off by default**, with fight_length): a fighter whose start health wasn't set
  (`Fighter.entry_set`; survive's start_hp sets it, so the overall search keeps its own entry health for the build)
  starts short by a deficit drawn from the real spread for its net worth (phase or rng draw like cast_timing).
  With it on, Pain Battery starts charged by the health Victor is missing.
- Slam Fire (on): a first cast held to real cast timing opens with it whatever the clip
  (`AbilityState.held_opener`; the ultimate setup skip from #92 uses it too). `fit_cast_timing.py` measures such
  abilities with `abilities.PROBE_HELD` (every first cast acts as held) in place of #92's ULT_WAIT pass; ultimates and
  abilities marked `held_opens` take that run.
- `length_factors.py --entry [--target-holds PATH]`: on factors already kept for cast timing (and refit since, #91,
  #78), target = the current corrections in duels at full health with the previous cast_timing.json; rounds scale
  them until the duels as configured give that again. Without it a refit doubled health-gated damage (the landing
  factors already priced in the missing low-health casts: Assassinate share 0.11 -> 0.40, real 0.16) and newly held
  abilities lost their level (Storm Cloud 0.21 -> 0.04, real 0.20).

Results (sim_vs_win is a correlation: higher is better). "This (default)" is measured on main after #96/#97, with
only the Silver, Celeste and Rat King rows refit (`fit_cast_timing.py --hero`, then `length_factors.py --entry
--target-holds --hero`). "With entry_hp on" is a full refit on main after #78/#95, whose own numbers it is compared
with (main moved 0.0314 -> 0.0316 audit between the two):

| | main | this (default) | with entry_hp on |
|---|---|---|---|
| damage audit mix | 0.0316 | 0.0320 | 0.0330 (main 0.0314) |
| sim_vs_win all / damage items | 0.165 / 0.044 | 0.163 / 0.043 | 0.164 / 0.037 (main 0.164 / 0.042) |
| clear of noise / per item | 0.267 / 0.238 | 0.266 / 0.235 | 0.259 / 0.216 (main 0.267 / 0.239) |
| opener timing sources > 0.5 s late (of 222), mean real - sim | 103, -0.47 s | 103, -0.49 s | 83, -0.25 s |

Mean first hit real / main / entry_hp on: Slam Fire 3.3 / 6.0 / 3.2 (3.3 by default); Assassinate 7.4 / 9.6 / 5.9;
Lethal Venom 6.3 / 12.0 / 6.8; Close The Deal 6.2 / 8.6 / 5.6; Killing Blow 6.9 / 11.1 / 9.6; Pain Battery 5.0 / 7.6
/ 6.0; Soul Exchange 4.3 / 4.4 / 2.5 (too early). Entry health puts the executes on real timing but lowers the
per-item win match (Silver, Vindicta, Sinclair lose most; Seven gains), so it stays opt-in: to use it, set
entry_hp=True and rerun `length_factors.py 4 --write --entry --target-holds <cast_timing.json before>`.

Left: Djinn's Mark (stacks build in the fight, real first pop 9.8 s vs sim 12.6 s); with entry_hp, Killing Blow is
still ~3 s late and Soul Exchange ~2 s early. (Executes and Djinn's Mark: next section.)

### Execute gates on real entry health; Djinn's Mark gaps (2026-10-26)

Follow-up of the section above: entry health put the executes on real timing but lowered the per-item win match,
because every fight then started short (shorter fights for every hero, not only the executes). Djinn's Mark popped
~3 s late.

- `Mechanics.entry_gate` (**on**, with fight_length, entry_hp off): a fighter facing an execute (Killing Blow,
  Assassinate, Close The Deal, Lethal Venom: `mechanics.EXECUTE_GATES`) gets the same real entry deficit draw, but
  its health stays; only those gates and their low-health scaling see it (`Fighter.gate_hp` / `gate_frac`). Fights
  against other heroes draw nothing. Levels kept with `length_factors.py --entry --target-holds --hero` for the four
  heroes (target run with entry_gate off).
- Djinn's Mark: in 260 Phantom+ replays, after a mark real Mirage lands no next mark on that enemy within
  VictimStackDuration ~48% of the time at 5 s, ~24% at 8 s (fight still going; `scripts/mechanics/djinn_gaps.py` ->
  `data/djinn_gaps.json`): most first pops are low-stack expiry pops. The sim's steady gun never let marks expire.
  Now (`mirage.MARK_GAPS`, fights booked over real lengths with an rng or phase) each mark draws that gap: no mark
  until they expire and pop. A first cast held to real cast timing pops the marks there are (`held_opens =
  "first_hit"`; the fit's probe counts it on sight by 2 s since the first mark waits for a gun hit). Mirage's rows
  refit with `fit_cast_timing.py --hero Mirage`, then `length_factors.py --entry --target-holds <before> --target-off
  deadsim.heroes.mirage.MARK_GAPS --hero Mirage` (Djinn's Mark length_corr 2.54 -> 6.56: the duel holds one target,
  real Mirage marks several).

Timing (mean first-hit time real / main / this; P(first hit by 1 / 3 / 6 s) real vs this):

| source | real | main | this | used by 1/3/6 s real | this |
|---|---|---|---|---|---|
| Killing Blow | 6.9 | 11.3 | 8.3 | 0.01 / 0.03 / 0.06 | 0.00 / 0.02 / 0.05 |
| Assassinate | 7.4 | 10.2 | 6.2 | 0.02 / 0.06 / 0.13 | 0.07 / 0.10 / 0.17 |
| Lethal Venom | 6.3 | 11.8 | 6.9 | 0.00 / 0.04 / 0.27 | 0.00 / 0.18 / 0.26 |
| Close The Deal | 6.2 | 9.4 | 6.0 | 0.01 / 0.04 / 0.10 | 0.00 / 0.15 / 0.24 |
| Djinn's Mark | 9.8 | 12.2 | 9.1 | 0.06 / 0.10 / 0.23 | 0.05 / 0.10 / 0.21 |

Djinn's Mark split-half (gaps fit on one half of the replays, first-pop curve of the other half; holds as fitted):
mean |real - sim| of the 0-20 s curve 0.164 -> 0.046 (even) and 0.164 -> 0.076 (odd).

Results on main after #100 (sim_vs_win is a correlation: higher is better): sim_vs_win at 27k all pairs 0.159 ->
0.162, damage items 0.041 -> 0.050, clear of noise 0.264 -> 0.265, per item 0.230 -> 0.231 (full entry_hp: per item
-0.023). Damage audit mix 0.0311 -> 0.0317 (Vindicta 0.056 -> 0.061, Danny 0.022 -> 0.026); source levels kept
(Killing Blow share 0.033, Djinn's Mark 0.284 -> 0.273, real 0.291).

Left: Assassinate now ~1 s early (the shot-would-kill check on gate health); Killing Blow ~1.4 s late.

### Killing Blow and Soul Exchange on real timing (2026-10-26)

Follow-up of the section above, on the real cast curves after the cast reader fix (#108). P(first cast by t | fight
still going), Shiv's Killing Blow: real 0.03 / 0.07 / 0.13 / 0.36 by 1 / 3 / 6 / 20 s, main 0.00 / 0.02 / 0.08 /
0.84 (median of the casts 8.5 s real, 11.2 s main): late, and cast in 2.3x the fights. Lady Geist's Soul Exchange: real
0.03 / 0.09 / 0.16 / 0.42, main 0.02 / 0.05 / 0.08 / 0.18 (median 8.6 s real, 6.4 s main): early, and in half the
fights. From the 260 replays (`scripts/mechanics/execute_timing.py` -> `data/execute_timing.json`):

- Most real first Killing Blows in a fight are no execute: by 20 s 26% of fights have a first cast without one (the
  slash on a target at ~55% health for ~7% of its health, or a miss; the ult then sits out its whole cooldown, next
  cast ~200 s later vs ~10 s after an execute's recast), 10% an execute. The sim only cast on an execute.
- Real Geists swap at ~25% health on a ~90% target. They enter fights at ~75% health and take ~1.15x as much from
  other enemies as from their pair enemy: the 1v1 duel rarely opens that gap.
- Shiv's target also takes ~0.9x from others, but the sim's duels already bring it down faster than a real pair
  fight: with that damage seen by the gate the executes came ~3 s early, so Killing Blow doesn't use it.

**Change:**
- `Mechanics.execute_timing` (**on**, with cast_timing): each fight draws a Killing Blow plan, spent at a real time
  (`commit_holds`, the real no-execute first cast curve; an execute if the target is under the threshold by then), wait
  for the execute gate (`exec_share` 0.10 of the fights, fitted on the audit duels so the cast share by 20 s matches),
  or not cast (on cooldown). Soul Exchange's first cast is held to a real first cast time (or not cast; `hold_share`
  0.79, fitted the same way), then its gap gate. Draws like cast_timing (phase or rng; deterministic fights skip).
- `Mechanics.gate_assist` (**on**, with fight_length): Geist's gate health (`Fighter.gate_hp`) is short by a real entry
  deficit and by 1.14x the damage she takes in the duel; the swap's gap and its damage use it. Health stays.
- Levels kept: `length_factors.py --entry --target-entry --target-off MECH.gate_assist,MECH.execute_timing --hero
  Shiv` (and Lady Geist): the target run has the two new flags off and the entry gate as on main (new options
  `--target-entry`, `MECH.flag` in `--target-off`). Killing Blow length_corr 0.65 -> 2.22 (landing x corr 0.23 ->
  0.78), Soul Exchange 0.96 -> 0.40.

**Results:**
- Curves now: Killing Blow 0.04 / 0.05 / 0.12 / 0.36 (quartiles of the casts 4.0 / 7.9 / 13.5 s, real 4.1 / 8.5 /
  13.6), Soul Exchange 0.02 / 0.06 / 0.14 / 0.48 (4.0 / 8.4 / 15.4 s, real 3.7 / 8.6 / 13.7). Mean |real - sim| of the
  0-20 s curve 0.201 -> 0.011 and 0.103 -> 0.021.
- Damage audit, all heroes on main after #112: mix 0.0303 -> 0.0303 (player-weighted).
- Damage audit (full sample, both heroes): Shiv mix 0.03 -> 0.03, Geist 0.01 -> 0.02; Killing Blow share 0.034 ->
  0.031 (real 0.056), Soul Exchange 0.089 -> 0.094 (real 0.139). Split-half (plans and levels fitted on one half, the
  other half audited, against main): source distance Shiv 0.051 -> 0.057 / 0.026 -> 0.025, Geist 0.083 -> 0.086 /
  0.065 -> 0.059 (odd / even audited): flat.
- sim_vs_win at 27k (a correlation: higher is better): all pairs 0.171 -> 0.174, damage items 0.054 -> 0.053, clear
  of noise 0.272 -> 0.273, per item 0.251 -> 0.250: flat.

## Tankbuster minimum damage (2026-10-25)

Follow-up of cast timing (its audit loss was mostly Tankbuster on spirit heroes). In 260 Phantom+ replays (every
hero-vs-hero DamageEvent, `analysis/work/replay_damage` in the project folder) Tankbuster releases on ~93% of ability
hits big enough, with small releases (mean 75-170 per release): Flog 1226 of 1381 hits, Kinetic Carbine 952 of 1005,
Scorn 929 of 1122. By the damage the hit dealt, its trigger share ramps from 0.26 at 80-100 to 0.63 at 120-140 and
0.92 at 165+: the 165 MinimumDamage is checked before the target's resists (which vary). Mystic Burst's 80 is a step
at 80 dealt (0.21 at 60-80, 0.57 at 80-100), so it checks the damage dealt. The sim checked Tankbuster after resists,
so hits of 100-165 dealt never released it: Mo & Krill's Scorn, Drifter's Rend, Holliday's Powder Keg, Mina's Rake.

**Change:** `Hit.pre_mit` (the hit / landing before the target's resists and damage-taken amps); Tankbuster checks it.
The sim's trigger share by damage dealt now ramps too (0.10 at 80-100, 0.42 at 120-140, 0.94 at 165+), a little
later than real (sim resists are lower or replay damage leaves out barrier hits; not fitted).

**Results** (main after cast timing):
- Tankbuster hero x item error (holder-weighted |ln real/sim|) 0.353 -> 0.245 (Mo & Krill 2.37 -> 1.08, Holliday
  1.89 -> 1.11, Drifter 2.26 -> 1.63, Lash 1.17 -> 1.02); pooled holders real/sim 1.36 -> 1.16. All hero x item rows
  0.223 -> 0.212. Same on each half of the sample (even / odd match ids: 0.232 -> 0.224, 0.231 -> 0.216).
- Whole-match damage mix 0.0377 -> 0.0387: Mo & Krill (0.025 -> 0.045), Lash, Holliday. Their items were already over
  in the whole-match mix while Tankbuster was 1.9-2.4x under in the holders-only table: the mix compares the whole
  match (early game without the item) with duels at 30/60/90%, which overweights mid-game items.
- sim_vs_win at 27k: all pairs 0.205 -> 0.204, per item 0.302 -> 0.300, damage items 0.026 -> 0.024: flat.
- A per-hero factor refit (`item_landing_heroes.py`) on top no longer helps held-out data on this main (mix and
  hero x item worse on both halves), so the factors are unchanged.

Left: Paradox (3.3x under) and Bebop (2.1x) Tankbuster; both trigger right in the sim (Kinetic Carbine, Sticky Bomb),
but have few qualifying hits per duel. Grey Talon / Pocket / Mina are 0.88-0.93 (fine).

## Heroes furthest from real damage: refit to the audit, Victor's ult, Bebop's hook (2026-10-25)

Damage audit on main after cast timing (#86) and the timing follow-ups (#90, #92): player-weighted mix distance 0.0378. Many heroes' ability factors
came from the old all-rank sample (Deadman Danny's Close The Deal real share 0.043 there vs 0.098 in Phantom+).

- **Refit straight to the audit.** `length_factors.py` can't redo a refit hero's length_corr once the factors are
  scaled for cast timing (keep mode refuses; `--refit` targets the in-full ratio of duels with held casts, which is
  not what the landing fit saw: held-out 0.040 -> 0.063). So, per hero: `refit_landing_heroes.py --iterate 2
  --sample phantom` (in-full landing, the dummy page), then 3 rounds of audit + `scripts/ability_corr_heroes.py
  --hero H --write` (length_corr x (real/sim)^(n/(n+20)) per ability, from the audit's sources), then audit +
  `item_landing_heroes.py --hero H --write` (new `--hero`: refits that hero's item rows, keeps everyone else's;
  without it the script replaced the whole "heroes" block).
- **Held-out check.** Fit on even match ids, audit the odd ones, then the reverse. Kept only heroes better both
  ways (checked again after #90): Venator, Infernus, Victor, Silver, Seven, Vyper, Paige, Mirage, Ivy, Kelvin, plus
  Bebop (needs a row for the new hook; one half better, one worse). Rem was better before #90, not after. Worse in one direction (left as they were): Shiv, Baba, Billy, Celeste, Warden, Violet;
  worse or flat held-out: Paradox, Vindicta, Danny, Drifter, McGinnis, Lash, Grey Talon, Dynamo, Lady Geist, Viscous.
  Haze, Yamato, Sinclair and Apollo were left to the fight-combo PR (#78).
- **Victor (`heroes/frank.py`, `data/victor_revive.json`, `scripts/mechanics/victor_revive.py`).** Real ult damage
  is 53% the T1 per-bullet bonus ("while on cooldown") and 47% the revive blast. In 59 Phantom+ replays (4.6
  revives a match) the ult is still on cooldown at the start of 11% of his lane fights and 30-50% later; the sim
  always started with it ready. Fights with fight_length and an rng or fight phase now draw the seconds since his
  last revive (20 bins per phase) and start with the rest of the cooldown left.
- **Bebop (`heroes/bebop.py`).** Grapple Arm deals 0.7 x light melee damage on hit (raw ability data: Damage 0 with
  an ELightMeleeDamage stat_scale 0.7, dropped by `data/game/abilities.json`). Replays: one hit on 42% of casts,
  median 51 before 8 min and 96 at 30-40 min, ~1 s after the cast. The sim dealt 0 (real 4.6% of his damage).
  Other zero-base scaled properties the normalizer drops (Kelvin Ice Path ExplodeDamage, Magnetic Flux GrabDamage,
  Setup Bishop PulseDamage...) are a possible follow-up.

Results (full Phantom+ sample, on main after #92): mix 0.0378 -> 0.0331; Vyper 0.076 -> 0.018, Mirage 0.110 ->
0.026, Victor 0.059 -> 0.018 (ult share 0.023 -> 0.056, real 0.058), Paige 0.066 -> 0.017, Seven 0.050 -> 0.026,
Infernus 0.043 -> 0.021, Bebop 0.023 -> 0.021. sim_vs_win at 27k flat (checked on main after #90: all pairs
0.167 -> 0.166, per item 0.235 -> 0.238, damage items 0.040 -> 0.038). `damage_audit.py` writes to
`$AUDIT_OUT.json/.md` when set.
Left: Paradox Kinetic Carbine hit count (real often partly charged, ~3.7 hits per 1000 gun dmg vs sim 2.0) and
Bebop Sticky / Uppercut hit counts (both drive Tankbuster procs).

### Deadman Danny and a per-ability check (2026-10-25)

The mix distance above only compares gun / abilities / items / melee, so it misses a hero whose ability total is right
but whose abilities are off against each other. Danny was like that: Close The Deal 0.030 of his damage vs 0.098
real, Strix Salvo 0.31 vs 0.25, Chimera Mk1 0.27 vs 0.20. The per-ability check is half the summed share gaps over every
source. The same refit as above was tried on the 28 heroes not refit yet, fit on one half and audited on the other,
both ways. Only Danny got better on both measures both ways (sources 0.113 -> 0.019 and 0.119 -> 0.018, mix 0.032 ->
0.025 and 0.037 -> 0.020). Full sample (main after #78): Danny sources 0.116 -> 0.014, mix 0.035 -> 0.022 (Close The Deal 0.096,
Strix 0.247, Chimera 0.200), audit 0.0314 -> 0.0306 (0.0316 -> 0.0309 on main after #97, Apollo unchanged). Paradox, Vindicta, Shiv, Pocket, Solomon and the rest were
mixed or worse on one half and were left as they were.

## Apollo: slow-gun players back in the fits, cast timing rows (2026-10-25)

Apollo had no `data/cast_timing.json` rows and the worst audit mix (0.20). The replays were not the gap: the cast
timing replays hold 1,366-1,812 Apollo fights per ability. The sim side was: `landing_rates.gun_known` needed 150 API
hero hits, and Apollo's gun (0.38 s cycle) lands a median 69 a Phantom+ match (300 shots, vs 334 / 1360 over all
heroes), so 6 of 111 Apollo players were in the audit, the landing fits and the cast timing sim curves (MIN_DUELS
30 dropped him).

- `landing_rates.SLOW_GUNS` gives a hero its own (min hits, min shots): Apollo (40, 150), about the old limits x his
  shots share, 92 of 111 players. `own_aim` replaces the hard-coded 300 shots in `skill_of` and the audit. The
  0.20 was those 6 gun-heavy players: with 92 the mix is 0.06 before any refit (real gun share 0.11, not 0.24).
  Others with the same gap (The Doorman 5%, Violet 1%, Kelvin 14%, Solomon 31% of players known) need their own
  refit before they join.
- `fit_cast_timing.py fit --hero NAME [--write]` fits one hero (all its players) and swaps only its rows into the
  data file and the report. Apollo: Sigil, Riposte and Flawless Advance held (sim cast all three on sight; real by
  3 s 0.37 / 0.33 / 0.21), timing curve gap 0.333 -> 0.079; the ult keeps its health gate (not on sight).
- Then 3 rounds of audit + `ability_corr_heroes.py --hero Apollo --write` and `item_landing_heroes.py --hero Apollo
  --write`. A landing refit first gave the same end factors (length_corr absorbs it), so it was left out.

Held-out (fit on even match ids, audit odd, and the reverse), Apollo mix distance: 0.065 -> 0.045 and 0.071 ->
0.048 (cast timing alone: 0.065 / 0.078). Full sample: Apollo 0.06 -> 0.04; player-weighted mix 0.0314 on main
(6 Apollo players) -> 0.0316 (92), other heroes unchanged. sim_vs_win 27k: all pairs 0.164 -> 0.165, damage items
0.042 -> 0.044, per item 0.239 -> 0.238; Apollo's own 129 pairs 0.31 -> 0.28 (noise level at that n).
Left: Melee Charge on Apollo 5x under (real 0.42 of gun damage while held, sim 0.08), Itani Lo Sahn cast in 80% of
sim duels by 20 s vs 43% real (health gate, duels to the death).

## Violet, The Doorman, Kelvin, Solomon: the other slow guns (2026-10-25)

The Apollo gap again: their guns land a median 67 (Violet), 99 (The Doorman), 98 (Kelvin), 129 (Solomon) API hero
hits a Phantom+ match, so 150 hits kept 4 of 424 Violet, 2 of 39 Doorman, 12 of 88 Kelvin and 42 of 137 Solomon
players. `landing_rates.SLOW_GUNS` gives them (40, 150), Kelvin (55, 150): 376, 38, 80, 136 players.

- `fit_cast_timing.py fit --hero NAME --write` for each: Violet all four abilities held (curve gap 0.190 -> 0.050),
  The Doorman Call Bell, Luggage Cart, Hotel Guest (0.399 -> 0.164), Solomon refit with all players (his three rows
  had come from 42; 0.585 -> 0.153).
- Then 3 rounds of audit + `ability_corr_heroes.py --write` and `item_landing_heroes.py --write` for those three.

Held-out (fit on even match ids, audit odd, and the reverse), mix distance with the new players, before -> after:
Violet 0.043 -> 0.031 / 0.036 -> 0.033, The Doorman 0.185 -> 0.036 / 0.217 -> 0.058, Solomon 0.032 -> 0.014 /
0.080 -> 0.054. Kelvin got worse both ways with his holds (0.056 -> 0.068 / 0.024 -> 0.072: holding his casts doubles
his gun share, real 0.09, and the refit overshoots abilities) and flat without them (0.051 / 0.024), so he only
gets the extra players: no cast timing rows, factors from PR #91 kept.
Full sample: Violet 0.051 -> 0.028, The Doorman 0.285 -> 0.019, Solomon 0.049 -> 0.018, Kelvin 0.046 -> 0.040;
player-weighted mix 0.0309 -> 0.0302 with 670 more players. sim_vs_win 27k (correlation, higher is better) flat:
all pairs 0.164 -> 0.163, damage items 0.042 -> 0.040, per item 0.237 -> 0.237.
Left: The Doorman's corrections (x3-4) rest on 38 players; Violet's four real cast curves are near identical (ult
cast by 20 s in 98% of fights), worth a look in the cast replays; Solomon's Develop Queen corr sits at the 10 cap;
Rem, Paige, Sinclair also keep under half their players at 150 hits.

## Close-range items on far heroes: Stalker's reach, melee openers (2026-10-26)

Tyler: the site recommended Stalker and Melee Charge to Vindicta, who plays too far away to use them (Phantom+
builds had Melee Charge at 18k, Stalker at 27k; Grey Talon, McGinnis, Mina, Sinclair... had Spirit Snatch / Stalker
the same way). Vindicta at 18k, popular build + item: Melee Charge +26% score (melee damage 4 -> 85 per fight),
Stalker +16%.

- Melee openers. `Mechanics.melee_timing` gave every melee item holder one full opening melee (heavy for Melee
  Charge) in ~65% of fights, drawn from the holds pooled over real holders. Later melee ticks pay it back, which keeps
  the fitted rate for heroes who melee often, but Vindicta lands 0.0094 melees/s even with a melee item, so the debt
  was never paid and the opener was ~6x her real melee. Every hero with real opener rows melees >= 0.036/s with one
  melee item (Bebop the lowest) and opens about as often as the pool (real by 20 s / pooled 0.45-1.17, no trend with
  rate). Below `MELEE_OPEN_FULL_RATE` = 0.036 (outside the data) a hero now opens in rate / 0.036 of those fights:
  Vindicta 26% of them (~17% of all fights, was ~65%), McGinnis 20%, Haze 52%, Infernus 71%; heroes with rows
  unchanged. Real low-melee heroes almost never
  buy these items (11 melee item holders among them in the 600-match sample), so their landing can't be checked
  directly; their absence is the evidence.
- Stalker procs off cooldown on a bullet hit with the target within 8 m. It took a per-bullet chance p_within(8.5),
  so a hero 8 m away 7-13% of the time procced it about every 1 / p bullets: on cooldown. Now each proc counts x
  cooldown / (cooldown + the expected wait for the drift to bring the target within 8 m) (`FX.reach_share`, the mean
  field abilities use, `Engine.reach_ready`): Vindicta vs typical enemies 0.24-0.35, close heroes 0.55-0.75. Real
  holders proc it later than the old sim on every hero (opener timing: used by 1 / 3 / 6 s real 0.08-0.30 / 0.32-0.48 /
  0.46-0.59, sim 0.38-0.81 / 0.65-0.95 / 0.86-1.0), which the old landing factors (pooled 0.754, per hero ~0.63)
  absorbed. Refit: pooled 0.754 -> 0.946, then `item_landing_heroes.py --item Stalker --write` (new option: refit one
  item's rows): Abrams 0.66, Bebop 0.89, Billy 0.74, Calico 0.76, Silver 0.69, Yamato 0.63, Drifter 1.0 (cap; real/sim
  1.30). The 8 Stalker holders on low-melee heroes: real/sim 1.16 -> 0.97.

Results (main -> this): damage audit player-weighted mix 0.0311 -> 0.0313 (0.0317 -> 0.0317 after rebasing on #103, 0.0309 -> 0.0310 on #101),
pooled Stalker real/sim 1.06 -> 1.11 (Drifter at the cap), items |log real/sim| 0.158 -> 0.164; most of that is Rebuttal 1.26 -> 1.61, whose sim damage is a
handful of parries per player and flips with any change to a fight (per-hero rows move both ways: Bebop 0.13 -> 0.07,
Wraith 0.02 -> 0.10 of gun damage); turning the melee cap off leaves it the same. sim_vs_win 27k: all pairs 0.159 ->
0.168, damage items 0.041 -> 0.063, edges clear of noise 0.264 -> 0.264, per item 0.230 -> 0.237. Mean sim gain per
1000 souls: Spirit Strike 0.114 -> 0.097, Spirit Snatch 0.084 -> 0.068, Melee Charge 0.070 -> 0.057; on Vindicta
Melee Charge 0.049 -> 0.009, Spirit Snatch 0.106 -> 0.022 (Stalker is a movement item, not in sim_vs_win). Vindicta's
overall search: no Stalker or Melee Charge at any budget (18k: Mystic Shot, Headshot Booster, Locket... ; 27k: Focus
Lens, Toxic Bullets...). Stalker's movement speed value (movement_value.json, pooled over holders) is unchanged.

## Rem, Paige, Sinclair: just under the hit cutoff; Violet's cast curves were cooldown cuts (2026-10-26)

Rem (median 551 shots / 133 API hero hits a Phantom+ match), Paige (447 / 135) and Sinclair (685 / 141) sit just under
150 hits, so `gun_known` kept 23 of 62, 58 of 139 and 20 of 56 players. `landing_rates.SLOW_GUNS` gives them (60, 200):
57, 135 and 55 players.

Violet's four real cast curves were near identical (each "cast" in 97-99% of fights by 20 s) because the replay reader
took every new cooldown start as a cast. Two things move the start without a cast: cooldown cuts (Violet's Living Ink
hits cut her other cooldowns 1.5 s: 75% of the dropped Violet rows land within 0.1 s of a hit by another of her
abilities, 2% of the kept ones) and pauses (they shift the tick -> game time offset, 1-10 stretches a replay).
`fit_cast_timing.real_casts` keeps a row only when its start is the game time in one of the replay's offset
stretches, or up to 20 s later and past the ability's last start (cooldown after the duration: Rem's Lil Helpers).
Cuts were 63% of Violet's rows, 63% of Rem's, 76% of Deadman Danny's, 3-20% for most heroes. Real cast by 20 s:
Violet's Abstract Landscape 0.98 -> 0.36, Flow State 0.99 -> 0.80, Still Life 0.99 -> 0.87; Rem's Naptime 0.98 ->
0.55; Deadman Danny's Rocketeer 0.91 -> 0.55; 50 of 170 real rows move by more than 0.05
(`validation/cast_timing_real.json` is refit for all heroes; holds were refit only for Rem and Violet).

Cast timing refit (`fit_cast_timing.py fit --hero`) for all four, then 3 rounds of audit + `ability_corr_heroes.py`
and `item_landing_heroes.py`. Held-out (fit on even match ids, audit odd, and the reverse), mix distance with the new
players, before -> after:

| hero | fit odd, audit even | fit even, audit odd | kept |
|---|---|---|---|
| Rem | 0.089 -> 0.036 | 0.132 -> 0.045 | holds + refit |
| Paige | 0.018 -> 0.044 | 0.038 -> 0.035 | players only |
| Sinclair | 0.019 -> 0.026 | 0.066 -> 0.050 | players only |
| Violet | 0.024 -> 0.035 | 0.032 -> 0.037 | holds + refit |

Violet keeps the new holds although her mix is a little worse: the old holds were fitted on the cut rows (her ult
held as cast by 20 s in all but 2% of fights), and sim_vs_win 27k (correlation, higher is better) is the same with
either: main all pairs 0.162 / damage items 0.048 / per item 0.233; this branch 0.163 / 0.037 / 0.237; with Violet's
old holds 0.162 / 0.039 / 0.236. Full sample: Rem 0.108 -> 0.024, Violet 0.028 -> 0.036, Paige 0.026, Sinclair 0.040;
player-weighted mix 0.0315 -> 0.0313.
Left: the other 46 heroes' holds still rest on the old real curves (biggest moves: Deadman Danny's Rocketeer, Graves'
ability_necro_gravestone, Ivy's Air Drop, Grey Talon's Guided Arrow); refit hero by hero with a split-half check.
`fight_patterns/replay_openers.py` filters cuts with one offset per replay, so it drops real casts after a pause.

## The other heroes' cast holds on the fixed real curves (2026-10-26)

After the cast reader fix above, 21 more heroes held a first cast whose real curve moved by more than 0.05 (Deadman
Danny's Chimera Mk1 0.40, Graves' Borrowed Decree 0.28, Ivy's Air Drop 0.25, Grey Talon, Seven, McGinnis, ...). Each was
refit on its own (`fit_cast_timing.py fit --hero`, then 3 rounds of audit + `ability_corr_heroes.py` and
`item_landing_heroes.py`) on the even or odd match ids of the sample and audited on the other half
(`AUDIT_HEROES=name` audits one hero's players, ~5 s a half). The comparison is with the same refit on the old holds
("ref"), since a half-sample refit alone moves the mix; main's own factors ("base") were fitted on both halves.
Kept only where the mix is better on both halves and the per-source gap (half the summed |real - sim| share over all
sources) is not worse by more than 0.005:

| hero | half audited | base | ref (old holds, refit) | new holds only | new holds + refit |
|---|---|---|---|---|---|
| Ivy | even | 0.039 | 0.036 | 0.054 | 0.031 |
| Ivy | odd | 0.041 | 0.039 | 0.051 | 0.033 |
| Vindicta | even | 0.069 | 0.023 | 0.077 | 0.023 |
| Vindicta | odd | 0.055 | 0.022 | 0.065 | 0.024 |
| Deadman Danny | even | 0.022 | 0.028 | 0.076 | 0.018 |
| Deadman Danny | odd | 0.025 | 0.028 | 0.081 | 0.026 |

Kept: Ivy and Vindicta (Vindicta's gain is mostly the refit: Assassinate's length_corr 0.21 -> 0.35, Crow Familiar
1.29 -> 1.62; the new holds are level with the old ones there). Deadman Danny is borderline (mix better than ref
both ways, per-source 0.021 -> 0.027 on the odd half) and keeps #98's audit fit. The other 18 were mixed or worse
on the held-out half; "new holds only" is worse for most because their length corrections were fitted to the old
holds. Full sample: Ivy 0.040 -> 0.030, Vindicta 0.062 -> 0.018; player-weighted mix 0.0313 -> 0.0302.
sim_vs_win 27k (correlation, higher is better) is flat: all pairs 0.172 -> 0.170, damage items 0.058, per item
0.244 -> 0.243.

## Melee hits grow with weapon damage; Uppercut procs spirit items (2026-10-26)

The hero calibration thread found the sim's Exploding Uppercut far smaller than real (sim median 98 before resists,
none at 165+; real median 104 after resists, 90th percentile 187). `scripts/mechanics/melee_scaling.py` (260 Phantom+
fight replays, every hero-vs-hero DamageEvent, + the validation sample's builds and real weapon power):

- Uppercut is one hit per victim, the size of the victim's own light melee hit from the same Bebop (ratio 1.0), and
  melee-resisted, not spirit-resisted (no trend with the victim's spirit resist). So the ability is right and the
  light melee formula is short: real / (base + boon growth) x (1 + melee bonus) x (1 - melee resist) climbs with the
  attacker's real weapon power, within the same match minute, for Uppercut and for every hero's light melee alike
  (lowest fifth of basic melee hits: 0.99 below 10% weapon power, 1.33 at 30-60%, 1.69 above 100%). It is flat with
  0.5 x the weapon bonus (0.97 / 1.00 / 1.08 / 1.09 / 1.05); 1.0 overshoots (0.76 above 100%). Now
  `engine.MELEE_WEAPON_SCALE` = 0.5: every melee hit (basic and ability: `Fighter.melee_mult`) x (1 + melee bonus +
  0.5 x weapon bonus). Uppercut stays ~1.10 x the formula at every weapon power (not modeled).
- Uppercut alone on a tick releases Tankbuster on 24% and Mystic Burst on 19% of holders' hits; Grapple Arm and basic
  melee (also melee damage) never do. `AbilityImpl.spirit_procs`: Uppercut's hits pass Mystic Burst / Tankbuster's
  spirit check (their MinimumDamage checks unchanged).
- On-melee items proc on ability melee hits too: Spirit Snatch on 72% of Grapple Arm hits by holders, 33% of Uppercut,
  27% of basic melee; Spirit Strike 44 / 17 / 11%. The sim procced them on basic melee only. `items_fx._any_melee`:
  Spirit Snatch, Spirit Strike, Lifestrike / Melee Lifesteal (and its slow) proc on any non-item melee hit, an ability
  hit weighing its landing factor. Melee Charge / Crushing Fists stay basic-melee only (heavy melee).

Refits, so damage totals stay where the audit had them (bigger hits, fewer of them): every hero's melee rate x (old /
new sim melee per gun damage, two rounds; Bebop 0.0396 -> 0.030, Venator 0.195 -> 0.12, Billy 0.218 -> 0.151) and the
length_corr of the abilities that scale with light melee (Uppercut 1.71 -> 1.44, Grapple Arm 2.18 -> 1.74, Calico
Leaping Slash, Yamato Flying Slash, Viscous Puddle Punch, Drifter Rend, Billy Bashdown, Silver Boot Kick); then Spirit
Snatch / Spirit Strike: pooled landing x new / old pooled real/sim (1.213 (uncut) -> 0.853, 1.073 -> 0.872) and
`item_landing_heroes.py --item "Spirit Snatch" --item "Spirit Strike"`.

Results (main -> this, full sample): damage audit player-weighted mix 0.0310 -> 0.0316, sources 0.0304 -> 0.0306;
Bebop Mystic Burst real/sim 1.53 -> 1.20, Spirit Snatch 1.09 -> 0.96, Spirit Strike 1.23 -> 0.97, Uppercut 1.00 ->
1.00; Tankbuster stays 1.57 (Bebop's spirit builds rarely reach 165 before resists; real Uppercut releases it even at
84-150 dealt). Split halves (even / odd match ids; the Spirit Snatch / Strike refit fit on one half, audited on the
other): mix 0.0343 -> 0.0345 and 0.0309 -> 0.0318, hero x item |log real/sim| 0.210 -> 0.208 and 0.207 -> 0.204
(melee and Mystic Burst / Tankbuster rows 0.256 -> 0.241, 0.248 -> 0.232). sim_vs_win 27k: all pairs 0.171 -> 0.169, damage items 0.070 -> 0.067, edges clear of noise
0.265 -> 0.267, per item 0.240 -> 0.241 (flat); mean gain per 1000 souls Spirit Snatch 0.066 -> 0.060, Spirit Strike
0.094 -> 0.093. On main after #106/#108: audit mix 0.0302 -> 0.0308.

## Tankbuster on Bebop: Uppercut releases it on a flat share of hits (2026-10-26)

Bebop's Tankbuster was 1.55 x under real in the holders-only table (43 holders). Replays (260 Phantom+ fight
replays, every hero-vs-hero DamageEvent with victim health) say Tankbuster's own rule is right: a release is exactly
(40 + 7.5% of the victim's health before it) x charge (ratio 1.00 at 14 s+ since the last release, 0.68 at 7-14 s),
the charge is shared over victims (not per victim), and Tankbuster per Sticky Bomb damage for Bebop holders is 0.25
real vs 0.26 sim. Sticky Bomb triggers 88% of Bebop's real releases, Uppercut ~10%. The same 43 players are ~1.5 x
under per gun on Sticky Bomb (5.05 vs 3.19) and Uppercut (1.04 vs 0.77) too: the Bebops who buy Tankbuster barely
shoot, so most of the gap is the gun denominator, not the item (all Bebops by game phase: Sticky Bomb per gun
0.97-1.02 real/sim, Tankbuster 1.10 late).

What was wrong: Uppercut releases Tankbuster on a flat share of its hits whatever their size (215 Uppercuts alone on
their tick by 27 holders: 7-26% in every 20-damage bin from 80 to 200 dealt, 38 of 215 overall; the misses come a
median 37 s after the last release, so not for lack of charge). The sim applied the 165 minimum, so only 5% of its
Uppercuts released. Now `AbilityImpl.tankbuster_chance` (Uppercut: `bebop.TANKBUSTER_CHANCE` = 0.18) releases it on
that share of hits and skips the minimum; Mystic Burst keeps its 80 dealt check (its Uppercut share falls with hit
size in replays, likely holders selling it late, so not changed). Nothing refit: Bebop has no per-hero Tankbuster
factor and the pooled one is above 1 (uncut).

Results (main -> this, full sample, same machine): audit mix 0.0309 -> 0.0308, hero x item |log real/sim| 0.2335 ->
0.2328; Bebop Tankbuster 1.53 -> 1.35, Bebop sources 0.0252 -> 0.0245; split halves (even / odd match ids, Bebop
only, nothing fitted): sources 0.0292 -> 0.0290 and 0.0212 -> 0.0212, odd-half Tankbuster 1.12 -> 1.04 (even half
under 20 holders). sim_vs_win 27k for Bebop unchanged (only Bebop's Uppercut changes). Left: the gun of spirit-built
Bebops; Tankbuster under on Paradox / Drifter / Violet (pooled real/sim 1.42, uncut) is not this.

## Paradox's Carbine count (2026-10-26)

Paradox had the 6th widest mix gap (0.062: gun 0.28 vs 0.24 real, melee 0.046 vs 0.025, Kinetic Carbine / Pulse
Grenade / Swap 1.2-1.5x under per gun damage, Tankbuster 1.6x, Mystic Burst 1.8x, Spirit Burn 2.6x). In 70 Phantom+
replays (`scripts/mechanics/carbine_replays.py`, fight-length raw) against the audit's own duels:

| | real | sim |
|---|---|---|
| Carbine hits per 1000 gun damage | 3.7 | 1.9 |
| Carbine hit, median, at 30 / 60 / 90% of the match | 196 / 432 / 508 | 351 / 613 / 888 (before landing) |
| his gun hit, median, same points | 17 / 26 / 31 | 17 / 26 / 31 |
| Carbine hits per fight (fights where he dealt 300+) | 0.67-0.77 | 0.60-0.68 per duel |
| gap from his last gun hit to a mid-fight Carbine hit, median | 3.2 s | 2.9 s |

So his gun hits are right and the Carbine hit is ~0.6x the sim's full-charge formula, at every stage and at T2 and T3
alike (a Carbine hit is 11.6x his median gun hit at 30% of the match, 16.4x at 90%, sim 21-29x). A short charge
explains part of it (hits that come less than 2 s after his last gun hit are 5.6-9.4x his gun hit, longer ones level
off at ~13x), the rest is the formula. Per fight the count is right; the gap is that a real fight is short and
mostly Carbine-opened (half the hits are the fight's first damage), so real Paradox lands twice the Carbines for his
gun damage. 1102 of 1375 real Tankbuster releases come with a Carbine hit (Swap 216, Pulse Grenade 28), so Tankbuster
and Mystic Burst follow the count.

Tried, on even/odd match halves (fit the ability length corrections on one, audit the other):

| | mix, odd half | mix, even half |
|---|---|---|
| main | 0.054 | 0.074 |
| refit (3 rounds `ability_corr_heroes.py --hero Paradox`) | 0.051 | 0.036 |
| Carbine at 0.6x + refit | 0.065 | 0.055 |
| Paradox fights 0.877x the pooled length (fit_length.py's hero_mean_ratio) + refit | 0.051 | 0.034 |
| the same at 0.7x + refit | 0.049 | 0.034 |

The smaller Carbine is worse: Mystic Reverb echoes the hit (1.37x under) and the length correction just scales the
hit back up, so the count stays as it is. Shorter Paradox fights move Tankbuster a little (1.63 -> 1.42 at 0.7x) and
need a per-hero fight length the engine doesn't have. Kept: the refit alone, better on both halves (redone on main after #107/#110: odd 0.058 -> 0.052, even 0.075 ->
0.043). Full sample: Paradox 0.064 -> 0.045 (gun 0.278 -> 0.252, abilities 0.435 -> 0.502, real 0.483; length_corr
Pulse Grenade 1.236 -> 1.680, Kinetic Carbine 1.204 -> 1.437, Paradoxical Swap 1.526 -> 2.350), then
`item_landing_heroes.py --hero Paradox` (Express Shot, Headhunter barely move); player-weighted audit 0.0308 ->
0.0303, other heroes move only by duel noise. sim_vs_win 27k (correlation, higher is better) flat: all
pairs 0.171 -> 0.172, damage items 0.054 -> 0.055, per item 0.251. Left: Tankbuster
1.72x under and melee 0.6x over; the count needs short, Carbine-opened fights in the duel model.


## Carbine pokes (2026-10-26)

Follow-up of "Paradox's Carbine count": where real Paradox's extra Carbines per gun damage come from. In the 260
fight-length replays (`scripts/fight_length/ability_pokes.py`, fit_length.py's fights: gaps < 5 s, 4+ hits both
ways):

| | real |
|---|---|
| Carbine hits outside any fight (pokes: a lone hit, or a target that doesn't answer) | 58% (his gun damage: 44%) |
| Carbine hits per 1000 gun damage, in fights / in all | 2.78 / 3.73 (sim 1.9) |
| poke hits per fight of his | 0.55 |
| median Carbine hit / his median gun hit, in fights / pokes | 13.7x / 21.5x (sim formula 21-29x) |
| fights opened by a Carbine | 24% (the sim's precast already opens ~25%) |
| Tankbuster with the Carbine hit, in fights / pokes | 39% / 48% |

So the duel was not missing Carbine-opened fights: it was missing the pokes beside them, which are full-charge hits
(the formula's size), while hits in fights, openers included, are 0.64x that. New `Mechanics.pokes` (on with
fight_length): an ability with a used row in `data/ability_pokes.json` lands its real poke hits per fight beside the
duel (`fight.add_pokes`): one cast on the duel's target in a fresh engine (full health, cooldowns ready, no gun, no
other casts, 10 s for Mystic Reverb's echo and DoTs), its damage and procs added x pokes_per_fight to the duel's
damage, the fight itself untouched. `survival.survive` (overall score, sim_vs_win) adds the hero's own pokes too.
Kinetic Carbine in a fight deals `chrono.CARBINE_FIGHT_HIT` = 0.64 x the formula, a poke the full hit. Only Paradox's
Carbine is used: it is the one ability whose poke hits are much bigger than its fight hits (Sinclair's Vexing Bolt
1.5x is next); other abilities with many pokes (Grey Talon Guided Owl, Ivy Air Drop, Lurking Terrors) are in the
file for later.

Split-half (fit on one half: 3 rounds `ability_corr_heroes.py --hero Paradox`, then 3 rounds of
`item_landing_heroes.py --hero Paradox` with an ability round between; audit the other half; same recipe for both):

| held-out half | mix, main | mix, pokes | sources, main | sources, pokes | holders' item log error, main | pokes |
|---|---|---|---|---|---|---|
| odd | 0.051 | 0.031 | 0.049 | 0.026 | 0.32 | 0.09 |
| even | 0.044 | 0.035 | 0.045 | 0.037 | 0.43 | 0.14 |

(Two item rounds on main change nothing; the gain is the pokes.) Full sample: Paradox 0.045 -> 0.030, sources
0.041 -> 0.024; holders-only real/sim Tankbuster 2.08 -> 1.14, Mystic Burst 1.81 -> 1.12, Mystic Shot 1.49 -> 1.24,
Spirit Burn 2.32 -> 1.00, Mystic Reverb 1.12 -> 0.99. length_corr Kinetic Carbine 1.437 -> 1.052, Pulse Grenade
1.680 -> 1.724, Swap 2.350 -> 2.344. Paradox's Mystic Reverb row falls to 0.315: a poke's echo hits a full-health
target (+10% of current health) every time, while real Reverb lands 0.3-0.37 echoes per Carbine hit in pokes and
fights alike. Player-weighted audit 0.0303 -> 0.0299 on main after #113 (only Paradox moves). sim_vs_win 27k flat: all pairs 0.172 -> 0.171, damage items 0.055 -> 0.054, per item
0.251 -> 0.251 (Paradox is 1 of 44 heroes and pokes only add his own damage). Left: melee 0.63x over.

## Item rows per total damage (2026-10-26)

The audit's item tables (and so `item_landing_heroes.py`, which fits on the hero x item rows) divided an item's
damage by the holder's gun damage while it was owned. The sim follows how much a player shoots only through build
and aim (per-player real vs sim gun share correlates 0.3-0.8 by hero), so a build that barely shoots gets a sim gun
denominator that is too big: Bebop's Mystic Reverb holders' real gun share is half the sim's, and Tankbuster, Sticky
Bomb and Uppercut all read ~1.4x under on those Bebops (PR #110). Divided by all of the holder's damage while owned
instead, Bebop Tankbuster reads 0.97 (was 1.34), Mystic Burst 1.03 (1.16).

Per total damage the rows are steadier: the even/odd match halves' hero x item ratios agree better (mean |log A -
log B| 0.105 -> 0.072, correlation 0.91 -> 0.95, 120 shared rows). Fitting the per-hero item factors (two passes of
`item_landing_heroes.py` from main's factors) on one half and auditing the other:

| fit half -> audit half | per-source gap, per gun fit | per total fit | mix, per gun fit | per total fit |
|---|---|---|---|---|
| even -> odd | 0.0361 | 0.0346 | 0.0350 | 0.0347 |
| odd -> even | 0.0331 | 0.0319 | 0.0295 | 0.0300 |

(per-source gap = player-weighted half the summed absolute share gaps over every source.) Full sample after two
passes, on main after #117: mix 0.0284 -> 0.0274, per-source gap 0.0278 -> 0.0257; 139 hero x item factors (was 127),
mostly lower (Bebop Mystic Reverb 0.56 -> 0.36, Tankbuster on Bebop/Celeste/Rem/Solomon now just under 1). sim_vs_win
27k (on main after #114): all pairs 0.175 -> 0.173, damage items 0.054 -> 0.052, edges clear of noise 0.273 -> 0.270, per item 0.251 -> 0.248
(as flat as PR #85's 0.176 -> 0.173). `AUDIT_NORM=gun` gives the old tables. The per-source ratios (and
`ability_corr_heroes.py`) stay per gun: they pool every player of a hero, where per gun and per share have the same
fixed point. Scripts that import the audit's `sim_player` for its held-item rows (`item_landing.py`, `length_factors.py`) keep per gun: only the audit's own run defaults to total. The pooled `item_landing.py` fit is unchanged
(per gun; refitting it moves pooled factors a lot, see "Per-hero item factors").

## Baba's gun: 8.8 per shot, not per pellet (2026-10-26)

Baba had the audit's widest mix gap (0.093) with Torment Pulse 2.17x under per gun, though Torment Pulse itself matches
replays (uptime and hit size). The anchor was off: her gun dealt 2.0x real damage per shot (sim gun damage / shots vs
replay gun damage / `shots_fight4`, `gun_calib/gun_stats.json.gz`; other heroes 0.93-1.33x), and every Baba ability,
melee and item factor is fitted relative to gun damage, so all her sources ran 2-3.6x real per fight second while the
time-based Torment Pulse could not follow.

Replays: a Baba gun hit is one damage event per shot. In the first 70 s (level 1, no items) the values peak at 9 (8.8
body) and 14 (x1.65 head) with steps near 3 and 6; almost none reach 17-26, which 2-3 pellets of 8.8 would give
although the API counts 2.14 pellets per hitting shot. Mo & Krill's 2.82 x 4 peak at 3, 6, 9, 12 as listed. So the
data's 8.8 (and its level growth) is the whole shot: `build.SHOT_SPLIT_PELLETS` divides it by the pellets (and
`BuildUp.per_hit`). Threadsap's gun bonus is one event on the tick of 74-78% of gun hits, one shot's worth each: now
once per landed shot, not per pellet. After the split the gun reads 0.67x real per shot.

Refit of Baba only (`refit_landing_heroes.py --iterate 2`, 3x `ability_corr_heroes.py`, `melee_audit_fit.py`,
3x `ability_corr_heroes.py` again since the melee rate drives Granny Long Legs' ground pounds, 2x
`item_landing_heroes.py --hero Baba`). Split-half (fit on even match ids, audit odd, and reverse), old code with the
same refit as reference:

| fit -> audit | mix old | mix new | per-source old | per-source new |
|---|---|---|---|---|
| even -> odd | 0.099 | 0.032 | 0.105 | 0.056 |
| odd -> even | 0.090 | 0.049 | 0.108 | 0.055 |

Full sample: Baba 0.093 -> 0.031, Torment Pulse holders 1.87 -> 0.98, all heroes 0.0256 -> 0.0243; melee rate
0.176 -> 0.070. sim_vs_win 27k all pairs 0.166 -> 0.167, edges clear of noise 0.266, per item 0.238. Drifter's
"3 x 19.5" looks the same in replays (early hits peak at 20, never 39 or 58; gun 1.64x real per shot): not changed.

## Abrams' gun per shot (2026-10-26)

The Drifter thread read Abrams' gun at 2.0x real per shot (sim gun damage / trigger pulls in the Phantom+ audit duels
vs replay gun damage / shots within 4 s of hero damage). That compares different players at different times: the 16
Abrams in the replays aimed 0.228 per pellet where the sample's 138 aim 0.278 (1.22x), and his real hits come early
(laning) while the audit duels sit at 30/60/90% of the match (1.17x on the same players). `scripts/gun_calib/
shot_damage.py` runs the audit duels for the replay matches' own players (fetched in `fetch_validation` format) at 19
evenly spaced points and takes the per-player sim/real geometric mean: Abrams 1.19x (95% 1.05-1.35, 16 players), in the
band of Billy 1.19, Danny 1.17, Kelvin 1.15, Apollo 1.20 (Haze 1.03, Wraith 1.01, Bebop 1.00).

Checked against his replay gun DamageEvents (16 matches, 2111 hits; `effectiveness` is the falloff, `pre_damage` the
damage before resists, head pellets come as their own event): body hits sit at whole multiples of 3.6 x (1 + weapon
power) per pellet, so 3.6 is per pellet as listed; falloff 0.94 damage-weighted (sim 0.96); Close Quarters' +20%
shows on hits inside 17 m; Shoulder Charge T3's +1.5 lands per pellet after weapon power, within 6 s of a charge hit
(the sim's weapon % conversion gives the same). Real pellets land together (a third of shots hit, 5.5 pellets each;
the sim draws them one by one, 0.86 of shots hitting) but damage per shot doesn't depend on that. No model change.

Same measure on main for the other split-pellet guns: Drifter 1.36x (1.27-1.46), Baba 0.61x (0.55-0.68); with the
Drifter PR's whole-shot landing Drifter 0.74x, Baba 0.85x. Shot-count outliers (replay shot steps don't match the
sim's trigger pulls: charged or alt-fire guns): Paradox 6.7, Venator 3.3, Seven 3.1, Lash 3.0, Sinclair 2.4, Violet
1.8.
## Drifter's gun: 19.5 per shot; split shots land whole (2026-10-26)

Drifter's "19.5 x 3" is the whole shot as well: in the first 45 s of 10 Phantom+ replays (pulled with the gun's
`hits`/`crit_damage` columns) his body hits peak at 19-20 and his heads at 26-27, with nothing near 39 or 58, which two
or three pellets of 19.5 would give although the API counts 1.87 pellet hits per hitting shot. The sim's gun dealt
1.63x real per shot. Every other shotgun (Abrams, Calico, Mo & Krill, Shiv, Pocket, Silver, Yamato, Rat King) shows
volleys of several pellets' worth, so the data is per pellet there. `build.SHOT_SPLIT_PELLETS` gains 64.

Split, the two guns read low instead (Drifter 0.57x, Baba 0.65x real per shot): their replay hits sit at the full
shot, but the sim drew each pellet on its own with the API's pellet accuracy, landing ~1.2 pellets per hitting shot.
`SHOT_SPLIT_PELLETS` now maps each hero to a shot-landing factor and `Engine.fire` lands such a shot whole (pellets
and head or body together) with chance pellet accuracy x that factor. Drifter 2.16: fitted on the replay players
themselves (`gun_calib/shot_damage.py`), 0.97x real per shot (95% 0.90-1.05; other heroes 1.0-1.04x). Baba 1.40 =
pellets / API pellet hits per replay gun hit (3 / 2.14), 0.88x per shot: at the per-shot fit (1.59, 1.01x) her
split-half refit got worse both ways (mix 0.029 -> 0.045 / 0.039 -> 0.029). Per-shot on-hit items
(`items_fx.shots_hit`) and Threadsap's once-per-shot bonus follow; Express Shot's double shot is two whole shots.

Refit of Baba and Drifter only (same order as for Baba above). Split-half, old code with the same refit as reference:

| hero | fit -> audit | mix old | mix new | per-source old | per-source new |
|---|---|---|---|---|---|
| Drifter | even -> odd | 0.046 | 0.026 | 0.031 | 0.019 |
| Drifter | odd -> even | 0.033 | 0.013 | 0.031 | 0.027 |
| Baba | even -> odd | 0.029 | 0.034 | 0.054 | 0.047 |
| Baba | odd -> even | 0.039 | 0.017 | 0.052 | 0.049 |

Full sample: Drifter 0.045 -> 0.021, Baba 0.031 -> 0.023, all heroes 0.0243 -> 0.0233. sim_vs_win 27k all pairs
0.167 -> 0.170, edges clear of noise 0.266 -> 0.270, per item 0.238 -> 0.240. Baba's Granny Long Legs fits a
landing x length_corr of 2.9 (2.0 before, 1.8 before Baba's split): the pounds per cast or their damage are short
of real, not new here (follow-up).

## Target health for Opening Rounds (2026-10-26)

Opening Rounds adds weapon damage against targets above half health. `scripts/fight_length/target_health.py` measures
how gun damage spreads over the target's health share at the hit (before it). The real side uses every hero gun hit in
the 260 Phantom+ replays (`fetch_fights.py` extracts, weapon id from `data/game/weapons.json`). The sim side uses the
damage audit's duels, with each hit weighted by P(fight still going):

| | gun damage on targets above half health |
|---|---|
| real, all gun hits on heroes | 0.628 |
| real, inside pair fights (lane / mid / late) | 0.640 (0.686 / 0.635 / 0.614) |
| sim duels before | 0.846 |
| sim, as Opening Rounds now sees the target | 0.643 / 0.633 (even / odd match halves; real 0.641 / 0.640) |

The cause is that a sim target starts every duel at full health, and only the duel's opponent damages it. In real
pair fights, 47% of targets enter in the top decile and the rest enter already hurt. During the fight, other enemies
add 0.71x as much damage to the target as the pair opponent does.

`Mechanics.target_health` (on, with fight_length) handles this. When the enemy holds an item in
`mechanics.TARGET_HEALTH_ITEMS` (Opening Rounds), that item sees the fighter's health
(`Fighter.item_hp_frac`) as short by two amounts:

- a real entry deficit (the same draw as `entry_gate`, shared through `Fighter.entry_drawn`);
- `TARGET_ASSIST` x the damage the fighter has taken in the duel.

The fighter's real health, the fight's length and execute gates don't change, as with `entry_gate` (making the health
itself short, `entry_hp`, hurt sim_vs_win). With the raw 0.71, the share falls to 0.54 and damage piles up at 0-10%,
because real targets losing health that fast also die or back off sooner. So `TARGET_ASSIST` is fitted instead: 0.35
matches real on both halves (0.25 gives 0.67 / 0.66). An immortal enemy's refill (survive) starts a new life that the
item sees as full; without that, the overall search's enemy would read 0% for the rest of the fight.

Tankbuster, Mystic Reverb and Rupture deal damage based on the target's current health, so the same skew applies to
them. They were left as they were here; Tankbuster and Decay (Rupture) followed with their factors refit, see "Target
health for Tankbuster and Decay" below.

Results:

| | main | this |
|---|---|---|
| damage audit mix (player-weighted) | 0.0243 | 0.0243 (gun share 0.2465 -> 0.2458, real 0.2431; no hero moves > 0.002) |
| sim_vs_win 27k all pairs / damage items | 0.167 / 0.047 | 0.170 / 0.051 |
| edges clear of noise / per item | 0.266 / 0.238 | 0.269 / 0.240 |
| Opening Rounds sim gain per 1000 souls (real edge -1.47 pt) | 0.0716 | 0.0648 |

Nothing is refit. Opening Rounds' bonus isn't a fitted factor, and only its holders' gun damage moves (~2%).

## Baba's melee bunches into Granny Long Legs (2026-10-26)

Granny Long Legs fitted a landing x length_corr of ~1.9 (landing 2.42, clipped to 1.5, x 1.275): the sim's ground
pounds came out at about half of real before the fit. Per pound, nothing is short: in 260 Phantom+ replays (59 Baba
players) 97% of the pounds land on the tick of a heavy bench melee, 71% of bench melees are pounds (the
`GLL_HEAVY_SHARE`), 5% of pounds hit a second hero, and a pound is 1.15x its heavy melee (median 149 vs 132). The gap
is when she melees. With her casts from `cast_timing/raw` (window = cast + 10 s, or to her last bench melee), the
bench is up 38% of her fight seconds and holds 82% of her melee hits in fights: she melees 7.7x as often on it as off
it. The sim's melee was one steady rate, so only 53% of her melee damage (and so of her heavies) fell in the window.

`baba.py` now splits her fitted melee rate into 2.17x inside the window and 0.28x outside (`GLL_MELEE_RATIO` 7.7,
average kept at the 38% uptime) through a new engine counter `melee_focus` (rate mult in, rate mult out, until), with
0.5 s weighted melee ticks so the rate follows the window's edges. In the audit 75% of her melee now lands in it.

Refit of Baba only (melee rate, ability length_corr, per-hero item factors; 4 rounds): melee rate 0.107 -> 0.126 hits/s,
Granny Long Legs length_corr 1.275 -> 0.818 (effective 1.91 -> 1.23), Spirit Strike 0.53 -> 0.64 and Spirit Snatch
0.69 -> 0.79 (melee items needed less of a cut). Split-half, old code with the same refit as reference:

| fit -> audit | mix old | mix new | per-source old | per-source new | GLL real / old / new |
|---|---|---|---|---|---|
| even -> odd | 0.031 | 0.036 | 0.053 | 0.053 | 0.103 / 0.092 / 0.097 |
| odd -> even | 0.016 | 0.017 | 0.054 | 0.056 | 0.103 / 0.122 / 0.117 |

Granny Long Legs itself is closer on both held-out halves; the mix is flat (the even -> odd half: Feed The Birds is
over there, so a fuller Granny Long Legs pushes the ability share further over). Full sample: mix 0.023 -> 0.024,
per-source 0.023 -> 0.024 (0.023 again after rebasing on the target-health change). sim_vs_win 27k (all heroes, side by side): all pairs 0.170 -> 0.170, edges clear of
noise 0.270 -> 0.270, per item 0.240 -> 0.240. Kept as the more faithful model: the fudge factor that stood in for the timing is mostly
gone, and her melee items now see her melee where she really lands it.

## Silver's wolf form on real fight timing (2026-10-26)

Survey first (scratch scripts): for every hero ability with a duration, the share of the hero's gun / melee / ability /
item damage landing inside [cast, cast + AbilityDuration], real Phantom+ pair fights (fight_length + cast_timing
replays, every damage id named by hashing raw/items.json class names) against the audit duels (expected over real
fight lengths). For the self buffs the in-window share is close: Wraith Full Auto gun 0.40 real / 0.36 sim, Grey
Talon Rain of Arrows 0.53 / 0.55, Lady Geist Life Drain 0.39 / 0.33, Rat King Royal Pestments 0.44 / 0.35, Baba
Granny Long Legs melee 0.74 / 0.78 (after the bunching above). Several sim buffs are up longer than real (Seven Power
Surge, Solomon, Paige: recasts), which is cast frequency, not bunching. The one large gap was Silver's wolf form.

Read from her hits (Lycan Curse's cooldown starts when the form ends, so its cooldown starts are not casts): a run of
wolf hits (Lycan Claws, Go For The Throat, Mauling Leap, Tail Whack) broken by a human-form hit or a 6 s gap. In 2383
pair fights of 50 Silver players: 12% start with her already in wolf form, the form is up 21% of fight time, and wolf
hits are 40% of her damage (claws 15%, rifle 25%). She transforms in only ~1 in 3 of the other fights (Kaplan-Meier:
3% by 2 s, 11% by 5 s, 32% by 10 s, 60% by 20 s). The sim started every duel at 0 rage and transformed 7-12 s into
nearly all of them (by 5 s 2%, by 20 s 95%): wolf form 14% of fight time, wolf hits 25% (claws ~5%), and the wolf
abilities carried landing x length_corr fudges of 1.25-1.55 while her human abilities were cut to 0.5-0.7.

Rage and the cooldown carry over between fights. `werewolf.LycanCurse.draw_plan` (Mechanics.execute_timing's draw,
`WOLF_TIMING`) now draws each fight's first transform from data/wolf_timing.json (scripts/mechanics/wolf_timing.py):
cast at t = 0 (already in wolf form) in 12%, else at a real time or not at all; later casts follow the rage rule.
Deterministic fights keep the rage rule. Audit duels: wolf form 23.5% of fight time, wolf hits 28%, claws 9%.

Refit of Silver only (her three wolf rows got their `class` so ability_corr_heroes.py fits them; 3 rounds, then
item_landing_heroes.py): landing x length_corr Slam Fire 0.51 -> 0.61, Boot Kick 0.72 -> 0.86, Entangling Bola 1.06
-> 1.17, Go For The Throat 1.25 -> 1.15, Mauling Leap 1.45 -> 1.09, Tail Whack 1.55 -> 2.09 (summed |log| 2.09 ->
1.76). Audit, full sample: mix 0.034 -> 0.019. Split-half (old code refit the same way as reference): one draw per
duel and 3 duels a player make her wolf shares swing between samples, so held-out runs were averaged over 5 draw
offsets: mix 0.033 -> 0.020 and 0.032 -> 0.024 (better both halves), per-source 0.037 -> 0.034 and 0.028 -> 0.039.
sim_vs_win 27k (all heroes, side by side): all pairs 0.172 -> 0.173, edges clear of noise 0.273 -> 0.273, per item
0.243 -> 0.243. Kept as the more faithful model: the wolf form comes when real players have it, the mix is closer on
both held-out halves, and four of her six ability fudges moved toward 1.

## Target health for Tankbuster and Decay (2026-10-26)

`target_health.py items` takes the items that deal damage from the target's health and measures, for each real hit
on an enemy hero in the 260 replays, the target's health share before it, and the hit's damage per current and per
max health by health decile (the one that stays flat is what the item scales with):

| item | scales with (replays) | mean target health share at a hit: real | sim duels before | as the item sees it now |
|---|---|---|---|---|
| Tankbuster | current health (40 + 7.5%) | 0.586 (halves 0.585 / 0.588) | 0.71 | 0.59 / 0.59 |
| Decay (Rupture) | current health (1.9%/s) | 0.628 (0.643 / 0.615) | 0.74 | 0.65 / 0.65 |
| Toxic Bullets | max health (control) | 0.485 | 0.71 | - |
| Mystic Reverb | neither (see below) | 0.637 | 0.68 | - |

Tankbuster and Decay are now in `TARGET_HEALTH_ITEMS` and deal their health part from `Fighter.item_hp`: the entry
deficit and third parties as for Opening Rounds, but at `CURRENT_HEALTH_ASSIST` 0.15 x the damage taken instead of
0.35 (0.35 piles Tankbuster hits on near-empty targets, mean 0.53 and 13% in the bottom decile vs real 8%; 0.15
matches the real deciles too).

Refit (`item_landing_heroes.py --item Tankbuster --item Decay --pooled --keep-level <audit before>`, audit,
`--item` alone for the hero rows, audit). Tankbuster's pooled factor is uncut (1.42) so its 1.04 -> 1.14 real/sim
drop can't be fit by the factor; `--keep-level` scales its length_corr 0.91 -> 1.00 to keep the old level (the
change moves which targets it hits hardest, not how often real holders get it). Decay's pooled factor goes 1.17
(uncut) -> 0.97. Split-half (fit on even match ids, audit the odd half): pooled Tankbuster 1.144 -> 1.076, Decay
0.929 -> 0.903, these items' hero rows |log real/sim| 0.172 -> 0.122 (unfit -> fit; main's own factors were fit on
both halves, so it is no held-out baseline).

Mystic Reverb: the sim adds the tooltip's 10% of the target's current health to the echo, but real echoes on heroes
don't scale with health at all (1457 echoes: damage = 0.27 x the trigger damage 3 s earlier + 0.006 x current +
0.007 x max health + 83; median echo / trigger 0.48, the 50% alone). Without the bonus (factors refit, real/sim 0.80
-> 1.06) sim_vs_win's damage items fell 0.056 -> 0.038 and all pairs 0.172 -> 0.170: its real win edge is positive on
most heroes (up to +5 pt), and the overrated echo is what gave it value. So it stays on
(`MysticReverb.CURRENT_HEALTH_BONUS`) until something else explains Reverb's edge.

Results (sim_vs_win per pair: the Decay change alone lifts damage items by ~0.011, Tankbuster's leaves every pair as
it was):

| | main | this |
|---|---|---|
| damage audit mix (player-weighted) | 0.0233 | 0.0235 |
| real/sim: Tankbuster / Decay (holders, per damage) | 1.04 / 0.86 | 1.05 / 0.96 |
| sim_vs_win 27k all pairs / damage items | 0.172 / 0.056 | 0.175 / 0.066 |
| edges clear of noise / per item | 0.273 / 0.242 | 0.277 / 0.248 |
| Decay sim gain per 1000 souls (real edge -4.55 pt) | 0.0889 | 0.0809 |

## Silver's Tail Whack and the wolf abilities' holds (2026-10-26)

After the wolf form moved to real timing, Tail Whack's landing x length_corr went 1.55 -> 2.09 while the other wolf
fudges moved toward 1. Replays (fight_length raw, 50 Silver players): per hit Tail Whack matches its formula
(45 + 1.5 x spirit power, pre-resist, ratio ~1.1 with the T1 +25 unknown), so the gap was cast count. Real wolf runs
open with their abilities at once (median first hit after the run start: Mauling Leap 0.5 s, Tail Whack 0.7 s, Go For
The Throat 1.1 s), Tail Whack 0.85x as many casts as Go For The Throat. The sim cast it 0.70 times per transform
(0.55x Go For The Throat), median 2.9 s in: each wolf ability shares an AbilityState with the human ability in its
slot, and that slot's first-cast hold (Mechanics.cast_timing, fitted on the human ability's own class) held the wolf
casts too. The Bola's long hold blocked Tail Whack most (in the audit duels 7124 blocked checks vs 115 casts).

Fix: `AbilityImpl.held(c)` says whether the slot's hold applies; Silver's wolf slots answer no while transformed, and
a wolf cast doesn't count as the human ability's first cast (`held_opener`). Replays also show 1.20 enemy heroes hit
per Tail Whack (Go For The Throat 1.07, Mauling Leap 1.01): `werewolf.TAIL_WHACK_OTHERS` = 0.20 x Damage lands on the
others near the target (mechanics._splash). Sim now: Tail Whack 1.04 casts per transform, median 1.1 s in.

Refit of Silver only (ability_corr_heroes.py 3 rounds, then item_landing_heroes.py): landing x length_corr Tail
Whack 2.09 -> 0.96, Go For The Throat 1.15 -> 0.76, Mauling Leap 1.09 -> 0.59 (both now cast as often as their
cooldowns allow, more than real players do), human abilities unchanged. Audit, full sample averaged over 5 draws
(`AUDIT_SEED`): mix 0.0196 -> 0.0180, per-source 0.0178 -> 0.0161. Split-half (main refit the same way as
reference, 5 draws): per-source 0.048 -> 0.043 and 0.047 -> 0.037 (better both halves), mix 0.022 -> 0.018 and
0.026 -> 0.028; held-out Tail Whack real/sim 0.76 -> 0.82 and 1.18 -> 1.01.
sim_vs_win 27k (all heroes, main vs this side by side): all pairs 0.173 -> 0.174, edges clear of noise 0.273 -> 0.273,
per item 0.243 -> 0.244.

## Aim table rebuilt from Phantom+ (2026-10-26)

`data/skill_defaults.json` (each hero's hero-only gun accuracy and headshot rate p25/p50/p75/p90, median bullet
distance; the searches' aim and the dummy defaults) came from the 400-match `matches_sample.jsonl.gz` of 13 Oct,
below Phantom. Now `scripts/fetch_aim_sample.py` pulls final custom stats of 4,200 Phantom+ ranked matches (average
badge 91-116, 420 a day over 10 days of patch 09-29, six 4-hour slices a day so every region's prime time is in;
bulk metadata endpoint, ~1.5 min, no SQL quota) into `validation/aim_sample.jsonl.gz` (no account ids), and
`build_skill_defaults.py` builds from it: 42,523 player-games with >= 300 hero-aimed shots (was 4,486), every hero
>= 171 (was 26). Graves and Deadman Danny are skipped explicitly (API under-records their guns; aim stays replay-fitted
in `gun_calibration.json`).

Change vs the old table: all-hero p50 0.2585 -> 0.2623, p75 0.3197 -> 0.3264; per hero p50 mean |change| 1.1 points
(Shiv +3.3, Violet +2.6, Lady Geist +2.3; Doorman -5.5, old n was 26), headshot rate +0.2 points on average.
No refit: landing/item/melee fits and the damage audit use each player's own real aim, the table only fills in
low-shot players and the distance. Damage audit (full phantom_sample, main vs this): mix 0.0233 -> 0.0236 (noise;
Mo & Krill +0.007 from his 10.0 -> 9.4 m distance). sim_vs_win 27k all heroes: all pairs 0.177 -> 0.171, edges clear
of noise 0.277 -> 0.271, per item 0.249 -> 0.248. Seven alone is 0.0043 of the drop: his p75 aim 0.266 -> 0.272 tips
his 27k popular build over a kill threshold, so every gun item's gain jumps ~+0.16 together (Close Quarters, HVR,
Extended Magazine), a knife-edge rather than a model change; without Seven the change is -0.001.
Refresh after a patch: `python3 scripts/fetch_aim_sample.py && python3 scripts/build_skill_defaults.py` (defaults =
the committed sample: --badge 91 --days 10 --per-day 420, i.e. 70 matches per 4-hour slice; the Ranked filter runs
after the per-slice limit but every fetched match was Ranked). Matches of 25+ minutes only, the same filter as the
old sample (fetch_validation.py), so old vs new differ by rank and size, not game length.

## Silver's claws and rifle aim (2026-10-26)

After the wolf form moved to real timing and its abilities to real holds, Silver's wolf hits were still 28% of her
damage against real 40% (wolf_timing.py's per-pair-fight count). Broken down on the 50 replay players (fight_length
raw, union of her pair fights, damage to enemy heroes) against the audit duels (expected over real fight lengths):

| | real | sim before | sim now |
|---|---|---|---|
| wolf form up, share of fight time | 0.18 | 0.25 | 0.24 |
| Lycan Claws, share of her damage | 0.158 | 0.099 | 0.155 |
| rifle, share of her damage | 0.233 | 0.263 | 0.212 |
| wolf hits (claws + Go For The Throat + Mauling Leap + Tail Whack) | 0.357 | 0.27 | 0.32 |
| claw hits per wolf run | 5.7 (run 6.8 s) | 3.8 (6.1 s) | 5.9 (5.8 s) |
| rifle damage per shot, replay players (shot_damage.py, rifle only) | 1 | 1.26 (1.13-1.41) | 1.01 |

The form is up as often as real (more, if anything) and the wolf abilities already matched per source; the claws
were short and the rifle long. Both aim with the player's API hero accuracy, which is mostly the rifle's pellets
(0.41): the claws are one large swing at close range and land ~1.5x that per swing in replays, and the rifle's
pellets land less than the blend says. `Stats.hit_mult` (Engine.fire's hit chance x it): `werewolf.CLAW_HIT` 1.55 for
the claws, `build.GUN_HIT` {Silver: 0.80} for the rifle. Claw damage per hit already matched (real mean 90, sim 93). Both are fitted at her
sample aim (~0.41): hit chance is capped at 1, so above ~0.65 aim (a dummy-page slider) the claws gain less than 1.55x.

Refit of Silver only (ability_corr_heroes.py 3 rounds, then item_landing_heroes.py): landing x length_corr moved
little (Slam Fire 0.70 -> 0.75, Entangling Bola 0.93 -> 0.98, Tail Whack 1.17 -> 1.07; items Stalker, Spirit Snatch,
Cold Front rows), as her gun total stays where it was. Audit, Silver, full sample averaged over 5 draws: mix 0.0204
-> 0.0174, per-source 0.0209 -> 0.0184. Split-half (main refit the same way as reference, 5 draws per held-out half):
per-source 0.0378 -> 0.0378 and 0.0435 -> 0.0438, mix 0.0242 -> 0.0240 and 0.0310 -> 0.0282 (the audit pools both
weapons as gun, so it can't see the split itself; claws alone at 1.6 with the rifle as it was: mix worse on one half).
sim_vs_win 27k (all heroes, main vs this side by side): all pairs 0.177 -> 0.176, edges clear of noise 0.277 ->
0.276, per item 0.249 -> 0.248, damage items 0.066 -> 0.066 (flat: only Silver changes).
The remaining wolf gap is the wolf abilities in fights (real 20% of her pair-fight damage, sim 16%; they match per
whole match), likely team fights.

## McGinnis's Mini Turret (2026-10-26)

McGinnis was second-furthest from real in the audit (mix 0.083): Mini Turret 58% of her sim damage against 47% real,
her gun 15% against 20%. Per audit phase the gap was largest in the lane (30% of the match: turret 0.65 sim vs 0.45
real, gun 0.15 vs 0.31). Not her ability order: duels on each player's real unlock and upgrade order (the sample's
item list carries the ability events) put the turret at 0.59, no better.

Cause: from tier 2 (3 charges, 3 s between charges, most players by 5-8 min) the sim cast every charge on sight, ~2.6
turrets by 10 s into every duel. Real McGinnis players place far fewer (summons replays, 160 Phantom+ matches, own
turrets placed from 1 s before a pair fight's first hit, wall turrets dropped: they come in groups a few ticks
apart): 0.89 by 10 s in the lane (< 15 min), 1.11 mid, 1.13 late, and the gap to the next one is median ~9-11 s,
2-9% within 2 s (scripts/mechanics/turret_gaps.py -> data/turret_gaps.json).

`forge.TURRET_PACING` (on, with fight_length and cast_timing, in fights with an rng or a fight phase): after each turret
the next one waits a gap drawn from the real ones for the net worth's phase (mechanics.LENGTH_PHASES), as well as for
its charge. Sim turrets by 10 s: 1.05 / 1.10 / 1.21 at 30 / 60 / 90% of the match. Deterministic fights (the dummy
page) keep casting on sight.

Audit, McGinnis, before any refit, on 6 draws (AUDIT_SEED 0-5): mix 0.083 / 0.116 / 0.113 / 0.106 / 0.100 / 0.102 ->
0.033 / 0.072 / 0.073 / 0.048 / 0.049 / 0.052. Draw 0 (the default) is a lucky one for her: her 49 players x 3 duels
move the mix by ~0.03 between draws, so the refit averages 4 draws. Heavy Barrage was already over on the other draws
(0.18-0.25 vs real 0.14) and pacing raised its share further.

Refit of McGinnis only (ability_corr_heroes.fit on the mean of draws 0-3, 3 rounds; then item_landing_heroes.py --hero):
length_corr Mini Turret 4.01 -> 3.85, Heavy Barrage 9.66 -> 4.44, Spectral Wall 1.66 -> 2.41; Escalating Exposure row
0.59 -> 0.62. Split-half (fit on draws 0-3 of one half's matches, audit draws 6-9 of the other; reference: pacing with
the old corrections): per-source 0.102 -> 0.027 and 0.071 -> 0.037, mix 0.056 -> 0.047 and 0.044 -> 0.040. The
one-draw --split (draw 0 only) refused it (mix +0.004 on one half). Whole sample, draws 6-9: mix 0.032, turret 0.49
vs real 0.47; draw 0: 0.028 (from 0.084). Whole audit mean mix on main after #135: 0.0259 -> 0.0247.
sim_vs_win 27k (all heroes, main vs this side by side): all pairs 0.172 -> 0.170, edges clear of noise 0.268 -> 0.266,
per item 0.250 -> 0.244, damage items 0.067 -> 0.066 (about flat; McGinnis also moves every hero's fights against her).
turret_gaps.py reads the summons replays in the shared folder (manual refit, like the other replay fits).

## Ability recasts on real timing (2026-10-26)

The sim recast every ability the moment its cooldown was up (its own rule allowing). `scripts/cast_timing/recast_timing.py
real` measures what real Phantom+ players do in the 259 cast-timing replays: in each pair fight, every cast whose
cooldown runs out before the fight ends is a recast chance, ready = the cast + the player's cooldown at that moment
(the sim's `AbilityState.cooldown()` of the player's real build at that minute), delay = the next cast - ready,
censored at the fight's end (Kaplan-Meier). Charged abilities and ultimates are left out. 19k chances:

| P(recast by t s after ready, fight still going) | 0.5 s | 1 s | 2 s | 4 s | 8 s |
|---|---|---|---|---|---|
| real, pooled | 0.14 | 0.24 | 0.39 | 0.58 | 0.78 |
| sim before (typical ability) | ~0.9 | ~0.9 | ~0.9 | ~0.95 | ~1.0 |

Per ability in `recast_timing.md` (e.g. Geist Malice real 0.20 / 0.39 / 0.59 / 0.79 / 0.93, Warden Flask 0.17 / 0.33 /
0.51 / 0.72 / 0.85). `Mechanics.recast_timing` (on): after each cast of a single-charge, non-ultimate ability the next
one waits a delay past the cooldown drawn from `data/recast_timing.json` (20 equal-probability waits per ability with
100+ real chances, the chance-weighted pooled curve for the rest; abilities the sim already gates, Victor's Aura of
Suffering and Pain Battery, Solomon's Setup Bishop, skip). Draws like cast_timing (fight phase hash or rng);
deterministic fights (the dummy page) are unchanged; a cooldown reset (Refresher) clears the wait. Mean |real - sim|
of the curves (0-8 s, 40 abilities) 0.344 -> 0.119.

Split-half: waits fitted on even match ids against the odd ids' real curves and the reverse: 0.13 / 0.13 with per-ability
rows, 0.14 / 0.14 pooled-only, ~0.34 without. The two halves' pooled curves agree within 0.015.

Levels kept: `length_factors.py 4 --entry --target-entry --target-off MECH.recast_timing --write` scales every
correction so each source gives the expected source / gun it gave with recasts on ready (Geist Malice x1.47, Yamato
Crimson Slash x1.22, Mina Rake x1.22; items within 0.94-1.13). The change moves when in a fight ability damage lands and
what cooldown reduction buys, not the fitted levels.

| | main | this |
|---|---|---|
| damage audit mix (player-weighted) | 0.0231 | 0.0225 |
| sim_vs_win 27k all pairs / damage items | 0.172 / 0.068 | 0.174 / 0.069 |
| edges clear of noise / per item | 0.267 / 0.248 | 0.266 / 0.250 |
| sim gain per 1000 souls: Compress / Superior / Transcendent Cooldown | 0.019 / 0.021 / 0.013 | 0.014 / 0.017 / 0.011 |

Left: Silver's form swaps reset cooldowns (`reset_cooldown` clears the wait), so Boot Kick and Slam Fire still recast
fast in the sim; charged abilities still spend charges on ready.

## Victor's Aura of Suffering on at the fight start (2026-10-26)

The opener-timing check put Victor's aura damage late: P(first aura hit by 1 s) 0.11 in the sim against 0.46 real,
damage-weighted mean time 9.0 s against 5.2, 6% of it in the first 2 s against 26%. Its length_corr had grown to 4.83
to make up the level.

Cause: the aura is a toggle, and its cooldown starts when it is toggled OFF. In the cast-timing replays every aura
cooldown start sits at the end of a run of aura ticks (3,806 of 3,815 within 0.5 s of a run's last tick), none at a
run's start, so `fit_cast_timing.py`'s "first cast in the fight" for the aura was its first toggle-off, a median
~7.5 s in, and the sim held the toggle-on that long. Read from his hits instead (scripts/mechanics/aura_timing.py ->
data/aura_timing.json, 59 Victors, pair fights after his first aura hit of the match), real Victors keep it on
between fights: it is already on at the start of 31% of lane fights, 59% mid and 76% late (on for a median 1.7 /
3.5 / 5.0 s, so partly ramped: the first tick of a carried aura is a median 18 damage against 6 for a fresh one), and
in the other fights it goes on early (lane / mid / late by 1 s 0.27 / 0.40 / 0.47).

`frank.AURA_TIMING` (on, with Mechanics.execute_timing: fight length, cast timing, an rng or a fight phase):
AuraOfSuffering.draw_plan draws per fight, by net worth phase, either on at the start with the ramp that far along,
or a real toggle-on time (or not by 20 s). The aura's cast-timing row is dropped and fit_cast_timing.py skips
abilities with their own draw_plan. Pre-fight self-damage is not booked. Deterministic fights (dummy page) unchanged.

Refit of Victor only, on main after the recast timing (#138) (ability_corr_heroes.fit on the mean of audit draws
0-3, 5 rounds): Aura of Suffering length_corr 4.83 -> 1.045, Pain Battery 1.55 -> 1.64, Shocking Reanimation 3.06 ->
3.49. Victor audit (mean of draws 0-3): mix 0.0097 -> 0.0105, per-source 0.0359 -> 0.0077. Split-half (fit 3 rounds
on one half's matches, audit the other, draws 0-3; reference: main's model refit the same way): mix 0.0178 -> 0.0145
and 0.0163 -> 0.0158, per-source 0.0235 -> 0.0184 and 0.0198 -> 0.0181 (better on both halves). opener_timing
compare: aura first 2 s 0.06 -> 0.20 (real 0.26), mean time 9.0 -> 6.3 s (real 5.2). sim_vs_win 27k (before #138):
Victor's pairs 0.258 -> 0.250 (damage items 0.230 -> 0.238, clear edges 0.400 -> 0.404); all heroes 0.171, clear
edges 0.267, per item 0.248, damage items 0.066 (flat against main's 0.170 / 0.266 / 0.244 / 0.066).

## Cooldown items at the fight start (2026-10-27)

After the recast fix (#138) cooldown items lost 20-30% of their sim value, and they were already ranked low against
real wins: sim_vs_win 27k per-item sim gain rank (of 141) vs real Phantom+ win edge rank, before #138 / on main:
Superior Cooldown 109 / 121 (edge +0.7, rank 12), Compress Cooldown 115 / 126 (+0.4, rank 22), Transcendent
Cooldown 126 / 131 (-0.4, rank 56). Two checks on the 259 cast-timing replays:
- Recasts: real holders' wait past the (shorter) cooldown matches matched non-holders' (same hero, ability, 10-min
  bin): P(recast by 0.5/1/2/4/8 s) 0.14/0.23/0.38/0.58/0.82 vs 0.15/0.25/0.40/0.61/0.80. Measured from the cooldown
  they would have had without the items it is 0.35/0.41/0.51/0.67/0.86, so the cut is used in full; recast_timing's
  waits drawn independent of the cooldown are right.
- Fight starts: the sim opens each fight with every ability ready and holds the first cast to the real cast timing,
  whose share of fights started with an ability still cooling came from real (mostly item-less) cooldowns, so
  cooldown items bought no fight starts. `scripts/cast_timing/cdr_ready.py real` -> per fight start and single-charge
  ability (ults included): time since the last cast tau, the cooldown, the cooldown without item cdr. Ready = tau >=
  cooldown (item cdr: cooldown items, ult cooldown items, a Compress Cooldown imbue; mechanics.item_cd_keep). Ults: holders ready at 0.467 of fight starts vs matched non-holders 0.425; non-holders' tau at the
  holders' cooldown ratio (0.81) would give 0.513, so holders get rho 0.47 of it (halves by hero id parity 0.48 /
  0.47). Abilities: 0.572 vs 0.545 vs 0.616, rho 0.38 (halves 0.45 / 0.23). Holders cast more between fights, so
  their tau is shorter.
- Model (Mechanics.cdr_ready, ON): mechanics.cdr_ready_u moves the first-cast hold quantile so the ready share goes
  from r(1) to r(1) + rho x (r(k) - r(1)), k = the cooldown share the build's items leave, r = non-holders' share
  of fights with tau >= k x cooldown (per ability with >= 300 fights, else pooled ult / ability; data/cdr_ready.json).
  The real holds' early quantiles stretch over the new ready share, the late / not-cast ones shrink into the rest.
- Results (27k sim_vs_win, main -> this): all pairs 0.176 -> 0.179, clear edges 0.269 -> 0.274, per item 0.255 ->
  0.260, damage items 0.068 -> 0.069. Superior Cooldown sim gain 0.0171 -> 0.0222 (rank 121 -> 108), Transcendent
  0.0111 -> 0.0138 (131 -> 127), Compress 0.0136 -> 0.0152 (126 -> 123). Damage audit mix 0.0228 -> 0.0232 (noise:
  real builds hold few cooldown items). Cooldown items still rank below their real edge: what is left is outside a
  fight (farming, pushing, more casts between fights), which the overall score does not see; the win blend carries it.

## Djinn's Mark after the fight (2026-10-27)

Re-ranking heroes by audit mix distance after the 2026-10-26 evening merges (4 draws, AUDIT_SEED 0-3, on main after
#141): Mirage 0.066, Viscous 0.055 (n 29), Celeste 0.052, Apollo 0.050, Ivy 0.047 (all heroes 0.024). Mirage had
drifted from ~0.03: bisecting main (Mirage-only audits, 4 draws per commit) put most of it on #138, whose
level-keeping pass cut Djinn's Mark's length_corr 6.56 -> 5.81 (Djinn's Mark share 0.263 -> 0.236, real 0.291) and
pushed his items' share up. Skipping its recast wait alone moved it 0.005; the fitted correction was absorbing a
mechanism gap.

`scripts/mechanics/djinn_pops.py real` (260 Phantom+ replays, 923 Mirage pair fights) vs `sim` (the audit's duels of
the sample's Mirage players, weighted as booked):

| | pops / 10 s of fight | expiry pops | marks popped 1 / 2 / 3 / 4+ |
|---|---|---|---|
| real | 0.72 | 64% | 58 / 23 / 17 / 2% |
| sim before | 0.43 | 34% | 58 / 28 / 9 / 6% |
| sim, marks outlast a disengage | 0.78 | 53% | 54 / 30 / 10 / 6% |

Real marks mostly pop on expiry after the shooting stops. The sim booked each pop by P(the real fight still goes on)
at the pop, so marks still on a target when a fight ends (most real fights end in a disengage) never popped. In game
they pop on expiry anyway. mirage.MARKS_OUTLAST (on): a pop books as likely as the fight still going at the last
mark (Engine.book_at, the time length_w reads by default). A fight that ends between the mark and a cast still gets
the marks, on expiry instead.

Refit Mirage only (ability_corr_heroes.py 3 rounds, item_landing_heroes.py --hero Mirage): Djinn's Mark length_corr
5.85 -> 4.05, Ricochet 0.40 -> 0.39, Toxic Bullets 0.69 -> 0.65. Mirage, 4 draws: mix 0.065 -> 0.046, per-source
0.059 -> 0.038, Djinn's Mark 0.237 -> 0.287 (real 0.291). His item share stays high (0.21 vs 0.17): his holders-only
item rows already read 0.93-0.97, so that is the per-hero table's mid-game item bias. Split-half (fit on one half,
audit the other, 4 draws; a refit on the old model as the reference): held-out half 1 per-source 0.053 -> 0.061, mix
0.047 -> 0.047; half 0 per-source 0.065 -> 0.056, mix 0.083 -> 0.069. Halves are 22 players each and their real
Djinn's Mark share differs (0.278 / 0.298), so the replays above carry the case. All-hero audit flat (0.0232 ->
0.0232, seed 0). sim_vs_win 27k, Mirage (the only hero touched): all pairs 0.233 -> 0.232, damage items -0.158 ->
-0.127, clear edges Spearman 0.18 -> 0.27.

## Melee Charge and Crushing Fists heavies (2026-10-27)

Apollo and Celeste tied as the heroes furthest from real (mix 0.051, 4 draws). Apollo's gap was mostly Melee Charge:
holders-only real/sim 4.4 (pooled 1.58, Crushing Fists 1.74, Drifter 3.6 / 5.4). Three causes, from the fight-length
replays (`scripts/mechanics/melee_heavy.py`, 260 Phantom+ replays):

- Real holders' basic melee hits are about half heavies that proc the item (a proc is 0.25x the melee hit on the same
  tick, every one): Apollo 0.67, Abrams 0.54, Venator 0.67, Yamato 0.46, Billy 0.20, pooled 0.475. The sim's
  rotation was 30% heavy for everyone. Mechanics.heavy_holders (on): a holder's rotation takes the hero's share
  (data/melee_heavy.json, shrunk to pooled with 100 hits) at a melee rate cut so melee damage per second stays the
  fitted one (fight.heavy_holder_skill); only the item's procs move.
- Below MELEE_MIN_RATE a melee tick is weighted (Apollo 0.64, Drifter 0.47): the proc already comes in the weight's
  share of ticks, but the bonus was also of the weighted hit, so the item scaled with w^2. The bonus is now of a
  whole heavy (Lifestrike's % heal the same).
- Apollo's Riposte follow-up was an ability light melee that never procced the item (and was cut by reach
  availability, though it follows a dash). The game books it as basic melee: a peak of melee hits 0.75-2.25 s after
  real Riposte casts, about 39% of his melee hits (sim 36%), 46% of holders' follow-ups proc Melee Charge. It is now
  a basic melee (Engine.melee_hit, heavy at the rotation's share). Drifter's Rend, Viscous' Puddle Punch and Billy's
  Bashdown proc the item in replays like a heavy (307 of 438, 99 of 124, 201 of 281 procs on their tick):
  items_fx.HEAVY_MELEE_ABILITIES.

Apollo's melee rate refit to the audit (melee_audit_fit.py, 0.128 -> 0.078: the follow-ups now land in full). Full
audit: Melee Charge 1.58 -> 1.12, Crushing Fists 1.74 -> 1.15; holders Apollo MC 4.1 -> 1.4, Drifter MC 3.6 -> 1.1,
CF 5.4 -> 1.4, Billy 1.8 -> 1.0, Abrams 1.19 -> 1.07; Apollo mix 0.043 -> 0.038, Drifter 0.030 -> 0.023, weighted
0.0232 -> 0.0230. The pooled factors (2.25 / 3.05) are above 1 and so unused (accuracy.item_landing caps at 1): no
item refit. Apollo's ability corrections (ability_corr_heroes.py --split): mix lower on both halves (0.035 -> 0.027,
0.048 -> 0.039) but per-source worse on one (0.031 -> 0.033), so kept as they were. sim_vs_win 27k all heroes: all
pairs 0.178 -> 0.181, damage items 0.069 -> 0.078, clear edges Spearman 0.279 -> 0.287.

Left: Apollo's items read ~1.2x under per holder (Tankbuster, Torment Pulse, Mystic Burst 1.5); real Mystic Burst
procs off Spirit Snatch's spirit hit, which the sim books procs=False. Celeste's gun is right per shot
(shot_damage.py 1.03, 8 players) and her items per gun ~1.0; all four abilities read ~1.2x under per gun.

## An allied Nurse's Wretched Vapors (2026-10-27)

Re-ranking heroes by damage mix after #142/#143 (4 audit draws) put Ivy first among heroes with a steady gap (0.046;
Viscous 29 players and Celeste noise). Her item holders' gaps (Alchemical Fire, Decay, Cold Front ~0.65x real) rest
on 9-16 players, and replay item casts show her use per fight and damage per cast in line with other heroes. Her
largest single source gap was "other": `ability_nurse_adrenaline_rush`, real 1.0% of her damage, sim 0.03%.

The game credits Wretched Vapors' crash to whoever hit the vapored hero, and real Nurses mostly vapor their allies
(`nurse.SELF_CAST` 0.2). In the validation sample, crash credit is 1.50% of the damage of every player whose enemy team
has a Nurse and exactly 0 for the rest; the audit's duels booked 0.08% (only her self-cast, when the foe is her).

`Mechanics.ally_vapors` (a share, b share): a duel fighter with a Nurse teammate (not Nurse herself) gets
`nurse.AllyVapors`: `ALLY_VAPORS` of each incoming hit is deferred, then crashes `CRASH_DELAY` 2 s later at
+DeferredDamageBonusPercent (30%), credited to the attacker as the crash (no procs). The damage audit sets it from the
real teams (`AUDIT_ALLY_VAPORS=0` turns it off); everywhere else it is (0, 0), so the build search, survival and
sim_vs_win are unchanged. `scripts/nurse/fit_ally_vapors.py` fits the share: 0.018 gives 1.48% (real 1.50%).

Damage audit, 4 draws (AUDIT_SEED 0-3), mix distance weighted by players 0.0243 -> 0.0209 (unweighted 0.0262 ->
0.0229), 41 heroes better, 2 worse (Solomon 0.013 -> 0.015). Ivy 0.046 -> 0.042, Apollo 0.050 -> 0.045, Violet
0.034 -> 0.028, Calico 0.036 -> 0.031. Sim "other" share 0.006 -> 0.013 (real 0.018; the rest is Shiv's deferred
damage, 0.009 real vs 0.006, and zip lines). One scalar fitted on the whole sample: the real share is the same in
both match-id halves (even 1.46%, odd 1.54%). No landing refit: the crash takes the same share from every other source.

## Area abilities hit more heroes later in the match (2026-10-27)

Re-ranking heroes after #145 (4 audit draws): Viscous (29 players), Celeste, Apollo, Mirage and Ivy lead but swing
0.03-0.06 between draws or were checked already; Nurse Harrow (347 players) sat at a steady 0.034, gun under (real
0.29, sim 0.26), Lurking Terrors over (0.300 / 0.328). Split by game phase (real damage between 25-35 / 55-65 /
85-95% of the match vs the audit's 30 / 60 / 90% duels), her ult share is real 0.15 / 0.36 / 0.45, sim 0.28 / 0.35 /
0.35. The same early-over / late-under shape shows for Sinclair, Violet, Pocket, Seven, Dynamo, Warden and Solomon.

Real ult casts per fight (once the ult has been cast in the match) do not change with the phase (~0.2-0.3 by 20 s
for Nurse in every third of the match), but the heroes an area ability hits do: replay DamageEvents give Lurking
Terrors 2.3 heroes per hitting cast before 45% of the match, 2.8 to 75%, 3.1 after. An ability's landing factor
absorbs the pooled count; area items already had a phase curve (area_hits.py), abilities had none.

`scripts/team/ability_area_phase.py` (fight_length replays, 260 matches): fights as area_hits.py (one attacker's run
of hero damage, gaps < 8 s, main target = most gun damage); per hero ability and the attacker's own net worth bin,
rel = (1 + other / main) / (1 + the gun's other / main) (the gun switches targets more late too: 0.21 in lane, 0.40
late, and its calibration already counts every hero); shrunk to the pooled rel (60 fights), non-decreasing.
`Mechanics.ability_area_phase` multiplies the ability's damage at the duel's souls by rel(souls) / pooled rel
(`mechanics.ability_area_mult`, data/ability_area_phase.json), so the pooled level stays and only the shape moves;
the damage audit's `AUDIT_AREA_PHASE=0` turns it off.

Split-half (corrections refit 2 rounds on one match-id half with the term off and on, judged on the other half by
the source distance at each of the 30 / 60 / 90% points, mix not worse by more than 0.002): better on both halves for
Baba, Bebop, Dynamo, Grey Talon, Kelvin, Mina, Mo & Krill, Nurse Harrow, Paige, Paradox, Pocket, Rat King, Violet,
Viscous (Nurse 0.119 -> 0.111 / 0.119 -> 0.109, Rat King 0.068 -> 0.062 / 0.070 -> 0.052, Paige 0.141 -> 0.127 /
0.126 -> 0.114); clearly worse for Haze, Infernus and Deadman Danny (their sim ability share already follows the real
one by phase, so something else in their model leans the other way). Only the 14 kept heroes get rows
(`ability_area_phase.HEROES`; `--all` writes every hero to judge more). Their ability corrections refit 3 rounds on
the whole sample (ability_corr_heroes.py).

Damage audit, 4 draws, mix distance weighted by players 0.0209 -> 0.0200; Nurse 0.034 -> 0.012, Kelvin 0.020 ->
0.014, Baba 0.017 -> 0.013, Grey Talon 0.026 -> 0.023; Viscous 0.051 -> 0.056, Mo & Krill 0.014 -> 0.019, Bebop
0.018 -> 0.022, Paige 0.013 -> 0.016 (kept: their held-out per-phase distance fell on both halves, the pooled mix
rose within the 0.002 slack there). The curve is a static snapshot like area_hits.json (fight_length replays in the
project folder): rerun ability_area_phase.py --write and refit the 14 heroes' corrections after a big patch.
Most of Nurse's pooled gain is the refit itself (her corrections were stale:
held-out mix 0.009 / 0.014 with the term off and refit, 0.010 / 0.015 on); the term moves her damage between phases.
sim_vs_win 27k all heroes: all pairs 0.181 -> 0.183, damage items 0.078 -> 0.080, clear edges Spearman 0.287 -> 0.291.

## Apollo's ult on real readiness (2026-10-27)

Re-ranking heroes after #147 / #150 / #153 (4 audit draws, weighted mix 0.0203): Viscous 0.054 (29 players),
Celeste 0.049, Apollo 0.045, Ivy 0.044, Mirage 0.042, Calico 0.041. Viscous, Celeste and Ivy were judged noise before;
Apollo's gap is steady in its mean shares: abilities 0.579 vs real 0.534, Itani Lo Sahn 0.120 vs 0.100.

Cause: Itani Lo Sahn has no cast_timing hold (its own gate: target at or below 60% health), so every duel started
with it ready. Apollo cast it in 92% of his audit duels by 20 s, real Phantom+ Apollos in 38% of pair fights
(cast_timing_real.json; 1 / 3 / 6 / 20 s: real 0.01 / 0.04 / 0.10 / 0.38, sim 0.01 / 0.09 / 0.35 / 0.92). The
replays' readiness rows (cdr_ready.py) say why: real Apollos start only 53% of fights with the ult off cooldown
(time since the last cast >= its cooldown). Per cast the sim then dealt 0.80x the real damage (446 vs 556 per real
cast, fight_length replays + real_casts, 276 casts of 43 Apollos), its landing correction having absorbed the
extra casts.

`Mechanics.gate_ready` (on): an ability in `mechanics.GATE_READY` (only Apollo's ult) starts a fight on cooldown
past its real ready share (data/cdr_ready.json at 1 x cooldown, raised by cooldown items as cdr_ready). The cast curve
becomes 0.01 / 0.05 / 0.20 / 0.52. Itani Lo Sahn's delayed hit is booked at the slash's fight weight
(`fencer.FROZEN_BOOKED`, Engine.book_at): the target is frozen, the fight can't end before the hit. Itani's length
correction refit to the audit (6 draws): 1.625 -> 1.93, per cast now 537 (0.97x real), 0.49 casts per duel (was 0.86).

Lowering the gate to 40% health matches the real cast curve exactly (0.00 / 0.03 / 0.09 / 0.41) but Apollo's
sim_vs_win fell 0.367 -> 0.350 with it, so the gate stays at 60%.

Results: Apollo mix 0.045 -> 0.038 (4 draws; 0.034 over 6), per-source 0.040 -> 0.029; weighted audit 0.0203 ->
0.0202. Split-half (correction fitted on one match-id half, 10 draws on the other): mix 0.046 -> 0.037 and 0.040 ->
0.035 vs main; per-source 0.041 -> 0.035 on one half, 0.042 -> 0.048 on the other (the ult's share at ~50 casts per
half swings). A plain correction refit on main (1.625 -> 1.33) scores about the same on the audit (mix 0.032) and
sim_vs_win (0.370), but by making each of the extra casts smaller (0.65x real per cast). Apollo sim_vs_win 27k:
all items 0.367 -> 0.375, within slot and tier 0.385 -> 0.390, clear edges 0.569 -> 0.578, damage items 0.238 ->
0.236. Other gated ults cast too often (Seven's Storm Cloud 0.90 vs 0.57, Venator 0.84 vs 0.34, Yamato 0.99 vs 0.47,
Grey Talon 1.00 vs 0.47, Mo & Krill 1.00 vs 0.49 by 20 s, cast_timing.md) are candidates for GATE_READY, each with
its own correction refit.

## More gated ults on real readiness (2026-10-27)

Follow-up of "Apollo's ult on real readiness": five more ults the sim gates itself (no cast_timing hold) started
every duel ready. First cast by 1 / 3 / 6 / 20 s, real Phantom+ pair fights vs audit duels on main:

| ult | real | sim (always ready) | sim (gate_ready) | real fights started ready |
|---|---|---|---|---|
| Seven: Storm Cloud | 0.06 / 0.11 / 0.17 / 0.41 | 0.85 / 0.85 / 0.85 / 0.91 | 0.38 / 0.38 / 0.38 / 0.41 | 0.48 |
| Venator: Ira Domini | 0.03 / 0.07 / 0.14 / 0.33 | 0.06 / 0.31 / 0.61 / 0.98 | 0.02 / 0.14 / 0.27 / 0.42 | 0.43 |
| Yamato: Shadow Transformation | 0.03 / 0.10 / 0.19 / 0.45 | 0.00 / 0.10 / 0.24 / 1.00 | 0.00 / 0.05 / 0.10 / 0.50 | 0.50 |
| Grey Talon: Guided Owl | 0.02 / 0.04 / 0.09 / 0.29 | 0.87 / 0.88 / 0.99 / 1.00 | 0.32 / 0.32 / 0.39 / 0.39 | 0.39 |
| Mo & Krill: Combo | 0.07 / 0.13 / 0.20 / 0.42 | 0.00 / 0.94 / 1.00 / 1.00 | 0.00 / 0.45 / 0.47 / 0.47 | 0.42 |

Their length corrections had absorbed the extra casts (Storm Cloud 0.31, Guided Owl 0.45, Combo 0.49); with the gate
an ult-only refit brings them to 1.01 / 1.24 / 1.34. Each hero was judged by split-half: every ability correction of
the five fitted on one match-id half (4 rounds of 4 audit draws), 6 draws on the other half, against the same
refit with the gate off (main's own factors were fitted on both halves, so they are not a fair baseline):

| hero | mix gate / plain refit (half 1, half 0) | per source (half 1, half 0) |
|---|---|---|
| Seven | 0.032 / 0.021, 0.029 / 0.025 | 0.057 / 0.052, 0.046 / 0.045 |
| Venator | 0.066 / 0.014, 0.061 / 0.022 | 0.045 / 0.015, 0.047 / 0.017 |
| Yamato | 0.038 / 0.040, 0.040 / 0.048 | 0.038 / 0.039, 0.034 / 0.041 |
| Grey Talon | 0.020 / 0.025, 0.019 / 0.031 | 0.021 / 0.019, 0.020 / 0.025 |
| Mo & Krill | 0.045 / 0.014, 0.021 / 0.035 | 0.041 / 0.032, 0.032 / 0.043 |

sim_vs_win 27k for the five heroes (Pearson, all items): main 0.174, all five gated + refit 0.254, all five refit
with the gate off 0.158; per hero (main -> gated): Seven 0.107 -> 0.246, Yamato 0.200 -> 0.235, Grey Talon 0.288 ->
0.284, Mo & Krill 0.303 -> 0.304, Venator 0.205 -> 0.201.

Kept: Yamato only (better on both held-out halves). Venator's stakes count as gun damage, so gating the ult takes
~18% of his gun damage away (gun share 0.49 -> 0.40 vs real 0.48) and only a gun refit could fix it. Seven gains the
most on sim_vs_win but his held-out mix is worse on both halves; Grey Talon's per-source distance is worse on one
half, Mo & Krill's mix on one; their sim_vs_win is flat. They stay always ready.

Yamato with the gate (mechanics.GATE_READY), his three ability corrections refit on the whole sample (4 rounds of 6
draws): Power Slash 2.292 -> 2.611, Flying Slash 0.869 -> 0.917, Crimson Slash 1.412 -> 1.468. Yamato audit (8 draws)
mix 0.0236 -> 0.0224, per source 0.0197 -> 0.0197; sim_vs_win of the five heroes 0.174 -> 0.183, within slot and tier
0.232 -> 0.237, clear edges 0.294 -> 0.307; Yamato 0.200 -> 0.252.

## Venator's stakes and ult readiness (2026-10-27)

Follow-up of "More gated ults on real readiness", where gating Ira Domini dropped Venator's gun share 0.49 -> 0.40.
The game books the ult's stakes under their own weapon, `citadel_weapon_priest_crossbow(_crit)`, not his gun
(`citadel_weapon_priest_set`), and the damage matrix shows them apart: Phantom+ Venator damage is plain gun 0.378,
stakes 0.101, Ira Domini (blessed + execute) 0.117. The sim booked stakes as "gun" with no landing factor, at 0.27-0.33
of his damage, while his plain gun sat at 0.16. Both added up to the real 0.48 "gun" share, and his ability
corrections had been fitted on top of that (Consecrating Grenade 1.62, Gutshot 1.57, Snap Trap 2.37, melee rate
0.114). Plain gun damage per shot is right: scripts/gun_calib/shot_damage.py read Venator 3.31x real per shot with
the stakes in, 1.05x (0.97-1.13) without them. Replays (analysis/work/replay_damage, 100 Venators): 1.63 stake hits on
heroes per cast (of 3) for 1.42 blessed hits, 258 / 296 damage each.

Now: stakes are "Ira Domini (stakes)" (bullet damage that procs like the gun, priest.STAKES_AS_ULT) with their own
landing row (class citadel_weapon_priest_crossbow, landing_rates.ALIASES); the audit maps the real crossbow to it
(landing_rates.real_key), so stakes count as ability damage on both sides; melee_items_fit.py leaves them out of real
gun. Ira Domini joins mechanics.GATE_READY. Venator's corrections and melee rate refit to the audit (3 rounds of 4
draws): Grenade 0.866, Gutshot 1.015, Snap Trap 1.206, Ira Domini 1.908, stakes 0.918 (x landing 0.65), melee rate
0.051.

Split-half, judged with stakes as a source of their own on both sides (main's own audit hides them inside gun), each
variant fitted on one match-id half, 3 draws on the other:

| variant | per source (half 1, half 0) | mix (half 1, half 0) |
|---|---|---|
| main (stakes as gun), refit | 0.128, 0.129 | 0.242, 0.236 |
| stakes under the ult, gate off, refit | 0.022, 0.026 | 0.029, 0.023 |
| stakes under the ult, gate on, refit | 0.020, 0.015 | 0.026, 0.019 |

Whole sample, 4 draws: per source 0.007, mix 0.014 (gun 0.376 vs real 0.379). Full audit flat 0.0186 -> 0.0187 (one
draw; other heroes move by their Venator foes). sim_vs_win 27k, Venator only: all items 0.210 -> 0.225, damage items
0.187 -> 0.240, within slot and tier 0.234 -> 0.255.

## Melee by game phase (2026-10-27)

Re-rank on main after #150-#159 (4 draws, all heroes 0.0202): Viscous 0.054 (n 29), Celeste 0.049, Ivy 0.044 (all
three judged noise before), Mirage 0.041, Calico 0.040 (n 110, steady), Warden 0.038 (n 33), Apollo 0.037. Calico's
whole-match mix had melee under (0.123 vs real 0.149) and items over (0.348 vs 0.312). Phase by phase (real damage in
the frac +- 15% window of the sample's damage_series, sim duels at that frac only) her items match real at every
phase (0.26 / 0.30 / 0.40 both), so "items over" was the late duels' weight; melee was 0.188 / 0.146 / 0.108 real vs
0.148 / 0.131 / 0.108 sim. Per hit sizes match the formula at every phase (replays, melee_scaling.py k = 0.5), so it is
the rate. The same holds for nearly every hero: real melee share over sim, players weighted, 1.20 / 0.91 / 0.74 at
30 / 60 / 90% of the match (ranged heroes drop most: Ivy 1.47 / 0.72 / 0.51, Nurse 1.10 / 0.59 / 0.44; melee heroes
flat: Abrams 0.92 / 1.01 / 1.05). Real players melee in the lane and stop later; the fitted rate is one number.

Mechanics.melee_phase: the melee rate x melee_phase_mult(hero, net worth) (data/melee_phase.json,
scripts/mechanics/melee_phase.py, 3 rounds): real over sim melee share at each frac, shrunk in ln to the pooled curve
(heroes weighted by real melee damage, 30 players), at the hero's median net worth there, linear in ln net worth
between, flat outside. Pooled 1.16 / 0.97 / 0.87; Calico 1.39 / 1.18 / 0.98.

Split-half (fit on one match-id half, audit the other, 4 draws whole match / 2 draws per phase):

| half | whole-match mix | phase mix 30 / 60 / 90% | phase melee gap 30 / 60 / 90% |
|---|---|---|---|
| odd, base | 0.0233 | 0.0406 / 0.0328 / 0.0434 | 0.0116 / 0.0055 / 0.0103 |
| odd, fit on even | 0.0240 | 0.0370 / 0.0317 / 0.0409 | 0.0058 / 0.0032 / 0.0054 |
| even, base | 0.0219 | 0.0384 / 0.0339 / 0.0405 | 0.0112 / 0.0065 / 0.0089 |
| even, fit on odd | 0.0229 | 0.0359 / 0.0332 / 0.0386 | 0.0073 / 0.0046 / 0.0047 |

Phase by phase every number is better on both halves; the whole-match mix is a little worse because it compares the
whole real match (lane-heavy melee included) with three duels whose damage grows with the phase, so the flat rate
fitted to it was its own optimum. Kept on the phase-matched view (as for ability_area_phase) and sim_vs_win 27k, all
heroes: all items 0.242 -> 0.245, damage items 0.146 -> 0.154, within slot and tier 0.282 -> 0.286, per item 0.341 ->
0.343. Whole sample, 4 draws: all heroes 0.0202 -> 0.0206; Calico 0.040 -> 0.036 (melee 0.123 -> 0.132), Apollo
0.037 -> 0.034, Dynamo 0.017 -> 0.013, Nurse 0.013 -> 0.017 (whole-match melee 0.031 -> 0.021 vs real 0.032).

## Ult casts by game phase (2026-10-27)

Follow-up of melee by game phase: the same phase-matched audit for every kind of damage (scripts/phase_mix.py: real
damage in the frac +- 5% window of the sample's damage_series vs audit duels at that frac only, 2 draws, players
weighted). Real / sim share at 30 / 60 / 90% of the match before:

| kind | 30% | 60% | 90% |
|---|---|---|---|
| gun | 0.270 / 0.275 | 0.230 / 0.248 | 0.202 / 0.224 |
| melee | 0.068 / 0.068 | 0.050 / 0.050 | 0.042 / 0.042 |
| ult | 0.100 / 0.106 | 0.110 / 0.108 | 0.125 / 0.107 |
| other abilities | 0.465 / 0.467 | 0.445 / 0.442 | 0.402 / 0.406 |
| items (all) | 0.080 / 0.074 | 0.146 / 0.140 | 0.209 / 0.207 |

Items and plain abilities follow real by phase. The ult is over early and under late; the gun over late. Big-burst ults
were the early ones (Violet 0.11 real vs 0.19 sim at 30%, Solomon 0.12 / 0.19, Seven, Sinclair, McGinnis, Pocket).

Cause of the early part: the ult holds (data/cast_timing.json) are one curve over the whole match, but real players
cast the ult in fewer fights early. From the fight-length replays' pair fights (scripts/cast_timing/ult_phase.py), the
Kaplan-Meier P(ult cast by 20 s) over the hero's whole-match one is 0.88 before 45% of the match, 1.06 to 75%, 1.02
after (Solomon 0.53 / 1.50 / 0.78, Infernus 0.76 / 1.15 / 1.07). A fight counts once the ult is unlocked: cast before
in the match, or the fourth ability unlock reached at that net worth (with "cast before" alone the fights between the
unlock and the first cast are left out and the early bin came out 1.11).

Mechanics.ult_phase: the ult hold's cast share c becomes min(0.98, c x ult_phase_mult(net worth)) (data/ult_phase.json,
per hero shrunk in ln to the pooled ratio with 3000 fights, linear in ln net worth between the bins' median net worths);
the cast holds keep their order and stretch over the new share. 28 heroes with an ult hold; gated ults keep their own
timing. Split-half on the replays (fit on one match-id half, weighted squared ln error on the other half's per-bin
ratios): off 1693 / 1952, fit 1560 / 1703 (shrink 300: 1775 / 1851, pooled only: 1571 / 1724).

Results: ult share at 30% 0.106 -> 0.100 (real 0.100), phase mix distance 0.0543 / 0.0468 / 0.0672 -> 0.0534 /
0.0460 / 0.0657; whole-match mix flat (3 draws 0.0208 / 0.0208); sim_vs_win 27k all 0.245 -> 0.246, clear of noise
0.350 -> 0.352, within slot and tier 0.287 flat. No levels refit.

Left: the late ult gap (real 0.125 vs 0.109 at 90%) is mostly Nurse (0.45 vs 0.32) and Violet (0.23 vs 0.18), both
already on ability_area_phase; real ult casts per fight are flat from 60% to 90%, so it is damage per cast. The gun's
late over (0.91x) is spread (Paige 0.135 real vs 0.262 sim at 90%, Nurse, Violet, Shiv, Lash, Abrams). Permanent
pickups (sample power_ups: by 90% +97 HP, +9.6% weapon power, +4.8% fire rate, +7 spirit) are not modelled; small and
on both sides.

## Gun damage late in the match (2026-10-27)

Follow-up of ult casts by game phase: the phase-matched audit (scripts/phase_mix.py) had the gun 0.97x / 0.93x / 0.91x
real at 30 / 60 / 90% of the match, spread over many heroes. scripts/gun_calib/gun_phase.py splits it per hero bullet
hit (real: damage_series gun damage / stats hero_bullets_hit in frac +- 0.1; sim: the audit's duels): real damage per
hit is flat from 60% to 90% for most heroes (Paige 54.2 -> 54.6, Nurse 27.1 -> 27.2, Wraith 11.2 -> 11.0) while the
sim's grows (67 -> 72, 32 -> 38, 13 -> 16); geo mean sim/real 0.82 / 0.83 / 0.93.

Replays (160 Phantom+ matches of the validation sample, scripts/gun_calib/fetch_gun_hits.py: every gun hit on a hero
with pre_damage, effectiveness, crit_damage, damage_absorbed; raw in /mnt/project-files/analysis/work/gun_phase) split
the per hit gap (gun_phase.py --replays): falloff (0.88 / 0.91 / 0.87 real, 0.90 sim) and crit share (0.14 / 0.13 /
0.13 vs 0.14 / 0.15 / 0.15) match; damage / pre_damage does not (0.94 / 0.89 / 0.83 real, 1.00 / 1.00 / 0.97 sim).
Two parts:

- Barriers: the game's damage numbers (DamageEvent damage = the API damage matrix, checked per player) leave out what a
  barrier soaks. Real: 5% / 9% / 9% of gun damage, 5% / 9% / 10% of other damage (grouped demo query, 30 matches). The
  sim books barrier damage as dealt (gun 6% / 11% / 12%, all 6% / 9% / 10%). Mechanics.unbook_absorbed drops it from
  dmg_out / dmg_exp (the duel is unchanged). Kept OFF: late gun share only 0.223 -> 0.221, and the whole-match audit
  goes 0.0207 -> 0.0215 (items rise; item_landing was fitted with barrier damage booked).
- Bullet resist: per hit (damage + absorbed) / pre_damage over 1 - the target's build resist after the shooter's build
  shred (compute_stats at the hit's time; scripts/gun_calib/resist_check.py) is 0.99 / 0.99 / 0.98 real (match-id
  halves 0.993 / 0.996 / 0.983 and 0.991 / 0.988 / 0.973), the audit's duels 1.01 / 1.04 / 1.05: a duel keeps every
  shred debuff (shred items, Hunter's Aura at its single-target x2, hero abilities: Rat King's bites, Silver, Wraith,
  Yamato, Haze) on its one target. Late, items add +0.057 and abilities +0.024 over no in-fight shred (0.967).
  Per shooting hero (late, real vs sim at 60 / 90%), fitting separate item and ability factors gave 0.40 / 0.40 on one
  half and 0.30 / 0.25 on the other (one factor 0.40 / 0.30); held-out per hero rmse 0.082 -> 0.055 and 0.074 -> 0.048
  (no shred at all 0.059 / 0.061). Mechanics.shred_uptime = 0.35 multiplies the in-fight bullet_shred debuffs (build
  shred unchanged). Holders of a shred item read +10-14% in real (Hunter's Aura 1.114 vs 0.978 without) against
  +13-18% in the sim with every debuff in full; per holder comparisons mix in who builds them, so the per hero fit
  decides.

Results (shred_uptime 0.35, unbook off): phase_mix gun 0.276 / 0.243 / 0.219 (real 0.270 / 0.230 / 0.202; before
0.278 / 0.247 / 0.223), mix distance 0.0534 / 0.0460 / 0.0657 -> 0.0529 / 0.0453 / 0.0642; whole-match audit (2
draws) 0.0207 -> 0.0209 (heroes with their own gun shred lose gun share: Drifter, Silver, Bebop, Paradox, Yamato).
sim_vs_win 27k flat: all 0.246 -> 0.245, within slot and tier 0.286 -> 0.287, clear of noise 0.352 -> 0.354, damage
items 0.154 -> 0.155 (no tier_caps locally, both runs the same).

Left: the late gun over (0.219 vs 0.202) is now mostly spirit builds that shoot less late in real games (Paige 0.254 vs
0.135, Nurse, Celeste, Dynamo, Doorman, Viscous, Rem, Kelvin: their real gun share drops 3x from 30% to 90%), and the
late ult under (Nurse, Violet) takes share from the gun too. Per victim, real damage / pre_damage is far lower on Shiv
(0.65: Bloodletting defers), Viscous 0.80, Mo & Krill 0.84, Yamato 0.87 (the sim's Shiv defers too).

## Ability order (2026-10-27)

Re-ranking heroes by damage mix on main after #160-#163 (4 audit draws, all heroes 0.021): Viscous 0.057 (29
players), Celeste 0.048, Ivy 0.047, Mirage 0.045, Calico 0.038. Phase-matched (scripts/phase_mix.py) Ivy is in line at
every phase (her whole-match item gap is the mid-game bias of the per-hero table). Celeste is not: her ult share was
0.13 / 0.12 / 0.16 at 30 / 60 / 90% of the match against the real 0.12 / 0.17 / 0.21, her gun 0.24 / 0.18 / 0.18
against 0.20 / 0.14 / 0.13.

Not the orb's bounces: in the fight-length replays (447 Shining Wonder casts) the orb hits the cast's main target 2.0
times per cast in lane and 2.8 late, other heroes 0.63 -> 0.86 x that; the sim's hits per cast (1 + prism rebounds at
Dazzling Trick T3) grow 1.0 -> 1.4 over the same net worths, about the real shape, and the landing x length_corr carries
the level. The per-hit damage does not: sim raw 169 / 182 / 193 / 202 / 348 at 8k / 14k / 20k / 27k / 35k souls, real
(after resist) 157 / 177 / 257 / 306 / 313. A loadout without an ability order follows the hero's single most played
full order (fight.popular_ability_order), and Celeste's top row puts every point into Dazzling Trick before the ult:
Shining Wonder tier 0.42 at 60% of the match, real players (their ability events in the sample's items) 1.57.

The same shows on many heroes (mean |real - popular| tier gap over abilities x 30 / 60 / 90%: Ivy 0.84, Sinclair 0.81,
Paige 0.67, Doorman 0.63, McGinnis 0.62; all heroes 0.39; Ivy's Kudzu Connection 0.0 vs 2.1 real at 60%).
`scripts/ability_order.py` writes data/ability_order.json: each hero's ability events sorted by the median net worth
real players bought them at (a player who never did counts above every net worth), an ability's own events in order.
Tier gap with it 0.39 -> 0.26 over all heroes (Celeste 0.27 -> 0.21; her ult at 60% 0.88: one order cannot reach a mean
of 1.57).

On for `fight.ORDER_HEROES` (Celeste only so far): their loadouts without an order follow the median order
(fight.default_ability_order), and the damage audit gives their players their real tiers at the duel's moment
(damage_audit.real_tiers; AUDIT_REAL_TIERS=0 for the median order), so the fitted factors are per cast at real tiers.
Celeste's corrections refit 3 rounds (ability_corr_heroes.py: Light Eater 1.60 -> 1.88, Dazzling Trick 1.47 -> 2.29,
Radiant Daggers 0.92 -> 1.13, Shining Wonder 3.99 -> 4.03). Split-half against the same refit on main's code (fit on
one match-id half, 4 draws on the other): mix 0.0225 -> 0.0223 and 0.0275 -> 0.0232, per-source 0.0595 -> 0.0581 and
0.0516 -> 0.0523.

Results: Celeste mix (6 draws) 0.049 -> 0.019 (0.040 before the refit); phase-matched ult 0.126 / 0.157 / 0.158 (real
0.122 / 0.169 / 0.208), gun 0.203 / 0.158 / 0.170 (real 0.204 / 0.135 / 0.132); phase mix distance (all heroes) 0.0515
/ 0.0457 / 0.0606 -> 0.0514 / 0.0453 / 0.0602. sim_vs_win Celeste 27k all 0.429 -> 0.445, within slot and tier 0.430
-> 0.444; 37k 0.347 -> 0.355 / 0.348 -> 0.354.

Left: her late ult (0.158 vs 0.208 at 90%, with real tiers) and late gun; the other heroes with large tier gaps (Ivy,
Sinclair, Paige, Doorman, McGinnis) need the same split-half judgement before going on ORDER_HEROES.

### More heroes on the median order (2026-10-27)

The five heroes with the largest tier gaps, each judged on its own: the hero added to `ORDER_HEROES` with its ability
corrections refit 3 rounds on one match-id half, audited on the other (8 draws), against the same refit on main's code.
McGinnis (49 players) was then judged again the way his draws need (each fit round on the mean of seeds 0-3, held-out
test on seeds 6-9, as for #136), and Ivy and Paige too.

| hero | held-out mix, main code -> median order (half 1 / half 0) | per-source | kept |
| --- | --- | --- | --- |
| Ivy | 0.0483 -> 0.0469 / 0.0440 -> 0.0394 (seed-averaged 0.0443 -> 0.0429 / 0.0487 -> 0.0467) | better both | yes |
| Paige | 0.0353 -> 0.0262 / 0.0245 -> 0.0211 (seed-averaged 0.0325 -> 0.0228 / 0.0339 -> 0.0218) | better both | yes |
| McGinnis | 0.0826 -> 0.0820 / 0.0402 -> 0.0391, seed-averaged 0.0325 -> 0.0376 / 0.0465 -> 0.0445 | seed-averaged worse one half | no |
| Sinclair | 0.0238 -> 0.0249 / 0.0376 -> 0.0392 | better both | no |
| The Doorman | 0.0191 -> 0.0216 / 0.0187 -> 0.0233 | worse one half | no |

Sinclair's and the Doorman's corrections already absorb their popular orders (both sit near 0.01-0.02 mix), and
McGinnis's turret pacing (#136) already found his real per-player order no better. Ivy and Paige corrections refit on
the whole sample (seed-averaged, 3 rounds): Ivy Entangling Thorns 1.60 -> 1.86, Stone Form 0.78 -> 0.90, Air Drop
1.49 -> 1.68; Paige Bookwyrm 1.50 -> 2.01, Captivating Read 1.18 -> 1.29, Rallying Charge 2.16 -> 1.99. Ivy now has
Kudzu Connection at tier 2-3 by 8-14k souls (popular order: 0 until ~27k).

Results (4 draws): all heroes 0.0207 -> 0.0205, Ivy 0.047 -> 0.043, Paige 0.015 -> 0.013, others flat.
sim_vs_win (all heroes, 27k + 37k pooled): all 0.240 -> 0.241, within slot and tier 0.276 -> 0.277; Ivy 27k 0.163 ->
0.168, 37k 0.158 -> 0.163; Paige 27k 0.188 -> 0.207, 37k 0.172 -> 0.190.
## Gun time by build (2026-10-27)

After the shred fix the late gun was still over (phase_mix gun 0.276 / 0.243 / 0.219 sim vs 0.270 / 0.230 / 0.202
real at 30 / 60 / 90%), mostly on spirit heroes (Paige 0.261 vs 0.135 at 90%). scripts/gun_calib/gun_build.py puts
each player-match's real gun share in the window frac +- 0.05 beside the audit duel at that frac, with the build's
spirit item souls. Real over sim gun share (share-corrected: r(1-g) / g(1-r)) falls with the souls in spirit items,
not with the phase: 0.95 with none, 0.93 under 2k, 0.88 at 2-5k, 0.84 at 5-9k, 0.80 at 9-14k, 0.74 at 14-20k, 0.66
past 20k, and each bin is the same at 30, 60 and 90% of the match. It holds within a hero (low vs high spirit lean at
90%: Ivy 1.23 / 0.38, Bebop 1.03 / 0.58, Holliday 1.22 / 0.66, Graves 1.00 / 0.73; within-hero slope -18e-3 ln per 1k
spirit souls). The real lost share goes to abilities; items match.

Mechanics.gun_lean: the gun's fire interval and reload are / exp(-gun_lean x spirit item souls / 1000) (stretching
only the interval moved the share half as much: a longer clip means fewer reloads). Fitted by the ln-ratio slope over
spirit souls crossing 0: 0.0264 on even match ids, 0.0257 on odd; within-hero slope at 0.028: -2.7e-3 / -1.0e-3 per
1k (from -18e-3). Set 0.028.

Results (gun_lean 0.028): phase_mix gun real/sim 0.98 / 0.95 / 0.93 -> 1.00 / 1.00 / 1.04. sim_vs_win 27k: all 0.245
-> 0.263, within slot and tier 0.287 -> 0.296, clear of noise 0.354 -> 0.369, damage items 0.155 -> 0.166. The
whole-match audit (4 draws) 0.0210 -> 0.0299: it compares the whole real match, gun-heavy lane included, with duels at
30 / 60 / 90% only, and the old late over-shooting had been filling in for the missing lane (Drifter, Graves, Danny,
Grey Talon, Paradox, Yamato whole-match gun 0.02-0.03 under now, though each phase matches). Split-half ability
refit (ability_corr_heroes.py --split, all heroes) kept Seven, Dynamo, Shiv, Mina, Violet: whole-match 0.0277, phase
mix 0.0529 / 0.0453 / 0.0642 -> 0.0547 / 0.0424 / 0.0615. Left: the sim gun is ~0.95x real share even without spirit
items; melee over for spirit builds too (0.031 vs 0.023 past 0.65 spirit lean at 90%).

## Violet's Still Life draws (2026-10-27)

Re-ranking on main after #164/#166 with each hero's sampling noise (bootstrap of the real players, 200 draws): Violet
had the largest gap clear of noise (0.029 with 376 players, noise 0.005); Calico 0.041 is the known mid-game bias of the
whole-match table, Warden / Viscous (0.06) have 33 / 29 players and noise ~0.03. Violet's time-based items were under on
her only (holders: Torment Pulse 1.9x, Mystic Burst 1.6x, Tankbuster 1.4x, Mystic Shot 1.25x; ~1.0 on every other
hero) and she killed in 64% of her audit duels (median 13.8 s; Baba 10%, Celeste 24%), so those items got little time.

Same players (the 155 Violets of the 260 fight-length replays), per gun hit: Tankbuster and Mystic Shot procs 0.72 /
0.14 in the sim vs 0.95 / 0.18 real, and open PR #165 (gun time by build) moves them to 0.95 / 0.17; that part is the
spirit-build gun rate. The rest is Still Life (`scripts/mechanics/still_life_draws.py`, 4917 draws):

- a completed draw ends 2.61 s after its first tick (AbilityChannelTime 2.6) whatever Violet hit meanwhile: the BuildUp
  props do not shorten it;
- Violet lands 0.01 gun hits per second while drawing vs 0.55 when engaged, and casts nearly nothing else;
- 48% of draws complete; P(broken by t) 0.05 / 0.18 / 0.34 / 0.44 / 0.52 at 0 / 0.75 / 1.5 / 2.0 / 2.5 s.

The sim let her shoot through the draw, completed it when the meter reached 100 (seconds plus shots) and stunned in 92%
of draws. Now (deadsim/heroes/artist.py) a draw channels AbilityChannelTime with the gun locked and her other abilities
waiting, breaks at a time drawn from the real curve (SKETCH_BREAK; fights with a phase or an rng, as recast waits are
drawn), and only an unbroken draw ends in Damage + stun.

Judged on main before #165: split-half (corrections refit 3 rounds on one match-id half, 2 draws on the other, against
the same refit on main's code) mix 0.0340 -> 0.0300 and 0.0260 -> 0.0240; Violet mix (4 draws) 0.030 -> 0.027; duels
she wins outright 64% -> 59%; sim_vs_win 27k all heroes flat (all 0.249, within slot and tier 0.297).

Again after #165 merged (gun time by build): split-half with 6 draws per half, per-source 0.0209 -> 0.0198 and 0.0172
-> 0.0163, mix 0.0195 -> 0.0158 and 0.0168 -> 0.0167. Violet's corrections refit 3 rounds on top of #165 (Still Life
1.79 -> 2.66, Abstract Landscape 2.04 -> 2.23, Flow State 2.60 -> 2.46, Living Ink 1.36 -> 1.33). Violet mix (4 draws)
0.018 -> 0.014; holders' Torment Pulse 1.68 -> 1.51, Mystic Shot 1.12 -> 1.06. sim_vs_win Violet 27k + 37k: all 0.360
-> 0.380, within slot and tier 0.396 -> 0.407, clear of noise 0.432 -> 0.496 (damage items 0.507 -> 0.464).

Left: she still kills fast in duels (Living Ink's cooldown cuts are the next
suspect: in replays Still Life was recast early in 83% of chances).
## Whole-match audit cover (2026-10-27)

After the gun slowdown (above) the whole-match audit read 0.0210 -> 0.0280 while every phase matched real better. The
audit compared the whole real match (lane included) with duels at 30 / 60 / 90% pooled by sim damage, and sim damage
per duel grows much faster with the phase than real damage does (per fifth of the match, real 18 / 29 / 42 / 57 / 76
vs sim duel damage ~1 / 2 / 5 / 9 / 13): the sim side read like the late game. Duels drawn across the match by real
damage, pooled the same way, gave 0.0316 (item share 0.171 vs real 0.152, the late game again); reweighting each duel
to the real damage gave 0.0344 (gun +0.015: ability-heavy duels deal more, so equal weights favour the gun).

damage_audit.py now (AUDIT_COVER=1, main's default; importers of sim_player keep 30 / 60 / 90%): 5 duels per
player-match at the times its cumulative real damage passes (i + u) / 5 of the total, and the sim mix of each fifth of
the match (pooled by sim damage inside it) weighted by the real damage in that fifth, per hero. Per fifth the sim mix
matches real: gun 0.388 / 0.378, 0.262 / 0.261, 0.237 / 0.238, 0.222 / 0.214, 0.207 / 0.192 (real / sim).

Results (2 draws): whole-match mix 0.0280 (30 / 60 / 90%) -> 0.0202; the same audit with gun_lean 0 reads 0.0230, so
the gun slowdown is an improvement there. ability_corr_heroes.py --split (all heroes, now on the cover audit) kept
Apollo, Mirage, Lash, McGinnis, Mina, Infernus: 0.0202 -> 0.0193 (Apollo 0.040 -> 0.018, Lash 0.028 -> 0.017,
McGinnis 0.023 -> 0.011). The audit runs 5 duels instead of 3 (~2 min on 4 cores).

## Nurse's Lurking Terrors runs its channel (2026-10-27)

Re-ranked on the cover audit (#169), per-source distance with each hero split by match-id halves: Sinclair (0.094) is
noise (Audience Participation 0.18 / 0.35 on one half, 0.23 / 0.20 on the other: the copied ult varies), Lady Geist
(0.084, 37 players), Viscous and Warden (29 / 33) are small; Nurse Harrow (0.040, 347 players) had the same gaps on
both halves. By phase (phase_mix.py --window 0.05) her ult share was 0.21 / 0.34 / 0.33 in the sim vs 0.15 / 0.36 /
0.45 real at 30 / 60 / 90% of the match, Leech Therapy over late (0.37 vs 0.26).

Replays (234 Nurse matches of the fight-length replays): Terrors deals 304 / 747 / 1117 / 1321 per cast at net worth
<10k / 10-20k / 20-30k / 30k+ (2.1 to 3.1 heroes, damage spanning 3.9 to 6.6 s; T3 casts 6.4 s of the 10 s channel,
taking 2 damage meanwhile); the first cast share per fight is flat over the match for all her abilities. In the audit
duels the channel was cut short more and more as the match goes on: the channel left when the duel ended (time cap,
target dead, Nurse dead or stunned) was 15% of it at 30% of the match and 35% at 90% (T3 channel 10 s, faster kills),
on top of every tick being weighed by P(the two still trade then).

Now (deadsim/heroes/nurse.py TERRORS_COMMIT): Terrors' ticks are booked at the channel start's fight weight
(Engine.book_at: feared targets flee but keep taking the DPS), and the channel left when the duel ends lands at the
last tick's damage, in full at the time cap and x TERRORS_OTHERS (0.5: the other heroes' share of a real cast, 0.40
in lane to 0.53 late) when the target died; none when Nurse died or is stunned (Engine.run calls the abilities'
on_fight_end). Real ability tiers for Nurse (fight.ORDER_HEROES) were tried too: Leech late better, early ult worse,
dropped.

Split-half (Nurse's corrections refit 3 rounds on one half, against the same refit on the old code, judged on the
other): phase mix 0.090 / 0.042 / 0.110 -> 0.067 / 0.041 / 0.086 and 0.143 / 0.101 / 0.078 -> 0.110 / 0.096 / 0.041
at 30 / 60 / 90%; whole-match held-out mix 0.022 -> 0.024 and 0.021 -> 0.021. Refit on the whole sample (Terrors
length_corr 2.55 -> 1.84, Leech 1.48 -> 1.42): audit 0.0187 -> 0.0184, Nurse 0.016 -> 0.013 (per source 0.040 ->
0.008). A stun that broke the channel leaves nothing to land at the end. sim_vs_win Nurse 27k + 37k: all 0.286 -> 0.302, within slot and tier 0.312 -> 0.332.

Left: Nurse's early ult is still over (0.22 vs 0.15 at 30%).

## Victor's revive (2026-10-27)

After the cover audit (#169) Victor's ult share was under at every phase and more so late, on both match-id halves
(phase_mix.py --window 0.05, real / sim: 1.45 / 1.78 / 2.12 at 30 / 60 / 90%; even 1.59 / 1.61 / 2.25, odd 1.30 /
1.97 / 2.01). In the replays (59 Victor matches) half his ult damage is the T1 bonus per bullet while it is on
cooldown, and real Victors shoot ~50% of their mid / late bullets with it on. Per bullet hit the sim's bonus matches
(its T1 damage per on-cooldown gun damage ~0.47 raw); the duels just started on cooldown too rarely.

scripts/mechanics/victor_revive.py (data/victor_revive.json, read by heroes/frank.py CARRY_COOLDOWN) had three faults:
- casts: it kept cooldown starts at the replay's one most common tick offset, so every cast after a game pause was
  dropped (273 of 342 revives kept; 25% of his T1 hits came >240 s after the last kept cast, impossible). Now
  fit_cast_timing.real_casts (per stretch of the replay): 96% of T1 hits fall inside a cooldown.
- phases: split by minutes (9 / 25), the sim reads net worth (10k / 27k); now his net worth at the fight start.
- fights: his aura's self-damage ticks out of combat counted as fights (~40% of the mid ones); now left out. And the
  rest of a fight he revives in counts as a fight of its own started on cooldown (3 s after the cast): real fights
  with a revive in them last ~25 s vs 6-9 s and go on a mean 9-11 s after it with half the fight's bullets, but a sim
  duel's blast mostly finishes its one foe, so nothing of that part was in the sim.
On cooldown at a fight's start (T3 145 s / T1 240 s): lane 0.11 / 0.11 -> 0.13 / 0.18, mid 0.30 / 0.54 -> 0.44 /
0.67, late 0.29 / 0.47 -> 0.51 / 0.72.

Split-half (data from one half's replays and Victor's corrections refit 3 rounds on that half of the sample, against
the same refit on the old data, judged on the other half): whole-match held-out mix 0.0220 -> 0.0210 and 0.0200 ->
0.0180, per source 0.0399 -> 0.0392 and 0.0272 -> 0.0256; phase mix 0.0545 / 0.0433 / 0.0495 -> 0.0469 / 0.0430 /
0.0458 and 0.0385 / 0.0227 / 0.0426 -> 0.0344 / 0.0281 / 0.0411 at 30 / 60 / 90%.

Kept without a refit (corrections as they were): ult by phase 1.45 / 1.78 / 2.12 -> 1.34 / 1.42 / 1.63 real / sim,
phase mix 0.0298 / 0.0414 / 0.0467 -> 0.0253 / 0.0325 / 0.0433, Victor whole-match mix 0.021 -> 0.020 (ult share
0.030 -> 0.036, real 0.058), audit 0.0184 -> 0.0185. sim_vs_win Victor 27k + 37k: all 0.238 -> 0.257, within slot
and tier 0.264 -> 0.276, damage items 0.145 -> 0.162, edges clear of noise 0.496 -> 0.523. A Victor refit on top
(3 / 5 rounds) runs Shocking Reanimation's length_corr from 3.49 to 8.9 / 10.0 (the KEEP_RANGE cap; landing 2.94),
puts the ult at 0.64 / 1.01 / 1.04 (over at 30%: natural lane revives x that correction) and lowers sim_vs_win
(within 0.257 / 0.251), so the levels stay.

Tried, not kept: a drawn third-party revive. Real Victors who start a fight with the ult ready revive in it in 3%
of lane fights, 21% mid and 27% late, a median ~14 s in (victor_revive.py prints it, json "in_fight"), mostly to
the fight's other enemies; a sim duel's lone foe gets him there in ~5%, late in the duel where the length weights
count the blast at ~0.1, which is why the blast's correction runs to the cap. Drawing those revives (blast booked
at the fight start's weight) brought the correction to 0.5-1.2, but the halves disagreed (held-out per source
0.0399 -> 0.0244 on one, 0.0272 -> 0.0397 on the other; 60% phase mix 0.0227 -> 0.0617): a few big blasts per
half sample. Left: the ult is still under (1.34 / 1.42 / 1.63); those third-party revives are the cause, and need a
version with less variance (an expected-value blast per fight) before a refit can follow.

## Soul Exchange swaps whole (2026-10-28)

Lady Geist was the next hero gap on the whole-match audit: Soul Exchange at 0.073 of her damage vs 0.139 real
(1.70x under), Essence Bomb and Malice over (0.235 / 0.190 vs 0.190 / 0.144), and under at every phase (ult real /
sim 3.05 / 1.96 / 1.71 at 30 / 60 / 90%, scripts/phase_mix.py). The audit sample has only 37 Geist players, so
validation/geist_sample.jsonl.gz adds 443 more Phantom+ matches with a Geist (match ids from aim_sample.jsonl.gz,
none in phantom_sample; fetch_validation.get + slim): ~240 more Geist players. Soul Exchange there: 0.137 real vs
0.074 sim, the same gap.

Cause (scripts/mechanics/swap_real.py on the 260 replays, 33 Geists, 144 casts): a real swap takes 0.52 of the
target's max health (median; target at 0.88, Geist at 0.25), 93% of casts hit a hero. The sim swap went through
Soul Exchange's fitted landing factor x length_corr (1.42 x 0.41 = 0.58, a level kept through #113's timing change
from fits on 37 players), so its target lost ~0.20 per swap. The swap is a health swap, not a hit that lands part
of the time: Mechanics.swap_full (on) books it whole on ghost.SWAP_LAND = 0.93 of casts (Accum draw), without the
factor; ability_corr_heroes.py leaves its row alone (UNSCALED).

Swap alone (no refit): Soul Exchange 0.088 -> 0.135 (2 seeds), right on both match-id halves of both samples
(phantom 0.116 / 0.151 vs real 0.121 / 0.155; Geist sample 0.116 / 0.111 vs 0.135 / 0.139); held-out per-source
distance 0.076 / 0.084 -> 0.050 / 0.048 and 0.108 / 0.097 -> 0.082 / 0.071, but the class mix worse (Essence Bomb,
Malice, Life Drain corrections had been fitted around the short swap: ability share too high, gun 0.26 vs 0.29).

Geist's other corrections refit (ability_corr_heroes fit, 3 rounds) on phantom + Geist samples: Essence Bomb 1.576
-> 0.942, Life Drain 1.763 -> 1.536, Malice 1.852 -> 1.228. Split-half on the Geist sample (fit one half, audit the
other, 2 seeds): per source 0.108 / 0.097 -> 0.035 / 0.026, mix 0.058 / 0.051 -> 0.022 / 0.015; the same refit
without swap_full lands about the same (0.029 / 0.027, mix 0.018 / 0.022, its Soul Exchange correction refit to
~0.58), so on the audit the two are even: swap_full is kept because it is what the replays show per cast, with one
free factor fewer. (On 18-player halves of the phantom sample alone the refits disagreed: why the earlier sweeps
left Geist.)

Results: Geist whole-match mix 0.035 -> 0.010, Soul Exchange 0.073 -> 0.145, Essence Bomb 0.235 -> 0.162, Malice
0.190 -> 0.146 (real 0.139 / 0.190 / 0.144); audit 0.0185 -> 0.0184. Phase mix (both samples, window 0.05) 0.135 /
0.128 / 0.129 -> 0.015 / 0.069 / 0.080, ult real / sim 2.37 / 1.69 / 1.55 -> 0.95 / 0.77 / 0.81 (now a little over
mid and late). sim_vs_win Lady Geist 27k + 37k: all 0.410 -> 0.398, within slot and tier 0.409 -> 0.395, damage
items 0.389 -> 0.415 (swap alone 0.416 within; the plain refit 0.396), within one hero's noise.

## Replay readers after game pauses (2026-10-28)

A pause moves the replay's tick -> game time offset (1-10 stretches per replay; the 259 cast replays: median 21 s of
pauses, 75th percentile 46 s). #172 found victor_revive.py dropped every cast after a pause; the other replay readers:

- `fight_patterns/replay_openers.py` kept only casts on the replay's most common offset: 21% of the casts in the 259
  cast replays dropped (half the replays lost over 18%), plus every cast whose cooldown starts after its duration
  (Calico's Ava, Ivy's Air Drop, Rem's Lil Helpers read ~0). Now `fit_cast_timing.real_casts`, and `--split` reads the
  cast_timing + fight_length extracts (259 matches; no Mo burrow rows). The 'replay' block of data/fight_patterns.json
  (what combo_check.py compares with) is rebuilt from them: cast shares ~25% higher for every hero. On the same 259
  replays the fix alone changes the replay order of Shiv, Wraith, Rem and Warden's ult setup; combo_check.py with the
  file's and the fixed variant: timing error, mix and ability log error the same to 0.001 for all four (under cast
  timing the holds decide when abilities go out, the order only breaks ties), so `order` / `ult_after` stay.
- `team/area_hits.py` and `team/ability_area_phase.py` put a fight's game time at one offset per match (the ticks
  past the game clock at its end), so fights before a pause read their net worth up to a pause's length early (median
  16 s). Now `fit_length.clock_offset` (deaths line the clock up per stretch; all 260 replays): area item phase bins
  move <= 0.05 (inside their 95% bands), ability phase curves <= 0.04. Audit 0.0184 -> 0.0186, sim_vs_win 27k all
  0.296 -> 0.296, within slot and tier 0.331 -> 0.331, damage items 0.184 -> 0.183: kept as the correct reading, no
  refit (nothing moved enough to need one).
- `nurse/nurse_replays.py` (report only, its leech extracts are not kept) has the same one-offset net worth; left.
- `fight_patterns/replay_imbues.py` and `mechanics/split_shot_replays.py` only compare damage ticks with each other
  (no game clock): not affected.

## Soul Exchange waits for a real swap gap (2026-10-28)

After the whole swap (#173) Soul Exchange matched the whole match (0.145 vs 0.139) but not the phases: on the Geist
sample (238 players) real ult share 0.142 / 0.134 / 0.145 at 30 / 60 / 90% (flat), sim 0.154 / 0.174 / 0.182 (real /
sim 0.92 / 0.77 / 0.80, scripts/phase_mix.py).

Replays (swap_real.py, now also printing the gap at each swap): a real swap takes the same ~0.48 of the target's max
health at every phase (0.49 / 0.47 / 0.48), 0.89-0.98 of casts hit. The sim's swap took 0.30 / 0.35 / 0.34, and it
swapped ~1.3x as often per damage Geist dealt (pair fights: real swaps per Geist damage in target max healths 0.32 /
0.36 mid / late, sim duels ~0.45 at every phase): two errors that cancel early and not later. Why: the sim swapped as
soon as Geist was SWAP_MIN_GAIN 0.3 below her target (gap at swap median 0.43, target 0.79), real Geists wait for a
bigger gap (median 0.61, quartiles 0.45 / 0.75; target 0.88, Geist 0.25; the halves agree within 0.03).

Mechanics.swap_gap (on): each fight's swap (Mechanics.execute_timing's plan, SoulExchange.draw_plan) waits for a gap
drawn from the real swaps' gaps (ghost.SWAP_GAPS, 20 quantiles; a draw independent of the hold's) instead of 0.3. The
sim's gaps at swap then match real (median 0.59, quartiles 0.47 / 0.74). Fewer duels reach their gap, so the hold
share was refit (execute_timing.py --se-only --write, new option: keeps Killing Blow's rows): 0.789 -> 0.992, at its
cap: the sim's cast by 20 s is 0.33 vs real 0.42 (the duels don't open a real gap as often as real fights with fresh
third parties do). Swap size per cast 0.37 / 0.40 / 0.47.

Tried first, dropped: Geist's area abilities on Mechanics.ability_area_phase (Essence Bomb 0.86 -> 1.20, Malice 0.89
-> 1.03 by net worth): late phase better, early much worse, held-out phase distance worse on both halves.

Split-half (phantom + Geist samples, 507 matches; Geist corrections refit 3 rounds on one match-id half, audit the
other; reference = main's model refit the same way):
| held-out | per-source | whole mix | phase mix 30 / 60 / 90% | ult real / sim 30 / 60 / 90% |
|---|---|---|---|---|
| odd, main | 0.0285 | 0.0160 | 0.011 / 0.078 / 0.084 | 0.95 / 0.74 / 0.78 |
| odd, swap_gap | 0.0223 | 0.0210 | 0.038 / 0.037 / 0.073 | 1.25 / 0.93 / 0.83 |
| even, main | 0.0258 | 0.0250 | 0.029 / 0.049 / 0.067 | 0.93 / 0.80 / 0.84 |
| even, swap_gap | 0.0234 | 0.0130 | 0.032 / 0.033 / 0.056 | 1.23 / 0.99 / 0.94 |

Per source and summed phase distance better on both halves; mid game now right, late closer, early now under (the
early duels rarely open a 0.6 gap). Whole-sample refit moved Geist's corrections by < 0.003.

Results: full audit (phantom sample, all heroes) 0.0184 -> 0.0184; Geist there (37 players) 0.015 -> 0.023, Soul
Exchange 0.145 -> 0.121 (real 0.139). sim_vs_win Lady Geist 27k + 37k: all 0.405 -> 0.380, within slot and tier 0.402
-> 0.380, edges clear of noise 0.604 -> 0.641 (one hero, 259 pairs). Left: early swaps (0.8x real).

## Viscous: Express Shot on the alt fire (2026-10-28)

Viscous was the hero furthest from real damage on the whole-match audit after #177: mix 0.068 (29 players), 0.077 on
a new sample of 410 Phantom+ matches with a Viscous (221 players; match ids from aim_sample.jsonl.gz not in
phantom_sample, fetch_validation.get + slim, as the Geist sample). Express Shot read 2.7x under (0.069 of his damage
real vs 0.026 sim), Spirit Snatch 1.7x, Melee Charge 1.5x, his abilities a little over.

Cause (scripts/mechanics/viscous_alt_fire.py, 22 Viscous players in the fight_length replays):
- Viscous has an alt fire (citadel_weapon_viscous_set_2: one 42-damage slow goo shot per 1.26 s) beside his
  10.34-damage primary. Players holding Express Shot put a median 45% of their gun damage in it (4% without the item),
  and its proc events sit at 1.3x an alt-fire hit (median 113 vs alt 88, primary 26): the proc rides the alt shot,
  whose bonus is the item's ProcBaseAttackDamagePercentAltFire. Real damage per proc ~160 from the second fifth on;
  the sim fired it as two primary bullets with +125%, ~50.
- Spirit Snatch procs on 0.98 of landed Puddle Punch casts (286 / 292; 83% of the procs right after a Punch; Melee
  Charge 99 / 124). The sim procced on-melee items on an ability melee hit in its landing factor's share
  (min(1, landing)): Punch's landing x length_corr is 0.51, but it stands for a real hit about half the sim's full one
  (real median ~125 vs ~280 before the factor), not for half the hits landing.

Fix: items_fx.EXPRESS_ALT (Viscous): the proc shot's damage is the alt weapon's bullet over the primary's (raw
items.json) with the alt-fire bonus; items_fx.FULL_MELEE_PROC (Puddle Punch) procs on-melee items in full. Sim
landed damage per proc 111 / 150 / 167 at 0-40 / 40-70 / 70-100% of the match (real ~160 throughout). No refit:
ability_corr_heroes --split on the phantom + Viscous sample (250 players) was worse on one half's mix, kept none.

Results (Viscous, phantom + Viscous sample, 250 players): mix 0.076 -> 0.038; per-source distance by match-id half
0.070 -> 0.048 / 0.083 -> 0.056 (mix 0.074 -> 0.034 / 0.077 -> 0.041); holders Express Shot real/sim 2.66 -> 1.03,
Spirit Snatch 1.66 -> 1.45, Melee Charge 1.55 -> 1.24. Full audit 0.0184 -> 0.0185 (Viscous there 0.068 -> 0.027).
sim_vs_win Viscous 27k + 37k: all 0.448 -> 0.453, within slot and tier 0.438 -> 0.444, damage items 0.408 -> 0.434.
Left: his abilities still a little over (Splatter 0.31 vs 0.28), and the alt fire's own shots (non-proc) are not
modelled: holders' gun is one primary weapon in the sim. Shiv and Yamato also have alt weapons and read Express Shot
1.35x / ~1.2x under: the same check may apply.
