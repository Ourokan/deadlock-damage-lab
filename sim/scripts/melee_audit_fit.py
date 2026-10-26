"""Refit some heroes' melee rates (data/melee_rates.json) straight to the damage audit.

landing_rates.py --fit-melee fits the rates in its own model (every ability landing 100%, no mechanics, the older
all-ranks sample), and PR #107 rescaled them keeping each hero's old audit ratio, so some heroes kept a stale rate:
Paradox melees 1.6x his real melee/gun damage in the audit, Kelvin and Violet half. Melee hit sizes match replays
(scripts/mechanics/melee_scaling.py, every hero's light melee 0.93-1.03x the formula), so the gap is the rate.

Each round runs damage_audit.py for the heroes' players and scales rate by the audit's MELEE real/sim, then writes
the file; 2 rounds converge to ~1.00. Judge with split-half (fit on even match ids, audit odd, and reverse) and keep
only heroes better both ways (validation/README.md "Melee rates refit to the audit").

usage: python3 scripts/melee_audit_fit.py "Hero,Hero" [sample=validation/phantom_sample.jsonl.gz] [rounds=2]
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MELEE_FILE = os.path.join(ROOT, "data", "melee_rates.json")


def main():
    heroes = [h.strip() for h in sys.argv[1].split(",") if h.strip()]
    sample = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "validation", "phantom_sample.jsonl.gz")
    rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    out = os.path.join(tempfile.mkdtemp(), "audit")
    for k in range(rounds + 1):
        subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "damage_audit.py"), sample], cwd=ROOT,
                       check=True, stdout=subprocess.DEVNULL,
                       env=dict(os.environ, AUDIT_HEROES=",".join(heroes), AUDIT_OUT=out))
        audit = json.load(open(out + ".json"))["heroes"]
        d = json.load(open(MELEE_FILE))
        by_name = {v["name"]: v for v in d["heroes"].values()}
        for h in heroes:
            m = audit[h]["sources"].get("MELEE")
            row = by_name[h]
            print(f"round {k} {h}: melee real/sim {m and m['real_over_sim']}, mix distance "
                  f"{audit[h]['mix_distance']}, rate {row['rate']}", flush=True)
            if k < rounds and m:
                row["rate"] = round(row["rate"] * m["real_over_sim"], 4)
                row["audit_fit"] = True
        if k < rounds:
            json.dump(d, open(MELEE_FILE, "w"), indent=1)


if __name__ == "__main__":
    main()
