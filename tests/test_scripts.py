"""Tests for the logo-localizer scripts. Run: python -m unittest discover -s tests"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from PIL import Image, ImageChops, ImageDraw  # noqa: E402

import codex_image  # noqa: E402
import compare_sheet  # noqa: E402
import init_job  # noqa: E402
import job_spec  # noqa: E402
import make_mask  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Workspace(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()



class MaskAndInkTests(Workspace):
    def _sample(self) -> Image.Image:
        image = Image.new("RGB", (100, 60), (200, 140, 30))
        ImageDraw.Draw(image).rectangle((30, 20, 69, 39), fill=(255, 255, 255))
        return image

    def test_ink_mask_stays_in_box(self):
        mask, used = make_mask.build_mask(self._sample(), [[10, 10, 90, 50]], ink=True, grow=3)
        self.assertEqual(mask.getbbox(), (27, 17, 73, 43))
        self.assertEqual(used, [[10, 10, 90, 50]])

    def test_color_mask_takes_only_text_colours_and_joins_masks(self):
        image = self._sample()  # white text on orange
        ImageDraw.Draw(image).rectangle((12, 12, 20, 20), fill=(20, 20, 20))  # dark graffiti in the box
        mask, _ = make_mask.build_mask(image, [[10, 10, 90, 50]], colors=[(255, 255, 255)], grow=0)
        self.assertEqual(mask.getpixel((15, 15)), 0)  # graffiti is not text
        self.assertEqual(mask.getpixel((50, 30)), 255)
        extra = self.root / "extra.png"
        Image.new("L", image.size, 0).save(extra)
        img_path = self.root / "img.png"
        image.save(img_path)
        out = self.root / "m.png"
        self.assertEqual(make_mask.main([str(img_path), "--box", "10", "10", "90", "50", "--ink-color", "#FFFFFF",
                                         "--add-mask", str(extra), "--out", str(out)]), 0)
        with Image.open(out) as saved:
            self.assertEqual(saved.getpixel((15, 15)), 0)

    def test_union_mask_covers_old_and_new_ink_only_where_changed(self):
        source = self._sample()
        ImageDraw.Draw(source).rectangle((12, 44, 16, 47), fill=(60, 60, 60))  # same in both: background
        generated = source.copy()
        draw = ImageDraw.Draw(generated)
        draw.rectangle((30, 20, 69, 39), fill=(200, 140, 30))  # old text removed
        draw.rectangle((50, 25, 84, 34), fill=(255, 255, 255))  # new text, wider to the right
        mask, _ = make_mask.build_mask(source, [[10, 10, 90, 50]], others=[generated])
        self.assertEqual(mask.getbbox(), (31, 21, 84, 39))  # both texts, minus the 1 px speck filter edge
        self.assertEqual(mask.getpixel((14, 45)), 0)


class CodexImageTests(Workspace):
    def test_composite_restores_outside_mask_after_upscaled_output(self):
        source = Image.new("RGB", (200, 100), (0, 0, 255))
        mask = Image.new("L", source.size, 0)
        ImageDraw.Draw(mask).rectangle((50, 30, 149, 69), fill=255)
        generated = Image.new("RGB", (554, 277), (255, 0, 0))  # image_gen upscales, same aspect
        result, notes = codex_image.composite(source, generated, mask, feather=4)
        self.assertEqual(ImageChops.difference(source, result).getbbox(), (50, 30, 150, 70))
        self.assertIn("rescaled_from", notes)
        self.assertNotIn("warning", notes)

    def test_composite_warns_when_aspect_changes(self):
        source = Image.new("RGB", (200, 100), (0, 0, 255))
        mask = Image.new("L", source.size, 255)
        _, notes = codex_image.composite(source, Image.new("RGB", (300, 300), "red"), mask)
        self.assertIn("warning", notes)

    def _prompt(self, *extra):
        out = self.root / "p.txt"
        self.assertEqual(codex_image.main(["prompt", *extra, "--out", str(out)]), 0)
        return out.read_text(encoding="utf-8")

    def _job(self, text_type="display", chosen=True, check=True, mode="localize"):
        job = self.root / "job"
        init_job.main([str(job), "--mode", mode])
        Image.new("RGB", (120, 60), "white").save(job / "source" / "x.png")
        spec = job_spec.load(job)
        spec["source"]["file"] = "source/x.png"
        spec["regions"] = [{"id": "btn", "box": [10, 10, 90, 40], "description": "the button label",
                            "decision": "TRANSLATE", "text_type": text_type, "source_text": "START",
                            "target_text": "ابدأ", "chosen_by_user": chosen}]
        spec["route"] = "condensed kufi"
        spec["styles"] = [{"id": str(i), "batch": 1, "kind": "first", "name": f"style {i}",
                           "description": f"look number {i}"} for i in range(1, 5)]
        spec["anchors"] = ["tall narrow letters", "thin cyan outline", "blue glow"]
        spec["keep"] = ["the logo"]
        spec["sentence_map"] = [{"target": "ابدأ", "source": "START", "role": "button", "lines": 1}]
        spec["word_map"] = [{"target": "ابدأ", "source": "START", "line": 1, "role": "main title"}]
        spec["letter_map"] = [{"target": "ا", "line": 1, "color": "#FE8081", "style": "tilted", "from": "S"}]
        (job / "job.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        if check:
            self.assertEqual(job_spec.main(["check", str(job)]), 0)
        return job / "job.json"

    def test_localize_prompt_carries_exact_arabic_and_forbids_invention(self):
        text = self._prompt("--kind", "localize-text", "--spec", str(self._job()))
        self.assertIn('Text (verbatim): "ابدأ"', text)
        self.assertIn('Original text: "START"', text)
        self.assertIn("right to left", text)
        self.assertIn("the logo", text)
        self.assertIn("outline, shadow, glow", text)
        self.assertIn("Image 1: edit target", text)
        self.assertIn("Core rule: outside the button label", text)
        self.assertIn("never complete it", self._prompt("--kind", "remove-text", "--region", "the title"))
        self.assertLess(text.index("Visual anchors"), text.index("Text (verbatim)"))
        self.assertIn("line 1 ا #FE8081 (tilted, from S)", text)
        self.assertIn("line 1 «ابدأ» (main title, from START)", text)
        self.assertLess(text.index("Words, in reading order"), text.index("Letter colours"))
        self.assertIn("«ابدأ» (button, 1 lines, from START)", text)
        self.assertLess(text.index("Phrases ("), text.index("Words, in reading order"))

    def test_letter_map_colours_must_be_hex(self):
        spec = self._job(check=False)
        data = job_spec.load(spec)
        data["letter_map"][0]["color"] = "pink"
        spec.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(job_spec.main(["check", str(spec)]), 1)

    def test_redrawn_text_needs_a_passed_spec(self):
        with self.assertRaises(SystemExit):
            self._prompt("--kind", "localize-text", "--target-text", "ابدأ")
        draft = self._job(check=False)
        with self.assertRaises(SystemExit):
            self._prompt("--kind", "localize-text", "--spec", str(draft))

    def test_designed_text_blocked_until_the_user_chose(self):
        spec = self._job(text_type="logo", chosen=False, check=False)
        self.assertEqual(job_spec.main(["check", str(spec)]), 1)
        self.assertEqual(job_spec.load(spec)["stage"], "draft")
        data = job_spec.load(spec)
        data["regions"][0]["chosen_by_user"] = True
        spec.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(job_spec.main(["check", str(spec)]), 0)
        self.assertEqual(job_spec.load(spec)["stage"], "preflight")
        with self.assertRaises(SystemExit):  # the approved text cannot be swapped at prompt time
            self._prompt("--kind", "logo", "--spec", str(spec), "--target-text", "ابدا")
        self.assertIn("Arabic lettering route: condensed kufi", self._prompt("--kind", "logo", "--spec", str(spec)))

    def test_standalone_logo_uses_source_as_reference_and_other_languages_work(self):
        spec = self._job(mode="standalone", text_type="logo", check=False)
        data = job_spec.load(spec)
        data["target_language"] = "fr"
        data["regions"][0]["target_text"] = "Équipe de minuit"
        spec.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(job_spec.main(["check", str(spec)]), 0)
        text = self._prompt("--kind", "logo", "--spec", str(spec))
        self.assertIn("standalone French version", text)
        self.assertIn("Image 1: the source logo (style reference)", text)
        self.assertIn("every accent, diacritic", text)
        self.assertNotIn("Core rule", text)

    def test_layer_prompt_needs_one_of_four_styles_and_asks_for_transparency(self):
        spec = self._job(text_type="logo")
        text = self._prompt("--kind", "layer", "--spec", str(spec), "--style-id", "3")
        self.assertIn("fully transparent background", text)
        self.assertIn("This version's style (style 3): look number 3", text)
        self.assertIn("about 2.67:1", text)
        self.assertIn('Text (verbatim): "ابدأ"', text)
        self.assertNotIn("Core rule", text)
        with self.assertRaises(SystemExit):
            self._prompt("--kind", "layer", "--spec", str(spec), "--style-id", "9")
        data = job_spec.load(spec)
        data["styles"] = data["styles"][:3]
        spec.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(job_spec.main(["check", str(spec)]), 1)

    def test_extra_batches_run_on_numbers_and_avoid_earlier_styles(self):
        spec = self._job(text_type="logo")
        data = job_spec.load(spec)
        data["styles"] += [{"id": str(i), "batch": 2, "kind": "creative", "name": f"bold {i}",
                            "description": f"bold look {i}"} for i in range(5, 9)]
        spec.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(job_spec.main(["check", str(spec)]), 0)
        text = self._prompt("--kind", "layer", "--spec", str(spec), "--style-id", "6")
        self.assertIn("more inventive batch", text)
        self.assertIn("Must look clearly different from every earlier version: style 1: look number 1", text)
        self.assertNotIn("bold 5", text.split("Must look")[1])
        self.assertNotIn("Must look", self._prompt("--kind", "layer", "--spec", str(spec), "--style-id", "2"))
        for broken in ({"id": "1"}, {"kind": "first"}, {"batch": 3}):  # repeated number, wrong kind, wrong batch
            bad = json.loads(json.dumps(data))
            bad["styles"][5].update(broken)
            spec.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(job_spec.main(["check", str(spec)]), 1, broken)
        bad = json.loads(json.dumps(data))
        bad["styles"][7]["kind"] = "close"  # one batch, one kind
        spec.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(job_spec.main(["check", str(spec)]), 1)

    def test_place_fits_layer_in_box_and_keeps_source_format(self):
        plate = Image.new("RGB", (200, 100), (10, 20, 30))
        layer = Image.new("RGBA", (400, 100), (0, 0, 0, 0))
        ImageDraw.Draw(layer).rectangle((100, 25, 299, 74), fill=(255, 0, 0, 255))
        result, logo, notes = codex_image.place(plate, layer, (50, 20, 150, 80))
        self.assertEqual(logo.size, (200, 50))
        self.assertEqual(notes["placed_size"], [100, 25])
        self.assertEqual(notes["placed_at"], [50, 37])
        self.assertEqual(result.getpixel((100, 50)), (255, 0, 0))
        self.assertEqual(result.getpixel((10, 90)), (10, 20, 30))
        with self.assertRaises(SystemExit):  # an opaque "transparent" layer is refused
            codex_image.place(plate, Image.new("RGBA", (40, 20), (255, 255, 255, 255)), (0, 0, 40, 20))
        out = self.root / "final.jpg"
        layer.save(self.root / "layer.png")
        plate.save(self.root / "plate.jpg")
        self.assertEqual(codex_image.main(["place", "--plate", str(self.root / "plate.jpg"), "--layer",
                                           str(self.root / "layer.png"), "--box", "50", "20", "150", "80",
                                           "--out", str(out), "--logo-out", str(self.root / "logo.png")]), 0)
        with Image.open(out) as im:
            self.assertEqual((im.format, im.size), ("JPEG", (200, 100)))
        with Image.open(self.root / "logo.png") as im:
            self.assertEqual(im.mode, "RGBA")

    def test_logo_prompt_needs_target_text(self):
        with self.assertRaises(SystemExit):
            codex_image.main(["prompt", "--kind", "logo"])

    def test_collect_copies_newest_and_never_overwrites(self):
        home = self.root / "codexhome"
        (home / "generated_images" / "t1").mkdir(parents=True)
        older, newer = home / "generated_images" / "t1" / "a.png", home / "generated_images" / "t1" / "b.png"
        Image.new("RGB", (4, 4), "red").save(older)
        Image.new("RGB", (6, 4), "blue").save(newer)
        os.utime(older, (1, 1))
        old_env = os.environ.get("CODEX_HOME")
        os.environ["CODEX_HOME"] = str(home)
        try:
            out = self.root / "job" / "raw_1.png"
            self.assertEqual(codex_image.main(["collect", "--out", str(out)]), 0)
            self.assertEqual(Image.open(out).size, (6, 4))
            self.assertTrue(Path(str(out) + ".json").is_file())
            with self.assertRaises(SystemExit):
                codex_image.main(["collect", "--out", str(out)])
        finally:
            if old_env is None:
                os.environ.pop("CODEX_HOME", None)
            else:
                os.environ["CODEX_HOME"] = old_env


class SheetCliTests(Workspace):
    def test_sheet_puts_source_and_candidate_side_by_side(self):
        Image.new("RGB", (8, 8), "blue").save(self.root / "s.png")
        Image.new("RGB", (8, 8), "red").save(self.root / "c.png")
        out = self.root / "sheet.png"
        self.assertEqual(compare_sheet.main(["--source", str(self.root / "s.png"), "--candidate",
                                             str(self.root / "c.png"), "--out", str(out)]), 0)
        self.assertTrue(out.is_file())


class JobTests(Workspace):
    def test_init_job_creates_folders_and_keeps_existing_spec(self):
        job = self.root / "job"
        self.assertEqual(init_job.main([str(job), "--mode", "standalone"]), 0)
        for name in ("source", "work", "out", "review", "job.json"):
            self.assertTrue((job / name).exists(), name)
        self.assertFalse((job / "manifest.json").exists())
        self.assertEqual(json.loads((job / "job.json").read_text(encoding="utf-8"))["stage"], "draft")
        (job / "job.json").write_text("{}", encoding="utf-8")
        init_job.main([str(job), "--mode", "standalone"])
        self.assertEqual((job / "job.json").read_text(encoding="utf-8"), "{}")



class SheetTests(Workspace):
    def test_transparent_candidate_gets_background_rows(self):
        source = Image.new("RGBA", (40, 20), (0, 0, 0, 0))
        candidate = source.copy()
        candidate.putpixel((5, 5), (255, 255, 255, 255))
        sheet = compare_sheet.build_sheet([("source", source), ("cand", candidate)])
        self.assertGreater(sheet.height, 4 * 20)  # native + dark + light + checker rows


if __name__ == "__main__":
    unittest.main()
