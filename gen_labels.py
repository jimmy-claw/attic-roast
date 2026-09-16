#!/usr/bin/env python3
"""Generate the Attic Roast label family.

Coffee = Fifty Beans (Brno). The three labels are the REAL lineup (special/funky
lots), so the copy matches the beans: variety, process, producer, notes.
Our job is the branding, not the coffee identity.

Brand note: this is deliberately NOT branded as any company. The room at Dark
Prague is the Attic, so the coffee is "Attic Roast" — privacy, parallel
infrastructure, and the city. No vendor name appears anywhere on the artwork.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "labels")

def emblem(color="#E2542B", stroke=10, cls="emblem"):
    """Attic Roast mark: a cup with a keyhole stamped on its body.
    No rim line on top (it read as a stray stroke); the body edge IS the rim.
    The stamp is a keyhole, not a logo: private-by-default is the point."""
    return f'''<svg class="{cls}" viewBox="0 0 200 200" fill="none" aria-label="Attic Roast" style="color:{color}">
<g fill="none" stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">
<path d="M42 112 H140 L128 164 a14 14 0 0 1 -13 13 H67 a14 14 0 0 1 -13 -13 Z"/>
<path d="M140 126 a25 25 0 0 1 0 38"/>
</g>
<g fill="currentColor"><circle cx="91" cy="139" r="11"/><path d="M85.6 147.5 h10.8 l-3.4 17.5 h-4 z"/></g>
</svg>'''

def head(title, wmm, hmm, bg="#0C0C0D", extra=""):
    # Chromium rounds @page sizes to whole POINTS (157.16mm -> 156.97mm), so we render on a
    # page 1.5mm larger, anchor the piece to the BOTTOM-LEFT, and let ghostscript crop the
    # extra (gs -dFIXEDMEDIA keeps the bottom-left of the larger page). Result: exact trim,
    # no white hairline at the edge.
    wpt, hpt = round((wmm+1.5)/25.4*72, 3), round((hmm+1.5)/25.4*72, 3)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>
@page{{size:{wpt}pt {hpt}pt;margin:0}}
html,body{{margin:0;padding:0}}
body.pg{{position:relative;width:{wmm+1.5}mm;height:{hmm+1.5}mm;background:{bg};overflow:hidden}}
body.pg > *{{position:absolute;left:0;bottom:0}}
</style>
<link rel="stylesheet" href="label.css">{extra}</head>
'''

# ── the special coffees (Fifty Beans, Brno) ───────────────────────────────────
# All four: Edinson Argote, Colombia · enzymatic fermentation · espresso & filter · 499 Kč
VARIANTS = [
 dict(slug="disco-parallel", wide_size="40pt", pun="Disco<br>Parallel", size="36pt",
      accent="#E2542B", accent_text="#F4794E",
      process="Enzymatic fermentation",
      notes="Blackberry candy · Cherries · Herbs",
      lot="Disco Candy",
      origin="Ombligon · Edinson Argote, Colombia"),
 dict(slug="private-fizz", wide_size="40pt", pun="Private<br>Fizz", size="40pt",
      accent="#E85D9E", accent_text="#F58BB6",
      process="Enzymatic fermentation",
      notes="Rose water · Raspberry soda · Florals",
      lot="Rose Fizz",
      origin="Typica Mejorado · Edinson Argote, Colombia"),
 dict(slug="proof-of-pop", wide_size="40pt", pun="Proof<br>of Pop", size="38pt",
      accent="#8B5CF6", accent_text="#A98BFF",
      process="Enzymatic fermentation",
      notes="Raspberry cake · Stone fruit",
      lot="Crazy Pop",
      origin="Caturra Chiroso · Edinson Argote, Colombia"),
 dict(slug="do-not-crumble", wide_size="40pt", pun="Do Not<br>Crumble", size="33pt",
      accent="#F2A93B", accent_text="#F7C46B",
      process="Enzymatic fermentation",
      notes="Vanilla · Cherries · Disco",
      lot="Vanilla Crumble",
      origin="Colombia & Ethiopia"),
]

KICKER = "Attic&nbsp;Roast&nbsp;×&nbsp;Dark&nbsp;Prague&nbsp;2026"
KICKER_SHORT = "Attic&nbsp;Roast&nbsp;×&nbsp;Dark&nbsp;Prague"

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
        250&nbsp;g&nbsp;·&nbsp;Whole&nbsp;bean<br>Roasted&nbsp;by&nbsp;Fifty&nbsp;Beans&nbsp;·&nbsp;Brno
      </div>
    </div>
    <div class="rule"></div>
    <div class="row">
      <span class="tiny">Old&nbsp;Wastewater&nbsp;Treatment&nbsp;Plant&nbsp;·&nbsp;Prague</span>
      <span class="tiny">Espresso&nbsp;&amp;&nbsp;filter</span>
    </div>
  </div>
</div>'''

def wide_inner(v):
    return WIDE_INNER.format(emblem=emblem(v["accent"], 9), size=v["wide_size"], pun=v["pun"],
                             accent=v["accent"], accent_text=v["accent_text"],
                             process=v["process"], notes=v["notes"], lot=v["lot"], origin=v["origin"])

def wide_label_html(v):
    return head(f"Attic Roast — {v['slug']}", 157.16, 130) + '<body class="pg">\n' + wide_inner(v) + "\n</body></html>"

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
      <span class="tiny">250&nbsp;g&nbsp;·&nbsp;Whole&nbsp;bean</span>
      <span class="tiny">Fifty&nbsp;Beans&nbsp;·&nbsp;Brno</span>
    </div>
  </div>
</div>'''

def label_inner(v):
    return LABEL_INNER.format(emblem=emblem(v["accent"], 10), size=v["size"], pun=v["pun"],
                              accent=v["accent"], accent_text=v["accent_text"],
                              process=v["process"], notes=v["notes"], lot=v["lot"],
                              origin=v["origin"])

def label_html(v):
    return head(f"Attic Roast — {v['slug']}", 70, 100) + '<body class="pg">\n' + label_inner(v) + "\n</body></html>"

BACK_INNER = '''<div class="label">
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
</div>'''

def back_inner():
    return BACK_INNER.replace("{emblem_sm}", emblem("#E2542B", 12))

STICKER = '''<body class="pg">
<div class="sticker" style="--accent:#E2542B">
  <div style="color:var(--ember)">{emblem}</div>
  <div class="display" style="font-size:11pt;margin-top:1.6mm">Attic&nbsp;Roast</div>
  <div style="width:22mm;height:.3mm;background:var(--accent);margin:1.8mm 0"></div>
  <div class="mono" style="font-size:5pt;letter-spacing:.14em;color:var(--sage);text-transform:uppercase">Dark Prague 2026<br>Coffee</div>
</div>
</body></html>
'''

CARD = '''<body class="pg">
<div class="card">
  <img class="bg" src="../assets/img/hero-plant.jpg" alt="">
  <div class="veil"></div>
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
      <span class="tiny">Roasted&nbsp;by&nbsp;Fifty&nbsp;Beans&nbsp;·&nbsp;Brno&nbsp;·&nbsp;250&nbsp;g&nbsp;whole&nbsp;bean</span>
      <span class="tiny">Old&nbsp;Wastewater&nbsp;Treatment&nbsp;Plant&nbsp;·&nbsp;Prague</span>
    </div>
  </div>
</div>'''

def wide_back_inner():
    return WIDE_BACK_INNER.replace("{emblem_lg}", emblem("#E2542B", 8))

def sheet_html(contents=None, note=""):
    """A4 sheet holding two 157.16 x 130 mm labels, stacked, with crop marks."""
    W,H=157.16,130
    xs=(26.42, 26.42)        # centred: (210-157.16)/2
    ys=(16.0, 150.0)          # clear of the header line and the crop marks
    if contents is None:
        contents=[wide_inner(v) for v in VARIANTS[:2]]
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

def main():
    os.makedirs(OUT, exist_ok=True)
    n=0
    for v in VARIANTS:
        open(os.path.join(OUT,f"{v['slug']}.html"),"w").write(wide_label_html(v)); n+=1
        open(os.path.join(OUT,f"{v['slug']}-small.html"),"w").write(label_html(v)); n+=1
    open(os.path.join(OUT,"back.html"),"w").write(head("back",157.16,130)+'<body class="pg">\n'+back_inner()+"\n</body></html>"); n+=1
    open(os.path.join(OUT,"sticker.html"),"w").write(head("sticker",50,50)+STICKER.format(emblem=emblem("#E2542B", 11, "emblem emblem--sm"))); n+=1
    open(os.path.join(OUT,"table-card.html"),"w").write(head("card",148,210)+CARD.format(emblem=emblem("#E2542B", 10, "emblem emblem--card"))); n+=1
    open(os.path.join(OUT,"cup-sleeve.html"),"w").write(head("sleeve",230,55)+SLEEVE.format(emblem=emblem("#E2542B", 11, "emblem emblem--sleeve"))); n+=1
    open(os.path.join(OUT,"sheet-a4-1.html"),"w").write(head("sheet1",210,297,bg="#F4F3EC")+sheet_html([wide_inner(VARIANTS[0]),wide_inner(VARIANTS[1])],"Disco Parallel &middot; Private Fizz")); n+=1
    open(os.path.join(OUT,"sheet-a4-2.html"),"w").write(head("sheet2",210,297,bg="#F4F3EC")+sheet_html([wide_inner(VARIANTS[2]),wide_back_inner()],"Do Not Crumble &middot; back")); n+=1
    print(f"wrote {n} templates to {OUT}")

if __name__ == "__main__":
    main()
