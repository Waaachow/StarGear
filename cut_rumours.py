# Transcribe -> align -> cut the Crimson Nova scene VO masters (audio/Rumours/<...>.mp3)
# into per-line clips (audio/Rumours/vo/<char>_NN.mp3). Same route as cut_combat.py.
# The line lists below MUST stay in scene order (they mirror SCENES.crimson_nova in
# episode1.html) so the clip numbering + the emitted who|text -> file map line up.
#
#   python cut_rumours.py
#
# Emits audio/Rumours/scene_vo.json and prints a paste-ready SCENE_VO block for episode1.html.
import os, re, json, difflib, subprocess
from faster_whisper import WhisperModel

HERE = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(HERE, "audio", "Rumours")
OUTDIR = os.path.join(SRCDIR, "vo")
os.makedirs(OUTDIR, exist_ok=True)
FFM = r"C:\Users\Steve\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FFP = FFM.replace("ffmpeg.exe", "ffprobe.exe")
PAD_H, PAD_T = 0.12, 0.30

# master file  ->  (speaker name for who|text keys + clip prefix,  [lines in scene order])
JOBS = [
 ("Voss_Crimson.mp3", "Voss", [
    "So... you're Crimson Nova.",
    "Despite the theatrics...",
    "...your reputation precedes you.",
    "You've protected more civilian convoys than most patrol fleets.",
    "What are your terms?",
    "Welcome aboard... temporarily.",
 ]),
 ("Kael_Crimson.mp3", "Kael", [
    "This is absurd.",
    "We're wasting valuable time.",
    "I prefer competent.",
    "I somehow doubt that's possible.",
    "I object.",
 ]),
 ("Rex_Astra.mp3", "Rex", [
    "I've heard of him!",
    "He destroyed six pirate cruisers by himself at Black Rift!",
    "Right... seven.",
    "Deal.",
 ]),
 ("Astra_Crimson.mp3", "Astra", [
    "No! This is AWESOME!",
    "And escaped before the navy arrived!",
    "You use smoke bombs in space?",
    "Can we hire him right now?",
 ]),
 ("Selyra_Crimson.mp3", "Selyra", [
    "Is this some kind of human ritual?",
    "I wish to witness another entrance.",
 ]),
 ("Tessa_Crimson.mp3", "Tessa", [
    "...Should... someone clap?",
    "...You charge?",
    "...How?",
 ]),
 ("Crimson_voice.mp3", "Crimson", [
    "The one and only!",
    "Protector of the frontier!",
    "Defender of justice!",
    "Champion of hope!",
    "...I usually get applause by now.",
    "Seven.",
    "It was seven cruisers.",
    "Oh!",
    "You're the serious one.",
    "Hahaha!",
    "Good.",
    "I'd hate to disappoint you.",
    "Someone has to.",
    "Anyway!",
    "I'm available for hire.",
    "Fuel isn't free.",
    "Neither are smoke bombs.",
    "Only during the entrance.",
    "Trade secret.",
    "Pay me before departure.",
    "I fight until the battle's won.",
    "No civilian casualties.",
    "No piracy.",
    "And absolutely no interrupting my entrance.",
    "I knew I liked this crew.",
    "Justice never clocks out, Captain.",
    # greeting scene (may or may not be in the recording; unmatched lines are skipped)
    "StarGear! Back for a dose of inspiration?",
    "Still keeping the void honest, I trust. The Nova is watching!",
 ]),
]

def toks(s):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "")).split() if t]

print("loading whisper (base, cpu)...")
model = WhisperModel("base", device="cpu", compute_type="int8")

manifest, scene_vo, any_unmatched = {}, {}, False
for fname, who, lines in JOBS:
    src = os.path.join(SRCDIR, fname)
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
            spans.append(None); continue
        ws = [words[heard_i[j]] for j in idx]
        spans.append([min(w["s"] for w in ws), max(w["e"] for w in ws)])
    print(f"\n{who:8s} {fname}  match={sm.ratio():.3f}  ({len([s for s in spans if s])}/{len(lines)} lines)")
    print(f"   heard: {full[:150]}")
    dur = float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
    out_lines = []
    for i, sp in enumerate(spans):
        num = i + 1
        if sp is None:
            print(f"   {num:2d}. (no audio) {lines[i]}"); continue
        s, e = sp
        lo = 0.0 if i == 0 or spans[i-1] is None else (spans[i-1][1] + s) / 2
        hi = dur if i == len(spans)-1 or spans[i+1] is None else (e + spans[i+1][0]) / 2
        a = max(lo, s - PAD_H, 0.0)
        b = min(hi, e + PAD_T, dur)
        out = os.path.join(OUTDIR, f"{who.lower()}_{num:02d}.mp3")
        subprocess.run([FFM, "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                        "-i", src, "-ac", "1", "-ar", "44100", "-b:a", "192k",
                        "-af", "afade=t=in:st=0:d=0.04,afade=t=out:st=%.3f:d=0.06" % max(b-a-0.06, 0),
                        out], check=True)
        rel = "audio/Rumours/vo/%s_%02d.mp3" % (who.lower(), num)
        out_lines.append({"file": os.path.basename(out), "start": round(a, 2), "end": round(b, 2), "text": lines[i]})
        scene_vo[who + "|" + lines[i]] = rel
        print(f"   {num:2d}. {a:6.2f} -> {b:6.2f}  {lines[i]}")
    if any(s is None for s in spans[:26 if who == "Crimson" else len(lines)]):
        any_unmatched = True
    manifest[who] = out_lines

json.dump(scene_vo, open(os.path.join(SRCDIR, "scene_vo.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("\n%d clips written" % sum(len(v) for v in manifest.values()))
print("\n--- paste into episode1.html (SCENE_VO) ---")
print("const SCENE_VO = {")
for k, v in scene_vo.items():
    print("  %s: %s," % (json.dumps(k, ensure_ascii=False), json.dumps(v)))
print("};")
if any_unmatched:
    print("\n!! some SCENE lines had NO MATCH — check the master against the script")
