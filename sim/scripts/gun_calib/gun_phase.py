"""Gun damage per hero bullet hit by game phase, real vs the audit's duels (survey).

Real: gun damage on enemy heroes (damage_series) / hero_bullets_hit (stats) between frac - W and frac + W of the
match. Sim: the damage audit's duel at frac, gun damage / hits (Engine.damage hook as shot_damage.py). Shotgun pellet
counts make the levels differ per hero; the trend over the phases is what this is for.
--replays: per gun hit terms from the replays (fetch_gun_hits.py rows: damage, pre_damage, effectiveness = falloff,
crit_damage, damage_absorbed) against the same matches' audit duels: resist (damage / pre), falloff, crit share,
zero-damage hits, and the share of gun damage barriers absorb.
First used 2026-10-27 (validation/README.md "Gun damage late in the match"): the sim's gun per hit grew 1.15x from
30% to 90% of the match against real's; falloff and crits matched, resist + barriers did not (Mechanics.shred_uptime).

usage: python3 gun_phase.py [--sample PATH] [hero,hero] [workers]                  (~1 min on 4 cores)
       python3 gun_phase.py --replays <fetch_gun_hits work dir> [workers]
"""
import collections
import gzip
import json
import math
import os
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import damage_audit as A  # noqa: E402
import landing_rates as L  # noqa: E402
from deadsim import engine, game  # noqa: E402

FRACS = (0.3, 0.6, 0.9)
W = 0.1
SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
_acc = collections.Counter()
_damage, _bullet = engine.Engine.damage, engine.Engine.bullet_damage
_frac = [None]
_last = {}


def _counted_bullet(self, f, extra_pct=0.0):
    per, crit = _bullet(self, f, extra_pct)
    if self.fighters and f is self.fighters[0]:
        _last["base"] = f.st.bullet_damage * (1.0 + f.weapon_pct() + extra_pct)
        _last["fall"] = self.hit_falloff(f.st)
    return per, crit


def _counted_damage(self, src, dst, raw, kind, source, *a, **k):
    mine = bool(self.fighters) and src is self.fighters[0]
    bar0 = sum(b[0] for b in dst.barriers if b[1] > self.t and b[0] > 0) if mine else 0.0
    amt = _damage(self, src, dst, raw, kind, source, *a, **k)
    if mine:
        absorbed = max(0.0, bar0 - sum(b[0] for b in dst.barriers if b[1] > self.t and b[0] > 0))
        _acc[("all", _frac[0])] += amt or 0.0
        _acc[("all_abs", _frac[0])] += absorbed
        if source == "gun" and k.get("book") is None:
            _acc[("gun_abs", _frac[0])] += absorbed
    if source == "gun" and k.get("book") is None and self.fighters and src is self.fighters[0]:
        fr = _frac[0]
        _acc[("dmg", fr)] += amt or 0.0
        if amt:
            h = k.get("hits", 0) or 0
            _acc[("hits", fr)] += h
            _acc[("raw", fr)] += raw
            res = engine.combine_resist(dst.bullet_resists(), list(src.st.bullet_shred) + dst.mods.values("bullet_shred"))
            _acc[("keep", fr)] += raw * (1.0 - res)
            _acc[("keep_st", fr)] += raw * (1.0 - engine.combine_resist(dst.st.bullet_resist, src.st.bullet_shred))
            _acc[("keep_res", fr)] += raw * (1.0 - engine.combine_resist(dst.bullet_resists(), src.st.bullet_shred))
            _acc[("heads", fr)] += k.get("headshots", 0) or 0
            _acc[("base", fr)] += _last.get("base", 0.0) * h
            _acc[("fall", fr)] += _last.get("fall", 0.0) * h
    return amt


def sim_job(job):
    out = {}
    engine.Engine.damage, engine.Engine.bullet_damage = _counted_damage, _counted_bullet
    try:
        for fr in FRACS:
            _acc.clear()
            _frac[0] = fr
            L.FRACS = (fr,)
            A.sim_player(job)
            out[fr] = (_acc[("dmg", fr)], _acc[("hits", fr)],
                       {x: _acc[(x, fr)] for x in ("raw", "heads", "base", "fall", "all", "all_abs", "gun_abs", "keep", "keep_st", "keep_res")})
    finally:
        engine.Engine.damage, engine.Engine.bullet_damage = _damage, _bullet
    return out


def interp(ts, vs, t):
    if t <= ts[0]:
        return vs[0] * t / ts[0]
    for i in range(1, len(ts)):
        if t <= ts[i]:
            return vs[i - 1] + (vs[i] - vs[i - 1]) * (t - ts[i - 1]) / (ts[i] - ts[i - 1])
    return vs[-1]


