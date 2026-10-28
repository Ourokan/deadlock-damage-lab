"""Combat mechanics (added 2026-10-15, on by default since 2026-10-16): parry, enemy summons that can be shot, other enemies near the target
(multi-target items), and movement (escape and chase, slows, dashes, mobility items).

An Engine built without a mechanics value uses DEFAULT (Mechanics(): all on, no extra nearby enemies):

    from deadsim.mechanics import Mechanics
    duel(a, b)                                              # parry, summons and movement on
    duel(a, b, mechanics=None)                              # the earlier model
    duel(a, b, mechanics=Mechanics(movement=False))
    duel(a, b, mechanics=Mechanics(extra_targets=1.0))      # a team fight with one more enemy hero next to the target
    import deadsim.mechanics; deadsim.mechanics.DEFAULT = None   # off for every Engine built without one

time_to_kill's dummy never runs, parries or times Counterspell; survival/survival.py turns movement off (an
escape would count as surviving).

Settings fitted to real ranked matches (validation/README.md, "New mechanics"):
- Parry: Skill.parry_rate = share of incoming heavy melees the defender parries (0.15: 5% of all hero melees, from
  team parry counts vs enemy melee hits). A parry cancels the melee and stuns the attacker for ParriedStunTime
  (2.75 s), during which he takes VictimDamageTakenScale (25%) more damage. Light melees are not parried
  (assumption). With parry on, the melee rotation runs 1 / (1 - parry_rate x heavy_share) faster so landed melee
  damage stays at the fitted rate. Missed parries (as common as successes in real games) cost nothing here.
- Counterspell: when the enemy casts an aimed ability (skillshot / target / aoe) and Counterspell is ready, the
  holder times a spell parry with Skill.spell_parry_rate; for SpellParryDuration it blocks the damage, DoTs and
  debuffs of that cast (and of any other enemy ability or item hit). Ultimates use Skill.spell_parry_rate_ult when
  set. Real holders' ability damage taken drops ~0-3% after buying it (same-player before/after vs teammates), and
  in-match vs teammates it moves no more than their gun damage, Lash's Death Slam included (validation/README.md
  "Cleanses"), so the rates are low (scripts/fit_counterspell.py).
- Summons (Mechanics.summons): McGinnis turrets and Graves' zombies, ghouls, Deadheads and gravestone have health
  (from the data, + boons) and the enemy spends a share of its trigger pulls on each living kind, at acc_mult x its
  hero accuracy. Shares and accuracy multipliers per kind are in data/summon_targeting.json: the shares are fitted
  so the sim's share of enemy gun damage that hits summons instead of the owner matches Phantom+ replays
  (scripts/summons/). Skill.summon_focus overrides every kind's share. Non-gun damage the owner takes (area
  abilities, items, melee) also hits every living summon: x its kind's splash share, fitted the same way (in the replays
  60-70% of what enemies deal to zombies and turrets is not gun damage). A kind with break_p (the gravestone) is
  broken by the enemy break_s after it lands with that probability, as an expected value (real share of gravestones that took
  hero damage and were destroyed by a hero; real median time to break). A dead summon stops attacking. Damage to
  summons is not hero damage (`FightResult.*_summon`). A summon lives at most life_other_s (real median life of
  summons no hero killed). Every other hero summon (Sinclair's Assistant, Grey Talon's
  owl, Solomon's pieces, Rat King's rats and banner, Medicinal Specter) has no health in the replays: it can't be shot.
- Other enemies (Mechanics.extra_targets): expected number of other enemy heroes close to the target. Ricochet
  bounces and Split Shot pellets that hit them are booked apart (`FightResult.*_splash`), they never kill anyone.
  Real Ricochet damage is 15% of its holders' gun damage, which is 0.23 bounces per hit, so a fair team-fight
  value is about 0.25, not 1-2.
- Split Shot also hits the main target: during the active each landed gun bullet lands SPLIT_PRIMARY_HIT more
  copies (x SPLIT_REF_M / the holder's median fight distance: the fan's share on the target, Mechanics.split_range), which proc on-hit items like bullets (Mercurial Magnum's bonus rides on them in replays). Other nearby
  enemies take SPLIT_SECONDARY_COVER x Mechanics.extra_targets copies per landed bullet. Both from Phantom+ replays
  (scripts/mechanics/split_shot_replays.py, 614 activations of Vyper, Wraith, Yamato, Paige): in the 5 s after an
  activation the main target takes 0.73 Split Shot hits per gun bullet landed on it (Vyper 0.76, Wraith 0.59), the
  others 0.29 of that, with ~0.29 other enemies within 13 m (real_nearby). Side copies are capped at one per landed
  bullet (each target is hit once per fan), so a team fight's 4-5 living enemies don't run past the fit.
  The active waits until the holder can shoot a target that can be hurt (not into Vyper's own petrify).
- Movement (Mechanics.movement): fighters hold their distance (the step 2 calibration) until one is losing and below
  Skill.flee_hp; he stops shooting and runs, the other chases and keeps shooting. Speed = hero max_move_speed +
  move speed items and buffs, times (1 - slows x (1 - slow resist)); stunned / immobilized = 0. Both dash
  (ground_dash_distance over ground_dash_duration) while stamina lasts; stamina items add charges and regen. The
  runner escapes when the gap reaches Mechanics.escape_dist: the fight ends with no winner (`FightResult.escaped`).
  Slows come from abilities with a SlowPercent-type property (applied on cast at spirit accuracy, a generic
  approximation) and from items: Slowing Hex, Mystic Slow, Slowing Bullets, Cold Front, Arctic Blast, Phantom
  Strike, Lifestrike. Escape tools: Warp Stone, Ethereal Shift, Fleetfoot, Dispel Magic, Counterspell,
  Magic Carpet, Enduring Speed, stamina items. Phantom Strike closes the gap on a runner. Hero mobility abilities
  (grapples, teleports, flight) are NOT modeled: only items, base speed, sprint and stamina. Majestic Leap gets no
  escape value: real holders escape less often, not more (it is an engage tool), so it keeps its step 2 barrier only.
- Range spread (Mechanics.range_drift): the distance is lognormal around the fight distance (log sd and drift time from
  real Phantom+ 1v1 positions, data/fight_range.json), and the engine takes distance effects as expectations over it
  (Engine.p_within / spread_mean / reach_ready). See validation/README.md "Range spread".
"""
from __future__ import annotations

import bisect
import json
import math
import os
import zlib
from dataclasses import dataclass

from .build import combine_resist
from .data import GAME
from .items_fx import BuildUp, FX, CC_KEYS, _any_melee, _melee_proc


SUMMON_ACC_MAX = 0.9        # cap on accuracy against a summon (acc_mult x hero accuracy)
SPLIT_PRIMARY_HIT = 0.73    # Split Shot copies landing on the main target per landed gun bullet (replays)
SPLIT_SECONDARY_COVER = 0.73  # copies on other enemies per landed gun bullet per nearby enemy (replays)
SPLIT_REF_M = 11.5          # holder's median fight distance at which SPLIT_PRIMARY_HIT holds (Mechanics.split_range)
SPLIT_MIN_M = 8.2           # closest fitted median distance (Yamato): closer heroes (Abrams 7.5) don't extrapolate
WARP_AWAY = 0.3             # share of Warp Stone's teleport range that ends up as extra gap when running (fit)
MELEE_REACH = 6.0           # beyond this gap (+ start distance) rotation melees don't land
FLEE_RECOVER = 0.25         # stop running once health is this much above flee_hp (heals)
SPRINT_DELAY = 2.0          # a runner sprints (hero sprint_speed + Sprint Boots) after this long (assumption)
PARRIED_CAST_SPAN = 3.5     # s after its cast delay that a spell-parried cast's own effects stay blocked
CHASE_PROB = 0.85           # share of runs the other side chases (full speed, dashing); else he stands and shoots (fit)


