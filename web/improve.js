// Improvements tab: a player's 15 most recent matches against Phantom+ players on the same hero, phase by phase,
// turned into a short list of what to work on first. The numbers are read straight from the Deadlock API in the
// browser: one bulk call for the stat timelines (souls, damage, kills, deaths, last hits, items), then each match's
// own metadata for what only it has (hero-only accuracy, unspent souls, parries, damage per source).
// Benchmarks: data/improve.json (analysis/scripts/improve_benchmarks.cjs, which runs the same functions below on a
// Phantom+ sample, so the player's numbers and the benchmarks are measured the same way).
// The pure functions at the top also run in Node; the tab code uses app.js globals ($, esc, fmt, pct, S, load).
"use strict";

const Improve = (() => {
  const API = "https://api.deadlock-api.com";
  const N_MATCHES = 15;
  const PHASES = [
    { id: "lane", label: "Lane", span: "0-10 min", from: 0, to: 600 },
    { id: "mid", label: "Mid game", span: "10-20 min", from: 600, to: 1200 },
    { id: "late", label: "Late game", span: "20 min on", from: 1200, to: Infinity },
  ];
  const MIN_PHASE_S = 180;   // a phase counts in a match only when the match lasted at least this far into it

  // ---------- one player in one match ----------
  const teamOf = (t) => String(t).replace(/^Team/, "");
  const itemRows = (p) => (p.items || []).map((x) => Array.isArray(x) ? x : [x.item_id, x.game_time_s, x.sold_time_s || 0]);

  // a cumulative stat at game time t, linear between the stat snapshots (every 3 min, plus the end)
  function at(stats, key, t) {
    let t0 = 0, v0 = 0;
    for (const s of stats) {
      const t1 = s.time_stamp_s, v1 = s[key] || 0;
      if (t1 >= t) return t1 === t0 ? v1 : v0 + (v1 - v0) * (t - t0) / (t1 - t0);
      t0 = t1; v0 = v1;
    }
    return v0;
  }

  // The player's numbers in one bulk-metadata match (or a fetch_improve_sample.py row): whole match and per phase.
  function features(m, who) {   // who: account id, or the player row itself
    const p = typeof who === "object" ? who : m.players.find((x) => Number(x.account_id) === Number(who));
    if (!p || !p.stats?.length) return null;
    const dur = m.duration_s, min = dur / 60, st = p.stats;
    const team = teamOf(p.team), mates = m.players.filter((x) => teamOf(x.team) === team);
    const teamKills = mates.reduce((s, x) => s + (x.kills || 0), 0);
    const deaths = (p.death_details || []).map((d) => d.game_time_s);
    const k = p.kills || 0, d = p.deaths || 0, a = p.assists || 0;
    const f = {
      match_id: m.match_id, start_time: m.start_time, hero: Number(p.hero_id), win: teamOf(m.winning_team) === team,
      dur, kills: k, deaths: d, assists: a, net_worth: p.net_worth, lane: p.assigned_lane,
      v: {
        "all.spm": p.net_worth / min,
        "all.dpm": at(st, "player_damage", dur) / min,
        "all.kp": teamKills ? (k + a) / teamKills : null,
        "all.dka": d / Math.max(1, k + a),
        "all.d10": 10 * d / min,
      },
      items: [],
    };
    for (const ph of PHASES) {
      const end = Math.min(ph.to, dur);
      if (end - ph.from < MIN_PHASE_S) continue;
      const len = (end - ph.from) / 60, dv = (key) => (at(st, key, end) - at(st, key, ph.from)) / len;
      f.v[`${ph.id}.spm`] = dv("net_worth");
      f.v[`${ph.id}.dpm`] = dv("player_damage");
      f.v[`${ph.id}.d10`] = 10 * deaths.filter((t) => t >= ph.from && t < end).length / len;
      if (ph.id === "lane") { f.v["lane.lh"] = dv("creep_kills"); f.v["lane.dn"] = dv("denies"); }
      else f.v[`${ph.id}.jg`] = dv("gold_neutral_creep");
    }
    // first purchase of each item, with the net worth then (sold and re-bought items count once)
    const seen = new Set();
    for (const [id, t] of itemRows(p).sort((x, y) => x[1] - y[1])) {
      if (seen.has(id) || t <= 0) continue;
      seen.add(id);
      f.items.push([id, t, Math.round(at(st, "net_worth", t))]);
    }
    f.build = { items: itemRows(p).map(([id, t, sold]) => [id, t, sold || 0]), nw: st.map((x) => [x.time_stamp_s, x.net_worth]) };   // for Aim.heldAt
    return f;
  }

  // What only a match's own metadata has: the final custom stats (accuracy, unspent souls, parries) and the damage
  // per source dealt to enemy heroes. `custom` is name -> value, `sources` source name -> damage (as slim() in
  // sim/scripts/fetch_validation.py, so sim/validation/phantom_sample.jsonl.gz rows go through the same code).
  function extras(custom, sources, durS, netWorth) {
    const out = {}, min = durS / 60;
    const shots = custom["Enemy Hero Accuracy##Shots"], hits = custom["Enemy Hero Accuracy##Hits"] || 0;
    if (shots >= 50) { out["x.acc"] = hits / shots; if (hits >= 20) out["x.hs"] = (custom["Enemy Hero Accuracy##Headshots"] || 0) / hits; }
    // souls held on average, in minutes of the player's own income (raw souls held grow with income, so richer
    // players, who win more, hold more)
    if (custom["Unspent Gold Minutes"] != null && netWorth > 0) out["x.unspent"] = custom["Unspent Gold Minutes"] / netWorth;
    const ps = custom["Parry Success"] || 0, pm = custom["Parry Miss"] || 0;
    if (shots != null) out["x.parry"] = 10 * ps / min;   // custom stats present (absent keys = 0)
    if (ps + pm >= 3) out["x.parryhit"] = ps / (ps + pm);
    const tot = ["Bullet", "Ability", "Melee", "Misc"].reduce((s, k) => s + (sources[k] || 0), 0);
    const src = {};
    if (tot > 0) {
      let gun = 0, item = 0;
      for (const [k, v] of Object.entries(sources)) {
        if (["Bullet", "Ability", "Melee", "Misc"].includes(k)) continue;
        if (k.startsWith("citadel_weapon_")) gun += v;
        else if (k.startsWith("upgrade_")) item += v;
        const name = k.startsWith("citadel_weapon_") ? "gun" : k;
        src[name] = (src[name] || 0) + v / tot;
      }
      const melee = (sources.Melee || 0) / tot;
      Object.assign(out, { "x.gun": gun / tot, "x.melee": melee, "x.item": item / tot, "x.ability": Math.max(0, 1 - gun / tot - melee - item / tot) });
    }
    return { v: out, src };
  }

  const nameMap = (list) => Object.fromEntries((list || []).map((c) => [c.id, c.name]));

  // /v1/matches/{id}/metadata -> the player's final custom stats and damage per source to enemy heroes
  function fromMeta(meta, accountId) {
    const mi = meta.match_info || meta;
    const p = (mi.players || []).find((x) => Number(x.account_id) === Number(accountId));
    if (!p) return null;
    const names = nameMap(mi.custom_user_stats), last = p.stats?.length ? p.stats[p.stats.length - 1] : null;
    const custom = {};
    for (const c of last?.custom_user_stats || []) custom[names[c.id] || c.id] = c.value;
    const dm = mi.damage_matrix || {}, det = dm.source_details || {}, sn = det.source_name || [], ty = det.stat_type || [];
    const team = Object.fromEntries(mi.players.map((x) => [x.player_slot, teamOf(x.team)]));
    const sources = {};
    for (const dd of dm.damage_dealers || []) {
      if (dd.dealer_player_slot !== p.player_slot) continue;
      for (const s of dd.damage_sources || []) {
        const i = s.source_details_index;
        if (i >= sn.length || ty[i] !== 0) continue;
        for (const t of s.damage_to_players || []) {
          if (t.damage?.length && t.target_player_slot in team && team[t.target_player_slot] !== teamOf(p.team)) sources[sn[i]] = (sources[sn[i]] || 0) + t.damage[t.damage.length - 1];
        }
      }
    }
    return extras(custom, sources, mi.duration_s, p.net_worth);
  }

  // ---------- spreads ----------
  const Q = Array.from({ length: 19 }, (_, i) => 5 * (i + 1)), MID = 9;   // p5, p10 ... p95; q[MID] = median
  function quantiles(xs, at = Q) {
    const s = xs.filter((x) => x != null && isFinite(x)).sort((a, b) => a - b);
    if (!s.length) return null;
    return at.map((q) => { const i = (s.length - 1) * q / 100, lo = Math.floor(i); return s[lo] + (s[Math.min(lo + 1, s.length - 1)] - s[lo]) * (i - lo); });
  }
  // where v sits in a [p5 ... p95] spread, as a percentile. Counts (deaths in a phase) repeat one value over many
  // grid points: a value equal to a run of them gets the middle of the run, so "1 death" in a spread where most
  // players die once reads as about average, not as the bottom of the run.
  function pctOf(v, q) {
    if (v == null || !q) return null;
    const n = q.length;
    if (v < q[0]) return 2.5;
    if (v > q[n - 1]) return 97.5;
    let lo = -1, hi = -1;
    for (let i = 0; i < n; i++) if (Math.abs(q[i] - v) <= 1e-9 * Math.max(1, Math.abs(v))) { if (lo < 0) lo = i; hi = i; }
    if (lo >= 0) {
      const a = lo === 0 ? 0 : Q[lo], b = hi === n - 1 ? 100 : Q[hi];   // a run at an end reaches past it
      return (a + b) / 2;
    }
    for (let i = 1; i < n; i++) if (v < q[i]) return Q[i - 1] + 5 * (v - q[i - 1]) / (q[i] - q[i - 1]);
    return 50;
  }
  const median = (xs) => { const q = quantiles(xs, [50]); return q ? q[0] : null; };
  const mean = (xs) => xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null;

  // ---------- what to say ----------
  // dir: +1 higher is better, -1 lower is better, 0 just a different style (shown, never ranked as advice)
  const M = {
    "lane.spm": { label: "Souls per minute", dir: 1, unit: "/min", tip: "Lane souls: last hit every creep you can, secure the orbs from your own last hits, and break boxes and statues between waves." },
    "lane.lh": { label: "Last hits per minute", dir: 1, unit: "/min", d: 1, tip: "Last hits: hit the trooper that is about to die, not the one at full health, and shoot the soul orb right after." },
    "lane.dn": { mean: true, label: "Denies per minute", dir: 1, unit: "/min", d: 2, tip: "Denies: shoot the enemy's soul orbs before they do; it takes souls from them as well as giving you some." },
    "lane.dpm": { label: "Hero damage per minute", dir: 1, unit: "/min", tip: "Lane pressure: trade with the enemy laner when their gun is reloading or their key ability is on cooldown." },
    "lane.d10": { mean: true, label: "Deaths per 10 min", dir: -1, unit: "", d: 1, tip: "Lane deaths: each one gives up a wave or two of souls. Back off when you're under half health and the enemy rotator has gone missing." },
    "mid.spm": { label: "Souls per minute", dir: 1, unit: "/min", tip: "Mid-game farm: between fights, take jungle camps and push the side lanes instead of walking around." },
    "mid.jg": { label: "Jungle souls per minute", dir: 1, unit: "/min", tip: "Jungle: clear the camps on your way to every fight or rotation, and come back to them as they respawn." },
    "mid.dpm": { label: "Hero damage per minute", dir: 1, unit: "/min", tip: "Mid-game fights: be there when your team fights, and keep shooting the nearest enemy rather than waiting for the perfect target." },
    "mid.d10": { mean: true, label: "Deaths per 10 min", dir: -1, unit: "", d: 1, tip: "Mid-game deaths: don't push a lane alone when the enemies aren't showing on the map, and back off before you're out of health." },
    "late.spm": { label: "Souls per minute", dir: 1, unit: "/min", tip: "Late-game farm: keep side lanes pushed and take the big camps whenever your team isn't fighting." },
    "late.jg": { label: "Jungle souls per minute", dir: 1, unit: "/min", tip: "Late jungle: big camps and the Sinners' Sacrifice pay off most between objectives." },
    "late.dpm": { label: "Hero damage per minute", dir: 1, unit: "/min", tip: "Late fights: open with your damage while the enemy is grouped, and stay in range to keep shooting." },
    "late.d10": { mean: true, label: "Deaths per 10 min", dir: -1, unit: "", d: 1, tip: "Late deaths cost the most: a long respawn and often an objective. Move with your team and don't face-check corners." },
    "all.spm": { advise: false, label: "Souls per minute", dir: 1, unit: "/min", tip: "Total souls decide how many items you have in every fight." },
    "all.dpm": { advise: false, label: "Hero damage per minute", dir: 1, unit: "/min", tip: "Damage output: spend more of each fight shooting or casting at enemy heroes." },
    "all.kp": { label: "Kill participation", dir: 1, pct: true, tip: "Kill participation: join more of your team's kills. Rotate toward fights you can reach and help finish low-health enemies." },
    "all.dka": { label: "Deaths per kill or assist", dir: -1, d: 2, tip: "Deaths per fight: you die often for how many kills you take part in. Fight next to your team and leave a fight that's lost early." },
    "all.d10": { advise: false, label: "Deaths per 10 min", dir: -1, d: 1, tip: "Deaths: every death costs souls and time off the map." },
    "x.acc": { label: "Hero accuracy", dir: 1, pct: true, tip: "Aim: shots that hit enemy heroes (troopers and creeps don't count here). Practise tracking, and fight at a range your gun hits well." },
    "x.hs": { label: "Headshot share of hits", dir: 1, pct: true, tip: "Headshots: aim at head height; a headshot does much more gun damage." },
    "x.unspent": { label: "Souls left unspent (minutes of income)", dir: -1, d: 1, unit: " min", tip: "Unspent souls do nothing: buy items sooner, since even a component in the slot is better than souls in the pocket." },
    "x.parry": { label: "Parries per 10 min", dir: 1, d: 1, tip: "Parries: parry the enemy's melee and heavy melee charges; a parry stuns them and they take extra damage." },
    "x.gun": { label: "Gun share of damage", dir: 0, pct: true },
    "x.ability": { label: "Ability share of damage", dir: 0, pct: true },
    "x.melee": { label: "Melee share of damage", dir: 0, pct: true },
    "x.item": { label: "Item share of damage", dir: 0, pct: true },
  };

  // The benchmark spread for a metric on a hero (falls back to all heroes when the hero's sample is small).
  function benchQ(bench, hero, key) {
    const h = bench.heroes[hero];
    return (h && h.n >= 40 && h.m[key]) || bench.all.m[key] || null;
  }

  // the benchmark's average for count metrics (shown next to the player's average), same fallback as benchQ
  function Improve_mean(bench, h, key) { return (h && h.n >= 40 ? h.mean?.[key] : null) ?? bench.all.mean?.[key] ?? null; }

  // rows: features() of each match (+ .x from extras()), bench: data/improve.json.
  // Each match is placed against its own hero's spread, then the player's percentile on a metric is the mean of
  // those, so a mix of heroes still compares like with like. "You" is the median match (mean for counts).
  function analyze(rows, bench) {
    const keys = Object.keys(M);
    const stats = {};
    for (const key of keys) {
      const per = [];
      for (const r of rows) {
        const v = key.startsWith("x.") ? r.x?.v[key] : r.v[key];
        const q = benchQ(bench, r.hero, key);
        if (v == null || !q) continue;
        const h = bench.heroes[r.hero], avg = Improve_mean(bench, h, key);
        per.push({ v, p: pctOf(v, q), q50: M[key].mean && avg != null ? avg : q[MID], hero: r.hero });
      }
      if (!per.length) continue;
      const p = mean(per.map((x) => x.p)), info = M[key];
      const good = info.dir ? (info.dir > 0 ? p : 100 - p) : null;   // percentile in the "better" direction
      // Phantom+ win-rate gap between the halves, in points; whole-match numbers carry the game's result in them
      // (the winning side ends up with the kills and the souls), so they count half
      const w = Math.max(0, info.dir * (bench.meta.win[key] ?? 0)) * (key.startsWith("all.") ? 0.5 : 1);
      const short = good == null ? 0 : Math.max(0, 50 - good) / 50;    // 0 at the median, 1 at the very bottom
      stats[key] = { key, n: per.length, mine: (info.mean ? mean : median)(per.map((x) => x.v)), bench: median(per.map((x) => x.q50)), p, good, w, priority: short * w * Math.min(1, per.length / 3) };
    }
    return stats;
  }

  // Items: per hero, the player's purchase timings against Phantom+ players on the hero, core items skipped,
  // and items bought often that Phantom+ players rarely buy and win less with. edge = win_edge.json heroes.
  function itemAdvice(rows, bench, edge, names) {
    const out = [];
    const byHero = {};
    for (const r of rows) (byHero[r.hero] ||= []).push(r);
    for (const [hero, rs] of Object.entries(byHero)) {
      const hb = bench.heroes[hero]?.items || {};
      const mine = {};
      for (const r of rs) for (const [id, t, nw] of r.items) if (hb[id] || names(id)) (mine[id] ||= []).push([t, nw]);
      const timing = [];
      for (const [id, xs] of Object.entries(mine)) {
        const b = hb[id];
        if (!b || !names(id)) continue;
        const t = median(xs.map((x) => x[0])), nw = median(xs.map((x) => x[1]));
        timing.push({ id: Number(id), hero: Number(hero), n: xs.length, share: xs.length / rs.length, t, nw, bshare: b[0], bt: b[1], bnw: b[4], late: t - b[1], nwLate: nw - b[4], edge: edge?.[hero]?.[id]?.[0] ?? null });
      }
      timing.sort((a, b) => b.bshare - a.bshare);
      // core Phantom+ items this player skips (3+ matches on the hero to say "skip"), unless holders win less with them
      const skipped = rs.length >= 3 ? Object.entries(hb).filter(([id, b]) => b[0] >= 0.5 && names(id) && (mine[id]?.length || 0) / rs.length <= 0.25 && !(edge?.[hero]?.[id]?.[0] < -0.5))
        .map(([id, b]) => ({ id: Number(id), hero: Number(hero), bshare: b[0], bt: b[1], share: (mine[id]?.length || 0) / rs.length, edge: edge?.[hero]?.[id]?.[0] ?? null })) : [];
      const odd = timing.filter((x) => x.share >= 0.5 && x.n >= 2 && x.bshare < 0.15 && x.edge != null && x.edge <= -1);
      out.push({ hero: Number(hero), n: rs.length, timing, skipped, odd });
    }
    return out.sort((a, b) => b.n - a.n);
  }

  // Ranked advice cards from analyze() + itemAdvice() (+ builds vs the sim, optional).
  function advice(stats, items, sim) {
    const cards = [];
    for (const s of Object.values(stats)) {
      const info = M[s.key];
      if (!info.dir || !info.tip || info.advise === false || s.priority < 0.5 || s.good >= 40) continue;
      const ph = PHASES.find((x) => s.key.startsWith(x.id + "."));
      cards.push({ kind: "metric", key: s.key, priority: s.priority, phase: ph ? `${ph.label} (${ph.span})` : "Whole match", title: info.label, s, tip: info.tip });
    }
    // a metric shows up once: the phase where it is furthest behind beats the whole-match number
    const seen = new Set();
    const metric = cards.sort((a, b) => b.priority - a.priority).filter((c) => {
      const base = c.key.split(".")[1];
      const fam = base === "d10" || base === "dka" ? "deaths" : base;
      if (seen.has(fam)) return false;
      seen.add(fam); return true;
    });
    const out = [...metric];
    // item cards: weighted like a metric 1 SD behind on a mid-weight stat (they are concrete, cheap to act on)
    for (const h of items) {
      const late = h.timing.filter((x) => x.bshare >= 0.4 && x.n >= 2 && x.nwLate >= 2500 && x.late >= 120);
      if (late.length) out.push({ kind: "late", hero: h.hero, priority: 2.5 + Math.min(2, late.length * 0.5), rows: late.slice(0, 3) });
      if (h.skipped.length) out.push({ kind: "skip", hero: h.hero, priority: 2 + Math.min(2, h.skipped.length * 0.5), rows: h.skipped.slice(0, 3) });
      if (h.odd.length) out.push({ kind: "odd", hero: h.hero, priority: 2 + Math.min(2, -Math.min(...h.odd.map((x) => x.edge)) / 2), rows: h.odd.slice(0, 3) });
    }
    if (sim && sim.overlap != null && sim.overlap < 0.4 && sim.n >= 2) out.push({ kind: "sim", priority: 1.5, sim });
    return out.sort((a, b) => b.priority - a.priority);
  }

  return { API, N_MATCHES, PHASES, M, MID, at, features, extras, fromMeta, quantiles, pctOf, median, mean, analyze, itemAdvice, advice, benchQ, teamOf };
})();

