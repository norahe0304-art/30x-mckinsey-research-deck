# Image Handoff (to an image generator, e.g. Codex / image-creator)

Decks need: a **cover hero** (always), a **subject image** per subcategory/line/module (if real photos
aren't available), and **optional duotone divider images**. Write a handoff doc the generator can
execute task-by-task, then drop PNGs into `images/` and wire them into the engine by filename.

**What the subject image is, by archetype** (the white-bg / no-shadow spec below is universal):
- *Physical goods* — a product cutout on pure white.
- *Software / SaaS* — a clean UI/dashboard frame, or a single abstract product motif.
- *OSS / service / methodology* — an abstract conceptual hero (architecture motif, geometric form);
  there is no "product" to shoot, so lean on the cover hero + dividers and keep inner pages text-led.

## Global style contract (put at top of every handoff)
- Photorealistic, premium, catalog-grade. No text, no logos, no watermark, no hands, no props.
- Brand palette only (list the exact hexes for this brand — e.g. navy `#051C2C`, plus accent colors).
- **Subject cutouts:** pure white `#FFFFFF` background, **NO shadow, NO reflection**, PNG, square
  (e.g. 1254×1254), subject centered with margin. (Shadows get rejected — the deck blends white-bg
  images with `mix-blend-mode:multiply`; a shadow shows as a gray smudge.)
- **Cover hero:** the ONE image on navy. 2400×1350 (16:9), solid navy bg, subject cluster (products,
  UI frames, or an abstract motif) in the RIGHT ~45%, LEFT ~55% empty navy for the title. Soft
  cinematic light; subtle shadow OK here only.
- **Divider duotone (optional):** navy-monochrome (navy shadows + soft cyan-white `#9CC3E6`
  highlights), object lower-right, rest empty navy, 1600×1600. Quiet, nearly dissolving.

## Per-image task block (repeat)
```
## TASK n — `<filename>.png`  [REQUIRED|OPTIONAL]
- Size: <W>×<H>
- Background: <white #FFFFFF | navy #051C2C>, <shadow: no | mood-only>
Prompt:
```<one vivid paragraph: subject, materials, brand colors, layout, lighting, the no-text/no-shadow rules>```
Accept if: <one-line acceptance test>
```

## Machine-readable manifest (optional, for scripted generation)
End the handoff with a JSON array of `{file, required, w, h, background, shadow, prompt}` so the
generator can loop.

## Wiring returned images into the engine
- Cover: `cover()` uses `product-images/cover-hero.png` as a full-bleed `background:center/cover`,
  text constrained to the left ~55%.
- Subject/line pages: a `HERO` dict maps subcategory/module index → filename; caption from a `CAP` dict.
- Dividers: `divider-01.png … divider-06.png`, placed as an absolutely-positioned `<img>` with a
  left-fade `mask-image` so the square dissolves into the navy (no seam).
- Always verify dimensions after generation: `magick identify -format '%wx%h' <file>`.

## Cleanup of stock/photo cutouts (if a source photo has a shadow)
```bash
magick in.jpg -fuzz 7% -fill white -draw "color 0,0 floodfill" \
              -fuzz 13% -fill white -opaque white -resize 1254x1254 out.png
```
Verify the whiten didn't eat light-colored product areas (cream/sage) before using.
