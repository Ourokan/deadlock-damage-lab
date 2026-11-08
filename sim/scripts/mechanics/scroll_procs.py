"""Lightning Scroll in Phantom+ replays, per holder hero (holders from 10 s before their first proc): procs, ult casts
(clusters of ult hits on heroes, gaps <= 6 s), procs per cast and per hero the cast hit, procs per point of ult damage
dealt to heroes (items_fx.SCROLL_PER_ULT_DMG), and the proc's median size.

usage: python3 -I scroll_procs.py <raw dir> [raw dir ...]
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
ITEM = next(i for i, v in NAMES.items() if v[0] == "item" and v[1] == "Lightning Scroll")
HERO = {h.id: h for h in G.heroes.values()}


def main(dirs):
    seen = {}
    for d in dirs:   # a match in several dirs counts once
        for f in glob.glob(os.path.join(d, "*.ndjson.gz")):
            seen.setdefault(os.path.basename(f), f)
    st = collections.defaultdict(collections.Counter)
    size = collections.defaultdict(list)
    for fn in sorted(seen.values()):
        ctl, ev = {}, []
        for line in gzip.open(fn, "rt"):
            r = json.loads(line)
            if r["k"] == "ctl":
                ctl[r["a"]] = int(str(r.get("s") or "0").split("|")[0])
            elif r["k"] == "dmg" and r.get("s"):
                ev.append((r["tick"], r["a"] // 100000, r["a"] % 100000, int(r["s"].split("|")[0]), r["v"]))
        ev.sort()
        heroes = set(ctl)
        for me, hid in ctl.items():
            h = HERO.get(hid)
            if h is None:
                continue
            mine = [e for e in ev if e[1] == me and e[2] in heroes]
            procs = [e for e in mine if e[3] == ITEM]
            if not procs:
                continue
            ults = {a.id for a in h.abilities if a.ultimate}
            t0 = procs[0][0] - 640
            uh = [e for e in mine if e[3] in ults and e[0] >= t0]
            casts = []
            for e in uh:
                if casts and e[0] - casts[-1][-1][0] <= 6 * 64:
                    casts[-1].append(e)
                else:
                    casts.append([e])
            c = st[h.name]
            c["holders"] += 1
            c["procs"] += len(procs)
            c["casts"] += len(casts)
            c["victims"] += sum(len({e[2] for e in cs}) for cs in casts)
            c["ult_dmg"] += sum(e[4] for e in uh)
            size[h.name] += [e[4] for e in procs]
    print(f"{len(seen)} replays")
    for n, c in sorted(st.items(), key=lambda x: -x[1]["procs"]):
        print(f"{n:13s} holders {c['holders']:3d} procs {c['procs']:4d} casts {c['casts']:3d} "
              f"per cast {c['procs'] / max(1, c['casts']):.2f} per hero hit {c['procs'] / max(1, c['victims']):.2f} "
              f"per 1000 ult dmg {1000 * c['procs'] / max(1, c['ult_dmg']):.2f} size median {statistics.median(size[n]):.0f}")


if __name__ == "__main__":
    main(sys.argv[1:])
