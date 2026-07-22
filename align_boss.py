# Align whisper word timings against the known boss `lines` text so each line gets an
# exact [start, end]. Same difflib sequence-matching as align_station.py.
#
# ⚠ ONE EXTRA CASE the other alignments never hit: a NON-LEXICAL line. Drax's "Heh..." is
# a laugh — whisper transcribes no words for it at all, so it can never be matched by
# text. Any line that matches nothing falls back to an ENERGY search: look in the gap
# between its neighbours' spans and take the loudest contiguous run of sound. That's the
# only place silence detection is used, and only to place a line we already know is there.
import os, json, re, difflib, subprocess, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "audio", "bounties")
TMP = os.path.join(HERE, "_boss_tmp.wav")
vo = json.load(open(os.path.join(HERE, "boss_vo.json"), encoding="utf-8"))

# Recording order == order across the spec's `lines` beats: start, hp50, hp25, defeat.
BOSSES = {
 "drax": ["Another bounty hunter.",
          "Tell me... do they even know why they want me dead?",
          "Good.",
          "It's been years since someone made me earn a victory.",
          "This ship...",
          "...she still remembers war.",
          "Heh...",
          "Perhaps...",
          "...it's finally time to let the dead rest."],
 "sable": ["You've got a good lock. That's rare.",
           "Hold onto it. It won't last.",
           "There. You're learning.",
           "Most people only ever shoot where I was.",
           "...I can't feel the third jump any more.",
           "That's how it takes you. A piece at a time.",
           "Oh.",
           "It's quiet.",
           "...I'd forgotten quiet."],
 "dross": ["Southern drift is a toll road. You'll have been told.",
           "No? Then we'll do this the other way.",
           "You're through the first plate. That's further than most.",
           "I'll add the repairs to your account.",
           "...you're actually going to do it.",
           "Twenty years I held this lane.",
           "Ledger's closed, then.",
           "Tell them...",
           "...tell them I was owed."],
}
HOP = 0.010


def toks(s):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "")).split() if t]


def envelope(path):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "16000", TMP],
                   check=True)
    w = wave.open(TMP, "rb")
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    w.close()
    n = max(1, int(HOP * sr))
    frames = len(a) // n
    return np.array([np.sqrt(np.mean(a[i * n:(i + 1) * n] ** 2)) for i in range(frames)])


def loudest_run(rms, lo, hi):
    """Longest contiguous above-threshold run inside [lo,hi] seconds → (start,end) or None."""
    i0, i1 = max(0, int(lo / HOP)), min(len(rms), int(hi / HOP))
    if i1 - i0 < 3:
        return None
    win = rms[i0:i1]
    thr = max(float(win.max()) * 0.25, float(np.percentile(rms, 15)) * 4)
    best = cur = None
    for i, v in enumerate(win):
        if v > thr:
            cur = i if cur is None else cur
        elif cur is not None:
            if best is None or i - cur > best[1] - best[0]:
                best = (cur, i)
            cur = None
    if cur is not None and (best is None or len(win) - cur > best[1] - best[0]):
        best = (cur, len(win))
    if not best:
        return None
    return ((i0 + best[0]) * HOP, (i0 + best[1]) * HOP)


result, problems = {}, []
for key, lines in BOSSES.items():
    if key not in vo:
        problems.append(f"{key}: no transcript"); continue
    words = [w for seg in vo[key]["segments"] for w in seg["words"]]
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

    # energy fallback for lines no words could be matched to (laughs, sighs)
    rms = None
    dur = vo[key]["duration"]
    for li, sp in enumerate(spans):
        if sp is not None:
            continue
        if rms is None:
            rms = envelope(os.path.join(DIR, vo[key]["file"]))
        prev_end = next((spans[j][1] for j in range(li - 1, -1, -1) if spans[j]), 0.0)
        next_start = next((spans[j][0] for j in range(li + 1, len(spans)) if spans[j]), dur)
        run = loudest_run(rms, prev_end, next_start)
        if run:
            spans[li] = [run[0], run[1]]
            print(f"  ({key} line {li+1} '{lines[li]}' has no words — "
                  f"placed by sound in the {prev_end:.2f}-{next_start:.2f}s gap)")
        else:
            problems.append(f"{key} line {li+1}: NO MATCH and no sound in the gap")

    for li in range(1, len(spans)):
        if spans[li] and spans[li - 1] and spans[li][0] < spans[li - 1][1] - 0.05:
            problems.append(f"{key}: line {li+1} starts before line {li} ends")

    result[key] = {"file": vo[key]["file"], "spans": spans}
    print(f"\n{key}  match={sm.ratio():.3f}  ({dur:.1f}s)")
    for li, sp in enumerate(spans):
        if sp is None:
            print(f"   {li+1}. !! NO SPAN  {lines[li]}")
        else:
            gap = "" if li == 0 or not spans[li - 1] else f" gap {sp[0]-spans[li-1][1]:+.2f}s"
            print(f"   {li+1}. {sp[0]:6.2f} -> {sp[1]:6.2f} ({sp[1]-sp[0]:4.2f}s){gap}  {lines[li]}")

if os.path.exists(TMP):
    os.remove(TMP)
json.dump({"bosses": {k: {"file": v["file"], "lines": BOSSES[k], "spans": v["spans"]}
                      for k, v in result.items()}},
          open(os.path.join(HERE, "boss_spans.json"), "w", encoding="utf-8"), indent=1)
print("\nwrote boss_spans.json")
print("PROBLEMS: " + ("; ".join(problems) if problems else "none"))
