"""The job spec (<job>/job.json): what was measured, decided and approved, and the stage reached.

  new    write a job.json skeleton (init_job.py does this for you)
  check  validate job.json, move it to the "preflight" stage and print the
         preflight summary to show the user before the first image_gen call
  done   mark the job delivered

job.json is a working file that drives the job, not a log. codex_image.py
prompt --spec builds the image_gen prompt from it and refuses to run before
`check` has passed, so designed text cannot be drawn before the user chose it.

Examples:
  python job_spec.py check jobs/witchfire
  python job_spec.py done jobs/witchfire
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import parse_box, utf8_stdio, write_json  # noqa: E402

STAGES = ("draft", "preflight", "delivered")
TEXT_TYPES = ("logo", "display")
MODES = ("localize", "standalone")
DECISIONS = ("TRANSLATE", "KEEP", "REVIEW")
BATCH = 4
BATCH_KINDS = ("close", "creative")  # extra batches: close to the original's spirit / more inventive


def new_spec(mode: str) -> dict:
    return {
        "version": 1,
        "stage": "draft",
        "mode": mode,
        "source": {"file": "", "size": None},
        "source_language": "",
        "target_language": "ar",
        "regions": [
            {"id": "title", "box": [0, 0, 1, 1], "description": "where it is, in words",
             "decision": "TRANSLATE", "text_type": "logo", "source_text": "", "target_text": "",
             "chosen_by_user": False}
        ],
        "route": "",
        "styles": [
            {"id": "1", "batch": 1, "kind": "first", "name": "",
             "description": "one of four clearly different styles, chosen by the model"}
        ],
        "chosen_style": "",
        "anchors": [],
        "lettering": {"skeleton": "", "stroke": "", "rhythm": "", "signature_letter": ""},
        "surface": {"palette": [], "texture": "", "effects": []},
        "features": [],
        "sentence_map": [],
        "word_map": [],
        "letter_map": [],
        "keep": [],
        "avoid": [],
        "uncertain": [],
        "brief": [],
    }


def spec_path(job: str | Path) -> Path:
    path = Path(job)
    return path if path.suffix == ".json" else path / "job.json"


def load(job: str | Path) -> dict:
    path = spec_path(job)
    if not path.is_file():
        raise SystemExit(f"ERROR {path} not found; run init_job.py first")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def problems(spec: dict, root: Path) -> list[str]:
    """Everything that blocks the preflight; empty when the spec is ready."""
    found = []
    source = spec.get("source") or {}
    size = None
    src = root / source.get("file", "") if source.get("file") else None
    if spec.get("mode") not in MODES:
        found.append(f"mode must be one of {', '.join(MODES)}")
    if not (spec.get("target_language") or "").strip():
        found.append("target_language: the language to translate into (ar unless the user named another)")
    if not src or not src.is_file():
        found.append("source.file: copy the user's image into source/ and name it here")
    else:
        from PIL import Image

        with Image.open(src) as im:
            size = im.size
        source["size"] = list(size)
    regions = spec.get("regions") or []
    if not any(r.get("decision") == "TRANSLATE" for r in regions):
        found.append("regions: the logo or title to translate (decision TRANSLATE)")
    for r in regions:
        rid = r.get("id") or "?"
        if r.get("decision") not in DECISIONS:
            found.append(f"regions[{rid}].decision must be one of {', '.join(DECISIONS)}")
        if r.get("text_type") not in TEXT_TYPES:
            found.append(f"regions[{rid}].text_type must be one of {', '.join(TEXT_TYPES)}")
        if spec.get("mode") == "localize":
            try:
                parse_box(r.get("box"), *(size or (None, None)))
            except (ValueError, TypeError) as exc:
                found.append(f"regions[{rid}].box: {exc}")
        if r.get("decision") != "TRANSLATE":
            continue
        if not (r.get("target_text") or "").strip():
            found.append(f"regions[{rid}].target_text is empty")
        if r.get("chosen_by_user") is not True:
            found.append(f"regions[{rid}]: the text needs the user's choice from the translation card "
                         "(chosen_by_user: true); show the cards and wait")
    anchors = spec.get("anchors") or []
    if not 3 <= len(anchors) <= 5:
        found.append("anchors: give 3-5 visual anchors from the analysis card")
    styles = spec.get("styles") or []
    ids = [s.get("id") for s in styles]
    found += style_problems(styles)
    if spec.get("chosen_style") and spec["chosen_style"] not in ids:
        found.append("chosen_style: must be one of the style ids (set only after the user picks)")
    for i, entry in enumerate(spec.get("sentence_map") or []):
        if not (entry.get("target") or "").strip():
            found.append(f"sentence_map[{i}].target: the target phrase this entry describes")
    for i, entry in enumerate(spec.get("word_map") or []):
        if not (entry.get("target") or "").strip():
            found.append(f"word_map[{i}].target: the target word this entry describes")
        colour = entry.get("color")
        if colour and not (isinstance(colour, str) and colour.startswith("#") and len(colour) in (4, 7)):
            found.append(f"word_map[{i}].color: {colour!r} is not a #RRGGBB code")
    for i, entry in enumerate(spec.get("letter_map") or []):
        if not (entry.get("target") or "").strip():
            found.append(f"letter_map[{i}].target: the target letter this entry colours")
        colour = entry.get("color")
        if colour and not (isinstance(colour, str) and colour.startswith("#") and len(colour) in (4, 7)):
            found.append(f"letter_map[{i}].color: {colour!r} is not a #RRGGBB code")
    for colour in (spec.get("surface") or {}).get("palette") or []:
        if not (isinstance(colour, str) and colour.startswith("#") and len(colour) in (4, 7)):
            found.append(f"surface.palette: {colour!r} is not a #RRGGBB code")
    return found


def style_problems(styles: list[dict]) -> list[str]:
    """Styles are numbered 1, 2, 3... across the whole job, four per batch, never reused."""
    found = []
    if not styles or len(styles) % BATCH:
        found.append(f"styles: batches of exactly {BATCH} clearly different styles ({len(styles)} given)")
    for i, s in enumerate(styles):
        number, batch = str(i + 1), i // BATCH + 1
        if str(s.get("id")) != number:
            found.append(f"styles[{i}].id must be \"{number}\": numbers run on across batches and never repeat")
        if s.get("batch") != batch:
            found.append(f"styles[{number}].batch must be {batch}")
        kind = s.get("kind")
        if batch == 1 and kind not in (None, "", "first"):
            found.append(f"styles[{number}].kind: the first batch is \"first\"")
        if batch > 1 and kind not in BATCH_KINDS:
            found.append(f"styles[{number}].kind must be one of {', '.join(BATCH_KINDS)} (the option the user picked)")
        if batch > 1 and kind != styles[(batch - 1) * BATCH].get("kind"):
            found.append(f"styles[{number}].kind: all {BATCH} styles of batch {batch} share one kind")
        if not (s.get("description") or "").strip():
            found.append(f"styles[{number}].description: what this style looks like")
    return found


def preflight_lines(spec: dict) -> list[str]:
    out = [f"mode: {spec.get('mode')} | {spec.get('source_language') or '?'} -> {spec.get('target_language')} | "
           f"source: {spec['source'].get('file')} {spec['source'].get('size')}"]
    for r in spec.get("regions") or []:
        line = f"[{r.get('decision')}] {r.get('id')} ({r.get('text_type')}) box {r.get('box')}: {r.get('description', '')}"
        if r.get("decision") == "TRANSLATE":
            line += f' | "{r.get("source_text", "")}" -> "{r.get("target_text", "")}" (chosen by the user)'
        out.append(line)
    if spec.get("route"):
        out.append(f"route: {spec['route']}")
    for s in spec.get("styles") or []:
        kind = f" [{s['kind']}]" if s.get("kind") in BATCH_KINDS else ""
        out.append(f"style {s.get('id')}{kind}: {s.get('name') or ''} - {s.get('description', '')}")
    if spec.get("anchors"):
        out.append("anchors: " + "; ".join(spec["anchors"]))
    if spec.get("sentence_map"):
        out.append("phrases: " + "; ".join(sentence_line(e) for e in spec["sentence_map"]))
    if spec.get("word_map"):
        out.append("words (reading order): " + "; ".join(word_line(e) for e in spec["word_map"]))
    if spec.get("letter_map"):
        out.append("letters (reading order): " + "; ".join(letter_line(e) for e in spec["letter_map"]))
    for f in spec.get("features") or []:
        out.append(f"feature: {f.get('name')} -> {f.get('decision')}" + (f" ({f['to']})" if f.get("to") else ""))
    if spec.get("keep"):
        out.append("stays unchanged: " + "; ".join(spec["keep"]))
    if spec.get("uncertain"):
        out.append("uncertain: " + "; ".join(spec["uncertain"]))
    if spec.get("mode") == "localize":
        out.append("plan: clean plate (old logo out), then 4 transparent logo layers, one per style, each placed "
                   "on the plate; show the 4 and wait for the user's pick; then letter and mark tables on the "
                   "chosen one only")
    else:
        out.append("plan: 4 transparent logo layers, one per style; show the 4 and wait for the user's pick; "
                   "then letter and mark tables on the chosen one only")
    return out


def sentence_line(entry: dict) -> str:
    """One target phrase's role and lockup, e.g. '«دوكي دوكي» (main title, 2 lines, from DOKI DOKI, stacked)'."""
    lines = f"{entry['lines']} lines" if entry.get("lines") else ""
    extra = ", ".join(v for v in (entry.get("role", ""), lines, f"from {entry['source']}" if entry.get("source") else "",
                                  entry.get("style", "")) if v)
    head = f"«{entry.get('target', '')}»"
    return f"{head} ({extra})" if extra else head


