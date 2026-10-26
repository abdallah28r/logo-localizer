# Visual review is mandatory

No image is approved from numbers. Open the files themselves.

## How to look

- **Native size first** (the decision), then zoomed on glyph edges and mask
  seams (`compare_sheet.py --zoom x0 y0 x1 y1 --zoom-factor 4`).
- **Side by side** with the source, always
  (`compare_sheet.py --source ... --candidate ...`).
- **Transparent assets** on dark, light, and checkerboard (automatic when an
  image has alpha).
- **In context and small:** at the size it will be seen (store tile, app
  icon, thumbnail), not a zoomed crop alone.

## Letter check (every result)

The steps below are written for Arabic, the main target. For another target
script, the same table checks every accent, diacritic, tone mark, and the
stroke count of each character.

Models often drop or merge dots while the word still looks right at a
glance. For each word:

1. Crop the word and enlarge it at least 3× (`compare_sheet.py --zoom ...`).
2. Write a letter table, right to left, from what you **see**, not from the
   intended text: `ا · ل · خ(•1 above) · ل · ا · ي(••2 below) · ا`.
3. Compare it with the approved text letter by letter: count of letters,
   joins, and the number and side of the dots (ب ت ث ن ي ج خ ف ق ش ز ذ ض ظ غ ة).
4. Report every mismatch to the user in the table; never round a missing
   dot up to "fine", and never fix it without the user's request.
5. **Every detached mark is a possible dot until shown otherwise.** Sparks,
   shards, drips, and particles in the letters' color turn letters into
   other letters: a shard above ح reads خ (الساحرة → الساخرة), two or three
   above س read ش, one below ح reads ج, a short slanted stroke reads as a
   haraka or hamza. The letter table above lists only letters, so it misses
   them; do this as a separate pass:
   - On the zoomed crop of each word, find every detached blob near the
     letters (sparks, shards, drips, particles) and give each a number,
     right to left.
   - Write a mark table with one row per number:
     `# · over/under which letter · real dot of the text? · if read as a dot,
     the word becomes … · decision`. The fourth column is the test: read the
     word as if the mark were a dot (or haraka) on the nearest letter.
   - If that reading is a different word or letter, the mark must go: move
     it clear of the letter's dot zone (not above or below any letter that
     can take dots), make it clearly not a dot (much smaller, a long streak,
     a different color), or remove it. "It looks like a spark to me" is not
     a pass; a reader who meets the word cold decides.
   - Check marks touching a letter (spurs, flame tips) the same way.
   Unless the approved text includes harakat, the word must read the same
   whether each mark is taken as a dot or not.

Put both tables (letters and marks) in the final reply so the user can
check them too.

## The transparent layer

Look at the chosen layer (`out/logo_N.png`) on dark, light and checkerboard
(the comparison sheet does this for images with alpha) and report:

- missing parts (a letter, a dot, an emblem cut off at the edge of the
  layer) or extra parts (a backdrop, a panel, a piece of scene);
- stains, specks or a pale or dark halo around the letters;
- glow or shadow that became a solid block instead of staying soft.

On the placed version, also report where the logo looks pasted on: light,
sparks or objects that passed in front of the old logo now sit behind it.

## Background inside the region

A mask allows change, it does not prove the change was wanted. After the
clean plate:

1. Zoom the region side by side (`compare_sheet.py --zoom ...`) and
   look at every spot where the old letters stood: the rebuilt background must
   be plain continuation of the surface. Invented graffiti, numbers, letters,
   faces, symbols, or a partly hidden mark that was completed into something
   new (a "9:49" that became "940") must be reported to the user, with the
   fix you would suggest (a stricter `remove-text` prompt or a smaller mask).
2. Say in the final reply what was rebuilt behind the old letters.

## Report to the user when

- Text is wrong: spelling, missing or extra dots, disconnected letters,
  reversed order, wrong word, glossary mismatch, mangled digits or Latin.
- Placement, baseline, perspective, weight, color, opacity, spacing, or style
  distorts the source or clashes with nearby elements. (In `localize`, size
  alone is a suggestion to the user, not an error.)
- A phrase's place, lines or lockup differs from `sentence_map`, a word's
  place, size, line or look differs from `word_map` in `job.json` (check each
  phrase, then its words, then their letters).
- A letter's colour or style differs from `letter_map` in `job.json` (check
  each letter against its `#hex` on the zoomed crop; repeated letters keep
  one colour).
- An outline, shadow, glow, panel, decoration, or glyph was invented.
- Source text remains, the background is blurred or repeated, a seam shows,
  or any subject, face, lighting, composition, or transparency changed.
- It passes the numbers but looks worse.

## Checks are by eye

No script judges the result. Check by eye: residual source text, clipping,
exact text and spelling, every dot and detached mark, transparency, and
native format.

## What to tell the user

No review records are written (the comparison sheets in `review/` are enough).
In the final reply give, in a line each: what was
checked and why the result passes, which directions were rejected and why,
and anything still uncertain. Say "opened and checked" only for images you
actually opened in this session.
