# Eclipse Runner — Skit Project

A small toolkit + visual-novel web app that turns per-character TTS recordings into
game-style "skit" cutscenes for **Episode 1** of *Eclipse Runner*.

---

## Contents

| File / folder | What it is |
|---|---|
| `Script.txt` | The episode script — 9 skits, 4 characters (Voss, Tessa, Rex, Astra). |
| `Voss.mp3`, `Tessa.mp3`, `Rex.mp3`, `Astra.mp3` | Full-episode TTS recordings, one per character. Each line is preceded by a **spoken slate label** ("VOSS underscore zero one", "Skit two…") that gets cut out. |
| `Voss_2.mp3` | **Preferred Voss voice** — cleaner take, and includes the "Fair point." line the original omits. Used for all Voss lines. |
| `voss.png`, `rex.png`, `tessa.png` | Transparent character portraits used by the app. (`astra.png` still needed.) |
| `index.html` | The original Skit 1 visual-novel player (open in a browser). |
| `episode1.html` | **StarGear — Episode 0 "The Ghost Signal"** player: visual novel + embedded flight/combat, runs on placeholder art. (Filename kept as `episode1.html`.) |
| `EPISODE1_ASSETS.md` | Upload checklist for Episode 1 (backgrounds, CGs, character sprites) and their exact paths. |
| `iso_grid_prototype.html` | The isometric space flight + turn-based combat game embedded by `episode1.html`. |
| `ISO_GRID_SPEC.md` | Design spec for the isometric grid prototype. |
| `econ_sim.py` | Station-economy property tests, pure maths, no browser. Asserts the market can't print coin, that trade routes decay to zero without going negative, and that all four commodities earn comparably. **Duplicates the game's price constants — update both together.** |
| `verify_econ.py` | The same properties driven against the real `iso_grid_prototype.html` in Playwright, plus save/load of the cost basis and market intel. Re-run both after any market tuning. |
| `audio/line_00.mp3` … `line_10.mp3` | Per-line voice clips for Skit 1, indexed to the app's dialogue. |
| `Skit1.mp3` | The full Skit 1 dialogue stitched in script order. |
| `Skit1_share_64k.mp3` / `Skit1_share_32k.mp3` | Compressed copies for sharing (64k recommended). |
| `build_skit1.py` | Rebuilds `Skit1.mp3` from the source recordings. |
| `build_lines.py` | Rebuilds the per-line clips in `audio/`. |
| `transcribe.py` | Transcribes the character mp3s with timestamps (alignment reference). |
| `transcript.txt` | Saved full transcript of all character recordings. |

---

## The visual-novel app (`index.html`)

Open `index.html` in any modern browser.

- **Full-width dialogue bar** along the bottom (classic VN style).
- **Three fixed character positions:** Voss (left), Rex (middle), Tessa (right).
- Characters **appear on their first line** and stay on screen.
- The **active speaker is bright**; everyone else is dimmed.
- Each line plays its **synced voice clip**, with the typewriter paced to the audio.

### Controls
| Key | Action |
|---|---|
| `Space` / `→` / `Enter` / click | Advance (first press completes a still-typing line) |
| `M` / 🔊 button | Mute / unmute |
| `R` | Replay from the start (on the end screen) |

---

## StarGear — Episode 0 (playable prototype)

> The series/ship is named **StarGear** (formerly "Aegis"). Displayed as **Episode 0 — "The Ghost
> Signal"**; the file is still `episode1.html`.

Open **`episode1.html`** in a browser. It plays as a loop of **title screen → visual-novel scenes →
flight → combat → "To Be Continued" → back to the title**, and runs **right now on labelled
placeholders**. Drop real art in and each placeholder is replaced automatically (paths + the
override maps are in **`EPISODE1_ASSETS.md`**) — no code edits.

- **Cast:** Voss, Kael, Selyra, Rex, Tessa, Astra (+ voice-only Ghost Signal / Unknown transmissions).
- **Flight & combat beats embed `iso_grid_prototype.html`.** Its four zones map to the episode's
  locations: Whispering Nebula · Broken Moon Orbit · Silent Armada · Command Nexus.
- **Continuity:** your position **and** the fog-of-war **carry across segments** — each leg resumes
  where the last ended instead of snapping back to the rim. Saved per playthrough; a new game resets it.
- **Gameplay can't be skipped.** Travel beats end when you **fly to the objective waypoint** and
  confirm a **"Progress the story? Yes / No"** prompt (No turns the ship 180° and backs it off three
  tiles). Combat beats are scripted: the battle **starts immediately** and ends when you **win**.
  Mission 1 opens with **3 ships, one of which flees on the first enemy turn** (the drone Scene 2 says
  was "reporting us").
- **Ending:** finishing the episode shows **"To Be Continued…"**; advancing returns to the title and
  resets the run.
- **Voice-over:** all six crew (Voss, Kael, Selyra, Astra, Rex, Tessa) are voiced per line — the
  typewriter paces to each clip; the 🔊 button (top-right) mutes. Voss & Rex have character art;
  the rest still render as placeholders.

