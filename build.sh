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

echo "== 1/5 · templates (both directions)"
python3 gen_labels.py

echo "== 2/5 · render (exact-size PDF + 300 dpi PNG)"
# wipe first: a leftover artifact from an earlier run otherwise gets swept into the
# previews and the zips, so the build stops being a function of the sources.
rm -rf out; mkdir -p out
for t in dark sunrise; do
  theme_conf "$t"
  for p in "${PIECES[@]}"; do
    IFS=: read -r name file w h <<<"$p"
    "$DIR/render.sh" "$DIR/$SRC/$file" "$w" "$h" "$t-$name"
  done
done

echo "== 3/5 · downloads"
for t in dark sunrise; do
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
for theme, lab, zoo in [("dark","assets/img/labels","assets/img/zoom"),
                        ("sunrise","assets/img/labels-sunrise","assets/img/zoom-sunrise")]:
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

echo "== 5/5 · zips"
for t in dark sunrise; do
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
echo "== verification: sunrise accents are legible on a cream ground =="
python3 - <<'PYCHECK'
def lin(c):
    c/=255.0
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lum(h):
    r,g,b=(int(h[i:i+2],16) for i in (1,3,5))
    return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def ratio(a,b):
    la,lb=lum(a),lum(b); hi,lo=max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)
GROUND="#FBF3E4"
lots=[("Disco Parallel","#D9411C","#A83210"),("Private Fizz","#C42A7C","#961D5E"),
      ("Do Not Crumble","#B0740A","#8A5A06"),("Proof of Pop","#5B3ACF","#4429A6")]
bad=0
for name, acc, txt in lots:
    r1, r2 = ratio(acc,GROUND), ratio(txt,GROUND)
    # the accent carries the mark and rules (large, so 3:1 is the bar); the tiny
    # metadata uses the darker tint and must clear 4.5:1.
    ok = r1>=3.0 and r2>=4.5
    bad += 0 if ok else 1
    print(f"  {name:16s} accent {acc} {r1:.2f}:1 (>=3)   text {txt} {r2:.2f}:1 (>=4.5)   {'ok' if ok else '!! FAIL'}")
print(f"  ink on cream: {ratio('#1A140C',GROUND):.1f}:1")
import sys; sys.exit(1 if bad else 0)
PYCHECK

echo
echo "== verification: the horizon band is on every sunrise piece, absent from every dark one =="
python3 - <<'PYCHECK'
# Read the LAST FEW ROWS of each rendered piece, take the longest run of each stripe
# colour across those rows, and require it to be a sensible fraction of the width.
#
# Two earlier versions of this check were wrong, in opposite directions, and both cost
# real time: counting colour presence ANYWHERE reported a false leak on dark proof-of-pop
# (its grape accent is close to the violet stripe), and reading only the bottom two rows
# missed pieces where the band's last millimetre is cropped. Reading a few rows and
# requiring actual runs has neither failure mode.
from PIL import Image
import sys, os
STRIPES=[("sun",(247,179,43)),("coral",(242,100,60)),("magenta",(232,80,141)),
         ("violet",(124,92,255)),("aqua",(47,179,201))]
PIECES=["disco-parallel","private-fizz","proof-of-pop","do-not-crumble","back","sticker",
        "disco-parallel-small","private-fizz-small","proof-of-pop-small","do-not-crumble-small",
        "cup-sleeve","table-card"]
def longest(path):
    im=Image.open(path).convert("RGB"); w,h=im.size
    best={}
    for y in range(h-1,max(h-8,0),-1):
        prev=None; run=0
        for x in range(w):
            p=im.getpixel((x,y)); hit=None
            for name,t in STRIPES:
                if sum(abs(a-b) for a,b in zip(p,t))<40: hit=name; break
            if hit==prev and hit: run+=1
            else: prev,run=hit,1
            if hit and run>best.get(hit,0): best[hit]=run
    return w, best
bad=[]
for f in PIECES:
    for theme, want in (("sunrise",5),("dark",0)):
        p=f"out/{theme}-{f}.png"
        if not os.path.exists(p): continue
        w, best = longest(p)
        n=len([k for k,v in best.items() if v >= 0.08*w])
        if n != want: bad.append(f"{theme}/{f} showed {n}")
if bad:
    for b in bad: print("   !!"+b)
    sys.exit(1)
print(f"   sunrise: all 5 stripes on all {len(PIECES)} pieces")
print(f"   dark:    no band on all {len(PIECES)} pieces")
PYCHECK

echo "== verification: no vendor name anywhere in the artwork =="
if grep -rin "logos\|λ" labels/*.html labels-sunrise/*.html index.html 2>/dev/null; then
  echo "  !! FOUND — fix before printing"; exit 1
fi
echo "  clean (both directions)"
