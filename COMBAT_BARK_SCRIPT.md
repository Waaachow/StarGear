# Crew combat barks — recording script

Combat barks live in `iso_grid_prototype.html` in the `CREW_BARKS` table. A crew member
**occasionally** speaks when they act in a fight, or reacts to a kill, a crewmate going down,
or a heavy hit. Same delivery and cutting route as the crew chatter, station keepers, and boss
VO: **one master per character with all their lines back-to-back**, cut afterward.

| | |
|---|---|
| **Masters** | `audio/Combat/<Name>_Combat.mp3` — one per crew member, lines in the order below |
| **Cut clips** | `audio/Combat/<name>_NN.mp3` — generated, don't cut these by hand |
| **Numbering** | position across that character's whole run below, top to bottom |
| **Wiring** | each line's `vo` in `CREW_BARKS` already points at its clip (`rex_01.mp3`, …) |

Record in the listed order with a clear beat (~1s) between lines — the cutter matches word
timings against this known text, so order is what tells it which span is which clip. Read the
lines exactly as written; if one reads badly out loud, change it here **and** in `CREW_BARKS`.

These are **barks** — short, thrown out mid-fight, not delivered to camera. Keep them quick and
punchy; energy over polish. VO is optional: until a master is recorded, the line just shows as a
silent subtitle.

⚠️ **Append, don't insert.** Adding a line in the middle of a character's run renumbers every
clip after it and forces a re-cut of that character. New lines go at the END of that character's
list here *and* at the end of their run in the table.

---

## Rex Calder · Gunner · `Rex_Combat.mp3`

**Direction.** Cocky, trigger-happy, having the time of his life. Grins through everything. The
knocked-out line (08) is the one moment it goes hard — real anger, protective.

1. Locked on — say goodnight.
2. Lighting 'em up!
3. This is my favourite part.
4. Missile away — eat that!
5. One special delivery, incoming.
6. Danger close? Not for us.
7. Scratch one!
8. Hey! Nobody takes my crew.
9. Okay — that one I felt.

## Tessa Rourke · Engineer · `Tessa_Combat.mp3`

**Direction.** Dry, practical gearhead. Talks about the ship the way a mechanic talks about a car
she loves and complains about. Never rattled — the closest she gets is 08/09, and even then it's
"give me a second" more than panic.

1. Pushing the reactor — don't tell the warranty.
2. Overclocking. Everyone gets a little extra reach.
3. Redlining her. Make it count.
4. Patching the hull — hold still.
5. Welding on the fly. Classic us.
6. That'll hold. Probably.
7. One less thing to fix.
8. They're hit — I need a second here!
9. That one hurt — the hull's screaming.

## Dr. Kael Mercer · Science Officer · `Kael_Combat.mp3`

**Direction.** Precise, analytical, a half-step detached — he's reading instruments, not shouting.
Calm confidence. "Target neutralised" (10) is a clinical note, not a cheer.

1. Shields up. Ten percent is ten percent.
2. Deflectors online. Mind the gaps.
3. Bracing the grid.
4. Scan complete — I can see everything they've got.
5. Got their specs. Aim for the seams.
6. Sensors have them cold.
7. Jamming their comms — blind for a beat.
8. Scrambled. That bought us a turn.
9. Their targeting just went dark.
10. Target neutralised.

## Astra · Pilot · `Astra_Combat.mp3`

**Direction.** Cool, unflappable, a little playful at the stick. Flying is easy for her and it
shows. "Big hit! Evasive, now." (08) is the one time she sharpens up.

1. Repositioning. Watch the burn.
2. Sliding to a better angle.
3. New vector — keep up.
4. Space-hop! Blink and you missed it.
5. Folding past them — hold on.
6. Not where you thought I'd be.
7. Clean kill. Next.
8. Big hit! Evasive, now.

## Dr. Selyra · Medic · `Selyra_Combat.mp3`

**Direction.** Warm, steady, caring — the calm hand in the room. The revive lines (1–3) are said
straight to the crewmate she's bringing back. The adrenaline lines (4–6) push with encouragement,
not aggression. "Someone's down — cover them!" (07) is urgent but controlled.

1. Not today. On your feet.
2. I've got you — back in the fight.
3. Stay with me. There — up you go.
4. Adrenaline's in — go, go!
5. One more push. You've got this.
6. Move while it's hot!
7. Someone's down — cover them!

## Elias Voss · Captain · `Voss_Combat.mp3`

**Direction.** Steady command voice, unhurried, absolute. Never shouts. "We do not leave people
behind!" (04) is the hardest line — conviction, not volume. "Hold together. Absorb it and answer."
(05) is reassurance dressed as an order.

1. I've got their station — follow my lead.
2. Taking the helm on this one.
3. Do as I do. Now.
4. We do not leave people behind!
5. Hold together. Absorb it and answer.

---

# v0.6 additions — the third-ability barks (NOT yet recorded)

Three lines per crew, one bark set per new unlockable ability. **Numbering continues each
character's existing run** so the clip names don't collide (`audio/Combat/<name>_NN.mp3`). Same
per-character direction as above. Wired in `CREW_BARKS`; the game subtitles them and stays silent
until these are cut.

## Astra · Evasive Roll (`astra-evade`)
9. Evasive pattern — try to hit that.
10. Juking hard — their aim's a guess now.
11. Too slippery for you.

## Rex · Railgun (`rex-railgun`)
10. Railgun's charged — punching straight through!
11. One shot, one very long hole.
12. Full spike — right down the line!

## Kael · Disruptor Pulse (`kael-disruptor`)
11. Disruptor pulse — their systems are seizing.
12. Overloaded them. They'll skip a beat.
13. Frying their circuits — hold there.

## Voss · Focus Fire (`voss-focus`)
6. Focus fire — everyone, that one.
7. Mark's on the target. Hit it together.
8. Concentrate on my mark.

## Tessa · Vent Plasma (`tessa-vent`)
10. Venting plasma — clear the deck!
11. Reactor overflow, right in their faces.
12. Hot exhaust coming through!

## Selyra · Triage (`selyra-triage`)
8. Triage — everyone's back on their feet.
9. All hands, up! I've got you.
10. No one stays down on my watch.
