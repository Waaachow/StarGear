
# Image generation prompts

Companion to `AUDIO_PROMPTS.md` — the prompts behind the generated art in `Assets/`,
kept so anything can be regenerated consistently. Asset list and priorities live in
`ASSETS_NEEDED.md`.

House notes for UI icons: HUD palette is scrap `#8dffb0` / `#9fb4c8`, coin `#f2c14e`,
panel chrome `rgba(120,200,220,0.45)` on `rgba(4,10,18,0.72)`. Light from the upper
left, dark navy outline, transparent background, square and centred.

Generators tend to output ~1200×896 regardless of what the prompt asks for. Crop to the
art bounds and downscale to 64×64 before use — `Assets/ui/*_64.png` are the files the
game actually loads; the full-size originals sit beside them as masters.

---

## UI icons

### U1 — Scrap · `Assets/ui/scrap.png` → `scrap_64.png` ✅

> Game UI icon of a piece of salvaged starship scrap: a small torn, angular chunk of hull
> plating with a bent rivet edge and one broken strut, seen three-quarter on. Flat
> semi-stylised sci-fi HUD art, thick clean silhouette, minimal interior detail, chunky
> readable shapes. Cool metal palette — desaturated blue-grey plate (#9fb4c8) with a pale
> cyan-green rim light (#8dffb0) along the top-left edge and a soft cyan inner glow.
> Subtle dark outline for contrast on a dark background. Centred, square composition with
> even margin, fully transparent background, no text, no drop shadow, no background panel.
> 64×64 icon design that stays legible when scaled down to 24px.

### U2 — Coin · `Assets/ui/coin.png` → `coin_64.png` ✅

> Game UI icon of a sci-fi trade credit coin: a circular metal token viewed straight-on,
> slightly thick edge with fine milled ridging around the rim. Centred on the face is a
> single engraved four-pointed compass star with elongated horizontal points and short
> vertical points, sitting inside a thin concentric ring. Purely geometric navigational
> motif — no religious, national, or cultural symbolism, no lettering or numerals of any
> kind. Flat semi-stylised sci-fi HUD art, bold clean silhouette, minimal interior detail,
> chunky readable shapes. Warm gold palette — #f2c14e face with a brighter highlight
> sweeping the upper-left quadrant and a darker amber (#a8801f) rim and engraved recess.
> Subtle dark navy outline for contrast against a dark background. Perfectly square
> composition, coin centred with even margin on all four sides, fully transparent
> background, no drop shadow, no background panel, no text. 64×64 icon design that stays
> legible when scaled down to 24px.

## Trade station sprites (U3)

Four stations, four sprites — see `TRADE_STATIONS` in `iso_grid_prototype.html`. Shared
house style, one paragraph of local flavour each. Paths: `Assets/space/Trade_<id>.png`
(`hub`, `neb`, `moon`, `armada`). Drawn at `TRADE_SCALE = 1.5`, so they sit visibly larger
than `Station.png` (the unmanned comm satellite) — silhouette has to read as *inhabited*,
not just *big*.

**Shared preamble** — paste ahead of each flavour paragraph:

> Hand-painted semi-stylised sci-fi game sprite of a manned deep-space trade station, seen
> from a high three-quarter isometric angle looking slightly down, as a single object
> floating in empty space. Steampunk-space aesthetic: riveted metal plating, exposed pipes
> and trusses, brass and worn-steel accents against cool blue-grey hull. Lit from the upper
> left with a cool key light and warm interior glow spilling from lit windows and open dock
> mouths, so the station clearly reads as inhabited. Chunky readable silhouette, moderate
> interior detail, dark navy rim for contrast against a black starfield. Fully transparent
> background, no starfield, no nebula, no planet, no text, no signage, no lettering or
> numerals, no drop shadow, no ground plane. Centred with even margin, ~1200×896.

### Waypoint Hub · `Trade_hub.png` — central start, general trade, first stop

> A broad hexagonal core with a wide slow-rotating docking ring, four short arms ending in
> open hangar mouths lit warm amber, and rows of small lit habitation windows. Symmetrical,
> tidy, well-maintained — the busiest and most civilised station in the sector. Cargo pods
> in neat stacks clamped along the ring, a pair of small tugs docked at the outer arms.
> Palette leans warm brass and clean pale steel.

### Veil Anchorage · `Trade_neb.png` — Whispering Nebula (NW), nebula relics

> A tall irregular station grown outward from a mined-out asteroid anchor, its hull a
> patchwork of mismatched salvaged plating in faded violet and teal. Long antenna masts and
> dish arrays bristle from the upper structure, trailing loose cabling. Faint magenta and
> cyan light bleeds from behind the plating and along the seams, as if nebula colour has
> soaked into the metal. Fewer, dimmer windows — quieter and stranger than the other
> stations, half research post and half relic market.

### Quarry Station · `Trade_moon.png` — Broken Moon (NE), raw ore, mining

> A heavy industrial platform built around a central ore-processing tower, with slab-sided
> hoppers, exposed conveyor gantries and a large rock-crusher maw on the underside glowing
> hot orange from within. Blunt, functional, dust-stained; ochre and rust tones over grey
> steel. Mining rigs and cutting gear clamped to external racks, a squat cargo barge docked
> at a loading spur. Fewer habitation windows, more floodlights.

### Salvage Reach · `Trade_armada.png` — Silent Armada (SE), salvage, scrap

> A working station assembled out of the sectioned corpse of a capital warship: a huge
> cannibalised hull segment forms the spine, with newer prefab modules bolted along it and
> cutting scaffolds still clamped in place. Torn plating, exposed frame ribs, and severed
> conduits left visible on the salvaged sections; a crane arm holds a hull fragment
> mid-strip. Cold green-white worklights against dark scorched metal. Improvised and
> lopsided, but plainly lived in.

## Station dock backdrops (U6)

One interior per station, so docking four places doesn't feel like opening the same menu
four times. Paths: `Assets/<Station_Name>.png` at **1376×768** (same ratio as the title
art). **All four delivered 2026-07-21 and wired** via `drawDockBackdrop` (cover-fit to the
canvas under a 0.62 scrim). All four came from the prompts below, including `Waypoint_Hub.png`
and `Salvage_Reach.png`, which were **regenerated from scratch** — these prompts supersede the
original uploads of those two and deliberately don't reference them. Each prompt is
self-contained; paste one, generate, move on.

### Waypoint Hub · `Assets/Waypoint_Hub.png`

> Hand-painted semi-stylised sci-fi game background, wide 16:9, 1376×768. The interior of a
> busy, well-kept deep-space trade station, seen from standing eye level as if you have just
> walked in. Steampunk-space aesthetic: riveted metal walls, exposed pipes and cable runs,
> brass fittings and polished trim over clean pale steel plating. A broad trade counter runs
> across the lower foreground, slightly out of focus. Neat stacks of cargo pods and crates
> against the side wall, a bank of blank display panels glowing soft cyan to one side. A tall
> arched window in the middle distance looks out onto the docking ring, ships lit warm amber
> against black starfield. Warm brass lamp light in the foreground against the cold blue glow
> of screens and the void beyond. Bright, orderly, prosperous — the most civilised station in
> the sector. Painterly brushwork, moderate detail, strong depth with dark framing edges and a
> bright focal middle. Completely empty of people — no figures, no crowd, no silhouettes. No
> text, no lettering, no numerals, no signage, no readable writing of any kind; boards and
> displays show only abstract glyphs, bars and coloured lights, or are left blank. Keep the
> central third relatively uncluttered so a UI panel can sit over it.

### Salvage Reach · `Assets/Salvage_Reach.png`

> Hand-painted semi-stylised sci-fi game background, wide 16:9, 1376×768. The interior of a
> deep-space salvage station improvised inside the gutted hull of a capital warship, seen from
> standing eye level as if you have just walked in. Steampunk-space aesthetic: riveted metal,
> exposed pipes and cable runs, brass and worn steel. The far wall is torn hull plating and
> exposed frame ribs left where they were cut, with newer prefab panels bolted over the gaps
> and severed conduits capped off. A counter welded from a slab of hull plate runs across the
> lower foreground, slightly out of focus; salvaged parts, coils of cable and stripped
> components racked and hung on every wall. Cold green-white worklights on clamp stands
> against dark scorched metal, a few warm bulbs strung overhead. Through a ragged opening in
> the middle distance, drifting warship wrecks against black starfield. Lopsided and cluttered
> but plainly lived in. Painterly brushwork, moderate detail, strong depth with dark framing
> edges and a bright focal middle. Completely empty of people — no figures, no crowd, no
> silhouettes. No text, no lettering, no numerals, no signage, no readable writing of any
> kind; boards and displays show only abstract glyphs, bars and coloured lights, or are left
> blank. Keep the central third relatively uncluttered so a UI panel can sit over it.

### Veil Anchorage · `Assets/Veil_Anchorage.png`

> Hand-painted semi-stylised sci-fi game background, wide 16:9, 1376×768. The interior of a
> quiet deep-space station grown inside a mined-out asteroid — half research post, half relic
> market — seen from standing eye level as if you have just walked in. Steampunk-space
> aesthetic: riveted metal, exposed pipes and cable runs, brass fittings. Rough rock walls
> behind a patchwork of mismatched salvaged plating in faded violet and teal. A trade counter
> runs across the lower foreground, slightly out of focus; behind it, shelves and glass cases
> of strange nebula relics — irregular glowing fragments and odd instrument arrays lit from
> within. Loose cabling and antenna feeds run across the ceiling. A wide viewport in the middle
> distance opens onto a magenta and cyan nebula, whose light pours in and bleeds along the wall
> seams as if the colour has soaked into the metal. Dim, cool, more shadow than lamplight;
> hushed and eerie. Painterly brushwork, moderate detail, strong depth with dark framing edges
> and a bright focal middle. Completely empty of people — no figures, no crowd, no silhouettes.
> No text, no lettering, no numerals, no signage, no readable writing of any kind; boards and
> displays show only abstract glyphs, bars and coloured lights, or are left blank. Keep the
> central third relatively uncluttered so a UI panel can sit over it.

### Quarry Station · `Assets/Quarry_Station.png`

> Hand-painted semi-stylised sci-fi game background, wide 16:9, 1376×768. The interior of a
> blunt industrial mining station on the edge of the ore works, seen from standing eye level as
> if you have just walked in. Steampunk-space aesthetic: riveted metal, exposed pipes, heavy
> brass and rust-stained steel. Slab-sided ore hoppers and a conveyor gantry run overhead with
> dust hanging in the light shafts. A scarred steel counter runs across the lower foreground,
> slightly out of focus, with cutting gear, drill bits and raw ore samples piled at one end;
> heavy mining rigs clamped to racks along the wall. Harsh white floodlights on gantry mounts,
> plus hot orange glow spilling from a crusher shaft to one side. Ochre and rust tones over
> grey steel, everything dust-stained. Through a wide dock mouth in the middle distance, the
> cracked grey face of a shattered moon against black starfield. Functional, grimy, heavy.
> Painterly brushwork, moderate detail, strong depth with dark framing edges and a bright focal
> middle. Completely empty of people — no figures, no crowd, no silhouettes. No text, no
> lettering, no numerals, no signage, no readable writing of any kind; boards and displays show
> only abstract glyphs, bars and coloured lights, or are left blank. Keep the central third
> relatively uncluttered so a UI panel can sit over it.

⚠️ **No fake signage.** An earlier pass came back with AI-rendered board text ("AVAILABLY
CONTRACTS", "COMMODITY PRICE") — garbled, and it competes with the real UI. The no-text clause
at the end of each prompt is deliberate and load-bearing; keep it, and reject a pass that draws
letterforms on the board wall even if the rest is good.

---

## Bounty boss ships (B5)

Enemy hulls live in `Assets/obj/` as an **`<name>_ne.png` / `<name>_sw.png` pair**, 1200×896,
transparent background. The two are the same ship seen from opposite diagonals — near
mirrors, but redrawn rather than flipped (compare `Wing_ne` / `Wing_sw`). The renderer also
flips sprites per facing, so the pair only has to cover the two diagonal views.

House style for hulls: **painted semi-stylised sci-fi game sprite**, bold dark outlines,
heavy weathering and battle damage, glowing engine/weapon emissives, top-down
three-quarter view with the ship filling the frame, isolated cutout on transparent
background. No text, no lettering, no readable insignia.

⚠️ A unique boss hull must be registered in **`BOSS_SHIPS`**, never `ENEMY_SHIPS` — the
latter is what random patrols draw from and what the codex builds hull entries from.

### Drax's escort wing · `Assets/obj/hound_ne.png` + `hound_sw.png`

The fighters visible **inside the Blood Crown's open hangar bay** in `blood_ne.png` — this is
that ship, drawn properly. Flown by veterans Drax took in; they die for him and he lets them.
It should read as *lesser kin* of the flagship: same colours and cruelty, a fraction of the
size, none of the ceremony.

> Painted semi-stylised sci-fi game sprite of a small, fast raider strike fighter, seen from a
> top-down three-quarter view, filling the frame. Lesser kin of a much larger pirate flagship:
> the same oxblood-crimson and black iron plating, the same hot red glowing emissives, but a
> fraction of the size and far cruder. A lean predatory arrowhead hull with forward-swept
> wings, twin oversized engines glowing furnace-red at the rear, a chin-mounted autocannon and
> underslung rocket pods. Salvaged military craft rebuilt by hand: mismatched armour panels
> bolted over old fleet-grey plating, crimson war paint sprayed over the seams, patched
> battle damage, scorched exhaust staining. A single small horned skull motif on the prow —
> one, not many; this is a rank-and-file raider, not the flagship. Steampunk-space detailing:
> exposed pipework, brass fittings, riveted armour, hanging chain. Bold dark outlines, painted
> shading, strong red rim light. Isolated cutout on a fully transparent background — no
> background, no starfield, no ground shadow. 1200×896. No text, no lettering, no numerals, no
> readable insignia of any kind.

For the `_sw` version, regenerate the identical ship from the opposite diagonal (nose toward
the lower left), or horizontally mirror the `_ne` art — the existing pairs are close enough to
mirrors that either reads correctly in game.

### Sable Renn's *Half-Light* · `Assets/obj/half_ne.png` + `half_sw.png`

Bounty 2's interceptor. Deliberately the **opposite of the Blood Crown**: no skulls, no
horns, no red. Where Drax is a war machine dressed as a threat, the Half-Light is a working
courier ship that has been pushed far past what it was built for. The blink drive is the only
extravagant thing on it, and it is visibly hurting the airframe.

> Painted semi-stylised sci-fi game sprite of a small, extremely fast blink-drive interceptor,
> seen from a top-down three-quarter view, filling the frame. A slender, elegant courier hull
> — long and needle-nosed with a narrow canopy set far forward and swept delta wings folded
> tight to the body, built for speed rather than war. Pale bone-white and cold grey plating
> with faded teal trim, scuffed and patched, an honest working ship kept immaculate for years
> and then run into the ground. Bolted along its spine is an oversized experimental blink
> drive that plainly does not belong: an exposed brass-and-glass coil assembly glowing pale
> cyan-white, wrapped in improvised heat shrouding and cabling, scorching the hull plate
> around its mounts. The rear third of the ship looks faintly **unfinished** — plating and
> panel edges fading toward translucency, hairline cyan fractures running forward from the
> drive, a ghost of a second silhouette offset a few pixels behind the hull like an
> afterimage. Small twin engines, almost no visible weaponry, a pair of compact mine dispensers
> underslung near the tail. Steampunk-space detailing: brass fittings, rivets, exposed
> pipework, worn leather-wrapped grips. Bold dark outlines, painted shading, cool cyan rim
> light against a dark hull. Isolated cutout on a fully transparent background — no
> background, no starfield, no ground shadow. 1200×896. No text, no lettering, no numerals, no
> readable insignia of any kind.

### Harkin Dross's *Tithe* · `Assets/obj/tithe_ne.png` + `tithe_sw.png`

Bounty 3's siege barge. The third point of the triangle: Drax's Blood Crown is a **war
machine**, Sable's Half-Light is a **fragile thoroughbred**, the Tithe is **industrial plant
that was never meant to fight** — an ore hauler with the works' own armour bolted onto it. It
should look heavy, slow, bodged together, and absolutely immovable.

> Painted semi-stylised sci-fi game sprite of a huge, slow armoured industrial barge, seen
> from a top-down three-quarter view, filling the frame. Unmistakably a **converted ore
> hauler**, not a warship: a long slab-sided hull with bulk ore hoppers along its spine, a
> conveyor gantry, heavy hydraulic arms and a squat blockish bridge set well back. Bolted over
> its flanks are **three enormous mismatched slabs of blast plating**, clearly scavenged from
> mine workings and welded on at angles, each scarred and dented, with the raw weld beads
> still showing. Mounted on the bow are a pair of massive **crusher rams** — industrial ore
> jaws repurposed as weapons, blunt and pitted. Ochre, rust-orange and grimy steel, dust
> caked into every recess, hydraulic fluid stains; amber worklights and the hot orange glow of
> a furnace throat venting between the plates. Two big slow thruster nozzles, minimal
> weaponry beyond the rams. Steampunk-space detailing: rivets, exposed pipework, brass
> pressure gauges, heavy chain slung along the rails. Bold dark outlines, painted shading,
> warm amber rim light against a dark hull. Isolated cutout on a fully transparent background
> — no background, no starfield, no ground shadow. 1200×896. No text, no lettering, no
> numerals, no readable insignia of any kind.

---

## Bounty target CGs and portraits (B4)

Two images per bounty, matching what Drax already has:

| | Path | Format |
|---|---|---|
| **Encounter CG** | `Assets/CG/cg_<name>.png` | Wide 16:9 splash shown as the fight opens, dialogue bar across the bottom. **Export at 1920×1080** — Drax's came in at 7552px/40 MB, which is slow to decode in-game. |
| **Avatar** | `Assets/char/bounties/<name>.png` | Full-body character on a transparent background, ~1200×896, same style as the crew. The board crops head-and-shoulders from it automatically. |

⚠️ Keep the **central lower third of a CG clear** — the dialogue bar sits there.

### Sable Renn — encounter CG · `Assets/CG/cg_afterimage.png`

Drax's CG is a throne: him standing on his warship, symmetrical, in command. Hers should be
the opposite — **caught mid-escape, off-centre, already half gone**.

> Dramatic wide 16:9 sci-fi splash illustration, 1920×1080, painted semi-stylised comic-book
> style with bold dark outlines and strong rim lighting. A lone slender white-and-grey blink
> interceptor tearing across the frame at a diagonal through a dim shipping lane, caught at
> the instant it jumps. The ship is **repeated three times across the image as fading
> afterimages** — sharp and solid at the leading edge, translucent and cyan-fractured behind,
> the trailing copy almost gone. Pale cyan-white light bleeds from an oversized brass blink
> drive on its spine. Behind and around it drift **stranded freighters, dark and powerless**,
> running lights out, one venting a slow plume — disabled, not destroyed. Small
> cyan-glowing mines hang in the ship's wake like scattered seed. Inset into the upper area,
> the pilot: a lean woman in a worn flight suit and cracked visor, one hand on the yoke, her
> own figure edged with the same cyan fracturing as her ship, her expression tired and
> apologetic rather than triumphant. Cold palette — bone white, cold grey, deep blue-black
> void, cyan glow, one small warm amber light in a freighter window. Sense of speed, silence
> and loss. Keep the central lower third relatively uncluttered for a dialogue bar. No text,
> no lettering, no numerals, no readable insignia of any kind.

### Sable Renn — avatar · `Assets/char/bounties/afterimage.png`

> Clean anime / JRPG character art, bold dark outlines, cel shading with soft gradients. A
> full-body standing portrait of a lean woman in her mid-thirties, a blockade-running courier
> pilot. Wiry and light-framed, pale skin, dark hair cut short and practical with a cyan
> streak, sharp tired eyes and dark circles under them. Quietly wry expression, not hostile —
> someone apologising in advance. She wears a worn pale-grey flight suit with faded teal trim
> and a scuffed leather harness, patched at the elbows, a cracked visor pushed up on her
> forehead, brass-fitted gloves and a compact sidearm holstered but clearly unused. Her left
> arm and the left side of her body are **faintly translucent and fractured with fine cyan
> lines**, as if part of her is still somewhere else — subtle, not gory. Steampunk-space
> detailing: brass buckles, rivets, exposed cabling on the harness. Cool cyan rim light from
> one side against a neutral fill. Standing straight on, relaxed, hands loose. Isolated cutout
> on a fully transparent background — no background, no floor, no shadow. Portrait 1200×896.
> No text, no lettering, no numerals, no readable insignia of any kind.

### Harkin Dross — encounter CG · `Assets/CG/cg_tollman.png`

The third composition should be **static and blocking**. Drax's CG is a throne; Sable's is an
escape; Dross's is a **closed road**. Symmetrical, heavy, filling the frame — a wall you have
to get through, with a queue of ships waiting behind it.

> Dramatic wide 16:9 sci-fi splash illustration, 1920×1080, painted semi-stylised comic-book
> style with bold dark outlines and strong rim lighting. An enormous rust-and-ochre armoured
> ore barge parked **broadside across the middle of the frame**, blocking a shipping lane
> completely — slab-sided, plated with mismatched welded blast shields, two huge industrial
> crusher rams on the bow, amber worklights burning along its length and a furnace throat
> glowing hot orange between the plates. It fills the composition edge to edge, deliberately
> immovable. Behind and beyond it, a **queue of ordinary freighters holding station**, running
> lights on, waiting their turn — no wrecks, nothing burning; this is a toll gate, not a
> massacre. In the foreground lower left, seen from behind and small against the barge, a
> single ship approaching that clearly is not going to pay. Inset in the upper right, the
> man himself: a broad grey-bearded ore foreman in a heavy work coat, entirely calm, holding
> a brass-cornered ledger slate, looking out at you with the patience of someone reading an
> invoice. Warm industrial palette — ochre, rust, dust, amber light — against the cold blue
> black of the lane. Keep the central lower third relatively uncluttered for a dialogue bar.
> No text, no lettering, no numerals, no readable writing on the ledger or anywhere else.

### Harkin Dross — avatar · `Assets/char/bounties/tollman.png`

> Clean anime / JRPG character art, bold dark outlines, cel shading with soft gradients. A
> full-body standing portrait of a heavy-set man in his late fifties, a former ore-haulage
> foreman turned toll collector. Broad and thick through the chest and shoulders, weathered
> tanned skin, close-cropped grey hair and a full grey beard, deep lines around the eyes.
> Calm, courteous, entirely unbothered — the expression of a man about to explain a charge to
> you, not threaten you. He wears a long heavy canvas work coat in ochre and rust over a
> grease-stained vest and industrial harness, thick mining gauntlets, a brass-buckled belt
> hung with tools and a coil of chain. Under one arm he carries a **brass-cornered ledger
> slate**; his other hand rests easily at his side. Steampunk-space detailing: rivets, brass
> pressure gauges, worn leather, heavy stitching. Warm amber worklight from one side against
> a neutral fill. Standing square on, feet planted, immovable. Isolated cutout on a fully
> transparent background — no background, no floor, no shadow. Portrait 1200×896. No text, no
> lettering, no numerals, no readable writing on the ledger or anywhere else.
>
> *(He should read as kin to Dova Krezh at Quarry Station — same industry, same dust, twenty
> years older and gone into business for himself. Deliberate echo; don't copy her design.)*

---

## Station keepers (C2)

One keeper per station, standing behind their own counter — the face you talk to when you
dock. Paths: **`Assets/char/keepers/<id>.png`** — `hub.png`, `neb.png`, `moon.png`,
`armada.png`. Wired via `keeperLayout`/`drawStationView`; a missing file just leaves the old
centred, keeper-less layout, so these can land one at a time.

**Format — different from the crew art, read this first.** These are **waist-up**, portrait
**896×1200**, **transparent background**. *Not* full-body like `Assets/char/<NAME>/<Name>-Status.png`:
the painted counter covers everything below the waist anyway, and a head-to-waist slice of a
full body is a wide, short region that eats too much screen width to fit beside the UI panel at
1280px. Fill the frame — head near the top edge, cut at the waist, minimal empty margin, since
the drawn width comes straight from the image's aspect ratio.

**Style** must match the existing crew art: clean anime / JRPG character art, bold dark
outlines, cel shading with soft gradients, saturated but not garish. Facing the viewer,
three-quarter or straight on, relaxed, at ease behind their own counter — this is a greeting,
not a combat pose. Keep the palette in each one keyed to its room so they don't look pasted in.

Names below are drafts — rename freely, the art is what matters and the `id` filenames don't
change.

### Waypoint Hub · `Assets/char/keepers/hub.png` — *Marla Quen, stationmaster*

The tidiest, most prosperous station in the sector, and the player's first stop. She's the
welcome mat: brisk, warm, treats you like a regular from the first minute.

> Clean anime / JRPG character art, bold dark outlines, cel shading with soft gradients. A
> waist-up portrait of a woman in her early fifties, the stationmaster of a prosperous
> deep-space trade post. Solid, capable build, warm brown skin, greying black hair pinned up
> neatly with a few loose strands. Laugh lines, direct friendly gaze, the faint patient smile of
> someone who has heard every haggle twice. She wears a smart double-breasted quartermaster's
> coat in deep navy with brass buttons and gold piping over a high-collared cream shirt, a
> brass-framed data slate tucked under one arm, reading glasses hung on a chain. Steampunk-space
> aesthetic: brass fittings, riveted trim, practical tailoring. Warm brass lamplight from the
> front left, cool cyan screen glow rimming her right side. Relaxed, welcoming, at ease behind
> her own counter. Framed head to waist, filling the frame, head near the top edge. Isolated
> cutout on a fully transparent background — no background scenery, no floor, no shadow cast
> onto anything. Portrait orientation 896×1200. No text, no lettering, no numerals, no insignia
> with readable writing of any kind.

### Veil Anchorage · `Assets/char/keepers/neb.png` — *Oris Vale, relic dealer*

Deep in the Whispering Nebula, dealing in relics nobody can explain. Half appraiser, half
mystic; prices a find like a jeweller and talks about it like an omen.

> Clean anime / JRPG character art, bold dark outlines, cel shading with soft gradients. A
> waist-up portrait of a lean elderly man, a dealer in strange relics aboard a nebula station.
> Late sixties, pale weathered skin lit violet and teal, long silver hair tied back, a close
> grey beard. Sharp, amused, knowing expression — someone who enjoys knowing more than you do.
> He wears layered robes of deep violet and dusk blue over a worn brass-fitted pressure suit,
> the collar open, heavy rings on long fingers, an appraiser's jeweller loupe on a headband
> pushed up onto his forehead. He holds a small unidentifiable crystalline artifact up between
> two fingers, glowing faint cyan and lighting his face from below. Steampunk-space aesthetic:
> brass fittings, riveted trim, worn leather. Magenta and teal nebula light, cool and moody,
> with the artifact as a warm focal glow. Framed head to waist, filling the frame, head near the
> top edge. Isolated cutout on a fully transparent background — no background scenery, no floor,
> no shadow cast onto anything. Portrait orientation 896×1200. No text, no lettering, no
> numerals, no insignia with readable writing of any kind.

### Quarry Station · `Assets/char/keepers/moon.png` — *Dova Krezh, ore foreman*

The mining station: raw ore, dust and heavy machinery. Blunt, fair, no patience for haggling —
the counterweight to Marla's warmth.

> Clean anime / JRPG character art, bold dark outlines, cel shading with soft gradients. A
> waist-up portrait of a powerfully built woman in her forties, foreman of an ore-processing
> station. Broad shoulders, thick forearms, tanned skin grey with rock dust, a short blunt
> undercut of dark hair, an old scar through one eyebrow. Flat, level, unimpressed expression —
> fair but done talking. She wears heavy canvas mining overalls in ochre and rust over a grease-
> stained vest, a brass-buckled tool harness across her chest, welding goggles pushed up on her
> forehead. Her left forearm is a battered brass-and-steel prosthetic, plainly built for work
> rather than looks. Steampunk-space aesthetic: rivets, brass, worn heavy steel. Harsh white
> floodlight from above, hot orange furnace glow spilling from the lower left. Arms folded,
> planted, immovable. Framed head to waist, filling the frame, head near the top edge. Isolated
> cutout on a fully transparent background — no background scenery, no floor, no shadow cast
> onto anything. Portrait orientation 896×1200. No text, no lettering, no numerals, no insignia
> with readable writing of any kind.

### Salvage Reach · `Assets/char/keepers/armada.png` — *Wick, scrapper*

A yard built inside a gutted warship, out where the Silent Armada drifts. Young, wiry, magpie
energy — will buy absolutely anything and talk the whole time.

> Clean anime / JRPG character art, bold dark outlines, cel shading with soft gradients. A
> waist-up portrait of a wiry young scrapper in their early twenties, running a salvage yard
> built inside a gutted warship. Slight build, freckled brown skin smudged with grease, messy
> copper-red hair sticking up at angles, a wide crooked grin and bright eager eyes — a magpie
> who has just spotted something shiny. They wear a patched flight jacket in faded green over a
> scavenged mesh undersuit, mismatched gloves, a bandolier of hand tools and stripped
> components slung across the chest, and heavy brass-rimmed magnifying goggles shoved up into
> their hair. One hand holds up a salvaged component like it's treasure. Steampunk-space
> aesthetic: brass, rivets, improvised gear, everything mended. Cold green-white worklight from
> the side, warm string-bulb light behind. Loose, animated, mid-sentence. Framed head to waist,
> filling the frame, head near the top edge. Isolated cutout on a fully transparent background —
> no background scenery, no floor, no shadow cast onto anything. Portrait orientation 896×1200.
> No text, no lettering, no numerals, no insignia with readable writing of any kind.

⚠️ **Transparent background is load-bearing here.** These are composited over the painted room
at runtime. A generation that comes back on a white, grey or scenic background — or with a
drop shadow / ground plane baked in — will draw as a visible rectangle over the backdrop.
Reject those even if the character is right. Same for a full-body result: crop it to the waist
before saving, or the figure will float above the counter instead of standing behind it.

---

⚠️ **Watch the centre glyph.** The first pass at this prompt asked for a "geometric
star/hex glyph" and the generator produced a hexagram — a gold coin stamped with a Star of
David, which reads as an antisemitic trope and was thrown away. Keep the glyph pinned to a
specific non-symbolic shape and keep the explicit "no religious, national, or cultural
symbolism" clause. Safe motifs: four-pointed compass star, concentric rings, chevrons,
orbital ellipse. Avoid: hexagrams, crescents, red five-pointed stars, anything flag-like.
At 24px the glyph is a few pixels anyway — a plain ringed coin with no glyph is a fine
fallback if the generator keeps drifting.


---

## Opening cinematic — "Journey Begins" (`Assets/intro/`)

The 12 shots behind the opening narration in `episode1.html` (`PROLOGUE_SHOTS`). One still
per narration line; the engine pans/zooms each one (Ken Burns) and crossfades between them,
so **leave headroom** — the image is scaled 1.02–1.55x and can drift ±3% horizontally.
Any missing file just plays black, so these can land one at a time.

**House style for the whole sequence** (paste into every prompt): painted sci-fi matte
painting, cinematic widescreen, deep blue-black space with warm amber accents, soft
volumetric light, no lens flare spam, no text, no lettering, no numerals, no UI. Landscape
16:9. Matches the existing `Assets/CG/` art — hand-painted, semi-stylised, slightly
steampunk-brass in the ship details.

**The StarGear** where it appears: a small brass-and-iron exploration vessel — riveted
warm-gold hull plates, an exposed gear housing amidships, twin cyan thruster glow, stubby
swept wings. It should read as tiny and hand-made against everything around it.

Composition note: the narration sits across the **lower third**, so keep that band quiet —
no critical detail below ~70% height.

### I1 — `1.png` · "Out here…" · zoom in

> Empty deep space, almost entirely black, with a faint dusting of distant stars gathering
> toward the centre. No ships, no planets, no nebula — just the void and the first suggestion
> of starlight. Extremely dark, high contrast, a sense of enormous empty distance.

### I2 — `2.png` · "It's easy to believe we're alone." · zoom out

> A single small starship in silhouette, dead centre and very small in frame, drifting through
> empty black space. Only its two cyan thruster lights and a thin rim of starlight along the
> hull are visible. Overwhelming negative space around it.

### I3 — `3.png` · "Just one ship drifting…" · slow orbit

> Three-quarter view of the small brass exploration ship from slightly below, hull catching a
> cold blue-white key light from the left and a faint warm glow from its own windows. Stars
> streaming past behind it. Ship occupies the upper-middle of the frame, closer than in I2 but
> still dwarfed by the field of stars.

### I4 — `4.png` · "But space isn't empty." · pan right

> A vast nebula beginning to glow across the frame — magenta, teal and gold gas clouds lit from
> within, layered in depth with dark dust lanes. The tiny ship as a distant silhouette near the
> left edge for scale. Awe, not danger.

### I5 — `5.png` · "It's alive." · pan left

> A busy corner of space: several small ships crossing at different distances, streaks of
> meteors, a large planet rotating in the middle distance, glowing traffic lights strung between
> distant stations. Layered, full of motion and small points of light. Warm and populated.

### I6 — `6.png` · "Every star…" · zoom in

> Close-up of a brilliant star filling most of the frame — churning golden-white plasma surface,
> arcing prominences, a corona bleeding into the dark. Dramatic, blinding, dominant.

### I7 — `7.png` · "Every world…" · pan right

> A beautiful ringed planet seen from above the ring plane — banded turquoise and cream
> atmosphere, crisp shadowed rings casting a line across the globe, two small moons. Serene,
> postcard-perfect, sunlight raking from the right.

### I8 — `8.png` · "Every life…" · zoom in

> A small convoy of five or six mismatched civilian ships travelling in loose formation,
> mid-distance, lit warmly from behind by a distant sun. Windows and running lights visible.
> Intimate and human in scale against a huge quiet starfield.

### I9 — `9.png` · "They're all connected…" · pan left

> A wide view of a star system network: rivers of pale blue-white light arcing between distant
> suns like glowing highways through space, curving across the frame and converging toward the
> horizon. Points of light where lanes meet. Ordered, luminous, web-like.

### I10 — `10.png` · "…turning together like gears in a machine…" · slow orbit

> The signature shot: two or three enormous spiral galaxies rendered as vast interlocking
> clockwork gears — brass teeth and armatures woven into the spiral arms, star-dust catching the
> ridges, meshing where the arms meet. Cosmic scale but unmistakably a mechanism. Deep blue-black
> with warm brass highlights.

### I11 — `11.png` · "Sometimes a single choice…" · zoom in

> Rear three-quarter view of the small brass ship accelerating away from camera, thrusters
> flaring bright cyan into long tails, hull leaning into the burn. Stars beginning to elongate.
> Motion and commitment.

### I12 — `12.png` · "…is enough to set that machine in motion." · hard rush 🔁 needs a re-roll

> The warp jump, as a completely wordless abstract background plate. A tunnel of cool blue-white
> light streaks radiating outward from a small point near the upper-middle of the frame, with the
> tiny dark silhouette of a ship dissolving into it. **The centre must be a contained glow, not a
> blown-out white blast** — keep the brightest core small and let the streaks fall off to deep
> navy and near-black toward the edges, so overlaid title text stays readable. The bottom third
> of the frame should be the darkest, quietest part of the image: streaks only, no subject, no
> emblem, no bright mass. Pure speed and light, nothing else in frame.
>
> Absolutely no text, no lettering, no words, no logo, no wordmark, no title treatment, no gear
> emblem, no badge, no insignia, no watermark, no signature, no numerals of any kind anywhere in
> the image. This is a plain background plate — the title is drawn over it in the game.

⚠️ **The first generation came back with a title baked in.** It painted a large
"STAR GEAR ODYSSEY" wordmark and gear emblem across the lower half — wrong game name, fighting
the engine's own title card, and cropped mid-word by the shot's zoom. The centre was also blown
out to pure white, which washed out the overlaid title text.

This shot is the one the **STARGEAR / EPISODE 0 / The Ghost Signal** card fades up over, so it
has two hard jobs: carry no lettering of its own, and stay dark enough in the middle band for
white text to sit on it. Reject any result with a logo in it, however good the light looks.
If the generator keeps insisting on a wordmark, ask for "an abstract light-speed texture" and
drop the word "warp" — that's what pulls it toward movie-poster compositions.

### I13-I20 — the closing passage · ⏳ not generated

The VO continues for ~20s past the original 12-line script (Voss's closing monologue).
These eight shots currently **reuse earlier stills as placeholders** — they read, but they
repeat. Same house style, StarGear description and lower-third rule as I1-I12 above.
Marked `todo:true` in `PROLOGUE_SHOTS`.

### I13 — `13.png` · "A rescue answered." · pan left

> A small civilian ship adrift and dark, listing, with one cyan searchlight from the rescuing
> brass vessel sweeping across its hull. Warm rescue light against cold dead metal. Hopeful,
> not triumphant.

### I14 — `14.png` · "A path unexplored." · pan right

> A narrow gap opening in a dense dust cloud, revealing an unmapped star system glowing faintly
> beyond it. The tiny brass ship poised at the threshold, small at the lower left. Invitation
> and unknown.

### I15 — `15.png` · "A stranger who becomes a friend…" · zoom in

> Two small ships of very different make drifting hull-to-hull in open space, docking clamps
> joined, warm light spilling between them. Quiet, companionable, no weapons visible.

### I16 — `16.png` · "…or an enemy." · zoom in

> The same silhouette turned hostile: a single angular warship emerging from shadow, red running
> lights, gun ports lit, bearing down on the viewer. Cold red and black against the blue palette
> of the rest of the sequence — this is the one shot that breaks the warmth.

### I17 — `17.png` · "I don't know what waits for us beyond the next jump." · pan left

> Looking out from behind the brass ship toward a distant, ambiguous light — could be a star,
> could be something else. Heavy dark foreground, the ship small and centred, the light far off.
> Uncertainty rather than threat.

### I18 — `18.png` · "None of us do." · zoom out

> Pulled far back: the ship reduced to a single point of light against an enormous field of
> stars and faint galaxies. The most empty, humbling frame in the sequence. Echoes I1.

### I19 — `19.png` · "But that's why we keep moving forward." · zoom in

> The brass ship in three-quarter view running steady toward the upper right, thrusters lit warm
> and even, a sunrise-coloured nebula opening ahead of it. Resolve and forward motion — the
> emotional turn of the whole monologue.

### I20 — `20.png` · "I'm Captain Elias Voss, and this is the voyage of the StarGear." · hard rush

> Optional — `12.png` (the warp jump) currently carries this line into the title card and works
> well. Only generate a replacement if you want the closing line on the ship rather than the jump:
> a heroic low three-quarter hero shot of the StarGear filling the frame, lit warm from below,
> stars streaking behind.
