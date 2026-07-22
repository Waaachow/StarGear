import sys, json
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

for name in ["Voss", "Tessa", "Rex"]:
    path = rf"c:\Users\Steve\OneDrive\Desktop\Skit\{name}.mp3"
    segments, info = model.transcribe(path, language="en", vad_filter=False)
    print(f"===== {name} =====")
    for s in segments:
        print(f"[{s.start:7.2f} -> {s.end:7.2f}] {s.text.strip()}")
    print()
