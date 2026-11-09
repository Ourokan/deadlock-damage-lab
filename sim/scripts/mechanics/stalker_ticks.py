"""Stalker's DoT ticks per proc by the holder's net worth, real (replays) vs the audit duels (2026-11-09).

Real: fight_length raw DamageEvents (ability id = Stalker's item id), per attacker x victim; ticks 0.5 s apart, a new
proc after a 0.75 s gap or 10 ticks; the attacker's net worth from the match's stats at the proc (cast_timing raw for
the replay clock offset). Sim (--sim): the damage audit's duels of Stalker holders at 30 / 60 / 90% of the match, ticks
dealt per proc (deaths cut them). data/stalker_ticks.json: real bins + sim_ticks (Mechanics.stalker_ticks).

usage: python3 stalker_ticks.py real [--sample PATH,...] [--parity even|odd] [--write]
       python3 stalker_ticks.py sim SAMPLE [workers=4] [max_players=1500]
"""
import bisect
import collections
import gzip
import json
import os
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
for p in (ROOT, os.path.join(ROOT, "scripts"), os.path.join(ROOT, "scripts", "cast_timing")):
    sys.path.insert(0, p)
from deadsim import engine, game, items_fx  # noqa: E402

RAW = "/mnt/project-files/analysis/work/fight_length/raw"
CAST_RAW = "/mnt/project-files/analysis/work/cast_timing/raw"
OUT = os.path.join(ROOT, "data", "stalker_ticks.json")
BINS = [(0, 6000), (6000, 12000), (12000, 20000), (20000, 30000), (30000, 1e9)]
T = 64


def stalker_id():
    return next(i for i, it in game().items.items() if it.class_name == "upgrade_weapon_backstabber")


def real(samples, parity=None):
    import fit_cast_timing as CT
    sid = str(stalker_id())
    ms = {}
    for fn in samples:
        for line in gzip.open(fn, "rt"):
            m = json.loads(line)
            ms[m["match_id"]] = m
    res = collections.defaultdict(list)
    for f in os.listdir(RAW):
        mid = int(f.split(".")[0])
        m = ms.get(mid)
        if m is None or not os.path.exists(f"{CAST_RAW}/{f}"):
            continue
        if parity and (mid % 2 == 0) != (parity == "even"):
            continue
        cr = CT.real_casts([json.loads(x) for x in gzip.open(f"{CAST_RAW}/{f}", "rt")])
        if not cr:
            continue
        off = statistics.median([r["tick"] / CT.T - r["v"] for r in cr])
        rows = [json.loads(x) for x in gzip.open(os.path.join(RAW, f), "rt")]
        hero = {r["a"]: int(r["s"]) for r in rows if r["k"] == "ctl"}
        byh = {p["hero_id"]: p for p in m["players"]}
        ev = collections.defaultdict(list)
        for r in rows:
            if r["k"] == "dmg" and r.get("s", "").split("|")[0] == sid:
                ev[r["a"]].append(r["tick"])
        for a, ticks in ev.items():
            p = byh.get(hero.get(a // 100000))
            if p is None:
                continue
            st = sorted(p["stats"], key=lambda s: s["time_stamp_s"])
            ts = [s["time_stamp_s"] for s in st]
            ticks.sort()
            bursts, cur = [], None
            for t in ticks:
                if cur is None or t - cur[-1] > 0.75 * T or len(cur) >= 10:
                    if cur:
                        bursts.append(cur)
                    cur = [t]
                else:
                    cur.append(t)
            if cur:
                bursts.append(cur)
            for b in bursts:
                i = max(0, min(len(st) - 1, bisect.bisect_left(ts, b[0] / T - off)))
                nw = st[i]["net_worth"]
                k = next(j for j, (lo, hi) in enumerate(BINS) if lo <= nw < hi)
                res[k].append((len(b), nw))
    out = []
    for k in sorted(res):
        v = res[k]
        out.append({"net_worth": round(sum(x[1] for x in v) / len(v)), "ticks": round(sum(x[0] for x in v) / len(v), 2),
                    "procs": len(v)})
    return out


_acc = collections.Counter()
_cur = [None]


def _sim_job(job):
    import damage_audit as A
    import landing_rates as L
    use0, dmg0 = items_fx.Stalker.use, engine.Engine.damage

    def use(self, *a, **k):
        if self.f.e.fighters and self.f is self.f.e.fighters[0]:
            _acc[(_cur[0], "procs")] += 1
        return use0(self, *a, **k)

    def damage(self, src, dst, raw, kind, source, *a, **k):
        amt = dmg0(self, src, dst, raw, kind, source, *a, **k)
        if source == "Stalker" and self.fighters and src is self.fighters[0] and (amt or 0) > 0:
            _acc[(_cur[0], "ticks")] += 1
        return amt

    items_fx.Stalker.use, engine.Engine.damage = use, damage
    out = {}
    for fr in (0.3, 0.6, 0.9):
        _acc.clear()
        _cur[0] = fr
        L.FRACS = (fr,)
        A.sim_player(job)
        out[fr] = dict(_acc)
    return out


def sim(sample, workers, cap):
    import landing_rates as L
    from deadsim import mechanics as M
    M.DEFAULT.stalker_ticks = False   # the duels' own ticks, before the curve
    sid = stalker_id()
    jobs = []
    for line in gzip.open(sample, "rt"):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] in game().heroes and L.gun_known(p) and any(i[0] == sid for i in p["items"]):
                jobs.append((m, p["slot"]))
    tot = collections.Counter()
    with ProcessPoolExecutor(workers) as ex:
        for s in ex.map(_sim_job, jobs[:cap], chunksize=4):
            for fr, d in s.items():
                for k, v in d.items():
                    tot[k] += v
    return {fr: tot[(fr, "ticks")] / max(1, tot[(fr, "procs")]) for fr in (0.3, 0.6, 0.9)}


def main():
    args = sys.argv[1:]
    if args and args[0] == "sim":
        print(sim(args[1], int(args[2]) if len(args) > 2 else 4, int(args[3]) if len(args) > 3 else 1500))
        return
    samples = [os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")]
    if "--sample" in args:
        samples = args[args.index("--sample") + 1].split(",")
    parity = args[args.index("--parity") + 1] if "--parity" in args else None
    bins = real(samples, parity)
    for b in bins:
        print(b)
    if "--write" in args:
        d = json.load(open(OUT))
        d["bins"] = bins
        json.dump(d, open(OUT, "w"), indent=2)
        print("wrote", OUT, "(sim_ticks kept:", d["sim_ticks"], ")")


if __name__ == "__main__":
    main()