@dataclass
class Mechanics:
    parry: bool = True
    summons: bool = True
    movement: bool = True
    range_drift: bool = True     # distance spreads around the start distance (Engine.p_within etc., fight_range.json)
    extra_targets: float = 0.0   # expected other enemy heroes near the target (multi-target items)
    escape_dist: float = 40.0    # gap (m) at which a runner is out of the fight
    # survival curve of real fight length (real_length(souls)): P(still trading at k x LENGTH_STEP s | nobody
    # died). None = the fight's damage counts in full until a death or max_time (dmg_exp = dmg_out)
    fight_length: tuple | None = None
    # with fight_length: the hits of each source the sim casts on sight are booked as if its first use came after the
    # real hold (opener_holds, data/opener_timing.json): real players often open later or on cooldown from a fight
    # before. Off by default: with it on, length_factors.py must be rerun (the corrections move toward 1) and the
    # overall search's builds did not get better (validation/README.md "Opener timing")
    opener_timing: bool = False
    # with fight_length: each ability's first cast waits a hold drawn from the real Phantom+ cast timing (cast_holds,
    # data/cast_timing.json, scripts/cast_timing/fit_cast_timing.py), so a duel no longer opens with every ability
    # and the ultimate at t=0 (real players cast the ult in ~10-40% of fights; on cooldown or held). Fights with a
    # Skill.fight_phase draw the hold quasi-randomly from it, others from the engine rng; deterministic fights
    # (no rng, no phase) keep casting on sight
    cast_timing: bool = True
    # melee item holders' opening melee (2026-10-25): with fight_length, a fighter holding a melee item (Spirit Strike,
    # Spirit Snatch, Melee Charge, Crushing Fists) lands one full melee hit at a time drawn from the real holders'
    # first proc (data/melee_timing.json, scripts/fight_length/melee_timing.py); the steady melee rate then pays it
    # back (a long fight keeps the fitted melee; a short one up to one hit more, as real openers add). Draws like
    # cast_timing (phase or rng; deterministic fights skip)
    melee_timing: bool = True
    # heavy melee of Melee Charge / Crushing Fists holders (2026-10-27): real holders' basic melee hits are ~half heavies
    # that proc the item (Apollo 0.67, Abrams 0.54; data/melee_heavy.json, scripts/mechanics/melee_heavy.py), the
    # rotation's HEAVY_SHARE is 0.3 for everyone. A holder's rotation takes the hero's real share, at a melee rate
    # cut so melee damage per second stays the fitted one (fight.heavy_holder_skill); only the item's procs move
    heavy_holders: bool = True
    # fight entry health (2026-10-25): with fight_length, a fighter whose start health wasn't set (survive's
    # start_hp) starts short of full by a deficit drawn from the real Phantom+ entry health spread at hero combat
    # start (data/sustain.json entry_deficit_q, scripts/sustain/fit_sustain.py; about half the fights start full).
    # Health-gated abilities (Killing Blow, Assassinate, Close The Deal, Lethal Venom) then meet their threshold as
    # early as in real fights. Draws like cast_timing (phase or rng; deterministic fights start full). Off by default:
    # with it on (factors kept with length_factors.py --entry) execute timing matches real, but sim_vs_win per item
    # fell 0.239 -> 0.216 and the audit 0.0314 -> 0.0330 (validation/README.md "Fight entry health")
    entry_hp: bool = False
    # execute gates on real entry health (2026-10-26): with fight_length and entry_hp off, a fighter whose start health
    # wasn't set gets the same real entry deficit draw, but only health-gated execute abilities see it
    # (Fighter.gate_hp: Killing Blow, Assassinate, Close The Deal, Lethal Venom cast and scale on health short by
    # it), so they land as early as in real fights while every fight keeps its length (validation/README.md
    # "Execute gates on real entry health")
    entry_gate: bool = True
    # third parties at the health gates (2026-10-26): with fight_length, Soul Exchange's Geist sees her health short
    # by a real entry deficit (as entry_gate) and by the damage the real pair fight's other enemies add (data/execute_timing.json assist: ~1.15x the damage from
    # the pair enemy, scripts/mechanics/execute_timing.py), so the swap's gap opens as in real fights; only the gate
    # sees it (Fighter.self_gate_frac; execute gates on Geist don't), health and fight length stay
    gate_assist: bool = True
    # target health for health-conditional items (2026-10-26): with fight_length, a fighter facing an enemy that holds
    # an item conditioned on its target's health (TARGET_HEALTH_ITEMS: Opening Rounds; Tankbuster and Decay, which
    # deal damage from it) is seen by that item short by a real entry deficit (as entry_gate) and by TARGET_ASSIST x
    # the damage it takes in the duel (the real fight's third parties, Fighter.item_hp_frac; CURRENT_HEALTH_ASSIST
    # for Tankbuster and Decay, Fighter.item_hp). Health and fight length stay. Sim duels landed 85% of gun damage on
    # targets above half health, real Phantom+ replays 64% (scripts/fight_length/target_health.py,
    # validation/README.md "Target health")
    target_health: bool = True
    # Killing Blow and Soul Exchange first casts on real timing (2026-10-26): with cast_timing, each fight draws a
    # plan (data/execute_timing.json). Killing Blow: spent at a real time without an execute (most real first casts:
    # the slash on a ~55% target or a miss, then the whole cooldown), wait for the execute gate, or not cast (on
    # cooldown). Soul Exchange: held to a real first cast time (or not cast), then its gap gate
    execute_timing: bool = True
    # ability pokes (2026-10-26): with fight_length, an ability with a used row in data/ability_pokes.json (Paradox's
    # Kinetic Carbine) also lands its real poke hits per fight beside the duel: pokes_per_fight casts on the duel's
    # target outside the fight, damage and procs booked in full, the duel's health and cooldowns untouched
    # (fight.add_pokes; scripts/fight_length/ability_pokes.py, validation/README.md "Carbine pokes")
    pokes: bool = True
    # ability recasts on real timing (2026-10-26): with fight_length, after each cast of a single-charge, non-ultimate
    # ability the next one also waits a delay past the cooldown drawn from the real Phantom+ recast curve (data/
    # recast_timing.json: P(recast by t s after ready | fight still going), per ability, pooled for abilities without a
    # row; abilities the sim already gates keep their own timing; None = not again this fight). The sim recast ~90%
    # within 0.5 s of ready, real players ~20% (scripts/cast_timing/recast_timing.py). Draws like cast_timing.
    # Landing corrections were kept at their levels (length_factors.py --entry --target-entry --target-off
    # MECH.recast_timing), so it moves when ability damage lands and what cooldown items are worth, not how much
    # the fitted factors give (validation/README.md "Ability recasts on real timing")
    recast_timing: bool = True
    # charged abilities' gaps (2026-10-28): recast timing skips charged abilities, so the sim cast the next charge as
    # soon as AbilityCooldownBetweenCharge allowed: Viscous' second Puddle Punch 1.7 s after the first, inside Spirit
    # Snatch's 6 s cooldown (54% of sim Punches met it on cooldown, 24% of real ones; Snatch read 1.5x under). With a
    # row in data/charge_gaps.json (scripts/mechanics/charge_gaps.py) the wait from a cast to the next is drawn from
    # the real gaps between landed casts (Punch: 22% under 6 s), its finite part as recast_timing's resets. Off: Snatch
    # per landed Punch then matches real (0.46 -> 0.88), but the sim lands fewer Punches, and the Punch refit that
    # needs made the held-out damage mix worse (split-half 0.024 -> 0.038), validation/README.md "Viscous: procs per hit"
    charge_gaps: bool = False
    # cooldown items at the fight start (2026-10-27): the real holds (cast_timing) carry real players' share of fights
    # opened with an ability still cooling from the fight before, at real cooldowns, so cooldown items only bought
    # recasts. With cast_timing, a build whose items cut an ability's cooldown (to k x) starts more fights with it
    # ready: the ready share rises by rho x (r(k) - r(1)), r = real share of fights with time since the last cast >=
    # k x cooldown, rho = the share of it real holders get (data/cdr_ready.json, scripts/cast_timing/cdr_ready.py);
    # the hold draw moves from the late / not-cast end of the real holds to the early end by that much
    cdr_ready: bool = True
    # gated ults at the fight start (2026-10-27): an ability the sim gates itself (no cast_timing hold) started every
    # fight ready, so Apollo cast Itani Lo Sahn in 92% of his audit duels by 20 s vs 38% of real Phantom+ pair fights:
    # real Apollos open only 53% of fights with the ult off cooldown (data/cdr_ready.json, time since the last cast >=
    # cooldown). With cast_timing, an ability in GATE_READY starts a fight on cooldown (not cast in it) past its real
    # ready share, raised by cooldown items as cdr_ready; ready, it keeps its own gate (mechanics.gate_ready)
    gate_ready: bool = True
    # an allied Nurse's Wretched Vapors (2026-10-27): real Nurses mostly vapor their allies (nurse.SELF_CAST), and the
    # game credits the crash to whoever hit the vapored ally, as ability_nurse_adrenaline_rush. A duel has no ally, so
    # (a share, b share): the expected share of each fighter's incoming damage an allied Nurse's rush defers, crashed
    # back at +DeferredDamageBonusPercent and booked as the attacker's crash (nurse.AllyVapors). Set per duel by the
    # damage audit from the real teams (nurse.ally_vapors_share: a teammate Nurse); 0 elsewhere (no teams)
    ally_vapors: tuple = (0.0, 0.0)
    # area abilities' extra heroes by game phase (2026-10-27): an ability's landing factor absorbs its pooled hits on
    # the other enemies of real fights, but those grow with net worth (lane trades -> team fights: Lurking Terrors
    # 2.6 heroes per main hit at 5k, 4.2 at 42k; the gun 1.2 -> 1.4). Its damage at the duel's net worth is x rel(nw)
    # / pooled rel, rel = its hits per main hit over the gun's (ability_area_mult, data/ability_area_phase.json,
    # scripts/team/ability_area_phase.py): the
    # pooled level stays, the phase shape moves (Nurse's ult share real 0.15 / 0.36 / 0.45 at 30 / 60 / 90% of the
    # match, sim 0.28 / 0.35 / 0.35 before)
    ability_area_phase: bool = True
    # Mo & Krill's prefight Burrow by game phase (2026-10-28): the sim opened every fight with Mo emerging on the target
    # (deadsim.patterns prefight). Real Phantom+ Mos are underground at the start of ~7% of lane fights and ~20% later
    # (scripts/mechanics/krill_burrow.py, Burrow's m_bInGround in 90 replays). With cast_timing, Burrow opens burrowed in
    # its real share at the fighter's net worth (data/burrow_prefight.json, linear in ln net worth); otherwise its first
    # cast waits a hold drawn from the non-negative part of its real hold (cast_timing; the negative part is the
    # burrowed starts)
    burrow_prefight: bool = True
    # Graves' jars and Grasping Hands by game phase (2026-10-28): a duel can't collect deaths, so Graves opened every
    # fight with 2 stored jars and threw both, and cast Grasping Hands on its pooled hold. Real Phantom+ Graves throw
    # 0 / 1 / 2 / 3+ jars in 41 / 45 / 12 / 3% of lane fights and ~28 / 49 / 17 / 6% later, and cast Grasping Hands
    # in 0.70x the match's share of fights before 30% of it, ~1.1x after (scripts/mechanics/graves_jars.py, 73
    # replays). With fight draws (phase or rng) the jars at the start are a draw from that share at the fighter's net
    # worth (necro.JarOfDead) and Grasping Hands' hold cast share is x its mult (as ult_phase; data/graves_phase.json)
    # Off: it beat main before a refit, but a plain Graves refit on the same halves did better held out (per-source
    # 0.019 / 0.025 vs 0.023 / 0.027 with it), validation/README.md "Mo & Krill and Graves by game phase"
    graves_phase: bool = False
    # Rem's Tag Along (2026-10-28): it needs an ally, so the sim never cast it and Rem shot through every duel. Real
    # Phantom+ Rems ride an ally for 5% of their lane combat time, 9-11% mid game and 14% late (attach state bit in 25
    # replays, scripts/mechanics/rem_tag_along.py); while attached they deal no gun, Pillow Toss or melee damage and
    # take ~8% of the damage (3 vs 38 per s), but their items and Naptime keep hitting. With fight draws (phase or
    # rng) Rem is attached for windows drawn so the share of the duel matches data/tag_along.json at his net worth
    # (lengths from its real quantiles, alternating with exponential free gaps): gun, melee and Pillow Toss locked,
    # damage taken x familiar.TAG_TAKEN (Mods "damage_taken_mult", on top of amps)
    tag_along: bool = True
    # Paradox's Pulse Grenade pulses (2026-10-28): the sim kept the time-slowed target inside for every pulse (5, 7 at
    # T3), so a landed throw dealt them all and stacked the damage amp 5-7 times. Real Phantom+ throws that hit a hero
    # hit their main victim with 1.7 pulses in the lane and ~2.1 later (3,311 throws in 70 replays,
    # scripts/mechanics/pulse_grenade.py), and the game books the amp under Pulse Grenade (19% of its damage, ~2
    # stacks per hit). Pulse i deals and stacks x P(more than i pulses) at the fighter's net worth
    # (data/pulse_hits.json, linear in ln net worth) and the amp on Paradox's other hits is booked under Pulse Grenade
    # (engine.BOOKED_AMPS). Off: refit on top of it (ability_corr_heroes --split, 3,661 fresh Phantom+ matches), it
    # held out worse than a plain Paradox refit on the same halves (per-source 0.027 / 0.026 vs 0.023 / 0.023, mix
    # 0.032 / 0.034 vs 0.028 / 0.031), also with the booked amp left unscaled (0.027 / 0.026) or unbooked (0.025 /
    # 0.024): the refit lifts Pulse Grenade's correction to ~2.1 and Paradox's gun share, already under, drops
    pulse_hits: bool = False
    # melee by game phase (2026-10-27): real players melee most in the lane and less as the game goes on (the hero's
    # real melee share over the sim's, all heroes: 1.20x at 30% of the match, 0.91x at 60%, 0.74x at 90%; Calico 1.27 /
    # 1.15 / 1.03, while per hit sizes match the formula). The melee rate is fitted flat, so at the duel's net worth it
    # is x melee_phase_mult (data/melee_phase.json, scripts/mechanics/melee_phase.py: real over sim melee share at
    # 30 / 60 / 90% of the match, shrunk to the pooled curve; linear in ln net worth between the points, flat outside)
    melee_phase: bool = True
    # ult casts by game phase (2026-10-27): the ult holds (cast_timing) are one curve over the whole match, but real
    # players cast the ult in fewer fights early: P(cast by 20 s of a pair fight) 0.88x the whole-match share before
    # 45% of the match, 1.06x to 75%, 1.02x after (Solomon 0.61 / 1.33 / 0.86, Infernus 0.79 / 1.12 / 1.06). The hold's
    # cast share at the fighter's net worth is x ult_phase_mult (data/ult_phase.json, scripts/cast_timing/ult_phase.py)
    ult_phase: bool = True
    # opt-in (2026-10-27): damage a barrier soaks is not booked as dealt. The game's damage numbers (DamageEvent damage,
    # the API damage matrix) are health lost; what a barrier absorbs is in damage_absorbed only (replays: gun 5% / 9% /
    # 9% of hits on heroes before 45% / to 75% / after, other damage 5% / 9% / 10%; the sim's duels book gun 6% / 11% /
    # 12%, all damage 6% / 9% / 10%). The duel is unchanged (the barrier still takes the hit), only dmg_out / dmg_exp
    # drop it. Off: it moves the late gun share only 0.223 -> 0.221 (real 0.202) and the whole-match audit was fitted
    # with barrier damage booked (0.0207 -> 0.0215 on, items rise); it would need an item_landing refit with it on
    unbook_absorbed: bool = False
    # bullet resist shred debuffs in fights (2026-10-27): a duel keeps every shred debuff (items, Hunter's Aura, hero
    # abilities) on its one target, so the sim's gun hits late in the match kept 1.05x the damage the target's build
    # resists allow; real gun hits on heroes keep 0.99x / 0.99x / 0.98x at 30 / 60 / 90% of the match (160 replays,
    # DamageEvent (damage + absorbed) / pre_damage over the target's build resist, scripts/gun_calib/gun_phase.py
    # --replays): real fights spread the shooter's hits over targets and the debuffs lapse. Fitted per attacker hero
    # (split-half 0.40 / 0.30, items and abilities alike): the in-fight shred values are x shred_uptime
    shred_uptime: float = 0.35
    # debuffs under focus (2026-10-28): survive(focus=) makes the one simulated foe hit x focus to stand in for that
    # many enemies, but it still applies its stuns, slows, silences and shreds once. Status resist saves the same
    # share of every enemy's debuff time, so the focused fighter's resist counts x focus (Fighter.status_resist,
    # at most 1): Debuff Reducer's 25% had half the duel value of the enemy team's debuffs it shortens
    status_focus: bool = True
    # CC lands like the ability (2026-10-28): an ability's stun / silence / disarm / immobilize always went on the
    # target in full while its damage counts x its landing (skillshot spirit accuracy, the fitted ability landing
    # factor, the wait for the target to be in reach). Replays (scripts/fight_length/cc_time.py, pawn modifier state
    # bits, 260 Phantom+ matches): a player is stunned or asleep 2.7% and silenced 2.2% of their combat time by ALL
    # enemies (63% / 58% of it from their pair-fight foe), while damage_audit's duels had the ONE foe stun them 4.2% and
    # silence them 3.1%. On: the CC's duration is x the ability's landing (capped at 1; items' CC is unchanged): sim
    # stun 3.3%, most per-hero gaps close (Mo & Krill 26% -> 10% of combat time, real 6%); whole-match audit flat
    # (0.0180 -> 0.0181); sim_vs_win 27k all 0.298 -> 0.301 but within slot and tier hero halves -0.001 / +0.000, 37k
    # within 0.317 -> 0.316 in both halves: off (validation/cc_time.md). status_focus off instead: 27k within
    # 0.333 -> 0.331, both halves
    cc_landing: bool = False
    # gun time by build (2026-10-27): real players shoot less the more souls their build has in spirit items (real
    # over sim gun share, Phantom+ sample, scripts/gun_calib/gun_build.py: about 0.94 with < 2k spirit souls, 0.78 at
    # 10-16k, 0.65 past 24k, the same at 30 / 60 / 90% of the match for the same spirit souls; within a hero too: Ivy
    # 1.23 gun builds / 0.38 spirit builds, Bebop 1.03 / 0.58), while the sim fires whenever it can. The gun's fire
    # interval and reload time are / exp(-gun_lean x spirit item souls / 1000) (the gun's whole timeline slows, so its
    # damage per second drops by that factor)
    gun_lean: float = 0.028
    # abilities by build (2026-10-28): real players with more souls in spirit items also open fights with their abilities
    # sooner and recast them sooner after cooldown (Phantom+ replays, stratified Cox per ability: hazard x exp(0.0060 per
    # 1000 spirit item souls) for first casts with net worth and cooldown reduction in the model, both halves of the
    # matches 0.0079 / 0.0075 without cdr; recasts 0.0101 +- 0.0021 with the same terms), while the sim drew both from one curve per ability.
    # With cast_timing / recast_timing, each draw u becomes 1 - (1 - u) ^ (1 / hr), hr = exp(ability_lean x (spirit
    # item souls - the hero's mean over its real chances) / 1000) (data/ability_lean.json): the hero's pooled curve stays
    # its average, spirit builds cast sooner, gun builds later. The damage audit had every hero's ability share ~4% under
    # and item share ~10% over on spirit builds (same hero, same fifth of the match), items alone fine
    # (scripts/cast_timing/ability_lean.py, validation/README.md "Abilities by build"). Opt-in (0.006 = the replay fit):
    # it cut a quarter of that ability gap on held-out halves, but sim_vs_win 27k all 0.307 -> 0.302, within slot and
    # tier 0.343 -> 0.342 (spirit power and charge items gain value), so the searches keep it off
    ability_lean: float = 0.0
    # Soul Exchange swaps whole (2026-10-28): the swap is a health swap, not a hit that lands part of the time, yet it
    # took its fitted landing factor x length_corr (1.42 x 0.41 = 0.58), so the target lost ~0.20 of its max health per
    # swap vs ~0.50 in real Phantom+ replays (scripts/mechanics/swap_real.py) and the audit had it at half its real
    # share. On: the swap skips those factors and lands on ghost.SWAP_LAND of casts (real hits per cast)
    swap_full: bool = True
    # Soul Exchange's gap from replays (2026-10-28): the sim swapped as soon as Geist was SWAP_MIN_GAIN 0.3 below her
    # target (gap at swap median 0.43, target 0.79), real Geists wait for more (median 0.61, target 0.88; swap_real.py),
    # so the sim swapped ~1.3x as often per damage dealt for ~0.75x the health each, and Soul Exchange read ~1.25x real
    # in mid and late game. On: each fight's swap (Mechanics.execute_timing's plan) waits for a gap drawn from ghost.SWAP_GAPS
    swap_gap: bool = True
    # Sinclair's copied ultimates by ultimate (2026-10-28): Audience Participation's copy took one landing factor x
    # length_corr (0.60 x 4.8) whatever ultimate it copied, so the copies real Sinclairs get little from (Combo, Seismic
    # Impact, Nox Nostra, Feed The Birds: ~0.15-0.25x the sim's share in Phantom+ matches) carried as much as the area
    # ultimates that make most of her real copy damage (Lurking Terrors, Abstract Landscape, Storm Cloud), and the
    # copy read 1.5x its real share of her damage. On: the copy's factor also x the copied ultimate's real/sim ratio
    # (magician.copy_ult_factors, data/copy_ult.json, scripts/mechanics/copy_ult.py). Split-half: the held-out split of
    # her copy damage by ultimate 0.37 -> 0.19 / 0.20 (half the summed share gaps), but sim_vs_win for Sinclair dropped
    # (within slot and tier 0.381 -> 0.366, all 0.360 -> 0.349) where the plain Audience Participation refit held
    # (0.380 / 0.358): kept off, the refit alone is in data/landing_rates_mech.json
    copy_ult: bool = False
    # Ballistic Enchantment stacks (2026-10-28, items ranked furthest from real wins): +20% weapon damage per unique
    # enemy hero the imbued ability damaged in the last 20 s, but a duel has one enemy, so the sim's holder had at most
    # one stack. Real holders deal 1.15x the hero damage per minute of non-holders (27k, same hero, net worth and game
    # time), the sim's build 1.055x: the item furthest under its real damage. In Phantom+ replays a player shooting
    # with an area ability's hits fresh carries 1.5-2.8 of them (Malice 2.4, Aura of Suffering 2.6, Fixation 1.9),
    # single-target abilities 1.0. On: a stack is worth WeaponPowerPerStack x that count (ballistic_stacks,
    # data/ballistic_stacks.json, scripts/team/ballistic_stacks.py); 1 for abilities without a row
    ballistic_stacks: bool = True
    # Split Shot's fan by distance (2026-10-28): the BulletSplitShot copies spread over SpreadAngleDegrees, so the
    # share that lands on the main target falls with distance like its angular size. Real copies per landed gun bullet
    # (scripts/mechanics/split_shot_replays.py): Yamato 1.10 at an 8.2 m median fight distance, Vyper 0.76 at 10.9,
    # Wraith 0.59 at 15.6 (Paige 0.73 at 15.8 on 6 activations) = 8.4 / distance (activation weighted). On: the main
    # target takes SPLIT_PRIMARY_HIT x SPLIT_REF_M / the holder's median distance (skill_defaults.json, the hero's real
    # median, not the duel's current gap; at least SPLIT_MIN_M, the fit's closest hero) copies, so a
    # far hero (Vindicta 25.8 m: 0.33) no longer gets close-range Vyper's 0.73; off: SPLIT_PRIMARY_HIT for everyone
    split_range: bool = True


