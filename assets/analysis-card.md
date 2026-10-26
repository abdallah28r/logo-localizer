# Analysis card (template)

Fill this from `job.json` after the research and analysis gate (SKILL.md)
passed: the research stays in `job.json` and the card does not repeat it.
Show it to the user as the filled block below, every field present; never
replace it with a prose summary. Write it in the user's language and show it
before the translation card. Keep it under 55 lines: when the analysis is
longer, fold letter rows into «كل الحروف مثل الكلمة» and give each field its
shortest true form; the full detail stays in `job.json`. Measure where you
can; say "unclear" rather than guess. The depth rule (SKILL.md) applies:
every number below is a minimum.

```text
التصميم: <what it is and where it is used>
المعنى والوظيفة: <what the logo says about the work and how its design expresses it>
المحيط: <what surrounds or touches the logo (background, frame, box, emblem, effects) and how it changes the reading>
نوع النص: شعار | عرض     الاستراتيجية: replace | shorten | reorder | keep

الهيكل:   <case, structure, width class, aspect ratio e.g. 5:1>
الخط:     <weight, contrast level + tool, terminals, corners>
الإيقاع:  <spacing, counters, baseline, repeated verticals, slant>
الصوت:    <mood: at least 3 words, as many as are true: e.g. heavy, rough, western…>
السطح:    <fill, texture, outline, bevel/3D, shadow, glow, colours>
الإضاءة:  <light direction, highlights, glow, reflections, and the effects they create>

تحليل النص (الشعار ← كل جملة ← كل كلمة ← كل حرف):
الجملة 1: «<source phrase>» — الدور: <main title / subtitle / tagline> · الموضع والأسطر: <where, how many lines> · الحجم: <share of the logo>
  عام: <the phrase's lockup: stacking, alignment, direction, overall colour scheme, shared effects>
  العلاقة: <how it sits against the other phrases and emblems; overlaps, spacing, direction>
  المعنى والوظيفة: <what this phrase says and does in the logo>
  الكلمة 1: «<source word>» — السطر <n> · الحجم: <share of the phrase>
    عام: <the word's colour(s), tilt, baseline, overlap, outline, shadow, texture, spacing>
    الجوار: <letters, shapes, effects or emblems touching or near the word, and how they change its reading, shape and transfer>
    | الحرف | اللون | النمط الخاص: ميل، حجم، إزاحة، حد، ظل، ملمس | الجوار وأثره |
    | <e.g. D> | <#FE8081> | <tilted −8°, raised, dark rose 3D edge> | <overlaps the O; the star touches its top; keep a gap for the Arabic dot> |
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
- Measure before describing: zoom on one letter and divide its height by
  its width: 2 or more is condensed/tall, 1.2–2 normal-tall, 0.8–1.2 normal,
  under 0.8 wide. State the number.
- At every level apply the whole-to-part analysis with neighbours
  (`text-design-transfer.md` section 2, item 8).
- Analyse from the whole to the part: the logo (the fields above), then each
  phrase (a title, a subtitle, a tagline: its role, place, lines and lockup),
  then each word of that phrase in general (line, size, colours, tilt,
  effects, its relation to the other words), then each letter of that word in
  particular. Write a
  letter row only for letters that differ from their word (colour, tilt,
  size, offset, outline, texture); when every letter shares the word's look,
  write «كل الحروف مثل الكلمة». Colours are `#RRGGBB` read from a zoomed
  crop of the letter's face, not the edge or shadow; write "unclear" when you
  cannot read one. A subtitle in its own style is a word block too, even
  when it stays untranslated.
- **Transfer rule** for phrases, words and letters. Reading order flips
  between LTR and RTL scripts: the first source letter maps to the first
  target letter in reading order (the rightmost Arabic letter), and a
  repeated source letter keeps its colour on its counterpart. Example: DOKI
  → دوكي gives D's colour to د, O's to و, K's to ك, I's to ي. Say what you
  will do when the target has more or fewer letters (continue the cycle,
  merge, or give the extra letter the colour of its neighbour in the
  source).
- Anchors are what most decides likeness (silhouette, proportions, signature
  stroke, surface, a key ornament), written as visible facts; they go first
  in every prompt.
- Name an Arabic structure for every transferred feature (which letter,
  which stroke), not "similar style".
- `job.json` holds all of this and more, and gains the chosen text, the
  styles and the maps at stage 2 (SKILL.md section 0); `codex_image.py
  prompt --spec` repeats its key lines in every prompt.
