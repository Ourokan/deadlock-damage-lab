"""How much ally healing items really give teammates, vs the 3v3 team_value.py fits. Run from sim/:

    python3 scripts/team/ally_heal.py /mnt/project-files/analysis/work/sustain   (~5 min)

team_value.py casts an ally heal on the neediest teammate whenever it is ready. Real Phantom+ holders (damage matrix
of the 400 sustain replays, fetch_sustain.py: heals credited to the item, to the holder vs to anyone else, after
9 min while held) use Healing Nova and Rescue Beam on teammates about as the 3v3 does, but Restorative Locket almost
only on themselves: 6 HP/min to teammates vs 118 to self, where the 3v3 heals teammates 2.5x more than the holder.

Per item: real ally heal per held minute / the 3v3's ally heal per fight minute (27k popular builds, LINEUPS lineups x 3
holders x focus/spread x 12/20 m, like team_value.py), divided by the same ratio pooled over the other items (held
minutes weights; leave-one-out so Locket's many holders don't set its own reference): the share of the game spent
fighting and casting is the same for every heal item. overall_search.team_value multiplies the
item's team value by it (capped at 1; barrier and aura items have no heal data and keep 1). Writes data/ally_heal.json.
Static: the replays live in the shared folder, CI can't refit it.
"""
import collections
import dataclasses
import glob
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, SIM)
sys.path.insert(0, HERE)

import team_value as TV  # noqa: E402
from deadsim import Loadout  # noqa: E402
from deadsim.data import game  # noqa: E402
from deadsim.dmatrix import win  # noqa: E402
from deadsim.team import team_fight  # noqa: E402

OUT = os.path.join(SIM, "data", "ally_heal.json")
ITEMS = ("Healing Nova", "Rescue Beam", "Restorative Locket")
SOULS = 27000
LINEUPS = 15
MID_S = 540      # after the laning phase


def real(folder):
    """{item: [HP/min to self, HP/min to teammates, held minutes]} after MID_S s while held."""
    g = game()
    by = {it.name: it for it in g.items.values() if it.name in ITEMS}
    ids = {it.id: n for n, it in by.items()}
    acc = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for fn in sorted(glob.glob(os.path.join(folder, "*.json.gz"))):
        with gzip.open(fn, "rt") as f:
            m = json.load(f)
        times = m["times"]
        if not times:
            continue
        for p in m["players"]:
            slot = str(p["slot"])
            iv = collections.defaultdict(list)
            for iid, t0, ts in p["items"]:
                if iid in ids and t0 > 0:
                    iv[ids[iid]].append((t0, ts or 1e9))
            rows = m["heal"].get(slot, [])
            for k, t1 in enumerate(times):
                t0 = times[k - 1] if k else 0
                if t0 < MID_S:
                    continue
                for n, spans in iv.items():
                    if not any(a <= t0 and b >= t1 for a, b in spans):
                        continue
                    for st, src, tgt, cum in rows:
                        if st in (1, 5) and src == by[n].class_name:
                            acc[n][0 if str(tgt) == slot else 1] += win(cum, k, len(times))
                    acc[n][2] += (t1 - t0) / 60
    return {n: [v[0] / v[2], v[1] / v[2], v[2]] for n, v in acc.items() if v[2]}


def sim(item):
    """3v3 ally heal of the item's holder per fight minute (team_value.py's fights)."""
    ally, t = 0.0, 0.0
    for six in TV.lineups()[:LINEUPS]:
        a = [Loadout(h, TV.popular(h, SOULS), souls=SOULS, skill=TV.skill(h)) for h in six[:3]]
        b = [Loadout(h, TV.popular(h, SOULS), souls=SOULS, skill=TV.skill(h)) for h in six[3:]]
        for k in range(3):
            base = [dataclasses.replace(x, items=[i for i in x.items if i != item]) for x in a]
            w = list(base)
            w[k] = dataclasses.replace(base[k], items=base[k].items + [item])
            for focus in ("focus", "spread"):
                for dist in (12.0, 20.0):
                    r = team_fight(w, b, focus=focus, distance=dist, max_time=TV.MAX_TIME, huddle=1.0, aoe_share=0.0)
                    ally += r.fighters[k]["healing_given_by_source"].get(item, 0.0)
                    t += r.time
    return ally / t * 60


def main():
    re = real(sys.argv[1])
    sm = {n: sim(n) for n in ITEMS}
    ratio = {n: re[n][1] / sm[n] for n in ITEMS if sm[n] > 0}

    def pooled(skip=None):
        rest = [n for n in ratio if n != skip]
        return sum(ratio[n] * re[n][2] for n in rest) / sum(re[n][2] for n in rest)
    out = {"source": f"ally_heal.py: {len(glob.glob(os.path.join(sys.argv[1], '*.json.gz')))} Phantom+ sustain "
                     f"replays after {MID_S} s vs the 3v3 at {SOULS} souls",
           "pooled_real_per_sim": round(pooled(), 4), "items": {}}
    for n in ITEMS:
        out["items"][n] = {"real_self_hp_min": round(re[n][0], 1), "real_ally_hp_min": round(re[n][1], 1),
                           "held_min": round(re[n][2]), "sim_ally_hp_fight_min": round(sm[n], 1),
                           "real_per_sim": round(ratio[n], 4), "factor": round(min(1.0, ratio[n] / pooled(n)), 3)}
        print(n, out["items"][n])
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
