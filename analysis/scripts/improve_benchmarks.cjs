// Phantom+ benchmarks for the site's Improvements tab (web/improve.js): per hero, the spread of every number the tab
// compares a player on, whole match and per phase, how much more the better half of Phantom+ players wins on each,
// and when Phantom+ players buy each item.
//
//   python3 analysis/scripts/fetch_improve_sample.py --n 3000   # analysis/work/improve/sample.jsonl.gz (stat timelines)
//   python3 analysis/scripts/fetch_improve_sample.py --winners  # match results for sim/validation/phantom_sample.jsonl.gz
//   node analysis/scripts/improve_benchmarks.cjs                # -> analysis/out/improve_benchmarks.json (web/build.py copies it)
//
// The stat-timeline numbers come from the bulk sample; accuracy and headshots from sim/validation/aim_sample.jsonl.gz
// (4,200 Phantom+ matches); unspent souls, parries and damage mix from sim/validation/phantom_sample.jsonl.gz (600).
// "win" per metric: within each hero, players above the hero's median vs below it, win rate difference in points
// (pooled over heroes). It is an association (winning teams farm and fight more), used only to rank the advice.
"use strict";
const fs = require("fs"), path = require("path"), zlib = require("zlib");
const ROOT = path.resolve(__dirname, "../..");
const Improve = require(path.join(ROOT, "web/improve.js"));

const lines = (f) => zlib.gunzipSync(fs.readFileSync(path.join(ROOT, f))).toString().split("\n").filter(Boolean).map((l) => JSON.parse(l));
const r = (x, d) => (x == null ? null : Math.round(x * 10 ** d) / 10 ** d);
const dig = (q) => q.map((x) => r(x, Math.abs(q[Improve.MID]) >= 100 ? 0 : Math.abs(q[Improve.MID]) >= 1 ? 2 : 4));

const shop = JSON.parse(fs.readFileSync(path.join(ROOT, "search/out/items.json")));
const vals = {};     // hero -> key -> [[value, win, game-state bin]]
const items = {};    // hero -> item -> [[t, nw]]
const players = {};  // hero -> count (bulk sample)
const src = {};      // hero -> source -> sum of shares, plus count
const add = (hero, key, v, win, bin = 0) => { if (v == null || !isFinite(v)) return; ((vals[hero] ||= {})[key] ||= []).push([v, win, bin]); };
// game state when a phase starts: own team's net worth lead, in bins (lane starts even)
const START = Object.fromEntries(Improve.PHASES.map((ph) => [ph.id, ph.from]));
const leadBin = (lead) => (lead < -6000 ? -2 : lead < -2000 ? -1 : lead <= 2000 ? 0 : lead <= 6000 ? 1 : 2);

const sample = lines("analysis/work/improve/sample.jsonl.gz");
let t0 = Infinity, t1 = 0;
for (const m of sample) {
  const st = typeof m.start_time === "string" ? Date.parse(m.start_time.replace(" ", "T") + "Z") / 1000 : m.start_time;
  t0 = Math.min(t0, st); t1 = Math.max(t1, st);
  const teamNw = (team, t) => m.players.filter((p) => Improve.teamOf(p.team) === team).reduce((s, p) => s + Improve.at(p.stats || [], "net_worth", t), 0);
  for (const p of m.players) {
    const f = Improve.features(m, p);
    if (!f) continue;
    players[f.hero] = (players[f.hero] || 0) + 1;
    const me = Improve.teamOf(p.team), bins = {};
    for (const [ph, t] of Object.entries(START)) bins[ph] = t ? leadBin(teamNw(me, t) - teamNw(me === "0" ? "1" : "0", t)) : 0;
    for (const [k, v] of Object.entries(f.v)) add(f.hero, k, v, f.win, bins[k.split(".")[0]] ?? 0);
    for (const [id, t, nw] of f.items) if (shop[id]) ((items[f.hero] ||= {})[id] ||= []).push([t, nw]);
  }
}

const winners = JSON.parse(fs.readFileSync(path.join(ROOT, "analysis/work/improve/winners.json")));
for (const m of lines("sim/validation/phantom_sample.jsonl.gz")) {
  const won = winners[m.match_id];
  for (const p of m.players) {
    if (!p.damage_sources || !Object.keys(p.damage_sources).length) continue;
    const x = Improve.extras(p.custom || {}, p.damage_sources, m.duration_s, Number(p.net_worth)), hero = Number(p.hero_id);
    const win = won == null ? null : Improve.teamOf(won) === Improve.teamOf(p.team);
    for (const [k, v] of Object.entries(x.v)) if (k !== "x.acc" && k !== "x.hs") add(hero, k, v, win);
    const s = (src[hero] ||= { n: 0, s: {} });
    s.n++;
    for (const [k, v] of Object.entries(x.src)) s.s[k] = (s.s[k] || 0) + v;
  }
}
// accuracy and headshots: the bigger aim sample for the spread; win gap from the 600 matches with results
const accWin = {};
for (const m of lines("sim/validation/phantom_sample.jsonl.gz")) {
  const won = winners[m.match_id];
  for (const p of m.players) {
    const x = Improve.extras(p.custom || {}, {}, m.duration_s);
    for (const k of ["x.acc", "x.hs"]) if (x.v[k] != null) ((accWin[p.hero_id] ||= {})[k] ||= []).push([x.v[k], won == null ? null : Improve.teamOf(won) === Improve.teamOf(p.team)]);
  }
}
for (const m of lines("sim/validation/aim_sample.jsonl.gz")) {
  for (const p of m.players) {
    const x = Improve.extras(p.custom || {}, {}, m.duration_s);
    for (const k of ["x.acc", "x.hs"]) add(Number(p.hero_id), k, x.v[k], null);
  }
}

