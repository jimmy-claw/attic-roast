# Attic Roast — branding

Coffee branding for the **Attic Roast** coffee session at **Dark Prague 2026**
(Old Wastewater Treatment Plant, Prague). Beans by **Fifty Beans**, Brno.

**No company appears on this artwork.** The room at Dark Prague is the Attic, so the
coffee is named for the room, not for a vendor. Privacy, parallel infrastructure and
the city carry the design instead. If you are editing this, keep it that way.

## A direction that was rejected

A light, colourful "sunrise" variant was built and shown (cream ground, colour inside the
mark, a full-bleed band of five parallel stripes along the bottom of every piece). **Václav
rejected it: "it looks pretty terrible — does not match the existing ones at all."** Fifty
Beans' own shelf labels are what this sits next to, and matching them matters more than the
idea. So the deliverable is the dark direction only, and `build.sh` builds only that.

The code path remains (`THEMES` in `gen_labels.py`, `python3 gen_labels.py sunrise`) so it can
be reproduced rather than re-invented, but nothing in `site/` ships it.

What we learned from the attempt, worth keeping: reading a rendered PNG for pixels is the
only reliable check — three attempts at verifying that band from the markup all said "fine"
while it was wrong on the page.

## Build

```bash
./build.sh          # templates -> print PDFs -> previews -> zip, all in one go
```

Everything in `site/` is generated. Edit `gen_labels.py` (artwork) or `site/index.html`
(the site), then re-run `build.sh` — never hand-edit anything under `site/labels/`,
`site/downloads/` or the preview images.

## What's here

- `gen_labels.py` — the label family. Single source for every printed piece.
- `render.sh` — one piece: headless Chromium -> ghostscript (exact page box) -> 300 dpi PNG.
- `build.sh` — all 14 pieces, previews, and the zip.
- `site/index.html` — the presentation site.
- `site/attic-roast-print-kit.zip` — everything, for the roaster.

## Pieces

| piece | size |
|---|---|
| bag label (four lots) | **156.56 × 129.40 mm** — revised 25/09, 0.3 mm off each side |
| small bag label | 70 × 100 mm |
| back label | dropped — front only |
| round sticker | 50 mm Ø |
| table card | A5, 148 × 210 mm |
| cup sleeve | 230 × 55 mm |
| A4 label sheet | 210 × 297 mm, two labels + crop marks + 2 mm bleed |

## The mark

A cup with **two parallel bars** stamped on its body — one line, no fills. Not a logo,
and not a lock: a keyhole was tried first and read as a padlock. The bars say
**parallel** — parallel society, parallel infrastructure — with a nod to `//`.
The cup is drawn by its edge alone (no rim stroke; the silhouette does that work).

## Colour

Ink `#0C0C0D` · bone `#F4F3EC` · sage `#A7AFA9`, plus one accent per lot:
ember `#E2542B`, rose `#E85D9E`, amber `#F2A93B`, grape `#8B5CF6`.
For print, convert to CMYK and proof the accents; ink is rich black.
