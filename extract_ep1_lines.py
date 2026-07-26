# Episode 1 VO pipeline, step 1: pull every character line + narration line out of
# ep1.html's EP1 script (exact text, in file order) so the alignment step has a
# reference to match whisper transcripts against. Writes ep1_vo_work/ref_lines.json.
import re, json, os

REPO = r"c:\Users\Steve\OneDrive\Desktop\Skit"
WORK = os.path.join(REPO, "ep1_vo_work")
os.makedirs(WORK, exist_ok=True)

SRC = os.path.join(REPO, "ep1.html")
text = open(SRC, encoding="utf-8").read()

def unescape(s):
    return s.replace('\\"', '"').replace("\\\\", "\\")

# VO'd cast only — Elias/Quinn/Rowan/Raze/etc have no keeper-master audio yet.
CHARS = ["Voss", "Rex", "Astra", "Kael", "Selyra", "Tessa"]

char_lines = {c: [] for c in CHARS}
narr_lines = []

who_text_re = re.compile(r'who:"((?:[^"\\]|\\.)*)"[^\n]*?text:"((?:[^"\\]|\\.)*)"')
narr_re = re.compile(r'narr:"((?:[^"\\]|\\.)*)"')

for i, line in enumerate(text.split("\n"), 1):
    m = who_text_re.search(line)
    if m:
        who = unescape(m.group(1))
        txt = unescape(m.group(2))
        if who in char_lines:
            char_lines[who].append((i, txt))
        continue
    m2 = narr_re.search(line)
    if m2:
        narr_lines.append((i, unescape(m2.group(1))))

json.dump({"chars": char_lines, "narr": narr_lines},
          open(os.path.join(WORK, "ref_lines.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

for c in CHARS:
    print(c, len(char_lines[c]))
print("narr", len(narr_lines))