def real_row(m, p, G):
    T, tm = m["duration_s"], m["damage_times"]
    classes = list({ab.class_name for ab in G.hero(p["hero_id"]).abilities})
    st = sorted(p["stats"], key=lambda s: s["time_stamp_s"])
    sts = [s["time_stamp_s"] for s in st]
    hits = [s["hero_bullets_hit"] for s in st]
    out = {}
    for fr in FRACS:
        lo, hi = max(0.0, fr - W) * T, min(1.0, fr + W) * T
        g = 0.0
        for k, ser in p["damage_series"].items():
            if k in L.CATEGORY or A.kind(L.real_key(k, classes), G, set(classes)) != "gun":
                continue
            g += interp(tm, ser, hi) - interp(tm, ser, lo)
        out[fr] = (g, interp(sts, hits, hi) - interp(sts, hits, lo))
    return out


def main():
    args = [a for a in sys.argv[1:]]
    if "--replays" in args:
        i = args.index("--replays")
        return replays_main(args[i + 1], int(args[i + 2]) if len(args) > i + 2 else os.cpu_count())
    sample = SAMPLE
    if "--sample" in args:
        i = args.index("--sample")
        sample = args[i + 1]
        del args[i:i + 2]
    G = game()
    heroes = set(G.heroes) if not args or args[0] == "all" else {G.hero(x.strip()).id for x in args[0].split(",")}
    workers = int(args[1]) if len(args) > 1 else os.cpu_count()
    jobs, reals = [], []
    for line in gzip.open(sample, "rt"):
        m = json.loads(line)
        for p in m["players"]:
            if p["hero_id"] in heroes and L.gun_known(p) and p.get("stats"):
                jobs.append((m, p["slot"]))
                reals.append((p["hero_id"], real_row(m, p, G)))
    per = collections.defaultdict(lambda: collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0.0]))
    with ProcessPoolExecutor(workers) as ex:
        for (hid, r), s in zip(reals, ex.map(sim_job, jobs, chunksize=4)):
            for fr in FRACS:
                if r[fr][1] > 0 and s[fr][1] > 0:
                    a = per[hid][fr]
                    a[0] += r[fr][0]; a[1] += r[fr][1]; a[2] += s[fr][0]; a[3] += s[fr][1]
    pool = collections.defaultdict(list)
    print("hero            real/sim dmg per hit at " + " / ".join(f"{f:.0%}" for f in FRACS) + "   (sim/real ratio)")
    for hid, d in sorted(per.items(), key=lambda x: G.hero(x[0]).name):
        cells, rat = [], []
        for fr in FRACS:
            a = d[fr]
            if a[1] and a[3]:
                rp, sp = a[0] / a[1], a[2] / a[3]
                cells.append(f"{rp:6.1f}/{sp:6.1f}={sp / rp:4.2f}")
                rat.append(sp / rp)
            else:
                cells.append(" " * 18)
        if len(rat) == len(FRACS):
            for fr, x in zip(FRACS, rat):
                pool[fr].append(math.log(x))
            print(f"{G.hero(hid).name:14s} " + "  ".join(cells) + f"   late/early {rat[-1] / rat[0]:.2f}")
    print("geo mean sim/real per hit:", "  ".join(f"{fr:.0%} {math.exp(statistics.mean(v)):.3f}" for fr, v in pool.items()))



# ---- replays: per-hit terms (fetch_gun_hits.py rows) ----------------------------------------------------------------
REPLAY_BINS = ((0.2, 0.4), (0.5, 0.7), (0.8, 1.01))
CAST_RAW = "/mnt/project-files/analysis/work/cast_timing/raw"


def replay_terms(work, sample=SAMPLE):
    """{hero id: {bin: Counter(hits, dmg, pre, eff, crit, zero)}} over the replay gun hits on enemy heroes, and the
    sample's matches that have replays {match id: match}."""
    sys.path.insert(0, os.path.join(ROOT, "scripts", "cast_timing"))
    import fit_cast_timing as CT
    ms = {}
    raw = os.path.join(work, "raw")
    ids = {int(f.split(".")[0]) for f in os.listdir(raw) if f.endswith(".ndjson.gz")}
    for line in gzip.open(sample, "rt"):
        m = json.loads(line)
        if m["match_id"] in ids:
            ms[m["match_id"]] = m
    out = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for mid, m in ms.items():
        cf = os.path.join(CAST_RAW, f"{mid}.ndjson.gz")
        if not os.path.exists(cf):
            continue
        cr = CT.real_casts([json.loads(x) for x in gzip.open(cf, "rt")])
        if not cr:
            continue
        off = statistics.median([r["tick"] / CT.T - r["v"] for r in cr])
        rows = [json.loads(x) for x in gzip.open(os.path.join(raw, f"{mid}.ndjson.gz"), "rt")]
        hero = {r["a"]: int(r["s"]) for r in rows if r["k"] == "ctl"}
        T = m["duration_s"]
        for r in rows:
            if r["k"] != "dmg":
                continue
            att, vic = divmod(r["a"], 100000)
            hid = hero.get(att)
            if hid is None or vic not in hero:
                continue
            fr = (r["tick"] / CT.T - off) / T
            b = next((b for b in REPLAY_BINS if b[0] <= fr < b[1]), None)
            if b is None:
                continue
            parts = r["s"].split("|")
            _, pre, eff, crit = parts[:4]
            ab = float(parts[7] or 0) if len(parts) > 7 else 0.0
            if ab > 1e6:   # immune (invulnerable): the whole hit
                ab = float(pre or 0)
            c = out[hid][b]
            c["abs"] += ab
            c["hits"] += 1
            c["dmg"] += r["v"]
            c["pre"] += float(pre or 0)
            c["eff"] += float(eff or 0)
            c["crit"] += float(crit or 0) > 0
            c["zero"] += r["v"] <= 0
    return out, ms


