"""Transcribe the bounty-boss VO masters with word timestamps.

Same route as transcribe_station.py / transcribe_explore.py: whisper the whole take
keeping every word's start/end, and let align_boss.py match that sequence against the
known line text. Silence splitting is never used — see align_boss.py.
"""
import os, json
from faster_whisper import WhisperModel

DIR = r"c:\Users\Steve\OneDrive\Desktop\Skit\audio\bounties"
MASTERS = {"drax": "red_reaver.mp3",          # clip prefix -> master file
           "sable": "afterimage.mp3",
           "dross": "tollman.mp3"}

model = WhisperModel("base", device="cpu", compute_type="int8")

out = {}
for key, fname in MASTERS.items():
    path = os.path.join(DIR, fname)
    if not os.path.exists(path):
        print(f"!! missing {path}")
        continue
    segments, info = model.transcribe(path, language="en", vad_filter=False,
                                      word_timestamps=True)
    print(f"===== {key}  ({fname}, {info.duration:.2f}s) =====")
    segs = []
    for s in segments:
        print(f"[{s.start:7.2f} -> {s.end:7.2f}] {s.text.strip()}")
        segs.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                     "words": [{"w": w.word, "s": w.start, "e": w.end}
                               for w in (s.words or [])]})
    out[key] = {"file": fname, "duration": info.duration, "segments": segs}
    print()

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "boss_vo.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("wrote boss_vo.json")
