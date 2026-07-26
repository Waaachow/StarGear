# StarGear — Build TODO

Transcribed from Steve's to-do list (2026-07-20), with the design answers given in the
same session folded in. Status: ☐ not started · ◐ in progress · ✅ done.

---

## Status at 2026-07-21 — everything on the original list is built; no asset gates a feature

**Done:** dynamic start menu · scrap/coin economy + cargo capacity · enemy scrap drops · module
breakage on a loss · post-story free play · achievements · star map legend · mini-map · boss
framework + 3 bounty bosses · trade stations + dock screen · sell scrap / repair / buy+sell modules ·
commodity market · bounty board · side missions · missions tabs · exploration scan · crew chatter ·
per-hull attack visuals · SFX layer · save/load · **title-screen Load Game** · **scrap/coin icons**.

**Still open:**
1. **Clean up avatars** — ◐ **Astra done 2026-07-22; other 5 crew remain.** The defect was a green
   matte halo (leftover background pixels fringing the outline). Steve hand-cleaned Astra's 11 poses
   and delivered them as `*_v2.png`; verified like-for-like (same pose/crop/expression, halo gone —
   Angry_v2 also recolored its anger marks green→red) and **copied each over its original filename**
   (`Neutral.png`, `Astra-Status.png`, etc.), so code references need no change. `_v2` files kept as
   backup. **Tessa done 2026-07-22** — Steve replaced all 11 poses with clean transparent 1200×896
   cutouts (verified alpha=0, new art is more Western-comic than the old anime style); only fix
   needed was renaming his `Tessa_Status.png` → `Tessa-Status.png` (the code wants a hyphen).
   **Rex done 2026-07-22** — 11 clean transparent poses; status card was already correctly named, but
   his old files carried messy download names (`Shocked (4).png`/`Thinking (5).png`) and I had to fix
   `episode1.html`'s `CHAR_ART.REX` list (~line 466) to the new clean `Shocked`/`Thinking` names or the
   VN would fall back to Neutral. **Selyra done 2026-07-22** — 11 clean transparent poses, zero fixes
   (status card already hyphen-named, all expressions matched, no suffixed files). **Kael done
   2026-07-22** — 12 clean transparent poses, zero fixes. **Voss done 2026-07-22 — ALL SIX CREW
   COMPLETE, this item is CLOSED.** Voss verified clean via saturated-green pixel count (0.07%) vs the
   haloed `dist\build` copies (2–5%), since the preview backdrop was misleading. Historically it was:
   Steve cleaned each and saved
   **straight over the original filenames** (no `_v2`), no swap step needed; **watch two things: (a)
   the status card must be `<Name>-Status.png` with a HYPHEN, and (b) if any filename actually
   changes, update `CHAR_ART.<NAME>` in `episode1.html`.** Also `dist\build\Assets\char\<NAME>\` still
   holds the old halo'd copies — corrected on next build.
2. ~~`Assets/space/Trade_Station.png`~~ — ✅ **done 2026-07-21**, and better than specified: Steve
   supplied **four** station sprites rather than one shared, so `tradeImg` is now keyed by station id
   (`Assets/space/Trade_<id>.png`). No asset gates a built feature any more.
3. ~~**Bounty boss identities**~~ — ✅ **ALL THREE COMPLETE 2026-07-21.** Nothing placeholder is
   left in any of them: each has a name, biography, unique ship, encounter CG, mugshot, codex
   entry and nine voiced lines.
   | id | Target | Ship | Reads as |
   |----|--------|------|----------|
   | `wolfpack` | **Captain Malachar Drax**, "The Red Reaver" | *Blood Crown* + Hound escorts | Grand, calm, ideological — spends other people |
   | `phaserunner` | **Sable Renn**, "The Afterimage" | *Half-Light* | Quiet, tired, apologetic — harms by accident |
   | `siegehauler` | **Harkin Dross**, "The Tollman" | *Tithe* | Courteous, transactional, immovable |

   Drax's identity was supplied by Steve; Sable and Dross were generated here and approved.
   **Generic systems built along the way, which any future boss inherits from its spec:**
   `lines` (start/hp50/hp25/defeat, fired at HP thresholds), `cg` (encounter splash), `portrait`
   (board + codex mugshot, with an optional `portraitCrop`), `banner`, `bio`, `vo` (clip prefix),
   and `BOSS_SHIPS` for unique hulls with a per-hull draw `scale`.
4. ✅ **Mix playtest — ACCEPTED AS-IS by Steve (2026-07-24).** `SFX_VOL` levels + the code-side
   length caps (`SFX_MAXMS`; `ui_select` ~0.9s, `scrap` ~0.5s, `laser` ~3s, `explode` ~5s) are kept as
   the final v0.6 audio mix — no re-balance, no regenerating shorter clips. Closed.
5. ✅ **Packaged 2026-07-22** — `StarGear - Episode 0 - The Ghost Signal - v0.4.zip` built
   (~407 files, ~137 MB; up from 74.6 mostly on clean char art + new VO + station art).
   ⚠️ **The four dock interiors stay PNG, not JPEG** — the iso builds their path dynamically
   (`Assets/${s.name.replace(/ /g,"_")}.png`, [iso_grid_prototype.html:458]), so the build's
   literal `.png→.jpg` rewrite can't reach it; converting them shipped flat-fill dock screens.
   Documented in `build_itch.ps1`; don't re-add them to the JPEG list without a `.jpg` retry
   in the loader. `char/` left at native PNG (needs alpha). Historical note below:
   ⚠️ **This entry used to claim the build script was broken; it wasn't.** Checked properly
   2026-07-21: `START_SCREEN.png` still exists *and* its compression step is guarded by
   `Test-Path`, and `Assets/`+`audio/` are copied **recursively** — so `Start_Menu/`, `ui/`,
   the station backdrops and sprites, the keepers and every new audio folder already ship
   with no script change. What's actually left:
   - bump `$zip` from **v0.3 → v0.4**
   - decide compression on the four dock backdrops (~6.5 MB, opaque, so they belong in the
     JPEG list) and `char/` (37.5 MB, needs alpha so it stays PNG, but could be downscaled)
   - ✅ already fixed while wiring Drax: the png→jpg rewrite now covers **both** html files
     (the iso references `Assets/CG` too and would have pointed at a deleted file), and the
     CG JPEG cap is general rather than CG02-by-name.
   Current zip would land ~80 MB, up from 74.6.
6. ✅ **`DEVLOG-v0.4.md` is current (verified 2026-07-22)** — covers the keepers + VO, all
   three bounty identities, the economy pass (spread, intel, sell-at-profit guard), combat
   barks, Field Manual/tips, menu restructure and the mixer. Ready to post as-is.
7. ~~**Station art**~~ — ✅ **complete 2026-07-21.** 4/4 backdrops, 4/4 space sprites, 4/4 keeper
   portraits, the dock-screen re-layout, and welcome/send-off dialogue for each keeper, all voiced.

**First human playtest happened 2026-07-20** (Steve). It produced the eleven-item defect list
below — nine fixed the same day, **P8 and P10 closed 2026-07-21. All eleven are now done.**
Everything *else* here is still headless-verified only (state probes + screenshots), which
catches crashes and wrong values but not feel.

**A second request batch landed 2026-07-21** — story-carrying saves, downloadable save files,
finite station stock, single-stage bounties, the dock prompt and more. See the
**Session 2026-07-21** table below; all fourteen items are built and Playwright-verified,
none of them human-played.

**`DEVLOG-v0.4.md` is the player-facing release note for the WHOLE v0.3 → v0.4 span**, not
just this playtest pass — that's the economy, trade stations, Ship Config fit-grid, bounty
bosses, side missions, scan, voiced chatter, the SFX layer, save/load and achievements, plus
the fixes below. Everything since the v0.3 zip on 2026-07-18 is unreleased.

---

## Combat chatter — Steve, 2026-07-22

Crew now speak **occasionally during combat**, the in-fight counterpart to exploration `CHATTER`.
Built as `CREW_BARKS` + `crewBarkSay()` / `tickCrewBark()` / `drawCrewBark()` in
`iso_grid_prototype.html`, modelled on the existing chatter and `bossSay` systems.

- **Triggers.** Action barks fire from each crew member's `apply*` handler (Rex's laser/missile
  in `fireCrewWeapon`, Tessa Overclock/Repair, Kael Shield/Scan/Transmission, Astra Move/Hop,
  Selyra Revive/Adrenaline, Voss Tactics). Reactive barks: `kill` (a downed ship the fight
  outlives, at the `combat.pending` resolution), `ally-down` (both knockout sites, spoken by a
  *standing* crewmate), `heavy-hit` (both hull-damage sites, only when the blow is ≥20% of max HP).
- **Cadence.** `CREW_BARK_CHANCE = 0.34` (~1 in 3) with a `CREW_BARK_GAP = 6500ms` cooldown so
  lines never stack; `ally-down` bypasses the roll. Scripted `bossSay` always wins the bar.
- **VO.** New `CREW_BARK_VO` channel out of `audio/Combat/`, wired into `applyAudioMix()` so the
  Voice slider scales it. **All 48 lines recorded and cut (2026-07-22)** — Steve read the six
  per-character masters (`<Name>_Combat.mp3`), cut into `<name>_NN.mp3` by `cut_combat.py`
  (transcribe→align→cut, mirroring the Explore pipeline); every clip verified decoding in-game.
  Full script + delivery notes: `COMBAT_BARK_SCRIPT.md`. Logged as A14 in `ASSETS_NEEDED.md`.
- Verified in Playwright (barks fire on actions, respect cooldown, yield to boss lines, no
  console errors, missing clips fall back to subtitles).

## Playtest defects — Steve, 2026-07-20 (first human playthrough)

Ordered roughly by how cheap the fix looks, not by importance. **P1–P7, P9 and P11 were
fixed and verified in a headless browser** (2026-07-20); **P8 and P10 were both closed
2026-07-21** — P8 by re-cutting the missing takes from the keeper master (no re-recording
needed after all), P10 by the dock-screen re-layout plus all four keeper portraits and their
dialogue. **The playtest list is now fully closed.** What remains is a mix playtest, the
bounty boss identities, the avatar cleanup, and packaging v0.4 — see "Still open" above.

| # | Defect / note | Where | Pri |
|---|---------------|-------|-----|
| P1 | ✅ **ACCEPTED by Steve for v0.4 (2026-07-20).** **Start menu was letterboxed** — vertical bars down the sides. `.sgFrame` used `width:min(100vw, 177.78vh)`, which *fits* the 1376:768 art inside the viewport. Now `max(100vw, 179.17vh)` so it **covers** and crops instead, anchored `top:0` so the overflow falls on the empty nebula at the bottom and never the logo. `#startMenu` moved out of the frame and anchored to the viewport, so cropping can't take the buttons. Verified at 16:9, 21:9 and 5:4. | `episode1.html` | P1 |
| P11 | ✅ **ACCEPTED by Steve for v0.4 (2026-07-20).** **Title background drifted.** The 40s `sgDrift` pan read as a wobble, not parallax. Animation deleted; ship bounce and logo glow kept. | `episode1.html` | P1 |
| P2 | ✅ **Coin/Scrap vanished when the menu opened.** `drawResourceBar()` bailed on `menuOpen`. The *root* menu is a left-hand panel drawn over the undimmed game, so the chip now stays up; sub-views draw a full-screen backdrop and still suppress it. | [iso_grid_prototype.html:2555](iso_grid_prototype.html#L2555) | P1 |
| P3 | ✅ **Last legend entry was cropped** on the Star Map — "unlit = uncharted" sat exactly on the panel's bottom edge. The height formula's constants had drifted from the layout below it (`34/20/14` vs the real `44/22/…`); rewritten term-for-term so adding a row can't clip the footer again. | [`drawMapLegend`](iso_grid_prototype.html#L7137) | P1 |
| P4 | ✅ **No LOAD option on the main menu.** Added **LOAD GAME** to the title, shown only when a slot has something in it. It opens a picker listing all three slots (date, coin, scrap, scans, achievements, position), then fades to black and boots the iso with `load=<n>` on the hash — a new boot hook that calls `loadFromSlot()` after `initWorld()`, and skips the first-flight tutorial. The picker owns the keyboard while up (Esc backs out) so Space can't start a new game behind it. ~~⚠️ A save stores economy/ship/codex/map but no story beat, so loading always resumes in FREE ROAM~~ — **fixed 2026-07-21, see S1**: the snapshot now carries the beat and the title jumps there. | `episode1.html` · [iso boot](iso_grid_prototype.html#L7550) | P0 |
| P5 | ✅ **Scan SFX didn't fire for Kael's combat Scan.** `applyEnemyTarget` now plays the same `sfx("scan")` cue as the free-roam sweep. | [iso_grid_prototype.html:3561](iso_grid_prototype.html#L3561) | P1 |
| P6 | ✅ **Side missions and bounties were visible before you'd taken them.** Jobs now have a **taken** state between "open" and "active": a station board hands you the contract (`accept*`), and the Missions menu decides which one you're actually running (`activate*`) — that's what places the world marker. The SIDE/BOUNTY tabs list only what you've collected, with ↑↓ to select and Enter (or a second click) to make one active; empty tabs point you at a station board. Taking a job while nothing is running still activates it immediately, so a one-job-at-a-time player sees no change. Station boards still list **everything**, marking already-taken ones "◆ IN YOUR LOG" — per Steve, that's how you learn jobs exist. Verified: fresh log empty → take two → only those two listed → switching demotes the old one to "taken", not back to the board. | job state + missions view · station boards | P1 |
| P7 | ✅ **Ship Database was missing enemies.** The three bounty bosses are now dex entries, built from `BOSS_SPECS` rather than hand-listed, so registering a boss adds it automatically — their `dexTactics` strings were already written on every spec and had **no reader at all** before this. Scanning a boss credits its own entry rather than the hull it borrows; escorts still credit their hull. Boss cards show contract facts (threat, hull pattern, payout, last-seen zone) instead of the borrowed hull's stats, which aren't the boss's numbers. ⚠️ **"Know Your Enemy" now needs 10 scans, not 7** — an in-flight save will read 7/10 and the achievement now requires beating all three bounties. Say if you'd rather it stayed at the six hulls + Nexus. Boss art still borrowed until `ASSETS_NEEDED` B5 lands. | `DEX_ENTRIES` · `dbStats` | P1 |
| P8 | ✅ **Kael's voice bug — FIXED 2026-07-21, with no re-recording needed.** Steve: **`Kael_2.mp3` is the keeper** (he deleted `Kael.mp3`). Timestamps pinned the mismatch: 15 of 17 Kael clips were rendered 29/06 20:39 — 20 min after `Kael_2.mp3` was saved — while `kael_02_03.mp3` and `kael_04.mp3` were outliers from 09/07 12:15, rendered from the deleted sample. **The premise that `kael_04` had to be re-rendered was wrong**: transcribing the keeper master shows it *does* contain "Captain...", in fact **three times** (4.06 / 14.98 / 17.94). The 29/06 batch simply missed two of them — the gap before the first is 0.56s where the rest of the take has 0.7s+, so a silence-based split glued it onto the end of "It's an order." (the same failure mode as the Explore files). ✅ Re-cut **both** missing takes from the keeper with ffmpeg: `kael_04.mp3` (4.01–4.33, worried) and a new **`kael_04b.mp3`** (18.17–18.67, elated). ✅ Bonus fix: **"Captain..." appears twice in the episode** — Scene 2 (Worried) and Scene 6 (Excited) — and `VO_MAP` is keyed by `who\|text`, so both beats shared one clip. Scene 6 now carries an inline `vo:` override pointing at `kael_04b`, so each beat gets its own correctly-inflected take. ✅ `kael_02_03` was a *combined* clip for two sentences that already exist separately from the good batch; the script line was split back into two and the file is unreferenced. Both wrong-voice files moved to `audio/Episode0/vo/_retired/` (not deleted — no git here). Verified in Playwright: no page errors, the two beats resolve to different clips, no step anywhere in the episode shares a clip with another, both files load (0.72s / 0.77s). **Voss was never affected** — all 16 Ep0 clips are one batch from `audio/Episode0/Voss.mp3`, and `audio/Explore/` is a single clean batch. ⚠️ **Do not delete the root `Voss.mp3`/`Voss_2.mp3`** — `build_skit1.py`/`build_lines.py` slice Skit 1 out of them by timestamp (`README.md:14`). ☐ Not yet heard by a human. | `audio/Episode0/vo/` · [episode1.html:585](episode1.html#L585) | **P0** |
| P9 | ✅ **Scan yields were wrong.** The coin `cache` type is deleted outright — scanning never pays cash now, so coin stays something you *earn at a station*, per the locked-in economy rule below. Scrap is down from 55% to 30% of finds and the rest are trade-goods crates you still have to sell. Measured across the whole map: **49 goods, 13 scrap, 0 coin** (was roughly 34 scrap / 15 coin / 13 goods). Overall find density (`0.004`) is untouched. | [`poiAt`](iso_grid_prototype.html#L2240) | P1 |
| P10 | ✅ **Station characters — CLOSED 2026-07-21.** All four keepers delivered, wired and verified docked; each has a welcome and a send-off. Details below. Four stations = 4 backdrops + 4 keeper portraits, not one of each. ✅ **Backdrops 4/4 (2026-07-21)** and wired: `drawDockBackdrop` cover-fits `Assets/<Station_Name>.png` under a 0.62 scrim, keyed by station id, falling back to the old flat fill. All four verified docked in a browser. ✅ **Space sprites 4/4** — each station has its own hull in the world now, not a shared one. ✅ **Keeper portraits 4/4 (2026-07-21)** — Marla Quen (Hub) · Oris Vale (Veil Anchorage) · Dova Krezh (Quarry) · Wick (Salvage Reach), generated from the prompts now in `IMAGE_PROMPTS.md` §C2, all correctly transparent waist-up cutouts. ✅ **Welcome + send-off dialogue** per keeper (`KEEPERS`, three greetings and two farewells each, rotating), and ✅ **fully voiced** — all 20 lines cut from four masters by `transcribe_station.py`/`align_station.py`/`cut_station.py`; script in `KEEPER_VO_SCRIPT.md`. Leaving now runs the send-off with the UI cleared away — every exit route (Esc, UNDOCK tab, back button) goes through `requestUndock`, and pressing again during the beat leaves at once. ✅ **Dock screen re-laid-out (2026-07-21).** The diagnosis in `ASSETS_NEEDED.md` was wrong: the scrim was fine, the *panel* was the problem — a **fixed 560px** box whatever was in it, so TRADE (one row) drew a ~480px empty slab across the middle of the art. It's now **content-sized** (`bodyH` from the row count, floor 150 — the tab column is its own stack of chips beside the panel, not inside it, so the panel is free to be shorter). It also **slides to the side opposite the keeper**, who is drawn first so the UI overlaps them. Keeper placement is per-station data on `TRADE_STATIONS` (`side`/`dx`/`scale`/`baseline`) because each room's counter sits differently — Quarry's recedes left, the Hub's open corridor is right. Below ~1000px wide the keeper is dropped rather than squeezing both. Verified with a stand-in figure at 1808×690, 1280×800 and 1000×700, no page errors. ☐ **Portraits 0/4** — prompts now written, see below. | [`keeperLayout`](iso_grid_prototype.html#L6866) · `drawStationView` | P1 |

**Design question falling out of P6 — answered by Steve, 2026-07-20:** the station board
still lists what's available. That's how you learn jobs exist; the hiding applies to the
Missions view and world markers only. Built that way.

⚠️ **P6's two-stage job model was superseded on 2026-07-21** — see S7/S8 below. Accepting a
job or contract now starts it outright. The board-still-lists-everything ruling stands.

---

## Session 2026-07-21 — Steve's requests, all built and verified in Playwright

Verified with `pg.on("pageerror")` clean on both files, plus state probes and screenshots.
Nothing here is human-playtested yet.

| # | Change | Where |
|---|--------|-------|
| S1 | ✅ **Saves carry story position.** `episode1.html` publishes `{beat, bg, freePlay, started}` to shared key **`stargear_story_v1`** on every `runBeat`; `saveSnapshot()` (now `v:2`) folds it in; the title's LOAD **resumes that beat** with its background instead of always dropping into free roam. **This closes the P4 warning.** A save with no `story` block (i.e. pre-today) still loads into free roam, so old saves keep working. | `episode1.html` · `saveSnapshot`/`loadFromSlot` |
| S2 | ✅ **Downloadable save files.** The snapshot JSON exports as `stargear-YYYYMMDD-HHMM.sgsave`. In-game SAVE/LOAD screen: **E** download / **I** import into the highlighted slot, both with on-screen buttons. Title picker: a ⤓ per filled slot and a **Load from file…** button. Imports land in their own slot key `stargear_save_file`, addressed as **`load=f`** on the hash — `SAVE_KEY` accepts `"f"`, and `HAS_LOAD` replaces the old `LOAD_SLOT >= 0` tests (`"f" >= 0` is false — that's the trap). Files are validated on `ax`/`ay` before being stored. | both files |
| S3 | ✅ **LOAD GAME is always on the title**, empty slots or not — otherwise there's no route into file import on a fresh browser. `refreshLoadBtn` no longer hides it. | `episode1.html` |
| S4 | ✅ **Dock prompt.** Coming to rest beside a station raises a Y/N panel modelled on the story prompt (`dockPrompt`/`drawDockPrompt`, E or Y docks, N/Esc declines). Declining re-arms only after you leave the radius; `undock()` sets `dockDeclined` so it can't re-ask the instant you leave the screen. The "press E to dock" pill stays as the way back in. | `iso_grid_prototype.html` |
| S5 | ✅ **Station inventories — markets that can sell out.** Each station holds finite per-commodity stock (`stationStock`, `STOCK_KEY`; baselines 140 producer / 65 par / 35 importer) and price = base × station modifier × `stockFactor` (clamped **0.7–1.5**). Buying and selling walk the price **one unit at a time**, so clearing a shelf costs more per unit and dumping a hold crashes the local price. Shelves drift back to baseline at `RESTOCK_MS_PER_UNIT` 18s, applied on dock and while the market is open. Stock travels in the save. **Tuning is measured, not guessed:** 40-unit ore runs pay **218 → 120 → 93 → 40 → sold out**. An earlier 0.45 floor made repeat runs a *loss*, which punishes engaging with the system — **don't go back to it**; profit should decay to zero, never below. | `goodsPrice`/`buyGoods`/`sellGoods` |
| S6 | ✅ **Bounties are single-stage.** Accepting sets state **`accepted`** and every accepted contract is marked in the world **and** on the Star Map at once; flying to any mark starts that fight. `acceptedBounties()` drives all three (trigger, world marks, map marks). `normalizeBounties()` migrates old `taken`/`active` saves on load. | bounty block · `drawBountyMarker` · `drawMapView` |
| S7 | ✅ **Accepting a side mission starts it** — no separate "make active" step. | `acceptSide` |
| S8 | ✅ **Collection objectives show progress.** Steps may carry an optional `prog() → {have, need}`; the live step renders a **17 / 40** tally in the Missions checklist and on the station job board. Added to the four countable steps. | `stepProgressText` |
| S9 | ✅ **Scan scrap rate 30% → 12%** (Steve: still too often), amounts 3–11 (was 4–17). Density `0.004` untouched. | `poiAt` |
| S10 | ✅ **A hull is scanned once, forever.** `isScanned(e)` treats any ship whose type is in the codex as scanned, and scanning one marks the rest of that type on the field. Kael's Scan is now for new hulls only. | `isScanned` |
| S11 | ✅ **Know Your Enemy fixed at 10** (`KNOW_YOUR_ENEMY_TARGET`), not `DEX_ENTRIES.length` — Steve's ruling on the P7 question: more enemy hulls are coming with the bounty ships, so 10 is the finished roster's target. **⚠️ Superseded the same day by N6** — the bounty hulls landed as four codex cards, so the roster is 11 and the target tracks `DEX_ENTRIES.length` again. | `ACHIEVEMENTS` |
| S12 | ✅ **HUD chip splits SCRAP and CARGO onto their own lines** under HOLD (was a combined `SCRAP/CARGO 0 / 6` row). **⚠️ Superseded by R1** — Steve didn't want the breakdown; the chip is back to two fixed rows, SCRAP and COIN. | `drawResourceBar` |
| S13 | ✅ **Cargo module wording** — "Capacity to hold 30 more scrap." on all three hold modules and the generated blurb. ⚠️ Note the hold is shared: goods eat the same capacity, so a Cargo Pod also buys 15 units of ore. The text names scrap only, per Steve. | `SHIP_MODULES` · `moduleBlurb` |
| S14 | ✅ **Scene 1 opens on the empty bridge** for **1.5s** — no cast, no dialogue box — before Astra appears. The 1.5s covers `fadeBlack`'s 0.5s fade-in, leaving ~1s of clear background. New `{pause, quiet}` step flag; `doPause(ms, quiet)` hides `bar` and `clearPause` restores it, so skipping the hold with Space also restores it. | `episode1.html` EP1 beat 0 |

**Open questions from this session:** none outstanding — but S5's numbers and S14's hold
length are feel calls that want a human playthrough before the v0.4 build.

## Station polish — Steve, 2026-07-21 (after seeing the keepers in-game)

| # | Change | Where |
|---|--------|-------|
| T1 | ✅ **The old "⏵ DOCK AT …" pill is gone.** Arriving already raises its own Y/N prompt, so two things were asking the same question. `drawDockHint`/`_dockHitRect` and the click handler are deleted. **E still docks while you're alongside**, which is what stops a declined prompt from meaning a lap of the station before you can change your mind. | `drawDockHint` removed |
| T2 | ✅ **Keepers no longer cut off square at the waist.** The art is cut flat, which read as a hard edge floating over the counter. Each keeper is now pre-rendered once with the bottom **20% dissolved to transparent** (`keeperFaded`, cached per station), and sunk by half that band so the dissolve straddles the counter line instead of ending above it. The speech panel stays anchored to the true counter line (`kp.base`), not the faded hem. | `keeperFaded` · `keeperLayout` |
| T3 | ✅ **UNDOCK appeared twice** — as a tab and as the top-left button. Steve prefers the top one because it reads as *back* rather than a seventh thing to trade with. The tab is removed from `STATION_TABS` along with its row; the button and Esc are the two ways out. | `STATION_TABS` · `stationRows` |
| T5 | ✅ **The greeting waits a beat.** Docking used to fire the keeper's line on the same frame as the screen. Now `keeperPending = {id, at}` holds it for `KEEPER_GREET_DELAY` **1000ms**, so the dock clunk and the room land first and the keeper reads as speaking *to* you rather than over your arrival. Leaving during the silent beat cancels it, so a quick in-and-out can't fire a greeting after the goodbye. | `dockAt` · `tickKeeper` |
| T6 | ✅ **Dock radius widened**, `DOCK_DIST` 3 → **4.5** tiles. At 3 you could slide past a station without it ever offering, which reads as the station being broken rather than missed. Verified: offered at 3 and 4 tiles, not at 5. | `DOCK_DIST` |
| T7 | ✅ **Waypoint Hub moved off the doorstep**, (6,8) → **(0,-36)**. ⚠️ **The tile grid is not the visibility bound** — objects render well outside the 13×13 window, so the first attempt at (0,18) still drew on screen at spawn despite being "off-grid". Measured with the game's own `worldToScreen`: 36 tiles is the nearest distance hidden at every aspect from 1366×768 to 1920×1080, and it's also just outside `MINIMAP_R` (34), so the radar opens empty too. Still by far the nearest station (others ~54) at ~11s of cruise, in OPEN space with 7.7 tiles of pocket clearance, and out toward the first story objective so you meet it en route. Verified: nothing on screen or minimap at spawn on four aspects; arriving still offers the dock. | `TRADE_STATIONS` |
| T8 | ✅ **SIDE and BOUNTY tabs no longer carry a `0/3` counter.** The Missions tab strip read `SIDE 0/3` / `BOUNTY 0/3`, which framed both as checklists to clear. Labels are now plain. **AWARDS keeps its `x/y`** — that one really is a collection tracker. `ep0.sidesDone/sidesTotal` and `bountiesDone/bountiesTotal` still update (achievements read them); only the label draw changed. | `drawMissionTabs` |
| T9 | ✅ **Station rows size themselves to their text — bounty briefs were being cut off.** Rows were a fixed 76px with room for exactly two sub-lines, the second ellipsized, so a ~240-char bounty brief lost its last half (including "Wanted alive or dead") and you couldn't read the contract you were accepting. Now the blurbs are **wrapped before the rows are laid out** and `rowH` is sized to the longest one on that board; every wrapped line draws. ⚠️ The mugshot was `rowH - 16`, which would have grown the portrait with the row — it's a fixed `ROW_MUG` 60 now. Wrap width and draw width come from one shared `stationRowTextW()` so they can't disagree; note it leaves the font set to the label's 15px, so the caller resets to 11px before wrapping. Verified in Playwright at 1600×900 and 1366×768: all three briefs read in full, other tabs unchanged, no page errors. | `drawStation` · `stationRowTextW` |
| T4 | ✅ **Bug found while testing T1–T3:** the send-off beat was re-timed from *when the clip's metadata arrived* rather than when the line started, so a cold-loaded clip dragged the goodbye well past the audio (measured 3821ms of beat for a 2.59s clip). Now anchored to `keeperSay.startedAt`. Verified cold and warm: 3.37s clip → 3821ms, 2.59s clip → 3035ms. | `keeperLine` sync |

## Drax fight polish — Steve, 2026-07-21 (first look at the Wolfpack fight)

| # | Change | Where |
|---|--------|-------|
| D1 | ✅ **Boss ships faced the wrong way.** Boss parts are stationary, so nothing ever set their facing — they sat on the spawn default (FWD/NE) with their backs to you all fight. Regular enemies get a facing from moving and firing. `faceBossPartsAtPlayer()` now turns every boss ship toward the player each frame (skipped mid-glide so a blink still settles on its own end facing). Affected the Blood Crown too; it was just less obvious than a Hound with a glowing lance on its nose. | `faceBossPartsAtPlayer` |
| D2 | ✅ **Escorts respawned too fast.** `WOLFPACK.callEvery` 3 → **5** boss turns. At 3 the window where the flagship is actually exposed barely existed, which undercut the whole burst-race idea. | `WOLFPACK` |
| D3 | ✅ **Scanned Hounds didn't stay scanned.** Scanning credited the hull correctly, but `isScanned()` asked a different question for boss parts — whether the *contract* (`wolfpack`) was scanned — so every fresh escort read as unknown. Boss parts other than the core now identify by their own hull. | `isScanned` |
| D4 | ✅ **Bug found while fixing D3:** scanning any escort called `discoverShip(bossDexId())`, so a throwaway Hound unlocked **Drax's own codex card** and ticked "Know Your Enemy" without ever identifying the flagship. Only `part === "core"` credits the contract now. | `applyEnemyTarget` |
| D6 | ✅ **Bounty mugshot is head-and-shoulders**, not a shrunken whole figure. `drawMugshot()` takes a source-rect crop out of the full-body portrait, tunable per character via a spec `portraitCrop` ({cx, top, h} as fractions of the art) so a differently-framed portrait needs no new art. | `drawMugshot` |
| D7 | ✅ **The encounter CG now opens the fight** instead of following the name banner. ⚠️ **First attempt silently failed**: it required `_cgImg.complete` on the frame combat starts, and at 7552px / 40 MB the art hasn't decoded yet, so it fell through to the old path. Declaring `cg` is now enough — the banner is held, the splash goes up the moment the image is ready, and after 6s of waiting it gives up and plays the banner as normal. The held name card is released as the CG fades. | `startCombat` · `tickCombat` |
| D8 | ✅ **Boss dialogue uses a VN-style bar**, not a HUD pill: wide, bottom-anchored, dark panel with an accent spine and the speaker's name above the line. Full width over the CG; narrowed and left-anchored in the arena so it clears the crew panel. | `drawBossSay` |
| D9 | ✅ **Regression caught by the final smoke test:** giving each boss its own `banner` left the other three falling back to a bare "COMBAT!", so the **Nexus lost its "THE NEXUS AWAKENS" card**. The fallback is now the spec's own `name` uppercased, and the Nexus sets its banner explicitly. All four verified: THE RED REAVER / THE PHASE RUNNER / THE SIEGE HAULER / THE NEXUS AWAKENS. | `startCombat` |
| D5 | ✅ **Scrap/coin chip hidden in combat.** The hold is an exploration concern and the battle HUD is busy enough. Salvage still announces itself with its `+N SCRAP` floater. | `drawResourceBar` |

## Menu + defeat batch — Steve, 2026-07-21

| # | Change | Where |
|---|--------|-------|
| M1 | ✅ **Losing a fight costs cargo** — see the locked design answer below. `loseCargoOnDefeat()` takes 30–50% of scrap and every trade good, one fraction for the whole hold, minimum 1 unit of anything you're carrying. Coin untouched. Reported in the combat log and as a `-N% CARGO` floater. Verified over 300 rolls: fraction always 30–50, coin never moved, empty hold is a no-op, and a single relic is still taken. | `loseCargoOnDefeat` |
| M2 | ✅ **Cargo added to the pause menu** — itemised manifest with a capacity bar, per-commodity quantities and rough base value, plus coin listed separately as "banked — not in the hold". The HUD chip only shows totals and is now hidden in combat and at stations, so this is where you read the manifest. | `drawCargoView` |
| M3 | ✅ **Sound levels in Options** — **Master · Voice · Music · Effects**, persisted in `stargear_audio_v1`. They're **multipliers over the existing hand-tuned mix** (`BGM.vol`, `SFX_VOL`, each VO channel's own `vol`), so the relative balance is preserved and the sliders only scale it; Master multiplies all three. ↑↓ picks a row, ←→ adjusts in 5% steps, or click anywhere on a bar. `applyAudioMix()` retunes anything already playing so a drag is audible immediately. | `audioMix` · `drawOptionsView` |

## Menu restructure + ship database — Steve, 2026-07-21 (evening)

Steve: *"the menu is getting crowded"*. All verified in Playwright at 1280×900 with
`pageerror` clean and screenshots of every screen touched. Not human-playtested.

| # | Change | Where |
|---|--------|-------|
| N1 | ✅ **Root menu cut 9 entries → 7**, in Steve's order: **Star Map · Ship · Crew · Missions · Ship Database · Save / Load · Options**. Ship Database was missing from the order he gave; he chose to keep it in the root menu above Save/Load rather than bury it as a tab. | `MENU_ITEMS` |
| N2 | ✅ **"Ship Config" → "Ship", with tabs: CONFIGURATION · CARGO.** Cargo is no longer a root entry. One `menuView` (`"shipConfig"`) with a `shipTab` — the tab strip is `drawShipTabs`, modelled on `drawMissionTabs`, and the CARGO tab label carries the live hold count (`CARGO 0/70`). Dropping the old "SHIP CONFIG" heading freed exactly the space the strip needed, so the fit-grid layout is untouched. | `SHIP_TABS` · `drawShipView` |
| N3 | ✅ **Achievements folded into Missions as a fourth tab, AWARDS `x/y`.** The root entry is gone and the standalone `menuView === "achievements"` branches (draw, key, click) are deleted — `drawAchievementsView` is now only reached from `missionTab === 3`. Its `y = 54` already cleared the tab strip, so the panel needed no relayout. `checkAchievements()` runs on opening Missions and on every tab change. | `MISSION_TABS` · `drawMissionsView` |
| N4 | ⚠️ **Tab keys collide with the fit-grid.** In Ship, ←/→ switch tabs **only when no module ghost is held** — while placing, the arrows drive the grid cursor. **Tab** always switches. Clicking a tab drops a held ghost first, and grid clicks are ignored while CARGO is up (`_scfgGrid`'s hit rects are stale there). Don't "simplify" this by making ←/→ unconditional. | `handleMenuKey` · `handleMenuClick` |
| N5 | ✅ **The Ship Database shows SHIPS, not faces.** Bounty cards were built from `BOSS_SPECS` and drew `spec._portraitImg`, so the codex silhouettes were *people*. Boss cards are now built from **`BOSS_SHIPS`** (the hull list) — so **Drax's wolfpack is two entries, Blood Crown and Hound**, per Steve. 11 cards: 6 patrol hulls + Nexus + Blood Crown / Hound / Half-Light / Tithe. Named hulls get the ordinary stat block from their profile (the numbers already matched the fight: `SHIP_PROFILES["Blood Crown"].hp` 26 = `WOLFPACK.coreHp`), then *Flown by* / *Contract* / *Last seen*; the Hound gets *Wing of* and no bounty of its own. Drax's biography stays as KNOWN HISTORY on the flagship card, which grew 470 → **540px** to fit stats + bio, with tactics clamped to 4 lines so it can't run into the history strip. ⚠️ **A future boss on a *common* hull now adds no card** — that hull is already in the database. If a new bounty should appear in the codex it needs a unique hull in `BOSS_SHIPS`. | `DEX_ENTRIES` · `BOSS_HULL_DEX` · `dbStats` |
| N5a | ✅ **Dex ids moved from contract to hull.** `bossDexId()` returns the spec's `shipName` (`"Blood Crown"`), which is the id its escorts' hull scan already used; only the Nexus keeps `"Nexus"`. `migrateDex()` translates pre-existing saves (`wolfpack`→`Blood Crown`, `phaserunner`→`Half-Light`, `siegehauler`→`Tithe`) on both the localStorage and slot paths, **and drops ids matching no card** — otherwise a stale id inflates `shipDex.size` forever. | `bossDexId` · `migrateDex` |
| N6 | ✅ **Know Your Enemy is `DEX_ENTRIES.length` (11)** and its description builds from the constant. Steve: *"Know your enemy is now 11 ships"*. Reverses S11 — the hulls S11 was holding a slot for have arrived. ⚠️ Two consequences: **the Nexus counts**, so 100% is finale-gated, and **a Hound must be scanned**, which only happens inside the Red Reaver fight. Flagged to Steve; no ruling yet. | `KNOW_YOUR_ENEMY_TARGET` |
| N7 | ✅ Ammo-less hulls (Hound, Half-Light, Tithe) read **"Missiles — None"** instead of `3 dmg × 0`. | `dbStats` |

## Onboarding — Steve, 2026-07-21 (evening)

Steve: *"the two tutorials we have are out of date, and were basic"*. The game had exactly
two pop-ups (`explore`, `combat`) written when it was flight + a fight — nothing about
scanning, docking, cargo, modules, missions or bounties, and no way to look anything up
again once dismissed. Verified in Playwright at 1280×720 **and** 1000×600, `pageerror`
clean, every tip trigger and every manual chapter screenshotted.

| # | Change | Where |
|---|--------|-------|
| O1 | ✅ **FIELD MANUAL — a browsable reference in the root menu**, 9 chapters: Flight · Scanning & Star Map · Docking & Trade · Cargo/Scrap/Coin · Modules & Power · Crew & Abilities · Combat · Missions/Jobs/Bounties · Saving & Progress. Content lives in one `MANUAL` array; a chapter line is a paragraph string, a `{ h }` sub-heading or a `{ k, t }` key row, and `manualPageLayout()` measures all three so a page **scrolls** (↑↓ / PageUp-Dn / wheel, with a rail) rather than overrunning. Index/page pair modelled on the Ship Database views. New `book` menu icon so it doesn't reuse Missions' warning triangle. | `MANUAL` · `drawManualView` · `drawManualPageView` |
| O2 | ✅ **Ten contextual first-time tips, up from two.** `tutContent()`'s if-chain became a `TIPS` table: `explore` (reworded — now covers F and E), `scan`, `dock`, `cargo`, `modules`, `missions`, `combat` (trimmed), `combatTarget`, `combatOut`, `defeat`. Seen-keys bumped to `_v3` so the two reworded ones show once more. A tip raised while another is up **queues** instead of being dropped. | `TIPS` · `showTutorial` |
| O3 | ✅ **Combat tips staged rather than one wall of text.** The single COMBAT pop-up now covers only the core loop; facing/range fires from `beginAction` the first time you aim, end-of-turn from `spendAction` when the count hits 0, and what a loss costs fires from `tickCombat` **after** the wreck banner plays out (not from `loseCombat`, which would cover the explosion). | `beginAction` · `spendAction` · `tickCombat` |
| O4 | ✅ **Options → Tutorial Tips ON/OFF**, persisted in `stargear_tips_v1`. `showTutorial` early-outs when off, running the caller's `onClose` so nothing that chains off a tip can stall. The Field Manual is unaffected by the toggle. Both toggle rows now come from one `toggleRow()` helper; panel 430→412px. | `tipsOn` · `drawOptionsView` |
| O5 | ✅ **Root menu rows size to the visible height** — at 8 entries a fixed 56px row overflowed a short window. Also: HUD strip retitled StarGear and now lists **F** and **E**, which it never did. | `drawMenu` |
| O6 | ⚠️ **The cargo tip rides `_holdFullNoted`**, which `tickChatter` only services outside combat/menus — so it lands after the fight, alongside the crew's "hold full" line, not mid-battle. `doScan` now sets the same flag when a sweep leaves salvage behind. Don't move the tip to the pickup site or it'll fire over the arena. | `tickChatter` · `doScan` |

## Ability switching wasn't discoverable — Steve, 2026-07-21 (playtest feedback)

Feedback: *"it wasn't clear that you switch abilities"*. This is the second time it's come
up (Brett's v0.2 list said "swap onboarding" too). **All six crew have exactly two
abilities** — the swap isn't a corner feature, it's half the combat system, and four
things were burying it. Steve chose tips **plus** the menu reorder. Verified in Playwright,
`pageerror` clean.

| # | Change | Where |
|---|--------|-------|
| A1 | ✅ **⇄ Switch Action moved above the locked-slot rows.** It was drawn *last*, under "Slot 2 — Locked" and "Slot 3 — Locked", so it read as more locked content; it now sits directly under the ability it swaps. One line reordered in `actionPickRows`. ⚠️ Don't "tidy" the root rows back into slot order — the padlocks are what made this invisible. | `actionPickRows` |
| A2 | ✅ **`switch` tip** — fires the first time a crew action menu opens in battle, with that menu visible behind it. States the rule (two abilities each, with examples), the cost asymmetry (**in battle it costs the turn, from Menu → Crew it's free**), and that the greyed Slot 2/3 rows are a *different* thing. | `TIPS.switch` · `activateCrew` |
| A3 | ✅ **`crewSlot` tip** — fires on first opening a crew character sheet, the place a loadout is set for free. Both routes in (Enter on the roster, clicking a portrait) now go through a shared **`openCrewChar()`** so the tip can't be reached by only one of them. | `openCrewChar` |
| A4 | ✅ **Manual chapter 6 rewritten around it** — subtitle is now *"Two abilities each — choosing between them is the game"*, and the chapter leads with a table of all six pairs (Astra Maneuver/Space Hop, Rex Lasers/Missile, …). Chapter 7 gained a THE ACTION MENU section describing the row order and the cost. The core `combat` tip now says "every crew member carries two abilities" instead of the old "each crew member has their own abilities", which was exactly the phrasing that let people assume they were fixed. | `MANUAL` · `TIPS.combat` |
| A5 | ✅ **Crew sheet: the `1 / 2` counter moved inside the ⇄ SWAP chip** (`⇄ SWAP 1/2`, chip 96→116px). It had been drawn below the chip, landing on the ability description. Wrapping the description away from it instead just ellipsized it, so the chip absorbed the count. | `drawCrewCharView` |
| A6 | ⚠️ **Still open: `activateCrew` fires immediately when only one option is available** ([the `crewAvailableIdxs(c).length <= 1` early-out]), so a crew member with a dead module skips the menu entirely and teaches "clicking a crew just shoots". Steve declined always-open-the-menu because it costs a click on every routine turn. If the feedback recurs, that's the next lever. | `activateCrew` |

## HUD chip trimmed to SCRAP + COIN — Steve, 2026-07-21 (evening)

Steve, on the three-line HOLD / SCRAP / CARGO / COIN chip: *"I don't like this breakdown.
I only want to see scrap and coin"*. Not verified in Playwright yet.

| # | Change | Where |
|---|--------|-------|
| R1 | ✅ **The chip is two fixed rows again: SCRAP `n / cap` + bar, then COIN.** The HOLD relabel, the CARGO line and the variable height are gone — `h` is a constant 52 instead of `goods ? 84 : 52`, so the chip no longer grows when you pick up trade goods. The top number is **scrap alone**, not hold-used. | `drawResourceBar` |
| R2 | ⚠️ **The bar still shows the whole hold** — scrap green, trade goods grey on top — so it can read fuller than the SCRAP number explains. That's deliberate: with no CARGO line, the grey segment is the *only* on-screen sign that ore is eating your salvage room, and "hold full, pickups stopping" has to stay legible. Don't drop the second segment without giving that warning somewhere else. The itemised manifest is Menu → Ship → CARGO (`drawCargoView`, unchanged). | `drawResourceBar` |

## Station economy pass — Steve, 2026-07-21 (evening)

Steve: *"Take a look at the economy between the space stations. I want the player to be
encouraged to buy stock in one place, and sell it another for a profit, without creating
an infinite money glitch."* All built and verified in Playwright (`errors: []`), plus a
standalone property simulation.

**There WAS a working infinite money glitch, and it needed no travel and no risk.**
`buyGoods` and `sellGoods` both priced off one `goodsPrice()`. A buy paid each price
*before* its stock decrement; a sell collected each price *after*. So buying N and
immediately selling N back **at the same station** returned the whole price ladder one
rung higher than you paid — net always ≥ 0 (**+44 coin a cycle** on relics at Salvage
Reach), stock left exactly where it started, repeatable forever standing still, and it
scaled with capital.

| # | Change | Where |
|---|--------|-------|
| E1 | ✅ **`TRADE_SPREAD` 0.85 — stations buy for less than they sell.** `goodsPrice` split into `goodsBuyPrice` / `goodsSellPrice` (the old name survives as a buy-side alias). This is the fix: every same-station round trip goes from +1…+44 to −39…−787, so the *only* source of margin is the difference between two stations — exactly the loop Steve wants encouraged. **Do not remove.** | `iso_grid_prototype.html` |
| E2 | ✅ **Shelf depth is flat — `STOCK_DEPTH` 200 for everything.** It used to vary with the price modifier (140 / 65 / **35**), so an importer's shelf was *shallower than the 40-unit hold*: one trade inverted the local market and run 2 of any route was already a loss. Regional flavour belongs in `STATION_PRICES`; doubling it up in the depth just broke the curve. Depth is now ~5× the hold, so a full load moves price a visible ~11%. | `baseStock` |
| E3 | ⚠️ **The scarcity clamp is deliberately WIDE (0.55–1.60).** Tightening it *looks* like the way to tame repeat-run grinding and does the opposite: if glut and scarcity can't fully cancel the two stations' modifiers, the arbitrage never closes and the route settles on a **permanent** floor — a tight 0.85–1.15 clamp left neb→armada relics paying **+960 a run, forever**. Don't narrow it. | `stockFactor`, `STOCK_SWING/LO/HI` |
| E4 | ✅ **Cost basis + sell-at-profit guard.** `econ.basis[id]` = average coin/unit paid, rolled forward on each buy, dropped when the last unit leaves. `sellGoods(sid, id, all)` stops when the next unit would fetch less than you paid; `sellableAtProfit()` sizes the row. A crashed market *may* price below your cost — the game just never makes you eat it. Dumping the lot stays available as a separate, explicitly-priced "Dump all" row. Under this guard the old exploit sells **0 units** — it isn't merely unprofitable, it's inexpressible. | `buyGoods`, `sellGoods` |
| E5 | ✅ **Per-commodity restock** (`COMMODITIES[].restock`, seconds/unit: ore 8 · parts 14 · meds 24 · relics 40), replacing one global `RESTOCK_MS_PER_UNIT` 18s. **This is the master dial on long-run inflation** — sustainable income on any route is exactly `restock rate × margin/unit`. A flat rate made relics worth ~150 coin/min sustained against ore's ~20, so nothing else was worth carrying; now every good sustains 40–72 coin/min. The drift clock is per-commodity (`stockTouched[station][commodity]`, migrates from the old single number). | `touchStock` |
| E6 | ✅ **Market intel — the "encourage" half.** Nothing used to tell you where to *sell*; the screen only described the station you stood in, so the loop was invisible without notes. Docking now records that station's prices (`marketIntel`, `stargear_intel_v1`), and each MARKET row carries a third line: *"▸ Veil Anchorage pays 14 each · +6 a unit · seen just now · 55 tiles NW"*, or "no price data", or "no known buyer above N". The CARGO manifest shows the best known market per held good. **Deliberately not live** — the staleness is the reason to go and look. | `recordIntel`, `bestKnownMarket`, `stationRows`, `drawCargoView` |
| E7 | ✅ **`START_COIN` 250 on a fresh game.** Starting on 0 coin put the market out of reach until you'd fought and sold scrap, so a first session often never saw the trade loop. ~2 lots of ore: enough to learn it, not enough to skip earning it. | fresh-game boot branch |
| E8 | ✅ `wrapLines` honours an explicit `\n` (the intel line has to sit on its own row, not wherever the wrap lands). `stockHint` thresholds retuned to the deviation the price actually reacts to. `drawCargoView`'s quantity column is measured off the note instead of a fixed 120px inset — the longer market hint ran straight over the number. | various |

**Measured result** (moon→neb ore, consecutive runs, no restock): **+231 → +127 → +28 → 0**,
then flat. Decays to nothing, never negative, no permanent floor. Same-station cycles:
**0 units sold, coin only ever falls.** Save/load carries `econ.basis` and `marketIntel`
(snapshot `v:3`); a fresh game wipes both and grants exactly 250 coin.

⚠️ **`recordIntel` runs every frame the market is on screen** — it only writes localStorage
when a price actually moved. Don't make it persist unconditionally.

**Both tests live at the project root and should be re-run after any market tuning:**
`python econ_sim.py` (pure maths, no browser — asserts the three properties above) and
`python verify_econ.py` (drives the real file in Playwright — asserts no page errors, that
buy/sell cycling can't gain coin, the route decay curve, and that basis/intel survive
save+load). ⚠️ `econ_sim.py` **duplicates the constants** from the `TRADE COMMODITIES` block,
so change both together or the sim will be validating a market the game doesn't have.

**Not yet played by a human.**

## Design answers already locked in
- **Core loop** — explore space → combat / dock at station → back to space.
- **Trade margin comes from the difference between two stations, never from one.**
  Stations buy at `TRADE_SPREAD` (0.85) of what they sell, so a buy-then-sell-back at the
  same station is always a loss. This is what stops the money printer — don't remove it.
- **A route decays to zero and stops there; it never punishes you.** Repeating a run pays
  less each time until it's worth nothing. Selling refuses to go below what you paid unless
  you explicitly choose "Dump all". (Supersedes nothing — it's the mechanism that finally
  delivers the older "don't make repeat runs a loss" rule.)
- **Scrap** = raw pickup. **Coin** = money. Scrap converts to coin *only* by selling at a station.
- **Scrap capacity** — at capacity, pickups simply stop (forces a station run). Nothing is bumped.
- **Repairs and module purchases** are paid in **coin**.
- **Scrap auto-collects** on kill (no flying over drops).
- **Ship parts = the same module system** as the Ship Config grid — varying shapes/sizes (RoF-style).
- **Module breakage** happens after a **loss**, not a win. *Which* modules break is **random**.
  A broken module **still occupies its grid slot** but its **effect is inactive**.
- **Losing a fight also costs cargo** (Steve, 2026-07-21): whoever broke you off takes
  **30–50%** of the hold — scrap *and* trade goods. One fraction is rolled for the whole hold
  so it reads as "they took a third of everything", and any cargo at all loses at least 1 unit.
  `LOOT_LOSS_MIN`/`MAX` are the tunables.
- **Coin is NEVER taken on defeat** — confirmed by Steve 2026-07-21. It isn't in the hold;
  coin is what you've already banked at a station. Only cargo is lootable.
- **Mission/story losses are not exempt** — confirmed by Steve 2026-07-21. A restaged story
  fight strips resources and breaks modules exactly like any other loss. The cargo loss is
  geometric so repeated attempts can never zero the hold, and a mandatory fight costing you
  something each time you fail is the intent. **No special case; don't add one.**
- **Pirate Bounties** = kill target X for coin. **Side Missions** = multi-step / story-flavoured.
- **Points of interest** (scan) — TBD.
- **Achievements** — triggers TBD, Steve has some in mind.

---

## Visual
- ✅ **Dynamic Start Menu** — layered animated title promoted into `episode1.html`, with
  fade-to-black on Start. **Revised and signed off for v0.4 (Steve, 2026-07-20):** full-bleed
  at any aspect ratio (cover, not fit, anchored top so the logo never crops), a **still**
  background (the drift pan was cut — it read as a wobble), buttons anchored to the viewport
  rather than the art frame, and **LOAD GAME** beside Start when a save exists. Ship bounce and
  logo glow are the only motion. **Treat this as the locked v0.4 title screen** — don't
  re-litigate the framing or re-add the drift without Steve asking.
- ✅ **Clean up avatars** — **ALL 6 crew done 2026-07-22** (Astra, Tessa, Rex, Selyra, Kael, Voss —
  green matte halo removed, poses cleaned and saved over original filenames). See the itemized note
  under "Still open" #1 at the top of this file for the per-character detail and verification method.
- ✅ **Mini-map** — corner radar (bottom-right), local charted space + hostiles + objective, free-roam only.

## Battle
- ✅ **Different enemy attack visuals** — each hull now has a signature shot you can read without
  checking the log (`ENEMY_FX` + the style renderer in `drawShots`):
  **Cyclops** pale-blue *lance* (thin, precise, hot muzzle) · **Dread** red *twin* beams ·
  **Gunner** the orange baseline *beam* · **Neo** violet *scatter* burst · **Tank** heavy amber
  *pulse* (dashed slug) · **Wing** fast thin green *twin*. Missiles keep the shared bolt but take the
  hull's colour. All procedural — no art needed.
- ✅ **Enemy sound fx** — and combat SFX generally (Brett's #1). Built the whole playback layer:
  `sfx(name, gain)` with pooled `Audio` elements and per-cue levels (`SFX_VOL`), hooked into every
  shot, hit, shield-absorb, **miss**, explosion, scan, salvage pickup, sale and dock. A missing file
  is a silent no-op, so it degrades cleanly. All 12 audio files are delivered and load correctly.
  See `AUDIO_PROMPTS.md` for the hook table — **and the note that `laser.mp3` (~3s) and
  `explode.mp3` (~5s) came back far longer than specified**; capped in code via `SFX_MAXMS`, but
  worth regenerating short.
- ✅ **Defeated enemies = scrap** — auto-collects on the kill, capped by cargo capacity, with a
  `+N SCRAP` / `HOLD FULL` floater. Payout per hull is `SHIP_PROFILES[x].scrap`.

## Ship
- ◐ **Config grid** — RoF-style module fit-grid in `iso_grid_prototype.html`. Now also shows
  **BROKEN** parts (red slash, slot still occupied).
- ✅ **Ship parts — DONE v0.6 (2026-07-24).** 6 new modules giving all 6 crew grid presence: 4 free
  gate modules (Voss Tactics/Transmission, Tessa Overclock, Selyra Adrenaline) + 2 bought enhancers
  (Repair Bay, Med Bay — `boosts` Repair/Heal). See `DEVLOG-v0.6.md`.
- ✅ **Capacity to hold scrap** — `CARGO_BASE` 40 + a fitted **Cargo Hold** module (+30). At
  capacity pickups stop.

## Win/Lose
- ☐ **After boss fight return to space.** *(Now covered by free play — see below. Confirm that's what you meant.)*
- ✅ **Lose → return to space, 1–2 ship modules broken.** Free-roam losses are survivable: the
  StarGear breaks off, `breakRandomModules(1–2)` wrecks random non-core parts, and you limp away.
  **Story/mission losses are still a game over** (the episode's DEFEAT screen) — confirm if you'd
  rather those were survivable too.
- ✅ **Post-story free play** — the ending screen now has **◀ RETURN TO THE SECTOR**, which drops
  you back into free-roam with all progress intact for optional content.

## Space stations
**Built.** A new `OBJ.TRADE` object type — four hand-placed, manned stations (`TRADE_STATIONS`):
**Waypoint Hub** (0,-36 — moved out from the start 2026-07-21 so nothing sits on the doorstep on load) · **Veil Anchorage** (-30,-46) · **Quarry Station** (44,-30) ·
**Salvage Reach** (30,46). Fly within 3 tiles → a **DOCK** prompt (press **E** or click; `D` was taken
by "move right") → the dock screen, with tabs down the left. Stations always show on the Star Map and
mini-map, charted or not, so the economy loop is always findable. **Art delivered 2026-07-21:** each
station has its **own** sprite (`Assets/space/Trade_<id>.png`) and its **own** painted dock interior
(`Assets/<Station_Name>.png`) — the Hub is a tidy brass ring station, Veil Anchorage a violet
patchwork on an asteroid anchor, Quarry an ore platform with a glowing crusher, Salvage Reach a
cannibalised warship hull. The procedural ring-station survives as a per-station fallback.

- ✅ **Sell scrap for coin** — TRADE tab, `SCRAP_PRICE` 3 coin/unit.
- ✅ **Repair broken ship modules** — REPAIR tab, cost scales with module size (`repairCost`, min 40).
  The tab carries a badge with the number of broken modules.
- ✅ **Buy new ship modules** — MODULES tab. Introduced **module ownership** (`shipOwned`), separate
  from *installed*: Ship Config now only lists what you own, and the shop sells what you don't.
  Starting stock: **Cargo Pod** (+15 cargo, 220), **Expanded Hold** (+45, 480), **Armour Plating**
  (+6 max hull, 320 — wired through the new `playerMaxHp()`).
- ❌ **Sell ship modules** — REMOVED 2026-07-26 at Steve's request (see the playtest session below).
  `sellbackValue`/`stationSoldMods` and the "Sell <module>" row are gone; buying and fitting stand.
- ✅ **Buy/sell resources for trade** — MARKET tab. Four commodities (Raw Ore 12 · Machine Parts 30 ·
  Medical Supplies 55 · Nebula Relics 90) with **per-station price multipliers** (`STATION_PRICES`), so
  each station is cheap in what its region produces and dear in what it lacks — ore is 7 at the mining
  station and 16 at the nebula. Rows label themselves "cheap here" / "pays well here". Buy in lots of
  10, sell all at once. **Goods share the cargo hold with scrap**, so loading up on ore means no room
  for salvage — the hold is the real decision. The HUD chip shows scrap only; the grey second segment of
  its bar is what the trade goods are taking up (see R1).
- ◐ **Pirate Bounties** — Steve: *"three bounties, boss fights with unique tactics like the Command Nexus."*
  The **boss framework is built** (`BOSS_SPECS` / `registerBoss` in `iso_grid_prototype.html`): the Nexus
  is now one registered spec among several, and each boss owns its setup, per-turn tactics and phase
  transitions. **All three bounty bosses are implemented and playable** — stage one directly with
  `iso_grid_prototype.html#mission&boss=<id>`:

  | id | placeholder name | hull | tactic |
  |----|------|------|--------|
  | `wolfpack` | The Wolfpack | Dread + Wing escorts | Flagship is **invulnerable while any escort lives** and calls a fresh pair in every 3 turns. Burst-damage race — clear escorts, dump everything into the flagship before the next wave. |
  | `phaserunner` | The Phase Runner | Neo | **Blinks** to a telegraphed cell each turn and leaves a **live mine** where it left. Read the marker and meet it where it lands; at ≤50% it seeds two mines a turn. |
  | `siegehauler` | The Siege Hauler | Tank | Weak point under **three armour plates that rotate around it each turn and get rebuilt**. Strip all three in one window; stay out of the **ram lane** telegraphed down your row (three rows at ≤40%). |

  ⚠ **Names, hulls and flavour are placeholders** — the *fights* are finished. When Steve supplies the
  characters/ships, change each spec's `name` / `subtitle` / `hull` / `dexTactics` and leave the tactics alone.

  **The board is now live too.** The BOUNTIES tab lists all three with their briefs and payouts
  (900 / 750 / 1200 coin). Accepting one marks its target in the sector — an amber crosshair in the
  world with an off-screen rim arrow, plus a dashed course line on the Star Map and a pip on the
  mini-map. Fly within 2 tiles and the boss fight starts; winning pays the coin, closes the contract
  and ticks `ep0.bountiesDone`, which drives the **Bounty Board Clear** achievement. One contract at a
  time (taking a second hands the first back); you can also abandon from the board. Losing is
  survivable as everywhere else — you limp off, and have to leave the mark and return to re-engage.
- ✅ **Side Missions** — multi-step, story-flavoured jobs, taken from a station's new **JOBS** tab.
  Each job is posted at **one** station, so you have to find the work — that gives the stations
  their own character instead of making them interchangeable. Three written:
  | Job | Posted at | Steps | Pays |
  |-----|-----------|-------|------|
  | **The Long Haul** | Waypoint Hub | acquire 10 Medical Supplies → deliver to Quarry Station | 450 |
  | **Ghosts on the Scope** | Veil Anchorage | fly to the echo source → scan there → destroy 2 hostiles | 600 |
  | **Salvage Rights** | Salvage Reach | bank 40 scrap → bring it to Salvage Reach | 500 |

  Steps are data (`SIDE_MISSIONS`): each declares a `check()` polled by `tickSides()`, an optional
  `mark` (drawn as a **green** waypoint in the world, so it never reads as the amber bounty mark) and
  `take()` to consume what it asked for. Adding a step type = adding a check. One job active at a
  time; completing all three drives the **Odd Jobs** achievement, which is now fully live.

## Story
- ✅ **Dialog while exploring** — see below; the same system covers both entries.
- ✅ **Opening cinematic — "Journey Begins"** (2026-07-21, replaced the 2026-07-20 text-on-black
  narration) — a beat between the title screen and Scene 1, ~26s end to end. Start fades to black, then
  `audio/Intro/Speech_v3.mp3` (24.66s) plays over the `#prologue` overlay while **12 shots** — one
  narration line each, paired with a still from `Assets/intro/1.png`–`12.png` — pan/zoom (Ken Burns)
  and crossfade into one another, ending on a **STARGEAR / EPISODE 0 / The Ghost Signal** title card.
  Shot list is `PROLOGUE_SHOTS` in `episode1.html`. Skippable (click / Space / Esc, which forfeits the
  card), respects 🔊, falls through to Scene 1 if the audio is missing or autoplay is blocked.
  **Sync:** each shot carries an `at:` cue and playback reads `prologueAudio.currentTime` every frame,
  so it can't drift — **don't go back to timer-based pacing** (the first version spaced shots with
  `setTimeout` by word count and desynced badly). Re-recording the VO means re-measuring the cues:
  see `INTRO_VO_SCRIPT.md`. **Not yet playtested by a human.**

## Exploring
- ✅ **Generic dialog** — **crew chatter** (`CHATTER` + `say()` + `tickChatter`). The crew talk to each
  other as you fly, as a subtitle bar with the speaker's name in their accent colour. Two jobs:
  fill the long quiet stretches (**Brett's playtest #7** — the run to the Silent Armada was silent),
  and comment on events so they land.
  Triggers: **idle** (timer, so travel is never silent but never chatty), **entering each region**,
  **hostile sighted**, **victory**, **module broken**, **hold full**, **pulling alongside a station**,
  **scan find**. Lines rotate through their pool rather than picking at random, so you don't hear the
  same one twice running. Adding dialogue = adding strings to `CHATTER`; `who` must match a CREW name.
  **Fully voiced (2026-07-20).** All 34 lines have clips in `audio/Explore/` (`tessa_01.mp3` …), cut
  from the six per-character session recordings (`<Name>_Explore.mp3`, still in the folder as the
  masters) by transcribing with faster-whisper and aligning the word timings to the known line text —
  the same route as the Episode 0 VO. Playback is `playChatterVO()` on its own channel, layered over
  music and SFX; the subtitle's `dur` is taken from the clip's real `duration` at runtime, so
  **re-recording a line needs no code change**. A missing clip or blocked autoplay degrades to a
  silent subtitle. Combat/menu/map cut the voice with the subtitle.
  ⚠️ Clip numbering is that character's line order **across the whole `CHATTER` table**, so inserting
  a line mid-table means re-cutting that character — append at the end of their run where possible.
  **Not yet playtested by a human** — worth checking Voss's line 2 and Selyra's 4→5 boundary, which
  had the tightest gaps in the source recordings.
- ✅ **Scan** — press **F** in free-roam. Sweeps a radius around the ship (animated ring) and turns up
  **salvage, coin caches and trade-goods crates**. Sites are generated deterministically from the map
  seed and **consumed once found** (`poiFound`, persisted), so a spot can't be re-farmed.
  **Module-upgradable exactly as specified:** range is 6 with nothing fitted, **+5 from a powered
  Sensor Suite** (the same part that gives Kael his combat Scan) and **+2 from a Cargo Hold** — and
  with no working Sensor Suite it refuses to sweep at all. Measured yield: **0.45 finds per sweep at
  base range vs 2.36 upgraded**, so the Sensor Suite is worth its grid space without the scan
  trivialising the economy. Tune with the `0.004` density in `poiAt` — raising it gets silly fast
  (3.5% gave 19 finds in one press).

## Menu
- ✅ Scrap amount — top-right chip with a capacity bar (amber near full, red at full).
- ✅ Coin amount — same chip.
- ✅ **Missions view with story / side mission / bounty tabs** — tab strip across the top with live
  progress counters (`SIDE 1/3`, `BOUNTY 1/3`). **STORY** keeps the original episode log from
  `episode1.html`; **SIDE** and **BOUNTY** share a job-list renderer where the active job expands
  into a step checklist (✓ done · ▶ current, with the current step's hint). ←→ or click to switch.
- ✅ **Achievements** — new menu option. Episode 0 set, per Steve:
  1. **The Ghost Signal** — complete Episode 0 *(wired: `episode1.html` flags it at the END beat)*
  2. **Bounty Board Clear** — complete every Ep 0 bounty *(counter waits on the bounty board)*
  3. **Odd Jobs** — complete every Ep 0 side mission *(counter waits on side missions)*
  4. **Know Your Enemy** — scan every Ep 0 ship *(wired: `shipDex` vs `DEX_ENTRIES`)*
  Rows show progress bars; unlocks raise a gold banner. An achievement whose total is still 0
  can never fire, so unbuilt systems can't hand out a free unlock.
- ✅ **Save/Load** — new menu option, **3 slots**. Each slot bundles the whole picture: position and
  facing, economy (coin/scrap/trade goods), ship loadout, owned + broken modules, ship codex,
  achievements, Ep 0 progress, the bounty board, and the charted fog map. Slots list their date, coin,
  scrap, scans, achievements and where you were standing. **Enter** saves, **L** loads, **Del** clears
  (load is on its own key so a stray double-click can't wipe a run). Loading rebuilds all derived state
  and re-persists the live keys so they agree with the slot.

## Star Map
- ✅ **Legend** — key panel beside the disc: your ship, story objective, hostile contact, plus the
  zone colours and "unlit = uncharted". Tucks into the map corner on narrow windows.

---

## Playtest — Steve, 2026-07-26

Fourteen items from a human playthrough, all fixed and Playwright-verified (`pageerror`
clean on both files). Not yet re-played by Steve.

| # | Fix | Where |
|---|-----|-------|
| 1 | **Kael's "not a distress call" VO cut out.** Two short clips (`kael_02.mp3` + `kael_03.mp3`) played back to back for one sentence, with an audible gap between them. Re-cut as one continuous take from the `Kael_2.mp3` keeper master (1.93–3.62s) into `kael_02_03.mp3`, and merged the two script lines into one. | `episode1.html` EP1 beat 0 |
| 2 | **Objective arrival needed circling to trigger.** `ARRIVE_DIST` was **1** tile — tighter than every other arrival radius in the game (dock 4.5, bounty 2, waypoint 1.5). Now **2**. | `ARRIVE_DIST` |
| 3 | **Bounties auto-started on arrival, no confirm.** Added `bountyPrompt`/`drawBountyPrompt`/`engageBounty`/`declineBounty`, modelled exactly on `dockPrompt`/`hangarPrompt` — Y/N panel, re-arms on leaving the mark. | `iso_grid_prototype.html` |
| 4 | **Crew screen showed Kael "1/3" actions with only 2 available.** The ⇄ SWAP counter divided by `c.slot0.options.length` (3 — Scan/Shield/Disruptor Pulse), not by what's actually unlocked (Disruptor Pulse needs the Disruptor Array module). Now counts against `crewAvailableIdxs(c)`. | `drawCrewCharView` |
| 5 | **Added an explicit ACCEPT button** to BOUNTIES/JOBS station rows instead of the implicit "click the row again to confirm" idiom — taking a contract is a one-way commitment and wanted a deliberate button. | `stationRows`/`_menuHit.stationAccept` |
| 6 | **Salvage Rights auto-completed on accept.** It's posted *and* turned in at the same station (Salvage Reach), so accepting it while already docked there with 40+ scrap already in the hold passed both steps in the same breath. Delivery-style steps now carry `requiresFreshDock` and need an actual dock **event** after the step goes live, not just already sitting in the right place — `dockSession` counters on `dockAt()`. | `tickSides`, `SIDE_MISSIONS` |
| 7 | **"The Ghost Signal" achievement never visibly popped.** It only unlocked if the player separately returned to free-roam after the ending — anyone who just watched the end screen got nothing. `endEpisode()` now unlocks it directly (writes `stargear_ach_v1`) and shows its own toast on the ending screen. | `episode1.html` |
| 8 | **Removed selling ship modules** entirely — the MODULES tab, `stationAction`'s `sellmod` case, `sellbackValue`, and the now-dead `stationSoldMods` re-buy mechanic (save format too). | `iso_grid_prototype.html` |
| 9 | **Voss's Tactics let you reassign another crew member's loadout.** Borrowing a crew's role for the turn still offered "Switch Action", which permanently changed *their* equipped ability via Voss's action point. The switch row is now hidden whenever `ap.borrower` is set — Tactics uses their current action as-is. | `actionPickRows` |
| 10 | **Primary objective banner ellipsized hard** ("Deliver to quarry s…") at a flat 220px. Width now sizes to the label (220–340px clamp). | `drawPrimaryObjective` |
| 11 | **Star Map station hover now shows unaccepted work** — "N job(s) posted here" (station-specific) and "N bounties open" (galaxy-wide board), above the existing keeper/market lines. | `stationTip`/`stationJobCounts` |
| 12 | **Added hit-number and MISS floaters**, matching the existing "+N SCRAP" style — every damage source (base weapon, crew weapons, Crimson's attack, enemy fire, all four bosses' `bossHitPlayer`) now pops a `-N` or `MISS` above the target. | `spawnFloater` call sites |
| 13 | **Crimson's hangar now appears on the Star Map** once you've actually met him (`crimsonMet`), using the same starburst glyph as his Mercenary menu entry. Hidden before that — he's still just a rumour at the Hub. | `drawMapView` |
| 14 | **Crew face ability label could run to the panel edge** — "Disruptor Pulse" (Kael's) is the longest ability name in the game and had no width guard, unlike every other dynamic label in the file. Clamped with `fitText`. | combat side panel crew-face loop |