if (typeof module !== "undefined") module.exports = Improve;

// ---------- the tab ----------
const IM = { inited: false, run: 0, rows: null, who: null, busy: false };
const IM_KEY = "ddl.improve", IM_FRESH_MS = 30 * 60 * 1000;
const IM_BULK = "&game_mode=normal&include_info=true&include_player_info=true&include_player_stats=true&include_player_items=true"
  + "&include_player_death_details=true&order_by=match_id&order_direction=desc";

const imRead = () => { try { return JSON.parse(localStorage.getItem(IM_KEY) || "null"); } catch { return null; } };
const imWrite = (v) => { try { localStorage.setItem(IM_KEY, JSON.stringify(v)); } catch { /* storage full or off: just not kept */ } };
const imSleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function imGet(path) {
  for (let i = 0; ; i++) {
    try { return await Aim.get(path); } catch (e) {
      if (i >= 2 || (e.status && e.status !== 429 && e.status < 500)) throw e;   // rate limited or busy: wait and try again
      await imSleep(4000 * (i + 1));
    }
  }
}
const imHero = (id) => S.heroById[id]?.name || `Hero ${id}`;
const imItem = (id) => S.items[id]?.name;
const imClock = (s) => s == null ? "–" : `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, "0")}`;
function imVal(key, v) {
  const m = Improve.M[key];
  if (v == null) return "–";
  if (m.pct) return pct(v, v < 0.1 ? 1 : 0);
  return fmt(v, m.d || 0) + (m.unit && m.unit !== "/min" ? m.unit : "");
}

