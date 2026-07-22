import os, json, subprocess

HERE  = os.path.dirname(os.path.abspath(__file__))
SRC   = r"c:\Users\Steve\OneDrive\Desktop\Skit\audio\Explore"
FFM   = r"C:\Users\Steve\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
PAD_H, PAD_T = 0.12, 0.30      # breathing room head/tail
data  = json.load(open(os.path.join(HERE, "explore_spans.json"), encoding="utf-8"))

manifest = {}
for name, spans in data["spans"].items():
    src = os.path.join(SRC, f"{name}_Explore.mp3")
    dur = float(subprocess.run([FFM.replace("ffmpeg.exe", "ffprobe.exe"), "-v", "error",
                 "-show_entries", "format=duration", "-of", "csv=p=0", src],
                capture_output=True, text=True).stdout.strip())
    out_lines = []
    for i, (s, e) in enumerate(spans):
        # clamp the pad so it never crosses into the neighbouring line
        lo = 0.0 if i == 0 else (spans[i - 1][1] + s) / 2
        hi = dur if i == len(spans) - 1 else (e + spans[i + 1][0]) / 2
        a  = max(lo, s - PAD_H, 0.0)
        b  = min(hi, e + PAD_T, dur)
        out = os.path.join(SRC, f"{name.lower()}_{i+1:02d}.mp3")
        subprocess.run([FFM, "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                        "-i", src, "-ac", "1", "-ar", "44100", "-b:a", "192k",
                        "-af", "afade=t=in:st=0:d=0.04,afade=t=out:st=%.3f:d=0.06" % max(b - a - 0.06, 0),
                        out], check=True)
        out_lines.append({"file": os.path.basename(out), "start": round(a, 2), "end": round(b, 2),
                          "text": data["lines"][name][i]})
        print(f"{os.path.basename(out):16s} {a:6.2f} -> {b:6.2f}  {data['lines'][name][i]}")
    manifest[name] = out_lines

json.dump(manifest, open(os.path.join(HERE, "explore_manifest.json"), "w", encoding="utf-8"), indent=1)
print("\n%d clips written" % sum(len(v) for v in manifest.values()))
