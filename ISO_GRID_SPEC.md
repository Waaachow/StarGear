# 13×13 Moving-World Isometric Space Game — Specification

**Version:** 2.0
**Implementation:** `iso_grid_prototype.html` (single-file canvas prototype)
**Status:** Documents the shipped prototype

> **What changed from v1.0:** the grid grew from 7×7 to **13×13**, the terrain
> became open **space** (with a separate planet/asteroid/station object layer and
> a parallax starfield), and two gameplay systems were added on top of the
> moving-world engine: **wandering ships** (red hostile / blue neutral) and a
> **mouse-driven turn-based combat** mode. Sections 0–6 describe the world
> engine; sections 7–8 describe the gameplay layers.

---

## 0. Overview & Invariants

A fixed 13×13 isometric grid of diamond tiles. The **ship never moves** — it is
permanently anchored above the centre tile `grid[6][6]`. All apparent motion is
produced by **shifting the world underneath the ship** and generating fresh
tiles at the leading edge.

**Hard invariants (must always hold):**

1. `GRID_SIZE == 13`. Logical storage is `Tile grid[13][13]`.
2. Centre tile is always `grid[6][6]` (`CENTER == 6`).
3. The ship's screen position is constant for the entire program lifetime
   (`SHIP_ANCHOR`), recomputed only on canvas resize.
4. After any completed move, the array is again a fully-populated 13×13 with no
   `null`/empty cells.
5. Exactly one row **or** one column changes per discrete free-roam move.
6. Indexing convention: `grid[x][y]` — **x = column, y = row**. Fixed everywhere.

**Axis directions (logical):**

- `+x` → world "right" / east
- `+y` → world "down-screen" / south
- "Forward" (player presses up) = world content moves toward the player; rows
  scroll so new content enters at `y = 0`.

---

## 1. Coordinate System

Three coordinate spaces. Conversions are pure functions.

### 1.1 Constants

```
TILE_WIDTH        = 64      // diamond full width  in pixels (2:1 ratio)
TILE_HEIGHT       = 32      // diamond full height in pixels (= TILE_WIDTH / 2)
HALF_W            = 32      // TILE_WIDTH  / 2
HALF_H            = 16      // TILE_HEIGHT / 2
Z_PIXELS_PER_UNIT = 32      // pixels of vertical screen offset per 1.0 worldZ
GRID_SIZE         = 13
CENTER            = 6       // index of centre tile on each axis
RISE_MS = 300, DROP_MS = 250, LATERAL_MS = 300
```

### 1.2 Spaces

| Space   | Fields                    | Meaning                                          |
|---------|---------------------------|--------------------------------------------------|
| Logical | `x, y` (int, 0..12)       | Array indices into `grid[x][y]`.                 |
| World   | `worldX, worldY, worldZ`  | Iso-projected position; Z = rise/drop height.    |
| Screen  | `screenX, screenY`        | Final pixel position after camera + ship offset. |

### 1.3 Projection (logical → world)

```
worldX = (x - y) * HALF_W
worldY = (x + y) * HALF_H
worldZ = animation height offset   // 0.0 at rest; animated for rise/drop
```

### 1.4 World → Screen

The camera is locked so the centre tile `(6,6)` maps to the screen anchor
`SHIP_ANCHOR = (canvasW/2, canvasH/2 − 40)`.

```
CENTER_WORLD_X = (6 - 6) * HALF_W = 0
CENTER_WORLD_Y = (6 + 6) * HALF_H = 192

screenX = SHIP_ANCHOR.x + (worldX - CENTER_WORLD_X) + cameraOffsetX
screenY = SHIP_ANCHOR.y + (worldY - CENTER_WORLD_Y) + cameraOffsetY
                        - worldZ * Z_PIXELS_PER_UNIT
```

- `cameraOffsetX/Y` are non-zero only during a lateral-shift animation (§4) or
  the combat exit slide (§8). At rest they are 0.
