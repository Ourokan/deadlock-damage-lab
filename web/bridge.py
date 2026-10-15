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


def run(req_json):
    q = json.loads(req_json)
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
    distance = q.get("distance")
    r = damage_test(hero.name, [i.name for i in items], souls=q.get("souls"), dummy=dummy, skill=skill,
                    distance=distance)
    r["used"] = {
        "hero": hero.name, "items": [i.name for i in items], "item_cost": sum(i.cost for i in items),
        "accuracy": round(skill.accuracy, 4), "headshot": round(skill.headshot, 4),
        "distance": distance if distance is not None else default_distance(hero.name),
    }
    return json.dumps(r)
