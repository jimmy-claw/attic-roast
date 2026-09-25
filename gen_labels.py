#!/usr/bin/env python3
"""Generate the Attic Roast label family.

Coffee = Fifty Beans (Brno). The three labels are the REAL lineup (special/funky
lots), so the copy matches the beans: variety, process, producer, notes.
Our job is the branding, not the coffee identity.

Brand note: this is deliberately NOT branded as any company. The room at Dark
Prague is the Attic, so the coffee is "Attic Roast" — privacy, parallel
infrastructure, and the city. No vendor name appears anywhere on the artwork.
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Two directions. "dark" is the Dark Prague room; "sunrise" is the same design seen in
# daylight — outdoors, colourful, funky. The layout is identical: only the ground, the
# accents and the treatment of a full-width rule change, because a full-width rule in
# sunrise becomes a band of parallel stripes (the horizon — and, literally, parallel).
SUNRISE_CSS = """
:root{--ink:#FBF3E4;--ink2:#F3E8D4;--bone:#1A140C;--sage:#8A7660}
html,body{background:#FBF3E4}
.rule--full{background:none;height:1.8mm;opacity:1;
  background-image:linear-gradient(90deg,
    #F7B32B 0 20%,#F2643C 20% 40%,#E8508D 40% 60%,#7C5CFF 60% 80%,#2FB3C9 80% 100%)}
.sleeve__rule{height:2.2mm;
  background-image:linear-gradient(90deg,
    #F7B32B 0 20%,#F2643C 20% 40%,#E8508D 40% 60%,#7C5CFF 60% 80%,#2FB3C9 80% 100%)}
.bands{display:flex;position:absolute;left:0;right:0;bottom:0;height:6mm;z-index:9;flex:none}
.bands--sm{height:4mm}
.sheet{background:#F2E7D3}
.cell,.bleed{background:#FBF3E4}
.cr{background:#6B716C}
.card .bg{opacity:.70;filter:saturate(1.2) brightness(1.08)}
.card .veil{background:linear-gradient(180deg,rgba(251,243,228,.50) 0%,rgba(251,243,228,.86) 45%,#FBF3E4 100%)}
"""

THEMES = {
 "dark": dict(out="labels", bg="#0C0C0D", sheet_bg="#F4F3EC", css=""),
 "sunrise": dict(out="labels-sunrise", bg="#FBF3E4", sheet_bg="#F2E7D3", css=SUNRISE_CSS),
}

def emblem(color="#E2542B", stroke=10, cls="emblem", bar=None):
    """Attic Roast mark: a cup with two parallel bars stamped on its body.
    No rim line on top (it read as a stray stroke); the body edge IS the rim.
    The bars are not a logo and not a lock: they say *parallel* — parallel
    society, parallel infrastructure — and they echo // for the people in the
    room. A keyhole was tried first and read as a padlock."""
    barw = max(5, round(stroke * 0.8))  # lighter than the silhouette, and it fits at every weight
    barc = bar or "currentColor"
    return f'''<svg class="{cls}" viewBox="0 0 200 200" fill="none" aria-label="Attic Roast" style="color:{color}">
<g fill="none" stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">
<path d="M42 112 H140 L128 164 a14 14 0 0 1 -13 13 H67 a14 14 0 0 1 -13 -13 Z"/>
<path d="M140 126 a25 25 0 0 1 0 38"/>
</g>
<g stroke="{barc}" stroke-width="{barw}" stroke-linecap="round">
<path d="M70 158 L86 132"/><path d="M96 158 L112 132"/>
</g>
</svg>'''

def head(title, wmm, hmm, bg="#0C0C0D", extra="", theme="dark"):
    # Chromium rounds @page sizes to whole POINTS (157.16mm -> 156.97mm), so we render on a
    # page 1.5mm larger, anchor the piece to the BOTTOM-LEFT, and let ghostscript crop the
    # extra (gs -dFIXEDMEDIA keeps the bottom-left of the larger page). Result: exact trim,
    # no white hairline at the edge.
    wpt, hpt = round((wmm+1.5)/25.4*72, 3), round((hmm+1.5)/25.4*72, 3)
    theme_css = f'<style>{THEMES[theme]["css"]}</style>' if THEMES[theme]["css"] else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>
@page{{size:{wpt}pt {hpt}pt;margin:0}}
html,body{{margin:0;padding:0}}
body.pg{{position:relative;width:{wmm+1.5}mm;height:{hmm+1.5}mm;background:{bg};overflow:hidden}}
body.pg > *{{position:absolute;left:0;bottom:0}}
</style>
<link rel="stylesheet" href="label.css">{theme_css}{extra}</head>
'''

# ── the special coffees (Fifty Beans, Brno) ───────────────────────────────────
# All four: Edinson Argote, Colombia · enzymatic fermentation · espresso & filter · 499 Kč
VARIANTS = [
 dict(slug="disco-parallel", wide_size="40pt", pun="Disco<br>Parallel", size="36pt",
      accent="#E2542B", accent_text="#F4794E", s_accent="#D9411C", s_text="#A83210",
      process="Enzymatic fermentation",
      notes="Blackberry candy · Cherries · Herbs",
      lot="Disco Candy",
      origin="Ombligon · Edinson Argote, Colombia"),
 dict(slug="private-fizz", wide_size="40pt", pun="Private<br>Fizz", size="40pt",
      accent="#E85D9E", accent_text="#F58BB6", s_accent="#C42A7C", s_text="#961D5E",
      process="Enzymatic fermentation",
      notes="Rose water · Raspberry soda · Florals",
      lot="Rose Fizz",
      origin="Typica Mejorado · Edinson Argote, Colombia"),
 dict(slug="proof-of-pop", wide_size="40pt", pun="Proof<br>of Pop", size="38pt",
      accent="#8B5CF6", accent_text="#A98BFF", s_accent="#5B3ACF", s_text="#4429A6",
      process="Enzymatic fermentation",
      notes="Raspberry cake · Stone fruit",
      lot="Crazy Pop",
      origin="Caturra Chiroso · Edinson Argote, Colombia"),
 dict(slug="do-not-crumble", wide_size="40pt", pun="Do Not<br>Crumble", size="33pt",
      accent="#F2A93B", accent_text="#F7C46B", s_accent="#B0740A", s_text="#8A5A06",
      process="Enzymatic fermentation",
      notes="Vanilla · Cherries · Disco",
      lot="Vanilla Crumble",
      origin="Colombia & Ethiopia"),
]

KICKER = "Attic&nbsp;Roast&nbsp;×&nbsp;Dark&nbsp;Prague&nbsp;2026"
KICKER_SHORT = "Attic&nbsp;Roast&nbsp;×&nbsp;Dark&nbsp;Prague"

BAND_COLOURS = ["#F7B32B","#F2643C","#E8508D","#7C5CFF","#2FB3C9"]
# Fully self-contained: every dimension inline, no class, no cascade. Three attempts to
# style this from CSS failed because .wide > * and body.pg > * (and flex shrinking) kept
# winning, and the failure was invisible in the markup — the element was always present.
# The theme now decides in Python whether the band exists at all.
def bands_html(h="6mm"):
    cells = "".join(
        f'<i style="flex:1 1 0;display:block;height:100%;background:{c}"></i>' for c in BAND_COLOURS)
    # left:0 + an explicit width, NOT left:0;right:0. With left+right the box came out
    # 100 mm wide on a 157 mm label (the stripes were equal fifths of a shrink-to-fit
    # box), so the horizon stopped two-thirds of the way across. An explicit 100% of the
    # padding box cannot be shrink-to-fit and covers the label edge to edge.
    # position:fixed, not absolute. Absolute resolved against whatever ancestor Chrome
    # picked (the stripes came out 100 mm wide on a 157 mm label and the horizon stopped
    # two-thirds across, no matter whether I used left+right or an explicit width). Fixed
    # resolves against the page, which is what a full-bleed horizon actually wants.
    return ('<div style="display:flex;position:fixed;left:0;width:100%;bottom:0;'
            f'height:{h};z-index:9">{cells}</div>')

STORY = ("Private by default is not a setting, it is a place to stand: "
         "communities that run on their own ground instead of someone else's. "
         "Special lots were chosen for the <span style=\"color:var(--bone)\">Attic Roast</span> "
         "coffee session at Dark Prague — exotic varieties, advanced fermentation, "
         "roasted in Brno by <span style=\"color:var(--bone)\">Fifty Beans</span>.")

# ── the wide 157.16 x 130 mm label (the size Fifty Beans actually prints) ─────
WIDE_INNER = '''<div class="wide" style="--accent:{accent};--accent-text:{accent_text}">
  <div class="row">
    <span class="tiny tiny--bone">''' + KICKER + '''</span>
      </div>

  <div class="wide__main">
    <div class="wide__left">
      <h1 class="display wide__name" style="font-size:{size}">{pun}</h1>
      <div class="rule rule--full" style="margin-top:5mm"></div>
      <div class="mono" style="font-size:8.6pt;letter-spacing:.14em;text-transform:uppercase">{process}</div>
      <div class="mono" style="font-size:8pt;color:var(--sage);margin-top:2mm;letter-spacing:.05em;text-transform:uppercase">{notes}</div>
      <div class="wide__facts">
        <div class="wide__fact"><b>Lot</b><span>{lot}</span></div>
        <div class="wide__fact"><b>Variety · origin</b><span>{origin}</span></div>
        <div class="wide__fact"><b>For</b><span>Espresso &amp; filter</span></div>
      </div>
    </div>
    <div class="wide__right">
      <div style="color:var(--accent)">{emblem}</div>
      <div class="mono" style="font-size:5.6pt;letter-spacing:.16em;color:var(--sage);text-transform:uppercase;text-align:center;margin-top:3mm">Attic&nbsp;Roast<br>Dark&nbsp;Prague</div>
    </div>
  </div>

  <div class="wide__footer">
    <div class="row" style="align-items:flex-end">
      <div class="mono" style="font-size:8pt;color:var(--accent-text);line-height:1.45;text-transform:uppercase;letter-spacing:.08em">Build&nbsp;the&nbsp;parallel,<br>one&nbsp;cup&nbsp;at&nbsp;a&nbsp;time.</div>
      <div class="mono" style="font-size:6pt;color:var(--sage);line-height:1.6;text-transform:uppercase;letter-spacing:.06em;text-align:right">
        200&nbsp;g&nbsp;·&nbsp;Whole&nbsp;bean<br>Roasted&nbsp;by&nbsp;Fifty&nbsp;Beans&nbsp;·&nbsp;Brno
      </div>
    </div>
    <div class="rule"></div>
    <div class="row">
      <span class="tiny">Old&nbsp;Wastewater&nbsp;Treatment&nbsp;Plant&nbsp;·&nbsp;Prague</span>
      <span class="tiny">Espresso&nbsp;&amp;&nbsp;filter</span>
    </div>
  </div>
  {bands}
</div>'''


LABEL_INNER = '''<div class="label" style="--accent:{accent};--accent-text:{accent_text}">
  <div class="row">
    <span class="tiny tiny--bone">''' + KICKER_SHORT + '''</span>
      </div>
  <div style="margin-top:3mm">{emblem}</div>
  <h1 class="display" style="font-size:{size};margin-top:3mm">{pun}</h1>
  <div class="rule rule--full" style="margin-top:3mm"></div>
  <div class="mono" style="font-size:7pt;letter-spacing:.12em;text-transform:uppercase">{process}</div>
  <div class="mono" style="font-size:6.1pt;color:var(--sage);margin-top:1.3mm;letter-spacing:.06em;text-transform:uppercase">{notes}</div>
  <div class="mono" style="font-size:5.4pt;color:var(--bone);margin-top:2.2mm;letter-spacing:.08em">{lot}</div>
  <div class="mono" style="font-size:5.1pt;color:var(--sage);margin-top:.8mm;letter-spacing:.06em;text-transform:uppercase">{origin}</div>
  <div class="footer">
    <div class="mono" style="font-size:6.6pt;color:var(--accent-text);line-height:1.5;text-transform:uppercase;letter-spacing:.08em">Build&nbsp;the&nbsp;parallel,<br>one&nbsp;cup&nbsp;at&nbsp;a&nbsp;time.</div>
    <div class="rule"></div>
    <div class="row">
      <span class="tiny">200&nbsp;g&nbsp;·&nbsp;Whole&nbsp;bean</span>
      <span class="tiny">Fifty&nbsp;Beans&nbsp;·&nbsp;Brno</span>
    </div>
  </div>
  {bands}
</div>'''

# NOT PRINTED. Fifty Beans' own back label already carries origin, producer, roast and
# best-before dates, a QR code, the barcode and a full brew recipe, in Czech. A second back
# label would restate a subset of that in a different voice, so the bag carries OUR FRONT
# ONLY (Václav, 2026-09-16: "let's go with one label on the front"). This template is kept
# because it costs nothing and a plain bag may want one day.
BACK_INNER = '''<div class="back">
  <div>
    <div class="row" style="margin-bottom:5mm">
      <span class="tiny tiny--bone">''' + KICKER_SHORT + '''</span>
          </div>
    <div class="display" style="font-size:16pt;color:var(--ember)">Private-by-default<br>caffeine.</div>
    <div class="rule rule--full" style="margin:4mm 0"></div>
    <p class="mono" style="font-size:6.1pt;line-height:1.65;color:var(--sage)">
      ''' + STORY + '''
    </p>
  </div>

  <div>
    <div class="mono" style="font-size:6.0pt;line-height:1.75;color:var(--sage);text-transform:uppercase">
      <span style="color:var(--bone)">Brew</span> · filter 60 g/L · 4:00<br>
      <span style="color:var(--bone)">Espresso</span> · 18 g in · 36 g out · 27 s<br>
      <span style="color:var(--ember-text)">Best 10 days after roast (espresso) / 7 (filter).<br>
      On opening, let the bag air 24 h before brewing.</span>
    </div>
    <div class="rule"></div>
    <div class="row">
      <div class="mono" style="font-size:5.3pt;line-height:1.7;color:var(--sage);letter-spacing:.08em;text-transform:uppercase">
        Roasted by Fifty Beans · Brno<br>
        Speciality arabica · small batch<br>
        <span style="color:var(--bone)">fiftybeans.cz</span>
      </div>
      <div style="color:var(--ember);width:16mm">{emblem_sm}</div>
    </div>
  </div>
  {bands_sm}
</div>'''

STICKER = '''<body class="pg">
<div class="sticker" style="--accent:#E2542B">
  <div style="color:var(--ember)">{emblem}</div>
  <div class="display" style="font-size:11pt;margin-top:1.6mm">Attic&nbsp;Roast</div>
  <div style="width:22mm;height:.3mm;background:var(--accent);margin:1.8mm 0"></div>
  <div class="mono" style="font-size:5pt;letter-spacing:.14em;color:var(--sage);text-transform:uppercase">Dark Prague 2026<br>Coffee</div>
</div>
{bands_sm}
</body></html>
'''

CARD = '''<body class="pg">
<div class="card">
  <img class="bg" src="../assets/img/hero-plant.jpg" alt="">
  <div class="veil"></div>
  {bands}
<div class="in">
    <div class="row">
      <span class="tiny tiny--bone">''' + KICKER + '''</span>
      <span class="tiny">Old&nbsp;Wastewater&nbsp;Plant&nbsp;·&nbsp;Prague</span>
    </div>
    <div class="spacer" style="flex:1"></div>
    <div style="color:var(--ember);margin-bottom:6mm">{emblem}</div>
    <div class="display" style="font-size:52pt">Coffee<br>Session</div>
    <div class="rule rule--full" style="margin:6mm 0 5mm"></div>
    <div class="sans" style="font-family:'Space Grotesk',sans-serif;font-size:15pt;color:var(--bone)">
      Pour. Sip. Chat.
    </div>
    <p class="mono" style="font-size:7pt;line-height:1.7;color:var(--sage);margin-top:4mm;max-width:105mm;text-transform:uppercase">
      Special lots — Disco&nbsp;Candy, Rose&nbsp;Fizz, Crazy&nbsp;Pop. Exotic varieties,
      enzymatic fermentation, roasted in Brno by Fifty&nbsp;Beans.
    </p>
    <div class="row" style="margin-top:10mm;align-items:flex-end">
      <div class="display" style="font-size:13pt;color:var(--sage)">Build&nbsp;the<br>Parallel.</div>
      <div class="mono" style="font-size:6pt;color:var(--sage);text-align:right;text-transform:uppercase;letter-spacing:.08em">
        Dark&nbsp;Prague&nbsp;2026<br>Old&nbsp;Wastewater&nbsp;Plant
      </div>
    </div>
  </div>
</div>
</body></html>
'''

SLEEVE = '''<body class="pg">
<div class="sleeve">
  <div class="sleeve__rule"></div>
  <div class="sleeve__in">
    <div style="color:var(--ember)">{emblem}</div>
    <div class="sleeve__txt">
      <div class="display" style="font-size:26pt">Attic&nbsp;Roast</div>
      <div class="mono" style="font-size:8.6pt;letter-spacing:.2em;color:var(--sage);text-transform:uppercase;margin-top:2mm">
        Coffee&nbsp;Session&nbsp;·&nbsp;Dark&nbsp;Prague&nbsp;2026&nbsp;·&nbsp;Old&nbsp;Wastewater&nbsp;Plant
      </div>
      <div class="mono" style="font-size:8.6pt;letter-spacing:.16em;color:var(--ember-text);text-transform:uppercase;margin-top:3.5mm">
        Build&nbsp;the&nbsp;parallel,&nbsp;one&nbsp;cup&nbsp;at&nbsp;a&nbsp;time.
      </div>
    </div>
  </div>
  <div class="sleeve__rule"></div>
</div>
</body></html>
'''

WIDE_BACK_INNER = '''<div class="wide">
  <div class="row">
    <span class="tiny tiny--bone">''' + KICKER + '''</span>
      </div>

  <div class="wide__main">
    <div class="wide__left">
      <div class="display" style="font-size:26pt;color:var(--ember)">Private-by-default<br>caffeine.</div>
      <div class="rule rule--full" style="margin:4mm 0"></div>
      <p class="mono" style="font-size:7pt;line-height:1.7;color:var(--sage);max-width:88mm">
        ''' + STORY + '''
      </p>
    </div>

    <div class="wide__right">
      <div style="color:var(--ember);width:38mm">{emblem_lg}</div>
      <div class="mono" style="font-size:6pt;letter-spacing:.14em;color:var(--sage);text-transform:uppercase;margin-top:4mm;text-align:center">Attic&nbsp;Roast<br>Dark&nbsp;Prague&nbsp;2026</div>
    </div>
  </div>

  <div class="wide__footer">
    <div class="wide__facts" style="margin-top:0">
      <div class="wide__fact"><b>Brew · filter</b><span>60 g/L · 4:00</span></div>
      <div class="wide__fact"><b>Brew · espresso</b><span>18 g in · 36 g out · 27 s</span></div>
      <div class="wide__fact"><b>Best</b><span>10 days after roast (espresso) / 7 (filter). On opening, let the bag air 24 h.</span></div>
    </div>
    <div class="rule"></div>
    <div class="row">
      <span class="tiny">Roasted&nbsp;by&nbsp;Fifty&nbsp;Beans&nbsp;·&nbsp;Brno&nbsp;·&nbsp;200&nbsp;g&nbsp;whole&nbsp;bean</span>
      <span class="tiny">Old&nbsp;Wastewater&nbsp;Treatment&nbsp;Plant&nbsp;·&nbsp;Prague</span>
    </div>
  </div>
</div>'''

def pick(v, theme):
    """Accents for a theme. The sunrise accents are darker so the tiny text still
    passes contrast on a cream ground instead of on ink."""
    return (v["s_accent"], v["s_text"]) if theme == "sunrise" else (v["accent"], v["accent_text"])

def mark_for(v, theme, stroke, cls="emblem"):
    """Sunrise draws the cup in ink with the lot's colour in the bars, so the colour
    lives inside the mark instead of flooding the whole glyph."""
    if theme == "sunrise":
        return emblem("#1A140C", stroke, cls, bar=v["s_accent"])
    return emblem(v["accent"], stroke, cls)

def wide_inner(v, theme="dark"):
    a, at = pick(v, theme)
    return WIDE_INNER.format(emblem=mark_for(v, theme, 9), size=v["wide_size"], pun=v["pun"], bands=bands_html() if theme == "sunrise" else "",
                             accent=a, accent_text=at,
                             process=v["process"], notes=v["notes"], lot=v["lot"], origin=v["origin"])

def wide_label_html(v, theme="dark"):
    return (head(f"Attic Roast — {v['slug']}", 156.56, 129.4, bg=THEMES[theme]["bg"], theme=theme)
            + '<body class="pg">\n' + wide_inner(v, theme) + "\n</body></html>")

def label_inner(v, theme="dark"):
    a, at = pick(v, theme)
    return LABEL_INNER.format(emblem=mark_for(v, theme, 10), size=v["size"], pun=v["pun"], bands=bands_html("4mm") if theme == "sunrise" else "",
                              accent=a, accent_text=at,
                              process=v["process"], notes=v["notes"], lot=v["lot"],
                              origin=v["origin"])

def label_html(v, theme="dark"):
    return (head(f"Attic Roast — {v['slug']}", 70, 100, bg=THEMES[theme]["bg"], theme=theme)
            + '<body class="pg">\n' + label_inner(v, theme) + "\n</body></html>")

def back_inner(theme="dark"):
    m = emblem("#1A140C", 12, bar="#D9411C") if theme == "sunrise" else emblem("#E2542B", 12)
    return BACK_INNER.replace("{emblem_sm}", m).replace("{bands_sm}", bands_html() if theme == "sunrise" else "")

def wide_back_inner(theme="dark"):
    m = emblem("#1A140C", 8, bar="#D9411C") if theme == "sunrise" else emblem("#E2542B", 8)
    return WIDE_BACK_INNER.replace("{emblem_lg}", m).replace("{bands_sm}", bands_html() if theme == "sunrise" else "")

def sheet_html(contents=None, note="", theme="dark"):
    """A4 sheet holding two 157.16 x 130 mm labels, stacked, with crop marks."""
    W,H=157.16,130
    xs=(26.42, 26.42)        # centred: (210-157.16)/2
    ys=(16.0, 150.0)         # clear of the header line and the crop marks
    if contents is None:
        contents=[wide_inner(v, theme) for v in VARIANTS[:2]]
    def mark(x,y,hf,ht,vf,vt):
        return (f'<i class="cr" style="left:{min(hf,ht)}mm;top:{y}mm;width:{abs(ht-hf)}mm;height:0.25mm"></i>'
                f'<i class="cr" style="left:{x}mm;top:{min(vf,vt)}mm;width:0.25mm;height:{abs(vt-vf)}mm"></i>')
    marks=[]
    for (x,y) in zip(xs,ys):
        marks.append(mark(x, y-0.125, x-3, x, y-3.125, y-0.125))
        marks.append(mark(x+W, y-0.125, x+W, x+W+3, y-3.125, y-0.125))
        marks.append(mark(x, y+H, x-3, x, y+H, y+H+3))
        marks.append(mark(x+W, y+H, x+W, x+W+3, y+H, y+H+3))
    bleeds="".join(f'<div class="bleed" style="left:{x-2}mm;top:{y-2}mm;width:{W+4}mm;height:{H+4}mm"></div>'
                   for (x,y) in zip(xs,ys))
    cells="".join(f'<div class="cell" style="left:{x}mm;top:{y}mm;width:{W}mm;height:{H}mm">{c}</div>'
                  for (x,y),c in zip(zip(xs,ys), contents))
    return ('<body class="pg"><div class="sheet">'
            '<div class="sheet__head"><span>Attic Roast &mdash; label sheet</span>'
            '<span>two &times; 157.16 &times; 130 mm &middot; print at 100% &middot; no scaling</span></div>'
            + bleeds + "".join(marks) + cells +
            f'<div class="sheet__note">{note}</div>'
            '</div></body></html>')

def main(theme="dark"):
    OUT = os.path.join(ROOT, THEMES[theme]["out"])
    # wipe stale templates: the back label was dropped from the build, and without
    # this its .html survives in the repo and keeps getting rendered by hand.
    if os.path.isdir(OUT):
        for f in os.listdir(OUT):
            if f.endswith(".html"): os.remove(os.path.join(OUT, f))
    os.makedirs(OUT, exist_ok=True)
    bg = THEMES[theme]["bg"]
    n=0
    for v in VARIANTS:
        open(os.path.join(OUT,f"{v['slug']}.html"),"w").write(wide_label_html(v, theme)); n+=1
        open(os.path.join(OUT,f"{v['slug']}-small.html"),"w").write(label_html(v, theme)); n+=1
    open(os.path.join(OUT,"sticker.html"),"w").write(head("sticker",50,50,bg=bg,theme=theme)+STICKER.format(bands_sm=(bands_html("4mm") if theme == "sunrise" else ""), emblem=mark_for(VARIANTS[0], theme, 11, "emblem emblem--sm"))); n+=1
    open(os.path.join(OUT,"table-card.html"),"w").write(head("card",148,210,bg=bg,theme=theme)+CARD.format(bands=(bands_html() if theme == "sunrise" else ""), emblem=mark_for(VARIANTS[0], theme, 10, "emblem emblem--card"))); n+=1
    open(os.path.join(OUT,"cup-sleeve.html"),"w").write(head("sleeve",230,55,bg=bg,theme=theme)+SLEEVE.format(emblem=mark_for(VARIANTS[0], theme, 11, "emblem emblem--sleeve"))); n+=1
    open(os.path.join(OUT,"sheet-a4-1.html"),"w").write(head("sheet1",210,297,bg=THEMES[theme]["sheet_bg"],theme=theme)+sheet_html([wide_inner(VARIANTS[0],theme),wide_inner(VARIANTS[1],theme)],"Disco Parallel &middot; Private Fizz",theme)); n+=1
    open(os.path.join(OUT,"sheet-a4-2.html"),"w").write(head("sheet2",210,297,bg=THEMES[theme]["sheet_bg"],theme=theme)+sheet_html([wide_inner(VARIANTS[2],theme),wide_inner(VARIANTS[3],theme)],"Proof of Pop &middot; Do Not Crumble",theme)); n+=1
    print(f"  {theme}: wrote {n} templates to {os.path.basename(OUT)}")

if __name__ == "__main__":
    # Dark only by default. The 'sunrise' direction below was built, shown, and rejected:
    # it does not match Fifty Beans' existing shelf labels. The code path is kept so it can
    # be reproduced with `gen_labels.py sunrise` rather than re-invented, but it is not
    # part of the deliverable and build.sh does not generate it.
    which = sys.argv[1:] or ["dark"]
    for t in which:
        main(t)
