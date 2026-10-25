// Fight replay (Real match tab): finds the fights of a loaded match in its 1 s position and health paths, then
// replays a picked fight in the team sim (bridge.replay) with every hero's real items, souls, ability upgrades, aim,
// health at the start and the distance they fought at. Any hero's items can be changed to see what else would have
// happened. Uses app.js helpers and match.js state (M, pl, itemsAt, netWorthAt, heroName, clock, TEAM, API).
"use strict";

const R = { id: null, paths: null, deaths: [], n: 0, fights: [], f: null, edit: {}, base: null, mine: null, swaps: null, run: 0, only: true, kills: false, focus: null };
const RP = { NEAR: 50, GAP: 4, SPLIT: 40, MIN_LEN: 3, MIN_DROP: 0.2, MAX_TIME: 45, UPM: 39.37 };

// ---------- fetch ----------
// the single-match endpoint is the one with match_paths and death_details; it is not in the bulk shape match.js reads
async function rpFetch(id) {
  const r = await fetch(`${API}/v1/matches/${id}/metadata`);
  if (!r.ok) throw new Error(r.status === 503 || r.status === 429
    ? "The Deadlock API is busy fetching this match's replay data from Steam; try again in a few minutes."
    : `The Deadlock API answered ${r.status} for the match's position data.`);
  const mi = (await r.json()).match_info || {};
  const mp = mi.match_paths;
  if (!mp || !mp.paths?.length) throw new Error("This match has no position data in the Deadlock API.");
  return rpNorm(mi);
}

const rpArr = (v) => (typeof v === "string" ? JSON.parse(v) : v || []);

// game units -> meters, per player {x, y, hp (0-100), c (combat flags)} by player slot; deaths from death_details
function rpNorm(mi) {
  const mp = mi.match_paths, paths = {};
  for (const pp of mp.paths) {
    const xs = rpArr(pp.x_pos), ys = rpArr(pp.y_pos);
    const x0 = Number(pp.x_min), y0 = Number(pp.y_min);
    const sx = (Number(pp.x_max) - x0) / (mp.x_resolution || 16383), sy = (Number(pp.y_max) - y0) / (mp.y_resolution || 16383);
    paths[Number(pp.player_slot)] = { x: xs.map((v) => (x0 + v * sx) / RP.UPM), y: ys.map((v) => (y0 + v * sy) / RP.UPM),
      hp: rpArr(pp.health), c: rpArr(pp.combat_type) };
  }
  const deaths = [];
  for (const p of mi.players || []) for (const d of p.death_details || [])
    deaths.push({ t: d.game_time_s, slot: p.player_slot, killer: d.killer_player_slot, ttk: d.time_to_kill_s });
  return { paths, deaths: deaths.sort((a, b) => a.t - b.t) };
}

