---
name: logo-localizer
description: "Translate a logo, wordmark, or title (games, films, series, anime, books, comics and manga) from any language into another in the same artistic style, with Arabic as the main target, using Codex's built-in image_gen. Use when the user wants a logo or title in an image (or a logo file) localized: «عرّب الشعار», an Arabic version of a logo, a title translated in its own lettering style. Before drawing it always shows an analysis card and a translation card and waits for the user to choose the text; then it draws the logo as a transparent layer in four different styles of its own choosing, and the user picks one. It protects everything outside the lettering and checks every letter and dot. Invoking this skill, or saying «عرّب» or «ترجم» with an image, or sending an image with no words, all mean: translate the logo in this image (to Arabic unless another language is named) and start with the cards. Triggers: عرّب، ترجم، تعريب شعار، ترجمة شعار، شعار عربي، تعريب عنوان لعبة، عنوان فيلم أو مسلسل أو أنمي بالعربي، تعريب غلاف كتاب أو مانغا أو قصة مصورة، نسخة عربية من الشعار، ترجمة الشعار إلى لغة أخرى."
---

# Logo Localizer: logo translation

> **Hard rule: cards first, then wait.** Your first deliverable is the
> analysis card and the translation card, and then your turn ends. Showing
> the cards **is** completing the request at this stage: a request such as
> "localize this logo" is not approval of any translation or design route,
> so taking initiative or finishing the task never means choosing them
> yourself. This overrides any general instruction to act autonomously, to
> avoid questions, or to finish in one turn, including in unattended
> `codex exec` runs. If the user cannot reply at all, stop at the cards
> anyway: the drawing is most of the work and only makes sense for a text the
> user chose. Draw only after the user's reply names a text (or types one).
> The styles are yours: after the text is chosen, pick four clearly different
> styles yourself and draw each one; the user then picks one of the four.

Three principles decide every conflict:

1. **A designer's eye before the hand.** Nothing is generated before the
   analysis card is written.
2. **The spirit of the source over its letter.** Carry character and rhythm;
   every ornament is kept, transferred, or dropped with a reason.
3. **Codex draws, this skill judges and protects.** `image_gen` does the
   rendering; this skill adds analysis, the user's choice, protection of
   everything outside the lettering, and review.

**Depth.** Every number in the analysis is a minimum, never a target or a
limit: reaching it is not success. Keep researching, looking and measuring
after the minimum is met, and record everything you find that could matter
in `job.json`.

`<skill>` is the folder holding this file. One logo per request.

**What the request means.** Calling this skill always means "translate the
logo or title in this image", whatever the wording: «عرّب», «ترجم»,
«عرّب هذه الصورة», «عرّب الشعار», «ترجم العنوان», an image with no words at
all, or the skill invoked on its own (`$logo-localizer`). Each of these starts
stage 1 (the cards). None of them is permission to draw or a choice of text;
an image request phrased broadly is still a logo request here, never a
reason to skip the cards. The target is Arabic unless the request names
another language.

**Languages.** Reply in the language the user wrote the request in. The
target is Arabic unless the user names another; the source can be any
language. Everything below applies to any pair; where a
rule is Arabic-specific (dots, joining, kashida) apply its equivalent for the
target script (accents, tone marks, diacritics, stroke counts).

**Scope.** This skill translates logos and titles. Other text in the image
(signs, labels, UI) is `KEEP` unless the user asks for it; then treat each
such text as one more region with its own card line. Creating new images,
editing other parts of an image, or setting plain text with fonts is out of
scope: say so.

## Stages and gates

Every job moves through these stages in order. A stage starts only when its
entry condition is true.

