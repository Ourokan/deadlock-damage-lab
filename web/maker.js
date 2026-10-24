// Build maker tab: build from scratch against an enemy team whose builds follow the popular builds at your souls.
// Every change runs you against each enemy in the live sim (bridge.maker: both fight back for 15 s and refill
// instead of dying); hovering an item previews it; suggestions rank next buys by damage, survival and utility.
// Uses app.js globals ($, $$, esc, fmt, pct, S, load, simCall, tile, renderShop, damageHero, nearestBudget, startWorker...).
"use strict";

const MK_T = 15;                                  // fight length, s
const MK_ENEMIES = [1, 2, 6, 31, 7];              // Infernus, Seven, Abrams, Lash, Wraith
const MK_MAX = 12;
const MK_POP_FLOOR = 0.05;                        // enemy builds: items at least this share of the hero's players hold
// ranked players' held-item cost / net worth (search/scripts/build_pool.py item_share)
const MK_SHARE = [[6500, 0.80], [10000, 0.836], [15000, 0.858], [21500, 0.879], [30000, 0.894], [42000, 0.895], [60000, 0.885]];
const MK_TAGS = {
  cc: { label: "Crowd control", pts: 5, why: "stuns, silences or roots set up kills for teammates and peel for them" },
  slow: { label: "Slow", pts: 2, why: "keeps targets in reach for the whole team" },
  mobility: { label: "Mobility", pts: 4, why: "chase, escape and rotate faster, which a standing fight can't show" },
  escape: { label: "Escape", pts: 4, why: "gets you out of a fight you'd lose" },
  team: { label: "Team support", pts: 5, why: "heals or shields teammates; the 1v1 sim only sees you" },
  aoe: { label: "Hits groups", pts: 3, why: "damages several enemies in team fights; the 1v1 sim sees one" },
  antiheal: { label: "Anti-heal", pts: 4, why: "cuts the enemy team's healing, including heals from their supports" },
  cleanse: { label: "Cleanse / status resist", pts: 4, why: "shortens or removes the enemy team's stuns, silences and slows" },
  stealth: { label: "Stealth", pts: 2, why: "picks and escapes from out of sight" },
  reach: { label: "Range", pts: 2, why: "longer cast range and bigger areas" },
  farm: { label: "Farming", pts: 2, why: "more souls over the match, not more fight power now" },
};

const MK = {
  inited: false, data: null, workers: [], gen: 0,
  hero: 13, aim: "p75", items: [], nw: null, offset: 0, enemies: [...MK_ENEMIES],
  w: { d: 1, s: 1, u: 1 }, sort: "soul", all: false,
  cache: new Map(), base: null, hover: null, sugg: [], sugTotal: 0,
};

// ---------- souls ----------
function mkShare(nw) {
  const p = MK_SHARE;
  if (nw <= p[0][0]) return p[0][1];
  for (let i = 1; i < p.length; i++) if (nw <= p[i][0]) return p[i - 1][1] + (p[i][1] - p[i - 1][1]) * (nw - p[i - 1][0]) / (p[i][0] - p[i - 1][0]);
  return p[p.length - 1][1];
}
const mkCost = (items) => items.reduce((s, i) => s + (S.items[i]?.cost || 0), 0);
// net worth whose typical item spend is this many souls
function mkNetWorth(itemSouls) {
  let nw = itemSouls / 0.85;
  for (let k = 0; k < 4; k++) nw = itemSouls / mkShare(nw);
  return Math.round(nw / 100) * 100;
}
const mkMyNW = () => (MK.nw != null ? MK.nw : mkNetWorth(mkCost(MK.items)));
const mkEnemyNW = () => Math.max(0, mkMyNW() + MK.offset);

function mkUsage(nw) {
  const u = MK.data?.usage;
  if (!u) return null;
  return u[nearestBudget(Object.keys(u), nw)];
}

// item ids an item is built from (recursive), and items that contain it
const mkComps = (id) => (MK.data?.components[id] || []).map(Number);
const mkConflict = (a, b) => mkComps(a).includes(b) || mkComps(b).includes(a);

