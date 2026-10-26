# Analysis card (template)

Fill this before drawing the logo or title. Show it to the user as the filled block
below, every field present; never replace it with a prose summary. Use `text-design-transfer.md` sections 1–3,
plus `logo-localization.md` for logos. Write the card in the user's
language and show it together with the translation card; keep it under 55
lines. Measure where you can; say "unclear" rather than guess.

The card is a view of `job.json`, written after the research and before the
card: `job.json` holds the whole analysis, the card shows what matters most
when the analysis is longer than the card.

**Depth.** Every number in the analysis is a minimum, never a target or a
limit: reaching it is not success. Keep researching, looking and measuring
after the minimum is met, and record everything you find that could matter.

```text
التصميم: <what it is and where it is used>
نوع النص: شعار | عرض     الاستراتيجية: replace | shorten | reorder | keep

الهيكل:   <case, structure, width class, aspect ratio e.g. 5:1>
الخط:     <weight, contrast level + tool, terminals, corners>
الإيقاع:  <spacing, counters, baseline, repeated verticals, slant>
الصوت:    <mood: at least 3 words, as many as are true: e.g. heavy, rough, western…>
السطح:    <fill, texture, outline, bevel/3D, shadow, glow, colours>

تحليل النص (الشعار ← كل جملة ← كل كلمة ← كل حرف):
الجملة 1: «<source phrase>» — الدور: <main title / subtitle / tagline> · الموضع والأسطر: <where, how many lines> · الحجم: <share of the logo>
  عام: <the phrase's lockup: stacking, alignment, direction, overall colour scheme, shared effects>
  العلاقة: <how it sits against the other phrases and emblems>
  الكلمة 1: «<source word>» — السطر <n> · الحجم: <share of the phrase>
    عام: <the word's colour(s), tilt, baseline, overlap, outline, shadow, texture, spacing>
    | الحرف | اللون | النمط الخاص: ميل، حجم، إزاحة، حد، ظل، ملمس |
    | <e.g. D> | <#FE8081> | <tilted −8°, raised, dark rose 3D edge> |
  الكلمة 2: «...» — (same levels)
الجملة 2: «...» — (same levels)
قاعدة النقل: جمل: <which target phrase takes which source phrase's place, lines and lockup> · كلمات: <which target word takes which source word's place, size and look> · حروف: <by reading order / by letter identity (repeated letters keep one colour) / one look for all / a repeating pattern>

المميزات:
| الميزة | القرار | السبب |
| <e.g. bullet holes in letters> | أبقِ / انقل → <Arabic letter or part> / احذف | <why> |

الاتجاه (بخط لغة الهدف): <the general direction for the target script>
الأساليب: أربعة أساليب مختلفة أختارها بعد اختيارك للنص، وأرسم كلاً منها في صورة مستقلة لتختار منها
الحرف المميِّز: <which Arabic letter carries the signature gesture, if any>
المراسي البصرية: <at least 3 things that must not be lost for the result to read as this logo; list every one you find>
مخاطر القراءة: <dots near effects, closed counters, stacking, cultural load>
```

Rules for filling it:

- The direction and the four styles are your decision: the card informs
  the user, it does not ask them to choose a style before the drawings.
- Judge conflicts in this order: readable correct Arabic > character and
  rhythm of the source > fidelity of ornaments.
- Every ornament and every non-text element of the lockup (an emblem
  between the words, a sparkle, an underline, a frame) gets its own row and
  decision; dropping one silently is a mistake.
- Measure before describing: zoom on one letter; height ≥ 2× width means
  condensed/tall, close to 1× normal, below wide. State the number.
- Analyse from the whole to the part: the logo (the fields above), then each
  phrase (a title, a subtitle, a tagline: its role, place, lines and lockup),
  then each word of that phrase in general (line, size, colours, tilt,
  effects, its relation to the other words), then each letter of that word in
  particular. Write a
  letter row only for letters that differ from their word (colour, tilt,
  size, offset, outline, texture); when every letter shares the word's look,
  write «كل الحروف مثل الكلمة». Colours are `#RRGGBB` sampled from the face,
  not the edge or shadow. A subtitle in its own style is a word block too,
  even when it stays untranslated. Then state the transfer rule for phrases,
  words and letters. Reading order flips between LTR and RTL
  scripts: the first source letter maps to the first target letter in reading
  order (the rightmost Arabic letter), and a repeated source letter (the two
  O's) keeps its colour on its counterpart. Say what you will do
  when the target has more or fewer letters (continue the cycle, merge, or
  give the extra letter the colour of its neighbour in the source).
- Anchors are what most decides likeness (silhouette, proportions, signature
  stroke, surface, a key ornament), written as visible facts; they go first
  in every prompt.
- Name an Arabic structure for every transferred feature (which letter,
  which stroke), not "similar style".
- Write `job.json` from the research and analysis before showing the card
  (route, anchors, lettering, surface, features, and anything else you found,
  SKILL.md section 0). After the user chooses the text, add it to `job.json`
  with the four styles, `sentence_map` (one entry per target phrase),
  `word_map` (one entry per target word) and `letter_map` (one entry per
  target letter): the transfer rules applied to the chosen text.
  `codex_image.py prompt --spec` repeats its key lines in every prompt.
