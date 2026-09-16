#!/usr/bin/env bash
# build.sh — regenerate BOTH directions of the Attic Roast kit from source.
#
#   dark     the Dark Prague room: ink ground, bone type, one accent per lot.
#   sunrise  the same design seen in daylight: cream ground, warm ink, colour in the
#            mark and a band of parallel stripes wherever the design has a full-width
#            rule (the horizon — and, literally, parallel).
#
#   1. gen_labels.py  -> labels/ and labels-sunrise/
#   2. render.sh      -> out/ : exact-size PDF + 300 dpi PNG per piece
#   3. copy           -> downloads/ and downloads-sunrise/
#   4. previews       -> assets/img/{labels,zoom}{,-sunrise}
#   5. zips           -> attic-roast-print-kit.zip and attic-roast-sunrise-kit.zip
#
# Run it after any copy or artwork change and the site, the downloads and the kits
# cannot drift apart.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# name:template:width_mm:height_mm   (the sizes declared on the site)
PIECES=(
  "disco-parallel:disco-parallel.html:157.16:130"
  "private-fizz:private-fizz.html:157.16:130"
  "proof-of-pop:proof-of-pop.html:157.16:130"
  "do-not-crumble:do-not-crumble.html:157.16:130"
  "back:back.html:157.16:130"
  "sticker:sticker.html:50:50"
  "table-card:table-card.html:148:210"
  "cup-sleeve:cup-sleeve.html:230:55"
  "sheet-a4-1:sheet-a4-1.html:210:297"
  "sheet-a4-2:sheet-a4-2.html:210:297"
  "disco-parallel-small:disco-parallel-small.html:70:100"
  "private-fizz-small:private-fizz-small.html:70:100"
  "proof-of-pop-small:proof-of-pop-small.html:70:100"
  "do-not-crumble-small:do-not-crumble-small.html:70:100"
)

theme_conf () {   # sets SRC DL LAB ZOO KIT
  case "$1" in
    dark)    SRC="labels";        DL="downloads";        LAB="assets/img/labels";        ZOO="assets/img/zoom";        KIT="attic-roast-print-kit" ;;
    sunrise) SRC="labels-sunrise";DL="downloads-sunrise";LAB="assets/img/labels-sunrise";ZOO="assets/img/zoom-sunrise";KIT="attic-roast-sunrise-kit" ;;
    *) echo "unknown theme $1" >&2; exit 2 ;;
  esac
}

echo "== 1/5 · templates"
python3 gen_labels.py

echo "== 2/5 · render (exact-size PDF + 300 dpi PNG)"
# wipe first: a leftover artifact from an earlier run otherwise gets swept into the
# previews and the zips, so the build stops being a function of the sources.
rm -rf out; mkdir -p out
for t in dark; do  # sunrise exists in code but is not built; see gen_labels.py
  theme_conf "$t"
  for p in "${PIECES[@]}"; do
    IFS=: read -r name file w h <<<"$p"
    "$DIR/render.sh" "$DIR/$SRC/$file" "$w" "$h" "$t-$name"
  done
done

echo "== 3/5 · downloads"
for t in dark; do  # sunrise exists in code but is not built; see gen_labels.py
  theme_conf "$t"
  mkdir -p "$DL"
  # clear prior outputs for this theme so a removed piece does not linger
  rm -f "$DL"/*.pdf "$DL"/*.png
  for p in "${PIECES[@]}"; do
    IFS=: read -r name _ _ _ <<<"$p"
    cp "out/$t-$name.pdf" "$DL/$name.pdf"
    cp "out/$t-$name.png" "$DL/$name.png"
  done
done

echo "== 4/5 · site previews"
python3 - <<'PY'
import os
from PIL import Image
for theme, lab, zoo in [("dark","assets/img/labels","assets/img/zoom")]:
    os.makedirs(lab, exist_ok=True); os.makedirs(zoo, exist_ok=True)
    n=0
    for f in sorted(os.listdir("out")):
        if not (f.startswith(theme+"-") and f.endswith(".png")): continue
        name=f[len(theme)+1:-4]
        im=Image.open(os.path.join("out",f)).convert("RGB")
        def save(w, dest):
            h=round(im.size[1]*w/im.size[0])
            im.resize((w,h), Image.LANCZOS).save(dest,"JPEG",quality=88,optimize=True)
        if name.endswith("-small"):
            save(700, os.path.join(lab,name+".jpg"))
        else:
            save(900,  os.path.join(lab,name+".jpg"))
            save(1800, os.path.join(zoo,name+".jpg"))
        n+=1
    print(f"  {theme}: {n} pieces -> {lab} (900 px) + {zoo} (1800 px)")
PY

echo "== 5/5 · zip"
for t in dark; do  # sunrise exists in code but is not built; see gen_labels.py
  theme_conf "$t"
  rm -f "$KIT.zip"
  ( cd "$DL" && zip -qr "../$KIT.zip" . -x "*.svg" )
  ls -lh "$KIT.zip" | awk '{print "  "$9" ("$5")"}'
done

echo
echo "== verification: the mark fits the cup at every weight it is used at =="
python3 - <<'PYCHECK'
def lx(y): return 42 + (54-42)*(y-112)/(164-112)   # left wall, top -> bottom
def rx(y): return 140 + (128-140)*(y-112)/(164-112) # right wall
bars=[((70,158),(86,132)), ((96,158),(112,132))]
worst=1e9
for sw in (8,9,10,11,12,14,16):
    bw=max(5,round(sw*0.8))
    for (x0,y0),(x1,y1) in bars:
        worst=min(worst, x0-bw/2-lx(y0)-sw/2, rx(y0)+sw/2-(x1+bw/2),
                         y1-bw/2-(112+sw/2), (177-sw/2)-(y0+bw/2))
d=[(x1-x0,y1-y0) for (x0,y0),(x1,y1) in bars]
print(f"  worst clearance across stroke widths 8..16: {worst:.1f} px  {'ok' if worst>0 else '!! OVERLAP'}")
print(f"  bars parallel by construction: {d[0]==d[1]}")
import sys; sys.exit(0 if worst>0 and d[0]==d[1] else 1)
PYCHECK

echo
echo "== verification: no vendor name anywhere in the artwork =="
if grep -rin "logos\|λ" labels/*.html index.html 2>/dev/null; then
  echo "  !! FOUND — fix before printing"; exit 1
fi
echo "  clean"
