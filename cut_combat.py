# Transcribe -> align -> cut the six combat-bark masters into the numbered clips
# CREW_BARKS references (audio/Combat/<name>_NN.mp3). Same route as the Explore
# pipeline (transcribe_explore / align_explore / cut_explore), folded into one pass.
#
#   python cut_combat.py
#
# Whisper mishears a few words, so lines are aligned as token SEQUENCES with difflib
# rather than word-for-word. The line lists below MUST stay in the same order as each
# character's run in CREW_BARKS / COMBAT_BARK_SCRIPT.md — that order is the clip numbering.
import os, re, json, difflib, subprocess
from faster_whisper import WhisperModel

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "audio", "Combat")
FFM  = r"C:\Users\Steve\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FFP  = FFM.replace("ffmpeg.exe", "ffprobe.exe")
PAD_H, PAD_T = 0.12, 0.30      # breathing room head/tail

LINES = {
 "Rex":   ["Locked on — say goodnight.",
           "Lighting 'em up!",
           "This is my favourite part.",
           "Missile away — eat that!",
           "One special delivery, incoming.",
           "Danger close? Not for us.",
           "Scratch one!",
           "Hey! Nobody takes my crew.",
           "Okay — that one I felt."],
 "Tessa": ["Pushing the reactor — don't tell the warranty.",
           "Overclocking. Everyone gets a little extra reach.",
           "Redlining her. Make it count.",
           "Patching the hull — hold still.",
           "Welding on the fly. Classic us.",
           "That'll hold. Probably.",
           "One less thing to fix.",
           "They're hit — I need a second here!",
           "That one hurt — the hull's screaming."],
 "Kael":  ["Shields up. Ten percent is ten percent.",
           "Deflectors online. Mind the gaps.",
           "Bracing the grid.",
           "Scanning — I can read their whole hand now.",
           "Got their specs. Aim for the seams.",
           "Sensors have them cold.",
           "Jamming their comms — blind for a beat.",
           "Scrambled. That bought us a turn.",
           "Their targeting just went dark.",
           "Target neutralised."],
 "Astra": ["Repositioning. Watch the burn.",
           "Sliding to a better angle.",
           "New vector — keep up.",
           "Space-hop! Blink and you missed it.",
           "Folding past them — hold on.",
           "Not where you thought I'd be.",
           "Clean kill. Next.",
           "Big hit! Evasive, now."],
 "Selyra":["Not today. On your feet.",
           "I've got you — back in the fight.",
           "Stay with me. There — up you go.",
           "Adrenaline's in — go, go!",
           "One more push. You've got this.",
           "Move while it's hot!",
           "Someone's down — cover them!"],
 "Voss":  ["I've got their station — follow my lead.",
           "Taking the helm on this one.",
           "Do as I do. Now.",
           "We do not leave people behind!",
           "Hold together. Absorb it and answer."],
}

def toks(s):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "")).split() if t]

print("loading whisper (base, cpu)...")
model = WhisperModel("base", device="cpu", compute_type="int8")

manifest, any_unmatched = {}, False
for name, lines in LINES.items():
    src = os.path.join(SRC, f"{name}_Combat.mp3")
    if not os.path.exists(src):
        print(f"!! MISSING {src} — skipped"); continue

    # ---- transcribe ----
    segments, _ = model.transcribe(src, language="en", vad_filter=False, word_timestamps=True)
    words = [{"w": w.word, "s": w.start, "e": w.end}
             for seg in segments for w in (seg.words or [])]

    # ---- align expected line text against heard words ----
    heard = [re.sub(r"[^a-z0-9]", "", w["w"].lower().replace("'", "")) for w in words]
    heard_i = [i for i, t in enumerate(heard) if t]
    heard_t = [heard[i] for i in heard_i]
    want, owner = [], []
    for li, ln in enumerate(lines):
        for t in toks(ln):
            want.append(t); owner.append(li)
    sm = difflib.SequenceMatcher(a=want, b=heard_t, autojunk=False)
    hit = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            hit[a + k] = b + k
    spans = []
    for li in range(len(lines)):
        idx = [hit[i] for i in range(len(want)) if owner[i] == li and i in hit]
        if not idx:
            spans.append(None); any_unmatched = True; continue
        ws = [words[heard_i[j]] for j in idx]
        spans.append([min(w["s"] for w in ws), max(w["e"] for w in ws)])
    print(f"\n{name:7s} match={sm.ratio():.3f}")

    # ---- cut ----
    dur = float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
    out_lines = []
    for i, sp in enumerate(spans):
        if sp is None:
            print(f"   {i+1:2d}. !! NO MATCH  {lines[i]}"); continue
        s, e = sp
        lo = 0.0 if i == 0 or spans[i-1] is None else (spans[i-1][1] + s) / 2
        hi = dur if i == len(spans)-1 or spans[i+1] is None else (e + spans[i+1][0]) / 2
        a = max(lo, s - PAD_H, 0.0)
        b = min(hi, e + PAD_T, dur)
        out = os.path.join(SRC, f"{name.lower()}_{i+1:02d}.mp3")
        subprocess.run([FFM, "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                        "-i", src, "-ac", "1", "-ar", "44100", "-b:a", "192k",
                        "-af", "afade=t=in:st=0:d=0.04,afade=t=out:st=%.3f:d=0.06" % max(b-a-0.06, 0),
                        out], check=True)
        out_lines.append({"file": os.path.basename(out), "start": round(a, 2), "end": round(b, 2), "text": lines[i]})
        print(f"   {i+1:2d}. {a:6.2f} -> {b:6.2f}  {lines[i]}")
    manifest[name] = out_lines

json.dump(manifest, open(os.path.join(HERE, "combat_manifest.json"), "w", encoding="utf-8"), indent=1)
print("\n%d clips written" % sum(len(v) for v in manifest.values()))
if any_unmatched:
    print("!! some lines had NO MATCH — check the master's read against the script above")