// expensive-item caps for this net worth (search tier caps: no more 6400+ / 3200+ items than 90% of players hold)
function mkCaps(nw) {
  const cell = mkUsage(nw);
  if (!cell) return null;
  const u = MK.data.usage, keys = Object.keys(u).map(Number).sort((a, b) => a - b);
  const fit = keys.filter((b) => u[b].item_budget <= mkShare(nw) * nw);
  return u[fit.length ? fit[fit.length - 1] : keys[0]].caps;
}
const mkWithinCaps = (items, caps) => !caps || Object.entries(caps).every(([t, c]) => items.filter((i) => S.items[i]?.cost >= Number(t)).length <= c);

// what the hero's players hold at about this net worth, filled most-held first up to the item souls
function mkPopular(hero, nw) {
  const cell = mkUsage(nw), row = cell?.heroes[hero];
  if (!row) return [];
  const limit = mkShare(nw) * nw, caps = mkCaps(nw), out = [];
  let spent = 0;
  for (const [id, f] of Object.entries(row.items).sort((a, b) => b[1] - a[1])) {
    const i = Number(id), c = S.items[i]?.cost;
    if (f < MK_POP_FLOOR || out.length >= MK_MAX) break;
    if (!c || spent + c > limit || out.some((x) => mkConflict(x, i)) || !mkWithinCaps([...out, i], caps)) continue;
    out.push(i); spent += c;
  }
  return out;
}

// ---------- sim calls ----------
const mkKey = (items, enemies) => `${MK.hero}|${MK.aim}|${mkMyNW()}|${[...items].sort().join(".")}|${enemies.map((e) => e.hero + ":" + e.items.join(".") + ":" + e.souls).join(",")}`;
const mkEnemyLoadouts = () => { const nw = mkEnemyNW(); return MK.enemies.map((h) => ({ hero: h, items: mkPopular(h, nw), souls: Math.max(1, nw) })); };

function mkReq(variants, enemies) {
  return { hero: MK.hero, aim: MK.aim, souls: Math.max(1, mkMyNW()), T: MK_T, enemies, variants };
}

// main worker (app.js S.engine): the current build and hover previews, newest request wins (seq: a result for an
// older request, even one answered from the cache since, never calls back)
const MKL = { busy: false, next: null, seq: 0 };
function mkLive(items, cb) {
  const enemies = mkEnemyLoadouts(), key = mkKey(items, enemies), seq = ++MKL.seq;
  if (MK.cache.has(key)) { MKL.next = null; cb(MK.cache.get(key)); return; }
  MKL.next = { items, enemies, key, cb, seq };
  if (!MKL.busy) mkPump();
}
async function mkPump() {
  const job = MKL.next; MKL.next = null;
  if (!job) { MKL.busy = false; return; }
  MKL.busy = true;
  try {
    const r = await simCall("maker", mkReq([job.items], job.enemies));
    MK.cache.set(job.key, r.variants[0]);
    if (job.seq === MKL.seq) job.cb(r.variants[0]);
    else if (MKL.next?.key === job.key) { MKL.next.cb(r.variants[0]); MKL.next = null; }
  } catch (e) {
    mkMsg("The sim failed on this build: " + e.message);
  } finally { mkPump(); }
}

// suggestion workers: their own Pyodide instances, so suggestions don't hold up the live view
function mkStartWorkers() {
  if (MK.workers.length) return;
  // phones share the page's sim worker: a second Pyodide instance costs ~15 MB to load and enough memory for
  // mobile browsers to reload the tab
  if (matchMedia("(pointer: coarse)").matches) { MK.workers.push({ call: (req) => simCall("maker", req) }); return; }
  const n = (navigator.hardwareConcurrency || 2) >= 6 ? 2 : 1;
  const base = new URL(".", location.href).href;
  for (let k = 0; k < n; k++) {
    const w = { worker: new Worker(new URL("worker.js", location.href)), ready: null, pending: {}, id: 0 };
    w.ready = new Promise((res, rej) => {
      w.worker.onmessage = (e) => {
        const m = e.data;
        if (m.type === "ready") res();
        else if (m.id && w.pending[m.id]) { w.pending[m.id](m); delete w.pending[m.id]; }
        else if (m.type === "error") rej(new Error(m.message));
      };
    });
    w.call = (req) => w.ready.then(() => new Promise((res, rej) => {
      const id = ++w.id;
      w.pending[id] = (m) => (m.type === "error" ? rej(new Error(m.message)) : res(m.result));
      w.worker.postMessage({ type: "maker", id, req });
    }));
    w.worker.postMessage({ type: "init", base, b64: !!window.__ARTIFACT__ });
    MK.workers.push(w);
  }
}

