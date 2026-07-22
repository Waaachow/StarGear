# Audio generation prompts

Prompts for the missing audio in `ASSETS_NEEDED.md`. SFX prompts are written for
**ElevenLabs Sound Effects** (or any text-to-SFX tool); the BGM prompt is for **Suno / Udio**.

House style: clean sci-fi, not gritty-realistic. Dry and short — the game layers these
over BGM, so anything with a long tail will mud up. Export MP3, mono is fine for SFX.

Drop files at `audio/SFX/<name>.mp3` (create the folder) and `audio/BGM/Station.mp3`.

> **Status: A1–A12 all delivered and wired** (2026-07-20). Kept for reference — regenerating a
> cue means reusing its prompt below. Levels were tuned blind in `SFX_VOL`
> (`iso_grid_prototype.html`) and still want a playtest pass against the real files.
>
> Outstanding: A11's second clip (the quiet menu move/hover tick) was never generated — only the
> confirm blip exists, and it fires on station actions, not menu navigation.

---

## A1 — Laser fire → `audio/SFX/laser.mp3`  **P0**
> Short dry sci-fi laser cannon shot. Sharp synthetic zap with a fast downward pitch sweep,
> tight punchy transient, minimal reverb tail. Single shot, no echo. 0.3 seconds.

- Target length: **0.25–0.4s**. Generate 3–4 variants; the game fires this constantly, so pick the least fatiguing one.
- Should still read at low volume under music. Avoid anything "buzzy" — it gets harsh on repeat.

## A2 — Missile launch → `audio/SFX/missile.mp3`  **P0**
> Missile launching from a spacecraft. Percussive ignition thump followed by a rushing whoosh
> that doppler-shifts away, hissing rocket exhaust trailing off. Dry, no music. 0.8 seconds.

- Target length: **0.6–1.0s**. Wants noticeably more body than the laser so the two weapons read apart instantly.

## A3 — Hit / impact → `audio/SFX/hit.mp3`  **P0**
> Energy weapon slamming into a metal starship hull. Blunt low-mid thud with a metallic crunch
> and a short sparking sizzle. Dry, tight, no reverb tail. 0.4 seconds.

- Target length: **0.3–0.5s**. This is the "you connected" confirmation — it needs low-end weight the laser doesn't have.

## A4 — Shield hit → `audio/SFX/shield_hit.mp3`  **P1**
> Energy shield absorbing an incoming shot. Bright glassy ring with a shimmering harmonic
> bloom, hollow bell-like resonance fading fast. No impact crunch, no debris. 0.5 seconds.

- Target length: **0.4–0.6s**. Deliberately the *opposite* of A3: bright and ringing where the hull hit is dull and heavy.
  Players should be able to tell shields from hull with their eyes shut.

## A5 — Miss / near-miss → `audio/SFX/miss.mp3`  **P1**
> Energy bolt whipping past close by and missing. Fast doppler whoosh passing left to right,
> thin airy zip, quiet, no impact. 0.3 seconds.