// ---------- fight detection ----------
// A fight second links two enemy heroes when both are alive within NEAR m, one of them is flagged in hero combat
// and one of them lost health that second; linked heroes form a group. Each kill also adds its victim and killer for
// every second of the time to kill, so fights where the killer stood further off or was never flagged still show.
// Groups chain into one fight when they share a hero and are at most GAP s apart. A fight longer than SPLIT s (a long
// push) is cut at every lull of 2+ s. Kept: MIN_LEN+ s with a death or a hero losing MIN_DROP of their health.
function rpDetect(paths, team, deaths) {
  const slots = Object.keys(paths).map(Number).filter((s) => team[s] != null);
  const n = Math.min(...slots.map((s) => paths[s].hp.length));
  const alive = (s, t) => paths[s].hp[t] > 0;
  const lost = (s, t) => t > 0 && paths[s].hp[t] < paths[s].hp[t - 1];
  const flagged = (s, t) => paths[s].c[t] & 1;
  const dist = (a, b, t) => Math.hypot(paths[a].x[t] - paths[b].x[t], paths[a].y[t] - paths[b].y[t]);
  const act = [];   // {t, g: Set of slots}
  for (let t = 1; t < n; t++) {
    const par = {};
    const find = (x) => { while ((par[x] ??= x) !== x) x = par[x]; return x; };
    const edges = [];
    for (const a of slots) for (const b of slots) {
      if (a >= b || team[a] === team[b] || !alive(a, t) || !alive(b, t)) continue;
      if ((flagged(a, t) || flagged(b, t)) && (lost(a, t) || lost(b, t)) && dist(a, b, t) <= RP.NEAR) edges.push([a, b]);
    }
    for (const [a, b] of edges) par[find(a)] = find(b);
    const groups = {};
    for (const [a, b] of edges) { const g = (groups[find(a)] ||= new Set()); g.add(a); g.add(b); }
    for (const g of Object.values(groups)) act.push({ t, g });
  }
  for (const d of deaths) {
    if (team[d.killer] == null || team[d.slot] == null || team[d.killer] === team[d.slot]) continue;
    for (let t = Math.max(1, d.t - Math.max(2, Math.min(15, Math.round(d.ttk || 0)))); t <= d.t; t++) act.push({ t, g: new Set([d.slot, d.killer]) });
  }
  act.sort((a, b) => a.t - b.t);
  let open = [];
  const chains = [];
  for (const e of act) {
    const hit = open.filter((F) => e.t - F.t1 <= RP.GAP && [...e.g].some((s) => F.slots.has(s)));
    let F = hit[0];
    if (!F) { F = { t1: e.t, slots: new Set(), ents: [] }; open.push(F); chains.push(F); }
    for (const G of hit.slice(1)) {
      F.ents.push(...G.ents); G.slots.forEach((s) => F.slots.add(s));
      G.ents = []; open = open.filter((x) => x !== G);
    }
    F.ents.push(e); e.g.forEach((s) => F.slots.add(s)); F.t1 = e.t;
    open = open.filter((x) => e.t - x.t1 <= RP.GAP);
  }
  const fights = [];
  for (const C of chains) {
    if (!C.ents.length) continue;
    const ents = C.ents.sort((a, b) => a.t - b.t);
    let pieces = [ents];
    if (ents[ents.length - 1].t - ents[0].t + 1 > RP.SPLIT) {
      pieces = [[ents[0]]];
      for (const e of ents.slice(1)) {
        const cur = pieces[pieces.length - 1];
        if (e.t - cur[cur.length - 1].t > 2) pieces.push([e]); else cur.push(e);
      }
    }
    for (const P of pieces) {
      const first = {};
      for (const e of P) for (const s of e.g) first[s] ??= e.t;
      fights.push({ t0: P[0].t, t1: P[P.length - 1].t, first });
    }
  }
  fights.sort((a, b) => a.t0 - b.t0);
  const out = [], used = new Set();
  for (const F of fights) {
    const before = Math.max(0, F.t0 - 1), after = Math.min(n - 1, F.t1 + 1);
    // a hero still respawning when the fight starts joins at the health it has when it first shows up alive; one
    // dead the whole time (seeded by a kill just before its respawn) is no part of it
    const firstAlive = (s) => { for (let t = Math.max(before, F.first[s] - 1); t <= after; t++) if (paths[s].hp[t] > 0) return t; return null; };
    const players = Object.keys(F.first).map(Number).filter((s) => firstAlive(s) != null);
    const dd = deaths.filter((d) => !used.has(d) && d.t >= F.t0 && d.t <= F.t1 + 2 && players.includes(d.slot));
    dd.forEach((d) => used.add(d));
    const hp0 = {}, hp1 = {};
    for (const s of players) {
      hp0[s] = paths[s].hp[firstAlive(s)] / 100;
      hp1[s] = dd.some((d) => d.slot === s) ? 0 : paths[s].hp[after] / 100;
    }
    const drop = Math.max(...players.map((s) => hp0[s] - Math.min(...paths[s].hp.slice(F.t0, after + 1)) / 100));
    if (F.t1 - F.t0 + 1 < RP.MIN_LEN || (!dd.length && drop < RP.MIN_DROP)) continue;
    // distance: every second, each living hero to its nearest living enemy in the fight
    const ds = [];
    for (let t = F.t0; t <= F.t1; t++) for (const a of players) {
      if (!alive(a, t)) continue;
      const near = Math.min(...players.filter((b) => team[b] !== team[a] && alive(b, t)).map((b) => dist(a, b, t)));
      if (isFinite(near)) ds.push(near);
    }
    ds.sort((a, b) => a - b);
    out.push({ t0: F.t0, t1: F.t1, players, hp0, hp1, deaths: dd, join: Object.fromEntries(players.map((s) => [s, F.first[s] - F.t0])),
      dist: ds.length ? ds[Math.floor(ds.length / 2)] : 15 });
  }
  return out;
}

