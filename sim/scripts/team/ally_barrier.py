"""How much ally barrier items really give teammates, vs the 3v3 team_value.py fits. Run from sim/:

    python3 scripts/team/ally_barrier.py HOLDER_RATES.json   (~30 s; holder_rates.py output on fight_rate_ext)

ally_heal.py scales ally heal items' team value by how much real holders heal teammates; barrier items had no heal
data and kept their full 3v3 value, so Divine Barrier, whose 3v3 holder shields the neediest teammate whenever it is
ready, scored +0.13 log of team value (the largest of any item with Heroic Aura) for a real win edge near zero.
Real Phantom+ holders' extra barrier on teammates per minute (holder_rates.py "team_barrier", holders / non-holders
ratio - 1 times the non-holders' base, at the same hero, net worth and game time): Divine Barrier +172 HP/min at 27k
(each match-id half 172 / 173; their own barrier +212), Guardian Ward +16. The same measure for the ally heal items
("team_heal"): Healing Nova +336, Rescue Beam +191. Per item: real ally HP/min / the 3v3's ally HP per fight minute
(ally_heal.sim, barrier_given counted like healing_given), divided by the heal items' median ratio (the share of the
game spent fighting is the same for every item), capped at 1. Written into data/ally_heal.json beside the heal
items' factors (overall_search.team_value reads them by name).
"""
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, SIM)
sys.path.insert(0, HERE)

import ally_heal as AH  # noqa: E402

BARRIER = ("Divine Barrier", "Guardian Ward")
# Guardian Ward is measured but keeps factor 1: its real ally barrier is tiny (+16 HP/min, factor 0.115), but it already
# ranks under its real edge within slot and tier (-1.2 z at 27k from its duel and death parts), and cutting its team
# value lowers sim_vs_win (27k within 0.3805 -> 0.3760 with both, 0.3832 with Divine Barrier alone; 37k alike).
APPLY = ("Divine Barrier",)
HEAL_REF = ("Healing Nova", "Rescue Beam")   # Locket left out: its ally heal is the outlier ally_heal.py corrects
BAND = "27000_2"   # all matches at the 27k band (ally_heal.SOULS)


def real(rates):
    """{item: extra HP/min given to teammates by holders}: (ratio - 1) x non-holders' base rate."""
    t = rates[BAND]
    out = {}
    for n in BARRIER + HEAL_REF:
        r, z, base = t[n]["team_barrier" if n in BARRIER else "team_heal"]
        out[n] = (r - 1) * base
    return out


def main():
    with open(sys.argv[1]) as f:
        rates = json.load(f)
    re = real(rates)
    sm = {n: AH.sim(n, barrier=n in BARRIER) for n in BARRIER + HEAL_REF}
    ratio = {n: max(0.0, re[n]) / sm[n] for n in sm if sm[n] > 0}
    ref = statistics.median(ratio[n] for n in HEAL_REF)
    with open(AH.OUT) as f:
        out = json.load(f)
    out["barrier_source"] = (f"ally_barrier.py: holder_rates.py team_barrier / team_heal at the 27k band vs the 3v3 at "
                             f"{AH.SOULS} souls; heal items' median real/sim {ref:.4f}")
    for n in BARRIER:
        out["items"][n] = {"real_ally_extra_hp_min": round(re[n], 1), "sim_ally_hp_fight_min": round(sm[n], 1),
                           "real_per_sim": round(ratio[n], 4), "measured_factor": round(min(1.0, ratio[n] / ref), 3),
                           "factor": round(min(1.0, ratio[n] / ref), 3) if n in APPLY else 1.0}
        print(n, out["items"][n])
    for n in HEAL_REF:
        print(f"{n} (reference) real {re[n]:.1f} HP/min, 3v3 {sm[n]:.1f}, ratio {ratio[n]:.4f}")
    with open(AH.OUT, "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
