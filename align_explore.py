# Align the whisper word timings against the known CHATTER line text, so each
# line gets an exact [start, end]. Whisper mis-hears a few words ("Holes holding"
# for "Hull's holding"), so we align token SEQUENCES with difflib rather than
# matching words one-for-one.
import os, json, re, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
vo = json.load(open(os.path.join(HERE, "explore_vo.json"), encoding="utf-8"))

# expected lines, in recording order == order in CHATTER (idle lines first, then events)
LINES = {
 "Tessa": ["Drive's running clean. Enjoy it while it lasts.",
           "If anyone's bored, the coolant lines need bleeding.",
           "That moon didn't crack on its own. Something did that.",
           "Hull's holding. Mostly.",
           "That's a module gone. I can't fix it out here — we need a station.",
           "Hold's full, Captain. We're leaving salvage behind.",
           "Docking clamps in range. I've got a repair list as long as my arm.",
           "Salvage on the sweep. Reel it in."],
 "Kael":  ["Long-range is quiet. Suspiciously quiet.",
           "I've been reading the fleet manifests again. They don't add up.",
           "Particle density is climbing. Sensors are going to get vague in here.",
           "The signal's strongest here. It's practically shouting.",
           "Hostile transponder. They've seen us.",
           "We're flying with a hole in the grid. Mind how you fight.",
           "Sensors have something. Logging it."],
 "Astra": ["Course holding. Nothing on the approach vectors.",
           "We're a long way from anywhere out here.",
           "The nebula plays havoc with the drive. Taking it slow.",
           "Whatever's at the centre of this, we're close.",
           "I can burn past them if you'd rather not fight.",
           "No more room. Nearest station's the smart move."],
 "Rex":   ["You know what I miss? Weather. Space has no weather.",
           "Guns are warm. Just saying.",
           "Mind the debris field. I'd rather not repaint the hull.",
           "Contact! Red profile, closing.",
           "Scratch one. Who's next?"],
 "Selyra":["Everyone's patched up. For once.",
           "Try to eat something before the next fight, Captain.",
           "So many of them. And not one light on.",
           "No casualties. Let's keep it that way.",
           "Station ahead. Hot food and a working shower."],
 "Voss":  ["Steady as she goes.",
           "Keep your eyes open. Quiet isn't the same as safe.",
           "Hold formation discipline. We're guests in a graveyard."],
}

def toks(s):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("'", "")).split() if t]

result = {}
for name, lines in LINES.items():
    words = [w for seg in vo[name] for w in seg["words"]]
    heard = [re.sub(r"[^a-z0-9]", "", w["w"].lower().replace("'", "")) for w in words]
    heard_i = [i for i, t in enumerate(heard) if t]          # drop empties
    heard_t = [heard[i] for i in heard_i]

    want, owner = [], []
    for li, ln in enumerate(lines):
        for t in toks(ln):
            want.append(t); owner.append(li)

    # map want-index -> heard-index for the matching blocks
    sm = difflib.SequenceMatcher(a=want, b=heard_t, autojunk=False)
    hit = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            hit[a + k] = b + k

    spans, unmatched = [], []
    for li in range(len(lines)):
        idx = [hit[i] for i in range(len(want)) if owner[i] == li and i in hit]
        if not idx:
            unmatched.append(li); spans.append(None); continue
        ws = [words[heard_i[j]] for j in idx]
        spans.append([min(w["s"] for w in ws), max(w["e"] for w in ws)])
    result[name] = {"spans": spans, "unmatched": unmatched,
                    "ratio": round(sm.ratio(), 3)}
    print(f"{name:7s} match={sm.ratio():.3f}")
    for li, sp in enumerate(spans):
        if sp is None:
            print(f"   {li+1}. !! NO MATCH  {lines[li]}")
        else:
            print(f"   {li+1}. {sp[0]:6.2f} -> {sp[1]:6.2f}  {lines[li]}")
    print()

json.dump({"lines": LINES, "spans": {k: v["spans"] for k, v in result.items()}},
          open(os.path.join(HERE, "explore_spans.json"), "w", encoding="utf-8"), indent=1)
print("wrote explore_spans.json")
