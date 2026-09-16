import os,sys,json,base64,urllib.request,urllib.error
KEY=os.environ["VKEY"]
OUT="/home/vpavlin/dark-prague-coffee/art"
JOBS=[
 ("hero-plant","flux-2-pro",1344,768,
  "Cinematic wide photograph inside a vast 1906 Art Nouveau industrial wastewater treatment plant: cast-iron arches, riveted pipes, brick and oxidised metal, monumental machinery. Dark and moody, deep near-black shadows, single shaft of warm bone-white light from a high window, faint steam. No people. Muted desaturated palette of charcoal, bone and sage green, one small ember-orange glow. Editorial, high detail, 35mm, no text."),
 ("beans-macro","flux-2-pro",1024,1024,
  "Extreme macro photograph of dark-roasted coffee beans scattered on a matte black steel surface, dramatic low-key lighting, single ember-orange rim light, deep shadows, glossy bean oils, shallow depth of field. Minimal, editorial, high detail. No text."),
 ("emblem-stamp","recraft-v4-pro",1024,1024,
  "Flat monochrome emblem on solid black background, single bone-white line: a simple coffee cup seen from the side, its three ribbons of steam drawn as a network topology graph with round nodes and straight connecting edges. Minimal geometric vector logo, thick even strokes, centered, generous margins, no text, no shading, screenprint look."),
 ("pattern","recraft-v4-pro",1024,1024,
  "Seamless repeating pattern, flat vector, bone-white and sage-grey thin line art on near-black: alternating coffee beans and small network graph nodes connected by straight lines. Even spacing, tileable, minimal, technical blueprint feel, no text."),
 ("attic-scene","flux-2-pro",1344,768,
  "Documentary photograph: people gathered around a long table drinking coffee inside a raw Art Nouveau industrial hall with cast-iron columns and pipes, laptop and notebooks, warm ember pendant light, dark charcoal shadows, candid conversation, muted film palette, no text, no logos."),
 ("bag-mockup","nano-banana-pro",1024,1024,
  "Product photograph of a matte black 250 gram coffee bag standing on rough concrete in dim industrial light, blank label area, subtle ember-orange edge light, dark moody background with out-of-focus pipes. Minimal, premium, no text on the bag."),
]
def gen(name,model,w,h,prompt):
    body=json.dumps({"model":model,"prompt":prompt,"width":w,"height":h,
                     "format":"png","safe_mode":False,"hide_watermark":True}).encode()
    req=urllib.request.Request("https://api.venice.ai/api/v1/image/generate",data=body,
        headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    try:
        r=json.load(urllib.request.urlopen(req,timeout=300))
    except urllib.error.HTTPError as e:
        print(f"  !! {name}: HTTP {e.code} {e.read()[:300].decode(errors='replace')}"); return False
    imgs=r.get("images") or []
    if not imgs: print(f"  !! {name}: no images"); return False
    p=f"{OUT}/{name}.png"; open(p,"wb").write(base64.b64decode(imgs[0]))
    print(f"  ok {name}: {os.path.getsize(p)//1024} KB ({model} {w}x{h})"); return True
for name,model,w,h,prompt in JOBS:
    print(f"-> {name}")
    gen(name,model,w,h,prompt)
