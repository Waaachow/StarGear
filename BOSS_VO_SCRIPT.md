# Bounty boss VO — recording script

Boss dialogue lives on each spec in `iso_grid_prototype.html` as
`lines: { start, hp50, hp25, defeat }`. Each beat is an array of consecutive lines, played
one after another. Same delivery and cutting route as the crew chatter and the station
keepers: **one master per character with all their lines back-to-back**, cut afterwards.

| | |
|---|---|
| **Masters** | `audio/bounties/<name>.mp3` — one per boss, all lines in the order below |
| **Cut clips** | `audio/bounties/<key>_NN.mp3` — generated, don't cut these by hand |
| **Numbering** | position across the whole entry: start, then hp50, then hp25, then defeat |
| **Wiring** | the spec's `vo` is the clip prefix (`vo: "bounties/drax"`), and `BOSS_BEATS` fixes the beat order the numbering follows |

Record in the listed order with a clear beat (~1s) between lines — the cutter matches word
timings against this known text, so order is what tells it which span is which clip. Read the
lines exactly as written; if one reads badly out loud, change it here *and* in the spec.

⚠️ **Append, don't insert.** Adding a line in the middle renumbers every clip after it and
forces a re-cut of that character.

---

## Captain Malachar Drax · "The Red Reaver" · `Drax_Boss.mp3`

Nine lines, four beats. Fires as: **start** on the encounter CG · **hp50** and **hp25** when
his hull crosses those thresholds · **defeat** over the win banner.

**Direction.** He speaks like an old fleet officer, not a criminal. **He never shouts.**
Confident, unshakably calm, unhurried even while losing. He genuinely respects a capable
opponent — the 50% line is approval, not a threat. The 25% line is spoken to the ship, half to
himself, with affection. The defeat lines are tired rather than bitter: a man finally allowed
to put something down.

### Beat 1 — encounter (`drax_01`, `drax_02`)

Another bounty hunter.

Tell me... do they even know why they want me dead?

> The first line is flat, almost bored — he's seen many. The second is a real question, and the
> pause is him deciding whether it's worth asking.

### Beat 2 — 50% hull (`drax_03`, `drax_04`)

Good.

It's been years since someone made me earn a victory.

> "Good." is a commander praising a subordinate's shot. Warm, not sarcastic.

### Beat 3 — 25% hull (`drax_05`, `drax_06`)

This ship...

...she still remembers war.

> Quieter. To the ship, not to you. Pride and grief in the same breath.

### Beat 4 — defeat (`drax_07`, `drax_08`, `drax_09`)

Heh...

Perhaps...

...it's finally time to let the dead rest.

> A short breath of a laugh, not a death rattle. Three separate fragments with real gaps —
> he's thinking between them. The last line is relief.

---

## Sable Renn · "The Afterimage" · `red_reaver.mp3`'s sibling — `audio/bounties/afterimage.mp3`

Nine lines, four beats, same shape as Drax. Clip prefix **`sable`** →
`audio/bounties/sable_01..09.mp3`.

**Direction.** The deliberate opposite of Drax. He is grand, calm and certain; she is
**quiet, quick and tired**. Short breaths, clipped delivery, a dry half-smile you can hear.
She isn't taunting you — she's almost apologising, which should land as sadder than a threat.
The 25% lines are the first time she sounds frightened, and she's talking about herself, not
the fight. The defeat lines are **relief**, not despair: three small fragments with real gaps,
someone finally allowed to stop.

Never shouts. Never gloats. If a line sounds like a villain, it's wrong.

### Beat 1 — encounter (`sable_01`, `sable_02`)

You've got a good lock. That's rare.

Hold onto it. It won't last.

> Genuine, almost complimentary. The second line isn't a boast — it's a fact she's sorry about.

### Beat 2 — 50% hull (`sable_03`, `sable_04`)

There. You're learning.

Most people only ever shoot where I was.

> Approval. She's enjoying being properly chased for once.

