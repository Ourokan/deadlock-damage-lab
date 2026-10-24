"""Real sustain between and during fights, from Phantom+ replays fetched by fetch_sustain.py.

Measures (all per item holder, item bought before the 180 s sample window starts and not sold before it ends):
- heal per minute each healing item is credited with in the damage matrix (stat_type 1 heals, 5 regen; Healing
  Booster is credited with the healing its amp adds), per game phase;
- heal prevented per minute by Healbane (stat_type 2) and its kill heal;
- every self-heal source per minute for everyone (regen, trooper heal pickups, fountain...), per phase;
- fight entry health: health % at each hero-combat start after >= GAP_MIN s out of hero combat, and the time out of
  combat before it, per phase; holders of each item vs non-holders of the same hero in the same phase.

Writes the full report json (<report json>) and the compact inputs the overall score reads (<sim data json>,
sim/data/sustain.json): heal pickups per minute, each farm-heal item's real rate, fight entry health and the time
out of combat before a fight, per phase.

usage: python3 -I fit_sustain.py <sim dir> <matches dir> <report json> <sim data json>
"""
import collections, glob, gzip, json, os, statistics, sys
sys.path.insert(0, sys.argv[1])
from deadsim.data import game  # noqa: E402

G = game()
MATCHES, OUT_JSON, OUT_SIM = sys.argv[2], sys.argv[3], sys.argv[4]
PHASES = (("lane", 0, 540), ("mid", 540, 1500), ("late", 1500, 99999))
GAP_MIN = 8
ITEMS = ["Healing Booster", "Radiant Regeneration", "Restorative Shot", "Counterspell", "Healbane", "Tankbuster",
         "Rebuttal", "Dispel Magic", "Opening Rounds", "Monster Rounds", "Extra Regen", "Mystic Regeneration",
         "Spirit Lifesteal", "Bullet Lifesteal", "Healing Rite", "Fortitude", "Healing Nova", "Leech",
         "Siphon Bullets", "Infuser", "Rescue Beam", "Restorative Locket", "Divine Barrier", "Return Fire"]
by_name = {}
for i, it in G.items.items():
    if it.name in ITEMS:
        by_name[it.name] = it
cls_name = {it.class_name: n for n, it in by_name.items()}
id_name = {it.id: n for n, it in by_name.items()}


def at(s, k, n):
    """Damage-matrix arrays are cumulative per sample time but right-aligned: a source that starts later (an item
    bought mid game) has a shorter array whose first entry is the sample time len(times) - len(s)."""
    i = k - (n - len(s))
    return s[i] if 0 <= i < len(s) else (0 if i < 0 else s[-1])


def win(s, k, n):
    """Amount added to cumulative array s in sample window k (of n)."""
    return at(s, k, n) - at(s, k - 1, n)


def phase(t):
    for n, a, b in PHASES:
        if a <= t < b:
            return n


heal_rate = collections.defaultdict(lambda: collections.defaultdict(lambda: [0.0, 0.0]))   # item -> phase -> [hp, min]
src_rate = collections.defaultdict(lambda: collections.defaultdict(float))               # phase -> source -> hp
src_min = collections.defaultdict(float)
prevent = collections.defaultdict(lambda: [0.0, 0.0])
entry = collections.defaultdict(list)          # phase -> [(hero, held set, hp%, gap s)]
parry = collections.defaultdict(lambda: [0.0, 0.0, 0.0])   # item/none -> [success, miss, minutes]
taken = collections.defaultdict(lambda: [0.0, 0.0])        # phase -> [damage taken, minutes]
n_match = 0
FIELD_ITEMS = ("Healing Booster", "Radiant Regeneration", "Restorative Shot", "Extra Regen", "Fortitude",
               "Spirit Lifesteal", "Bullet Lifesteal", "Mystic Regeneration", "Healing Rite")