function imMaybeInit() { if ((location.hash || "").slice(1).split("/")[0] === "improve") imInit(); }
if (typeof window !== "undefined") { window.addEventListener("hashchange", imMaybeInit); imMaybeInit(); }

async function imInit() {
  await S.booted;
  if (!IM.inited) {
    IM.inited = true;
    $("#im-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = $("#im-form button"); btn.disabled = true;
      imStatus("Looking up the player…");
      try { const who = await Aim.resolve($("#im-id").value); imStart(who.id, who.name, true); } catch (err) { imStatus(err.message, true); } finally { btn.disabled = false; }
    });
    $("#im-again").onclick = () => IM.who && imStart(IM.who.id, IM.who.name, true);
    $("#im-signin").onclick = () => { const pop = $("#acct-pop"); pop.hidden = false; $("#acct-id")?.focus(); window.scrollTo({ top: 0, behavior: "smooth" }); };
    Account.onChange((me) => { if (me && (location.hash || "").startsWith("#improve")) imStart(me.id, me.name); else imShow(); });
  }
  imShow();
}

// who to read: the signed-in player unless another one was typed on this tab
function imShow() {
  const me = Account.current();
  $("#im-signin").hidden = !!me;
  $("#im-who").textContent = me ? `Signed in as ${me.name}.` : "Sign in with Steam to read your own matches, or type any player below.";
  if (IM.who && IM.rows) return;
  if (me) imStart(me.id, me.name);
}

