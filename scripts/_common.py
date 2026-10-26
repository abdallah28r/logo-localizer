"""Small helpers shared by the logo-localizer scripts."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ARABIC_RE = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
SUPPORTED_MODES = ("RGB", "RGBA", "L", "LA")


def utf8_stdio() -> None:
    """Windows consoles default to a legacy code page; Arabic output needs UTF-8."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_box(values, width: int | None = None, height: int | None = None) -> tuple[int, int, int, int]:
    """Validate an [x0, y0, x1, y1] box (x1/y1 exclusive), optionally against an image size."""
    if values is None or len(values) != 4:
        raise ValueError("box needs four integers: x0 y0 x1 y1")
    x0, y0, x1, y1 = (int(v) for v in values)
    if not (x0 < x1 and y0 < y1) or x0 < 0 or y0 < 0:
        raise ValueError(f"invalid box {values}: need 0 <= x0 < x1 and 0 <= y0 < y1")
    if width is not None and (x1 > width or y1 > height):
        raise ValueError(f"box {values} exceeds image size {width}x{height}")
    return x0, y0, x1, y1


def parse_size(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)[xX×](\d+)", value.strip())
    if not match:
        raise ValueError(f"size must look like 1080x1080, got {value!r}")
    return int(match.group(1)), int(match.group(2))


def parse_color(value: str, opacity: float = 1.0) -> tuple[int, int, int, int]:
    """'#RRGGBB', '#RRGGBBAA', 'transparent', or a Pillow color name -> RGBA."""
    from PIL import ImageColor

    if value.lower() == "transparent":
        return (0, 0, 0, 0)
    rgba = ImageColor.getcolor(value, "RGBA")
    return rgba[0], rgba[1], rgba[2], round(rgba[3] * max(0.0, min(1.0, opacity)))


def write_json(path: str | Path, data) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_json(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))
