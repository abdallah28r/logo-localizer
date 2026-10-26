"""Build a tight edit mask for an image: whole boxes, or only the ink inside them.

Writes an L mask (255 = may change) used by codex_image.py composite. The
mask never leaves its boxes.

For redrawn text, use --union-with on the generated image: the mask becomes
the old text ink plus the new text ink, so the composite removes every old
letter and takes every new one without a rectangular patch around them.

When the box also holds background detail that contrasts with its
surroundings (graffiti, signs, props), pick the text by its own colours with
--ink-color (the fill and outline/shadow from job.json's palette): only those
pixels count as ink, so the background between and behind the letters stays
the source's. --add-mask joins masks
made earlier (the old-text mask of a clean plate plus the new-text mask).

Examples:
  python make_mask.py source/x.png --box 120 40 520 110 --out work/m.png
  python make_mask.py source/x.png --box 120 40 520 110 --ink --grow 3 --out work/m.png
  python make_mask.py source/x.png --box 120 40 520 110 --union-with work/raw_2.png --grow 12 --out work/m.png
  python make_mask.py source/x.png --box 32 35 790 535 --ink-color "#F1F0E9" --ink-color "#8D2234" --grow 4 --out work/old_text.png
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import parse_box, parse_color, print_json, utf8_stdio  # noqa: E402

import numpy as np  # noqa: E402
from PIL import Image, ImageChops, ImageDraw, ImageFilter  # noqa: E402


def ink_mask(image: Image.Image, box, tol: int = 40) -> tuple[np.ndarray, dict]:
    """Boolean ink array for the box (box-local): alpha on transparent images, else distance from the border colour."""
    crop = np.asarray(image.convert("RGBA").crop(box)).astype(np.int16)
    alpha = crop[..., 3]
    if (alpha < 250).mean() > 0.2:
        return alpha > 16, {"method": "alpha>16"}
    rgb = crop[..., :3]
    ring = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    bg_rgb = np.median(ring, axis=0)
    return np.abs(rgb - bg_rgb).max(axis=2) > tol, {"method": "color-distance", "tol": tol}


def color_ink(image: Image.Image, box, colors, color_tol: int = 60) -> np.ndarray:
    """Pixels in the box within color_tol (max channel distance) of any of the text colours."""
    rgb = np.asarray(image.convert("RGB").crop(box)).astype(np.int16)
    near = np.zeros(rgb.shape[:2], dtype=bool)
    for color in colors:
        near |= np.abs(rgb - np.array(color[:3], dtype=np.int16)).max(axis=2) <= color_tol
    return near


def build_mask(image: Image.Image, boxes, ink: bool = False, grow: int = 0, tol: int = 40, pad: int = 0,
               others=(), colors=(), color_tol: int = 60):
    """others: images (e.g. the generated one) whose ink in the same boxes joins the mask; implies ink.
    colors: the text's own colours; when given, only pixels near them count as ink."""
    width, height = image.size
    others = [o if o.size == image.size else o.resize(image.size, Image.LANCZOS) for o in others]
    ink = ink or bool(others) or bool(colors)

    def find(img, box):
        return color_ink(img, box, colors, color_tol) if colors else ink_mask(img, box, tol=tol)[0]

    mask = Image.new("L", image.size, 0)
    used = []
    for raw in boxes:
        x0, y0, x1, y1 = parse_box(raw, width, height)
        box = (max(0, x0 - pad), max(0, y0 - pad), min(width, x1 + pad), min(height, y1 + pad))
        used.append(list(box))
        region = Image.new("L", image.size, 0)
        if ink:
            found = find(image, box)
            if others:
                # old ink plus new ink, kept only where the pixels actually changed:
                # background detail present in both images is not text
                base = np.asarray(image.convert("RGB").crop(box)).astype(np.int16)
                changed = np.zeros(found.shape, dtype=bool)
                for other in others:
                    found = found | find(other, box)
                    pixels = np.asarray(other.convert("RGB").crop(box)).astype(np.int16)
                    changed |= np.abs(pixels - base).max(axis=2) > tol
                found = found & changed
            local = Image.fromarray((found * 255).astype("uint8"), "L")
            if others or colors:
                local = local.filter(ImageFilter.MinFilter(3))  # drop 1-2 px specks of noise
            for step in range(0, grow, 3):  # small passes: one large MaxFilter is very slow
                local = local.filter(ImageFilter.MaxFilter(2 * min(3, grow - step) + 1))
            region.paste(local, box[:2])  # grown inside the box only, so it never leaves it
        else:
            ImageDraw.Draw(region).rectangle((box[0], box[1], box[2] - 1, box[3] - 1), fill=255)
        mask = ImageChops.lighter(mask, region)
    return mask.point(lambda v: 255 if v else 0), used


def main(argv=None) -> int:
    utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("image")
    p.add_argument("--box", nargs=4, type=int, action="append", required=True, metavar=("X0", "Y0", "X1", "Y1"),
                   help="repeat for several regions")
    p.add_argument("--pad", type=int, default=0, help="enlarge each box")
    p.add_argument("--ink", action="store_true", help="mask only ink pixels inside each box")
    p.add_argument("--union-with", action="append", default=[], metavar="IMAGE",
                   help="add this image's ink in the same boxes (the generated text); implies --ink")
    p.add_argument("--grow", type=int, default=2, help="dilate ink by N px (with --ink)")
    p.add_argument("--tol", type=int, default=40)
    p.add_argument("--ink-color", action="append", default=[], metavar="HEX",
                   help="a colour of the text itself (fill, outline, shadow); repeatable; implies --ink")
    p.add_argument("--color-tol", type=int, default=60, help="max channel distance from an --ink-color")
    p.add_argument("--add-mask", action="append", default=[], metavar="PNG",
                   help="join an earlier mask of the same size (e.g. old text + new text)")
    p.add_argument("--out", required=True, help="L mask PNG")
    args = p.parse_args(argv)
    others = [Image.open(path) for path in args.union_with]
    with Image.open(args.image) as im:
        mask, used = build_mask(im, args.box, args.ink, args.grow, args.tol, args.pad, others,
                                [parse_color(c) for c in args.ink_color], args.color_tol)
    for path in args.add_mask:
        with Image.open(path) as extra:
            if extra.size != mask.size:
                raise SystemExit(f"ERROR {path} size {extra.size} differs from {mask.size}")
            mask = ImageChops.lighter(mask, extra.convert("L").point(lambda v: 255 if v else 0))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    mask.save(args.out)
    print_json({"mask": args.out, "boxes": used,
                "masked_pixels": mask.histogram()[255], "bbox": mask.getbbox()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
