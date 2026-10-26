// Match import: load a real match from the Deadlock API, put a player's build against an opponent's build, and test
// what would have dealt more damage. Uses app.js helpers (S, simCall, tile, damageHero, nearestBudget ...).
"use strict";

const API = "https://api.deadlock-api.com";
const M = { match: null, a: null, d: null, t: null, run: 0, aim: true };
const TEAM = ["Amber", "Sapphire"];

// ---------- fetch + normalize ----------
// The bulk endpoint reads the API's own store (fast, no Steam); the single-match one can fall back to Steam for
// matches the store doesn't have yet. Both shapes become {id, duration, players:[{slot, hero, team, ...}]}.
async function fetchMatch(id) {
  const bulk = `${API}/v1/matches/metadata?match_ids=${id}&include_info=true&include_player_info=true`
    + "&include_player_items=true&include_player_stats=true&include_player_final_stats=true";
  try {
    const r = await fetch(bulk);
    if (r.ok) { const d = await r.json(); if (Array.isArray(d) && d.length) return normBulk(d[0]); }
  } catch (e) { /* fall through to the single-match endpoint */ }
  const r = await fetch(`${API}/v1/matches/${id}/metadata`);
  if (r.status === 404) throw new Error("No match with that ID was found.");
  if (!r.ok) {
    const wait = Number(r.headers.get("retry-after"));
    throw new Error(r.status === 503 || r.status === 429
      ? `The Deadlock API doesn't have this match stored and Steam is busy${wait ? `; try again in about ${Math.ceil(wait / 60)} min` : ""}.`
      : `The Deadlock API answered ${r.status}.`);
  }
  return normSingle(await r.json());
}

const teamNo = (t) => (String(t).endsWith("1") ? 1 : 0);
// Hero accuracy (shots aimed at enemy heroes) is what the sim takes. Statlocker's headline accuracy is shots_hit over all
// shots fired, troopers, neutrals and objectives included, so it usually runs much higher; we show it next to ours.
const aimFrom = (c, f) => {
  const shots = c["Enemy Hero Accuracy##Shots"], hits = c["Enemy Hero Accuracy##Hits"], hs = c["Enemy Hero Accuracy##Headshots"];
  const all = (f?.shots_hit || 0) + (f?.shots_missed || 0);
  return shots >= 100 && hits > 0 ? { accuracy: hits / shots, headshot: (hs || 0) / hits, shots, all: all ? f.shots_hit / all : null } : null;
};
const aimText = (a) => `${pct(a.accuracy, 1)}, ${pct(a.headshot, 1)} heads`;
const allAimRow = (a) => (a?.all != null
  ? `<span title="Shots hit over all shots fired, troopers, neutrals and objectives included. The sim uses hero accuracy.">All targets (Statlocker's accuracy)</span><span>${pct(a.all, 1)}</span>` : "");
const normPlayer = (p, custom, final) => ({
  slot: p.player_slot, account: p.account_id, hero: p.hero_id, team: teamNo(p.team), lane: p.assigned_lane,
  kda: [p.kills, p.deaths, p.assists], net_worth: p.net_worth,
  items: (p.items || []).map((x) => ({ id: x.item_id, t: x.game_time_s, sold: x.sold_time_s || 0 })),
  nw: (p.stats || []).map((s) => [s.time_stamp_s, s.net_worth]),
  aim: aimFrom(custom || {}, final),
});

function normBulk(m) {
  return { id: m.match_id, duration: m.duration_s,
    players: m.players.map((p) => normPlayer(p, p.final_stats?.custom_user_stats, p.final_stats)) };
}

function normSingle(d) {
  const mi = d.match_info || d;
  const names = Object.fromEntries((mi.custom_user_stats || []).map((c) => [c.id, c.name]));
  return { id: mi.match_id, duration: mi.duration_s,
    players: mi.players.map((p) => {
      const last = p.stats?.[p.stats.length - 1];
      const custom = Object.fromEntries((last?.custom_user_stats || []).map((c) => [names[c.id] || c.id, c.value]));
      return normPlayer(p, custom, last);
    }) };
}