- Subtracting `worldZ * Z_PIXELS_PER_UNIT` renders a tile with `worldZ < 0`
  **lower** on screen (sunken), so a rising tile climbs into place.

### 1.5 Screen → Logical (picking / hit-test)

```
worldX = screenX - SHIP_ANCHOR.x
worldY = screenY - SHIP_ANCHOR.y + CENTER_WORLD_Y
gx = (worldX / HALF_W + worldY / HALF_H) / 2
gy = (worldY / HALF_H - worldX / HALF_W) / 2
```

`gridCoordsAt` returns fractional coords; `cellAtScreen` rounds them. Used by
the combat cursor, click-to-move, and wandering-ship distance checks.

### 1.6 Example coordinates

`worldX = (x-y)*32`, `worldY = (x+y)*16`, at rest `worldZ = 0`.

| Tile      | (worldX, worldY) |
|-----------|------------------|
| (0,0)     | (0, 0)           |
| (6,6) ctr | (0, 192)         |
| (12,0)    | (384, 192)       |
| (0,12)    | (-384, 192)      |
| (12,12)   | (0, 384)         |

Centre `(6,6) = (0,192)` maps to `SHIP_ANCHOR`. ✓

### 1.7 Render ordering

Painter's algorithm over all renderables (tiles + dropping tiles + objects).
Sort ascending by:

```
primary   = band  = (x + y)         // iso depth: lower sum farther back/top
secondary = worldZ                  // for equal band, lower Z drawn first
tertiary  = order                   // 0 = settled tile, 1 = rising tile, 2 = object
```

The `order` key makes rising tiles composite over their settled neighbours
within a band, and world objects (planets/stations) draw on top of their tiles.

---

## 2. Moving-World Behaviour (free-roam)

Each free-roam move discards one edge line, shifts the rest one step, and
generates a new edge line. The **logical array is mutated atomically at
move-start**; the lateral slide + per-tile rise/drop are presentational
catch-up (§4). A world origin `(worldOriginX, worldOriginY)` tracks the absolute
coordinate of array cell `(0,0)` for deterministic generation.

### 2.1 Direction → array operation

| Input        | World appears to | Discard    | Shift           | Generate at | Origin   |
|--------------|------------------|------------|-----------------|-------------|----------|
| Up (Forward) | move toward you  | row `y=12` | rows down (+y)  | `y = 0`     | `oY -= 1`|
| Down (Back)  | move away        | row `y=0`  | rows up (−y)    | `y = 12`    | `oY += 1`|
| Left         | slide right      | col `x=12` | cols right (+x) | `x = 0`     | `oX -= 1`|
| Right        | slide left       | col `x=0`  | cols left (−x)  | `x = 12`    | `oX += 1`|

### 2.2 Shift (Forward shown; others symmetric)

```
function shiftForward():
    worldOriginY -= 1
    for x in 0..12: enqueueDrop(grid[x][12])          // old edge sinks out
    for y from 12 down to 1:                           // shift rows down (high→low)
        for x in 0..12: grid[x][y] = grid[x][y-1]
    for x in 0..12:                                    // generate new row at y=0
        t = generateTile(worldOriginX + x, worldOriginY + 0, startZ = -1.0)
        grid[x][0] = t; enqueueRise(t)
```

`shiftBackward`/`shiftLeft`/`shiftRight` mirror this with the opposite iteration
order so each source cell is read before being overwritten.

### 2.3 Memory-safe array manipulation

- No reallocation per move; the backing arrays are reused, only references move.
- Discarded edge tiles are detached from `grid`, pushed to `droppingTiles`, and
  freed only when their drop animation completes (§5).
- Surviving tiles keep their `id` and absolute `(x,y)`; never re-ID them.

---

## 3. World Content: Tiles, Objects, Background

### 3.1 Deterministic RNG