// ---------- scoring ----------
const mkSum = (rows, k) => rows.reduce((s, r) => s + r[k], 0);
const MK_CAP = 45;   // time to kill/die beyond this counts as "not in this fight"
function mkCompare(base, v) {
  const dmg = mkSum(base, "dealt") > 0 ? mkSum(v, "dealt") / mkSum(base, "dealt") - 1 : 0;
  // survival: geometric mean change in how long each enemy needs to kill you
  const surv = Math.exp(base.reduce((s, b, k) => s + Math.log(Math.min(MK_CAP, v[k].ttd) / Math.min(MK_CAP, b.ttd)), 0) / Math.max(1, base.length)) - 1;
  return { dmg, surv };
}

// utility: points per tag x strength, scaled by the enemy team (anti-heal, cleanse) and by what the build already has
function mkContext(base) {
  const healShare = base && mkSum(base, "dealt") > 0 ? mkSum(base, "enemy_heal") / mkSum(base, "dealt") : 0.2;
  const ccNames = [];
  for (const h of MK.enemies) for (const a of MK.data?.hero_cc[h] || []) ccNames.push(`${S.heroById[h]?.name}'s ${a}`);
  const nw = mkEnemyNW();
  let ccItems = 0;
  for (const h of MK.enemies) for (const i of mkPopular(h, nw)) ccItems += (MK.data.utility[i]?.cc || 0) >= 1 ? 1 : 0;
  return { healShare, cc: ccNames.length + ccItems, ccNames, ccItems };
}
function mkUtility(id, ctx, owned) {
  const tags = MK.data?.utility[id];
  if (!tags) return { pts: 0, why: [] };
  let pts = 0;
  const why = [];
  for (const [t, s] of Object.entries(tags)) {
    const def = MK_TAGS[t];
    if (!def) continue;
    let mult = 1, note = def.why;
    if (t === "antiheal") {
      mult = Math.min(2, Math.max(0.25, ctx.healShare / 0.2));
      note = `the enemies heal back ${pct(ctx.healShare)} of what you deal to them`;
    } else if (t === "cleanse") {
      mult = Math.min(2, Math.max(0.25, ctx.cc / 5));
      note = ctx.cc ? `the enemy team has ${ctx.cc} crowd-control tools (${ctx.ccNames.slice(0, 3).join(", ")}${ctx.cc > 3 ? "…" : ""})` : "the enemy team has little crowd control";
    }
    const have = owned.reduce((n, i) => n + (MK.data.utility[i]?.[t] || 0), 0);
    if (have > 0) { mult *= t === "antiheal" ? 0.2 : Math.pow(0.6, have); note += t === "antiheal" ? "; you already have anti-heal, and it doesn't stack" : "; you already have some"; }
    const p = def.pts * s * mult;
    pts += p;
    if (p >= 0.5) why.push({ tag: def.label, pts: p, note });
  }
  return { pts, why: why.sort((a, b) => b.pts - a.pts) };
}
const mkValue = (x) => MK.w.d * 100 * x.dmg + MK.w.s * 100 * x.surv + MK.w.u * x.util;