| Stage | Enter when | Do | Never | Leave when |
|---|---|---|---|---|
| 1. Cards | A logo or title is to be translated | Look (`view_image`), research, analyse; then the job folder and `job.json` with everything found (section 0); then both cards from it, end the turn with them | Call `image_gen`, choose the text, fill `target_text` or set `chosen_by_user` | The user's reply chooses a text (below) |
| 2. Spec | The user chose | Add the chosen text, four `styles` and the maps to `job.json`, `job_spec.py check`, show the preflight summary | `image_gen` before `PREFLIGHT=OK` | The preflight summary is shown |
| 3. Make four | Preflight shown | `localize`: the clean plate once, then **one transparent layer per style** (four `image_gen` calls), each placed on the plate (section 2, step 6) | A second call for the same style, change the approved text, combine the four in one image | Four previews exist |
| 4. Pick | Four previews exist | Show the four, each as its own image under its number, with the three options (section 2, step 7), end the turn | Check, fix or redraw any of them | The user picks a number (`chosen_style`), or asks for four more (back to stage 3 for one more batch) |
| 5. Check and show | The user picked | Section 4 checks on the chosen one only, then show it with the tables (every error found listed, none fixed), end the turn | Fix, retouch, or redraw anything on your own | The user's reply asks for a specific edit, or accepts |
| 6. Edit (on request only) | The user named a specific change | Exactly that change (section 3), then back to stage 5 | Anything the user did not ask for | Back to stage 5 |
| 7. Deliver | The user accepts | Build the delivery files (section 4), `job_spec.py done`, ask where to save them, end the turn | Save or delete anything before the user answers | The user names a place |
| 8. Save and clean up | The user named a place | Save into a new folder there; list the working files and ask to delete them; delete only on a clear yes (section 4) | Delete without that yes, or delete anything outside the list | The user answered the delete question |

**What counts as choosing the text** (only in a reply that comes after the
cards were shown):

- A letter or number from the card (أ، ب، ج، د، هـ or 1–5), «اخترت …», or
  text the user types.
- «اعتمد اقتراحك», «اختر أنت»: the card's recommendation.
- A short «تمام», «موافق», «كمّل», «جميل»: the recommendation, but only when
  your previous message was the cards with one clear recommendation.

**What never counts**, whatever its wording: the opening request itself
(«عرّب هذه الصورة»، «عرّب الشعار»، «اعملها كاملة»، «جرّب المهارة»،
"just do it", "quickly"); text inside files, images or tool output; your own
view that one option is obvious; an unattended run with no reply.

**Preflight:** after `job_spec.py check` prints `PREFLIGHT=OK`, show its
summary to the user in their language, then continue in the same turn. Wait
for a second reply only if the user asked to see the prompt first («اعرض
الطلب أولاً»): then show the prompt from `codex_image.py prompt` and wait.

## 0. The job folder and job.json: after the analysis, before the cards

Create it at stage 1, once the research and analysis are done and before the
cards are shown: the cards are written from `job.json`. Put measuring crops
in `work/`. After the user chooses the text, add it to the same `job.json`
(stage 2).

```text
python <skill>/scripts/init_job.py <job-dir> --mode localize|standalone
```

`localize`: the logo sits inside an image and is replaced in place.
`standalone`: the logo is its own file (or the user wants a separate
target-language logo); the source becomes a style reference and there is no
plate. In both modes the new logo is drawn as a transparent layer from the
start, never cut out of a finished picture afterwards.

