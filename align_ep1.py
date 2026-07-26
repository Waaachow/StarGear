# Episode 1 VO pipeline, step 2: align a whisper.cpp word-level transcript
# (ep1_vo_work/<Char>_words.json) against that character's reference lines
# (ep1_vo_work/ref_lines.json, from extract_ep1_lines.py) and work out which
# script lines the keeper-master audio actually still contains.
#
# Why this exists: the Episode 1 keeper masters (audio/Episode1/<Name>_ep1.mp3)
# are ONE continuous take per character covering every line they speak in the
# episode, not one clip per line like Episode 0's audio/Episode0/vo/*.mp3. This
# recovers per-line boundaries automatically instead of hand-splitting ~250 cues.
#
# The masters were recorded against an EARLIER draft of ep1.html's script — e.g.
# Kael's file opens with "Convoy route is clear," which doesn't exist in the
# current script at all. So matching is deliberately conservative and order-
# independent (each line searches the whole track on its own merit, not just
# forward from wherever the previous line matched) and a meaningful fraction of
# lines will legitimately have no match. That's expected, not a bug — those
# lines just play without a clip, same as before this pipeline existed.
#
# Producing <Char>_words.json (word-level timestamps): from the repo root,
#   1. Get a whisper.cpp ggml model, e.g.:
#      curl -L -o ep1_vo_work/ggml-base.en.bin \
#        https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
#   2. Get the silero VAD model:
#      curl -L -o ep1_vo_work/ggml-silero-v5.1.2.bin \
#        https://huggingface.co/ggml-org/whisper-vad/resolve/main/ggml-silero-v5.1.2.bin
#   3. Run ffmpeg's whisper filter with max_len=1 (near-word-level segments) —
#      NOTE: ffmpeg on Windows chokes on POSIX-style paths (/c/...) inside the
#      colon-delimited filter string, so cd into ep1_vo_work first and use bare
#      relative filenames for model/destination (only -i can take any path form):
#        cd ep1_vo_work
#        ffmpeg -y -i ../audio/Episode1/<Name>_ep1.mp3 -af \
#          "whisper=model=ggml-base.en.bin:language=en:queue=8:format=json:\
#           destination=<Name>_words.json:vad_model=ggml-silero-v5.1.2.bin:\
#           vad_threshold=0.5:vad_min_silence_duration=0.3:max_len=1" -f null -
#
# `python align_ep1.py <Name>` (or `Narration`) then prints match/skip per line
# and writes ep1_vo_work/<Name>_align.json for cut_ep1_vo.py to consume.

import json, re, sys, os
from collections import Counter

REPO = r"c:\Users\Steve\OneDrive\Desktop\Skit"
WORK = os.path.join(REPO, "ep1_vo_work")
REF = json.load(open(os.path.join(WORK, "ref_lines.json"), encoding="utf-8"))

def norm_word(w):
    w = w.lower()
    return re.sub(r"[^a-z0-9']", "", w)

def load_asr_words(path):
    words = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue  # ffmpeg's destination writer doesn't escape stray literal quote tokens
        raw = d["text"].strip()
        nw = norm_word(raw)
        if not nw:
            continue
        words.append({"w": nw, "raw": raw, "start": d["start"], "end": d["end"]})
    return words

def tokenize_line(text):
    return [norm_word(w) for w in re.findall(r"[A-Za-z0-9']+", text) if norm_word(w)]

def lcs_align(ref_words, asr_words):
    """Longest-common-subsequence alignment (order-preserving) between the two
    word lists. Returns [(ref_idx, asr_idx), ...]. Sizes here are tiny (a line
    vs. a local window), so the classic O(n*m) DP is plenty fast."""
    n, m = len(ref_words), len(asr_words)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            if ref_words[i] == asr_words[j]:
                dp[i][j] = dp[i+1][j+1] + 1
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j+1])
    pairs = []
    i = j = 0
    while i < n and j < m:
        if ref_words[i] == asr_words[j]:
            pairs.append((i, j)); i += 1; j += 1
        elif dp[i+1][j] >= dp[i][j+1]:
            i += 1
        else:
            j += 1
    return pairs