// ---------- candidates ----------
// buying id: the build it gives (an upgrade replaces its components) and the souls it costs on top
function mkBuy(items, id) {
  const comps = mkComps(id), next = [...items.filter((i) => !comps.includes(i)), id];
  return { items: next, extra: mkCost(next) - mkCost(items), upgrades: items.filter((i) => comps.includes(i)) };
}
function mkCanBuy(id, items = MK.items) {
  const it = S.items[id];
  if (!it || it.cost <= 0 || items.includes(id)) return false;
  if (items.some((i) => mkComps(i).includes(id))) return false;          // already built into an owned item
  return mkBuy(items, id).items.length <= MK_MAX;
}
function mkCandidates() {
  const items = MK.items, nw = mkMyNW(), free = MK_MAX - items.length;
  const row = mkUsage(nw)?.heroes[MK.hero]?.items || {};
  const out = [];
  for (const [id, it] of Object.entries(S.items)) {
    const i = Number(id);
    if (!mkCanBuy(i)) continue;
    const b = mkBuy(items, i);
    if (it.tier === 5 && nw < 35000) continue;                              // legendary items come late
    if (!MK.all) {
      if (free <= 3 && !b.upgrades.length && it.cost < 1600) continue;      // slots fill up: skip the cheapest tier
      if (free <= 1 && !b.upgrades.length && it.cost < 3200) continue;
      if (!mkWithinCaps(b.items, mkCaps(mkNetWorth(mkCost(b.items))))) continue;
    }
    out.push({ id: i, ...b, prior: (row[id] || 0) + (MK.data.utility[id] ? 0.05 : 0) + (it.effect_modeled ? 0.02 : 0) });
  }
  out.sort((a, b) => b.prior - a.prior);
  return MK.all ? out : out.slice(0, 36);
}

async function mkSuggest() {
  const gen = ++MK.gen, base = MK.base;
  MK.sugg = [];
  if (!base) return;
  const cands = mkCandidates(), enemies = mkEnemyLoadouts(), ctx = mkContext(base);
  MK.sugTotal = cands.length;
  mkRenderSugg();
  if (!cands.length) return;
  mkStartWorkers();
  let next = 0;
  const run = async (w) => {
    while (next < cands.length && gen === MK.gen) {
      const chunk = cands.slice(next, next + 2); next += 2;
      try {
        const r = await w.call(mkReq(chunk.map((c) => c.items), enemies));
        if (gen !== MK.gen) return;
        chunk.forEach((c, k) => {
          MK.cache.set(mkKey(c.items, enemies), r.variants[k]);
          const cmp = mkCompare(base, r.variants[k]), u = mkUtility(c.id, ctx, MK.items);
          MK.sugg.push({ ...c, rows: r.variants[k], ...cmp, util: u.pts, why: u.why });
        });
        mkRenderSugg();
      } catch (e) { if (gen === MK.gen) mkMsg("Suggestions stopped: " + e.message); return; }
    }
  };
  await Promise.all(MK.workers.map(run));
}

// ---------- rendering ----------
function mkMsg(t) { const el = $("#mk-msg"); el.hidden = !t; el.textContent = t || ""; }
const mkSigned = (x, d = 0) => (x > 0 ? "+" : x < 0 ? "−" : "") + fmt(Math.abs(x), d);
const mkPctS = (x) => (x > 0 ? "+" : x < 0 ? "−" : "") + fmt(Math.abs(x * 100), Math.abs(x) < 0.1 ? 1 : 0) + "%";
const mkTime = (t) => (t >= MK_CAP ? `over ${MK_CAP} s` : `${fmt(t, 1)} s`);

function mkRenderBuild() {
  $("#mk-hero").value = MK.hero;
  $("#mk-aim").value = MK.aim;
  const ids = [...MK.items].sort((a, b) => S.items[a].slot.localeCompare(S.items[b].slot) || S.items[a].cost - S.items[b].cost);
  $("#mk-build").innerHTML = ids.map((i) => tile(i, { remove: true, cost: true })).join("");
  const cost = mkCost(MK.items), nw = mkMyNW();
  $("#mk-nw").placeholder = `auto: ${fmt(nw)}`;
  $("#mk-budget").textContent = `${fmt(cost)} souls in items · ${MK.items.length}/${MK_MAX} slots · net worth ${fmt(nw)}${MK.nw == null ? " (from your items)" : ""}`;
  renderShop("mk", MK.items);
  const enw = mkEnemyNW();
  $("#mk-enw").textContent = `Enemy builds: what Phantom+ players of each hero hold most at about ${fmt(enw)} net worth (${fmt(mkShare(enw) * enw)} souls in items).`;
}

