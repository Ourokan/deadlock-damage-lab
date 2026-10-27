"""Bullet resist in fights: what real gun hits keep vs the target's build resist, and the same for the audit's duels
(Mechanics.shred_uptime fit, 2026-10-27).

Real (fetch_gun_hits.py rows): per gun hit (damage + damage_absorbed) / pre_damage over 1 - the target's build bullet
resist after the shooter's build shred (compute_stats at that time); pre_damage is before resists. Sim: the audit's duel
gun hits, damage before the barrier over pre-resist damage (raw x the shooter's damage amps) over the same build term.
1.0 = the fight adds nothing to the build resist; shred debuffs push it up, in-fight resist buffs down. Real 0.99 /
0.99 / 0.98 at 30 / 60 / 90% of the match, sim 1.01 / 1.04 / 1.05 with every shred debuff in full.
Prints per phase and per shooting hero (late: >= 50% of the match, sim duels at 60 / 90%), and with --sim the
hits-weighted rmse of the per hero ratios.

usage: python3 resist_check.py <fetch_gun_hits work dir> [--parity 0|1] [--sim] [--uptime K] [workers]
"""
import collections
import dataclasses
import functools
import gzip
import json
import math
import os
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path[:0] = [ROOT, os.path.join(ROOT, "scripts"), os.path.join(ROOT, "scripts", "cast_timing"), HERE]
import fit_cast_timing as CT  # noqa: E402
import gun_phase as GP  # noqa: E402
import landing_rates as L  # noqa: E402
from deadsim import engine, game  # noqa: E402
from deadsim.build import combine_resist, compute_stats  # noqa: E402

LATE = 0.5


@functools.lru_cache(maxsize=None)
def _stats(hid, items, souls):
    return compute_stats(game().hero(hid), list(items), souls=souls)


def keep_of(byh, ah, vh, t):
    vi, vs = L.build_at(byh[vh], t)
    ai, as_ = L.build_at(byh[ah], t)
    return 1.0 - combine_resist(_stats(vh, tuple(sorted(vi)), vs).bullet_resist,
                                _stats(ah, tuple(sorted(ai)), as_).bullet_shred)


def real(work, parity):
    """{("phase", bin) | ("hero", name): [kept damage, build-allowed damage]} over the replays' gun hits."""
    G = game()
    raw = os.path.join(work, "raw")
    ids = {int(f.split(".")[0]) for f in os.listdir(raw) if f.endswith(".ndjson.gz")}
    acc = collections.defaultdict(lambda: [0.0, 0.0])
    for line in gzip.open(GP.SAMPLE, "rt"):
        m = json.loads(line)
        mid = m["match_id"]
        if mid not in ids or (parity is not None and mid % 2 != parity):
            continue
        cf = os.path.join(GP.CAST_RAW, f"{mid}.ndjson.gz")
        cr = CT.real_casts([json.loads(x) for x in gzip.open(cf, "rt")]) if os.path.exists(cf) else []
        if not cr:
            continue
        off = statistics.median([r["tick"] / CT.T - r["v"] for r in cr])
        rows = [json.loads(x) for x in gzip.open(os.path.join(raw, f"{mid}.ndjson.gz"), "rt")]
        hero = {r["a"]: int(r["s"]) for r in rows if r["k"] == "ctl"}
        byh = {p["hero_id"]: p for p in m["players"]}
        for r in rows:
            if r["k"] != "dmg":
                continue
            att, vic = divmod(r["a"], 100000)
            ah, vh = hero.get(att), hero.get(vic)
            if ah not in byh or vh not in byh or ah not in G.heroes or vh not in G.heroes:
                continue
            parts = r["s"].split("|")
            pre = float(parts[1] or 0)
            if pre <= 0 or len(parts) < 8:
                continue
            ab = float(parts[7] or 0)
            ab = pre if ab > 1e6 else ab   # immune: the whole hit
            t = r["tick"] / CT.T - off
            b = next((b for b in GP.REPLAY_BINS if b[0] <= t / m["duration_s"] < b[1]), None)
            if b is None:
                continue
            k = keep_of(byh, ah, vh, t) * pre
            keys = [("phase", b)] + ([("hero", G.hero(ah).name)] if t / m["duration_s"] >= LATE else [])
            for key in keys:
                acc[key][0] += r["v"] + ab
                acc[key][1] += k
    return acc


