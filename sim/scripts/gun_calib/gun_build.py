"""Gun share of damage by build and game phase, real vs the audit's duels (survey).

Per player-match and frac: the real gun share of the player's damage in the window frac +- WINDOW of the match
(damage_series) beside the sim's gun share in the audit duel at that frac (damage_audit.sim_player, AUDIT_SEEDS
draws), with the build's spirit lean (spirit items' souls / all items' souls at that time). Pooled real / sim gun
share (players weighted) per frac and spirit bin, the other kinds beside it, and the per-hero split.

usage: python3 gun_build.py [--sample PATH] [--window 0.05] [--parity even|odd] [--dump PATH] [--lean X] [workers]
       python3 gun_build.py --report PATH
"""
import collections
import gzip
import json
import os
import pickle
import random
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "mechanics"))
import damage_audit as D  # noqa: E402
import landing_rates as L  # noqa: E402
import melee_phase as MP  # noqa: E402
from deadsim import game  # noqa: E402

FRACS = (0.3, 0.6, 0.9)
WINDOW = 0.05
AUDIT_SEEDS = (0, 1)
SAMPLE = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
KINDS = ("gun", "ability", "item", "melee", "other")
BINS = (0.0, 0.2, 0.35, 0.5, 0.65, 1.01)


def spirit_souls(p, t):
    """(souls in spirit items, souls in all items) of the player's build at match time t"""
    G = game()
    items, _ = L.build_at(p, t)
    return sum(G.items[i].cost for i in items if G.items[i].slot == "spirit"), sum(G.items[i].cost for i in items)


def job(arg):
    m, slot = arg
    G = game()
    p = next(x for x in m["players"] if x["slot"] == slot)
    h = G.hero(p["hero_id"])
    classes = {a.class_name for a in h.abilities}
    T, tm = m["duration_s"], m["damage_times"]
    rows = []
    for fr in FRACS:
        real = collections.Counter()
        for k, ser in p["damage_series"].items():
            if k in L.CATEGORY:
                continue
            lo, hi = max(0.0, fr - WINDOW) * T, min(1.0, fr + WINDOW) * T
            real[D.kind(L.real_key(k, list(classes)), G, classes)] += MP.cum(tm, ser, hi) - MP.cum(tm, ser, lo)
        sim = collections.Counter()
        L.FRACS = (fr,)
        for seed in AUDIT_SEEDS:
            D.SEED = seed
            _, d, _ = D.sim_player((m, slot))
            tot = sum(v for k, v in d.items() if not k.startswith("_")) or 1.0
            for k, v in d.items():
                if not k.startswith("_"):
                    sim[D.kind(k, G, classes)] += v / tot / len(AUDIT_SEEDS)
        rt = sum(real.values())
        if rt <= 0:
            continue
        sp, tot = spirit_souls(p, fr * T)
        rows.append({"hero": p["hero_id"], "match": m["match_id"], "frac": fr, "lean": sp / tot if tot else 0.0, "spirit": sp,
                     "souls": L.build_at(p, fr * T)[1], "real": {k: real[k] / rt for k in KINDS},
                     "sim": {k: sim[k] for k in KINDS}, "real_dmg": rt})
    return rows


def main():
    args = sys.argv[1:]
    global WINDOW
    sample = args[args.index("--sample") + 1] if "--sample" in args else SAMPLE
    if "--window" in args:
        WINDOW = float(args[args.index("--window") + 1])
    par = None
    if "--parity" in args:
        par = 0 if args[args.index("--parity") + 1] == "even" else 1
    dump = args[args.index("--dump") + 1] if "--dump" in args else None
    if "--lean" in args:   # try a Mechanics.gun_lean (workers fork after this)
        import dataclasses
        D.MECH = dataclasses.replace(D.MECH, gun_lean=float(args[args.index("--lean") + 1]))
    pos = [a for i, a in enumerate(args) if a.isdigit() and (i == 0 or not args[i - 1].startswith('--'))]
    workers = int(pos[0]) if pos else os.cpu_count()
    G = game()
    jobs = []
    for line in gzip.open(sample):
        m = json.loads(line)
        if par is not None and m["match_id"] % 2 != par:
            continue
        for p in m["players"]:
            if p["hero_id"] in G.heroes and L.gun_known(p) and p.get("damage_series"):
                jobs.append((m, p["slot"]))
    random.Random(1).shuffle(jobs)
    rows = []
    with ProcessPoolExecutor(workers) as ex:
        for r in ex.map(job, jobs, chunksize=8):
            rows.extend(r)
    if dump:
        pickle.dump(rows, open(dump, "wb"))
    report(rows, G)


def report(rows, G):
    print("pooled real / sim share by spirit lean (spirit item souls / item souls)")
    for fr in FRACS:
        print(f"== {fr:.0%}")
        for lo, hi in zip(BINS, BINS[1:]):
            rs = [r for r in rows if r["frac"] == fr and lo <= r["lean"] < hi]
            if len(rs) < 20:
                continue
            line = " ".join(f"{k} {sum(r['real'][k] for r in rs) / len(rs):.3f}/{sum(r['sim'][k] for r in rs) / len(rs):.3f}"
                            for k in KINDS[:4])
            print(f" lean {lo:.2f}-{hi:.2f} n{len(rs):5d}  {line}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--report":
        report(pickle.load(open(sys.argv[2], "rb")), game())
    else:
        main()