function mkEnemyCard(k, rows, prev) {
  const h = MK.enemies[k], loads = mkEnemyLoadouts()[k];
  const opts = S.heroes.map((x) => `<option value="${x.id}"${x.id === h ? " selected" : ""}>${esc(x.name)}</option>`).join("");
  const r = rows?.[k], p = prev?.[k];
  let stats = '<p class="hint">Simulating…</p>';
  if (r) {
    const win = r.ttk < r.ttd;
    const d = (a, b, good) => (b == null || Math.abs(a - b) < 0.5 ? "" : ` <span class="mk-d ${(a > b) === good ? "up" : "down"}">${mkSigned(a - b)}</span>`);
    const dt = (a, b, good) => (b == null || Math.abs(Math.min(a, MK_CAP) - Math.min(b, MK_CAP)) < 0.05 ? "" : ` <span class="mk-d ${(a > b) === good ? "up" : "down"}">${mkSigned(Math.min(a, MK_CAP) - Math.min(b, MK_CAP), 1)} s</span>`);
    stats = `<div class="mk-nums">
      <div><span>You deal</span><b>${fmt(r.dealt)}</b>${d(r.dealt, p?.dealt, true)}</div>
      <div><span>You take</span><b>${fmt(r.taken)}</b>${d(r.taken, p?.taken, false)}</div>
      <div><span>You kill them in</span><b>${mkTime(r.ttk)}</b>${dt(r.ttk, p?.ttk, false)}</div>
      <div><span>They kill you in</span><b>${mkTime(r.ttd)}</b>${dt(r.ttd, p?.ttd, true)}</div>
    </div>
    <div class="mk-bar" title="Share of the damage in this fight that is yours"><i style="width:${pct(r.dealt / Math.max(1, r.dealt + r.taken))}"></i></div>
    <p class="fine">${win ? '<b class="good">You win this duel.</b>' : r.ttk >= MK_CAP && r.ttd >= MK_CAP ? "Nobody dies soon." : '<b class="bad">You lose this duel.</b>'}
      Most of their damage: ${r.top_taken.map(([s, v]) => `${esc(s)} ${fmt(v)}`).join(", ") || "–"}.</p>`;
  }
  return `<div class="mk-enemy">
    <div class="row"><label class="f"><span>Enemy ${k + 1}</span><select data-k="${k}" class="mk-ehero">${opts}</select></label>
      <button class="ghost" data-rm="${k}"${MK.enemies.length < 2 ? " disabled" : ""} aria-label="Remove enemy">Remove</button></div>
    <div class="build mini">${loads.items.length ? loads.items.map((i) => tile(i, { static: true })).join("") : '<span class="hint">No items yet at this souls</span>'}</div>
    ${stats}
  </div>`;
}

function mkRenderEnemies() {
  const rows = MK.hover ? MK.hover.rows : MK.base;
  const prev = MK.hover ? MK.base : null;
  $("#mk-enemies").innerHTML = MK.enemies.map((_, k) => mkEnemyCard(k, rows, prev)).join("")
    + (MK.enemies.length < 5 ? '<button class="ghost" id="mk-addenemy">Add an enemy</button>' : "");
  mkRenderSummary();
}

