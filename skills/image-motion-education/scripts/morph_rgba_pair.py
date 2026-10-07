#!/usr/bin/env python3
"""Facial in-betweens adapted from sunxiayi/image-motion-animation (MIT).

See references/provenance.md and references/upstream-license.txt. This helper
cannot determine whether anatomy, silhouette, or contact anchors are compatible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview a flow-safe pair of transparent character poses."
    )
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--frames", type=int, default=9, help="Output count including endpoints")
    parser.add_argument("--canvas-width", type=int, default=760)
    parser.add_argument("--canvas-height", type=int, default=760)
    parser.add_argument("--target-height", type=int, default=680)
    parser.add_argument("--bottom", type=int, default=742)
    return parser.parse_args()


def normalize(path: Path, width: int, height: int, target_height: int, bottom: int) -> np.ndarray:
    if min(width, height, target_height) <= 0 or not 0 < bottom <= height:
        raise ValueError("Canvas dimensions, target height and bottom anchor must be valid")
    source = Image.open(path).convert("RGBA")
    if source.getchannel("A").getbbox() is None:
        raise ValueError("A facial state cannot be fully transparent")
    target_width = round(source.width * target_height / source.height)
    sprite = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
    if target_width > width:
        scale = width / target_width
        target_width = width
        target_height = round(target_height * scale)
        sprite = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    left = round((width - sprite.width) / 2)
    top = round(bottom - sprite.height)
    if top < 0 or top + sprite.height > height:
        raise ValueError("Sprite does not fit the requested canvas/bottom anchor")
    canvas.alpha_composite(sprite, (left, top))
    return np.asarray(canvas).copy()


def flow_gray(rgba: np.ndarray) -> np.ndarray:
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    rgb = rgba[:, :, :3].astype(np.float32)
    composite = rgb * alpha + 232.0 * (1.0 - alpha)
    return cv2.cvtColor(composite.astype(np.uint8), cv2.COLOR_RGB2GRAY)


def estimate(first: np.ndarray, second: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    estimator = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    estimator.setFinestScale(1)
    return (
        estimator.calc(flow_gray(first), flow_gray(second), None),
        estimator.calc(flow_gray(second), flow_gray(first), None),
    )


def warp(source: np.ndarray, flow: np.ndarray, amount: float) -> np.ndarray:
    rows, columns = source.shape[:2]
    grid_x, grid_y = np.meshgrid(
        np.arange(columns, dtype=np.float32), np.arange(rows, dtype=np.float32)
    )
    return cv2.remap(
        source,
        grid_x - flow[:, :, 0] * amount,
        grid_y - flow[:, :, 1] * amount,
        cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )


def morph(
    first: np.ndarray,
    second: np.ndarray,
    forward: np.ndarray,
    backward: np.ndarray,
    progress: float,
) -> np.ndarray:
    if progress <= 0:
        return first
    if progress >= 1:
        return second
    # Premultiply before interpolation so hidden RGB outside the silhouette cannot
    # bleed into partially transparent fur or the white sticker edge.
    a = first.astype(np.float32) / 255.0
    b = second.astype(np.float32) / 255.0
    a[:, :, :3] *= a[:, :, 3:4]
    b[:, :, :3] *= b[:, :, 3:4]
    a = np.clip(warp(a, forward, progress), 0.0, 1.0)
    b = np.clip(warp(b, backward, 1.0 - progress), 0.0, 1.0)
    mixed = a * (1.0 - progress) + b * progress
    alpha = mixed[:, :, 3:4]
    mixed[:, :, :3] = np.divide(mixed[:, :, :3], np.maximum(alpha, 1e-6))
    return np.clip(mixed * 255.0, 0, 255).astype(np.uint8)


def main() -> None:
    args = parse_args()
    if args.frames < 2:
        raise SystemExit("--frames must be at least 2")
    if args.output_dir.exists() and (not args.output_dir.is_dir() or any(args.output_dir.iterdir())):
        raise SystemExit("Use a fresh or empty output directory; existing frames are preserved")
    with Image.open(args.first) as a, Image.open(args.second) as b:
        if a.size != b.size:
            raise SystemExit("Use matching source canvases and reviewed face/contact anchors")
    first = normalize(
        args.first, args.canvas_width, args.canvas_height, args.target_height, args.bottom
    )
    second = normalize(
        args.second, args.canvas_width, args.canvas_height, args.target_height, args.bottom
    )
    forward, backward = estimate(first, second)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for index in range(args.frames):
        progress = index / (args.frames - 1)
        frame = Image.fromarray(morph(first, second, forward, backward, progress))
        frame.save(args.output_dir / f"morph-{index:03d}.png")
    manifest = {
        "source": "sunxiayi/image-motion-animation@875a0d402e488a2df358b11fb3cccc3f050c5968 (MIT), adapted",
        "inputs": [{"path": str(p.resolve()), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                   for p in (args.first, args.second)],
        "frames_including_endpoints": args.frames,
        "canvas": [args.canvas_width, args.canvas_height],
        "target_height": args.target_height, "bottom": args.bottom,
        "versions": {"python": platform.python_version(), "opencv": cv2.__version__, "numpy": np.__version__, "pillow": Image.__version__},
        "algorithm": "DIS medium bidirectional flow; premultiplied RGBA warp and blend",
        "review": "Unreviewed output: inspect every in-between; this helper cannot validate compatibility",
    }
    (args.output_dir / "morph.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
