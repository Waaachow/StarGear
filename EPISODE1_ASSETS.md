# Episode 0 — "The Ghost Signal" · Asset Inventory

`episode1.html` runs fully **right now** with labelled placeholders. There are **two ways** to
supply real art; each placeholder is replaced automatically with no other code changes:

1. **Convention paths** — drop files at the exact paths below (lowercase, case-sensitive):
   `assets/bg/`, `assets/cg/`, `assets/char/`.
2. **Override maps** — for differently-named files, add one line to `BG_OVERRIDE` / `CG_OVERRIDE`
   near the top of `episode1.html`, e.g. `BG01: "Assets/Bridge.png"`. Anything not listed falls back
   to its convention path. (Character sprites use `charFile()` / the convention only, for now.)

Recommended formats: backgrounds/CGs as `.png` or `.jpg`; character sprites as **transparent `.png`**,
full-body, bottom-aligned, roughly 3:4 portrait. CGs display **letterboxed** (`object-fit:contain`), so
any aspect ratio shows fully.

---

## Backgrounds → `assets/bg/`

| ID | File | Description | Used for | Status |
|----|------|-------------|----------|--------|
| BG01 | `Assets/Bridge.png` *(override)* | Bridge — Normal | Everyday conversations | ✅ |
| BG02 | `Assets/Bridge Red Alert.png` *(override)* | Bridge — Red Alert | Combat briefings / emergencies | ✅ |
| BG03 | `Assets/Bg03.png` *(override)* | Captain's Chair | Serious command moments | ✅ |
| BG04 | `Assets/bg04.png` *(override)* | Holographic Tactical Display | Scans, maps, tactical planning | ✅ |
| BG05 | `assets/bg/bg05.png` | Deep Space Exterior | Scene transitions | ☐ |
| BG06 | `Assets/bg06.png` *(override)* | Silent Armada Exterior | Fleet discovery scenes | ✅ |
| BG07 | `assets/bg/bg07.png` | Final Battlefield Exterior | Ending scenes | ☐ |