// ---------- build at a moment ----------
function itemsAt(p, t) {
  const out = [];
  for (const x of p.items) if (S.items[x.id] && x.t <= t && (!x.sold || x.sold > t) && !out.includes(x.id)) out.push(x.id);
  return out;
}
function netWorthAt(p, t) {
  if (t >= M.match.duration || !p.nw.length) return p.net_worth;
  const pts = [[0, 0], ...p.nw, [M.match.duration, p.net_worth]];
  for (let i = 1; i < pts.length; i++) {
    const [t1, v1] = pts[i];
    if (t1 >= t) { const [t0, v0] = pts[i - 1]; return Math.round(v0 + ((v1 - v0) * (t - t0)) / Math.max(1, t1 - t0)); }
  }
  return p.net_worth;
}
const clock = (s) => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, "0")}`;
// heroes the sim doesn't have yet (a new hero in real matches) still get their name, from data/hero_names.json
const heroName = (id) => S.heroById[id]?.name || M.names?.[id] || `Hero ${id}`;
const pl = (slot) => M.match.players.find((p) => p.slot === slot);
const label = (p) => `${heroName(p.hero)} · ${TEAM[p.team]} · ${p.kda.join("/")} · ${fmt(p.net_worth / 1000, 1)}k`;

// the enemy who shared the lane, else the richest enemy
function defaultTarget(a) {
  const foes = M.match.players.filter((p) => p.team !== a.team && S.heroById[p.hero]);
  return (foes.find((p) => p.lane === a.lane) || foes.sort((x, y) => y.net_worth - x.net_worth)[0])?.slot ?? null;
}

// ---------- UI ----------
function renderPick() {
  const box = $("#m-pick");
  if (!M.match) { box.hidden = true; return; }
  box.hidden = false;
  const opts = (sel) => [0, 1].map((tm) => `<optgroup label="Team ${TEAM[tm]}">${M.match.players.filter((p) => p.team === tm).map((p) =>
    `<option value="${p.slot}"${p.slot === sel ? " selected" : ""}${S.heroById[p.hero] ? "" : " disabled"}>${esc(label(p))}${S.heroById[p.hero] ? "" : " (not in the sim yet)"}</option>`).join("")}</optgroup>`).join("");
  $("#m-a").innerHTML = opts(M.a);
  $("#m-d").innerHTML = opts(M.d);
  const marks = [...new Set([...pl(M.a).nw.map((x) => x[0]), M.match.duration])].filter((t) => t >= 300 && t <= M.match.duration);
  $("#m-t").innerHTML = marks.map((t) => `<option value="${t}"${t === M.t ? " selected" : ""}>${t === M.match.duration ? `End of match (${clock(t)})` : clock(t)}</option>`).join("");
  const a = pl(M.a), d = pl(M.d);
  const side = (p, who) => {
    const items = itemsAt(p, M.t), cost = items.reduce((s, i) => s + S.items[i].cost, 0);
    return `<div class="card"><h3>${who}: ${esc(heroName(p.hero))}</h3>${items.length ? tiles(items, { static: true }) : '<p class="hint">No items yet.</p>'}
      <div class="kv"><span>Net worth at ${clock(M.t)}</span><span>${fmt(netWorthAt(p, M.t))}</span><span>Items held</span><span>${fmt(cost)}</span>
      ${who === "Player" ? `<span>Hero accuracy this match</span><span>${p.aim ? aimText(p.aim) : "too few shots"}</span>${allAimRow(p.aim)}` : ""}</div></div>`;
  };
  $("#m-sides").innerHTML = side(a, "Player") + side(d, "Target");
  $("#m-aim").disabled = !a.aim;
  $("#m-aim").checked = !!a.aim && M.aim;
}

async function loadMatch(e) {
  e?.preventDefault();
  const id = ($("#m-id").value.match(/\d{6,}/) || [])[0];
  if (!id) { mStatus("Paste a match ID: the number from the match screen, Statlocker or the Deadlock API.", true); return; }
  mStatus("Loading the match from the Deadlock API…");
  $("#m-load").disabled = true;
  try {
    [M.match, M.names] = await Promise.all([fetchMatch(id), load("data/hero_names.json")]);
    const known = M.match.players.filter((p) => S.heroById[p.hero]);
    if (!known.length) throw new Error("None of this match's heroes are in the sim yet.");
    M.a = known[0].slot; M.d = defaultTarget(known[0]); M.t = M.match.duration;
    if (location.hash !== `#match/${id}`) history.replaceState(null, "", `#match/${id}`);
    mStatus(`Match ${id}, ${clock(M.match.duration)} long. Pick the player and the target, then test.`);
    $("#m-out").innerHTML = "";
    renderPick();
    rpLoad(id);
  } catch (err) {
    M.match = null; renderPick();
    $("#r-box").hidden = true;
    mStatus(err.message || "Couldn't load that match.", true);
  } finally { $("#m-load").disabled = false; }
}
function mStatus(t, bad) { const s = $("#m-status"); s.textContent = t; s.className = bad ? "err" : "hint"; }

