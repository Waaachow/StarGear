# StarGear episode foundation template

A ready-to-run starting point for a new StarGear episode/story page, forked from the
Episode 0 engine (`iso_grid_prototype.html` / `episode1.html`) with everything
story-specific stripped out. First built as "Project Echoes" (2026-07-27); this is
that same build, genericized so it can be copied for the *next* one without
re-doing the strip-down work.

⚠️ **These two files must live next to the project's `Assets/` folder** (i.e. copy
them to the project root, not run them from inside `_templates/`) — every sprite is
loaded from a relative path like `Assets/obj/Cyclops_ne.png`, which only resolves
correctly one level up from here. Running them in place shows a working title
screen and menu but every ship sprite 404s.

## What's in it

- **`episode-template.html`** — the title screen (Start button over a procedural
  CSS placeholder background — no image asset needed) that fades to black and boots
  the flight engine in a fullscreen iframe. No VN/cast/dialogue system and no
  title-screen Load panel — there's no story yet, so Start always drops you into
  free-roam, and save/load lives entirely in the flight engine's own Menu → Save/Load.
- **`episode-template-flight.html`** — the forked flight/combat/menu engine. Working:
  ship flight over an open sector, random roaming enemy ships, turn-based space
  combat, the 6 crew with their existing abilities, the Ship Config module grid,
  scanning, scrap/cargo/coin HUD, Ship Database (6 common hulls), Field Manual (7
  chapters), and save/load. Deliberately **empty/placeholder**: no world objects
  (nebula/asteroids/planets/stations/wrecks/hangar/Nexus — `buildMap()` returns
  `[]`), no themed regions (`ZONES = []`, map reads as one uniform "Open Space"), no
  stations/trade/market, no bounties, no side missions, no story waypoints, no
  achievements/awards (Missions is a single "No missions yet" placeholder tab).

## How to start a new episode from this

1. Copy both files to wherever the new episode lives (e.g. the project root), and
   give them your own names — e.g. `episode2.html` / `episode2_flight.html`.
2. In the outer shell file, update the `gpFrame.src = "episode-template-flight.html"`
   line to point at your renamed flight file.
3. **Rename the `localStorage` prefix** — every save/state key in the flight file
   starts with `NEWEP_` (e.g. `NEWEP_save_0`, `NEWEP_shipdex`). Find-and-replace
   `NEWEP_` with a short slug unique to this episode (e.g. `ep2_`). This is not
   cosmetic: if two episodes on the same domain share a prefix, their saves,
   discovered ships, tips-seen state, etc. will silently clobber each other. (This
   bit us once already — Project Echoes originally inherited Episode 0's exact
   `stargear_*` keys before it was caught and renamed to `echoes_*`.)
4. Update the `<title>` tags (both files) and the title-screen kicker/title text
   (`.peKicker` / `.peTitle` in the outer shell) to the new episode's name.
5. Swap the procedural placeholder background for real title art when it exists —
   see the `.peBg`/`.peGlow` rules and the `pePlaceholderTag` note in the outer shell
   for where that lives.
6. Re-add whatever story-specific systems this episode actually needs (world
   objects, stations, bounties, side jobs, story beats, achievements) — the code
   that used to run all of that in Episode 0 is documented in
   `iso_grid_prototype.html` / `episode1.html` if you want to port a piece of it back
   rather than rebuild from scratch.

## Verifying a new instance

Playtest over `http://localhost:8123` (a static server rooted at the project dir),
**never `file://`** — file:// partitions localStorage per-iframe, which makes saves
disappear and looks like a bug when it isn't. A minimal server script:

```js
const http = require("http"), fs = require("fs"), path = require("path");
const ROOT = "<project dir>";
const TYPES = { ".html":"text/html", ".js":"text/javascript", ".css":"text/css",
  ".png":"image/png", ".jpg":"image/jpeg", ".mp3":"audio/mpeg" };
http.createServer((req, res) => {
  const fp = path.join(ROOT, decodeURIComponent(req.url.split("?")[0]));
  fs.readFile(fp, (err, data) => {
    if (err) { res.writeHead(404); res.end("404"); return; }
    res.writeHead(200, { "Content-Type": TYPES[path.extname(fp).toLowerCase()] || "application/octet-stream" });
    res.end(data);
  });
}).listen(8123, () => console.log("serving :8123"));
```

Drive it with Playwright (`chromium.launch()`, `page.on("pageerror", ...)`) rather
than a headless-Edge check — that's what caught the original localStorage
collision and confirmed the stripped systems (empty `MAP_OBJECTS`/`TRADE_STATIONS`/
`BOUNTIES`/`SIDE_MISSIONS`/`ACHIEVEMENTS`, trimmed `DEX_ENTRIES`) actually hold at
runtime, not just in the source.
