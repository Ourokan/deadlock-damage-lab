"""One hero's real ult rows (ult_phase.py real_rows format) from the fight-length replays plus more replays of that
hero, for ult_rate_match.py --rows: the 260 fight-length replays have few fights of a hero seen in few matches
(Dynamo: 1137 rows from 18 matches, his late bins under 150 fights each).

The extra replays are fetched like the fight-length and cast-timing ones (fight_length/fetch_fights.py and
cast_timing/fetch_ability_casts.py SQL, one demo query per match) for the hero's sample matches
(validation/<hero>_sample.jsonl.gz), into <work>/raw (damage events + pawn heroes) and <work>/casts (ability casts).

usage: python3 -I hero_ult_rows.py --hero Dynamo --work /mnt/project-files/analysis/work/dynamo_replays
       --sample validation/dynamo_sample.jsonl.gz [--out PATH (default <work>/ult_rows.pkl)]
"""
import os
import pickle
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts", "fight_length"))
sys.path.insert(0, HERE)
import fit_cast_timing as CT  # noqa: E402
import fit_length as FL  # noqa: E402
import ult_phase as UP  # noqa: E402


def jobs_in(fights, casts, sample, hero_id, ults):
    have = lambda d: {f.split(".")[0] for f in os.listdir(d) if f.endswith(".ndjson.gz")}  # noqa: E731
    mids = have(fights) & have(casts)
    s = FL.load_sample(sample, mids)
    return [(os.path.join(fights, f"{m}.ndjson.gz"), os.path.join(casts, f"{m}.ndjson.gz"), s[m], ults)
            for m in sorted(mids) if m in s and any(p["hero_id"] == hero_id for p in s[m]["players"])]


def main():
    from deadsim import game
    a = sys.argv[1:]
    h = game().hero(a[a.index("--hero") + 1])
    work = a[a.index("--work") + 1]
    sample = os.path.abspath(a[a.index("--sample") + 1])
    out = a[a.index("--out") + 1] if "--out" in a else os.path.join(work, "ult_rows.pkl")
    ult = next(ab for ab in h.abilities if ab.ultimate)
    ults = {h.id: (ult.id, ult.class_name)}
    jobs = jobs_in(CT.FIGHTS, CT.CASTS, CT.SAMPLE, h.id, ults)
    jobs += jobs_in(os.path.join(work, "raw"), os.path.join(work, "casts"), sample, h.id, ults)
    rows = []
    with Pool(4) as p:
        for r in p.imap_unordered(UP.real_rows, jobs):
            rows += r
    with open(out, "wb") as fh:
        pickle.dump(rows, fh)
    print(f"{len(rows)} fight starts from {len(jobs)} matches -> {out}")


if __name__ == "__main__":
    main()