def replays_main(work, workers):
    G = game()
    real, ms = replay_terms(work)
    jobs = [(m, p["slot"]) for m in ms.values() for p in m["players"] if p["hero_id"] in G.heroes and L.gun_known(p)]
    sim = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    with ProcessPoolExecutor(workers) as ex:
        for (m, slot), s in zip(jobs, ex.map(sim_job, jobs, chunksize=4)):
            hid = next(p["hero_id"] for p in m["players"] if p["slot"] == slot)
            for fr, b in zip(FRACS, REPLAY_BINS):
                d, h, x = s[fr]
                c = sim[hid][b]
                c["hits"] += h; c["dmg"] += d
                for k, v in x.items():
                    c[k] += v
    print(f"{len(ms)} replay matches; per hit real / sim by match fraction {REPLAY_BINS} (sim duels at {FRACS})")
    print("columns: dmg per hit, resist (dmg/pre), falloff, crit share, zero-damage share")
    pooled = collections.defaultdict(lambda: collections.defaultdict(list))
    for hid in sorted(real, key=lambda h: G.hero(h).name if h in G.heroes else ""):
        if hid not in G.heroes or hid not in sim:
            continue
        cells = []
        for b in REPLAY_BINS:
            r, s = real[hid][b], sim[hid][b]
            if r["hits"] < 50 or s["hits"] <= 0:
                cells.append(None)
                continue
            rv = (r["dmg"] / r["hits"], r["dmg"] / max(r["pre"], 1e-9), r["eff"] / r["hits"], r["crit"] / r["hits"],
                  r["zero"] / r["hits"])
            sv = (s["dmg"] / s["hits"], s["dmg"] / max(s["raw"], 1e-9), s["fall"] / s["hits"], s["heads"] / s["hits"], 0.0)
            cells.append((rv, sv))
            for i, k in enumerate(("per_hit", "resist", "falloff", "crit")):
                pooled[b][k].append((math.log(sv[i] / rv[i]) if rv[i] > 0 and sv[i] > 0 else 0.0, r["hits"]))
        if any(c is None for c in cells):
            continue
        print(f"{G.hero(hid).name:14s} " + " | ".join(
            f"{rv[0]:5.1f}/{sv[0]:5.1f} r{rv[1]:.2f}/{sv[1]:.2f} f{rv[2]:.2f}/{sv[2]:.2f} c{rv[3]:.2f}/{sv[3]:.2f} z{rv[4]:.2f}"
            for rv, sv in cells))
    for b in REPLAY_BINS:
        print(b, "hit-weighted geo mean sim/real:", "  ".join(
            f"{k} {math.exp(sum(x * w for x, w in v) / sum(w for _, w in v)):.3f}" for k, v in pooled[b].items()))
    for b in REPLAY_BINS:   # pooled real terms
        t = collections.Counter()
        for hid in real:
            t.update(real[hid][b])
        u = collections.Counter()
        for hid in sim:
            u.update(sim[hid][b])
        print(b, f"pooled real absorbed share {t['abs'] / (t['dmg'] + t['abs']):.3f} resist w/o absorbed "
                 f"{(t['dmg'] + t['abs']) / t['pre']:.3f} | sim absorbed share {u['gun_abs'] / u['dmg']:.3f} "
                 f"resist w/o absorbed {u['dmg'] / u['raw']:.3f} (target resists only {u['keep'] / u['raw']:.3f})")
        print(b, f"pooled real resist {t['dmg'] / t['pre']:.3f} falloff {t['eff'] / t['hits']:.3f} crit {t['crit'] / t['hits']:.3f} "
                 f"zero {t['zero'] / t['hits']:.3f} | sim resist {u['dmg'] / u['raw']:.3f} falloff {u['fall'] / u['hits']:.3f} "
                 f"crit {u['heads'] / u['hits']:.3f}")


if __name__ == "__main__":
    main()
