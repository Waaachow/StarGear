"""Cut the four station-keeper masters into 20 per-line clips.

Reads station_spans.json (from align_station.py) and writes
audio/Station/<id>_NN.mp3 — 01..03 welcomes, 04..05 send-offs, matching the order
of each keeper's entry in the KEEPERS table in iso_grid_prototype.html.

Boundaries from whisper are approximate, and on a fast take (Wick) consecutive lines
come back butted together with no gap at all, which clips word edges. So every
boundary between two lines is REFINED against the waveform: look in a window around
it for the quietest point and split there. Silence is not used to *find* the lines —
that never works on these takes — only to place a boundary the aligner already found.
"""
import os, json, subprocess, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "audio", "Station")
TMP = os.path.join(HERE, "_station_tmp.wav")

LEAD, TAIL = 0.10, 0.18          # padding kept around each line
SEARCH = 0.32                    # how far either side of a boundary to hunt for quiet
HOP = 0.005

spans = json.load(open(os.path.join(HERE, "station_spans.json"), encoding="utf-8"))["keepers"]


def envelope(path):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "16000", TMP],
                   check=True)
    w = wave.open(TMP, "rb")
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    w.close()
    n = max(1, int(HOP * sr))
    frames = len(a) // n
    rms = np.array([np.sqrt(np.mean(a[i * n:(i + 1) * n] ** 2)) for i in range(frames)])
    return rms, len(a) / sr


def quietest(rms, t, dur):
    """Time of the lowest-energy frame within +/-SEARCH of t."""
    lo = max(0, int((t - SEARCH) / HOP))
    hi = min(len(rms), int((t + SEARCH) / HOP))
    if hi <= lo:
        return t
    return (lo + int(np.argmin(rms[lo:hi]))) * HOP


total = 0
for name, k in spans.items():
    src = os.path.join(DIR, f"{name}_Station.mp3")
    sid, lines, sp = k["id"], k["lines"], k["spans"]
    rms, dur = envelope(src)
    print(f"=== {name} -> {sid} ({dur:.2f}s) ===")

    # refine each internal boundary to the quietest point between the two lines
    cuts = []
    for i in range(len(sp)):
        start = sp[i][0] if i == 0 else None
        cuts.append([start, None])
    for i in range(len(sp) - 1):
        mid = (sp[i][1] + sp[i + 1][0]) / 2
        q = quietest(rms, mid, dur)
        # never let the split eat into either line's matched words
        q = min(max(q, sp[i][1] - 0.05), sp[i + 1][0] + 0.05)
        cuts[i][1] = q
        cuts[i + 1][0] = q
    cuts[0][0] = sp[0][0]
    cuts[-1][1] = sp[-1][1]

    for i, (a, b) in enumerate(cuts):
        # pad outward, but stay inside the neighbouring line and the file
        lo = max(0.0, a - LEAD)
        hi = min(dur, b + TAIL)
        if i > 0:
            lo = max(lo, cuts[i - 1][1])
        if i < len(cuts) - 1:
            hi = min(hi, cuts[i + 1][0])
        out = os.path.join(DIR, f"{sid}_{i+1:02d}.mp3")
        length = hi - lo
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{lo:.3f}", "-to", f"{hi:.3f}",
                        "-i", src,
                        "-af", f"afade=t=in:st=0:d=0.02,afade=t=out:st={max(0, length-0.06):.3f}:d=0.06",
                        "-b:a", "128k", out], check=True)
        print(f"  {sid}_{i+1:02d}.mp3  {lo:6.2f} -> {hi:6.2f}  ({length:4.2f}s)  {lines[i]}")
        total += 1
    print()

if os.path.exists(TMP):
    os.remove(TMP)
print(f"wrote {total} clips to {DIR}")