function imStatus(t, err = false) { const el = $("#im-status"); el.textContent = t; el.classList.toggle("err", err); }

async function imStart(id, name, force = false) {
  if (IM.busy && IM.who?.id === id && !force) return;
  const run = ++IM.run;
  IM.who = { id, name }; IM.busy = true;
  $("#im-again").hidden = false;
  try {
    const c = imRead();
    if (!force && c?.id === id && Date.now() - c.at < IM_FRESH_MS && c.rows?.length) {
      IM.rows = c.rows; await imRender();
      imStatus(`${name}: last ${c.rows.length} matches, read ${Math.round((Date.now() - c.at) / 60000)} min ago.`);
      return;
    }
    imStatus(`Reading ${name}'s last ${Improve.N_MATCHES} matches…`);
    $("#im-out").innerHTML = "";
    let ms;
    try { ms = await imGet(`/v1/matches/metadata?account_ids=${id}&limit=${Improve.N_MATCHES + 5}${IM_BULK}`); } catch (e) {
      throw new Error("The Deadlock API did not answer. Try again in a minute.");
    }
    if (run !== IM.run) return;
    ms = (ms || []).filter((m) => m.match_mode === "Ranked" || m.match_mode === "Unranked" || m.match_mode == null).slice(0, Improve.N_MATCHES);
    const rows = ms.map((m) => Improve.features(m, id)).filter(Boolean);
    if (!rows.length) throw new Error("No recent matches found for this player. New matches can take a while to show up in the Deadlock API.");
    IM.rows = rows;
    await imRender();
    // what only each match's own metadata has: accuracy, unspent souls, parries, damage per source
    let next = 0, done = 0, failed = 0;
    const work = async () => {
      while (next < rows.length) {
        const r = rows[next++];
        try { r.x = Improve.fromMeta(await imGet(`/v1/matches/${r.match_id}/metadata`), id); } catch { failed++; }
        if (run !== IM.run) return;
        done++;
        imStatus(`${name}: ${rows.length} matches read. Reading aim and damage mix match by match: ${done} of ${rows.length}…`);
      }
    };
    await Promise.all([work(), work(), work()]);
    if (run !== IM.run) return;
    imWrite({ id, at: Date.now(), rows });
    await imRender();
    imStatus(`${name}: last ${rows.length} matches.` + (failed ? ` Aim and damage mix missing for ${failed} of them (the API didn't answer).` : ""));
  } catch (e) {
    if (run === IM.run) imStatus(e.message, true);
  } finally { if (run === IM.run) IM.busy = false; }
}