// ---------- state from the match ----------
async function rpLoad(id) {
  R.id = id; R.paths = null; R.fights = []; R.f = null; R.base = R.mine = R.swaps = null; R.edit = {};
  $("#r-box").hidden = false;
  $("#r-fight").innerHTML = ""; $("#r-out").innerHTML = "";
  rpStatus("Loading the match's positions and deaths to find its fights…");
  try {
    const d = await rpFetch(id);
    if (R.id !== id) return;
    R.paths = d.paths; R.deaths = d.deaths;
    const team = Object.fromEntries(M.match.players.map((p) => [p.slot, p.team]));
    R.fights = rpDetect(d.paths, team, d.deaths);
    rpStatus(R.fights.length ? `${R.fights.length} fights found. Pick one to replay it.` : "No fights between heroes were found in this match's position data.", !R.fights.length);
    rpList();
  } catch (e) {
    if (R.id === id) rpStatus(e.message || "Couldn't load the match's position data.", true);
  }
}
function rpStatus(t, bad) { const s = $("#r-status"); s.textContent = t; s.className = bad ? "err" : "hint"; }

const rpSide = (F, tm) => F.players.filter((s) => pl(s)?.team === tm);
const rpKnown = (s) => !!S.heroById[pl(s)?.hero];
const rpHeroes = (slots) => slots.map((s) => esc(heroName(pl(s).hero))).join(", ") || "–";

function rpList() {
  const fs = R.fights.filter((F) => (!R.only || M.a == null || F.players.includes(M.a)) && (!R.kills || F.deaths.length));
  const who = M.a != null ? esc(heroName(pl(M.a).hero)) : "";
  $("#r-only-who").textContent = who ? heroName(pl(M.a).hero) : "the player";
  $("#r-list").innerHTML = fs.length ? `<div class="scroll"><table class="r-fights"><thead><tr><th>When</th><th class="n">Length</th>
    <th>${TEAM[0]}</th><th>${TEAM[1]}</th><th>Deaths</th><th></th></tr></thead><tbody>${fs.map((F) => {
      const i = R.fights.indexOf(F), dead = F.deaths.map((d) => esc(heroName(pl(d.slot).hero))).join(", ");
      return `<tr class="${R.f === F ? "pop" : ""}"><td>${clock(F.t0)}</td><td class="n">${F.t1 - F.t0 + 1} s</td><td>${rpHeroes(rpSide(F, 0))}</td><td>${rpHeroes(rpSide(F, 1))}</td>
        <td>${dead || "none"}</td><td><button class="chip-btn" data-rf="${i}">${R.f === F ? "Picked" : "Replay"}</button></td></tr>`;
    }).join("")}</tbody></table></div>` : `<p class="hint">No fights ${R.kills ? "with a kill " : ""}with ${who || "this player"} were found. Untick the boxes to see every fight.</p>`;
}

