
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
