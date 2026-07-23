# StarGear — Episode 0: The Ghost Signal — v0.5

> **WORKING DRAFT — running log.** Entries are added as work lands. Terse for now;
> polish into the Itch devlog post at release, in the style of DEVLOG-v0.4.md.
> Sourced from the two 2026-07-22 v0.4 playtests (Brett + Steve).

---

## 🎨 Art fixes

- **Oris Vale's portrait repaired** (2026-07-23) — the Veil Anchorage relic dealer's
  avatar (`Assets/char/keepers/neb.png`) had a transparency checkerboard baked into the
  gem he holds; the art has been redone with a clean crystal.
- **"The Fleet Awakens" CG redrawn** (2026-07-23) — the bridge CG (CG03, the crew watching
  the ancient fleet ignite) showed Selyra twice; the duplicate is now Tessa. Old art kept
  as `*-old.png`, unreferenced.

## 🔊 Audio / VO fixes

- **Kael's combat barks re-recorded** (2026-07-23) — his scan line "Scanning — I can
  read their whole hand now" broke his precise, instruments-first character (Brett
  flagged it); rewritten as *"Scan complete — I can see everything they've got"* and
  the whole ten-line set re-cut from a fresh master. Bonus: the old cut was missing
  **"Target neutralised"** entirely — Kael's kill line had been playing silent — and
  it now exists.
- **Kael's flustered thank-you actually stumbles** (2026-07-23) — the burn-treatment
  scene's "Thank... Thank you." was compressed into under a second with a 0.14s gap,
  playing as a stutter rather than an embarrassed beat. Re-edited from the original
  take: a real half-second hesitation and room for the last word to land.
- **Story voices answer on cue** (2026-07-23) — Astra's "Multiple power signatures"
  hung for half a second before she spoke; it turned out 42 of the episode's 57
  voice clips carried baked-in leading silence (up to 0.8s — nearly all of Voss's
  lines). Every clip is now trimmed to a uniform 80 ms lead, so dialogue lands the
  moment the line appears. (Originals kept in `vo/_pretrim_backup/`.)
- **Kael's "Sensors have something" re-cut** (2026-07-23) — the clip now runs to the
  end of his chatter master with a gentler fade (was cut 0.16s early on a whisper
  end-timestamp). ⏳ needs an ear-check; if it still sounds clipped, the take itself
  ends abruptly and the line joins the re-record list.
- **Mission music no longer drops out** (2026-07-23) — fixes Brett's LOC02 dropout:
  every episode beat reloads the game iframe, and music refused to restart until a
  click/keypress happened *inside the new iframe* — and if a single play attempt was
  rejected, nothing ever retried, so a whole fight could run silent while voices and
  effects played on. Music now starts at boot (each segment reload picks its track
  straight back up inside the episode), and every click or key re-asserts the right
  track if it ever dropped — combat, dockside or explore.

## ⚔️ Battle fixes

- **Story and bounty kills drop scrap now** (2026-07-23) — boss fights paid nothing:
  the Blood Crown, its Hounds, the Half-Light and the Tithe all had scrap values
  defined since v0.4 that were never handed out, and the Command Nexus finale was
  scrap-free too. Now everything that dies pays out — bounty hulls at their real
  values, Nexus shield generators a little, the core a lot — and escorts still
  alive when a flagship falls explode *and* pay, instead of being lost salvage.
  The full-hold rule still applies: what doesn't fit is left behind.

- **The Command Nexus holds still** (2026-07-23) — the Mission 2 battle at the Nexus
  ("clear the approach") framed itself wherever you happened to fly in from, so the
  fortress could sit anywhere on the battlefield — even half off-screen — varying
  with approach direction. That fight now uses the same fixed staging as the finale:
  the Nexus anchored in the same spot, every run, still dormant until the story wakes
  it. Your ship still returns to its true approach position afterwards.
- **Scanning any piece of a boss identifies the boss** (2026-07-23) — scanning a
  Nexus shield generator or one of the Tithe's blast plates used to reveal that one
  piece and record nothing, so you could beat the Command Nexus or Harkin Dross and
  still find their Ship Database cards locked — the scan felt broken. Now the core,
  a generator or a plate all unlock the boss's codex entry (and the whole boss reads
  as scanned). Escorts are still their own ships — scanning a Hound identifies
  Hounds, not the Blood Crown.
- **Your shield is visible now** (2026-07-23) — the combat panel always lists
  SHIELD (dimmed "down" until Kael raises it, then "−10% dmg" in shield blue), and
  a pulsing shield bubble wraps the StarGear on the arena while it's active — so
  the state of your defence is readable at a glance from either place.
