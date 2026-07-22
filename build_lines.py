import os, subprocess

DIR = r"c:\Users\Steve\OneDrive\Desktop\Skit"
FFMPEG = r"C:\Users\Steve\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
TMP = os.path.join(DIR, "_clips")
AUDIO = os.path.join(DIR, "audio")
os.makedirs(TMP, exist_ok=True)
os.makedirs(AUDIO, exist_ok=True)
SR = "44100"

# (file, start, end) -- dialogue only, slate labels excluded. Voss from the cleaner Voss_2.
clips = {
    "V01": ("Voss_2",  5.32,  8.04),
    "VFP": ("Voss_2", 10.96, 11.90),
    "V03": ("Voss_2", 14.82, 17.76),
    "V04": ("Voss_2", 20.48, 21.50),
    "V05": ("Voss_2", 24.04, 24.86),
    "V06": ("Voss_2", 27.66, 29.02),
    "T01": ("Tessa", 4.98,  5.95),
    "T02": ("Tessa", 9.24,  9.85),
    "T03": ("Tessa",12.62, 13.62),
    "T04": ("Tessa",15.58, 16.60),
    "T05": ("Tessa",19.94, 20.64),
    "T06": ("Tessa",23.06, 24.58),
    "T07": ("Tessa",27.40, 28.00),
    "T08": ("Tessa",30.45, 32.00),
    "R01": ("Rex",   4.64,  5.90),
    "R02": ("Rex",   7.86, 10.36),
    "RP":  ("Rex",  25.45, 26.45),
}

# One entry per dialogue LINE (index matches LINES[] in index.html)
lines = [
    ["V01"],                 # 0  Voss
    ["T01"],                 # 1  Tessa
    ["R01", "R02"],          # 2  Rex
    ["VFP"],                 # 3  Voss
    ["T02", "T03"],          # 4  Tessa
    ["V03"],                 # 5  Voss
    ["T04", "T05", "T06"],   # 6  Tessa
    ["RP"],                  # 7  Rex
    ["T07", "T08"],          # 8  Tessa
    ["V04"],                 # 9  Voss
    ["V05", "V06"],          # 10 Voss
]
INTRA_GAP = 0.22

def run(args):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error"] + args, check=True)

def extract(cid):
    f, s, e = clips[cid]
    out = os.path.join(TMP, f"{cid}.wav")
    run(["-ss", str(s), "-to", str(e), "-i", os.path.join(DIR, f"{f}.mp3"),
         "-ac", "1", "-ar", SR, out])
    return out

sil = os.path.join(TMP, "sil_intra.wav")
run(["-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", str(INTRA_GAP), sil])
for cid in clips:
    extract(cid)

for i, line in enumerate(lines):
    seq = []
    for ci, cid in enumerate(line):
        seq.append(os.path.join(TMP, f"{cid}.wav"))
        if ci != len(line) - 1:
            seq.append(sil)
    listfile = os.path.join(TMP, f"l{i}.txt")
    with open(listfile, "w", encoding="utf-8") as fh:
        for p in seq:
            fh.write("file '" + p.replace("\\", "/") + "'\n")
    out = os.path.join(AUDIO, f"line_{i:02d}.mp3")
    run(["-f", "concat", "-safe", "0", "-i", listfile, "-ar", SR, "-ac", "1", "-b:a", "192k", out])
    print("wrote", os.path.basename(out))
print("done")
