# Episode 1 Sector — Assets Needed

Scoped to the new sector's landmark sprites (`project_echoes_flight.html`, built per
`Episode 1 - Sector World Design.txt`). Every entry below has a working procedural
canvas fallback already in place — nothing here blocks the sector from looking right
today; dropping in real art is a drop-in swap (no code changes), since every draw
function checks `img.complete` before using its sprite.

Legend: ✅ done · ◐ in progress · ⚠️ needs rework · (bare) not started
Pri: P0 = blocks it looking right · P1 = wanted · P2 = polish

## Landmarks

| # | Asset | Path | Notes | Pri |
|---|---|---|---|---|
| 1 | Main Station | `Assets/space/Main_Station.png` | Rotating hab ring, multiple docking bays, cargo cranes, bright industrial nav lighting — the sector centrepiece. | P1 |
| 2 | Communications Relay | `Assets/space/Comms_Relay.png` | Comms arrays, solar panels, long antennae, docking arm, walkways. | P1 |
| 3 | Mercenary Hangar | `Assets/space/Merc_Hangar.png` | Hollowed-asteroid outpost, reinforced dock, gantries, storage containers, fuel tanks — rough/independent. NOT the Crimson Nova hangar palette (that's a separate, unrelated feature). | P1 |
| 4 | Hidden Installation | `Assets/space/Hidden_Installation.png` | Massive concealed complex — rotating rings, heavy armour, red warning lights. One of the largest structures in the sector. | P1 |
| 5 | Jump Gate | `Assets/space/Jump_Gate.png` | Large circular gate, nav beacons, clean symmetrical architecture. | P1 |

## Mining Belt

| # | Asset | Path | Notes | Pri |
|---|---|---|---|---|
| 6 | Mining-belt asteroid variant | `Assets/space/Astroid_Mining.png` | Optional distinct rock texture w/ visible drilling scars — currently reuses the existing `Astroid.png` slot. | P2 |
| 7 | Mining rig | `Assets/space/Mining_Rig.png` | Small drill/laser turret + beam accent, scattered through the belt. | P1 |

## Nebula

| # | Asset | Path | Notes | Pri |
|---|---|---|---|---|
| 8 | Gas cloud | `Assets/space/Gas_Cloud.png` | Bright coloured gas/dust cloud with electrical-discharge accents — distinct from the old `Crystal.png` shard look used in Episode 0. | P1 |

## Ambient / Traffic

| # | Asset | Path | Notes | Pri |
|---|---|---|---|---|
| 9 | Navigation buoy | `Assets/space/Buoy.png` | Small blinking nav marker, scattered in open space and along the Trade Lane. | P1 |
| 10 | Civilian freighter/hauler | `Assets/obj/Civilian_ne.png` + `Assets/obj/Civilian_sw.png` | Distinct hull for Trade Lane traffic — currently placeholder-reuses the hostile `Enemy` hull tinted blue. | P2 |

## Story Part 1 (Echoes_Part1.txt)

Scoped to `project_echoes.html`'s new VN engine and Cogwheel Station's first real
dock (`project_echoes_flight.html`). Same procedural-fallback rule as above — every
entry below already renders as a labelled placeholder box, nothing here blocks Part 1
from playing today.

| # | Asset | Notes | Pri |
|---|---|---|---|
| 11 | Rowan (character art) | Commander of Cogwheel Station — no folder, no expression set yet (`Assets/char/ROWAN/`). Always shows the plain color+initial placeholder card until drawn. | P1 |
| 12 | ✅ `BG_BRIDGE` | Scene 1 backdrop — reuses Episode 0's existing `Assets/Bridge.png` (the crew are on the StarGear's bridge, not on an exterior establishing shot). | done |
| 13 | `BG_COGWHEEL` | Scene 2 backdrop — Cogwheel Station Dock. | P2 |
| 14 | `BG_OPSOFFICE` | Scene 3 backdrop — Rowan's Operations Office. | P2 |
| 15 | `CG_CRIMSON_FLYBY` | CG event — Crimson's fighter barrel-rolling past the StarGear on arrival. | P1 |
| 16 | `CG_SECTOR_MAP` | CG event — Rowan's holographic sector map (mining sites, comms relay, broken patrol route). | P1 |
| 17 | Cogwheel Station dock backdrop/keeper | `TRADE_STATIONS` entry `main_station` has no `keeper` and no dock-screen backdrop art yet — falls back to the flight engine's existing no-art station layout. | P2 |

