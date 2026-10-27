// Browser test of the built site: node web/tests/browser_test.cjs [--shots DIR]
//
// Serves web/ (after `python3 web/build.py --pyodide DIR`) on localhost, opens it in headless Chromium at desktop and
// phone size and goes through every tab: the live sim loads in Pyodide, the damage test, item breakdown, build maker,
// real match (a made-up match served in place of the Deadlock API) and its fight replay, team fight and every precomputed tab with its
// Test button. Fails on any page or worker error (JS or Python), console error, local file that 404s, request to an
// unexpected host, error box left showing, or (on the phone) a page wider than the screen.
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium, devices } = require("playwright");

const WEB = path.resolve(__dirname, "..");
const args = process.argv.slice(2);
const SHOTS = args.includes("--shots") ? path.resolve(args[args.indexOf("--shots") + 1]) : null;
// --record-stdlib: rewrite web/stdlib_keep.txt with the stdlib modules the sim workers imported over the whole test
const RECORD_STDLIB = args.includes("--record-stdlib");
const KEEP = path.join(WEB, "stdlib_keep.txt");
const imported = new Set();
const SIM_LOAD_MS = 180000;
const STEP_MS = 90000;
const MATCH_ID = 990000001;
// hosts the page may ask for: Google Fonts (dropped, the page falls back to system fonts) and the Deadlock API (the
// Real match tab, answered with a made-up match)
const FONT_HOSTS = ["fonts.googleapis.com", "fonts.gstatic.com"];
const API_HOST = "api.deadlock-api.com";

const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json",
  ".wasm": "application/wasm", ".zip": "application/zip", ".txt": "text/plain", ".mjs": "text/javascript" };

// ---------- static server ----------
function serve(missing) {
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, "http://x");
    let p = path.normalize(path.join(WEB, decodeURIComponent(url.pathname)));
    if (p !== WEB && !p.startsWith(WEB + path.sep)) { res.writeHead(403).end(); return; }
    if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, "index.html");
    if (!fs.existsSync(p)) { missing.push(url.pathname); res.writeHead(404).end("not found"); return; }
    res.writeHead(200, { "Content-Type": TYPES[path.extname(p)] || "application/octet-stream", "Cache-Control": "no-store" });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise((ok) => server.listen(0, "127.0.0.1", () => ok(server)));
}

// ---------- made-up match for the Real match tab (bulk /v1/matches/metadata shape) ----------
function fakeMatch() {
  const read = (f) => JSON.parse(fs.readFileSync(path.join(WEB, "data", f)));
  const heroes = read("heroes.json").filter((h) => fs.existsSync(path.join(WEB, "data/damage/heroes", `${h.id}.json`))).slice(0, 12);
  if (heroes.length < 2) throw new Error("web/data/damage has fewer than 2 heroes: run web/build.py first");
  const duration = 1800;
  // the last player is a hero the sim doesn't have yet when there is one (a new hero in real matches): the page
  // still names it and leaves it out of the sims
  const known = new Set(read("heroes.json").map((h) => String(h.id)));
  const NEW_HERO = Object.keys(read("hero_names.json")).find((id) => !known.has(id));
  const players = heroes.map((h, k) => {
    const d = read(`damage/heroes/${h.id}.json`);
    const items = (d.budgets["27000"] || Object.values(d.budgets)[0]).popular.items;
    return {
      player_slot: k + 1, account_id: 1000 + k, hero_id: NEW_HERO && k === heroes.length - 1 ? Number(NEW_HERO) : h.id, team: `Team${k % 2}`, assigned_lane: [1, 4, 6][Math.floor(k / 2) % 3],
      kills: 5, deaths: 4, assists: 8, net_worth: 30000 + 500 * k,
      items: items.map((id, i) => ({ item_id: id, game_time_s: 120 + i * 120, sold_time_s: 0 })),
      stats: [300, 600, 900, 1200, 1500].map((t) => ({ time_stamp_s: t, net_worth: Math.round((30000 * t) / duration) })),
      final_stats: { custom_user_stats: { "Enemy Hero Accuracy##Shots": 2000, "Enemy Hero Accuracy##Hits": 700, "Enemy Hero Accuracy##Headshots": 90 } },
    };
  });
  return [{ match_id: MATCH_ID, duration_s: duration, players }];
}