Randomness is derived from a **hash of absolute world coordinate + world seed**,
not an advancing stream, so a tile/object is identical regardless of the path
taken to reach it. The implementation uses a 64-bit splitmix-style hash
(`hash64`) reduced to a float in `[0,1)` (`rand01(seed, gx, gy, salt)`); a `salt`
distinguishes independent draws at the same coordinate.

### 3.2 Tiles — open space by default

```
TileType = { GROUND, METAL, HAZARD, EMPTY, BOOST, SPACE }
```

The base layer is **uniform open space**: `pickType()` always returns `SPACE`.
The other types (deck plating, alloy, reactor vent, void, warp pad) retain full
sprite styling and detail rendering and are kept for future use, but are not
generated by default. Each type has a `TILE_STYLE` entry (top/side/edge colours,
optional `glow` accent, and a label).

`generateTile(absX, absY, startZ)` returns `{ id, x:absX, y:absY, type, height:0,
worldZ:startZ, targetZ:0, anim:null }`. `id` is a monotonic global counter.

### 3.3 Object layer — the fixed sector catalogue

> **Current design (pocket layout):** the world is a finite circle (radius
> `MAP_RADIUS` = 100) whose object catalogue is built once from a constant
> `MAP_SEED` by `buildMap()` into `MAP_OBJECTS`; `collectObjects()` windows that
> fixed list to the visible 13×13 view (+ margin). The **four themed zones are
> distinct disc POCKETS in the four quadrants** (`ZONES` = `{region,cx,cy,r}`:
> Nebula NW · Moon NE · Armada SE · Nexus SW) around a central **open-space hub**
> where the player spawns (`SPAWN {0,0}`). `regionAt(ax,ay)` returns the pocket a
> tile is inside, else `REGION.OPEN` (the void), else `OUTSIDE`. `STORY_TARGETS`
> are the pocket centres, so the story route loops through all quadrants instead
> of a straight radial line. (Earlier builds used concentric rings + a rim spawn;
> that's fully replaced.) `buildMap` clusters each zone's objects around its
> pocket via a `scatter()` helper, plus landmark planets + light debris in OPEN.

```
OBJ = { NONE, PLANET, ASTEROID_S, ASTEROID_L, STATION,
        CRYSTAL, WRECK, WARSHIP, MOON, NEXUS }
OBJ_FOOTPRINT = { PLANET:4, ASTEROID_S:1, ASTEROID_L:2, STATION:1,
                  CRYSTAL:2, WRECK:1, WARSHIP:2, MOON:7, NEXUS:8 }   // square tiles
```

`buildMap()` places: one `NEXUS` at the core (0,0); a lattice of ~245 `WARSHIP`
hulls (r 24–50); one `MOON` plus a belt of `WRECK`/`STATION` debris (r 52–78);
a `CRYSTAL`/`STATION`/`ASTEROID_S` field in the nebula (r 78–100); and two
landmark `PLANET`s in the outer nebula. Each object carries `variant` (0–1, hashed
per placement) and `hue`, used for per-instance rotation / flip / colour.

**Rendering — custom sprites with procedural fallback.** Objects render as **flat
billboards centred on their tile** (they are *not* skewed into the iso plane).
`drawObject` dispatches to `drawPlanet` / `drawAsteroid` / `drawStation` /
`drawCrystal` / `drawWreck` / `drawWarship` / `drawMoon` / `drawNexus`. Each of
these loads a player-provided PNG from **`Assets/space/`** and, if the image is
loaded, blits it scaled to the object's footprint (`<TYPE>_SCALE` tunable per
draw fn); if not, it falls back to the procedural drawing (`drawXProcedural`).
Sprites are transparent-background cutouts (~1200×896). Notes:

- **Asteroid** — one `Astroid.png` serves both `ASTEROID_S` (scale 1) and
  `ASTEROID_L` (scale 2), varied by a small tumble + horizontal flip.