DRIFT_MIN, DRIFT_MAX = 1.5, 40.0   # meters; 40 = the fit's "nearest enemy" cut
_DRIFT = None


def drift_params():
    """(log_sd, tau_s) of real 1v1 fight distance around its median: data/fight_range.json (Phantom+ match_paths,
    scripts/range/fit_range.py)."""
    global _DRIFT
    if _DRIFT is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "fight_range.json")) as fh:
            a = json.load(fh)["duel"]["all"]
        _DRIFT = (a["log_sd"], a["tau_s"])
    return _DRIFT


def reach_share_at(median_m, reach_m, cooldown_s):
    """FX.reach_share without a fight: expected share of an on-cooldown proc that needs the target within reach_m,
    for a hero whose real fight distance is lognormal around median_m (drift_params): cooldown / (cooldown + the
    expected wait for the drift to bring the target in), Engine.reach_ready's mean field with no walk-in."""
    from .engine import REACH_P_FLOOR
    sd, tau = drift_params()
    p = 0.5 * (1.0 + math.erf(math.log(reach_m / median_m) / (sd * math.sqrt(2.0))))
    return cooldown_s / (cooldown_s + (1.0 - p) * tau / max(p, REACH_P_FLOOR))


LENGTH_STEP = 0.5   # s between fight_length points (data/fight_length.json step_s)
LENGTH_PHASES = ((10000, "lane"), (27000, "mid"))   # net worth bounds as overall_search.game_phase; above: "late"
_LENGTH = None


def real_length(souls=None):
    """Real Phantom+ fight length as a Mechanics.fight_length curve (data/fight_length.json,
    scripts/fight_length/fit_length.py): P(two enemy heroes are still trading t s after their first hit | neither
    died), at t = 0, LENGTH_STEP, ...; for the game phase of net worth souls (lane < 10k, late > 27k), all fights
    when souls is None. Median ~7.5 s, mean ~9 s to 30 s; only ~16% of real fights end in a death."""
    global _LENGTH
    if _LENGTH is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "fight_length.json")) as fh:
            a = json.load(fh)
        assert abs(a["step_s"] - LENGTH_STEP) < 1e-9
        _LENGTH = {k: tuple(v["survival"]) for k, v in a["phases"].items()}
    if souls is None:
        return _LENGTH["all"]
    ph = next((n for hi, n in LENGTH_PHASES if souls < hi), "late")
    return _LENGTH.get(ph, _LENGTH["all"])


_POKES = None


def poke_rows(hero):
    """{ability class: real poke hits per fight} for a hero's abilities with a used row in data/ability_pokes.json
    (Mechanics.pokes): hits outside any fight (no fight_length run of 4+ hits both ways), per fight of the hero."""
    global _POKES
    if _POKES is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "data", "ability_pokes.json")
        _POKES = {}
        if os.path.exists(fn):
            with open(fn) as fh:
                for r in json.load(fh)["abilities"]:
                    if r.get("use"):
                        _POKES.setdefault(r["hero_id"], {})[r["class_name"]] = r["pokes_per_fight"]
    return _POKES.get(hero.id, {})


_OPENER = None


def opener_holds(hero, items):
    """{damage source name: hold values (s)} for a fighter (Mechanics.opener_timing): its abilities' and items' real
    hold before their first use in a fight (data/opener_timing.json, scripts/fight_length/opener_timing.py), items
    pooled over heroes for a hero without a row. Only sources the sim casts on sight have one: in real Phantom+
    fights they land a median ~3 s later (on cooldown from the fight before, or held), the sim's at ~0.5 s."""
    global _OPENER
    if _OPENER is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "opener_timing.json")) as fh:
            _OPENER = json.load(fh)
    src, pooled = _OPENER["sources"], _OPENER["items_pooled"]
    out = {}
    for ab in hero.abilities:
        q = src.get(f"{hero.id}:{ab.class_name}")
        if q:
            out[ab.name] = tuple(q)
    for it in items:
        q = src.get(f"{hero.id}:{it.class_name}") or pooled.get(it.class_name)
        if q:
            out[it.name] = tuple(q)
    return out


_CAST = None
_MELEE_T = None


def cast_holds():
    """{"hero id:ability class": QBINS hold values (s) before the ability's first cast in a fight, None = not cast
    in that fight} (data/cast_timing.json)."""
    global _CAST
    if _CAST is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "cast_timing.json")) as fh:
            _CAST = json.load(fh)["sources"]
    return _CAST


_PREFIGHT = None


def prefight_share(hero_id, souls):
    """Mechanics.burrow_prefight: the share of fights the hero opens with its prefight ability at net worth souls
    (data/burrow_prefight.json, linear in ln net worth, flat outside), None without a row."""
    global _PREFIGHT
    if _PREFIGHT is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "data", "burrow_prefight.json")
        _PREFIGHT = {}
        if os.path.exists(fn):
            with open(fn) as fh:
                for k, v in json.load(fh)["heroes"].items():
                    _PREFIGHT[k] = [(math.log(nw), x) for nw, x in v["points"]]
    pts = _PREFIGHT.get(str(hero_id))
    return _interp_ln(pts, souls) if pts else None


def melee_holds():
    """{item class: {"fights", "holds": QBINS times (s) of a holder's opening melee proc, None = none}}
    (data/melee_timing.json)."""
    global _MELEE_T
    if _MELEE_T is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "melee_timing.json")) as fh:
            _MELEE_T = json.load(fh)["items"]
    return _MELEE_T


_HEAVY = None


def holder_heavy_share(hero_id):
    """Mechanics.heavy_holders: heavy share of a Melee Charge / Crushing Fists holder's melee (data/melee_heavy.json,
    the hero's row or pooled)."""
    global _HEAVY
    if _HEAVY is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "melee_heavy.json")) as fh:
            _HEAVY = json.load(fh)
    row = _HEAVY["heroes"].get(str(hero_id))
    return row["share"] if row else _HEAVY["pooled"]


MELEE_OPEN_FULL_RATE = 0.036   # landed melees/s: Bebop's with one melee item, the lowest of the real opener rows
HEAVY_OPENERS = frozenset({"upgrade_melee_charge", "upgrade_crushing_fists"})   # proc on a heavy melee


