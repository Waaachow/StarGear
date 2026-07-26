# Transcribe -> align -> cut audio/Rumours/Crimson_greet.mp3 (the "crimson_greet" revisit
# scene) into audio/Rumours/vo/crimson_greet_NN.mp3, and merge into scene_vo.json alongside
# the existing crimson_nova cut from cut_rumours.py.
#
#   python cut_crimson_greet.py
import os, re, json, difflib, subprocess
from faster_whisper import WhisperModel

HERE = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(HERE, "audio", "Rumours")
OUTDIR = os.path.join(SRCDIR, "vo")
FFM = r"C:\Users\Steve\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FFP = FFM.replace("ffmpeg.exe", "ffprobe.exe")
PAD_H, PAD_T = 0.12, 0.30

LINES = [
    "StarGear! Back for a dose of inspiration?",
    "Still keeping the void honest, I trust. The Nova is watching!",
]

def toks(s):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "")).split() if t]

src = os.path.join(SRCDIR, "Crimson_greet.mp3")
print("loading whisper (base, cpu)...")
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, _ = model.transcribe(src, language="en", vad_filter=False, word_timestamps=True)
words = [{"w": w.word, "s": w.start, "e": w.end} for seg in segments for w in (seg.words or [])]
full = "".join(w["w"] for w in words).strip()
print(f"heard: {full}")

heard = [re.sub(r"[^a-z0-9]", "", w["w"].lower().replace("'", "")) for w in words]
heard_i = [i for i, t in enumerate(heard) if t]
heard_t = [heard[i] for i in heard_i]
want, owner = [], []
for li, ln in enumerate(LINES):
    for t in toks(ln):
        want.append(t); owner.append(li)
sm = difflib.SequenceMatcher(a=want, b=heard_t, autojunk=False)
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

scene_vo_path = os.path.join(SRCDIR, "scene_vo.json")
scene_vo = json.load(open(scene_vo_path, encoding="utf-8"))

for i, sp in enumerate(spans):
    num = i + 1
    if sp is None:
        print(f"   {num:2d}. (no audio) {LINES[i]}"); continue
    s, e = sp
    lo = 0.0 if i == 0 or spans[i-1] is None else (spans[i-1][1] + s) / 2
    hi = dur if i == len(spans)-1 or spans[i+1] is None else (e + spans[i+1][0]) / 2
    a = max(lo, s - PAD_H, 0.0)
    b = min(hi, e + PAD_T, dur)
    out = os.path.join(OUTDIR, f"crimson_greet_{num:02d}.mp3")
    subprocess.run([FFM, "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                    "-i", src, "-ac", "1", "-ar", "44100", "-b:a", "192k",
                    "-af", "afade=t=in:st=0:d=0.04,afade=t=out:st=%.3f:d=0.06" % max(b-a-0.06, 0),
                    out], check=True)
    rel = "audio/Rumours/vo/crimson_greet_%02d.mp3" % num
    scene_vo["Crimson|" + LINES[i]] = rel
    print(f"   {num:2d}. {a:6.2f} -> {b:6.2f}  {LINES[i]}  -> {rel}")

json.dump(scene_vo, open(scene_vo_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("\nupdated scene_vo.json (%d total entries)" % len(scene_vo))
