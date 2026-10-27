# Rebuttal and Debuff Reducer vs real wins; status resist under focus (2026-10-28)

Question (follow-up of `deaths_per_engagement.md`): Rebuttal is still the overall score's 140th of 141 items by mean
gain at 27k and Debuff Reducer stays undervalued against their real Phantom+ win edges. What does the sim miss?

## Rebuttal: its low value is real

Within its slot and tier (the real edge compares against those), Rebuttal is last in real games too
(27k, mean over heroes):

| tier 1 vitality | sim gain / 1000 souls | real edge |
|---|---|---|
| Extra Regen | +0.037 | -0.66 |
| Melee Lifesteal | +0.036 | -1.85 |
| Healing Rite | +0.028 | -2.23 |
| Grit | +0.013 | +0.94 |
| Extra Health | +0.007 | +0.04 |
| **Rebuttal** | **-0.025** | **-2.52** |

Its overall rank (140 / 141) is a per-soul artefact of a cheap item carrying the real death rate and focus cost
factors (holders die 1.07x and take 1.07x per minute, kills + assists 1.04x). Lifting it hurts the check: dropping its
focus cost alone, within slot and tier 0.331 -> 0.329. Its parry already counts (holders parry 1.9x, `Rebuttal` in
`mechanics.py`). No change.

Focus cost per engagement (damage taken ratio / kills + assists ratio, as #171 did for deaths) was tried for every
item and is worse (27k within 0.331 -> 0.314 at FOCUS_GAMMA 0.4, both match-id halves 0.315 / 0.311); damage taken /
damage dealt lifts within (0.345) but lowers all pairs and per item (0.290, 0.413). Neither kept.

## Debuff Reducer: status resist counted one enemy's debuffs

The overall duel's single enemy hits x FOCUS (2) to stand in for the enemy team's damage, but it applied its stuns,
slows, silences, disarms and shreds once. Status resist saves the same share of every enemy's debuff time, so its
saving under focus is resist x the number of enemies. Fix: `Mechanics.status_focus` (on): `survive(focus=)` sets the
holder's `Fighter.status_focus = focus` and every debuff duration uses `Fighter.status_resist()` = (status resist)
x status_focus, at most 1. The audit and the dummy (focus 1) are unchanged; the enemy's own resist against the
holder's debuffs is unchanged (only the holder is focused).

## Results (sim_vs_win, blend off, all heroes; local pools from the shared 10-14 snapshots)

| | all pairs | within slot and tier | per item | within, hero halves | all, hero halves |
|---|---|---|---|---|---|
| 27k main | 0.294 | 0.331 | 0.430 | 0.331 / 0.332 | 0.281 / 0.309 |
| **27k status focus** | **0.296** | **0.334** | **0.433** | **0.333 / 0.335** | **0.282 / 0.311** |
| 37k main | 0.281 | 0.311 | 0.410 | 0.310 / 0.313 | 0.271 / 0.294 |
| **37k status focus** | **0.283** | **0.314** | **0.414** | **0.313 / 0.316** | **0.273 / 0.295** |

Items that move (mean gain per 1000 souls): Blood Tribute +0.006, Debuff Reducer +0.005 / +0.006, Weighted Shots
+0.002 / +0.003, Spellbreaker, Unstoppable; nothing else moves more than 0.0005. Debuff Reducer's mean gain rank
131 -> 121 (27k), 135 -> 120 (37k).

## Left

Debuff Reducer is still below its tier's middle in the sim (real edge +0.3, third of 16 tier-2 vitality items): it
keeps the focus cost of its holders' 1.05x damage taken. Status resist against the enemy team's debuffs on teammates
(cleanse-like value) and debuffs from more than FOCUS enemies are not modelled.
