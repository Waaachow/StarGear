# v0.5 Local Playtest Checklist

All 21 v0.4 defects, original ref numbers. Test in the local dev files
(`episode1.html` / `iso_grid_prototype.html`) — **dist\build is still v0.4**.
Fullscreen the browser for #1 to get a true repro of Brett's setup.

## Brett's defects

- [x] **#1 Fullscreen + Esc** ✅ PASS (Brett, 2026-07-23) — go fullscreen, open any menu, press **Q** → menu
  closes, fullscreen stays. Q backs out everywhere Esc did (menus, undock, drop
  held module, decline prompts, skip boss intro, cancel targeting, load panel).
  Hints on screen should all say Q now; top bar shows "Back: Q".
- [x] **#2 Module grab-on-inspect** ✅ PASS (Brett, 2026-07-23) — 💡 feature ask:
  clicking again while *holding* a module should release the grab (put it back) — Ship → Configuration: first click on a
  module **inspects** (info card on the blueprint: name, power status, what it
  does); clicking the *same* module again picks it up. No more instant grab.
- [x] **#3 Popup overlap** ✅ PASS (Brett, 2026-07-23) — dock at a station, accept a job with a long title →
  the "Job accepted: …" message sits on its **own line above** the key hints,
  no text collision. (Also: first-time tips should never open on top of a
  docking/story Y/N prompt — they wait.)
- [x] **#4 Post-combat position jump** ✅ PASS (Brett, 2026-07-23) — note your map square, enter combat, use
  Maneuver/Space Hop to move around, win → you're back on the **exact square**
  the fight started (camera eases home, but the position is the entry position).
- [x] **#5 Job removal guard** ✅ PASS (Brett, 2026-07-23) — 💡 feature ask:
  remove hand-back entirely (you shouldn't be able to return a taken job at all) — station board, click a job you've already taken,
  then activate it → first activation shows *"Hand back …? Progress is lost —
  activate again to confirm"*; only an immediate repeat hands it back. Switching
  row/tab cancels the ask.
- [x] **#6 Swap reset** ✅ PASS (Brett, 2026-07-23) — swap some crew abilities, then start a story mission /
  cross an episode beat → swaps survive. Also: save, reload the save → swaps
  survive. New game → swaps back to defaults.
- [x] **#7 LOC02 music dropout** ✅ PASS (Brett, 2026-07-23) — play into LOC02 → music keeps going through
  the beat transition. If it ever drops, any click/keypress brings it back.
- [x] **#8 Kael scan VO** ✅ PASS (Brett/Steve, 2026-07-23) — scan in combat → new line *"Scan complete — I can
  see everything they've got"* (whole 10-line set is a fresh re-cut; his kill
  line "Target neutralised" now actually plays — it was silent in v0.4).

## Steve's defects

**Audio/VO**
- [x] **#9 Kael "Thank… thank you"** ✅ PASS (Steve, 2026-07-23) — burn-treatment CG scene: proper flustered
  hesitation, no stutter, no tapping. *(You already passed this in-session —
  quick confirm in context.)*
- [x] **#10 Kael "sensors have something"** ✅ PASS (Steve, 2026-07-23) — ear-check cleared, re-cut is good — re-cut runs
  to the end of the take with a gentler fade. If it *still* sounds clipped, the
  take itself ends abruptly → goes on the re-record list.
- [x] **#11 Astra "Multiple signatures" delay** ✅ PASS (Steve, 2026-07-23) — line fires the moment the text
  appears. (42 of 57 VN clips were lead-trimmed — listen for any VN line that
  now feels *early* or clipped at the start, too.)

**CG / art**
- [x] **#12 Fleet Awakens CG** ✅ PASS (Steve, 2026-07-23) — bridge CG shows Tessa, not a second Selyra.
- [x] **#13 Oris Vale avatar** ✅ PASS (Steve, 2026-07-23) — Veil Anchorage keeper: gem is clean, no
  checkerboard.

**Battle**
- [x] **#14 Nexus placement** ✅ PASS (Steve, 2026-07-23) — Mission 2 "clear the approach": fly in from
  different directions → the Nexus sits in the **same NW spot every time**,
  same as the finale staging; still dormant. Exiting returns you to your
  approach position.
- [x] **#15 Boss scanning** ✅ PASS (Steve, 2026-07-23) — RE-FIXED 2026-07-23 — Steve hit it on the BOUNTY
  path (scanning a Tithe plate didn't unlock the codex). Root cause: in a bounty
  fight `pendingBossId` is cleared the instant `startCombat` returns and no `#boss=`
  hash sets `BOSS_ID`, so `bossIdNow()` was null mid-fight → `bossDexId()` returned
  null → `discoverShip(null)` no-op. Now `bossDexId()` reads the live
  `combat.boss.spec` first. (First v0.5 fix only covered the mission-hash path — my
  test used that path and passed falsely.) **Re-test over the real bounty**: — scan a Nexus shield generator or a Tithe blast
  plate → the boss's Ship Database card unlocks (hull, generator, or plate all
  count). Scanning a Hound escort still identifies Hounds, not the Blood Crown.
- [x] **#16 Off-turn rotation** ✅ PASS (Steve, 2026-07-23) — boss fight: enemies face you at fight start,
  then only turn during **their** phase. Moving on your turn doesn't make them
  swivel.
