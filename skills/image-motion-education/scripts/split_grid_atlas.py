#!/usr/bin/env python3
"""Extract atlas cells; adapted from sunxiayi/image-motion-animation (MIT).

See ../references/provenance.md and ../references/upstream-license.txt.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_names(raw: str | None, count: int) -> list[str]:
    if raw is None:
        return [f"asset-{index + 1:02d}" for index in range(count)]
    names = [value.strip() for value in raw.split(",") if value.strip()]
    if len(names) != count:
        raise ValueError(f"Expected {count} comma-separated names, got {len(names)}")
    if len(set(names)) != len(names):
        raise ValueError("Asset names must be unique")
    if any(name in (".", "..") or "/" in name or "\\" in name for name in names):
        raise ValueError("Asset names must be plain filename stems")
    return names


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--columns", type=int, required=True)
    parser.add_argument("--rows", type=int, required=True)
    parser.add_argument("--names", help="Comma-separated output stems in row-major order")
    parser.add_argument("--margin", type=int, default=12)
    parser.add_argument("--keep-cell-size", action="store_true", help="Keep equal cell canvases for pose alignment")
    args = parser.parse_args()

    if args.columns < 1 or args.rows < 1:
        raise ValueError("columns and rows must be positive")
    if args.margin < 0:
        raise ValueError("margin must be nonnegative")

    image = Image.open(args.atlas).convert("RGBA")
    if args.columns > image.width or args.rows > image.height:
        raise ValueError("Grid cannot have more cells than pixels")
    if args.keep_cell_size and (image.width % args.columns or image.height % args.rows):
        raise ValueError("Equal canvases require dimensions divisible by the grid")
    count = args.columns * args.rows
    names = parse_names(args.names, count)
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise ValueError("Use an empty output directory")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for index, name in enumerate(names):
        column = index % args.columns
        row = index // args.columns
        left = round(column * image.width / args.columns)
        right = round((column + 1) * image.width / args.columns)
        top = round(row * image.height / args.rows)
        bottom = round((row + 1) * image.height / args.rows)
        cell = image.crop((left, top, right, bottom))
        bounds = cell.getchannel("A").getbbox()
        if bounds is None:
            raise RuntimeError(f"Cell {index + 1} ({name}) contains no visible pixels")

        inner_left, inner_top, inner_right, inner_bottom = bounds
        crop = (
            max(0, inner_left - args.margin),
            max(0, inner_top - args.margin),
            min(cell.width, inner_right + args.margin),
            min(cell.height, inner_bottom + args.margin),
        )
        (cell if args.keep_cell_size else cell.crop(crop)).save(args.output_dir / f"{name}.png")


if __name__ == "__main__":
    main()