// ---------- one fight ----------
function rpPick(i) {
  R.f = R.fights[i]; R.edit = {}; R.base = R.mine = R.swaps = null;
  const F = R.f;
  for (const s of F.players) if (rpKnown(s)) R.edit[s] = itemsAt(pl(s), F.t0);
  R.focus = F.players.includes(M.a) && rpKnown(M.a) ? M.a : F.players.find(rpKnown);
  rpList(); rpRender(); rpRun();
  $("#r-fight").scrollIntoView({ behavior: "smooth", block: "start" });
}

// the focus hero's team is side "a"
function rpTeams() {
  const tm = pl(R.focus).team, F = R.f;
  const known = F.players.filter(rpKnown);
  return [known.filter((s) => pl(s).team === tm), known.filter((s) => pl(s).team !== tm)];
}

function rpMember(s, items) {
  const p = pl(s), F = R.f;
  const m = { hero: p.hero, items, souls: netWorthAt(p, F.t0), hp: F.hp0[s],
    abilities: p.items.filter((x) => !S.items[x.id] && x.t <= F.t0).map((x) => x.id) };
  if (p.aim) { m.accuracy = p.aim.accuracy; m.headshot = p.aim.headshot; }
  return m;
}

// edit: items per slot (R.edit), or null for everyone's real items; slots missing from it keep their real items
function rpReq(edit) {
  const [a, b] = rpTeams(), F = R.f;
  const m = (s) => rpMember(s, edit?.[s] || itemsAt(pl(s), F.t0));
  return { a: a.map(m), b: b.map(m), distance: Math.max(3, F.dist), max_time: Math.min(RP.MAX_TIME, Math.max(4, F.t1 - F.t0 + 1)), focus: "focus" };
}
const rpChanged = () => R.f && R.f.players.some((s) => R.edit[s] && R.edit[s].join() !== itemsAt(pl(s), R.f.t0).join());

// the fight's paths: one line per hero over the fight, a dot where it started, a cross where it died
function rpMap(F) {
  const pts = [];
  for (const s of F.players) for (let t = F.t0; t <= F.t1; t++) pts.push([R.paths[s].x[t], R.paths[s].y[t]]);
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  const pad = 6, x0 = Math.min(...xs) - pad, y0 = Math.min(...ys) - pad;
  const span = Math.max(30, Math.max(...xs) - x0 + pad, Math.max(...ys) - y0 + pad);
  const X = (x) => ((x - x0) / span) * 300, Y = (y) => 300 - ((y - y0) / span) * 300;
  const tm = pl(R.focus).team;
  const lines = F.players.map((s) => {
    const p = R.paths[s], cls = pl(s).team === tm ? "r-a" : "r-b";
    const d = [];
    for (let t = F.t0; t <= F.t1; t++) if (p.hp[t] > 0) d.push(`${X(p.x[t]).toFixed(1)},${Y(p.y[t]).toFixed(1)}`);
    if (!d.length) return "";
    const [sx, sy] = d[0].split(","), [ex, ey] = d[d.length - 1].split(",");
    const died = F.deaths.some((x) => x.slot === s);
    return `<g class="${cls}${s === R.focus ? " me" : ""}"><polyline points="${d.join(" ")}"/><circle cx="${sx}" cy="${sy}" r="4"/>`
      + (died ? `<path d="M${ex - 4},${ey - 4}l8,8m0,-8l-8,8"/>` : "")
      + `<text x="${Number(sx) + 6}" y="${Number(sy) - 6}">${esc(heroName(pl(s).hero))}</text></g>`;
  }).join("");
  return `<svg class="r-map" viewBox="-10 -10 320 320" role="img" aria-label="Where each hero moved during the fight">${lines}
    <line class="r-scale" x1="0" y1="312" x2="${(10 / span) * 300}" y2="312"/><text class="r-scale" x="${(10 / span) * 300 + 4}" y="316">10 m</text></svg>`;
}