- [x] **#17 Shield UI** ✅ PASS (Steve, 2026-07-23) — combat panel always lists SHIELD (dim "down" until
  Kael raises it, then "−10% dmg"); a pulsing blue bubble wraps the StarGear
  while it's active.
- [x] **#18 Scrap drops** ✅ PASS (Steve, 2026-07-23) — bounty bosses, Hounds, Nexus generators (small) and
  core (big) all pay scrap; escorts alive when the flagship dies explode *and*
  pay. Full hold still caps what you keep.
  - 👁 **Design watch:** Drax's Hound waves + Tithe's rebuilding plates now pay
    per kill — see if in-fight farming feels abusable.

**UI scaling**
- [x] **#19 Six-crew shrink** ✅ PASS (Steve, 2026-07-23) — story scene with 5–6 crew: full-size characters
  overlapping shoulders, speaker brightened and in front. ≤4 crew unchanged.
- [x] **#20 Module list scroll** ✅ PASS (Steve, 2026-07-23) — fixed-height rows,
  wheel/arrow scroll. Scroll wasn't evident on first pass; **REDESIGNED 2026-07-23:** header module count + scrollbar with up/down arrows +
  explicit "▼ N more below" counter + scroll-shadow fades on the rows at any edge
  with more beyond it. (First pass crammed "▲ scroll up for more" into the header
  gap and it squashed — Steve flagged; text cue removed, shadows do that job now.)
  Screenshots on Desktop: modules_scroll_top.png / _mid.png. Re-check in-game.
- [x] **#21 Story log after load** ✅ PASS (Steve, 2026-07-23) — finish the episode (or load a post-story
  save) → Missions ▸ STORY shows the full episode as completed recaps plus an
  active "Open Sector — Free Play" entry. Mid-story saves still resume the log
  correctly.

## New defects found during v0.5 playtest

- [x] **#25 Tithe weak point should be a bigger target** ✅ PASS (Steve, 2026-07-23) — once all 3 plates are stripped, the exposed core is
  hittable on any of the 3 tiles the barge lies across (was a single centre tile),
  so finishing hits aren't finicky. A shot that overlaps several of those tiles
  still counts as **one** hit (damage loops over ships, not tiles). The widened
  target is inert while the plates are up, so it never clashes with targeting the
  rotating plates. **All three tiles light up orange under the hull** (like the
  centre) when open, matching exactly what's hittable. **The footprint is
  FACING-AWARE** — the barge sprite draws "/" facing fore/aft and "\" facing
  left/right (2 art orientations + h-flip) and re-faces the player, so the lit tiles
  now follow the hull whichever way it turns (first two attempts used a fixed axis
  and looked wrong when the barge was flipped). Screenshots: tithe_face_FWD/LEFT.png.
  Re-test: strip the plates, fire on any part of the hull.

- [x] **#22 Achievement state on load** (Steve, 2026-07-23) — the "didn't unlock on
  completion" report was actually the file:// partitioning (resolved). The real
  code change: a save is a point-in-time snapshot, so **loading restores the exact
  achievement + completion state from when it was saved** (first attempt wrongly
  ratcheted — Steve saw a pre-completion save load with the achievement still
  unlocked). Now loading a pre-completion save re-locks The Ghost Signal and clears
  the done-flag; a post-completion save restores it. **Verified over http:** complete
  → unlock; load older save → locked; load newer save → unlocked. Steve to re-confirm.

- [x] **#23 "Saved game lost" — NOT A PRODUCT BUG** (Steve, 2026-07-23) —
  saving then reloading showed nothing in the title Load panel *when opened as a
  local file* (`file://`, double-click). Cause: Chrome/Edge partition the game
  iframe's `localStorage` separately from the parent page on `file://`, so the
  save lands in a bucket the title panel can't read (the in-game Save/Load screen
  still sees it — it's inside the same iframe). Over **http** (itch.io https, or
  the local `http://localhost:8123` server) parent + iframe share one store and
  saves load normally. **Decision: ship v0.5 as itch web (https) — no code fix.**
  👉 **Playtest locally over http://localhost:8123/episode1.html, not by opening
  the file**, so you're testing the real environment.
  - **Same cause, second symptom:** completing the story didn't unlock "The Ghost
    Signal" **on file://** either — the episode-complete handshake (parent writes
    `stargear_ep0_done`, game iframe reads it at next boot) crosses the same
    partitioned boundary. Verified end-to-end over http: story completion unlocks
    the achievement and persists. No code fix — ship itch web, test over http.

- [x] **#24 Tithe bounty too hard — plates rebuilt too fast** ✅ PASS (Steve, 2026-07-23)
  — TUNED: Harkin Dross's blast plates rebuilt in 3 enemy
  turns, so the first plate was back before you could strip all three and punish
  the open weak point. Rebuild delay raised 3 → 6 turns. Re-fight the Tithe
  bounty: stripping all three plates should now leave a real open window on the
  core. (Dial `SIEGEHAULER.plateRegen` if it needs more/less.)

---
**After the pass:** report fails/oddities → then devlog polish → itch build →
v0.5 zip (excluding `_pretrim_backup/`, `*-old.png`, `*_v1/_v2` masters,
`kael_07_old.mp3`, `kael_09_stammer_orig.mp3`; dock interiors stay PNG; itch
page controls text switches Esc → Q).
