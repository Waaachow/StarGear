"""Transcribe the four station-keeper masters with word timestamps.

Same route as transcribe_explore.py: whisper the whole take, keep every word's
start/end, and let align_station.py match that word sequence against the known
line text. Silence detection is deliberately NOT used — see align_station.py.
"""
import os, json
from faster_whisper import WhisperModel

DIR = r"c:\Users\Steve\OneDrive\Desktop\Skit\audio\Station"
KEEPERS = ["Marla", "Oris", "Dova", "Wick"]

model = WhisperModel("base", device="cpu", compute_type="int8")

out = {}
for name in KEEPERS:
    path = os.path.join(DIR, f"{name}_Station.mp3")
    if not os.path.exists(path):
        print(f"!! missing {path}")
        continue
    segments, info = model.transcribe(path, language="en", vad_filter=False,
                                      word_timestamps=True)
    print(f"===== {name}  ({info.duration:.2f}s) =====")
    segs = []
    for s in segments:
        print(f"[{s.start:7.2f} -> {s.end:7.2f}] {s.text.strip()}")
        segs.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                     "words": [{"w": w.word, "s": w.start, "e": w.end}
                               for w in (s.words or [])]})
    out[name] = {"duration": info.duration, "segments": segs}
    print()

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "station_vo.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("wrote station_vo.json")