// the sim's best overall build (Phantom+) at each match's net worth vs what the player held then
async function imSim(rows) {
  const idx = await load("data/overall/index.json"), mk = await load("data/maker.json");
  const comps = (id) => (mk?.components[id] || []).map(Number);
  const out = [];
  for (const r of rows) {
    const keys = Object.keys(idx?.heroes[r.hero]?.brackets?.phantom || {});
    if (!keys.length) continue;
    const bk = nearestBudget(keys.filter((k) => Number(k) <= r.net_worth).length ? keys.filter((k) => Number(k) <= r.net_worth) : keys, r.net_worth);
    const d = await load(`data/overall/heroes/${r.hero}_phantom_${bk}.json`);
    const best = d?.builds?.[0]?.items;
    if (!best) continue;
    const held = Aim.heldAt(r.build, Number(bk), (id) => Object.hasOwn(S.items, id), comps).items;
    // an item counts as matched when the player held it or something built from it
    const fam = (id) => new Set([Number(id), ...comps(id)]);
    const hit = best.filter((b) => held.some((h) => fam(h).has(Number(b))));
    out.push({ r, bk: Number(bk), best, held, hit });
  }
  const n = out.length;
  return { n, rows: out, overlap: n ? out.reduce((s, x) => s + x.hit.length / x.best.length, 0) / n : null };
}

