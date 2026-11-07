"""Does a replay decode hero ability entities? One demo query per match (2026-11-07).

Counts rows in every ability table (cooldown start + owner columns) and DamageEvent, then names the heroes whose
abilities have rows (owner pawns voted by ability id, as replay_openers does). A healthy match shows 12 heroes;
"0 hero ability tables" with only Slide/Jump/ZipLine rows is the broken decode a thread saw after the 11-05 hotfix
(not reproducible on 2026-11-07: post-hotfix demos decode normally).

usage: python3 -I demo_check.py <match_id> [...] [--fresh TAG]   (--fresh bypasses the API's result cache)
"""
import collections
import json
import os
import struct
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from demo_query import run  # noqa: E402
from fetch_replays import get, API  # noqa: E402
from deadsim.data import game  # noqa: E402

G = game()
AB = {a.id: hid for hid in G.heroes for a in G.hero(hid).abilities}
MOVES = ("Slide", "Jump", "Dash", "Sprint", "ZipLine", "Mantle", "Climb", "HoldMelee", "MeleeParry", "PrimaryWeapon_Empty")


def query():
    need = {"m_flCooldownStart", "m_hOwnerEntity", "m_nSubclassID"}
    tabs = [t["name"] for t in get(f"{API}/matches/demo/schema")["tables"]
            if need <= {c["name"] for c in t["columns"]} and t["name"].startswith(("CCitadel_Ability_", "CAbility_"))]
    parts = [f"""SELECT '{t}' AS t, CAST("m_hOwnerEntity" AS BIGINT) % 16384 AS o, encode("m_nSubclassID", 'hex') AS s, count(*) AS n FROM {t} GROUP BY 2, 3""" for t in tabs]
    parts.append("SELECT 'DamageEvent' AS t, 0 AS o, '' AS s, count(*) AS n FROM DamageEvent")
    return "\nUNION ALL\n".join(parts)


def check(mid, sql, fresh=None):
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "r.ndjson")
        run(mid, sql, out, fresh=fresh)
        rows = [json.loads(line) for line in open(out)]
    tables = collections.Counter()
    votes = collections.defaultdict(collections.Counter)
    for r in rows:
        tables[r["t"]] += r["n"]
        if r["t"] != "DamageEvent" and r.get("s"):
            aid = struct.unpack("<I", bytes.fromhex(r["s"][:8]))[0]
            if aid in AB:
                votes[r["o"]][AB[aid]] += r["n"]
    hero_tabs = [t for t, n in tables.items() if n and t != "DamageEvent" and not t.endswith(MOVES)]
    heroes = sorted(G.hero(c.most_common(1)[0][0]).name for c in votes.values())
    print(f"{mid}: DamageEvent {tables['DamageEvent']}, Slide {tables['CCitadel_Ability_Slide']}, "
          f"{len(hero_tabs)} hero ability tables, {len(heroes)} heroes: {', '.join(heroes)}")
    return len(heroes)


def main():
    args, fresh = sys.argv[1:], None
    if "--fresh" in args:
        i = args.index("--fresh"); fresh = args[i + 1]; del args[i:i + 2]
    sql = query()
    for mid in args:
        try:
            check(mid, sql, fresh)
        except BaseException as e:  # noqa: BLE001
            print(f"{mid}: {str(e)[:120]}")


if __name__ == "__main__":
    main()
