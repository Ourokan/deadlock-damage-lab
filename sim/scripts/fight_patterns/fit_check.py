"""Per hero: real damage mix fit with fight patterns off (slot order) vs on, as the mean |log landing factor| of
scripts/landing_rates.py --hero. A pattern is kept when it fits no worse than slot order (data/fight_patterns.json).

usage: python3 fit_check.py <out.json> [mech]
"""
import sys, os, io, json, math, contextlib, collections
SIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, SIM); sys.path.insert(0, SIM + "/scripts")
mech = len(sys.argv) > 2
OUT = sys.argv[1]
import deadsim.mechanics as M
if not mech:
    M.DEFAULT = None
import landing_rates as L
from deadsim import game
G = game()
orig = L.skill_of
MODE = {"on": True}
def skill_of(p):
    s = orig(p); s.fight_pattern = MODE["on"]; return s
L.skill_of = skill_of
import re
out = {}
for hid in sorted(G.heroes):
    h = G.hero(hid); out[h.name] = {}
    for on in (False, True):
        MODE["on"] = on
        sys.argv = ["x", "100000", "4", "--hero", h.name]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            L.main()
        txt = buf.getvalue()
        lands = {m.group(1).strip(): float(m.group(2)) for m in re.finditer(r"landing (.+?)\s+([\d.]+)$", txt, re.M)}
        out[h.name]["on" if on else "off"] = lands
    off, on_ = out[h.name]["off"], out[h.name]["on"]
    err = lambda d: sum(abs(math.log(max(v, 0.01))) for v in d.values()) / max(1, len(d))
    out[h.name]["err"] = [round(err(off), 3), round(err(on_), 3)]
    print(f"{h.name:15} err off {err(off):.2f} on {err(on_):.2f}  " + " ".join(f"{k}:{off.get(k)}->{on_.get(k)}" for k in on_ if off.get(k) != on_.get(k)), flush=True)
json.dump(out, open(OUT, "w"), indent=1)