fountain = collections.defaultdict(list)       # (hero, phase, net worth bin) -> [(field items held, fountain HP/min)]
alive_s, combat_s = collections.Counter(), collections.Counter()
# mean health missing 30 s before a living trip into base (not a respawn), mid game, from the 1 s positions in
# analysis/work/range_paths (Phantom+): 74% health -> 0.26 of max health healed per trip
TRIP_DEFICIT = 0.26
# living trips into base per minute, mid game, same source (1.94 per 10 min); late game trips are mostly shopping and
# defending, so heal trips there are scaled by fountain healing (late / mid), at most the mid game rate (late fountain
# healing is higher, mostly from fighting next to it while defending the base, which costs no time on the map)
HEAL_TRIPS_MID = 0.194
for fn in sorted(glob.glob(os.path.join(MATCHES, "*.json.gz"))):
    m = json.load(gzip.open(fn, "rt"))
    times = m["times"]
    if not times:
        continue
    n_match += 1
    keys = m["stat_keys"]
    for p in m["players"]:
        slot = str(p["slot"])
        held_iv = collections.defaultdict(list)
        for iid, t0, ts in p["items"]:
            if iid in id_name and t0 > 0:
                held_iv[id_name[iid]].append((t0, ts or 1e9))

        def holds(n, a, b):
            return any(t0 <= a and ts >= b for t0, ts in held_iv.get(n, []))

        rows = [r for r in m["heal"].get(slot, [])]
        for k, t1 in enumerate(times):
            t0 = times[k - 1] if k else 0
            mins = (t1 - t0) / 60
            ph = phase(t0)
            src_min[ph] += mins
            for st, src, tgt, cum in rows:
                if st in (1, 5) and str(tgt) == slot:
                    src_rate[ph][src] += win(cum, k, len(times))
            for n in held_iv:
                if not holds(n, t0, t1):
                    continue
                cn = by_name[n].class_name
                hp = sum(win(cum, k, len(times)) for st, src, tgt, cum in rows
                         if st in (1, 5) and src == cn and str(tgt) == slot)
                heal_rate[n][ph][0] += hp
                heal_rate[n][ph][1] += mins
                if n == "Healbane":
                    pv = sum(win(cum, k, len(times)) for st, src, tgt, cum in rows if st == 2 and src == cn)
                    prevent[ph][0] += pv
                    prevent[ph][1] += mins
        st = p["stats"]
        it_ = keys.index("player_damage_taken")
        for a, b in zip(st, st[1:]):
            ph = phase(a[0])
            if a[it_] is not None and b[it_] is not None:
                taken[ph][0] += b[it_] - a[it_]
                taken[ph][1] += (b[0] - a[0]) / 60
        # parry counts at the end of the game
        last = {nm: v[-1][1] for nm, v in p["parry"].items() if v}
        dur = m["duration_s"] / 60
        for n in ("Counterspell", "Rebuttal", None):
            if n is None or held_iv.get(n):
                key = n or "everyone"
                parry[key][0] += last.get("Parry Success", 0)
                parry[key][1] += last.get("Parry Miss", 0)
                parry[key][2] += dur
        # fountain healing per 180 s window with the field-heal items held (base trips saved)
        fsrc = [r for r in rows if r[1] == "modifier_citadel_in_fountain" and str(r[2]) == slot]
        nw_at = {x[0]: x[keys.index("net_worth")] for x in p["stats"]}
        for k, t1 in enumerate(times):
            t0 = times[k - 1] if k else 0
            if t0 < 540:
                continue
            fh = sum(win(c, k, len(times)) for _, _, _, c in fsrc)
            held = frozenset(n for n in FIELD_ITEMS if holds(n, t0, t1))
            fountain[(p["hero_id"], phase(t0), (nw_at.get(t1) or 0) // 5000)].append((held, fh / ((t1 - t0) / 60)))
        # fight entries
        path = m["paths"].get(slot)
        if not path or not path["hp"]:
            continue
        hp, cb = path["hp"], path["combat"]
        for t in range(min(len(hp), len(cb))):
            if hp[t] > 0:
                alive_s[phase(t)] += 1
                combat_s[phase(t)] += bool(cb[t] & 1)
        out_since = 0
        prev = False
        for t in range(1, min(len(hp), len(cb))):
            c = bool(cb[t] & 1) and hp[t] > 0
            if c and not prev:
                gap = t - out_since
                if gap >= GAP_MIN and hp[t - 1] > 0:
                    held = frozenset(n for n in held_iv if holds(n, t, t))
                    entry[phase(t)].append((p["hero_id"], held, hp[t - 1], gap))
            if prev and not c:
                out_since = t
            if hp[t] <= 0:
                out_since = t
            prev = c

res = {"matches": n_match, "phases": {n: [a, b] for n, a, b in PHASES}, "items": {}, "entry": {}, "sources": {}}
for n in ITEMS:
    res["items"][n] = {ph: {"hp_per_min": round(v[0] / v[1], 1) if v[1] > 3 else None, "holder_minutes": round(v[1])}
                       for ph, v in heal_rate[n].items()}
res["healbane_prevented_per_min"] = {ph: round(v[0] / v[1], 1) for ph, v in prevent.items() if v[1]}
res["damage_taken_per_min"] = {ph: round(v[0] / v[1], 1) for ph, v in taken.items() if v[1]}
res["parry_per_10min"] = {k: {"success": round(v[0] / v[2] * 10, 2), "miss": round(v[1] / v[2] * 10, 2)}
                          for k, v in parry.items() if v[2]}
for ph, rows in src_rate.items():
    top = sorted(rows.items(), key=lambda x: -x[1])[:15]
    res["sources"][ph] = {s: round(v / src_min[ph], 1) for s, v in top}
for ph, rows in entry.items():
    hps = [r[2] for r in rows]
    gaps = [r[3] for r in rows]
    d = {"n": len(rows), "entry_hp_mean": round(statistics.mean(hps), 1), "entry_hp_median": statistics.median(hps),
         "gap_median_s": statistics.median(gaps), "gap_mean_s": round(statistics.mean(gaps), 1),
         "share_below_80": round(sum(h < 80 for h in hps) / len(hps), 3), "holders": {}}
    # matched holder vs non-holder entry hp: same hero, same phase
    byh = collections.defaultdict(list)
    for h, held, x, g in rows:
        byh[h].append((held, x))
    for n in ITEMS:
        diff, w = 0.0, 0
        for h, L in byh.items():
            a = [x for held, x in L if n in held]
            b = [x for held, x in L if n not in held]
            if len(a) >= 5 and len(b) >= 5:
                k = min(len(a), len(b))
                diff += (statistics.mean(a) - statistics.mean(b)) * k
                w += k
        if w >= 30:
            d["holders"][n] = {"entry_hp_diff": round(diff / w, 2), "weight": w}
    res["entry"][ph] = d
os.makedirs(os.path.dirname(OUT_JSON) or ".", exist_ok=True)
json.dump(res, open(OUT_JSON, "w"), indent=1)

# compact inputs for damage/scripts/overall_search.py
FARM_ITEMS = ("Radiant Regeneration", "Mystic Regeneration", "Restorative Shot", "Healing Rite", "Spirit Lifesteal",
              "Bullet Lifesteal")
PICKUPS = ("medic_trooper_aoe_health_pickup", "citadel_pickup_health_float_in_world")
MIN_HOLDER_MIN = 300     # thinner phases borrow the next phase's rate (few players hold these in lane)
sim = {"source": f"{n_match} Phantom+ replays (sim/scripts/sustain/fit_sustain.py)",
       "pickup_hp_per_min": {}, "farm_heal_hp_per_min": {}, "entry_hp": {}, "gap_s": {}}
for ph, *_ in PHASES:
    tot = sum(v for s, v in src_rate[ph].items() if s.startswith(PICKUPS))
    sim["pickup_hp_per_min"][ph] = round(tot / src_min[ph], 1)
    sim["entry_hp"][ph] = round(res["entry"][ph]["entry_hp_mean"] / 100, 3)
    sim["gap_s"][ph] = res["entry"][ph]["gap_median_s"]
order = [ph for ph, *_ in PHASES]
for n in FARM_ITEMS:
    row = {}
    for k, ph in enumerate(order):
        v = heal_rate[n][ph]
        if v[1] < MIN_HOLDER_MIN:
            nxt = next((heal_rate[n][q] for q in order[k + 1:] if heal_rate[n][q][1] >= MIN_HOLDER_MIN), None)
            v = nxt or v
        row[ph] = round(v[0] / v[1], 1) if v[1] else 0.0
    sim["farm_heal_hp_per_min"][n] = row
sim["combat_share"] = {ph: round(combat_s[ph] / alive_s[ph], 3) for ph in order}
sim["fountain_hp_per_min"] = {ph: round(src_rate[ph].get("modifier_citadel_in_fountain", 0) / src_min[ph], 1)
                              for ph in order}
# fountain HP saved per HP/min of an item's field healing: matched holder - non-holder fountain healing per item
# (same hero, phase, 5k net worth bin), pooled least squares through 0 over the field-heal items
sh = ss = 0.0
fit_rows = {}
for n in FIELD_ITEMS:
    for ph in ("mid", "late"):
        diff = w = 0.0
        for (h, p_, b), L in fountain.items():
            if p_ != ph:
                continue
            a = [x for held, x in L if n in held]
            c = [x for held, x in L if n not in held]
            if len(a) >= 4 and len(c) >= 4:
                k = min(len(a), len(c))
                diff += (statistics.mean(c) - statistics.mean(a)) * k
                w += k
        heal = heal_rate[n][ph][0] / heal_rate[n][ph][1] if heal_rate[n][ph][1] else 0.0
        if w >= 100 and heal > 0:
            saved = diff / w
            fit_rows[f"{n} {ph}"] = {"field_heal_per_min": round(heal, 1), "fountain_saved_per_min": round(saved, 1),
                                     "weight": int(w)}
            sh += saved * heal * w
            ss += heal * heal * w
sim["fountain_pass"] = round(max(0.0, sh / ss), 4) if ss else 0.0
# Tried 2026-10-24: each item's own matched saving instead of the pooled pass (Fortitude ~60 HP/min, Radiant and
# lifesteal ~10). Fortitude then took every hero's late build (12 of 12 vs ~7% of Phantom+ players): holders of tank
# items differ in more than the item (frontliners), so the per-item rows are not used.
sim["field_heal_hp_per_min"] = {n: {ph: round(heal_rate[n][ph][0] / heal_rate[n][ph][1], 1)
                                    if heal_rate[n][ph][1] >= MIN_HOLDER_MIN else 0.0 for ph in ("mid", "late")}
                                for n in FIELD_ITEMS}
sim["trip_deficit"] = TRIP_DEFICIT
fh = sim["fountain_hp_per_min"]
sim["heal_trips_per_min"] = {"mid": HEAL_TRIPS_MID, "late": round(HEAL_TRIPS_MID * min(1.0, fh["late"] / fh["mid"]), 3)}
mid = res["healbane_prevented_per_min"].get("mid", 0.0)
sim["healbane_prevented_per_combat_s"] = round(mid / 60 / sim["combat_share"]["mid"], 2)
res["fountain_fit"] = fit_rows
json.dump(res, open(OUT_JSON, "w"), indent=1)
old_sim = json.load(open(OUT_SIM)) if os.path.exists(OUT_SIM) else {}
# healbane_landing is written by fit_healbane.py (needs the sim; run it after this script). Kept across refits only
# while the real rate it was fitted against is unchanged, else dropped (Healbane back at full strength) until refit.
if "healbane_landing" in old_sim:
    if old_sim.get("healbane_landing_real") == sim["healbane_prevented_per_combat_s"]:
        sim["healbane_landing"] = old_sim["healbane_landing"]
        sim["healbane_landing_real"] = old_sim["healbane_landing_real"]
    else:
        print("healbane_landing dropped: the real rate changed, rerun fit_healbane.py", file=sys.stderr)
json.dump(sim, open(OUT_SIM, "w"), indent=1)
print(json.dumps(sim, indent=1))