// spreads, and the win gap between each hero's halves
const out = { meta: {}, all: { m: {} }, heroes: {}, names: {} };
const pooled = {}, gap = {};   // gap[key][bin] = {hi: [wins, n], lo: [wins, n]}
for (const [hero, ks] of Object.entries(vals)) {
  const h = (out.heroes[hero] = { n: players[hero] || 0, m: {}, items: {}, src: {} });
  for (const [k, xs] of Object.entries(ks)) {
    const q = Improve.quantiles(xs.map((x) => x[0]));
    h.m[k] = dig(q);
    if (Improve.M[k]?.mean) (h.mean ||= {})[k] = r(Improve.mean(xs.map((x) => x[0])), 2);
    (pooled[k] ||= []).push(...xs.map((x) => x[0]));
    const wins = (k === "x.acc" || k === "x.hs") ? accWin[hero]?.[k] || [] : xs;
    for (const [v, w, bin = 0] of wins) {
      if (w == null || v === q[Improve.MID]) continue;
      const g = ((gap[k] ||= {})[bin] ||= { hi: [0, 0], lo: [0, 0] });
      const side = v > q[Improve.MID] ? g.hi : g.lo;
      side[0] += w ? 1 : 0; side[1]++;
    }
  }
  for (const [id, xs] of Object.entries(items[hero] || {})) {
    const share = xs.length / Math.max(1, players[hero]);
    if (share < 0.03) continue;
    const tq = Improve.quantiles(xs.map((x) => x[0]), [50, 25, 75]);
    h.items[id] = [r(share, 3), Math.round(tq[0]), Math.round(tq[1]), Math.round(tq[2]), Math.round(Improve.median(xs.map((x) => x[1])))];
  }
  const s = src[hero];
  if (s) for (const [k, v] of Object.entries(s.s).sort((a, b) => b[1] - a[1]).slice(0, 12)) h.src[k] = r(v / s.n, 3);
}
for (const [k, xs] of Object.entries(pooled)) {
  out.all.m[k] = dig(Improve.quantiles(xs));
  if (Improve.M[k]?.mean) (out.all.mean ||= {})[k] = r(Improve.mean(xs), 2);
}
// win gap per metric: within each game-state bin, then averaged with each bin weighted by its smaller half, so a
// phase number isn't credited with the win its team's lead at the phase start already brought
const wr = (x) => x[0] / Math.max(1, x[1]);
const winGap = (bins) => {
  let s = 0, w = 0;
  for (const g of Object.values(bins)) { const n = Math.min(g.hi[1], g.lo[1]); if (n >= 20) { s += n * (wr(g.hi) - wr(g.lo)); w += n; } }
  return w ? 100 * s / w : 0;
};
out.meta = {
  generated: new Date().toISOString(), badge: "Phantom+ (average badge 91 and up)",
  matches: sample.length, players: Object.values(players).reduce((a, b) => a + b, 0),
  from: new Date(t0 * 1000).toISOString().slice(0, 10), to: new Date(t1 * 1000).toISOString().slice(0, 10),
  win: Object.fromEntries(Object.entries(gap).map(([k, g]) => [k, r(winGap(g), 1)])),
};
// display names of the damage sources the spreads mention (abilities and items, by class name)
const abil = JSON.parse(fs.readFileSync(path.join(ROOT, "data/game/abilities.json")));
const cls = Object.fromEntries([...abil.map((a) => [a.class_name, a.name]), ...Object.values(shop).map((i) => [i.class_name, i.name])]);
for (const h of Object.values(out.heroes)) for (const k of Object.keys(h.src)) if (cls[k]) out.names[k] = cls[k];
fs.writeFileSync(path.join(ROOT, "analysis/out/improve_benchmarks.json"), JSON.stringify(out));
console.log(out.meta, Object.keys(out.heroes).length, "heroes,", (fs.statSync(path.join(ROOT, "analysis/out/improve_benchmarks.json")).size / 1024).toFixed(0), "KB");
