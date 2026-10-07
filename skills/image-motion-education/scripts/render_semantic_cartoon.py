#!/usr/bin/env python3
"""Render raster poses; adapted from sunxiayi/image-motion-animation (MIT).

See ../references/provenance.md and ../references/upstream-license.txt.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter


def resolve_path(spec_dir: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else spec_dir / path


def rgb(value: str) -> tuple[int, int, int]:
    normalized = value.lstrip("#")
    if len(normalized) != 6:
        raise ValueError(f"Expected #RRGGBB color, got {value!r}")
    return tuple(int(normalized[index:index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def require_number(mapping: dict[str, Any], key: str) -> float:
    value = mapping.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{key!r} must be a finite number")
    return float(value)


class Renderer:
    def __init__(self, spec_path: Path, spec: dict[str, Any]) -> None:
        self.spec_path = spec_path
        self.spec_dir = spec_path.parent
        self.spec = spec
        canvas = spec.get("canvas")
        if not isinstance(canvas, dict):
            raise ValueError("canvas must be an object")

        self.width = round(require_number(canvas, "width"))
        self.height = round(require_number(canvas, "height"))
        self.fps = require_number(canvas, "fps")
        self.motion_fps = require_number(canvas, "motion_fps") if "motion_fps" in canvas else self.fps
        self.duration = require_number(spec, "duration")
        if min(self.width, self.height, self.fps, self.motion_fps, self.duration) <= 0:
            raise ValueError("canvas dimensions, rates, and duration must be positive")
        if self.width != canvas["width"] or self.height != canvas["height"]:
            raise ValueError("canvas width and height must be integers")
        if not math.isclose(self.duration * self.fps, round(self.duration * self.fps), abs_tol=1e-7, rel_tol=0):
            raise ValueError("duration * fps must be an integer frame count")
        self.background = (*rgb(str(canvas.get("background", "#f7f1e3"))), 255)

        shadow = spec.get("shadow", {})
        if not isinstance(shadow, dict):
            raise ValueError("shadow must be an object")
        self.shadow_rgb = rgb(str(shadow.get("color", "#918d85")))
        self.shadow_opacity = float(shadow.get("opacity", 0.0))
        self.shadow_blur = float(shadow.get("blur", 1.2))
        self.shadow_offset_x = round(float(shadow.get("offset_x", 12)))
        self.shadow_offset_y = round(float(shadow.get("offset_y", 15)))

        self.character_stages = self._track("character_stages", required=True)
        self.prop_tracks = self._track("prop_tracks")
        self.subtitle_tracks = self._track("subtitle_tracks")
        self.character_stages.sort(key=lambda value: require_number(value, "start"))
        self.prop_tracks.sort(key=lambda value: require_number(value, "appear"))
        self.subtitle_tracks.sort(key=lambda value: require_number(value, "start"))

        starts = [require_number(stage, "start") for stage in self.character_stages]
        if starts[0] != 0 or starts[-1] >= self.duration or len(set(starts)) != len(starts):
            raise ValueError("Stages must begin at 0, have unique starts, and start before duration")

        pose_paths = [str(stage.get("asset", "")) for stage in self.character_stages]
        if not bool(spec.get("allow_pose_reuse", True)) and len(set(pose_paths)) != len(pose_paths):
            raise ValueError("character_stages reuse a pose asset; set allow_pose_reuse=true only for an intentional callback")

        all_assets = pose_paths
        all_assets += [str(track.get("asset", "")) for track in self.prop_tracks]
        all_assets += [str(track.get("asset", "")) for track in self.subtitle_tracks]
        if any(not value for value in all_assets):
            raise ValueError("Every track entry requires an asset path")
        self.images = {value: self._load(value) for value in set(all_assets)}
        self.background_image = None
        if "background_asset" in canvas:
            self.background_image = self._load(str(canvas["background_asset"]))
            if self.background_image.size != (self.width, self.height):
                raise ValueError("background_asset must match canvas dimensions; compose it deliberately first")

        for stage in self.character_stages:
            for key in ("x", "bottom", "scale"):
                require_number(stage, key)
            if stage["scale"] <= 0:
                raise ValueError("stage scale must be positive")
        for track in self.prop_tracks:
            for key in ("scene_start", "scene_end", "appear", "x", "y", "width"):
                require_number(track, key)
            if not (0 <= track["scene_start"] <= track["appear"] < track["scene_end"] <= self.duration) or track["width"] <= 0:
                raise ValueError("Invalid prop interval or width")
        previous_end = 0.0
        for track in self.subtitle_tracks:
            for key in ("start", "end", "x", "y", "height"):
                require_number(track, key)
            if not (previous_end <= track["start"] < track["end"] <= self.duration) or track["height"] <= 0:
                raise ValueError("Subtitle intervals must be ordered, nonoverlapping and inside the video")
            previous_end = track["end"]

    def _track(self, key: str, required: bool = False) -> list[dict[str, Any]]:
        value = self.spec.get(key, [])
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            raise ValueError(f"{key} must be an array of objects")
        if required and not value:
            raise ValueError(f"{key} must not be empty")
        return value

    def _load(self, value: str) -> Image.Image:
        path = resolve_path(self.spec_dir, value)
        if not path.is_file():
            raise FileNotFoundError(path)
        return Image.open(path).convert("RGBA")

    def quantize(self, time: float) -> float:
        return math.floor(time * self.motion_fps + 1e-6) / self.motion_fps

    def transform(self, source: Image.Image, *, width: int | None = None, height: int | None = None,
                  scale: float | None = None, rotation: float = 0.0) -> Image.Image:
        if width is not None:
            size = (width, round(source.height * width / source.width))
        elif height is not None:
            size = (round(source.width * height / source.height), height)
        elif scale is not None:
            size = (round(source.width * scale), round(source.height * scale))
        else:
            size = source.size
        if min(size) < 1:
            raise ValueError("Transformed image must be at least one pixel in both dimensions")
        image = source.resize(size, Image.Resampling.LANCZOS)
        if rotation:
            image = image.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=True)
        return image

    def paste(self, canvas: Image.Image, image: Image.Image, x: float, y: float, *, bottom: bool = False) -> None:
        left = round(x - image.width / 2)
        top = round(y - image.height) if bottom else round(y - image.height / 2)
        alpha = image.getchannel("A").filter(ImageFilter.GaussianBlur(self.shadow_blur))
        shadow = Image.new("RGBA", image.size, (*self.shadow_rgb, 255))
        shadow.putalpha(alpha.point(lambda value: round(value * self.shadow_opacity)))
        canvas.alpha_composite(shadow, (left + self.shadow_offset_x, top + self.shadow_offset_y))
        canvas.alpha_composite(image, (left, top))

    def active_character(self, time: float) -> tuple[dict[str, Any], int]:
        index = 0
        for candidate, stage in enumerate(self.character_stages):
            if time >= require_number(stage, "start"):
                index = candidate
            else:
                break
        return self.character_stages[index], index

    def draw_character(self, canvas: Image.Image, time: float) -> None:
        stage, index = self.active_character(time)
        start = require_number(stage, "start")
        local = self.quantize(max(0.0, time - start))
        landing_duration = float(stage.get("landing_duration", 0.25))
        landing = max(0.0, 1.0 - local / landing_duration) if landing_duration > 0 else 0.0
        direction = -1 if index % 2 else 1
        x = require_number(stage, "x") + direction * landing * float(stage.get("landing_x", 0))
        bottom = require_number(stage, "bottom") - math.sin(min(1.0, local / max(landing_duration, 1e-6)) * math.pi) * float(stage.get("landing_y", 0))
        rotation = float(stage.get("rotation", 0)) + direction * landing * float(stage.get("landing_rotation", 0))
        scale = require_number(stage, "scale") * (1.0 + landing * float(stage.get("landing_scale", 0)))
        pose = self.transform(self.images[str(stage["asset"])], scale=scale, rotation=rotation)
        self.paste(canvas, pose, x, bottom, bottom=True)

    def draw_props(self, canvas: Image.Image, time: float) -> None:
        for track in self.prop_tracks:
            scene_start = require_number(track, "scene_start")
            scene_end = require_number(track, "scene_end")
            appear = require_number(track, "appear")
            if not (scene_start <= time < scene_end) or time < appear:
                continue
            entrance_duration = float(track.get("entrance_duration", 0.34))
            progress = min(1.0, self.quantize(max(0.0, time - appear)) / max(entrance_duration, 1e-6))
            steps = max(1, int(track.get("entrance_steps", 3)))
            step = round(progress * steps) / steps
            x = require_number(track, "x")
            y = require_number(track, "y")
            direction = -1 if x < self.width / 2 else 1
            draw_x = x + direction * (1.0 - step) * float(track.get("entrance_x", 0))
            draw_y = y - math.sin(step * math.pi) * float(track.get("entrance_y", 0))
            width = round(require_number(track, "width") * (float(track.get("start_scale", 1)) + step * (1 - float(track.get("start_scale", 1)))))
            rotation = direction * (1.0 - step) * float(track.get("entrance_rotation", 0))
            asset = self.transform(self.images[str(track["asset"])], width=width, rotation=rotation)
            self.paste(canvas, asset, draw_x, draw_y)

    def draw_subtitles(self, canvas: Image.Image, time: float) -> None:
        for track in self.subtitle_tracks:
            if require_number(track, "start") <= time < require_number(track, "end"):
                source = self.images[str(track["asset"])]
                subtitle = self.transform(source, height=round(require_number(track, "height")), rotation=float(track.get("rotation", 0)))
                self.paste(canvas, subtitle, require_number(track, "x"), require_number(track, "y"))
                return

    def render_frame(self, time: float) -> Image.Image:
        canvas = Image.new("RGBA", (self.width, self.height), self.background)
        if self.background_image is not None:
            canvas.alpha_composite(self.background_image)
        self.draw_props(canvas, time)
        self.draw_character(canvas, time)
        self.draw_subtitles(canvas, time)
        return canvas.convert("RGB")


def contact_sheet(frames: list[Image.Image], destination: Path, columns: int = 6) -> None:
    if not frames:
        return
    thumb_width = 320
    thumb_height = round(thumb_width * frames[0].height / frames[0].width)
    rows = math.ceil(len(frames) / columns)
    sheet = Image.new("RGB", (columns * thumb_width, rows * thumb_height), (247, 241, 227))
    for index, frame in enumerate(frames):
        thumb = frame.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        sheet.paste(thumb, ((index % columns) * thumb_width, (index // columns) * thumb_height))
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("frames_dir", type=Path)
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--limit-frames", type=int, help="Render only the first N frames for testing")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    renderer = Renderer(args.spec.resolve(), spec)
    if args.frames_dir.exists() and any(args.frames_dir.iterdir()):
        raise ValueError("Use an empty frames directory to avoid stale frames or overwriting approved work")
    if args.contact_sheet and args.contact_sheet.exists():
        raise ValueError("Contact sheet already exists; choose a fresh path")
    args.frames_dir.mkdir(parents=True, exist_ok=True)
    total = round(renderer.duration * renderer.fps)
    if args.limit_frames is not None:
        if args.limit_frames < 1:
            raise ValueError("limit-frames must be positive")
        total = min(total, args.limit_frames)

    raw_times = spec.get("contact_sheet_times", [])
    if not isinstance(raw_times, list) or any(not isinstance(value, (int, float)) for value in raw_times):
        raise ValueError("contact_sheet_times must be an array of numbers")
    sample_indices = {min(total - 1, max(0, round(float(value) * renderer.fps))) for value in raw_times}
    samples: dict[int, Image.Image] = {}

    for index in range(total):
        frame = renderer.render_frame(index / renderer.fps)
        frame.save(args.frames_dir / f"frame-{index:04d}.png", compress_level=2)
        if index in sample_indices:
            samples[index] = frame

    if args.contact_sheet:
        contact_sheet([samples[index] for index in sorted(samples)], args.contact_sheet)


if __name__ == "__main__":
    main()
