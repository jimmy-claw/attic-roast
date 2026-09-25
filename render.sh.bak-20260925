#!/usr/bin/env bash
# render.sh <label.html> <w_mm> <h_mm> [outname]
# Print-ready output: headless Chromium PDF -> ghostscript normalises the page box to
# EXACT points (Chromium rounds to whole pt, so 157.16mm came out 156.97mm) -> 300dpi PNG.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
HTML="$1"; WMM="$2"; HMM="$3"; NAME="${4:-$(basename "$HTML" .html)}"
mkdir -p "$DIR/out"
WPT=$(python3 -c "print(round($WMM/25.4*72,3))")
HPT=$(python3 -c "print(round($HMM/25.4*72,3))")
CHR="chromium --headless=new --no-sandbox --disable-gpu --virtual-time-budget=8000"

$CHR --print-to-pdf="$DIR/out/$NAME.raw.pdf" --no-pdf-header-footer "file://$HTML" >/dev/null 2>&1
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 \
   -dFIXEDMEDIA -dDEVICEWIDTHPOINTS="$WPT" -dDEVICEHEIGHTPOINTS="$HPT" \
   -dAutoRotatePages=/None -sOutputFile="$DIR/out/$NAME.pdf" "$DIR/out/$NAME.raw.pdf" >/dev/null 2>&1
rm -f "$DIR/out/$NAME.raw.pdf"
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r300 -sOutputFile="$DIR/out/$NAME.png" "$DIR/out/$NAME.pdf" >/dev/null 2>&1

python3 - "$DIR/out/$NAME.pdf" "$DIR/out/$NAME.png" "$WMM" "$HMM" <<'PY'
import sys, re
from PIL import Image
pdf, png, wmm, hmm = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
d = open(pdf,'rb').read()
m = re.search(rb'/MediaBox\s*\[([^\]]+)\]', d)
mm = [round(float(x)*25.4/72, 2) for x in m.group(1).split()] if m else None
im = Image.open(png); w,h = im.size
ok = mm and abs(mm[2]-wmm) < 0.02 and abs(mm[3]-hmm) < 0.02
print(f"  {pdf.split('/')[-1]}: {w}x{h}px · PDF box {mm[2]}x{mm[3]}mm (target {wmm}x{hmm}) {'' if ok else '  <-- SIZE MISMATCH'}")
PY