*(BG02, BG05, BG07 aren't referenced by the current script but are reserved for future scenes.)*

## Event CGs → `assets/cg/`

| ID | File | Title | Description | Status |
|----|------|-------|-------------|--------|
| CG01 | `Assets/CG/CG01-Ghost Signal.png` *(override)* | The Ghost Signal | Bridge illuminated by the eerie transmission. | ✅ |
| CG02 | `assets/cg/cg02.png` | Ocean of Silent Warships | The **StarGear** dwarfed by thousands of dormant cruisers, destroyers and carriers. | ☐ |
| CG03 | `assets/cg/cg03.png` | The Fleet Awakens | The **StarGear** surrounded as thousands of blue engines ignite at once. | ☐ |
| CG04 | `assets/cg/cg04.png` | Ancient Command Dreadnought | The colossal dreadnought emerges from hyperspace; the **StarGear** tiny in the foreground. | ☐ |
| CG05 | `assets/cg/cg05.png` | Silence | The battlefield after victory. | ☐ |

## Character Sprites → `assets/char/`

Transparent PNGs, one per expression. Path pattern: `assets/char/<name>_<expression>.png`
(lowercase, spaces → underscores). The active speaker brightens; others dim.

> Source avatars uploaded into `Assets/` with **solid grey backgrounds** are auto-processed
> (background keyed out + cropped to the figure) into `assets/char/<name>_<expr>.png`. Voss & Rex
> are done; the same flow handles the rest.

### Captain Voss — `voss_*`  (cmd blue)  ✅ provided (bg removed)
- `assets/char/voss_neutral.png` ✅
- `assets/char/voss_thinking.png` ✅
- `assets/char/voss_stern.png` ✅
- `assets/char/voss_small_smile.png` ✅  *(from `Assets/Voss-Slight_Smile.png`)*
- `assets/char/voss_concerned.png` ✅

### Kael (Doctor Mercer) — `kael_*`  (teal)
- `assets/char/kael_curious.png` ☐
- `assets/char/kael_excited.png` ☐
- `assets/char/kael_embarrassed.png` ☐
- `assets/char/kael_worried.png` ☐
- `assets/char/kael_determined.png` ☐

### Selyra — `selyra_*`  (medic pink)
- `assets/char/selyra_gentle_smile.png` ☐
- `assets/char/selyra_neutral.png` ☐
- `assets/char/selyra_concerned.png` ☐
- `assets/char/selyra_focused.png` ☐

### Rex — `rex_*`  (orange)  ✅ provided (bg removed)
- `assets/char/rex_smirk.png` ✅
- `assets/char/rex_stern.png` ✅  *(script's Rex "Stern" expression)*
- `assets/char/rex_neutral.png` ✅
- `assets/char/rex_angry.png` ✅
- `assets/char/rex_laughing.png` ☐ (not yet provided)

### Tessa — `tessa_*`  (green)
- `assets/char/tessa_smirk.png` ☐
- `assets/char/tessa_confident.png` ☐
- `assets/char/tessa_focused.png` ☐
- `assets/char/tessa_surprised.png` ☐

### Astra — `astra_*`  (AI purple)
- `assets/char/astra_neutral.png` ☐
- `assets/char/astra_curious.png` ☐
- `assets/char/astra_analytical.png` ☐
- `assets/char/astra_soft_smile.png` ☐

---

## Space Objects → `Assets/space/`

Sprites for the objects in the embedded flight game (`iso_grid_prototype.html`).
Transparent-background PNG cutouts (~1200×896), drawn as flat billboards centred on
their tile. Each has a `<TYPE>_SCALE` tunable above its `drawX` function, and a
procedural fallback (`drawXProcedural`) if the file is missing. See ISO_GRID_SPEC §3.3.

| Object | File | Zone | Notes | Status |
|--------|------|------|-------|--------|
| Broken Moon | `broken_moon.png` | Moon Orbit | Green-glow shattered planetoid | ✅ |
| Planet 1 | `Planet1.png` | Nebula (landmark) | Crystalline world w/ orbital rings | ✅ |
| Planet 2 | `Planet2.png` | Nebula (landmark) | Green ocean world | ✅ |
| Asteroid | `Astroid.png` *(filename typo)* | Nebula | Serves both small + large; tumbled/flipped | ✅ |
| Crystal | `Crystal.png` | Nebula | Cyan shard rosette; rotated per instance | ✅ |
| Station | `Station.png` | Moon + Nebula | Comm satellite; red beacon baked in | ✅ |
| Wreck | `Wreck.png` | Moon Orbit | Torn hull fragment; red beacon baked in | ✅ |
| Warship | `Warship.png` | Silent Armada | Dormant top-down capital ship; random headings | ✅ |
| Nexus (dormant) | `Nexus_dormant.png` | Command Nexus | Dark powered-down fortress (default) | ✅ |
| Nexus (active) | `Nexus_active.png` | Command Nexus | Lit fortress + beam; cross-faded in when it **awakens for battle** | ✅ |

> The Nexus is dormant until a battle erupts at the core, then awakens (energy + beam)
> and returns to dormant on victory — see ISO_GRID_SPEC §3.5.

---

## Notes

- **Ship name** is **StarGear** throughout (overview, CGs, ending line "Prepare the StarGear for jump").
- **Voice-only transmissions** (`SIGNAL` / `UNKNOWN`) have no sprite — they render as styled
  nameplates ("Ghost Signal" / "Unknown") in the dialogue bar.
- **Flight & combat** beats embed `iso_grid_prototype.html`. Its four zones are now distinct **pockets
  around a central hub** (you start in the middle); the story route loops out through all quadrants.
  Locations: Whispering Nebula (LOC01) · Broken Moon Orbit (LOC02) · Silent Armada (LOC03) · Command Nexus (LOC04).
  Travel beats end at the objective via a **"Progress the story?" prompt**; combat beats load it with
  `#mission` (plus `at=<zone>`, `enemies=<n>`, `flee=1`), start the battle immediately, and advance on
  victory. Player position **and** fog-of-war persist across beats.
- **Nexus finale = ships → CG04 → boss.** The Command Nexus sequence is a normal **ship battle**
  ("Mission 2", `#mission&at=nexus`) → Scene 5 CG03/**CG04** (dreadnought emerges) → the **three-phase
  fortress boss** ("Final Mission", `#mission&at=nexus&boss=1` — the `boss=1` flag is what makes it the
  boss, not a ship fight) → Scene 6 CG05. The Nexus is dormant until the boss battle, then awakens.
- **Defeat → game over.** If the ship is destroyed, the iso posts `{type:"defeated"}`; the episode shows
  the **thanks-for-playing** screen (`#endOverlay`, `Assets/THANKS.png`) and click/Space resets to the title.
- **Testing:** the flight game's **Options → Testing Mode** toggle adds an on-screen **SKIP OBJECTIVE**
  button (persisted in localStorage) that jumps to the next objective. The old episode `#gpFooter` Skip
  button + top toolbars are now hidden.
- **Audio (VO) is wired.** All six crew (Voss, Kael, Selyra, Astra, Rex, Tessa) have per-line voice:
  source `audio/Episode0/<Name>.mp3` recordings are cut into clips in `audio/Episode0/vo/` and mapped
  to lines via `VO_MAP` in `episode1.html`. The typewriter paces to each clip; 🔊 toggle mutes.
  Still silent by design: the SIGNAL/UNKNOWN transmissions and two short Kael stammer beats.
- **Opening cinematic is wired ("Journey Begins").** Start (or Space) on the title fades to black and
  plays `audio/Intro/Speech_v3.mp3` (24.66s) over the `#prologue` overlay before Scene 1 — twelve
  shots, each one narration line paired with a still that pans/zooms (Ken Burns) and crossfades into
  the next, ending on a title card showing the **start-menu logo** (`Assets/Start_Menu/Menu_3_logo.png`)
  over **EPISODE 0 / The Ghost Signal** (the logo replaced the old "STARGEAR" text so it matches the
  title screen, 2026-07-22). The shot list lives in
  `PROLOGUE_SHOTS` in `episode1.html`. Click or any advance key skips (skipping goes straight to Scene 1
  and forfeits the card); 🔊 mutes it; it falls through to Scene 1 if the audio never plays.
  - **Sync model:** each shot carries an `at:` cue — the second its line is spoken — and playback reads
    `prologueAudio.currentTime` every frame to decide which shot is up. It re-derives the answer
    continuously, so it cannot accumulate drift and re-syncs itself after a stall. An earlier version
    spaced the shots with `setTimeout` weighted by word count; that ran the text on a clock independent
    of the audio, so any delay in `play()` offset the two permanently, and word count turned out to be a
    poor proxy for how long a line takes to speak. Don't reintroduce timer-based pacing here.
  - ⚠️ **The `at:` values are specific to `Speech_v3.mp3` — a re-recorded VO needs them re-measured.**
    They are **measured, not estimated**: the clip was transcribed with word-level timestamps
    (`faster-whisper`, `base.en`) and the transcript aligned to the script by Needleman-Wunsch,
    matching **52 of 52** words. To redo it for a new recording, either repeat that, or open
    `episode1.html?cuetune=1`, listen, and tap Space as each line starts — the tuner prints a
    ready-to-paste `PROLOGUE_SHOTS` table to the console.
  - A 1.2s lead-in (`PROLOGUE_LEAD_IN`) holds the starfield before the first word, per the script's
    "black screen, stars slowly fade into view".
  - Recording script: `INTRO_VO_SCRIPT.md`. **`Speech_v3.mp3` is the only intro VO on disk** — the two
    earlier takes were deleted 2026-07-21. Take 2 (`speech_v2.mp3`, 46s) **overran the script** by ~21s
    of extra monologue with no shots to cover it, which is what made the text look out of sync; take 1
    (`Speech.mp3`, 39.5s) belonged to the older nine-block text-on-black script. If that closing
    monologue is ever wanted back it needs **a re-record plus ~8 more stills** — prompts are parked in
    `IMAGE_PROMPTS.md` as I13–I20, but the audio is gone.
  - **Stills live in `Assets/intro/`** — `1.png` … `12.png`, one per line, prompts in `IMAGE_PROMPTS.md`.
    ✅ All twelve in place. A shot whose file is missing plays black and the line still reads, so they
    can be swapped one at a time without breaking the sequence.
    - ⚠️ **Watch for baked-in titles on `12.png`.** The first generation came back with a "STAR GEAR
      ODYSSEY" wordmark across the lower half — wrong game name, clashing with the title card that
      fades up over it, and cropped mid-word by the shot's zoom. Re-rolled 2026-07-21 and the current
      file is clean. The I12 prompt now carries a hard no-lettering clause plus "contained core, dark
      bottom third" — keep both if it's ever regenerated.

### Not yet provided / open questions
- The **boss dreadnought** fight is now a real **three-phase Nexus fortress** boss (shield generators →
  exposed core → overload race) with the fortress as the awakened backdrop — see ISO_GRID_SPEC §8 / memory.
  (The narrative "three phases" — escort fleet / shield generators / transmission upload — are simplified
  to generators → core; refine if you want the fleet/upload beats too.)
- Character **reference art / colours** are guesses (Kael teal, Selyra pink, Astra purple, etc.) —
  adjust in `CHARS` inside `episode1.html` if you have a style guide.
