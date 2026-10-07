"""Behavior checks use synthetic fixtures, never production artwork or TTS."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
module_spec = importlib.util.spec_from_file_location("renderer", SCRIPTS / "render_semantic_cartoon.py")
module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(module)
Renderer = module.Renderer


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        for name, color in (("a", "red"), ("b", "blue"), ("prop", "green"), ("caption", "white")):
            image = Image.new("RGBA", (20, 20))
            ImageDraw.Draw(image).rectangle((4, 4, 15, 15), fill=color)
            image.save(self.work / f"{name}.png")
        self.spec = {
            "duration": 1,
            "canvas": {"width": 100, "height": 100, "fps": 30, "motion_fps": 8, "background": "#000000"},
            "character_stages": [{"start": 0, "asset": "a.png", "x": 50, "bottom": 50, "scale": 1}],
        }

    def renderer(self, spec=None):
        return Renderer(self.work / "spec.json", deepcopy(self.spec if spec is None else spec))

    def run_helper(self, name, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / name), *map(str, args)], capture_output=True, text=True)

    def test_default_hold_and_seek_are_stable(self):
        r = self.renderer()
        a = r.render_frame(0).tobytes()
        self.assertEqual(a, r.render_frame(0.8).tobytes())
        self.assertEqual(a, r.render_frame(0).tobytes())

    def test_pose_switch_is_not_delayed_by_transform_cadence(self):
        self.spec["character_stages"].append({"start": 0.15, "asset": "b.png", "x": 50, "bottom": 50, "scale": 1})
        r = self.renderer()
        self.assertEqual(r.render_frame(4 / 30).getpixel((50, 40)), (255, 0, 0))
        self.assertEqual(r.render_frame(5 / 30).getpixel((50, 40)), (0, 0, 255))

    def test_prop_and_caption_intervals_are_end_exclusive(self):
        self.spec["prop_tracks"] = [{"scene_start": 0, "scene_end": 0.15, "appear": 0, "asset": "prop.png", "x": 80, "y": 40, "width": 20}]
        self.spec["subtitle_tracks"] = [{"start": 0.15, "end": 0.5, "asset": "caption.png", "x": 50, "y": 80, "height": 20}]
        r = self.renderer()
        self.assertEqual(r.render_frame(4 / 30).getpixel((80, 40)), (0, 128, 0))
        self.assertEqual(r.render_frame(5 / 30).getpixel((80, 40)), (0, 0, 0))
        self.assertEqual(r.render_frame(5 / 30).getpixel((50, 80)), (255, 255, 255))
        self.assertEqual(r.render_frame(0.5).getpixel((50, 80)), (0, 0, 0))

    def test_background_and_intentional_return_pose(self):
        Image.new("RGB", (100, 100), "yellow").save(self.work / "background.png")
        self.spec["canvas"]["background_asset"] = "background.png"
        self.spec["character_stages"].append({"start": 0.5, "asset": "a.png", "x": 50, "bottom": 50, "scale": 1})
        self.assertEqual(self.renderer().render_frame(0.5).getpixel((0, 0)), (255, 255, 0))
        Image.new("RGB", (80, 80)).save(self.work / "background.png")
        with self.assertRaisesRegex(ValueError, "match canvas"):
            self.renderer()

    def test_invalid_timeline_fails_before_frames(self):
        for value in (float("nan"), True, -1, 0.015):
            with self.subTest(value=value):
                spec = deepcopy(self.spec)
                spec["duration"] = value
                with self.assertRaises(ValueError):
                    self.renderer(spec)
        self.spec["character_stages"][0]["start"] = 0.1
        with self.assertRaises(ValueError):
            self.renderer()

    def test_renderer_refuses_stale_output(self):
        spec_path = self.work / "spec.json"
        spec_path.write_text(json.dumps(self.spec))
        frames = self.work / "frames"
        frames.mkdir()
        sentinel = frames / "frame-0999.png"
        sentinel.write_bytes(b"keep")
        result = self.run_helper("render_semantic_cartoon.py", spec_path, frames)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sentinel.read_bytes(), b"keep")
        self.assertEqual(len(list(frames.iterdir())), 1)

    def test_atlas_audit_and_preserved_canvas_extraction(self):
        atlas = Image.new("RGBA", (80, 40))
        draw = ImageDraw.Draw(atlas)
        draw.rectangle((10, 10, 29, 29), fill="red")
        draw.rectangle((50, 10, 69, 29), fill="blue")
        source = self.work / "atlas.png"
        atlas.save(source)
        common = (source, "--columns", 2, "--rows", 1, "--names", "a,b")
        result = self.run_helper("audit_atlas_safe_margins.py", *common)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_helper("split_grid_atlas.py", source, self.work / "poses", *common[1:], "--keep-cell-size")
        self.assertEqual(result.returncode, 0, result.stderr)
        for name, color in (("a", (255, 0, 0, 255)), ("b", (0, 0, 255, 255))):
            with Image.open(self.work / "poses" / f"{name}.png") as pose:
                self.assertEqual(pose.size, (40, 40))
                self.assertEqual(pose.getpixel((20, 20)), color)
                self.assertEqual(pose.getpixel((0, 0))[3], 0)
        atlas.putpixel((0, 10), (255, 0, 0, 255))
        atlas.save(source)
        result = self.run_helper("audit_atlas_safe_margins.py", *common)
        self.assertNotEqual(result.returncode, 0)

    def test_splitter_rejects_escaping_names(self):
        result = self.run_helper("split_grid_atlas.py", self.work / "a.png", self.work / "poses", "--columns", 1, "--rows", 1, "--names", "../escape")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.work / "escape.png").exists())

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/ffprobe unavailable")
    def test_full_encode_frame_count_and_decode(self):
        path = self.work / "spec.json"
        path.write_text(json.dumps(self.spec))
        frames = self.work / "frames"
        result = self.run_helper("render_semantic_cartoon.py", path, frames)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list(frames.glob("frame-*.png"))), 30)
        video = self.work / "smoke.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-n", "-framerate", "30", "-i", str(frames / "frame-%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(video)], check=True)
        probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-of", "json", str(video)]))
        stream = probe["streams"][0]
        self.assertEqual((stream["width"], stream["height"], stream["avg_frame_rate"], stream["nb_read_frames"]), (100, 100, "30/1", "30"))
        subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(video), "-f", "null", "-"], check=True)


if __name__ == "__main__":
    unittest.main()