def melee_opener(f):
    """Mechanics.melee_timing: (seconds into the fight, heavy) of the fighter's opening melee, or None (no melee item
    with a fit, nothing to draw from, or a no-opener draw). The item with the most real fights decides."""
    rows = melee_holds()
    held = [it.class_name for it in (getattr(fx, "item", None) for fx in f.items_fx)
            if it is not None and it.class_name in rows]
    phase, rng = f.skill.fight_phase, f.e.rng
    if not held or (phase is None and rng is None):
        return None
    cls = max(held, key=lambda c: rows[c]["fights"])
    q = rows[cls]["holds"]
    u = (phase + zlib.crc32(f"melee|{f.name}".encode()) / 2 ** 32) % 1.0 if phase is not None else rng.random()
    h = q[min(len(q) - 1, int(u * len(q)))]
    if h is None:
        return None
    # The opener moves the hero's own first melee earlier (the steady rate pays it back, Engine.melee_open); it must
    # not add melee a hero doesn't do. The holds are pooled over real holders, every hero of which melees at least
    # MELEE_OPEN_FULL_RATE with one melee item and opens about as often as the pool (validation/README.md "Close-range
    # items on far heroes"). Below that rate, outside the data, a hero opens with one in rate / MELEE_OPEN_FULL_RATE of the
    # fights: Vindicta (0.0094/s, she fights at ~26 m) opens in ~17% of fights, not the pool's ~65%.
    k = min(1.0, f.skill.melee_rate / MELEE_OPEN_FULL_RATE)
    if k < 1.0 and (u * len(q)) % 1.0 >= k:   # u's place inside its hold bin: uniform, independent of the bin
        return None
    return h, cls in HEAVY_OPENERS


def hold_first_casts(f):
    """Mechanics.cast_timing at the fight start: each unlocked ability with a real hold gets its first cast moved to
    now + a hold drawn from it (never in this fight for a None value). The hold is AbilityState.held_until, not its
    cooldown, so items that read cooldowns (Witchmail's cut, Refresher's reset) neither see a held ability as cooling
    nor release it. The prefight ability (Mo & Krill's Burrow,
    deadsim.patterns) keeps its own timing."""
    holds = cast_holds()
    phase = f.skill.fight_phase
    rng = f.e.rng
    if phase is None and rng is None:
        return
    pre = f.plan.prefight if f.plan is not None else None
    hid = f.st.hero.id
    for ab in f.abilities:
        if not ab.unlocked:
            continue
        q = holds.get(f"{hid}:{ab.ab.class_name}")
        if ab is pre:
            if not (q and getattr(f.e.mech, "burrow_prefight", False)):
                continue
            share = prefight_share(hid, f.st.souls)
            if share is None:
                continue
            if phase is not None:
                u = (phase + zlib.crc32(f"{ab.ab.class_name}|{f.name}".encode()) / 2 ** 32) % 1.0
            else:
                u = rng.random()
            if u < share:
                continue   # opens burrowed (patterns.fight_start)
            f.skip_prefight = True
            pos = [h for h in q if h is None or h >= 0]   # the negative holds are the burrowed starts
            h = pos[min(len(pos) - 1, int((u - share) / (1 - share) * len(pos)))]
            ab.held_until = f.e.t + (math.inf if h is None else h)
            ab.timed = True
            continue
        if not q:
            if f"{hid}:{ab.ab.class_name}" in GATE_READY and getattr(f.e.mech, "gate_ready", False):
                gate_ready(f, ab)
            continue
        if phase is not None:
            u = (phase + zlib.crc32(f"{ab.ab.class_name}|{f.name}".encode()) / 2 ** 32) % 1.0
        else:
            u = rng.random()
        if getattr(f.e.mech, "cdr_ready", False):
            u = cdr_ready_u(f, ab, u)
        if ab.ab.ultimate and getattr(f.e.mech, "ult_phase", False):
            u = ult_phase_u(f, ab, q, u)
        if ab.ab.class_name == GRAVES_WALL and getattr(f.e.mech, "graves_phase", False):
            u = share_u(q, u, _interp_ln(graves_phase()["wall_mult"], f.st.souls))
        u = lean_u(f, u)
        h = q[min(len(q) - 1, int(u * len(q)))]
        ab.held_until = f.e.t + (math.inf if h is None else max(0.0, h))
        ab.timed = True
        ab.precast_at = f.e.t + h if h is not None and h < 0 else None


# gated abilities that start a fight on cooldown past their real ready share (Mechanics.gate_ready). Apollo's ult: cast
# by 20 s in 92% of the audit duels -> 52% (real 38%). Yamato's Shadow Transformation: 1.00 -> 0.49 (real 0.45). Seven's,
# Grey Talon's and Mo & Krill's ults were tried and left out: their held-out audit got worse (validation/README.md
# "More gated ults on real readiness"). Venator's Ira Domini joined once its stakes were booked under the ult, not gun
# (validation/README.md "Venator's stakes and ult readiness")
GATE_READY = frozenset({"77:ability_fencer_ultimate", "27:citadel_ability_infinity_slash", "65:ability_priest_weaponswap"})


def gate_ready(f, ab):
    """Mechanics.gate_ready at the fight start: ab (no cast_timing hold, its own gate) is on cooldown for the whole
    fight past its real share of fights started ready (data/cdr_ready.json at 1 x the cooldown; cooldown items raise
    it as cdr_ready_u; an ult with a data/ult_phase.json row x its mult at the fighter's net worth, Mechanics.ult_phase).
    Draws like hold_first_casts."""
    phase, rng = f.skill.fight_phase, f.e.rng
    if phase is not None:
        u = (phase + zlib.crc32(f"{ab.ab.class_name}|{f.name}".encode()) / 2 ** 32) % 1.0
    else:
        u = rng.random()
    if getattr(f.e.mech, "cdr_ready", False):
        u = cdr_ready_u(f, ab, u)
    d = cdr_ready_rows()
    key = f"{f.st.hero.id}:{ab.ab.class_name}"
    c = d["sources"].get(key) or d["pooled"]["ult" if ab.ab.ultimate else "ability"]
    share = c[-1]
    if ab.ab.ultimate and getattr(f.e.mech, "ult_phase", False):
        # a gated ult with an ult_phase row (Apollo's, matched by ult_rate_match.py): its ready share by net worth
        share = min(ULT_PHASE_CAP, share * ult_phase_mult(key, f.st.souls))
    if u >= share:
        ab.held_until = math.inf


_CDR = None


def cdr_ready_rows():
    """data/cdr_ready.json: {"k_grid", "rho": {"ability"|"ult": {"rho"...}}, "pooled": {..: curve}, "sources":
    {"hero id:ability class": curve}}, curve = real share of fights started ready at k x the cooldown."""
    global _CDR
    if _CDR is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "cdr_ready.json")) as fh:
            _CDR = json.load(fh)
    return _CDR


def item_cd_keep(f, ab):
    """The share of ab's cooldown the fighter's items leave (1 = no item cooldown reduction): cooldown items, ult
    cooldown items and a Compress Cooldown imbue (AbilityState.cooldown's item terms)."""
    reds = [f.st.cdr] + ([f.st.ult_cdr] if ab.ab.ultimate else [])
    reds += [it.p("CooldownReduction") / 100 for it in ab.imbues if it.class_name == "upgrade_magic_tempo"]
    keep = 1.0
    for r in reds:
        keep *= 1.0 - max(0.0, min(0.95, r))
    return keep


def cdr_ready_u(f, ab, u):
    """Mechanics.cdr_ready: the hold quantile u for a build whose items leave k of ab's cooldown. The real ready
    share r(1) becomes r(1) + rho x (r(k) - r(1)); the holds below the real ready share stretch over the new one,
    the rest shrink into what is left."""
    keep = item_cd_keep(f, ab)
    if keep >= 0.999 or ab.max_charges() > 1:
        return u
    d = cdr_ready_rows()
    tag = "ult" if ab.ab.ultimate else "ability"
    c = d["sources"].get(f"{f.st.hero.id}:{ab.ab.class_name}") or d["pooled"][tag]
    ks = d["k_grid"]
    k = max(ks[0], keep)
    j = min(len(ks) - 2, bisect.bisect_right(ks, k) - 1)
    rk = c[j] + (c[j + 1] - c[j]) * (k - ks[j]) / (ks[j + 1] - ks[j])
    r1 = c[-1]
    r = min(0.999, r1 + max(0.0, d["rho"][tag]["rho"] * (rk - r1)))
    if r <= r1 or r1 <= 0.0:
        return u
    return u * r1 / r if u < r else r1 + (u - r) * (1.0 - r1) / (1.0 - r)


_LEAN = None


def lean_center(hero_id):
    """Mechanics.ability_lean: the hero's mean spirit item souls over its real first-cast chances (data/ability_lean.json),
    the pooled mean for a hero without one, None without the file."""
    global _LEAN
    if _LEAN is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "data", "ability_lean.json")
        _LEAN = {}
        if os.path.exists(fn):
            with open(fn) as fh:
                _LEAN = json.load(fh)["center"]
    if not _LEAN:
        return None
    c = _LEAN.get(str(hero_id))
    return c if c is not None else sum(_LEAN.values()) / len(_LEAN)


def lean_u(f, u):
    """Mechanics.ability_lean: a hold / wait quantile u at the fighter's cast hazard ratio (proportional hazards on the
    real curve: P(by t) = 1 - (1 - P(t)) ^ hr)."""
    hr = f.cast_hazard
    if hr == 1.0:
        return u
    return 1.0 - (1.0 - u) ** (1.0 / hr)


_RECAST = None


def recast_rows():
    """data/recast_timing.json: {"sources": {"hero id:ability class": QBINS waits}, "pooled": QBINS, "skip": [keys]}."""
    global _RECAST
    if _RECAST is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "recast_timing.json")) as fh:
            _RECAST = json.load(fh)
        _RECAST["skip"] = set(_RECAST.get("skip", ()))
    return _RECAST


_CHARGE_GAPS = None


def charge_gap(ab, phase, rng):
    """Mechanics.charge_gaps: the gap (s) from a cast of a charged ability to its next, drawn from the real gaps
    under 20 s (data/charge_gaps.json), or None without a row."""
    global _CHARGE_GAPS
    if _CHARGE_GAPS is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "data", "charge_gaps.json")
        _CHARGE_GAPS = {}
        if os.path.exists(fn):
            with open(fn) as fh:
                _CHARGE_GAPS = {k: v["q"] for k, v in json.load(fh)["sources"].items()}
    f = ab.f
    q = _CHARGE_GAPS.get(f"{f.st.hero.id}:{ab.ab.class_name}")
    if not q:
        return None
    if phase is not None:
        u = (phase + zlib.crc32(f"charge|{ab.ab.class_name}|{f.name}|{ab.casts}".encode()) / 2 ** 32) % 1.0
    else:
        u = rng.random()
    return q[min(len(q) - 1, int(u * len(q)))]


def recast_wait(ab, cls=None, n=None, finite=False):
    """Mechanics.recast_timing, at a cast: the wait (s) past the cooldown before the next cast of ab, drawn from the
    real recast curve (inf: not again this fight), 0 for charged abilities, ultimates, abilities whose sim timing is
    its own (skip) and fights without a phase or rng. cls: the ability class cast from ab's slot when it isn't ab's
    own (Silver's wolf abilities), n its cast count (default ab.casts). finite: only the waits of the casts that
    came (a reset: the curve's not-again share is mostly fights ending, which the sim's fight length already does)."""
    f = ab.f
    phase, rng = f.skill.fight_phase, f.e.rng
    if phase is None and rng is None:
        return 0.0
    if ab.max_charges() > 1 and getattr(f.e.mech, "charge_gaps", False):
        gap = charge_gap(ab, phase, rng)
        if gap is not None:
            return max(0.0, gap - ab.charge_delay())
    if ab.max_charges() > 1 or ab.ab.ultimate:
        return 0.0
    rows = recast_rows()
    cls = cls or ab.ab.class_name
    key = f"{f.st.hero.id}:{cls}"
    if key in rows["skip"]:
        return 0.0
    q = rows["sources"].get(key) or rows["pooled"]
    if phase is not None:
        u = (phase + zlib.crc32(f"recast|{cls}|{f.name}|{ab.casts if n is None else n}".encode()) / 2 ** 32) % 1.0
    else:
        u = rng.random()
    u = lean_u(f, u)
    if finite:
        q = [h for h in q if h is not None] or [0.0]
    h = q[min(len(q) - 1, int(u * len(q)))]
    return math.inf if h is None else max(0.0, h)


_ENTRY = None


def entry_deficits(souls):
    """Real entry health deficits (share of max health, ENTRY quantiles) at net worth souls."""
    global _ENTRY
    if _ENTRY is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "sustain.json")) as fh:
            _ENTRY = json.load(fh)["entry_deficit_q"]
    ph = next((n for hi, n in LENGTH_PHASES if souls < hi), "late")
    return _ENTRY[ph]


