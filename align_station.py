# Align the whisper word timings against the known KEEPERS line text, so each line
# gets an exact [start, end]. Same method as align_explore.py: whisper mis-hears words
# ("hole's got some new dense" for "hull's got some new dents"), so we align token
# SEQUENCES with difflib rather than matching words one-for-one, and we never try to
# split on silence — the takes run lines together.
import os, json, re, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
vo = json.load(open(os.path.join(HERE, "station_vo.json"), encoding="utf-8"))

# Recording order == order in KEEPERS: the three welcomes, then the two send-offs.
# Keyed by master-file name; `id` is the station id the cut clips are named for.
KEEPERS = {
 "Marla": ("hub", [
    "Waypoint Hub, and welcome to it. Clamps are on, take your time.",
    "Back again. Hold's a mess, I imagine — the counter's open.",
    "Good to see the StarGear in one piece. Mostly.",
    "Safe lanes, Captain. Come back with something interesting.",
    "Clamps released. Don't be a stranger."]),
 "Oris": ("neb", [
    "The nebula let you through, then. It doesn't always.",
    "Ah — a buyer. Or a seller. You've the look of both.",
    "Careful what you brought in with you. Things follow, out here.",
    "Go carefully. The Veil remembers a face.",
    "Take what you've learned. Leave what you haven't."]),
 "Dova": ("moon", [
    "Quarry Station. Ore's priced on the board and I don't haggle.",
    "You're on the pad. Mind the dust, it gets everywhere.",
    "Buying or selling? Either way, be quick about it.",
    "Clear of the clamps. Don't scratch my dock on the way out.",
    "Right. Go on, then."]),
 "Wick": ("armada", [
    "Salvage Reach! You brought me something, didn't you? You did.",
    "Ohh, that hull's got some new dents. Want me to take them off your hands?",
    "Come in, come in — mind the cable, that one's live.",
    "Bring me back something with SERIAL NUMBERS on it!",
    "Fly safe! Well — fly. Safe's optional."]),
}


def toks(s):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "")).split() if t]


result, problems = {}, []
for name, (sid, lines) in KEEPERS.items():
    if name not in vo:
        problems.append(f"{name}: no transcript"); continue
    words = [w for seg in vo[name]["segments"] for w in seg["words"]]
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
            spans.append(None); problems.append(f"{name} line {li+1}: NO MATCH"); continue
        ws = [words[heard_i[j]] for j in idx]
        spans.append([min(w["s"] for w in ws), max(w["e"] for w in ws)])

    # sanity: spans must be in order and not overlap, or a boundary landed wrong
    for li in range(1, len(spans)):
        if spans[li] and spans[li - 1] and spans[li][0] < spans[li - 1][1] - 0.05:
            problems.append(f"{name}: line {li+1} starts before line {li} ends")

    result[name] = {"id": sid, "spans": spans}
    print(f"{name:6s} -> {sid:6s} match={sm.ratio():.3f}  ({vo[name]['duration']:.1f}s)")
    for li, sp in enumerate(spans):
        if sp is None:
            print(f"   {li+1}. !! NO MATCH  {lines[li]}")
        else:
            gap = "" if li == 0 or not spans[li - 1] else f" gap {sp[0]-spans[li-1][1]:+.2f}s"
            print(f"   {li+1}. {sp[0]:6.2f} -> {sp[1]:6.2f} ({sp[1]-sp[0]:4.2f}s){gap}  {lines[li]}")
    print()

json.dump({"keepers": {k: {"id": v["id"], "lines": KEEPERS[k][1], "spans": v["spans"]}
                       for k, v in result.items()}},
          open(os.path.join(HERE, "station_spans.json"), "w", encoding="utf-8"), indent=1)
print("wrote station_spans.json")
if problems:
    print("\nPROBLEMS:")
    for p in problems:
        print("  -", p)
else:
    print("\nno problems: every line matched, in order, no overlaps")