// ---------- compare ----------
function baseReq() {
  const a = pl(M.a), d = pl(M.d);
  const req = { hero: a.hero, items: itemsAt(a, M.t), souls: netWorthAt(a, M.t), aim: "p50",
    dummy: { hero: d.hero, items: itemsAt(d, M.t), souls: netWorthAt(d, M.t), immortal: true } };
  if ($("#m-aim").checked && a.aim) { req.accuracy = a.aim.accuracy; req.headshot = a.aim.headshot; }
  return req;
}

async function alternatives(req) {
  const d = await damageHero(req.hero);
  if (!d) return [];
  // the richest search budget whose item spend the player's net worth covers
  const keys = Object.keys(d.budgets).sort((x, y) => x - y);
  const bk = [...keys].reverse().find((k) => (d.budgets[k].item_budget ?? Number(k)) <= req.souls) ?? keys[0], b = d.budgets[bk];
  const out = [{ label: `Popular ${fmt(bk / 1000)}k`, items: b.popular.items }];
  for (const [k, l] of Object.entries(OBJ)) for (const [i, x] of (b.objectives[k]?.builds || []).slice(0, 2).entries())
    out.push({ label: `Most dmg ${l} #${i + 1} (${fmt(bk / 1000)}k)`, items: x.items });
  const seen = new Set();
  return out.filter((x) => { const k = [...x.items].sort().join(); if (seen.has(k)) return false; seen.add(k); return true; })
    .map((x) => ({ ...x, budget: b }));
}

async function compare() {
  const run = ++M.run, req = baseReq(), out = $("#m-out");
  const mine = { label: "Their build", items: req.items, mine: true };
  const rows = [mine, ...(await alternatives(req))];
  const go = $("#m-go");
  go.disabled = true; go.textContent = "Testing…";
  const draw = (note) => { if (run === M.run) out.innerHTML = renderRows(req, rows) + (note ? `<p class="hint">${note}</p>` : ""); };
  try {
    for (const r of rows) {
      r.res = await simCall("run", { ...req, items: r.items });
      draw(S.ready ? "Testing builds…" : "The sim is still loading…");
    }
    const swaps = await trySwaps(req, mine.res, rows, run);
    if (run !== M.run) return;
    out.innerHTML = renderRows(req, rows) + renderSwaps(req, mine.res, swaps);
  } catch (e) {
    if (run === M.run) out.innerHTML += `<p class="err">The sim failed: ${esc(e.message)}</p>`;
  } finally { go.disabled = false; go.textContent = "Test what would have dealt more"; }
}

// one-for-one swaps of an owned item for an equal-or-cheaper item that the stronger builds use
async function trySwaps(req, base, rows, run) {
  const owned = new Set(req.items);
  const cand = new Set();
  for (const r of rows.slice(1)) for (const i of r.items) if (!owned.has(i) && S.items[i]) cand.add(i);
  const pairs = [];
  for (const o of req.items) for (const c of cand) if (S.items[c].cost <= S.items[o].cost) pairs.push([o, c]);
  pairs.sort((x, y) => S.items[y[1]].cost - S.items[x[1]].cost);
  const out = [];
  for (const [n, [o, c]] of pairs.slice(0, 60).entries()) {
    if (run !== M.run) return out;
    $("#m-out .swaps-note")?.remove();
    $("#m-out").insertAdjacentHTML("beforeend", `<p class="hint swaps-note">Trying single item swaps (${n + 1}/${Math.min(60, pairs.length)})…</p>`);
    const res = await simCall("run", { ...req, items: req.items.map((i) => (i === o ? c : i)) });
    out.push({ out: o, in: c, res, gain: res.damage["15s"] - base.damage["15s"] });
  }
  return out.sort((x, y) => y.gain - x.gain);
}