- **Warship** — dormant top-down capital ship; each lattice ship gets a full
  **random heading** (`variant·2π`) so the armada reads as a scattered dead fleet.
- **Station / Wreck** — comm satellite / torn hull fragment, each with its red
  beacon baked into the art.
- **Nexus** — two layers (`Nexus_dormant.png` + `Nexus_active.png`) cross-faded by
  the `nexusWake` state (see §3.5); the tiered fortress fires an energy beam when
  awake. `NEXUS_BB` holds each layer's measured content bounds so the differently
  framed arts align by base width + base bottom.

**Legacy procedural note.** The original design divided the world into 6×6 chunks
with one hashed object per chunk (`chunkObject`, type weights, in-chunk offset).
This is fully replaced by the fixed catalogue above; the `drawXProcedural`
functions are what remains of the old procedural appearance and now serve only as
the not-yet-loaded fallback.

### 3.4 Background — parallax starfield + nebula

Behind the grid, `drawBackground` paints a vertical gradient, three soft
nebula radial gradients, and a starfield of ~`w*h/2600` stars across three
parallax depths (`m = 0.25 / 0.5 / 1.0`). Stars twinkle (sine on alpha) and the
whole field drifts: a steady **ambient drift** keeps it cruising while idle, plus
`world.bgX/bgY` accumulate during moves at `BG_PARALLAX` (0.35) of the world's
displacement so the field slides with travel.

### 3.5 Command Nexus — dormant / awaken state

The core `NEXUS` object is **dormant** (dark, powered-down `Nexus_dormant.png`, no
beam) by default and only **awakens** for a battle at the core — energy surges and
the central beam fires (`Nexus_active.png`) — then returns to dormant once the
fight is won.

- `nexusAwake` — target boolean; `nexusWake` — eased 0→1, advanced at the top of
  `update()` (so it ramps smoothly even while the world is paused for combat/menus).
- `drawNexus` always draws the dormant layer, then fades the active layer in with
  alpha = `nexusWake · (0.82 + 0.18·sin)` (a subtle surge once awake).
- **Awaken:** `startCombat` sets `nexusAwake = true` when the fight is at the core
  (player within `NEXUS_WAKE_RANGE` = 10 tiles of (0,0), or `COMBAT_AT === "nexus"`).
- **Dormant again:** `winCombat` clears it (visible power-down during the win
  banner); `recenterAndExit` also clears it as a catch-all (it runs for won *and*
  lost).
- Because `render()` draws the world before the combat overlay, the awakened
  fortress and its tall beam show **behind the combat arena** during a core battle.

---

## 4. Animation System

All animations are delta-time based. State lives on `tile.anim` (rise/drop) or
on `world.lateral` (camera slide). Easings:

```
cubicOut(t)   = 1 - (1-t)^3        // rise
cubicIn(t)    = t^3                // drop
cubicInOut(t) = t<0.5 ? 4t^3 : 1 - (-2t+2)^3 / 2   // lateral slide
```

### 4.1 Rise / Drop (per-tile)

- **Rise:** new tile `worldZ` −1.0 → 0.0, 300 ms, `cubicOut`.
- **Drop:** outgoing tile `worldZ` 0.0 → −1.0, 250 ms, `cubicIn`; on completion
  the tile is removed from `droppingTiles` and freed. Dropping tiles fade via
  `alpha = clamp01(1 + worldZ)`.

### 4.2 Lateral camera slide (whole world)

On `beginMove`, `cameraOffset` is set to a one-tile start offset and eased to
`(0,0)` over 300 ms (`cubicInOut`), so incoming content slides in from the
correct edge with no pop:

```
Forward : start (+HALF_W, -HALF_H)
Backward: start (-HALF_W, +HALF_H)
Left    : start (-HALF_W, -HALF_H)
Right   : start (+HALF_W, +HALF_H)
```

