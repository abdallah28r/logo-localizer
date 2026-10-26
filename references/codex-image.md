# Using Codex's built-in image_gen

The single owner of engine mechanics. For tool behaviour, input handling, and
prompt craft follow Codex's own `imagegen` skill; for exploring creative
directions follow `art-direct-imagegen`. This file adds only what
logo-localizer needs on top of them.

## Facts observed on this machine

- `image_gen` returns the **whole image**, usually **upscaled with the same
  aspect ratio** (a 640×320 source came back 1774×887), and it changes the
  background slightly everywhere. It has **no mask**.
- Outputs land in `~/.codex/generated_images/<thread>/...png`. Copy them into
  the job before using them; never leave a deliverable only there.
- To edit a file on disk, open it with `view_image` first so it is in the
  conversation, then call `image_gen`. Label every image by index and role
  (`Image 1: edit target`, `Image 2: style reference`).
- A call takes about a minute. On a machine low on memory Codex can crash
  (`memory allocation ... failed`); retry once, then tell the user.

## One step, end to end

1. Write the prompt with `codex_image.py prompt --spec <job>/job.json` (it
   follows the imagegen schema: use case, input images, visual anchors first,
   verbatim text, lettering and surface, ornaments, a core rule for what stays
   the original, constraints, avoid). Redrawn text (`localize-text`, `logo`)
   needs the spec after `job_spec.py check`; the text comes only from it.
   `--style` or `--design-notes` add to it. Save it with
   `--out work/prompt_n.txt`.
2. Call `image_gen` with that prompt and the images it names.
3. `codex_image.py collect --out <job>/work/raw_n.png --prompt-file work/prompt_n.txt`
   copies the newest output into the job (never overwrites) and saves a
   small note with the prompt, so a good result can be reproduced.
4. **Clean plate** (`--kind remove-text`): make the old logo's ink mask
   (`make_mask.py`, `localization-rules.md` section 4) and
   `codex_image.py composite --source ... --generated work/raw_plate.png --mask work/old_logo.png --out work/plate.png`.
   This scales the output back to the source size and takes only the masked
   pixels. A `warning` about the aspect ratio means check the region closely.
5. **Layer** (`--kind layer --style-id N`): the prompt asks for the logo
   alone on a transparent background, in that style, with the original
   logo's proportions. `codex_image.py place --plate work/plate.png --layer work/layer_N.png --box ... --out out/preview_N.<ext> --logo-out out/logo_N.png`
   fits it into the old logo's box. `place` refuses a layer without real
   transparency: show it to the user and say so, do not redraw it unasked.
   `standalone`: no plate and no `place`; the layer is the result.
6. Review (`visual-review.md`), show the version with its tables, and wait
   for the user's decision (SKILL.md sections 3 and 4).

## Prompting notes that matter for text

- Put the exact text once, in `Text (verbatim)`; for Arabic the prompt asks
  for connected letters, every dot, Arabic-Indic digits and `٪`. Still check
  every letter: the probe kept the Latin `%` once.
- Describe the region in words ("the large title in the upper middle"),
  since there is no mask; the composite enforces the boundary afterwards.
- For a layer, say "fully transparent background" and forbid any backdrop,
  panel or checkerboard; the prompt from `--kind layer` already does.
- Name the lettering structure, not only the colour: "condensed heavy sans,
  tall narrow letters" stops the model from drifting to a rounded face.
- Attach the source logo or a cropped sample as a style reference when the
  lettering is distinctive; say which features to carry over.
- Change one thing per retry and repeat the invariants each time.

## Edits and drift

Every `image_gen` call redraws the whole picture, even when asked to change
one letter, so edits stacked on generated versions drift. Edit the chosen
layer itself (still on transparency), then `place` it again; a move or resize
needs only `place`. Edits happen only
when the user asks (SKILL.md section 3). After three stacked edits, ask the
user whether to redraw from the untouched source with the current version
attached as a reference ("Image 2: reference for letter shapes, colours and
effects").
For a colour fix, name each letter and its exact `#hex` and say that shapes,
dots, shadows and texture stay as they are.