function renderRows(req, rows) {
  const base = rows[0].res?.damage["15s"];
  const sorted = [rows[0], ...rows.slice(1).filter((r) => r.res).sort((x, y) => y.res.damage["15s"] - x.res.damage["15s"])];
  const tr = (r) => {
    const cost = r.items.reduce((s, i) => s + (S.items[i]?.cost || 0), 0), d = r.res?.damage;
    const rel = d && base && !r.mine ? d["15s"] / base - 1 : null;
    return `<tr class="${r.mine ? "pop" : ""}"><td>${esc(r.label)}${r.mine ? '<span class="tag">real</span>' : ""}</td>`
      + `<td>${bdTiles({ kind: "test", hero: req.hero, souls: req.souls, items: r.items, req: { ...req, items: r.items } })}</td><td class="n">${fmt(cost)}</td>`
      + ["5s", "15s", "30s"].map((k) => `<td class="n">${d ? fmt(d[k]) : "…"}</td>`).join("")
      + `<td class="n ${rel > 0 ? "up" : rel < 0 ? "down" : ""}">${rel == null ? "–" : signed(rel)}</td>`
      + `<td><button class="chip-btn" data-mload='${JSON.stringify(r.items)}'>Open in test</button></td></tr>`;
  };
  const a = pl(M.a), d = pl(M.d);
  return `<p class="hint">${esc(heroName(a.hero))} at ${fmt(req.souls)} souls shooting ${esc(heroName(d.hero))} (${fmt(req.dummy.souls)} souls, the items it held at ${clock(M.t)}),
    ${req.accuracy != null ? `with this match's aim (${pct(req.accuracy, 1)} hero accuracy)` : "with median ranked aim"}. The target refills HP so damage keeps counting. Other builds come from the damage search at the nearest net worth they can afford.</p>
    <div class="scroll"><table><thead><tr><th>Build</th><th>Items</th><th class="n">Item souls</th><th class="n">5 s</th><th class="n">15 s</th><th class="n">30 s</th><th class="n">15 s vs theirs</th><th></th></tr></thead>
    <tbody>${sorted.map(tr).join("")}</tbody></table></div>`;
}

function renderSwaps(req, base, swaps) {
  const good = swaps.filter((s) => s.gain > 0.005 * base.damage["15s"]).slice(0, 6);
  return `<div class="card" style="margin-top:16px"><h3>Best single swaps</h3>
    <p class="hint">Their build with one item traded for an equal or cheaper item from the stronger builds above, against the same target.</p>
    ${good.length ? `<div class="kv">${good.map((s) => `<span>${tile(s.out, { static: true })} → ${tile(s.in, { static: true })}</span><span class="up">+${fmt(s.gain)} (${signed(s.gain / base.damage["15s"])})</span>`).join("")}</div>`
      : "<p>No single swap adds damage against this target. Their build was already close to the best the sim found.</p>"}</div>`;
}

function openInTest(items) {
  const r = baseReq();
  Object.assign(S.A, { hero: r.hero, souls: r.souls, items: [...items], label: `Match ${M.match.id}`, aim: r.accuracy != null ? "custom" : "p50" });
  if (r.accuracy != null) { $("#a-acc").value = (r.accuracy * 100).toFixed(1); $("#a-hs").value = (r.headshot * 100).toFixed(1); }
  Object.assign(S.D, { mode: "hero", hero: r.dummy.hero, items: [...r.dummy.items] });
  $("#d-souls").value = r.dummy.souls;
  location.hash = "test";
  renderAttacker(); renderTarget(); renderPresets(); syncDummyHint(); runTest();
}

// ---------- boot ----------
function matchFromHash() {
  const id = (location.hash.match(/^#match\/(\d+)/) || [])[1];
  if (id && String(M.match?.id) !== id) { $("#m-id").value = id; loadMatch(); }
}

(async function bootMatch() {
  await S.dataReady;
  $("#m-form").addEventListener("submit", loadMatch);
  $("#m-a").onchange = (e) => { M.a = Number(e.target.value); if (M.d != null && pl(M.d).team === pl(M.a).team) M.d = defaultTarget(pl(M.a)); renderPick(); if (R.fights.length) rpList(); };
  $("#m-d").onchange = (e) => { M.d = Number(e.target.value); renderPick(); };
  $("#m-t").onchange = (e) => { M.t = Number(e.target.value); renderPick(); };
  $("#m-aim").onchange = (e) => { M.aim = e.target.checked; };
  $("#m-go").onclick = () => { if (M.match && M.a != null && M.d != null) compare(); };
  $("#m-out").addEventListener("click", (e) => { const b = e.target.closest("[data-mload]"); if (b) openInTest(JSON.parse(b.dataset.mload)); });
  window.addEventListener("hashchange", matchFromHash);
  matchFromHash();
})();