Wandering ships are part of the world, so on move-start their base position is
advanced by the content displacement (`e.x -= startX; e.y -= startY`), and the
live `cameraOffset` is added at draw time so they slide smoothly with the world.

### 4.3 Input lockout / buffering

While a move animates, new input is **buffered** (at most one). The buffered move
fires once the lateral slide is done and no rise animations remain.

---

## 5. Tile memory rules

1. A tile leaves the grid at move-start; outgoing edge tiles are pushed to
   `droppingTiles` before being overwritten.
2. A dropping tile stays in memory and is rendered until its drop finishes.
3. On drop completion it is removed from `droppingTiles` and released; its `id`
   is never reused.
4. Never free a tile still referenced by the live grid.
5. Rising tiles are live grid members from the moment of generation.

---

## 6. Rendering Pipeline

Per frame: `drawBackground` → collect renderables → depth sort (§1.7) → draw
tiles → draw world objects → (free-roam) draw wandering ships then the player
ship and centre-tile marker → (combat) `drawCombat`. UI/HUD is HTML overlay.

- **Tile sprites** are pre-rendered once per type to offscreen canvases
  (`buildTileSprite`, 2× supersampled) and blitted; energy tiles (`glow`) add a
  shadow-blur halo. `showGrid`/`showIDs` overlay diamond outlines / tile ids.
- **Ship** (§6.1) is drawn after all tiles at `SHIP_ANCHOR` with a cosmetic sine
  bob and a soft shadow ellipse; it is never affected by `cameraOffset`.

### 6.1 Ship sprites & facing

The ship uses two PNG cutouts: `north east.png` (NE) and `south west.png` (SW).
The other two facings are horizontal flips:

```
FWD   -> NE            LEFT  -> NE flipped
BACK  -> SW            RIGHT -> SW flipped
```

`drawShip(cx, cy, dir, tint?)` renders at 96 px wide. An optional `tint`
(red/blue) recolours only opaque pixels via a cached `source-atop` fill, used for
wandering and enemy ships. If a sprite hasn't loaded it falls back to a rectangle.

---

## 7. Wandering Ships (free-roam)

Ships drift across the grid independently of the player, entering from an edge
and leaving on the far side.

```
TARGET_RED = 1, TARGET_BLUE = 2          // kept at a 2:1 blue:red ratio
ENEMY_SPEED_MIN = 11, ENEMY_SPEED_MAX = 18   // px/s idle drift
CHASE_SPEED = 60                          // px/s red homing speed
AGGRO_TILES = 8                           // red ships chase within this range
```

- **Red = hostile**, **blue = neutral.** Spawns are topped up every frame to
  maintain the target counts and ratio.
- Ships spawn on a random border cell and head inward along one of the four iso
  axes (`ISO_DIRS`); when they drift off the grid they are removed.
- **Aggro:** a red ship within `AGGRO_TILES` of the player charges at
  `CHASE_SPEED`. It commits to one iso axis for a **full tile leg** (`e.leg`)
  before re-aiming (`bestIsoDir`), so it staircases cleanly instead of jittering.
- **Engagement:** when a red ship comes within 46 px of the player's drawn
  position (accounting for the live `cameraOffset`), it triggers `startCombat()`.
  Blue ships never chase, never collide into combat, and never appear in a fight.
- `combatCooldown` (set to 5000 ms on combat exit) suppresses instant re-engage.

---

## 8. Turn-Based Combat