_acc = collections.Counter()
_damage = engine.Engine.damage
_frac = [None]


def _hook(self, src, dst, raw, kind, source, *a, **k):
    on = source == "gun" and self.fighters and src is self.fighters[0] and k.get("book") is None \
        and not k.get("ignore_resist")
    if on:
        pre = raw * src.st.outgoing_mult * (1.0 - src.stat("outgoing_penalty")) * (1.0 + src.stat("damage_amp"))
        allowed = pre * (1.0 - combine_resist(dst.st.bullet_resist, src.st.bullet_shred))
    amt = _damage(self, src, dst, raw, kind, source, *a, **k)
    if on and amt:
        for key in [("phase", _frac[0])] + ([("hero", src.st.hero.name)] if _frac[0] >= LATE else []):
            _acc[key + ("kept",)] += amt
            _acc[key + ("allowed",)] += allowed
    return amt


def sim_job(job):
    _acc.clear()
    engine.Engine.damage = _hook
    try:
        for fr in GP.FRACS:
            _frac[0] = fr
            L.FRACS = (fr,)
            GP.A.sim_player(job)
    finally:
        engine.Engine.damage = _damage
    return dict(_acc)


def sim(parity, workers):
    jobs = []
    for line in gzip.open(GP.SAMPLE, "rt"):
        m = json.loads(line)
        if parity is not None and m["match_id"] % 2 != parity:
            continue
        jobs += [(m, p["slot"]) for p in m["players"] if L.gun_known(p)]
    t = collections.Counter()
    with ProcessPoolExecutor(workers) as ex:
        for s in ex.map(sim_job, jobs, chunksize=4):
            t.update(s)
    out = collections.defaultdict(lambda: [0.0, 0.0])
    for k, v in t.items():
        out[k[:-1]][0 if k[-1] == "kept" else 1] += v
    return out


def main():
    args = sys.argv[1:]
    work = args.pop(0)
    parity = None
    if "--parity" in args:
        i = args.index("--parity")
        parity = int(args[i + 1])
        del args[i:i + 2]
    do_sim = "--sim" in args
    if do_sim:
        args.remove("--sim")
    if "--uptime" in args:
        i = args.index("--uptime")
        GP.A.MECH = dataclasses.replace(GP.A.MECH, shred_uptime=float(args[i + 1]))
        del args[i:i + 2]
    workers = int(args[0]) if args else os.cpu_count()
    r = real(work, parity)
    s = sim(parity, workers) if do_sim else {}
    print("kept / build-allowed gun damage, real" + (f" | sim (shred_uptime {GP.A.MECH.shred_uptime})" if do_sim else ""))
    for b, fr in zip(GP.REPLAY_BINS, GP.FRACS):
        a = r[("phase", b)]
        line = f"  match {b[0]:.0%}-{min(1.0, b[1]):.0%}: real {a[0] / a[1]:.3f}"
        if do_sim:
            x = s[("phase", fr)]
            line += f" | sim at {fr:.0%} {x[0] / x[1]:.3f}"
        print(line)
    heroes = sorted(k[1] for k in r if k[0] == "hero" and r[k][1] > 30000)
    print(f"per shooting hero, >= {LATE:.0%} of the match:")
    num = den = 0.0
    for h in heroes:
        a = r[("hero", h)]
        line = f"  {h:14s} real {a[0] / a[1]:.3f}"
        if do_sim and s.get(("hero", h), [0, 0])[1]:
            x = s[("hero", h)]
            line += f"  sim {x[0] / x[1]:.3f}"
            num += a[1] * (x[0] / x[1] - a[0] / a[1]) ** 2
            den += a[1]
        print(line)
    if den:
        print(f"per hero rmse (weighted by real build-allowed damage): {math.sqrt(num / den):.4f}")


if __name__ == "__main__":
    main()