function mkRenderSummary() {
  const el = $("#mk-sum"), b = MK.base;
  if (!b) { el.innerHTML = '<p class="hint">Waiting for the sim…</p>'; return; }
  const cur = MK.hover ? MK.hover.rows : b;
  const wins = cur.filter((r) => r.ttk < r.ttd).length;
  // the preview line is always there (a placeholder when not hovering), so hovering never moves the page
  const idle = matchMedia("(hover: hover)").matches ? "Hover an item to preview it against every enemy." : "Tap an item to buy it; tap an owned item to sell it.";
  let head = `<p class="mk-prev idle">${idle}</p>`;
  if (MK.hover) {
    const c = mkCompare(b, cur), it = S.items[MK.hover.id];
    const parts = [];
    if (Math.abs(c.dmg) >= 0.0005) parts.push(`${mkPctS(c.dmg)} damage dealt`);
    if (Math.abs(c.surv) >= 0.0005) parts.push(`${mkPctS(c.surv)} time to die`);
    if (MK.hover.extra) parts.push(`${MK.hover.extra > 0 ? "costs" : "frees"} ${fmt(Math.abs(MK.hover.extra))} souls`);
    const txt = `${MK.hover.sell ? "Without" : "With"} ${it?.name || ""}: ${parts.join(", ") || "no change in these fights"}`;
    head = `<p class="mk-prev" title="${esc(txt)}">${MK.hover.sell ? "Without" : "With"} <b>${esc(it?.name || "")}</b>: ${parts.join(", ") || "no change in these fights"}</p>`;
  }
  el.innerHTML = head + `<div class="mk-tot">
    <div><span>You deal, all ${cur.length} fights</span><b>${fmt(mkSum(cur, "dealt"))}</b></div>
    <div><span>Damage you take</span><b>${fmt(mkSum(cur, "taken"))}</b></div>
    <div><span>Duels you win</span><b>${wins} of ${cur.length}</b></div></div>`;
}

function mkRenderSugg() {
  const ctxNote = $("#mk-sug-status");
  const done = MK.sugg.length;
  if (!MK.base) { $("#mk-sugg").innerHTML = ""; ctxNote.textContent = ""; return; }
  ctxNote.textContent = !MK.sugTotal ? "Nothing left to buy here." : done < MK.sugTotal ? `Checked ${done} of ${MK.sugTotal} items against your enemies…` : `Checked ${MK.sugTotal} items${MK.all ? "" : ": the ones players of this hero buy most at this point, plus utility items"}.`;
  const per = MK.sort === "soul";
  const list = MK.sugg.map((x) => ({ ...x, v: mkValue(x), vs: mkValue(x) / Math.max(0.4, x.extra / 1000) }))
    .sort((a, b) => (per ? b.vs - a.vs : b.v - a.v)).slice(0, 10);
  const top = Math.max(1, ...list.map((x) => (per ? x.vs : x.v)));
  $("#mk-sugg").innerHTML = list.map((x) => {
    const it = S.items[x.id], score = per ? x.vs : x.v;
    const parts = [];
    if (Math.abs(x.dmg) >= 0.005) parts.push(`${mkPctS(x.dmg)} damage`);
    if (Math.abs(x.surv) >= 0.005) parts.push(`${mkPctS(x.surv)} time to die`);
    const why = x.why.map((w) => `<b>${esc(w.tag)}</b>: ${esc(w.note)}`).join(" · ");
    return `<button class="mk-sug" data-id="${x.id}">
      <span class="mk-sug-h">${tile(x.id, { static: true })}<span class="c">${x.upgrades.length ? `upgrade, +${fmt(x.extra)}` : fmt(x.extra)} souls</span>
        <span class="mk-score" title="${per ? "Value per 1,000 souls" : "Value"}"><i style="width:${Math.max(0, score / top * 100)}%"></i></span></span>
      <span class="mk-sug-b">${parts.join(", ") || "No change in the 1v1 fights"}${x.util >= 0.5 ? `, utility ${fmt(x.util, 1)} pts` : ""}.${why ? ` ${why}.` : ""}</span>
    </button>`;
  }).join("") || (MK.sugTotal ? '<p class="hint">Working…</p>' : "");
}