> **Combat model:** the player side is **crew-driven** — each turn the six crew
> take `ACTIONS_PER_TURN` actions via their face-circles (Maneuver, Lasers, Missile,
> Shield, Heal, Scan, Overclock, Tactics, …), aimed manually (§8.2). This replaced an
> earlier Phaser/Missile/Fire ship-button model; the sections below are current.
>
> **Per-hull enemies.** The six hostile hulls (Cyclops, Dread, Gunner, Neo, Tank,
> Wing) are no longer interchangeable: each has its own `SHIP_PROFILES` entry —
> `hp`, `moves`, `ammo`, `phaserDmg`/`missileDmg`, and AI doctrine fields
> `prefRange` (stand-off distance it steers toward), `rangeW` (how hard it holds
> that range vs. moving little), `missileBias` (reach for missiles first). The
> per-hull `moves`/`prefRange` drive `planEnemyMove`'s BFS reach and firing-tile
> scoring, and `enemyFire` uses per-hull damage. The `ENEMY_*` constants below are
> now fallbacks only.
>
> **Nexus boss fight.** A battle with hash `boss=1` (`BOSS_FLAG`) is the stationary
> three-phase **Command Nexus** boss — no ships. Its core + 3 shield generators are
> `combat.enemies` entries flagged `boss` (reusing weapon/aim/kill code); `combat.boss`
> holds phase/telegraph/overload state. Phase 1: core shielded → destroy generators.
> Phase 2: core exposed, boss telegraphs a beam lane (dodge). Phase 3 (core ≤40%):
> wider beam + overload turn-timer (race). Weak points render as glowing glyphs with
> grid-cell markers + a green "will-hit" aim highlight; the boss shows one amber core
> avatar. Tunables in `NEXUS_BOSS`; the fortress backdrop is framed by `NEXUS_ARENA_CELL`.
> See the project memory for the full boss spec.

Combat starts three ways: colliding with a wandering **red** ship in free-roam;
the episode loading the game with **`#mission`** (`&at=<zone>` stages the spawn,
`&enemies=<n>` forces a count, `&flee=1` scripts an intro retreat); or
**`#…boss=1`** for the Nexus fortress boss (§8.7). The world freezes and the 13×13
grid becomes the battle arena. Combat is **mouse-driven** (keys 1–6 / arrows /
Enter assist).

```
PLAYER_MAX_HP = 20 · ACTIONS_PER_TURN = 3 · START_AMMO = 3
LASER_DMG = 2 (Rex Lasers, 3×3 cone) · CREW_MISSILE_DMG = 4 (Rex Missile, line-5)
REPAIR_HP = 7 · SHIELD_PCT = 0.10 · INCAP_CHANCE = 0.25 · INCAP_TURNS = 2 · JAM_CHANCE = 0.5
Enemy stats & damage are PER-HULL (SHIP_PROFILES); the old ENEMY_* consts are fallbacks.
```

### 8.1 Setup (`startCombat`)

