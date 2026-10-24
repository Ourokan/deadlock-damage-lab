"""Scale the extra gap healing of a build (vs the popular build) in the overall score's fight entry health so that
item holders arrive as much fuller as real Phantom+ holders do: model entry health gain of popular build + item vs
the popular build (HEROES, one budget per phase) against the matched holder vs non-holder entry health difference
(analysis/out/sustain_real.json entry.<phase>.holders, from fit_sustain.py). One scale per phase, weighted least
squares over the field-heal items but Fortitude; then Fortitude's own restore scale (its RestoreDelay needs time
without any damage: creeps and troopers reset it), so the biggest item doesn't set everyone's scale. Writes
entry_heal_scale and fortitude_heal_scale into sim/data/sustain.json.

Before this fit (2026-10-24) Fortitude came out +8.1 points of health at mid game fight entry vs +6.0 real and +6.3
vs +3.5 late (its restore needs 10 s without any damage; creeps and troopers reset it), and every item's late gain
was 2-4x the real one.

Refit order (not run by CI, sim/data/sustain.json is a static snapshot): fit_sustain.py, fit_healbane.py, this.
usage (repo root, search/work pools built): python3 sim/scripts/sustain/fit_entry.py
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "damage", "scripts"))
import game_path as GP  # noqa: E402
import overall_search as O  # noqa: E402

S = O.S
HEROES = ("Haze", "Abrams", "Seven", "Infernus", "Lash", "Wraith", "Bebop", "Pocket", "Victor", "Celeste", "Kelvin",
          "Rat King", "Venator", "Drifter", "McGinnis", "Vindicta")
BUDGETS = {"mid": 18000, "late": 37000}
MIN_WEIGHT = 1000     # matched holder rows behind a real difference
REAL = os.path.join(ROOT, "analysis", "out", "sustain_real.json")


def gains(ph, scale, fort=1.0):
    """item -> mean entry health gain (points of max health) of popular build + item over the popular build."""
    b = BUDGETS[ph]
    pools = S.load_pools(b)
    sus = O.sustain()
    sus.setdefault("entry_heal_scale", {})[ph] = scale
    sus.setdefault("fortitude_heal_scale", {})[ph] = fort
    out = {}
    for hero in HEROES:
        h = S.G().hero(hero).id
        pop = S.popular_build(h, GP.item_budget(b), pools)
        d = O.entry_deficit(h, pop, b)
        e0 = O.entry_hp_start(h, pop, b, d) / O.build_stats(h, pop, b)["max_hp"]
        for n in sus["fountain_saved_hp_per_min"]:
            it = S.G().item(n)
            if it.id in pop:
                continue
            items = GP.with_item(pop, it.id)
            e = O.entry_hp_start(h, items, b, d) / O.build_stats(h, items, b)["max_hp"]
            out.setdefault(n, []).append(100 * (e - e0))
    return {n: sum(v) / len(v) for n, v in out.items()}


def grid(ph, rows, scale=None):
    best = None
    for k in range(5, 201, 5):
        if scale is None and k > 100:
            break
        g = gains(ph, k / 100) if scale is None else gains(ph, scale, k / 100)
        sse = sum(r["weight"] * (g[n] - r["entry_hp_diff"]) ** 2 for n, r in rows.items() if n in g)
        if best is None or sse < best[0]:
            best = (sse, k / 100, g)
    return best[1], best[2]


def main():
    real = json.load(open(REAL))["entry"]
    scale, fort = {}, {}
    for ph in BUDGETS:
        rows = {n: r for n, r in real[ph]["holders"].items() if r["weight"] >= MIN_WEIGHT}
        scale[ph], _ = grid(ph, {n: r for n, r in rows.items() if n != "Fortitude"})
        fort[ph], g = grid(ph, {"Fortitude": rows["Fortitude"]}, scale[ph])
        print(ph, "scale", scale[ph], "fortitude", fort[ph],
              {n: f"{g[n]:+.2f} vs real {r['entry_hp_diff']:+.2f}" for n, r in rows.items() if n in g})
    scale["lane"], fort["lane"] = scale["mid"], fort["mid"]   # 10k stage entry; lane trades use fortitude's
    with open(O.SUSTAIN_PATH) as f:
        sus = json.load(f)
    sus["entry_heal_scale"], sus["fortitude_heal_scale"] = scale, fort
    with open(O.SUSTAIN_PATH, "w") as f:
        json.dump(sus, f, indent=1)


if __name__ == "__main__":
    main()