## Story Part 2 (Echoes_Part2.txt)

Scoped to the belt→relay→Cogwheel investigation chain and the fleet-arrival cutscene
that closes Part 2 (`STORY_TARGETS.belt/relay/station2/station3` in
`project_echoes_flight.html`, the `wreckage_scan`/`comms_relay`/`rowan_debrief`/
`fleet_call`/`fleet_arrival` scenes in `project_echoes.html`). Same
procedural-fallback rule as everything above.

| # | Asset | Notes | Pri |
|---|---|---|---|
| 18 | `BG_RELAY` | Scene 6 backdrop — the dark, powered-down Communications Relay interior. | P2 |
| 19 | `CG_SECURITY_FEED` | CG event — the relay's distorted security recording of unknown androids. | P1 |
| 20 | `CG_FLEET_ARRIVAL` | CG event — Part 2's closing beat: ships dropping out of hyperspace above Cogwheel Station. | P1 |
| 21 | "???" (Raze) placeholder card | The Part 2 transmission voice has no `CHARS` art entry by design — his identity is withheld from the player until a later part. Always the plain placeholder card; do not draw real art for him yet. | — |

## Story Part 3 (Echoes_Part3.txt)

Scoped to the `the_truth` scene in `project_echoes.html` (Scenes 8-12: Astra's origin,
Raze's ultimatum, Crimson's arrival, the evacuation order) and the Evacuation Escort
battle it hands off to (`startEvacMission()` in `project_echoes_flight.html`). Same
procedural-fallback rule as everything above — nothing here blocks Part 3 from playing
today.

| # | Asset | Notes | Pri |
|---|---|---|---|
| 22 | `CG_ASTRA_ORIGIN` | CG event — the wrecked Aegis transport, a younger Voss boarding with a flashlight, rows of inactive androids in the cargo bay. | P1 |
| 23 | `CG_ASTRA_ORIGIN_2` | CG event — young Astra looking up at Voss from the one open pod. Scared, confused, no older than she looks now. | P1 |
| 24 | `CG_ENEMY_FLEET` | CG event — dozens of enemy warships dropping from hyperspace, a gigantic carrier looming behind them. | P1 |
| 25 | `CG_RAZE_REVEAL` | CG event — Captain Raze's transmission reveal: elegant black armour, white cape, expressionless, a red-lit bridge behind him. | P1 |
| 26 | Raze (character art) | Antagonist commander — no folder yet (`Assets/char/RAZE/`). Always shows the placeholder card. **Do not reuse** the old `_archive/Episode1-v1/Episode 1 Prep/Captain Raze.png` concept art — that was drawn for the abandoned earlier draft (an older, grizzled engineer-captain look) and doesn't match this Raze's current description (elegant black armour, white cape, cold and formal). | P1 |

## Deferred (explicitly out of scope this pass)

- **Visual progression over time** — new debris fields, battle damage to structures,
  more visible patrols, burned-out ships in the Trade Lane, repair vessels working
  damaged infrastructure. Per the design doc's "Visual Progression" section; not
  designed or scheduled yet.
- **Part 2's "optional activities"** — the script names mercenary contracts, merchant
  escorts, and pirate-cleanup missions as what fills the post-debrief window before
  Rowan's fleet call. None of those job systems exist yet (`SIDE_MISSIONS`/`BOUNTIES`
  are still empty in Project Echoes), so the window is gated on two general free-roam
  actions instead — a scan find or a non-mission combat win (see
  `noteOptionalActivity()` in `project_echoes_flight.html`). Swap in real job systems
  later without changing the trigger's shape.
- **Escort/station-damage mechanics for the Evacuation Escort battle** — the script
  names escorting three civilian transports, destroying interceptors, and preventing
  station damage as separate objectives. Only the real combat exists; the escort and
  station-damage tracking have no systems to hook into yet, so the battle plays as one
  real fight against a forced wave of interceptors (see `startEvacMission()` in
  `project_echoes_flight.html`) — same simplification call as Part 2's optional
  activities.
- **Part 4** (`Echoes_Part4.txt`, "Hold the Line") — Part 3 stops the moment the
  Evacuation Escort battle begins (`the_truth` scene ends, `startEvacMission()` fires),
  matching the script's own boundary ("as the mission begins, Raze's fleet advances..."
  — everything past that line is Part 4). A future pass picks up from there.