### Controls
| Where | Key | Action |
|---|---|---|
| Visual novel | `Space` / `→` / `Enter` / click | Advance dialogue (first press completes a still-typing line) |
| Visual novel | 🔊 button (top-right) | Mute / unmute the voice-over |
| Flight | Arrows / WASD | Move the ship |
| Flight | `M` (or `Enter`) | Open the **Starship Menu** — pauses the game |
| Flight | `R` | Recenter to the spawn point |
| Objective | `Y` / `N` (or click) | Answer the "Progress the story?" prompt — pauses the game |
| Combat | Mouse | Click tiles to move; click action buttons (Phaser / Missile / Fire / End Turn) |

> The **Starship Menu** has Star Map · Ship · Crew · Missions · Ship Database · Save / Load ·
> Options, all functional. **Ship** is tabbed (CONFIGURATION · CARGO) and **Missions** carries
> STORY · SIDE · BOUNTY · AWARDS. The menu **can't be opened during combat**.

> Notes: the boss (Ancient Command Dreadnought) currently reuses a standard combat encounter
> as a placeholder, and no per-line voice is wired into the episode yet.

---

## How a skit is built

1. **Transcribe** each character mp3 with `faster-whisper` (model `base`, word timestamps)
   to get exact word-level timings — see `transcribe.py`.
2. **Locate** each script line's dialogue in the recording, **excluding** the spoken slate label.
3. **Cut** each clip with ffmpeg and **concatenate** in script order with natural gaps
   (~0.4 s between speakers, ~0.22 s within a line).
4. `build_skit1.py` → one combined `Skit1.mp3`; `build_lines.py` → per-line clips for the app.

### Cutting crew chatter VO (`audio/Explore/`)

Same idea, but the line text is already known, so the clip boundaries are found by **aligning the
transcript to the script** rather than by hand or by silence detection — silence detection was tried
and does not work here (Voss pauses mid-sentence, and Kael's second half has no detectable gaps).

1. `transcribe_explore.py` — whisper each `<Name>_Explore.mp3` with word timestamps → `explore_vo.json`.
2. `align_explore.py` — `difflib`-match the heard word sequence against the known `CHATTER` lines and
   take each line's span from its first/last matched word → `explore_spans.json`. It prints a match
   ratio per character; **anything below ~0.9 means check that character by ear before cutting.**
   Sequence matching is what absorbs the mishearings ("Hull's holding" → "Holes holding").
3. `cut_explore.py` — ffmpeg out one clip per line, padding clamped to the midpoint between
   neighbouring lines so nothing bleeds, with short fades on each edge.

Naming is `<name>_NN.mp3`, where `NN` is that character's line order **across the whole `CHATTER`
table** top to bottom. The masters stay in `audio/Explore/` next to the cut clips.

### Requirements
- **ffmpeg** (installed via `winget install Gyan.FFmpeg`).
- **Python 3.12** with `faster-whisper` and `pillow`
  (`pip install faster-whisper pillow`).

> Note: the file paths to `ffmpeg.exe` are hard-coded near the top of the build scripts —
> update them if ffmpeg moves.

### Make a smaller shareable audio file
```
ffmpeg -i Skit1.mp3 -ac 1 -c:a libmp3lame -b:a 64k Skit1_share_64k.mp3
```
Speech compresses very well — 64 kbps mono is effectively transparent and ~1/3 the size.

---

## Status

**Done**
- Skit 1 audio (`Skit1.mp3` + compressed shares).
- Visual-novel player with Voss, Rex, and Tessa.
- **StarGear Episode 0** end-to-end playable on placeholders (`episode1.html`): full script,
  title → VN ↔ flight ↔ combat → "To Be Continued" loop, no-skip gameplay with a "Progress the
  story?" prompt, position + fog continuity across segments, and a Starship Menu with a Missions log.
- Isometric flight/combat prototype (`iso_grid_prototype.html`): fixed 4-zone circular sector,
  persistent fog-of-war Star Map, mouse turn-based combat, scripted mission combat (immediate start,
  Mission 1 enemy flee).
- First real art wired via override maps: Bridge + Bridge Red Alert (BG01/BG02), Ghost Signal (CG01).
- **Episode 0 voice-over for the full crew** (Voss, Kael, Selyra, Astra, Rex, Tessa): per-line clips
  in `audio/Episode0/vo/`, mapped via `VO_MAP`, typewriter paced to audio, 🔊 mute toggle.
- **Crew chatter voice-over** (2026-07-20): all 34 free-roam chatter lines voiced, clips in
  `audio/Explore/`, played by `playChatterVO()` on its own channel. The subtitle holds for the clip's
  real duration, so re-recording a line needs no code change.
- **Voss & Rex character art**: uploaded avatars background-removed + cropped into `assets/char/`.

**To do**
- Build **Skits 2–9** into the player.
- **Remaining cast portraits** — Kael, Selyra, Astra, Tessa art (+ `rex_laughing`).
- Upload remaining Episode 0 backgrounds/CGs per `EPISODE1_ASSETS.md`.
- A dedicated three-phase **boss fight** for the Command Dreadnought (currently a placeholder encounter).
- Voice for the SIGNAL/UNKNOWN transmissions (currently text-only).
