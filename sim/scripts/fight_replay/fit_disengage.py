"""When heroes join and leave real fights, from the same fights the site's replay finds (detect.cjs, needs node).

Per hero-second of fighting (from its first to its last fighting second), by health share at that second: the chance
it leaves alive while the fight goes on (its last fighting second, no death, before the fight's end) and the chance it
dies. Also how many heroes join after the start and how many survivors leave before the end. check_replay.py mode
"hazard" uses the leave rate.

usage: python3 -I fit_disengage.py <repo dir> <metadata dir>
"""
import collections as C
import json
import os
import statistics as st
import subprocess
import sys

ROOT = os.path.abspath(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    meta = sys.argv[2]
    leave, die, n = C.Counter(), C.Counter(), C.Counter()
    joins, gaps = [], []
    for fn in sorted(f for f in os.listdir(meta) if f.endswith(".json")):
        r = subprocess.run(["node", os.path.join(HERE, "detect.cjs"), os.path.join(ROOT, "web/replay.js"),
                            os.path.join(meta, fn), "hp"], capture_output=True, text=True)
        if r.returncode:
            continue
        d = json.loads(r.stdout)
        for F in d["fights"]:
            dead = {x["slot"] for x in F["deaths"]}
            L = F["t1"] - F["t0"]
            for s in map(str, F["players"]):
                j, la = F["join"][s], F["last"][s]
                joins.append(j)
                for t in range(j, la + 1):
                    b = min(9, int(d["hp"][s][F["t0"] + t] / 10))
                    n[b] += 1
                    if t == la:
                        if int(s) in dead:
                            die[b] += 1
                        elif la < L:
                            leave[b] += 1
                if int(s) not in dead:
                    gaps.append(L - la)
    print("health   hero-s   leave/s   die/s")
    for b in range(10):
        print(f"{b * 10:3d}-{b * 10 + 10:3d}%  {n[b]:7d}  {leave[b] / max(1, n[b]):.3f}    {die[b] / max(1, n[b]):.3f}")
    print(f"all       {sum(n.values()):7d}  {sum(leave.values()) / sum(n.values()):.3f}    "
          f"{sum(die.values()) / sum(n.values()):.3f}")
    late = [j for j in joins if j > 0]
    print(f"heroes joining after the start {len(late) / len(joins):.2f} (median {st.median(late)} s in); survivors "
          f"leaving before the end {sum(g > 0 for g in gaps) / len(gaps):.2f} (median {st.median([g for g in gaps if g > 0])} s early)")


if __name__ == "__main__":
    main()
