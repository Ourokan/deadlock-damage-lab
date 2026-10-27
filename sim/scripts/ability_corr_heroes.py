"""Per-hero ability length corrections straight from the damage audit, for heroes whose landing factors were refit.

refit_landing_heroes.py fits each ability's landing factor with every hit of a 20 s duel in full and the casts on
sight (what the dummy page runs). The searches and the audit book damage over real fight lengths with first casts
held to real cast times (Mechanics.fight_length + cast_timing), through landing x length_corr. length_factors.py
can't redo length_corr for a refit hero any more: its keep mode refuses factors already scaled for cast timing, and
its --refit target (the in-full ratio in duels with held casts) is not what the landing fit saw (held-out audit
0.040 -> 0.063 for 13 refit heroes).

So for each named hero's ability rows in data/landing_rates_mech.json, from the audit's per-hero sources
(validation/damage_audit.json, real/sim of source damage over gun damage):

    length_corr = length_corr x (real/sim) ^ (players / (players + PRIOR))

clipped to KEEP_RANGE. Note the heroes in the file's meta "audit_corr_heroes". Run the audit, then this, a few rounds (each audit reads the new factors). Abilities the
audit does not see on a hero (never cast, no real damage) keep their correction.

--split judges the heroes first (validation/README.md "Stale ability corrections"): fit ROUNDS rounds on even match
ids and audit the odd ones, then the reverse; keep only heroes whose held-out per-source distance (half the summed
|real - sim| share over every source) is lower on both halves and whose mix distance is not worse by more than
MIX_SLACK. The kept heroes are then fitted ROUNDS rounds on the whole sample and written; the rest keep their rows.

usage: python3 scripts/ability_corr_heroes.py [--audit PATH] [--prior N] --hero NAME [--hero NAME ...] [--write]
       python3 scripts/ability_corr_heroes.py --split [--sample PATH] [--rounds N] --hero NAME [--hero NAME ...]
"""
import gzip
import json
import math
import os
import subprocess
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PATH = os.path.join(ROOT, "data", "landing_rates_mech.json")
PRIOR = 20
KEEP_RANGE = (0.1, 10.0)   # as length_factors.py's keep mode
# abilities whose damage skips its landing factor x length_corr (Mechanics.swap_full: Soul Exchange swaps whole)
UNSCALED = {"ability_health_swap"}


def fit(audit, heroes, prior=PRIOR):
    data = json.load(open(PATH))
    for h in heroes:
        a = audit["heroes"].get(h)
        rows = data["heroes"].get(h)
        if not a or not rows:
            print(f"{h}: not in the audit or the landing file")
            continue
        w = a["players"] / (a["players"] + prior)
        for name, r in rows.items():
            if r.get("class") in UNSCALED:
                continue
            src = a["sources"].get(r.get("class") or "")
            x = src and src.get("real_over_sim")
            if not x or x <= 0:
                continue
            old = r.get("length_corr", 1.0)
            new = max(KEEP_RANGE[0], min(KEEP_RANGE[1], old * math.exp(w * math.log(x))))
            r["length_corr"] = round(new, 3)
            print(f"{h:15s} {name:28s} real/sim {x:5.2f}  length_corr {old:.3f} -> {new:.3f}")
    return data


ROUNDS = 3
MIX_SLACK = 0.002


def source_distance(a):
    return 0.5 * sum(abs(s["real_share"] - s["sim_share"]) for s in a["sources"].values())


def save(data):
    tmp = PATH + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(data, fh, indent=1)
    os.replace(tmp, PATH)


def run_audit(heroes, sample, out):
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "damage_audit.py"), sample], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL, env=dict(os.environ, AUDIT_HEROES=",".join(heroes), AUDIT_OUT=out))
    with open(out + ".json") as fh:
        return json.load(fh)


def fit_rounds(heroes, sample, rounds, tmp, prior=PRIOR):
    for _ in range(rounds):
        save(fit(run_audit(heroes, sample, os.path.join(tmp, "fit")), heroes, prior))


def split_keep(heroes, sample, rounds, prior=PRIOR):
    tmp = tempfile.mkdtemp()
    halves = {}
    for parity in (0, 1):
        halves[parity] = os.path.join(tmp, f"half{parity}.jsonl.gz")
        with gzip.open(sample, "rt") as src, gzip.open(halves[parity], "wt") as dst:
            for line in src:
                if json.loads(line)["match_id"] % 2 == parity:
                    dst.write(line)
    with open(PATH) as fh:
        orig = json.load(fh)
    keep = {h: True for h in heroes}
    try:
        for fit_on, test_on in ((0, 1), (1, 0)):
            save(orig)
            base = run_audit(heroes, halves[test_on], os.path.join(tmp, "base"))["heroes"]
            fit_rounds(heroes, halves[fit_on], rounds, tmp, prior)
            new = run_audit(heroes, halves[test_on], os.path.join(tmp, "new"))["heroes"]
            for h in heroes:
                if h not in base or h not in new:
                    keep[h] = False
                    continue
                b, n = base[h], new[h]
                bs, ns = source_distance(b), source_distance(n)
                print(f"held-out half {test_on} {h:15s} sources {bs:.4f} -> {ns:.4f}  mix {b['mix_distance']:.4f} -> "
                      f"{n['mix_distance']:.4f}", flush=True)
                keep[h] &= ns < bs and n["mix_distance"] <= b["mix_distance"] + MIX_SLACK
    finally:
        save(orig)
    return [h for h in heroes if keep[h]]


def main():
    args = sys.argv[1:]
    path = os.path.join(ROOT, "validation", "damage_audit.json")
    prior = PRIOR
    if "--audit" in args:
        path = args[args.index("--audit") + 1]
    if "--prior" in args:
        prior = float(args[args.index("--prior") + 1])
    heroes = [args[i + 1] for i, a in enumerate(args) if a == "--hero"]
    if "--split" in args:
        sample = os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
        if "--sample" in args:
            sample = args[args.index("--sample") + 1]
        rounds = int(args[args.index("--rounds") + 1]) if "--rounds" in args else ROUNDS
        heroes = split_keep(heroes, sample, rounds, prior)
        print("kept:", ", ".join(heroes) or "none", flush=True)
        if heroes:
            fit_rounds(heroes, sample, rounds, tempfile.mkdtemp(), prior)
        return
    data = fit(json.load(open(path)), heroes, prior)
    if "--write" in args:
        json.dump(data, open(PATH, "w"), indent=1)


if __name__ == "__main__":
    main()
