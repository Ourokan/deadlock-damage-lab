"""Kill participation per hero and what movement items do to it (Phantom+, current patch).

Tyler asked (2026-10-21): which heroes take part in more kills than most, how that tracks owning movement items, and
to value movement items higher in the overall score because they win chases and escapes.

Inputs
  analysis/work/kill_participation/*.jsonl.gz   team, kills, deaths, assists per player (scripts/fetch_kda.py)
  data/builds/player_builds/*.jsonl.gz           items held at the end of the match (same match_id, account_id)

Measures (one row per player per Phantom+ match, matches with 6 players a side and >= 1 kill per team only)
  KP        = (kills + assists) / own team's kills          chase: share of the team's kills you were part of
  deaths/10 = deaths per 10 minutes                         escape: how often you die
  KA/10     = (kills + assists) per 10 minutes

Movement item effect, matched like item_win_edge.py: stratum = (hero, final net worth // 2500, duration // 300 s).
In each stratum the players holding the item at the end are compared with the players who don't; the effect is
the holder-weighted mean of the differences (SE from the stratum variances). Net worth is the main confounder (rich
players fight more and own more items), so every comparison is at the same net worth, same hero, same game length.

Score weight (sim/data/movement_value.json, read by damage/scripts/overall_search.py)
  chase  = KP holders / KP non-holders               (used when z >= 2, else 1)
  escape = deaths/10 non-holders / deaths/10 holders (used when z >= 2, else 1)
  value  = min(CAP, max(1, chase x escape))
  stack_cap[k] = the same for holding k (3 = 3+) movement items vs none: caps a build's combined value, since
                 movement items overlap (one escape tool covers most of what a second adds)
The 1v1 overall fight has no movement (an escape would end it, see survival.py), so this factor is how the overall
score credits what a movement item does outside the duel. A value below 1 is not applied: a holder who dies more is
mostly an engage player (Majestic Leap), which the item doesn't cause.

    python3 scripts/kill_participation.py
"""
from __future__ import annotations

import glob
import gzip
import json
import math
import os
from collections import defaultdict

ROOT = "/mnt/project-files"
KDA = f"{ROOT}/analysis/work/kill_participation"
BUILDS = f"{ROOT}/data/builds/player_builds"
OUT = f"{ROOT}/analysis/out"
SIM_OUT = f"{ROOT}/sim/data/movement_value.json"
ITEMS = {x["id"]: x for x in json.load(open(f"{ROOT}/data/game/shop_items.json"))}
HEROES = {h["id"]: h["name"] for h in json.load(open(f"{ROOT}/data/game/heroes.json"))}
MOVEMENT = ["Sprint Boots", "Extra Stamina", "Enduring Speed", "Arcane Surge", "Kinetic Dash", "Fleetfoot", "Stalker",
            "Stamina Mastery", "Majestic Leap", "Warp Stone", "Veil Walker", "Shadow Weave", "Phantom Strike",
            "Magic Carpet", "Ethereal Shift"]
MOVE_ID = {i: x["name"] for i, x in ITEMS.items() if x["name"] in MOVEMENT}
NW_BIN, DUR_BIN = 2500, 300
Z_MIN, CAP = 2.0, 1.25


def load_kda():
    rows = {}
    for p in sorted(glob.glob(f"{KDA}/*.jsonl.gz")):
        with gzip.open(p, "rt") as f:
            for line in f:
                r = json.loads(line)
                rows[(r["match_id"], r["account_id"])] = r
    return rows


def load_items(keys):
    held = {}
    for p in sorted(glob.glob(f"{BUILDS}/*.jsonl.gz")):
        with gzip.open(p, "rt") as f:
            for line in f:
                r = json.loads(line)
                k = (r["match_id"], r["account_id"])
                if k in keys:
                    held[k] = {MOVE_ID[i] for i in r["final_items"] if i in MOVE_ID}
    return held


def players():
    kda = load_kda()
    teams = defaultdict(list)
    for k, r in kda.items():
        teams[(r["match_id"], r["team"])].append(r)
    good = set()
    for (m, t), ps in teams.items():
        o = teams.get((m, "Team1" if t == "Team0" else "Team0"), [])
        if len(ps) == 6 and len(o) == 6 and sum(p["kills"] for p in ps) > 0:
            good.add((m, t))
    held = load_items({k for k, r in kda.items() if (r["match_id"], r["team"]) in good})
    out = []
    for k, r in kda.items():
        tk = (r["match_id"], r["team"])
        if tk not in good or k not in held or r["duration_s"] < 600:
            continue
        team_kills = sum(p["kills"] for p in teams[tk])
        mins = r["duration_s"] / 60
        out.append({
            "hero": r["hero_id"], "won": r["won"], "nw": r["net_worth"], "dur": r["duration_s"],
            "kp": min(1.0, (r["kills"] + r["assists"]) / team_kills),
            "d10": r["deaths"] / mins * 10, "ka10": (r["kills"] + r["assists"]) / mins * 10,
            "move": held[k],
        })
    return out


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def var(xs):
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / max(1, len(xs) - 1)


