# StarGear — v0.6 Devlog

Running log of v0.6 work. Newest entries at the bottom of each section. v0.5 shipped fully
playtested (see `DEVLOG-v0.5.md`); v0.6 opens the untriaged feedback backlog — starting with
player-set navigation, the most-requested item across both playtesters.

---

## Custom waypoints — DONE (2026-07-24), Playwright-verified

**Ask:** "the ability to add / remove a custom waypoint. it should auto remove when you reach it."
(Steve). Player-set navigation — "waypoints / course-setting" topped both Brett's and Steve's
v0.4 feedback lists.

**Design decisions (locked with Steve):**
- **Place/remove by clicking the Star Map.** Click empty space to drop it, click the mark to
  remove it. One waypoint at a time; a new placement replaces the old.
- Map now closes via the **Back button + Q/M/Esc** (it used to close on *any* click — that had to
  change so a placement click doesn't also dismiss the map).
- **Auto-clears on arrival** — no prompt, unlike the story/bounty marks; flying onto it just
  deletes it.
- **Persists across Save/Load** (snapshot bumped `v:4 → v:5`; old saves default to no waypoint).
- Violet (`196,142,255`), distinct from objective green / bounty amber / station blue.

**Implementation (all in `iso_grid_prototype.html`):** rides the existing marker machinery —
`drawWorldMark` gives the in-world crosshair + off-screen rim arrow for free; the Star-Map diamond
+ course line and the mini-map pip are copy-swap-color from the bounty blocks. New state
`customWaypoint = {ax,ay}` + `setWaypoint`/`clearWaypoint`; the Star-Map click handler now tests the
Back-button rect first (close), then inverts the disc transform to place/toggle a waypoint; the
disc transform is stashed in `_mapDisc` each draw. Auto-remove is a `Math.hypot <= 1.5` check in
`update()` after the bounty block. Save snapshot bumped `v:4 → v:5` with a `waypoint` field.

**Verified** over `http://localhost:8123` with Playwright, `pageerror` clean: place at exact clicked
tile · placing doesn't close the map · re-click toggles off · Back button closes and the waypoint
survives · in-world crosshair + off-screen rim arrow + violet mini-map pip · save `v:5` carries and
restores it · a pre-v5 save loads clean with no waypoint · flying within 1.5 tiles auto-clears it.

**Gotcha for future click tests:** the first-flight tutorial is a **DOM overlay** (`#tut.show`), not a
canvas thing — setting the JS `tutorialOpen` flag doesn't hide it, so it intercepts real mouse
clicks over the map. Call `closeTutorial()` (drain the queue) to dismiss it before driving map clicks.

_Status: done — **human-playtested by Steve 2026-07-24, PASS.** Feel calls left open (Steve OK'd as-is
for now): violet vs. station-blue at a glance, and `WAYPOINT_ARRIVE_DIST = 1.5` (story objective uses 1)._

---

## Confirm end-turn with unspent actions — DONE (2026-07-24), Playwright-verified

**Ask:** Brett's v0.4 feedback — "Confirm prompt when ending turn with unused actions." Ending a
combat turn (End Turn button or Enter) was instant; easy to burn a turn with crew who could still act.

**Design decisions (locked with Steve):**
- **Fires only if a crew member could actually still act** — uses the existing `canCrewAct(i)`
  predicate (folds in actions-remaining, not incapacitated/offline, not already-acted). Never nags
  when the leftover points are unusable, so you're never forced to click through a pointless prompt.
- **Defeatable** via a new Options toggle **"Confirm End Turn"** (default ON, persisted in
  `stargear_confirmend_v1`), mirroring the Tutorial Tips / Testing Mode toggles.

**Implementation (all in `iso_grid_prototype.html`):** a Y/N modal `drawEndTurnConfirm()` copied from
`drawDockPrompt` (amber accent, "END TURN (Y)" / "KEEP GOING (N)"), drawn topmost in the combat
render branch. A transient `combat.confirmEnd` flag + `hasUsableAction()` / `tryEndTurn()` helpers;
both end-turn call sites (button, Enter) route through `tryEndTurn`, which raises the modal or ends
outright. The modal owns clicks + keys while up (Y/Enter confirm, N/Q/Esc dismiss); the flag is
cleared in `endPlayerTurn` so it can't leak into the enemy phase. Options panel grew `412 → 472px`
for the third toggle row.

**Verified** over `http://localhost:8123` with Playwright, `pageerror` clean: button raises the
confirm · YES ends / NO keeps (budget intact) · no prompt when actions are exhausted or all crew have
acted · toggle OFF ends directly (and persists) · Enter raises + Y ends + Esc dismisses (keyboard
path) · Options shows three toggle rows incl. `confirmend`. Screenshots: modal over the arena, and
the Options panel un-clipped at 1000×600.

_Status: done — **human-playtested by Steve 2026-07-24, PASS.** Feel calls left open (Steve OK'd
as-is): "KEEP GOING" wording, and amber accent vs. the green dock prompt._

---

## Fit modules while docked — DONE (2026-07-24), Playwright-verified

**Ask:** Brett's v0.4 feedback — "Option while docked to open the modules/Configuration screen to fit
a new part." The station MODULES tab only *bought* a part (into `shipOwned`); the fit-grid was
reachable only from the pause menu → Ship → CONFIGURATION, so you had to undock to fit what you'd
just bought. The buy message literally said "Fit it in Ship Config."

**Design decision (locked with Steve):** trigger = a **"⚙ Fit Modules" row at the top of the MODULES
tab**, right where parts are bought.

**Implementation (all in `iso_grid_prototype.html`):** the dock screen and the fit-grid are already
sibling `menuView`s (`"station"` / `"shipConfig"`) under one `menuOpen`, so this reuses the entire
Configuration screen untouched — it just routes between them, mirroring the existing `mapFromMenu`
return-target pattern. New `shipCfgFromDock` flag; a `"⚙ Fit Modules"` MODULES row whose
`stationAction("config")` switches `menuView` to `"shipConfig"` (same init as the menu's Ship entry);
both fit-grid back-outs (Back button + Esc/Q/M) return to `"station"` (MODULES tab) when the flag is
set, else to root; back-button label reads **"◀ STATION"**; `bgmWanted()` hardened to keep the dock
track in the sub-screen; `undock()` clears the flag. Buy message updated to point at the new row.

**Verified** over `http://localhost:8123` with Playwright, `pageerror` clean: Fit Modules is the top
MODULES row · opens the fit-grid still docked · **buy→fit end-to-end** (a part bought at the dock
appears in the fit inventory and can be placed onto `shipLoadout`) · Esc + Back both return to the
dock MODULES tab (not root) · undock clears state · dock music holds in the sub-screen · no stale
station confirm survives the round-trip. Screenshots: MODULES tab with the new row, and the fit-grid
opened from the dock ("◀ STATION" back button).

_Status: done — **human-playtested by Steve 2026-07-24, PASS.** Feel calls left open (Steve OK'd as-is):
"⚙ Fit Modules" wording, and returning to the MODULES tab vs. the dock's first tab._

### Follow-up: can't remove a cargo hold you're still using (2026-07-24, Playwright-verified)
Steve spotted the edge case: removing a hold module while carrying more than the reduced capacity
would allow left the ship over capacity (and let you sell the hold module for coin while keeping the
cargo). Now **blocked at every removal path**:
- **Station Sell** (`sellmod`) — refuses a cargo module when `cargoUsed() > cargoCap() − its cargo`,
  with a "Can't sell … Sell cargo first." message.
- **Fit-grid uninstall** — centralized into a new `dropGhost()` used by all three drop points
  (Esc/Q, tab-switch, Back button). Picking up a load-bearing hold and dropping it **snaps it back**
  to where it came from (pickup stores `from` on the ghost) and flashes an amber footer note
  (`scfgMsg`/`scfgFlash`). Repositioning (net-zero pick-up-and-replace) is unaffected; a normal
  uninstall still works when the hold isn't over capacity.
Verified: sell blocked over-cap / allowed under-cap · fit-grid drop snaps back + flashes (incl. real
Esc) · repositioning works · normal uninstall works · `pageerror` clean.

---

## Objective pinning — one primary objective on the HUD (2026-07-24, Playwright-verified)

**Ask:** Steve's v0.4 ask. One **primary objective** shown on a persistent HUD panel so you always
know what to chase next and how far along a collect/kill step is. Rules (Steve): one at a time; story
pinned by default; ask "make this primary?" when you pick up a new objective; the pin follows a chain
(side-mission steps); **unpin entirely when the chain ends** (Steve's call, even if the story is still
active); the player can unpin the story default; show the `N/M` counter for collect-N / do-N steps.

**Implementation (all in `iso_grid_prototype.html`):** the pin is a lightweight reference
`primaryObjective = { kind:"story"|"side"|"bounty", id? }` resolved **live** each frame by
`primaryInfo()` — so counters and step advances stay authoritative in the existing mission systems
(no copied state). Mirrors the `customWaypoint` pattern.
- **HUD panel** `drawPrimaryObjective()` — right edge, **vertically centred** in the visible area
  (between the SCRAP/COIN chip and the mini-map; Steve's placement, after trying top-left then
  under-the-chip). Shows the label, `stepProgressText` counter (`"3 / 10"`), and `bearingTo(target)`
  distance/heading, tinted by kind (story green / side green / bounty amber).
- **"Make primary?" prompt** `drawPrimaryPrompt` (clone of `drawObjectivePrompt`) raised at
  `acceptSide`/`acceptBounty`. It renders **above the pause menu** and its input is intercepted at the
  **top** of the click/keydown handlers, so it works while docked (objectives are accepted at a station).
- **Chain follow / unpin** — side steps advance automatically (the resolver re-reads
  `activeSideStep()`); `completeSide`/`completeBounty` `clearPin()` when the pinned one finishes.
- **Persistence** — new `stargear_pin_v1` key (continuation-gated like sides/bounties). An **absent**
  key = "never touched → default story"; a **stored `null`** (player unpinned) is respected and
  persists, so the story default doesn't creep back and a pure story run stays pinned across reloads.
  Save snapshot bumped **v:5 → v:6** (`pin`); `normalizePin()` drops a pin whose objective is gone.
- **Controls** — Missions view: a 📌 PIN/PINNED toggle on the tracked side/bounty row, and a 📌 PIN
  STORY / UNPIN STORY control on the STORY tab.
- **In-world arrows limited to the primary + waypoint (Steve, 2026-07-24):** **every** objective
  still shows its crosshair in space, but only the **pinned** objective and the **custom waypoint**
  get an **off-screen rim arrow** pointing to them. Done by adding an `arrow` param to `drawWorldMark`
  (off-screen branch draws the rim arrow only when `arrow` is true); `drawBountyMarker` passes
  `isPinned("bounty", id)` / `isPinned("side", …)` per objective, and `drawObjectiveMarker`'s
  off-screen branch is gated on `isPinned("story")`. A non-pinned objective that's off-screen simply
  draws nothing until you approach; its on-screen crosshair is unchanged. The Star Map (all marks +
  course lines) and the mini-map (all pips) are unchanged. Verified: an unpinned bounty shows its
  crosshair on-screen with no edge arrow, while the pinned story shows its rim arrow off-screen.

**Verified** over `http://localhost:8123`, `pageerror` clean: story pinned by default (label +
distance, no counter) · accepting a job raises the prompt over the station and PIN IT pins it (real
click) · the counter shows `18 / 40` and follows `tickSides` to the next step · completing the
chain unpins entirely with the story still active · bounty pin→complete unpins · unpinning the story
persists as `null` · save/load round-trips the pin and `normalizePin` drops a stale one. Screenshots:
HUD panel (story + side-with-counter), the prompt over the station, the Missions row + STORY-tab
controls.

_Status: done — **human-playtested by Steve 2026-07-24, PASS** (incl. the right-centre panel placement
and the arrows-only-for-primary+waypoint refinement). Unpin-entirely-on-chain-end OK'd as-is._

---

## Cargo capacity +30% (2026-07-24)

Steve's v0.4 ask ("the hold felt tight — goods and scrap share it"). `CARGO_BASE` **40 → 52** (+30%),
the single source everything else computes from via `cargoCap()`. A fresh ship (with its default
Cargo Hold +30 fitted) now holds **82** (was 70); module bonuses (Cargo Hold +30 / Pod +15 /
Expanded +45) unchanged. Verified: `cargoCap()` returns 82 on a fresh boot, `pageerror` clean.

---

## Unscanned-hull indicator in space (2026-07-24, Playwright-verified)

From Brett's "show which ships have/haven't been scanned." Discussed with Steve and narrowed: the
**combat** indicator is redundant (an enemy's `HP/SHLD` readout already appears *only once scanned*),
so we do the useful half in **free-roam** — a small pulsing cyan **"?"** above a hostile whose hull
isn't in the codex yet, a nudge to scan it (feeds *Know Your Enemy*). **Unscanned hulls only**;
catalogued hulls show nothing. Feasible because a wanderer's hull is fixed at spawn, so `isScanned(e)`
is already correct in free-roam — **no new state/persistence**, purely derived.

**Implementation (all in `iso_grid_prototype.html`):** new `UNSCANNED_RGB` cyan + `drawUnscannedTag()`;
one line in `drawEnemies` after the sprite draw — `if (e.hostile && !isScanned(e)) drawUnscannedTag(ex, ey-42)`
using the ship's own camera-corrected position so the badge tracks during glides. `drawEnemies` isn't
on the combat path, so nothing appears in the arena. Added a line to the SCANNING first-time tip
explaining the glyph.

**Verified** over `http://localhost:8123`, `pageerror` clean: an uncatalogued hostile shows the "?";
`discoverShip(hull)` (or a scan) hides it (`isScanned` → true); catalogued hulls never badge; combat
unchanged. Screenshots: "?" above an unscanned hostile, and the same hull after cataloguing (no badge).

_Status: done — **human-playtested by Steve 2026-07-24, PASS.** (Also investigated a "no enemies in
free-flight" report same session: A/B-probed v0.5 vs v0.6, identical sparse behaviour — not a
regression from any v0.6 change. The free-roam encounter-rate weakness is pre-existing; **Steve
REJECTED addressing it (2026-07-24)** — leave the patrol tuning as-is.)_

---

## Star Map station hover tooltip (2026-07-24, Playwright-verified)

Previously **rejected** ("station hover info"); Steve revived it with a specific angle — hover a
station on the Star Map to see a trade tip. Locked with Steve: **based on prices you've actually seen**
(`marketIntel`, so unvisited stations just prompt "dock to learn"), and **includes the keeper name**.

**Implementation (all in `iso_grid_prototype.html`):** in `drawMapView`'s station loop, a per-station
hover test (`Math.hypot(mouseX-sx, mouseY-sy) <= 12`, using the existing canvas `mousemove` globals) —
the hovered station also brightens. After the header, `drawStationTip(st, sx, sy)` draws a `techPanel`
tooltip (clamped/flipped to stay on-screen, styled after the combat action-hover tooltip): station
name + `Keeper — <name>` (in the keeper's accent) + trade tips from `stationTip(st)`. Tips derive from
**observed** `marketIntel` prices, **normalised by each commodity's base** so "Cheapest to buy" /
"Best to sell" reflect the station's character, not just the cheapest good by nature; **the actual
price numbers are NOT shown** (Steve, 2026-07-24 — just the commodity name), plus a `market seen <age>`
line via `intelAge`. Hover uses `mouseX/mouseY`; no new listener. Star-Map click still sets a waypoint
(hover ≠ click, no conflict).

**Verified** over `http://localhost:8123`, `pageerror` clean: hovering a seeded/visited Hub shows
"Waypoint Hub / Keeper — Marla Quen / Cheapest to buy: Raw Ore / Best to sell: Nebula Relics / market
seen just now" (no prices); an unvisited station shows "Keeper — Oris Vale / No prices yet — dock to
learn."; the builder returns the right lines for seen vs unseen. Screenshots of both.

_Status: done — **human-playtested by Steve 2026-07-24, PASS.**_

---

## Defect fix: Star Map didn't pause the world (2026-07-24, Playwright-verified)

Steve: had the Star Map up and enemies kept moving and *initiated combat* — the menu/map is meant to
freeze the world. Root cause: `update()`'s pause guard listed `menuOpen || objectivePrompt ||
dockPrompt || tutorialOpen` but **not `mapOpen`** — and opening the Star Map sets `menuOpen = false;
mapOpen = true`, so the world (enemy movement + the collision→`startCombat` check) kept ticking under
the overlay. Fix: add `mapOpen` to the guard. Verified: with a hostile 1 tile away, opening the map
freezes it and no combat starts; closing the map resumes and it collides as normal. `pageerror` clean.
**Confirmed fixed by Steve 2026-07-24.**

---

## Ruling: N6 "Know Your Enemy" — INCLUDE (2026-07-24)

Steve ruled the achievement keeps all 11 codex hulls — **including the Nexus and the Hound** — so
100% is finale-gated and requires scanning a Hound inside the Red Reaver fight. No code change
(`KNOW_YOUR_ENEMY_TARGET = DEX_ENTRIES.length` already reflects this); comment updated to record the
ruling. N6 is closed.

---

## Ruling: A6 crew action-menu skip — LEAVE AS-IS (2026-07-24)

`activateCrew`'s `crewAvailableIdxs(c).length <= 1` early-out (a single-option crew fires immediately,
skipping the action popup) stands. Steve confirmed keeping it — the extra click every routine turn
isn't worth the discoverability gain. Revisit only if the "abilities aren't discoverable" feedback
recurs. A6 closed as WONTFIX.

---

## Ruling: Mix playtest — ACCEPT AS-IS (2026-07-24)

Steve accepted the current audio mix as final for v0.6 — the hand-tuned `SFX_VOL` levels and the
code-side length caps (`SFX_MAXMS`, covering the over-long `ui_select`/`scrap`/`laser`/`explode`)
stay. No re-balance pass, no regenerating shorter clips. Closed.

---

## Ship parts — modules for all six crew (2026-07-24, Playwright-verified)

TODO "Ship parts / more modules." Steve's brief: give the three crew that lacked fit-grid modules
(Voss, Tessa, Selyra) their own — 2 per crew. Chosen model = **hybrid**: hard-gate the four *utility*
abilities, keep the two *recovery* abilities (Repair/Heal) always-on with an **enhancer** module each.
Ownership rule (Steve): a module required for an ability the crew already has must be **free**; genuinely
new upgrade modules are **purchases** — which maps exactly to the existing price-based ownership
(`shipOwned = SHIP_MODULES.filter(m => !m.price)`), no special-casing.

**6 new modules (all in `iso_grid_prototype.html`):**
- **Gate modules (free / standard kit)** — `command` (Voss Tactics), `comms` (Voss Transmission),
  `overclock` (Tessa Overclock), `stim` (Selyra Adrenaline). Distinct colors (Voss steel-blue, Tessa
  copper, Selyra rose) + shapes; procedural, no art.
- **Enhancer modules (bought at a station, `price:300`)** — `repairbay` (Tessa) and `medbay` (Selyra),
  which carry a **`boosts`** field instead of `action`. Repair Bay: Repair mends **7 → 12** hull while
  powered. Med Bay: Heal also patches **+4 hull** while powered.

**Mechanism — no gating rewrite needed.** Added all six crew to `SHIP_CREW`; `shipActionPowered`
already returns "available" for any action with **no** gate module, so Repair/Heal (whose modules use
`boosts`, not `action`) stay always-on, while the four gated abilities go offline if their module is
removed/unpowered. Enhancer effects read `moduleActive("repairbay"/"medbay")`. Ship Config footer
denominator fixed (`10 / 10`, was hardcoded `/ 6`). **Save migration:** `ensureDefaultOwned()` +
`placeMissingDefault()` at both load sites so a pre-v0.6 run gains the 4 new gate modules (owned +
auto-fitted) rather than leaving a crew mid-ability.

**Verified** over `http://localhost:8123`, `pageerror` clean: fresh loadout auto-places all 11 default
modules (grid fits); enhancers not owned by default; gated abilities powered by default and go OFFLINE
when their module is pulled; Repair/Heal always available; Voss goes offline only with both gates gone
while Tessa/Selyra never do; Repair 7→12 with Repair Bay powered; shop lists Buy Repair Bay / Buy Med
Bay; old-save migration owns+places the 4 gates. Screenshots: fit-grid (12 modules, "10/10 powered")
and the MODULES shop.

_Status: done — not yet human-playtested. Feel calls for Steve: the two enhancer numbers (Repair +5,
Med Bay +4 hull), the 300-coin price, and the module colors/shapes._

---

## Ship parts II — a new third combat action per crew (2026-07-24, Playwright-verified)

Steve: "one more module per crew" → and (after rejecting enhancers) "I want **new actions**." So each
crew gets a brand-new **third swappable ability**, unlocked by a **purchasable** gate module (new
action = purchase). A crew without the module keeps its two abilities; buy + fit the module and the
third joins the ⇄ swap. Delivered as a 3rd Slot-1 option — the locked Slot 2/3 UI rows (a separate
"second simultaneous slot" idea) are untouched.

**The six new abilities** (Voss's went through a revision — original "Rally" was too like Tactics, so
Steve picked **Focus Fire**):
- **Astra · Evasive Roll** (self) — this enemy turn each incoming hit has a 50% chance to miss (`p.dodge`).
- **Rex · Railgun** (aim) — piercing shot down the full line, `RAILGUN_DMG 8`.
- **Kael · Disruptor Pulse** (enemy) — guaranteed: target enemy skips its next action (`e.skipTurn`).
- **Voss · Focus Fire** (enemy) — mark an enemy; crew attacks deal +50% damage to it this turn (`e.marked`, `MARK_MULT 1.5`).
- **Tessa · Vent Plasma** (self) — damages every enemy in the 8 squares around the ship (`VENT_DMG 4`).
- **Selyra · Triage** (self) — revive ALL incapacitated crew at once.

**Mechanism (all in `iso_grid_prototype.html`):** 3rd `{name,desc}` per crew in `slot0.options`;
`ACTION_TARGET` entries; effects wired into `applySelfAction` / `applyAim` / `applyEnemyTarget`; two
new `attackCells` patterns (`railgun` full-line, `vent` 8-around); the mark multiplier in
`fireCrewWeapon`'s damage line (so any crew weapon benefits); dodge consumed in both player-damage
sites (`enemyFire` + `bossHitPlayer`); `p.dodge` + all `e.marked` cleared at the round reset. Six
priced gate modules (350 coin) — being priced they're shop-only and `shipActionPowered` gates each
new option automatically; no migration (new content, old saves just lack them). Ship Config footer
now counts **owned** action modules (`shipOwned.has`), so unbought modules don't read as "offline."

**Verified** over `http://localhost:8123`, `pageerror` clean: new abilities locked by default; each
unlocks when its module is fitted+powered; Rex gains a 3rd swap option; Focus Fire does 1.5× damage
on a marked enemy; Evasive Roll sets dodge; Disruptor Pulse stuns; Triage revives all; Vent Plasma +
Railgun deal damage through the real pipeline; round reset clears dodge+marks; removing a module
re-locks its ability. Screenshots: MODULES shop (6 new "Buy …" rows) and Rex's combat action menu
showing Railgun equipped with ⇄ Switch over three abilities.

_Status: done — **human-playtested by Steve 2026-07-24, PASS.** Numbers/price OK'd as-is
(`DODGE_CHANCE 0.5`, `MARK_MULT 1.5`, `RAILGUN_DMG 8`, `VENT_DMG 4`, 350 coin)._

---

## Per-station module shops + shape preview + draggable Ship-Config scrollbar (2026-07-24, Playwright-verified)

Three requests from Steve, all in `iso_grid_prototype.html`:

**1. Each station sells DIFFERENT modules.** The MODULES tab used to list every unowned module at
every station. Now a `STATION_MODULE_STOCK` map gives each station an exclusive, themed subset —
**Hub**: Cargo Pod / Repair Bay / Fire Director · **Veil Anchorage**: Disruptor Array / Med Bay /
Triage Bay · **Quarry**: Expanded Hold / Plasma Vents / Evasion Thrusters · **Salvage Reach**: Armour
Plating / Railgun Mount. The buy loop filters to `stationBuyableMods(sid)`. Selling stays universal,
and — Steve's call — a station **re-sells anything you sold there**: `stationSoldMods[sid]` is recorded
on `sellmod` and unioned into that station's buy list, so a sale is always reversible on the spot.
Persisted like `marketIntel` (`SOLDMODS_KEY`, continuation-gated + in the save blob).

**2. Module shape preview in the shop.** Each MODULES row now draws the part's polyomino ("tetris")
footprint in its module colour, in the row's left slot (reusing the bounty-mugshot layout offset), so
you see what a part will occupy before buying. New `drawModuleShape(mod, x, y, box)`; rows carry a
`modId`.

**3. Draggable Ship-Config scrollbar.** The inventory scrollbar was display-only (wheel/arrows). Now
its geometry is stashed each draw (`_scfgScrollbar`); a `mousedown` on the track grabs it
(`_scfgDragging`), `mousemove` maps the cursor Y to `scfgScroll` (`scfgScrollToY`), and a window
`mouseup` releases. Clicking the track jumps the thumb there. Thumb brightens while dragging.

**Verified** over `http://localhost:8123`, `pageerror` clean: each station lists only its own stock and
they differ; railgun is exclusive to Salvage Reach; buy-at-Salvage → sell-at-Hub → Hub re-buys it, and
that memory survives save/load; shop rows show the correct shapes (screenshot); dragging the scrollbar
thumb to the bottom sets `scfgScroll` to max and to the top sets 0, releasing on mouseup. Screenshots:
Hub vs Salvage Reach MODULES tabs (different stock + shape icons).

_Status: done — **human-playtested by Steve 2026-07-24, PASS.**_

---

## Combat dialog + SFX hooks for the six new actions (2026-07-24, Playwright-verified)

The new third abilities were borrowing existing barks (Railgun used Rex's laser line; **Vent Plasma
even spoke as Rex** because `fireCrewWeapon` hardcoded the Rex bark). Gave each its own combat dialog +
a dedicated SFX cue.

**Dialog:** 6 new `CREW_BARKS` sets (3 in-character lines each) — `astra-evade`, `rex-railgun`,
`kael-disruptor`, `voss-focus`, `tessa-vent`, `selyra-triage`, wired into each ability's apply. Fixed
`fireCrewWeapon`'s bark + log routing so `vent`→Tessa (`tessa-vent`) and `railgun`→`rex-railgun`
(instead of always Rex-laser). VO clip names continue each character's run
(astra_09–11, rex_10–12, kael_11–13, voss_06–08, tessa_10–12, selyra_08–10).

**SFX:** 6 new cues registered in `SFX_VOL` and called from each action — `railgun`, `vent`,
`disruptor`, `evade`, `focus`, `triage`.

Both degrade gracefully — subtitles show and SFX are silent until the audio exists. **Needed audio
tracked** in `ASSETS_NEEDED.md` (new section) and the read lines appended to `COMBAT_BARK_SCRIPT.md`
for Steve to record; SFX prompts to generate.

**Verified** over `http://localhost:8123`, `pageerror` clean: each new action fires a bark with the
correct speaker (Vent now correctly Tessa, not Rex), the 6 bark sets are well-formed, and the 6 SFX
cues are registered.

_Status: done — subtitles + SFX hooks live; **VO + SFX audio files still to be created by Steve**
(non-blocking; both degrade to text/silence)._

**VO update (2026-07-24): the 18 bark lines are now RECORDED + cut.** Steve read them into six
`audio/Combat/<Name>_E2.mp3` masters; `cut_combat_e2.py` (a numbering-offset clone of `cut_combat.py`)
transcribed/aligned/cut them — **all six matched the script at ratio 1.000** — into astra_09–11,
rex_10–12, kael_11–13, voss_06–08, tessa_10–12, selyra_08–10 (66 combat clips total now). The new
actions are fully voiced.

**SFX update (2026-07-25): all 6 cues DELIVERED — this section is now fully closed.** Prompts were
written to `AUDIO_PROMPTS.md` § "v0.6 third-ability SFX (A15–A20)" and Steve generated all six the
same day. **Every one landed inside its spec length** — railgun 0.88s · vent 0.80s · disruptor 0.68s ·
evade 0.48s · focus 0.48s · triage 0.88s — the first audio batch in the project needing no
regeneration and no `SFX_MAXMS` trim. Zero code changes: the files just drop in at
`audio/SFX/<cue>.mp3` against the keys already in `SFX_VOL`.

⚠️ **One fix on arrival: `disruptor` came in as `distruptor.mp3`** (renamed). Worth remembering as a
class of bug — `_sfxPool` builds its path from the cue key, and a missing file is a deliberate silent
no-op, so a typo'd asset filename produces **no error, no log, no placeholder**: the ability just
plays nothing and looks like a mixing problem. Nothing in the existing verification would have caught
it; the filename-vs-`SFX_VOL` spelling check is the only thing that does.

**Verified** over `http://localhost:8123`, `pageerror` clean: all six requests 200, each pooled
`Audio` reaches `readyState 4` with the decoded duration matching the file, `SFX._missing` empty after
firing every cue through `sfx()`, and all 17 SFX distinct by MD5. (Their file *sizes* collide in
groups — the generator exports at a fixed ~205–212 kbps, so equal-length clips are byte-identical in
size; hash, don't size-compare.)

_The third abilities are now complete end to end: mechanics, gate modules, shop stock, dialog, VO and SFX._

---

## Station menu restructure — DONE (2026-07-24), Playwright-verified

**Ask:** "update the station menu. Repair should be within the Modules menu option, instead of Trade
and Market I want simply **Resources** with two tabs: **Buy** (buy resources) and **Sell** (sell
resources for a profit or not — drop the word 'dump' — and where you sell scrap)." (Steve)

**What changed:** the station's left tab column went from six tabs
(`TRADE, MARKET, REPAIR, MODULES, BOUNTIES, JOBS`) to **four**
(`RESOURCES, MODULES, BOUNTIES, JOBS`):
- **RESOURCES** is a single tab carrying a new **BUY / SELL** sub-tab strip at the top of the rows
  panel (a nested-tab pattern that's new for stations — modeled on the left tab column). **BUY** is
  the commodity buy list (was TRADE); **SELL** is scrap + commodity selling (was MARKET). The
  "Dump all X" row is relabeled **"Sell all X"** — the word *dump* is gone everywhere.
- **REPAIR** folded into **MODULES**: broken-part repair rows now render right under "⚙ Fit Modules",
  and the broken-count badge moved from the old REPAIR tab onto MODULES.

**Implementation (all in `iso_grid_prototype.html`):** `STATION_TABS` shortened; new
`RESOURCE_SUBS = ["BUY","SELL"]` + `stationSub` state (reset in `dockAt` and on every main-tab
switch). `stationRows()` RESOURCES branch splits on `RESOURCE_SUBS[stationSub]`; MODULES branch got
the repair rows. `drawStationView` reserves `subH = 36` for the sub-tab chip strip, offsets
`listTop`/`maxRows`, stores chip hit-rects in `_menuHit.stationSub`, and moved the broken badge to
MODULES. Input: **Tab** toggles Buy/Sell while on RESOURCES (keyboard); the chip strip is clickable;
the footer hint gains "Tab buy/sell" only on RESOURCES.

**Verified** over `http://localhost:8123` with Playwright, `pageerror` clean: tabs are exactly
`[RESOURCES, MODULES, BOUNTIES, JOBS]`; BUY lists only `buygoods:` rows (no scrap); SELL leads with
"Sell all scrap" then commodity rows; no label anywhere contains "dump"; repair rows appear under
MODULES with the broken badge = broken count; Tab flips the sub-tab; switching main tabs resets to
BUY. Screenshots: `restruct_buy.png`, `restruct_sell.png`, `restruct_modules.png`.

---

## Missions menu — STORY + AWARDS restyled to match SIDE/BOUNTY (2026-07-24), Playwright-verified

**Ask:** "in the menu mission tab make story and awards consistent with the style and formatting
on bounty and jobs." (Steve)

The Missions screen has four tabs. **SIDE** and **BOUNTY** share one look (`drawJobList`): a single
full-width `techPanel` container, centred title, full-width rows inset 16px, a footer hint. **STORY**
and **AWARDS** each drew their own thing — STORY was a two-column list + detail panel titled
"MISSIONS"; AWARDS used a narrower container (660 vs 720), a bigger 22px title, and 22px row insets.

**What changed (both in `iso_grid_prototype.html`):**
- **STORY** (`drawMissionsView` story branch) rebuilt as a single-container list like the job lists:
  720-wide panel, `top 58`, cyan rim, centred **"STORY LOG"** title, full-width rows (`x+16 / w-32`,
  radius 10). Completed missions read `✓ COMPLETE · <kind>`; the active one reads `◆ ACTIVE OBJECTIVE`
  in green. The **selected** mission expands to reveal its recap underneath — the same
  expand-the-live-row idea the SIDE list uses for its checklist. The **PIN STORY** control moved from
  a floating top-right button onto the active row's right edge, matching the per-row 📌 PIN on jobs
  (same `_menuHit.storyPinBtn`, so no click-handler change). Empty state now matches jobs' centred
  message inside the container.
- **AWARDS** (`drawAchievementsView`) aligned to the same container metrics: width 720, `top 58`,
  `h` on the `visH − 90` formula, radius 14; title dropped 22px→**18px** at `top+30`, with the
  `N / M UNLOCKED` count right-aligned on the title line; rows re-inset to `x+16 / w-32`, radius 10.
  Row content (glyph, name, desc, progress bar) is unchanged.

Both keep their own accent rim (STORY cyan, AWARDS gold) — the same per-tab colour cue SIDE (green)
and BOUNTY (gold) already use.

**Verified** over `http://localhost:8123` with Playwright, `pageerror` clean: all four tabs render on
the identical container geometry; STORY rows collapse/expand with the recap on the selected row and
the active row carries the pin; AWARDS title/insets/footer line up with the job lists. Screenshots
`missions_story_full.png`, `missions_awards.png`, `missions_bounty.png`.

---

## No more handing back jobs / bounties (2026-07-24), Playwright-verified

**Ask:** "Job/bounty hand-back — agree with Brett, you shouldn't be able to hand them back." (Steve)

An accepted contract or job is now a commitment — the station boards no longer offer a hand-back.
Previously an accepted bounty's row action was `abandon:<id>` and an accepted side job's was
`dropside:<id>` (each behind a two-step `stationConfirm` guard). Now:
- **BOUNTIES / JOBS rows** — only an **OPEN** contract is actionable (`act: st === "open" ? … : null`,
  `ok: st === "open"`). Accepted/in-progress rows render greyed and read-only (they still show the
  mark status + reward); done rows unchanged.
- Removed the now-unreachable `dropside` / `abandon` branches from `stationAction`, the orphaned
  `stationConfirm` two-step confirm computation, and the four dead helpers
  (`abandonSide` / `handBackSide` / `abandonBounty` / `handBackBounty`).

No escape hatch remains for a job you can't finish — that was the original reason hand-back existed,
but Steve's call is that a contract is a contract.

**Verified** over `http://localhost:8123` with Playwright, `pageerror` clean (confirms no dangling
references to the removed helpers): after accepting the first bounty + first side mission, the
accepted rows carry `act: null`, no row exposes an `abandon:` / `dropside:` action, and open contracts
still accept normally. Screenshot `handback_bounties.png`.

---

## Station rumours + the Crimson Nova hangar encounter (2026-07-25), Playwright-verified

Two linked features: a **rumour** system, and a friendly-NPC VN encounter it hints at.

**Rumours (iso).** A new read-only **RUMOURS** tab on the station screen — tips that point you at
things in the sector. You don't *accept* a rumour and it raises no objective marker; it's flavour,
and some players will find the thing without ever reading it. `STATION_TABS` gained `"RUMOURS"`; a
`RUMOURS` data array keyed by station id; `stationRows()` renders each as an inert `act:null` row
(the existing greyed, non-interactive idiom). First rumour, at the **Waypoint Hub** — "A Hero for
Hire" — teases the Crimson Nova out at the edge of the system.

**Crimson Nova (Orion Blaze).** A theatrical mercenary hero whose ship, the Crimson Comet, is parked
in a **hangar on the rim**. The map gets a new dockable `OBJ.HANGAR` rendered from the existing
`Assets/space/Crimson.png` (a mercenary base with a landing pad + "NOW ACCEPTING CONTRACTS" signage),
placed once at `(-72,-58)` (~92 tiles out, inside `MAP_RADIUS`, off every route — you find it by
exploring). Flying up raises an "Enter the hangar?" prompt (crimson-accented, modelled on the station
dock prompt); entering plays a full **visual-novel scene** — Steve's authored ~52-line
`Crimson_Script.txt` — then returns you to free-roam. **Skit only, no reward** (the hiring negotiation
is in-fiction setup; actually hiring Crimson to fight is future work). He's **re-encounterable**: the
full scene once, a short greeting after.

**The cross-frame bridge.** During free play the iso runs inside episode1's `#gpFrame` iframe, so the
scene plays in episode1's VN engine over the still-live game. New `playScene` (iso→parent) /
`sceneDone` (parent→iso) messages: the iso posts `{type:"playScene", id: crimsonMet ? "crimson_greet"
: "crimson_nova"}` and pauses its sim (`sceneActive`); episode1 overlays the VN **without tearing down
the iframe** (`hideGameplayKeep()` toggles `#gameplay` hidden but never sets `src="about:blank"`,
which would wipe iso state), drives it through a `sceneMode`/`activeScene`/`curSteps()` indirection
layered onto the existing `nextStep`/`advance`/`autoTick`, and on the last step `endScene()` reshows
the iframe, refocuses it, and posts `sceneDone` back. The iso then un-pauses and sets `crimsonMet`.

**VN registration.** `Crimson` added to `CHARS` (crimson `#ff5a4a`); `CHAR_ART.CRIMSON` lists the 20
poses the script names; `EXPR_ALIAS` gained crew-cue fallbacks (Calm Smile→Smirk, Confused→Thinking,
Annoyed→Angry, etc.) so every crew line resolves to existing art. A `[data-n="7"]` cast rule lets the
six crew + Crimson share the stage. Scene BG `BG_CRIMSON`. Persistence: `crimsonMet` in
`localStorage["stargear_crimson_v1"]` + the save snapshot (bumped **v6→v7**; pre-v7 → not met).

**Verified** over `http://localhost:8123`, `pageerror` clean (real JS errors — asset 404s for the
not-yet-created art degrade to placeholders): RUMOURS tab (inert row at the Hub, fallback elsewhere);
hangar placed + rendered + "ENTER HANGAR" prompt; Crimson registered + `charFile` resolves + the
54-step scene well-formed; **full round-trip** — iso `enterHangar()` → parent plays `crimson_nova`
(gameplay hidden, iframe src untouched) → `endScene()` → iso resumes with `crimsonMet` set; second
visit requests `crimson_greet`; `crimsonMet` survives save/load; the linear EP1 story still advances
through the shared sequencer. Screenshots: `crimson_scene2.png` (the staged 7-cast scene),
`hangar_prompt.png`.

_Status: code complete + verified. **Awaiting art from Steve** (all degrade gracefully): the Crimson
portrait set, the hangar-interior BG, and (optional) VO — see `ASSETS_NEEDED.md`. Tunable:
`HANGAR_SCALE` (1.7) if the rim sprite wants to read bigger._

**Assets update (2026-07-25):** the **scene BG** (`Assets/Crimson_Hanger.png`), **Kael's Deadpan**
pose, and **all VO** landed. Steve recorded the seven speakers into `audio/Rumours/*.mp3`;
`cut_rumours.py` (whisper align + cut) split them into `audio/Rumours/vo/<char>_NN.mp3` and emitted a
`SCENE_VO` map (keyed `who|text`, consulted by `showLine` after `VO_MAP`) — **50 of 52 lines voiced**
(the 2 unvoiced are Crimson's silent "..." beats; the greeting's 2 lines weren't recorded → subtitle
only for now). Playwright-verified: BG + Deadpan resolve, `SCENE_VO` covers 50 lines, clips serve 200,
`pageerror` clean. **Remaining:** the Crimson portrait set (Steve is drawing the ~12 missing poses +
moving `Assets/char/Mercenaries/CRIMSON/` → `Assets/char/CRIMSON/`).

**Duo staging (2026-07-25):** the Crimson scene no longer crowds all six crew on stage. New `duo`
scene flag: Crimson is pinned right (CSS `#cast.duo .char[data-who="Crimson"]{margin-left:auto}`) and
only the **current + previous crew speaker** show on the left. `sceneStageDuo(who)` keeps two fixed
slots (a new speaker evicts whichever slot isn't the immediately-previous speaker, so positions stay
stable); the scene opens on Crimson alone for his entrance. Also made the scene reachable **any time
the iso is embedded** (story travel leg or free play), not free-play-only, and added an
`episode1.html?freeplay=1` dev shortcut for testing. Playwright-verified: staging invariants across all
52 lines, real click → scene fires in both a story beat and free play (beatIdx preserved), duo layout
renders (crew left, Crimson right).

---

## Crimson Nova joins as a hireable combat ally (2026-07-26), Playwright-verified

**Ask:** the hire-as-combat-ally mechanic the VN scene sets up ("I'm available for hire"). Steve's
brief: 100 coin per battle, first battle free, auto-deducted at combat start; if you can't afford it
he sits the fight out and heads home, rehire by flying back to the hangar; a **Mercenary** menu entry
to check his status or release him any time; he follows one tile behind in free-roam; in combat an AI
"Guest" phase runs between the player's turn and the enemy's, with his own space chatter and combat
barks. Steve's explicit call, after a first design pass recommended a support-only/untouchable
build for scope reasons: **he's targetable** — real HP, enemies can hit him, and a knockout sends him
home (leaves the team) until re-hired. That one decision is what most of the design below is shaped
around.

**Persistence (all in `iso_grid_prototype.html`):** new `crimsonHired`/`crimsonFreeUsed`, a dedicated
`CRIMSON_HIRE_KEY` (`crimsonMet`'s existing `CRIMSON_KEY` is a bare "1"/"0" flag, not worth widening).
Continuation-gated like every other subsystem; save snapshot bumped **v:7 → v:8**. The free-battle flag
is global and one-time-ever — it survives release/rehire and only resets on a truly fresh game.

**Hire/rehire is entirely the existing hangar round trip** — no separate "hire" button. Both
`crimson_nova` (first meeting) and `crimson_greet` (every revisit) now hire/re-hire him in the
`sceneDone` handler; the tip only shows once, for free, off `showTutorial`'s own seen-gate. "Returns to
base" on a no-show or a knockout is just `crimsonHired = false` — no travel, no animation; the
free-roam escort is gated on that flag every frame and simply stops appearing next frame.

**The fee** is checked once, in `startCombat()`: free if `!crimsonFreeUsed`, else `spendCoin(100)`; on
success `combat.guest` is built with real `hp`/`maxhp` (10); on failure `crimsonHired` flips false and
a `noShow` bark fires once the opening banner clears.

**The Guest combat phase** — turn order is player → guest (if present) → enemy, every round.
`endPlayerTurn()`'s old tail (unconditionally starting the enemy phase) is now `beginEnemyPhase()`,
reached either straight from the player's turn (no guest this fight) or via a new `beginGuestPhase()` →
`guestAdvance()` → `finishGuestTurn()` → `beginEnemyPhase()` chain when he's present. `guestAdvance` is
a compact two-beat state machine (a flourish, then the shot) — simpler than `enemyAdvance`'s
move/fire/gap cycle since he's parked at a fixed arena tile and never moves. His kit is personality,
not a menu: **Spotlight Shot** (≤2 live enemies, single target — whichever is closest to the player,
protective framing, 3 dmg) or **Supernova Strike** (3+, every live enemy, 2 dmg each, showman framing)
— he never misses. Reuses `fireCrewWeapon`'s exact damage/kill/`combat.pending` pipeline, so kills
explode and grant scrap through the one existing code path; his shot is the first caller to ever pass
`pending.endAfter: true` (crew shots always pass `false`), which is what the `tickCombat` pending-gate
now routes to `finishGuestTurn()` instead of `endPlayerTurn()` when `combat.phase === "guest"`.

**Vulnerability turned out cheap.** `shotFromTile(gx,gy,target,e)` was already generic on its target
parameter — only `enemyFire(e,weapon,face,target)` needed a 4th argument and a branch (no dodge, no
shield for him — he's not fitted with the player's modules; a knockout nulls `combat.guest`, flips
`crimsonHired` false, and fires a `knockedOut` bark). A new `pickEnemyTarget(e)` rolls a
**30% chance** to shoot him instead of the player, but only when he's *already* in a valid firing line
from wherever the enemy would move anyway — `planEnemyMove` is deliberately untouched, so **enemies
never reposition to hunt him specifically**, only take the opportunistic shot. Flagged as a first-pass
simplification in the same "revisit if it doesn't land" spirit as A6's WONTFIX.

**Turn-order bar / banner / guidance / panel:** a third `kind: "guest"` in `combatTurnOrder()`
(vanishes the instant he's knocked out), a `#ff5a4a` team colour throughout, a `guest` `BANNER_STYLE`
entry ("★ CRIMSON NOVA" / "CRIMSON'S TURN"), a guidance-pill case, and a `· guest…` suffix on the panel
header. His HP ring needed **no special-casing** — `combat.guest.hp`/`.maxhp` are real, so the existing
fraction-of-max arc math just works. Deliberately **not** added to `combat.crew`/`CREW` — the crew face
grid has a hardcoded 3-row layout and feeds `canCrewAct`/`hasUsableAction` (the confirm-end-turn modal),
none of which should know about him.

**Free-roam following:** a small `shipTrail` ring buffer (position + facing, pushed on every completed
move) so `crimsonEscortPos()` reads the entry from one move ago — trailing the player's actual path,
not just an offset of whatever direction they currently face. `Assets/obj/CrimsonComet_ne.png`/`_sw.png`
were already on disk and completely unreferenced; registered the same way `BOSS_SHIPS` registers a hull.

**Chatter + barks:** one shared `SPEAKER_ACCENTS` fallback fixes both `drawChatter` and `drawCrewBark`'s
accent lookup for a non-crew speaker (previously anyone not in `CREW` rendered in flat cyan). A
dedicated `CHATTER.crimsonIdle` pool rolls on its own independent timer, gated on `crimsonHired`, so it
never competes with the crew's idle slot. Combat barks are a dedicated `CRIMSON_BARKS` table +
`crimsonBarkSay()` — deliberately **not** folded into `CREW_BARKS`' shared reactive pools (`kill`,
`heavy-hit`, etc.), which would fire his lines even in fights he isn't hired for. He shares the
`crewBark` display slot/cooldown/VO channel rather than a parallel state machine — there's only one
bark bar on screen, so nothing was gained by duplicating `tickCrewBark`/`drawCrewBark`. Six trigger
keys: `join`, `attack`, `supernova`, `knockedOut`, `heavyHit`, `noShow`.

**Mercenary menu:** `MENU_ITEMS` (8 entries) is now built by `menuItems()`, which splices in a 9th
**Mercenary** entry once `crimsonMet` — a new `"nova"` starburst glyph, a status view modelled on
`drawOptionsView` (hired/at-hangar, fee reminder, first-battle-free note), and a one-click **RELEASE**
button, no confirm modal (matches the "release him any time" casual framing — trivially reversible by
flying back).

**Verified** over `http://localhost:8123` with Playwright, driving **real** `startCombat()`/
`tickCombat()` through the actual game loop rather than isolated stubs, `pageerror` clean throughout:
hire via the hangar round trip + tip fires once + Mercenary entry appears; release flips immediately +
revisiting re-hires; free-roam escort trails exactly one move behind through direction changes and
disappears on release; first fight free regardless of coin, second fight deducts exactly 100; `combat.guest`
built with real hp/maxhp on an affordable fight; **"CRIMSON'S TURN"** banner between the player's and
enemy's; Spotlight Shot at ≤2 enemies (single target) vs Supernova Strike at 3+ (every enemy) — measured
directly against enemy HP before/after; insufficient coin → no guest phase at all, `noShow` bark,
`crimsonHired` flips false, turn goes straight from player to enemy; a real enemy can find a valid
facing against his tile (`shotFromTile` generalization) and `enemyFire`'s guest branch reduces his HP;
driving his HP to 1 and landing a hit nulls `combat.guest` and flips `crimsonHired` false; turn-order bar
renders his accent/HP ring without crashing. **Full regression pass:** an un-hired fight never creates
`combat.guest` and the turn order has no `guest` entry; an ordinary crew action (Rex firing lasers)
behaves exactly as before; a **boss fight** (`#mission&boss=wolfpack`) still renders correctly with him
present, boss core + guest both appear in the turn order; save v8 round-trips `crimsonMet`/
`crimsonHired`/`crimsonFreeUsed` alongside the rest of the snapshot untouched.

_Status: done — code complete, Playwright-verified, **not yet human-playtested.** Feel calls flagged for
Steve: `CRIMSON_MAX_HP` (10), `CRIMSON_DMG`/`CRIMSON_AOE_DMG` (3/2), the 3-enemy Supernova threshold,
`CRIMSON_TARGET_CHANCE` (30%), and `CRIMSON_SHIP.scale` (untuned — first time seeing the art at 1× in
either the arena or free-roam). **VO not yet recorded** — 13 combat bark clips + 5 explore idle clips,
both degrade to subtitle-only; see `ASSETS_NEEDED.md`._

---

## Fluid held-key explore movement — investigated, ROLLED BACK (2026-07-26)

**Ask:** Steve — holding a direction key in free-roam felt sticky rather than fluid.

**What was tried** (three rounds, each Playwright-verified but each still reported as "stepping" by
Steve on hands-on try): (1) held-key chaining (a `heldMoveDirs` stack + `keyup`/`blur` listeners so a
move auto-repeats while a key is held, instead of relying on the OS's native keyboard repeat delay/rate);
(2) linear easing on chained segments so consecutive tile-slides hold constant velocity through the
boundary instead of decelerating-then-reaccelerating every tile; (3) suppressing the tile rise/drop
pop-in animation and shortening the per-tile duration (300ms→150ms) specifically for held/chained steps.

**Diagnosis (2026-07-26):** rather than a fourth speculative tweak, verified the animation directly —
sampled `world.cameraOffsetX/Y` on every real rAF frame during a held glide (zero frozen frames, changes
every rendered frame) and cross-checked with an actual Playwright video recording, frame-by-frame. The
camera math had no remaining discontinuity. The likely real source of the "stepping" read: every tile
renders as a raised, beveled 3D block with visible side faces and edges (`buildTileSprite()`) — a
diamond-grid pattern baked into the tile sprite itself, visible even with the debug grid overlay off.
A grid of visible-edged blocks scrolling past reads as a tiled surface advancing, which is accurate to
what's on screen, not a smoothness defect.

**Steve's ruling:** this is the game's actual tile-scroll visual style, not a bug — and then asked for
the three movement changes to be **rolled back** rather than kept. Reverted in full: `heldMoveDirs`/
`dirForKey`, the `keyup`/`blur` listeners, the `chained` parameter through `requestMove`/`beginMove`/the
four `shift*` functions/`enqueueRise`/`enqueueDrop`, `world.bufferedChained`, the `linear` easing
function, and `LATERAL_MS_CHAINED` — all removed from `iso_grid_prototype.html`. Confirmed via
Playwright: no `pageerror`, a single tap still moves exactly one tile, and holding no longer
auto-chains (movement is purely OS-key-repeat-driven again, matching pre-2026-07-26 behavior). Closed;
no further attempts planned on this ask. The full float-position rearchitecture that was scoped as a
possible fallback (see the plan file) is not being pursued either.

---

## Full human playtest — Steve, 2026-07-26 (all fixes above + Crimson as ally)

Every 2026-07-26 fix and the ship-parts-I 6-crew modules all **PASS**. Testing the Crimson Nova
ally end-to-end surfaced ten more items, all fixed same session (all in `iso_grid_prototype.html`
unless noted):

| # | Fix | Where |
|---|-----|-------|
| 1 | **Mercenary menu no longer auto-opens after the "he's joined" tip.** `sceneDone`'s `showTutorial("crimsonHired", …)` had an `onClose` that force-opened the menu on the Mercenary tab; the tip already tells you where to find it, so the callback is dropped — closing the tip now just returns to free-roam. | `sceneDone` handler |
| 2 | **Mercenary screen redesigned** to read like the crew character sheet instead of a bare status box: a bio column (new `CRIMSON_BIO`), his **Heroic Pose** portrait (new `crimsonPortraitImg`, `Assets/char/Mercenaries/CRIMSON/Heroic_Pose.png`), then name/status/cost/RELEASE in a third column — same 3-column shape as `drawCrewCharView`. | `drawMercenaryView` |
| 3–5 | **Guest combat visuals recolored blue.** Turn order avatar, HP ring, world HP bar and the turn banner all keyed off Crimson's personal coral (`#ff5a4a`, still his color for chatter/menu/hangar) — introduced a separate `GUEST_TEAM_COLOR` (`#4ac8ff`) so the *team slot* reads distinctly from a faction color, and so a future second guest doesn't inherit a name that isn't theirs. | `BANNER_STYLE.guest`, `drawTurnOrder`, `drawHpBar` call site |
| 4 | **Banner text genericized** — "CRIMSON'S TURN" → "GUEST'S TURN", tag "★ CRIMSON NOVA" → "★ GUEST", for the same reusability reason. | `beginGuestPhase` |
| 6 | **Brief pause before his turn.** `guestAi`'s initial timer was 300ms — shorter than the 1200ms banner's rise, so the flourish started while "GUEST'S TURN" was still animating in. Now uses the same `ENEMY_GAP_MS` (520ms) beat the enemy phase gives its first ship. | `beginGuestPhase` |
| 7 | **ACCEPT button text was unreadably dark** (`#0c1a10`, near-black) on the dark job/bounty row panel. Now the same green as the button's own outline (`#7ee787`). | `stationRows` ACCEPT button |
| 8 | **Repair now pops a floater**, matching the hit/miss convention — Tessa's Repair and the Med Bay hull-patch-on-Heal bonus were silent besides the log line; both now spawn a `+N` green floater. | `applySelfAction` Repair · `applyCrewTarget` Heal/Med Bay |
| 9 | **JOBS tab was missing its badge entirely.** The station tab-badge logic had a branch for MODULES (broken count) and BOUNTIES (open count) but none for JOBS, so a station with an open job never showed its count (Waypoint Hub: BOUNTIES showed 3, JOBS showed nothing for its 1 open job, "The Long Haul"). Added the matching branch, station-scoped like the board itself. | station tab badge loop |
| 10 | **Enter no longer opens the pause menu in free-roam** — only `M` does now. Enter was doing double duty as both the global menu-open key and the confirm key for every Y/N prompt/dialogue-advance, and kept opening the menu by accident off that muscle memory. Field Manual, HUD footer hint and the explore tip all updated to say `M` only. | free-roam key switch · `MANUAL` · HUD hint · `TIPS.explore` |

**Not yet re-verified** (code complete, syntax-checked, server round-trip confirmed the new portrait
asset resolves; awaiting the next human pass).

### Re-playtest — Steve, 2026-07-26: all ten items PASS, plus two new bugs and three follow-up asks

All ten items from the table above confirmed working in-game. Testing them turned up two more bugs,
which were fixed the same session:

- **Mercenary screen: bio text overflowed its box, and the status column left a dead gap of
  whitespace before the panel's right edge.** The bio column was too narrow for `CRIMSON_BIO` at its
  panel height (~16 wrapped lines needed, box only fit ~14) and the status column's long sentences
  were single unwrapped `fillText` calls, so short lines left blank space where nothing else was
  drawn. Fixed by widening the bio column (260→340px, freeing up horizontal room so the same text
  wraps to fewer lines) with a hard `maxLines` cap as a backstop against any future bio edit
  overflowing again, and wrapping the status column's sentences to its actual width via `wrapText`
  instead of letting them run unconstrained. | `drawMercenaryView` |
- **AUTO/mute buttons stayed on screen during live gameplay after any Crimson VN scene.**
  `hideGameplayKeep()` (shows those buttons for the scene) has no counterpart being undone —
  `endScene()` revealed gameplay again but never hid them back, unlike `hideGameplay()`'s own
  pairing with `showGameplay()`. This bug existed as soon as the "scene over live gameplay" path
  landed; it just took hiring Crimson to trigger it. Fixed in `endScene()` (episode1.html). |

Three follow-up asks from the same session, all in `iso_grid_prototype.html` unless noted:

- **Guest status row swapped above End Turn** (was below it) — End Turn stays the panel's fixed
  last element either way; the guest row now sits between the crew faces and it. | `combatPanelLayout` /
  `drawCombatPanel` |
- **Turn-start pause lengthened twice** — `TURN_START_PAUSE` 520ms (shared with `ENEMY_GAP_MS`) →
  750ms → **1100ms**, now close to the turn banner's full 1200ms display, for both the guest and
  enemy phase hand-offs. | `beginGuestPhase` / `beginEnemyPhase` |
- **Skip button added to VN sections** (episode1.html) — a "Skip ▸" button beside AUTO/mute, shown
  only during dialogue (a `"vn"` beat or a standalone scene like Crimson's), hidden during gameplay
  the same way AUTO/mute are (all four show/hide call sites updated together, closing off the same
  bug class as the AUTO/mute leak above). Clicking it jumps straight to the end of the *current*
  section — reuses `nextStep()`'s own end-of-section branch (`endScene()` / `runBeat(beatIdx+1)`) by
  landing `stepIdx` one short of it, rather than duplicating that logic. |

Also this session: the Crimson-hangar rumour's closing line ("out at the very edge of the system")
was made directive — now names Veil Anchorage as the landmark ("out past Veil Anchorage — the far
edge of the charted nebula, and further still"), matching the hangar's actual placement further out
along the same bearing.

All syntax-checked clean; not yet re-verified in-game.
