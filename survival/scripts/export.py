"""Collect work/jobs/*.json into out/ for the web page and a readable report.

out/index.json        per hero x budget x damage margin: popular vs best build time alive and damage change
out/heroes/<id>.json  the full job result (top 10 builds per margin, matchups, item removal losses)
out/report.md         tables with item names
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path[:0] = [os.path.join(ROOT, "..", "sim"), os.path.join(ROOT, "..", "search", "scripts")]
import search as S  # noqa: E402
items = json.load(open(os.path.join(ROOT, "..", "search", "out", "items.json")))
heroes_meta = {h["id"]: h["name"] for h in json.load(open(os.path.join(ROOT, "..", "data", "game", "heroes.json")))}


def name(i):
    it = items.get(str(i))
    return it["name"] if it else str(i)


def main():
    os.makedirs(os.path.join(ROOT, "out", "heroes"), exist_ok=True)
    jobs = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(ROOT, "work", "jobs", "*.json")))]
    by_hero = {}
    for j in jobs:
        by_hero.setdefault(j["hero_id"], {})[str(j["budget"])] = j
    index = {"settings": {}, "heroes": {}}
    md = ["# Tank survival builds", ""]
    for h, budgets in sorted(by_hero.items(), key=lambda x: heroes_meta.get(x[0], "")):
        json.dump({"hero_id": h, "hero": heroes_meta.get(h), "budgets": budgets},
                  open(os.path.join(ROOT, "out", "heroes", f"{h}.json"), "w"))
        md += [f"## {heroes_meta.get(h)}", "",
               "| Souls | Margin | Popular alive (s) | Best alive (s) | Damage vs popular | Core (kept) | Swapped out | Added |",
               "|---|---|---|---|---|---|---|---|"]
        idx = {}
        for b, j in sorted(budgets.items(), key=lambda x: int(x[0])):
            index["settings"] = {"focus": j["focus"], "max_time": j["max_time"], "core_rate": j["core_rate"]}
            pop = j["popular"]
            idx[b] = {"core": j["core"], "popular": {"items": pop["items"], "score": pop["score"],
                                                     "time_alive": pop[f"focus_{j['focus']:g}"]["time_alive"]}}
            for m, r in j["margins"].items():
                best = r["builds"][0]
                idx[b][m] = {"items": best["items"], "score": best["score"],
                             "time_alive": best[f"focus_{j['focus']:g}"]["time_alive"],
                             "damage_vs_popular": best["damage_vs_popular"]}
                g = S.G()
                gone = [i for i in pop["items"] if i not in best["items"]]
                new_ = [i for i in best["items"] if i not in pop["items"]]
                up = {i: j for i in gone for j in new_ if i in S.component_ids(g.items[j])}
                out_ = [name(i) + (f" (upgraded to {name(up[i])})" if i in up else "") for i in gone]
                in_ = [name(i) for i in new_]
                md.append(f"| {int(b) // 1000}k | {float(m):.0%} | {idx[b]['popular']['time_alive']:.1f} | "
                          f"{best[f'focus_{j['focus']:g}']['time_alive']:.1f} | {best['damage_vs_popular']:+.0%} | "
                          f"{', '.join(name(i) for i in j['core']) or '-'} | {', '.join(out_) or '-'} | "
                          f"{', '.join(in_) or '-'} |")
        md.append("")
        index["heroes"][str(h)] = {"hero": heroes_meta.get(h), "budgets": idx}
    json.dump(index, open(os.path.join(ROOT, "out", "index.json"), "w"))
    open(os.path.join(ROOT, "out", "report.md"), "w").write("\n".join(md))
    print(f"{len(jobs)} jobs exported", file=sys.stderr)


if __name__ == "__main__":
    main()