def matched(rows, has, metric):
    """Holder-weighted mean of (holder mean - non-holder mean) over strata, its SE and the non-holder mean."""
    strata = defaultdict(lambda: ([], []))
    for r in rows:
        s = strata[(r["hero"], r["nw"] // NW_BIN, r["dur"] // DUR_BIN)]
        s[0 if has(r) else 1].append(r[metric])
    num = base = n = v = 0.0
    for h, o in strata.values():
        if len(h) < 2 or len(o) < 5:
            continue
        num += len(h) * (mean(h) - mean(o))
        base += len(h) * mean(o)
        v += len(h) ** 2 * (var(h) / len(h) + var(o) / len(o))
        n += len(h)
    if not n:
        return None
    return {"diff": num / n, "base": base / n, "se": math.sqrt(v) / n, "n": int(n)}


def effect(rows, has):
    res = {m: matched(rows, has, m) for m in ("kp", "d10", "ka10")}
    if res["kp"] is None:
        return None
    kp, d = res["kp"], res["d10"]
    chase = 1 + kp["diff"] / kp["base"]
    escape = d["base"] / (d["base"] + d["diff"])
    z_kp, z_d = kp["diff"] / kp["se"], -d["diff"] / d["se"]
    used = (chase if z_kp >= Z_MIN else 1.0) * (escape if z_d >= Z_MIN else 1.0)
    return {
        "holders": kp["n"],
        "kp": round(kp["base"] + kp["diff"], 4), "kp_others": round(kp["base"], 4), "kp_diff": round(kp["diff"], 4),
        "kp_z": round(z_kp, 1),
        "deaths10": round(d["base"] + d["diff"], 3), "deaths10_others": round(d["base"], 3), "deaths_z": round(z_d, 1),
        "ka10_diff": round(res["ka10"]["diff"], 3),
        "chase": round(chase, 4), "escape": round(escape, 4),
        "value": round(min(CAP, max(1.0, used)), 4),
    }


def pearson(xs, ys):
    mx, my = mean(xs), mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))