def entry_deficit(f):
    """A deficit (share of max health) drawn from the real entry health spread for f's net worth, for a fighter at
    full health whose start wasn't set (f.entry_set); None when there is none to draw (no phase, no rng)."""
    if f.entry_set or f.hp < f.max_hp:
        return None
    phase = f.skill.fight_phase
    rng = f.e.rng
    if phase is None and rng is None:
        return None
    q = entry_deficits(f.st.souls)
    if phase is not None:
        u = (phase + zlib.crc32(f"entry_hp|{f.name}".encode()) / 2 ** 32) % 1.0
    else:
        u = rng.random()
    return q[min(len(q) - 1, int(u * len(q)))]


def entry_health(f):
    """Mechanics.entry_hp at the fight start: the fighter starts short by entry_deficit."""
    d = entry_deficit(f)
    if d is not None:
        f.hp = max(1.0, f.max_hp * (1.0 - d))


# abilities that cast or scale on the target's health (Fighter.gate_hp)
EXECUTE_GATES = {"citadel_ability_shiv_killing_blow", "citadel_ability_hornet_snipe", "ability_deadpack_ultimate",
                 "ability_viper_venom"}


# abilities that cast or scale on their caster's own health (Fighter.gate_hp, Mechanics.gate_assist)
SELF_GATES = {"ability_health_swap"}


def entry_gate(f):
    """Mechanics.entry_gate at the fight start: the fighter's health stays, execute gates see it short by
    entry_deficit (Fighter.gate_hp). Drawn only against an enemy with one, so other fights stay as they were."""
    if f.enemy is None or not any(ab.ab.class_name in EXECUTE_GATES and ab.unlocked for ab in f.enemy.abilities):
        return
    d = entry_deficit(f)
    f.entry_gap = d or 0.0
    f.entry_drawn = True


# items conditioned on the target's health (Fighter.item_hp_frac, Mechanics.target_health)
# Tankbuster and Decay deal damage from the target's current health (Fighter.item_hp): real hits land on targets at
# 0.59 / 0.63 of their health, the sim's duels at 0.71 / 0.74 (scripts/fight_length/target_health.py items)
TARGET_HEALTH_ITEMS = {"upgrade_pristine_emblem", "upgrade_magic_shock", "upgrade_rupture"}
# third parties' damage per damage the target takes in the duel, as such items see it: fitted so the duels' gun
# damage above half target health matches real (scripts/fight_length/target_health.py fit). The raw real ratio in
# pair fights is 0.71, but a real target losing health that fast also dies or backs off sooner
TARGET_ASSIST = 0.35
# the same for the damage of current-health items (Fighter.item_hp): fitted so their hits' mean target health share
# matches real (target_health.py items: Tankbuster 0.59 / 0.59 per half, real 0.59 / 0.59; Decay 0.65 / 0.65, real
# 0.64 / 0.62). Opening Rounds' 0.35 piles Tankbuster hits on near-empty targets (mean 0.53)
CURRENT_HEALTH_ASSIST = 0.15
TARGET_HEALTH_ALL = False   # target_health.py: every fighter gets the draw (to measure all gun damage)


def target_health(f):
    """Mechanics.target_health at the fight start (after entry_gate): against an enemy holding a TARGET_HEALTH_ITEMS
    item, f's health as those items see it is short by a real entry deficit and TARGET_ASSIST x its damage taken."""
    e = f.enemy
    held = e is not None and any(getattr(getattr(fx, "item", None), "class_name", None) in TARGET_HEALTH_ITEMS
                                 for fx in e.items_fx)
    if e is None or not (held or TARGET_HEALTH_ALL):
        return
    f.item_assist = TARGET_ASSIST
    if not f.entry_drawn:
        f.entry_gap = entry_deficit(f) or 0.0
        f.entry_drawn = True
    f.item_gap = f.entry_gap


EXEC_ROW = "all"   # data/execute_timing.json row (the split-half check uses "even" / "odd")
_EXEC = None


def execute_timing_data():
    global _EXEC
    if _EXEC is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "execute_timing.json")) as fh:
            _EXEC = json.load(fh)
    return _EXEC[EXEC_ROW]


def gate_assist(f):
    """Mechanics.gate_assist at the fight start: the holder of a self gate (Soul Exchange's Geist) sees its health
    short by a real entry deficit (entry_deficit, as entry_gate) and by the real third parties' damage per damage it
    takes in the duel (Fighter.gate_assist)."""
    a = execute_timing_data()["assist"]
    own = [a.get(ab.ab.class_name, 0.0) for ab in f.abilities if ab.unlocked and ab.ab.class_name in SELF_GATES]
    if not own:
        return
    f.gate_assist = max(own)
    if not f.entry_gap:
        f.entry_gap = entry_deficit(f) or 0.0
        f.entry_drawn = True


def execute_plans(f):
    """Mechanics.execute_timing, after hold_first_casts: abilities with a drawn first cast plan (impl.draw_plan:
    Killing Blow, Soul Exchange) get a draw like cast_timing's (phase or rng; deterministic fights skip)."""
    phase, rng = f.skill.fight_phase, f.e.rng
    if phase is None and rng is None:
        return
    for ab in f.abilities:
        draw = getattr(ab.impl, "draw_plan", None)
        if not ab.unlocked or draw is None or not getattr(ab.impl, "plans", True):
            continue   # plans False: an opt-in plan turned off draws nothing (the rng stream stays as without it)
        if phase is not None:
            u = (phase + zlib.crc32(f"plan|{ab.ab.class_name}|{f.name}".encode()) / 2 ** 32) % 1.0
        else:
            u = rng.random()
        draw(ab.ctx, u)


def precast(f):
    """Mechanics.cast_timing, after both fighters' fight start: an ability drawn with a negative hold (its real damage
    lands at the fight's first hit or within PRE_S of it, but the sim's cast takes longer to land: a Kinetic Carbine
    charge, a Sticky Bomb fuse, a Concussive Combustion wind-up) is cast that long before t = 0, so its charge-up and
    gun lock fall before the fight and its hit opens it, as in the real fights the hold comes from
    (scripts/cast_timing/fit_cast_timing.py, due times). The cast's own rule still decides (try_cast); one it turns
    down waits for the first chance in the fight."""
    t0 = f.e.t
    # earliest first: a later precast's cast lock must not turn down one that went out before it
    for ab in sorted((a for a in f.abilities if getattr(a, "precast_at", None) is not None),
                     key=lambda a: a.precast_at):
        at = ab.precast_at
        ab.precast_at = None
        if ab.ready_at > t0:
            continue   # on cooldown at the start (spent before the fight): nothing to precast
        ready, held, lock = ab.ready_at, ab.held_until, f.gun_locked_until
        ab.ready_at = ab.held_until = at   # ready then, not only from t = 0
        if lock <= t0:
            f.gun_locked_until = min(lock, at)   # free then too (a cast gated on "not busy")
        f.e.t = at
        try:
            cast = ab.try_cast()
        finally:
            f.e.t = t0
        if not cast:
            ab.ready_at, ab.held_until = ready, held
            if f.gun_locked_until == min(lock, at):
                f.gun_locked_until = lock


DEFAULT = Mechanics()   # None turns the new mechanics off for every Engine built without an explicit value

RICOCHET_RADIUS = 13.0   # m: Ricochet's bounce radius, the reach used for a duel's extra_targets
_NEAR = None


_AREA = None
_AREA_PHASE = None
_ABIL_AREA = None


def ability_area_mult(cls, souls):
    """Mechanics.ability_area_phase: rel(souls) / pooled rel for an area ability (class name) with a
    row in data/ability_area_phase.json, linear in ln net worth between its bins' mean net worths, flat outside;
    1.0 without a row."""
    global _ABIL_AREA
    if _ABIL_AREA is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "data", "ability_area_phase.json")
        _ABIL_AREA = {}
        if os.path.exists(fn):
            with open(fn) as fh:
                for k, v in json.load(fh)["abilities"].items():
                    _ABIL_AREA[k] = (v["pooled"], [(math.log(b["net_worth"]), b["rel"]) for b in v["bins"]])
    row = _ABIL_AREA.get(cls)
    if row is None or not souls:
        return 1.0
    base, pts = row
    x = math.log(max(souls, 1.0))
    if x <= pts[0][0]:
        return pts[0][1] / base
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1:
            return (y0 + (y1 - y0) * (x - x0) / max(1e-9, x1 - x0)) / base
    return pts[-1][1] / base


_BALLISTIC = None


def ballistic_stacks(cls):
    """Mechanics.ballistic_stacks: real unique heroes an ability (class name) damaged in the last 20 s at its user's
    gun hits, given at least one (data/ballistic_stacks.json); 1.0 without a row."""
    global _BALLISTIC
    if _BALLISTIC is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "data", "ballistic_stacks.json")
        _BALLISTIC = {}
        if os.path.exists(fn):
            with open(fn) as fh:
                _BALLISTIC = {k: v["stacks"] for k, v in json.load(fh)["abilities"].items()}
    return max(1.0, _BALLISTIC.get(cls, 1.0))


_ULT_PHASE = None


def ult_phase_mult(key, souls):
    """Mechanics.ult_phase: multiplier on the ult hold's cast share ("hero id:class") at net worth souls
    (data/ult_phase.json), linear in ln net worth between its points, flat outside; 1.0 without data."""
    global _ULT_PHASE
    if _ULT_PHASE is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "data", "ult_phase.json")
        _ULT_PHASE = {}
        if os.path.exists(fn):
            with open(fn) as fh:
                for k, v in json.load(fh)["sources"].items():
                    _ULT_PHASE[k] = [(math.log(nw), m) for nw, m in v["points"]]
    return _interp_ln(_ULT_PHASE.get(key), souls)


def _interp_ln(pts, souls):
    if not pts or not souls:
        return 1.0
    x = math.log(max(souls, 1.0))
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / max(1e-9, x1 - x0)
    return pts[-1][1]


ULT_PHASE_CAP = 0.98


def ult_phase_u(f, ab, q, u):
    """The hold quantile u with the hold's cast share c (its non-None values) at c x ult_phase_mult: holds in the cast
    part keep their order and stretch over the new share, the not-cast part shrinks into what is left."""
    return share_u(q, u, ult_phase_mult(f"{f.st.hero.id}:{ab.ab.class_name}", f.st.souls))


GRAVES_WALL = "ability_necro_zombiewall"
_TAG = None


def tag_along_windows(f, name, horizon=60.0):
    """Mechanics.tag_along: [(start s, length s)] of the duel's Tag Along windows (Rem on an ally), a stationary
    alternating draw whose attached share is data/tag_along.json's at f's net worth; [] for deterministic fights or with
    the mechanic off."""
    global _TAG
    if not (f.e.mech is not None and getattr(f.e.mech, "tag_along", False) and getattr(f.e, "length", False)):
        return []
    phase, rng = f.skill.fight_phase, f.e.rng
    if phase is None and rng is None:
        return []
    if _TAG is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "tag_along.json")) as fh:
            d = json.load(fh)
        _TAG = ([(math.log(nw), x) for nw, x in d["points"]], d["lengths"])
    pts, lens = _TAG
    p = min(0.9, max(0.0, _interp_ln(pts, f.st.souls)))
    if p <= 0:
        return []
    import random
    seed = (phase + zlib.crc32(f"{name}|{f.name}".encode()) / 2 ** 32) % 1.0 if phase is not None else rng.random()
    r = random.Random(int(seed * 2 ** 32))
    mean_len = sum(lens) / len(lens)
    gap = mean_len * (1 - p) / p   # mean free gap: attached share p
    out, t = [], 0.0
    if r.random() < p:   # attached at the fight start: the rest of a window, drawn length-biased
        u, acc = r.random() * sum(lens), 0.0
        n = next((x for x in lens if (acc := acc + x) >= u), lens[-1]) * r.random()
        out.append((0.0, n))
        t = n
    while True:
        t += r.expovariate(1.0 / gap)
        if t >= horizon:
            return out
        n = lens[min(len(lens) - 1, int(r.random() * len(lens)))]
        out.append((t, n))
        t += n


_PULSE = None


def pulse_survival(f):
    """Mechanics.pulse_hits: [P(the main victim takes more than i pulses)] of a landed Pulse Grenade at f's net worth
    (data/pulse_hits.json), None with the mechanic off."""
    global _PULSE
    if f.e.mech is None or not getattr(f.e.mech, "pulse_hits", False):
        return None
    if _PULSE is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "pulse_hits.json")) as fh:
            pts = json.load(fh)["points"]
        _PULSE = [[(math.log(nw), s[i]) for nw, s in pts] for i in range(len(pts[0][1]))]
    return [_interp_ln(p, f.st.souls) for p in _PULSE]


