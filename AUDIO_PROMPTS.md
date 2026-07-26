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

# v0.6 third-ability SFX (A15–A20) — ✅ **DELIVERED 2026-07-25**

Six cues, one per crew member's new third combat ability (see `DEVLOG-v0.6.md` → "Ship parts II").
Registered in `SFX_VOL` and called from each ability's apply handler, so **dropping the file at the
path was the whole integration** — no code change.

> **All six delivered 2026-07-25 and every one landed inside its spec length** (0.88 / 0.80 / 0.68 /
> 0.48 / 0.48 / 0.88s) — the first audio batch here that needed no regeneration and no `SFX_MAXMS`
> trim. Verified loading + decoding in-game over `http://localhost:8123`: HTTP 200, `readyState 4`,
> `SFX._missing` empty, `pageerror` clean, all 17 SFX distinct by MD5. Prompts kept below for
> regeneration.
>
> ⚠️ **`disruptor` arrived misspelled as `distruptor.mp3`** and was renamed. The loader builds its
> path from the cue key (`"audio/SFX/" + name + ".mp3"`), so a typo is a **silent** miss — the cue
> never plays and nothing logs it. Match `SFX_VOL`'s spelling exactly.

Same house style as above: clean sci-fi, dry, short. Three extra constraints specific to this batch:

1. **They must not be confusable with `laser` / `missile` / `hit`.** These are the *special* moves —
   each should announce itself as something the ordinary weapons can't do.
2. **A crew VO bark fires over the top** (~1 in 3 uses, `audio/Combat/`). Keep energy out of the
   vocal band (~300 Hz–3 kHz) where you can — lean low/thump or high/sparkle — so the line stays
   intelligible underneath.
3. **These fire once per use, never in bursts** (unlike laser/scrap), so there's no `SFX_POOL` and no
   `SFX_MAXMS` cap on any of them. A modest tail is fine; anything past ~1s will outlast the
   animation.

| # | Cue | Crew · ability | Path | `SFX_VOL` | Target |
|---|-----|----------------|------|-----------|--------|
| A15 | `railgun`   | Rex · Railgun (piercing full-line, 8 dmg) | `audio/SFX/railgun.mp3`   | 0.75 | 0.7–1.0s |
| A16 | `vent`      | Tessa · Vent Plasma (all 8 adjacent squares) | `audio/SFX/vent.mp3` | 0.70 | 0.6–0.9s |
| A17 | `disruptor` | Kael · Disruptor Pulse (enemy skips its turn) | `audio/SFX/disruptor.mp3` | 0.60 | 0.5–0.8s |
| A18 | `evade`     | Astra · Evasive Roll (50% incoming miss chance) | `audio/SFX/evade.mp3` | 0.50 | 0.35–0.5s |
| A19 | `focus`     | Voss · Focus Fire (marks a target, +50% dmg) | `audio/SFX/focus.mp3`  | 0.50 | 0.4–0.6s |
| A20 | `triage`    | Selyra · Triage (revives all downed crew) | `audio/SFX/triage.mp3` | 0.55 | 0.7–1.0s |

## A15 — Railgun → `audio/SFX/railgun.mp3`  **P1**
> Heavy electromagnetic railgun firing from a warship. Short rising capacitor whine charging up,
> then a violent low-end CRACK as the slug launches, with a metallic ringing snap and a brief
> tearing air rip trailing behind it. Dry, powerful, no music, no reverb wash. 0.9 seconds.

- The heaviest cue in the crew set — it's an 8-damage shot that pierces a whole line, and it should
  sound like the most expensive thing on the ship. Give it **more low-end weight than `missile`**.
- The charge-then-crack shape is the point: a flat bang reads as just a louder laser.
- Keep the charge **under ~0.3s**. The animation doesn't wait for it.

## A16 — Vent Plasma → `audio/SFX/vent.mp3`  **P1**
> Superheated plasma venting outward from a spacecraft hull in all directions. Pressurised hiss
> release building into a deep whoomph of igniting gas, roiling fire body, fast decay.
> Enveloping and omnidirectional, not a directional shot. Dry. 0.8 seconds.

- Must read as **an area burst around the ship, not a shot leaving it** — that's the mechanical
  difference the player has to learn (it hits all 8 surrounding squares). Broad and diffuse where the
  railgun is a point.
- No metallic transient at the front; the hiss-into-whoomph swell is what distinguishes it.

