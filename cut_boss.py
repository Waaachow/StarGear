"""Cut the bounty-boss masters into per-line clips.

Reads boss_spans.json (from align_boss.py) and writes audio/bounties/<key>_NN.mp3,
numbered in the order the lines appear across the spec's `lines` beats
(start, then hp50, then hp25, then defeat).

As in cut_station.py, whisper's boundaries are approximate and consecutive lines can
come back butted together, so every internal boundary is refined against the waveform:
look around it for the quietest point and split there.
"""
import os, json, subprocess, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "audio", "bounties")
TMP = os.path.join(HERE, "_boss_cut_tmp.wav")

LEAD, TAIL = 0.10, 0.18
SEARCH = 0.30          # fallback: quietest single frame within this of the boundary
SNAP = 0.95            # preferred: a real silence RUN within this of the boundary
MIN_GAP = 0.10         # a run must be this long to count as a pause between lines
HOP = 0.005

spans = json.load(open(os.path.join(HERE, "boss_spans.json"), encoding="utf-8"))["bosses"]


TARGET_PEAK = 0.85      # masters arrive at wildly different levels; even them out
MAX_GAIN = 6.0


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
    # Peak-normalise per master. Sable's take came in at ~0.15 peak against Drax's 0.87,
    # which would have made her a quarter the volume of the other two in game.
    peak = float(np.abs(a).max()) or 1.0
    gain = min(MAX_GAIN, max(1.0, TARGET_PEAK / peak))
    return rms, len(a) / sr, gain


def quietest(rms, t):
    lo = max(0, int((t - SEARCH) / HOP))
    hi = min(len(rms), int((t + SEARCH) / HOP))
    if hi <= lo:
        return t
    return (lo + int(np.argmin(rms[lo:hi]))) * HOP


def silence_runs(rms):
    """Contiguous low-energy stretches long enough to be a pause between lines."""
    thr = max(float(np.percentile(rms, 20)) * 2.5, float(rms.max()) * 0.03)
    runs, cur = [], None
    for i, v in enumerate(rms):
        if v < thr:
            cur = i if cur is None else cur
        elif cur is not None:
            if (i - cur) * HOP >= MIN_GAP:
                runs.append((cur * HOP, i * HOP))
            cur = None
    if cur is not None and (len(rms) - cur) * HOP >= MIN_GAP:
        runs.append((cur * HOP, len(rms) * HOP))
    return runs


def boundary(rms, runs, t):
    """Split point for a boundary the aligner put near `t`.

    Prefer the centre of the nearest real pause: whisper's word timings can drift by
    several hundred ms inside a long segment, which put one of Drax's boundaries in the
    middle of the word "Perhaps". A silence run is ground truth; the quietest single
    frame is not, because inside continuous speech there is always *some* minimum.
    """
    best = None
    for (a, b) in runs:
        c = (a + b) / 2
        if abs(c - t) <= SNAP and (best is None or abs(c - t) < abs(best - t)):
            best = c
    return best if best is not None else quietest(rms, t)


total = 0
for key, k in spans.items():
    src = os.path.join(DIR, k["file"])
    lines, sp = k["lines"], k["spans"]
    # A master that didn't align (wrong recording, missing lines) leaves null spans.
    # Skip it loudly rather than crashing or, worse, cutting nine wrong clips.
    missing = [i + 1 for i, s in enumerate(sp) if not s]
    if missing:
        print(f"!! {key}: skipped — no span for line(s) {missing}. "
              f"Check {k['file']} is the right recording, then re-run transcribe+align.\n")
        continue
    rms, dur, gain = envelope(src)
    print(f"=== {key} ({k['file']}, {dur:.2f}s, gain x{gain:.2f}) ===")

    runs = silence_runs(rms)
    cuts = [[sp[i][0] if i == 0 else None, None] for i in range(len(sp))]
    for i in range(len(sp) - 1):
        # NOT clamped to the aligner's spans: when the word timings have drifted, the
        # span itself is wrong, so clamping to it would preserve the error.
        q = boundary(rms, runs, (sp[i][1] + sp[i + 1][0]) / 2)
        cuts[i][1] = q
        cuts[i + 1][0] = q
    cuts[0][0] = sp[0][0]
    cuts[-1][1] = max(sp[-1][1], cuts[-1][0] + 0.2)
    # boundaries must stay in order after snapping
    for i in range(1, len(cuts)):
        if cuts[i][0] < cuts[i - 1][0]:
            raise SystemExit(f"{key}: boundaries out of order at line {i+1} — check boss_spans.json")

    for i, (a, b) in enumerate(cuts):
        lo = max(0.0, a - LEAD)
        hi = min(dur, b + TAIL)
        if i > 0:
            lo = max(lo, cuts[i - 1][1])
        if i < len(cuts) - 1:
            hi = min(hi, cuts[i + 1][0])
        out = os.path.join(DIR, f"{key}_{i+1:02d}.mp3")
        length = hi - lo
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{lo:.3f}", "-to", f"{hi:.3f}",
                        "-i", src,
                        "-af", f"volume={gain:.3f},afade=t=in:st=0:d=0.02,"
                               f"afade=t=out:st={max(0, length-0.06):.3f}:d=0.06",
                        "-b:a", "128k", out], check=True)
        print(f"  {key}_{i+1:02d}.mp3  {lo:6.2f} -> {hi:6.2f} ({length:4.2f}s)  {lines[i]}")
        total += 1
    print()

if os.path.exists(TMP):
    os.remove(TMP)
print(f"wrote {total} clips to {DIR}")