def main():
    rows = players()
    by_hero = defaultdict(list)
    for r in rows:
        by_hero[r["hero"]].append(r)
    # movement items held per player, at the same net worth: residual vs the all-hero mean of its net worth bin
    nw_mean = defaultdict(list)
    for r in rows:
        nw_mean[r["nw"] // NW_BIN].append(len(r["move"]))
    nw_mean = {k: mean(v) for k, v in nw_mean.items()}
    heroes = []
    for h, rs in by_hero.items():
        if len(rs) < 500:
            continue
        heroes.append({
            "id": h, "name": HEROES.get(h, str(h)), "players": len(rs),
            "kp": round(mean([r["kp"] for r in rs]), 4),
            "deaths10": round(mean([r["d10"] for r in rs]), 3),
            "movement_items": round(mean([len(r["move"]) for r in rs]), 3),
            "movement_items_vs_same_worth": round(mean([len(r["move"]) - nw_mean[r["nw"] // NW_BIN] for r in rs]), 3),
            "top_movement": sorted(({n: sum(n in r["move"] for r in rs) / len(rs) for n in MOVEMENT}).items(),
                                   key=lambda x: -x[1])[:3],
        })
    heroes.sort(key=lambda x: -x["kp"])
    kps = sorted(x["kp"] for x in heroes)
    cut = kps[int(len(kps) * 2 / 3)]
    high = {x["id"] for x in heroes if x["kp"] >= cut}
    for x in heroes:
        x["high_kp"] = x["id"] in high
    corr = {
        "kp_vs_movement_items": round(pearson([x["kp"] for x in heroes], [x["movement_items"] for x in heroes]), 3),
        "kp_vs_movement_items_same_worth": round(pearson([x["kp"] for x in heroes],
                                                         [x["movement_items_vs_same_worth"] for x in heroes]), 3),
    }
    items = {}
    for n in MOVEMENT:
        e = effect(rows, lambda r, n=n: n in r["move"])
        if e is None:
            continue
        e["high_kp_heroes"] = effect([r for r in rows if r["hero"] in high], lambda r, n=n: n in r["move"])
        e["other_heroes"] = effect([r for r in rows if r["hero"] not in high], lambda r, n=n: n in r["move"])
        items[n] = e
    any_move = effect(rows, lambda r: bool(r["move"]))
    # several movement items overlap (one escape is enough): measured effect of holding k (3 = 3+) vs none
    stack = {}
    for k in (1, 2, 3):
        e = effect([r for r in rows if not r["move"] or len(r["move"]) == k or (k == 3 and len(r["move"]) > 3)],
                   lambda r, k=k: len(r["move"]) >= k)
        stack[k] = e
    res = {"players": len(rows), "bracket": "phantom", "nw_bin": NW_BIN, "dur_bin": DUR_BIN, "high_kp_cut": cut,
           "heroes": heroes, "correlation": corr, "any_movement_item": any_move, "items": items,
           "by_count": {str(k): e for k, e in stack.items()}}
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(f"{OUT}/kill_participation.json", "w"), indent=1)
    json.dump({
        "_note": ("Overall-score multiplier per movement item: real Phantom+ chase (kill participation) x escape "
                  "(deaths per 10 min) effect at the same hero, net worth and game length; only effects with z >= 2, "
                  "floor 1, cap %.2f. Built by analysis/scripts/kill_participation.py." % CAP),
        "items": {n: e["value"] for n, e in sorted(items.items()) if e["value"] > 1.0},
        "_stack_note": ("Cap on the combined value of 2 and of 3+ weighted items: the measured chase x escape of "
                        "holding that many movement items vs none (the items overlap, so values don't multiply)."),
        "stack_cap": {str(k): round(min(CAP, max(1.0, stack[k]["chase"] * stack[k]["escape"])), 4) for k in (2, 3)},
    }, open(SIM_OUT, "w"), indent=1)
    write_md(res)


def write_md(res):
    L = ["# Kill participation and movement items (Phantom+)", "",
         f"{res['players']:,} Phantom+ player rows (patch 09-29-2026, 2026-09-30 to 2026-10-13, games of 10+ min). "
         "KP = (kills + assists) / team kills. Movement items = held at the end of the match.", "",
         "## Heroes by kill participation", "",
         "| Hero | KP | Deaths / 10 min | Movement items held | vs same net worth | Most held |", "|---|---|---|---|---|---|"]
    for x in res["heroes"]:
        top = ", ".join(f"{n} {s:.0%}" for n, s in x["top_movement"] if s >= 0.05) or "-"
        L.append(f"| {'**' + x['name'] + '**' if x['high_kp'] else x['name']} | {x['kp']:.0%} | {x['deaths10']:.2f} | "
                 f"{x['movement_items']:.2f} | {x['movement_items_vs_same_worth']:+.2f} | {top} |")
    c = res["correlation"]
    L += ["", f"Bold = top third by KP (KP >= {res['high_kp_cut']:.0%}). Across heroes, KP vs movement items held: "
          f"r = {c['kp_vs_movement_items']:+.2f}; at the same net worth: r = {c['kp_vs_movement_items_same_worth']:+.2f}.",
          "", "## What each movement item does (same hero, net worth and game length)", "",
          "| Item | Holders | KP | KP others | z | Deaths/10 | others | z | Chase | Escape | Score weight | Chase, top-third KP heroes | Chase, others |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    a = res["any_movement_item"]
    rows = sorted(res["items"].items(), key=lambda x: -x[1]["value"]) + [("Any movement items", a)]
    for n, e in rows:
        split = [f"{g['chase']:.3f} (z {g['kp_z']:+.1f})" if g else "-"
                 for g in (e.get("high_kp_heroes"), e.get("other_heroes"))]
        L.append(f"| {n} | {e['holders']:,} | {e['kp']:.1%} | {e['kp_others']:.1%} | {e['kp_z']:+.1f} | "
                 f"{e['deaths10']:.2f} | {e['deaths10_others']:.2f} | {e['deaths_z']:+.1f} | {e['chase']:.3f} | "
                 f"{e['escape']:.3f} | {e['value'] if 'items' not in n else '-'} | {split[0]} | {split[1]} |")
    L += ["", "Holding several movement items (vs none, same matching): " + "; ".join(
        f"{k}{'+' if k == '3' else ''}: chase {e['chase']:.3f}, escape {e['escape']:.3f}"
        for k, e in res["by_count"].items()) + ". They overlap, so a build's combined weight is capped at the "
        "2 and 3+ values.",
        "", "Chase = KP ratio holders / others; escape = deaths ratio others / holders (deaths z > 0 = holders die "
          "less). Score weight = chase x escape, each part only when its z >= 2, floor 1, cap "
          f"{CAP}; the overall build score multiplies by it (damage/scripts/overall_search.py)."]
    open(f"{OUT}/kill_participation.md", "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
