"""Build the static site's data: python3 build.py [--pyodide DIR]

Fills web/data (JSON the page reads), web/py/sim.zip (deadsim + game data + dummy.py + bridge.py, unpacked into
Pyodide's file system) and web/vendor/pyodide (self-hosted Pyodide core, so the page needs no CDN). Stdlib only.
Re-run after the sim or any search output changes; lists load whatever exists.
"""
import argparse
import base64
import glob
import json
import os
import shutil
import zipfile

ROOT = os.environ.get("DEADSIM_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root (the folder holding sim/, data/, damage/ ...)
WEB = os.path.dirname(os.path.abspath(__file__))
PYODIDE_FILES = ["pyodide.js", "pyodide.asm.js", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]


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


def build_zip(path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in glob.glob(os.path.join(ROOT, "sim/deadsim/**/*.py"), recursive=True):
            z.write(f, os.path.relpath(f, ROOT))
        for f in glob.glob(os.path.join(ROOT, "sim/data/*.json")):
            z.write(f, os.path.relpath(f, ROOT))
        for name in ["abilities.json", "heroes.json", "shop_items.json", "weapons.json", "raw/items.json"]:
            z.write(os.path.join(ROOT, "data/game", name), "data/game/" + name)
        for fn, body in slim_ability_orders().items():
            z.writestr("data/builds/aggregates/per_hero/" + fn, body)
        z.write(os.path.join(ROOT, "damage/dummy.py"), "damage/dummy.py")
        z.write(os.path.join(WEB, "bridge.py"), "damage/bridge.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pyodide", help="folder with an extracted pyodide-core release (copied to vendor/pyodide)")
    a = ap.parse_args()
    data = os.path.join(WEB, "data")
    os.makedirs(data, exist_ok=True)
    shutil.copy(os.path.join(ROOT, "search/out/items.json"), os.path.join(data, "items.json"))
    shutil.copy(os.path.join(ROOT, "data/patch.json"), os.path.join(data, "patch.json"))
    with open(os.path.join(ROOT, "damage/out/index.json")) as fh:
        heroes = [{"id": h["id"], "name": h["name"]} for h in json.load(fh)["heroes"]]
    with open(os.path.join(data, "heroes.json"), "w") as fh:
        json.dump(sorted(heroes, key=lambda h: h["name"]), fh)
    counts = {k: copy_out(os.path.join(ROOT, src), os.path.join(data, k))
              for k, src in [("damage", "damage/out"), ("duel", "search/out"), ("tank", "survival/out")]}
    os.makedirs(os.path.join(WEB, "py"), exist_ok=True)
    build_zip(os.path.join(WEB, "py", "sim.zip"))
    if a.pyodide:
        dst = os.path.join(WEB, "vendor", "pyodide")
        os.makedirs(dst, exist_ok=True)
        for f in PYODIDE_FILES:
            shutil.copy(os.path.join(a.pyodide, f), dst)
    # the Artifact preview wraps the page in its own document, so it gets the body without the wrapper tags
    with open(os.path.join(WEB, "index.html")) as fh:
        html = fh.read()
    head = html[html.index("<head>") + 6:html.index("</head>")]
    body = html[html.index("<body>") + 6:html.index("</body>")]
    head = "\n".join(l for l in head.splitlines() if "charset" not in l and 'name="viewport"' not in l)
    with open(os.path.join(WEB, "artifact.html"), "w") as fh:
        fh.write(head.strip() + "\n<script>window.__ARTIFACT__ = 1;</script>\n" + body.strip() + "\n")
    for z in ["py/sim.zip", "vendor/pyodide/python_stdlib.zip"]:
        if os.path.exists(os.path.join(WEB, z)):
            with open(os.path.join(WEB, z), "rb") as fh, open(os.path.join(WEB, z + ".b64.txt"), "w") as out:
                out.write(base64.b64encode(fh.read()).decode())
    print("files copied:", counts, "| sim.zip", os.path.getsize(os.path.join(WEB, "py", "sim.zip")) // 1024, "KB")


if __name__ == "__main__":
    main()
