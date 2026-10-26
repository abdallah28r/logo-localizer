# Translating a logo inside an image

The strict rule set for `localize` (the logo sits in an image and is replaced
in place). `standalone` jobs use sections 1 and 2 only.

## 1. Classify every text region first

- `TRANSLATE`: the logo or title the user asked for, and any other text the
  user named.
- `KEEP`: everything else by default: signs, labels, UI, text on clothing,
  products or packaging, signatures, incidental scenery, illegible
  microtext; a brand name the user wants kept in its original script.
- `REVIEW`: function unclear, context missing, or decorative in one place and
  critical in another. Ask one question per `REVIEW` item.

A standalone name plate is `TRANSLATE` when its spelling is approved and it
fits the design; this never extends to names in clothing, logos, or
decoration. Critical text may override a `KEEP` category only if it can be
replaced inside the same design without distortion. Never add a subtitle,
tooltip, caption, legend, or overlay that the source lacks.

Use only approved spellings for names and terms (the user's glossary, the
product's existing translation, or `job.json`). Unknown meaning or an
unapproved name becomes `REVIEW`, never a guess.

## 2. Preserve the source style

Note only the properties that affect the edit: fill, outline (width or none),
shadow (or none), glow (or none), opacity, font character, weight, spacing,
alignment, baseline, rotation, perspective, texture, blending. **Absence is a
property:** no outline in the source means no outline in the target. Never
flatten a textured or perspective label, and never fix contrast with an
invented panel, stroke, shadow, or glow; if the new text cannot stay readable
without one, keep the source.

**Lettering:** how to read the source lettering and carry its character
into the target script is in `text-design-transfer.md` and
`logo-localization.md`; never swap in a stock font look.

**Size priority:** readable correct text > intact artwork > source
typography > approximate scale > occupancy numbers. Visible-ink bounds are evidence, not
a target to maximize; keep intentional empty space. If the text looks small,
try size, weight, line spacing, alignment, line breaks, and safe layout
inside the design (in that spirit, not that order). Never resize the whole
image, stretch or squeeze glyphs non-uniformly, add effects, or move text
outside. Stop enlarging when the next step hurts balance; a slightly smaller
balanced result beats exact width with distorted letters. Arabic has no
letter-spacing: never track Arabic apart (it breaks joining).

**On overflow** (text does not fit the space), in this order: shorter
natural wording (offer it on the translation card), slight size change, safe
line breaks, safe container change, then a smaller size. These size rules
apply to every mode; other files point here instead of repeating them.

The final size is judged by eye on the comparison sheet; `place` fits the
new logo inside the old logo's box.

**Reusing old candidates:** a prior approval does not
carry over. Check how the lettering was made; if glyphs were resampled only to
fill the source width, compare at native size against the pristine source and
a natural-proportion alternative, and replace only a visually worse result.

## 3. Routes

One route: **the logo is a transparent layer from the start.**

1. **Clean plate** (`localize` only, once): remove the whole old logo
   (lettering and the emblems or badge that belong to it) with
   `--kind remove-text`, composited through the old logo's ink mask
   (section 4) into `work/plate.png`.
2. **Four layers:** one `image_gen` call per style in `job.json`
   (`--kind layer --style-id N`), each drawing the complete target-language
   logo (lettering plus its own emblems, badge and ornaments) alone on a
   transparent background, with the source attached as the style reference.
   Never cut a logo out of a finished picture to make it transparent: tests
   of background removal and of alpha from a redrawn picture both left
   missing or extra parts and stains.
3. **Place:** `codex_image.py place` trims each layer to its visible pixels
   and fits it inside the old logo's box (same place, about the same size,
   proportions kept, centred), over the plate. It also writes the trimmed
   transparent logo.
4. **Pick, then check:** the user picks a numbered preview, or asks for four
   more (close to the original, or more inventive) with the next numbers on
   the same plate; only the picked
   one is checked (SKILL.md sections 3 and 4). If the result is worse than
   the untouched source, say so and let the user decide.

A layer that lies flat over the picture can look pasted on (light, sparks or
objects that pass in front of the old logo). Report it on the chosen version;
do not fix it unasked.

## 4. Redrawing text with image_gen

`image_gen` has no mask and changes the whole image slightly, so:

- Describe only the decided region and the exact approved text; the model
  may not reclassify or widen the region (`codex-image.md` for the prompt).
- Always `codex_image.py composite` the plate onto the untouched source
  through the mask, and reject it if fidelity cannot be restored.
- **Clean plate mask:** the old logo's ink only, never the whole box:
  `make_mask.py <src> --box ... --ink --grow N --out work/old_logo.png`.
  When the box holds other contrasting detail (graffiti, signs, props), pick
  the logo by its own colours from `job.json`'s palette:
  `make_mask.py <src> --box ... --ink-color <fill> --ink-color <outline/shadow> --grow N --out work/old_logo.png`.
  Composite the `remove-text` result through it: outside the mask the plate
  keeps the source's pixels. What lay hidden behind the old logo is rebuilt
  by `image_gen`; check it by eye (`visual-review.md`).
- Check AI-written Arabic letter by letter: wrong letters, missing dots,
  disconnected or reversed letters, Latin `%` instead of `٪`, or extra words
  must be reported to the user.

## 5. Checks

Before delivering, open the comparison sheet (`compare_sheet.py --source ...
--candidate ...`) and look (`visual-review.md`). In the final reply, list each
region with its decision (`TRANSLATE`, `KEEP`, `REVIEW`) so the user sees
what was left untouched.
