# Opening narration VO — recording script

The "Journey Begins" cinematic that plays between the title screen and Scene 1. **12 lines,
one per shot**, Captain Voss narrating. Source of truth for the text is `PROLOGUE_SHOTS` in
`episode1.html` — the lines below are copied from it verbatim and must stay that way.

---

## Delivery

| | |
|---|---|
| **Master** | `audio/Intro/Speech_v3.mp3` — all 12 lines back-to-back, one take ✅ recorded, 24.66s |
| **Cutting** | None. The clip plays whole; the engine syncs the text to it by timestamp |
| **Length** | Anything. The cues are measured from the file, so a longer or shorter read is fine |

Voss is talking to himself as much as to us — **reflective, unhurried, quietly awed**. Not a
trailer voice. The register lifts once, on *"It's alive."*, then settles again.

**Two things the sequence depends on:**

1. **Leave a clear beat (~1s) of silence between every line.** Each line is a separate shot with
   its own image; the text and the picture change together. Lines run into each other and the
   pictures start cutting mid-sentence.
2. **Take a full 1.5–2s pause after line 1.** "Out here…" opens on black with the stars barely
   up — it needs room to land before line 2 arrives.

Ellipses are trailing beats, not full stops — lines 6-8 and 10-12 in particular should feel like
one thought continuing across the pauses, not six separate statements.

---

## The 12 lines

| # | Line | Shot |
|---|---|---|
| 1 | Out here… | black, stars fading up |
| 2 | It's easy to believe we're alone. | the StarGear alone, tiny |
| 3 | Just one ship drifting through an endless sea of stars. | camera circling the ship |
| 4 | But space isn't empty. | nebulae beginning to glow |
| 5 | It's alive. | traffic, meteors, a turning world |
| 6 | Every star… | close on a sun |
| 7 | Every world… | the ringed planet |
| 8 | Every life… | a small convoy |
| 9 | They're all connected… | warp lanes webbing between suns |
| 10 | …turning together like gears in a machine… | galaxies as brass clockwork |
| 11 | Sometimes a single choice… | the StarGear accelerating |
| 12 | …is enough to set that machine in motion. | warp jump → title card |

Then the **STARGEAR / EPISODE 0 / The Ghost Signal** card, drawn by the engine — don't read it.

---

## Notes per beat

> **1-2.** The quietest moment in the game. Almost a murmur.
>
> **3.** One continuous line — don't break it up. It's the longest read here.
>
> **4-5.** The turn. *"But space isn't empty"* is a small correction; *"It's alive"* is the lift —
> two words, given weight, then straight back down.
>
> **6-8.** A list, gathering. Each one slightly warmer than the last. Same cadence three times.
>
> **9-10.** The thesis. *"…turning together like gears in a machine…"* is the title drop in
> everything but name — let it breathe.
>
> **11-12.** Settle back to the opening register. *"…in motion."* is the last thing heard before
> the title card, so land it and stop — no trailing air, no sign-off.

---

## ⚠️ What not to include

Take 2 ran ~21 seconds long because it kept going past line 12 (that file has since been deleted):

> *"A rescue answered. A path unexplored. A stranger who becomes a friend… or an enemy. I don't
> know what waits for us beyond the next jump. None of us do. But that's why we keep moving
> forward. I'm Captain Elias Voss, and this is the voyage of the StarGear."*

— plus *"too vast for any of us to truly understand"* on the end of line 10. There are no shots
for any of it, so it played over recycled images. **End the take on "…in motion."**

(It's a good passage. If it's wanted later it needs ~8 more stills — prompts are parked in
`IMAGE_PROMPTS.md` as I13-I20.)

---

## After recording

Drop the new file in `audio/Intro/`, point `PROLOGUE_SRC` at it, and re-measure the cues — the old
`at:` values are timestamps into the previous take and will be wrong. Two ways:

- **By ear:** open `episode1.html?cuetune=1`, tap Space as each line starts, paste the table it
  prints to the console over `PROLOGUE_SHOTS`.
- **Measured:** transcribe with word timestamps (`faster-whisper`, `base.en`) and align the
  transcript to the script text. This is how the current values were derived — it matched 51 of
  52 words and is more accurate than tapping.
