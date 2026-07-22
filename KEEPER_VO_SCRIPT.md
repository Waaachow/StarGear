# Station keeper VO — recording script

Four new speaking parts, one per trade station. 20 lines total: **3 welcomes + 2 send-offs each**.
Source of truth for the text is the `KEEPERS` block in `iso_grid_prototype.html` — the lines below
are copied from it verbatim and must stay that way (see *Why the text must match* below).

Same delivery shape as the Episode 0 and Explore VO: **one recording per character with all five
lines back-to-back**, cut into per-line clips afterwards.

---

## Delivery

| | |
|---|---|
| **Masters** | `audio/Station/<Name>_Station.mp3` — one per keeper, all 5 lines in the order below |
| **Cut clips** | `audio/Station/<id>_NN.mp3` — generated, don't make these by hand |
| **ids** | `hub` (Marla) · `neb` (Oris) · `moon` (Dova) · `armada` (Wick) |
| **Numbering** | `01`–`03` = welcomes, `04`–`05` = send-offs, in table order |

**Leave a clear beat (~1s) of silence between lines** and try not to pause mid-sentence. The cutter
aligns word timings against the known text rather than hunting for silence — that's how the Explore
batch had to be done, because Voss pauses mid-sentence and Kael's second half has no usable gaps —
but clean gaps still make the result tighter and easier to check.

---

## Marla Quen · Waypoint Hub · `Marla_Station.mp3`

Stationmaster of the tidiest, busiest port in the sector, fifties. **Warm, brisk, unflappable.**
Treats the captain like a regular from the first minute. She's the friendliest voice in the game —
the counterweight to Dova.

1. Waypoint Hub, and welcome to it. Clamps are on, take your time.
2. Back again. Hold's a mess, I imagine — the counter's open.
3. Good to see the StarGear in one piece. Mostly.
4. Safe lanes, Captain. Come back with something interesting.
5. Clamps released. Don't be a stranger.

> Line 2's dash is a beat, and *"the counter's open"* is generous, not sarcastic.
> Line 3: "Mostly" is a dry aside — a small smile, not a punchline.

## Oris Vale · Veil Anchorage · `Oris_Station.mp3`

Relic dealer deep in the nebula, late sixties. **Unhurried, amused, faintly ominous.** Half appraiser,
half mystic — he enjoys knowing more than you do and is in no rush to share it. Quietest of the four;
let the lines sit.

1. The nebula let you through, then. It doesn't always.
2. Ah — a buyer. Or a seller. You've the look of both.
3. Careful what you brought in with you. Things follow, out here.
4. Go carefully. The Veil remembers a face.
5. Take what you've learned. Leave what you haven't.

> Line 2: the dash is a small pause of appraisal, sizing the captain up.
> Line 3 should be a genuine warning delivered pleasantly — that's the whole character.

## Dova Krezh · Quarry Station · `Dova_Station.mp3`

Ore foreman, forties, built like the machinery. **Blunt, flat, fair.** Not hostile — she just has work
to do and no interest in haggling. Shortest, most clipped delivery of the four.

1. Quarry Station. Ore's priced on the board and I don't haggle.
2. You're on the pad. Mind the dust, it gets everywhere.
3. Buying or selling? Either way, be quick about it.
4. Clear of the clamps. Don't scratch my dock on the way out.
5. Right. Go on, then.

> Line 5 is barely a sentence — a dismissal, almost thrown away. Keep it under a second if you can.
> Nothing here should sound angry; she's this brusque with everyone.

## Wick · Salvage Reach · `Wick_Station.mp3`

Scrapper running a yard inside a gutted warship, early twenties. **Fast, delighted, over-caffeinated.**
Magpie energy — everything the captain brings in is the best thing they've seen all week. The loudest
and most animated of the four. Gender-neutral, referred to as *they* in the code.

1. Salvage Reach! You brought me something, didn't you? You did.
2. Ohh, that hull's got some new dents. Want me to take them off your hands?
3. Come in, come in — mind the cable, that one's live.
4. Bring me back something with SERIAL NUMBERS on it!
5. Fly safe! Well — fly. Safe's optional.

> Line 1: *"You did"* is Wick answering their own question, not waiting for a reply.
> Line 4: the capitals are **emphasis**, not volume — that's the treasure, said with relish.
> Line 5: the dash is a self-correction mid-thought, quick.

---

## Why the text must match

The cutter transcribes each master with word timestamps and `difflib`-matches the heard words against
these exact strings to find where each line starts and ends. **Ad-libs, dropped words and reordered
lines break the alignment** and the clip boundaries land in the wrong place. If a line reads badly out
loud, change it *here and in `KEEPERS`* rather than improvising in the booth — send me the new wording
and I'll update the code so the two never disagree.

Mishearings are fine and expected — sequence matching absorbed "Hull's holding" → "Holes holding" on
the Explore batch without trouble. It's *missing or extra* content that hurts.

## ⚠️ Appending lines later

Clip numbers are each keeper's line order **across their whole entry** (welcomes then send-offs). So
inserting a sixth line *between* existing ones renumbers everything after it and forces a full re-cut
of that keeper. **Append new lines at the end of a pool**, or expect to re-cut. This is the same trap
as the `CHATTER` table.

## ✅ Delivered and cut — 2026-07-21

All four masters recorded, all 20 clips cut and wired.

**Pipeline** (re-run any step if a master is re-recorded):

```
python transcribe_station.py    # word timestamps -> station_vo.json
python align_station.py         # match against the text above -> station_spans.json
python cut_station.py           # -> audio/Station/<id>_NN.mp3
```

`cut_station.py` does one thing the Explore cutter didn't need: it **refines every boundary
against the waveform**, hunting for the quietest point in a ±0.32s window around where the
aligner put it. Wick's take runs lines together with no gap at all, so whisper butted three
boundaries at exactly 0.00s apart, which would have clipped word edges.

**Verified**: all 20 clips transcribe back to their own line with silent edges (nothing clipped).
The one low match score is `hub_02` — "Hold's a mess" is heard as "Hold some S", the same
mishearing as in the master; every word is present and the cut is correct.

**Playback**: `KEEPER_VO` / `playKeeperVO()` on its own channel, layered over music and SFX.
The subtitle's duration **and the send-off beat** are both taken from the clip's real duration at
runtime — so re-recording a line changes its timing automatically, with no code edit. A missing
clip or blocked autoplay degrades to a silent subtitle.
