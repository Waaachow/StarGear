import os, subprocess

DIR = r"c:\Users\Steve\OneDrive\Desktop\Skit"
FFMPEG = r"C:\Users\Steve\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
TMP = os.path.join(DIR, "_clips")
os.makedirs(TMP, exist_ok=True)

SR = "44100"

# (file, start, end) for each dialogue clip, slate labels excluded
clips = {
    "V01": ("Voss_2",  5.32,  8.04),  # Tell me we've got something interesting on the schedule.
    "VFP": ("Voss_2", 10.96, 11.90),  # Fair point.
    "V03": ("Voss_2", 14.82, 17.76),  # Those are the exact words I never want to hear.
    "V04": ("Voss_2", 20.48, 21.50),  # Put it on screen.
    "V05": ("Voss_2", 24.04, 24.86),  # Set a course.
    "V06": ("Voss_2", 27.66, 29.02),  # Let's see who's calling.
    "T01": ("Tessa", 4.98,  5.95),   # Define interesting.
    "T02": ("Tessa", 9.24,  9.85),   # Actually...
    "T03": ("Tessa",12.62, 13.62),   # That's weird.
    "T04": ("Tessa",15.58, 16.60),   # I'm getting a transmission.
    "T05": ("Tessa",19.94, 20.64),   # Long range.
    "T06": ("Tessa",23.06, 24.58),   # Doesn't match any known beacon.
    "T07": ("Tessa",27.40, 28.00),   # No.
    "T08": ("Tessa",30.45, 32.00),   # Which somehow makes it worse.
    "R01": ("Rex",   4.64,  5.90),   # Please don't.
    "R02": ("Rex",   7.86, 10.36),   # Last time interesting tried to shoot us.
    "RP":  ("Rex",  25.45, 26.45),   # Pirates?
}

# Lines in script dialogue order. Each line = list of clip ids spoken back-to-back.
lines = [
    ["V01"],          # VOSS:  Tell me we've got something interesting on the schedule.
    ["T01"],          # TESSA: Define interesting.
    ["R01", "R02"],   # REX:   Please don't. Last time "interesting" tried to shoot us.
    ["VFP"],          # VOSS:  Fair point.
    ["T02", "T03"],   # TESSA: Actually... That's weird.
    ["V03"],          # VOSS:  Those are the exact words I never want to hear.
    ["T04", "T05", "T06"],  # TESSA: I'm getting a transmission. Long range. Doesn't match any known beacon.
    ["RP"],           # REX:   Pirates?
    ["T07", "T08"],   # TESSA: No. Which somehow makes it worse.
    ["V04"],          # VOSS:  Put it on screen.
    ["V05", "V06"],   # VOSS:  Set a course. Let's see who's calling.
]

INTRA_GAP = 0.22   # gap between clips within the same spoken line
INTER_GAP = 0.40   # gap between different speakers' lines

def run(args):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error"] + args, check=True)

def extract(cid):
    f, s, e = clips[cid]
    out = os.path.join(TMP, f"{cid}.wav")
    run(["-ss", str(s), "-to", str(e), "-i", os.path.join(DIR, f"{f}.mp3"),
         "-ac", "1", "-ar", SR, out])
    return out

def silence(dur, tag):
    out = os.path.join(TMP, f"sil_{tag}.wav")
    run(["-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", str(dur), out])
    return out

# build silence files
sil_intra = silence(INTRA_GAP, "intra")
sil_inter = silence(INTER_GAP, "inter")

# extract all clips
for cid in clips:
    extract(cid)

# build ordered concat list
seq = []
for li, line in enumerate(lines):
    for ci, cid in enumerate(line):
        seq.append(os.path.join(TMP, f"{cid}.wav"))
        if ci != len(line) - 1:
            seq.append(sil_intra)
    if li != len(lines) - 1:
        seq.append(sil_inter)

listfile = os.path.join(TMP, "concat.txt")
with open(listfile, "w", encoding="utf-8") as fh:
    for p in seq:
        fh.write("file '" + p.replace("\\", "/") + "'\n")

out_mp3 = os.path.join(DIR, "Skit1.mp3")
run(["-f", "concat", "-safe", "0", "-i", listfile,
     "-ar", SR, "-ac", "1", "-b:a", "192k", out_mp3])
print("WROTE", out_mp3)