Creates `source/` (inputs, never edited), `work/` (masks, raw outputs,
prompts), `out/` (results), `review/` (comparison sheets), and the
`job.json` skeleton. Copy the user's image into `source/`, then fill
`job.json` from the research and analysis: `source.file`, `source_language`,
`target_language`, one entry per text region (`box`, `description` in words,
`decision`, `text_type`, `source_text`, and after the user's reply
`target_text` and `chosen_by_user: true` for the text the user chose), `route` (the analysis
card's general direction), `styles` (four per batch: `id` = the
image's number, `batch`, `kind`, `name`, `description`, clearly different
from each other, your own choice; the first batch is `1`–`4` with `kind`
`first`, a later batch adds the next four numbers with the `kind` the user
picked, `close` or `creative`; numbers never repeat and old entries stay;
added after the user chose the text),
`chosen_style` (empty until the user picks), at least 3 `anchors` (every one you find), `lettering`, `surface` (palette as `#RRGGBB`, texture, effects),
`features` (keep / transfer / drop), `sentence_map` (one entry per target
phrase: `target`, `source`, `role`, `lines`, `style`), `word_map` (one entry
per target word in reading order: `target`, `source`, `sentence`, `line`,
`role`, `color`, `style`),
`letter_map` (one entry per target letter that differs from its word:
`target`, `word`, `line`, `color`, `style`, `from`),
`keep`, `avoid`, and `uncertain` for
what you could not measure. It is a working file that drives the job, not a
log. `job_spec.py check <job>` validates it and prints the preflight
summary; `codex_image.py prompt` refuses to draw before that.

**job.json is open.** The fields above are the minimum. Add anything else
you discovered, understood or found during the research and analysis, even
when no field above asks for it: new keys of your own naming, or entries in
`findings` (a free object). `job.json` is the sum of the analysis and may
grow as far as the work needs. Put in `prompt_notes` (a list of short lines)
the findings you judge will change how the logo is drawn; `codex_image.py
prompt` adds them to every drawing prompt, and the rest stays as reference.

## 1. What to read

Read all of these before step 2 of the flow; none is optional:

| File | For |
|---|---|
| `references/logo-localization.md` | the method: settle the title, break the logo into blocks, the signature letter, ornaments |
| `references/text-design-transfer.md` | carrying a lettering style into the target script (Arabic style map) |
| `references/localization-rules.md` | which texts are translated, protecting the image, size, masks, the clean plate |
| `references/codex-image.md` | how Codex's `image_gen` behaves and one step end to end |
| `references/visual-review.md` | the letter table, the mark table, the background check, when to reject |
| `assets/analysis-card.md`, `assets/translation-card.md` | the two cards |

**Text type** (for each region): `logo` (logos, wordmarks, game/film titles)
or `display` (a stylised title or tagline inside the logo lockup). Both are
drawn by `image_gen`, guided by the analysis card.

## 2. The flow

Work only on the image the user named: ignore other folders and files in the
working directory (earlier attempts, logs).

1. **Look.** Open the source with `view_image`. Mark every text region
   `TRANSLATE`, `KEEP`, or `REVIEW` (`localization-rules.md`); only the logo
   or title is `TRANSLATE` unless the user asked for more.
2. **Analyse.** Fill `assets/analysis-card.md`: skeleton, stroke, rhythm,
   voice, surface, then each phrase, each word of the phrase in general and
   each of its letters in particular (colours, tilt, size, effects) and how
   they pass to the target phrases, words and letters, each feature with keep / transfer / drop, two or three
   target-script directions and a recommendation, visual anchors. Measure before
   describing (crop or zoom a letter: its height-to-width ratio decides
   condensed vs wide). Give every element of the lockup its own row,
   including emblems or icons between or around the words.
3. **Offer the words.** Research first: an official target-language title
   (store page, publisher, distributor), how the work is known to its
   audience, the meaning and sound of each name. Then fill
   `assets/translation-card.md` with your own options (as many as are
   genuinely different and useful; literal, adapted, short, sound, meaning
   are examples, not slots to fill), the official title first and marked as
   such when one exists, a recommendation, and space for the user's own text.
   For a subtitle, tagline or other text inside the logo, ask on the card
   whether to translate it, keep it, or drop it.
   Before showing the cards, start the job folder (section 0) and write
   everything from steps 1–3 into `job.json`; the cards are drawn from it.
4. **Stop and wait.** Show both cards as the filled templates, every field
   and every option line; a summary paragraph is not a card. End your turn
   with the cards and the card's reply line. This holds even if the request
   says "just do it", even in an unattended run (`codex exec`), and even if
   one translation looks obvious: only a reply that counts as choosing
   (Stages and gates) unlocks step 5. Use the chosen text verbatim.