// the same match in the single-match shape with match_paths and death_details, for the fight replay: players 1
// (Amber) and 2 (Sapphire) fight 15 m apart from 600 s to 612 s and player 2 dies; everyone else stands far off
function fakeReplay() {
  const m = fakeMatch()[0], n = m.duration_s + 1;
  const paths = m.players.map((p) => {
    const k = p.player_slot, x = Array(n).fill(1000 + 1200 * k), y = Array(n).fill(0), hp = Array(n).fill(100), c = Array(n).fill(0);
    if (k <= 2) {
      for (let t = 600; t <= 612; t++) {
        x[t] = 8000 + (k === 2 ? 600 : 0); y[t] = 16000; c[t] = 1;
        hp[t] = k === 2 ? Math.max(0, 100 - 9 * (t - 599)) : 100 - Math.floor((t - 599) / 3) * 4;
      }
      for (let t = 613; t < n; t++) hp[t] = k === 2 && t < 630 ? 0 : hp[612] || 100;
    }
    return { player_slot: String(k), x_min: "0", x_max: "16383", y_min: "0", y_max: "16383", x_pos: x, y_pos: y, health: hp, combat_type: c };
  });
  const players = m.players.map((p) => ({ ...p, death_details: p.player_slot === 2 ? [{ game_time_s: 612, killer_player_slot: 1, time_to_kill_s: 10 }] : [] }));
  return { match_info: { ...m, players, match_paths: { interval_s: 1, x_resolution: 16383, y_resolution: 16383, paths } } };
}

// the signed-in player (Steam sign-in): account 1000 is player 1 of the made-up match; their match history is three
// matches on that hero, each served in the single-match shape with the per-snapshot aim stats Aim.matchStats reads
const PLAYER = 1000, AIM_MATCHES = [MATCH_ID + 1, MATCH_ID + 2, MATCH_ID + 3];
function fakePlayer() {
  const p = fakeMatch()[0].players[0];
  const names = ["Enemy Hero Accuracy##Shots", "Enemy Hero Accuracy##Hits", "Enemy Hero Accuracy##Headshots", "Outgoing Bullet Dist##20"];
  const vals = [2000, 700, 90, 500];
  const meta = { match_info: { custom_user_stats: names.map((name, id) => ({ id, name })), players: [{ ...p,
    stats: p.stats.map((x) => ({ ...x, custom_user_stats: vals.map((value, id) => ({ id, value })) })) }] } };
  const history = AIM_MATCHES.map((match_id, k) => ({ match_id, hero_id: p.hero_id, game_mode: 1, start_time: 1790000000 + k }));
  return { hero: p.hero_id, meta: JSON.stringify(meta), history: JSON.stringify(history),
    steam: JSON.stringify([{ account_id: PLAYER, personaname: "Test Player", avatar: null }]) };
}

// ---------- checks ----------
const failures = [];
function fail(where, msg) { failures.push(`[${where}] ${msg}`); console.log(`  FAIL ${msg}`); }

async function watch(context, where, base, missing) {
  const origin = new URL(base).origin, match = JSON.stringify(fakeMatch()), single = JSON.stringify(fakeReplay()), me = fakePlayer();
  const api = (route, body) => route.fulfill({ status: 200, contentType: "application/json", headers: { "access-control-allow-origin": "*" }, body });
  await context.route("**/*", (route) => {
    const u = new URL(route.request().url());
    if (u.origin === origin) return route.continue();
    if (FONT_HOSTS.includes(u.hostname)) return route.abort();
    if (u.hostname === API_HOST && u.pathname === "/v1/matches/metadata")
      return route.fulfill({ status: 200, contentType: "application/json", headers: { "access-control-allow-origin": "*" }, body: match });
    if (u.hostname === API_HOST && u.pathname === `/v1/matches/${MATCH_ID}/metadata`)
      return route.fulfill({ status: 200, contentType: "application/json", headers: { "access-control-allow-origin": "*" }, body: single });
    if (u.hostname === API_HOST && u.pathname === "/v1/players/steam") return api(route, me.steam);
    if (u.hostname === API_HOST && u.pathname === `/v1/players/${PLAYER}/match-history`) return api(route, me.history);
    if (u.hostname === API_HOST && AIM_MATCHES.some((m) => u.pathname === `/v1/matches/${m}/metadata`)) return api(route, me.meta);
    fail(where, `request to an unexpected host: ${u.href}`);
    return route.abort();
  });
  // worker.js answers {type:"error"} for Python exceptions; log those so they count like any console error
  await context.addInitScript(() => {
    const W = window.Worker;
    window.Worker = class extends W {
      constructor(...a) {
        super(...a);
        (window.__simWorkers ||= []).push(this);
        this.addEventListener("message", (e) => { if (e.data && e.data.type === "error") console.error("[sim worker] " + e.data.message); });
        this.addEventListener("error", (e) => console.error("[sim worker error] " + (e.message || e)));
      }
    };
  });
  const page = await context.newPage();
  page.on("pageerror", (e) => fail(where, `page error: ${e.message}`));
  page.on("console", (m) => { if (m.type() === "error" && !/net::ERR_FAILED/.test(m.text())) fail(where, `console error: ${m.text().slice(0, 2000)}`); });
  page.on("requestfailed", (r) => { if (new URL(r.url()).origin === origin) fail(where, `request failed: ${r.url()} ${r.failure()?.errorText}`); });
  page.on("response", (r) => { if (new URL(r.url()).origin === origin && r.status() >= 400) fail(where, `${r.status()} for ${new URL(r.url()).pathname}`); });
  page.on("worker", (w) => w.on("console", (m) => {
    if (m.type() === "error") fail(where, `worker console error: ${m.text().slice(0, 2000)}`);
    // worker.js had to fetch the full stdlib: add the module to web/stdlib_keep.txt (or rerun with --record-stdlib)
    else if (m.text().includes("not in the slim stdlib") && !RECORD_STDLIB) fail(where, m.text());
  }));
  return page;
}

