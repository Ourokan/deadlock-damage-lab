// Runs the Python combat sim (deadsim) in Pyodide, off the page's main thread.
// Messages in: {type:"init", base} then {type:"run"|"breakdown"|"team", id, req}. Out: {type:"ready"|"result"|"error", ...}.
let py = null;

// b64: the Artifact preview can't serve .zip files, so it gets them as base64 text (written by build.py)
async function getZip(url, b64) {
  if (!b64) return (await fetch(url)).arrayBuffer();
  const bin = atob((await (await fetch(url + ".b64.txt")).text()).trim());
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out.buffer;
}

async function init(base, b64) {
  importScripts(base + "vendor/pyodide/pyodide.js");
  const opts = { indexURL: base + "vendor/pyodide/" };
  if (b64) opts.stdLibURL = URL.createObjectURL(new Blob([await getZip(base + "vendor/pyodide/python_stdlib.zip", true)]));
  py = await loadPyodide(opts);
  const zip = await getZip(base + "py/sim.zip", b64);
  py.unpackArchive(zip, "zip", { extractDir: "/app" });
  py.runPython(`
import sys
sys.path[:0] = ["/app/sim", "/app/damage"]
from bridge import run, breakdown, team
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
    } else if (m.type === "run" || m.type === "breakdown" || m.type === "team") {
      const t = performance.now();
      const out = py.globals.get(m.type)(JSON.stringify(m.req));
      self.postMessage({ type: "result", id: m.id, result: JSON.parse(out), ms: performance.now() - t });
    }
  } catch (err) {
    self.postMessage({ type: "error", id: m.id, message: String(err && err.message || err) });
  }
};