function imBar(p) {
  if (p == null) return "";
  return `<span class="im-pbar" title="Percentile among Phantom+ players on the same hero"><i style="left:${Math.max(0, Math.min(100, p))}%"></i></span>`;
}
const imTone = (good) => good == null ? "" : good < 30 ? "bad" : good >= 60 ? "good" : "";
const imImpact = (p) => p >= 6 ? "High impact" : p >= 2.5 ? "Medium impact" : "Low impact";

function imCard(c, i, edgeNote) {
  const head = (t, sub) => `<div class="im-card-h"><span class="im-n">${i + 1}</span><div><h3>${t}</h3><p class="fine">${sub}</p></div></div>`;
  if (c.kind === "metric") {
    const s = c.s;
    return `<div class="card im-card">${head(`${esc(c.title)}<span class="tag">${esc(c.phase)}</span>`, imImpact(c.priority))}
      <div class="kv"><span>You</span><span class="${imTone(s.good)}"><b>${imVal(c.key, s.mine)}</b></span>
      <span>Phantom+ median (same heroes)</span><span>${imVal(c.key, s.bench)}</span>
      <span>Your rank among Phantom+</span><span>${s.good == null ? "–" : `${fmt(s.good)}th percentile`}</span></div>
      <p>${esc(c.tip)}</p></div>`;
  }
  const rowsOf = (xs, f) => `<ul class="im-list">${xs.map(f).join("")}</ul>`;
  if (c.kind === "late") return `<div class="card im-card">${head(`Core items come late<span class="tag">${esc(imHero(c.hero))}</span>`, imImpact(c.priority))}
      ${rowsOf(c.rows, (x) => `<li><b>${esc(imItem(x.id))}</b>: you buy it at ${imClock(x.t)} with ${fmt(x.nw)} souls, Phantom+ at ${imClock(x.bt)} with ${fmt(x.bnw)}.</li>`)}
      <p>You buy these at a higher net worth than Phantom+ players do, so other items are going in first. Move them up your buy order.</p></div>`;
  if (c.kind === "skip") return `<div class="card im-card">${head(`Phantom+ core items you skip<span class="tag">${esc(imHero(c.hero))}</span>`, imImpact(c.priority))}
      ${rowsOf(c.rows, (x) => `<li><b>${esc(imItem(x.id))}</b>: ${pct(x.bshare)} of Phantom+ ${esc(imHero(c.hero))} players buy it (usually by ${imClock(x.bt)}), you in ${pct(x.share)} of your matches${edgeNote(x.edge)}.</li>`)}
      <p>Try them in your next few matches on this hero; tap Build maker to test them against your own build.</p></div>`;
  if (c.kind === "odd") return `<div class="card im-card">${head(`Items that rarely pay off<span class="tag">${esc(imHero(c.hero))}</span>`, imImpact(c.priority))}
      ${rowsOf(c.rows, (x) => `<li><b>${esc(imItem(x.id))}</b>: in ${pct(x.share)} of your matches, only ${pct(x.bshare)} of Phantom+ players buy it${edgeNote(x.edge)}.</li>`)}
      <p>Phantom+ players on this hero who buy these win less often than those who don't, at the same net worth.</p></div>`;
  if (c.kind === "sim") return `<div class="card im-card">${head("Your builds vs the sim's best builds", imImpact(c.priority))}
      <p>On average your items share ${pct(c.sim.overlap)} of the sim's best overall build at the same net worth. See the comparison below, and the Best overall builds tab for why it picks them.</p></div>`;
  return "";
}

