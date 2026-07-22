import os, json
from faster_whisper import WhisperModel

DIR = r"c:\Users\Steve\OneDrive\Desktop\Skit\audio\Explore"
model = WhisperModel("base", device="cpu", compute_type="int8")

out = {}
for name in ["Tessa", "Kael", "Astra", "Rex", "Selyra", "Voss"]:
    path = os.path.join(DIR, f"{name}_Explore.mp3")
    segments, info = model.transcribe(path, language="en", vad_filter=False, word_timestamps=True)
    print(f"===== {name} =====")
    segs = []
    for s in segments:
        print(f"[{s.start:7.2f} -> {s.end:7.2f}] {s.text.strip()}")
        segs.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                     "words": [{"w": w.word, "s": w.start, "e": w.end} for w in (s.words or [])]})
    out[name] = segs
    print()

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "explore_vo.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("wrote explore_vo.json")
