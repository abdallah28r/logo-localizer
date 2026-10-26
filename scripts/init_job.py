"""Create an logo-localizer job folder and its job.json skeleton. Never overwrites existing files.

Example: python init_job.py jobs/witchfire --mode localize
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import print_json, utf8_stdio, write_json  # noqa: E402
from job_spec import new_spec  # noqa: E402

MODES = ("localize", "standalone")

BRIEF = """- Where the logo appears (game cover, store page, poster, app icon):
- Source language -> target language (Arabic unless stated):
- Official target-language title, if one exists (store page, publisher):
- Approved names and terms (source -> target):
- Formats to deliver (same as source unless stated):
"""


def write_spec(path: Path, mode: str, created: list[str]) -> None:
    if not path.exists():
        spec = new_spec(mode)
        spec["brief"] = BRIEF.strip().splitlines()
        write_json(path, spec)
        created.append(str(path))


def main(argv=None) -> int:
    utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("job_dir")
    p.add_argument("--mode", choices=MODES, required=True)
    args = p.parse_args(argv)
    root = Path(args.job_dir)
    created: list[str] = []
    for folder in ("source", "work", "out", "review"):
        target = root / folder
        if not target.exists():
            target.mkdir(parents=True)
            created.append(str(target))
    write_spec(root / "job.json", args.mode, created)
    print_json({"job": str(root), "mode": args.mode, "created": created,
                "next": "Copy inputs into source/ (never edit them) and put measuring crops in work/. "
                        "After the research and analysis, write them into job.json; show both cards "
                        "and wait for the user's reply. After it, add the "
                        "chosen text and four styles, then run job_spec.py check and show the preflight "
                        "before any image_gen call."})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
