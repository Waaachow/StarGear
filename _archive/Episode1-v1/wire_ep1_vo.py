# Episode 1 VO pipeline, step 4: wire ep1_vo_manifest.json (from cut_ep1_vo.py)
# into ep1.html — populates VO_MAP for lines whose text is unique to that
# character, and sets `vo:` directly on the specific step for lines whose text
# repeats elsewhere (a "who|text" key can't tell repeats like Kael's four
# "Captain."s apart, so only a repeat that itself matched confidently gets
# wired, and only onto that one step).
import json, re, os

REPO = r"c:\Users\Steve\OneDrive\Desktop\Skit"
HTML = os.path.join(REPO, "ep1.html")

manifest = json.load(open(os.path.join(REPO, "ep1_vo_manifest.json"), encoding="utf-8"))

def js_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

unique_entries = sorted((m for m in manifest if m["unique"]), key=lambda m: (m["char"], m["line_no"]))
inline_entries = [m for m in manifest if not m["unique"]]

lines = open(HTML, encoding="utf-8").read().split("\n")

for m in inline_entries:
    idx = m["line_no"] - 1
    esc_text = js_escape(m["text"])
    needle = f'text:"{esc_text}"'
    if needle not in lines[idx]:
        raise SystemExit(f"Line {m['line_no']} doesn't contain expected text: {lines[idx]!r}")
    lines[idx] = lines[idx].replace(needle, f'{needle}, vo:"{m["path"]}"', 1)
    print(f"inline vo -> {m['char']} L{m['line_no']}: {m['text']!r}")

map_lines = []
cur_char = None
for m in unique_entries:
    if m["char"] != cur_char:
        cur_char = m["char"]
        map_lines.append(f"  // {cur_char}")
    key = js_escape(f'{m["char"]}|{m["text"]}')
    map_lines.append(f'  "{key}": "{m["path"]}",')

vo_map_block = "const VO_MAP = {\n" + "\n".join(map_lines) + "\n};"

joined = "\n".join(lines)
old_decl = "const VO_MAP = {};"
if joined.count(old_decl) != 1:
    raise SystemExit(f"Expected exactly 1 empty VO_MAP declaration, found {joined.count(old_decl)}")
joined = joined.replace(old_decl, vo_map_block, 1)
open(HTML, "w", encoding="utf-8").write(joined)
print(f"Wrote VO_MAP with {len(unique_entries)} entries + {len(inline_entries)} inline vo: fields")