- **Boss ships no longer track you on your own turn** (2026-07-23) — bounty bosses
  and their escorts used to swivel to face your ship the instant you moved, even
  mid-player-turn, which read as enemies acting out of turn. They now face you when
  the fight opens and re-face only on the enemy phase — turning is something they
  do on *their* turn, like every other ship.

## 🧭 Quality of life & fixes

- **The story log survives the credits** (2026-07-23) — in free play (after finishing
  the episode, or loading any post-story save) the Missions menu's STORY tab was
  completely empty. It now shows the full episode as a completed log — every
  segment with its recap — plus an "Open Sector — Free Play" entry as the active
  line, so a loaded game always shows where you are and what you've done.
- **The module list scrolls instead of shrinking** (2026-07-23) — Ship Config's
  inventory used to compress its rows to cram in everything you owned, so buying
  modules made the list steadily harder to read. Rows are now a fixed, readable
  height and the list scrolls — mouse wheel or arrow keys — with an "n–m of N"
  pager, matching the station board.
- **A full bridge no longer shrinks the crew** (2026-07-23) — with five or six crew
  on screen in story scenes, everyone used to scale down to fit side by side. Now
  characters stay full size and overlap shoulders instead, with whoever's speaking
  brightened and brought to the front — so the crowd reads like a crew standing
  together, not a lineup of miniatures. Scenes with four or fewer are unchanged.
- **Station messages get their own line** (2026-07-23) — fixes Brett's overlapping-
  text defect (confirmed by Steve's screenshot): the station screen printed the last
  action's result ("Job accepted: …") on the *same line* as the keyboard hints, so a
  long message ran straight through them. The message now sits on its own row above
  the hints, at full width.
- **Popups take turns now** (2026-07-23) — hardening found on the way: the
  crew-chatter tick runs even while a Y/N panel is up and could fire a first-time
  tip (e.g. *full hold*) on top of the "Request docking?" panel. Tips now never
  open over a docking or story prompt — they queue and appear once it's answered.
- **Handing back a job asks first** (2026-07-23) — fixes Brett's vanished side job:
  on a station board, a job or bounty you'd taken had "hand it back" as its click
  action, so one stray click on an already-selected row silently returned it to the
  board. Dropping work is now a two-step ask — the first activation shows
  *"Hand back …? Progress is lost — activate again to confirm"* and only an
  immediate repeat goes through; changing row, tab, or doing anything else in
  between cancels the ask.
- **Combat no longer moves your ship** (2026-07-23) — fixes the post-combat position
  jump (Brett + Steve both hit it): leaving a fight used to resurface the ship at
  wherever it had *moved to on the combat grid*, so a Maneuver or Space Hop during
  the fight read as a teleport a few squares from where you remembered stopping —
  and a combat jump was silently worth free sector travel. The ship now returns to
  the exact spot the fight started; the camera still eases home from the final
  combat tile, so the return reads as flying back rather than a cut.
- **Crew action swaps now stick** (2026-07-23) — fixes Brett's swap-reset defect:
  starting a story mission (or any episode beat transition) silently reset every
  crew member's chosen ability back to default, because swaps were the one piece of
  ship state never persisted. They now survive segment reloads the same way the
  module loadout does, ride inside save slots (save format v4; older saves load
  fine with default swaps), and reset properly on a fresh game.
- **Ship Config: inspect before you grab** (2026-07-23) — fixes Brett's module
  grab-on-inspect defect: clicking a module used to instantly rip it off the grid.
  Now the first click **inspects** — an info card on the blueprint shows the module's
  name, power status and what it does (ability text for crew modules, capacity/hull
  text for the rest) — and clicking the **same module again** picks it up. Same
  click-to-select, click-again-to-confirm idiom the station and save screens already
  use. Footer hint and the modules tip teach it.
- **Q is the new back/cancel key** (2026-07-23) — fixes Brett's fullscreen defect: Esc is
  reserved by the browser to exit fullscreen, so pressing it to leave a menu dropped you
  out of fullscreen with the menu still open. Q now does everything Esc did — back out of
  menus, undock, drop a held module, decline prompts, skip the boss intro, cancel
  targeting — in both the sector game and the episode shell (load panel, free play). All
  ~20 on-screen key hints now advertise Q instead of Esc, the top bar lists "Back: Q",
  and the Field Manual explains the Esc/fullscreen browser behavior. Esc still works
  everywhere it used to (harmless when windowed).

## ✨ New

*(none yet)*