def word_line(entry: dict) -> str:
    """One target word's place and look, e.g. 'line 1 «دوكي» (main title, from DOKI, tilted letters)'."""
    head = " ".join(v for v in (f"line {entry['line']}" if entry.get("line") else "",
                                f"«{entry.get('target', '')}»", entry.get("color", "")) if v)
    extra = ", ".join(v for v in (entry.get("role", ""), f"from {entry['source']}" if entry.get("source") else "",
                                  entry.get("style", "")) if v)
    return f"{head} ({extra})" if extra else head


def letter_line(entry: dict) -> str:
    """One target letter's look, e.g. 'line 1 د #FE8081 (tilted -8°, from D)'."""
    head = " ".join(str(v) for v in (f"line {entry['line']}" if entry.get("line") else "", entry.get("target", ""),
                                     entry.get("color", "")) if v)
    extra = ", ".join(v for v in (entry.get("style", ""), f"from {entry['from']}" if entry.get("from") else "") if v)
    return f"{head} ({extra})" if extra else head


def cmd_new(args) -> int:
    path = spec_path(args.job)
    if path.exists():
        raise SystemExit(f"ERROR {path} exists; edit it instead")
    write_json(path, new_spec(args.mode))
    print(path)
    return 0


def cmd_check(args) -> int:
    path = spec_path(args.job)
    spec = load(path)
    found = problems(spec, path.parent)
    if found:
        for line in found:
            print(f"BLOCKED {line}")
        print("PREFLIGHT=BLOCKED")
        return 1
    if spec.get("stage") == "draft":
        spec["stage"] = "preflight"
    write_json(path, spec)
    print("\n".join(preflight_lines(spec)))
    print("PREFLIGHT=OK  show this summary to the user (in their language) before the first image_gen call")
    return 0


