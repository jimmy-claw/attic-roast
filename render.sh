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
# A RELATIVE path silently renders a blank page: the URL becomes file://labels/x.html,
# which is invalid, and Chromium happily prints about:blank at the right size. Caught on
# 2026-09-25 only because the ink coverage was checked. Require an absolute path.
case "$1" in /*) ;; *) echo "render.sh: pass an ABSOLUTE html path (got: $1) — a relative one renders blank" >&2; exit 2;; esac
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
# A label PDF must be exactly ONE page. Every label rendered from 2026-09-16 until 2026-09-25
# carried a SECOND, EMPTY page: .wide::before is a vignette inset -5mm on every side, so it
# overhung the page box and Chromium paginated the spill. Nothing caught it because nothing
# counted pages. So count them.
import subprocess
_pi = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True)
_np = 0
for _l in _pi.stdout.splitlines():
    if _l.startswith('Pages:'):
        _np = int(_l.split()[1])
if _np != 1:
    print(f'  X {pdf.split("/")[-1]}: {_np} PAGES - a label must be exactly 1. Look for an element overhanging the page box (see .wide::before in label.css).')
    raise SystemExit(1)
# CONTENT, not just the envelope. On 2026-09-25 four labels passed every size and page-count
# check while being completely BLANK: a relative html path made the URL file://labels/x.html,
# which is invalid, so Chromium printed about:blank at exactly the right dimensions. Nothing
# noticed because nothing looked at the pixels. A blank page is ~100% one luminance value,
# whichever direction the label runs, so test for a single flat band rather than for darkness.
_im = Image.open(png).convert("L")
_hist = _im.histogram()
_total = _im.size[0] * _im.size[1]
_dominant = max(_hist) / _total
if _dominant > 0.99:
    print(f"  X {pdf.split('/')[-1]}: {_dominant*100:.1f}% of pixels are one value - the page is BLANK. "
          f"Check the html path is absolute (file:// with a relative path prints an empty page).")
    raise SystemExit(1)

im = Image.open(png); w,h = im.size
ok = mm and abs(mm[2]-wmm) < 0.02 and abs(mm[3]-hmm) < 0.02
print(f"  {pdf.split('/')[-1]}: {w}x{h}px · PDF box {mm[2]}x{mm[3]}mm (target {wmm}x{hmm}) {'' if ok else '  <-- SIZE MISMATCH'}")
PY