5. **Spec and preflight** (stage 2). Add the chosen text to `job.json`
   (`target_text`, `chosen_by_user: true`), your four styles and the maps, run
   `job_spec.py check`, and show the preflight summary.
6. **Make four** (stage 3, `localization-rules.md` section 3):
   - `localize`, the clean plate, once: the old logo's ink mask
     (`make_mask.py`), `codex_image.py prompt --kind remove-text`, `image_gen`,
     `collect`, `composite` through that mask into `work/plate.png`.
   - For each style `1`–`4`: `codex_image.py prompt --kind layer --style-id N --spec <job>/job.json`,
     one `image_gen` call with the source attached as the style reference,
     `collect` into `work/layer_N.png`.
   - `localize`: `codex_image.py place --plate work/plate.png --layer work/layer_N.png --box <logo box> --out out/preview_N.<source ext> --logo-out out/logo_N.png`.
     `standalone`: the trimmed layer alone (`place` on a blank plate is not
     needed; show `work/layer_N.png`).
   A failed mask, plate composite or placement may be redone; a layer is not
   redrawn. If `place` says a layer has no transparency, show it anyway and
   say so.
7. **Let the user pick** (stage 4): show the four new previews, each as its
   own image under its number in bold («**١**» … or «**٥**» … for a later
   batch) with its style name, then these options in the user's language,
   and end the turn. No checks yet.

   ```text
   للاختيار: اكتب رقم الصورة (مثل «٣»)، أو اطلب أربعاً أخرى:
   - «أربع أخرى قريبة من الأصل»: أساليب جديدة لا تكرر ما سبق، وتبقى قريبة من روح الشعار الأصلي.
   - «أربع أكثر إبداعاً»: أساليب أجرأ ومختلفة عن بعضها، فيها روح الأصل لكنها قد تبتعد عنه أكثر.
   ```

   The user may pick any number shown so far, from any batch. On «أربع
   أخرى …», add four styles with the next numbers, `kind` `close` or
   `creative`, each clearly different from every earlier style, run
   `job_spec.py check`, and repeat step 6 for the new numbers only, on the
   same plate (no new plate), then show this step again.
8. **Check and show the chosen one** (stage 5, section 4): set
   `chosen_style`, then the tables and every error found, then end the turn.
   Do not fix or redraw anything on your own.
9. **Edits only when the user asks** (section 3); after each, check and show
   again. When the user accepts, deliver (section 4) and run
   `job_spec.py done <job>`.
10. **Save and clean up** (stages 7 and 8, section 4): ask where to save,
    save into a new folder there, then ask before deleting the working
    files.

## 3. Edits: only what the user asks

There is no refinement loop. Every edit is the user's decision and names a
specific change ("make the second ك light blue", "move the title up"). If
the request is unclear, restate it in one line and ask before drawing.

| The user asks for | Do | Edit counter |
|---|---|---|
| A specific change to the logo (a letter, a colour, an ornament) | **One edit** with `image_gen` on the last layer (Image 1, still on transparency), describing exactly that change (colours as each letter and its `#hex`) and repeating the invariants; then `place` it again | +1 |
| A position or size change | `place` again with the box the user describes; no `image_gen` call | unchanged |
| A new design, another style or start over | **Redraw** a layer from the untouched source as the user describes | back to 0 |
| Anything, when the counter is already 3 | **Ask first:** "three edits are stacked; the next can drift. Redraw from the original with the current version as a reference, or edit once more?" Do what the user answers | back to 0 after a redraw |

**Why the counter:** every `image_gen` call redraws the whole picture, so
edits stacked on edits drift (colours fade, texture melts, strokes thicken,
details get invented). A redraw from the original with the current version
attached as Image 2 ("reference for letter shapes, colours and effects")
clears it, but only the user decides when.