function mkShareURL() {
  const p = new URLSearchParams();
  p.set("h", MK.hero); p.set("aim", MK.aim);
  if (MK.items.length) p.set("i", MK.items.join("."));
  p.set("e", MK.enemies.join("."));
  if (MK.offset) p.set("o", MK.offset);
  if (MK.nw != null) p.set("nw", MK.nw);
  return "#maker/" + p.toString();
}
function mkReadShare() {
  const m = /^#maker\/(.+)$/.exec(location.hash);
  if (!m) return;
  const p = new URLSearchParams(m[1]), ids = (k) => (p.get(k) || "").split(".").filter((x) => /^\d+$/.test(x)).map(Number);
  if (S.heroById[Number(p.get("h"))]) MK.hero = Number(p.get("h"));
  if (["p25", "p50", "p75", "p90"].includes(p.get("aim"))) MK.aim = p.get("aim");
  MK.items = [...new Set(ids("i").filter((i) => S.items[i]))].slice(0, MK_MAX);
  const e = ids("e").filter((h) => S.heroById[h]).slice(0, 5);
  if (e.length) MK.enemies = e;
  MK.offset = [-5000, 0, 5000].includes(Number(p.get("o"))) ? Number(p.get("o")) : 0;
  MK.nw = p.has("nw") && isFinite(parseFloat(p.get("nw"))) ? Math.max(0, parseFloat(p.get("nw"))) : null;
}

// ---------- updates ----------
function mkChanged() {
  MK.hover = null; MK.base = null; MK.gen++; MK.sugg = []; MK.sugTotal = 0;
  mkRenderBuild(); mkRenderEnemies(); mkRenderSugg(); mkMsg("");
  try { history.replaceState(null, "", mkShareURL()); } catch { /* sandboxed */ }
  mkLive(MK.items, (rows) => { MK.base = rows; mkRenderEnemies(); mkSuggest(); });
}

let mkHoverTimer = null;
function mkPreview(id) {
  clearTimeout(mkHoverTimer);
  if (id == null) { if (MK.hover) { MK.hover = null; mkRenderEnemies(); } return; }
  mkHoverTimer = setTimeout(() => {
    if (!MK.base) return;
    const owned = MK.items.includes(id);
    let items, extra;
    if (owned) { items = MK.items.filter((i) => i !== id); extra = -S.items[id].cost; }
    else if (mkCanBuy(id)) ({ items, extra } = mkBuy(MK.items, id));
    else return;
    const want = { id, sell: owned, extra };
    MK.pendingHover = want;
    mkLive(items, (rows) => { if (MK.pendingHover === want) { MK.hover = { ...want, rows }; mkRenderEnemies(); } });
  }, 90);
}

function mkToggle(id) {
  if (MK.items.includes(id)) MK.items = MK.items.filter((i) => i !== id);
  else if (mkCanBuy(id)) MK.items = mkBuy(MK.items, id).items;
  else { mkMsg(MK.items.length >= MK_MAX ? "All 12 slots are full. Sell an item first." : `${S.items[id]?.name} is already part of an item you own.`); return; }
  mkChanged();
}

async function mkLoadPopular(budget) {
  const d = await damageHero(MK.hero);
  const b = d?.budgets[budget];
  if (!b) return;
  MK.items = [...b.popular.items]; MK.nw = null;
  mkChanged();
}