async function imRender() {
  const rows = IM.rows;
  const [bench, we] = await Promise.all([load("data/improve.json"), load("data/win_edge.json")]);
  if (!bench) { $("#im-out").innerHTML = '<p class="empty">The Phantom+ benchmarks are missing from this build of the site.</p>'; return; }
  const stats = Improve.analyze(rows, bench);
  const items = Improve.itemAdvice(rows, bench, we?.heroes, imItem);
  const sim = await imSim(rows).catch(() => null);
  const cards = Improve.advice(stats, items, sim);
  const edgeNote = (e) => e == null ? "" : `; real win edge for holders ${e > 0 ? "+" : ""}${fmt(e, 1)} pt`;

  const wins = rows.filter((r) => r.win).length;
  const heroes = {};
  for (const r of rows) (heroes[r.hero] ||= []).push(r);
  const heroLine = Object.entries(heroes).sort((a, b) => b[1].length - a[1].length).map(([h, rs]) => `${esc(imHero(h))} ${rs.length}`).join(", ");
  const k = rows.reduce((s, r) => s + r.kills, 0), d = rows.reduce((s, r) => s + r.deaths, 0), a = rows.reduce((s, r) => s + r.assists, 0);
  const summary = `<div class="im-sum">
    <div><b>${rows.length}</b><span>matches</span></div><div><b>${wins}-${rows.length - wins}</b><span>wins-losses</span></div>
    <div><b>${fmt(k / rows.length, 1)} / ${fmt(d / rows.length, 1)} / ${fmt(a / rows.length, 1)}</b><span>K / D / A per match</span></div>
    <div><b>${heroLine}</b><span>heroes</span></div></div>`;

  const top = cards.slice(0, 5);
  const adviceHtml = top.length ? `<h2>Work on these first</h2><div class="cards">${top.map((c, i) => imCard(c, i, edgeNote)).join("")}</div>`
    : '<p class="empty">Nothing stands out: you are at or above the Phantom+ median on every number this page checks.</p>';
  const more = cards.slice(5);
  const moreHtml = more.length ? `<details class="chg"><summary>${more.length} more things to work on</summary><div class="cards">${more.map((c, i) => imCard(c, i + 5, edgeNote)).join("")}</div></details>` : "";

  // phase tables
  const row = (key) => {
    const s = stats[key];
    if (!s) return "";
    return `<tr><td>${esc(Improve.M[key].label)}</td><td class="n ${imTone(s.good)}">${imVal(key, s.mine)}</td><td class="n">${imVal(key, s.bench)}</td>
      <td class="n">${s.good == null ? fmt(s.p) : fmt(s.good)}</td><td class="im-bar-c">${imBar(s.good ?? s.p)}</td></tr>`;
  };
  const table = (title, keys, note = "") => {
    const body = keys.map(row).join("");
    return body ? `<div class="card"><h3>${title}</h3>${note}<div class="scroll"><table><thead><tr><th>Number</th><th class="n">You</th><th class="n">Phantom+</th><th class="n">Percentile</th><th></th></tr></thead><tbody>${body}</tbody></table></div></div>` : "";
  };
  const phases = Improve.PHASES.map((ph) => table(`${ph.label} (${ph.span})`, Object.keys(Improve.M).filter((k) => k.startsWith(ph.id + "."))));
  const whole = table("Whole match", ["all.spm", "all.dpm", "all.kp", "all.dka", "all.d10", "x.acc", "x.hs", "x.unspent", "x.parry"]);
  const mix = table("Damage mix", ["x.gun", "x.ability", "x.item", "x.melee"], '<p class="fine">Share of your damage to enemy heroes. Percentile here is just where you sit (a different style, not better or worse).</p>');

  // items per hero
  const itemsHtml = items.filter((h) => h.timing.length).map((h) => {
    const body = h.timing.slice(0, 14).map((x) => `<tr><td>${esc(imItem(x.id))}</td><td class="n">${pct(x.share)}</td><td class="n">${pct(x.bshare)}</td>
      <td class="n">${imClock(x.t)}</td><td class="n">${imClock(x.bt)}</td><td class="n ${x.late > 180 ? "bad" : x.late < -120 ? "good" : ""}">${x.late >= 0 ? "+" : "−"}${imClock(Math.abs(x.late))}</td>
      <td class="n">${x.edge == null ? "–" : (x.edge > 0 ? "+" : "") + fmt(x.edge, 1)}</td></tr>`).join("");
    return `<div class="card"><h3>${esc(imHero(h.hero))} items (${plural(h.n, "match", "matches")})</h3><div class="scroll"><table><thead><tr><th>Item</th><th class="n">You buy</th><th class="n">Phantom+ buy</th>
      <th class="n">Your time</th><th class="n">Phantom+ time</th><th class="n">Later by</th><th class="n">Win edge</th></tr></thead><tbody>${body}</tbody></table></div>
      <p class="fine">Times are the first purchase. Win edge: how much more often Phantom+ holders of the item win on this hero, at the same net worth, in points.</p></div>`;
  }).join("");

  const simHtml = sim?.rows.length ? `<div class="card"><h3>Your builds vs the sim's best overall build</h3><div class="scroll"><table><thead><tr><th>Match</th><th class="n">Net worth</th><th>Sim's best build</th><th class="n">You had</th></tr></thead><tbody>
    ${sim.rows.map((x) => `<tr><td>${esc(imHero(x.r.hero))} ${x.r.win ? "win" : "loss"}</td><td class="n">${fmt(x.bk / 1000)}k</td>
      <td><div class="build">${x.best.map((id) => tile(id, { static: true, cls: x.hit.includes(id) ? "" : "im-miss" })).join("")}</div></td><td class="n">${x.hit.length} of ${x.best.length}</td></tr>`).join("")}
    </tbody></table></div><p class="fine">Faded items are ones you didn't have (or anything built from them) when your net worth reached that point. Sim builds are for Phantom+, ranked by damage before dying against the typical real build of every hero.</p></div>` : "";

  const matchHtml = `<div class="card"><h3>The matches</h3><div class="scroll"><table><thead><tr><th>Hero</th><th>Result</th><th class="n">Length</th><th class="n">K / D / A</th><th class="n">Souls /min</th><th class="n">Damage /min</th><th class="n">Accuracy</th></tr></thead><tbody>
    ${rows.map((r) => `<tr><td>${esc(imHero(r.hero))}</td><td class="${r.win ? "good" : "bad"}">${r.win ? "Win" : "Loss"}</td><td class="n">${imClock(r.dur)}</td><td class="n">${r.kills} / ${r.deaths} / ${r.assists}</td>
      <td class="n">${fmt(r.v["all.spm"])}</td><td class="n">${fmt(r.v["all.dpm"])}</td><td class="n">${r.x?.v["x.acc"] != null ? pct(r.x.v["x.acc"]) : "–"}</td></tr>`).join("")}
    </tbody></table></div></div>`;

  const m = bench.meta;
  $("#im-out").innerHTML = `${summary}${adviceHtml}${moreHtml}
    <h2>Phase by phase</h2><div class="cards">${phases.join("")}${whole}${mix}</div>
    ${itemsHtml || simHtml ? `<h2>Items and builds</h2>` : ""}
    ${itemsHtml ? `<details class="chg"><summary>When you buy your items, hero by hero</summary><div class="chg-b stack">${itemsHtml}</div></details>` : ""}
    ${simHtml ? `<details class="chg"><summary>Your builds vs the sim's best builds, match by match</summary><div class="chg-b">${simHtml}</div></details>` : ""}
    <details class="chg"><summary>The ${rows.length} matches read</summary><div class="chg-b">${matchHtml}</div></details>
    <p class="fine">Benchmarks: ${fmt(m.players)} players in ${fmt(m.matches)} ${esc(m.badge)} ranked matches, ${esc(m.from)} to ${esc(m.to)} (accuracy, unspent souls, parries and damage mix from a smaller Phantom+ sample). Each of your matches is compared with Phantom+ players on the same hero. Advice is ranked by how far you are below the median times how much more the better half of Phantom+ players wins on that number; winning teams also farm and fight more, so treat the ranking as a guide.</p>`;
}
