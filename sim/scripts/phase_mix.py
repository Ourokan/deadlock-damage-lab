"""The damage audit by game phase: each hero's share of damage by kind (gun, melee, ult, other abilities, items by
slot) in real matches around 30 / 60 / 90% of the match against the sim's duels at that fraction.

The audit's whole-match mix compares the whole real match with duels at 30 / 60 / 90%, whose damage grows with the
phase, so a source that moves with the phase can look right (or wrong) there for the wrong reason. This puts the
real damage in the window frac +- WINDOW of the sample's damage_series beside the audit run with only duels at frac
(AUDIT_SEEDS draws), pooled over heroes (players weighted) and per hero. Small sim sources (< 1% of a hero's
damage) are left out of the audit's per-source table: they show as "it_small" (items) and in "abil".
First used 2026-10-27 (validation/README.md "Ult casts by game phase"): items and plain abilities matched real at
every phase, the ult was 0.94x real at 30% and 1.17x under at 90%.

usage: python3 phase_mix.py [--sample PATH] [--window 0.05] [-v]     (~3 min on 4 cores)
"""
import collections
import json
import os
import statistics
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mechanics"))
from deadsim import game  # noqa: E402
import landing_rates as L  # noqa: E402
import melee_phase as MP  # noqa: E402

FRACS = MP.FRACS
AUDIT_SEEDS = (0, 1)
CATS = ("gun", "melee", "ult", "abil", "it_weapon", "it_spirit", "it_vitality", "it_small", "other")


def cat(k, h, classes, G, D):
    kd = D.kind(k, G, classes)
    if kd == "ability":
        ab = next((a for a in h.abilities if a.class_name == k), None)
        return "ult" if ab is not None and ab.ultimate else "abil"
    if kd == "item":
        it = G.items_by_class.get(k)
        return "it_" + it.slot if it else "other"
    return kd


def sim_cats(sample, G, D):
    """{frac: {hero id: (Counter cat -> mean sim share, players)}}"""
    out = {}
    for fr in FRACS:
        L.FRACS = (fr,)
        acc = collections.defaultdict(lambda: [collections.Counter(), 0])
        for seed in AUDIT_SEEDS:
            path = os.path.join(tempfile.gettempdir(), f"phase_mix_{os.getpid()}_{fr}_{seed}")
            os.environ["AUDIT_SEED"], os.environ["AUDIT_OUT"] = str(seed), path
            D.SEED = seed
            sys.argv = ["damage_audit.py", sample]
            D.main()
            for name, row in json.load(open(path + ".json"))["heroes"].items():
                h = G.hero(name)
                classes = {a.class_name for a in h.abilities}
                sm, c, ab, it = row["sim_mix"], collections.Counter(), 0.0, 0.0
                c["gun"], c["melee"], c["other"] = sm["gun"], sm["melee"], sm.get("other", 0.0)
                for k, s in row["sources"].items():
                    cc = cat(k, h, classes, G, D)
                    if cc in ("ult", "abil"):
                        c[cc] += s["sim_share"]
                        ab += s["sim_share"]
                    elif cc.startswith("it_"):
                        c[cc] += s["sim_share"]
                        it += s["sim_share"]
                c["abil"] += max(0.0, sm["ability"] - ab)
                c["it_small"] += max(0.0, sm["item"] - it)
                for k in CATS:
                    acc[h.id][0][k] += c[k] / len(AUDIT_SEEDS)
                acc[h.id][1] = row["players"]
        out[fr] = dict(acc)
    L.FRACS = FRACS
    return out


def main():
    args = sys.argv[1:]
    sample = args[args.index("--sample") + 1] if "--sample" in args else MP.SAMPLE
    if "--window" in args:
        MP.WINDOW = float(args[args.index("--window") + 1])
    verbose = "-v" in args
    G = game()
    import damage_audit as D
    real, nws = MP.real_phase(sample, G, lambda k, G_, c: k)
    sim = sim_cats(sample, G, D)
    rows = {}
    for hid in real:
        if not all(hid in sim[fr] for fr in FRACS):
            continue
        h = G.hero(hid)
        classes = {a.class_name for a in h.abilities}
        pts = {}
        for fr in FRACS:
            c = collections.Counter()
            for k, v in real[hid][fr].items():
                c[cat(k, h, classes, G, D)] += v
            t = sum(c.values()) or 1.0
            pts[fr] = ({k: c[k] / t for k in CATS}, sim[fr][hid][0], sim[fr][hid][1], statistics.median(nws[hid][fr]))
        rows[hid] = pts
    print(f"pooled (players weighted) real / sim share at {' / '.join(f'{f:.0%}' for f in FRACS)} of the match "
          f"(real window +- {MP.WINDOW})")
    for k in CATS:
        line = []
        for fr in FRACS:
            n = sum(r[fr][2] for r in rows.values())
            rs = sum(r[fr][0][k] * r[fr][2] for r in rows.values()) / n
            ss = sum(r[fr][1][k] * r[fr][2] for r in rows.values()) / n
            line.append(f"{rs:.3f}/{ss:.3f}" + (f"={rs / ss:.2f}" if ss > 0 else "     "))
        print(f"{k:12s}", "  ".join(line))
    for fr in FRACS:
        n = sum(r[fr][2] for r in rows.values())
        d = sum(r[fr][2] * 0.5 * sum(abs(r[fr][0][k] - r[fr][1][k]) for k in CATS) for r in rows.values()) / n
        print(f"mix distance at {fr:.0%}: {d:.4f}")
    if verbose:
        for k in CATS:
            print("==", k, "real / sim per hero")
            for hid, r in sorted(rows.items(), key=lambda x: -x[1][FRACS[0]][2]):
                a = [(r[fr][0][k], r[fr][1][k]) for fr in FRACS]
                if max(x for x, _ in a) >= 0.03:
                    print(f" {G.hero(hid).name:14s} n{r[FRACS[0]][2]:4d} " + "  ".join(f"{x:.3f}/{y:.3f}" for x, y in a))


if __name__ == "__main__":
    main()
