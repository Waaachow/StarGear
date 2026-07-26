# Transcribe -> align -> cut audio/Combat/Crimson_Combat.mp3 (CRIMSON_BARKS, 13 lines across
# 6 triggers) into audio/Combat/crimson_<trigger>_NN.mp3. Standalone script since Crimson's
# clip names are grouped per-trigger, not one flat per-character sequence like cut_combat.py.
#
#   python cut_crimson_combat.py
#
# Recording order below MUST match CRIMSON_BARKS in iso_grid_prototype.html.
import os, re, json, difflib, subprocess
from faster_whisper import WhisperModel

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "audio", "Combat")
FFM  = r"C:\Users\Steve\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FFP  = FFM.replace("ffmpeg.exe", "ffprobe.exe")
PAD_H, PAD_T = 0.12, 0.30

# (trigger, text) in CRIMSON_BARKS order — clip name is crimson_<trigger>_NN.mp3, NN restarts per trigger
LINES = [
 ("join",       "Crimson Nova, reporting for a proper show."),
 ("join",       "Try to keep up, Captain — I intend to be memorable."),
 ("attack",     "Watch closely — this is my favorite part."),
 ("attack",     "Center stage, if you please!"),
 ("attack",     "Nova Comet does it again."),
 ("super",      "For the whole audience — Supernova Strike!"),
 ("super",      "One for everyone! That's how you play a full house."),
 ("hit",        "Ha! Barely felt that. Barely."),
 ("hit",        "Alright, that one earned some respect."),
 ("ko",         "Curtain call for me — regroup without me, Captain!"),
 ("ko",         "That's the show, folks — I'm out!"),
 ("noshow",     "Can't run the show for free, Captain — find me back at the hangar once you're paid up."),
 ("noshow",     "No coin, no Comet. I'll be at the hangar."),
]

def toks(s):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "")).split() if t]

src = os.path.join(SRC, "Crimson_Combat.mp3")
print("loading whisper (base, cpu)...")
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, _ = model.transcribe(src, language="en", vad_filter=False, word_timestamps=True)
words = [{"w": w.word, "s": w.start, "e": w.end} for seg in segments for w in (seg.words or [])]
full = "".join(w["w"] for w in words).strip()
print(f"heard: {full}\n")

heard = [re.sub(r"[^a-z0-9]", "", w["w"].lower().replace("'", "")) for w in words]
heard_i = [i for i, t in enumerate(heard) if t]
heard_t = [heard[i] for i in heard_i]
want, owner = [], []
for li, (trig, ln) in enumerate(LINES):
    for t in toks(ln):
        want.append(t); owner.append(li)
sm = difflib.SequenceMatcher(a=want, b=heard_t, autojunk=False)
print(f"match ratio={sm.ratio():.3f}")
hit = {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        hit[a + k] = b + k
spans = []
for li in range(len(LINES)):
    idx = [hit[i] for i in range(len(want)) if owner[i] == li and i in hit]
    if not idx:
        spans.append(None); continue
    ws = [words[heard_i[j]] for j in idx]
    spans.append([min(w["s"] for w in ws), max(w["e"] for w in ws)])

dur = float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())

trig_count = {}
manifest = []
any_unmatched = False
for i, sp in enumerate(spans):
    trig, text = LINES[i]
    trig_count[trig] = trig_count.get(trig, 0) + 1
    num = trig_count[trig]
    if sp is None:
        print(f"   !! NO MATCH  [{trig}_{num:02d}]  {text}"); any_unmatched = True; continue
    s, e = sp
    lo = 0.0 if i == 0 or spans[i-1] is None else (spans[i-1][1] + s) / 2
    hi = dur if i == len(spans)-1 or spans[i+1] is None else (e + spans[i+1][0]) / 2
    a = max(lo, s - PAD_H, 0.0)
    b = min(hi, e + PAD_T, dur)
    out = os.path.join(SRC, f"crimson_{trig}_{num:02d}.mp3")
    subprocess.run([FFM, "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                    "-i", src, "-ac", "1", "-ar", "44100", "-b:a", "192k",
                    "-af", "afade=t=in:st=0:d=0.04,afade=t=out:st=%.3f:d=0.06" % max(b-a-0.06, 0),
                    out], check=True)
    manifest.append({"file": os.path.basename(out), "start": round(a, 2), "end": round(b, 2), "text": text})
    print(f"   {a:6.2f} -> {b:6.2f}  [{trig}_{num:02d}]  {text}  -> {os.path.basename(out)}")

json.dump(manifest, open(os.path.join(HERE, "crimson_combat_manifest.json"), "w", encoding="utf-8"), indent=1)
print("\n%d clips written" % len(manifest))
if any_unmatched:
    print("!! some lines had NO MATCH — check the master's read against the script")
