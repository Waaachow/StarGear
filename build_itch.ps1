# Builds the itch.io HTML bundle for Star Gear - Episode 0 - The Ghost Signal.
# Produces "<title> - v0.1.zip" in the project root with index.html at the zip root.
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$ErrorActionPreference = "Stop"

$root  = Split-Path -Parent $MyInvocation.MyCommand.Path
$build = Join-Path $root "dist\build"
$A     = Join-Path $build "Assets"
$index = Join-Path $build "index.html"
$zip   = Join-Path $root "StarGear - Episode 0 - The Ghost Signal - v0.4.zip"

# ---------- 1. stage a clean tree ----------
if (Test-Path $build) { Remove-Item $build -Recurse -Force }
New-Item -ItemType Directory -Path $build -Force | Out-Null
Copy-Item (Join-Path $root "episode1.html")           (Join-Path $build "index.html")
Copy-Item (Join-Path $root "iso_grid_prototype.html") $build
Copy-Item (Join-Path $root "Assets") (Join-Path $build "Assets") -Recurse
Copy-Item (Join-Path $root "audio")  (Join-Path $build "audio")  -Recurse
# loose root sprites the iso game loads by bare filename (player StarGear hull)
foreach ($n in @("north east.png","south west.png")) { Copy-Item (Join-Path $root $n) $build }
# drop dev leftovers from the staged copy
Get-ChildItem $A -Recurse -File | Where-Object { $_.Name -like "*--old*" } | ForEach-Object { [System.IO.File]::Delete($_.FullName) }
Get-ChildItem (Join-Path $build "audio") -File | Where-Object { $_.Name -like "line_*.mp3" } | ForEach-Object { [System.IO.File]::Delete($_.FullName) }

# ---------- 2. image compression helpers ----------
$jpgCodec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() |
  Where-Object { $_.FormatID -eq [System.Drawing.Imaging.ImageFormat]::Jpeg.Guid }
function JpegParams([int]$q) {
  $ep = New-Object System.Drawing.Imaging.EncoderParameters(1)
  $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [int64]$q)
  return $ep
}
function To-Jpeg($srcPng, [int]$maxW, [int]$q) {   # opaque art -> JPEG, returns Assets-rel .png path
  $img = [System.Drawing.Image]::FromFile($srcPng)
  $w = $img.Width; $h = $img.Height
  if ($maxW -gt 0 -and $w -gt $maxW) { $s = $maxW/$w; $nw = [int]($w*$s); $nh = [int]($h*$s) } else { $nw = $w; $nh = $h }
  $bmp = New-Object System.Drawing.Bitmap($nw, $nh)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.Clear([System.Drawing.Color]::Black); $g.DrawImage($img, 0, 0, $nw, $nh)
  $g.Dispose(); $img.Dispose()
  $dst = [System.IO.Path]::ChangeExtension($srcPng, ".jpg")
  $bmp.Save($dst, $jpgCodec, (JpegParams $q)); $bmp.Dispose()
  [System.IO.File]::Delete($srcPng)
  return $srcPng.Substring($build.Length + 1).Replace('\','/')
}
function Shrink-Png($srcPng, [int]$maxEdge) {       # sprite downscale, keeps alpha + filename
  $img = [System.Drawing.Image]::FromFile($srcPng)
  $w = $img.Width; $h = $img.Height; $long = [Math]::Max($w,$h)
  if ($long -le $maxEdge) { $img.Dispose(); return }
  $s = $maxEdge/$long; $nw = [int]($w*$s); $nh = [int]($h*$s)
  $bmp = New-Object System.Drawing.Bitmap($nw, $nh, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.Clear([System.Drawing.Color]::Transparent); $g.DrawImage($img, 0, 0, $nw, $nh)
  $g.Dispose(); $img.Dispose()
  $tmp = "$srcPng.tmp"; $bmp.Save($tmp, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
  [System.IO.File]::Delete($srcPng); [System.IO.File]::Move($tmp, $srcPng)
}

# ---------- 3. compress ----------
$converted = @()
# CGs are drawn full-screen, so nothing gains from being wider than 1920. This used to
# cap CG02 by name; cg_red_reaver.png arrived at the same 7552x4256 / 40 MB, so the cap
# is now general and the next oversized CG is handled without editing this script.
foreach ($f in Get-ChildItem "$A\CG" -File -Filter *.png) {
  $converted += (To-Jpeg $f.FullName 1920 88)
}
# NOTE: the four station dock interiors (Waypoint_Hub/Veil_Anchorage/Quarry_Station/
# Salvage_Reach.png) are opaque and look like JPEG candidates, but the iso builds their
# path DYNAMICALLY (`Assets/${s.name.replace(/ /g,"_")}.png`), so the literal .png->.jpg
# rewrite below can't reach it and the built game would silently fall back to the flat
# fill. They stay PNG (~6 MB) unless the loader grows a .jpg retry.
foreach ($n in @("Bridge.png","Bridge Red Alert.png","Bg03.png","bg04.png","bg06.png","START_SCREEN.png","THANKS.png","DEFEAT.png")) {
  $p = Join-Path $A $n; if (Test-Path $p) { $converted += (To-Jpeg $p 0 88) }
}
foreach ($sub in @("obj","space")) { foreach ($f in Get-ChildItem (Join-Path $A $sub) -File -Filter *.png) { Shrink-Png $f.FullName 900 } }
foreach ($n in @("north east.png","south west.png")) { Shrink-Png (Join-Path $build $n) 900 }
# char/* left at native PNG (shown large, need alpha)

# rewrite .png -> .jpg refs (plain replace so em/en-dashes match verbatim).
# BOTH html files: the iso now references Assets/CG too (boss encounter art), and
# rewriting only index.html left it pointing at a .png the build had just deleted.
foreach ($doc in @($index, (Join-Path $build "iso_grid_prototype.html"))) {
  if (-not (Test-Path $doc)) { continue }
  $html = [System.IO.File]::ReadAllText($doc, [System.Text.Encoding]::UTF8)
  foreach ($rel in $converted) { $html = $html.Replace($rel, [System.IO.Path]::ChangeExtension($rel, ".jpg")) }
  [System.IO.File]::WriteAllText($doc, $html, (New-Object System.Text.UTF8Encoding($false)))
}

# ---------- 4. zip (forward-slash entries; itch needs index.html at the root) ----------
if (Test-Path $zip) { [System.IO.File]::Delete($zip) }
$fs = [System.IO.File]::Open($zip, [System.IO.FileMode]::Create)
$archive = New-Object System.IO.Compression.ZipArchive($fs, [System.IO.Compression.ZipArchiveMode]::Create)
$base = (Resolve-Path $build).Path.TrimEnd('\') + '\'
$n = 0
Get-ChildItem $build -Recurse -File | ForEach-Object {
  $rel = $_.FullName.Substring($base.Length).Replace('\','/')
  $entry = $archive.CreateEntry($rel, [System.IO.Compression.CompressionLevel]::Optimal)
  $es = $entry.Open(); $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
  $es.Write($bytes, 0, $bytes.Length); $es.Close(); $n++
}
$archive.Dispose(); $fs.Close()

$zmb = [math]::Round(((Get-Item $zip).Length/1MB),1)
Write-Output ("Built: " + (Split-Path $zip -Leaf))
Write-Output ("Files: $n   Size: $zmb MB")
