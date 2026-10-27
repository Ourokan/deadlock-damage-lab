// Steam sign-in: who is using the page, so the damage test and build maker can use the player's own aim on each hero
// and load their own builds. The site is static (no server), so "Sign in through Steam" reads the SteamID that
// Steam's OpenID page hands back without asking Steam to confirm it (that check needs a server). It only ever
// reads public match stats, so a faked ID just shows someone else's public numbers; typing a Steam ID or profile
// link does the same thing without the redirect. Everything is kept in this browser (localStorage).
"use strict";

const Account = (() => {
  const KEY = "ddl.player", AIM_KEY = "ddl.player.aim", BACK_KEY = "ddl.signin.back", STATE_KEY = "ddl.signin.state";
  const STEAM64 = 76561197960265728n, OPENID = "https://steamcommunity.com/openid/login";
  const NS = "http://specs.openid.net/auth/2.0", SELECT = NS + "/identifier_select";
  const FRESH_MS = 12 * 3600 * 1000;   // per-hero aim is read again after this long
  const subs = [];
  const pending = new Map();           // hero id -> in-flight aim read

  const read = (k) => { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch { return null; } };
  const write = (k, v) => { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, JSON.stringify(v)); } catch { /* storage off */ } };

  let me = read(KEY);                 // {id (SteamID3 account id), name, avatar, via: "steam"|"typed", at}
  let aims = (me && read(AIM_KEY)) || {};
  if (aims.id !== me?.id) aims = { id: me?.id, heroes: {} };

  const emit = () => subs.forEach((f) => { try { f(me); } catch (e) { console.error(e); } });

  // Off to Steam's sign-in page; it comes back to this page with openid.* in the query string. A random value in
  // return_to ties the answer to a sign-in this tab started, so a crafted link can't switch someone's account.
  function signIn() {
    const st = Array.from(crypto.getRandomValues(new Uint8Array(12)), (b) => b.toString(16).padStart(2, "0")).join("");
    try { sessionStorage.setItem(BACK_KEY, location.href); sessionStorage.setItem(STATE_KEY, st); } catch { /* no sessionStorage: the answer is refused */ }
    const back = `${location.origin}${location.pathname}?st=${st}`;
    const p = new URLSearchParams({ "openid.ns": NS, "openid.mode": "checkid_setup", "openid.return_to": back,
      "openid.realm": location.origin + "/", "openid.identity": SELECT, "openid.claimed_id": SELECT });
    location.assign(`${OPENID}?${p}`);
  }

  // Run once at startup, before anything reads the query string: takes Steam's answer out of the address bar
  // (putting back the link the page was on) and returns the account id it named, or null.
  function takeReturn() {
    const q = new URLSearchParams(location.search);
    if (!q.has("openid.mode")) return null;
    let back = null, st = null;
    try { back = sessionStorage.getItem(BACK_KEY); st = sessionStorage.getItem(STATE_KEY); sessionStorage.removeItem(BACK_KEY); sessionStorage.removeItem(STATE_KEY); } catch { /* no saved link */ }
    if (!st || q.get("st") !== st) back = null;   // not a sign-in this tab started: drop the answer and its link
    try { history.replaceState(null, "", back && new URL(back).origin === location.origin ? back : location.pathname + location.hash); } catch { /* sandboxed */ }
    const m = back != null && q.get("openid.mode") === "id_res" && q.get("openid.op_endpoint") === OPENID
      && /^https:\/\/steamcommunity\.com\/openid\/id\/(7656\d{13})$/.exec(q.get("openid.claimed_id") || "");
    return m ? Number(BigInt(m[1]) - STEAM64) : null;
  }

  async function setPlayer(id, via, name = null) {
    let row = null;
    try { row = (await Aim.get(`/v1/players/steam?account_ids=${id}`))[0]; } catch { /* name and picture are only labels */ }
    me = { id, name: row?.personaname || name || `Player ${id}`, avatar: row?.avatar || null, via, at: Date.now() };
    write(KEY, me);
    if (aims.id !== id) { aims = { id, heroes: {} }; write(AIM_KEY, aims); }
    emit();
    return me;
  }

  // Steam profile link, SteamID64, SteamID3 or Steam name (Aim.resolve) -> signed in as that player.
  async function enter(text) {
    const who = await Aim.resolve(text);
    return setPlayer(who.id, "typed", who.name);
  }

  function signOut() {
    me = null; aims = { id: null, heroes: {} };
    write(KEY, null); write(AIM_KEY, null);
    emit();
  }

  const cached = (hero) => (me && aims.heroes[hero]) || null;

  // The signed-in player's hero-only accuracy, headshot rate and fight distance on this hero (Aim.fromMatches: last
  // 10 matches, all heroes when there are fewer than 3 on it), plus their latest build on it. Kept for 12 h.
  async function heroAim(hero, { force = false, onProgress } = {}) {
    if (!me) return null;
    const c = cached(hero);
    if (c && !force && Date.now() - c.at < FRESH_MS) return c;
    const key = `${me.id}:${hero}`;
    if (!pending.has(key)) {
      const id = me.id;
      pending.set(key, Aim.fromMatches(id, hero, { onProgress }).then((r) => {
        const row = { accuracy: r.accuracy, headshot: r.headshot, distance: r.distance, matches: r.matches, shots: r.shots,
          scope: r.scope, failed: r.failed, last: r.last, at: Date.now() };
        if (me?.id === id) { aims.heroes[hero] = row; write(AIM_KEY, aims); }
        return row;
      }).finally(() => pending.delete(key)));
    }
    return pending.get(key);
  }

  return { signIn, takeReturn, setPlayer, enter, signOut, heroAim, cached, current: () => me, onChange: (f) => subs.push(f) };
})();

if (typeof module !== "undefined") module.exports = Account;