Normal battle: `n = clamp(redCount, 2, 4)` enemies on random tiles ≥3 (Manhattan)
from the centre, each assigned a random hull from `SHIP_PROFILES`; player at
`(6,6)`. A `boss=1` battle instead builds the **Nexus fortress** (§8.7) and no
ships. The grid is flattened, any in-progress move cancelled, and `combat.crew[]`
tracks each roster member's availability. Phases: `player → enemy → (player …) →
won | lost`.

### 8.2 Player turn — crew actions

Combat is **crew-driven** (this replaced the old Phaser/Missile/Fire ship model).
Each turn the six crew take **`ACTIONS_PER_TURN` (3)** actions. The right panel is
a 2×3 grid of **crew face-circles**; clicking a face (or keys 1–6) opens a small
**action picker** (`activateCrew`): **▶ USE** the crew's equipped ability, or
**⇄ Change** it (swapping is itself that crew's action). USE begins **manual
targeting** (`combat.targeting`), keyed off `ACTION_TARGET[name].kind`:

- **self** (Overclock, Repair, Shield) — applies immediately.
- **move / hop** (Maneuver, Space Hop) — click a tile, then a facing chevron; the ship **glides** (`startWalk`/`tickWalk`).
- **aim** (Lasers = 3×3 cone, Missile = 1×5 line) — click the grid to fire in that direction (`attackCells`; Overclock adds `bonus` +1 reach).
- **enemy** (Scan reveals HP/shield; Transmission jams the next action at `JAM_CHANCE`) — click a ship.
- **crew** (Heal revives an incapacitated crewmate; Adrenaline grants a 2nd action) — click a face.
- **role** (Voss **Tactics** — assume ANOTHER crew's role and use their action, **including incapacitated** crew).

Esc / right-click / clicking the acting crew cancels. `spendAction` marks the crew
done and decrements the budget; at 0 only **End Turn** remains. Each crew's ability
is `slot0` (a swappable pair): Astra Maneuver/Space Hop · Voss Tactics/Transmission ·
Rex Lasers/Missile · Tessa Overclock(+1 range)/Repair(+7 hull) · Selyra Heal/Adrenaline ·
Kael Scan/Shield(−10% dmg).

### 8.3 Enemy turn

Per-hull AI (see the banner above). Each ship acts one at a time, spotlighted:
`planEnemyMove` BFS-plans to a firing tile scored by its `SHIP_PROFILES` doctrine
(move little, steer toward `prefRange`), glides there, then fires per-hull damage
(`enemyFire`). A hit can **incapacitate** a crew member (`INCAP_CHANCE`, never the
last one; auto-revives after `INCAP_TURNS` player turns) — `player.shieldPct`
(Kael's Shield) softens it. The Nexus boss runs its own turn instead (§8.7).

### 8.4 FX

- `spawnShot`/`drawShots`: a fading phaser beam, or a missile bolt that travels
  from shooter to target (enemy shots drawn thicker).
- `spawnExplosion`/`drawExplosions`: an expanding shockwave ring, a hot radial
  core flash, and outward-flying debris (bigger for the player's death).

### 8.5 Resolution & exit

- **Win** (`winCombat`): "ENEMIES/MISSION" banner; on a `#mission` beat it posts
  `{type:"missionComplete"}` to the parent episode.
- **Lose** (`loseCombat`): player ship explodes, "SHIP DESTROYED"; on exit the game
  posts `{type:"defeated"}` so the episode shows its game-over screen.
- `recenterAndExit` slides the grid so the player's combat tile becomes the new
  centre (origin updated, grid regenerated), eases the camera back, sets
  `combatCooldown = 5000` (≥5 s no re-engage), respawns wanderers, resumes free-roam.

### 8.6 Combat UI

Right-side panel (`combatPanelLayout`): turn header, **HULL / ACTIONS / SHIELD**
stats, the 2×3 **crew face-circles** (dimmed + ✓ when spent, a revive-countdown
number when incapacitated, accent / green-target / gold-active rings), and the
**End Turn** button. A bottom-right **guidance pill** (`drawPill`) states the
current step; a top **turn-order bar** (`drawTurnOrder`) shows play order with HP
rings and cross-highlights the hovered ship. Banners announce COMBAT! / ENEMY TURN
/ YOUR TURN / phase changes; HP bars float over each ship. (Testing Mode adds a
bottom-left **SKIP** button.)

### 8.7 Nexus boss fight

A `boss=1` battle is the stationary three-phase **Command Nexus** boss (no ships).
Its **core + 3 shield generators** are `combat.enemies` entries flagged `boss`
(reusing the weapon/aim/Scan/kill pipeline); `combat.boss` holds phase / telegraph
/ overload state; all numbers live in `NEXUS_BOSS`. **Phase 1** — the core is
shielded/invulnerable (`fireCrewWeapon` skips damage to it) → destroy the
generators. **Phase 2** — core exposed; the boss **telegraphs a beam lane** down
the player's column, firing it next turn (dodge with Maneuver/Space Hop) while you
damage the core. **Phase 3** (core ≤ 40%) — the beam widens to three columns and an
**overload turn-timer** starts (a full-arena blast after `overloadTurns`) → race to
kill the core. Weak points render as glowing glyphs with per-cell grid markers and
a green **"will-hit"** aim highlight; the boss shows one amber **core avatar** in the
turn bar. The awakened fortress art is the backdrop, framed by `NEXUS_ARENA_CELL`.

