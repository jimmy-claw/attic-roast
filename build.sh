#!/usr/bin/env bash
# build.sh — regenerate the whole Attic Roast kit from source.
#
#   1. gen_labels.py       -> labels/*.html
#   2. render.sh           -> out/*.pdf (exact physical size) + out/*.png (300 dpi)
#   3. copy               -> downloads/ (the files the site links)
#   4. site previews       -> assets/img/labels (900 px) + zoom (1800 px)
#   5. zip                -> attic-roast-print-kit.zip
#
# Was assembled by hand once; now it is one command. Re-run after any copy or
# artwork change and the site, the downloads and the zip cannot drift apart.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "== 1/5 · templates"
python3 gen_labels.py

# name:template:width_mm:height_mm   (matches the sizes declared on the site)
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
  # the small 70x100 mm bag labels (not on the site, but part of the family)
  "disco-parallel-small:disco-parallel-small.html:70:100"
  "private-fizz-small:private-fizz-small.html:70:100"
  "proof-of-pop-small:proof-of-pop-small.html:70:100"
  "do-not-crumble-small:do-not-crumble-small.html:70:100"
)

echo "== 2/5 · render (print PDF at exact size + 300 dpi PNG)"
# wipe first: a leftover artifact from an earlier run otherwise gets swept into the
# previews and the zip, so the build stops being a function of the sources.
rm -rf out; mkdir -p out
for p in "${PIECES[@]}"; do
  IFS=: read -r name file w h <<<"$p"
  "$DIR/render.sh" "$DIR/labels/$file" "$w" "$h" "$name"
done

echo "== 3/5 · downloads"
mkdir -p downloads
for p in "${PIECES[@]}"; do
  IFS=: read -r name _ _ _ <<<"$p"
  cp "out/$name.pdf" downloads/
  cp "out/$name.png" downloads/
done
# the standalone brand marks
cp downloads/brand/mark-*.svg downloads/ 2>/dev/null || true

echo "== 4/5 · site previews"
python3 - <<'PY'
import os
from PIL import Image
SRC="out"; LAB="assets/img/labels"; ZOO="assets/img/zoom"
os.makedirs(LAB, exist_ok=True); os.makedirs(ZOO, exist_ok=True)
names=[f[:-4] for f in sorted(os.listdir(SRC)) if f.endswith(".png")]
def resize(p, w, dest):
    im=Image.open(p).convert("RGB")
    h=round(im.size[1]*w/im.size[0])
    im.resize((w,h), Image.LANCZOS).save(dest, "JPEG", quality=88, optimize=True)
    return (w,h)
n=0
for name in names:
    p=os.path.join(SRC,name+".png")
    if name.endswith("-small"):          # family extra: keep it out of the site grid
        resize(p, 700, os.path.join(LAB,name+".jpg"))
    else:
        resize(p, 900,  os.path.join(LAB,name+".jpg"))
        resize(p, 1800, os.path.join(ZOO,name+".jpg"))
    n+=1
print(f"  {n} pieces -> {LAB} (900 px) + {ZOO} (1800 px)")
PY

echo "== 5/5 · zip"
rm -f attic-roast-print-kit.zip
( cd downloads && zip -qr ../attic-roast-print-kit.zip . -x "*.svg" )
# make sure nobody links a kit name that does not exist
if [ -f logos-attic-coffee-print-kit.zip ]; then rm -f logos-attic-coffee-print-kit.zip; fi
ls -lh attic-roast-print-kit.zip | awk '{print "  "$9" ("$5")"}'

echo
echo "== verification: no vendor name anywhere in the artwork =="
if grep -rin "logos\|λ" labels/*.html index.html 2>/dev/null; then
  echo "  !! FOUND — fix before printing"; exit 1
fi
echo "  ✓ clean"
