"""Helpers around Codex's built-in image_gen tool: write the prompt, collect the output, composite it.

  prompt     print a ready image_gen prompt (Codex imagegen schema) for one job step
  collect    copy the newest image_gen output from ~/.codex/generated_images into the job
  composite  put an edited result back onto the untouched source through the mask
  place      put a transparent logo layer onto the clean plate, in the old logo's box

image_gen has no mask: it returns the whole image (often upscaled, same
aspect ratio) with small changes everywhere. In localize/edit always
`composite` the result onto the source so only the decided region changes.

The logo itself is drawn as a transparent layer (`--kind layer`, one call per
style in job.json, numbered 1, 2, 3... across batches), never extracted from a finished picture afterwards. The
clean plate (`--kind remove-text`, composited through the old logo's ink)
takes the old logo out; `place` fits the layer into the old logo's box.

Redrawing text (`localize-text`, `logo`, `layer`) needs --spec <job>/job.json
after `job_spec.py check` passed: the text, region, anchors and style come
from it, and designed text the user did not choose is refused.

Examples:
  python codex_image.py prompt --kind layer --style-id 1 --spec jobs/doki/job.json --out jobs/doki/work/prompt_1.txt
  python codex_image.py collect --out work/layer_1.png
  python codex_image.py composite --source source/x.png --generated work/raw_plate.png --mask work/old_logo.png --out work/plate.png
  python codex_image.py place --plate work/plate.png --layer work/layer_1.png --box 120 40 520 300 --out out/preview_1.png --logo-out out/logo_1.png
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ARABIC_RE, parse_box, print_json, sha256, utf8_stdio, write_json  # noqa: E402
import job_spec  # noqa: E402

from PIL import Image, ImageChops, ImageFilter  # noqa: E402

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
ARABIC_TEXT_RULE = ("Write it right to left in correctly connected Arabic letter forms, every dot and hamza "
                    "in place, Arabic-Indic digits and the Arabic percent sign ٪ when the text uses them; "
                    "spell it exactly as given, no extra words or marks.")
OTHER_TEXT_RULE = ("Spell it exactly as given in its own script, with every accent, diacritic and tone mark; "
                   "no extra words or marks.")

KINDS = {
    "localize-text": ("text-localization",
                      "Replace only the lettering of {region} with the exact text below, in the same lettering "
                      "style. Keep placement, size, baseline, perspective, fill, outline, shadow, texture and "
                      "effects as in the original, including their absence."),
    "logo": ("text-localization",
             "Redraw the logo/title in {region} in {language} with the exact text below, keeping the logo's "
             "character, rhythm, weight and effects as described below. Treat it as custom lettering, not a "
             "font swap."),
    "remove-text": ("precise-object-edit",
                    "Remove the logo in {region} (its lettering and any emblem, badge or ornament that belongs to "
                    "it) and rebuild the surface behind it so it continues naturally. Add no text, letters, "
                    "numbers, logos, faces, symbols or new graffiti. Where a background mark (graffiti, a sign, a "
                    "number) was partly hidden by the logo, leave it cut off and fill the hidden part with plain "
                    "surrounding surface; never complete it."),
    "layer": ("logo-brand",
              "Draw the {language} version of the logo in {region} of Image 1 as a standalone logo on a fully "
              "transparent background (PNG with alpha), with the exact text below. Only the logo: its "
              "lettering and the emblems, badge and ornaments that belong to it; no scene, no backdrop, no "
              "panel, no frame or box that the original logo lacks. Glow and shadow that belong to the logo "
              "stay soft and semi-transparent. Treat it as custom lettering, not a font swap."),
}
STANDALONE = ("Create a standalone {language} version of the logo in Image 1 with the exact text below, on a plain "
              "background, keeping its character, rhythm, weight, surface and effects. Treat it as custom "
              "lettering, not a font swap.")
LANGUAGES = {"ar": "Arabic", "en": "English", "fr": "French", "es": "Spanish", "de": "German", "fa": "Persian",
             "ur": "Urdu", "tr": "Turkish", "ja": "Japanese", "zh": "Chinese", "ko": "Korean"}


TEXT_KINDS = ("localize-text", "logo", "layer")


BATCH_RULES = {
    "close": ("This is an extra batch close to the original: keep the original logo's spirit, mood, palette and "
              "character; find new letterforms and treatments."),
    "creative": ("This is an extra, more inventive batch: keep the original logo's spirit and its key emblems, but "
                 "be bolder and move further from its exact look; make it clearly different from the other styles "
                 "of this batch."),
}


def pick_style(spec: dict, style_id: str | None) -> dict:
    """The style a layer prompt is built for (one numbered style in job.json)."""
    styles = {str(s.get("id")): s for s in spec.get("styles") or []}
    if style_id not in styles:
        raise SystemExit(f"ERROR --style-id must be one of {', '.join(map(str, styles)) or 'the styles in job.json'}")
    return styles[style_id]


def apply_spec(args) -> dict | None:
    """Fill the text arguments from job.json; refuse redrawn text without a passed preflight."""
    if not args.spec:
        if args.kind in TEXT_KINDS:
            raise SystemExit("ERROR redrawing text needs --spec <job>/job.json (after job_spec.py check)")
        return None
    spec = job_spec.load(args.spec)
    region = job_spec.require_ready(spec, args.region_id) if args.kind in TEXT_KINDS else None
    if region:
        if args.target_text and args.target_text != region.get("target_text"):
            raise SystemExit("ERROR --target-text differs from the approved text in job.json")
        args.target_text = region.get("target_text")
        args.source_text = args.source_text or region.get("source_text")
        args.region = args.region or region.get("description")
    lettering = {k: v for k, v in (spec.get("lettering") or {}).items() if v}
    surface = spec.get("surface") or {}
    style = [f"{k}: {v}" for k, v in lettering.items()]
    if surface.get("texture"):
        style.append(f"surface: {surface['texture']}")
    if surface.get("palette"):
        style.append("palette: " + ", ".join(surface["palette"]))
    if surface.get("effects"):
        style.append("effects: " + "; ".join(surface["effects"]))
    if style and not args.style:
        args.style = "; ".join(style)
    args.keep = (args.keep or []) + list(spec.get("keep") or [])
    args.avoid = (args.avoid or []) + list(spec.get("avoid") or [])
    return spec


def build_prompt(args) -> str:
    spec = apply_spec(args)
    use_case, template = KINDS[args.kind]
    if args.kind in TEXT_KINDS and not args.target_text:
        raise SystemExit("ERROR this kind needs the approved text (from job.json)")
    region = args.region or "the text area"
    code = (spec or {}).get("target_language") or "ar"
    language = LANGUAGES.get(code.lower(), code)
    layer = args.kind == "layer"
    standalone = (bool(spec) and spec.get("mode") == "standalone" and args.kind == "logo") or layer
    if standalone and not layer:
        template = STANDALONE
    lines = [f"Use case: {use_case}"]
    if args.asset:
        lines.append(f"Asset type: {args.asset}")
    lines.append("Primary request: " + template.format(region=region, language=language))
    if layer:
        style = pick_style(spec, args.style_id)
        lines.append(f"This version's style ({style.get('name') or style['id']}): {style.get('description', '')}")
        if style.get("kind") in BATCH_RULES:
            lines.append(BATCH_RULES[style["kind"]])
        earlier = [s for s in spec.get("styles") or [] if (s.get("batch") or 1) < (style.get("batch") or 1)]
        if earlier:
            lines.append("Must look clearly different from every earlier version: "
                         + "; ".join(f"{s.get('name') or s.get('id')}: {s.get('description', '')}" for s in earlier))
        box = (job_spec.require_ready(spec, args.region_id) or {}).get("box")
        if box and len(box) == 4 and box[3] > box[1]:
            lines.append(f"Shape: close to the original logo's proportions, about {(box[2] - box[0]) / (box[3] - box[1]):.2f}:1 "
                         "(width:height), so it fits the original logo's place.")
    first = "the source logo (style reference)" if standalone else "edit target"
    lines.append(f"Input images: Image 1: {first}" + "".join(
        f"; Image {i}: style reference" for i in range(2, 2 + (args.references or 0))))
    if spec and spec.get("anchors"):
        lines.append("Visual anchors (must not be lost): " + "; ".join(spec["anchors"]))
    if spec and spec.get("route") and args.kind in TEXT_KINDS:
        lines.append(f"{language} lettering route: {spec['route']}")
    if args.source_text:
        lines.append(f'Original text: "{args.source_text}"')
    if args.target_text:
        rule = f" {ARABIC_TEXT_RULE}" if ARABIC_RE.search(args.target_text) else f" {OTHER_TEXT_RULE}"
        lines.append(f'Text (verbatim): "{args.target_text}"{rule}')
    if args.style:
        lines.append(f"Style/medium: {args.style}")
    if spec and spec.get("sentence_map") and args.kind in TEXT_KINDS:
        lines.append("Phrases (each target phrase takes this role, place, line count and lockup): "
                     + "; ".join(job_spec.sentence_line(e) for e in spec["sentence_map"]))
    if spec and spec.get("word_map") and args.kind in TEXT_KINDS:
        lines.append("Words, in reading order (each target word takes this place, size and look): "
                     + "; ".join(job_spec.word_line(e) for e in spec["word_map"]))
    if spec and spec.get("letter_map") and args.kind in TEXT_KINDS:
        lines.append("Letter colours and styles, in reading order (each target letter takes exactly this colour "
                     "and style): " + "; ".join(job_spec.letter_line(e) for e in spec["letter_map"]))
    for feat in (spec or {}).get("features") or []:
        if feat.get("decision") in ("transfer", "keep", "drop"):
            to = (f" to {feat['to']}" if feat["decision"] == "transfer" else f" ({feat['to']})") if feat.get("to") else ""
            lines.append(f"Ornament: {feat.get('name')}: {feat['decision']}{to}")
    if spec and spec.get("prompt_notes") and args.kind in TEXT_KINDS:
        lines.append("Findings from the analysis: " + "; ".join(spec["prompt_notes"]))
    if args.design_notes:
        notes = Path(args.design_notes).read_text(encoding="utf-8-sig").strip()
        lines.append("Design notes (from the analysis card): " + " ".join(notes.split()))
    keep = [] if standalone else ["everything outside " + region]
    keep += args.keep or []
    if args.kind in TEXT_KINDS and not standalone:
        lines.append(f"Core rule: outside {region} the image stays the original; inside it only the lettering "
                     "changes, in the same style.")
    if keep:
        lines.append("Constraints: change only what is requested; keep unchanged: " + "; ".join(keep))
    avoid = ["extra text", "watermark"] + (args.avoid or [])
    if args.kind in TEXT_KINDS:
        avoid.append("adding an outline, shadow, glow, panel or caption the original lacks")
    if layer:
        avoid.append("any opaque, white, black or checkerboard background")
    lines.append("Avoid: " + "; ".join(avoid))
    return "\n".join(lines)


def cmd_prompt(args) -> int:
    text = build_prompt(args)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def newest_output(since: float | None = None) -> Path | None:
    root = codex_home() / "generated_images"
    if not root.is_dir():
        return None
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES]
    if since is not None:
        files = [p for p in files if p.stat().st_mtime >= since]
    return max(files, key=lambda p: p.stat().st_mtime, default=None)


def cmd_collect(args) -> int:
    since = None
    if args.since_minutes is not None:
        since = dt.datetime.now().timestamp() - args.since_minutes * 60
    source = Path(args.file) if args.file else newest_output(since)
    if source is None or not source.is_file():
        raise SystemExit("ERROR no image_gen output found (check ~/.codex/generated_images or pass --file)")
    out = Path(args.out)
    if out.exists():
        raise SystemExit(f"ERROR {out} exists; collect never overwrites, choose a new name (e.g. raw_2.png)")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, out)
    with Image.open(out) as im:
        size, mode = list(im.size), im.mode
    note = {"tool": "codex image_gen", "from": str(source), "file": out.name, "sha256": sha256(out),
            "size": size, "mode": mode,
            "collected": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    if args.prompt_file:
        note["prompt"] = Path(args.prompt_file).read_text(encoding="utf-8-sig").strip()
    write_json(str(out) + ".json", note)
    print_json({**note, "next": "Open it. For localize/edit run `composite` next; never deliver it raw."})
    return 0


def composite(source: Image.Image, generated: Image.Image, mask: Image.Image, feather: int = 0):
    """Source outside the mask, generated inside it, after scaling the output back to the source size."""
    notes = {}
    gen = generated.convert("RGBA")
    if gen.size != source.size:
        src_ratio, gen_ratio = source.width / source.height, gen.width / gen.height
        notes["rescaled_from"] = list(gen.size)
        if abs(src_ratio - gen_ratio) / src_ratio > 0.01:
            notes["warning"] = (f"aspect ratio changed ({gen_ratio:.3f} vs {src_ratio:.3f}); the region may be "
                                "distorted, check the sheet closely")
        gen = gen.resize(source.size, Image.LANCZOS)
    hard = mask.convert("L").point(lambda v: 255 if v else 0)
    if hard.size != source.size:
        raise SystemExit("ERROR mask size differs from the source")
    weight = hard
    if feather > 0:
        weight = ImageChops.multiply(hard.filter(ImageFilter.GaussianBlur(feather)), hard)  # inward only
        notes["feather"] = feather
    result = Image.composite(gen, source.convert("RGBA"), weight)
    if source.mode != "RGBA":
        result = result.convert(source.mode)
    return result, notes


def cmd_composite(args) -> int:
    if Path(args.out).resolve() == Path(args.source).resolve():
        raise SystemExit("ERROR --out must differ from --source")
    with Image.open(args.source) as im:
        source = im.copy()
    with Image.open(args.generated) as im:
        generated = im.copy()
    with Image.open(args.mask) as im:
        mask = im.copy()
    result, notes = composite(source, generated, mask, args.feather)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    result.save(args.out)
    print_json({"out": args.out, "out_sha256": sha256(args.out), "size": list(result.size), "mode": result.mode,
                **notes, "next": "compare_sheet.py --source ... --candidate ..., then open it."})
    return 0


def trim_layer(layer: Image.Image) -> Image.Image:
    """The layer cut to its visible pixels; refuses a layer without real transparency."""
    if "A" not in layer.getbands():
        raise SystemExit("ERROR the layer has no alpha channel; it was not drawn on transparency (tell the user)")
    layer = layer.convert("RGBA")
    alpha = layer.getchannel("A")
    if alpha.getextrema()[0] == 255:
        raise SystemExit("ERROR the layer is fully opaque; it was not drawn on transparency (tell the user)")
    bbox = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox is None:
        raise SystemExit("ERROR the layer is empty")
    return layer.crop(bbox)


def place(plate: Image.Image, layer: Image.Image, box):
    """Fit the trimmed layer inside box (keeping its proportions, centred) over the plate.

    Returns the result, the trimmed layer and notes."""
    logo = trim_layer(layer)
    x0, y0, x1, y1 = box
    scale = min((x1 - x0) / logo.width, (y1 - y0) / logo.height)
    size = (max(1, round(logo.width * scale)), max(1, round(logo.height * scale)))
    fitted = logo.resize(size, Image.LANCZOS)
    at = (x0 + (x1 - x0 - size[0]) // 2, y0 + (y1 - y0 - size[1]) // 2)
    canvas = plate.convert("RGBA")
    canvas.alpha_composite(fitted, at)
    result = canvas.convert(plate.mode) if plate.mode != "RGBA" else canvas
    notes = {"layer_size": list(logo.size), "placed_at": list(at), "placed_size": list(size),
             "scale": round(scale, 4)}
    return result, logo, notes


def cmd_place(args) -> int:
    with Image.open(args.plate) as im:
        plate = im.copy()
    with Image.open(args.layer) as im:
        layer = im.copy()
    box = parse_box(args.box, *plate.size)
    result, logo, notes = place(plate, layer, box)
    for path in (args.out, args.logo_out):
        if path:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
    out = Path(args.out)
    (result.convert("RGB") if out.suffix.lower() in (".jpg", ".jpeg") else result).save(out, quality=95)
    if args.logo_out:
        logo.save(args.logo_out)
    print_json({"out": args.out, "size": list(result.size), "mode": result.mode, **notes,
                "logo_out": args.logo_out,
                "next": "compare_sheet.py --source <src> --candidate <out>, then open it."})
    return 0


def main(argv=None) -> int:
    utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("prompt", help="print an image_gen prompt")
    pr.add_argument("--kind", choices=list(KINDS), required=True)
    pr.add_argument("--spec", help="<job>/job.json; required for localize-text and logo")
    pr.add_argument("--region-id", help="which TRANSLATE region of job.json (when there are several)")
    pr.add_argument("--style-id", help="--kind layer: the style's number in job.json (1, 2, 3...)")
    pr.add_argument("--region", help="where, in words: 'the large title in the upper middle'")
    pr.add_argument("--source-text")
    pr.add_argument("--target-text", help="optional check: must equal the approved text in job.json")
    pr.add_argument("--style", help="lettering/visual style in one line (from the analysis card)")
    pr.add_argument("--design-notes", help="file with the short analysis-card summary to pass along")
    pr.add_argument("--asset", help="where the image will be used")
    pr.add_argument("--references", type=int, default=0, help="number of extra style-reference images attached")
    pr.add_argument("--keep", action="append", help="must stay unchanged; repeatable")
    pr.add_argument("--avoid", action="append", help="must not appear; repeatable")
    pr.add_argument("--out", help="also save the prompt to this file")

    co = sub.add_parser("collect", help="copy the newest image_gen output into the job")
    co.add_argument("--out", required=True, help="e.g. <job>/work/raw_1.png (never overwritten)")
    co.add_argument("--file", help="a specific generated file instead of the newest one")
    co.add_argument("--since-minutes", type=float, help="only consider outputs from the last N minutes")
    co.add_argument("--prompt-file", help="the prompt used; saved in the note next to the image")

    cp = sub.add_parser("composite", help="edited result back onto the untouched source through the mask")
    cp.add_argument("--source", required=True)
    cp.add_argument("--generated", required=True)
    cp.add_argument("--mask", required=True, help="L mask from make_mask.py --out (255 = may change)")
    cp.add_argument("--feather", type=int, default=0, help="soften the seam inward by N px")
    cp.add_argument("--out", required=True)

    pl = sub.add_parser("place", help="transparent logo layer onto the clean plate, inside the old logo's box")
    pl.add_argument("--plate", required=True, help="the clean plate (source with the old logo removed)")
    pl.add_argument("--layer", required=True, help="the transparent logo layer from image_gen")
    pl.add_argument("--box", nargs=4, type=int, required=True, metavar=("X0", "Y0", "X1", "Y1"),
                    help="the old logo's box from job.json; the layer is fitted inside it")
    pl.add_argument("--out", required=True, help="the result, in the source's format (.jpg stays .jpg)")
    pl.add_argument("--logo-out", help="also save the trimmed transparent logo (PNG)")

    args = p.parse_args(argv)
    return {"prompt": cmd_prompt, "collect": cmd_collect, "composite": cmd_composite,
            "place": cmd_place}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