_GRAVES = None


def graves_phase():
    """data/graves_phase.json as {"jar_throws": [(ln nw, [p0, p1, p2, p3])], "wall_mult": [(ln nw, mult)]}."""
    global _GRAVES
    if _GRAVES is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "graves_phase.json")) as fh:
            d = json.load(fh)
        _GRAVES = {"jar_throws": [(math.log(nw), p) for nw, p in d["jar_throws"]],
                   "wall_mult": [(math.log(nw), m) for nw, m in d["wall_mult"]]}
    return _GRAVES


def jar_throws(f, name):
    """Mechanics.graves_phase: the jars Graves throws this fight, drawn from the real share at his net worth (phase
    draw or rng, as hold_first_casts); None for deterministic fights or with the mechanic off."""
    if not (f.e.mech is not None and getattr(f.e.mech, "graves_phase", False) and getattr(f.e, "length", False)):
        return None
    phase, rng = f.skill.fight_phase, f.e.rng
    if phase is None and rng is None:
        return None
    u = (phase + zlib.crc32(f"{name}|{f.name}".encode()) / 2 ** 32) % 1.0 if phase is not None else rng.random()
    pts = graves_phase()["jar_throws"]
    x = math.log(max(f.st.souls or 1.0, 1.0))
    if x <= pts[0][0]:
        ps = pts[0][1]
    elif x >= pts[-1][0]:
        ps = pts[-1][1]
    else:
        (x0, p0), (x1, p1) = next((a, b) for a, b in zip(pts, pts[1:]) if x <= b[0])
        w = (x - x0) / max(1e-9, x1 - x0)
        ps = [a + (b - a) * w for a, b in zip(p0, p1)]
    acc = 0.0
    for k, p in enumerate(ps):
        acc += p / sum(ps)
        if u < acc:
            return k
    return len(ps) - 1


def share_u(q, u, m):
    """The hold quantile u with the hold's cast share c (its non-None values) at min(CAP, c x m)."""
    c = sum(h is not None for h in q) / len(q)
    if abs(m - 1.0) < 1e-6 or c <= 0.0 or c >= 1.0:
        return u
    c2 = min(ULT_PHASE_CAP, c * m)
    return u * c / c2 if u < c2 else c + (u - c2) * (1.0 - c) / (1.0 - c2)


_MELEE_PHASE = None


def melee_phase_mult(hero_id, souls):
    """Mechanics.melee_phase: multiplier on the hero's melee rate at net worth souls (data/melee_phase.json, the
    hero's row or pooled), linear in ln net worth between its points, flat outside; 1.0 without data."""
    global _MELEE_PHASE
    if _MELEE_PHASE is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "data", "melee_phase.json")
        _MELEE_PHASE = {}
        if os.path.exists(fn):
            with open(fn) as fh:
                for k, v in json.load(fh)["heroes"].items():
                    _MELEE_PHASE[k] = [(math.log(nw), m) for nw, m in v["points"]]
    return _interp_ln(_MELEE_PHASE.get(str(hero_id)), souls)


def area_extra(name, souls=None):
    """Extra hits on other heroes per hit on the main target for an area item, from Phantom+ replay damage events
    (data/area_hits.json, scripts/team/area_hits.py), or None when the item has no fit. A duel's damage of the item
    x this is what it also deals to the other enemies in a real fight. With souls: at that net worth (early fights
    are lane trades, late ones team fights; one replay-fitted curve for every area item, linear in ln net worth
    between its bins, flat outside); without: pooled over whole matches."""
    global _AREA, _AREA_PHASE
    if _AREA is None:
        fn = os.path.join(os.path.dirname(__file__), "..", "data", "area_hits.json")
        _AREA = {}
        if os.path.exists(fn):
            with open(fn) as fh:
                a = json.load(fh)
            _AREA = {k: v["extra_per_main"] for k, v in a["items"].items()}
            _AREA_PHASE = a.get("phase")
    x = _AREA.get(name)
    if x is None or souls is None or not _AREA_PHASE:
        return x
    pts = [(math.log(b["net_worth"]), b["fit"]) for b in _AREA_PHASE["bins"]]
    v = math.log(max(souls, 1.0))
    if v <= pts[0][0]:
        return x * max(0.0, pts[0][1])
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if v <= x1:
            return x * max(0.0, y0 + (y1 - y0) * (v - x0) / (x1 - x0))
    return x * pts[-1][1]


def real_nearby(kind, radius, souls):
    """Real mean count in a Phantom+ fight second (data/team_value.json positions, scripts/team/fit_team.py): kind
    "extra" = other enemies within radius m of the target, "extra_self" = of the holder, "allies" = teammates within
    radius m, "any_ally" = share of seconds with a teammate within radius m. Linear in the radius, log-linear in net
    worth between budget bins. real_nearby("extra", RICOCHET_RADIUS, souls) is a duel's Mechanics.extra_targets."""
    global _NEAR
    if _NEAR is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "team_value.json")) as fh:
            _NEAR = json.load(fh)["positions"]
    pos = _NEAR
    radii = pos["radii_m"]

    def at(row):
        tab = row[kind]
        r = max(radii[0], min(radii[-1], radius))
        hi = next(x for x in radii if x >= r)
        lo = max(x for x in radii if x <= r)
        if hi == lo:
            return tab[str(lo)]
        return tab[str(lo)] + (tab[str(hi)] - tab[str(lo)]) * (r - lo) / (hi - lo)

    bins = sorted(int(b) for b in pos["budgets"] if b != "all")
    s = max(bins[0], min(bins[-1], souls))
    hi = next(b for b in bins if b >= s)
    lo = max(b for b in bins if b <= s)
    if hi == lo:
        return at(pos["budgets"][str(lo)])
    w = math.log(s / lo) / math.log(hi / lo)
    return at(pos["budgets"][str(lo)]) * (1 - w) + at(pos["budgets"][str(hi)]) * w



_RAW = None


def raw_props(class_name):
    """Properties of any entry in raw/items.json (parry etc. are not shop items), as floats where possible."""
    global _RAW
    if _RAW is None:
        with open(os.path.join(GAME, "raw", "items.json")) as f:
            _RAW = {x.get("class_name"): x for x in json.load(f)}
    out = {}
    for k, v in ((_RAW.get(class_name) or {}).get("properties") or {}).items():
        v = v.get("value") if isinstance(v, dict) else v
        try:
            out[k] = float(str(v).rstrip("msx%"))
        except (TypeError, ValueError):
            pass
    return out


def _debuff(target, key, value, duration, tag):
    dur = duration * max(0.0, 1.0 - target.status_resist())
    if dur <= 0:
        return
    target.mods.add(key, value, dur, tag)
    target.mark_debuff(key, tag)
    if key in CC_KEYS:
        for fx in target.items_fx:
            g = getattr(fx, "on_cc", None)
            if g:
                g(target, key)


def nearby_enemies(f):
    """Expected other enemy heroes near f's target: Mechanics.extra_targets in a duel, the living ones in a team fight."""
    g = getattr(f.e, "nearby_enemies", None)
    return g(f) if g is not None else f.e.mech.extra_targets


def _splash(f, amount, kind, source):
    """Damage to other enemy heroes near the target, mitigated like a hit on the target (its resists stand in for
    theirs), booked in f.counters["splash"]."""
    if amount <= 0:
        return 0.0
    team_splash = getattr(f.e, "team_splash", None)
    if team_splash is not None:          # team fight: the other enemies are real fighters
        return team_splash(f, amount, kind, source)
    e = f.enemy
    amt = amount * f.st.outgoing_mult * (1.0 + f.stat("damage_amp"))
    if kind == "bullet":
        amt *= 1.0 - combine_resist(e.st.bullet_resist, f.st.bullet_shred)
    elif kind == "spirit":
        amt *= 1.0 - combine_resist(e.st.spirit_resist, f.st.spirit_shred)
    d = f.counters.setdefault("splash", {})
    d[source] = d.get(source, 0.0) + amt
    d = f.counters.setdefault("splash_exp", {})
    d[source] = d.get(source, 0.0) + amt * f.e.length_w(src=f, source=source)
    return amt


# ---------------------------------------------------------------------------------------------------------------
# Parry
# ---------------------------------------------------------------------------------------------------------------
def parry_check(eng, att, dfd, raw, w):
    """Called for every rotation heavy melee. Returns the share of `raw` that lands (0 if parried)."""
    if not dfd.alive or dfd.mods.active("stun") or dfd.skill.parry_rate <= 0:
        return 1.0
    p = dfd.skill.parry_rate * dfd.counters.get("parry_mult", 1.0)
    k = dfd.acc("parry").take(min(1.0, p) * min(1.0, w))
    if k:
        parried(eng, att, dfd, raw / max(w, 1e-9))
    if w >= 1.0:
        return 0.0 if k else 1.0
    return 1.0 - min(1.0, p)


def parried(eng, att, dfd, full):
    pp = raw_props("citadel_ability_melee_parry")
    d = pp.get("ParriedStunTime", 2.75)
    _debuff(att, "stun", 1, d, ("parry", "stun"))
    _debuff(att, "damage_taken_amp", pp.get("VictimDamageTakenScale", 25) / 100, d, ("parry", "amp"))
    dfd.counters["parries"] = dfd.counters.get("parries", 0) + 1
    eng.note(f"{dfd.name} parries {att.name}")
    for fx in dfd.items_fx:
        g = getattr(fx, "on_parry", None)
        if g:
            g(dfd, att, full)


# ---------------------------------------------------------------------------------------------------------------
# Spell parry (Counterspell)
# ---------------------------------------------------------------------------------------------------------------
def spell_blocked(eng, src, dst, ability=None):
    """True if dst's open spell-parry window blocks this ability / item hit from src."""
    sp = dst.counters.get("spell_parry")
    if not sp:
        return False
    t = eng.t
    until, ab, ab_until, fx = sp
    if t <= until or (ability is not None and ability is ab and t <= ab_until):
        fx.success(dst)
        return True
    if t > max(until, ab_until):
        dst.counters.pop("spell_parry", None)
    return False


# ---------------------------------------------------------------------------------------------------------------
# Summons
# ---------------------------------------------------------------------------------------------------------------
_TARGETING = None


def summon_targeting():
    """{kind: {"focus": share of trigger pulls, "acc_mult": accuracy vs on a hero}} from data/summon_targeting.json."""
    global _TARGETING
    if _TARGETING is None:
        with open(os.path.join(os.path.dirname(__file__), "..", "data", "summon_targeting.json")) as fh:
            _TARGETING = json.load(fh)["kinds"]
    return _TARGETING


class Summon:
    def __init__(self, owner, name, hp, spirit_resist=0.0, bullet_resist=0.0, until=math.inf, kind="turret",
                 on_death=None):
        self.owner, self.name, self.hp = owner, name, hp
        self.bullet_resist, self.spirit_resist = bullet_resist, spirit_resist
        self.until = until
        self.kind = kind
        t = summon_targeting().get(kind, {})
        self.focus, self.acc_mult, self.splash = t.get("focus", 0.0), t.get("acc_mult", 1.0), t.get("splash", 0.0)
        self.on_death = on_death
        self.weight = 1.0   # expected share of fights it is still standing in (see _break)
        self.alive = True

    def hurt(self, amount, kind="bullet"):
        res = self.bullet_resist if kind == "bullet" else self.spirit_resist if kind == "spirit" else 0.0
        amt = min(self.hp, amount * (1.0 - res))
        self.hp -= amt
        if self.hp <= 0:
            self.alive = False
            self.owner.e.note(f"{self.name} of {self.owner.name} destroyed")
            if self.on_death:
                self.on_death()
        return amt


def add_summon(owner, name, hp, spirit_resist=0.0, bullet_resist=0.0, life=math.inf, delay=0.0, kind="turret",
               on_death=None):
    """A summon the enemy can shoot, or None if summons are off. Give it to Engine.dot as guard= so its damage
    stops when it dies. kind picks its row in data/summon_targeting.json; on_death runs if it is killed. Its life
    is capped at the row's life_other_s: the median real life of summons no enemy hero killed (troopers, other
    heroes, left behind), which a 1v1 doesn't have."""
    m = owner.e.mech
    if m is None or not m.summons:
        return None
    life = min(life, summon_targeting().get(kind, {}).get("life_other_s", math.inf))
    s = Summon(owner, name, hp, spirit_resist, bullet_resist, owner.e.t + delay + life, kind, on_death)
    owner.counters.setdefault("summons", []).append(s)
    row = summon_targeting().get(kind, {})
    if row.get("break_p"):
        owner.e.after(delay + row["break_s"], _break, s, row["break_p"])
    return s