---

## 9. Data Structures (as implemented)

```
world = {
  grid[13][13],                 // grid[x][y] of Tile
  worldOriginX, worldOriginY,   // absolute coord of array cell (0,0)
  moving, currentMove, bufferedMove,
  lateral,                      // {elapsed, dur, startX, startY, ease} | null
  cameraOffsetX, cameraOffsetY,
  droppingTiles[],              // tiles animating their exit
  shipBobPhase, shipFacing,     // cosmetic bob + which sprite/orientation
  bgX, bgY,                     // accumulated starfield parallax
}

Tile  = { id, x, y, type, height, worldZ, targetZ, anim }
anim  = { kind:"rise"|"drop", elapsed, dur, start, end, ease }

enemy (free-roam) = { x, y, vx, vy, facing, bob, hostile, leg? }

combat = {
  phase, turn, movesLeft, selectedWeapon,
  player  = { gx, gy, vgx, vgy, walk, facing, hp, maxhp, ammo },
  enemies = [{ gx, gy, vgx, vgy, walk, facing, hp, maxhp, ammo, bob }],
  flashes[], explosions[], shots[], log[], banner, ai, endTimer
}
walk = { path:[{gx,gy}...], prog }       // sprite glide state
```

---

## 10. Update Loop

```
update(dt):
  tick rise/drop on all grid + dropping tiles
  if lateral:   ease cameraOffset → 0; drift bgX/bgY; clear when done
  cleanup finished dropping tiles
  if move complete (no lateral, no rises left): clear moving; fire buffered move
  advance shipBobPhase; decay combatCooldown
  if combat:  tickCombat(dt)            // glides, FX, banners, enemy AI machine
  else:       updateEnemies(dt)         // drift, aggro, top-up, collision→startCombat
```

`render()` branches: in combat it calls `drawCombat` and returns; otherwise it
draws wandering ships, the player ship, and the centre-tile marker.

---

## 11. Controls

**Free-roam:** Arrows / WASD = move · `M` / `Enter` = open the **Starship Menu** (pauses the game;
Ship Status · Ship Config · Star Map · Missions · Options — only Star Map & Missions functional) ·
`R` = return to spawn · `I` = toggle tile ids · `G` = toggle grid outlines.

**Objective prompt:** reaching a story waypoint raises a "Progress the story?" panel (pauses the game):
`Y` / Enter / click YES to continue; `N` / Esc / click NO to turn 180° and back off three tiles.

**Combat (mouse-driven):** click a reachable tile to move · click Phaser/Missile
to select (shows range) · click Fire to shoot · click End Turn to pass. Keyboard
assists: Arrows/WASD = facing · `1` = phaser · `2` = missile · `F` = fire ·
`Enter` = end turn.

---

## 12. Implementation status

The prototype implements all of the above in one file, `iso_grid_prototype.html`:
the moving-world engine (§0–6), deterministic space/object generation (§3), the
parallax background (§3.4), wandering-ship AI (§7), and the full mouse-driven
turn-based combat with enemy AI and FX (§8).

**Added since v2.0 (driven by `episode1.html` embedding):** a pause **Starship Menu** (`M`) with a
**Missions** log and **Star Map**; an objective **"Progress the story?"** prompt; **scripted mission
combat** (`#mission` starts the battle immediately, with params `at=<zone>` / `enemies=<n>` / `flee=1`);
and **persistence** across the per-segment reloads — player position via the embed hash (`start=ax,ay`)
and **fog-of-war** via `localStorage`. The menu and the prompt both fully pause the game.

**Not yet present / possible next steps:** terrain/tile gameplay (all tiles are open space today),
object collision or interaction (planets/stations are purely visual), and sound.

---

*End of specification.*
