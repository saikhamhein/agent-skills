#!/usr/bin/env python3
"""Audit alpha margins; adapted from sunxiayi/image-motion-animation (MIT).

See ../references/provenance.md and ../references/upstream-license.txt.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_names(raw: str | None, count: int) -> list[str]:
    if raw is None:
        return [f"cell-{i + 1:02d}" for i in range(count)]
    names = [part.strip() for part in raw.split(",") if part.strip()]
    if len(names) != count:
        raise ValueError(f"Expected {count} names, got {len(names)}")
    return names


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("--columns", type=int, required=True)
    parser.add_argument("--rows", type=int, required=True)
    parser.add_argument("--names")
    parser.add_argument("--min-margin-ratio", type=float, default=0.08)
    parser.add_argument("--alpha-threshold", type=int, default=8)
    args = parser.parse_args()

    if args.columns < 1 or args.rows < 1:
        raise ValueError("columns and rows must be positive")
    if not 0 <= args.min_margin_ratio < 0.5:
        raise ValueError("min-margin-ratio must be in [0, 0.5)")
    if not 0 <= args.alpha_threshold <= 255:
        raise ValueError("alpha-threshold must be in [0, 255]")

    atlas = Image.open(args.atlas).convert("RGBA")
    if args.columns > atlas.width or args.rows > atlas.height:
        raise ValueError("Grid cannot have more cells than pixels")
    count = args.columns * args.rows
    names = parse_names(args.names, count)
    failures = []

    for index, name in enumerate(names):
        column, row = index % args.columns, index // args.columns
        left = round(column * atlas.width / args.columns)
        right = round((column + 1) * atlas.width / args.columns)
        top = round(row * atlas.height / args.rows)
        bottom = round((row + 1) * atlas.height / args.rows)
        cell = atlas.crop((left, top, right, bottom))
        binary = cell.getchannel("A").point(
            lambda value: 255 if value > args.alpha_threshold else 0
        )
        bounds = binary.getbbox()
        if bounds is None:
            failures.append(f"{name}: empty cell")
            continue

        x0, y0, x1, y1 = bounds
        required_x = round(cell.width * args.min_margin_ratio)
        required_y = round(cell.height * args.min_margin_ratio)
        margins = (x0, y0, cell.width - x1, cell.height - y1)
        passed = (
            margins[0] >= required_x
            and margins[2] >= required_x
            and margins[1] >= required_y
            and margins[3] >= required_y
        )
        status = "PASS" if passed else "FAIL"
        print(
            f"{status} {name}: margins L/T/R/B={margins}, "
            f"required>={required_x}px horizontal/{required_y}px vertical"
        )
        if not passed:
            failures.append(name)

    if failures:
        raise SystemExit(
            "Atlas safe-margin audit failed: " + ", ".join(failures)
        )


if __name__ == "__main__":
    main()
