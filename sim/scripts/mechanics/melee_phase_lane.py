"""Lane point for Mechanics.melee_phase: each hero's melee multiplier in the lane (the first fifth of the match).

data/melee_phase.json has points at 30 / 60 / 90% of the match (melee_phase.py) and is flat below the first one
(~6k net worth), but real players melee even more in the lane: on the post-hotfix sample the lane fifth's melee share
read 0.025 off per player (Vindicta 0.047 real vs 0.021 sim, Warden 0.093 vs 0.065, Seven 0.073 vs 0.051).

Fit: the damage audit's lane fifth (cover mode, AUDIT_FIFTH_SOURCES=1) gives real / sim melee share per hero; the
lane point is the multiplier now in use at the hero's lane net worth x that ratio, shrunk in ln to the pooled ratio
(heroes weighted by real melee damage) with SHRINK players of weight, clamped. Its net worth is the median of the
hero's players at 10% of the match. Fitting at 10% of the match directly (melee_phase.py with FRACS 0.1) overshot:
that duel set's melee share is far lower than the audit's lane fifth, so the lane got worse held out.

Only heroes with a melee_phase row get a point (prepended, kept below the row's first point); one round. Rows that
already have a lane point (Abrams and Warden from melee_phase.py --fracs 0.1,0.3,0.6,0.9, or an earlier run of this
script) are left as they are, so a second run adds nothing. Re-running melee_phase.py --write (default fracs) drops
the lane points.

usage: python3 melee_phase_lane.py [--sample PATH] [--audit AUDIT.json] [--write]
(--audit: an audit JSON written with AUDIT_FIFTH_SOURCES=1 on the same sample, instead of running one)
"""
import gzip
import json
import math
import os
import statistics
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(HERE, ".."))
from deadsim import game  # noqa: E402
from deadsim.mechanics import melee_phase_mult  # noqa: E402
import landing_rates as L  # noqa: E402

OUT = os.path.join(ROOT, "data", "melee_phase.json")
SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
LANE_FRAC = 0.1
SHRINK = 30
CLAMP = (0.25, 3.0)
LANE_MAX = 4000   # a row whose first point is below this net worth already has a lane point: left as it is


def lane_net_worth(sample, G):
    """{hero id: median net worth of its players at LANE_FRAC of the match}"""
    nw = {}
    for line in gzip.open(sample, "rt"):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] in G.heroes and L.gun_known(p):
                nw.setdefault(p["hero_id"], []).append(L.build_at(p, LANE_FRAC * m["duration_s"])[1])
    return {hid: statistics.median(v) for hid, v in nw.items()}


def run_audit(sample):
    path = os.path.join(tempfile.mkdtemp(), "audit")
    env = dict(os.environ, AUDIT_FIFTH_SOURCES="1", AUDIT_OUT=path)
    subprocess.run([sys.executable, os.path.join(HERE, "..", "damage_audit.py"), sample], env=env, check=True,
                   stdout=subprocess.DEVNULL)
    return path + ".json"


def lane_rows(audit, nws, old, G):
    """{hero id str: (net worth, real lane melee share, sim share, players, multiplier now)}"""
    rows = {}
    for hid, row in old["heroes"].items():
        a = audit["heroes"].get(row["name"])
        fs = a and a.get("fifth_sources")
        if not fs or not fs[0] or int(hid) not in nws:
            continue
        rs, ss = fs[0].get("MELEE", [0.0, 0.0])
        nw = round(nws[int(hid)])
        if row["points"][0][0] < LANE_MAX:   # already has a lane point (this script, or melee_phase.py --fracs 0.1,...)
            continue
        if rs > 0 and ss > 0 and nw < row["points"][0][0]:
            rows[hid] = (nw, rs, ss, a["players"], melee_phase_mult(int(hid), nw))
    return rows


def main():
    args = sys.argv[1:]
    sample = args[args.index("--sample") + 1] if "--sample" in args else SAMPLE
    audit_path = args[args.index("--audit") + 1] if "--audit" in args else run_audit(sample)
    G = game()
    old = json.load(open(OUT))
    rows = lane_rows(json.load(open(audit_path)), lane_net_worth(sample, G), old, G)
    w = sum(p[3] * p[1] for p in rows.values())
    pooled = sum(p[3] * p[1] * math.log(p[1] / p[2] * p[4]) for p in rows.values()) / w
    for hid, (nw, rs, ss, n, cur) in sorted(rows.items(), key=lambda x: old["heroes"][x[0]]["name"]):
        lr = (n * math.log(rs / ss * cur) + SHRINK * pooled) / (n + SHRINK)
        m = round(min(CLAMP[1], max(CLAMP[0], math.exp(lr))), 4)
        r = old["heroes"][hid]
        r["points"] = [[nw, m]] + r["points"]
        r["lane"] = {"real_melee": rs, "sim_melee": ss}
        print(f"{r['name']:14s} n{n:5d} nw {nw:5d} lane melee real {rs:.3f} sim {ss:.3f}  mult {cur:.2f} -> {m:.2f}")
    print("pooled lane ratio", round(math.exp(pooled), 3))
    if "--write" in args:
        old["pooled"]["0.1"] = round(math.exp(pooled), 4)   # numeric key: melee_phase.py --hero shrinks to the nearest frac
        old["lane_source"] = (f"{os.path.basename(sample)} damage audit lane fifth (AUDIT_FIFTH_SOURCES=1), "
                              "scripts/mechanics/melee_phase_lane.py")
        json.dump(old, open(OUT, "w"), indent=1)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