def cmd_done(args) -> int:
    path = spec_path(args.job)
    spec = load(path)
    if spec.get("stage") == "draft":
        raise SystemExit("ERROR run `check` first; a draft job was never preflighted")
    spec["stage"] = "delivered"
    write_json(path, spec)
    print("stage=delivered")
    return 0


def require_ready(spec: dict, region_id: str | None) -> dict:
    """The region a prompt is built for, only once the preflight passed (used by codex_image.py)."""
    if spec.get("stage") not in ("preflight", "delivered"):
        raise SystemExit("ERROR job.json is still a draft: run `job_spec.py check <job>` and show the preflight first")
    regions = [r for r in spec.get("regions") or [] if r.get("decision") == "TRANSLATE"]
    if region_id:
        regions = [r for r in regions if r.get("id") == region_id]
    if len(regions) != 1:
        raise SystemExit("ERROR pick one TRANSLATE region with --region-id")
    region = regions[0]
    if region.get("chosen_by_user") is not True:
        raise SystemExit("ERROR text without the user's choice; show the cards and wait")
    return region


def main(argv=None) -> int:
    utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="write a job.json skeleton")
    n.add_argument("job")
    n.add_argument("--mode", choices=MODES, required=True)
    for name in ("check", "done"):
        sub.add_parser(name).add_argument("job", help="job folder or its job.json")
    args = p.parse_args(argv)
    return {"new": cmd_new, "check": cmd_check, "done": cmd_done}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
