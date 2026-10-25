// Runs the site's fight detection (web/replay.js rpNorm + rpDetect) on one saved match metadata JSON
// (/v1/matches/{id}/metadata) and prints the fights as JSON. usage: node detect.cjs <web/replay.js> <match.json>
"use strict";
const fs = require("fs"), vm = require("vm");
const ctx = { S: { dataReady: new Promise(() => {}) }, console, Math, JSON, Object, Number, Set, isFinite };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], "utf8") + "\nthis.rpNorm = rpNorm; this.rpDetect = rpDetect;", ctx);
const mi = JSON.parse(fs.readFileSync(process.argv[3])).match_info;
const d = ctx.rpNorm(mi);
const team = Object.fromEntries(mi.players.map((p) => [p.player_slot, String(p.team).endsWith("1") ? 1 : 0]));
process.stdout.write(JSON.stringify({ fights: ctx.rpDetect(d.paths, team, d.deaths), deaths: d.deaths.length }));
