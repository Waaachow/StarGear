# Transcribe -> align -> cut the SIX "E2" combat-bark masters (audio/Combat/<Name>_E2.mp3)
# into the v0.6 third-ability clips. Same route as cut_combat.py, but each character's
# clips are numbered starting at START[name] (continuing their existing run) instead of 1.
#
#   python cut_combat_e2.py
#
# The line lists below MUST stay in the same order as each character's new run in
# CREW_BARKS / COMBAT_BARK_SCRIPT.md — that order is the clip numbering.
import os, re, json, difflib, subprocess
from faster_whisper import WhisperModel

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "audio", "Combat")
FFM  = r"C:\Users\Steve\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FFP  = FFM.replace("ffmpeg.exe", "ffprobe.exe")
PAD_H, PAD_T = 0.12, 0.30      # breathing room head/tail

# new third-ability lines (3 per crew), and the clip number the run continues from
LINES = {
 "Astra":  ["Evasive pattern — try to hit that.",
            "Juking hard — their aim's a guess now.",
            "Too slippery for you."],
 "Rex":    ["Railgun's charged — punching straight through!",
            "One shot, one very long hole.",
            "Full spike — right down the line!"],
 "Kael":   ["Disruptor pulse — their systems are seizing.",
            "Overloaded them. They'll skip a beat.",
            "Frying their circuits — hold there."],
 "Voss":   ["Focus fire — everyone, that one.",
            "Mark's on the target. Hit it together.",
            "Concentrate on my mark."],
 "Tessa":  ["Venting plasma — clear the deck!",
            "Reactor overflow, right in their faces.",
            "Hot exhaust coming through!"],
 "Selyra": ["Triage — everyone's back on their feet.",
            "All hands, up! I've got you.",
            "No one stays down on my watch."],
}
START = { "Astra": 9, "Rex": 10, "Kael": 11, "Voss": 6, "Tessa": 10, "Selyra": 8 }

def toks(s):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "")).split() if t]

print("loading whisper (base, cpu)...")
model = WhisperModel("base", device="cpu", compute_type="int8")

manifest, any_unmatched = {}, False
for name, lines in LINES.items():
    src = os.path.join(SRC, f"{name}_E2.mp3")
    if not os.path.exists(src):
        print(f"!! MISSING {src} — skipped"); any_unmatched = True; continue

    segments, _ = model.transcribe(src, language="en", vad_filter=False, word_timestamps=True)
    words = [{"w": w.word, "s": w.start, "e": w.end}
             for seg in segments for w in (seg.words or [])]
    full = "".join(w["w"] for w in words).strip()

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
    print(f"\n{name:7s} E2  match={sm.ratio():.3f}")
    print(f"   heard: {full[:140]}")

    dur = float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
    out_lines = []
    for i, sp in enumerate(spans):
        num = START[name] + i
        if sp is None:
            print(f"   {num:2d}. !! NO MATCH  {lines[i]}"); continue
        s, e = sp
        lo = 0.0 if i == 0 or spans[i-1] is None else (spans[i-1][1] + s) / 2
        hi = dur if i == len(spans)-1 or spans[i+1] is None else (e + spans[i+1][0]) / 2
        a = max(lo, s - PAD_H, 0.0)
        b = min(hi, e + PAD_T, dur)
        out = os.path.join(SRC, f"{name.lower()}_{num:02d}.mp3")
        subprocess.run([FFM, "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                        "-i", src, "-ac", "1", "-ar", "44100", "-b:a", "192k",
                        "-af", "afade=t=in:st=0:d=0.04,afade=t=out:st=%.3f:d=0.06" % max(b-a-0.06, 0),
                        out], check=True)
        out_lines.append({"file": os.path.basename(out), "start": round(a, 2), "end": round(b, 2), "text": lines[i]})
        print(f"   {num:2d}. {a:6.2f} -> {b:6.2f}  {lines[i]}")
    manifest[name] = out_lines

json.dump(manifest, open(os.path.join(HERE, "combat_e2_manifest.json"), "w", encoding="utf-8"), indent=1)
print("\n%d clips written" % sum(len(v) for v in manifest.values()))
if any_unmatched:
    print("!! some lines had NO MATCH — check the master's read against the script")
