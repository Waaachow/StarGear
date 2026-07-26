# Episode 1 VO pipeline, step 3: cut a clip for every confidently-matched line
# from align_ep1.py, into audio/Episode1/vo/<char>_L<line_no>.mp3 (line-number
# naming, not sequential — most lines have no match, so gaps are expected and
# the number doubles as a pointer back to the exact ep1.html line for review).
# Writes ep1_vo_manifest.json at the repo root (final record of what got cut).
import json, os, subprocess, sys

sys.path.insert(0, r"c:\Users\Steve\OneDrive\Desktop\Skit")
from align_ep1 import load_asr_words, align_character, REF

REPO = r"c:\Users\Steve\OneDrive\Desktop\Skit"
WORK = os.path.join(REPO, "ep1_vo_work")
OUTDIR = os.path.join(REPO, "audio", "Episode1", "vo")
os.makedirs(OUTDIR, exist_ok=True)

CHARS = ["Voss", "Rex", "Astra", "Kael", "Selyra", "Tessa"]
PAD_START, PAD_END = 0.12, 0.20
MAX_WORDS_PER_SEC = 5.5  # a matched span faster than natural speech is a bad/truncated match

def get_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                           "-of", "default=noprint_wrappers=1:nokey=1", path],
                          capture_output=True, text=True).stdout.strip()
    return float(out)

manifest = []

for c in CHARS:
    asr_words = load_asr_words(os.path.join(WORK, f"{c}_words.json"))
    ref_lines = REF["chars"][c]
    results = align_character(ref_lines, asr_words)
    matched = [r for r in results if r["matched"]]
    matched.sort(key=lambda r: r["start"])

    text_count = {}
    for _, t in ref_lines:
        text_count[t] = text_count.get(t, 0) + 1

    master = os.path.join(REPO, "audio", "Episode1", f"{c}_ep1.mp3")
    dur = get_duration(master)

    cuts = []
    for i, r in enumerate(matched):
        s, e = r["start"] - PAD_START, r["end"] + PAD_END
        s = max(s, 0.0) if i == 0 else max(s, (matched[i-1]["end"] + r["start"]) / 2, matched[i-1]["end"])
        e = min(e, dur) if i == len(matched)-1 else min(e, (r["end"] + matched[i+1]["start"]) / 2, matched[i+1]["start"])
        cuts.append((s, e))

    for r, (s, e) in zip(matched, cuts):
        import re
        nwords = len(re.findall(r"[A-Za-z0-9']+", r["text"]))
        if e - s > 0 and nwords / (e - s) > MAX_WORDS_PER_SEC:
            print(f"  SKIP {c} L{r['line_no']} — {nwords/(e-s):.1f} words/sec, likely a truncated match")
            continue
        line_no = r["line_no"]
        fname = f"{c.lower()}_L{line_no}.mp3"
        outpath = os.path.join(OUTDIR, fname)
        rel_path = f"audio/Episode1/vo/{fname}"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", master,
                         "-ss", f"{s:.3f}", "-to", f"{e:.3f}",
                         "-c:a", "libmp3lame", "-q:a", "3", outpath], check=True)
        manifest.append(dict(char=c, line_no=line_no, text=r["text"],
                              unique=text_count[r["text"]] == 1,
                              path=rel_path, start=s, end=e, ratio=r["ratio"]))
    print(f"{c}: cut {sum(1 for m in manifest if m['char']==c)} clips")

json.dump(manifest, open(os.path.join(REPO, "ep1_vo_manifest.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("Total clips:", len(manifest))
print("Non-unique text (need inline vo:, not VO_MAP):", sum(1 for m in manifest if not m["unique"]))
