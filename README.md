# StarGear — Episode 0: *The Ghost Signal*

A browser game in a single pair of HTML files: a fully-voiced **visual novel** wrapped around an
**isometric space flight + turn-based combat** sandbox, with a trading economy, dockable stations,
bounty bosses, side missions, module fitting, and save/load. No build step, no dependencies —
**open `episode1.html` in a modern browser and press START.**

**Current version: v0.4** — see [DEVLOG-v0.4.md](DEVLOG-v0.4.md) for the full release notes
(and [DEVLOG-v0.3.md](DEVLOG-v0.3.md) for the previous release).

---

## Playing

| File | What it is |
|---|---|
| `episode1.html` | **The game.** Title screen → 12-shot opening cinematic → Episode 0 story (visual novel ↔ flight ↔ combat) → free roam after the ending. Embeds the iso prototype for every flight/combat beat. |
| `iso_grid_prototype.html` | The flight/combat/economy sandbox on its own, free-roam from the first frame. Useful for testing; the episode is the intended way in. |

### What's in v0.4 (highlights)

- **An economy** — scrap salvage, coin, a hold with hard capacity, and four commodities with
  per-station prices, finite stock, and markets that move when you trade. Same-station
  round-trips always lose money; profit comes from running routes.
- **Four trade stations**, each with its own exterior, painted interior, and a **fully-voiced
  keeper** — sell scrap, repair, buy/sell modules, trade goods, take work.
- **Three bounty bosses** — Drax's Blood Crown, Sable Renn's Half-Light, Harkin Dross's Tithe —
  each with unique tactics, art, and voiced dialogue that reacts to the fight.
- **Ship Config fit-grid** — modules are shaped pieces placed on the blueprint, and they *are*
  the crew's combat abilities; pull Rex's Missile Pod and Rex loses Missile.
- **Side missions, exploration scan, achievements, mini-map, Field Manual + contextual tips.**
- **Sound** — full SFX layer, dockside music, an Options mixer, and **82 newly voiced crew
  lines** (34 free-roam chatter + 48 combat barks) on top of the fully-voiced story and keepers.
- **Save/load** — three slots plus downloadable `.sgsave` files, story position included.

### Controls

| Where | Key | Action |
|---|---|---|
| Visual novel | `Space` / `→` / `Enter` / click | Advance (first press completes a still-typing line) |
| Flight | Arrows / WASD | Move the ship |
| Flight | `F` | Exploration scan |
| Flight | `E` | Dock at a nearby station |
| Flight | `M` / `Enter` | Starship Menu (Star Map · Ship · Crew · Missions · Ship Database · Save/Load · Field Manual · Options) |
| Combat | Mouse | Click tiles to move; click crew to act; ⇄ Switch Action swaps a crew member's two abilities |
| Objective | `Y` / `N` | Answer the "Progress the story?" / dock prompts |

> Every crew member carries **two abilities** — switching from Menu → Crew between fights is
> free; mid-battle it costs that crew member's turn. The Field Manual (in the menu) covers
> every system.

---

## Building the itch.io bundle

```powershell
powershell -ExecutionPolicy Bypass -File build_itch.ps1
```

Stages a clean tree under `dist\build`, compresses opaque art to JPEG (CGs capped at 1920w,
backgrounds + the four station interiors) and downscales sprites, rewrites the `.png → .jpg`
references in **both** HTML files, and zips with `index.html` at the root — producing
`StarGear - Episode 0 - The Ghost Signal - v0.4.zip`. Character art keeps native PNG (alpha).

## Testing

- `python econ_sim.py` — pure-maths property tests on the station economy (no browser): the
  market can't print coin, routes decay to zero without going negative, all four commodities
  earn comparably. ⚠️ **Duplicates the game's price constants — change both together.**
- `python verify_econ.py` — the same properties driven against the real
  `iso_grid_prototype.html` in **Playwright**, plus save/load of cost basis and market intel.
- Re-run both after any market tuning. UI/feature changes are verified with Playwright
  (`pageerror` clean + state probes + screenshots).

---

## Voice-over production pipeline

All VO is cut from **per-character master recordings** by transcript alignment — silence
detection does not work on this material (mid-sentence pauses, gapless runs).

1. **Transcribe** the master with `faster-whisper` (word timestamps) — `transcribe*.py`.
2. **Align** the heard words against the known script with `difflib` — `align_*.py`. Each
   prints a match ratio; **below ~0.9, check that character by ear before cutting.**
3. **Cut** one clip per line with ffmpeg, padding clamped to the midpoint between neighbouring
   lines, short fades on the edges — `cut_*.py`.

Four instances of the pipeline: **Explore** (crew chatter → `audio/Explore/`), **Combat**
(crew barks → `audio/Combat/`), **Station** (keeper lines → `audio/Station/`), **Boss**
(bounty dialogue → `audio/Boss/`). Scripts + delivery notes: `COMBAT_BARK_SCRIPT.md`,
`KEEPER_VO_SCRIPT.md`, `BOSS_VO_SCRIPT.md`, `INTRO_VO_SCRIPT.md`.

### Requirements

- **ffmpeg** (`winget install Gyan.FFmpeg`) — paths are hard-coded near the top of the cut
  scripts; update them if ffmpeg moves.
- **Python 3.12** with `pip install faster-whisper pillow` (plus `playwright` for the tests).

---

## Origins: the Eclipse Runner skit toolkit

The repo began as a toolkit that turns per-character TTS recordings into game-style "skit"
cutscenes, and that heritage is still here and working:

| File | What it is |
|---|---|
| `index.html` | The original Skit 1 visual-novel player. |
| `Script.txt` | The episode script — 9 skits, 4 characters. |
| `Voss.mp3` / `Voss_2.mp3` / `Tessa.mp3` / `Rex.mp3` / `Astra.mp3` | Full-episode character masters. ⚠️ **Don't delete** — `build_skit1.py` / `build_lines.py` slice Skit 1 out of them by timestamp. |
| `build_skit1.py` / `build_lines.py` | Rebuild `Skit1.mp3` / the per-line clips in `audio/`. |
| `transcribe.py` / `transcript.txt` | Whisper transcription of the masters (alignment reference). |

Skits 2–9 are still to be built into the player.

## Docs

- [DEVLOG-v0.4.md](DEVLOG-v0.4.md) / [DEVLOG-v0.3.md](DEVLOG-v0.3.md) — player-facing release notes.
- [TODO.md](TODO.md) — the working build log: every change, decision, and warning, by session.
- [ISO_GRID_SPEC.md](ISO_GRID_SPEC.md) — design spec for the iso prototype.
- [EPISODE1_ASSETS.md](EPISODE1_ASSETS.md) / [ASSETS_NEEDED.md](ASSETS_NEEDED.md) — art/audio checklists and exact paths.
- [IMAGE_PROMPTS.md](IMAGE_PROMPTS.md) / [AUDIO_PROMPTS.md](AUDIO_PROMPTS.md) — generation prompts for art and SFX.
