// Personal aim: pull a player's own hero accuracy, headshot rate and fight distance from their recent matches
// (Deadlock API, called straight from the browser) and place numbers against the ranked spread for a hero.
// Same numbers as sim/deadsim/accuracy.py player_skill(): the per-match "Enemy Hero Accuracy" stats count only
// bullets fired at heroes, unlike the overall accuracy on profile pages, which includes creeps.
"use strict";

const Aim = (() => {
  const API = "https://api.deadlock-api.com";
  const STEAM64 = 76561197960265728n;
  const SHOTS = "Enemy Hero Accuracy##Shots", HITS = "Enemy Hero Accuracy##Hits", HEADS = "Enemy Hero Accuracy##Headshots";
  const DIST = "Outgoing Bullet Dist##";
  const EDGES = { 10: 10, 20: 20, 30: 30, 40: 40, 50: 50, 75: 75, 100: 100, Infinite: 150 };

  async function get(path) {
    const r = await fetch(API + path);
    if (!r.ok) { const e = new Error(`${path} ${r.status}`); e.status = r.status; throw e; }
    return r.json();
  }

  // Steam profile link, SteamID64, SteamID3 ([U:1:n] or the bare number) or a Steam name -> {id, name}.
  // name is the Steam persona name looked up for the id, so the page can show whose matches it read.
  async function resolve(text) {
    const t = String(text).trim();
    if (!t) throw new Error("Enter your Steam profile link, Steam ID or Steam name.");
    const u3 = t.match(/^\[?U:1:(\d+)\]?$/i);
    const prof = t.match(/steamcommunity\.com\/profiles\/(\d{17})/) || t.match(/^(7656\d{13})$/);
    const id = u3 ? Number(u3[1]) : prof ? Number(BigInt(prof[1]) - STEAM64) : /^\d{1,10}$/.test(t) ? Number(t) : null;
    if (id != null) {
      let name = null;
      try { name = (await get(`/v1/players/steam?account_ids=${id}`))[0]?.personaname || null; } catch { /* name is only a label */ }
      return { id, name };
    }
    const vanity = t.match(/steamcommunity\.com\/id\/([^/?#]+)/);
    const q = vanity ? vanity[1] : t;
    let rows = [];
    try { rows = await get(`/v1/players/steam-search?search_query=${encodeURIComponent(q)}&limit=1`); } catch (e) { if (e.status !== 404) throw e; }
    if (!rows.length) throw new Error(`No Deadlock player found for "${q}". Paste your Steam profile link with the long number instead.`);
    return { id: rows[0].account_id, name: rows[0].personaname };
  }

  const player = (meta, accountId) => ((meta.match_info || meta).players || []).find((x) => x.account_id === accountId);

  // One player's hero-only gun numbers in one match, from the last stats snapshot, or null.
  function matchStats(meta, accountId) {
    const mi = meta.match_info || meta;
    const names = Object.fromEntries((mi.custom_user_stats || []).map((c) => [c.id, c.name]));
    const p = player(meta, accountId);
    const last = p?.stats?.length ? p.stats[p.stats.length - 1] : null;
    if (!last) return null;
    const cs = {};
    for (const c of last.custom_user_stats || []) cs[names[c.id] || c.id] = c.value;
    return cs[SHOTS] ? cs : null;
  }

  // Median engagement distance (m) from the bullet-hit distance histogram, as distance_profile() in accuracy.py.
  function medianDistance(dist) {
    const b = Object.entries(dist).map(([k, v]) => [EDGES[k], v]).filter(([e]) => e).sort((a, c) => a[0] - c[0]);
    const tot = b.reduce((s, [, v]) => s + v, 0);
    if (!tot) return null;
    let acc = 0, prev = 0;
    for (const [edge, v] of b) {
      const s = v / tot;
      if (acc + s >= 0.5) return prev + (edge - prev) * (0.5 - acc) / s;
      acc += s; prev = edge;
    }
    return prev;
  }

  // Recent normal matches (on heroId when it has at least `min` of them, else any hero) -> aim summary.
  async function fromMatches(accountId, heroId, { n = 10, min = 3, onProgress } = {}) {
    let hist;
    try { hist = await get(`/v1/players/${accountId}/match-history`); } catch (e) {
      throw new Error(e.status === 404 || e.status === 400 ? "That player has no Deadlock match history on record." : "The Deadlock API did not answer. Try again in a minute.");
    }
    const normal = hist.filter((m) => m.game_mode === 1).sort((a, b) => b.start_time - a.start_time);
    const onHero = normal.filter((m) => m.hero_id === heroId);
    const pool = (onHero.length >= min ? onHero : normal).slice(0, n * 2);
    const scope = onHero.length >= min ? "hero" : "all";
    let shots = 0, hits = 0, heads = 0, used = 0, next = 0, failed = 0, last = null;
    const dist = {};
    const worker = async () => {
      while (used < n && next < pool.length) {
        const m = pool[next++];
        let cs = null, meta = null;
        try { meta = await get(`/v1/matches/${m.match_id}/metadata`); cs = matchStats(meta, accountId); } catch (e) {
          if (e.status !== 404) failed++; // 404 = not ingested yet; anything else (429, 5xx, network) is a failed read
        }
        if (!cs || used >= n) continue;
        if (m.hero_id === heroId && (!last || m.start_time > last.start_time)) last = { ...buildOf(player(meta, accountId)), match_id: m.match_id, start_time: m.start_time };
        used++; shots += cs[SHOTS]; hits += cs[HITS] || 0; heads += cs[HEADS] || 0;
        for (const [k, v] of Object.entries(cs)) if (typeof k === "string" && k.startsWith(DIST)) { const b = k.slice(DIST.length); dist[b] = (dist[b] || 0) + v; }
        onProgress?.(used, Math.min(n, pool.length));
      }
    };
    await Promise.all([worker(), worker(), worker()]);
    if (!shots) throw new Error(failed ? "The Deadlock API did not answer for your matches (it may be rate limiting). Try again in a minute."
      : "No recent matches with aim stats yet. New matches can take a while to show up.");
    return { accuracy: hits / shots, headshot: heads / Math.max(1, hits), distance: medianDistance(dist),
      matches: used, failed, scope, shots, hits, headshots: heads, last };
  }

  // A player's purchases and net worth over one match (the item ids the shop shows; components and sold items included).
  function buildOf(p) {
    return { items: (p.items || []).map((x) => [x.item_id, x.game_time_s, x.sold_time_s || 0]),
      nw: (p.stats || []).map((s) => [s.time_stamp_s, s.net_worth]), net_worth: p.net_worth };
  }

  // Items held when the player's net worth first reached `souls` (or at the end, when it never did), from buildOf().
  // `known` keeps only ids the page can price (shop items); `comps(id)` (item ids it's built from) drops components
  // still listed next to the item that replaced them.
  function heldAt(b, souls, known, comps = () => []) {
    const pts = [[0, 0], ...b.nw];
    let t = Infinity;
    for (let i = 1; i < pts.length; i++) {
      const [t1, v1] = pts[i], [t0, v0] = pts[i - 1];
      if (v1 >= souls) { t = t0 + (t1 - t0) * (souls - v0) / Math.max(1, v1 - v0); break; }
    }
    const out = [];
    for (const [id, at, sold] of b.items) if (known(id) && at <= t && (!sold || sold > t) && !out.includes(id)) out.push(id);
    const inside = new Set(out.flatMap((id) => comps(id)));
    return { items: out.filter((id) => !inside.has(id)), t: isFinite(t) ? t : null };
  }

  // Where a value sits in a {p25, p50, p75, p90} spread, as a rough ranked percentile (linear between points).
  function percentile(v, q) {
    if (v == null || !q) return null;
    const pts = [[25, q.p25], [50, q.p50], [75, q.p75], [90, q.p90]];
    if (v <= pts[0][1]) return { below: v < pts[0][1], p: 25 };
    if (v >= pts[3][1]) return { above: v > pts[3][1], p: 90 };
    for (let i = 1; i < pts.length; i++) {
      const [p0, a] = pts[i - 1], [p1, b] = pts[i];
      if (v <= b) return { p: Math.round(p0 + (p1 - p0) * (v - a) / Math.max(1e-9, b - a)) };
    }
    return null;
  }

  return { resolve, fromMatches, matchStats, medianDistance, percentile, heldAt, get };
})();

if (typeof module !== "undefined") module.exports = Aim;