async function mkInit() {
  if (MK.inited || !S.heroes.length) return;
  MK.inited = true;
  MK.data = await load("data/maker.json");
  if (!MK.data) { mkMsg("The build maker's data didn't load."); return; }
  const opts = S.heroes.map((h) => `<option value="${h.id}">${esc(h.name)}</option>`).join("");
  $("#mk-hero").innerHTML = opts;
  mkReadShare();
  $("#mk-pop").innerHTML = '<span class="hint">Start from the popular build at</span>'
    + Object.keys(MK.data.usage || {}).map((b) => `<button class="chip-btn" data-b="${b}">${fmt(b / 1000)}k</button>`).join("")
    + '<button class="chip-btn" data-b="clear">Clear</button>';
  $("#mk-off").innerHTML = [[-5000, "5k behind"], [0, "Even"], [5000, "5k ahead"]].map(([v, l]) => `<button data-v="${v}" class="${v === MK.offset ? "on" : ""}">${l}</button>`).join("");
  $("#mk-sort").innerHTML = [["soul", "Per soul"], ["total", "Biggest impact"]].map(([v, l]) => `<button data-v="${v}" class="${v === MK.sort ? "on" : ""}">${l}</button>`).join("");
  if (MK.nw != null) $("#mk-nw").value = MK.nw;

  const tab = $("#tab-maker");
  $("#mk-hero").onchange = (e) => { MK.hero = Number(e.target.value); MK.items = []; MK.nw = null; $("#mk-nw").value = ""; mkChanged(); };
  $("#mk-aim").onchange = (e) => { MK.aim = e.target.value; MK.cache.clear(); mkChanged(); };
  $("#mk-nw").onchange = (e) => { const v = parseFloat(e.target.value); MK.nw = isFinite(v) && v >= 0 ? v : null; mkChanged(); };
  $("#mk-pop").onclick = (e) => { const b = e.target.dataset?.b; if (!b) return; if (b === "clear") { MK.items = []; MK.nw = null; $("#mk-nw").value = ""; mkChanged(); } else mkLoadPopular(b); };
  $("#mk-off").onclick = (e) => { const v = e.target.dataset?.v; if (v == null) return; MK.offset = Number(v); $$("#mk-off button").forEach((x) => x.classList.toggle("on", x === e.target)); mkChanged(); };
  $("#mk-sort").onclick = (e) => { const v = e.target.dataset?.v; if (!v) return; MK.sort = v; $$("#mk-sort button").forEach((x) => x.classList.toggle("on", x === e.target)); mkRenderSugg(); };
  for (const k of ["d", "s", "u"]) $(`#mk-w${k}`).oninput = (e) => { MK.w[k] = Number(e.target.value); mkRenderSugg(); };
  $("#mk-all").onchange = (e) => { MK.all = e.target.checked; mkSuggest(); };
  $("#mk-q").addEventListener("input", () => renderShop("mk", MK.items));
  $("#mk-slot").addEventListener("click", (e) => {
    if (e.target.tagName !== "BUTTON") return;
    $$("#mk-slot button").forEach((b) => b.classList.toggle("on", b === e.target));
    renderShop("mk", MK.items);
  });
  $("#mk-copy").onclick = async () => {
    const url = new URL(location.href); url.search = ""; url.hash = mkShareURL().slice(1);
    try { await navigator.clipboard.writeText(url.href); $("#mk-copy").textContent = "Link copied"; } catch { $("#mk-copy").textContent = "Copy failed"; }
    setTimeout(() => { $("#mk-copy").textContent = "Copy link"; }, 1500);
  };
  tab.addEventListener("click", (e) => {
    const t = e.target.closest("#mk-shop .it, #mk-build .it, .mk-sug");
    if (t) { mkToggle(Number(t.dataset.id)); return; }
    const rm = e.target.closest("[data-rm]");
    if (rm) { MK.enemies.splice(Number(rm.dataset.rm), 1); mkChanged(); return; }
    if (e.target.id === "mk-addenemy") { const used = new Set(MK.enemies); MK.enemies.push(S.heroes.find((h) => !used.has(h.id) && h.id !== MK.hero).id); mkChanged(); }
  });
  tab.addEventListener("change", (e) => {
    if (e.target.classList.contains("mk-ehero")) { MK.enemies[Number(e.target.dataset.k)] = Number(e.target.value); mkChanged(); }
  });
  // hover previews (mouse and pen only: a tap buys)
  tab.addEventListener("pointerover", (e) => {
    if (e.pointerType === "touch") return;
    const t = e.target.closest("#mk-shop .it, #mk-build .it, .mk-sug");
    mkPreview(t ? Number(t.dataset.id) : null);
  });
  tab.addEventListener("pointerleave", () => mkPreview(null));
  mkChanged();
}

function mkMaybeInit() { if ((location.hash || "").slice(1).split("/")[0] === "maker") mkInit(); }
window.addEventListener("hashchange", mkMaybeInit);
(function wait() { if (S.heroes.length) mkMaybeInit(); else setTimeout(wait, 200); })();