def best_window_match(ref_toks, asr_words):
    """Slide a window sized to the ref line across the WHOLE asr word stream
    (order-independent — see module docstring for why) and keep the highest-
    scoring window, scoring on both LCS coverage and how tightly packed the
    matched words are (a scattered 1-in-20 match scores worse than a dense
    3-in-4 one even at the same ratio)."""
    n = len(ref_toks)
    win = n + max(3, n)
    N = len(asr_words)
    best = None
    for start in range(N):
        hi = min(N, start + win)
        if hi - start < 1:
            break
        asr_window = [asr_words[k]["w"] for k in range(start, hi)]
        pairs = lcs_align(ref_toks, asr_window)
        if not pairs:
            continue
        n_matched = len(pairs)
        ratio = n_matched / n
        span = pairs[-1][1] - pairs[0][1] + 1
        density = n_matched / span if span else 0
        score = ratio * 0.7 + density * 0.3
        if best is None or score > best[0]:
            best = (score, ratio, start + pairs[0][1], start + pairs[-1][1], n_matched)
        if hi >= N:
            break
    if best is None:
        return None
    _, ratio, first_idx, last_idx, n_matched = best
    return ratio, first_idx, last_idx, n_matched

def align_character(ref_lines, asr_words, min_ratio=0.6):
    """ref_lines: [(line_no, text), ...] in script order. Matches each line
    independently against the whole track (see module docstring), then
    resolves any overlap where two lines claimed the same audio (higher-ratio
    match wins, the loser reverts to unmatched)."""
    word_counts = Counter(w["w"] for w in asr_words)
    results = []
    for line_no, text in ref_lines:
        ref_toks = tokenize_line(text)
        if not ref_toks:
            results.append(dict(line_no=line_no, text=text, matched=False, reason="no-words"))
            continue
        # a lone word ("No.", "So...") is too ambiguous to auto-splice unless
        # it's literally the only occurrence of that word in the whole track
        if len(ref_toks) == 1 and word_counts.get(ref_toks[0], 0) != 1:
            results.append(dict(line_no=line_no, text=text, matched=False, reason="ambiguous-1word"))
            continue
        m = best_window_match(ref_toks, asr_words)
        if m is None:
            results.append(dict(line_no=line_no, text=text, matched=False, reason="no-candidates"))
            continue
        ratio, first_idx, last_idx, n_matched = m
        ratio_needed = 1.0 if len(ref_toks) <= 2 else min_ratio
        if ratio < ratio_needed:
            results.append(dict(line_no=line_no, text=text, matched=False, reason="low-coverage",
                                 ratio=ratio))
            continue
        results.append(dict(line_no=line_no, text=text, matched=True, ratio=ratio,
                             start=asr_words[first_idx]["start"]/1000.0,
                             end=asr_words[last_idx]["end"]/1000.0,
                             asr_first=first_idx, asr_last=last_idx))

    matched = sorted((r for r in results if r["matched"]), key=lambda r: -r["ratio"])
    claimed = []
    for r in matched:
        f, l = r["asr_first"], r["asr_last"]
        if any(not (l < cf or f > cl) for cf, cl in claimed):
            r["matched"] = False
            r["reason"] = "overlap-collision"
        else:
            claimed.append((f, l))
    return results

if __name__ == "__main__":
    which = sys.argv[1]
    asr_words = load_asr_words(os.path.join(WORK, f"{which}_words.json"))
    ref_lines = REF["narr"] if which == "Narration" else REF["chars"][which]
    res = align_character(ref_lines, asr_words)
    matched = [r for r in res if r["matched"]]
    print(f"{which}: {len(matched)}/{len(res)} matched, asr_words={len(asr_words)}")
    for r in res:
        if r["matched"]:
            print(f"  L{r['line_no']:5d} [{r['start']:6.2f}-{r['end']:6.2f}] ratio={r['ratio']:.2f} :: {r['text'][:60]}")
        else:
            print(f"  L{r['line_no']:5d} SKIP({r['reason']}) :: {r['text'][:60]}")
    json.dump(res, open(os.path.join(WORK, f"{which}_align.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