def _break(s, p):
    """The enemy walks up and breaks summon s (melee) with probability p: Graves' gravestone, which bullets can't hurt.
    One break per fight can't be drawn as a deterministic Bernoulli (Accum would always fire for p >= 0.5), so it is
    an expected value: s.weight drops to 1 - p, and whatever the summon still does is scaled by it (necro.py: the
    aura and the damage of zombies spawned after it). FightResult.*_summons_out counts only real deaths, not breaks."""
    f = s.owner.enemy
    if f is not None and f.alive and alive(s) and s.alive:
        d = f.counters.setdefault("summon_dmg", {})   # not in summon_dmg_kind: that is the gun / splash fit
        d[s.name] = d.get(s.name, 0.0) + s.hp * p
        s.weight *= 1.0 - p


def alive(s):
    """True for a summon still standing (or no summon: summons off)."""
    return s is None or (s.alive and s.until > s.owner.e.t)


def live_summons(f):
    """The first (oldest) living summon of each kind f has out, in spawn order: the one the enemy shoots."""
    t = f.e.t
    out, seen = [], set()
    for s in f.counters.get("summons", ()):
        if s.alive and s.until > t and s.kind not in seen:
            seen.add(s.kind)
            out.append(s)
    return out


def live_summon(f):
    s = live_summons(f)
    return s[0] if s else None


def pick_summon(f, e):
    """The enemy summon f spends this trigger pull on, or None (shoot the hero)."""
    for s in live_summons(e):
        if s.bullet_resist >= 1.0:   # bullets can't hurt it (Graves' gravestone)
            continue
        focus = s.focus if f.skill.summon_focus is None else f.skill.summon_focus
        if focus > 0 and f.acc("summon_focus:" + s.kind).take(focus):
            return s
    return None


def note_hit_while_summoned(src, dst, amount, source):
    """dst took amount of hero damage while it has summons out. Books it per kind as [gun, other] (the fit compares
    it with damage to the summons) and splashes non-gun damage (area abilities, items, melee) onto every living
    summon: amount x its kind's splash share (fitted to replays against the damage all of a kind's summons take,
    see data/summon_targeting.json). Gun pulls go to one summon at a time (pick_summon: the oldest of each kind)."""
    d = dst.counters.setdefault("hit_while_summon", {})
    gun = source == "gun"
    for s in live_summons(dst):
        row = d.setdefault(s.kind, [0.0, 0.0])
        row[0 if gun else 1] += amount
    if gun:
        return
    t = dst.e.t
    for s in list(dst.counters.get("summons", ())):
        if s.alive and s.until > t and s.splash > 0:
            _book(src, s, s.hurt(amount * s.splash, "pure"), 1)


def _book(f, s, amt, i):
    d = f.counters.setdefault("summon_dmg", {})
    d[s.name] = d.get(s.name, 0.0) + amt
    k = f.counters.setdefault("summon_dmg_kind", {}).setdefault(s.kind, [0.0, 0.0])
    k[i] += amt


def shoot_summon(eng, f, s, n_bullets):
    """f spends this trigger pull on enemy summon s. Returns True (the pull is used)."""
    # out of the gun's range (Graves' tether) the pull misses, as in Engine.fire: bullet_damage is the in-range hit
    hits = f.acc("summon_hit").take(min(1.0, min(SUMMON_ACC_MAX, f.skill.accuracy * s.acc_mult) * eng.hit_reach(f.st)),
                                      n_bullets)
    if hits:
        per, _ = eng.bullet_damage(f)
        _book(f, s, s.hurt(per * hits, "bullet"), 0)
    return True


# ---------------------------------------------------------------------------------------------------------------
# Movement
# ---------------------------------------------------------------------------------------------------------------
SLOW_PROPS = ("SlowPercent", "MovementSlowPct", "MoveSlowPercent", "MovementSlow", "MoveSpeedSlowPct",
              "MoveSpeedAndDashSlowPct", "MovementSpeedSlow")
SLOW_DUR_PROPS = ("SlowDuration", "MovementSlowDuration", "DebuffDuration", "AbilityDuration")


def after_cast(state):
    """Hook from AbilityState.cast: generic ability slow on the enemy (movement mode)."""
    f = state.f
    m = f.e.mech
    if not m.movement or state.impl.kind in ("self", "passive"):
        return
    c = state.ctx
    pct = next((c.raw(p) for p in SLOW_PROPS if c.raw(p)), 0.0)
    if pct <= 0 or f.enemy is None:
        return
    dur = next((c.dur(p) for p in SLOW_DUR_PROPS if c.raw(p)), 2.0)
    land = f.skill.spirit_accuracy if state.impl.kind == "skillshot" else 1.0
    delay = c.raw("AbilityCastDelay")
    e = f.enemy
    f.e.after(delay, lambda: e.alive and _debuff(e, "move_slow", min(0.9, pct / 100) * land, dur,
                                                 ("ab_slow", state.ab.class_name)))


class Mover:
    """Distance control, escape and chase. Ticks every DT seconds."""
    DT = 0.1

    def __init__(self, eng):
        self.e = eng
        self.start = eng.distance
        for f in eng.fighters:
            b = f.st.hero.base
            x = f.st.extra
            f.counters["stamina"] = b.get("stamina", 3) + x.get("MODIFIER_VALUE_STAMINA", 0)
            f.counters["stamina_max"] = f.counters["stamina"]
            f.counters["stamina_regen"] = b.get("stamina_regen_per_second", 0.222) * (
                1 + x.get("MODIFIER_VALUE_STAMINA_REGEN_PER_SECOND_PERCENTAGE", 0) / 100)
            f.counters["dash_until"] = -1.0
        eng.after(self.DT, self.tick)

    # -- speeds --------------------------------------------------------------------------------------------
    def speed(self, f):
        if not f.alive or f.mods.active("immobilize"):
            return 0.0
        eth = None
        if f.mods.active("stun"):
            eth = f.mods.get("stun", "ethereal")
            if eth is None:
                return 0.0
        b = f.st.hero.base
        v = b.get("max_move_speed", 7.0) + f.st.extra.get("MODIFIER_VALUE_MOVEMENT_SPEED_MAX", 0) + f.stat("move_speed")
        for fx in f.items_fx:
            g = getattr(fx, "move_speed", None)
            if g:
                v += g(f)
        if f.counters.get("fleeing") and self.e.t - f.counters.get("flee_t", 0.0) >= SPRINT_DELAY:
            v += b.get("sprint_speed", 1.6) + f.st.extra.get("MODIFIER_VALUE_SPRINT_SPEED_BONUS", 0)
        if eth is not None:
            v = f.counters.get("float_speed", 2.5)
        slow = combine_resist(f.mods.values("move_slow"), ())
        sres = min(1.0, f.counters.get("slow_resist", 0.0) + f.stat("slow_resist"))
        v *= 1.0 - slow * (1.0 - sres)
        t = self.e.t
        if t < f.counters["dash_until"]:
            dash = b.get("ground_dash_distance_in_meters", 10.0) / max(0.2, b.get("ground_dash_duration", 0.68))
            dash *= 1.0 - min(0.9, f.stat("dash_slow")) * (1.0 - sres)
            v = max(v, dash)
        return max(0.0, v)

    def melee_reach(self, f, heavy):
        return melee_reach(f, heavy)

    def try_dash(self, f):
        if f.counters["stamina"] >= 1 and self.e.t >= f.counters["dash_until"] and f.alive \
                and not f.mods.active("stun") and not f.mods.active("immobilize"):
            f.counters["stamina"] -= 1
            f.counters["dash_until"] = self.e.t + f.st.hero.base.get("ground_dash_duration", 0.68)

    def draw(self, f):
        """A uniform [0, 1) draw: engine rng if sampling, else a hash of the matchup so a single fight stays
        deterministic while a population of fights gets the right mix (a one-off decision has no Accum)."""
        if self.e.rng is not None:
            return self.e.rng.random()
        h = hash((round(f.st.max_health, 1), f.st.souls, round(f.enemy.st.max_health, 1), f.enemy.st.souls,
                  round(self.e.t, 1), f.st.hero.id, f.enemy.st.hero.id))
        return (h % 1000003) / 1000003

    # -- loop -----------------------------------------------------------------------------------------------
    def tick(self):
        e = self.e
        if e.over:
            return
        a, b = e.fighters
        for f in (a, b):
            f.counters["stamina"] = min(f.counters["stamina_max"], f.counters["stamina"] + f.counters["stamina_regen"] * self.DT)
            fl = f.counters.get("fleeing")
            if not fl and f.alive and f.enemy.alive and not f.enemy.counters.get("fleeing") \
                    and f.hp_frac < f.skill.flee_hp and f.hp_frac < f.enemy.hp_frac and f.skill.use_actives:
                f.counters["fleeing"] = True
                f.counters["flee_t"] = e.t
                e.note(f"{f.name} runs")
                for fx in f.items_fx:
                    g = getattr(fx, "on_flee", None)
                    if g:
                        g(f)
                f.enemy.counters["chasing"] = self.draw(f) < CHASE_PROB
                for fx in f.enemy.items_fx:
                    g = getattr(fx, "on_enemy_flee", None)
                    if g:
                        g(f.enemy)
            elif fl and f.hp_frac > f.skill.flee_hp + FLEE_RECOVER:
                f.counters["fleeing"] = False
                e.note(f"{f.name} turns back")
        runner = a if a.counters.get("fleeing") else b if b.counters.get("fleeing") else None
        if runner is not None:
            chaser = runner.enemy
            runner.gun_locked_until = max(runner.gun_locked_until, e.t + self.DT + 0.01)
            self.try_dash(runner)
            for fx in chaser.items_fx:
                g = getattr(fx, "chase", None)
                if g and chaser.counters.get("chasing"):
                    g(chaser)
            vr = self.speed(runner)
            vc = 0.0
            if chaser.counters.get("chasing"):
                vc = self.speed(chaser)
                if vc < vr:
                    self.try_dash(chaser)
                    vc = self.speed(chaser)
            e.distance = max(1.0, e.distance + (vr - vc) * self.DT)
            if e.distance >= e.mech.escape_dist:
                e.escaped = runner.name
                e.note(f"{runner.name} escapes at {e.distance:.0f} m")
                e.over = True
                return
        elif e.distance > self.start:
            # nobody running: the chaser walks back into his fighting distance
            e.distance = max(self.start, e.distance - max(self.speed(a), self.speed(b)) * self.DT)
        e.after(self.DT, self.tick)


def melee_reach(f, heavy):
    """Gap beyond the start distance a rotation melee still lands from. Items with MeleeDistanceScale make heavy
    melees lunge that % farther (game data: Melee Charge 50, Crushing Fists 60, Runed Gauntlets 150; the largest
    held counts), so a chaser lands them on a runner sooner."""
    if not heavy:
        return MELEE_REACH
    return MELEE_REACH * (1.0 + max((fx.item.p("MeleeDistanceScale", 0.0) for fx in f.items_fx
                                      if getattr(fx, "item", None) is not None), default=0.0) / 100)


def melee_reachable(eng):
    mv = getattr(eng, "mover", None)
    return mv is None or eng.distance <= mv.start + MELEE_REACH


# ---------------------------------------------------------------------------------------------------------------
# Item handlers that only exist with mechanics on (attached by fight.make_fighter). `MECH_HANDLERS` is separate
# from items_fx.HANDLERS so items_fx.MODELED (search candidates) is unchanged.
# ---------------------------------------------------------------------------------------------------------------
MECH_HANDLERS = {}


def mech_handler(*class_names, need="parry"):
    def deco(cls):
        cls.need = need
        for n in class_names:
            MECH_HANDLERS.setdefault(n, []).append(cls)
        return cls
    return deco


def _base_fx(f, item, me):
    return next((fx for fx in f.items_fx if fx.item is item and fx is not me and not getattr(fx, "need", None)), None)


def _used_within(base, seconds):
    """The base handler's active was used within `seconds` (its ready_at minus its cooldown)."""
    if base is None or base.ready_at <= 0:
        return False
    return base.now < base.ready_at - base.cd() + seconds


@mech_handler("upgrade_melee_rebuttal", need="parry")
class Rebuttal(FX):
    """On a parry: heal ParrySuccessHealPercentage% of the parried damage, deal it back to the attacker, and
    +BonusDamagePercent% damage for BuffDuration. Holders parry REBUTTAL_PARRY_MULT x as often (real holders log
    0.88 parry successes per 3 min vs 0.47 for everyone else)."""
    REBUTTAL_PARRY_MULT = 1.9

    def on_start(self, f):
        f.counters["parry_mult"] = self.REBUTTAL_PARRY_MULT

    def on_parry(self, f, att, full):
        f.heal(full * self.item.p("ParrySuccessHealPercentage", 100) / 100, self.name, "item")
        f.e.damage(f, att, full, "melee", self.name, is_item=True, procs=False)
        self.buff("damage_amp", self.item.p("BonusDamagePercent", 30) / 100, self.item.p("BuffDuration", 6))