// error boxes the page shows (.err elements: #err, #tf-err, #mk-msg, #m-status when bad, sim failures in #m-out)
async function errorBoxes(page) {
  return page.$$eval(".err", (els) => els.filter((e) => !e.hidden && e.offsetParent !== null && e.textContent.trim()).map((e) => `#${e.id || e.className}: ${e.textContent.trim()}`));
}

async function step(page, where, name, fn) {
  const t = Date.now(), before = failures.length;
  console.log(`- ${where}: ${name}`);
  try {
    await fn();
  } catch (e) {
    fail(where, `${name}: ${e.message.split("\n")[0]}`);
  }
  for (const b of await errorBoxes(page).catch(() => [])) fail(where, `${name}: error shown on the page: ${b}`);
  if (where === "phone") {
    const w = await page.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth]);
    if (w[0] > w[1] + 1) fail(where, `${name}: page is ${w[0]} px wide on a ${w[1]} px screen`);
  }
  if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `${where}-${name.replace(/\W+/g, "_")}.png`), fullPage: false }).catch(() => {});
  console.log(`  ${failures.length > before ? "failed" : "ok"} (${((Date.now() - t) / 1000).toFixed(1)} s)`);
  return failures.length === before;
}

const go = (page, hash) => page.evaluate((h) => { location.hash = h; }, hash);
// wait until the damage test has a live result newer than `after` (S.runId counts every sim request)
const liveResult = (page, after) => page.waitForFunction((n) => S.runId > n && S.last && S.last.res && S.last.res.timeline && !$("#run").disabled, after, { timeout: STEP_MS });
const runId = (page) => page.evaluate(() => S.runId);