function rpCard(s) {
  const p = pl(s), F = R.f, items = R.edit[s] || [];
  const real = itemsAt(p, F.t0), changed = items.join() !== real.join();
  const late = F.join[s] >= 3 ? `<span>Joined</span><span>${F.join[s]} s in</span>` : "";
  const tiles = items.map((id) => {
    const it = S.items[id];
    return it ? `<button class="it x${real.includes(id) ? "" : " new"}" data-slot="${it.slot}" data-rdrop="${id}" data-s="${s}" title="Remove ${esc(it.name)}">${esc(it.name)}</button>` : "";
  }).join("");
  return `<div class="card r-card${s === R.focus ? " me" : ""}">
    <div class="row"><h3>${esc(heroName(p.hero))}</h3>${s === R.focus ? '<span class="tag">focus</span>' : `<button class="ghost" data-rfocus="${s}">Focus</button>`}
      ${changed ? `<button class="ghost" data-rreset="${s}">Real items</button>` : ""}</div>
    <div class="build">${tiles || '<span class="hint">No items.</span>'}</div>
    <input type="search" list="r-items" placeholder="Add an item" data-radd="${s}" aria-label="Add an item to ${esc(heroName(p.hero))}">
    <div class="kv"><span>Net worth</span><span>${fmt(netWorthAt(p, F.t0))}</span><span>Items held</span><span>${fmt(items.reduce((t, i) => t + (S.items[i]?.cost || 0), 0))}</span>
      <span>Health at the start</span><span>${pct(F.hp0[s])}</span><span>Hero accuracy this match</span><span>${p.aim ? pct(p.aim.accuracy, 1) : "median"}</span>${late}</div></div>`;
}

function rpRender() {
  const F = R.f;
  if (!F) { $("#r-fight").innerHTML = ""; return; }
  const [a, b] = rpTeams(), skipped = F.players.filter((s) => !rpKnown(s));
  const late = F.players.filter((s) => F.join[s] >= 3);
  $("#r-fight").innerHTML = `<h2>Fight at ${clock(F.t0)}, ${F.t1 - F.t0 + 1} s</h2>
    <div class="r-top">${rpMap(F)}<div class="stack"><p class="hint">Everyone starts at the health they had when the fight began, with the items, souls and ability
      upgrades they had then, their own hero accuracy from this match, ${fmt(F.dist)} m apart (the median distance to the nearest enemy during the fight).
      The sim runs ${F.t1 - F.t0 + 1 > RP.MAX_TIME ? `the first ${RP.MAX_TIME} s` : `the same ${fmt(rpReq(null).max_time)} s`} and each team focuses the enemy with the least health.${late.length ? ` Not modeled: ${rpHeroes(late)} joined late in the real fight, the sim has everyone there from the start.` : ""}${skipped.length ? ` Left out (not in the sim yet): ${rpHeroes(skipped)}.` : ""}</p>
      <p class="hint">Change any hero's items: tap an item to remove it, type to add one. The replay reruns after each change.</p>
      <p class="fine">How close it gets (checked 2026-10-25, sim/validation/README.md "Fight replay"): over 1,894 fights from 30 Phantom+ matches the sim had 1.8 times as many deaths as really happened (nobody backs off when low), and in fights where only one side lost heroes it had more deaths on that same side 329 times and on the other side 180 times. So read the changed items against the sim with the real items, not against the real fight.</p>
      <div class="row"><button class="run" id="r-swaps" type="button">Find the best single swap for ${esc(heroName(pl(R.focus).hero))}</button></div></div></div>
    <h3>Team ${TEAM[pl(R.focus).team]}</h3><div class="cards">${a.map(rpCard).join("")}</div>
    <h3>Team ${TEAM[1 - pl(R.focus).team]}</h3><div class="cards">${b.map(rpCard).join("")}</div>`;
  $("#r-items").innerHTML = Object.values(S.items).sort((x, y) => x.name.localeCompare(y.name)).map((it) => `<option value="${esc(it.name)}">`).join("");
}