### Beat 3 — 25% hull (`sable_05`, `sable_06`)

...I can't feel the third jump any more.

That's how it takes you. A piece at a time.

> Quieter, to herself. This is the drive eating her, not the damage. First real fear.

### Beat 4 — defeat (`sable_07`, `sable_08`, `sable_09`)

Oh.

It's quiet.

...I'd forgotten quiet.

> Not a death rattle. Surprise, then stillness, then something close to gratitude.

---

## Harkin Dross · "The Tollman" · `audio/bounties/tollman.mp3`

Nine lines, four beats. Clip prefix **`dross`** → `audio/bounties/dross_01..09.mp3`.

**Direction.** The third voice, and the trick is that he is **not angry and not threatening**.
He's a shift boss reading you an invoice. Unhurried, courteous, faintly weary — the tone of
someone who has had this conversation a thousand times and is mildly disappointed you're
going to make it difficult. Anger would be unprofessional.

The menace comes entirely from how reasonable he sounds. He genuinely believes he is the last
honest man on the drift.

The 25% beat is the first crack: not fear, **surprise** — nobody has ever got this far. The
defeat lines are a man closing a book, and the last one is the only time in the whole fight he
lets any grievance show.

### Beat 1 — encounter (`dross_01`, `dross_02`)

Southern drift is a toll road. You'll have been told.

No? Then we'll do this the other way.

> Flat, procedural. The second line is regret, not relish — he'd rather you'd just paid.

### Beat 2 — 50% hull (`dross_03`, `dross_04`)

You're through the first plate. That's further than most.

I'll add the repairs to your account.

> Genuine credit where it's due, then straight back to business. The second line is dry
> humour delivered completely straight.

### Beat 3 — 25% hull (`dross_05`, `dross_06`)

...you're actually going to do it.

Twenty years I held this lane.

> Surprise, then something quieter. The second line is said to himself.

### Beat 4 — defeat (`dross_07`, `dross_08`, `dross_09`)

Ledger's closed, then.

Tell them...

...tell them I was owed.

> Matter-of-fact, then a long pause, then the only bitter line he has. Don't shout it — it
> should sound like it costs him to say.

---

## ✅ Drax delivered and cut — 2026-07-21

Master `audio/bounties/red_reaver.mp3` → nine clips `audio/bounties/drax_01..09.mp3`.

```
python transcribe_boss.py    # word timestamps -> boss_vo.json
python align_boss.py         # match against the text above -> boss_spans.json
python cut_boss.py           # -> audio/bounties/<key>_NN.mp3
```

Two things this pipeline had to do that the keeper one didn't:

**1. A non-lexical line.** "Heh..." is a laugh — whisper transcribes no words for it, so text
matching can never place it. `align_boss.py` falls back to an **energy search**: any line that
matches no words is placed by finding the loudest contiguous run of sound in the gap between
its neighbours. It reported doing so, and landed it at 18.01–18.21s.

**2. Drifted word timings.** Whisper put the boundary between "Perhaps..." and the final line
at 19.58s — *inside the word "Perhaps"*, which actually runs 19.17–19.90. The first cut
therefore chopped "Perhaps" in half and started the last line with its tail. `cut_boss.py` now
**snaps each boundary to the centre of the nearest real silence run** (`silence_runs` /
`boundary`) rather than to the quietest single frame, because inside continuous speech there is
always *some* minimum and it means nothing. The boundary moved to 20.05s, in the true pause.
⚠️ Boundaries are deliberately **not** clamped to the aligner's spans — when the timings have
drifted, the span itself is wrong and clamping would preserve the error.

**Verified:** eight of nine clips transcribe back to their own line at a 1.00 match with silent
edges; the ninth is the laugh, which transcribes as "Oh, hell." and is correct by ear-independent
measures (right length, right position, clean edges). Subtitle timing is taken from each clip's
real duration at runtime — measured cold and warm — so re-recording a line needs no code change.
Unvoiced, everything still works on the `BOSS_LINE_MS` fallback.
