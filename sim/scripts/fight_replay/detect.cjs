// Runs the site's fight detection (web/replay.js rpNorm + rpDetect) on one saved match metadata JSON
// (/v1/matches/{id}/metadata) and prints the fights as JSON (with every hero's 1 s health path when "hp" is given).
// usage: node detect.cjs <web/replay.js> <match.json> [hp]
"use strict";
const fs = require("fs"), vm = require("vm");
const ctx = { S: { dataReady: new Promise(() => {}) }, console, Math, JSON, Object, Number, Set, isFinite };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], "utf8") + "\nthis.rpNorm = rpNorm; this.rpDetect = rpDetect;", ctx);
const mi = JSON.parse(fs.readFileSync(process.argv[3])).match_info;
const d = ctx.rpNorm(mi);
const team = Object.fromEntries(mi.players.map((p) => [p.player_slot, String(p.team).endsWith("1") ? 1 : 0]));
const out = { fights: ctx.rpDetect(d.paths, team, d.deaths), deaths: d.deaths.length, team };
if (process.argv[4] === "hp") out.hp = Object.fromEntries(Object.entries(d.paths).map(([s, p]) => [s, p.hp]));
if (process.argv[4] === "hp") out.xy = Object.fromEntries(Object.entries(d.paths).map(([s, p]) => [s, [p.x.map(Math.round), p.y.map(Math.round)]]));
process.stdout.write(JSON.stringify(out));
