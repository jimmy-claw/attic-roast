# Attic Roast — branding

Coffee branding for the **Attic Roast** coffee session at **Dark Prague 2026**
(Old Wastewater Treatment Plant, Prague). Beans by **Fifty Beans**, Brno.

**No company appears on this artwork.** The room at Dark Prague is the Attic, so the
coffee is named for the room, not for a vendor. Privacy, parallel infrastructure and
the city carry the design instead. If you are editing this, keep it that way.

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
| bag label (four lots) | 157.16 × 130 mm — matches Fifty Beans' own label |
| small bag label | 70 × 100 mm |
| back label | 157.16 × 130 mm |
| round sticker | 50 mm Ø |
| table card | A5, 148 × 210 mm |
| cup sleeve | 230 × 55 mm |
| A4 label sheet | 210 × 297 mm, two labels + crop marks + 2 mm bleed |

## The mark

A cup with a **keyhole** stamped on its body — one line, no fills. The stamp is not a
logo: private-by-default is the point, so the mark says privacy rather than saying a
name. The cup is drawn by its edge alone (no rim stroke; the silhouette does that work).

## Colour

Ink `#0C0C0D` · bone `#F4F3EC` · sage `#A7AFA9`, plus one accent per lot:
ember `#E2542B`, rose `#E85D9E`, amber `#F2A93B`, grape `#8B5CF6`.
For print, convert to CMYK and proof the accents; ink is rich black.
