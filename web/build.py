"""Build the static site's data: python3 build.py [--pyodide DIR]

Fills web/data (JSON the page reads), web/py/sim.zip (deadsim + game data + dummy.py + bridge.py, unpacked into
Pyodide's file system) and web/vendor/pyodide (self-hosted Pyodide core, so the page needs no CDN). Stdlib only.
Re-run after the sim or any search output changes; lists load whatever exists.
"""
import argparse
import base64
import glob
import importlib.util
import json
import marshal
import os
import shutil
import sys
import zipfile

ROOT = os.environ.get("DEADSIM_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root (the folder holding sim/, data/, damage/ ...)
WEB = os.path.dirname(os.path.abspath(__file__))
PYODIDE_FILES = ["pyodide.js", "pyodide.asm.js", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]
# Pyodide 0.26.4 runs Python 3.12: on a 3.12 build the bundles ship compiled .pyc (no compile at page load), on any
# other Python they ship the .py sources and still work
PYC = sys.version_info[:2] == (3, 12)
# drop from raw/items.json what only the game's UI uses (no sim code reads these keys): about 90% of its size
RAW_ITEM_DROP = {"description", "tooltip_details", "image", "image_webp", "shop_image", "shop_image_webp"}
RAW_PROP_DROP = {"icon", "label", "postvalue_label", "css_class", "display_units", "postfix", "prefix",
                 "loc_token_override", "can_set_token_override", "disable_value", "usage_flags", "tooltip_section",
                 "tooltip_is_elevated", "tooltip_is_important"}


def copy_out(src_dir, dst_dir):
    if not os.path.isdir(src_dir):
        return 0
    os.makedirs(os.path.join(dst_dir, "heroes"), exist_ok=True)
    n = 0
    for f in [os.path.join(src_dir, "index.json"), *glob.glob(os.path.join(src_dir, "heroes", "*.json"))]:
        if os.path.exists(f):
            rel = os.path.relpath(f, src_dir)
            with open(f) as fh:
                d = json.load(fh)
            with open(os.path.join(dst_dir, rel), "w") as fh:
                json.dump(d, fh, separators=(",", ":"))
            n += 1
    return n


def slim_ability_orders():
    """popular_ability_order() reads only oracle_plus.ability_order_stats; keep the row it would pick."""
    out = {}
    for fn in glob.glob(os.path.join(ROOT, "data/builds/aggregates/per_hero/*.json")):
        with open(fn) as fh:
            d = json.load(fh)
        rows = d["oracle_plus"]["ability_order_stats"]
        rows = [r for r in rows if len(r["abilities"]) >= 16] or rows
        keep = [max(rows, key=lambda r: r["matches"])] if rows else []
        out[os.path.basename(fn)] = json.dumps({"oracle_plus": {"ability_order_stats": keep}})
    return out


def pyc(source, dfile):
    """A sourceless .pyc of `source` (unchecked hash, so it never looks for the .py)."""
    code = compile(source, dfile, "exec", dont_inherit=True)
    return importlib.util.MAGIC_NUMBER + (1).to_bytes(4, "little") + importlib.util.source_hash(source) + \
        marshal.dumps(code)


def write_py(z, src, arc, dfile=None):
    """A module into a zip: compiled to arc + "c" (Python finds foo.pyc in place of foo.py) when PYC."""
    with open(src, "rb") as fh:
        body = fh.read()
    if PYC:
        z.writestr(arc + "c", pyc(body, dfile or "/app/" + arc))
    else:
        z.writestr(arc, body)


def write_json(z, src, arc, slim=None):
    """JSON without whitespace (the same values, read faster); slim(data) trims it first."""
    with open(src) as fh:
        d = json.load(fh)
    z.writestr(arc, json.dumps(slim(d) if slim else d, separators=(",", ":")))


def slim_raw_items(items):
    out = []
    for x in items:
        x = {k: v for k, v in x.items() if k not in RAW_ITEM_DROP}
        if isinstance(x.get("properties"), dict):
            x["properties"] = {k: {a: b for a, b in v.items() if a not in RAW_PROP_DROP} if isinstance(v, dict) else v
                               for k, v in x["properties"].items()}
        out.append(x)
    return out


def build_zip(path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in glob.glob(os.path.join(ROOT, "sim/deadsim/**/*.py"), recursive=True):
            write_py(z, f, os.path.relpath(f, ROOT))
        for f in glob.glob(os.path.join(ROOT, "sim/data/*.json")):
            write_json(z, f, os.path.relpath(f, ROOT))
        # fitted Dispel Magic shares and Counterspell rates, read by accuracy.hero_default_skill (no fallback, so
        # they must ship)
        for f in glob.glob(os.path.join(ROOT, "sim/validation/dispel/*fit_*.json")) + \
                glob.glob(os.path.join(ROOT, "sim/validation/counterspell/fit_*.json")):
            write_json(z, f, os.path.relpath(f, ROOT))
        for name in ["abilities.json", "heroes.json", "shop_items.json", "weapons.json", "raw/items.json"]:
            write_json(z, os.path.join(ROOT, "data/game", name), "data/game/" + name,
                       slim_raw_items if name == "raw/items.json" else None)
        for fn, body in slim_ability_orders().items():
            z.writestr("data/builds/aggregates/per_hero/" + fn, body)
        write_py(z, os.path.join(ROOT, "damage/dummy.py"), "damage/dummy.py")
        write_py(z, os.path.join(WEB, "bridge.py"), "damage/bridge.py")


def build_stdlib(full, path):
    """py/stdlib.zip: the part of Pyodide's standard library the site imports (stdlib_keep.txt), compiled, in place of
    the full 2.3 MB python_stdlib.zip. worker.js fetches the full one if anything outside the list is imported."""
    with open(os.path.join(WEB, "stdlib_keep.txt")) as fh:
        keep = {l.strip() for l in fh if l.strip() and not l.startswith("#")}
    with zipfile.ZipFile(full) as src, zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        names = set(src.namelist())
        for m in sorted(keep):
            parts = m.split(".")
            for i in range(1, len(parts) + 1):   # the module and every package above it
                p = "/".join(parts[:i])
                for arc in ([p + ".py"] if i == len(parts) else []) + [p + "/__init__.py"]:
                    if arc in names and arc + "c" not in z.namelist() and arc not in z.namelist():
                        body = src.read(arc)
                        if PYC:
                            z.writestr(arc + "c", pyc(body, "/lib/python312.zip/" + arc))
                        else:
                            z.writestr(arc, body)
        z.writestr("site-packages/", b"")
        # every module the full stdlib has, so worker.js fetches it only for those (not for optional imports such
        # as hashlib's _hashlib, which Pyodide has in neither)
        full_mods = sorted({n[:-3].removesuffix("/__init__").replace("/", ".") for n in names if n.endswith(".py")})
        z.writestr("_full_stdlib.py", "MODULES = frozenset(%r)\n" % full_mods)


CC_KEYS = ("StunDuration", "ImmobilizeDuration", "SleepDuration", "SilenceRadius", "LiftHeight", "LiftDuration",
           "TetherDuration", "CancelHookDuration")


def maker_data():
    """data/maker.json for the build maker (maker.js): item components, utility tags (web/maker_utility.json), each
    hero's crowd-control abilities, and the standard bracket's item hold rates (search/out/usage.json) to build enemy
    builds at any souls."""
    with open(os.path.join(ROOT, "data/game/shop_items.json")) as fh:
        items = json.load(fh)
    by_class = {x["class_name"]: x["id"] for x in items}
    by_name = {x["name"]: x["id"] for x in items}
    comps = {}
    for x in items:
        out, stack = set(), list(x["components"])
        while stack:
            c = by_class.get(stack.pop())
            if c is not None and c not in out and c != x["id"]:
                out.add(c)
                stack += next(y["components"] for y in items if y["id"] == c)
        if out:
            comps[str(x["id"])] = sorted(out)
    with open(os.path.join(WEB, "maker_utility.json")) as fh:
        util = {}
        for k, v in json.load(fh).items():
            if k.startswith("_"):
                continue
            if k not in by_name:   # a patch renamed or removed it: drop its tags rather than fail the deploy
                print(f"warning: maker_utility.json lists {k!r}, which is not in the shop", file=sys.stderr)
                continue
            util[str(by_name[k])] = v
    with open(os.path.join(ROOT, "data/game/abilities.json")) as fh:
        cc = {}
        for a in json.load(fh):
            if any(k in a["properties"] for k in CC_KEYS):
                cc.setdefault(str(a["hero_id"]), []).append(a["name"])
    with open(os.path.join(ROOT, "data/patch.json")) as fh:
        bracket = json.load(fh).get("standard", "phantom")
    usage, path = None, os.path.join(ROOT, "search/out/usage.json")
    if os.path.exists(path):
        with open(path) as fh:
            usage = json.load(fh).get(bracket)
    with open(os.path.join(WEB, "data", "maker.json"), "w") as fh:
        json.dump({"bracket": bracket, "components": comps, "utility": util, "hero_cc": cc, "usage": usage}, fh,
                  separators=(",", ":"))


def counters_data():
    """data/counters/index.json and heroes/<id>.json for the Counter items tab: the sim values from
    counters/out/sim.json (counters/scripts/export_sim.py) and the real-match buy triggers and win edges from
    counters/out/report.json + triggers.json (counters/scripts/report.py, triggers.py). Returns heroes written."""
    src = os.path.join(ROOT, "counters/out/sim.json")
    if not os.path.exists(src):
        return 0
    with open(src) as fh:
        sim = json.load(fh)
    real = {}
    rep_p, trig_p = os.path.join(ROOT, "counters/out/report.json"), os.path.join(ROOT, "counters/out/triggers.json")
    if os.path.exists(rep_p) and os.path.exists(trig_p):
        with open(rep_p) as fh:
            rep = json.load(fh)
        with open(trig_p) as fh:
            trig = json.load(fh)
        ids = {v: k for k, v in sim["heroes"].items()}
        for n, r in rep["items"].items():
            we = r.get("win_edge", {}).get("all_own_position") or [None]
            real[n] = {"buy_rate": r.get("buy_rate"), "buy_minute": r.get("buy_minute", {}).get("median"),
                       "win_edge": we[0],
                       "hero_lift": {ids[t["name"]]: round(t["rate_ratio"], 3) for t in trig.get(n, [])
                                     if t["kind"] == "hero" and t["name"] in ids}}
        real = {"matches": rep.get("matches"), "items": real}
    out = os.path.join(WEB, "data", "counters")
    os.makedirs(os.path.join(out, "heroes"), exist_ok=True)
    idx = {k: sim[k] for k in ("bracket", "built", "items", "heroes")}
    idx["real"] = real
    idx["budgets"] = {b: {k: d[k] for k in ("enemies", "weights", "items", "enemy")} for b, d in sim["budgets"].items()}
    with open(os.path.join(out, "index.json"), "w") as fh:
        json.dump(idx, fh, separators=(",", ":"))
    heroes = sorted({h for d in sim["budgets"].values() for h in d["hero"]})
    for h in heroes:
        with open(os.path.join(out, "heroes", f"{h}.json"), "w") as fh:
            json.dump({b: d["hero"][h] for b, d in sim["budgets"].items() if h in d["hero"]}, fh, separators=(",", ":"))
    return len(heroes)


def win_edge_data(data):
    """data/win_edge.json: real per-hero item win edge (refreshed from Ritualist+ matches by each patch rerun,
    pipeline/refresh_win_edge.py), hero id -> item id -> [edge, se] in win-rate points, for the overall tab."""
    path = os.path.join(ROOT, "analysis/out/hero_item_edge.json")
    if not os.path.exists(path):
        return
    with open(path) as fh:
        d = json.load(fh)
    heroes = {h: {i: [round(v[0], 2), round(v[1], 2)] for i, v in items.items()} for h, items in d["heroes"].items()}
    with open(os.path.join(data, "win_edge.json"), "w") as fh:
        json.dump({"meta": d["meta"], "heroes": heroes}, fh, separators=(",", ":"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pyodide", help="folder with an extracted pyodide-core release (copied to vendor/pyodide)")
    a = ap.parse_args()
    data = os.path.join(WEB, "data")
    os.makedirs(data, exist_ok=True)
    shutil.copy(os.path.join(ROOT, "search/out/items.json"), os.path.join(data, "items.json"))
    shutil.copy(os.path.join(ROOT, "data/patch.json"), os.path.join(data, "patch.json"))
    if os.path.exists(os.path.join(ROOT, "data/changes.json")):   # pipeline/changes.py: what each rerun changed
        shutil.copy(os.path.join(ROOT, "data/changes.json"), os.path.join(data, "changes.json"))
    # ranked aim spread; Graves and Danny (no hero accuracy in match stats) get their replay-fitted rows
    with open(os.path.join(ROOT, "sim/data/skill_defaults.json")) as fh:
        aim = json.load(fh)
    cal = os.path.join(ROOT, "sim/data/gun_calibration.json")
    if os.path.exists(cal):
        with open(cal) as fh:
            for hid, row in json.load(fh)["heroes"].items():
                aim["heroes"].setdefault(hid, row)
    with open(os.path.join(data, "skill_defaults.json"), "w") as fh:
        json.dump(aim, fh)
    win_edge_data(data)
    # Phantom+ benchmarks for the Improvements tab (analysis/scripts/improve_benchmarks.cjs)
    bench = os.path.join(ROOT, "analysis/out/improve_benchmarks.json")
    if os.path.exists(bench):
        shutil.copy(bench, os.path.join(data, "improve.json"))
    with open(os.path.join(ROOT, "damage/out/index.json")) as fh:
        heroes = [{"id": h["id"], "name": h["name"]} for h in json.load(fh)["heroes"]]
    with open(os.path.join(data, "heroes.json"), "w") as fh:
        json.dump(sorted(heroes, key=lambda h: h["name"]), fh)
    # every playable hero's name, sim or not, so a real match with a hero the sim doesn't have yet still names it
    with open(os.path.join(ROOT, "data/game/raw/heroes.json")) as fh:
        names = {h["id"]: h["name"] for h in json.load(fh) if h.get("player_selectable") and not h.get("disabled")}
    with open(os.path.join(data, "hero_names.json"), "w") as fh:
        json.dump(names, fh)
    counts = {k: copy_out(os.path.join(ROOT, src), os.path.join(data, k))
              for k, src in [("damage", "damage/out"), ("overall", "damage/out/overall"), ("path", "damage/out/path"), ("duel", "search/out"), ("tank", "survival/out")]}
    for name, key in (("order", "buy_order"), ("skill", "ability_order")):
        files = glob.glob(os.path.join(ROOT, "damage/out", name, "*.json"))
        os.makedirs(os.path.join(data, "damage", name), exist_ok=True)
        for f in files:
            with open(f) as fh:
                d = json.load(fh)
            with open(os.path.join(data, "damage", name, os.path.basename(f)), "w") as fh:
                json.dump(d, fh, separators=(",", ":"))
        counts[key] = len(files)
    maker_data()
    counts["counters"] = counters_data()
    os.makedirs(os.path.join(WEB, "py"), exist_ok=True)
    build_zip(os.path.join(WEB, "py", "sim.zip"))
    if a.pyodide:
        dst = os.path.join(WEB, "vendor", "pyodide")
        os.makedirs(dst, exist_ok=True)
        for f in PYODIDE_FILES:
            shutil.copy(os.path.join(a.pyodide, f), dst)
    full_std = os.path.join(WEB, "vendor", "pyodide", "python_stdlib.zip")
    if os.path.exists(full_std):
        build_stdlib(full_std, os.path.join(WEB, "py", "stdlib.zip"))
    # the Artifact preview wraps the page in its own document, so it gets the body without the wrapper tags
    with open(os.path.join(WEB, "index.html")) as fh:
        html = fh.read()
    head = html[html.index("<head>") + 6:html.index("</head>")]
    body = html[html.index("<body>") + 6:html.index("</body>")]
    head = "\n".join(l for l in head.splitlines() if "charset" not in l and 'name="viewport"' not in l)
    with open(os.path.join(WEB, "artifact.html"), "w") as fh:
        fh.write(head.strip() + "\n<script>window.__ARTIFACT__ = 1;</script>\n" + body.strip() + "\n")
    for z in ["py/sim.zip", "py/stdlib.zip", "vendor/pyodide/python_stdlib.zip"]:
        if os.path.exists(os.path.join(WEB, z)):
            with open(os.path.join(WEB, z), "rb") as fh, open(os.path.join(WEB, z + ".b64.txt"), "w") as out:
                out.write(base64.b64encode(fh.read()).decode())
    sizes = {z: os.path.getsize(os.path.join(WEB, "py", z)) // 1024 for z in ("sim.zip", "stdlib.zip")
             if os.path.exists(os.path.join(WEB, "py", z))}
    print("files copied:", counts, "|", ", ".join(f"{k} {v} KB" for k, v in sizes.items()), "| .pyc" if PYC else "| .py")


if __name__ == "__main__":
    main()