// false when the sim never loaded (every later sim step would only time out)
async function testTab(page, where) {
  const loaded = await step(page, where, "sim loads", async () => {
    await page.waitForFunction(() => ["ready", "error"].includes($("#engine").dataset.state), null, { timeout: SIM_LOAD_MS });
    const st = await page.$eval("#engine", (e) => `${e.dataset.state}: ${e.textContent}`);
    if (!st.startsWith("ready")) throw new Error(`sim did not load (${st})`);
  });
  if (!loaded) return false;
  await step(page, where, "damage test runs", async () => {
    await liveResult(page, 0);
    const d = await page.evaluate(() => S.last.res.damage["15s"]);
    if (!(d > 0)) throw new Error(`15 s damage is ${d}`);
  });
  await step(page, where, "edits rerun by themselves", async () => {
    // an untouched preset build follows a hero change, and the test reruns without pressing Run
    let n = await runId(page);
    const abrams = await page.evaluate(() => S.heroes.find((h) => h.name === "Abrams").id);
    await page.selectOption("#a-hero", String(abrams));
    await liveResult(page, n);
    const st = await page.evaluate(() => ({ hero: S.last.req.hero, preset: S.A.preset, items: S.last.req.items.join(".") }));
    const pop = await page.evaluate(async (h) => (await damageHero(h)).budgets["27000"].popular.items.join("."), abrams);
    if (st.hero !== abrams || st.preset !== "popular" || st.items !== pop) throw new Error(`hero change kept the old build: ${JSON.stringify(st)}`);
    n = await runId(page);
    await page.click("#a-shop .it:not(.owned)");
    await liveResult(page, n);
    if (!(await page.$("#marks .dl"))) throw new Error("no change against the last run shown");
    // the summary bar shows while the result is out of view
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForSelector("#resbar:not([hidden])", { timeout: 5000 });
    // a bad number shows a plain message instead of running, and clears once fixed
    await page.fill("#d-hp", "");
    await page.waitForFunction(() => !$("#err").hidden && /max HP/.test($("#err").textContent), null, { timeout: 5000 });
    if (!(await page.$("#results.stale"))) throw new Error("old result not dimmed while the input is bad");
    n = await runId(page);
    await page.fill("#d-hp", "2700");
    await liveResult(page, n);
    if (!(await page.$eval("#err", (e) => e.hidden))) throw new Error("input error still shown after fixing it");
    if (await page.$("#results.stale")) throw new Error("result still dimmed after fixing the input");
  });
  await step(page, where, "preset build + enemy hero target", async () => {
    const n = await runId(page);
    await page.click('#presets [data-k="fight_15s"]');
    await page.click('#d-mode [data-v="hero"]');
    await page.click("#run");
    await liveResult(page, n);
    const d = await page.evaluate(() => S.last.res.damage["15s"]);
    if (!(d > 0)) throw new Error(`15 s damage vs a hero is ${d}`);
    await page.click('#d-mode [data-v="plain"]');
  });
  await step(page, where, "item breakdown", async () => {
    await page.click("#res-build .build.tap .it");
    await page.waitForFunction(() => BD.data, null, { timeout: STEP_MS });
    const e = await page.evaluate(() => BD.data.error);
    if (e) throw new Error(`breakdown failed: ${e}`);
    await whyTab(page);
    await page.click("#sh-close");
  });
  return true;
}

