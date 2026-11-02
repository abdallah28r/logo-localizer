# Logo Localizer

**English** · [العربية](README.ar.md)

Translate the logo or title of a game, film, series, anime, book or comic into another language **while keeping its artistic style**. Arabic is the main target, and other languages work too.

Logo Localizer is a skill for [Codex](https://github.com/openai/codex), OpenAI's coding agent. You attach an image, choose the wording, and Codex draws four versions for you to pick from.

## How it works

1. **Attach an image** and ask for a translation.
2. **Confirm your permission.** Codex asks whether you own the logo or have the rights holder's permission. If you answer no, it stops.
3. **Read the analysis.** Codex studies the logo and researches the title, including any official translation.
4. **Choose the text.** Nothing is drawn until you pick an option or type your own.
5. **Pick a design.** You get four numbered versions. Choose one, or ask for four more.
6. **Check the letters.** Codex lists every wrong letter, dot or colour in the version you picked. It changes only what you ask it to.
7. **Get your files:**
   - the image in its original format and size
   - the logo alone on a transparent background
   - a side-by-side comparison with the original

## Installation

**You need:** the [Codex CLI or app](https://developers.openai.com/codex) with its built-in `image_gen` tool, and [Python 3.11 or newer](https://www.python.org/downloads/).

**Step 1.** Ask Codex to install the skill. Paste this into Codex:

```text
Use $skill-installer to install the skill at the root of the GitHub repo abdallah28r/logo-localizer, with --path . and --name logo-localizer.
```

Or install it yourself with Git:

```bash
git clone https://github.com/abdallah28r/logo-localizer.git ~/.codex/skills/logo-localizer
```

On Windows PowerShell:

```powershell
git clone https://github.com/abdallah28r/logo-localizer.git "$HOME\.codex\skills\logo-localizer"
```

**Step 2.** Install the two Python libraries:

```bash
python -m pip install -r ~/.codex/skills/logo-localizer/requirements.txt
```

On Windows PowerShell:

```powershell
python -m pip install -r "$HOME\.codex\skills\logo-localizer\requirements.txt"
```

**Step 3.** Restart Codex.

If Codex does not list the skill, move the folder to `~/.agents/skills/logo-localizer`, the user location in the [Codex skills docs](https://developers.openai.com/codex/skills).

## Usage

Attach an image and write something like:

- `Localize this logo into Arabic`
- `Translate this game's logo into French`
- `عرّب الشعار في هذه الصورة`
- `$logo-localizer` on its own

The target language is Arabic unless you name another. Each request handles one logo.

## Good to know

- **Your images go to OpenAI.** The Python scripts run on your computer and collect nothing, but Codex sends your image and text to OpenAI to draw and search the web. [OpenAI's terms](https://openai.com/policies/row-terms-of-use/) and privacy policy apply.
- **Check the result yourself.** The letter checks are done by eye, by the model and by you. No script proves the spelling is correct.
- **It uses your Codex limit.** Each drawing takes about a minute and counts against your usage.
- **Backgrounds can go wrong.** If the area behind the old logo cannot be rebuilt cleanly, Codex tells you and leaves the decision to you.

## Responsible use

**Use this tool only on logos you own or have permission to translate and use.** Logos and titles belong to their owners, and this tool gives you no rights to them. Translating, altering or publishing a logo may need permission even if you do not charge for it. Fan work is not automatically exempt, and the rules differ by country.

**You are responsible for how you use this tool.** The authors do not control what you process or publish, do not check your permission, and, as far as the law allows, accept no liability for your use of the tool or its results. Your answer to the permission question is your own statement. See the [MIT License](LICENSE) for the full terms.

- Do not present a result as official, or use it to impersonate a brand, person, government or organization.
- Do not use it to remove watermarks or credits.
- Follow the [OpenAI terms](https://openai.com/policies/row-terms-of-use/), which make you responsible for your input and output. They also forbid presenting AI output as made by a human when it was not.

Rights holders can [open an issue](https://github.com/abdallah28r/logo-localizer/issues) about this project. It hosts no third-party logos, and images you process are not sent to this repository.

## For developers

Run the tests from the project folder:

```bash
python -m unittest discover -s tests
```

| Path | Purpose |
|---|---|
| `SKILL.md` | The rules and stages Codex follows |
| `agents/openai.yaml` | The skill's display name and default prompt |
| `assets/` | The analysis card and translation card templates |
| `references/` | The method, with its published sources listed at the end of each file |
| `scripts/` | Local helpers for job files, masks, placement and comparison sheets |
| `tests/` | Unit tests |

## Credits and license

- This project uses [Pillow](https://github.com/python-pillow/Pillow) (MIT-CMU) and [NumPy](https://github.com/numpy/numpy) (BSD-3-Clause). pip installs them, and neither is bundled here.
- Its prompts use the field labels of OpenAI's `imagegen` skill (Apache-2.0) so that Codex can read them. No files from that skill are included.
- This is an independent project, not affiliated with or endorsed by OpenAI. Codex is a product of OpenAI. Other names mentioned in this repository belong to their owners.

Released under the [MIT License](LICENSE). The license covers this software only, not the logos you process or the images you create with it. The software comes with no warranty.