// ---------- run ----------
async function rpRun() {
  const run = ++R.run, F = R.f;
  if (!F) return;
  $("#r-out").innerHTML = `<p class="hint">${S.ready ? "Replaying the fight…" : "The sim is still loading…"}</p>`;
  try {
    if (!R.base || R.base.f !== F || R.base.focus !== R.focus) R.base = { f: F, focus: R.focus, res: await simCall("replay", rpReq(null)) };
    R.mine = rpChanged() ? await simCall("replay", rpReq(R.edit)) : null;
    if (run === R.run) rpResult();
  } catch (e) {
    if (run === R.run) $("#r-out").innerHTML = `<p class="err">The sim failed: ${esc(e.message)}</p>`;
  }
}

// health lost by a side over the fight, from start health (a dead hero loses all it had)
const rpLost = (res, side) => res.fighters.filter((x) => x.team === side).reduce((t, x) => t + x.start_hp - (x.alive ? x.hp : 0), 0);
const rpSwing = (res) => rpLost(res, "B") - rpLost(res, "A");
const rpDead = (res, side) => res.fighters.filter((x) => x.team === side && !x.alive).length;

function rpResult() {
  const F = R.f, base = R.base.res, mine = R.mine, [a, b] = rpTeams(), slots = [...a, ...b];
  const realDead = (side) => F.deaths.filter((d) => (side === "A" ? a : b).includes(d.slot)).length;
  // real health lost in HP, using the sim's max HP for each hero (the paths only have health as a share)
  const realLost = (side) => (side === "A" ? a : b).reduce((t, s, k) => t + (F.hp0[s] - F.hp1[s]) * base.fighters[side === "A" ? k : a.length + k].max_hp, 0);
  const end = (x) => (x.alive ? `${pct(x.hp / x.max_hp)}` : `died ${fmt(x.death_time, 1)} s`);
  const row = (s, k) => {
    const x = base.fighters[k], y = mine?.fighters[k], dd = F.deaths.find((d) => d.slot === s);
    const dmg = y ? y.damage - x.damage : null;
    return `<tr class="${s === R.focus ? "pop" : ""}"><td>${esc(TEAM[pl(s).team])}</td><td>${esc(heroName(pl(s).hero))}</td>
      <td class="n">${pct(F.hp0[s])} → ${dd ? `died ${dd.t - F.t0} s` : pct(F.hp1[s])}</td>
      <td class="n">${end(x)}</td><td class="n">${fmt(x.damage)}</td>
      ${mine ? `<td class="n">${end(y)}</td><td class="n">${fmt(y.damage)}</td><td class="n ${dmg > 0 ? "up" : dmg < 0 ? "down" : ""}">${dmg > 0 ? "+" : ""}${fmt(dmg)}</td>` : ""}</tr>`;
  };
  const line = (label, deadA, deadB, swing) => `<span>${label}</span><span>${deadB} / ${deadA}</span><span>${swing > 0 ? "+" : ""}${fmt(swing)}</span>`;
  const realSwing = realLost("B") - realLost("A");
  let head = "";
  if (mine) {
    const ds = rpSwing(mine) - rpSwing(base), dk = rpDead(mine, "B") - rpDead(base, "B"), dl = rpDead(mine, "A") - rpDead(base, "A");
    const parts = [];
    if (dk) parts.push(`${dk > 0 ? `${dk} more` : `${-dk} fewer`} enem${Math.abs(dk) === 1 ? "y" : "ies"} killed`);
    if (dl) parts.push(`${dl > 0 ? `${dl} more` : `${-dl} fewer`} of team ${TEAM[pl(R.focus).team]} dead`);
    head = `<p class="r-head ${ds > 0 ? "up" : ds < 0 ? "down" : ""}">With the changed items team ${TEAM[pl(R.focus).team]} comes out ${fmt(Math.abs(ds))} HP ${ds >= 0 ? "ahead" : "behind"} of the replay with the real items${parts.length ? `: ${parts.join(", ")}` : ""}.</p>`;
  }
  $("#r-out").innerHTML = `${head}<div class="kv kv3 r-sum"><span></span><span>Kills / deaths</span><span>HP swing</span>
      ${line("Real fight", realDead("A"), realDead("B"), realSwing)}${line("Sim, real items", rpDead(base, "A"), rpDead(base, "B"), rpSwing(base))}
      ${mine ? line("Sim, changed items", rpDead(mine, "A"), rpDead(mine, "B"), rpSwing(mine)) : ""}</div>
    <p class="fine">Kills and deaths are for team ${TEAM[pl(R.focus).team]}; HP swing is the health the enemies lost minus the health team ${TEAM[pl(R.focus).team]} lost (heals count).</p>
    <div class="scroll"><table class="r-table"><thead><tr><th>Team</th><th>Hero</th><th class="n">Real health</th><th class="n">Sim end</th><th class="n">Sim damage</th>
      ${mine ? '<th class="n">Changed: end</th><th class="n">Changed: damage</th><th class="n">Damage change</th>' : ""}</tr></thead>
      <tbody>${slots.map(row).join("")}</tbody></table></div>${R.swaps ? rpSwapsHTML() : ""}`;
}

