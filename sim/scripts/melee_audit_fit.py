"""Refit some heroes' melee rates (data/melee_rates.json) straight to the damage audit.

landing_rates.py --fit-melee fits the rates in its own model (every ability landing 100%, no mechanics, the older
all-ranks sample), and PR #107 rescaled them keeping each hero's old audit ratio, so some heroes kept a stale rate:
Paradox melees 1.6x his real melee/gun damage in the audit, Kelvin and Violet half. Melee hit sizes match replays
(scripts/mechanics/melee_scaling.py, every hero's light melee 0.93-1.03x the formula), so the gap is the rate.

Each round runs damage_audit.py for the heroes' players and scales rate by the audit's MELEE real/sim; 2 rounds
converge to ~1.00. Fitted rows get audit_fit (landing_rates.py --fit-melee leaves them alone).

--split first judges the heroes by split-half: fit on even match ids and audit the odd ones, then the reverse, and
keep only heroes whose mix distance is lower on both halves (validation/README.md "Melee rates refit to the
audit"). The kept heroes are then fitted on the whole sample; the rest keep their rates.

usage: python3 scripts/melee_audit_fit.py "Hero,Hero" [sample=validation/phantom_sample.jsonl.gz] [rounds=2] [--split]
"""
import gzip
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MELEE_FILE = os.path.join(ROOT, "data", "melee_rates.json")
TMP = tempfile.mkdtemp()


def load():
    with open(MELEE_FILE) as fh:
        return json.load(fh)


def save(d):
    tmp = MELEE_FILE + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(d, fh, indent=1)
    os.replace(tmp, MELEE_FILE)


def audit(heroes, sample, tag="audit"):
    out = os.path.join(TMP, tag)
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "damage_audit.py"), sample], cwd=ROOT,
                   check=True, stdout=subprocess.DEVNULL,
                   env=dict(os.environ, AUDIT_HEROES=",".join(heroes), AUDIT_OUT=out))
    with open(out + ".json") as fh:
        return json.load(fh)["heroes"]


def fit(heroes, sample, rounds, quiet=False):
    for k in range(rounds + 1):
        a = audit(heroes, sample)
        d = load()
        by_name = {v["name"]: v for v in d["heroes"].values()}
        for h in heroes:
            m = a[h]["sources"].get("MELEE")
            row = by_name[h]
            if not quiet:
                print(f"round {k} {h}: melee real/sim {m and m['real_over_sim']}, mix distance "
                      f"{a[h]['mix_distance']}, rate {row['rate']}", flush=True)
            if k < rounds and m:
                row["rate"] = round(row["rate"] * m["real_over_sim"], 4)
                row["audit_fit"] = True
        if k < rounds:
            save(d)


def split_keep(heroes, sample, rounds):
    """Heroes whose held-out mix distance is lower on both halves after fitting on the other half."""
    halves = {}
    for parity in (0, 1):
        path = os.path.join(TMP, f"half{parity}.jsonl.gz")
        with gzip.open(sample, "rt") as src, gzip.open(path, "wt") as dst:
            for line in src:
                if json.loads(line)["match_id"] % 2 == parity:
                    dst.write(line)
        halves[parity] = path
    orig = load()
    better = {h: True for h in heroes}
    try:
        for fit_on, test_on in ((0, 1), (1, 0)):
            save(orig)
            base = audit(heroes, halves[test_on], "base")
            fit(heroes, halves[fit_on], rounds, quiet=True)
            new = audit(heroes, halves[test_on], "new")
            for h in heroes:
                print(f"held-out half {test_on} {h}: mix distance {base[h]['mix_distance']} -> "
                      f"{new[h]['mix_distance']}", flush=True)
                better[h] &= new[h]["mix_distance"] < base[h]["mix_distance"]
    finally:
        save(orig)
    return [h for h in heroes if better[h]]


def main():
    args = [a for a in sys.argv[1:] if a != "--split"]
    heroes = [h.strip() for h in args[0].split(",") if h.strip()]
    sample = args[1] if len(args) > 1 else os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    rounds = int(args[2]) if len(args) > 2 else 2
    if "--split" in sys.argv:
        heroes = split_keep(heroes, sample, rounds)
        print("kept:", ", ".join(heroes) or "none", flush=True)
    if heroes:
        fit(heroes, sample, rounds)


if __name__ == "__main__":
    main()
