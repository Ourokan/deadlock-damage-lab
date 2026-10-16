// Team fight tab: 1-3 heroes a side fight in the live sim (bridge.team). Uses app.js globals ($, esc, fmt, S, load,
// damageHero, simCall) and only touches #tab-team.
"use strict";

const TF = { inited: false, souls: 27000, focus: "focus", a: [], b: [] };
const TF_START = { a: [13, 6, 11], b: [1, 2, 31] };   // Haze, Abrams, Dynamo vs Infernus, Seven, Lash (hero ids)

async function tfPopular(hero) {
  const d = await damageHero(hero);
  if (!d) return [];
  const keys = Object.keys(d.budgets).sort((x, y) => Math.abs(x - TF.souls) - Math.abs(y - TF.souls));
  return keys.length ? [...d.budgets[keys[0]].popular.items] : [];
}

async function tfAdd(side, hero) {
  if (TF[side].length >= 3) return;
  TF[side].push({ hero, items: await tfPopular(hero) });
  tfRender();
}

function tfMember(side, i) {
  const m = TF[side][i];
  const heroes = S.heroes.map((h) => `<option value="${h.id}"${h.id === m.hero ? " selected" : ""}>${esc(h.name)}</option>`).join("");
  const items = m.items.map((id) => {
    const it = S.items[id];
    return it ? `<button class="it x" data-slot="${it.slot}" data-side="${side}" data-i="${i}" data-drop="${id}" title="Remove">${esc(it.name)}</button>` : "";
  }).join("");
  return `<div class="tf-m">
    <div class="row">
      <label class="f"><span>Hero ${i + 1}</span><select data-side="${side}" data-i="${i}" class="tf-hero">${heroes}</select></label>
      <button class="ghost" data-side="${side}" data-i="${i}" data-pop="1">Popular build</button>
      <button class="ghost" data-side="${side}" data-i="${i}" data-rm="1"${TF[side].length < 2 ? " disabled" : ""}>Remove</button>
    </div>
    <div class="build">${items}</div>
    <input type="search" list="tf-items" placeholder="Add an item" data-side="${side}" data-i="${i}" class="tf-add">
  </div>`;
}

function tfRender() {
  for (const side of ["a", "b"]) {
    $(`#tf-${side}`).innerHTML = TF[side].map((_, i) => tfMember(side, i)).join("")
      + (TF[side].length < 3 ? `<button class="ghost" data-side="${side}" data-more="1">Add a hero</button>` : "");
  }
}

function tfResult(r) {
  const win = r.winner ? `Team ${r.winner} wins in ${fmt(r.time, 1)} s` : `Nobody wins in ${fmt(r.time, 0)} s`;
  const row = (x) => `<tr><td>${esc(x.team)}</td><td>${esc(x.hero)}</td><td>${fmt(x.damage)}</td><td>${fmt(x.damage_taken)}</td>
    <td>${fmt(x.healing_given + x.barrier_given)}</td><td>${fmt(x.kills)}</td>
    <td>${x.alive ? `${fmt(x.hp)} / ${fmt(x.max_hp)} HP` : `died at ${fmt(x.death_time, 1)} s`}</td></tr>`;
  const tot = (side, k) => r.fighters.filter((x) => x.team === side).reduce((s, x) => s + x[k], 0);
  const totRow = (side) => `<tr class="tf-tot"><td>${side}</td><td>Team</td><td>${fmt(tot(side, "damage"))}</td><td>${fmt(tot(side, "damage_taken"))}</td>
    <td>${fmt(tot(side, "healing_given") + tot(side, "barrier_given"))}</td><td>${fmt(tot(side, "kills"))}</td><td></td></tr>`;
  const support = r.fighters.filter((x) => x.healing_given > 0).map((x) =>
    `${esc(x.hero)}: ${Object.entries(x.healing_given_by_source).map(([k, v]) => `${esc(k)} ${fmt(v)}`).join(", ")}`).join(" · ");
  $("#tf-out").innerHTML = `<h2>${win}</h2>
    <div class="scroll"><table class="tf-table"><thead><tr><th>Team</th><th>Hero</th><th>Damage</th><th>Taken</th><th>Heals + shields given</th><th>Kills</th><th>End</th></tr></thead>
    <tbody>${r.fighters.map(row).join("")}${totRow("A")}${totRow("B")}</tbody></table></div>
    ${support ? `<p class="fine">Heals on teammates: ${support}</p>` : ""}`;
}

async function tfRun() {
  const btn = $("#tf-run");
  btn.disabled = true; btn.textContent = "Fighting…"; $("#tf-err").hidden = true;
  try {
    const req = { souls: TF.souls, focus: TF.focus, a: TF.a, b: TF.b };
    tfResult(await simCall("team", req));
  } catch (e) {
    $("#tf-err").hidden = false; $("#tf-err").textContent = "That fight failed: " + e.message;
  } finally {
    btn.disabled = false; btn.textContent = "Run team fight";
  }
}

async function tfInit() {
  if (TF.inited || !S.heroes.length) return;
  TF.inited = true;
  $("#tf-items").innerHTML = Object.values(S.items).map((it) => `<option value="${esc(it.name)}">`).join("");
  const byName = {};
  for (const [id, it] of Object.entries(S.items)) byName[it.name.toLowerCase()] = Number(id);
  const valid = (id) => S.heroById[id];
  for (const side of ["a", "b"]) for (const h of TF_START[side].filter(valid).slice(0, 3)) await tfAdd(side, h);
  const tab = $("#tab-team");
  tab.addEventListener("click", async (e) => {
    const t = e.target.closest("button"); if (!t) return;
    const side = t.dataset.side, i = Number(t.dataset.i);
    if (t.dataset.drop) { TF[side][i].items = TF[side][i].items.filter((x) => String(x) !== t.dataset.drop); tfRender(); }
    else if (t.dataset.pop) { TF[side][i].items = await tfPopular(TF[side][i].hero); tfRender(); }
    else if (t.dataset.rm) { TF[side].splice(i, 1); tfRender(); }
    else if (t.dataset.more) { const used = new Set(TF[side].map((m) => m.hero)); await tfAdd(side, S.heroes.find((h) => !used.has(h.id)).id); }
    else if (t.dataset.v && t.closest("#tf-focus")) { TF.focus = t.dataset.v; $$("#tf-focus button").forEach((x) => x.classList.toggle("on", x === t)); }
  });
  tab.addEventListener("change", async (e) => {
    const t = e.target, side = t.dataset.side, i = Number(t.dataset.i);
    if (t.classList.contains("tf-hero")) { TF[side][i] = { hero: Number(t.value), items: await tfPopular(Number(t.value)) }; tfRender(); }
    else if (t.classList.contains("tf-add")) {
      const id = byName[t.value.trim().toLowerCase()];
      if (id && !TF[side][i].items.includes(id)) { TF[side][i].items.push(id); tfRender(); }
      else t.value = "";
    } else if (t.id === "tf-souls") { TF.souls = Number(t.value) || 0; }
  });
  $("#tf-run").onclick = tfRun;
  S.whenReady.then(() => { $("#tf-run").disabled = false; });
}

function tfMaybeInit() { if ((location.hash || "").slice(1) === "team") tfInit(); }
window.addEventListener("hashchange", tfMaybeInit);
(function wait() { if (S.heroes.length) tfMaybeInit(); else setTimeout(wait, 200); })();