// ---------- best single swap ----------
// the focus hero's real items, one at a time traded for an equal or cheaper item from the damage search's builds at
// its net worth (like the match comparison above), scored by the HP swing of the whole fight
async function rpFindSwaps() {
  const F = R.f, s = R.focus, run = ++R.run, p = pl(s);
  const btn = $("#r-swaps");
  btn.disabled = true;
  try {
    if (!R.base || R.base.f !== F || R.base.focus !== s) R.base = { f: F, focus: s, res: await simCall("replay", rpReq(null)) };
    const real = itemsAt(p, F.t0), cand = new Set();
    for (const r of await alternatives({ hero: p.hero, souls: netWorthAt(p, F.t0) })) for (const i of r.items) if (!real.includes(i) && S.items[i]) cand.add(i);
    // each real item's candidates priciest first, taken in turns across the real items so every item gets tried
    const per = real.map((o) => [...cand].filter((c) => S.items[c].cost <= S.items[o].cost).sort((x, y) => S.items[y].cost - S.items[x].cost).map((c) => [o, c]));
    const todo = [];
    for (let k = 0; todo.length < 40 && per.some((l) => l.length > k); k++) for (const l of per) if (l[k] && todo.length < 40) todo.push(l[k]);
    const total = per.reduce((t, l) => t + l.length, 0), out = [], base = rpSwing(R.base.res);
    for (const [k, [o, c]] of todo.entries()) {
      if (run !== R.run) return;
      btn.textContent = `Trying swaps (${k + 1}/${todo.length})…`;
      // only the focus hero changes: everyone else keeps their real items
      const res = await simCall("replay", rpReq({ [s]: real.map((i) => (i === o ? c : i)) }));
      out.push({ out: o, in: c, gain: rpSwing(res) - base, kills: rpDead(res, "B") - rpDead(R.base.res, "B"), deaths: rpDead(res, "A") - rpDead(R.base.res, "A") });
    }
    if (run !== R.run) return;   // an edit or a new fight came in during the last run
    R.swaps = { slot: s, rows: out.sort((x, y) => y.gain - x.gain), tried: todo.length, total };
    rpResult();
  } catch (e) {
    if (run === R.run) $("#r-out").insertAdjacentHTML("beforeend", `<p class="err">The sim failed: ${esc(e.message)}</p>`);
  } finally {
    btn.disabled = false; btn.textContent = `Find the best single swap for ${heroName(p.hero)}`;
  }
}