## A17 — Disruptor Pulse → `audio/SFX/disruptor.mp3`  **P1**
> Electronic overload pulse frying a target's systems. Sharp electrical zap into a stuttering
> glitching buzz, digital circuitry crackling and destabilising, pitch collapsing downward as the
> power drops out. Cold and synthetic, no explosion, no fire. 0.7 seconds.

- The **downward power-loss collapse at the end is the meaning** — the enemy loses its next turn, and
  the sound should say "that thing just went dark", not "that thing took damage".
- Deliberately *electronic*, the opposite of A16's fire. No impact crunch — the target isn't hurt.

## A18 — Evasive Roll → `audio/SFX/evade.mp3`  **P1**
> Spacecraft manoeuvring thrusters firing a sharp evasive burst. Crisp compressed-gas whoosh with a
> quick banking doppler swing, tight and athletic, clean fade. No engine roar, no impact. 0.4 seconds.

- The shortest and lightest of the six. It's a **defensive buff on Astra's own ship** — quick and
  agile, never heavy. If it sounds powerful, it's wrong.
- Should sit comfortably under a bark; this one's the most likely to collide with dialogue.

## A19 — Focus Fire → `audio/SFX/focus.mp3`  **P1**
> Targeting computer locking on. Two-tone electronic acquisition tone with a tight bright confirm
> blip and a faint reticle sweep behind it. Clean, military, informational, not aggressive. 0.5 seconds.

- This is **information, not force** — Voss marks a target for the rest of the crew. Closest relative
  in the existing set is `scan` (technical, calm), but **shorter, harder and more decisive**; scan is
  a question, this is an answer.
- Keep it clearly apart from `ui_select` — it must not read as a menu click.

## A20 — Triage → `audio/SFX/triage.mp3`  **P1**
> Medical revival system engaging aboard a spacecraft. Soft defibrillator-style charge into a warm
> rising three-note chime, gentle life-support hum swelling underneath, hopeful and reassuring
> resolution. Clean sci-fi medical, no alarm, no urgency. 0.9 seconds.

- The only **warm, tonal, rising** cue in the batch — everything else is a weapon or a system.
  Selyra pulling the whole crew back up is the biggest relief moment in a fight; let it resolve
  upward rather than cutting off.
- Richer than `coin` (the other rewarding chime) and unmistakably distinct from it — this one is
  relief, not payday.

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
| `railgun` / `vent` | `fireCrewWeapon` — one cue per weapon pattern (Rex's Railgun, Tessa's Vent Plasma) |
| `evade` / `triage` | `applySelfAction` (Astra's Evasive Roll; Selyra's Triage, only when someone is actually revived) |
| `disruptor` / `focus` | `applyEnemyTarget` (Kael's Disruptor Pulse, Voss's Focus Fire) |

### Length check against spec

| File | Spec above | Delivered | Status |
|------|-----------|-----------|--------|
| `laser.mp3` | 0.25–0.4s | ~3s → **~0.75s** | ✅ regenerated 2026-07-20 |
| `explode.mp3` | 1.2–2.0s | ~5s → **~1.4s** | ✅ regenerated, now in spec |
| `ui_select.mp3` | 0.15s | ~0.9s | ⚠ still long for a menu blip — trimmed in code |
| `scrap.mp3` | 0.2–0.3s | ~0.5s | ⚠ fires in bursts — trimmed in code |
| `railgun.mp3` | 0.7–1.0s | 0.88s | ✅ in spec (2026-07-25) |
| `vent.mp3` | 0.6–0.9s | 0.80s | ✅ in spec |
| `disruptor.mp3` | 0.5–0.8s | 0.68s | ✅ in spec |
| `evade.mp3` | 0.35–0.5s | 0.48s | ✅ in spec |
| `focus.mp3` | 0.4–0.6s | 0.48s | ✅ in spec |
| `triage.mp3` | 0.7–1.0s | 0.88s | ✅ in spec |

**`SFX_MAXMS`** caps playback per cue with a ~90ms fade (so the trim isn't a click). After the
regeneration it's a safety net rather than an active trim: laser's cap now sits above the file
length and explode's was removed entirely. Only `ui_select` and `scrap` are still actually being
cut. Delete an entry to hear that cue in full.

All **17** SFX files verified distinct (MD5) — no accidental copies from regeneration. (Note their
file *sizes* collide in groups, e.g. `railgun.mp3` and `ui_select.mp3` are both 22509 bytes: the
generator exports at a fixed ~205–212 kbps, so equal-duration clips land on identical sizes. Size is
not a usable duplicate check here — hash them.)
