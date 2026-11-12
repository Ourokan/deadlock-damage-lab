"""Sinclair's copied ultimate: damage per Audience Participation cast by her net worth, real vs the audit duels (2026-11-12).

Real: fight_length raw DamageEvents of Sinclair's pawn from another hero's ultimate within COPY_S s of each Audience
Participation cast (cast_timing raw; replays book the copy under the copied hero's ultimate class), at her net worth
from the match's stats (cast_timing offset). Sim (--sim): the damage audit's duels of Sinclair players at FRACS of the
match with Mechanics.copy_ult_phase off, copy damage per cast and her net worth at the cast.
rel(bin) = real per cast / sim per cast at the bin's mean net worth (sim linear in ln net worth between its points,
flat below, its last segment extended above), scaled so the sim's damage-weighted mean rel is 1 (the Audience Participation corr carries the level).
data/copy_ult_phase.json: bins (Mechanics.copy_ult_phase, mechanics.copy_ult_phase_mult).

usage: python3 copy_ult_phase.py real [--parity even|odd]
       python3 copy_ult_phase.py write SAMPLE [max_players=150] [workers=4]   (real + sim, writes the file)
       python3 copy_ult_phase.py rebin   (real bins against the file's sim rows)
"""
import bisect
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
for p in (ROOT, os.path.join(ROOT, "scripts"), os.path.join(ROOT, "scripts", "cast_timing"),
          os.path.join(ROOT, "scripts", "fight_length")):
    sys.path.insert(0, p)
from deadsim import engine, game  # noqa: E402
from deadsim.heroes import magician  # noqa: E402

OUT = os.path.join(ROOT, "data", "copy_ult_phase.json")
COPY_S = 12.0   # the copy window (CopiedUltWindow 9 s) + cast delay + a DoT's tail
BINS = (0, 9500, 16500, 25000, 32000, 10 ** 9)
FRACS = (0.15, 0.3, 0.45, 0.6, 0.9)


def real(parity=None):
    import fit_cast_timing as CT
    import fit_length as FL
    import opener_timing as OT
    G = game()
    sin = G.hero("Sinclair")
    cid = next(a.id for a in sin.abilities if a.class_name == "ability_magician_copyult")
    ults = {a.id for h in G.heroes.values() for a in h.abilities if a.ultimate and h.id != sin.id}
    mids = {f.split(".")[0] for f in os.listdir(CT.CASTS)} & {f.split(".")[0] for f in os.listdir(CT.FIGHTS)}
    if parity:
        mids = {m for m in mids if (int(m) % 2 == 0) == (parity == "even")}
    sample = FL.load_sample(CT.SAMPLE, mids)
    rows = []
    for mid in sorted(mids):
        m = sample.get(mid)
        p = m and next((p for p in m["players"] if p["hero_id"] == sin.id), None)
        if p is None:
            continue
        hero, ev = OT.read(os.path.join(CT.FIGHTS, f"{mid}.ndjson.gz"))
        cr = CT.real_casts([json.loads(x) for x in gzip.open(os.path.join(CT.CASTS, f"{mid}.ndjson.gz"), "rt")])
        if not cr:
            continue
        off = statistics.median(r["tick"] / CT.T - r["v"] for r in cr)
        st = sorted(p["stats"], key=lambda s: s["time_stamp_s"])
        ts = [s["time_stamp_s"] for s in st]
        pawns = {k for k, v in hero.items() if v == sin.id}
        for r in cr:
            if int(r["s"]) != cid or r["a"] not in pawns:
                continue
            c = r["tick"] / CT.T
            d = sum(e[5] for e in ev if e[1] == r["a"] and c <= e[0] <= c + COPY_S and e[6] in ults)
            i = max(0, min(len(st) - 1, bisect.bisect_left(ts, c - off)))
            rows.append((st[i]["net_worth"], d))
    out = []
    for lo, hi in zip(BINS, BINS[1:]):
        v = [x for x in rows if lo <= x[0] < hi]
        if v:
            out.append({"net_worth": round(statistics.mean(x[0] for x in v)),
                        "real": round(statistics.mean(x[1] for x in v), 1), "casts": len(v)})
    return out


_acc = collections.Counter()
_cur = [None]


