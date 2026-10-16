"""Run sim/scripts/landing_rates.py --hero X with deadsim.mechanics on. usage: lr_mech.py SIM summons|parry|... k=v ... -- args"""
import sys, os
SIM = sys.argv[1]
sys.path.insert(0, SIM); sys.path.insert(0, os.path.join(SIM, "scripts"))
i = sys.argv.index("--")
opts, rest = sys.argv[2:i], sys.argv[i + 1:]
import deadsim.mechanics as M
mk, sk = {}, {}
for o in opts:
    k, v = o.split("=")
    (mk if k in M.Mechanics.__dataclass_fields__ else sk)[k] = (v == "1") if k in ("parry", "summons", "movement") else float(v)
M.DEFAULT = M.Mechanics(**mk)
import landing_rates as L
orig = L.skill_of
def skill_of(p):
    s = orig(p)
    for k, v in sk.items():
        setattr(s, k, v)
    return s
L.skill_of = skill_of
sys.argv = ["landing_rates.py"] + rest
print("mechanics", M.DEFAULT, "skill", sk, flush=True)
L.main()
