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

## Deferred (explicitly out of scope this pass)

- **Visual progression over time** — new debris fields, battle damage to structures,
  more visible patrols, burned-out ships in the Trade Lane, repair vessels working
  damaged infrastructure. Per the design doc's "Visual Progression" section; not
  designed or scheduled yet.
- **Part 2's investigation checklist** (scan wreckage / missing miners / comms relay /
  return to Rowan) — the "Investigate the Asteroid Belt" story stage
  (`STORY_TARGETS.belt` in `project_echoes_flight.html`) has no content of its own yet
  beyond the pin/waypoint; Part 2 fills in what actually happens there.
