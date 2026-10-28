# Real crowd-control time per fight vs the sim duel (2026-10-28)

Question (follow-up of `focus_share.md`): Debuff Reducer is 12th of 14 tier-2 vitality items in the overall score
but 3rd of 16 by real win edge. Is the sim's duel short of the stuns, silences and disarms real players sit through,
so status resist is worth too little?

Answer: no, the other way round. The sim duel puts more CC on a player from its one foe than real Phantom+ players
take from all enemies together. The main cause is that an ability's CC always lands in full, while its damage counts
only as often as it lands. Letting the CC land like the damage does (`Mechanics.cc_landing`) closes most per-hero
gaps, but sim_vs_win dips 0.001 in three of four budget halves, so it ships off (opt-in). Debuff Reducer's gap is not
in CC exposure.

## Real CC from replays

`scripts/fight_length/fetch_cc.py` pulls each player pawn's modifier state mask (`m_bvEnabledStateMask`, one row per
change) and the game's `AbilityNotifyEvent` (attacker, victim, ability, status bits 1 stun / 4 sleep / 8 silence /
16 disarm / 32 immobilize) from the 260 Phantom+ replays that `fight_length` already uses. The state bits were
matched to the notify statuses by which bit goes on with them: stun = bit 12 (97% of stun notifies; Knockdown 98%,
Petrifying Bola 98%), sleep = 144 (Sleep Dagger 100%), silence = 17 (Silence Wave 98%, 3.0 s runs). Immobilize (18)
also goes on without any notify and reads high; disarm has no clear bit (Sand Blast's disarm notifies turn nothing
on). Nurse's fear, Hotel Guest and Telekinesis send no notify and are not counted.

`scripts/fight_length/cc_time.py`: a player's combat time is the union of their pair fights (fit_length's runs of
damage with one enemy, both ways). Share of combat time under each CC:

| | all 260 matches | match-id half 0 | half 1 | from the pair-fight foe |
|---|---|---|---|---|
| stun | 2.46% | 2.47% | 2.46% | 63% |
| sleep | 0.28% | 0.25% | 0.31% | 84% |
| silence | 2.20% | 2.16% | 2.24% | 58% |
| immobilize (bit reads high) | 3.17% | 3.01% | 3.34% | 18% |
| disarm (unsure bit) | 0.45% | 0.48% | 0.42% | 1% |

14,507 combat minutes over 3,119 player-matches; stuns come 1.1 times per combat minute, 1.35 s each.

## The sim duel's CC

Same script, `--sim`: damage_audit's whole-match duels (each player's real build and aim against a real foe of the
same match, mechanics as the searches), 3,000 players, CC put on the player by the duel's one foe:

| | real, all enemies | sim before | sim with cc_landing |
|---|---|---|---|
| stun (+ sleep) | 2.74% | 4.24% | 3.27% |
| silence | 2.20% | 3.07% | 2.97% |
| disarm | (0.45%) | 2.09% | 1.90% |
| immobilize | (3.17%) | 0.51% | 0.36% |

Real stun from the pair-fight foe alone is 1.7% of combat time, so the sim's one foe still CCs ~2x what a real duel
partner does. Per hero (CC each hero puts on enemies per second of its own combat; real = notify-credited CC only, so
heroes whose CC sends no notify read low: Nurse, Doorman, Wraith, Rem, Holliday):

| hero | real | sim before | sim now |
|---|---|---|---|
| Mo & Krill | 5.7% | 25.7% | 10.3% |
| Vyper | 5.6% | 14.0% | 4.3% |
| Warden | 7.2% | 17.8% | 8.3% |
| Grey Talon | 12.3% | 19.0% | 10.6% |
| Graves | 5.4% | 10.0% | 4.3% |
| Ivy | 4.5% | 13.0% | 7.3% |
| Infernus | 2.2% | 4.4% | 2.7% |
| Haze | 7.0% | 13.5% | 11.4% |
| Abrams | 3.9% | 13.3% | 11.8% |
| Paradox | 5.7% | 14.8% | 13.6% |
| Celeste | 8.6% | 3.7% | 3.7% |
| Violet | 16.9% | 13.3% | 13.3% |

Still over after the change: Abrams (Seismic Impact's stun is not a skillshot and its landing factor is above 1),
Paradox, Sinclair, Silver, Calico, and items' CC (unchanged: item landing factors are about damage).

## The change: CC lands like the ability

`AbilityCtx.debuff` multiplies a stun / silence / disarm / immobilize's duration by `cc_land()`: the skillshot's
spirit accuracy x the ability's fitted landing factor x the reach wait, capped at 1 (the expected CC time, as the
damage is the expected damage). Checks, all on the same main:

| | main | cc_landing |
|---|---|---|
| sim_vs_win 27k all pairs | 0.298 | 0.301 |
| 27k within slot and tier | 0.333 (hero halves 0.3326 / 0.3345) | 0.333 (0.3316 / 0.3347) |
| 27k per item | 0.436 | 0.436 |
| 37k all pairs | 0.286 | 0.285 |
| 37k within slot and tier | 0.317 (0.3154 / 0.3194) | 0.316 (0.3144 / 0.3184) |
| whole-match damage audit (mix distance) | 0.0180 (halves 0.0187 / 0.0172) | 0.0181 (0.0186 / 0.0175) |

Off by default: it is what the replays show, but the within-tier check dips in both 37k halves and one 27k half
(by 0.001, about noise, and every other row is flat or up). The flag and the measuring script stay for a later look,
e.g. with an ability landing refit under it.

## Status resist under focus

With CC exposure measured, `Mechanics.status_focus` (status resist x focus 2 in the overall duel, PR #175) counts
resist against ~2.4x the real stun exposure. Turned off (with cc_landing on): 27k within 0.333 -> 0.331, both hero
halves (0.3303 / 0.3325). Its gain comes from the other debuffs status resist also shortens (slows, shreds, heal
cuts, DoTs), which this data does not measure. Left on.

## Debuff Reducer

27k, tier 2 vitality, mean sim gain per 1000 souls: 2.5 (12th of 14; real 3rd), 0.7 with cc_landing on. Real stun +
silence is ~5% of combat time, so a 25% status resist saves ~1.2% of it: the real edge of Debuff Reducer is not CC
time. Left for a later look: what else holders differ in (slows, heal cuts, DoTs, who buys it).
