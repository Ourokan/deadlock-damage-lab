"""What an on-hit item's procs ride on in Phantom+ replays, per hero: for each holder (from their first proc on), the
item's procs, the holder's gun hits on heroes, procs per gun hit, item damage / gun damage, the proc's size over the
gun hit it shares a tick with, and which of the holder's own sources hit the same victim in the proc's tick (gun,
an ability, another item, or nothing). An item that rides a source the sim's on-hit rule skips (an ability's bullets,
melee) shows up as procs sharing ticks with that source.

usage: python3 -I item_ticks.py "<Item>" <raw dir> [raw dir ...]
"""
import collections
import glob
import gzip
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fight_length"))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from opener_timing import sources  # noqa: E402
from deadsim.data import game  # noqa: E402

G = game()
NAMES = sources(G)
WEAP = {w["id"] for w in json.load(open(os.path.join(HERE, "..", "..", "..", "data", "game", "weapons.json")))}
ITEM = next(i for i, v in NAMES.items() if v[0] == "item" and v[1] == sys.argv[1])
WIN = int(os.environ.get("TICK_WIN", "0"))   # also count the victim's hits this many ticks either side
HERO = {h.id: h.name for h in G.heroes.values()}


def label(ab):
    if ab in WEAP:
        return "gun"
    return NAMES.get(ab, ("?", f"id {ab}"))[1]


def main(dirs):
    st = collections.defaultdict(lambda: collections.Counter())
    ratio = collections.defaultdict(list)
    seen = {}
    for d in dirs:   # a match in several dirs counts once
        for f in glob.glob(os.path.join(d, "*.ndjson.gz")):
            seen.setdefault(os.path.basename(f), f)
    files = sorted(seen.values())
    print(f"{len(files)} replays", flush=True)
    for fn in files:
        ctl, ev = {}, []
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if r["k"] == "ctl":
                ctl[r["a"]] = int(str(r.get("s") or "0").split("|")[0])
            elif r["k"] == "dmg" and r.get("s"):
                ev.append((r["tick"], r["a"] // 100000, r["a"] % 100000, int(r["s"].split("|")[0]), r["v"]))
        for me, hid in ctl.items():
            mine = [e for e in ev if e[1] == me]
            procs = [e for e in mine if e[3] == ITEM]
            if not procs:
                continue
            t0 = min(e[0] for e in procs)
            name = HERO.get(hid, str(hid))
            c = st[name]
            c["holders"] += 1
            by = collections.defaultdict(list)
            for t, _, v, ab, d in mine:
                if t < t0:
                    continue
                lab = label(ab)
                if ab == ITEM:
                    c["procs"] += 1; c["item_dmg"] += d
                elif lab == "gun":
                    c["gun_hits"] += 1; c["gun_dmg"] += d
                by[(t, v)].append((ab, lab, d))
            keys = sorted(by)
            vic = collections.defaultdict(list)
            for k in keys:
                vic[k[1]].append(k[0])
            for (t, v), L in by.items():
                if not any(ab == ITEM for ab, _, _ in L):
                    continue
                near = [x for tt in vic[v] if abs(tt - t) <= WIN and tt != t for x in by[(tt, v)]]
                others = sorted({lab for ab, lab, _ in L + near if ab != ITEM})
                c["with " + ("+".join(others) or "nothing")] += 1
                g = sum(d for _, lab, d in L if lab == "gun")
                if g:
                    ratio[name].append(sum(d for ab, _, d in L if ab == ITEM) / g)
    for name, c in sorted(st.items(), key=lambda x: -x[1]["procs"]):
        if c["procs"] < 50:
            continue
        r = ratio[name]
        withs = sorted(((k[5:], n) for k, n in c.items() if k.startswith("with ")), key=lambda x: -x[1])[:5]
        print(f"{name}: holders {c['holders']}, procs {c['procs']}, per gun hit {c['procs'] / max(1, c['gun_hits']):.3f}, "
              f"dmg/gun {c['item_dmg'] / max(1, c['gun_dmg']):.3f}, proc/gun hit median "
              f"{statistics.median(r) if r else 0:.2f}; same tick: "
              + ", ".join(f"{k} {n / c['procs']:.2f}" for k, n in withs))


if __name__ == "__main__":
    main(sys.argv[2:])