// the item sheet's Why tab: what the item does, every item of the build, and nothing wider than the sheet
async function whyTab(page) {
  await page.click('#sh-tabs [data-v="why"]');
  const ids = await page.evaluate(() => BD.data.items.map((x) => x.id));
  for (const id of ids) {
    await page.evaluate((i) => { BD.item = i; renderSheet(); }, id);
    const txt = await page.$eval("#sh-body", (b) => b.textContent);
    if (!(await page.$("#sh-body .why li"))) throw new Error(`no Why text for item ${id}`);
    if (/isn't counted yet|was picked for dealing/.test(txt)) throw new Error(`old Why text for item ${id}: ${txt.slice(0, 200)}`);
    const wide = await page.$eval(".sheet-in", (e) => e.scrollWidth > e.clientWidth + 1);
    if (wide) throw new Error(`the item sheet scrolls sideways for item ${id}`);
  }
  await page.click('#sh-tabs [data-v="damage"]');
}

// sign in by typing a Steam ID: the damage test switches to the player's own aim on the hero and "My last match"
// loads their items; then Steam's sign-in coming back to the page (a fresh page, the sim not awaited)
async function signInTab(page, where, base) {
  const me = fakePlayer();
  await step(page, where, "steam sign-in", async () => {
    await page.selectOption("#a-hero", String(me.hero));
    await page.click("#acct-who");
    await page.fill("#acct-id", String(PLAYER));
    let n = await runId(page);
    await page.click('#acct-pop button[type="submit"]');
    await page.waitForFunction(() => /Test Player/.test($("#acct").textContent), null, { timeout: STEP_MS });
    await page.waitForFunction((after) => S.runId > after && S.A.aim === "mine" && S.last?.req?.accuracy === 0.35 && !$("#run").disabled, n, { timeout: STEP_MS });
    if (!/Your aim: 35\.0% accuracy/.test(await page.$eval("#a-pull-msg", (e) => e.textContent))) throw new Error("no note on the aim used");
    n = await runId(page);
    await page.click('#presets [data-k="mine"]');
    await liveResult(page, n);
    const st = await page.evaluate(() => ({ label: S.A.label, items: S.last.req.items.length }));
    if (st.label !== "My last match" || !st.items) throw new Error(`My last match didn't load a build: ${JSON.stringify(st)}`);
  });
  await step(page, where, "steam sign-in return", async () => {
    const p2 = await page.context().newPage();
    const id64 = (76561197960265728n + BigInt(PLAYER)).toString();
    const q = new URLSearchParams({ "openid.mode": "id_res", "openid.op_endpoint": "https://steamcommunity.com/openid/login",
      "openid.claimed_id": `https://steamcommunity.com/openid/id/${id64}` });
    await p2.goto(base + "?" + q + "#test", { waitUntil: "load" });
    await p2.waitForFunction(() => Account.current()?.via === "steam" && /Test Player/.test($("#acct").textContent), null, { timeout: STEP_MS });
    if (/openid/.test(p2.url())) throw new Error(`Steam's answer left in the address bar: ${p2.url()}`);
    await p2.close();
  });
}

async function makerTab(page, where) {
  await step(page, where, "build maker", async () => {
    await go(page, "maker");
    await page.waitForSelector("#mk-pop [data-b]", { timeout: STEP_MS });
    await page.click("#mk-pop [data-b]:not([data-b=clear])");
    await page.waitForSelector("#mk-sum .mk-tot", { timeout: STEP_MS });
    await page.waitForFunction(() => MK.sugTotal > 0 && MK.sugg.length >= Math.min(4, MK.sugTotal), null, { timeout: SIM_LOAD_MS });
    const n = await page.$$eval("#mk-sugg .mk-sug", (x) => x.length);
    if (!n) throw new Error("no suggestions shown");
    // signed in (signInTab): your side uses your own aim
    if (await page.$eval("#mk-aim", (e) => e.value) !== "mine") throw new Error("the build maker isn't on the signed-in player's aim");
    await page.waitForFunction(() => /Your aim/.test($("#mk-aim-msg").textContent), null, { timeout: STEP_MS });
  });
}

async function matchTab(page, where) {
  await step(page, where, "real match", async () => {
    await go(page, "match");
    await page.fill("#m-id", String(MATCH_ID));
    await page.click("#m-load");
    await page.waitForSelector("#m-pick:not([hidden])", { timeout: STEP_MS });
    // every hero has its name, also one the sim doesn't have yet
    const unnamed = await page.$eval("#tab-match", (e) => (e.textContent.match(/\bHero \d+/) || [])[0]);
    if (unnamed) throw new Error(`a hero shows as "${unnamed}"`);
    await page.click("#m-go");
    await page.waitForFunction(() => /Best single swaps/.test($("#m-out").textContent) || $("#m-out .err"), null, { timeout: SIM_LOAD_MS });
  });
  await step(page, where, "fight replay", async () => {
    // the made-up match has one fight, player 1 against player 2 (the default player), and player 2 dies
    await page.waitForSelector("#r-list [data-rf]", { timeout: STEP_MS });
    await page.click("#r-list [data-rf]");
    await page.waitForSelector("#r-out .r-table", { timeout: SIM_LOAD_MS });
    if (!(await page.$("#r-fight .r-map polyline"))) throw new Error("no fight map");
    const real = await page.$eval("#r-out .r-sum", (e) => e.textContent);
    if (!/Real fight/.test(real)) throw new Error(`no real outcome: ${real}`);
    // the map's 10 m scale sits inside the drawing, not cut off below it
    const clip = await page.$eval("#r-fight .r-map", (svg) => { const a = svg.getBoundingClientRect(), b = svg.querySelector("text.r-scale").getBoundingClientRect(); return b.bottom > a.bottom + 1 || b.top < a.top; });
    if (clip) throw new Error("the map's 10 m scale is cut off");
    // drop an item: the replay reruns with the changed items next to the real ones
    await page.click("#r-fight .r-card.me [data-rdrop]");
    await page.waitForFunction(() => /Changed: end/.test($("#r-out").textContent) || $("#r-out .err"), null, { timeout: STEP_MS });
    await page.click("#r-swaps");
    await page.waitForFunction(() => /Best single swaps for/.test($("#r-out").textContent) || $("#r-out .err"), null, { timeout: SIM_LOAD_MS });
  });
}

async function teamTab(page, where) {
  await step(page, where, "team fight", async () => {
    await go(page, "team");
    await page.waitForSelector("#tf-run:not([disabled])", { timeout: STEP_MS });
    await page.click("#tf-run");
    await page.waitForFunction(() => $("#tf-out table") || !$("#tf-err").hidden, null, { timeout: STEP_MS });
  });
}

const STATIC_TABS = [["overall", "#o-out"], ["path", "#p-out"], ["damage", "#g-out"], ["duel", "#u-out"], ["tank", "#t-out"], ["counter", "#k-out"], ["changes", "#c-out"]];
async function staticTabs(page, where, sim) {
  for (const [tab, out] of STATIC_TABS) {
    await step(page, where, `${tab} tab`, async () => {
      await go(page, tab);
      await page.waitForFunction((s) => $(s).children.length > 0, out, { timeout: 30000 });
      const btn = await page.$(`${out} [data-test]`);
      if (!sim) return;
      if (tab === "overall") {
        // an item of the best overall build: the sheet compares it with the popular pick it stands in for
        await page.click(`${out} .card .build.tap .it`);
        await page.waitForFunction(() => BD.data, null, { timeout: STEP_MS });
        const e = await page.evaluate(() => BD.data.error);
        if (e) throw new Error(`breakdown failed: ${e}`);
        await whyTab(page);
        await page.click("#sh-close");
      }
      if (!btn) {
        // a fresh What changed log can have no rows; the Counter items tab is a table of items, not builds
        if (tab !== "changes" && tab !== "counter") throw new Error("no Test button in the tab");
        return;
      }
      const n = await runId(page);
      await btn.click();
      await liveResult(page, n);
    });
  }
}

async function run(browser, base, where, contextOpts, missing) {
  console.log(`\n== ${where} ==`);
  const context = await browser.newContext(contextOpts);
  const page = await watch(context, where, base, missing);
  await page.goto(base + "#test", { waitUntil: "load" });
  await step(page, where, "every tab in the header", async () => {
    // all tab links show on screen: none hidden past the edge of the header
    const off = await page.$$eval("#tabs a", (as) => as.filter((a) => { const r = a.getBoundingClientRect(), n = a.parentElement.getBoundingClientRect();
      return !r.width || r.right > Math.min(innerWidth, n.right) + 1 || r.bottom > n.bottom + 1; }).map((a) => a.textContent));
    if (off.length) throw new Error(`tabs out of view: ${off.join(", ")}`);
  });
  const sim = await testTab(page, where);
  if (sim) {
    await signInTab(page, where, base);
    await makerTab(page, where);
    await matchTab(page, where);
    await teamTab(page, where);
  } else console.log("  the sim did not load: skipping the build maker, real match, team fight and Test buttons");
  await staticTabs(page, where, sim);
  if (RECORD_STDLIB) {
    const names = await page.evaluate(() => Promise.all((window.__simWorkers || []).map((w) => new Promise((ok) => {
      const f = (e) => { if (e.data?.type === "modules") { w.removeEventListener("message", f); ok(e.data.names); } };
      w.addEventListener("message", f); w.postMessage({ type: "modules" }); setTimeout(() => ok([]), 5000);
    }))));
    for (const n of names.flat()) imported.add(n);
  }
  await context.close();
}

(async () => {
  if (!fs.existsSync(path.join(WEB, "py/sim.zip")) || !fs.existsSync(path.join(WEB, "vendor/pyodide/pyodide.js")))
    throw new Error("web/py/sim.zip or web/vendor/pyodide missing: run python3 web/build.py --pyodide DIR first");
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  const missing = [];
  const server = await serve(missing);
  const base = `http://127.0.0.1:${server.address().port}/`;
  const browser = await chromium.launch();
  try {
    await run(browser, base, "desktop", { viewport: { width: 1280, height: 900 } }, missing);
    const { defaultBrowserType, ...phone } = devices["iPhone 13"];
    await run(browser, base, "phone", phone, missing);
  } finally {
    await browser.close();
    server.close();
  }
  if (RECORD_STDLIB && imported.size) {
    const head = fs.readFileSync(KEEP, "utf8").split("\n").filter((l) => l.startsWith("#"));
    fs.writeFileSync(KEEP, [...head, ...[...imported].sort()].join("\n") + "\n");
    console.log(`\n${imported.size} stdlib modules written to ${KEEP}`);
  }
  for (const m of new Set(missing)) if (!failures.some((f) => f.includes(m))) failures.push(`[server] missing file ${m}`);
  if (failures.length) {
    console.log(`\n${failures.length} problem(s):\n` + failures.map((f) => "  " + f).join("\n"));
    process.exit(1);
  }
  console.log("\nAll tabs loaded and ran in the browser with no errors.");
})().catch((e) => { console.error(e); process.exit(1); });