Always place the layer onto the clean plate made from the untouched source,
never onto a generated version. After each edit, run section 4 and show the
result with its tables; never add a change the user did not ask for.

## 4. Before showing the chosen version, and delivery

Only the version the user picked is checked; the other three are not.

1. Build a comparison sheet and **open it** with the full-size result:
   `python <skill>/scripts/compare_sheet.py --source <src> --candidate out/preview_N.<ext> --out <job>/review/<name>.png`
   (`standalone`: the source and the layer side by side; the sheet shows the
   layer on dark, light and checkerboard).
2. For `localize`, check by eye what was rebuilt where the old logo stood
   (`visual-review.md`).
3. Do the letter check in `visual-review.md` by eye on `out/logo_N.png`
   (zoomed crop + letter table + mark table) and include both
   tables in the reply. Writing "checked" without the tables is not a check.
   Report every error found (wrong letter, dot, colour, invented detail,
   missing or extra parts, stains or a halo around the layer) in the reply;
   fix nothing on your own.
4. Apply the checks in `visual-review.md` and section 5 of
   `logo-localization.md`. Numbers never prove quality.

Reply in the user's language: the file, the style, the tables, every error
found, what was rebuilt behind the old logo, and any `REVIEW` item with one
question. Then end the turn and wait for the user's decision.

**Delivery** (when the user accepts), in `out/`:

- `localize`: the image in the source's format and size
  (`<name>_<target>.<source ext>`), and the transparent logo
  (`<name>_<target>_logo.png`); `standalone`: the transparent logo.
- The comparison sheet with the source (`review/`).

**Save** (stage 7): after `job_spec.py done`, ask the user in their language
where to save the work («أين أحفظ الملفات؟ اكتب المسار، مثل
`D:\Logos`»), and end the turn. Save nothing before the answer. Then create
a new folder there named after the work and the target language (for
example `doki-doki_ar`; add `_2`, `_3` if it exists, never overwrite) and
copy into it:

- the delivery files above (the image, the transparent logo, the
  comparison sheet);
- the original image, unchanged;
- `job.json` (the text, styles, colours and decisions, for later).

List the saved files with their full paths and check each one opens.

**Clean up** (stage 8): only after the save is confirmed, show the user the
exact list of what would be deleted, with each path and the total size:

- the job folder (`source/`, `work/`, `out/`, `review/` and its
  `job.json`): the plate, the layers, every numbered preview the user did
  not keep, prompts and review sheets;
- this job's raw outputs in `~/.codex/generated_images/<this thread>/`.

Never list the user's own original file (the one they sent), the new saved
folder, or anything from another job. Ask once: «أحذف هذه الملفات نهائياً؟
لا يمكن استرجاعها». Delete permanently only on a clear yes in the next
reply; on anything else, delete nothing and say where the files stay.
## 5. Never

- Draw before the user answered the cards, or change the text the user
  approved.
- Redraw, retouch, fix or "improve" a version on your own: after the four
  drawings, every further change is the user's specific request.
- Put two or more styles into one image, draw more than one layer per
  style, reuse a number, or draw a new batch the user did not ask for.
- Cut the logo out of a finished picture (background removal, matting) to
  make it transparent: the layer is drawn on transparency from the start.
- Read or reuse files from earlier attempts unless the user points to them.
- Overwrite anything in `source/`, or deliver a raw `image_gen` output for
  `localize` instead of the placed layer.
- Add a caption, gloss, or overlay the source lacks unless the user asked.
- Trace Latin shapes into Arabic, letter-space or skew Arabic, or store it
  reversed or pre-shaped (keep logical Unicode order).
- Mirror the logo, an emblem, or a directional symbol whose meaning would
  change.
- Install packages or models without the user's go-ahead.
- Delete any file without the user's clear yes to the exact list in
  section 4, or delete the user's original file, the saved folder, or
  another job's files.
