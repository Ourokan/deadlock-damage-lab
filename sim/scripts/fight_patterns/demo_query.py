"""Run one SQL query on a match replay (Deadlock API /v1/matches/demo/query) and save the NDJSON result.

usage: python3 -I demo_query.py <match_id> <sql file|-> <out.ndjson>   (needs node for zstd)
"""
import json, sys, time, urllib.request, subprocess
API = "https://api.deadlock-api.com/v1/matches/demo/query"
UA = {"User-Agent": "deadlock-build-sim/0.1 (research)", "Content-Type": "application/json"}
def run(mid, sql, out):
    body = json.dumps({"match_id": int(mid), "query": sql, "format": "ndjson"}).encode()
    for i in range(6):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(API, body, UA), timeout=60)); break
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            if e.code in (400, 404): raise SystemExit(f"{e.code} {msg}")
            time.sleep(20 * (i + 1))
    jid = r["job_id"]
    while True:
        s = json.load(urllib.request.urlopen(urllib.request.Request(f"{API}/{jid}", headers=UA), timeout=60))
        if s["status"] == "done": break
        if s["status"] == "failed": raise SystemExit("failed: " + str(s.get("error"))[:500])
        time.sleep(min(30, max(5, (s.get("estimated_wait_seconds") or 10) / 2)))
    raw = urllib.request.urlopen(urllib.request.Request(s["result_url"], headers=UA), timeout=300).read()
    data = subprocess.run(["node", "-e", "process.stdout.write(require('zlib').zstdDecompressSync(require('fs').readFileSync(0)))"], input=raw, capture_output=True).stdout if s["result_url"].endswith(".zst") else raw
    open(out, "wb").write(data)
    return out
if __name__ == "__main__":
    sql = sys.stdin.read() if sys.argv[2] == "-" else open(sys.argv[2]).read()
    print(run(sys.argv[1], sql, sys.argv[3]))
