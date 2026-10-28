"""Sinclair's copied ultimates, real vs sim per copied ultimate, for Mechanics.copy_ult (data/copy_ult.json).

The real damage matrix books a copy under the copied hero's own ability class (landing_rates.real_key folds them all
into Audience Participation); the sim books it as "Audience Participation (<ultimate>)". For each enemy ultimate X:
real share = Sinclair's damage from X's classes / all her damage to heroes, sim share = the same over the damage
audit's duels (damage_audit.sim_player, so the same model, foes and duel times as the audit). The factor moves X's
part of the copy damage toward real, inside Audience Participation (its own length_corr keeps the level):

    factor = old x (real share of X in all copies / sim share of X in all copies) ^ (n / (n + PRIOR))

n = Sinclair players facing X; ratios floored at FLOOR (a copy whose real damage is booked elsewhere, e.g. Bullet Dance
on Sinclair's own gun), factors clipped to CLIP, then scaled so the sim's copy damage keeps its total. Run a few
rounds (each reads the factors it wrote), with Audience Participation's corr refit between them
(ability_corr_heroes.py).

usage: python3 scripts/mechanics/copy_ult.py <sample.jsonl.gz> [--write] [--workers N]   (from sim/)
"""
import collections
import concurrent.futures as cf
import gzip
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
import damage_audit as D  # noqa: E402
import landing_rates as L  # noqa: E402
from deadsim.data import game  # noqa: E402
from deadsim.heroes import magician  # noqa: E402

PATH = os.path.join(ROOT, "data", "copy_ult.json")
SINCLAIR = 60
PRIOR = 40
FLOOR = 0.1
CLIP = (0.1, 10.0)
AGG = ("Bullet", "Ability", "Melee", "Misc")
PREFIX = "Audience Participation ("
_SIM_KEY = L.sim_key


def owner_ult(G):
    """(ability class -> owner hero's ultimate class, hero codename -> ultimate class, ult name -> class)."""
    by_class, by_code, by_name = {}, {}, {}
    for h in G.heroes.values():
        u = next((a for a in h.abilities if a.ultimate), None)
        if u is None:
            continue
        by_name[u.name] = u.class_name
        by_code[h.class_name.replace("hero_", "")] = u.class_name
        for a in h.abilities:
            by_class[a.class_name] = u.class_name
    return by_class, by_code, by_name


def real_ult(key, by_class, by_code):
    """The enemy ultimate a foreign source in Sinclair's damage was copied from (None: not a copy)."""
    if key in L.ENEMY_BOOKED or key in AGG or "magician" in key or key.startswith("upgrade") or "melee" in key:
        return None
    best = max((c for c in by_class if key == c or key.startswith(c + "_")), key=len, default=None)
    if best:
        return by_class[best]
    if key.startswith(L.STAKES):
        key = L.STAKES
    code = max((c for c in by_code if c in key), key=len, default=None)   # weapons: citadel_weapon_<codename>...
    return by_code[code] if code else None


def sim_key(name, names, G):
    if name.startswith(PREFIX):
        return "AP:" + name[len(PREFIX):].split(")")[0]
    return _SIM_KEY(name, names, G)


def sim_job(job):
    L.sim_key = sim_key   # copies by ultimate (the audit's module is the same landing_rates)
    m, slot = job
    _, out, _ = D.sim_player(job)
    c = collections.Counter()
    for k, v in out.items():
        k = k.split("|", 1)[-1]
        if not k.startswith("_"):
            c[k] += v
    return m["match_id"], c


def measure(sample, workers=4):
    """{ult class: [players facing it, real dmg, sim dmg]}, (real all, sim all)."""
    G = game()
    by_class, by_code, by_name = owner_ult(G)
    rows = collections.defaultdict(lambda: [0, 0.0, 0.0])
    jobs, real_all = [], 0.0
    with gzip.open(sample, "rt") as fh:
        for line in fh:
            m = json.loads(line)
            for p in m["players"]:
                if p["hero_id"] != SINCLAIR:
                    continue
                jobs.append((m, p["slot"]))
                ds = p["damage_sources"]
                real_all += sum(v for k, v in ds.items() if k not in AGG)
                for q in m["players"]:
                    if q["team"] != p["team"] and q["hero_id"] in G.heroes:
                        u = next((a for a in G.hero(q["hero_id"]).abilities if a.ultimate), None)
                        if u is not None:
                            rows[u.class_name][0] += 1
                for k, v in ds.items():
                    u = real_ult(k, by_class, by_code)
                    if u:
                        rows[u][1] += v
    sim_all = 0.0
    with cf.ProcessPoolExecutor(workers) as ex:
        for _, c in ex.map(sim_job, jobs, chunksize=4):
            for k, v in c.items():
                sim_all += v
                if k.startswith("AP:") and k[3:] in by_name:
                    rows[by_name[k[3:]]][2] += v
    return rows, real_all, sim_all


def fit(rows, old):
    real_c = sum(r[1] for r in rows.values()) or 1.0
    sim_c = sum(r[2] for r in rows.values()) or 1.0
    out = {}
    for u, (n, real, sim) in rows.items():
        f0 = old.get(u, 1.0)
        if sim <= 0 or n == 0:
            out[u] = f0
            continue
        x = max(FLOOR, (real / real_c) / (sim / sim_c))
        out[u] = max(CLIP[0], min(CLIP[1], f0 * math.exp(n / (n + PRIOR) * math.log(x))))
    # keep the sim's copy total: the new factors move damage between ultimates only
    new_sim = sum(r[2] * out[u] / old.get(u, 1.0) for u, r in rows.items() if r[2] > 0)
    s = sim_c / new_sim if new_sim > 0 else 1.0
    return {u: round(f * s, 3) for u, f in out.items()}


def main():
    args = sys.argv[1:]
    sample = args[0]
    workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 4
    os.environ.setdefault("AUDIT_COVER", "1")
    G = game()
    old = magician.copy_ult_factors()
    rows, real_all, sim_all = measure(sample, workers)
    new = fit(rows, old)
    names = {a.class_name: a.name for a in G.abilities.values()}
    print(f"copies: real {sum(r[1] for r in rows.values()) / real_all:.3f} of Sinclair's damage, "
          f"sim {sum(r[2] for r in rows.values()) / sim_all:.3f}")
    print(f"{'ultimate':26s} {'n':>4s} {'real':>6s} {'sim':>6s} {'factor':>13s}")
    for u, (n, real, sim) in sorted(rows.items(), key=lambda x: -x[1][1]):
        print(f"{names.get(u, u)[:26]:26s} {n:4d} {real / real_all:6.4f} {sim / sim_all:6.4f} "
              f"{old.get(u, 1.0):5.2f} -> {new.get(u, 1.0):5.2f}")
    if "--write" in args:
        out = {"meta": {"sample": os.path.basename(sample), "prior": PRIOR, "floor": FLOOR, "clip": CLIP,
                        "script": "scripts/mechanics/copy_ult.py"},
               "ults": {u: {"name": names.get(u, u), "players": rows[u][0], "real_share": round(rows[u][1] / real_all, 5),
                            "sim_share": round(rows[u][2] / sim_all, 5), "factor": new[u]}
                        for u in sorted(new)}}
        with open(PATH, "w") as fh:
            json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
