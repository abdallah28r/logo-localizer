# Logo Localizer

**[العربية](README.ar.md)**

A skill for [Codex](https://github.com/openai/codex) that translates logos and titles of games, films,
series, anime, books and comics from any language into another **in the same artistic style**. Arabic is
the main target.

It draws with Codex's built-in image tool (`image_gen`). It needs no API key and no server, and its
Python helpers run locally.

## What it does

1. **Reads the logo.** It analyses the logo from the whole down to each letter: structure, weight,
   rhythm, surface and ornaments, then every phrase, word and letter with its colour as a `#hex` code.
2. **Offers the words.** It researches the title first, including an official translation if one
   exists. Then it gives you its own translation options and a recommendation, and asks about any
   subtitle or tagline.
3. **Stops and waits.** Nothing is drawn before you choose or type the text.
4. **Draws four versions.** It removes the old logo from the image (a clean plate). Then it draws the
   new logo **on a transparent background** in four different styles, one image each, and places each
   one where the old logo was. The images are numbered 1–4.
5. **You pick, or ask for more.** Reply with a number, or ask for four more:
   - close to the original's spirit;
   - or more inventive, which may move further from the original.

   Numbers run on (5–8, 9–12…) and never repeat.
6. **Checks the one you picked.** It reports every wrong letter, dot, colour or invented detail in
   letter and mark tables. It fixes nothing on its own: every edit is your request.
7. **Delivers and tidies up.** It delivers three files:
   - the image in the original's format and size;
   - the logo alone with a transparent background;
   - a comparison sheet with the original.

   It asks where to save them, creates a new folder there, and deletes the working files only if you
   say yes.

## Requirements

- Codex with the built-in `image_gen` tool.
- Python 3.10 or newer, with Pillow and numpy:

  ```bash
  python -m pip install -r requirements.txt
  ```

## Installing

1. Copy the `logo-localizer` folder into your Codex skills folder:
   - Windows: `%USERPROFILE%\.codex\skills\logo-localizer`
   - macOS and Linux: `~/.codex/skills/logo-localizer`
2. Install the requirements, as shown above.
3. Restart Codex.

## Using it

Attach an image and write any of these:

- «عرّب الشعار في هذه الصورة»
- "Localize this logo into Arabic"
- "Translate this game's logo into French"
- or call the skill alone: `$logo-localizer`

The target language is Arabic unless you name another. One logo per request.

## Files

```text
logo-localizer/
├── SKILL.md                 the rules and the stages Codex follows
├── agents/openai.yaml       the skill's name and default prompt in Codex
├── assets/                  the analysis card and the translation card
├── references/              the method: logo analysis, Arabic lettering, checks
├── scripts/
│   ├── init_job.py          creates the job folder and job.json
│   ├── job_spec.py          checks job.json; no drawing before you chose the text
│   ├── codex_image.py       builds the drawing prompt, collects the result, makes the plate, places the logo
│   ├── make_mask.py         the old logo's mask for the clean plate
│   ├── compare_sheet.py     the comparison sheet
│   └── _common.py           shared helpers
└── tests/                   python -m unittest discover -s tests
```

## Limits

- The checks are done by eye, by the model and by you. No script proves the letters are right.
- Every drawing uses your Codex usage limit, about a minute per image.
- If the image tool cannot rebuild the background behind the old logo, the result is reported to you
  and nothing is fixed silently.

## Rights

This skill is a tool. You are responsible for having the right to translate, use and publish any logo
you run through it. Logos and titles belong to their owners.

## License

[MIT](LICENSE) © 2026 [abdallah28r](https://github.com/abdallah28r).