@mech_handler("upgrade_counterspell", need="parry")
class Counterspell(FX):
    """Spell parry timed against an enemy aimed cast (Skill.spell_parry_rate) when off cooldown; see module doc."""

    def on_enemy_cast(self, f, ab):
        sp = f.counters.get("spell_parry")
        if sp and sp[1] is ab:   # a recast of the parried ability is a new cast: only the parry window covers it
            sp[2] = min(sp[2], sp[0])
        if not self.ready() or not f.alive or f.mods.active("stun") or ab.impl.kind not in ("skillshot", "target", "aoe"):
            return
        sk = f.skill
        if ab.ab.ultimate and sk.spell_parry_rate_ult is not None:
            if not f.acc("spell_parry_ult").take(sk.spell_parry_rate_ult):
                return
        elif not f.acc("spell_parry").take(sk.spell_parry_rate):
            return
        self.use()
        win = self.item.p("SpellParryDuration", 0.8)
        lead = ab.ctx.raw("AbilityCastDelay")
        # a parried cast is negated whole: its own later effects (Death Slam's slam 2.6 s after the grab, delayed
        # detonations, DoT ticks) stay blocked for PARRIED_CAST_SPAN after its cast delay; other casts only inside
        # the SpellParryDuration window
        f.counters["spell_parry"] = [self.now + win, ab, self.now + lead + PARRIED_CAST_SPAN, self]
        self.done = False

    def success(self, f):
        if getattr(self, "done", True):
            return
        self.done = True
        f.counters["spell_parries"] = f.counters.get("spell_parries", 0) + 1
        f.heal(self.v("HealOnSuccess"), self.name, "item")
        d = self.item.p("BuffDuration", 6)
        self.buff("spirit_power", self.item.p("SpiritPower"), d)
        self.buff("move_speed", self.item.p("BonusMoveSpeed"), d)


@mech_handler("upgrade_ricochet", need="splash")
class Ricochet(FX):
    """Each gun hit bounces RicochetDamagePercent% to min(RicochetTargets, nearby enemies) other heroes."""

    def on_damage_dealt(self, f, t, hit):
        if not hit.gun_bullet() or (hit.source != "gun" and not hit.weapon_proc):
            return
        n = nearby_enemies(f)
        k = f.acc("ricochet").take(min(1.0, n), 1) if n < 1 else min(int(self.item.p("RicochetTargets", 2)), int(n))
        if k:
            _splash(f, hit.raw * k * self.item.p("RicochetDamagePercent", 65) / 100, "bullet", self.name)


def _take(acc, p, n):
    """acc.take for an expected count p per trial that can be above 1."""
    whole = int(p)
    return whole * n + acc.take(p - whole, n)


_split_dist = {}


def split_primary_hit(f):
    """Split Shot copies landing on the main target per landed gun bullet (Mechanics.split_range)."""
    if not getattr(f.e.mech, "split_range", False):
        return SPLIT_PRIMARY_HIT
    h = f.st.hero
    if h.id not in _split_dist:
        from .accuracy import default_distance
        _split_dist[h.id] = default_distance(h.id)
    return SPLIT_PRIMARY_HIT * SPLIT_REF_M / max(SPLIT_MIN_M, _split_dist[h.id])


@mech_handler("upgrade_split_shot", need="any")
class SplitShot(FX):
    """Active for BonusShotsDuration: every trigger pull also throws a fan of BulletSplitShot bullets. Each landed gun
    bullet lands split_primary_hit copies on the main target (on-hit items proc on them) and SPLIT_SECONDARY_COVER x
    nearby enemies (Mechanics.extra_targets) copies on others; each side hit adds a WeaponDamagePerStack% weapon
    damage stack (MaxStacks, WeaponDamageBonusDuration). Booked as Split Shot."""

    def try_active(self, f):
        if not self.ready() or f.e.distance > 35 or not f.can_shoot() or f.clip <= 0:
            return False
        e = f.enemy
        if e.mods.active("invulnerable") or e.mods.active("bullet_immune"):
            return False
        self.use()
        self.until = self.now + self.item.p("BonusShotsDuration", 5)
        return True

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "bullet" or hit.source != "gun" or not hit.hits or self.now >= getattr(self, "until", -1):
            return
        per = f.counters.get("bullet_per", 0.0)
        if not per:
            return
        k = _take(f.acc("split_main"), split_primary_hit(f), hit.hits)
        if k:
            f.e.damage(f, t, per * k, "bullet", self.name, is_item=True, hits=k)
        x = nearby_enemies(f)
        if x > 0:
            k2 = f.acc("split_side").take(min(1.0, SPLIT_SECONDARY_COVER * x), hit.hits)
            if k2:
                _splash(f, per * k2, "bullet", self.name)
                for _ in range(k2):
                    j = f.counters.get("split_stack", 0)
                    f.counters["split_stack"] = j + 1
                    self.buff("weapon_pct", self.item.p("WeaponDamagePerStack", 8) / 100,
                              self.item.p("WeaponDamageBonusDuration", 12),
                              tag=("split", j % int(self.item.p("MaxStacks", 5))))


# -- movement items ---------------------------------------------------------------------------------------------
class _MoveFX(FX):
    pass


@mech_handler("upgrade_cardio_calibrator", need="movement")
class EnduringSpeed(_MoveFX):
    """Passive move speed is in the static stats; this adds SlowResistancePercent."""

    def on_start(self, f):
        f.counters["slow_resist"] = f.counters.get("slow_resist", 0.0) + self.item.p("SlowResistancePercent") / 100


@mech_handler("upgrade_fleetfoot_boots", need="movement")
class Fleetfoot(_MoveFX):
    """Active: +ActiveBonusMoveSpeed and SlowResistancePercent for AbilityDuration, used to run or to chase."""

    def _go(self, f):
        if not self.ready():
            return
        self.use()
        d = self.item.p("AbilityDuration", 5)
        self.buff("move_speed", self.item.p("ActiveBonusMoveSpeed", 3), d)
        self.buff("slow_resist", self.item.p("SlowResistancePercent", 40) / 100, d)

    def on_flee(self, f):
        self._go(f)

    def chase(self, f):
        self._go(f)


@mech_handler("upgrade_reduce_debuff_duration", need="movement")
class DispelSpeed(_MoveFX):
    """Dispel Magic's active also gives +ActiveBonusMoveSpeed for BuffDuration."""

    def move_speed(self, f):
        base = getattr(self, "_b", None) or _base_fx(f, self.item, self)
        self._b = base
        return self.item.p("ActiveBonusMoveSpeed", 2) if _used_within(base, self.item.p("BuffDuration", 3)) else 0.0


@mech_handler("upgrade_self_bubble", need="movement")
class EtherealMove(_MoveFX):
    """Ethereal Shift: float at FloatMoveSpeed while in the void, then +BonusMoveSpeed for BuffDuration."""

    def on_start(self, f):
        f.counters["float_speed"] = self.item.p("FloatMoveSpeed", 2.5)

    def move_speed(self, f):
        return self.item.p("BonusMoveSpeed", 3) if f.mods.get("spirit_power", "eth") is not None else 0.0


@mech_handler("upgrade_magic_carpet", need="movement")
class MagicCarpet(_MoveFX):
    """Used to run: assumed +FlyMoveSpeed m/s for AbilityDuration (flying likely also breaks line of sight, not
    modeled)."""

    def on_flee(self, f):
        if self.ready():
            self.use()
            self.buff("move_speed", self.item.p("FlyMoveSpeed", 7), self.item.p("AbilityDuration", 12))


@mech_handler("upgrade_warp_stone", need="movement")
class WarpStoneMove(_MoveFX):
    """With movement on, Warp Stone is saved for running: its bullet resist, and on average WARP_AWAY of its
    AbilityCastRange teleport adds to the gap (fit: the full 11 m gave +23 pts escape share vs +6.5 real)."""

    def on_start(self, f):
        self.base = _base_fx(f, self.item, self)
        if self.base is not None:
            self.base.try_active = lambda f: False

    def on_flee(self, f):
        b = self.base
        if b is None or not b.ready() or f.mods.active("stun"):
            return
        b.use()
        self.buff("bullet_resist", self.item.p("BulletResist") / 100, self.item.p("CasterBuffDuration", 6))
        f.e.distance += self.item.p("AbilityCastRange", 11) * WARP_AWAY


@mech_handler("upgrade_phantom_strike", need="movement")
class PhantomChase(_MoveFX):
    """Phantom Strike on a runner within AbilityCastRange: its normal hit plus teleporting next to him, and its
    SlowPercent slow."""

    def on_start(self, f):
        self.base = _base_fx(f, self.item, self)

    def chase(self, f):
        b = self.base
        if b is None or not b.ready() or f.e.distance > self.item.p("AbilityCastRange", 25) + 0.5:
            return
        if b.try_active(f):
            f.e.distance = 2.0
            _debuff(f.enemy, "move_slow", self.item.p("SlowPercent", 40) / 100, self.item.p("SlowDuration", 3),
                    ("phantom", "slow"))


@mech_handler("upgrade_containment", need="movement")
class SlowingHex(_MoveFX):
    """Active on a runner in AbilityCastRange: SlowPercent slow and GroundDashReductionPercent shorter dashes."""

    def chase(self, f):
        if not self.ready() or f.e.distance > self.item.p("AbilityCastRange", 25) + 0.5:
            return
        self.use()
        d = self.item.p("AbilityDuration", 3.5)
        _debuff(f.enemy, "move_slow", self.item.p("SlowPercent", 16) / 100, d, ("hex", "slow"))
        _debuff(f.enemy, "dash_slow", abs(self.item.p("GroundDashReductionPercent", 26)) / 100, d, ("hex", "dash"))


@mech_handler("upgrade_magic_slow", need="movement")
class MysticSlow(_MoveFX):
    """Spirit damage from abilities / items slows by MovementSpeedSlow% (and dashes) for AbilityDuration."""

    def on_damage_dealt(self, f, t, hit):
        if hit.kind != "spirit" or not (hit.is_ability or hit.is_item) or hit.amount <= 0:
            return
        d = self.item.p("AbilityDuration", 2)
        _debuff(t, "move_slow", self.item.p("MovementSpeedSlow", 24) / 100, d, ("mslow", "slow"))
        _debuff(t, "dash_slow", abs(self.item.p("GroundDashReductionPercent", 10)) / 100, d, ("mslow", "dash"))


@mech_handler("upgrade_slowing_bullets", need="movement")
class SlowingBulletsMove(BuildUp):
    def proc(self, f, t):
        d = self.item.p("SlowDuration", 3.5)
        _debuff(t, "move_slow", self.item.p("SlowPercent", 24) / 100, d, ("sbullets", "slow"))
        _debuff(t, "dash_slow", abs(self.item.p("GroundDashReductionPercent", 20)) / 100, d, ("sbullets", "dash"))


SlowingBulletsMove.need = "movement"


@mech_handler("upgrade_cold_front", "upgrade_arctic_blast", need="movement")
class FrostSlow(_MoveFX):
    """Cold Front / Arctic Blast: their hit slows by MovementSpeedSlow / SlowPercent for AbilityDuration /
    SlowDuration."""

    def on_damage_dealt(self, f, t, hit):
        if hit.source != self.name:
            return
        pct = self.item.p("MovementSpeedSlow") or self.item.p("SlowPercent")
        d = self.item.p("SlowDuration") or self.item.p("AbilityDuration", 4)
        _debuff(t, "move_slow", pct / 100, d, ("frost", self.name))


@mech_handler("upgrade_boxing_glove", need="movement")
class LifestrikeSlow(_MoveFX):
    """Lifestrike's melee proc also slows SlowPercent for SlowDuration (same AbilityCooldown)."""

    def on_damage_dealt(self, f, t, hit):
        if not _any_melee(hit) or not _melee_proc(self, f, hit, ":slow"):
            return
        self.use()
        _debuff(t, "move_slow", self.item.p("SlowPercent", 48) / 100, self.item.p("SlowDuration", 2.5), ("lstrike", "slow"))


def attach(f, items):
    m = f.e.mech
    on = {"parry": m.parry, "splash": True, "any": True, "movement": m.movement}
    for it in items:
        for cls in MECH_HANDLERS.get(it.class_name, ()):
            if not on.get(cls.need, False):
                continue
            fx = cls(it, f)
            f.items_fx.append(fx)
            if hasattr(fx, "stat"):
                f.stat_hooks.append(fx.stat)
