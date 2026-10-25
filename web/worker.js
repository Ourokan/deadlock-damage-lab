// Runs the Python combat sim (deadsim) in Pyodide, off the page's main thread.
// Messages in: {type:"init", base} then {type:"run"|"breakdown"|"team"|"maker"|"replay", id, req}. Out: {type:"ready"|"result"|"error", ...}.
// {type:"modules"} answers {type:"modules", names}: the stdlib modules imported so far (browser_test.cjs --record-stdlib).
let py = null;

// b64: the Artifact preview can't serve .zip files, so it gets them as base64 text (written by build.py)
async function getZip(url, b64) {
  if (!b64) return (await fetch(url)).arrayBuffer();
  const bin = atob((await (await fetch(url + ".b64.txt")).text()).trim());
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out.buffer;
}

// The slim stdlib (py/stdlib.zip, build.py) holds only what the site imports. Importing anything else the full stdlib
// has (listed in _full_stdlib.py; a new code path) misses it, and this finder, last on sys.meta_path, then fetches
// Pyodide's full stdlib once (a synchronous request, fine in a worker), mounts it behind the slim one and retries, so
// the import still works, just slower.
const FULL_STDLIB_FINDER = `
import sys, importlib, importlib.abc, importlib.machinery
from _full_stdlib import MODULES as _FULL
class _FullStdlib(importlib.abc.MetaPathFinder):
    done = False
    def find_spec(self, name, path=None, target=None):
        if self.done or name not in _FULL:
            return None
        self.done = True
        import js
        js.loadFullStdlib(name)
        sys.path.append("/lib/full_stdlib.zip")
        for m in list(sys.modules.values()):   # packages already imported from the slim zip look in the full one too
            p = getattr(m, "__path__", None)
            if isinstance(p, list):
                p += [x.replace("/lib/python312.zip", "/lib/full_stdlib.zip") for x in p if x.startswith("/lib/python312.zip")]
        importlib.invalidate_caches()
        return importlib.machinery.PathFinder.find_spec(name, path, target)
sys.meta_path.append(_FullStdlib())
`;

async function init(base, b64) {
  // the sim bundle downloads while Pyodide starts
  const simZip = getZip(base + "py/sim.zip", b64);
  importScripts(base + "vendor/pyodide/pyodide.js");
  const opts = { indexURL: base + "vendor/pyodide/" };
  opts.stdLibURL = b64 ? URL.createObjectURL(new Blob([await getZip(base + "py/stdlib.zip", true)])) : base + "py/stdlib.zip";
  py = await loadPyodide(opts);
  self.loadFullStdlib = (name) => {
    console.warn(`[sim] ${name} is not in the slim stdlib (web/stdlib_keep.txt): loading the full stdlib`);
    const x = new XMLHttpRequest();
    x.open("GET", base + "vendor/pyodide/python_stdlib.zip" + (b64 ? ".b64.txt" : ""), false);
    if (!b64) x.responseType = "arraybuffer";
    x.send();
    let bytes;
    if (b64) { const bin = atob(x.responseText.trim()); bytes = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i); }
    else bytes = new Uint8Array(x.response);
    py.FS.writeFile("/lib/full_stdlib.zip", bytes);
  };
  py.runPython(FULL_STDLIB_FINDER);
  py.unpackArchive(await simZip, "zip", { extractDir: "/app" });
  py.runPython(`
import sys
sys.path[:0] = ["/app/sim", "/app/damage"]
from bridge import run, breakdown, team, maker, replay
from deadsim.data import game
game()
`);
}

self.onmessage = async (e) => {
  const m = e.data;
  try {
    if (m.type === "init") {
      await init(m.base, m.b64);
      self.postMessage({ type: "ready" });
    } else if (m.type === "modules") {
      self.postMessage({ type: "modules", names: py.runPython("' '.join(sorted(m for m in sys.modules if m in _FULL))").split(" ") });
    } else if (m.type === "run" || m.type === "breakdown" || m.type === "team" || m.type === "maker" || m.type === "replay") {
      const t = performance.now();
      const out = py.globals.get(m.type)(JSON.stringify(m.req));
      self.postMessage({ type: "result", id: m.id, result: JSON.parse(out), ms: performance.now() - t });
    }
  } catch (err) {
    self.postMessage({ type: "error", id: m.id, message: String(err && err.message || err) });
  }
};
