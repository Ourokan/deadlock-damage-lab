"""Browser entry point for the custom damage test (runs in Pyodide; also works in plain CPython).

run(json_str) takes the page's form as JSON and returns damage_test()'s result plus the settings actually used:
    {"hero": "Haze", "items": [ids or names], "souls": 27000, "aim": "p50", "accuracy": null, "headshot": null,
     "distance": null, "dummy": {"hero": "Abrams", "items": [...], "souls": null, "hp": null,
     "bullet_resist": null, "spirit_resist": null, "melee_resist": null, "immortal": true}}
"""
import json

from deadsim.accuracy import default_distance, hero_default_skill
from deadsim.data import game
from dummy import Dummy, damage_test


def _item(G, x):
    return G.item(int(x) if isinstance(x, (int, float)) or str(x).isdigit() else x)


def _setup(q):
    """The page's JSON -> (hero name, item names, damage_test kwargs)."""
    G = game()
    hero = G.hero(q["hero"])
    items = [_item(G, x) for x in q.get("items", [])]
    skill = hero_default_skill(hero.name, q.get("aim") or "p50")
    if q.get("accuracy") is not None:
        skill.accuracy = float(q["accuracy"])
    if q.get("headshot") is not None:
        skill.headshot = float(q["headshot"])
    dq = q.get("dummy") or {}
    dummy = Dummy(
        hero=G.hero(dq.get("hero") or "Haze").name,
        items=[_item(G, x).name for x in dq.get("items", [])],
        souls=dq.get("souls"), hp=dq.get("hp"),
        bullet_resist=dq.get("bullet_resist"), spirit_resist=dq.get("spirit_resist"),
        melee_resist=dq.get("melee_resist"), immortal=bool(dq.get("immortal", True)))
    kw = dict(souls=q.get("souls"), dummy=dummy, skill=skill, distance=q.get("distance"))
    return hero, items, kw


def run(req_json):
    q = json.loads(req_json)
    hero, items, kw = _setup(q)
    r = damage_test(hero.name, [i.name for i in items], **kw)
    r["used"] = {
        "hero": hero.name, "items": [i.name for i in items], "item_cost": sum(i.cost for i in items),
        "accuracy": round(kw["skill"].accuracy, 4), "headshot": round(kw["skill"].headshot, 4),
        "distance": kw["distance"] if kw["distance"] is not None else default_distance(hero.name),
    }
    return json.dumps(r)


def breakdown(req_json):
    """What each item adds to the build's damage, from one run without each item (same request as run()).

    loss: damage lost by each mark when the item is removed. share: the build's damage above the no-item hero split
    across items in proportion to their positive loss, so base + shares = total. sources: change in each damage
    source (30 s) the item causes; direct: damage booked under the item's own name (its procs)."""
    q = json.loads(req_json)
    hero, items, kw = _setup(q)
    names = [i.name for i in items]
    full = damage_test(hero.name, names, **kw)
    base = damage_test(hero.name, [], **kw)
    marks = list(full["damage"])
    out = {"total": full["damage"], "base": base["damage"], "sources": full["sources"], "items": []}
    for it in items:
        r = damage_test(hero.name, [n for n in names if n != it.name], **kw)
        delta = {k: round(v - r["sources"].get(k, 0.0), 1) for k, v in full["sources"].items()}
        for k, v in r["sources"].items():
            if k not in full["sources"]:
                delta[k] = round(-v, 1)
        out["items"].append({
            "id": it.id, "name": it.name, "cost": it.cost,
            "loss": {m: round(full["damage"][m] - r["damage"][m], 1) for m in marks},
            "direct": round(sum(v for k, v in full["sources"].items() if k == it.name or k.startswith(it.name + " ")), 1),
            "sources": {k: v for k, v in sorted(delta.items(), key=lambda x: -abs(x[1])) if abs(v) >= 1},
        })
    for m in marks:
        extra = full["damage"][m] - base["damage"][m]
        pos = sum(max(0.0, x["loss"][m]) for x in out["items"])
        for x in out["items"]:
            x.setdefault("share", {})[m] = round(extra * max(0.0, x["loss"][m]) / pos, 1) if pos > 0 else 0.0
    return json.dumps(out)