- Target length: **0.25–0.4s**. Keep this **quieter** than A1/A3 — it plays on every whiff and should feel like an absence.
  (Brett's feedback #1: right now a miss is silent and reads as the game ignoring you.)

## A6 — Ship explosion → `audio/SFX/explode.mp3`  **P0**
> Spacecraft exploding. Deep concussive boom with a bright debris crackle, low sub-bass drop
> and a short rumbling decay. Cinematic sci-fi, dry, no reverb wash. 1.5 seconds.

- Target length: **1.2–2.0s**. The one place a long tail is fine — it's the kill payoff.
- Optional: a second harder variant for boss kills.

## A7 — Scan ping → `audio/SFX/scan.mp3`  **P1**
> Sonar-style sensor sweep from a spaceship computer. Clean sine ping with a slow rising
> sweep and a soft echoing tail, calm and technical, not alarming. 1 second.

- Target length: **0.8–1.2s**. Should feel *informational*, not like a warning klaxon.

## A8 — Scrap pickup → `audio/SFX/scrap.mp3`  **P1**
> Small metallic collection chime. Light clink of scrap metal with a short bright bell
> sparkle on top. Crisp, tiny, satisfying. 0.25 seconds.

- Target length: **0.2–0.3s**. Fires in rapid bursts on auto-collect — must be short and non-fatiguing.
  If your tool allows, generate 2–3 slight variants and rotate them so a pickup streak doesn't machine-gun.

## A9 — Coin / sale → `audio/SFX/coin.mp3`  **P1**
> Currency transaction confirm. Bright coin chime with a small upward two-note lift,
> clean and rewarding, light digital sparkle. 0.5 seconds.

- Target length: **0.4–0.6s**. Richer and more "resolved" than A8 — this is the payday sound, scrap is the crumb.

## A10 — Station docking → `audio/SFX/dock.mp3`  **P2**
> Spacecraft docking with a station. Heavy metal clamps locking, hydraulic hiss, deep
> mechanical clunk settling, faint airlock pressurisation. 2 seconds.

- Target length: **1.5–2.5s**. Plays under a transition, so a longer sound is fine here.

## A11 — UI select / confirm → `audio/SFX/ui_select.mp3`  **P2**
Two clips — generate both, keep `ui_select.mp3` as the confirm.

**Move / hover:**
> Minimal UI blip. Very short soft synthetic tick, muted, neutral pitch, no tail. 0.08 seconds.

**Confirm:**
> UI confirmation beep. Short clean two-tone rising blip, bright digital, crisp, no reverb. 0.15 seconds.

- Keep both **very** quiet in the mix. Menu sounds are the fastest thing to annoy a player.

## A12 — Station BGM → `audio/BGM/Station.mp3`  **P1**
For Suno / Udio — instrumental, no vocals:

> **Style:** ambient sci-fi lounge, slow downtempo, warm analog synth pads, soft Rhodes
> electric piano, gentle upright bass pulse, brushed light percussion, distant hum of a
> space station. Calm, safe, unhurried, slightly melancholy. Instrumental only. Loopable.
>
> **Exclude:** drums-heavy, tense, orchestral, vocals, risers, builds.

- Target: **60–120s**, seamlessly loopable.
- Must sit clearly apart from `Explore.mp3` and `Combat.mp3` — this is the "you're safe, spend your money" track.
  Aim slower and warmer than either.
- Master it **quieter** than the combat track; it plays under dialogue at the dock screen.

---

## Notes

- Normalise SFX to roughly the same perceived loudness (≈ -16 LUFS) before dropping them in, or
  the explosion will blow out the pickups.
- ~~Every path above already has a procedural fallback~~ — **this was never true for SFX.** When this
  doc was written there was **no sound-effect system in the game at all**; `audio/SFX/` wasn't
  referenced anywhere, so the delivered files would have played nothing. The playback layer now
  exists (below) and *that* is what degrades gracefully: a missing file is a silent no-op.

## Playback layer (built 2026-07-20)

`iso_grid_prototype.html` now has `sfx(name, gain)`, backed by pooled `Audio` elements so rapid
repeats don't cut themselves off, with per-cue levels in **`SFX_VOL`**. Hook points:

| Cue | Fires from |
|-----|-----------|
| `laser` / `missile` | `spawnShot()` — every shot in the game routes through it |
| `hit` / `shield_hit` | `fireCrewWeapon` (one cue per volley, not per target), `enemyFire`, `bossHitPlayer` |
| `miss` | a volley that connects with nothing, and an enemy shot that whiffs |
| `explode` | `spawnExplosion()` |
| `scan` | `doScan()` |
| `scrap` | salvage auto-collect on a kill |
| `coin` | selling scrap, buying/selling trade goods |
| `dock` | docking (also crossfades BGM to the new `station` track) |
| `ui_select` | confirming a station action |

### Length check against spec

| File | Spec above | Delivered | Status |
|------|-----------|-----------|--------|
| `laser.mp3` | 0.25–0.4s | ~3s → **~0.75s** | ✅ regenerated 2026-07-20 |
| `explode.mp3` | 1.2–2.0s | ~5s → **~1.4s** | ✅ regenerated, now in spec |
| `ui_select.mp3` | 0.15s | ~0.9s | ⚠ still long for a menu blip — trimmed in code |
| `scrap.mp3` | 0.2–0.3s | ~0.5s | ⚠ fires in bursts — trimmed in code |

**`SFX_MAXMS`** caps playback per cue with a ~90ms fade (so the trim isn't a click). After the
regeneration it's a safety net rather than an active trim: laser's cap now sits above the file
length and explode's was removed entirely. Only `ui_select` and `scrap` are still actually being
cut. Delete an entry to hear that cue in full.

All 11 SFX files verified distinct (MD5) — no accidental copies from regeneration.