function rpSwapsHTML() {
  const sw = R.swaps, good = sw.rows.filter((x) => x.gain > 1).slice(0, 6);
  const fx = (x) => [x.kills ? `${x.kills > 0 ? "+" : ""}${x.kills} kill${Math.abs(x.kills) === 1 ? "" : "s"}` : "", x.deaths ? `${x.deaths > 0 ? "+" : ""}${x.deaths} death${Math.abs(x.deaths) === 1 ? "" : "s"}` : ""].filter(Boolean).join(", ");
  return `<div class="card" style="margin-top:16px"><h3>Best single swaps for ${esc(heroName(pl(sw.slot).hero))}</h3>
    <p class="hint">${sw.tried}${sw.total > sw.tried ? ` of ${sw.total}` : ""} swaps of one real item for an equal or cheaper item from the damage search's builds at this net worth${sw.total > sw.tried ? " (each real item's priciest options first)" : ""}, everyone else on their real items, scored by the fight's HP swing against the replay with the real items.</p>
    ${good.length ? `<div class="kv kv3">${good.map((x) => `<span>${tile(x.out, { static: true })} → ${tile(x.in, { static: true })}</span><span class="up">+${fmt(x.gain)} HP${fx(x) ? ` (${fx(x)})` : ""}</span>
      <span><button class="chip-btn" data-rapply='${JSON.stringify([sw.slot, x.out, x.in])}'>Try it</button></span>`).join("")}</div>`
      : `<p>None of the swaps tried improves this fight.</p>`}</div>`;
}

// ---------- boot ----------
(async function bootReplay() {
  await S.dataReady;
  $("#r-only").onchange = (e) => { R.only = e.target.checked; rpList(); };
  $("#r-kills").onchange = (e) => { R.kills = e.target.checked; rpList(); };
  $("#r-list").addEventListener("click", (e) => { const b = e.target.closest("[data-rf]"); if (b) rpPick(Number(b.dataset.rf)); });
  const box = $("#r-fight");
  box.addEventListener("click", (e) => {
    const t = e.target.closest("[data-rdrop],[data-rfocus],[data-rreset],#r-swaps");
    if (!t) return;
    if (t.id === "r-swaps") { rpFindSwaps(); return; }
    if (t.dataset.rfocus) { R.focus = Number(t.dataset.rfocus); R.swaps = null; rpRender(); rpRun(); return; }
    const s = Number(t.dataset.s ?? t.dataset.rreset);
    if (t.dataset.rreset) R.edit[s] = itemsAt(pl(s), R.f.t0);
    else R.edit[s] = R.edit[s].filter((i) => i !== Number(t.dataset.rdrop));
    R.swaps = null;   // its gains were measured from the real items; "Try it" keeps the list to pick from
    rpRender(); rpRun();
  });
  box.addEventListener("change", (e) => {
    const inp = e.target.closest("[data-radd]");
    if (!inp) return;
    const s = Number(inp.dataset.radd), name = inp.value.trim().toLowerCase();
    const id = Object.keys(S.items).map(Number).find((i) => S.items[i].name.toLowerCase() === name);
    if (id == null || R.edit[s].includes(id)) { inp.value = ""; return; }
    if (R.edit[s].length >= 12) { inp.value = ""; inp.placeholder = "12 items is the most a hero can hold"; return; }
    R.edit[s] = [...R.edit[s], id];
    R.swaps = null;
    rpRender(); rpRun();
  });
  $("#r-out").addEventListener("click", (e) => {
    const b = e.target.closest("[data-rapply]");
    if (!b) return;
    const [s, o, c] = JSON.parse(b.dataset.rapply);
    R.edit[s] = R.edit[s].map((i) => (i === o ? c : i));
    if (!R.edit[s].includes(c)) R.edit[s].push(c);
    rpRender(); rpRun();
  });
})();
