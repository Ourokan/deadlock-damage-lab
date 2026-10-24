"""Pull full match metadata for a sample of current-patch ranked matches and keep only what the
combat model is validated against: per-player item timeline, stat timeline (max_health, tech_power,
shots, headshots, damage) and per-source damage dealt to enemy heroes from the damage matrix (match totals, and cumulative at each
damage_times sample in damage_series).

usage: python3 fetch_validation.py <player_builds.jsonl.gz> <out.jsonl.gz> [n_matches]
       python3 fetch_validation.py --api <min_badge> <days> <out.jsonl.gz> [n_matches]
--api samples recent matches straight from the API (e.g. --api 91 4 for Phantom+ of the last 4 days).
"""
import gzip, json, random, sys, time, urllib.request, concurrent.futures as cf

UA = {"User-Agent": "deadlock-build-sim/0.1 (research)"}


def ids_from_builds(src, n):
    ids = set()
    with gzip.open(src, "rt") as f:
        for line in f:
            r = json.loads(line)
            if (r["badge"] or 0) >= 60 and r["duration_s"] > 1500:
                ids.add(r["match_id"])
    random.seed(7)
    return random.sample(sorted(ids), min(n, len(ids)))


def ids_from_api(min_badge, days, n):
    """Recent ranked matches at or above an average badge (91 = Phantom 1), from the bulk metadata endpoint."""
    now = int(time.time())
    url = (f"https://api.deadlock-api.com/v1/matches/metadata?min_unix_timestamp={now - days * 86400}"
           f"&max_unix_timestamp={now - 3 * 3600}&min_average_badge={min_badge}&min_duration_s=1500&limit=5000"
           f"&include_info=true&order_by=match_id&order_direction=desc")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
        ms = json.load(r)
    ids = sorted(m["match_id"] for m in ms if m.get("match_mode") in ("Ranked", 4, None) and m.get("duration_s", 0) > 1500)
    random.seed(7)
    return random.sample(ids, min(n, len(ids)))


STAT_KEYS = ("time_stamp_s", "net_worth", "max_health", "tech_power", "weapon_power", "shots_hit",
             "shots_missed", "hero_bullets_hit", "hero_bullets_hit_crit", "player_damage",
             "player_damage_taken", "ability_points", "kills", "deaths")


def get(mid):
    url = f"https://api.deadlock-api.com/v1/matches/{mid}/metadata"
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r)["match_info"]
        except Exception as e:  # noqa: BLE001 - retry anything transient
            time.sleep(3 * (i + 1))
    return None


def slim(m):
    dm = m.get("damage_matrix") or {}
    names = (dm.get("source_details") or {}).get("source_name", [])
    stypes = (dm.get("source_details") or {}).get("stat_type", [])
    # Damage matrix: stat_type 0 = damage dealt (1 mitigated?, 3 taken?, 5 healing); target slot 0 = non-heroes.
    # Source names "Bullet", "Ability", "Melee", "Misc" are per-damage-type totals of the named sources.
    team = {p["player_slot"]: p["team"] for p in m["players"]}
    dmg = {}  # player_slot -> {source_name: damage dealt to enemy heroes}
    times = dm.get("sample_time_s") or []
    series = {}  # player_slot -> {source_name: cumulative damage to enemy heroes at each of `times`}
    for d in dm.get("damage_dealers", []):
        me = d["dealer_player_slot"]
        acc = dmg.setdefault(me, {})
        ser = series.setdefault(me, {})
        for s in d["damage_sources"]:
            i = s["source_details_index"]
            if i >= len(names) or (stypes[i] if i < len(stypes) else None) != 0:
                continue
            rows = [t["damage"] for t in s["damage_to_players"]
                    if t["damage"] and t["target_player_slot"] in team and team[t["target_player_slot"]] != team.get(me)]
            tot = sum(r[-1] for r in rows)
            if tot:
                acc[names[i]] = acc.get(names[i], 0) + tot
                cum = ser.setdefault(names[i], [0] * len(times))
                for r in rows:   # arrays are right-aligned: a shorter one starts at a later sample
                    off = len(times) - len(r)
                    for k, v in enumerate(r):
                        if 0 <= off + k < len(times):
                            cum[off + k] += v
    cus = {c["id"]: c["name"] for c in m.get("custom_user_stats") or []}
    players = []
    for p in m["players"]:
        last = p["stats"][-1] if p["stats"] else {}
        custom = {cus.get(c["id"], str(c["id"])): c["value"] for c in last.get("custom_user_stats") or []}
        players.append({
            "account_id": p["account_id"], "slot": p["player_slot"], "team": p["team"],
            "hero_id": p["hero_id"], "level": p["level"], "net_worth": p["net_worth"],
            "items": [[x["item_id"], x["game_time_s"], x["sold_time_s"], x.get("upgrade_id", 0)] for x in p["items"]],
            "stats": [{k: s.get(k) for k in STAT_KEYS} for s in p["stats"]],
            "damage_sources": dmg.get(p["player_slot"], {}),
            "damage_series": series.get(p["player_slot"], {}),
            "custom": custom,
            "deaths": [{"t": d.get("game_time_s"), "killer": d.get("killer_player_slot"), "ttk": d.get("time_to_kill_s")}
                       for d in p.get("death_details") or []],
            "power_ups": [{"type": b.get("type"), "values": b.get("pickup_stat_values"), "times": b.get("pickup_times_s")}
                          for b in p.get("power_up_buffs") or []],
        })
    return {"match_id": m["match_id"], "duration_s": m["duration_s"], "damage_times": times,
            "badge": [m.get("average_badge_team0"), m.get("average_badge_team1")], "players": players}



def main(argv):
    if argv[0] == "--api":
        out, n = argv[3], int(argv[4]) if len(argv) > 4 else 300
        ids = ids_from_api(int(argv[1]), int(argv[2]), n)
    else:
        out, n = argv[1], int(argv[2]) if len(argv) > 2 else 300
        ids = ids_from_builds(argv[0], n)
    k = 0
    with gzip.open(out, "wt") as f, cf.ThreadPoolExecutor(4) as ex:
        for m in ex.map(get, ids):
            if m and m.get("damage_matrix"):
                f.write(json.dumps(slim(m), separators=(",", ":")) + "\n"); k += 1
    print("wrote", k, "matches")


if __name__ == "__main__":
    main(sys.argv[1:])
