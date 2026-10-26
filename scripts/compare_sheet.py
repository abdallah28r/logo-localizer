"""Build a review sheet: source and candidates side by side, plus the views review needs.

Rows: native size; dark/light/checkerboard backgrounds (automatic when any
image has transparency); and a zoomed crop (--zoom). Open the sheet AND the
full candidate before approving anything.

Examples:
  python compare_sheet.py --source source/x.png --candidate out/x_v1.png --out review/x_v1.png
  python compare_sheet.py --source source/x.png --candidate out/x_v1.png --zoom 120 40 520 110 --out review/x_zoom.png
  python compare_sheet.py --candidate out/a.png --candidate out/b.png --out review/a_vs_b.png
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import parse_box, print_json, utf8_stdio  # noqa: E402

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

GAP = 16
LABEL_H = 26
SHEET_BG = (48, 48, 52, 255)


def _label_font():
    try:
        return ImageFont.load_default(size=15)
    except TypeError:  # very old Pillow
        return ImageFont.load_default()


def checkerboard(size, cell: int = 12) -> Image.Image:
    board = Image.new("RGBA", size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(board)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(200, 200, 200, 255))
    return board


def on_background(image: Image.Image, background: str) -> Image.Image:
    rgba = image.convert("RGBA")
    if background == "checker":
        base = checkerboard(rgba.size)
    else:
        base = Image.new("RGBA", rgba.size, (16, 16, 16, 255) if background == "dark" else (245, 245, 245, 255))
    base.alpha_composite(rgba)
    return base


def has_alpha(image: Image.Image) -> bool:
    if image.mode not in ("RGBA", "LA", "PA") and "transparency" not in image.info:
        return False
    return image.convert("RGBA").getchannel("A").getextrema()[0] < 255


def build_sheet(columns: list[tuple[str, Image.Image]], zoom=None, zoom_factor: int = 4,
                backgrounds: str = "auto") -> Image.Image:
    rows: list[tuple[str, list[Image.Image]]] = []
    rows.append(("native", [on_background(img, "checker") if has_alpha(img) else img.convert("RGBA")
                            for _, img in columns]))
    want_bg = backgrounds == "yes" or (backgrounds == "auto" and any(has_alpha(img) for _, img in columns))
    if want_bg:
        for background in ("dark", "light", "checker"):
            rows.append((background, [on_background(img, background) for _, img in columns]))
    if zoom:
        crops = []
        for _, img in columns:
            box = parse_box(zoom, *img.size)
            crop = on_background(img.crop(box), "checker") if has_alpha(img) else img.crop(box).convert("RGBA")
            crops.append(crop.resize((crop.width * zoom_factor, crop.height * zoom_factor), Image.NEAREST))
        rows.append((f"zoom x{zoom_factor} {list(zoom)}", crops))

    font = _label_font()
    col_w = [max(row[1][i].width for row in rows) for i in range(len(columns))]
    width = GAP + sum(w + GAP for w in col_w)
    height = GAP + LABEL_H + sum(LABEL_H + max(img.height for img in imgs) + GAP for _, imgs in rows)
    sheet = Image.new("RGBA", (width, height), SHEET_BG)
    draw = ImageDraw.Draw(sheet)
    x = GAP
    for i, (name, img) in enumerate(columns):
        draw.text((x, GAP), f"{name}  {img.width}x{img.height} {img.mode}", fill=(235, 235, 235, 255), font=font)
        x += col_w[i] + GAP
    y = GAP + LABEL_H
    for row_name, imgs in rows:
        draw.text((GAP, y + 4), row_name, fill=(170, 200, 255, 255), font=font)
        y += LABEL_H
        x = GAP
        for i, img in enumerate(imgs):
            sheet.alpha_composite(img, (x, y))
            x += col_w[i] + GAP
        y += max(img.height for img in imgs) + GAP
    return sheet.convert("RGB")


def main(argv=None) -> int:
    utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--source", help="original image (omit for new designs)")
    p.add_argument("--candidate", action="append", required=True, help="repeat for several candidates")
    p.add_argument("--out", required=True)
    p.add_argument("--zoom", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("--zoom-factor", type=int, default=4)
    p.add_argument("--backgrounds", choices=["auto", "yes", "no"], default="auto")
    args = p.parse_args(argv)
    columns = []
    if args.source:
        with Image.open(args.source) as im:
            columns.append((f"source {Path(args.source).name}", im.copy()))
    for path in args.candidate:
        with Image.open(path) as im:
            columns.append((Path(path).name, im.copy()))
    sheet = build_sheet(columns, args.zoom, args.zoom_factor, args.backgrounds)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out)
    print_json({"sheet": args.out, "size": list(sheet.size),
                "next": "Open this sheet and the full-size candidate before judging the result."})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