def _sim_job(job):
    import damage_audit as A
    import landing_rates as L
    cast0, dmg0 = magician.AudienceParticipation.cast, engine.Engine.damage

    def cast(self, c, *a, **k):
        if c.engine.fighters and c.me is c.engine.fighters[0]:
            _acc[(_cur[0], "casts")] += 1
            _acc[(_cur[0], "nw")] += c.me.st.souls or 0
        return cast0(self, c, *a, **k)

    def damage(self, src, dst, raw, kind, source, *a, **k):
        amt = dmg0(self, src, dst, raw, kind, source, *a, **k)
        if isinstance(source, str) and source.startswith("Audience Participation (") and self.fighters \
                and src is self.fighters[0]:
            _acc[(_cur[0], "dmg")] += amt or 0
        return amt

    magician.AudienceParticipation.cast, engine.Engine.damage = cast, damage
    out = {}
    for fr in FRACS:
        _acc.clear()
        _cur[0] = fr
        L.FRACS = (fr,)
        A.sim_player(job)
        out[fr] = dict(_acc)
    return out


def sim(sample, cap, workers):
    import landing_rates as L
    from deadsim import mechanics as M
    M.DEFAULT.copy_ult_phase = False   # the duels' own copies, before the curve
    sid = game().hero("Sinclair").id
    jobs = []
    for line in gzip.open(sample, "rt"):
        m = json.loads(line)
        jobs += [(m, p["slot"]) for p in m["players"] if p["hero_id"] == sid and L.gun_known(p)]
    tot = collections.Counter()
    with ProcessPoolExecutor(workers) as ex:
        for s in ex.map(_sim_job, jobs[:cap], chunksize=2):
            for d in s.values():
                tot.update(d)
    return [{"frac": fr, "net_worth": round(tot[(fr, "nw")] / tot[(fr, "casts")]),
             "per_cast": round(tot[(fr, "dmg")] / tot[(fr, "casts")], 1), "casts": tot[(fr, "casts")],
             "dmg": round(tot[(fr, "dmg")])} for fr in FRACS if tot[(fr, "casts")] >= 100]


def interp_ln(pts, x, extend=False):
    """Linear in ln x between points; flat outside, or (extend) the end segments' lines past the last point (the sim's
    copy keeps growing past its 0.9 duels' ~29k, where the real top bin sits)."""
    x = math.log(x)
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    if extend:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        return y1 + (y1 - y0) * (x - x1) / (x1 - x0)
    return pts[-1][1]


def rel(bins, sims):
    sp = [(math.log(s["net_worth"]), s["per_cast"]) for s in sims]
    for b in bins:
        b["sim"] = round(interp_ln(sp, b["net_worth"], extend=True), 1)
        b["raw"] = b["real"] / b["sim"]
    rp = [(math.log(b["net_worth"]), b["raw"]) for b in bins]
    norm = sum(s["dmg"] * interp_ln(rp, s["net_worth"]) for s in sims) / sum(s["dmg"] for s in sims)
    for b in bins:
        b["rel"] = round(b.pop("raw") / norm, 4)
    return bins


def main():
    a = sys.argv[1:]
    if a and a[0] == "rebin":   # recompute rel from the file's sim rows (no duels)
        d = json.load(open(OUT))
        d["bins"] = rel(real(), d["sim"])
        json.dump(d, open(OUT, "w"), indent=2)
        for b in d["bins"]:
            print(b)
        return
    if a and a[0] == "write":
        bins, sims = real(), sim(a[1], int(a[2]) if len(a) > 2 else 150, int(a[3]) if len(a) > 3 else 4)
        d = {"source": "scripts/mechanics/copy_ult_phase.py (fight_length + cast_timing raw replays; damage audit duels)",
             "note": "copy damage x rel(nw) at Sinclair's net worth, linear in ln nw between bins, flat outside",
             "sim": sims, "bins": rel(bins, sims)}
        json.dump(d, open(OUT, "w"), indent=2)
        for b in d["bins"]:
            print(b)
        return
    parity = a[a.index("--parity") + 1] if "--parity" in a else None
    for b in real(parity):
        print(b)


if __name__ == "__main__":
    main()
