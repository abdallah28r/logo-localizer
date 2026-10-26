# Moving designed text into Arabic

The general rules for any text that is part of a design: titles, posters,
signs, comic lettering, game art, UI art. For logos and title treatments also
read `logo-localization.md`. Fill `assets/analysis-card.md` from sections 1–3
before generating anything.

## 1. Map the text before translating

- List every text item and give it one class: body/dialogue, caption,
  diegetic (signs, labels, boards), sound effect, title or logo, UI. Classes
  behave differently.
- For each item note its tie to the picture: the object it names, a pun on
  something shown, a colour or symbol, or "none". Translation must keep the
  tie; a title that contradicts the image hides the genre from viewers.
- Decide a strategy per item (Kaindl's taxonomy, widely used for comics):

| Strategy | Meaning | Use when |
|---|---|---|
| keep | leave the source text | woven into the art, foreign on purpose, or a brand kept in Latin |
| replace | redraw it in Arabic | meaning matters; the default for most items |
| gloss | keep the original, add a styled Arabic line nearby | the art must stay intact but readers need the meaning |
| shorten | drop part of it | redundant or no space |
| delete | remove it | trivial repetition only; never text that carries a plot cue |
| reorder | change order or direction | RTL flow or vertical text |

  Map these to the image classification: keep → `KEEP`, replace/shorten/
  reorder → `TRANSLATE`, gloss only if the user asks (it adds a new element).
- Sound effects: keep them near their source and keep their size, because
  size is volume; full redraw reads best for readers.

## 2. Profile the source lettering

Describe what the lettering does, then design Arabic that does the same.
Measure, do not guess (zoom on a letter: crop and enlarge):

1. **Skeleton:** case, structure (block, arched, stacked, slanted), width
   class, bounding-box aspect ratio.
2. **Stroke:** weight, contrast level (none/low/medium/high), the tool it
   suggests (broad nib, pointed pen, brush, geometric), terminals (flat,
   angled, round, pointed, slab), corners (sharp, rounded, broken).
3. **Rhythm:** spacing (tight/airy), counters (open/closed), baseline (flat,
   bouncing, arched), repeated verticals.
4. **Signature features:** the one or two details that make it recognisable:
   a ligature, a notch, a swapped glyph, negative space, an ornament.
5. **Surface:** fill, texture, outline, bevel/3D, shadow, glow, material.
   Record it separately from the skeleton; it is reapplied afterwards.
6. **Voice:** the mood the type expresses on van Leeuwen's features: weight,
   width, slope, roundness, connectivity, regularity.
7. **Strip test:** imagine the ornaments removed. If weak letters remain, the
   identity lives in the ornament and must be rebuilt, not copied.

## 3. Translate the character, not the shapes

- Pick an Arabic style that expresses the same character; never trace a
  Latin skeleton. Starting map (choose and justify):

| Source character | Arabic options | Watch out for |
|---|---|---|
| geometric / tech sans | modern Kufi, low-contrast Neo-Naskh | look-alike letters when over-geometrised |
| condensed tall titling | raised alif/lam, compressed bowls, Kufi with vertical emphasis | closed counters in م ف ق و ه |
| humanist / bookish | Naskh, Neo-Naskh | thin baseline next to heavy Latin stems |
| high-contrast serif, luxury | Naskh or Thuluth with contrast on the horizontals | hairlines vanishing at small size |
| blackletter, metal, dark fantasy | sharp angular Kufi, cut pen ends | dense texture merging teeth (س ش) |
| casual brush, comic | Ruqaa | low risk |
| retro poster | poster Ruqaa (Rakkas/Lalezar lineage) | cascades breaking reading order |
| formal script | plain Diwani | Jali Diwani is hard to read |
| pixel / blocky | square Kufi on the same grid | low legibility; one line, keep dots |
| slab, western, wood type | heavy blunt Kufi or Ruqaa, cut stem ends | Latin serifs added to Arabic |

  Nastaliq reads as Persian; Thuluth and Kufi carry religious associations.
  Check the fit with the product's tone.
- **Contrast runs horizontally in Arabic.** Keep the source's contrast level,
  put the thick strokes on baselines and bowls; copying vertical stress makes
  Arabic look Latinised.
- **Vertical anchors:** share the baseline, align alif/lam to the Latin cap or
  ascender height, and give Arabic its own median heights; never stretch the
  teeth to the Latin x-height.
- **Match colour, not stems:** compare both scripts zoomed out; Arabic looks
  smaller at equal size and its horizontals read heavier.
- **Translate accents:** flat cuts → flat alif/lam tops; angled cuts → angled
  tooth ends; dot shape echoes the detail language (square for blocky,
  diamond for sharp, round only for round). Arabic has no serifs;
  never add Latin ones.
- **Width:** never letter-space Arabic. Use one kashida per word on a joining
  connection, slightly curved, or a swash; get close to the source width, not
  identical.
- **Slant:** no skewed "italic" Arabic; use a style that already leans or a
  weight change, and tell the user it is a judgment call.
- **Dots carry identity:** about 18 base shapes differ only by dots. Keep
  every dot; keep drips, sparks, rivets and particles away from dot zones or
  make them clearly a different shape (the mark table in `visual-review.md`).
- **Effects** go on whole joined groups, never on single letters; give Arabic
  more line height than the Latin source.
- **Digits:** Arabic-Indic (٠١٢) for Mashriq audiences, Western for the
  Maghreb; ask if unsure. Numbers run left to right inside RTL text.
- **Do not mirror** logos, calligraphy, photos, or art with handedness.

## 4. Wording that fits the design

- Titles favour appeal over fidelity; literal when transparent and
  appealing, otherwise adapt while keeping the genre signal.
- Fixed space: shorten at word level, then clause level, then drop
  redundancy; the image carries part of the meaning.
- Offer a safer and a bolder option with a one-line back-translation on the
  translation card; the user decides.

## 5. Check the result

- Every letter joined, right-to-left, every dot present, spelling exact.
- Silhouette, weight, colour and texture match the source side by side at
  the same size, and at the small size it will be seen.
- No Latin letterform smuggled in (D-shaped د, o-shaped و).
- The tie to the picture still holds (back-translate the title).
- The user, as a native reader, gets the final say on readability.

## Sources

Professional: Chahine, "Typefaces have a body and a soul"
(khtt.net/en/page/17606) · 29LT Balenciaga, Balmain, Lanvin, afikra, Zarid
(blog.29lt.com) · TypeTogether multiscript guide (typetogether.com/multiscript-typography-guide)
· Khatt design brief and kashida rules (khtt.net/en/page/1714, /1821) ·
Pentagram Sharjah (pentagram.com/work/sharjah-city-brand) · Rosetta, Arabic
calligraphic styles (rosettatype.com) · Thoughtbot/Chahine on obliques
(thoughtbot.com/blog/do-not-use-obliques-in-arabic) · W3C alreq
(w3.org/TR/alreq) · ITI transcreation code (iti.org.uk) · Blambot lettering
grammar (blambot.com) · Ken Barber interview (lettering-daily.com) · Hische
logotype masterclass (underconsideration.com).
Academic: Nemeth, Harmonization of Arabic and Latin (tntypography.eu) ·
Kaindl via Puspitasari 2022 and Borodo & Wood (intralinea.org) · Zanettin
2014 (intralinea.org/print/article/2079) · Kim 2023 SFX
(intralinea.org/specials/article/2634) · Pavlina et al. 2025 poster cohesion
(jvolsu.com) · van Leeuwen 2006 (opus.lib.uts.edu.au, abstract) · Rohan et
al. 2021 (doras.dcu.ie/26346, abstract) · Benetello 2018 (jostrans.org) ·
Sharkas et al. 2025 title reception (research.uaeu.ac.ae, abstract).
