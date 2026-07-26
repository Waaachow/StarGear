
# Assets Steve needs to generate

Running list, built while working through `TODO.md`. Everything here has a working
procedural / placeholder fallback in code, so the game runs without them — dropping the
real file at the listed path swaps it in with no code change.

Legend: **P0** = blocks the feature looking right · **P1** = wanted · **P2** = polish.

---

## Audio — ✅ DELIVERED (2026-07-20)

All twelve are in place and wired; prompts kept in `AUDIO_PROMPTS.md` for regeneration.

| # | Asset | Path | Notes | Pri |
|---|-------|------|-------|-----|
| A1 | ✅ Laser fire | `audio/SFX/laser.mp3` | Player + enemy laser shot. Short, dry. | P0 |
| A2 | ✅ Missile launch | `audio/SFX/missile.mp3` | Launch whoosh. | P0 |
| A3 | ✅ Hit / impact | `audio/SFX/hit.mp3` | Shot connects on a hull. | P0 |
| A4 | ✅ Shield hit | `audio/SFX/shield_hit.mp3` | Absorbed by shields — brighter, ringing. | P1 |
| A5 | ✅ Miss / near-miss | `audio/SFX/miss.mp3` | Shot passes by. (Brett's feedback #1.) | P1 |
| A6 | ✅ Ship explosion | `audio/SFX/explode.mp3` | Enemy destroyed. | P0 |
| A7 | ✅ Scan ping | `audio/SFX/scan.mp3` | Kael's Scan / exploration scan sweep. | P1 |
| A8 | ✅ Scrap pickup | `audio/SFX/scrap.mp3` | Small metallic chime on auto-collect. | P1 |
| A9 | ✅ Coin / sale | `audio/SFX/coin.mp3` | Selling scrap at a station. | P1 |
| A10 | ✅ Station docking | `audio/SFX/dock.mp3` | Clamps / airlock on docking. | P2 |
| A11 | ⚠️ UI select / confirm | `audio/SFX/ui_select.mp3` | Confirm clip only. The second clip (quiet menu move/hover tick) was never generated — menu navigation is silent. Fine for now. | P2 |
| A12 | ✅ Station BGM | `audio/BGM/Station.mp3` | Calm dockside loop, distinct from Explore/Combat. | P1 |
| A13 | ✅ Crew chatter VO | `audio/Explore/<name>_NN.mp3` | All 34 `CHATTER` lines voiced, 34 clips cut from the six per-character masters (`<Name>_Explore.mp3`, kept in the same folder). Regenerate with `transcribe_explore.py` → `align_explore.py` → `cut_explore.py`. | P1 |
| A14 | ✅ Crew combat barks VO | `audio/Combat/<name>_NN.mp3` | All 48 `CREW_BARKS` lines voiced — occasional in-combat crew lines on actions + kill/ally-down/heavy-hit. 48 clips cut from the six per-character masters (`<Name>_Combat.mp3`, same folder) by `cut_combat.py` (transcribe→align→cut in one pass); all verified decoding in-game (2026-07-22). Script + delivery notes in `COMBAT_BARK_SCRIPT.md`. | P1 |

Remaining audio work: playtest the mix. `SFX_VOL` in `iso_grid_prototype.html` was tuned before the
real files existed, so the relative levels (explode 0.9 vs miss 0.35, etc.) are guesses. Chatter VO
sits on its own channel at `CHATTER_VO.vol = 0.9` against BGM 0.55 — also an untested guess.

## Battle visuals

| # | Asset | Path | Notes | Pri |
|---|-------|------|-------|-----|
| V1 | Per-hull attack FX | TBD | "Different enemy attack visuals" — one distinct muzzle/beam look per enemy hull (Cyclops / Dread / Gunner / Neo / Tank / Wing). Can be procedural; art only if you want painted beams. | P1 |

## UI / icons

| # | Asset | Path | Notes | Pri |
|---|-------|------|-------|-----|
| U1 | ✅ Scrap icon | `Assets/ui/scrap_64.png` | Delivered 2026-07-20, wired into the resource bar. Full-size original kept as `scrap.png`. | P1 |
| U2 | ✅ Coin icon | `Assets/ui/coin_64.png` | Same. Prompts in `IMAGE_PROMPTS.md` — read the note there before regenerating the coin. | P1 |
| U3 | ✅ **Trade station sprites** | `Assets/space/Trade_<id>.png` | Delivered 2026-07-21 — **four** sprites (`hub`, `neb`, `moon`, `armada`), one per station, all wired and verified in-game. `drawTrade` keys `tradeImg` by station id and falls back to the procedural ring-station per-station. Prompts in `IMAGE_PROMPTS.md`. | **P0** |
| U6 | ✅ Station dock backdrops | `Assets/<Station_Name>.png` | Delivered 2026-07-21 — all four, 1376×768, and all four text-free (the Waypoint Hub garbled-signage problem is gone; Hub and Salvage Reach were regenerated). Wired via `drawDockBackdrop`: cover-fit to the canvas under a 0.62 scrim. | P1 |
| U4 | Achievement icons | `Assets/ui/ach/<id>.png` | Once the achievement list is locked. | P2 |
| U5 | Module icons | `Assets/ui/mod/<id>.png` | Optional — Ship Config currently draws coloured shapes. | P2 |

## Space stations — one backdrop + one keeper each (playtest P10)

There are **four** stations (`TRADE_STATIONS` in `iso_grid_prototype.html`). Each wants an
interior backdrop and a character to talk to, so docking somewhere feels like arriving at a
place rather than opening the same menu four times. Naming: `Assets/<Station_Name>.png`,
1376×768. All four backdrops were generated from the self-contained prompts in
`IMAGE_PROMPTS.md` (U6) — including Waypoint Hub and Salvage Reach, which were regenerated
from scratch rather than kept from the original uploads.

Each station already has an economic personality to design against — `STATION_PRICES` makes
each cheap in what its region produces and dear in what it lacks — plus its own posted side job.

| Station | Region | Cheap in / known for | Posts | Space sprite | Backdrop | Keeper portrait |
|---------|--------|----------------------|-------|--------------|----------|-----------------|
| **Waypoint Hub** (0, -36) | central open space | general trade, first stop | *The Long Haul* | ✅ `Trade_hub.png` | ✅ `Waypoint_Hub.png` | ✅ `keepers/hub.png` |
| **Salvage Reach** (30, 46) | Silent Armada (SE) | salvage, scrap | *Salvage Rights* | ✅ `Trade_armada.png` | ✅ `Salvage_Reach.png` | ✅ `keepers/armada.png` |
| **Veil Anchorage** (-30, -46) | Whispering Nebula (NW) | nebula relics | *Ghosts on the Scope* | ✅ `Trade_neb.png` | ✅ `Veil_Anchorage.png` | ✅ `keepers/neb.png` |
| **Quarry Station** (44, -30) | Broken Moon (NE) | raw ore, mining | — | ✅ `Trade_moon.png` | ✅ `Quarry_Station.png` | ✅ `keepers/moon.png` |

**This table is complete as of 2026-07-21** — sprites, backdrops and keepers all delivered,
wired and verified in-game. The dock screen was re-laid-out the same day: the panel is
content-sized and slides to the side opposite the keeper, so the rooms read properly and the
figure has somewhere to stand.

| Station | Keeper | Reads as |
|---------|--------|----------|
| **Waypoint Hub** | *Marla Quen*, stationmaster, 50s | Brisk and warm — the welcome mat, first station you meet |
| **Veil Anchorage** | *Oris Vale*, relic dealer, 60s | Half appraiser, half mystic; prices relics like a jeweller |
| **Quarry Station** | *Dova Krezh*, ore foreman, 40s | Blunt, fair, no patience for haggling |
| **Salvage Reach** | *Wick*, scrapper, 20s | Magpie energy, buys anything, talks throughout |

Each has three welcomes and two send-offs in `KEEPERS` (`iso_grid_prototype.html`), rotating
rather than random. Adding dialogue = adding strings.

✅ **Keeper VO delivered and cut 2026-07-21.** All 20 lines voiced. Masters are the usual
one-per-character shape (`audio/Station/<Name>_Station.mp3`), cut to
`audio/Station/<id>_NN.mp3` by `transcribe_station.py` → `align_station.py` →
`cut_station.py` (spans kept in `station_spans.json`). Script and direction in
**`KEEPER_VO_SCRIPT.md`**. Playback is `KEEPER_VO`/`playKeeperVO` on its own channel;
subtitle duration and the send-off beat are both read from the clip at runtime, so
**re-recording a line needs no code change**. Missing clip or blocked autoplay = silent
subtitle, as everywhere else.

~~⚠️ Garbled text in the backdrops.~~ **Resolved 2026-07-21.** The regenerated `Waypoint_Hub.png`
and `Salvage_Reach.png` are text-free, as are the two new backdrops — all four were prompted
with an explicit "no lettering, glyph-only boards" clause. Keep that clause on any
regeneration; it sits at the end of each of the four prompts in `IMAGE_PROMPTS.md` (there is
no shared preamble to inherit it from — each prompt is standalone).

Layout note from the first pass: the station UI's body panel is a near-opaque slab across the
middle, which lands squarely on the window each backdrop is composed around. The rooms currently
read only at the edges (lamp, counter, tool wall). Dropping that panel's fill opacity would buy
back the best part of the art — worth doing when the screen is re-laid-out for portraits.

## Bounty bosses (Steve is supplying these)

Three bounties, each a boss fight with unique tactics. **The fights are already built and playable**
(`#mission&boss=wolfpack|phaserunner|siegehauler`) using placeholder names and existing enemy hulls —
so these assets re-skin a finished encounter rather than blocking one.

| # | Asset | Notes | Pri |
|---|-------|-------|-----|
| B1 | ✅ Bounty 1 — **Captain Malachar Drax, "The Red Reaver"** | **Delivered 2026-07-21.** Character, biography and all four dialogue beats supplied by Steve; flagship **Blood Crown** (`Assets/obj/blood_ne.png` / `blood_sw.png`), encounter CG (`Assets/CG/cg_red_reaver.png`), avatar (`Assets/char/bounties/red_reaver.png`). All wired: unique hull kept out of the patrol pool, dex card with portrait + KNOWN HISTORY, board mugshot, encounter splash over his opening lines. Escorts still fly the common Wing hull, which suits veterans flying whatever they have. | P1 |
| B2 | ◐ Bounty 2 — **Sable Renn, "The Afterimage"** | **2026-07-21.** Character, bio and 9 dialogue lines written and wired. ✅ ship *Half-Light* (`Assets/obj/half_ne.png`/`half_sw.png`, registered in `BOSS_SHIPS` at `scale: 0.88`), ✅ encounter CG (`Assets/CG/cg_afterimage.png`, 1376×768), ✅ avatar (`Assets/char/bounties/afterimage.png`, 343×768, `portraitCrop` tuned for the narrower frame). ✅ **VO cut and playing** — the first delivery was the wrong recording (a 6.7s text-to-speech sample); the corrected master landed 2026-07-21 and all 9 clips are cut. ⚠️ Her take came in at ~0.15 peak against Drax's 0.87, so `cut_boss.py` now **peak-normalises each master** (she got ×4.2) — otherwise she'd have been a quarter the volume of the other two. | P1 |
| B3 | ◐ Bounty 3 — **Harkin Dross, "The Tollman"** | **2026-07-21.** Character, bio and 9 lines written and wired. ✅ CG (`cg_tollman.png`, 1376×768), ✅ avatar (`tollman.png`), ✅ **VO cut and playing** (`tollman.mp3` → `dross_01..09`, aligned at a perfect 1.000 match), ✅ ship registered in `BOSS_SHIPS` as *Tithe* at `scale: 1.25` — the biggest hull in the game. ✅ Ship *Tithe* delivered and wired. Steve regenerated both sprites 2026-07-21 to clear a checkerboard artefact in the smoke; `tithe_ne` came back clean and `tithe_sw` had one small residual patch above the aft stack, which I removed by erasing that scrap of plume (backup kept as `tithe_sw--orig.png`). **Bounty 3 is complete.** *(An earlier note claimed the sprites faced the wrong way — that was wrong; the orientation is correct, the two views are just more alike than the other hulls' pairs.)* | P1 |
| B4 | Bounty portraits | For the station bounty board (mugshot per target). | P2 |
| B5 | ◐ Ship sprites | Each boss hull wants an `_ne` / `_sw` pair like `Assets/obj/<Name>_ne.png`, matching the existing six. Prompt + house style in `IMAGE_PROMPTS.md` § "Bounty boss ships (B5)". ✅ **Blood Crown** (`blood_ne/sw`) and ✅ **Hound**, Drax's escort wing (`hound_ne/sw`), both delivered 2026-07-21 and registered in `BOSS_SHIPS`. The Hound carries `scale: 0.72`, a new per-hull draw multiplier so a hull can read smaller than the common ships without touching `ENEMY_SCALE`. ☐ Bounties 2 and 3 still fly borrowed hulls. | P1 |

## Character art

| # | Asset | Notes | Pri |
|---|-------|-------|-----|
| C1 | Cleaned-up avatars | "Clean up avatars" on the to-do list — needs Steve to say which ones are wrong before anything is generated. | P1 |
| C2 | ✅ Station keepers — **4 portraits** | **Delivered and wired 2026-07-21**, all four, from the prompts in `IMAGE_PROMPTS.md` §"Station keepers (C2)". Waist-up cutouts at `Assets/char/keepers/<id>.png`, all correctly transparent (corner alpha 0, figure filling 96–98% of frame). Delivered ~648–817 × 768 rather than the specced 896×1200 — harmless, the draw sizes from the image's own aspect. Each keeper also has **welcome and send-off dialogue** (`KEEPERS`). | P1 |

## Audio — v0.6 third-ability combat lines + SFX — ✅ COMPLETE (VO 2026-07-24, SFX 2026-07-25)

Each crew's unlockable **third ability** (see `DEVLOG-v0.6.md`) has combat dialog + SFX hooks wired.
**Both halves are now delivered** — 18 VO barks and 6 SFX cues. Nothing in this section is outstanding.

**✅ VO barks — DELIVERED 2026-07-24.** Steve recorded the 18 lines into six `_E2.mp3` masters
(`audio/Combat/<Name>_E2.mp3`); `cut_combat_e2.py` transcribed/aligned/cut them into the numbered
clips (all six masters matched the script at **ratio 1.000**). Clips written and in-game:

| Ability | Trigger key | New clips |
|---|---|---|
| Astra · Evasive Roll | `astra-evade` | astra_09–11 ✅ |
| Rex · Railgun | `rex-railgun` | rex_10–12 ✅ |
| Kael · Disruptor Pulse | `kael-disruptor` | kael_11–13 ✅ |
| Voss · Focus Fire | `voss-focus` | voss_06–08 ✅ |
| Tessa · Vent Plasma | `tessa-vent` | tessa_10–12 ✅ |
| Selyra · Triage | `selyra-triage` | selyra_08–10 ✅ |

**✅ SFX — DELIVERED 2026-07-25. All six audio gaps for v0.6 are now closed.** One cue each at
`audio/SFX/<name>.mp3`, already registered in `SFX_VOL` and called from each ability, so dropping the
files in was the whole integration — no code change. Prompts kept for regeneration in
`AUDIO_PROMPTS.md` § "v0.6 third-ability SFX (A15–A20)".

| # | Cue | File | `SFX_VOL` | Spec | Delivered | Reads as |
|---|-----|------|-----------|------|-----------|----------|
| A15 | `railgun`   | `audio/SFX/railgun.mp3`   | 0.75 | 0.7–1.0s | ✅ 0.88s | capacitor whine → heavy low CRACK; the heaviest cue in the set |
| A16 | `vent`      | `audio/SFX/vent.mp3`      | 0.70 | 0.6–0.9s | ✅ 0.80s | pressurised hiss → plasma whoomph, broad/omnidirectional not a shot |
| A17 | `disruptor` | `audio/SFX/disruptor.mp3` | 0.60 | 0.5–0.8s | ✅ 0.68s | electrical zap → glitching buzz collapsing downward (systems going dark) |
| A18 | `evade`     | `audio/SFX/evade.mp3`     | 0.50 | 0.35–0.5s | ✅ 0.48s | crisp thruster whoosh with a banking doppler; lightest of the six |
| A19 | `focus`     | `audio/SFX/focus.mp3`     | 0.50 | 0.4–0.6s | ✅ 0.48s | targeting lock-on tone — informational, like `scan` but shorter and decisive |
| A20 | `triage`    | `audio/SFX/triage.mp3`    | 0.55 | 0.7–1.0s | ✅ 0.88s | warm rising medical chime; the only tonal, hopeful cue in the batch |

**Every one landed inside its spec length** — the first audio batch in the project that needed no
regeneration or `SFX_MAXMS` trim. All 17 SFX verified distinct (MD5), and all six verified loading +
decoding in the real game over `http://localhost:8123` (HTTP 200, `readyState 4`, `SFX._missing`
empty, `pageerror` clean).

⚠️ **The `disruptor` file arrived misspelled as `distruptor.mp3`** and was renamed on arrival. The
lookup is `"audio/SFX/" + name + ".mp3"` off the cue key in `SFX_VOL`, so a typo'd filename is a
**silent** failure — the cue just never plays and nothing logs. Check the exact spelling of these six
against `SFX_VOL` on any regeneration.

Three constraints baked into the prompts, worth keeping on a regeneration: they must not be
confusable with `laser`/`missile`/`hit`; they should keep energy out of the vocal band because a crew
bark plays over them; and they fire once per use (no `SFX_POOL`, no `SFX_MAXMS` cap on any of them),
so a modest tail is fine but anything past ~1s outlasts the animation.

---

## Crimson Nova encounter (v0.6, 2026-07-25) — code done, art pending

The rumour + hangar + VN scene are all wired and verified; these assets make it look finished. All
degrade gracefully (labelled placeholders / silence), so nothing here blocks.

**✅ Hangar map sprite — DONE.** `Assets/space/Crimson.png` (the mercenary base; wired to `OBJ.HANGAR`).

**Crimson portraits → `Assets/char/Mercenaries/CRIMSON/<Pose>.png`.** No folder move needed — the
resolver reads this sub-folder (`CHAR_DIR` override in `charFile`). Names use underscores; `enorm()`
ignores them, so the script's "Heroic Smile" resolves to `Heroic_Smile.png`.

The script names **21 poses** (incl. Neutral). **13 done, 8 to draw.** Each missing one shows the
labelled "C" placeholder until it lands:

| Pose (filename) | Status | Used for (script cues) |
|---|---|---|
| `Neutral.png`             | ✅ have | fallback / default |
| `Heroic_Smile.png`        | ✅ have | Heroic Smile |
| `Finger_Point.png`        | ✅ have | Finger Point |
| `Heroic_Pose.png`         | ✅ have | Heroic Pose |
| `Sparkling_Confidence.png`| ✅ have | Champion of hope! |
| `Proud.png`               | ✅ have | Seven. |
| `Finger_Up.png`           | ✅ have | Finger Up |
| `Dramatic_Shock.png`      | ✅ have | Oh! |
| `Heroic_Concern.png`      | ✅ have | You're the serious one. |
| `Laughing.png`            | ✅ have | Laughing |
| `Serious.png`             | ✅ have | Serious |
| `Wink.png`                | ✅ have | Wink |
| `Salute.png`              | ✅ have | Salute |
| `Eyes_Closed_Smile.png`   | ❌ draw — now shows **Heroic_Smile** | ...I usually get applause by now. |
| `Confident.png`           | ❌ draw — now shows **Sparkling_Confidence** | Good. / I fight until the battle's won. |
| `Humble_Smile.png`        | ❌ draw — now shows **Heroic_Concern** | (silent beat before "Someone has to.") |
| `Soft_Smile.png`          | ❌ draw — now shows **Heroic_Concern** | Someone has to. |
| `Grinning.png`            | ❌ draw — now shows **Laughing** | Anyway! |
| `Smile.png`               | ❌ draw — now shows **Heroic_Smile** | Neither are smoke bombs / No piracy. |
| `Professional.png`        | ❌ draw — now shows **Serious** | Pay me before departure. |
| `Heroic.png`              | ❌ draw — now shows **Heroic_Pose** | No civilian casualties. |

The 8 undrawn poses are aliased to the nearest existing Crimson avatar (via `EXPR_ALIAS`), so the
scene shows a real portrait on every line — no placeholders. **As each is drawn, add its name back to
`CHAR_ART.CRIMSON`** so the exact pose takes over from the fallback.

**✅ Scene background — DONE.** `Assets/Crimson_Hanger.png` (id `BG_CRIMSON`, wired in `BG_OVERRIDE`).

**✅ Kael "Deadpan" pose — DONE.** `Assets/char/KAEL/Deadpan.png` (added to `CHAR_ART.KAEL`, so
Kael's "I object." line now uses a dedicated pose instead of the Neutral fallback).

**✅ VO — DONE (2026-07-25, greet lines landed 2026-07-26).** Steve recorded all seven speakers into
`audio/Rumours/*.mp3` masters; `cut_rumours.py` (whisper align + cut, same route as `cut_combat.py`)
split them into per-line clips `audio/Rumours/vo/<char>_NN.mp3` and emitted the `SCENE_VO` map (keyed
`who|text`, consulted by `showLine` after `VO_MAP`). **All 52 scene lines are voiced** (the 2 silent
"..." beats don't need audio). `Rex_Astra.mp3` is Rex's take (confirmed by transcription). The
`crimson_greet` lines landed as a separate master (`audio/Rumours/Crimson_greet.mp3`) and were cut with
a standalone script, `cut_crimson_greet.py` (same align/cut logic, merges into the existing
`scene_vo.json` instead of regenerating it) → `crimson_greet_01/02.mp3`.

---

## Crimson Nova as a hireable combat ally (2026-07-26) — code + VO done

The hire mechanic (`DEVLOG-v0.6.md` → "Crimson Nova joins as a hireable combat ally") is code-complete
and Playwright-verified.

**✅ Space idle chatter — DONE (2026-07-26).** `audio/Explore/crimson_idle_01–05.mp3`, cut from
`audio/Explore/Crimson_Explore.mp3` by a standalone script, `cut_crimson_explore.py` (same
align/cut logic as `cut_explore.py`, just not folded into that script's fixed six-name list).
`CHATTER.crimsonIdle` in `iso_grid_prototype.html` plays them on his own idle timer while hired.

**✅ Combat barks — DONE (2026-07-26).** `audio/Combat/crimson_<trigger>_NN.mp3`, 13 clips cut from
`audio/Combat/Crimson_Combat.mp3` by `cut_crimson_combat.py` (0.980 whisper match, all 13 lines
found) — reuses the `CREW_BARK_VO` channel:

| Trigger | Clips | Fires |
|---|---|---|
| `join` | crimson_join_01–02 | first Guest turn of a fight |
| `attack` | crimson_attack_01–03 | Spotlight Shot (≤2 enemies) |
| `supernova` | crimson_super_01–02 | Supernova Strike (3+ enemies) |
| `heavyHit` | crimson_hit_01–02 | he takes ≥34% of his max HP in one hit |
| `knockedOut` | crimson_ko_01–02 | knocked out — retreats and leaves the team |
| `noShow` | crimson_noshow_01–02 | couldn't afford the fee, sits the fight out |

Crimson Nova is now fully voiced end to end: the hangar hire scene, the revisit greeting, free-roam
idle chatter, and every combat bark trigger.
